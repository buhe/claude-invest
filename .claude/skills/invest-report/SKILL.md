---
name: invest-report
description: 在当前文件夹生成对应公司的投资研究报告，markdown 格式。通过协调多个专业分析代理，综合分析公司的业务构成、资产负债表、估值、资本配置和管理层讨论与分析，生成完整的投资研究报告。当用户需要生成投资研究报告、全面分析公司、完整投资研究，或多维度分析公司（包括业务板块、财务状况、估值、资本配置、管理层视角）时使用
---

# 投资研究报告生成

## 概述

协调六个专业分析代理（segment-agent、balance-agent、value-agent、cap-agent、cap-acq-agent、mda-agent）对特定公司进行综合分析，汇总各代理的分析成果，生成一份完整的投资研究报告（markdown 格式）。

## 工作流程

⚠️ **强制要求**：本分析流程必须完整执行 **3次**，每轮包含全部六个分析代理。
           三轮完成后必须比对结果，差异优先通过三份报告比较解决，如果解决不了用红色标识，最后才能生成最终报告。

⚠️ **强制要求**：一定要在 claude code 页面显示每轮 subagent 运行的过程。




### 2. 准备数据
1. 调用 prepare-agent subagent 准备该公司数据

### 3. 三轮分析（必须全部完成）

🚨 **重要**：必须完成以下全部三轮分析，每轮都包含六个分析代理的独立分析。

#### 第一轮分析

使用单个消息同时启动六个分析代理（以获得最佳并行性能）：

```
【第一轮分析】请并行执行以下六个分析任务，各自独立工作：

1. segment-agent：使用 invest-seg skill 分析公司业务构成与成本结构比例
2. balance-agent：使用 invest-balance skill 分析公司资产负债表
3. value-agent：使用 invest-value skill 分析公司估值
4. cap-agent：使用 invest-cap skill 分析公司资本配置
5. cap-acq-agent：使用 invest-cap-acq skill 分析公司投资入股、收购、并购活动
6. mda-agent：使用 invest-mda skill 分析管理层对行业的战略观点和市场判断
```

每个代理会：
- 读取当前目录的年报 PDF 和参考资料 markdown
- 使用各自的 skill 生成独立的分析报告
- 输出 markdown 格式的分析结果

#### 第二轮分析

第一轮完成后，立即启动第二轮分析：

```
【第二轮分析】请再次并行执行以下六个分析任务，各自独立工作：

1. segment-agent：使用 invest-seg skill 分析公司业务构成与成本结构比例
2. balance-agent：使用 invest-balance skill 分析公司资产负债表
3. value-agent：使用 invest-value skill 分析公司估值
4. cap-agent：使用 invest-cap skill 分析公司资本配置
5. cap-acq-agent：使用 invest-cap-acq skill 分析公司投资入股、收购、并购活动
6. mda-agent：使用 invest-mda skill 分析管理层对行业的战略观点和市场判断
```

#### 第三轮分析

第二轮完成后，立即启动第三轮分析：

```
【第三轮分析】请第三次并行执行以下六个分析任务，各自独立工作：

1. segment-agent：使用 invest-seg skill 分析公司业务构成与成本结构比例
2. balance-agent：使用 invest-balance skill 分析公司资产负债表
3. value-agent：使用 invest-value skill 分析公司估值
4. cap-agent：使用 invest-cap skill 分析公司资本配置
5. cap-acq-agent：使用 invest-cap-acq skill 分析公司投资入股、收购、并购活动
6. mda-agent：使用 invest-mda skill 分析管理层对行业的战略观点和市场判断
```

### 4. 三轮结果比对与最终报告生成

#### 前置条件检查（必须全部满足才能生成最终报告）

- [ ] 第一轮分析已完成（6个代理报告已生成）
- [ ] 第二轮分析已完成（6个代理报告已生成）
- [ ] 第三轮分析已完成（6个代理报告已生成）
- [ ] 三轮结果已进行交叉比对
- [ ] 数据差异已识别并校验
- [ ] 不确定数据已用红色标识

**如果上述条件未满足，请勿生成最终报告，先执行缺失的分析轮次。**

#### 三轮结果比对步骤

1. **读取所有报告**：读取三轮共18份分析报告
2. **提取关键数据**：从每份报告中提取关键数据点和结论
3. **交叉验证**：比对三轮分析中的数据一致性
4. **识别差异**：标记三轮分析中存在差异的数据和洞见
5. **差异校验**：对差异数据查阅原始数据源进行验证
6. **标识不确定内容**：在最终报告中用红色标识不确定的内容

#### 生成最终报告

满足上述条件后，汇总三轮分析成果，按照 `references/report_template.md` 中的模板结构生成完整的投资研究报告：

**报告结构：**
1. 报告摘要（核心观点、关键指标、投资评级）
2. 业务构成与成本结构分析（来自 segment-agent）
3. 资产负债表分析（来自 balance-agent）
4. 企业估值分析（来自 value-agent）
5. 资本配置分析（来自 cap-agent 和 cap-acq-agent）
6. MD&A 管理层讨论与分析（来自 mda-agent）
7. 综合评估与投资建议（汇总各模块分析）
8. 数据来源与免责声明

**必须包含图片**：
在汇总报告中必须插入各代理生成的所有图表图片。使用以下格式：
```markdown
![图表描述](generated_images/图表文件名.png)
```

各代理应生成的图表：
- **segment-agent**: 业务板块饼图、成本结构饼图、收入趋势图、毛利率趋势图、研发投入图等
- **balance-agent**: 资产构成饼图、负债构成饼图、债务趋势图、财务比率趋势图等
- **value-agent**: 营业收入趋势图、净利润趋势图、自由现金流趋势图等
- **cap-agent**: 股息增长图、股数趋势图、资本配置分解图等
- **cap-acq-agent**: 投资入股活动汇总、收购活动分析等
- **mda-agent**: 主要为文本分析，解读管理层对行业的战略观点和市场判断，不生成图表

**图片文件名规范**（必须严格遵循）：
```
业务板块:     business_segments.png      (不是 business_segments_pie.png)
地理区域:     geographic_segments.png    (不是 geographic_segments_pie.png)
成本结构:     cost_structure.png         (不是 cost_structure_pie.png)
资产构成:     asset_composition.png
负债构成:     liability_composition.png
债务趋势:     debt_trend.png
收入趋势:     revenue_trend.png
净利润趋势:   net_income_trend.png
现金流趋势:   fcf_trend.png
股息增长:     dividend_growth.png
股数趋势:     share_count_trend.png
资本配置:     capital_allocation_breakdown.png
```

**图片引用要求**：
- 读取各代理生成的报告文件，提取其中引用的图片路径
- 在汇总报告的相应章节插入对应的图片引用
- 确保所有生成的图片都被包含在最终报告中
- **文件名必须与生成的实际文件名完全一致**

**综合评估要求：**
- 优势：汇总各模块分析中发现的正面因素
- 风险：汇总各模块分析中发现的负面因素（包括 mda-agent 识别的主要风险）
- 管理层评估：整合 mda-agent 的管理层可信度评分和能力总结
- 投资建议：基于综合分析给出明确的投资评级和理由
- 关键监控指标：列出未来需要重点跟踪的指标

**分析验证说明章节**（必须添加到最终报告中）：

```markdown
## 分析验证说明

本报告基于三轮独立分析生成：

| 轮次 | 完成时间 | 关键发现 |
|------|----------|----------|
| 第1轮 | [时间] | [摘要] |
| 第2轮 | [时间] | [摘要] |
| 第3轮 | [时间] | [摘要] |

**数据一致性验证**：
- 一致数据：[列出三轮一致的数据]
- 存在差异数据：<span style="color:red">[数据]（需校验）</span>

**不确定内容标识**：
<span style="color:red">⚠️ 以下内容存在不确定性，建议用户进行进一步校验：</span>
<span style="color:red">- [具体内容1]</span>
<span style="color:red">- [具体内容2]</span>
```

将完整的投资研究报告保存为 `[公司名称]_投资研究报告.md`，文件名使用公司中文名称。

## 语言规范

- 报告正文：中文
- 图表标签/标题：英文
- 专业术语：使用标准中文金融术语
- references 文件夹里有几篇我曾经写的研报，参考他们的风格

## 质量标准

1. **数据准确性**：确保各代理分析结果的数据一致性
2. **逻辑连贯性**：各部分分析应该相互支撑，形成完整的投资逻辑
3. **结论明确性**：给出明确的投资评级和理由
4. **风险充分性**：充分揭示投资风险，不回避负面因素

## 资源

### references/report_template.md

完整的投资研究报告模板，包含：
- 标准报告结构
- 各部分内容要求
- 综合评估指南

生成报告时参考此模板确保报告结构的完整性和一致性。

## 分析师一定是：大笨熊