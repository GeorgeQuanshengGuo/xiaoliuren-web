from __future__ import annotations

from .models import DivinationResult, Topic


def _format_actions(title: str, actions: list[str]) -> str:
    if not actions:
        return f"{title}：无"
    lines = [f"{title}："]
    lines.extend(f"- {action}" for action in actions)
    return "\n".join(lines)


def _format_solar_time(result: DivinationResult) -> str:
    if result.path.solar_datetime is None:
        return "未记录阳历时间"
    timezone = result.path.timezone or "未指定时区"
    return f"{result.path.solar_datetime.strftime('%Y-%m-%d %H:%M:%S')}（{timezone}）"


def build_llm_interpretation_prompt(result: DivinationResult) -> str:
    """Build a copyable prompt for users who want to ask an LLM for extra reading."""
    path = result.path
    question = result.question or "未填写具体问题"
    leap_month_text = "是" if path.is_leap_month else "否"
    lunar_year_text = str(path.lunar_year) if path.lunar_year else "未记录"

    extra_sections: list[str] = []
    if result.topic == Topic.LOST_ITEM:
        if result.likely_location_hint:
            extra_sections.append(f"寻找方向：{result.likely_location_hint}")
        if result.search_strategy:
            extra_sections.append(f"搜索策略：{result.search_strategy}")
        if result.caution:
            extra_sections.append(f"提醒：{result.caution}")

    extra_text = "\n".join(extra_sections) if extra_sections else "无"

    return f"""请你作为传统文化资料整理助手，基于以下“小六壬起课结果”做进一步解读。

请遵守这些要求：
- 只作为传统文化学习与娱乐参考，不替代医疗、法律、投资等专业建议。
- 解读要清楚、克制、有传统文化味道，不使用绝对化或收益承诺表述。
- 请结合用户问题，重点分析当前局势、问题含义、可执行建议、需要避免的做法，以及后续如何复盘。
- 如果信息不足，请明确指出需要补充哪些现实信息。

【用户问题】
{question}

【起课场景】
{result.topic.label}：{result.topic.description}

【起课路径】
- 流派：{path.rule_profile_name}
- 阳历时间：{_format_solar_time(result)}
- 农历年：{lunar_year_text}
- 农历月：{path.lunar_month} 月
- 是否闰月：{leap_month_text}
- 农历日：{path.lunar_day} 日
- 时辰：{path.branch.label}时
- 月位：{path.month_position}
- 日位：{path.day_position}
- 时位：{path.hour_position}
- 最终六神：{result.sign.value}

【本工具给出的基础解释】
结果总览：{result.overview}

当前局势：{result.current_situation}

对这个问题的含义：{result.question_meaning}

{_format_actions("建议行动", result.suggested_actions)}

{_format_actions("避免事项", result.avoid_actions)}

寻物补充：{extra_text}

复盘提示：{result.review_prompt}

请在以上信息基础上，输出一份更细致的分析。建议分为：
1. 总体判断
2. 当前局势
3. 对用户问题的具体含义
4. 可以采取的行动
5. 需要避免的做法
6. 复盘与现实验证方式
"""
