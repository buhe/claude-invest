#!/usr/bin/env python3
"""从《手把手教你读财报》抽取更多规则，扩充rules_detection.json"""
import json
from pathlib import Path

OUTPUT_DIR = Path("/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库")

with open(OUTPUT_DIR / "rules_detection.json") as f:
    existing = json.load(f)

# rules_detection.json是列表而非dict
if isinstance(existing, dict):
    existing_rules = existing.get("rules", [])
else:
    existing_rules = existing

existing_ids = {r["rule_id"] for r in existing_rules}

new_rules = [
    {
        "rule_id": "R023",
        "category": "应收账款",
        "market": ["A股"],
        "rule_name": "应收账款/营业收入比例超30%警戒线",
        "trigger_condition": "应收账款账面价值 / 营业收入 > 0.3（全年累计），或应收回款天数超过100天",
        "verdict": "应收账款占营收比过高，可能是放宽信用政策刺激销售，或存在虚构收入。需结合行业特性判断，制造业超过30%即需警惕。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 经营相关资产",
        "reference_quote": "如果一家公司应收账款占收入的比例过大，要么是行业竞争激烈，要么是公司采用了过于宽松的销售政策。"
    },
    {
        "rule_id": "R024",
        "category": "应收账款",
        "market": ["A股"],
        "rule_name": "1年以上长账龄应收账款大幅增长",
        "trigger_condition": "1年以上应收账款余额同比增幅超过50%，或1年以上占比超过应收账款总额的20%",
        "verdict": "长账龄应收账款激增，往往是公司放宽信用政策催收不利，或存在虚构应收账款（未真实发生销售）。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 经营相关资产",
        "reference_quote": "应收账款的账龄结构同样值得关心。如果1年以上的应收账款占比明显上升，说明公司催收不力，或者存在虚构应收账款的可能。"
    },
    {
        "rule_id": "R025",
        "category": "应收账款",
        "market": ["A股"],
        "rule_name": "坏账准备计提政策突然变更",
        "trigger_condition": "当年坏账计提政策（计提比例）发生重大变更，且变更方向为减少计提",
        "verdict": "坏账计提政策变更是利润操纵的常用手段。减少坏账计提可直接增加当期利润，需重点关注。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 经营相关资产",
        "reference_quote": "需要警惕那些改了会计估计（或会计政策）的上市公司。"
    },
    {
        "rule_id": "R026",
        "category": "营业收入",
        "market": ["A股"],
        "rule_name": "第四季度营收占比异常偏高",
        "trigger_condition": "第四季度营业收入占全年比重超过35%（行业平均约25%），且无明显季节性原因",
        "verdict": "Q4营收占比异常高，可能是公司在Q4集中确认收入，甚至虚构Q4销售。是收入造假的常见手法之一。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第三章 利润表",
        "reference_quote": "投资者需要警惕那些季度之间收入分布极不均匀的公司，尤其是Q4收入占比明显偏高的。"
    },
    {
        "rule_id": "R027",
        "category": "毛利率",
        "market": ["A股"],
        "rule_name": "毛利率明显高于行业平均水平且无合理解释",
        "trigger_condition": "毛利率比同行业第二名高出20个百分点以上，且无专利技术、特许经营权、品牌溢价等合理解释",
        "verdict": "毛利率异常高是财报造假的重要信号。需要有真实的竞争优势支撑，否则可能存在虚构收入或转移成本。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第三章 利润表",
        "reference_quote": "毛利率异常，往往有妖。如果一家公司毛利率远高于同行，没有特别的竞争优势支撑，则需要高度警惕。"
    },
    {
        "rule_id": "R028",
        "category": "存货",
        "market": ["A股"],
        "rule_name": "存货增长显著高于营收增长",
        "trigger_condition": "存货账面价值同比增幅 - 营业收入同比增幅 > 20个百分点，连续两年以上",
        "verdict": "存货增速远超营收，可能存在虚构采购、存货积压滞销、或通过虚构存货套取资金。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 生产相关资产",
        "reference_quote": "如果一家公司存货的增长速度显著高于营业收入的增长，需要警惕。"
    },
    {
        "rule_id": "R029",
        "category": "货币资金",
        "market": ["A股"],
        "rule_name": "货币资金收益率显著低于七天通知存款利率",
        "trigger_condition": "利息收入 / 货币资金平均余额 < 0.5%（即货币资金收益率低于0.5%），且货币资金规模较大（>10亿）",
        "verdict": "货币资金收益率偏低，可能存在虚增货币资金（账户资金被冻结或虚构），或资金已被大股东占用。需排查康得新式存贷双高风险。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 货币资金",
        "reference_quote": "如果公司账上有大量货币资金，却产生很少的利息收入，需要怀疑这笔货币资金的真实性。"
    },
    {
        "rule_id": "R030",
        "category": "固定资产",
        "market": ["A股"],
        "rule_name": "固定资产规模异常庞大（制造业）",
        "trigger_condition": "固定资产占总资产比例超过40%，且固定资产周转率（营收/固定资产净值）显著低于行业均值",
        "verdict": "固定资产占比过高意味着公司属于重资产行业，需要大量资本投入维持竞争力。折旧侵蚀利润，现金流压力大。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第二章 生产相关资产",
        "reference_quote": "固定资产是企业竞争壁垒的一部分，但如果固定资产占比过高，且周转率低下，说明公司的资产利用效率存在严重问题。"
    },
    {
        "rule_id": "R031",
        "category": "在建工程",
        "market": ["A股"],
        "rule_name": "在建工程长期不转固定资产",
        "trigger_condition": "在建工程余额超过预算的100%且超期一年以上不竣工结算，或在建工程占总资产比例超过15%且多年不转固",
        "verdict": "在建工程长期不转固可能是为了规避折旧、虚增利润，或将资金通过在建工程转移到体外。需排查资金流向。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 生产相关资产",
        "reference_quote": "在建工程长期不转固定资产，一方面可能是公司规避折旧以维持利润，另一方面也可能是资金实际上已经被转移。"
    },
    {
        "rule_id": "R032",
        "category": "利润质量",
        "market": ["A股"],
        "rule_name": "扣非净利润与净利润差距持续扩大",
        "trigger_condition": "连续3年以上：（净利润 - 扣非净利润）/ 净利润 > 30%，且呈扩大趋势",
        "verdict": "扣非净利润与净利润差距持续扩大，说明公司利润越来越多依赖非经常性损益，主营业务盈利能力在衰退。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第三章 利润表",
        "reference_quote": "非经常性损益可持续性极差，用它来评估企业盈利能力，没有意义。"
    },
    {
        "rule_id": "R033",
        "category": "合并报表",
        "market": ["A股"],
        "rule_name": "母子公司之间存在大量内部交易但未充分抵消",
        "trigger_condition": "合并报表中关联交易占比超过30%，且母公司与子公司利润结构高度不对称",
        "verdict": "内部交易未充分抵消是利润操纵的常见手法。通过高价出售给子公司再合并报表，可以虚增合并收入和利润。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第二章 经营相关资产",
        "reference_quote": "如果一家公司存在大量关联交易，且关联交易定价不透明，就需要高度警惕利润的真实性。"
    },
    {
        "rule_id": "R034",
        "category": "现金流量表",
        "market": ["A股"],
        "rule_name": "筹资活动现金流大进大出",
        "trigger_condition": "筹资活动现金流入和流出同时巨大（均超过经营活动现金流净额的2倍），借款规模持续增长",
        "verdict": "筹资现金流大进大出说明公司高度依赖融资输血，经营活动无法自给，财务风险极高。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第四章 现金流量表",
        "reference_quote": "筹资活动现金流的大进大出，反映了公司对外部资金的依赖程度。如果一家公司长期依赖筹资来维持经营，就需要警惕。"
    },
    {
        "rule_id": "R035",
        "category": "税务数据",
        "market": ["A股"],
        "rule_name": "税收优惠贡献利润占比过高",
        "trigger_condition": "当期所得税费用 / 营业利润 < 10%（即实际税率远低于法定税率15-25%），且无明确的高新技术企业或西部大开发等政策优惠文件",
        "verdict": "如果利润增长不伴随相应税收增长，可能是虚构利润。真实的交易必然伴随税收，而税收优惠需要有真实依据。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第三章 利润表",
        "reference_quote": "如果一家公司利润很高，但几乎不交税，那这个利润的真实性就值得怀疑。"
    },
    {
        "rule_id": "R036",
        "category": "海外业务",
        "market": ["A股"],
        "rule_name": "海外业务占比畸高且利润率异常",
        "trigger_condition": "海外收入占营业收入比例超过50%，且海外业务毛利率远高于国内业务，或海外收入增速远超行业整体增速",
        "verdict": "海外业务难以核查，是虚构收入的高发区。老唐在书中明确指出要警惕这种特征。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第三章 利润表",
        "reference_quote": "如果一家公司有大量收入来自海外，且无法验证，那这部分收入的真实性就很难保证。"
    },
    {
        "rule_id": "R037",
        "category": "大股东行为",
        "market": ["A股"],
        "rule_name": "大股东股权被冻结或质押比例过高",
        "trigger_condition": "大股东股权质押比例超过其持股数量的50%，或大股东股权被司法冻结",
        "verdict": "大股东高比例质押或股权冻结，往往意味着大股东面临资金压力，可能通过关联交易掏空上市公司。",
        "severity": "high",
        "source_chapter": "《手把手教你读财报》第八章 欺诈与反欺诈",
        "reference_quote": "大股东高比例质押是危险信号，意味着大股东在赌上市公司的股价，而这种赌性往往伴随对上市公司利益的侵占。"
    },
    {
        "rule_id": "R038",
        "category": "审计与治理",
        "market": ["A股"],
        "rule_name": "境外收入占主导却由小所审计",
        "trigger_condition": "海外收入占比超过50%，但负责审计的会计师事务所为非知名小所，或审计费用异常低",
        "verdict": "海外收入核查难度大，如果配套的审计资源薄弱，则海外收入的可信度更低。",
        "severity": "medium",
        "source_chapter": "《手把手教你读财报》第八章 欺诈与反欺诈",
        "reference_quote": "对于那些有大量海外业务的公司，审计质量的重要性更为突出。如果审计师能力不足或独立性存疑，财报的可信度会大打折扣。"
    }
]

# 合并新规则
all_rules = existing_rules + [r for r in new_rules if r["rule_id"] not in existing_ids]
rules_detect = {
    "description": "唐门排雷疑点检测规则库——基于唐朝《手把手教你读财报》《价值投资实战手册》两书方法论，针对A股/港股上市公司的财报疑点检测规则。",
    "total_count": len(all_rules),
    "high_risk_count": len([r for r in all_rules if r["severity"] == "high"]),
    "medium_risk_count": len([r for r in all_rules if r["severity"] == "medium"]),
    "rules": all_rules
}

with open(OUTPUT_DIR / "rules_detection.json", "w", encoding="utf-8") as f:
    json.dump(rules_detect, f, ensure_ascii=False, indent=2)

print(f"总规则数: {len(all_rules)}")
print(f"High: {len([r for r in all_rules if r['severity']=='high'])}")
print(f"Medium: {len([r for r in all_rules if r['severity']=='medium'])}")
cats = {}
for r in all_rules:
    cats[r["category"]] = cats.get(r["category"], 0) + 1
print("分类统计:", dict(sorted(cats.items(), key=lambda x: -x[1])))