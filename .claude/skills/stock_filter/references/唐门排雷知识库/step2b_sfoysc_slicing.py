#!/usr/bin/env python3
"""
《手把手教你读财报》全文提取 + 章节切片 + 自动打标签
"""
import re, json
from docx import Document
from pathlib import Path

DOCX_PATH = "/Users/flynn/Downloads/手把手教你读财报/手把手教你读财报/手把手教你读财报 财报是用来排除企业的 以一份真实的财报为案例(高清)/手把手教你读财报 财报是用来排除企业的 以一份真实的财报为案例(高清).docx"
OUTPUT_DIR = Path("/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库")

# ============ 标签函数（先定义，供后续使用） ============
def infer_stage(section):
    s = section
    if any(k in s for k in ["欺诈", "操纵", "造假", "反欺诈", "硬伤"]):
        return "硬伤检查"
    if any(k in s for k in ["利润表", "利润", "营收", "毛利率", "费用", "创造利润"]):
        return "利润表分析"
    if any(k in s for k in ["资产负债", "货币资金", "应收", "存货", "商誉", "负债", "资产", "经营相关", "生产相关", "投资相关"]):
        return "资产负债表分析"
    if any(k in s for k in ["现金流", "现金流量", "现金流肖像"]):
        return "现金流分析"
    if any(k in s for k in ["三大前提", "估值", "持续", "重要提示"]):
        return "三大前提判定"
    if any(k in s for k in ["财报附注", "所有者权益", "综合", "财务指标", "鸟瞰"]):
        return "综合分析"
    if any(k in s for k in ["管理层", "董事会", "重要事项", "会计数据", "汇报"]):
        return "综合分析"
    if any(k in s for k in ["读财报", "框架", "准备", "结构"]):
        return "综合分析"
    return "综合分析"

def infer_account_tags(content):
    tags = []
    mapping = [
        ("应收账款", ["应收账款", "应收款项", "坏账计提", "账龄", "应收票据"]),
        ("存货", ["存货", "周转天数", "跌价准备", "在产品"]),
        ("货币资金", ["货币资金", "现金", "银行存款", "存放同业"]),
        ("商誉", ["商誉", "收购", "减值测试", "商誉减值"]),
        ("固定资产", ["固定资产", "折旧", "在建工程", "工程物资"]),
        ("营业收入", ["营业收入", "营收", "销售收入", "销售额", "主营收入"]),
        ("营业成本", ["营业成本", "毛利润", "毛利率", "毛利润率"]),
        ("销售费用", ["销售费用", "市场推广费", "广告费", "促销费"]),
        ("管理费用", ["管理费用", "管理费"]),
        ("财务费用", ["财务费用", "利息支出", "利息收入", "汇兑损益"]),
        ("经营现金流", ["经营现金流", "经营活动现金流净额", "经营活动产生的现金流量净额"]),
        ("投资现金流", ["投资现金流", "购建固定资产", "资本支出", "投资支付的现金"]),
        ("筹资现金流", ["筹资现金流", "融资", "借款", "吸收投资", "分红", "分配股利"]),
        ("资产减值", ["资产减值", "减值准备", "计提减值", "信用减值"]),
        ("非经常性损益", ["非经常性损益", "营业外收入", "营业外支出", "政府补助"]),
        ("关联交易", ["关联交易", "关联销售", "关联采购", "关联方"]),
        ("利润操纵", ["利润操纵", "调节利润", "虚增利润", "虚增收入", "业绩洗澡"]),
    ]
    for tag, keywords in mapping:
        if any(kw in content for kw in keywords):
            tags.append(tag)
    return tags

def infer_risk_tags(content):
    tags = []
    mapping = [
        ("收入造假", ["虚增收入", "虚增营收", "虚构收入", "伪造合同", "虚构业务", "财务造假"]),
        ("资产虚增", ["虚增资产", "资产造假", "虚增利润"]),
        ("现金流异常", ["现金流异常", "经营活动现金流为负", "现金流造假"]),
        ("存贷双高", ["存贷双高", "货币资金和有息负债同时"]),
        ("减值不足", ["减值不足", "该减未减", "未充分计提", "少提减值"]),
        ("关联交易", ["关联交易", "关联方占用", "利益输送", "掏空上市公司"]),
        ("利润操纵", ["利润操纵", "调节利润", "业绩洗澡", "财务洗澡", "大洗澡"]),
        ("海外业务造假", ["海外业务", "境外收入", "税收优惠地"]),
        ("审计收买", ["购买审计意见", "收买会计师", "标准无保留意见"]),
    ]
    for tag, keywords in mapping:
        if any(kw in content for kw in keywords):
            tags.append(tag)
    return tags

def infer_case_tags(content):
    tags = []
    mapping = [
        ("茅台", ["贵州茅台", "茅台股份", "茅台集团", "600519"]),
        ("万福生科", ["万福生科", "万福生科造假"]),
        ("蓝田股份", ["蓝田股份", "蓝田"]),
        ("康得新", ["康得新", "康美药业", "康得新财务造假"]),
        ("雅戈尔", ["雅戈尔", "雅戈尔衬衫"]),
        ("洋河股份", ["洋河", "洋河股份"]),
        ("乐视", ["乐视", "贾跃亭", "乐视体育"]),
        ("格力电器", ["格力", "格力电器", "董明珠"]),
        ("暴风集团", ["暴风", "暴风影音", "暴风集团"]),
        ("中国平安", ["中国平安", "平安保险"]),
        ("獐子岛", ["獐子岛", "扇贝跑了"]),
        ("信威集团", ["信威", "信威集团"]),
    ]
    for tag, keywords in mapping:
        if any(kw in content for kw in keywords):
            tags.append(tag)
    return tags

# ============ 1. 读取全文 ============
doc = Document(DOCX_PATH)
paras = [p.text for p in doc.paragraphs]
total_chars = sum(len(t) for t in paras)
print(f"总段落: {len(paras)}, 总字符: {total_chars:,}")

# ============ 2. 建立目录结构 ============
CHAPTER_SECTIONS = [
    (88,  "第一章 你必须学会读财报",             "第一节  财报是用来排除企业的"),
    (134, "第一章 你必须学会读财报",             "第二节  财报大框架：财报阅读入门"),
    (188, "第一章 你必须学会读财报",             "第三节  读财报前的准备工作"),
    (262, "第一章 你必须学会读财报",             "第四节  重要提示"),
    (316, "第一章 你必须学会读财报",             "第五节  财报的结构"),
    (366, "第二章 投资高手关心的表——资产负债表", "第一节  货币资金"),
    (430, "第二章 投资高手关心的表——资产负债表", "第二节  经营相关资产"),
    (610, "第二章 投资高手关心的表——资产负债表", "第三节  生产相关资产"),
    (726, "第二章 投资高手关心的表——资产负债表", "第四节  投资相关资产"),
    (923, "第二章 投资高手关心的表——资产负债表", "第五节  负债和所有者权益"),
    (1022,"第二章 投资高手关心的表——资产负债表", "第六节  快速阅读资产负债表"),
    (1111,"第三章 资本市场追捧的表——利润表",    "第一节  利润表的重点"),
    (1160,"第三章 资本市场追捧的表——利润表",    "第二节  创造利润的过程"),
    (1313,"第三章 资本市场追捧的表——利润表",    "第三节  速读利润表"),
    (1379,"第四章 事关存亡的表——现金流量表",   "第一节  现金流量表拆解"),
    (1490,"第四章 事关存亡的表——现金流量表",   "第二节  企业的现金流肖像"),
    (1546,"第四章 事关存亡的表——现金流量表",   "第三节  现金流量表速读"),
    (1600,"第五章 财报的综合阅读及分析",         "第一节  鸟瞰三大表"),
    (1647,"第五章 财报的综合阅读及分析",         "第二节  财务指标分析"),
    (1747,"第五章 财报的综合阅读及分析",         "第三节  使用财务数据估值"),
    (1801,"第六章 所有者权益变动表和财报附注",   "第一节  所有者权益变动表"),
    (1867,"第六章 所有者权益变动表和财报附注",   "第二节  财报附注"),
    (1966,"第七章 管理层的汇报",                 "第一节  会计数据和财务指标摘要"),
    (1974,"第七章 管理层的汇报",                 "第二节  董事会报告"),
    (2150,"第七章 管理层的汇报",                 "第三节  重要事项"),
    (2177,"第八章 欺诈与反欺诈",                 "第一节  常见的操纵财报手法"),
    (2266,"第八章 欺诈与反欺诈",                 "第二节  财报被操纵的痕迹"),
]
SORTED_SECTIONS = sorted(CHAPTER_SECTIONS, key=lambda x: x[0])

def get_section(para_idx):
    last_chapter = "第一章 你必须学会读财报"
    last_section = "第一节  财报是用来排除企业的"
    for p_idx, chapter, section in SORTED_SECTIONS:
        if p_idx <= para_idx:
            last_chapter = chapter
            last_section = section
        else:
            break
    return last_chapter, last_section

# ============ 3. 清洗文本 ============
def clean_text(text):
    text = re.sub(r'股窜网\s*WWW\.gucuan\.com', '', text, flags=re.IGNORECASE)
    text = re.sub(r'第\s*\d+\s*页', '', text)
    text = re.sub(r'gucuan', '', text, flags=re.IGNORECASE)
    return text.strip()

# ============ 4. 切片 ============
MAX_LEN = 500
OVERLAP = 60

slices = []
slice_id = 1
current_buf = ""
current_buf_len = 0
current_chapter = ""
current_section = ""

for i, raw in enumerate(paras):
    text = clean_text(raw.strip())
    if len(text) < 15:
        continue

    chapter, section = get_section(i)

    if current_buf_len + len(text) + 1 > MAX_LEN and current_buf:
        slices.append({
            "book": "手把手教你读财报",
            "chapter": current_chapter,
            "section": current_section,
            "slice_id": f"S002_{slice_id:04d}",
            "content": current_buf.strip(),
            "word_count": len(current_buf),
            "tags": {
                "account": infer_account_tags(current_buf),
                "stage": infer_stage(current_section),
                "risk_type": infer_risk_tags(current_buf),
                "case": infer_case_tags(current_buf)
            }
        })
        slice_id += 1
        current_buf = current_buf[-OVERLAP:] + " " + text
        current_buf_len = len(current_buf)
        current_chapter = chapter
        current_section = section
    else:
        if current_buf:
            current_buf += "\n" + text
            current_buf_len += len(text) + 1  # +1 for newline
        else:
            current_buf = text
            current_buf_len = len(text)
        current_chapter = chapter
        current_section = section

    # 超长段落强制切
    if current_buf_len > MAX_LEN * 1.6 and "\n" not in current_buf[:-100]:
        content_to_save = current_buf[:MAX_LEN]
        rest = current_buf[MAX_LEN:]
        slices.append({
            "book": "手把手教你读财报",
            "chapter": current_chapter,
            "section": current_section,
            "slice_id": f"S002_{slice_id:04d}",
            "content": content_to_save.strip(),
            "word_count": len(content_to_save),
            "tags": {
                "account": infer_account_tags(content_to_save),
                "stage": infer_stage(current_section),
                "risk_type": infer_risk_tags(content_to_save),
                "case": infer_case_tags(content_to_save)
            }
        })
        slice_id += 1
        current_buf = rest
        current_buf_len = len(rest)

if current_buf.strip():
    slices.append({
        "book": "手把手教你读财报",
        "chapter": current_chapter,
        "section": current_section,
        "slice_id": f"S002_{slice_id:04d}",
        "content": current_buf.strip(),
        "word_count": len(current_buf),
        "tags": {
            "account": infer_account_tags(current_buf),
            "stage": infer_stage(current_section),
            "risk_type": infer_risk_tags(current_buf),
            "case": infer_case_tags(current_buf)
        }
    })

# ============ 5. 输出 ============
output_path = OUTPUT_DIR / "slices_sfoysc.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for s in slices:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

print(f"已写入: {output_path}")
print(f"总切片: {len(slices)}")
wc = [s["word_count"] for s in slices]
print(f"总字符: {sum(wc):,}, 平均: {sum(wc)/len(wc):.0f}字, 最短: {min(wc)}, 最长: {max(wc)}")
all_accounts = set()
all_risks = set()
all_cases = set()
for s in slices:
    all_accounts.update(s["tags"]["account"])
    all_risks.update(s["tags"]["risk_type"])
    all_cases.update(s["tags"]["case"])
stages = {}
for s in slices:
    st = s["tags"]["stage"]
    stages[st] = stages.get(st, 0) + 1
print(f"科目标签 {len(all_accounts)}: {sorted(all_accounts)}")
print(f"风险标签 {len(all_risks)}: {sorted(all_risks)}")
print(f"案例标签 {len(all_cases)}: {sorted(all_cases)}")
print(f"阶段分布: {stages}")