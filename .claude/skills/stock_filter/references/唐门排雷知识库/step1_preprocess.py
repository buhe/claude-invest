#!/usr/bin/env python3
"""
步骤1：文本预处理
从两本PDF中提取全文，清洗噪音，识别章节结构
"""
import pdfplumber
import re
import os

BOOKS = {
    "sfoysc": {
        "name": "手把手教你读财报",
        "short": "sfoysc",
        "path": "/Users/flynn/Downloads/手把手教你读财报/手把手教你读财报/手把手教你读财报 财报是用来排除企业的 以一份真实的财报为案例(高清)/手把手教你读财报 财报是用来排除企业的 以一份真实的财报为案例(高清).pdf"
    },
    "jztz": {
        "name": "价值投资实战手册",
        "short": "jztz",
        "path": "/Users/flynn/Downloads/价值投资实战手册/价值投资实战手册/价值投资实战手册 by 唐朝/价值投资实战手册 by 唐朝.pdf"
    }
}

def extract_full_text(pdf_path, max_pages=None):
    """提取PDF全部文字"""
    all_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        pages_to_read = max_pages or total
        print(f"  总页数: {total}，计划读取: {pages_to_read}")
        for i, page in enumerate(pdf.pages[:pages_to_read]):
            text = page.extract_text()
            if text:
                text = text.strip()
                text = re.sub(r'\n{3,}', '\n\n', text)
                all_pages.append(text)
    return "\n".join(all_pages), total

def detect_chapters(text, book_name):
    """检测章节标题，建立章节树"""
    chapter_patterns = [
        r'^(?:第[一二三四五六七八九十百零]+篇)\s*[:：]?\s*(.+)',
        r'^(?:第[一二三四五六七八九十百零]+章)\s*[:：]?\s*(.+)',
        r'^(?:第[一二三四五六七八九十百零]+节)\s*[:：]?\s*(.+)',
        r'^\d+\.\d+\s+[\u4e00-\u9fa5]',
        r'^[一二三四五六七八九十百零]+、\s*[\u4e00-\u9fa5]',
        r'^(?:上篇|下篇|前篇|后篇|导论|序章|引言|前言)\s*[:：]?\s*(.+)',
    ]
    lines = text.split('\n')
    chapters = []
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        for pattern in chapter_patterns:
            if re.match(pattern, line_stripped):
                chapters.append((i, line_stripped))
                break
    return chapters

def clean_noise(text):
    """清洗页眉页脚、页码等噪音"""
    lines = text.split('\n')
    cleaned = []
    skip_patterns = [
        r'本书由.*提供',
        r'更多电子书下载',
        r'^www\.',
        r'^http',
        r'^\s*第\s*\d+\s*页\s*$',
        r'^\s*-\s*\d+\s*-$',
    ]
    for line in lines:
        skip = False
        for pat in skip_patterns:
            if re.search(pat, line):
                skip = True
                break
        if not skip:
            cleaned.append(line)
    return '\n'.join(cleaned)

for key, book in BOOKS.items():
    print(f"\n{'='*60}")
    print(f"处理书籍: {book['name']}")
    print(f"{'='*60}")

    print("正在提取全文...")
    text, total_pages = extract_full_text(book['path'])
    print(f"  提取完成，总字符数: {len(text):,}")

    print("正在清洗噪音...")
    text = clean_noise(text)
    print(f"  清洗后字符数: {len(text):,}")

    print("正在检测章节结构...")
    chapters = detect_chapters(text, book['name'])
    print(f"  检测到章节/段落标题 {len(chapters)} 个")

    output_dir = f"/Users/flynn/WorkBuddy/20260424155824/唐门排雷知识库/{book['short']}"
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/full_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n章节结构（前30个）：")
    for idx, (page_num, title) in enumerate(chapters[:30]):
        print(f"  [{idx+1}] 第{page_num}行: {title[:70]}")

    if len(chapters) > 30:
        print(f"  ... 还有 {len(chapters)-30} 个章节标题")

print("\n步骤1完成！")
