from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from odmantic import ObjectId

from domains.projects.models import Project, ProjectInApi

router = APIRouter()


@router.post("", response_model=List[Project])
async def create_projects(projects_request: List[Project], request: Request) -> List[Project]:
    await request.app.engine.save_all(projects_request)
    return projects_request


@router.patch("/{id}", response_model=Project)
async def update_project_by_id(id: ObjectId, patch: ProjectInApi, request: Request) -> Project:
    project = await request.app.engine.find_one(Project, Project.id == id)
    if project is None:
        raise HTTPException(404)
    patch_dict = patch.dict(exclude_unset=True)
    patch_dict.pop('id', None)  # Don't reassign the PK
    for name, value in patch_dict.items():
        setattr(project, name, value)
    await request.app.engine.save(project)
    return project


@router.get("", response_model=List[Project])
async def get_projects(request: Request, fulltext: Optional[str] = None, name: Optional[str] = None) -> List[Project]:
    if fulltext is not None:
        # Note that the fulltext index is created in main.py
        projects = await request.app.engine.find(Project, {"$text": {"$search": fulltext}})
        return projects
    elif name is not None:
        projects = await request.app.engine.find(Project, Project.name.match(name), sort=Project.name)
        return projects
    else:
        projects = await request.app.engine.find(Project, sort=Project.name)
        return projects


@router.get("/count", response_model=int)
async def count_projects(request: Request) -> int:
    count = await request.app.engine.count(Project)
    return count


@router.get("/{id}", response_model=Project)
async def get_project_by_id(id: ObjectId, request: Request) -> Project:
    project = await request.app.engine.find_one(Project, Project.id == id)
    if project is None:
        raise HTTPException(404)
    return project


@router.delete("/{id}")
async def delete_project_by_id(id: ObjectId, request: Request) -> None:
    project = await request.app.engine.find_one(Project, Project.id == id)
    if project is None:
        raise HTTPException(404)
    else:
        await request.app.engine.delete(project)
        # Cascade delete related documents
        await request.app.mongodb_client.ottm.build.delete_many({"project": id})
        await request.app.mongodb_client.ottm.code_quality.delete_many({"project": id})
        await request.app.mongodb_client.ottm.issue.delete_many({"project": id})
        await request.app.mongodb_client.ottm.issue_revision.delete_many({"project": id})
        await request.app.mongodb_client.ottm.tool.delete_many({"project": id})
        await request.app.mongodb_client.ottm.system.buckets.traffic.delete_many({"meta.project": id})
        await request.app.mongodb_client.ottm.system.buckets.latency.delete_many({"meta.project": id})
        await request.app.mongodb_client.ottm.system.buckets.commit.delete_many({"meta.project": id})
        await request.app.mongodb_client.ottm.system.buckets.exception.delete_many({"meta.project": id})
        await request.app.mongodb_client.ottm.feature.delete_many({"project": id})
        await request.app.mongodb_client.ottm.requirement.delete_many({"project": id})
        await request.app.mongodb_client.ottm.version.delete_many({"project": id})
        await request.app.mongodb_client.ottm.resource.delete_many({"project": id})
        await request.app.mongodb_client.ottm.activity.delete_many({"project": id})
        await request.app.mongodb_client.ottm.timesheet.delete_many({"project": id})
        await request.app.mongodb_client.ottm.component.delete_many({"project": id})
