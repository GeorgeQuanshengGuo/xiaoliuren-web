from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from xiaoliuren.exceptions import InvalidTimezoneError
from xiaoliuren.calendar_service import convert_solar_to_lunar
from xiaoliuren.models import EarthlyBranch, SolarToLunarResult


def test_convert_solar_to_lunar_returns_month_day_and_branch() -> None:
    result = convert_solar_to_lunar(
        datetime(2026, 2, 17, 12, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
        "Asia/Shanghai",
    )

    assert isinstance(result, SolarToLunarResult)
    assert result.lunar_year == 2026
    assert result.lunar_month == 1
    assert result.lunar_day == 1
    assert result.branch is EarthlyBranch.WU


def test_naive_datetime_is_interpreted_in_timezone_name() -> None:
    result = convert_solar_to_lunar(datetime(2026, 2, 17, 12, 0), "Asia/Shanghai")

    assert result.solar_datetime.tzinfo == ZoneInfo("Asia/Shanghai")
    assert result.lunar_month == 1
    assert result.lunar_day == 1


def test_aware_datetime_is_converted_to_target_timezone() -> None:
    result = convert_solar_to_lunar(
        datetime(2026, 2, 16, 23, 0, tzinfo=ZoneInfo("America/Toronto")),
        "Asia/Shanghai",
    )

    assert result.solar_datetime.hour == 12
    assert result.branch is EarthlyBranch.WU


def test_twenty_three_thirty_branch_is_zi() -> None:
    result = convert_solar_to_lunar(datetime(2026, 2, 17, 23, 30), "Asia/Shanghai")

    assert result.branch is EarthlyBranch.ZI


def test_night_zi_changes_day_uses_next_day_for_lunar_conversion() -> None:
    result = convert_solar_to_lunar(
        datetime(2026, 2, 17, 23, 30),
        "Asia/Shanghai",
        night_zi_changes_day=True,
    )

    assert result.branch is EarthlyBranch.ZI
    assert result.solar_datetime.day == 18
    assert result.lunar_month == 1
    assert result.lunar_day == 2


def test_night_zi_changes_day_defaults_to_false() -> None:
    result = convert_solar_to_lunar(datetime(2026, 2, 17, 23, 30), "Asia/Shanghai")

    assert result.solar_datetime.day == 17
    assert result.lunar_month == 1
    assert result.lunar_day == 1


def test_invalid_timezone_name_raises_clear_error() -> None:
    with pytest.raises(InvalidTimezoneError, match="无效时区"):
        convert_solar_to_lunar(datetime(2026, 2, 17, 12, 0), "Not/A_Timezone")


def test_convert_solar_to_lunar_never_returns_none() -> None:
    result = convert_solar_to_lunar(datetime(2026, 2, 17, 12, 0), "Asia/Shanghai")

    assert result is not None
