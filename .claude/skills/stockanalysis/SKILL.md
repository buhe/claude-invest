---
name: stockanalysis
description: Fetch and extract company financial data from stockanalysis.com. Use when Claude needs to retrieve stock financial statements (income statement, balance sheet, cash flow), company overview, or key financial metrics like revenue, net income, operating cash flow, capital expenditures, and free cash flow for any publicly traded company by ticker symbol.
---

# Stockanalysis

## Overview

Fetches company financial data from [stockanalysis.com](https://stockanalysis.com/) using agent-browser or curl. Retrieves financial statements and key metrics for any publicly traded company by ticker symbol.

## URL Patterns

| Data Type | URL Pattern | Example |
|------------|-------------|---------|
| Company Overview | `https://stockanalysis.com/stocks/{TICKER}/` | https://stockanalysis.com/stocks/aapl/ |
| Income Statement | `https://stockanalysis.com/stocks/{TICKER}/financials/` | https://stockanalysis.com/stocks/aapl/financials/ |
| Balance Sheet | `https://stockanalysis.com/stocks/{TICKER}/financials/balance-sheet/` | https://stockanalysis.com/stocks/aapl/financials/balance-sheet/ |
| Cash Flow Statement | `https://stockanalysis.com/stocks/{TICKER}/financials/cash-flow-statement/` | https://stockanalysis.com/stocks/aapl/financials/cash-flow-statement/ |

## Quick Start

### Basic Company Data

```bash
agent-browser open "https://stockanalysis.com/stocks/{TICKER}/"
agent-browser snapshot
```

### Financial Statements

```bash
agent-browser open "https://stockanalysis.com/stocks/{TICKER}/financials/"
agent-browser open "https://stockanalysis.com/stocks/{TICKER}/financials/cash-flow-statement/"
```

## Data Extraction

### Key Financial Metrics

| Metric | Location | Description |
|---------|-----------|-------------|
| Revenue | Income Statement | Total revenue from operations |
| Net Income | Income Statement | Profit after all expenses and taxes |
| Operating Cash Flow | Cash Flow Statement | Cash generated from core business operations |
| Capital Expenditures (CapEx) | Cash Flow Statement | Cash spent on fixed assets and equipment |
| Free Cash Flow (FCF) | Cash Flow Statement | Operating Cash Flow - CapEx |
| Total Assets | Balance Sheet | All assets owned by the company |
| Total Liabilities | Balance Sheet | All debts and obligations |

### Free Cash Flow Calculation

```
FCF = Operating Cash Flow - Capital Expenditures
```

## Workflow

1. **Construct URL** using ticker symbol: `https://stockanalysis.com/stocks/{TICKER}/financials/`

2. **Open page** with agent-browser:
   ```bash
   agent-browser open "https://stockanalysis.com/stocks/{TICKER}/financials/"
   ```

3. **Take snapshot** to capture page content:
   ```bash
   agent-browser snapshot
   ```

4. **Extract data** from snapshot, focusing on:
   - Table headers (years/quarters)
   - Metric rows (revenue, net income, operating cash flow, capital expenditures, free cash flow)

5. **Format output** in clear table structure

## Data Periods

StockAnalysis provides data in multiple formats:
- **Annual**: Fiscal year data (default)
- **Quarterly**: Quarterly reports
- **TTM**: Trailing Twelve Months

Switch between periods using navigation buttons on the page.

## Common Ticker Examples

| Company | Ticker |
|----------|---------|
| Apple | AAPL |
| Microsoft | MSFT |
| Google/Alphabet | GOOGL |
| Amazon | AMZN |
| Tesla | TSLA |
| NVIDIA | NVDA |
| Meta | META |
| Berkshire Hathaway | BRK.B |
| Johnson & Johnson | JNJ |
| JPMorgan Chase | JPM |
