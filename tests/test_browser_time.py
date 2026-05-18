from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from xiaoliuren.exceptions import InvalidTimezoneError
from xiaoliuren.browser_time import (
    BROWSER_TIME_SOURCE,
    SERVER_FALLBACK_SOURCE,
    BrowserTimeInfo,
    parse_browser_iso_datetime,
    parse_browser_time_payload,
    select_current_time,
)


def test_parse_browser_iso_datetime_returns_timezone_aware_datetime() -> None:
    parsed = parse_browser_iso_datetime("2026-05-18T12:34:56.000Z")

    assert parsed.tzinfo is not None
    assert parsed.isoformat() == "2026-05-18T12:34:56+00:00"


def test_parse_browser_time_payload_accepts_json_string() -> None:
    info = parse_browser_time_payload(
        '{"browser_iso_datetime":"2026-05-18T12:00:00.000Z","browser_timezone":"Asia/Shanghai"}'
    )

    assert info is not None
    assert info.browser_timezone == "Asia/Shanghai"


def test_invalid_browser_timezone_falls_back_to_selected_timezone() -> None:
    selection = select_current_time(
        BrowserTimeInfo(
            browser_iso_datetime="2026-05-18T12:00:00.000Z",
            browser_timezone="Invalid/Timezone",
        ),
        fallback_timezone_name="Asia/Shanghai",
        now=datetime(2026, 5, 18, 20, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert selection.source == SERVER_FALLBACK_SOURCE
    assert selection.timezone_name == "Asia/Shanghai"
    assert selection.warning is not None


def test_missing_browser_time_falls_back_without_crashing() -> None:
    selection = select_current_time(
        None,
        fallback_timezone_name="Asia/Shanghai",
        now=datetime(2026, 5, 18, 20, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert selection.source == SERVER_FALLBACK_SOURCE
    assert selection.warning == "正在获取浏览器时间；本次暂按北京时间处理。"


def test_valid_browser_time_is_preferred() -> None:
    selection = select_current_time(
        BrowserTimeInfo(
            browser_iso_datetime="2026-05-18T12:00:00.000Z",
            browser_timezone="America/Toronto",
        ),
        fallback_timezone_name="Asia/Shanghai",
    )

    assert selection.source == BROWSER_TIME_SOURCE
    assert selection.timezone_name == "America/Toronto"


def test_invalid_fallback_timezone_raises_clear_error() -> None:
    with pytest.raises(InvalidTimezoneError, match="无效时区"):
        select_current_time(None, fallback_timezone_name="Invalid/Timezone")
