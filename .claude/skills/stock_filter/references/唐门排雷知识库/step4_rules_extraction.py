#!/usr/bin/env python3
"""
步骤4：疑点规则抽取
从唐书房方法论中提炼20+条可计算的排雷规则
"""
import json

# ===== 疑点规则库 =====
# 基于《手把手教你读财报》《价值投资实战手册》核心方法论
# 每条规则的trigger_condition描述为可直接计算/判断的条件

RULES = [
    # ===== 应收账款（4条）=====
    {
        "rule_id": "R001",
        "category": "应收账款",
        "market": ["A股", "港股"],
        "rule_name": "应收增速 vs 营收增速背离",
        "trigger_condition": "连续2年应收账款同比增长率 > 营业收入同比增长率，且差额超过10个百分点",
        "verdict": "应收增速持续高于营收，说明利润含金量低，存在虚增收入嫌疑",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》应收账款章节",
        "reference_quote": "应收账款增速长期高于营业收入增速，说明公司确认的营业收入并没有变成真金白银。"
    },
    {
        "rule_id": "R002",
        "category": "应收账款",
        "market": ["A股"],
        "rule_name": "应收账款/营业收入比例超30%警戒线",
        "trigger_condition": "应收账款期末余额 / 当期营业收入 > 0.30（30%）",
        "verdict": "超过30%说明公司对客户谈判能力极弱，或收入确认激进，需深入调查",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》应收账款章节",
        "reference_quote": "应收账款占营收比例超过30%就需要警惕，超过50%说明公司对客户谈判能力极弱，或者收入确认存在激进化倾向。"
    },
    {
        "rule_id": "R003",
        "category": "应收账款",
        "market": ["A股", "港股"],
        "rule_name": "应收/营收超100%（极高风险）",
        "trigger_condition": "应收账款期末余额 / 当期营业收入 > 1.0（100%）",
        "verdict": "极高风险。账面收入几乎全部是'白条'，利润几乎全是纸面利润，需立即排查",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》应收账款章节",
        "reference_quote": "应收账款/营业收入超过100%意味着利润几乎是纸面利润，是典型的财务异常信号。"
    },
    {
        "rule_id": "R004",
        "category": "应收账款",
        "market": ["A股"],
        "rule_name": "1年以上应收账款占比异常增长",
        "trigger_condition": "1年以上应收账款期末余额 / 应收账款总余额 > 0.20（20%），或占比同比上升超过5个百分点",
        "verdict": "账龄结构恶化，老账堆积，说明客户还款意愿弱或公司放宽信用政策，可能存在虚构客户",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》应收账款章节",
        "reference_quote": "一年以上的应收账款大幅增长，往往意味着公司放宽了信用政策，甚至可能存在虚构客户的情况。"
    },

    # ===== 存货（3条）=====
    {
        "rule_id": "R005",
        "category": "存货",
        "market": ["A股", "港股"],
        "rule_name": "存货激增而营收未同步增长",
        "trigger_condition": "存货同比增长率 > 营业收入同比增长率 + 15个百分点",
        "verdict": "存货增速远超营收，可能存在滞销、积压或虚构存货，需结合毛利率综合判断",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》存货章节",
        "reference_quote": "存货里的猫腻：一是存货金额异常增长，二是存货跌价准备计提不充分，三是存货周转天数明显延长。"
    },
    {
        "rule_id": "R006",
        "category": "存货",
        "market": ["A股"],
        "rule_name": "存货跌价准备计提不足",
        "trigger_condition": "存货跌价准备期末余额 / 存货期末余额 < 同行可比公司平均值 - 2个百分点，或突然大幅减少",
        "verdict": "与同行相比计提不足，意味着未来可能集中计提跌价损失，侵蚀利润",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》存货章节",
        "reference_quote": "存货跌价准备计提不充分，是上市公司调节利润的常见手段。"
    },
    {
        "rule_id": "R007",
        "category": "存货",
        "market": ["A股", "港股"],
        "rule_name": "存货周转天数显著延长",
        "trigger_condition": "存货周转天数同比增加超过30天，或超过同行平均2倍",
        "verdict": "周转天数延长反映变现速度下降，可能滞销或产品竞争力下降",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》存货章节",
        "reference_quote": "存货周转天数明显延长，往往意味着产品滞销或竞争力下降。"
    },

    # ===== 商誉（2条）=====
    {
        "rule_id": "R008",
        "category": "商誉",
        "market": ["A股", "港股"],
        "rule_name": "商誉占净资产比例超30%",
        "trigger_condition": "商誉期末余额 / 净资产期末余额 > 0.30（30%）",
        "verdict": "商誉占比过高，存在减值测试不足或大幅计提减值的风险",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》商誉章节",
        "reference_quote": "商誉占净资产比例过高是风险信号，更需要警惕的是该减值而不减值的情况。"
    },
    {
        "rule_id": "R009",
        "category": "商誉",
        "market": ["A股"],
        "rule_name": "被收购公司业绩不达标但商誉未减值",
        "trigger_condition": "被收购标的当年实际业绩 < 收购时盈利预测，且商誉未计提减值准备",
        "verdict": "业绩不达标但减值未计提，说明减值测试流于形式，未来集中爆雷风险大",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》商誉章节",
        "reference_quote": "更危险的是被收购企业业绩不达标，但商誉却迟迟不减值，这是财务造假的重灾区。"
    },

    # ===== 货币资金/存贷双高（3条）=====
    {
        "rule_id": "R010",
        "category": "货币资金",
        "market": ["A股"],
        "rule_name": "存贷双高（A股）",
        "trigger_condition": "货币资金 > 有息负债（短期借款+长期借款+应付债券）> 0，且利息支出 / 有息负债 > 5%",
        "verdict": "同时拥有巨额货币资金和巨额有息负债，是康得新等造假公司的典型特征",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》货币资金章节",
        "reference_quote": "康得新账面显示拥有巨额货币资金，同时又有巨额有息负债，利息支出高昂，这是典型的'存贷双高'，最终证明货币资金是虚构的。"
    },
    {
        "rule_id": "R011",
        "category": "货币资金",
        "market": ["A股", "港股"],
        "rule_name": "利息收入与货币资金规模不匹配",
        "trigger_condition": "利息收入 / 货币资金平均余额 < 1.5%（年化利率低于1.5%），且货币资金 > 5亿元",
        "verdict": "货币资金收益率极低，可能存在资金被占用、冻结或虚构的情况",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》货币资金章节",
        "reference_quote": "利息收入与货币资金规模不匹配，说明账面货币资金可能并不真实存在。"
    },
    {
        "rule_id": "R012",
        "category": "货币资金",
        "market": ["A股"],
        "rule_name": "受限资金占比过高",
        "trigger_condition": "（质押/冻结/受限货币资金）/ 货币资金总余额 > 0.50（50%）",
        "verdict": "一半以上资金受限，实际可动用资金极少，流动性风险极高",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》货币资金章节",
        "reference_quote": "大量货币资金处于受限状态，意味着公司表面富裕实际拮据。"
    },

    # ===== 经营现金流（3条）=====
    {
        "rule_id": "R013",
        "category": "经营现金流",
        "market": ["A股", "港股"],
        "rule_name": "经营现金流净额/净利润持续小于1",
        "trigger_condition": "连续3年经营现金流净额 / 净利润 < 1.0",
        "verdict": "利润长年无法转化为现金，是纸面利润的典型特征，需要追问原因",
        "severity": "high",
        "source_chapter": "《价值投资实战手册》利润真实性章节",
        "reference_quote": "连续多年经营现金流净额/净利润小于1，说明利润含金量低，甚至是纸面利润。经营现金流才是检验利润真实性的试金石。"
    },
    {
        "rule_id": "R014",
        "category": "经营现金流",
        "market": ["A股"],
        "rule_name": "销售商品收到现金/营业收入持续低于1.13（A股）",
        "trigger_condition": "连续2年（销售商品、提供劳务收到的现金）/ 营业收入 < 1.13",
        "verdict": "大量款项未收回，应收持续膨胀，营收质量低",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》现金流量表章节",
        "reference_quote": "销售商品收到现金/营业收入持续远低于1.13（考虑增值税），说明大量款项未收回，应收账款还在膨胀。"
    },
    {
        "rule_id": "R015",
        "category": "经营现金流",
        "market": ["港股"],
        "rule_name": "销售商品收到现金/营业收入低于1.0（港股）",
        "trigger_condition": "连续2年（销售商品、提供劳务收到的现金）/ 营业收入 < 1.0（港股无增值税）",
        "verdict": "港股无增值税参考基准为1.0，持续低于1说明现金回收能力弱",
        "severity": "medium",
        "source_chapter": "港股差异知识",
        "reference_quote": "港股无增值税，港股财报中'销售商品收到现金/营业收入'比值的参考基准应下调至接近1.0。"
    },

    # ===== 利润质量（3条）=====
    {
        "rule_id": "R016",
        "category": "利润质量",
        "market": ["A股", "港股"],
        "rule_name": "非经常性损益占净利润比重过高",
        "trigger_condition": "非经常性损益净额 / 净利润 > 0.30（30%），或同比大幅上升",
        "verdict": "利润过度依赖非经常性损益，主营业务盈利能力弱，利润不可持续",
        "severity": "medium",
        "source_chapter": "《价值投资实战手册》利润真实性章节",
        "reference_quote": "非经常性损益占净利润比重过高，说明利润质量低，主营业务不赚钱，靠偶然性收益维持。"
    },
    {
        "rule_id": "R017",
        "category": "利润质量",
        "market": ["A股", "港股"],
        "rule_name": "毛利率异常波动（无合理解释）",
        "trigger_condition": "毛利率较上年变化超过10个百分点，且无法从原材料价格、产品结构变化、汇率等找到合理解释",
        "verdict": "毛利率大起大落需警惕，可能是收入跨期确认、成本虚减或业务造假",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》利润表章节",
        "reference_quote": "毛利率明显高于同行业，或自身出现无法解释的大幅波动，往往有妖。"
    },
    {
        "rule_id": "R018",
        "category": "利润质量",
        "market": ["A股", "港股"],
        "rule_name": "费用率与营收变动方向背离",
        "trigger_condition": "营收同比增长 > 10%，但管理费用率或销售费用率同比下降超过5个百分点",
        "verdict": "营收大幅增长而费用率反而下降，异常节约可能意味着费用被资本化或跨期调节",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》利润表章节",
        "reference_quote": "费用率异常波动，尤其是营收未大幅增长的情况下费用率剧烈变化，需要警惕是否存在费用资本化、跨期调节等问题。"
    },

    # ===== 审计与治理（2条）=====
    {
        "rule_id": "R019",
        "category": "审计意见",
        "market": ["A股", "港股"],
        "rule_name": "审计意见非标准无保留",
        "trigger_condition": "审计报告意见类型 ≠ '标准无保留意见'（即：保留意见/无法表示意见/否定意见）",
        "verdict": "非标意见直接反映财务数据可信度存疑，一票否决项",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》审计报告章节",
        "reference_quote": "审计意见是无法表示意见或保留意见，直接一票否决，不必再看。"
    },
    {
        "rule_id": "R020",
        "category": "审计意见",
        "market": ["A股"],
        "rule_name": "频繁更换会计师事务所",
        "trigger_condition": "5年内更换会计师事务所超过2次（含2次），或当年出具非标意见后次年立即更换",
        "verdict": "频繁换所往往意味着公司与审计师在会计处理上存在重大分歧，是危险信号",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》审计报告章节",
        "reference_quote": "频繁更换会计师事务所，是危险信号，往往意味着公司与审计师在会计处理上存在重大分歧。"
    },

    # ===== 大股东与治理（2条）=====
    {
        "rule_id": "R021",
        "category": "大股东行为",
        "market": ["A股"],
        "rule_name": "大股东股权质押比例超50%",
        "trigger_condition": "大股东累计质押股份数 / 大股东持有股份总数 > 0.50（50%）",
        "verdict": "高比例质押后股价下跌可能引发爆仓风险，大股东可能存在资金链紧张或掏空动机",
        "severity": "high",
        "source_chapter": "《价值投资实战手册》公司治理章节",
        "reference_quote": "大股东质押比例过高，往往意味着大股东资金链紧张，有掏空上市公司的动机。"
    },
    {
        "rule_id": "R022",
        "category": "关联交易",
        "market": ["A股", "港股"],
        "rule_name": "关联交易占比畸高",
        "trigger_condition": "关联交易金额 / 营业收入 > 0.30（30%），或关联交易毛利率显著低于非关联交易",
        "verdict": "高度依赖关联交易是利益输送的温床，利润可能被关联方截留",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》关联交易章节",
        "reference_quote": "关联交易占比畸高且定价不公允，是大股东掏空上市公司的常用手段。"
    },
]

# ===== 输出规则库 =====
output_path = "/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/rules_detection.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(RULES, f, ensure_ascii=False, indent=2)

# 统计
from collections import Counter
categories = Counter(r['category'] for r in RULES)
severities = Counter(r['severity'] for r in RULES)

print(f"=== 规则库统计 ===")
print(f"总规则数: {len(RULES)}")
print(f"\n按科目分布:")
for cat, cnt in categories.most_common():
    print(f"  {cat}: {cnt}条")
print(f"\n按风险等级:")
for sev, cnt in severities.most_common():
    print(f"  {sev}: {cnt}条")

# 列出所有规则
print(f"\n规则清单:")
for r in RULES:
    print(f"  [{r['rule_id']}] {r['category']} - {r['rule_name']} (severity={r['severity']})")

print(f"\n已保存: {output_path}")
