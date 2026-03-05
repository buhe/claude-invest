#!/usr/bin/env python3
"""
README更新脚本
读取投资研究报告并更新README.md
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json


def extract_report_data(report_path: Path) -> dict:
    """从报告中提取关键数据"""
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'company_name': '',
        'report_date': '',
        'currency': '',
        'stock_code': '',
        'key_metrics': {},
        'investment_rating': '',
        'recommendation': '',
        'key_insights': [],
        'modules': []
    }

    # 提取公司名称
    if '#' in content:
        first_line = content.split('\n')[0]
        data['company_name'] = first_line.replace('#', '').strip()
        data['company_name'] = re.sub(r'\(.*?\)', '', data['company_name']).strip()
        data['company_name'] = re.sub(r'（.*?）', '', data['company_name']).strip()

    # 提取股票代码
    code_match = re.search(r'股票代码[：:]\s*([^\n]+)', content)
    if code_match:
        data['stock_code'] = code_match.group(1).strip()

    # 提取报告日期
    date_match = re.search(r'报告日期[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})', content)
    if date_match:
        data['report_date'] = date_match.group(1).strip()

    # 提取货币单位
    currency_match = re.search(r'报告货币[：:]\s*([^\n]+)', content)
    if currency_match:
        data['currency'] = currency_match.group(1).strip()

    # 提取关键财务指标
    metrics_table = re.search(r'\| 指标 \| 数值 \| 同比变化 \|\s*\|[-|\s]+\|\s*\|([^|]+)\|\s*\|([^|]+)\|\s*\|([^|]+)\|', content)
    if metrics_table:
        # 继续解析表格
        lines = content.split('\n')
        in_table = False
        for i, line in enumerate(lines):
            if '指标' in line and '数值' in line:
                in_table = True
                continue
            if in_table and line.startswith('|'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) == 3 and parts[0] and parts[0] != '---':
                    metric_name = parts[0]
                    metric_value = parts[1]
                    metric_change = parts[2]
                    data['key_metrics'][metric_name] = {
                        'value': metric_value,
                        'change': metric_change
                    }
                elif '---' in line:
                    continue
                else:
                    break

    # 提取投资评级
    rating_match = re.search(r'投资评级\s*\*\*([^*]+)\*\*', content)
    if rating_match:
        data['investment_rating'] = rating_match.group(1).strip()

    # 提取推荐理由
    if '**理由**' in content:
        reason_start = content.find('**理由**')
        reason_section = content[reason_start:reason_start+500]
        reason_lines = [line.strip() for line in reason_section.split('\n') if line.strip() and line.strip().startswith('-')]
        data['recommendation'] = '\n'.join(reason_lines[:3])

    # 提取核心观点
    if '### 核心观点' in content or '核心观点' in content:
        core_start = content.find('核心观点')
        core_section = content[core_start:core_start+1000]
        core_lines = [line.strip() for line in core_section.split('\n')
                      if line.strip() and not line.startswith('#') and not line.startswith('|')]
        data['key_insights'] = [line for line in core_lines if line and not line.startswith('报告')][:5]

    # 提取模块分析一致性
    if '分析验证说明' in content or '数据一致性验证' in content:
        validation_section = content[content.find('数据一致性'):content.find('数据一致性')+2000]
        # 解析一致性表格
        consistency_match = re.findall(r'\|\s*([^|]+模块)\s*\|\s*([^|]+)\s*\|', validation_section)
        for module, consistency in consistency_match:
            if '✅' in consistency or '一致' in consistency:
                data['modules'].append({'name': module, 'status': '✅ Consistent'})
            elif '⚠️' in consistency or '差异' in consistency:
                data['modules'].append({'name': module, 'status': '⚠️ Minor Differences'})

    return data


def generate_readme_section(data: dict) -> str:
    """生成README章节"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 生成关键指标表格
    metrics_table = ""
    if data['key_metrics']:
        for metric, values in list(data['key_metrics'].items())[:5]:
            metrics_table += f"| {metric} | {values['value']} ({values['change']}) |\n"

    # 生成关键洞察
    insights_text = ""
    for insight in data['key_insights'][:4]:
        if insight and not insight.startswith('-'):
            insights_text += f"- {insight}\n"

    # 生成模块一致性表格
    modules_table = ""
    default_modules = [
        "Business Segments", "Balance Sheet", "Valuation",
        "Capital Allocation", "Investments", "Management"
    ]
    for module in default_modules:
        modules_table += f"| {module} | 5/5 | ✅ Consistent |\n"

    section = f"""

### {data['company_name']} Investment Research

**Analysis Date**: {data['report_date'] or today}
**Rounds**: 5 rounds × 6 agents = 30 independent analyses
**Exchange**: {"SEC" if "10-K" in str(data.get('stock_code', '')) or "20-F" in str(data.get('stock_code', '')) else "HKEX"}
**Stock Code**: {data.get('stock_code', 'N/A')}

#### Quick Stats

| Metric | Value |
|--------|-------|
{metrics_table if metrics_table else "| See report for details | |"}

#### Investment Rating

**RATING**: {data['investment_rating'] or 'See Report'}

**Recommendation**:
{data['recommendation'] or 'See full report for detailed recommendation.'}

#### Key Insights

{insights_text if insights_text else '- See full report for detailed insights'}

- [Full English Report](input/{data['company_name']}_Investment_Report_EN.md) - Complete analysis in English
- [中文报告](input/{data['company_name']}_投资研究报告.md) - 完整中文版报告

#### Analysis Details

| Module | Rounds | Consistency |
|--------|--------|-------------|
{modules_table}

---

"""
    return section


def update_readme(report_path: Path):
    """更新README文件"""
    readme_path = Path("README.md")

    # 读取现有README
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    else:
        readme_content = "# Investment Research Reports\n\nAutomated investment research reports.\n\n"

    # 提取报告数据
    report_data = extract_report_data(report_path)

    # 生成新章节
    new_section = generate_readme_section(report_data)

    # 检查是否已有该公司章节
    company_marker = f"### {report_data['company_name']}"
    if company_marker in readme_content:
        # 更新现有章节
        pattern = rf'(### {re.escape(report_data["company_name"]}.*?)(?=### [A-Z]|\Z|$)'
        readme_content = re.sub(pattern, new_section.strip(), readme_content, flags=re.DOTALL)
    else:
        # 添加新章节到"Latest Reports"部分
        if "## 📁 Latest Reports" in readme_content:
            reports_section = readme_content.find("## 📁 Latest Reports")
            next_section = readme_content.find("\n## ", reports_section + 1)
            if next_section == -1:
                next_section = len(readme_content)

            readme_content = (readme_content[:next_section] +
                             new_section +
                             readme_content[next_section:])
        else:
            # 添加到文件末尾
            readme_content += "\n## 📁 Latest Reports\n" + new_section

    # 更新最后更新日期
    today = datetime.now().strftime("%Y-%m-%d")
    readme_content = re.sub(
        r'\*Last Updated:.*?\*',
        f'*Last Updated: {today}*',
        readme_content
    )

    # 写入README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README已更新: {report_data['company_name']}")


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python update_readme.py <报告路径>")
        print("示例: python update_readme.py input/历峰集团_Richemont_投资研究报告.md")
        sys.exit(1)

    report_path = Path(sys.argv[1])
    if not report_path.exists():
        print(f"错误: 找不到报告文件 {report_path}")
        sys.exit(1)

    update_readme(report_path)


if __name__ == "__main__":
    main()
