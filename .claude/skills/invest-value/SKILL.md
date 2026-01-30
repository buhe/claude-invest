---
name: invest-value
description: "从公司年报和参考资料（markdown）生成全面的企业估值研究报告（markdown格式）。当用户需要以下功能时使用：(1) 使用DCF方法分析企业估值，(2) 生成带有财务图表的估值报告，(3) 基于自由现金流研究企业内在价值，(4) 创建包含历史财务数据和未来预测的投资分析报告"
---

# 企业估值分析

从公司年报和参考资料生成全面的企业估值研究报告。

## 前置条件

使用此技能前，请确保当前目录包含：
- 公司年报（为了保证你的专注度，只使用最新一年的财报作为资料）
- 参考资料（markdown格式）

## 报告生成流程

### 步骤1：收集财务数据

1. **从参考资料中提取** - 读取当前目录中所有 markdown 文件以获取历史财务数据
2. **使用 stockanalysis 技能交叉验证** - 使用 `stockanalysis` 技能获取过去5年的财务数据进行验证
3. **解决数据差异** - 如果数据来源之间存在冲突，记录差异并注明哪个来源更具权威性

**所需数据：**
- 营业收入
- 净利润
- 经营活动现金流
- 资本支出（Capex）
- 自由现金流（FCF = 经营活动现金流 - 资本支出）
- 流通股数（用于每股计算）
- 当前股价

### 步骤2：生成图表（必填 - 最多10张图表）

**关键要求：**
- 使用 Python matplotlib 与真实数据 - 禁止使用 AI 图像生成工具
- 所有图表标签、标题和文本必须使用英文
- 分辨率：300 DPI
- 保存到当前工作目录的 `generated_images/` 子目录
- 每份报告最多10张图表

**必需图表：**

1. **营业收入趋势** (`revenue_trend.png`) - 蓝色线条 (#1E88E5)
2. **净利润趋势** (`net_income_trend.png`) - 绿色线条 (#43A047)
3. **自由现金流趋势** (`fcf_trend.png`) - 紫色线条 (#8E24AA)

**使用捆绑脚本：**

此技能包含 `scripts/generate_charts.py`，提供以下函数：
- `create_revenue_trend_chart(years, revenue, output_dir)`
- `create_net_income_trend_chart(years, net_income, output_dir)`
- `create_fcf_trend_chart(years, fcf, output_dir)`
- `generate_all_charts(financial_data, output_dir)`

**示例：**

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

**重要提示：** 从实际数据中动态提取年份 - 禁止硬编码。确保年份列表长度与数据值长度匹配。

### 步骤3：编写估值报告

创建一个名为 `{COMPANY_NAME}_valuation_report.md` 的 markdown 文件，结构如下：

```markdown
# {Company Name} 估值研究报告

## 1. 执行摘要

[公司概况和主要发现]

## 2. 财务分析

### 2.1 历史财务数据

![营业收入趋势](generated_images/revenue_trend.png)

![净利润趋势](generated_images/net_income_trend.png)

![自由现金流趋势](generated_images/fcf_trend.png)

### 2.2 历史财务数据表格（最近10年）

| 年份 | 营业收入 | 净利润 | 经营活动现金流 | 资本支出 | 自由现金流 | 营业收入增长率 % | 净利润增长率 % | 自由现金流增长率 % |
|------|---------|------------|---------------------|-------|----------------|------------------|---------------------|--------------|
{数据行}

### 2.3 未来10年自由现金流增长率估算

基于历史自由现金流增长率：
- [过去10年复合增长率]
- [过去5年复合增长率]
- [过去3年复合增长率]

**估算未来10年自由现金流增长率：** [X]%

**依据：** [基于行业趋势、公司指引、竞争地位等进行论证]

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

- 假设：c = ${每股自由现金流}, g = -5%, r = 10%
- 计算：V = ${c} × (1 + (-0.05)) / (0.10 - (-0.05)) = ${value}
- **内在价值：${value}/股**
- 当前股价：${current_price}
- 估值结论：[低估/高估] [X]%

#### 情景 2：0% 增长率
[相同格式]

#### 情景 3：5% 增长率
[相同格式]

#### 情景 4：7% 增长率
[相同格式]

#### 情景 5：9% 增长率
[相同格式]

#### 情景 6：估算增长率 ([X]%)
[相同格式]

### 3.3 估值结论

[各情景估值总结和建议]

## 4. 附录

### 4.1 完整财务数据表格

| 年份 | 营业收入 | 净利润 | 经营活动现金流 | 资本支出 | 自由现金流 |
|------|---------|------------|---------------------|-------|----------------|
{完整数据表格}

### 4.2 数据来源说明

- 年报（PDF）：[来源详情]
- 参考资料：[来源详情]
- stockanalysis.com：[交叉验证说明]

### 4.3 关键假设

[记录分析中所做的所有关键假设]
```

### 步骤4：数据验证

**验证要求：**
1. 使用 `stockanalysis` 技能获取过去5年的数据
2. 与参考资料进行交叉验证
3. 评估来源可信度（权威性、严谨性、相关性）
4. 关键陈述需要2个及以上独立来源
5. 记录任何差异 - 禁止隐藏矛盾

**贴现率说明：** 除非有特殊理由需要调整，否则使用10%作为贴现率。

## 资源

### scripts/generate_charts.py

用于生成财务趋势图的 Python matplotlib 脚本。

**函数：**
- `generate_all_charts(financial_data, output_dir)` - 生成全部三张图表
- `create_revenue_trend_chart(years, revenue, output_dir)` - 仅营业收入趋势
- `create_net_income_trend_chart(years, net_income, output_dir)` - 仅净利润趋势
- `create_fcf_trend_chart(years, fcf, output_dir)` - 仅自由现金流趋势

**图表规格：**
- 分辨率：300 DPI
- 折线图：12x6 英寸（16:9 宽高比）
- 专业商务风格
- 所有数据点显示标签
- 仅使用英文标签
