from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from odmantic import ObjectId

from domains.features.models import Feature, FeatureInApi
from domains.projects.models import Project

router = APIRouter()


@router.post("", response_model=List[Feature])
async def create_feature(features_request: List[FeatureInApi], request: Request):
    features = []
    for feature_req in features_request:
        project = await request.app.engine.find_one(Project, Project.id == ObjectId(feature_req.project_id))
        # Deal with the many to many relation between the feature and the requirements
        requirements = [ObjectId(req_id) for req_id in feature_req.requirement_ids]
        # Create the feature and link the projects and requirements
        feature = Feature(project=project,
                          synced=feature_req.synced,
                          name=feature_req.name,
                          description=feature_req.description,
                          resource=feature_req.resource,
                          payload=feature_req.payload,
                          requirement_ids=requirements)
        features.append(feature)
    await request.app.engine.save_all(features)
    return features


# TODO: PATCH verb

@router.get("", response_model=List[Feature])
async def get_features(request: Request, name: Optional[str] = None):
    query = ""
    if name:
        query = Feature.name == name
    return await request.app.engine.find(Feature, query)


@router.get("/count", response_model=int)
async def count_features(request: Request):
    count = await request.app.engine.count(Feature)
    return count


@router.get("/{id}", response_model=Feature)
async def get_feature_by_id(id: ObjectId, request: Request):
    feature = await request.app.engine.find_one(Feature, Feature.id == id)
    if feature is None:
        raise HTTPException(404)
    return feature


@router.delete("/{id}")
async def delete_feature_by_id(id: ObjectId, request: Request):
    feature = await request.app.engine.find_one(Feature, Feature.id == id)
    if feature is None:
        raise HTTPException(404)
    else:
        await request.app.engine.delete(feature)
        # Cascade delete related documents
        await request.app.mongodb_client.ottm.system.buckets.traffic.delete_many({"meta.feature": id})
        await request.app.mongodb_client.ottm.system.buckets.latency.delete_many({"meta.feature": id})


@router.get("/project/{id}", response_model=List[Feature])
async def get_project_features(request: Request, id: ObjectId):
    features = await request.app.engine.find(Feature, Feature.project == id)
    return features
