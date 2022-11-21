import uuid
from datetime import datetime
from typing import List
from langdetect import detect, LangDetectException, DetectorFactory
from odmantic import ObjectId
from domains.features.models import Feature
from domains.survey.exceptions import ModelNotFound
from domains.survey.models import SurveyInApi, Survey, SurveyRule, SurveyCommentApi, SurveyComment, \
    SurveyKeyTimestamp, SurveyCommentParameter
from domains.projects.models import Project

import domains.survey.formatter as mapper

DetectorFactory.seed = 0


def _detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return 'unknown'


async def _create_survey(survey: SurveyInApi, project: Project, engine) -> Survey:
    survey = mapper.map_survey_from_api_survey(survey, project)
    await engine.save(survey)
    return survey


async def _get_comments_from_feature(engine,
                                     feature: Feature,
                                     parameter: SurveyCommentParameter) -> List[SurveyComment]:
    query = SurveyComment.feature == feature.id
    if parameter.starting_date is not None:
        query = query & SurveyComment.date.gte(parameter.starting_date)
    if parameter.ending_date is not None:
        query = query & SurveyComment.date.lte(parameter.ending_date)
    if parameter.language is not None:
        query = query & (SurveyComment.language == parameter.language)

    comments = await engine.find(SurveyComment, query)

    return comments


async def _create_survey_rules(survey: Survey,
                               survey_api: SurveyInApi,
                               engine) -> List[SurveyRule]:
    survey_rules = []
    for feature_rule in survey_api.feature_rules:
        feature = await engine.find_one(Feature, Feature.resource == feature_rule.url)
        if feature is None:
            raise ModelNotFound

        survey_rule = SurveyRule(survey=survey,
                                 feature=feature,
                                 ratio=feature_rule.ratio,
                                 delay_to_answer=survey_api.delay_to_answer,
                                 delay_before_reanswer=feature_rule.delay_before_new_proposition,
                                 is_activated=True)
        survey_rules.append(survey_rule)
    await engine.save_all(survey_rules)
    return survey_rules


async def create_survey_rules(survey_api: SurveyInApi, engine) -> List[SurveyRule]:
    project = await engine.find_one(Project, Project.id == ObjectId(survey_api.project_id))
    if project is None:
        raise ModelNotFound
    survey = await _create_survey(survey_api, project, engine)
    return await _create_survey_rules(survey, survey_api, engine)


async def get_survey_rules(feature_url: str, engine) -> SurveyRule:
    feature = await engine.find_one(Feature, Feature.resource == feature_url)
    if feature is None:
        raise ModelNotFound
    survey_rule = await engine.find_one(SurveyRule, SurveyRule.feature == feature.id)
    if survey_rule is None:
        raise ModelNotFound
    return survey_rule


async def add_survey_comments(survey_comment_api: SurveyCommentApi, engine) -> SurveyComment:
    feature = await engine.find_one(Feature,
                                    Feature.resource == survey_comment_api.feature_url)
    if feature is None:
        raise ModelNotFound
    comment = mapper.map_survey_comment_from_survey_comment_api(survey_comment_api, feature)
    comment.language = _detect_language(survey_comment_api.description)
    await engine.save(comment)
    return comment


async def get_survey_comments(engine,
                              parameter: SurveyCommentParameter) -> List[SurveyComment]:
    comments = []
    if parameter.feature_url is not None:
        feature = await engine.find_one(Feature,
                                        Feature.resource == parameter.feature_url)
        comments = await _get_comments_from_feature(engine,
                                                    feature,
                                                    parameter)

    elif parameter.project_id is not None:
        features = await engine.find(Feature,
                                     Feature.project == ObjectId(parameter.project_id))

        for feature in features:
            result = await _get_comments_from_feature(engine,
                                                      feature,
                                                      parameter)
            comments = comments + result
    return comments


async def get_last_time_user_answered(feature_url: str, user_id: str, engine) -> datetime:
    feature = await engine.find_one(Feature, Feature.resource == feature_url)
    if feature is None:
        raise ModelNotFound
    comment_list = await engine.find(SurveyComment, SurveyComment.feature == feature.id,
                                     SurveyComment.user_id == uuid.UUID(user_id),
                                     sort=SurveyComment.date.desc())
    if comment_list is None or not comment_list:
        raise ModelNotFound
    return comment_list[0].date


async def add_timestamp_key_encoded(key: SurveyKeyTimestamp, engine):
    await engine.save(key)


async def get_timestamp_key_encoded(engine) -> str:
    timestamp_key_model = await engine.find_one(SurveyKeyTimestamp)
    if timestamp_key_model is None:
        raise ModelNotFound
    return timestamp_key_model.key
