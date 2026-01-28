---
name: invest-seg
description: 在包含公司年报（PDF）和参考资料（markdown）的当前目录中生成业务构成与成本结构比例研究报告（markdown 格式）。重点关注业务板块收入构成、地理区域划分、成本结构分析。当用户需要分析公司业务构成、收入来源分布或生成相关比例图表时使用。
---

# 业务构成与成本结构比例报告生成 Skill

## 工作流程

### 1. 准备阶段

首先确认当前目录包含：
- 公司最新年报（PDF 格式）
- 参考资料文件（markdown 格式）

使用 `ls` 命令检查文件列表。

### 2. 数据收集与验证

**数据来源评估**：
- 交叉对比参考资料与 stockanalysis skill 数据
- 评估数据来源的权威性、严谨性和相关性
- 关键主张需要 2 个或以上独立来源支持
- 记录所有矛盾点，不得隐藏

**使用 stockanalysis skill**：
```
使用 stockanalysis skill 获取最近五年的财务数据进行交叉验证
```

### 3. 报告结构

生成包含以下章节的 Markdown 报告：

#### 第 1 章：业务板块分析
- 列出所有业务板块及其收入占比
- 最近一年的增长率及主要原因
- 地理区域划分
- **插入图表 4：业务板块收入饼图**
- **插入图表：地理区域收入饼图**

#### 第 2 章：成本结构分析
- 成本构成比例
- **插入图表：成本构成比例饼图**


### 4. 图表生成规则

**关键要求**：
- 最多生成 10 张图表
- 所有图表标签和标题必须使用**英文**（即使报告是中文）
- 分辨率：300 DPI
- 线图/柱状图使用 16:9 比例 (figsize=12x6)
- 饼图使用 1:1 比例 (figsize=10x8)
- Python 代码保存在 `scripts/` 文件夹
- 图表保存到 `generated_images/` 目录

**图表模板**：

在报告中生成图表时，使用 scripts/generate_charts.py 中的函数：

```python
# 业务板块饼图
segments = ['Product A', 'Product B', 'Services', 'Other']  # 必须使用英文名
percentages = [35, 25, 30, 10]
create_business_segments_pie(segments, percentages, '2024')

# 地理区域饼图
regions = ['North America', 'Europe', 'Asia Pacific', 'Other']
percentages = [40, 30, 25, 5]
create_geographic_segments_pie(regions, percentages, '2024')

# 成本结构饼图
cost_categories = ['COGS', 'R&D', 'SG&A', 'Other']
percentages = [50, 15, 25, 10]
create_cost_structure_pie(cost_categories, percentages, '2024')

# 收入趋势线图
years = ['2020', '2021', '2022', '2023', '2024']
revenues = [100, 110, 125, 140, 155]
create_revenue_trend_line(years, revenues, 'Company Name')

# 债务权益柱状图
debt = [30, 35, 32, 28, 25]
equity = [70, 75, 80, 85, 90]
create_debt_equity_bar(years, debt, equity, 'Company Name')
```

**插入图表到报告**：
```markdown
![业务板块收入构成](generated_images/business_segments.png)
```

### 5. 代码执行

运行 Python 脚本生成图表：

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/Users/guyanhua/.claude/skills/invest-seg/scripts')
from generate_charts import *

# 在此处调用图表生成函数
# 示例：
# create_business_segments_pie(['Segment A', 'Segment B'], [60, 40], '2024')
EOF
```

### 6. 注意事项

- 年份必须从实际数据中提取，不要硬编码
- 地理区域划分需明确（如印度、中东归属）
- 时间基准：昨日日期
- 数据矛盾必须在报告中注明
- 所有图表使用英文标签

### 7. 输出文件

报告保存为：`[公司名称]_业务构成与成本结构报告.md`
