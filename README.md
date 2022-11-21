# OTTM API server

OTTM API server is a FastAPI/Python REST Server allowing to store and get metrics and basic information from a MongoDB database.
## Usage
Prior starting the server, you must have a mongoDB server instance running or launched from a container:

    docker run -d -p 27017-27019:27017-27019 -v /mongodb/data/db:/data/db --name mongodb mongo:latest

Install dependencies listed int requirements.txt

    python -m pip install -r requirements.txt

Change the content of the .env file or set the environement variable according to your configuration.

    cp .env-example .env

Launch the server:

    python main.py

See full API documentation (swagger) here: http://localhost:8000/docs

## prepare survey settings

Create a new project :

    POST /projects

[
  {
    "name": "string",
    "description": "string",
    "config": "string",
    "synced": "2022-11-21T18:02:40.203389",
    "is_active": true,
    "payload": {},
    "id": "5f85f36d6dfecacc68428a46"
  }
]

Create a feature for the project :

    POST /features

[
  {
    "project_id": "5f85f36d6dfecacc68428a46",
    "name": "string",
    "description": "string",
    "resource": "http://my_url",
    "synced": "2022-11-21T18:06:22.958010",
    "payload": {},
    "requirement_ids": [],
    "id": "5f85f36d6dfecacc68428a46"
  }
]    

Create a survey for the project and urls

    POST /survey

{
  "project_id": "5f85f36d6dfecacc68428a46",
  "feature_rules": [
    {
      "url": "http://my_url",
      "ratio": 0,
      "delay_before_new_proposition": 0
    }
  ],
  "is_activated": true,
  "delay_to_answer": 0
}


Create a new survey in database :

