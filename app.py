from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

from xiaoliuren.browser_time import get_browser_time_info, parse_browser_iso_datetime
from xiaoliuren.constants import (
    APP_VERSION,
    BRANCH_LABEL_TO_ENUM,
    CAST_METHOD_CURRENT,
    CAST_METHOD_LUNAR,
    CAST_METHOD_SOLAR,
    CAST_METHODS,
    DEFAULT_FALLBACK_TIMEZONE,
)
from xiaoliuren.engine import DEFAULT_PROFILE
from xiaoliuren.exceptions import DivinationInputError
from xiaoliuren.form_service import resolve_cast_request
from xiaoliuren.models import DivinationResult, Topic
from xiaoliuren.ui_helpers import (
    inject_page_styles,
    render_actions,
    render_intro_section,
    render_learning_section,
    render_path_table,
    render_result_card,
    render_sidebar_rules,
    render_text_card,
)


def topic_options() -> dict[str, Topic]:
    return {topic.label: topic for topic in Topic}


def render_result(result: DivinationResult) -> None:
    st.divider()
    render_result_card(result)
    render_text_card("结果总览", result.overview)
    render_text_card("当前局势", result.current_situation)
    render_text_card("对这个问题的含义", result.question_meaning)
    if result.topic == Topic.LOST_ITEM:
        if result.likely_location_hint:
            render_text_card("寻找方向", result.likely_location_hint)
        if result.search_strategy:
            render_text_card("搜索策略", result.search_strategy)
        if result.caution:
            render_text_card("提醒", result.caution)
    col_suggested, col_avoid = st.columns(2)
    with col_suggested:
        render_actions("建议行动", result.suggested_actions)
    with col_avoid:
        render_actions("避免事项", result.avoid_actions)
    render_text_card("复盘提示", result.review_prompt)
    render_path_table(result)


def main() -> None:
    st.set_page_config(page_title="小六壬起课工具", page_icon="☯", layout="centered")
    inject_page_styles()
    render_sidebar_rules(DEFAULT_PROFILE)

    st.title("小六壬起课工具")
    st.warning("本工具仅作传统文化学习与娱乐参考，不替代医疗、法律、投资等专业建议。")
    st.caption(f"当前采用流派：{DEFAULT_PROFILE.name}")
    st.caption(f"当前版本：{APP_VERSION}")
    render_intro_section()
    try:
        browser_time_info = get_browser_time_info()
    except DivinationInputError as exc:
        browser_time_info = None
        st.caption(f"浏览器时间识别暂不可用：{exc}")
    if browser_time_info is None:
        st.info("正在识别本机时间；如果暂未识别成功，本次会先按北京时间处理。")
    else:
        st.caption(f"已识别本机时区：{browser_time_info.browser_timezone}")

    topic_map = topic_options()
    try:
        now = (
            parse_browser_iso_datetime(browser_time_info.browser_iso_datetime).astimezone(
                ZoneInfo(browser_time_info.browser_timezone)
            )
            if browser_time_info
            else datetime.now(ZoneInfo(DEFAULT_FALLBACK_TIMEZONE))
        )
    except (DivinationInputError, ZoneInfoNotFoundError):
        now = datetime.now(ZoneInfo(DEFAULT_FALLBACK_TIMEZONE))

    st.markdown("### 起课输入")
    cast_method = st.radio("起课方式", CAST_METHODS, horizontal=True, key="cast_method")

    with st.form("cast_form"):
        night_zi_changes_day = st.checkbox("夜子时换日（23:00 后按次日换算农历）", value=False)
        topic_labels = list(topic_map.keys())
        topic_label = st.pills(
            "场景选择",
            topic_labels,
            default=topic_labels[0],
            required=True,
            width="stretch",
        )
        selected_topic_label = topic_label or topic_labels[0]
        question = st.text_area(
            "具体问题（可为空）",
            placeholder="例如：这件事今天适合推进吗？",
            max_chars=200,
        )

        selected_date = now.date()
        selected_time = now.time().replace(second=0, microsecond=0)
        lunar_month = 1
        manual_is_leap_month = False
        lunar_day = 1
        branch_label = "子"

        if cast_method == CAST_METHOD_CURRENT:
            st.caption("将使用浏览器识别到的本机时间；识别未完成时暂按北京时间处理。")

        if cast_method == CAST_METHOD_SOLAR:
            st.markdown("#### 阳历时间")
            st.caption("手动输入的阳历时间会按识别到的本机时区解释。")
            selected_date = st.date_input("阳历日期", value=now.date())
            selected_time = st.time_input("阳历时间", value=selected_time)

        if cast_method == CAST_METHOD_LUNAR:
            st.markdown("#### 农历月日时辰")
            col_month, col_leap, col_day = st.columns([1, 1, 1])
            lunar_month = col_month.number_input("农历月", min_value=1, max_value=12, value=1, step=1)
            manual_is_leap_month = col_leap.checkbox("是否闰月", value=False)
            lunar_day = col_day.number_input("农历日", min_value=1, max_value=30, value=1, step=1)
            branch_label = st.selectbox("时辰", list(BRANCH_LABEL_TO_ENUM.keys()), index=0)
            st.caption("闰月仅用于展示；小六壬算法默认按同名月份计算。")

        submitted = st.form_submit_button("开始起课", type="primary", use_container_width=True)

    render_learning_section()

    if submitted:
        try:
            result, time_source, actual_timezone, time_warning = resolve_cast_request(
                cast_method=cast_method,
                night_zi_changes_day=night_zi_changes_day,
                topic=topic_map[selected_topic_label],
                question=question,
                browser_time_info=browser_time_info,
                selected_date=selected_date,
                selected_time=selected_time,
                lunar_month=int(lunar_month),
                lunar_day=int(lunar_day),
                manual_is_leap_month=manual_is_leap_month,
                branch_label=branch_label,
            )
        except DivinationInputError as exc:
            st.error(str(exc))
        else:
            st.caption(f"当前实际使用的时间来源：{time_source}")
            if time_warning:
                st.info(time_warning)
            render_result(result)


if __name__ == "__main__":
    main()
