---
name: invest-value
description: "Generate comprehensive company valuation research reports in markdown format from annual reports (PDF) and reference materials (markdown). Use when user needs to: (1) Analyze company valuation using DCF method, (2) Generate valuation reports with financial charts, (3) Research company intrinsic value based on free cash flow, (4) Create investment analysis reports with historical financial data and future projections"
---

# Invest Value

Generate comprehensive company valuation research reports in markdown format.

## Prerequisites

Before using this skill, ensure the current directory contains:
- Company annual report (PDF format)
- Reference materials (markdown format)

## Report Generation Workflow

### Step 1: Gather Financial Data

1. **Extract from reference materials** - Read all markdown files in current directory for historical financial data
2. **Cross-validate with stockanalysis skill** - Use `stockanalysis` skill to fetch last 5 years of financial data for validation
3. **Resolve discrepancies** - If data conflicts between sources, document the discrepancy and note which source is more authoritative

**Data required:**
- Revenue
- Net Income
- Operating Cash Flow
- Capital Expenditures (Capex)
- Free Cash Flow (FCF = Operating Cash Flow - Capex)
- Shares outstanding (for per-share calculations)
- Current stock price

### Step 2: Generate Charts (MANDATORY - Maximum 10 Charts)

**CRITICAL REQUIREMENTS:**
- Use Python matplotlib with REAL data - NO AI image generation tools
- All chart labels, titles, and text MUST be in ENGLISH
- Resolution: 300 DPI
- Save to `generated_images/` subdirectory in current working directory
- Maximum 10 charts per report

**Required Charts:**

1. **Revenue Trend** (`revenue_trend.png`) - Blue line (#1E88E5)
2. **Net Income Trend** (`net_income_trend.png`) - Green line (#43A047)
3. **Free Cash Flow Trend** (`fcf_trend.png`) - Purple line (#8E24AA)

**Using the bundled script:**

The skill includes `scripts/generate_charts.py` with functions:
- `create_revenue_trend_chart(years, revenue, output_dir)`
- `create_net_income_trend_chart(years, net_income, output_dir)`
- `create_fcf_trend_chart(years, fcf, output_dir)`
- `generate_all_charts(financial_data, output_dir)`

**Example:**

```python
import sys
sys.path.insert(0, '/Users/guyanhua/.claude/skills/invest-value/scripts')
from generate_charts import generate_all_charts

financial_data = {
    'years': ['2019', '2020', '2021', '2022', '2023', '2024'],
    'revenue': [100, 110, 125, 140, 155, 170],
    'net_income': [20, 22, 25, 28, 31, 35],
    'fcf': [18, 20, 23, 26, 29, 32]
}
generate_all_charts(financial_data, output_dir="generated_images")
```

**IMPORTANT:** Extract years dynamically from actual data - DO NOT hardcode. Match years list length with data values length.

### Step 3: Write Valuation Report

Create a markdown file named `{COMPANY_NAME}_valuation_report.md` with the following structure:

```markdown
# {Company Name} 估值研究报告

## 1. 执行摘要

[Company overview and key findings]

## 2. 财务分析

### 2.1 历史财务数据

![Revenue Trend](generated_images/revenue_trend.png)

![Net Income Trend](generated_images/net_income_trend.png)

![Free Cash Flow Trend](generated_images/fcf_trend.png)

### 2.2 历史财务数据表格（最近10年）

| Year | Revenue | Net Income | Operating Cash Flow | Capex | Free Cash Flow | Revenue Growth % | Net Income Growth % | FCF Growth % |
|------|---------|------------|---------------------|-------|----------------|------------------|---------------------|--------------|
{data rows}

### 2.3 未来10年自由现金流增长率估算

Based on historical FCF growth rates:
- [Last 10 years CAGR]
- [Last 5 years CAGR]
- [Last 3 years CAGR]

**Estimated FCF growth rate for next 10 years:** [X]%

**Rationale:** [Justify based on industry trends, company guidance, competitive position, etc.]

## 3. DCF 估值

### 3.1 估值方法

使用贴现现金流（DCF）方法，贴现率 r = 10%。

公式：**V = c × (1 + g) / (r - g)**

其中：
- V = 每股内在价值
- c = 当前年度每股自由现金流
- g = 未来增长率
- r = 贴现率 = 10%

### 3.2 估值情景分析

#### 情景 1：-5% 增长率

- 假设：c = ${FCF per share}, g = -5%, r = 10%
- 计算：V = ${c} × (1 + (-0.05)) / (0.10 - (-0.05)) = ${value}
- **内在价值：${value}/股**
- 当前股价：${current_price}
- 估值结论：[低估/高估] [X]%

#### 情景 2：0% 增长率
[Same format]

#### 情景 3：5% 增长率
[Same format]

#### 情景 4：7% 增长率
[Same format]

#### 情景 5：9% 增长率
[Same format]

#### 情景 6：估算增长率 ([X]%)
[Same format]

### 3.3 估值结论

[Summary of valuation across scenarios and recommendation]

## 4. 附录

### 4.1 完整财务数据表格

| Year | Revenue | Net Income | Operating Cash Flow | Capex | Free Cash Flow |
|------|---------|------------|---------------------|-------|----------------|
{full data table}

### 4.2 数据来源说明

- 年报（PDF）：[Source details]
- 参考资料：[Source details]
- stockanalysis.com：[Cross-validation notes]

### 4.3 关键假设

[Document all key assumptions made in the analysis]
```

### Step 4: Data Verification

**Verification requirements:**
1. Use `stockanalysis` skill to fetch last 5 years data
2. Cross-validate with reference materials
3. Evaluate source credibility (authoritativeness, rigor, relevance)
4. Key claims require 2+ independent sources
5. Document any discrepancies - DO NOT hide contradictions

**Discount rate note:** Use 10% as the discount rate unless there's a specific reason to adjust.

## Resources

### scripts/generate_charts.py

Python matplotlib script for generating financial trend charts.

**Functions:**
- `generate_all_charts(financial_data, output_dir)` - Generate all three charts
- `create_revenue_trend_chart(years, revenue, output_dir)` - Revenue trend only
- `create_net_income_trend_chart(years, net_income, output_dir)` - Net income only
- `create_fcf_trend_chart(years, fcf, output_dir)` - FCF trend only

**Chart specifications:**
- Resolution: 300 DPI
- Line charts: 12x6 inches (16:9 aspect ratio)
- Professional business style
- Data labels on all points
- English labels only
