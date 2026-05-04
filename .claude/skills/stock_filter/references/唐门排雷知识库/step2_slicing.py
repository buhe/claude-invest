#!/usr/bin/env python3
"""
步骤2：自动切片
基于真实目录结构，对《价值投资实战手册》进行知识切片
"""
import pdfplumber
import re
import json
import os

REAL_TOC = [
    {"chapter": "第一章", "title": "正确面对股价波动", "page": 3, "sections": [
        {"title": "什么是投资", "page": 3},
        {"title": "股票的本质", "page": 6},
        {"title": "投资是持续终身的事", "page": 10},
        {"title": "股票收益的来源", "page": 19},
        {"title": "最简单的投资方法", "page": 26},
        {"title": "普通投资者的道路", "page": 32},
        {"title": "投资无须\"接盘侠\"", "page": 36},
        {"title": "股权与其他投资品的对比", "page": 44},
        {"title": "优质企业的特征", "page": 50},
    ]},
    {"chapter": "第二章", "title": "如何估算内在价值", "page": 63, "sections": [
        {"title": "格雷厄姆奠定的理论基石", "page": 65},
        {"title": "巴菲特的继承与思考", "page": 77},
        {"title": "芒格与费雪推动的突破", "page": 96},
        {"title": "应用于实战的快速估值法", "page": 108},
    ]},
    {"chapter": "第三章", "title": "企业分析案例", "page": 119, "sections": [
        {"title": "生人勿近雅戈尔", "page": 123},
        {"title": "\"生人勿近\"诞生记", "page": 138},
        {"title": "像老板一样投资", "page": 148},
        {"title": "利亚德印象", "page": 156},
        {"title": "长安汽车：独轮行驶", "page": 172},
        {"title": "2014，茅台的倒春寒", "page": 181},
        {"title": "茅台的供给侧之忧", "page": 191},
        {"title": "2018，茅台的明牌", "page": 197},
        {"title": "重估茅台", "page": 203},
        {"title": "解密洋河高成长", "page": 208},
        {"title": "从洋河的跌停说起", "page": 213},
        {"title": "奋进中的洋河", "page": 218},
        {"title": "白酒领军企业点评", "page": 225},
        {"title": "看不见边际的腾讯", "page": 250},
        {"title": "腾讯控股，巨象尚未停步", "page": 262},
        {"title": "王者海康", "page": 269},
        {"title": "梳理分众传媒", "page": 282},
        {"title": "民生银行的全面溃退", "page": 290},
        {"title": "宋城演艺印象", "page": 299},
        {"title": "\"投机者\"信立泰", "page": 306},
    ]},
]

BOOK_NAME = "价值投资实战手册"
BOOK_SHORT = "jztz"

print("加载全文...")
with open(f"/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/{BOOK_SHORT}/full_text.txt", encoding="utf-8") as f:
    full_text = f.read()

# 按页拆分
pages_text = {}
for block in full_text.split('[第'):
    m = re.match(r'^(\d+)页\](.*)', block, re.DOTALL)
    if m:
        pg = int(m.group(1))
        content = m.group(2)
        pages_text[pg] = content

print(f"拆分完成，共 {len(pages_text)} 页有文本")

def split_into_chunks(text, target_w=400, max_w=500):
    if not text or len(text.strip()) < 100:
        return []
    chunks = []
    paragraphs = text.split('\n')
    current_chunk = ''
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_chunk) + len(para) <= target_w:
            current_chunk += para + '\n'
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            if len(para) > max_w:
                for i in range(0, len(para), max_w):
                    chunks.append(para[i:i+max_w])
                current_chunk = ''
            else:
                current_chunk = para + '\n'
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def guess_stage(text):
    if any(kw in text for kw in ['审计意见', '会计师事务所', '大股东质押', '造假', '虚构']):
        return '硬伤检查'
    if any(kw in text for kw in ['营业收入', '毛利率', '净利率', '费用', '利润', '非经常性损益', '扣非']):
        return '利润表分析'
    if any(kw in text for kw in ['应收账款', '存货', '商誉', '货币资金', '负债', '资产', '借款', '固定资产']):
        return '资产负债表分析'
    if any(kw in text for kw in ['经营现金流', '投资现金流', '筹资现金流', '现金流净额']):
        return '现金流分析'
    if any(kw in text for kw in ['三大前提', '利润为真', '可持续', '资本投入', '护城河']):
        return '三大前提判定'
    return '综合分析'

def guess_risk(text):
    risks = []
    if any(kw in text for kw in ['应收账款', '应收']):
        risks.append('收入造假')
    if any(kw in text for kw in ['存货', '跌价准备']):
        risks.append('资产虚增')
    if any(kw in text for kw in ['现金流', '经营现金']):
        risks.append('现金流异常')
    if any(kw in text for kw in ['存贷双高', '有息负债', '利息支出']):
        risks.append('存贷双高')
    if any(kw in text for kw in ['商誉', '减值']):
        risks.append('减值不足')
    if any(kw in text for kw in ['关联交易', '关联方']):
        risks.append('关联交易')
    if any(kw in text for kw in ['虚增', '造假', '虚构', '粉饰']):
        risks.append('利润操纵')
    return list(set(risks))

def guess_cases(text):
    cases = []
    for kw_list, name in [
        (['贵州茅台', '茅台股份', '茅台\n'], '茅台'),
        (['康得新'], '康得新'),
        (['万福生科'], '万福生科'),
        (['蓝田股份'], '蓝田股份'),
        (['雅戈尔'], '雅戈尔'),
        (['腾讯控股', '腾讯\n'], '腾讯'),
        (['洋河股份', '洋河\n'], '洋河'),
        (['海康威视', '海康\n'], '海康威视'),
        (['分众传媒', '分众\n'], '分众传媒'),
        (['民生银行'], '民生银行'),
        (['宋城演艺', '宋城\n'], '宋城演艺'),
        (['信立泰'], '信立泰'),
        (['利亚德'], '利亚德'),
        (['长安汽车', '长安\n'], '长安汽车'),
    ]:
        if any(kw in text for kw in kw_list):
            cases.append(name)
    return list(set(cases))

slice_id = 1
all_slices = []

for ch in REAL_TOC:
    chapter = ch['chapter']
    chapter_title = ch['title']
    chapter_start = ch['page']
    ch_idx = REAL_TOC.index(ch)
    chapter_end = REAL_TOC[ch_idx + 1]['page'] if ch_idx + 1 < len(REAL_TOC) else 324

    for sec in ch['sections']:
        sec_title = sec['title']
        sec_page = sec['page']
        sec_idx = ch['sections'].index(sec)
        next_sec_page = ch['sections'][sec_idx + 1]['page'] if sec_idx + 1 < len(ch['sections']) else chapter_end

        sec_text = ''
        for pg in range(sec_page, next_sec_page):
            if pg in pages_text:
                sec_text += pages_text[pg] + '\n'

        if not sec_text.strip():
            print(f"  警告: {sec_title} 无文本")
            continue

        chunks = split_into_chunks(sec_text)
        for chunk in chunks:
            sl = {
                "book": BOOK_NAME,
                "chapter": f"{chapter} {chapter_title}",
                "section": sec_title,
                "slice_id": f"{BOOK_SHORT.upper()}_{slice_id:04d}",
                "content": chunk,
                "word_count": len(chunk),
                "tags": {
                    "account": [],
                    "stage": guess_stage(chunk),
                    "risk_type": guess_risk(chunk),
                    "case": guess_cases(chunk)
                }
            }
            all_slices.append(sl)
            slice_id += 1

        print(f"  切片: {chapter} - {sec_title}: {len(chunks)} 片")

total_words = sum(s['word_count'] for s in all_slices)
avg_words = total_words / len(all_slices) if all_slices else 0
min_w = min(s['word_count'] for s in all_slices)
max_w = max(s['word_count'] for s in all_slices)

print(f"\n=== 切片统计 ===")
print(f"总切片数: {len(all_slices)}")
print(f"总字符数: {total_words:,}")
print(f"平均每片: {avg_words:.0f} 字，最短: {min_w} 字，最长: {max_w} 字")

output_jsonl = f"/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/slices_jztz.jsonl"
with open(output_jsonl, "w", encoding="utf-8") as f:
    for sl in all_slices:
        f.write(json.dumps(sl, ensure_ascii=False) + '\n')
print(f"已保存: {output_jsonl}")

# 标签统计
all_stages = {}
all_risks = {}
all_cases = {}
for s in all_slices:
    st = s['tags']['stage']
    all_stages[st] = all_stages.get(st, 0) + 1
    for r in s['tags']['risk_type']:
        all_risks[r] = all_risks.get(r, 0) + 1
    for c in s['tags']['case']:
        all_cases[c] = all_cases.get(c, 0) + 1

print(f"\n阶段标签分布: {all_stages}")
print(f"风险标签分布: {all_risks}")
print(f"案例标签分布: {all_cases}")
