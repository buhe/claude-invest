---
name: invest-balance
description: Generate comprehensive balance sheet research reports in markdown format from company annual reports and reference materials (markdown). Use when user needs to create financial analysis reports focusing on balance sheet, asset composition, liability structure, and debt analysis. Triggered by requests for balance sheet analysis reports, asset liability composition analysis, debt trend analysis, financial statement research from annual reports, or investment research on company financial position
---

# 资产负债表研究报告生成

## 概述

从公司年报（为了保证你的专注度，只使用最新一年的财报作为资料）和参考资料（markdown）中提取和分析财务数据，使用 Python matplotlib 创建数据可视化，生成专业的资产负债表研究报告（中文），图表标签使用英文。

## 工作流程

### 1. 数据收集与验证

**读取源材料：**
- 年报：提取资产负债表数据、附注和相关财务报表
- 参考资料 markdown：审查现有财务数据和分析
- 使用 `stockanalysis` skill 获取 5 年历史数据进行交叉验证
- 数据准确很重要，参考资料中有历年三大表的数据，用于验证你从财报中获取的数据，以参考资料中数据为准。

**数据验证要求：** 详见 `invest-report/references/common-guidelines.md`（数据验证规范）。

### 2. 报告结构

按以下结构生成 markdown 报告：

```markdown
# [公司名称] 资产负债表研究报告

## 执行摘要
财务状况和关键发现概述

## 资产负债表概览
总资产、总负债、股东权益概览

## 资产分析
### 流动资产
- 现金及现金等价物
- 有价证券（如有）
- 应收账款分析（如有数据）
- 存货及其他流动资产

### 非流动资产
[插入图表 4：资产构成]

## 负债分析
### 流动负债
- 应付账款分析（如有）
- 短期债务及本期到期部分

### 非流动负债
- 长期债务结构

[插入图表 5：负债构成]

## 债务分析
- 债务结构与构成
- 债务偿还能力分析（经营活动现金流、资产出售、现金储备等）
- 债务偿付能力评估
- **短期偿债压力分析**（重点评估未来12个月到期的债务）

**⚠️ 必须包含计算验证表格：**
```markdown
### 偿债能力指标验证（[财年]）
| 指标 | 原始数据 | 计算过程 | 结果 |
|---|---|---:|---:|
| 经营现金流/总债务 | OCF: [数值], Debt: [数值] | [公式] | [结果] |
| 现金+短期投资/短期债务 | Cash: [数值], ST Inv: [数值], ST Debt: [数值] | [公式] | [结果] |
```

**⚠️ 短期债务定义（必须严格遵守）：**
"短期债务"必须包括所有需要在一年内偿还的债务项目，通常包括：
- 商业票据 (Commercial Paper)
- 短期债务/定期债务 (Short-term Debt / Term Debt - 流动负债部分)
- 一年内到期的长期债务 (Current Portion of Long-Term Debt，如有)

**计算公式：**
```
短期债务总额 = 商业票据 + 短期债务 + 一年内到期的长期债务（如有）
现金+短期投资/短期债务 = (现金及等价物 + 有价证券/短期投资) / 短期债务总额
```

**示例（正确计算）：**
```
现金及等价物: $35,934M
短期投资(有价证券): $18,763M
商业票据: $7,979M
短期债务(Term Debt): $12,350M

短期债务总额 = 7,979 + 12,350 = $20,329M
现金+短期投资 = 35,934 + 18,763 = $54,697M
比率 = 54,697 / 20,329 = 2.69倍
```

**示例（错误避免）：**
```
❌ 错误：只使用商业票据作为短期债务
短期债务 = 7,979（遗漏了Term Debt）
比率 = 54,697 / 7,979 = 6.85倍（虚高）

✅ 正确：包含所有短期债务项目
短期债务 = 7,979 + 12,350 = 20,329
比率 = 54,697 / 20,329 = 2.69倍
```

[插入图表 8：长期债务趋势（如有数据）]

## 稳健性与风险评估

### 资产负债表稳健性评价

**评估维度：**

1. **资本结构稳健性**
   - 债务权益比：[数值]（行业参考：< 2.0 为健康）
   - 资产负债率：[数值]（行业参考：< 60% 为稳健）
   - 财务杠杆水平：[评估]

2. **资产质量**
   - 流动资产占比：[数值]%（评估资产流动性）
   - 无形资产占比：[数值]%（评估资产"轻重度"）
   - 资产构成合理性：[评估]

3. **盈利支撑能力**
   - 总资产/营业收入：[数值]倍（资产使用效率）
   - 净利润/总资产：[数值]%（资产回报率）

**稳健性结论：**
- ✅ **稳健** / ⚠️ **一般** / ❌ **不稳健**
- [具体评估结论]

### 流动性风险评估

**关键流动性指标：**

| 指标 | 数值 | 健康阈值 | 评估 |
|------|------|----------|------|
| 流动比率 | [数值] | > 1.5 | [评估] |
| 速动比率 | [数值] | > 1.0 | [评估] |
| 现金+短期投资/短期债务 | [数值]倍 | > 1.0 | [评估] |
| 经营现金流/短期债务 | [数值]倍 | > 1.0 | [评估] |
| 营运资本 | [数值] | 正值为佳 | [评估] |

**流动性压力测试：**

| 压力情景 | 假设条件 | 应对能力评估 |
|----------|----------|--------------|
| 营收下降30% | 现金流入减少 | [评估] |
| 融资渠道收紧 | 无法续借短期债务 | [评估] |
| 短期债务集中到期 | 一年内到期债务偿付 | [评估] |

**流动性风险结论：**
- ✅ **无风险** / ⚠️ **存在一定风险** / ❌ **存在较高风险**
- [具体风险评估结论，包括：现金储备是否充足、短期偿债压力、融资渠道依赖度等]

### 综合评价

**资产负债表整体画像：**
- 资产负债表类型：[保守型 / 稳健型 / 激进型]
- 主要优势：[列举1-2项]
- 主要关注点：[列举1-2项]

## 数据来源
列出所有来源及权威性评估
```

### 3. 图表生成（强制执行）

⚠️ **重要**：在完成报告时，**必须**执行以下步骤来生成图表：

1. **创建图表生成脚本**：在当前目录创建Python脚本
2. **执行脚本生成图表**：使用Bash工具运行Python脚本
3. **验证图表文件**：检查 `generated_images/` 目录是否包含生成的图片
4. **在报告中引用图片**：使用markdown语法引用图表

**必需图表：**

**图表 1：资产构成（饼图）**
- 文件名：`asset_composition.png`
- 英文标签（如 "Cash & Investments", "Long-term Investments", "Goodwill", "Other"）
- 使用实际数据的年份

**图表 2：负债构成（饼图）**
- 文件名：`liability_composition.png`
- 英文标签（如 "Short-term Debt", "Long-term Debt", "Other Liabilities"）
- 使用实际数据的年份

**图表 3：债务趋势（折线图或柱状图）**
- 文件名：`debt_trend.png`
- 显示短期债务、长期债务、现金储备的多年趋势
- 从数据范围中提取实际年份（如 2020-2024）

**创建图表生成脚本模板：**

```python
#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
os.makedirs('generated_images', exist_ok=True)

# 图表1：资产构成饼图
def create_asset_composition():
    labels = ['Cash & Short-term\nInvestments', 'Long-term\nInvestments',
              'Goodwill', 'Other Assets']
    sizes = [31.7, 19.5, 25.1, 23.7]  # 替换为实际数据
    colors = ['#1E88E5', '#43A047', '#FB8C00', '#8E24AA']
    explode = (0.05, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.set_title('Asset Composition (2024)', fontsize=14, fontweight='bold')
    plt.savefig('generated_images/asset_composition.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: asset_composition.png')

# 图表2：负债构成饼图
def create_liability_composition():
    labels = ['Short-term Debt', 'Long-term Debt', 'Other Liabilities']
    sizes = [19.6, 21.6, 58.8]  # 替换为实际数据
    colors = ['#E53935', '#FB8C00', '#757575']
    explode = (0.05, 0.05, 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.set_title('Liability Composition (2024)', fontsize=14, fontweight='bold')
    plt.savefig('generated_images/liability_composition.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: liability_composition.png')

# 图表3：债务与现金趋势
def create_debt_trend():
    years = ['2020', '2021', '2022', '2023', '2024']  # 替换为实际年份
    short_term_debt = [27.14, 39.38, 28.47, 22.16, 19.42]  # 替换为实际数据
    long_term_debt = [22.72, 11.09, 13.18, 19.10, 20.13]  # 替换为实际数据
    cash = [42.92, 49.38, 42.55, 59.34, 76.91]  # 替换为实际数据

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(years))
    width = 0.25

    ax.bar(x - width, short_term_debt, width, label='Short-term Debt', color='#E53935')
    ax.bar(x, long_term_debt, width, label='Long-term Debt', color='#FB8C00')
    ax.plot(x + width*0.5, cash, marker='o', linewidth=2.5, label='Cash',
            color='#43A047', markersize=8)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amount (Billion CNY)', fontsize=12, fontweight='bold')
    ax.set_title('Debt and Cash Trend (2020-2024)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.savefig('generated_images/debt_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: debt_trend.png')

if __name__ == '__main__':
    create_asset_composition()
    create_liability_composition()
    create_debt_trend()
```

**执行步骤：**

1. 将上述脚本保存到当前目录（替换为从年报提取的实际数据）
2. 使用Bash工具执行：
   ```bash
   python generate_balance_charts.py
   ```
3. 验证图表已生成：
   ```bash
   ls generated_images/
   ```
4. 在报告中引用图片：
   ```markdown
   ![资产构成](generated_images/asset_composition.png)
   ![负债构成](generated_images/liability_composition.png)
   ![债务与现金趋势](generated_images/debt_trend.png)
   ```

**验证清单：**
```
□ Python脚本已创建并执行
□ generated_images/目录已创建
□ 所有3张图表已生成
□ 报告中已正确引用所有图片
```

### 4. 图表实现

**在 markdown 中插入图表：**
```markdown
### 资产构成分析（2024年）

![资产构成](generated_images/asset_composition.png)

**资产特点**：
- 现金储备充裕...
- 长期投资布局...
```

### 5. 计算验证与合理性检查 ⚠️ 强制执行

**所有计算结果必须经过以下验证：**

#### 5.1 基本计算验证

每个比率计算必须：
1. **显示原始数据**：在报告中明确列出计算用到的原始数值
2. **显示计算过程**：使用公式展示计算方式
3. **自检合理性**：结果必须符合常识范围

```
示例格式：
| 指标 | 计算过程 | 结果 |
|---|---|---:|
| 经营现金流/总债务 | 111,482 / 112,377 | 0.99倍 |
```

#### 5.2 常见比率合理范围（用于自查）

| 比率类型 | 合理范围 | 警示值 |
|---|---|---|
| 流动比率 | 0.5 - 3.0 | < 0.3 或 > 5.0 |
| 资产负债率 | 20% - 150% | > 200% |
| 现金+短期投资/短期债务 | 0.2 - 5 | > 10（异常，可能漏算债务） |
| 经营现金流/债务 | 0 - 2 | > 5（异常） |

**如果计算结果超出合理范围，必须重新核对原始数据和计算逻辑。**

**⚠️ 特别注意：如果"现金+短期投资/短期债务"计算结果 > 5倍，很可能是遗漏了部分短期债务项目，请检查是否完整计算了所有短期债务。**

#### 5.3 强制验证步骤

1. **交叉验证**：关键数据（总资产、总负债、现金流）至少从2个来源确认
2. **单位统一**：确保所有数值使用相同单位（亿美元/百万美元）
3. **逻辑检查**：
   - 资产 = 负债 + 权益（必须相等）
   - 流动资产 + 非流动资产 = 总资产
   - 流动负债 + 非流动负债 = 总负债
4. **数量级检查**：确认数量级正确（亿vs千万vs百亿）

#### 5.4 错误示例警示

```
❌ 错误：经营现金流/总债务 = 9.9倍
原始数据：经营现金流1,115亿，总债务1,124亿
正确计算：1,115 / 1,124 = 0.99倍
错误原因：未进行数量级检查，1,115/1,124明显接近1而非10

✅ 正确：经营现金流/总债务 = 0.99倍
原始数据：经营现金流1,115亿美元，总债务1,124亿美元
计算过程：111,482 / 112,377 = 0.992
```

### 6. 分析指南

**时间参考：** 使用昨日日期作为当前参考点

**语言规范：** 详见 `invest-report/references/common-guidelines.md`

**质量标准：**
- 将 PDF 数据与 stockanalysis skill 数据交叉验证
- 突出显示来源间的任何差异
- 为重大变化提供背景
- 评估财务健康状况和风险
- **必须给出明确的稳健性和流动性风险结论**（稳健/一般/不稳健，无风险/存在风险/存在较高风险）

**稳健性判断参考标准：**
| 指标 | 稳健 | 一般 | 不稳健 |
|------|------|------|--------|
| 债务权益比 | < 1.0 | 1.0 - 2.0 | > 2.0 |
| 资产负债率 | < 50% | 50% - 70% | > 70% |
| 流动比率 | > 2.0 | 1.5 - 2.0 | < 1.5 |
| 现金/短期债务 | > 1.5 | 1.0 - 1.5 | < 1.0 |

**流动性风险判断参考标准：**
| 风险等级 | 条件（满足任一即为该等级） |
|----------|---------------------------|
| **无风险** | 现金+短期投资/短期债务 > 1.5 且 经营现金流/短期债务 > 1.0 |
| **存在一定风险** | 现金+短期投资/短期债务 < 1.0 或 流动比率 < 1.5 |
| **存在较高风险** | 现金+短期投资/短期债务 < 0.5 或 经营现金流 < 0 |

## 资源

### scripts/

**asset_composition.py** - 生成资产构成饼图
- 函数：`generate_asset_composition_chart(asset_data, year, output_dir)`
- 创建带英文标签的饼图
- 300 DPI，10x8 图形尺寸

**liability_composition.py** - 生成负债构成饼图
- 函数：`generate_liability_composition_chart(liability_data, year, output_dir)`
- 创建带英文标签的饼图
- 300 DPI，10x8 图形尺寸

**debt_trend.py** - 生成长期债务趋势折线图
- 函数：`generate_debt_trend_chart(years, debt_values, output_dir)`
- 创建棕色折线图（#795548）
- 300 DPI，12x6 图形尺寸
- 验证年份/值长度匹配
