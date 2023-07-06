# Coding challenge for Team Location Decisions

Hi and thank you for taking the time to take this coding challenge!

There are 2 parts to this challenge.

1. [Front-end](https://github.com/dotidconsulting/coding-challenge-location-decisions/tree/main/front-end)
2. [Back-end](https://github.com/dotidconsulting/coding-challenge-location-decisions/tree/main/back-end)
 
The read me files are in each folder with instructions.


# Instructions to run the project code

backe-end:
**********

Python Version used: 3.10

Setup Virtual Environment: python -m -m venv venv

Activate Virtual Environment: venv\scripts\activate

Install dependencies:  pip install -r requirements.txt

    Load data into DB tables
    ************************

    Run loader.py

    This code expects the PostgreSQL DB is up and running in local.

    DB connection details: {
        host: localhost

        port: 5432

        DB name: POC

        user: postgres

        password: postgres
    }

    API Server
    **********
    Framework used FastAPI

    Run apis.py

    Navigate to localhost:8000/docs in your browser. This opens swaggerUI for the API endpoints

    Tests
    *****

    Run pytest from venv

    This picks all the test cases inside the project directory


front-end:
**********

NodeJS version used 17.6.0

Libraries used ReactJS and leaflet

Navigate to demo-app directory

Install dependencies - npm install

Run Web App - npm run

A new browser window opens with the reactJS application running.


