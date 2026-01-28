---
name: invest-balance
description: Generate comprehensive balance sheet research reports in markdown format from company annual reports (PDF) and reference materials (markdown). Use when user needs to create financial analysis reports focusing on balance sheet, asset composition, liability structure, and debt analysis. Triggered by requests for balance sheet analysis reports, asset liability composition analysis, debt trend analysis, financial statement research from annual reports, or investment research on company financial position
---

# 资产负债表研究报告生成

## 概述

从公司年报（PDF）和参考资料（markdown）中提取和分析财务数据，使用 Python matplotlib 创建数据可视化，生成专业的资产负债表研究报告（中文），图表标签使用英文。

## 工作流程

### 1. 数据收集与验证

**读取源材料：**
- 年报 PDF：提取资产负债表数据、附注和相关财务报表
- 参考资料 markdown：审查现有财务数据和分析
- 使用 `stockanalysis` skill 获取 5 年历史数据进行交叉验证
- 数据准确很重要，参考资料中有历年三大表的数据，用于验证你从财报中获取的数据，以参考资料中数据为准。

**数据验证要求：**
- 评估数据来源的权威性、严谨性和相关性
- 关键主张必须有 2 个及以上独立来源支持
- 引用相同出处的来源算作 1 个来源（而非 2 个）
- 透明记录所有矛盾点

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

**⚠️ 必须包含计算验证表格：**
```markdown
### 偿债能力指标验证（[财年]）
| 指标 | 原始数据 | 计算过程 | 结果 |
|---|---|---:|---:|
| 经营现金流/总债务 | OCF: [数值], Debt: [数值] | [公式] | [结果] |
| 现金/短期债务 | Cash: [数值], ST Debt: [数值] | [公式] | [结果] |
```

[插入图表 8：长期债务趋势（如有数据）]

## 数据来源
列出所有来源及权威性评估
```

### 3. 图表生成（最多 10 个图表）

**关键要求：**
- 所有图表必须使用 Python matplotlib 生成真实数据 - 禁止使用 AI 图像生成
- 所有图表标签、标题和文本必须使用英文
- 所有图表分辨率：300 DPI
- 保存到 `generated_images/` 子目录
- 从实际数据中动态提取年份 - 禁止硬编码

**必需图表：**

**图表 4：资产构成（饼图）**
- 使用 `scripts/asset_composition.py`
- 文件名：`asset_composition.png`
- 英文标签（如 "Current Assets", "Non-Current Assets"）
- 使用实际数据的年份

**图表 5：负债构成（饼图）**
- 使用 `scripts/liability_composition.py`
- 文件名：`liability_composition.png`
- 英文标签（如 "Current Liabilities", "Long-term Debt"）
- 使用实际数据的年份

**图表 8：长期债务趋势（折线图）**
- 使用 `scripts/debt_trend.py`
- 文件名：`debt_trend.png`
- 棕色线条（#795548），16:9 宽高比（12x6）
- 从数据范围中提取实际年份（如 2019-2024）
- 年份列表长度必须与数据值长度匹配

**可选附加图表**（最多 7 个）：
- 流动比率趋势
- 债务权益比
- 资产质量指标
- 现金流与债务义务对比
- 营运资本分析

### 4. 图表实现

**使用方式：**

```python
# 资产构成饼图
from scripts.asset_composition import generate_asset_composition_chart
asset_data = {'Current Assets': 35, 'Non-Current Assets': 65}
generate_asset_composition_chart(asset_data, '2024')

# 负债构成饼图
from scripts.liability_composition import generate_liability_composition_chart
liability_data = {'Current Liabilities': 25, 'Long-term Debt': 50, 'Other': 25}
generate_liability_composition_chart(liability_data, '2024')

# 长期债务趋势折线图
from scripts.debt_trend import generate_debt_trend_chart
years = ['2019', '2020', '2021', '2022', '2023', '2024']
debt_values = [100.5, 110.2, 105.8, 120.3, 115.7, 130.1]
generate_debt_trend_chart(years, debt_values)
```

**在 markdown 中插入图表：**
```markdown
![资产构成](generated_images/asset_composition.png)
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
| 现金/债务比 | 0 - 5 | > 10（异常） |
| 经营现金流/债务 | 0 - 2 | > 5（异常） |

**如果计算结果超出合理范围，必须重新核对原始数据和计算逻辑。**

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

**语言：**
- 报告正文：中文
- 图表标签/标题：英文
- 财务术语：使用专业中文术语（如 流动资产、非流动负债）

**质量标准：**
- 将 PDF 数据与 stockanalysis skill 数据交叉验证
- 突出显示来源间的任何差异
- 为重大变化提供背景
- 评估财务健康状况和风险

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
