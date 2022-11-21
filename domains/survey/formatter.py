from domains.features.models import Feature
from domains.survey.models import Survey, SurveyInApi, SurveyRule, SurveyRuleApi, SurveyComment, \
    SurveyCommentApi
from domains.projects.models import Project


def map_survey_from_api_survey(api_survey: SurveyInApi, project: Project) -> Survey:
    return Survey(project=project,
                  is_activated=api_survey.is_activated)


def map_survey_rule_out_api_from_survey(survey_rule: SurveyRule) -> SurveyRuleApi:
    return SurveyRuleApi(
        isActivated=survey_rule.is_activated,
        isActivatedOnFeature=survey_rule.is_activated,
        delayBeforeReAnswer=survey_rule.delay_before_reanswer,
        delayToAnswer=survey_rule.delay_to_answer,
        ratioDisplay=survey_rule.ratio
    )


def map_survey_comment_from_survey_comment_api(survey_comment_api: SurveyCommentApi, feature: Feature):
    return SurveyComment(
        feature=feature,
        user_id=survey_comment_api.user_id,
        date=survey_comment_api.date,
        rating=survey_comment_api.rating,
        description=survey_comment_api.description
    )


def map_model_comment_api_from_survey_comment(survey_comment: SurveyComment) -> SurveyCommentApi:
    return SurveyCommentApi(
        feature_url=survey_comment.feature.resource,
        user_id=str(survey_comment.user_id),
        date=str(survey_comment.date),
        rating=survey_comment.rating,
        description=survey_comment.description,
        language=survey_comment.language
    )


def map_survey_rule_api_from_survey_rule(rule : SurveyRule) -> SurveyRuleApi:
    return SurveyRuleApi(
        is_activated=rule.is_activated,
        is_activated_on_feature=rule.is_activated,
        delay_before_reanswer=rule.delay_before_reanswer,
        delay_to_answer=rule.delay_to_answer,
        ratio_display=rule.ratio
    )