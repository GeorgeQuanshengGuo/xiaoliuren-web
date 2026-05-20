from __future__ import annotations

from .models import Interpretation, SixSign, Topic

SIGN_PROFILES: dict[SixSign, dict[str, str]] = {
    SixSign.DA_AN: {
        "base_meaning": "稳定、安定、宜守",
        "element": "木",
        "traditional_image": "取木气生发而有根，主安处、原位、稳定基础。",
        "decision_focus": "重点看是否已有稳定条件，宜守成、整理、巩固。",
        "energy": "气象平和，像事物落在原位，有可依凭的基础。",
        "timing": "节奏偏稳，不宜急催，适合按既定顺序推进。",
        "risk": "风险多在过度求变，或把平稳误读为可以放松管理。",
        "advice": "守住核心目标，先做确定事项，稳中求成。",
    },
    SixSign.LIU_LIAN: {
        "base_meaning": "拖延、反复、纠缠",
        "element": "水",
        "traditional_image": "取水象迂回、暗流、牵连，主等待、迟滞、反复。",
        "decision_focus": "重点看流程卡点、旧账旧事、反复沟通和未完事项。",
        "energy": "气机缠绕，像线头未理顺，事情容易停在等待和反复确认上。",
        "timing": "节奏偏慢，短期内可能需要多一次沟通或补一次材料。",
        "risk": "风险多在拖久生变，或因旧问题未清而牵住新进展。",
        "advice": "放缓判断，整理卡点，把未完事项逐一收束。",
    },
    SixSign.SU_XI: {
        "base_meaning": "快速、有消息、有进展",
        "element": "火",
        "traditional_image": "取火象明亮、迅速、外显，主消息、回应、短期动象。",
        "decision_focus": "重点看新消息、新窗口和可快速确认的线索。",
        "energy": "气机向外，消息流动较快，容易出现回应、线索或转机。",
        "timing": "节奏偏快，适合主动跟进，但仍要核对细节。",
        "risk": "风险多在贪快，听到消息就仓促定案。",
        "advice": "把握窗口，及时确认，行动要快而不乱。",
    },
    SixSign.CHI_KOU: {
        "base_meaning": "口舌、冲突、误会",
        "element": "金",
        "traditional_image": "取金象锋利、边界、裁断，主言语冲突、规则和摩擦。",
        "decision_focus": "重点看话语、证据、边界、责任归属和冲突成本。",
        "energy": "气机带冲，言语、立场和边界容易变成焦点。",
        "timing": "节奏容易被争论打断，适合先澄清事实再推进。",
        "risk": "风险多在表达过重、听错意思、或把小分歧扩大。",
        "advice": "慎言，留痕，先核对事实，再处理情绪。",
    },
    SixSign.XIAO_JI: {
        "base_meaning": "小顺、小成、有转机",
        "element": "木",
        "traditional_image": "取木象生机与和合，主小成、小助力、逐步转顺。",
        "decision_focus": "重点看小范围机会、可验证成果和可借用的支持。",
        "energy": "气机渐开，虽不是大开大合，却有可用的小机会。",
        "timing": "节奏适中，适合先做小范围尝试，再逐步放大。",
        "risk": "风险多在高估小成，或忽略后续执行。",
        "advice": "顺势推进，从小处验证，把转机落实成行动。",
    },
    SixSign.KONG_WANG: {
        "base_meaning": "落空、虚耗、宜核查",
        "element": "土",
        "traditional_image": "取土象承载而空虚，主条件未实、信息缺口、方向待核。",
        "decision_focus": "重点看假设是否站得住、资源是否真实、投入是否虚耗。",
        "energy": "气机不实，像有影而未成形，信息和条件可能不足。",
        "timing": "节奏不宜急进，适合先停一停、查一查。",
        "risk": "风险多在凭想象推进，投入后发现方向并不扎实。",
        "advice": "核查来源，降低消耗，准备备选路径。",
    },
}

TOPIC_DESCRIPTIONS: dict[Topic, str] = {
    Topic.GENERAL: "综合事项重在看确定性、阻力与下一步节奏。",
    Topic.WEALTH: "财运/求财重在核对现金流、合同条款、预算边界和风险承受力；本解读不做收益承诺。",
    Topic.CAREER: "工作/事业重在看任务推进、沟通成本、资源配合与反馈速度。",
    Topic.JOB_SEARCH: "求职重在看岗位匹配、投递节奏、面试反馈、材料准备和后续跟进。",
    Topic.RELATIONSHIP: "感情/关系重在沟通、尊重边界和真实互动，不用于操控对方，也不制造恐惧。",
    Topic.LOST_ITEM: "寻物重在线索回溯、位置判断和是否有人移动过。",
    Topic.TRAVEL: "出行重在时间余量、证件票据、路线变化和途中沟通。",
    Topic.STUDY_EXAM: "学业/考试重在复习节奏、薄弱环节、临场状态和反馈修正。",
    Topic.WAITING_MESSAGE: "消息等待重在回复节奏、流程状态、对方是否需要提醒。",
    Topic.COOPERATION_CONTRACT: "合作/签约重在条款清晰、责任边界、记录留存和专业审阅；本解读不替代法律意见，重要合同请咨询专业人士。",
    Topic.HOME_MOVE: "家宅/搬迁重在居住稳定、家庭协商、手续预算和时间安排。",
    Topic.HEALTH_STATE: "身心状态只作生活状态提醒，不替代医疗诊断；有不适应咨询医生。",
    Topic.CUSTOM: "自定义问题按综合事项处理，重在看当前局势、可行动作和需核查处。",
}

SCENARIO_MEANINGS: dict[Topic, dict[SixSign, str]] = {
    Topic.GENERAL: {
        SixSign.DA_AN: "此事有稳定基础，先守住主线比临时换方向更合适。",
        SixSign.LIU_LIAN: "此事可能卡在旧问题、流程或反复确认中，需要先理顺再推进。",
        SixSign.SU_XI: "此事有较快出现消息或进展的象，适合主动把线索接住。",
        SixSign.CHI_KOU: "此事的阻力多在沟通和立场，先把话说清楚更重要。",
        SixSign.XIAO_JI: "此事有小转机，宜从可控的小步骤开始推进。",
        SixSign.KONG_WANG: "此事目前信息不够扎实，先核查事实比马上行动更稳。",
    },
    Topic.WEALTH: {
        SixSign.DA_AN: "财务面偏稳，适合盘点现金流、整理预算和确认既有收入安排。",
        SixSign.LIU_LIAN: "钱款或合作回款可能有拖延，重点核对账目、合同和付款节点。",
        SixSign.SU_XI: "可能较快出现报价、回款消息或求财线索，但仍需核查来源和条件。",
        SixSign.CHI_KOU: "财务沟通容易因价格、分账或承诺产生摩擦，适合白纸黑字确认。",
        SixSign.XIAO_JI: "有小额进账或资源互助的机会，适合小步试探，不宜放大预期。",
        SixSign.KONG_WANG: "财务信息可能不完整，需先查现金流、成本、合同和潜在风险。",
    },
    Topic.CAREER: {
        SixSign.DA_AN: "工作局面偏稳，适合推进既定任务和维护已有合作关系。",
        SixSign.LIU_LIAN: "任务可能被流程、审批或旧问题拖住，需要拆解卡点。",
        SixSign.SU_XI: "反馈和机会来得较快，适合投递、汇报、约谈或推进沟通。",
        SixSign.CHI_KOU: "职场中容易有误解或争论，表达要清楚，记录要完整。",
        SixSign.XIAO_JI: "有小成果或贵人助力，适合用阶段性成果争取空间。",
        SixSign.KONG_WANG: "方向或职责可能还不清楚，适合先确认目标和边界。",
    },
    Topic.JOB_SEARCH: {
        SixSign.DA_AN: "求职局面偏稳，适合打磨简历、整理作品集、维护已有内推和熟人渠道。",
        SixSign.LIU_LIAN: "求职进度可能卡在筛选、排期或等待反馈上，需要主动梳理投递记录和跟进节点。",
        SixSign.SU_XI: "较容易出现面试邀约、回复或新岗位线索，适合及时投递并快速确认时间安排。",
        SixSign.CHI_KOU: "面试沟通、薪资表达或岗位理解容易出现误差，回答问题要清楚，重要信息要留痕。",
        SixSign.XIAO_JI: "有小机会或阶段性进展，适合先争取面试、试岗、短名单或二面这类下一步。",
        SixSign.KONG_WANG: "岗位信息、招聘真实性或个人匹配度可能还不清楚，适合先核查 JD、公司背景和用人需求。",
    },
    Topic.RELATIONSHIP: {
        SixSign.DA_AN: "关系有安定基础，适合温和表达、稳定陪伴和长期经营。",
        SixSign.LIU_LIAN: "关系中可能有旧情绪或反复讨论的问题，需要耐心倾听。",
        SixSign.SU_XI: "互动回应较快，适合主动表达善意，但不宜逼迫对方表态。",
        SixSign.CHI_KOU: "误会和口气容易放大问题，沟通时先照顾事实和感受。",
        SixSign.XIAO_JI: "关系有小幅缓和或靠近的机会，适合用具体行动建立信任。",
        SixSign.KONG_WANG: "期待可能暂时没有落点，适合把注意力放回真实互动和自我照顾。",
    },
    Topic.LOST_ITEM: {
        SixSign.DA_AN: "多在原处、稳定位置、收纳处，可先查常放位置和固定容器。",
        SixSign.LIU_LIAN: "可能被夹住、遗忘在中途、反复经过之处，宜沿行动路线回看。",
        SixSign.SU_XI: "容易较快找到，先查刚刚经过处、手边区域和临时放置点。",
        SixSign.CHI_KOU: "可能与他人移动、误拿、争执有关，适合温和询问相关人员。",
        SixSign.XIAO_JI: "可找到但需多查一层，注意抽屉内层、袋中袋、遮挡物后方。",
        SixSign.KONG_WANG: "信息不足，可能不在预想位置，先扩大范围并重建最后一次看到的时间线。",
    },
    Topic.TRAVEL: {
        SixSign.DA_AN: "出行条件偏稳，适合按原计划走，并提前确认票据证件。",
        SixSign.LIU_LIAN: "行程可能延误或反复改动，建议预留时间和备用路线。",
        SixSign.SU_XI: "短途或临时出行较容易推进，但要避免因赶时间漏看信息。",
        SixSign.CHI_KOU: "途中沟通、同行意见或票务细节易出摩擦，宜提前说清。",
        SixSign.XIAO_JI: "行程中可能得到小帮助，适合小范围调整后继续前行。",
        SixSign.KONG_WANG: "行程条件不够实，先核查天气、交通、证件和预订状态。",
    },
    Topic.STUDY_EXAM: {
        SixSign.DA_AN: "学习状态适合稳扎稳打，先巩固基础题和固定复习节奏。",
        SixSign.LIU_LIAN: "容易拖延或反复卡在同类问题，适合列出薄弱点逐项补。",
        SixSign.SU_XI: "短期反馈较快，适合刷题、答疑、提交材料或冲刺复盘。",
        SixSign.CHI_KOU: "讨论和考试中要防审题偏差，少争论，多回到题干证据。",
        SixSign.XIAO_JI: "有小进步和转机，适合用阶段目标积累信心。",
        SixSign.KONG_WANG: "目标可能偏虚，先收窄范围，确认考点和优先级。",
    },
    Topic.WAITING_MESSAGE: {
        SixSign.DA_AN: "消息大概率按常规节奏来，适合耐心等待并保持渠道畅通。",
        SixSign.LIU_LIAN: "回复可能拖延或反复确认，适合在合适时间温和提醒。",
        SixSign.SU_XI: "较容易有快讯、回音或通知，适合主动查看常用渠道。",
        SixSign.CHI_KOU: "消息里可能夹带解释、争议或误会，收到后先核对语境。",
        SixSign.XIAO_JI: "会有一点有用线索，可能不是完整答案，但能推动下一步。",
        SixSign.KONG_WANG: "短期消息不够明朗，适合准备备选方案并减少空等。",
    },
    Topic.COOPERATION_CONTRACT: {
        SixSign.DA_AN: "合作基础较稳，适合逐条确认范围、交付和时间表。",
        SixSign.LIU_LIAN: "条款或流程可能反复修改，需耐心审阅版本变化。",
        SixSign.SU_XI: "推进较快，适合抓住沟通窗口，但重要条款仍需专业审阅。",
        SixSign.CHI_KOU: "利益分配、措辞和责任边界易引发争议，沟通记录要完整。",
        SixSign.XIAO_JI: "小规模试合作或阶段性推进较合适，先验证配合度。",
        SixSign.KONG_WANG: "合作条件可能未稳，签署前要核查主体、权责和违约条款。",
    },
    Topic.HOME_MOVE: {
        SixSign.DA_AN: "家宅事务偏稳，适合整理空间、确认手续和按计划推进。",
        SixSign.LIU_LIAN: "搬迁或家务可能被旧物、手续或家人意见拖住。",
        SixSign.SU_XI: "容易较快定下某个安排，适合及时确认时间和资源。",
        SixSign.CHI_KOU: "家人、邻里或合同沟通要温和，避免把小事说重。",
        SixSign.XIAO_JI: "小调整能带来改善，适合先处理最影响日常的一处。",
        SixSign.KONG_WANG: "条件可能尚未落实，先查预算、合同、交接和实际居住需求。",
    },
    Topic.HEALTH_STATE: {
        SixSign.DA_AN: "生活状态偏稳，适合维持规律作息和温和调养。",
        SixSign.LIU_LIAN: "状态可能反复，适合观察诱因、减少熬夜和过度消耗。",
        SixSign.SU_XI: "短期可能感到有改善或收到相关消息，但仍以专业判断为准。",
        SixSign.CHI_KOU: "压力、情绪或沟通冲突可能影响身心感受，适合先降噪。",
        SixSign.XIAO_JI: "有小幅恢复或调整空间，适合从饮食、睡眠、运动的小习惯入手。",
        SixSign.KONG_WANG: "信息不足，不宜自行下结论；记录症状和时间线更有帮助。",
    },
    Topic.CUSTOM: {
        SixSign.DA_AN: "自定义问题以稳定为主，先守住已确定的基础。",
        SixSign.LIU_LIAN: "自定义问题可能有拖延和反复，先理顺旧线索。",
        SixSign.SU_XI: "自定义问题有较快回应或进展，适合主动但保留核查。",
        SixSign.CHI_KOU: "自定义问题的关键在沟通，慎言比抢快更重要。",
        SixSign.XIAO_JI: "自定义问题有小转机，适合从低风险步骤开始。",
        SixSign.KONG_WANG: "自定义问题当前不够明朗，先核查再投入。",
    },
}

SIGN_ACTIONS: dict[SixSign, dict[str, list[str]]] = {
    SixSign.DA_AN: {
        "suggested": ["保持当前节奏", "优先完成确定事项", "把已有资源整理好"],
        "avoid": ["临时大幅转向", "因为表面平稳而忽略跟进"],
    },
    SixSign.LIU_LIAN: {
        "suggested": ["复盘卡点", "补齐资料和记录", "给流程预留缓冲"],
        "avoid": ["反复催促", "把未确认的信息当作结论"],
    },
    SixSign.SU_XI: {
        "suggested": ["主动跟进", "及时确认新消息", "把机会落到具体动作"],
        "avoid": ["只求速度忽略细节", "听到消息后仓促定案"],
    },
    SixSign.CHI_KOU: {
        "suggested": ["放慢语气", "把关键事项写清楚", "先核对事实再表达立场"],
        "avoid": ["情绪化回应", "在争执中做重要决定"],
    },
    SixSign.XIAO_JI: {
        "suggested": ["先做小范围尝试", "借助可信资源", "把小成果沉淀下来"],
        "avoid": ["把小顺利看成全面完成", "忽略后续执行"],
    },
    SixSign.KONG_WANG: {
        "suggested": ["核查来源", "降低无谓消耗", "准备备选路径"],
        "avoid": ["基于猜测加码", "忽视条件缺口"],
    },
}

TOPIC_ACTIONS: dict[Topic, dict[str, list[str]]] = {
    Topic.WEALTH: {
        "suggested": ["核对现金流、合同、付款节点和风险边界"],
        "avoid": ["把解读当作投资依据", "忽略成本和最坏情况"],
    },
    Topic.JOB_SEARCH: {
        "suggested": ["更新简历和作品集", "记录投递渠道、岗位要求和跟进时间", "准备面试中的项目案例和薪资边界"],
        "avoid": ["海投后不复盘", "忽略岗位真实性和用人需求", "在未确认条件前过早做决定"],
    },
    Topic.RELATIONSHIP: {
        "suggested": ["用清楚、尊重的方式表达真实想法"],
        "avoid": ["试图操控对方反应", "用猜测制造压力"],
    },
    Topic.LOST_ITEM: {
        "suggested": ["按最后一次看到物品的时间线回溯"],
        "avoid": ["一开始就扩大搜索到无关区域"],
    },
    Topic.HEALTH_STATE: {
        "suggested": ["记录作息、压力和身体感受", "有不适时咨询医生"],
        "avoid": ["自行替代专业诊疗", "忽视持续或加重的不适"],
    },
    Topic.COOPERATION_CONTRACT: {
        "suggested": ["保留书面记录并核对条款", "重要合同请咨询专业人士"],
        "avoid": ["把解读当成法律意见", "未看清权责就推进签署"],
    },
}


LOST_ITEM_HINTS: dict[SixSign, dict[str, str]] = {
    SixSign.DA_AN: {
        "likely_location_hint": "优先看原处、固定位置、常用收纳处，也留意被衣物、纸张、盒盖等遮挡的位置。",
        "search_strategy": "先回到物品平时最稳定的放置点，从桌面、抽屉、柜格、包内固定夹层依次检查，不急着扩大范围。",
        "caution": "不要因为第一眼没看到就判定不在原处，先移开遮挡物，再查一遍固定收纳区。",
    },
    SixSign.LIU_LIAN: {
        "likely_location_hint": "多留意中途停留处、夹层、反复经过的地方，可能拖一拖才显出线索。",
        "search_strategy": "按行动路线倒推，重点查座椅缝、书本文件夹层、外套口袋、转场时临时放下的台面。",
        "caution": "避免一边找一边换路线，先把走过的路径完整复盘，否则容易反复遗漏同一处。",
    },
    SixSign.SU_XI: {
        "likely_location_hint": "线索偏近，先看刚离开的位置、最近使用处、手边区域，较快有线索的可能性较高。",
        "search_strategy": "立刻检查最近三处活动点，例如刚坐过的位置、刚用过的包、刚经过的门口或柜台。",
        "caution": "动作可以快，但不要边找边移动太多物品，以免把原本清楚的线索打乱。",
    },
    SixSign.CHI_KOU: {
        "likely_location_hint": "可能与他人误拿、沟通争执、公共区域有关，也可能在被多人接触过的位置。",
        "search_strategy": "温和询问同桌、家人、同事或前台，核对是否有人帮忙收起、挪动或误拿。",
        "caution": "询问时避免带责备口气，先说清物品特征和最后出现位置，减少不必要的不快。",
    },
    SixSign.XIAO_JI: {
        "likely_location_hint": "位置多半不远，适合在小范围内多查一层，如袋中袋、抽屉内侧、遮挡物后方。",
        "search_strategy": "以最后使用点为中心画小范围，逐格检查桌面下方、包内暗袋、柜内第二层和物品背后。",
        "caution": "不要只看表层；此象重在细查，容易在多翻一层后出现线索。",
    },
    SixSign.KONG_WANG: {
        "likely_location_hint": "预设方向可能有误，当前信息不足，物品可能不在最先想到的位置。",
        "search_strategy": "先重建行动路径：何时最后看到、之后去了哪里、谁接触过，再按时间线重新划定搜索范围。",
        "caution": "不要只围着单一地点消耗时间；先补全信息，再决定扩大或转移搜索方向。",
    },
}


def _normalize_topic(topic: Topic | str) -> Topic:
    if isinstance(topic, Topic):
        return topic
    for item in Topic:
        if topic in {item.key, item.name, item.label}:
            return item
    raise ValueError(f"未知主题：{topic}")


def _merge_actions(sign: SixSign, topic: Topic, action_type: str) -> list[str]:
    topic_actions = TOPIC_ACTIONS.get(topic, {"suggested": [], "avoid": []})
    return [
        *SIGN_ACTIONS[sign][action_type],
        *topic_actions["suggested" if action_type == "suggested" else "avoid"],
    ]


def get_interpretation(
    sign: SixSign,
    topic: Topic | str,
    question: str | None = None,
) -> Interpretation:
    normalized_topic = _normalize_topic(topic)
    profile = SIGN_PROFILES[sign]
    topic_description = TOPIC_DESCRIPTIONS[normalized_topic]
    scenario_meaning = SCENARIO_MEANINGS[normalized_topic][sign]
    clean_question = question.strip() if question and question.strip() else ""
    question_prefix = f"针对“{clean_question}”，" if clean_question else ""

    overview = f"{question_prefix}{normalized_topic.label}得{sign.value}。{profile['base_meaning']}。"
    current_situation = (
        f"{sign.value}常见取象属{profile['element']}，{profile['traditional_image']}"
        f"本课气象为：{profile['energy']}"
        f"时间节奏上，{profile['timing']}"
        f"判断重点是：{profile['decision_focus']}"
        f"需要留意的是，{profile['risk']}"
    )
    question_meaning = (
        f"{topic_description}{scenario_meaning}"
        "这里的解读重点不是给出单一结论，而是把当前问题拆成节奏、阻力、"
        "可行动作和需要复核的条件。"
    )
    detail = (
        f"结果总览：{overview}\n\n"
        f"当前局势：{current_situation}\n\n"
        f"对这个问题的含义：{question_meaning}"
    )
    review_prompt = (
        "事后可复盘：实际进展是否符合此课提示的节奏、风险点是否出现、"
        "采取的行动是否让局面更清楚。"
    )
    lost_item_hint = (
        LOST_ITEM_HINTS[sign]
        if normalized_topic == Topic.LOST_ITEM
        else {"likely_location_hint": None, "search_strategy": None, "caution": None}
    )

    return Interpretation(
        summary=overview,
        detail=detail,
        overview=overview,
        current_situation=current_situation,
        question_meaning=question_meaning,
        suggested_actions=_merge_actions(sign, normalized_topic, "suggested"),
        avoid_actions=_merge_actions(sign, normalized_topic, "avoid"),
        review_prompt=review_prompt,
        likely_location_hint=lost_item_hint["likely_location_hint"],
        search_strategy=lost_item_hint["search_strategy"],
        caution=lost_item_hint["caution"],
    )
