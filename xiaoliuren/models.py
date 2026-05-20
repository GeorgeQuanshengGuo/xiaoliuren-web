from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SixSign(Enum):
    DA_AN = "大安"
    LIU_LIAN = "留连"
    SU_XI = "速喜"
    CHI_KOU = "赤口"
    XIAO_JI = "小吉"
    KONG_WANG = "空亡"


class EarthlyBranch(Enum):
    ZI = ("子", 0)
    CHOU = ("丑", 1)
    YIN = ("寅", 2)
    MAO = ("卯", 3)
    CHEN = ("辰", 4)
    SI = ("巳", 5)
    WU = ("午", 6)
    WEI = ("未", 7)
    SHEN = ("申", 8)
    YOU = ("酉", 9)
    XU = ("戌", 10)
    HAI = ("亥", 11)

    def __init__(self, label: str, index: int) -> None:
        self.label = label
        self.index = index

    def __str__(self) -> str:
        return self.label


class Topic(Enum):
    GENERAL = ("general", "综合事项", "适合尚未分类的一般问题。")
    WEALTH = ("wealth", "财运/求财", "关注收入、支出、机会与风险控制。")
    CAREER = ("career", "工作/事业", "关注职场进展、任务推进与职业选择。")
    JOB_SEARCH = ("job_search", "求职", "关注投递、面试、录用反馈与岗位匹配。")
    RELATIONSHIP = ("relationship", "感情/关系", "关注亲密关系、人际互动与沟通状态。")
    LOST_ITEM = ("lost_item", "寻物", "关注遗失物品的线索与查找方向。")
    TRAVEL = ("travel", "出行", "关注行程安排、延误与途中协调。")
    STUDY_EXAM = ("study_exam", "学业/考试", "关注学习节奏、备考状态与反馈。")
    WAITING_MESSAGE = ("waiting_message", "消息等待", "关注回复、通知、结果等待。")
    COOPERATION_CONTRACT = ("cooperation_contract", "合作/签约", "关注合作推进、条款沟通与边界。")
    HOME_MOVE = ("home_move", "家宅/搬迁", "关注家庭事务、居住调整与搬迁安排。")
    HEALTH_STATE = ("health_state", "身心状态", "关注日常作息、压力与生活状态提醒。")
    CUSTOM = ("custom", "自定义问题", "使用通用解释模板回应自定义问题。")

    def __init__(self, key: str, label: str, description: str) -> None:
        self.key = key
        self.label = label
        self.description = description


@dataclass(frozen=True)
class RuleProfile:
    name: str
    description: str
    leap_month_policy: str
    default_night_zi_changes_day: bool
    month_start_policy: str
    interpretation_policy: str


@dataclass(frozen=True)
class Interpretation:
    summary: str
    detail: str
    overview: str
    current_situation: str
    question_meaning: str
    suggested_actions: list[str]
    avoid_actions: list[str]
    review_prompt: str
    likely_location_hint: str | None = None
    search_strategy: str | None = None
    caution: str | None = None


@dataclass(frozen=True)
class DivinationPath:
    lunar_month: int
    lunar_day: int
    branch: EarthlyBranch
    month_position: int
    day_position: int
    hour_position: int
    sign: SixSign
    solar_datetime: datetime | None = None
    timezone: str | None = None
    lunar_year: int | None = None
    is_leap_month: bool = False
    rule_profile_name: str = "标准月日时起课法"


@dataclass(frozen=True)
class DivinationResult:
    sign: SixSign
    path: DivinationPath
    topic: Topic
    question: str
    summary: str
    detail: str
    overview: str
    current_situation: str
    question_meaning: str
    suggested_actions: list[str]
    avoid_actions: list[str]
    review_prompt: str
    likely_location_hint: str | None = None
    search_strategy: str | None = None
    caution: str | None = None


@dataclass(frozen=True)
class SolarToLunarResult:
    solar_datetime: datetime
    timezone: str
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    branch: EarthlyBranch


SolarConversionResult = SolarToLunarResult
