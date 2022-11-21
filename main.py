import os
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from starlette_exporter import PrometheusMiddleware, handle_metrics

import domains.projects.routes as projects_routes
import domains.survey.routes as surveys_routes
import domains.features.routes as features_routes

from schema import schema

load_dotenv()

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", False),
    allow_methods=os.getenv("CORS_ALLOW_METHODS", "*").split(","),
    allow_headers=os.getenv("CORS_ALLOW_HEADERS", "*").split(","),
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.getenv("DB_URL"))
    # app.mongodb = app.mongodb_client[os.getenv("DB_NAME")]
    app.engine = AIOEngine(motor_client=app.mongodb_client, database=os.getenv("DB_NAME"))
    # Recreate timeseries collections and indexes
    await schema.setup(app.mongodb_client, app.engine)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(projects_routes.router, prefix="/projects", tags=["projects"])
app.include_router(surveys_routes.router, prefix="/survey", tags=["survey"])
app.include_router(features_routes.router, prefix="/features", tags=["features"])


# Start the async event loop and ASGI server.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST"),
        reload=os.getenv("DEBUG_MODE"),
        port=int(os.getenv("PORT")),
    )
