import pytest
from databases import Database
from fastapi.testclient import TestClient
from pytest import fixture

from apis import app, metadata

@fixture(scope='module')
def event_loop():
   import asyncio
   loop = asyncio.get_event_loop()
   yield loop
   loop.close()

@fixture(scope='module')
async def db():
   db = Database("postgresql://postgres:postgres@localhost/POC")
   await db.connect()

   metadata.create_all(bind=db)
   yield db

   metadata.drop_all(bind=db)
   await db.disconnect()

@pytest.fixture(scope='module')
def client(db):
   with TestClient(app) as client:
       yield client

def test_age_structure(client):
   # Check status code when correct details are passed
   response = client.get("/api/age-structure/102/1")
   assert response.status_code == 200
   
   # Check response when invalid Sex value was passed
   response = client.get("/api/age-structure/102/4")
   assert response.json() == {"detail": "Invalid sex value"}

def test_age_structure_diff(client):
   # Check status code when correct details are passed
   response = client.get("/api/age-structure-diff/102/1/2011/2016")
   assert response.status_code == 200
   
   # Check response when invalid year value was passed
   response = client.get("/api/age-structure-diff/102/1/2011/2020")
   assert response.json() == {"detail": "Invalid Census_Year value"}
