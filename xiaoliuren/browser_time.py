from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .exceptions import DivinationInputError, InvalidTimezoneError


@dataclass(frozen=True)
class BrowserTimeInfo:
    browser_iso_datetime: str
    browser_timezone: str


@dataclass(frozen=True)
class CurrentTimeSelection:
    dt: datetime
    timezone_name: str
    source: str
    warning: str | None = None


BROWSER_TIME_SOURCE = "浏览器本地时间"
SERVER_FALLBACK_SOURCE = "服务器当前时间（默认北京时间）"


def parse_browser_iso_datetime(browser_iso_datetime: str) -> datetime:
    if not browser_iso_datetime:
        raise DivinationInputError("浏览器 ISO 时间为空")
    normalized = browser_iso_datetime.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise DivinationInputError(f"无法解析浏览器 ISO 时间：{browser_iso_datetime}") from exc
    if parsed.tzinfo is None:
        raise DivinationInputError("浏览器 ISO 时间必须包含时区信息")
    return parsed


def validate_timezone_name(timezone_name: str) -> str:
    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise InvalidTimezoneError(f"无效时区：{timezone_name}") from exc
    return timezone_name


def parse_browser_time_payload(payload: object) -> BrowserTimeInfo | None:
    if payload is None:
        return None
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise DivinationInputError("浏览器时间返回值不是有效 JSON") from exc
    if not isinstance(payload, dict):
        raise DivinationInputError("浏览器时间返回值格式不正确")

    iso_datetime = payload.get("browser_iso_datetime")
    timezone_name = payload.get("browser_timezone")
    if not isinstance(iso_datetime, str) or not isinstance(timezone_name, str):
        raise DivinationInputError("浏览器时间返回值缺少必要字段")
    return BrowserTimeInfo(
        browser_iso_datetime=iso_datetime,
        browser_timezone=timezone_name,
    )


def select_current_time(
    browser_info: BrowserTimeInfo | None,
    fallback_timezone_name: str,
    now: datetime | None = None,
) -> CurrentTimeSelection:
    fallback_timezone_name = validate_timezone_name(fallback_timezone_name)
    fallback_now = now or datetime.now(ZoneInfo(fallback_timezone_name))
    if fallback_now.tzinfo is None:
        fallback_now = fallback_now.replace(tzinfo=ZoneInfo(fallback_timezone_name))

    if browser_info is None:
        return CurrentTimeSelection(
            dt=fallback_now,
            timezone_name=fallback_timezone_name,
            source=SERVER_FALLBACK_SOURCE,
            warning="正在获取浏览器时间；本次暂按北京时间处理。",
        )

    try:
        browser_timezone = validate_timezone_name(browser_info.browser_timezone)
        browser_dt = parse_browser_iso_datetime(browser_info.browser_iso_datetime)
    except DivinationInputError as exc:
        return CurrentTimeSelection(
            dt=fallback_now,
            timezone_name=fallback_timezone_name,
            source=SERVER_FALLBACK_SOURCE,
            warning=str(exc),
        )

    return CurrentTimeSelection(
        dt=browser_dt.astimezone(UTC),
        timezone_name=browser_timezone,
        source=BROWSER_TIME_SOURCE,
    )


def select_browser_timezone(
    browser_info: BrowserTimeInfo | None,
    fallback_timezone_name: str,
) -> tuple[str, str | None]:
    fallback_timezone_name = validate_timezone_name(fallback_timezone_name)
    if browser_info is None:
        return fallback_timezone_name, "正在获取浏览器时区；本次暂按北京时间处理。"

    try:
        return validate_timezone_name(browser_info.browser_timezone), None
    except InvalidTimezoneError as exc:
        return fallback_timezone_name, f"{exc}；本次暂按北京时间处理。"


def get_browser_time_info(component_key: str = "browser_time") -> BrowserTimeInfo | None:
    from streamlit_js_eval import streamlit_js_eval

    payload = streamlit_js_eval(
        js_expressions="""
        JSON.stringify({
            browser_iso_datetime: new Date().toISOString(),
            browser_timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        })
        """,
        key=component_key,
    )
    return parse_browser_time_payload(payload)
