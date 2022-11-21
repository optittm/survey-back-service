from datetime import datetime
from typing import List, Optional
from uuid import UUID
from odmantic import Reference, Model
from pydantic import BaseModel

from domains.features.models import Feature
from domains.projects.models import Project


class FeatureRuleApi(BaseModel):
    """
    This class is only used for modeling the API input
    which is a textual representation of the actual data
    (most of the time JSON-based in python convention).
    """
    url: str
    ratio: int
    delay_before_new_proposition: int


class SurveyInApi(BaseModel):
    """
    This class is only used for modeling the API input
    which is a textual representation of the actual data
    (most of the time JSON-based in python convention).
    see :py:class:`~domains.survey.Survey`
    """
    project_id: str
    feature_rules: Optional[List[FeatureRuleApi]]
    is_activated: bool
    delay_to_answer: int


class Survey(Model):
    """
    This class is a model for a survey configuration.
    The survey configuration is used by the user feedback component.
    feedback component can be activated or not on the monitoring project by
    OTTM
    Attributes:
    -----------
        project:           Project (the application that contains many features)
        is_activated:      The userfeedback is applied or not for the project
    """
    project: Project = Reference()
    is_activated: bool


class SurveyRuleApi(BaseModel):
    """
    This class is only used for modeling the request input
    which is a textual representation of the actual data
    (most of the time JSON-based) in python convention.
    see :py:class:`~domains.survey.SurveyRule`
    """
    is_activated: bool
    is_activated_on_feature: bool
    delay_before_reanswer: int
    delay_to_answer: int
    ratio_display: int


class SurveyRule(Model):
    """
    This class is a model for a survey on a feature
    Each feature has its own apparition rules

    Attributes:
    -----------
        survey:                     Survey (Linked to the project)
        feature:                    Feature (One on the feature linked to the project)
        ratio:                      percentage of occurrence for the survey
        delay_to_answer:            Time in ms for the user to respond on the survey
        delay_before_reanswer:      Delay in month before a user can be eligible for user feedback
        is_activated:               Is the survey is activated on this feature

    """
    survey: Survey = Reference()
    feature: Feature = Reference()
    ratio: Optional[int]
    delay_to_answer: Optional[int]
    delay_before_reanswer: Optional[int]
    is_activated: bool


class SurveyCommentApi(BaseModel):
    """
    This class is only used for modeling the API input
    which is a textual representation of the actual data
    (most of the time JSON-based in python convention).
    see :py:class:`~domains.survey.SurveyComment`
    """
    feature_url: Optional[str]
    user_id: Optional[str]
    date: Optional[str]
    rating: Optional[str]
    description: Optional[str]
    language: Optional[str]


class SurveyCommentParameter(BaseModel):
    """
    This class is only used to encapsulate the different
    parameters for filtering the comments.
    """
    language: Optional[str] = None,
    feature_url: Optional[str] = None,
    project_id: Optional[str] = None,
    starting_date: Optional[datetime] = None,
    ending_date: Optional[datetime] = None


class SurveyComment(Model):
    """
    This class is a model for a user feedback.
    We store the comment and the rating given by the user, and the date.

    Attributes:
    -----------
        feature:          Feature (Feature linked to the project where the feedback is given)
        user_id:          Id of the user sending the feedback
        date:             Date when the feedback is given
        rating:           Rating (between 1 and 5)
        description:      Comment given by the user
        language:         comment's language

    """
    feature: Feature = Reference()
    user_id: UUID
    date: datetime
    rating: int
    description: Optional[str]
    language: Optional[str]


class SurveyKeyTimestamp(Model):
    """
    This class is a model for the encryption/decryption key
    used to encrypt/decrypt timestamp send to the user.
    Only one key can be stored in the BDD at the same time.
    Attributes:
    -----------
        key:      Timestamp's key for encryption/decryption. It is encoded (Base64).
        
    """
    key: str
