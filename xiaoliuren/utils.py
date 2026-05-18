from __future__ import annotations

from datetime import datetime

from .exceptions import DivinationInputError
from .models import EarthlyBranch

HOUR_TO_BRANCH: tuple[EarthlyBranch, ...] = (
    EarthlyBranch.ZI,
    EarthlyBranch.CHOU,
    EarthlyBranch.YIN,
    EarthlyBranch.MAO,
    EarthlyBranch.CHEN,
    EarthlyBranch.SI,
    EarthlyBranch.WU,
    EarthlyBranch.WEI,
    EarthlyBranch.SHEN,
    EarthlyBranch.YOU,
    EarthlyBranch.XU,
    EarthlyBranch.HAI,
)


def get_branch_by_hour(hour: int) -> EarthlyBranch:
    if not 0 <= hour <= 23:
        raise DivinationInputError("小时必须在 0 到 23 之间")
    if hour in (23, 0):
        return EarthlyBranch.ZI
    return HOUR_TO_BRANCH[(hour + 1) // 2]


def get_hour_branch(dt: datetime) -> EarthlyBranch:
    return get_branch_by_hour(dt.hour)


def get_hour_branch_label(dt: datetime) -> str:
    if dt.hour in (23, 0):
        return EarthlyBranch.ZI.label
    return get_hour_branch(dt).label
