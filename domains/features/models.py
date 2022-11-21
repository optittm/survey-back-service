from typing import List, Optional, Any, Dict
from datetime import datetime

from odmantic import Model, ObjectId, Reference

from domains.projects.models import Project


class FeatureInApi(Model):
    """
    This class is only used for modeling the API input
    Which is a textual representation of the actual data
    (most of the time JSON-based).
    """
    project_id: str
    name: str
    description: Optional[str]
    resource: Optional[str]
    synced: Optional[datetime]
    payload: Optional[Dict[Any, Any]]
    requirement_ids: List[ObjectId] = []


class Feature(Model):
    """
    This class is a model of an application feature.
    An example of feature is a web page of a larger application.
    One feature can implement several requirements.
    One requirement is implemented by one or more features.
    TODO: eventually links between components and features.

    Attributes:
    -----------
        project:             Project (the application that contains many features)  
        name:                Name of the feature
        description:         Description of the feature
        resource:            An example of resource is the URL of the feature
        synced:              If the feature was imported from a 3rd party tool, last time of synced
        payload:             Raw import from the 3rd tool
        requirement_ids:     List of requirements that the feature implements partly or fully
    """
    project: Project = Reference()
    name: str
    description: Optional[str]
    resource: Optional[str]
    synced: Optional[datetime]
    payload: Optional[Dict[Any, Any]]
    requirement_ids: List[ObjectId] = []
