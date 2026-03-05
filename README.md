# Claude Investment Research

Automated investment research analysis system powered by Claude Code.

## Prerequisites

```bash
npm install -g agent-browser
agent-browser install
```

## Workflow

1. **Download Financial Reports** - SEC (US) or HKEX (Hong Kong)
2. **Prepare Data** - Extract 5-year financial statements from StockAnalysis.com
3. **5-Round Analysis** - 6 specialized subagents analyze independently in parallel
4. **Cross-Comparison** - Diff-agent resolves conflicts across 5 rounds
5. **Generate Report** - Final comprehensive investment research report

## Skills

| Skill | Description |
|-------|-------------|
| `sec-fetcher` | Download 10-K (US) or 20-F (foreign) from SEC EDGAR |
| `hkex-fetcher` | Download annual reports from HKEX disclosure platform |
| `stockanalysis` | Extract financial data from StockAnalysis.com |
| `invest-seg` | Analyze business segments and cost structure |
| `invest-balance` | Analyze balance sheet |
| `invest-value` | Analyze valuation (DCF, cash flow) |
| `invest-cap` | Analyze capital allocation (dividends, buybacks) |
| `invest-cap-acq` | Analyze M&A and investment activities |
| `invest-mda` | Analyze management discussion and strategy |
| `invest-report` | Coordinate full analysis workflow and generate final report |

## Subagents

| Agent | Uses Skill | Analysis Focus |
|-------|------------|----------------|
| `prepare-agent` | `sec-fetcher`, `hkex-fetcher`, `stockanalysis` | Download reports and extract financial data |
| `segment-agent` | `invest-seg` | Business segments and cost structure |
| `balance-agent` | `invest-balance` | Balance sheet analysis |
| `value-agent` | `invest-value` | Valuation (DCF, cash flow) |
| `cap-agent` | `invest-cap` | Capital allocation (dividends, buybacks) |
| `cap-acq-agent` | `invest-cap-acq` | M&A and investment activities |
| `mda-agent` | `invest-mda` | Management discussion and strategy |
| `diff-agent` | - | Cross-validate and resolve conflicts across rounds |

## Usage

Research Apple and generate an investment report

Claude Code prompt:「研究苹果公司，生成一份中文投资报告」

### Output

Comprehensive markdown report with analysis, charts, and data validation.
![image-20260128195833127](https://raw.githubusercontent.com/buhe/pic/main/uPic/image-20260128195833127.png)

*The generated report can be in various languages; for example, **it can be explicitly stated that the generated report will be in English**.*
