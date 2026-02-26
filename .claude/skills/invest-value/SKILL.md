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

**数据验证要求：** 详见 `invest-report/references/common-guidelines.md`（数据验证规范）。

**所需数据：**
- 营业收入
- 净利润
- 经营活动现金流
- 资本支出（Capex）
- 自由现金流（FCF = 经营活动现金流 - 资本支出）
- 流通股数（用于每股计算）
- 当前股价
- 现金及现金等价物
- 短期投资
- 当前总市值

### 步骤2：生成图表（强制执行）

⚠️ **重要**：在完成报告时，**必须**执行以下步骤来生成图表：

1. **创建图表生成脚本**：在当前目录创建Python脚本
2. **执行脚本生成图表**：使用Bash工具运行Python脚本
3. **验证图表文件**：检查 `generated_images/` 目录是否包含生成的图片
4. **在报告中引用图片**：使用markdown语法引用图表

**必需图表：**

1. **营业收入趋势** (`revenue_trend.png`) - 蓝色主题
2. **净利润趋势** (`net_income_trend.png`) - 绿色主题（亏损为红色）
3. **自由现金流趋势** (`fcf_trend.png`) - 紫色主题

**创建图表生成脚本模板：**

```python
#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
os.makedirs('generated_images', exist_ok=True)

# 从实际数据中提取的年份和数值
years = ['2020', '2021', '2022', '2023', '2024']  # 替换为实际数据
revenue = [183.16, 200.23, 200.39, 445.10, 532.94]  # 替换为实际数据（亿元）
net_income = [-32.47, -0.55, 1.40, 9.92, 17.07]  # 替换为实际数据（亿元）
operating_cf = [-38.23, 24.75, 26.41, 220.04, 196.25]  # 替换为实际数据（亿元）
capex = [5.32, 5.70, 4.97, 6.06, 5.91]  # 替换为实际数据（亿元）
fcf = [round(operating_cf[i] - capex[i], 2) for i in range(len(years))]

# 图表1：收入趋势
def create_revenue_trend():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # 收入柱状图
    bars = ax1.bar(years, revenue, color='#1E88E5', edgecolor='white', linewidth=1.5)
    ax1.set_ylabel('Revenue (Billion CNY)', fontsize=11, fontweight='bold')
    ax1.set_title('Revenue Trend (2020-2024)', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, revenue):
        height = bar.get_height()
        ax1.annotate(f'{val:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    # 增长率折线图
    growth_rate = [(revenue[i] - revenue[i-1]) / revenue[i-1] * 100 if i > 0 else 0
                   for i in range(len(revenue))]
    colors = ['red' if x < 0 else '#43A047' for x in growth_rate]
    ax2.plot(years, growth_rate, marker='o', markersize=10, linewidth=2.5, color='#2E7D32')
    ax2.bar(years, growth_rate, color=colors, alpha=0.6, width=0.6)
    ax2.set_ylabel('Growth Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_title('Revenue Growth Rate', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    for i, (x, y) in enumerate(zip(years, growth_rate)):
        ax2.annotate(f'{y:.1f}%', xy=(i, y), xytext=(0, 10 if y > 0 else -15),
                    textcoords="offset points", ha='center', va='bottom' if y > 0 else 'top',
                    fontsize=10, fontweight='bold', color=colors[i])

    plt.tight_layout()
    plt.savefig('generated_images/revenue_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('[OK] revenue_trend.png')

# 图表2：净利润趋势
def create_net_income_trend():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # 净利润柱状图
    colors = ['#E53935' if x < 0 else '#43A047' for x in net_income]
    bars = ax1.bar(years, net_income, color=colors, edgecolor='white', linewidth=1.5)
    ax1.set_ylabel('Net Income (Billion CNY)', fontsize=11, fontweight='bold')
    ax1.set_title('Net Income Trend (2020-2024)', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    for bar, val in zip(bars, net_income):
        height = bar.get_height()
        ax1.annotate(f'{val:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5 if height > 0 else -15), textcoords="offset points",
                    ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=10, fontweight='bold')

    # 净利率折线图
    net_margin = [net_income[i] / revenue[i] * 100 for i in range(len(years))]
    ax2.plot(years, net_margin, marker='o', markersize=10, linewidth=2.5, color='#1E88E5')
    ax2.fill_between(years, net_margin, alpha=0.3, color='#1E88E5')
    ax2.set_ylabel('Net Margin (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_title('Net Profit Margin', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for i, (x, y) in enumerate(zip(years, net_margin)):
        ax2.annotate(f'{y:.1f}%', xy=(i, y), xytext=(0, 10),
                    textcoords="offset points", ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('generated_images/net_income_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('[OK] net_income_trend.png')

# 图表3：自由现金流趋势
def create_fcf_trend():
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(years))
    width = 0.25

    colors1 = ['#E53935' if x < 0 else '#43A047' for x in operating_cf]
    bars1 = ax.bar(x - width, operating_cf, width, label='Operating CF', color=colors1,
                   edgecolor='white', linewidth=1)

    bars2 = ax.bar(x, capex, width, label='Capital Expenditure', color='#FF9800',
                   edgecolor='white', linewidth=1)

    colors3 = ['#E53935' if x < 0 else '#1E88E5' for x in fcf]
    bars3 = ax.bar(x + width, fcf, width, label='Free Cash Flow', color=colors3,
                   edgecolor='white', linewidth=1)

    ax.set_ylabel('Amount (Billion CNY)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_title('Free Cash Flow Analysis (2020-2024)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

    plt.tight_layout()
    plt.savefig('generated_images/fcf_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('[OK] fcf_trend.png')

if __name__ == '__main__':
    create_revenue_trend()
    create_net_income_trend()
    create_fcf_trend()
    print('\nAll charts generated successfully!')
```

**执行步骤：**

1. 将上述脚本保存到当前目录（替换为从年报提取的实际数据）
2. 使用Bash工具执行：
   ```bash
   python generate_value_charts.py
   ```
3. 验证图表已生成：
   ```bash
   ls generated_images/
   ```
4. 在报告中引用图片：
   ```markdown
   ![营业收入趋势](generated_images/revenue_trend.png)
   ![净利润趋势](generated_images/net_income_trend.png)
   ![自由现金流趋势](generated_images/fcf_trend.png)
   ```

**验证清单：**
```
□ Python脚本已创建并执行
□ generated_images/目录已创建
□ 所有3张图表已生成
□ 报告中已正确引用所有图片
```

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

## 3. 资本市场担忧与利空分析

### 3.1 资本市场主要担忧

基于年报 MD&A、风险因素、投资者关系材料和市场公开信息，分析资本市场当前对公司的担忧：

**市场担忧要点：**
- [担忧1] - [具体描述和影响]
- [担忧2] - [具体描述和影响]
- [担忧3] - [具体描述和影响]

**对估值的影响：** [说明这些担忧如何影响市场对公司未来增长的预期]

### 3.2 公司主要利空因素

**短期利空（1-2年）：**
- [利空1] - [具体描述]
- [利空2] - [具体描述]

**长期利空（3年以上）：**
- [利空1] - [具体描述]
- [利空2] - [具体描述]

**利空对估值的影响：** [说明这些利空如何影响自由现金流增长率和估值]

### 3.3 现金与市值比率分析

**当前现金状况：**
- 现金及现金等价物：$X
- 短期投资：$Y
- 现金及短期投资合计：$(X + Y)
- 当前市值：$M
- **现金/市值比率：(X + Y) / M = [X]%**

**现金/市值比率分析：**
- [比率解读：如比率大于20%表示公司现金充裕，小于5%可能存在流动性压力]
- [与同行业公司对比（如有数据）]
- [对估值的影响：现金储备为估值提供下行保护]

## 4. DCF 估值

### 4.1 估值方法

使用贴现现金流（DCF）方法，贴现率 r = 10%。

公式：**V = c × (1 + g) / (r - g)**

其中：
- V = 每股内在价值
- c = 当前年度每股自由现金流
- g = 未来增长率
- r = 贴现率 = 10%

### 4.2 估值情景分析

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

### 4.3 估值结论

[综合考虑DCF估值结果、资本市场担忧和利空因素后的最终估值结论和建议]

## 5. 附录

### 5.1 完整财务数据表格

| 年份 | 营业收入 | 净利润 | 经营活动现金流 | 资本支出 | 自由现金流 |
|------|---------|------------|---------------------|-------|----------------|
{完整数据表格}

### 5.2 数据来源说明

- 年报（PDF）：[来源详情]
- 参考资料：[来源详情]
- stockanalysis.com：[交叉验证说明]

### 5.3 关键假设

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
