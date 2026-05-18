from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .exceptions import DivinationInputError, InvalidLunarDateError, InvalidTimezoneError
from .interpretations import get_interpretation
from .models import DivinationPath, DivinationResult, EarthlyBranch, RuleProfile, SixSign, Topic
from .utils import get_branch_by_hour

DEFAULT_PROFILE = RuleProfile(
    name="标准月日时起课法",
    description="按农历月、农历日、时辰顺推六神的默认起课法。",
    leap_month_policy="闰月按同名月份处理",
    default_night_zi_changes_day=False,
    month_start_policy="以农历月份数字起月，月位 = (农历月 - 1) % 6",
    interpretation_policy="使用本地通用解释模板",
)

SIGN_LIST: tuple[SixSign, ...] = (
    SixSign.DA_AN,
    SixSign.LIU_LIAN,
    SixSign.SU_XI,
    SixSign.CHI_KOU,
    SixSign.XIAO_JI,
    SixSign.KONG_WANG,
)

def validate_lunar_input(lunar_month: int, lunar_day: int) -> None:
    if not 1 <= lunar_month <= 12:
        raise InvalidLunarDateError("农历月份必须在 1-12 之间")
    if not 1 <= lunar_day <= 30:
        raise InvalidLunarDateError("农历日期必须在 1-30 之间")


def cast_by_lunar(
    lunar_month: int,
    lunar_day: int,
    branch: EarthlyBranch,
    profile: RuleProfile = DEFAULT_PROFILE,
) -> DivinationPath:
    validate_lunar_input(lunar_month, lunar_day)
    if not isinstance(branch, EarthlyBranch):
        raise DivinationInputError("时辰必须是十二时辰之一")

    month_position = (lunar_month - 1) % 6
    day_position = (month_position + lunar_day - 1) % 6
    hour_position = (day_position + branch.index) % 6
    return DivinationPath(
        lunar_month=lunar_month,
        lunar_day=lunar_day,
        branch=branch,
        month_position=month_position,
        day_position=day_position,
        hour_position=hour_position,
        sign=SIGN_LIST[hour_position],
        rule_profile_name=profile.name,
    )


def _validate_topic(topic: Topic) -> None:
    if not isinstance(topic, Topic):
        raise DivinationInputError("主题必须是 Topic 枚举值")


def normalize_question(question: str | None) -> str:
    normalized = question.strip() if question else ""
    if len(normalized) > 200:
        raise DivinationInputError("具体问题请控制在 200 字以内")
    return normalized


def _build_result(
    path: DivinationPath,
    topic: Topic,
    question: str | None,
) -> DivinationResult:
    _validate_topic(topic)
    normalized_question = normalize_question(question)
    interpretation = get_interpretation(path.sign, topic, normalized_question or None)
    return DivinationResult(
        sign=path.sign,
        path=path,
        topic=topic,
        question=normalized_question,
        summary=interpretation.summary,
        detail=interpretation.detail,
        overview=interpretation.overview,
        current_situation=interpretation.current_situation,
        question_meaning=interpretation.question_meaning,
        suggested_actions=interpretation.suggested_actions,
        avoid_actions=interpretation.avoid_actions,
        review_prompt=interpretation.review_prompt,
        likely_location_hint=interpretation.likely_location_hint,
        search_strategy=interpretation.search_strategy,
        caution=interpretation.caution,
    )


def _get_timezone(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise InvalidTimezoneError(f"无效时区：{timezone_name}") from exc


def cast_from_lunar_input(
    lunar_month: int,
    lunar_day: int,
    branch: EarthlyBranch,
    topic: Topic,
    question: str | None = None,
    profile: RuleProfile = DEFAULT_PROFILE,
) -> DivinationResult:
    path = cast_by_lunar(lunar_month, lunar_day, branch, profile=profile)
    return _build_result(path, topic, question)


def cast_from_solar_datetime(
    dt: datetime,
    timezone_name: str,
    topic: Topic,
    question: str | None = None,
    night_zi_changes_day: bool = False,
    profile: RuleProfile = DEFAULT_PROFILE,
) -> DivinationResult:
    from .calendar_service import convert_solar_to_lunar

    lunar = convert_solar_to_lunar(dt, timezone_name, night_zi_changes_day)
    path = cast_by_lunar(lunar.lunar_month, lunar.lunar_day, lunar.branch, profile=profile)
    path = replace(
        path,
        solar_datetime=lunar.solar_datetime,
        timezone=lunar.timezone,
        lunar_year=lunar.lunar_year,
        is_leap_month=lunar.is_leap_month,
    )
    return _build_result(path, topic, question)


def cast_from_current_time(
    timezone_name: str,
    topic: Topic,
    question: str | None = None,
    night_zi_changes_day: bool = False,
    profile: RuleProfile = DEFAULT_PROFILE,
) -> DivinationResult:
    timezone = _get_timezone(timezone_name)
    return cast_from_solar_datetime(
        datetime.now(timezone),
        timezone_name=timezone_name,
        topic=topic,
        question=question,
        night_zi_changes_day=night_zi_changes_day,
        profile=profile,
    )
