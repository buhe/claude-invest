#!/usr/bin/env python3
"""
步骤1（补充）：完整提取价值投资实战手册全文 + 建立章节树
"""
import pdfplumber
import re
import json

pdf_path = "/Users/flynn/Downloads/价值投资实战手册/价值投资实战手册/价值投资实战手册 by 唐朝/价值投资实战手册 by 唐朝.pdf"
output_dir = "/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/jztz"

print("正在完整提取价值投资实战手册（324页）...")

all_pages_text = []
page_stats = []

with pdfplumber.open(pdf_path) as pdf:
    print(f"总页数: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ''
        text = text.strip()
        if text:
            all_pages_text.append(f"[第{i+1}页]\n{text}")
        page_stats.append({'page': i+1, 'chars': len(text)})

full_text = "\n\n".join(all_pages_text)
print(f"\n提取统计：")
print(f"  有文字的页数: {sum(1 for p in page_stats if p['chars'] > 0)}")
print(f"  总字符数: {len(full_text):,}")
print(f"  平均每页字符: {len(full_text)/len(page_stats):.0f}")

with open(f"{output_dir}/full_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
print(f"全文已保存到 {output_dir}/full_text.txt")

print("\n正在分析章节结构...")

chapter_s树 = []
chapter_re = re.compile(r'^(第[一二三四五六七八九十百零\d]+章)\s*[:：\s]*(.{2,50})')
section_re = re.compile(r'^(\d+\.\d+)\s+(.{2,50})(?:\s+\d+)?$')

lines = full_text.split('\n')
current_chapter = None

for i, line in enumerate(lines):
    line_stripped = line.strip()
    if not line_stripped:
        continue
    cm = chapter_re.match(line_stripped)
    if cm:
        current_chapter = {'章号': cm.group(1), '标题': cm.group(2).strip(), '小节': [], '行号': i}
        chapter_s树.append(current_chapter)
        continue
    sm = section_re.match(line_stripped)
    if sm and current_chapter:
        current_section = {'编号': sm.group(1), '标题': sm.group(2).strip(), '行号': i}
        current_chapter['小节'].append(current_section)

print(f"\n识别到 {len(chapter_s树)} 个一级章节：")
for ch in chapter_s树:
    print(f"  {ch['章号']} {ch['标题'][:50]}")
    for sec in ch['小节'][:3]:
        print(f"    - {sec['编号']} {sec['标题'][:45]}")
    if len(ch['小节']) > 3:
        print(f"    ... 共 {len(ch['小节'])} 节")

with open(f"{output_dir}/chapters.json", "w", encoding="utf-8") as f:
    json.dump(chapter_s树, f, ensure_ascii=False, indent=2)

print("\n章节树已保存到 chapters.json")
print(f"\n=== 步骤1对《价值投资实战手册》完成统计 ===")
print(f"总页数: 324")
print(f"提取字符: {len(full_text):,}")
print(f"有文字页: {sum(1 for p in page_stats if p['chars'] > 0)}")
print(f"识别章节: {len(chapter_s树)} 章")
