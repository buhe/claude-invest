#!/usr/bin/env python3
"""
步骤5：港股差异知识补充
生成8条A股vs港股财报核心差异知识切片
"""
import json

HK_DIFF_SLICES = [
    {
        "rule_id": "R_HK001",
        "category": "会计准则差异",
        "market": ["港股", "A股"],
        "rule_name": "会计准则差异概览",
        "trigger_condition": "分析港股上市公司时，需确认其采用的会计准则（HKFRS/IFRS vs CAS/US GAAP）",
        "verdict": "不同准则下财报数据口径不同，直接比较需统一准则基础。港股上市公司通常采用HKFRS（香港财务报告准则，等同IFRS）或US GAAP。",
        "severity": "info",
        "reference_quote": "港股公司多采用HKFRS或US GAAP，与A股的CAS（中国会计准则）在收入确认、资产计量等关键问题上存在差异，分析时需注明准则类型。"
    },
    {
        "rule_id": "R_HK002",
        "category": "存货计价",
        "market": ["港股"],
        "rule_name": "IFRS禁止LIFO，港股存货计价与A股差异",
        "trigger_condition": "港股采用IFRS准则，公司不得使用LIFO（后进先出）法核算存货",
        "verdict": "IFRS禁止LIFO，意味着港股公司只能用FIFO（先进先出）或加权平均法。在通胀环境下，LIFO和FIFO的利润差异会显现，需注意。",
        "severity": "info",
        "reference_quote": "IFRS禁止LIFO，CAS允许LIFO，差异对利润的影响在通胀时期尤为显著。"
    },
    {
        "rule_id": "R_HK003",
        "category": "资产减值",
        "market": ["港股"],
        "rule_name": "IFRS全资产减值测试 vs A股特定资产减值",
        "trigger_condition": "港股采用IFRS准则，需每年对所有资产进行减值测试（CAS仅对特定资产设定固定计提范围）",
        "verdict": "IFRS减值测试更全面，但主观判断空间也更大。减值转回在IFRS下更灵活（存货和应收账款可转回，商誉不可转回），可能成为调节利润的工具。",
        "severity": "info",
        "reference_quote": "HKFRS要求每年对所有资产减值测试，CAS对特定资产设定固定范围。"
    },
    {
        "rule_id": "R_HK004",
        "category": "收入确认",
        "market": ["港股"],
        "rule_name": "IFRS 15履约义务识别 vs CAS时间点/时间间隔法",
        "trigger_condition": "港股采用IFRS 15，需识别单项履约义务，按「时点」或「时段」确认收入；A股CAS 14类似但细节差异较大",
        "verdict": "IFRS 15下同一业务可能确认时点不同，影响收入和利润的确认节奏。软件、游戏、SaaS等新经济业务影响尤为显著。",
        "severity": "info",
        "reference_quote": "IFRS 15的履约义务识别 vs CAS的时间点/时间间隔法，在服务型收入占比高的公司中差异显著。"
    },
    {
        "rule_id": "R_HK005",
        "category": "金融工具披露",
        "market": ["港股"],
        "rule_name": "IFRS对金融工具公允价值披露要求更细",
        "trigger_condition": "港股IFRS下，以公允价值计量的金融资产需分三级披露（Level 1/2/3），CAS披露要求相对简化",
        "verdict": "Level 3公允价值（无活跃市场定价）主观性强，可能被用于利润操纵。需关注公允价值层级分布和变动原因。",
        "severity": "info",
        "reference_quote": "IFRS对公允价值、风险敞口要求更细，CAS相对简化。Level 3公允价值的主观判断空间是潜在风险点。"
    },
    {
        "rule_id": "R_HK006",
        "category": "披露频次",
        "market": ["港股"],
        "rule_name": "港股仅要求中报与年报（无季报强制披露）",
        "trigger_condition": "港股主板仅要求披露半年报和年报，不强制要求季报；A股强制要求季报",
        "verdict": "港股财务信息频率低于A股，分析时需注意数据时效性。半年报数据有限，年报信息最为完整。",
        "severity": "info",
        "reference_quote": "A股强制季报，IFRS仅要求中报与年报，分析时需注明数据局限性。"
    },
    {
        "rule_id": "R_HK007",
        "category": "审计意见",
        "market": ["港股"],
        "rule_name": "港股/国际审计报告意见类型术语对照",
        "trigger_condition": "港股审计报告使用国际审计准则，意见类型：Unqualified（无保留）/ Qualified（保留）/ Adverse（否定）/ Disclaimer（无法表示）",
        "verdict": "与A股审计意见分类基本对应，但措辞为英文，需准确理解其严重程度。Unqualified with emphasis of matter（强调事项）不同于标准无保留，需结合具体事项判断。",
        "severity": "high",
        "reference_quote": "英文审计报告中各意见类型的判定：Unqualified/Qualified/Adverse/Disclaimer，重要性依次递增。"
    },
    {
        "rule_id": "R_HK008",
        "category": "增值税差异",
        "market": ["港股"],
        "rule_name": "港股无增值税，销售收现比参考基准下调至1.0",
        "trigger_condition": "香港地区不征收增值税/营业税，港股公司财报中的'销售商品收到现金/营业收入'比值参考基准应从A股的1.13下调至1.0",
        "verdict": "港股无增值税因素，销售收现比基准为1.0。若持续低于1.0，说明现金回收能力弱，需结合应收账款进一步分析。",
        "severity": "medium",
        "reference_quote": "港股无增值税，港股财报中'销售商品收到现金/营业收入'比值的参考基准应下调至接近1.0。"
    },
]

# 保存为切片格式
hk_slices = []
for i, r in enumerate(HK_DIFF_SLICES):
    slice_id = f"HK_DIFF_{i+1:03d}"
    hk_slices.append({
        "slice_id": slice_id,
        "book": "港股差异知识",
        "chapter": "港股vsA股财报差异",
        "section": r['category'],
        "content": f"【{r['rule_name']}】{r.get('reference_quote', r.get('verdict', ''))}\n\n具体内容：{r['verdict']}\n\n触发条件：{r['trigger_condition']}",
        "word_count": len(f"【{r['rule_name']}】{r.get('reference_quote', '')}\n\n具体内容：{r['verdict']}\n\n触发条件：{r['trigger_condition']}"),
        "tags": {
            "market_diff": "港股差异",
            "dimension": r['category'],
            "stage": "综合分析",
            "severity": r['severity']
        }
    })

output_path = "/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/slices_hk_diff.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for sl in hk_slices:
        f.write(json.dumps(sl, ensure_ascii=False) + '\n')

print(f"=== 港股差异切片统计 ===")
print(f"总切片数: {len(hk_slices)}")
for sl in hk_slices:
    print(f"  [{sl['slice_id']}] {sl['section']}")
print(f"\n已保存: {output_path}")
