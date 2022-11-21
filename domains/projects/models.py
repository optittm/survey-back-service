from typing import Optional, Any, Dict
from datetime import datetime

from odmantic import Model


class Project(Model):
    """
    This class is a model of a project.
    Not to be confused with a github/gitlab project.
    A project can contain many components.
    a component can be a standalone application or a code dependency 
    see :py:class:`domains.components.Component`

    Attributes:
    -----------
        name:                Name of the project
        description:         Description of the project
        config:              JSON based description of how various tools of the project are used
        synced:              If the project was imported from a 3rd party tool, last time of synced
        is_active:           Boolean indicating if the project is active
        payload:             Raw import from the 3rd tool

    """
    name: str
    description: Optional[str]
    config: Optional[Any]
    synced: Optional[datetime]
    is_active: bool = True
    payload: Optional[Dict[Any, Any]]


class ProjectInApi(Model):
    """
    This class is only used for modeling the API input
    which is a textual representation of the actual data
    (most of the time JSON-based).
    see :py:class:`~domains.projects.Project`
    """
    name: Optional[str]
    description: Optional[str]
    config: Optional[Any]
    synced: Optional[datetime]
    is_active: Optional[bool]
    payload: Optional[Dict[Any, Any]]
