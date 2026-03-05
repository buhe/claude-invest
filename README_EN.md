# Automated Investment Research System

A sophisticated multi-agent investment research system that performs comprehensive company analysis through 5 rounds of independent evaluation by 6 specialized agents.

## 🎯 Overview

This system automates the process of generating professional investment research reports by:

1. **Downloading financial reports** from SEC (US companies) or HKEX (HK companies)
2. **Running 5 rounds of analysis** - Each round uses 6 specialized agents
3. **Cross-validation** - Compares all 30 analyses and resolves conflicts
4. **Generating final reports** - Creates validated, comprehensive investment reports
5. **Translating to English** - Produces bilingual reports (Chinese & English)
6. **Updating README** - Automatically maintains an index of all reports

## 📊 System Architecture

### Analysis Agents

| Agent | Skill | Focus Area |
|-------|-------|-----------|
| **segment-agent** | invest-seg | Business segments, revenue mix, cost structure |
| **balance-agent** | invest-balance | Balance sheet, debt analysis, financial health |
| **value-agent** | invest-value | DCF valuation, intrinsic value, sensitivity analysis |
| **cap-agent** | invest-cap | Capital allocation, dividends, share buybacks |
| **cap-acq-agent** | invest-cap-acq | Investment activities, M&A transactions |
| **mda-agent** | invest-mda | Management quality, strategy, credibility |

### Workflow

```
Company Input
    ↓
Download Financial Reports (SEC/HKEX)
    ↓
┌─────────────────────────────────────┐
│ Round 1: 6 agents analyze in parallel│
├─────────────────────────────────────┤
│ Round 2: 6 agents analyze in parallel│
├─────────────────────────────────────┤
│ Round 3: 6 agents analyze in parallel│
├─────────────────────────────────────┤
│ Round 4: 6 agents analyze in parallel│
├─────────────────────────────────────┤
│ Round 5: 6 agents analyze in parallel│
└─────────────────────────────────────┘
    ↓
Diff-Agent: Cross-validate all rounds
    ↓
Generate Final Report (validated data)
    ↓
Translate to English
    ↓
Update README
```

## 🚀 Quick Start

### Prerequisites

1. **Claude Code** - Install from [Anthropic](https://claude.ai/code)
2. **agent-browser** (for HKEX/HK companies):
   ```bash
   npm install -g agent-browser
   agent-browser install
   ```

### Analyze a Company

#### Option 1: Using Claude Code (Recommended)

```bash
# In Claude Code
/研究 Apple Inc.

# For Chinese companies
/研究 腾讯控股
```

#### Option 2: Using the automation script

```bash
# US Company
python auto_analysis.py "Apple Inc." SEC

# HK Company
python auto_analysis.py "腾讯控股" HKEX

# Or use the shell script
bash run_analysis.sh "Apple Inc." SEC
```

## 📁 Project Structure

```
claude-invest/
├── .claude/
│   ├── skills/           # Analysis skills
│   │   ├── invest-report/ # Main coordination skill
│   │   ├── invest-seg/    # Segment analysis
│   │   ├── invest-balance/# Balance sheet analysis
│   │   ├── invest-value/  # Valuation analysis
│   │   ├── invest-cap/    # Capital allocation analysis
│   │   ├── invest-cap-acq/# Investment & M&A analysis
│   │   ├── invest-mda/    # MD&A analysis
│   │   ├── sec-fetcher/   # SEC report downloader
│   │   └── hkex-fetcher/  # HKEX report downloader
│   └── agents/           # Agent configurations
│       ├── prepare-agent  # Data preparation agent
│       ├── segment-agent  # Segment analysis agent
│       ├── balance-agent  # Balance sheet agent
│       ├── value-agent    # Valuation agent
│       ├── cap-agent      # Capital allocation agent
│       ├── cap-acq-agent  # Investment & M&A agent
│       ├── mda-agent      # MD&A agent
│       └── diff-agent     # Cross-validation agent
├── input/                # Analysis output directory
│   ├── references.md     # Extracted financial data
│   ├── *.pdf             # Annual reports
│   ├── *.htm             # SEC filings
│   └── generated_images/ # Analysis charts
├── auto_analysis.py      # Main automation script
├── run_analysis.sh       # Shell script wrapper
├── update_readme.py      # README updater
└── README.md             # This file
```

## 📊 Report Structure

Each investment research report includes:

### 1. Executive Summary
- Core investment thesis
- Key financial metrics
- Investment rating (Buy/Hold/Sell)
- Quick stats table

### 2. Business Segments Analysis
- Revenue mix by segment
- Geographic distribution
- Cost structure analysis
- Segment performance trends

### 3. Balance Sheet Analysis
- Asset composition
- Liability structure
- Debt analysis
- Financial health metrics
- Overall credit rating

### 4. Valuation Analysis
- DCF model with multiple scenarios
- Intrinsic value calculation
- Sensitivity analysis
- Market concerns analysis
- Valuation conclusion

### 5. Capital Allocation Analysis
- Dividend policy & history
- Share buyback programs
- Capital expenditure trends
- Investment efficiency (ROIC)

### 6. Management Assessment
- Executive team profiles
- Industry expertise
- Strategic vision
- Prediction accuracy
- Credibility score (out of 5)

### 7. Investment Recommendation
- Comprehensive strengths & weaknesses
- Risk assessment
- Clear investment rating
- Entry price guidance
- Key monitoring indicators

## 🔬 Data Validation

All reports undergo rigorous validation:

1. **5 Independent Rounds**: Each module analyzed 5 times
2. **Cross-Validation**: Diff-agent compares all 30 outputs
3. **Majority Rule**: Conflicts resolved by majority voting
4. **Source Priority**: SEC filings > StockAnalysis.com > Estimates
5. **Inconsistency Flagging**: Discrepancies clearly marked

### Consistency Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | 5/5 rounds consistent |
| ⚠️ | 4/5 or 3/5 consistent (documented) |
| 🔴 | Major discrepancy (requires verification) |

## 🌐 Supported Markets

| Market | Source | Report Type |
|--------|--------|-------------|
| **US** | SEC EDGAR | 10-K (domestic), 20-F (foreign) |
| **Hong Kong** | HKEXnews | Annual Reports |
| **China** | HKEXnews (H-share) | Annual Reports |

## 📝 Language Support

- **Report Language**: Chinese (primary), English (translated)
- **Chart Labels**: English
- **Code & Tables**: English

## 🎨 Generated Charts

Each report includes up to 10 professional charts:

- Business segments pie chart
- Geographic distribution pie chart
- Cost structure breakdown
- Asset composition
- Liability composition
- Revenue trend (5 years)
- Net income trend (5 years)
- Free cash flow trend (5 years)
- Dividend growth trend
- Capital allocation breakdown

All charts generated using Python matplotlib at 300 DPI.

## 🔧 Configuration

### Customize Analysis Rounds

Edit `auto_analysis.py`:

```python
self.rounds = 5  # Change number of analysis rounds
```

### Add New Agents

1. Create skill in `.claude/skills/`
2. Create agent in `.claude/agents/`
3. Add to agent list in `auto_analysis.py`

## 📈 Example Output

### Quick Stats Section

```markdown
| Metric | Value | YoY Change |
|--------|-------|------------|
| Revenue | €20.6B | +0.2% |
| Net Income | €2.9B | -6.7% |
| FCF | €3.8B | +7.5% |
```

### Investment Rating

```markdown
**RATING**: Moderate Buy

**Recommendation**:
- Reasonable valuation, intrinsic value (CHF 137.8) ≈ current price
- Strong financial health, debt-to-equity ratio only 34.7%
- Management credibility 4.1/5
- Wait for better entry point (below CHF 120) due to China demand weakness
```

## ⚠️ Disclaimer

**IMPORTANT**: These reports are for research and educational purposes only. They do not constitute investment advice. Always:

- Conduct your own due diligence
- Consult qualified financial advisors
- Consider your risk tolerance
- Verify information from primary sources

### Risk Factors

- Past performance ≠ future results
- Market conditions can change rapidly
- Currency fluctuations affect foreign stocks
- Analysis based on historical data

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional analysis modules
- More data sources
- Enhanced translation
- Additional market support
- UI/visualizations

## 📞 Support

For issues or questions:

1. Check existing reports in `input/`
2. Review `.claude/skills/` for methodology
3. Open a GitHub issue

## 📄 License

This project is for personal and educational use.

---

**Last Updated**: 2026-03-05
**System Version**: 2.0
**Generated by**: Claude Code Investment Research System
