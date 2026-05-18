from __future__ import annotations

from datetime import datetime

import pytest

from xiaoliuren.exceptions import DivinationInputError, InvalidLunarDateError, InvalidTimezoneError
from xiaoliuren.engine import (
    DEFAULT_PROFILE,
    cast_by_lunar,
    cast_from_current_time,
    cast_from_lunar_input,
    cast_from_solar_datetime,
    get_branch_by_hour,
    validate_lunar_input,
)
from xiaoliuren.models import DivinationResult, EarthlyBranch, SixSign, Topic


def test_zero_and_twenty_three_are_zi_hour() -> None:
    assert get_branch_by_hour(0) is EarthlyBranch.ZI
    assert get_branch_by_hour(23) is EarthlyBranch.ZI


def test_six_sign_order_is_stable() -> None:
    from xiaoliuren.engine import SIGN_LIST

    assert [sign.value for sign in SIGN_LIST] == ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]


def test_default_rule_profile_is_standard_school() -> None:
    assert DEFAULT_PROFILE.name == "标准月日时起课法"
    assert DEFAULT_PROFILE.leap_month_policy == "闰月按同名月份处理"
    assert DEFAULT_PROFILE.default_night_zi_changes_day is False


def test_one_and_two_are_chou_hour() -> None:
    assert get_branch_by_hour(1) is EarthlyBranch.CHOU
    assert get_branch_by_hour(2) is EarthlyBranch.CHOU


@pytest.mark.parametrize(
    ("hour", "branch"),
    [
        (0, EarthlyBranch.ZI),
        (1, EarthlyBranch.CHOU),
        (2, EarthlyBranch.CHOU),
        (3, EarthlyBranch.YIN),
        (4, EarthlyBranch.YIN),
        (5, EarthlyBranch.MAO),
        (6, EarthlyBranch.MAO),
        (7, EarthlyBranch.CHEN),
        (8, EarthlyBranch.CHEN),
        (9, EarthlyBranch.SI),
        (10, EarthlyBranch.SI),
        (11, EarthlyBranch.WU),
        (12, EarthlyBranch.WU),
        (13, EarthlyBranch.WEI),
        (14, EarthlyBranch.WEI),
        (15, EarthlyBranch.SHEN),
        (16, EarthlyBranch.SHEN),
        (17, EarthlyBranch.YOU),
        (18, EarthlyBranch.YOU),
        (19, EarthlyBranch.XU),
        (20, EarthlyBranch.XU),
        (21, EarthlyBranch.HAI),
        (22, EarthlyBranch.HAI),
        (23, EarthlyBranch.ZI),
    ],
)
def test_all_24_hours_map_to_expected_branch(hour: int, branch: EarthlyBranch) -> None:
    assert get_branch_by_hour(hour) is branch


def test_cast_sixth_lunar_month_fifth_day_si_is_su_xi() -> None:
    result = cast_by_lunar(6, 5, EarthlyBranch.SI)

    assert result.sign is SixSign.SU_XI
    assert result.rule_profile_name == DEFAULT_PROFILE.name
    assert result.month_position == 5
    assert result.day_position == 3
    assert result.hour_position == 2


def test_cast_third_lunar_month_fifth_day_chen_is_xiao_ji() -> None:
    result = cast_by_lunar(3, 5, EarthlyBranch.CHEN)

    assert result.sign is SixSign.XIAO_JI


def test_cast_eighth_lunar_month_seventeenth_day_chen_is_chi_kou() -> None:
    result = cast_by_lunar(8, 17, EarthlyBranch.CHEN)

    assert result.sign is SixSign.CHI_KOU


def test_default_profile_keeps_required_examples_unchanged() -> None:
    assert cast_by_lunar(6, 5, EarthlyBranch.SI, profile=DEFAULT_PROFILE).sign is SixSign.SU_XI
    assert cast_by_lunar(3, 5, EarthlyBranch.CHEN, profile=DEFAULT_PROFILE).sign is SixSign.XIAO_JI
    assert cast_by_lunar(8, 17, EarthlyBranch.CHEN, profile=DEFAULT_PROFILE).sign is SixSign.CHI_KOU


@pytest.mark.parametrize(
    ("lunar_month", "lunar_day", "message"),
    [
        (0, 1, "农历月份必须在 1-12 之间"),
        (13, 1, "农历月份必须在 1-12 之间"),
        (1, 0, "农历日期必须在 1-30 之间"),
        (1, 31, "农历日期必须在 1-30 之间"),
    ],
)
def test_validate_lunar_input_rejects_invalid_values(
    lunar_month: int,
    lunar_day: int,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_lunar_input(lunar_month, lunar_day)


@pytest.mark.parametrize(
    ("lunar_month", "lunar_day"),
    [(0, 1), (13, 1), (1, 0), (1, 31)],
)
def test_invalid_lunar_date_raises_custom_error(lunar_month: int, lunar_day: int) -> None:
    with pytest.raises(InvalidLunarDateError):
        validate_lunar_input(lunar_month, lunar_day)


def assert_complete_divination_result(result: DivinationResult) -> None:
    assert result.sign is result.path.sign
    assert result.path.lunar_month
    assert result.path.lunar_day
    assert result.path.branch
    assert result.summary
    assert result.detail
    assert isinstance(result.suggested_actions, list)
    assert isinstance(result.avoid_actions, list)
    assert result.suggested_actions
    assert result.avoid_actions


def test_cast_from_lunar_input_returns_complete_result() -> None:
    result = cast_from_lunar_input(
        lunar_month=6,
        lunar_day=5,
        branch=EarthlyBranch.SI,
        topic=Topic.GENERAL,
        question="今天适合推进吗？",
    )

    assert_complete_divination_result(result)
    assert result.sign is SixSign.SU_XI
    assert result.path.lunar_month == 6
    assert result.path.lunar_day == 5
    assert result.path.branch is EarthlyBranch.SI
    assert result.question == "今天适合推进吗？"


def test_cast_from_lunar_input_accepts_empty_question() -> None:
    result = cast_from_lunar_input(6, 5, EarthlyBranch.SI, Topic.GENERAL, question=None)

    assert_complete_divination_result(result)
    assert result.question == ""


def test_cast_from_lunar_input_rejects_long_question() -> None:
    with pytest.raises(DivinationInputError, match="200 字以内"):
        cast_from_lunar_input(6, 5, EarthlyBranch.SI, Topic.GENERAL, question="问" * 201)


def test_cast_from_solar_datetime_returns_complete_result() -> None:
    result = cast_from_solar_datetime(
        datetime(2026, 2, 17, 12, 0),
        timezone_name="Asia/Shanghai",
        topic=Topic.CAREER,
    )

    assert_complete_divination_result(result)
    assert result.path.solar_datetime is not None
    assert result.path.timezone == "Asia/Shanghai"
    assert result.path.lunar_year == 2026
    assert result.path.lunar_month == 1
    assert result.path.lunar_day == 1
    assert result.path.is_leap_month is False
    assert result.path.branch is EarthlyBranch.WU


def test_cast_from_current_time_returns_complete_result() -> None:
    result = cast_from_current_time("Asia/Shanghai", Topic.GENERAL)

    assert_complete_divination_result(result)
    assert result.path.solar_datetime is not None
    assert result.path.timezone == "Asia/Shanghai"
    assert isinstance(result.path.is_leap_month, bool)


def test_cast_from_solar_datetime_invalid_timezone_raises_custom_error() -> None:
    with pytest.raises(InvalidTimezoneError, match="无效时区"):
        cast_from_solar_datetime(
            datetime(2026, 2, 17, 12, 0),
            timezone_name="Invalid/Timezone",
            topic=Topic.GENERAL,
        )


def test_cast_by_lunar_invalid_branch_raises_clear_error() -> None:
    with pytest.raises(DivinationInputError, match="时辰必须是十二时辰之一"):
        cast_by_lunar(6, 5, "巳")  # type: ignore[arg-type]
