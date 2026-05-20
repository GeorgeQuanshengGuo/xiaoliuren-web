from __future__ import annotations

from .models import EarthlyBranch

APP_VERSION = "v0.2.0"
DEFAULT_FALLBACK_TIMEZONE = "Asia/Shanghai"

CAST_METHOD_CURRENT = "使用当前时间"
CAST_METHOD_SOLAR = "手动选择阳历时间"
CAST_METHOD_LUNAR = "手动输入农历月日时辰"

CAST_METHODS: tuple[str, ...] = (
    CAST_METHOD_CURRENT,
    CAST_METHOD_SOLAR,
    CAST_METHOD_LUNAR,
)

BRANCH_LABEL_TO_ENUM: dict[str, EarthlyBranch] = {
    branch.label: branch for branch in EarthlyBranch
}
