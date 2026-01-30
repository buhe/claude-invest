# 投资研究报告图片文件名规范

## 问题说明

之前存在的问题：报告中的图片引用文件名与实际生成的图片文件名不一致，例如：
- 报告引用：`generated_images/cost_structure_pie.png`
- 实际文件：`generated_images/cost_structure.png`

## 解决方案

通过引入统一的文件名常量管理机制，确保所有模块使用一致的文件名。

### 1. 创建的常量文件

每个技能模块都有 `scripts/__init__.py` 文件定义图片文件名常量：

#### invest-seg/scripts/__init__.py
```python
CHART_BUSINESS_SEGMENTS = "business_segments.png"
CHART_GEOGRAPHIC_SEGMENTS = "geographic_segments.png"
CHART_COST_STRUCTURE = "cost_structure.png"
```

#### invest-balance/scripts/__init__.py
```python
CHART_ASSET_COMPOSITION = "asset_composition.png"
CHART_LIABILITY_COMPOSITION = "liability_composition.png"
CHART_DEBT_TREND = "debt_trend.png"
```

#### invest-value/scripts/__init__.py
```python
CHART_REVENUE_TREND = "revenue_trend.png"
CHART_NET_INCOME_TREND = "net_income_trend.png"
CHART_FCF_TREND = "fcf_trend.png"
```

#### invest-cap/scripts/__init__.py
```python
CHART_DIVIDEND_GROWTH = "dividend_growth.png"
CHART_SHARE_COUNT_TREND = "share_count_trend.png"
CHART_CAPITAL_ALLOCATION_BREAKDOWN = "capital_allocation_breakdown.png"
```

### 2. 修改的文件

| 文件 | 修改内容 |
|------|----------|
| invest-seg/scripts/generate_charts.py | 使用常量替代硬编码文件名 |
| invest-balance/scripts/asset_composition.py | 使用常量替代硬编码文件名 |
| invest-balance/scripts/liability_composition.py | 使用常量替代硬编码文件名 |
| invest-balance/scripts/debt_trend.py | 使用常量替代硬编码文件名 |
| invest-value/scripts/generate_charts.py | 使用常量替代硬编码文件名 |
| invest-cap/scripts/chart_generator.py | 使用常量替代硬编码文件名；修复 `capital_allocation.png` → `capital_allocation_breakdown.png` |
| invest-seg/SKILL.md | 添加文件名规范说明 |
| invest-report/SKILL.md | 添加完整的文件名规范表格 |

### 3. 标准文件名列表

| 图表类型 | 正确文件名 | ❌ 错误文件名 |
|---------|-----------|--------------|
| 业务板块饼图 | business_segments.png | business_segments_pie.png |
| 地理区域饼图 | geographic_segments.png | geographic_segments_pie.png |
| 成本结构饼图 | cost_structure.png | cost_structure_pie.png |
| 资产构成饼图 | asset_composition.png | - |
| 负债构成饼图 | liability_composition.png | - |
| 债务趋势图 | debt_trend.png | - |
| 收入趋势图 | revenue_trend.png | - |
| 净利润趋势图 | net_income_trend.png | - |
| 自由现金流趋势图 | fcf_trend.png | - |
| 股息增长图 | dividend_growth.png | - |
| 股数趋势图 | share_count_trend.png | - |
| 资本配置图 | capital_allocation_breakdown.png | capital_allocation.png |

### 4. 如何确保一致性

1. **所有新图表必须使用常量**：在生成图表的 Python 代码中，使用 `from . import CHART_XXX` 导入常量
2. **报告引用必须匹配**：在 Markdown 报告中引用图片时，使用与常量相同的文件名
3. **参考 SKILL.md**：每个技能的 SKILL.md 文件都包含了正确的文件名示例

### 5. 验证方法

生成报告后，运行以下命令验证所有图片引用是否正确：

```bash
# 提取报告中的图片引用
grep -o 'generated_images/[^)]*' report.md | sort -u > referenced.txt

# 列出实际生成的图片文件
ls generated_images/*.png | xargs -n1 basename | sort > actual.txt

# 比较差异
diff referenced.txt actual.txt
```

## 更新日期

2025年1月30日
