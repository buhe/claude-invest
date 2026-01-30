---
name: invest-cap
description: 在包含公司年报和参考资料（markdown）的当前目录中生成资本配置研究报告（markdown 格式）。重点关注资本配置分析，包括分红、股票回购和投资。当用户需要创建投资研究报告、分析资本配置策略或生成投资分析财务图表时使用。
---

# 投资研究报告生成器

生成专业的资本配置研究报告，重点关注资本配置分析。当前目录应包含：
- 最新年报（为了保证你的专注度，只使用最新一年的财报作为资料）
- 参考资料（markdown 格式），其中有公司最近10年的主要投资项目

## 报告结构

### 资本配置章节（必需）

分析三个组成部分：**分红**、**股票回购** 和 **投资**

#### 1. 分红分析

计算并报告：
- **最近一年股息率**：每股年股息 / 当前股价
- **最近一年派息率**：年股息总额 / 净利润
- **5 年分红趋势**：增长率和稳定性
- **插入图表**：`![股息增长](generated_images/dividend_growth.png)` 使用 ChartGenerator.dividend_growth()

#### 2. 股票回购分析

计算并报告：
- **最近一年回购收益率**：回购总额 / 市值
- **5 年股数变化**：比较当前股数与 5 年前
- **股权激励 vs 回购影响**：股权激励是否抵消了回购？
  - 计算：(5 年前股数 - 当前股数) / 5 年前股数
  - 负变化 = 股权激励超过回购（摊薄）
  - 正变化 = 回购超过股权激励（增厚）
- **插入图表**：`![股数趋势](generated_images/share_count_trend.png)` 使用 ChartGenerator.share_count_trend()

#### 3. 投资分析

投资分析应包含以下**四个维度**：

##### 3.1 收购与并购投资 (M&A)

创建主要投资表格（最近 10 年）：
| 年份 | 投资/标的 | 金额 | 用途 | 结果 |
|------|-------------------|--------|---------|---------|

要求：
- 包含大于 10 年投资总额 1% 的投资
- 按金额降序排序
- 标记结果：已完成、进行中、已失败
- 分析投资战略演变和效率

##### 3.2 资本支出分析 (Capex)

**必须包含**：固定资产投资的年度趋势分析

| 项目 | 内容 |
|------|------|
| **计算指标** | 资本支出/营业收入、资本支出/自由现金流 |
| **趋势分析** | 5年资本支出变化趋势 |
| **投资方向** | 产能扩张、研发设施、数据中心、零售店等 |

**示例表格**：
| 年份 | 资本支出 | 占收入比 | 占FCF比 | 主要用途 |
|------|----------|----------|---------|----------|
| 2021 | $10.5B | 2.8% | 11.3% | 产能扩张、数据中心 |
| 2022 | $11.2B | 2.9% | 10.1% | 研发设施、芯片设备 |

##### 3.3 研发投资分析 (R&D)

**必须包含**：研发投入的深度分析

| 项目 | 内容 |
|------|------|
| **计算指标** | 研发费用/营业收入、研发费用增长率 |
| **趋势分析** | 5年研发投入变化 |
| **重点领域** | AI、芯片、新产品线等关键投资方向 |

**示例表格**：
| 年份 | 研发费用 | 占收入比 | 同比增长 | 重点投入领域 |
|------|----------|----------|----------|-------------|
| 2025 | $34.6B | 8.3% | +9.2% | AI、芯片、Vision Pro |

##### 3.4 战略性财务投资

分析公司的战略股权投资（如有）：
- 投资其他公司股权（如苹果投资滴滴）
- 合资企业
- 少数股权投资

**⚠️ 投资分析完整性检查**：

确保报告包含以下所有投资维度：
- [ ] M&A收购投资（如有）
- [ ] 资本支出分析（必需）
- [ ] 研发投资分析（必需）
- [ ] 战略财务投资（如有）

**图表**：`![资本配置分解](generated_images/capital_allocation.png)` 使用 ChartGenerator.capital_allocation_breakdown()

**资本配置分解图表应包含**：
- 股票回购
- 分红
- 资本支出
- 研发投资
- 收购（如有重大）


## 数据收集工作流程

### 步骤 1：从年报中提取数据

使用 PDF 阅读工具提取：
- 利润表（收入、净利润、每股收益）
- 资产负债表（股数、股东权益、债务）
- 现金流量表（分红、回购、资本支出）
- 资本配置附注
- 重大投资和收购

### 步骤 2：获取最新财务数据（如需要）

使用 `stockanalysis` skill 获取 5 年财务数据进行交叉验证：
```python
# 调用：stockanalysis skill
# 股票代码：[公司股票代码]
# 所需数据：利润表、资产负债表、现金流量表
```

与参考资料交叉验证以确保准确性。

### 步骤 3：验证数据来源

对每个关键主张：
- **使用 2 个或以上独立来源验证**
- 相同的原始来源 = 1 个来源（不是 2 个）
- **记录任何矛盾** - 不要隐藏
- 评估来源：权威性、严谨性、相关性

### 步骤 4：生成图表

使用绑定的 `scripts/chart_generator.py`：

```python
from scripts.chart_generator import ChartGenerator

# 重要：明确指定输出目录为当前工作目录下的 generated_images
import os
output_dir = os.path.join(os.getcwd(), "generated_images")
generator = ChartGenerator(output_dir=output_dir)

# 图表 6：股数趋势
generator.share_count_trend(years, share_counts)

# 图表 7：股息增长
generator.dividend_growth(years, dividends)

# 图表 10：资本配置分解
generator.capital_allocation_breakdown(years, dividends, repurchases)
```

**⚠️ 路径重要说明**：
- **必须**明确使用 `os.getcwd()` 获取当前工作目录
- 图片必须保存在**当前工作目录**的 `generated_images/` 下
- 不要在 skill 目录或任何其他位置生成图片
- 在 markdown 报告中引用图片时使用相对路径：`![描述](generated_images/图片名.png)`

**图表要求：**
- 每份报告最多 10 个图表
- 分辨率：300 DPI
- 所有标签和标题必须使用**英文**
- 从数据中动态提取年份（不要硬编码）
- 保存到**当前工作目录**的 `generated_images/` 目录

### 步骤 5：撰写报告

生成 markdown 报告，包含：
- 公司概述
- 资本配置分析（详细）
- 嵌入支持图表
- 数据来源引用
- 记录的矛盾点

## 图表模板

### 图表 6：股数趋势
```python
# 无股票分割的情况
generator.share_count_trend(
    years=['2019', '2020', '2021', '2022', '2023', '2024'],  # 从数据中提取
    share_counts=[1000000000, 980000000, 960000000, ...],
    title="Share Count Trend"
)

# 有股票分割的情况（如 Apple 2021 年 4:1 分割）
generator.share_count_trend(
    years=['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    share_counts=[5444000000, 5257000000, 5022000000, 4574000000, 4443000000, 16427000000, ...],
    title="Apple Share Count Trend (2016-2025)",
    split_year=2021,     # 股票分割发生的年份
    split_ratio=4.0      # 分割比例（4:1）
)
```

**⚠️ 重要：股票分割处理**
- 如果数据中包含股票分割前后数据，必须指定 `split_year` 和 `split_ratio` 参数
- 图表会自动将分割前的股数调整为分割后基准，使趋势连续可读
- 不指定这些参数会导致图表 Y 轴比例异常（高度过高）

### 图表 7：股息增长
```python
generator.dividend_growth(
    years=['2015', '2016', ..., '2024'],  # 从数据中提取
    dividends=[1.20, 1.32, 1.45, ...],
    title="Dividend Per Share Growth (Last 10 Years)"
)
```

### 图表 10：资本配置分解
```python
generator.capital_allocation_breakdown(
    years=['2020', '2021', '2022', '2023', '2024'],
    dividends=[2.5, 2.7, 2.9, 3.1, 3.3],
    repurchases=[5.2, 6.1, 4.8, 7.2, 8.5]
)
```

## 数据验证规则

1. **交叉核对**年报数据与 stockanalysis 数据
2. **记录差异**并说明原因
3. **独立来源** = 独立的数据提供商，非转载
4. **最新数据优先** = 使用昨天的日期作为参考点
5. **保守估计**当来源冲突时

## 输出格式

将报告保存为：`[公司名称]_投资报告_YYYY-MM-DD.md`

示例结构：
```markdown
# [公司名称]资本配置研究报告

**日期**：[昨天的日期]
**分析师**：Claude AI

## 资本配置分析

### 分红
- 股息率：X.X%
- 派息率：XX%
- 5 年趋势：[分析]

![股息增长](generated_images/dividend_growth.png)

### 股票回购
- 回购收益率：X.X%
- 股数变化：-X.X%（增厚）/ +X.X%（摊薄）

![股数趋势](generated_images/share_count_trend.png)

### 重大投资

![资本配置分解](generated_images/capital_allocation.png)

| 年份 | 投资 | 金额 | 用途 | 结果 |
|------|------------|--------|---------|---------|


---

**数据来源**：
- [年份] 年报：[链接/引用]
- stockanalysis.com：[股票代码]
- [其他来源及评级]
```

## 资源

### scripts/chart_generator.py

使用 matplotlib 生成财务图表的 Python 模块。

**可用方法：**
- `share_count_trend(years, share_counts, title, split_year=None, split_ratio=1.0)` - 股数趋势折线图，支持股票分割处理
- `dividend_growth(years, dividends, title)` - 股息增长柱状图
- `capital_allocation_breakdown(years, dividends, repurchases, title)` - 堆叠柱状图
- `revenue_trend(years, revenues, title)` - 收入趋势折线图
- `revenue_segment_breakdown(segments, values, title)` - 饼图
- `profit_margins(years, gross_margins, operating_margins, net_margins, title)` - 多条线

**所有图表：**
- 300 DPI 分辨率
- 仅使用英文标签
- 自动保存到 `generated_images/`
