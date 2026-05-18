from __future__ import annotations

import pytest

from xiaoliuren.interpretations import get_interpretation
from xiaoliuren.models import SixSign, Topic


@pytest.mark.parametrize("topic", list(Topic))
@pytest.mark.parametrize("sign", list(SixSign))
def test_all_topic_and_sign_combinations_return_interpretation(
    topic: Topic,
    sign: SixSign,
) -> None:
    interpretation = get_interpretation(sign, topic)

    assert interpretation.summary.strip()
    assert interpretation.detail.strip()
    assert interpretation.overview.strip()
    assert interpretation.current_situation.strip()
    assert interpretation.question_meaning.strip()
    assert isinstance(interpretation.suggested_actions, list)
    assert isinstance(interpretation.avoid_actions, list)
    assert interpretation.suggested_actions
    assert interpretation.avoid_actions
    assert interpretation.review_prompt.strip()


def test_health_state_contains_medical_diagnosis_notice() -> None:
    interpretation = get_interpretation(SixSign.DA_AN, Topic.HEALTH_STATE)

    assert "不替代医疗诊断" in interpretation.question_meaning
    assert "有不适" in interpretation.question_meaning
    assert "咨询医生" in interpretation.question_meaning


@pytest.mark.parametrize("sign", list(SixSign))
@pytest.mark.parametrize("topic", list(Topic))
def test_interpretation_avoids_sensitive_absolute_words(
    topic: Topic,
    sign: SixSign,
) -> None:
    interpretation = get_interpretation(sign, topic)
    combined_text = " ".join(
        [
            interpretation.summary,
            interpretation.detail,
            interpretation.overview,
            interpretation.current_situation,
            interpretation.question_meaning,
            *interpretation.suggested_actions,
            *interpretation.avoid_actions,
            interpretation.review_prompt,
        ]
    )

    banned_words = ["稳赚", "保证", "百分百准确", "必然", "一定发财", "一定分手"]
    for word in banned_words:
        assert word not in combined_text


@pytest.mark.parametrize("sign", list(SixSign))
def test_wealth_interpretation_emphasizes_risk_without_profit_promise(sign: SixSign) -> None:
    interpretation = get_interpretation(sign, Topic.WEALTH)

    assert "现金流" in interpretation.question_meaning
    assert "风险" in " ".join([interpretation.question_meaning, *interpretation.suggested_actions])


def test_cooperation_contract_contains_legal_notice() -> None:
    interpretation = get_interpretation(SixSign.CHI_KOU, Topic.COOPERATION_CONTRACT)

    assert "不替代法律意见" in interpretation.question_meaning
    assert "重要合同请咨询专业人士" in " ".join(
        [interpretation.question_meaning, *interpretation.suggested_actions]
    )


@pytest.mark.parametrize(
    ("sign", "expected_text"),
    [
        (SixSign.DA_AN, "原处"),
        (SixSign.LIU_LIAN, "夹住"),
        (SixSign.SU_XI, "刚刚经过处"),
        (SixSign.CHI_KOU, "误拿"),
        (SixSign.XIAO_JI, "多查一层"),
        (SixSign.KONG_WANG, "不在预想位置"),
    ],
)
def test_lost_item_directional_advice(sign: SixSign, expected_text: str) -> None:
    interpretation = get_interpretation(sign, Topic.LOST_ITEM)

    assert expected_text in interpretation.question_meaning


@pytest.mark.parametrize("sign", list(SixSign))
def test_lost_item_has_location_hint_and_search_strategy(sign: SixSign) -> None:
    interpretation = get_interpretation(sign, Topic.LOST_ITEM)

    assert interpretation.likely_location_hint
    assert interpretation.search_strategy
    assert interpretation.caution
    assert "一定能找到" not in " ".join(
        [
            interpretation.summary,
            interpretation.detail,
            interpretation.likely_location_hint,
            interpretation.search_strategy,
            interpretation.caution,
        ]
    )


def test_custom_topic_returns_normally() -> None:
    interpretation = get_interpretation(
        SixSign.XIAO_JI,
        Topic.CUSTOM,
        question="这件事适不适合继续推进？",
    )

    assert "自定义问题" in interpretation.summary
    assert "这件事适不适合继续推进？" in interpretation.summary
    assert interpretation.detail
