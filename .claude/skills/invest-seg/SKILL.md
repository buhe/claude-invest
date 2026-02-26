---
name: invest-seg
description: 在包含公司年报和参考资料（markdown）的当前目录中生成业务构成与成本结构比例研究报告（markdown 格式）。重点关注业务板块收入构成、地理区域划分、成本结构分析。当用户需要分析公司业务构成、收入来源分布或生成相关比例图表时使用。
---

# 业务构成与成本结构比例报告生成 Skill

## 工作流程

### 1. 准备阶段

首先确认当前目录包含：
- 公司最新年报（为了保证你的专注度，只使用最新一年的财报作为资料）
- 参考资料文件（markdown 格式）

使用 `ls` 命令检查文件列表。

### 2. 数据收集与验证

**第一步：查找官方报告板块（必须首先完成）**

在年报中搜索以下关键词查找官方报告板块：
- "Reportable Segments"
- "Operating Segments"
- "Business Segments"
- "Segment Information"
- 通常位于：MD&A章节 或 财务报表附注(Note)

**验证要求**：
```
□ 找到所有官方报告板块
□ 收入加起来 = 总收入（100%）
□ 如果不等于100%，查找原因（如：
  - 未分配收入/Other
  - 汇率调整
  - 消除分部间收入
）
```

**常见公司类型的板块结构**：

| 公司类型 | 典型板块数量 | 典型命名方式 | 验证要点 |
|---------|-------------|-------------|---------|
| 半导体/硬件 | 2-4个 | 按产品线或客户类型 | 注意细分市场≠官方板块 |
| 消费品 | 3-6个 | 按产品类别或品牌 | 通常完整拆分 |
| 互联网/软件 | 2-5个 | 按服务类型 | 注意"未分配收入" |
| 工业/制造 | 3-5个 | 按业务线或地区 | 可能按地区拆分 |
| 金融 | 2-4个 | 按业务类型 | 注意分部间抵消 |

**第二步：细分市场数据（严禁估算）**

⚠️ **重要：只使用年报中明确披露的细分市场数据**

**禁止行为**：
- ❌ 不要使用投资者关系材料、演示文稿、新闻稿中的数据
- ❌ 不要根据部分数据推算整体（如"约占X板块的91%"）
- ❌ 不要使用任何形式的估算、推断、猜测
- ❌ 不要引用行业报告、分析师报告中的细分数据

**允许行为**：
- ✅ 只使用年报中明确披露的细分市场数据
- ✅ 数据必须有具体的收入数字（不能只是百分比或描述）
- ✅ 数据来源必须明确标注为"年报第X章"或"Note X"

**如果年报没有细分市场数据**：
- 跳过细分市场分析
- 只分析官方报告板块
- 不要试图从其他来源"补充"数据

**数据来源评估**：详见 `invest-report/references/common-guidelines.md`（数据验证规范）。

**使用 stockanalysis skill**：
```
使用 stockanalysis skill 获取最近五年的财务数据进行交叉验证
```

### 3. 报告结构

生成包含以下章节的 Markdown 报告：

#### 第 1 章：官方报告板块分析（必须放在最前面）
- **第一张表格必须列出官方报告板块**
- 验证要求：所有官方报告板块收入加起来必须等于总收入（100%）
- 各板块收入、占比、同比增长
- **插入图表：业务板块收入饼图**（使用官方报告板块数据）

#### 第 2 章：地理区域分析
- 地理区域收入分布
- 发货目的地vs最终客户所在地的说明（如适用）
- **插入图表：地理区域收入饼图**

#### 第 3 章：成本结构分析
- 成本构成比例
- 成本变化趋势
- **插入图表：成本构成比例饼图**

**重要提醒**：
1. 第一张业务板块表格必须使用官方报告板块，加起来=100%
2. **不要提供细分市场分析**，除非年报中有明确披露
3. **严禁估算任何数据**，只使用官方GAAP披露


### 4. 图表生成规则

**图表生成规范：** 详见 `invest-report/references/common-guidelines.md`（图表生成通用规范）。

**强制要求：必须生成图表并插入到报告中**

⚠️ **重要**：在完成报告时，**必须**执行以下步骤来生成图表：

1. **创建图表生成脚本**：在当前目录创建Python脚本，使用从年报中提取的实际数据
2. **执行脚本生成图表**：使用Bash工具运行Python脚本
3. **验证图表文件**：检查 `generated_images/` 目录是否包含生成的图片
4. **在报告中引用图片**：使用markdown语法 `![描述](generated_images/文件名.png)` 引用图表

**图表模板**：

创建一个Python脚本（如 `generate_seg_charts.py`）来生成图表：

```python
#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
os.makedirs('generated_images', exist_ok=True)

# 业务板块饼图
def create_business_segments_pie(segments, percentages, year):
    labels = [f'{s}\n{p}%' for s, p in zip(segments, percentages)]
    colors = ['#1E88E5', '#43A047', '#FB8C00', '#E53935', '#8E24AA']
    explode = [0.05 if p == max(percentages) else 0 for p in percentages]

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(percentages, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Business Segments Revenue ({year})', fontsize=14, fontweight='bold')
    plt.savefig('generated_images/business_segments.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: business_segments.png')

# 地理区域饼图
def create_geographic_segments_pie(regions, percentages, year):
    labels = [f'{r}\n{p}%' for r, p in zip(regions, percentages)]
    colors = ['#1E88E5', '#43A047', '#FB8C00', '#E53935']
    explode = [0.05 if p == max(percentages) else 0 for p in percentages]

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(percentages, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Geographic Revenue ({year})', fontsize=14, fontweight='bold')
    plt.savefig('generated_images/geographic_segments.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: geographic_segments.png')

# 成本结构饼图
def create_cost_structure_pie(categories, percentages, year):
    labels = [f'{c}\n{p}%' for c, p in zip(categories, percentages)]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(percentages, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Cost Structure ({year})', fontsize=14, fontweight='bold')
    plt.savefig('generated_images/cost_structure.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated: cost_structure.png')

# 调用函数生成图表（使用从年报中提取的实际数据）
if __name__ == '__main__':
    year = '2024'  # 从数据中提取

    # 业务板块 - 替换为实际数据
    segments = ['Accommodation', 'Transportation', 'Tourism', 'Corporate', 'Other']
    percentages = [44.4, 41.7, 8.0, 5.0, 0.9]
    create_business_segments_pie(segments, percentages, year)

    # 地理区域 - 替换为实际数据
    regions = ['China Domestic', 'International']
    percentages = [80.6, 19.4]
    create_geographic_segments_pie(regions, percentages, year)

    # 成本结构 - 替换为实际数据
    categories = ['COGS', 'S&M', 'R&D', 'G&A']
    percentages = [20.5, 24.5, 8.4, 6.6]
    create_cost_structure_pie(categories, percentages, year)
```

**执行步骤**：

1. 将上述脚本保存到当前目录（替换为从年报提取的实际数据）
2. 使用Bash工具执行：
   ```bash
   python generate_seg_charts.py
   ```
3. 验证图表已生成：
   ```bash
   ls generated_images/
   ```
4. 在报告中引用图片：
   ```markdown
   ![业务板块收入构成](generated_images/business_segments.png)
   ![地理区域收入构成](generated_images/geographic_segments.png)
   ![成本构成](generated_images/cost_structure.png)
   ```

**图片文件名规范**：
- `business_segments.png` - 业务板块饼图
- `geographic_segments.png` - 地理区域饼图
- `cost_structure.png` - 成本结构饼图

**不要使用 `_pie` 后缀**，直接使用上述文件名。

**验证清单**：
```
□ Python脚本已创建并执行
□ generated_images/目录已创建
□ 所有3张图表已生成
□ 报告中已正确引用所有图片
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

**语言和图表规范：** 详见 `invest-report/references/common-guidelines.md`

### 6.1 业务板块分析重要注意事项 ⚠️⚠️⚠️

**核心原则：只使用官方GAAP披露的数据**

1. **必须查找官方报告板块**：
   - 在年报中搜索："Reportable Segments"、"Operating Segments"、"Business Segments"或"Segment Information"
   - 这些通常位于MD&A章节或财务报表附注(Note)
   - **验证要求**：所有官方报告板块的收入加起来必须等于总收入（100%）

2. **严禁估算数据**：
   - ❌ 不要使用投资者关系材料、演示文稿中的数据
   - ❌ 不要根据部分数据推算整体（如"约占X板块的91%"）
   - ❌ 不要引用行业报告、分析师报告中的细分数据
   - ❌ 不要提供任何形式的估算、推断、猜测

3. **如果年报没有细分市场数据**：
   - ✅ 只分析官方报告板块
   - ✅ 跳过细分市场分析
   - ❌ 不要试图从其他来源"补充"数据

4. **数据验证检查清单**：
   ```
   □ 官方报告板块收入总和 = 总收入（100%）
   □ 所有数据来源明确标注（如"年报第X章"或"Note X"）
   □ 没有任何估算、推断或猜测的数据
   ```

### 6.2 地理区域分析重要注意事项 ⚠️

**发货目的地 vs 最终客户所在地**：

许多公司（特别是硬件、半导体、科技制造公司）的地理收入数据可能基于**发货目的地**而非**最终客户所在地**。这会导致数据失真：

| 情况 | 问题示例 |
|------|----------|
| OEM/ODM制造中心 | 产品发货到台湾/富士康/广达组装，但最终客户是美国云服务商 |
| 区域分销中心 | 产品发货到新加坡/香港分销中心，但最终客户是东南亚各国 |
| 离岸贸易 | 产品发货到自由贸易区，但最终客户是其他国家 |

**正确分析原则**：

1. **识别数据口径**：年报通常会说明地理收入是基于"shipped to"还是"sold to"
2. **追索最终客户**：对于制造公司，需分析最终客户的实际所在地
3. **典型模式判断**：
   - **美国公司**：美国市场通常最大（本土云服务商、互联网公司）
   - **全球品牌**：发达市场（美、欧、日）通常占主导
   - **出口导向**：如果台湾/香港占比异常高，可能是发货地而非客户地

4. **修正说明**：如果数据基于发货地，必须在报告中添加说明：
   ```markdown
   **重要说明**：本地理收入数据基于发货目的地统计。
   实际上，发往台湾OEM/ODM厂商的产品最终销往美国和中国的客户。
   按最终客户所在地计算，美国/中国应该是最大的市场。
   ```

5. **典型客户分析**：结合公司业务特点判断合理分布：
   - 云服务商（AWS、Azure、GCP）→ 美国
   - 互联网巨头（Meta、Google、Microsoft）→ 美国
   - 消费电子 → 发达市场 + 中国
   - OEM/ODM → 可能是发货地，非最终客户地

### 7. 输出文件

报告保存为：`[公司名称]_业务构成与成本结构报告.md`
