from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .exceptions import CalendarConversionError, InvalidTimezoneError
from .models import SolarToLunarResult
from .utils import get_branch_by_hour


def apply_late_zi_day_change(dt: datetime, enabled: bool = False) -> datetime:
    if enabled and dt.hour == 23:
        return dt + timedelta(days=1)
    return dt


def _get_timezone(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise InvalidTimezoneError(f"无效时区：{timezone_name}") from exc


def _to_local_datetime(dt: datetime, timezone_name: str) -> datetime:
    timezone = _get_timezone(timezone_name)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone)
    return dt.astimezone(timezone)


def convert_solar_to_lunar(
    dt: datetime,
    timezone_name: str,
    night_zi_changes_day: bool = False,
) -> SolarToLunarResult:
    local_dt = _to_local_datetime(dt, timezone_name)
    branch = get_branch_by_hour(local_dt.hour)
    adjusted_dt = apply_late_zi_day_change(local_dt, night_zi_changes_day)

    try:
        from lunar_python import Solar
    except ImportError as exc:
        raise CalendarConversionError(
            "农历转换依赖不可用，请确认已安装 lunar_python。"
        ) from exc

    try:
        lunar = Solar.fromYmdHms(
            adjusted_dt.year,
            adjusted_dt.month,
            adjusted_dt.day,
            adjusted_dt.hour,
            adjusted_dt.minute,
            adjusted_dt.second,
        ).getLunar()
        lunar_month = int(lunar.getMonth())
        lunar_year = int(lunar.getYear())
        lunar_day = int(lunar.getDay())
    except Exception as exc:
        raise CalendarConversionError("阳历转农历失败，请检查输入日期和时区。") from exc

    return SolarToLunarResult(
        solar_datetime=adjusted_dt,
        timezone=timezone_name,
        lunar_year=lunar_year,
        lunar_month=abs(lunar_month),
        lunar_day=lunar_day,
        is_leap_month=lunar_month < 0,
        branch=branch,
    )


def solar_to_lunar(dt: datetime, use_late_zi_day_change: bool = False) -> SolarToLunarResult:
    return convert_solar_to_lunar(
        dt,
        timezone_name="Asia/Shanghai",
        night_zi_changes_day=use_late_zi_day_change,
    )
