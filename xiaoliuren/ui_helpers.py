from __future__ import annotations

import json
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from .constants import APP_VERSION
from .llm_prompt import build_llm_interpretation_prompt
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
        html, body, [class*="css"] {
            font-size: 18px;
        }
        .stApp {
            font-size: 1rem;
        }
        .block-container {
            max-width: 820px;
            padding-top: 2.25rem;
            padding-bottom: 2.5rem;
        }
        h1 {
            font-size: clamp(2.35rem, 8vw, 3.25rem) !important;
            line-height: 1.16 !important;
            margin-bottom: 0.7rem !important;
        }
        h2, h3 {
            line-height: 1.25 !important;
        }
        p, li, label, .stMarkdown, .stCaption, .stAlert, .stRadio, .stSelectbox,
        .stTextArea, .stDateInput, .stTimeInput, .stNumberInput, .stCheckbox {
            font-size: 1rem !important;
            line-height: 1.75 !important;
        }
        [data-testid="stCaptionContainer"] p {
            font-size: 0.98rem !important;
            line-height: 1.65 !important;
        }
        [data-testid="stAlert"] {
            font-size: 1rem !important;
            line-height: 1.7 !important;
        }
        [data-testid="stWidgetLabel"] p {
            font-size: 1.08rem !important;
            font-weight: 700 !important;
        }
        div[role="radiogroup"] label,
        [data-testid="stCheckbox"] label {
            min-height: 2.5rem;
            align-items: center;
        }
        div[role="radiogroup"] label p,
        [data-testid="stCheckbox"] label p {
            font-size: 1.08rem !important;
            font-weight: 700 !important;
        }
        .stSelectbox div[data-baseweb="select"] > div,
        .stDateInput input,
        .stTimeInput input,
        .stNumberInput input,
        .stTextArea textarea {
            min-height: 3.15rem;
            font-size: 1.05rem !important;
            line-height: 1.65 !important;
        }
        .stTextArea textarea {
            min-height: 7.5rem !important;
        }
        .stButton button,
        .stDownloadButton button,
        [data-testid="stFormSubmitButton"] button {
            min-height: 3.25rem;
            font-size: 1.12rem !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
        }
        [data-testid="stPills"] button {
            min-height: 2.7rem;
            padding: 0.55rem 0.9rem;
            font-size: 1.03rem !important;
            font-weight: 700 !important;
            border-radius: 999px !important;
        }
        .stTable table {
            font-size: 1rem;
        }
        .stTable th,
        .stTable td {
            padding: 0.78rem 0.9rem !important;
            line-height: 1.55 !important;
        }
        .result-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1.45rem;
            background: linear-gradient(180deg, #fffdf8 0%, #ffffff 100%);
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            margin: 1.1rem 0 0.9rem;
        }
        .result-label {
            color: #6B7280;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .result-sign {
            font-size: clamp(3.3rem, 12vw, 5.4rem);
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: 0;
        }
        .result-keywords {
            margin-top: 0.6rem;
            color: #374151;
            font-size: 1.2rem;
            font-weight: 600;
        }
        .result-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }
        .result-pill {
            border: 1px solid #E5E7EB;
            border-radius: 999px;
            padding: 0.4rem 0.8rem;
            color: #374151;
            background: rgba(255, 255, 255, 0.76);
            font-size: 0.98rem;
            line-height: 1.45;
        }
        .soft-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1.15rem;
            background: #FFFFFF;
            margin: 0.85rem 0;
        }
        .soft-card-title {
            color: #111827;
            font-weight: 800;
            font-size: 1.16rem;
        }
        .soft-card-body {
            color: #374151;
            line-height: 1.85;
            margin-top: 0.55rem;
            white-space: pre-line;
            font-size: 1.06rem;
        }
        .intro-card {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1.15rem;
            background: #FFFFFF;
            margin: 0.85rem 0 1.1rem;
        }
        .intro-eyebrow {
            color: #6B7280;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        .intro-title {
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
            color: #111827;
        }
        .intro-copy {
            color: #374151;
            line-height: 1.85;
            margin-bottom: 1rem;
            font-size: 1.06rem;
        }
        .intro-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
        }
        .intro-chip {
            border: 1px solid #E5E7EB;
            border-radius: 999px;
            padding: 0.38rem 0.78rem;
            color: #374151;
            background: #F9FAFB;
            font-size: 0.98rem;
            line-height: 1.45;
        }
        @media (max-width: 640px) {
            html, body, [class*="css"] {
                font-size: 17px;
            }
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.35rem;
            }
            .result-card,
            .soft-card,
            .intro-card {
                padding: 1rem;
            }
            .result-sign {
                font-size: clamp(3rem, 18vw, 4.4rem);
            }
            .stButton button,
            .stDownloadButton button,
            [data-testid="stFormSubmitButton"] button {
                min-height: 3.1rem;
            }
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
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_rules(profile: RuleProfile | None = None) -> None:
    with st.sidebar:
        st.caption(f"版本：{APP_VERSION}")

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


def render_llm_prompt_copy(result: DivinationResult) -> None:
    prompt = build_llm_interpretation_prompt(result)
    prompt_json = json.dumps(prompt, ensure_ascii=False)
    safe_prompt = escape(prompt)
    components.html(
        f"""
        <div class="copy-card">
            <div class="copy-title">复制给大语言模型解读</div>
            <div class="copy-body">
                点击下方按钮，会复制一段包含问题、起课路径和本页解释的提示词。
            </div>
            <button class="copy-button" type="button" onclick="copyPrompt()">复制解读提示词</button>
            <div id="copyStatus" class="copy-status" aria-live="polite"></div>
            <textarea id="promptText" class="copy-textarea" readonly>{safe_prompt}</textarea>
        </div>
        <script>
        const promptText = {prompt_json};
        async function copyPrompt() {{
            const status = document.getElementById("copyStatus");
            const textarea = document.getElementById("promptText");
            try {{
                if (navigator.clipboard && window.isSecureContext) {{
                    await navigator.clipboard.writeText(promptText);
                }} else {{
                    textarea.focus();
                    textarea.select();
                    document.execCommand("copy");
                    textarea.setSelectionRange(0, 0);
                }}
                status.textContent = "已复制，可以粘贴给大语言模型。";
                status.className = "copy-status success";
            }} catch (error) {{
                textarea.focus();
                textarea.select();
                status.textContent = "自动复制未成功，请手动全选下方文字复制。";
                status.className = "copy-status warning";
            }}
        }}
        </script>
        <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: #1F2937;
            font-size: 18px;
        }}
        .copy-card {{
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 1rem;
            background: #FFFFFF;
            box-sizing: border-box;
        }}
        .copy-title {{
            font-weight: 800;
            font-size: 1.15rem;
            margin-bottom: 0.35rem;
        }}
        .copy-body {{
            color: #4B5563;
            line-height: 1.75;
            margin-bottom: 0.8rem;
        }}
        .copy-button {{
            width: 100%;
            min-height: 3.2rem;
            border: 0;
            border-radius: 10px;
            background: #8B5CF6;
            color: white;
            font-size: 1.08rem;
            font-weight: 800;
            cursor: pointer;
        }}
        .copy-button:hover {{
            background: #7C3AED;
        }}
        .copy-status {{
            min-height: 1.8rem;
            margin-top: 0.65rem;
            color: #4B5563;
            line-height: 1.55;
        }}
        .copy-status.success {{
            color: #166534;
            font-weight: 700;
        }}
        .copy-status.warning {{
            color: #92400E;
            font-weight: 700;
        }}
        .copy-textarea {{
            width: 100%;
            height: 9rem;
            margin-top: 0.55rem;
            padding: 0.75rem;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            color: #374151;
            background: #F9FAFB;
            box-sizing: border-box;
            font-size: 0.95rem;
            line-height: 1.55;
            resize: vertical;
        }}
        @media (max-width: 640px) {{
            body {{
                font-size: 17px;
            }}
            .copy-card {{
                padding: 0.9rem;
            }}
        }}
        </style>
        """,
        height=410,
    )
