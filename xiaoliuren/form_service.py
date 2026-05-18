from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime, time

from .browser_time import BrowserTimeInfo, select_browser_timezone, select_current_time
from .constants import (
    BRANCH_LABEL_TO_ENUM,
    CAST_METHOD_CURRENT,
    CAST_METHOD_LUNAR,
    CAST_METHOD_SOLAR,
    DEFAULT_FALLBACK_TIMEZONE,
)
from .engine import cast_from_lunar_input, cast_from_solar_datetime
from .exceptions import DivinationInputError
from .models import DivinationResult, Topic


def resolve_cast_request(
    cast_method: str,
    night_zi_changes_day: bool,
    topic: Topic,
    question: str,
    browser_time_info: BrowserTimeInfo | None,
    selected_date: date,
    selected_time: time,
    lunar_month: int,
    lunar_day: int,
    manual_is_leap_month: bool,
    branch_label: str,
    timezone_name: str | None = None,
) -> tuple[DivinationResult, str, str, str | None]:
    fallback_timezone_name = timezone_name or DEFAULT_FALLBACK_TIMEZONE

    if cast_method == CAST_METHOD_CURRENT:
        selection = select_current_time(browser_time_info, fallback_timezone_name)
        result = cast_from_solar_datetime(
            dt=selection.dt,
            timezone_name=selection.timezone_name,
            topic=topic,
            question=question,
            night_zi_changes_day=night_zi_changes_day,
        )
        return result, selection.source, selection.timezone_name, selection.warning

    if cast_method == CAST_METHOD_SOLAR:
        actual_timezone, timezone_warning = select_browser_timezone(
            browser_time_info,
            fallback_timezone_name,
        )
        solar_dt = datetime.combine(selected_date, selected_time)
        result = cast_from_solar_datetime(
            dt=solar_dt,
            timezone_name=actual_timezone,
            topic=topic,
            question=question,
            night_zi_changes_day=night_zi_changes_day,
        )
        return result, "手动输入阳历时间（本机时区）", actual_timezone, timezone_warning

    if cast_method == CAST_METHOD_LUNAR:
        actual_timezone, timezone_warning = select_browser_timezone(
            browser_time_info,
            fallback_timezone_name,
        )
        branch = BRANCH_LABEL_TO_ENUM.get(branch_label)
        if branch is None:
            raise DivinationInputError("时辰必须是十二时辰之一")
        result = cast_from_lunar_input(
            lunar_month=int(lunar_month),
            lunar_day=int(lunar_day),
            branch=branch,
            topic=topic,
            question=question,
        )
        result = replace(
            result,
            path=replace(
                result.path,
                is_leap_month=manual_is_leap_month,
                timezone=actual_timezone,
            ),
        )
        return result, "手动输入农历时间", actual_timezone, timezone_warning

    raise DivinationInputError("未知起课方式")
