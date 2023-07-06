import pandas as pd
import psycopg2


def transformations(census_df):
    # Get distict Sex details
    sex_df = census_df[["SEX_ABS", "Sex"]].drop_duplicates(subset=["SEX_ABS", "Sex"])

    # Get distinct region details
    region_df = census_df[["ASGS_2016", "Region", "STATE"]].drop_duplicates(subset=["ASGS_2016", "Region"])

    # Get distinct state details
    state_df = census_df[["STATE", "State"]].drop_duplicates(subset=["STATE", "State"])
    state_df = state_df.rename(columns={"STATE": "STATE_ID"})

    # Remove cumilative age-cesnsus data for each region
    census_df = census_df.drop(census_df[census_df["AGE"] == "TT"].index)

    # Drop unneccessary columns from census data
    census_df = census_df[["SEX_ABS", "AGE", "ASGS_2016", "Census year", "Value"]]
    census_df = census_df.rename(columns={"Census year": "Census_year"})

    return sex_df, region_df, state_df, census_df

def get_db_connection():
    con = psycopg2.connect(dbname= "POC", host="localhost", port=5432, user="postgres", password="postgres")
    con.autocommit = True
    cur = con.cursor()
    return cur

def create_tables(cur):
    try:
        print("Creating tables if not exists")
        cur.execute("CREATE TABLE IF NOT EXISTS DimSex (SEX_ABS INT PRIMARY KEY, Sex TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS DimState (STATE_ID INT PRIMARY KEY, State Text)")
        cur.execute("CREATE TABLE IF NOT EXISTS DimRegion (ASGS_2016 INT PRIMARY KEY, Region Text, STATE_ID INT, FOREIGN KEY (STATE_ID) REFERENCES DimState(STATE_ID))")
        cur.execute("CREATE TABLE IF NOT EXISTS FactPopulation (SEX_ABS INT, AGE INT, ASGS_2016 INT, Census_year INT, Value INT, FOREIGN KEY (SEX_ABS) REFERENCES DimSex(SEX_ABS), FOREIGN KEY (ASGS_2016) REFERENCES DimRegion(ASGS_2016), UNIQUE (SEX_ABS, AGE, ASGS_2016, Census_year))")
        
        return True
    except Exception as e:
        print("Table creation failed with error :", e)
        return False

def insert_into_tables(cur):
    try:
        print("Inserting data into tables")
        insert_sex = "INSERT INTO DimSex (SEX_ABS, Sex) VALUES (%s, %s) ON CONFLICT (SEX_ABS) DO NOTHING"
        sexData = sex_df.itertuples(index=False, name=None)
        cur.executemany(insert_sex, sexData)

        insert_state = "INSERT INTO DimState (STATE_ID, State) VALUES (%s, %s) ON CONFLICT (STATE_ID) DO NOTHING"
        stateData = state_df.itertuples(index=False, name=None)
        cur.executemany(insert_state, stateData)

        insert_region = "INSERT INTO DimRegion (ASGS_2016, Region, STATE_ID) VALUES (%s, %s, %s) ON CONFLICT (ASGS_2016) DO NOTHING"
        regionData = region_df.itertuples(index=False, name=None)
        cur.executemany(insert_region, regionData)

        insert_census = "INSERT INTO FactPopulation (SEX_ABS, AGE, ASGS_2016, Census_year, Value) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (SEX_ABS, AGE, ASGS_2016, Census_year) DO UPDATE SET Value = EXCLUDED.Value"
        censusData = census_df.itertuples(index=False, name=None)
        cur.executemany(insert_census, censusData)

        return True
    except Exception as e:
        print("Inserting data into tables failed with error", e)
        return False

if __name__ == '__main__':
    # Read and import source data file
    print("Importinf source data")
    source_df = pd.read_csv('back-end\data\ABS_C16_T01_TS_SA_08062021164508583.xls')

    # Transform data to required formats
    print("Performing transformations")
    sex_df, region_df, state_df, census_df = transformations(source_df)

    # Get the DB connection
    print("Connecting to the DB")
    cur = get_db_connection()

    # Check and create neccessary tables
    tables_created = create_tables(cur)

    # Insert data into tables
    if tables_created:
        inserted = insert_into_tables(cur)
        if inserted:
            print("Data has been loaded to tables successfully")
        else:
            print("Data load has failed")