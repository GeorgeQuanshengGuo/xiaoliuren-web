from __future__ import annotations

from xiaoliuren.engine import cast_from_lunar_input
from xiaoliuren.llm_prompt import build_llm_interpretation_prompt
from xiaoliuren.models import EarthlyBranch, Topic


def test_llm_prompt_contains_core_result_fields() -> None:
    result = cast_from_lunar_input(
        lunar_month=6,
        lunar_day=5,
        branch=EarthlyBranch.SI,
        topic=Topic.WEALTH,
        question="最近是否适合推进一个副业收入机会？",
    )

    prompt = build_llm_interpretation_prompt(result)

    assert "最近是否适合推进一个副业收入机会？" in prompt
    assert "财运/求财" in prompt
    assert "最终六神：速喜" in prompt
    assert "农历月：6 月" in prompt
    assert "农历日：5 日" in prompt
    assert "时辰：巳时" in prompt
    assert "建议行动" in prompt
    assert "避免事项" in prompt
    assert "不替代医疗、法律、投资等专业建议" in prompt


def test_llm_prompt_includes_lost_item_extra_sections() -> None:
    result = cast_from_lunar_input(
        lunar_month=3,
        lunar_day=5,
        branch=EarthlyBranch.CHEN,
        topic=Topic.LOST_ITEM,
        question="钥匙放在哪里了？",
    )

    prompt = build_llm_interpretation_prompt(result)

    assert "寻找方向：" in prompt
    assert "搜索策略：" in prompt
    assert "钥匙放在哪里了？" in prompt
