from __future__ import annotations

from datetime import date, time

import pytest

from xiaoliuren.form_service import resolve_cast_request
from xiaoliuren.exceptions import DivinationInputError, InvalidLunarDateError, InvalidTimezoneError
from xiaoliuren.models import Topic


def test_ui_helper_accepts_empty_question_without_crashing() -> None:
    result, source, timezone, warning = resolve_cast_request(
        cast_method="手动输入农历月日时辰",
        timezone_name="Asia/Shanghai",
        night_zi_changes_day=False,
        topic=Topic.GENERAL,
        question="",
        browser_time_info=None,
        selected_date=date(2026, 2, 17),
        selected_time=time(12, 0),
        lunar_month=6,
        lunar_day=5,
        manual_is_leap_month=False,
        branch_label="巳",
    )

    assert result.question == ""
    assert source == "手动输入农历时间"
    assert timezone == "Asia/Shanghai"
    assert warning == "正在获取浏览器时区；本次暂按北京时间处理。"


def test_ui_helper_invalid_lunar_month_raises_user_facing_error() -> None:
    with pytest.raises(InvalidLunarDateError):
        resolve_cast_request(
            cast_method="手动输入农历月日时辰",
            timezone_name="Asia/Shanghai",
            night_zi_changes_day=False,
            topic=Topic.GENERAL,
            question="",
            browser_time_info=None,
            selected_date=date(2026, 2, 17),
            selected_time=time(12, 0),
            lunar_month=13,
            lunar_day=5,
            manual_is_leap_month=False,
            branch_label="巳",
        )


def test_ui_helper_invalid_branch_raises_user_facing_error() -> None:
    with pytest.raises(DivinationInputError, match="时辰必须是十二时辰之一"):
        resolve_cast_request(
            cast_method="手动输入农历月日时辰",
            timezone_name="Asia/Shanghai",
            night_zi_changes_day=False,
            topic=Topic.GENERAL,
            question="",
            browser_time_info=None,
            selected_date=date(2026, 2, 17),
            selected_time=time(12, 0),
            lunar_month=6,
            lunar_day=5,
            manual_is_leap_month=False,
            branch_label="甲",
        )


def test_ui_helper_invalid_timezone_raises_user_facing_error() -> None:
    with pytest.raises(InvalidTimezoneError):
        resolve_cast_request(
            cast_method="手动选择阳历时间",
            timezone_name="Invalid/Timezone",
            night_zi_changes_day=False,
            topic=Topic.GENERAL,
            question="",
            browser_time_info=None,
            selected_date=date(2026, 2, 17),
            selected_time=time(12, 0),
            lunar_month=6,
            lunar_day=5,
            manual_is_leap_month=False,
            branch_label="巳",
        )
