# Automated Investment Research System

自动化投资分析系统 - 通过5轮独立分析（每轮6个代理）生成专业的投资研究报告，自动翻译成英文并更新README。

[English Version](README_EN.md) | [使用指南](USAGE_GUIDE.md)

## 🎯 系统特点

- ✅ **全自动流程**：从下载财报到生成报告全程自动化
- ✅ **5轮独立分析**：每轮6个专业代理，共30份独立分析
- ✅ **交叉验证**：自动对比并解决数据冲突
- ✅ **双语输出**：自动生成中英文版本
- ✅ **专业图表**：每份报告包含6-10张数据图表
- ✅ **自动更新README**：维护所有报告的索引

## 📊 分析流程

```
公司输入 → 下载财报 → 5轮分析(30份报告) → 交叉验证 → 生成最终报告 → 翻译英文 → 更新README
```

## 🚀 快速开始

### 方法一：使用Claude Code（推荐）

```bash
# 在Claude Code中执行
/研究 Apple Inc.

# 或中文公司
/研究 腾讯控股
```

### 方法二：使用自动化脚本

```bash
# 美股公司
python auto_analysis.py "Apple Inc." SEC

# 港股公司
python auto_analysis.py "腾讯控股" HKEX

# 或使用shell脚本
bash run_analysis.sh "Apple Inc." SEC
```

## 📁 项目结构

```
claude-invest/
├── .claude/
│   ├── skills/           # 分析技能
│   │   ├── invest-report/ # 主协调技能
│   │   ├── invest-seg/    # 业务构成分析
│   │   ├── invest-balance/# 资产负债表分析
│   │   ├── invest-value/  # 估值分析
│   │   ├── invest-cap/    # 资本配置分析
│   │   ├── invest-cap-acq/# 投资并购分析
│   │   ├── invest-mda/    # MD&A分析
│   │   ├── sec-fetcher/   # SEC财报下载
│   │   └── hkex-fetcher/  # HKEX财报下载
│   └── agents/           # 代理配置
│       ├── prepare-agent  # 数据准备代理
│       ├── segment-agent  # 业务构成代理
│       ├── balance-agent  # 资产负债表代理
│       ├── value-agent    # 估值代理
│       ├── cap-agent      # 资本配置代理
│       ├── cap-acq-agent  # 投资并购代理
│       ├── mda-agent      # MD&A代理
│       └── diff-agent     # 交叉验证代理
├── input/                # 分析输出目录
├── auto_analysis.py      # 主自动化脚本
├── run_analysis.sh       # Shell脚本封装
├── update_readme.py      # README更新脚本
├── README.md             # 本文件
├── README_EN.md          # 英文版README
└── USAGE_GUIDE.md        # 详细使用指南
```

## 🤖 分析代理

| 代理 | 技能 | 分析内容 |
|-----|-------|---------|
| **segment-agent** | invest-seg | 业务构成、收入分布、成本结构 |
| **balance-agent** | invest-balance | 资产负债表、债务分析、财务健康度 |
| **value-agent** | invest-value | DCF估值、内在价值、安全边际 |
| **cap-agent** | invest-cap | 资本配置、分红、回购 |
| **cap-acq-agent** | invest-cap-acq | 投资活动、并购交易 |
| **mda-agent** | invest-mda | 管理层质量、战略、可信度 |

## 📈 报告结构

每份投资研究报告包含：

1. **报告摘要** - 核心观点、关键指标、投资评级
2. **业务构成分析** - 业务板块、地理分布、成本结构
3. **资产负债表分析** - 资产质量、债务水平、财务健康度
4. **企业估值分析** - DCF模型、内在价值、安全边际
5. **资本配置分析** - 分红政策、股票回购、投资效率
6. **管理层讨论分析** - 高管团队、战略观点、可信度评分
7. **综合评估与投资建议** - 优势、风险、投资建议
8. **数据来源与免责声明** - 数据来源、验证说明

## 🔬 数据验证

所有报告经过严格验证：

- **5轮独立分析**：每个模块分析5次
- **交叉验证**：diff-agent对比所有30份输出
- **多数原则**：冲突通过多数投票解决
- **来源优先级**：SEC财报 > StockAnalysis.com > 估算
- **不一致标识**：差异清晰标记

### 一致性标识

| 符号 | 含义 |
|-----|------|
| ✅ | 5/5轮一致 |
| ⚠️ | 4/5或3/5一致（已记录） |
| 🔴 | 重大差异（需校验） |

## 🌐 支持的市场

| 市场 | 数据源 | 报告类型 |
|-----|-------|---------|
| **美国** | SEC EDGAR | 10-K（本土）、20-F（外国） |
| **香港** | HKEXnews | 年报 |
| **中国** | HKEXnews（H股） | 年报 |

## 📝 最新报告

---

## Prerequisites

- **Financial** skill need `agent-browser`

  - Install `agent-browser` and make sure it is available on your PATH:

    ```bash
    npm install -g agent-browser
    agent-browser install  # Download Chromium
    ```

- A working shell (macOS, Linux, or Windows WSL) with network access.

## invest-report

Claude Code prompt：「研究苹果公司，生成一份中文投资报告」

![image-20260128195833127](https://raw.githubusercontent.com/buhe/pic/main/uPic/image-20260128195833127.png)

*The generated report can be in various languages; for example, **it can be explicitly stated that the generated report will be in English**.*

---

## 🔧 详细文档

- [使用指南](USAGE_GUIDE.md) - 详细的系统使用说明
- [English README](README_EN.md) - 英文版README
- [报告模板](.claude/skills/invest-report/references/report_template.md) - 投资报告模板

## ⚠️ 免责声明

**重要提示**：本报告仅供研究和教育用途，不构成投资建议。投资有风险，请：

- 进行自己的尽职调查
- 咨询合格财务顾问
- 考虑自己的风险承受能力
- 从主要来源验证信息

---

**最后更新**: 2026-03-05
**系统版本**: 2.0
**生成工具**: Claude Code Investment Research System