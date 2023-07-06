# Location Decisions Back-end challenge

## Description
Import and transform supplied ABS Census data into a database and serve through a Web API.



## CSV data download
- ABS Australia Population - SA4, Sex, Age for Census Years 2011 and 2016: [download](https://github.com/dotidconsulting/coding-challenge-location-decisions/tree/main/back-end/ABS_C16_T01_TS_SA_08062021164508583.xls)



## Tools to use
- For data import, C# or Python, MS SQL Server
- For API, C# ASP.NET Web API
- (Optional) Enable swagger



## Download this csv file and import its contents into a database (Feel free to use Python for this task)
- The CSV file contains population by Statistical Area Level 4 (SA4), Sex, Single year of age and Census Year in Australia
- Write a program to import and normalise the data into a MS SQL Database
- This program should be able to run for future Census data (append)
- Write a stored procedure or view that groups the data in 5 year age groups, ex 0-4 year old, 5-9 year old etc.

### TIP: DB Tables could be as follows (but structure the DB as you think best):
- DimRegion (Dimension Table)
- DimSex (Dimension Table)
- DimAge (Dimension Table)
- FactPopulation (Fact Table)



## Write a Web API project to serve the above population data with the following end points
- /api/age-structure/{SA4 Code}/{Sex}, for example /api/age-structure/102/1 should return all ages for males in Central Coast
- /api/age-structure-diff/{SA4 Code}/{Sex}/{Year1}/{Year2}, for example /api/age-structure-diff/102/1/2011/2016 should return the difference in age between 2016 and 2011 Census Years
- Try to also support passing a STATE CODE instead of a SA4 Code for the above end points. This should aggreate the SA4s ex. /api/age-structure/1/1 (This will summarise all SA4s in NSW)



## Acceptance criteria
- Try to utilise SOLID principles where it makes sense
- All API end points should return JSON format
- The following properties should be included in the JSON object:
  - Region Code (ex. SA4 code or STATE code)
  - Region name
  - Age
  - Sex (ex. Males/Females/Persons)
  - Population
- Write at least one test to verify valid response from one of the end points
  
Here is a sample of the JSON result: https://gist.github.com/Zir01/5107362ae7ea2b1290ff184cee935faa#file-pop_data

Here is a sample of the "DIFF" JSON result: https://gist.github.com/Zir01/97757f3ce41bf438f09c6fdab328d1c5#file-pop_data_diff



## Others
No need to implement the following, but think of ways to explain how to implement. We will cover it during the tech interview

- Think of ways you can secure the API using best practices. Think multi-tenant security. Ex. Role based security.
- Think of ways to setup a CI/CD pipelines
- What stradegies would you use to extend functionality within the API without breaking existing clients using the API?



## Submission
Please send us a link to your GitHub repo.

## Next steps
Once this is completed, we will invite you to meet the team to review and discuss your work, implementation and any code design architecture.

## Questions?
Please contact us here: bruce@id.com.au to ask any questions about the challenge.


