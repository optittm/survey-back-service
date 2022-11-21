from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Request, HTTPException

import domains.survey.formatter as mapper
from domains.survey import logic
from domains.survey.exceptions import ModelNotFound
from domains.survey.models import SurveyKeyTimestamp, SurveyCommentParameter, SurveyRuleApi, SurveyInApi, \
    SurveyCommentApi

router = APIRouter()


@router.post("", response_model=List[SurveyRuleApi])
async def create_survey_rules(request: Request, survey_api: SurveyInApi) -> List[SurveyRuleApi]:
    try:
        survey_rules = await logic.create_survey_rules(survey_api, request.app.engine)
        return [mapper.map_survey_rule_api_from_survey_rule(rule) for rule in survey_rules]
    except ModelNotFound as error:
        raise HTTPException(404) from error


@router.get("/rules", response_model=SurveyRuleApi)
async def get_survey_rule_from_feature(request: Request, feature_url: str) -> SurveyRuleApi:
    try:
        survey_rule = await logic.get_survey_rules(feature_url, request.app.engine)
        return mapper.map_survey_rule_api_from_survey_rule(survey_rule)
    except ModelNotFound as error:
        raise HTTPException(404) from error


@router.post("/comments", response_model=SurveyCommentApi)
async def add_survey_comments(request: Request,
                              survey_comment_api: SurveyCommentApi) -> SurveyCommentApi:
    try:
        comment = await logic.add_survey_comments(survey_comment_api, request.app.engine)
        return mapper.map_model_comment_api_from_survey_comment(comment)
    except ModelNotFound as error:
        raise HTTPException(404) from error


@router.get("/projects/{project_id}/comments", response_model=List[SurveyCommentApi])
async def get_comments(request: Request,
                       project_id: str,
                       language: Optional[str] = None,
                       feature_url: Optional[str] = None,
                       starting_date: Optional[datetime] = None,
                       ending_date: Optional[datetime] = None) -> List[SurveyCommentApi]:
    comments_filter_parameter = SurveyCommentParameter(
        language=language,
        feature_url=feature_url,
        project_id=project_id,
        starting_date=starting_date,
        ending_date=ending_date
    )
    comments = await logic.get_survey_comments(request.app.engine,
                                               comments_filter_parameter)

    result = [mapper.map_model_comment_api_from_survey_comment(c) for c in comments]

    return result


@router.get("/times", response_model=datetime)
async def get_last_time_user_answered(request: Request, user_id: str = None, feature_url: str = None) -> datetime:
    try:
        return await logic.get_last_time_user_answered(feature_url, user_id, request.app.engine)
    except ModelNotFound as error:
        raise HTTPException(404) from error


@router.post("/timestamps")
async def add_timestamp_key_encoded(request: Request, key: SurveyKeyTimestamp):
    await logic.add_timestamp_key_encoded(key, request.app.engine)


@router.get("/timestamps", response_model=str)
async def get_timestamp_key_encoded(request: Request) -> str:
    try:
        return await logic.get_timestamp_key_encoded(request.app.engine)
    except ModelNotFound as error:
        raise HTTPException(404) from error
