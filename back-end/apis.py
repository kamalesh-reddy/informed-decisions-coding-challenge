from fastapi import FastAPI, HTTPException
import databases
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select, join, func, case
from fastapi.responses import JSONResponse

app = FastAPI()
db = databases.Database("postgresql://postgres:postgres@localhost/POC")
metadata = MetaData()
engine = create_engine("postgresql://postgres:postgres@localhost/POC")
metadata.create_all(bind=engine)

sexData = Table('dimsex', metadata, autoload=True, autoload_with=engine)
regionData = Table('dimregion', metadata, autoload=True, autoload_with=engine)
stateData = Table('dimstate', metadata, autoload=True, autoload_with=engine)
censusData = Table('factpopulation', metadata, autoload=True, autoload_with=engine)

async def check_inputs_present(sa4_codes, sex, year1=None, year2=None):
    # Check if Region/State value exists in data

    state_query = select(stateData.c.state_id).where(stateData.c.state_id == sa4_codes[0])
    state_result = await db.fetch_one(state_query)

    if state_result:
        state_region_query = select(regionData.c.asgs_2016).where(regionData.c.state_id == sa4_codes[0])
        state_region_result = await db.fetch_all(state_region_query)
        sa4_codes = [sa4_code[0] for sa4_code in state_region_result]
        region_result = None
    else:
        region_query = select(regionData.c.asgs_2016).where(regionData.c.asgs_2016 == sa4_codes[0])
        region_result = await db.fetch_one(region_query)
    
    # Check if Sex value exists in data
    sex_query = select(sexData.c.sex_abs).where(sexData.c.sex_abs == sex)
    sex_result = await db.fetch_one(sex_query)

    if year1:
        year1_query = select(censusData.c.census_year).where(censusData.c.census_year == year1)
        year1_result = await db.fetch_one(year1_query)
    else:
        year1_result = None

    if year2:
        year2_query = select(censusData.c.census_year).where(censusData.c.census_year == year2)
        year2_result = await db.fetch_one(year2_query)
    else:
        year2_result = None

    return sa4_codes, sex_result, state_result, region_result, year1_result, year2_result

@app.get("/api/age-structure/{sa4_code}/{sex}")
async def get_age_structure(sa4_code: int, sex: int):
    sa4_codes = [sa4_code]
    
    # Check if the query paramteres are valid
    sa4_codes, sex_result, state_result, region_result, _, _ = await check_inputs_present(sa4_codes, sex)

    if not (state_result or region_result):
         raise HTTPException(status_code=404, detail="Invalid State/SA4_code")
    
    if not sex_result:
        raise HTTPException(status_code=404, detail="Invalid sex value")
    
    final_response = []
    
    for sa4_code in sa4_codes:
        census_query = select(
                    [
                        regionData.c.asgs_2016, regionData.c.region, censusData.c.age, sexData.c.sex, censusData.c.census_year, censusData.c.value
                    ]
                ).select_from(
                    join(
                        join(
                            regionData, censusData, regionData.c.asgs_2016 == censusData.c.asgs_2016
                        ), sexData, sexData.c.sex_abs == censusData.c.sex_abs
                    )
                ).where(
                    (regionData.c.asgs_2016 == sa4_code) & (sexData.c.sex_abs == sex)
                )

        results = await db.fetch_all(census_query)
        
        response_data = {
            "regionCode": results[0][0],
            "regionName": results[0][1],
            "data": [
                {
                "age": str(row[2]) + " year old",
                "sex": row[3],
                "censusYear": row[4],
                "population": row[5]  
                } for row in results]
        }
        
        final_response.append(response_data)
    
    return JSONResponse(content=final_response)

@app.get("/api/age-structure-diff/{sa4_code}/{sex}/{year1}/{year2}")
async def get_age_structure_diff(sa4_code: int, sex: int, year1: int, year2: int):
    sa4_codes = [sa4_code]
    # Check if the query paramteres are valid
    sa4_codes, sex_result, state_result, region_result, year1_result, year2_result = await check_inputs_present(sa4_codes, sex, year1, year2)

    if not (state_result or region_result):
        raise HTTPException(status_code=404, detail="Invalid State/SA4_code")
    
    if not sex_result:
        raise HTTPException(status_code=404, detail="Invalid Sex value")

    if not (year1_result and year2_result):
        raise HTTPException(status_code=404, detail="Invalid Census_Year value")
    
    final_response = []

    for sa4_code in sa4_codes:
        diff_census_query = select(
                [
                    regionData.c.asgs_2016, regionData.c.region, censusData.c.age, sexData.c.sex,
                    (
                        func.sum(case([(censusData.c.census_year == year2, censusData.c.value)], else_=0)) -
                        func.sum(case([(censusData.c.census_year == year1, censusData.c.value)], else_=0))
                    ).label('value_difference')
                ]
            ).select_from(
                join(
                    join(
                        regionData, censusData, regionData.c.asgs_2016 == censusData.c.asgs_2016
                    ), sexData, sexData.c.sex_abs == censusData.c.sex_abs
                )
            ).where(
                (regionData.c.asgs_2016 == sa4_code) & (sexData.c.sex_abs == sex)
            ).group_by(
                sexData.c.sex_abs,
                censusData.c.age,
                regionData.c.asgs_2016
            ).order_by(
                regionData.c.asgs_2016,
                censusData.c.age,
                sexData.c.sex_abs
            )

        results = await db.fetch_all(diff_census_query)
        
        response_data = {
            "regionCode": results[0][0],
            "regionName": results[0][1],
            "data": [
                {
                "age": str(row[2]) + " year old",
                "sex": row[3],
                "censusYear": f"{year1} - {year2}",
                "population": row[4]  
                } for row in results]
        }
        
        final_response.append(response_data)
    
    return JSONResponse(content=final_response)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",  port=8000)