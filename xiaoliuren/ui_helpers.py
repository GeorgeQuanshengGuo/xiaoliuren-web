from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from .models import DivinationResult, RuleProfile, SixSign

HERO_IMAGE_PATH = Path(__file__).resolve().parent.parent / "assets" / "xiaoliuren-six-signs.svg"

SIGN_KEYWORDS: dict[SixSign, str] = {
    SixSign.DA_AN: "安定｜宜守｜稳中求成",
    SixSign.LIU_LIAN: "拖延｜反复｜宜缓",
    SixSign.SU_XI: "快速｜消息｜可主动",
    SixSign.CHI_KOU: "口舌｜冲突｜慎言",
    SixSign.XIAO_JI: "小顺｜转机｜渐进",
    SixSign.KONG_WANG: "落空｜虚耗｜需核查",
}

SIGN_COLORS: dict[SixSign, str] = {
    SixSign.DA_AN: "#166534",
    SixSign.LIU_LIAN: "#854D0E",
    SixSign.SU_XI: "#B91C1C",
    SixSign.CHI_KOU: "#991B1B",
    SixSign.XIAO_JI: "#0369A1",
    SixSign.KONG_WANG: "#4B5563",
}

SIX_SIGN_STUDY_ROWS: list[dict[str, str]] = [
    {
        "六神": "大安",
        "常见取象": "木｜安定、原位、稳定基础",
        "判断重点": "已有条件是否稳固，宜守成、整理、巩固",
    },
    {
        "六神": "留连",
        "常见取象": "水｜拖延、牵连、反复等待",
        "判断重点": "流程卡点、旧问题、反复沟通和未完事项",
    },
    {
        "六神": "速喜",
        "常见取象": "火｜消息、快速、短期动象",
        "判断重点": "新回应、新窗口、可快速确认的线索",
    },
    {
        "六神": "赤口",
        "常见取象": "金｜口舌、边界、规则摩擦",
        "判断重点": "表达、证据、责任边界和冲突成本",
    },
    {
        "六神": "小吉",
        "常见取象": "木｜和合、小成、逐步转顺",
        "判断重点": "小范围机会、阶段成果和可借用的支持",
    },
    {
        "六神": "空亡",
        "常见取象": "土｜虚耗、落空、信息缺口",
        "判断重点": "假设是否真实、资源是否到位、方向是否要重核",
    },
]


def inject_page_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 760px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .result-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1.25rem;
            background: linear-gradient(180deg, #fffdf8 0%, #ffffff 100%);
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            margin: 1rem 0 0.75rem;
        }
        .result-label {
            color: #6B7280;
            font-size: 0.9rem;
            margin-bottom: 0.15rem;
        }
        .result-sign {
            font-size: clamp(2.7rem, 10vw, 4.5rem);
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: 0;
        }
        .result-keywords {
            margin-top: 0.45rem;
            color: #374151;
            font-size: 1.05rem;
            font-weight: 600;
        }
        .result-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.9rem;
        }
        .result-pill {
            border: 1px solid #E5E7EB;
            border-radius: 999px;
            padding: 0.28rem 0.68rem;
            color: #374151;
            background: rgba(255, 255, 255, 0.76);
            font-size: 0.86rem;
        }
        .soft-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            background: #FFFFFF;
            margin: 0.75rem 0;
        }
        .soft-card-title {
            color: #111827;
            font-weight: 800;
        }
        .soft-card-body {
            color: #374151;
            line-height: 1.75;
            margin-top: 0.45rem;
            white-space: pre-line;
        }
        .intro-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            background: #FFFFFF;
            margin: 0.75rem 0 1rem;
        }
        .intro-eyebrow {
            color: #6B7280;
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .intro-title {
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            color: #111827;
        }
        .intro-copy {
            color: #374151;
            line-height: 1.75;
            margin-bottom: 0.85rem;
        }
        .intro-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }
        .intro-chip {
            border: 1px solid #E5E7EB;
            border-radius: 999px;
            padding: 0.25rem 0.65rem;
            color: #374151;
            background: #F9FAFB;
            font-size: 0.86rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_intro_section() -> None:
    st.image(
        str(HERO_IMAGE_PATH),
        caption="配图：小六壬六神顺序示意图。本图为本项目自制视觉，用于帮助理解起课顺推关系。",
        width="stretch",
    )
    st.markdown(
        """
        <div class="intro-card">
            <div class="intro-eyebrow">开始之前</div>
            <div class="intro-title">小六壬是什么？</div>
            <div class="intro-copy">
                小六壬是一种民间常见的时间起课方法。它用农历月、农历日和当下时辰，
                沿“大安、留连、速喜、赤口、小吉、空亡”的顺序推算结果，
                帮助使用者整理问题、观察当前节奏，并在事后复盘实际情况。
                本工具会展示起课路径、六神取象和场景化建议，适合作为传统文化学习与娱乐参考。
            </div>
            <div class="intro-chips">
                <span class="intro-chip">月日时起课</span>
                <span class="intro-chip">六神取象分析</span>
                <span class="intro-chip">场景化建议</span>
                <span class="intro-chip">不保存起课记录</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_rules(profile: RuleProfile | None = None) -> None:
    with st.sidebar:
        if profile:
            st.header("当前流派")
            st.write(profile.name)
            st.caption(profile.description)

        st.header("规则说明")
        st.write("按农历月、农历日、时辰依次顺推六神。")
        st.write("月位 = (农历月 - 1) % 6")
        st.write("日位 = (月位 + 农历日 - 1) % 6")
        st.write("时位 = (日位 + 时辰序号) % 6")

        st.header("六神顺序")
        st.write("大安 → 留连 → 速喜 → 赤口 → 小吉 → 空亡")

        st.header("免责声明")
        st.caption("本工具仅作传统文化学习与娱乐参考，不替代医疗、法律、投资等专业建议。")


def render_learning_section() -> None:
    with st.expander("学习与规则说明", expanded=False):
        tab_rules, tab_signs, tab_app_rules, tab_examples, tab_review = st.tabs(
            ["起课规则", "六神速览", "本 App 规则", "起课示例", "如何复盘"]
        )

        with tab_rules:
            st.markdown("#### 小六壬起课规则")
            st.write("六神顺序：大安 → 留连 → 速喜 → 赤口 → 小吉 → 空亡")
            st.write("月位 = (农历月 - 1) % 6")
            st.write("日位 = (月位 + 农历日 - 1) % 6")
            st.write("时位 = (日位 + 时辰序号) % 6")
            st.markdown("#### 十二时辰表")
            st.table(
                [
                    {"时辰": "子", "序号": 0, "时间": "23:00-00:59"},
                    {"时辰": "丑", "序号": 1, "时间": "01:00-02:59"},
                    {"时辰": "寅", "序号": 2, "时间": "03:00-04:59"},
                    {"时辰": "卯", "序号": 3, "时间": "05:00-06:59"},
                    {"时辰": "辰", "序号": 4, "时间": "07:00-08:59"},
                    {"时辰": "巳", "序号": 5, "时间": "09:00-10:59"},
                    {"时辰": "午", "序号": 6, "时间": "11:00-12:59"},
                    {"时辰": "未", "序号": 7, "时间": "13:00-14:59"},
                    {"时辰": "申", "序号": 8, "时间": "15:00-16:59"},
                    {"时辰": "酉", "序号": 9, "时间": "17:00-18:59"},
                    {"时辰": "戌", "序号": 10, "时间": "19:00-20:59"},
                    {"时辰": "亥", "序号": 11, "时间": "21:00-22:59"},
                ]
            )

        with tab_signs:
            st.markdown("#### 六神速览")
            st.write(
                "小六壬结果不只看吉凶，也看取象、节奏和问题落点。"
                "下表是本工具采用的本地解释口径。"
            )
            st.table(SIX_SIGN_STUDY_ROWS)
            st.caption("不同传本和流派的细节会有差异；本工具先采用标准月日时起课法的一套克制解释。")

        with tab_app_rules:
            st.markdown("#### 当前 App 采用的规则")
            st.markdown("- 闰月按同名月份处理，例如闰二月仍按二月计算。")
            st.markdown("- 默认不启用夜子时换日。")
            st.markdown("- 可以在起课表单中手动开启夜子时换日。")
            st.markdown("- 本工具是传统文化学习与娱乐参考。")
            st.markdown("- 不替代医疗、法律、投资等专业建议。")

        with tab_examples:
            st.markdown("#### 起课示例")
            st.table(
                [
                    {"输入": "农历六月初五巳时", "结果": "速喜"},
                    {"输入": "农历三月初五辰时", "结果": "小吉"},
                    {"输入": "农历八月十七辰时", "结果": "赤口"},
                ]
            )

        with tab_review:
            st.markdown("#### 如何复盘")
            st.markdown("- 记录问题。")
            st.markdown("- 记录时间。")
            st.markdown("- 记录结果。")
            st.markdown("- 过几天回看实际情况。")
            st.markdown("- 不要把结果当作唯一决策依据。")


def render_result_card(result: DivinationResult) -> None:
    color = SIGN_COLORS[result.sign]
    keywords = SIGN_KEYWORDS[result.sign]
    safe_topic = escape(result.topic.label)
    safe_question = escape(result.question or "未填写具体问题")
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">最终六神</div>
            <div class="result-sign" style="color: {color};">{result.sign.value}</div>
            <div class="result-keywords">{keywords}</div>
            <div class="result-meta">
                <span class="result-pill">场景：{safe_topic}</span>
                <span class="result-pill">问题：{safe_question}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_text_card(title: str, body: str) -> None:
    safe_title = escape(title)
    safe_body = escape(body)
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="soft-card-title">{safe_title}</div>
            <div class="soft-card-body">{safe_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_actions(title: str, actions: list[str]) -> None:
    st.markdown(f"### {title}")
    for action in actions:
        st.markdown(f"- {action}")


def build_path_rows(result: DivinationResult) -> list[dict[str, str]]:
    path = result.path
    rows = [
        {"项目": "农历月", "值": f"{path.lunar_month} 月"},
        {"项目": "农历日", "值": f"{path.lunar_day} 日"},
        {"项目": "是否闰月", "值": "是" if path.is_leap_month else "否"},
        {"项目": "时辰", "值": f"{path.branch.label}时"},
        {"项目": "月位", "值": str(path.month_position)},
        {"项目": "日位", "值": str(path.day_position)},
        {"项目": "时位", "值": str(path.hour_position)},
        {"项目": "六神", "值": path.sign.value},
        {"项目": "流派", "值": path.rule_profile_name},
    ]
    if path.solar_datetime:
        rows.extend(
            [
                {
                    "项目": "阳历时间",
                    "值": path.solar_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                },
                {"项目": "时区", "值": path.timezone or "未指定"},
                {"项目": "农历年", "值": str(path.lunar_year or "未知")},
            ]
        )
    return rows


def render_path_table(result: DivinationResult) -> None:
    st.markdown("### 起课路径")
    st.table(build_path_rows(result))
