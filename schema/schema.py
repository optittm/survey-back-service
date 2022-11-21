import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from domains.projects.models import Project

async def setup(client, engine):
    '''
    Define native collections for timeseries
    And extra indexes

    Parameters
    ----------
    engine : AIOEngine
        Async IO Pymongo engine
    client : AsyncIOMotorClient
        Async IO Pymongo client
    '''
    # TODO : ODMantic project plan to add a feature allowing to specify it in the Model
    # Ensure we have a fulltext index so as to search through title and description fields
    motor_collection = engine.get_collection(Project)
    index_info = await motor_collection.index_information()
    if len(index_info) < 2:
        await motor_collection.create_index([("name", pymongo.TEXT), ("description", pymongo.TEXT)], name="idxProjectFullText", background=True)

    db = client.get_database()
    collections = await db.list_collection_names()

    # Traffic (number of hits) timeseries collection, metadata :
    #  - Project ID
    #  - Feature ID
    if "traffic" not in collections:
        await db.create_collection("traffic", timeseries = {
                    "timeField": "timestamp",
                    "metaField": "metadata"
        })

    # Latency (Response time in milliseconds) timeseries collection, metadata :
    #  - Project ID
    #  - Feature ID
    if "latency" not in collections:
        await db.create_collection("latency", timeseries = {
                    "timeField": "timestamp",
                    "metaField": "metadata"
        })

    # Availability (Boolean: is the feature available) timeseries collection, metadata :
    #  - Project ID
    #  - Feature ID
    if "availability" not in collections:
        await db.create_collection("availability", timeseries = {
                    "timeField": "timestamp",
                    "metaField": "metadata"
        })

    # Commit (number of modified lines of code) timeseries collection, metadata :
    #  - Project ID
    #  - Component ID
    #  - Contributor
    if "commit" not in collections:
        await db.create_collection("commit", timeseries = {
                    "timeField": "timestamp",
                    "metaField": "metadata"
        })

    # Exception (number of exceptions/errors raised in logs) timeseries collection, metadata :
    #  - Project ID
    #  - Component ID
    #  - Source (optional, e.g. micro-service)
    if "exception" not in collections:
        await db.create_collection("exception", timeseries = {
                    "timeField": "timestamp",
                    "metaField": "metadata"
        })
