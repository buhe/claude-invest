---
name: kweb-pe
description: "Calculate weighted PE ratio for KWEB ETF by fetching top 10 holdings from Yahoo Finance, retrieving individual stock PEs, and computing the weighted average including remaining holdings (assumed PE=20). Use when user wants to: Get KWEB holdings breakdown, Calculate KWEB's weighted PE, Analyze KWEB's valuation metrics."
---

# KWEB Weighted PE Calculator

## Overview

Calculate the weighted PE ratio for KWEB ETF by fetching its top 10 holdings from Yahoo Finance, retrieving each holding's individual PE ratio, and computing the weighted average PE including all remaining holdings (assumed to have PE=20).

## Workflow

This skill works with the **agent-browser** skill to perform web automation:

1. Use agent-browser to visit `https://hk.finance.yahoo.com/quote/KWEB/holdings` (direct holdings page)
2. Extract the top 10 holdings from the holdings table (name, symbol, weight percentage)
3. For each stock symbol, visit `https://hk.finance.yahoo.com/quote/{SYMBOL}/`
4. Extract PE ratio using grep: `agent-browser snapshot | grep -o "市盈率 (最近 12 個月) [0-9.]*"`
5. Parse the PE value from the grep output
6. Pass the collected data to `calculate_weighted_pe()` function

## Data Format

### KWEB Holdings Format (from Yahoo Finance HK)

The holdings data from Yahoo Finance Hong Kong uses Chinese company names and HK stock codes:

| Field | Example | Description |
|-------|---------|-------------|
| name | 騰訊控股 | Chinese company name |
| symbol | 0700.HK | Stock code (HK format) or US ticker |
| weight | 10.23 | Weight percentage (as a number) |
| pe | 24.81 | PE ratio (as a number) |

### Expected Holdings Data Format

```python
holdings = [
    {'name': '騰訊控股', 'symbol': '0700.HK', 'weight': 10.23, 'pe': 24.81},
    {'name': '阿里巴巴－Ｗ', 'symbol': '9988.HK', 'weight': 8.77, 'pe': 22.74},
    {'name': 'PDD Holdings Inc.', 'symbol': 'PDD', 'weight': 7.91, 'pe': 10.78},
    # ... more holdings
]
```

## Using the Script

### Helper Functions

The script `scripts/get_kweb_pe.py` provides these functions:

- `parse_weight(weight_text)` - Parse weight percentage from text like "10.23%"
- `parse_pe(pe_text)` - Parse PE ratio from text, returns None for N/A
- `calculate_weighted_pe(holdings, default_pe=20)` - Calculate weighted PE

### Running the Script

```bash
# Run calculation with holdings data
python3 scripts/get_kweb_pe.py

# Or import the functions in your own script
from scripts.get_kweb_pe import calculate_weighted_pe
```

## Calculation Formula

The weighted PE is calculated as:

```
Weighted PE = (Σ (weight% × PE) + (100% - total_weight%) × default_pe) / 100
```

Where:
- `weight%` is the holding's weight percentage
- `PE` is the holding's price-to-earnings ratio
- `total_weight%` is the sum of all included holdings' weights
- `default_pe` (default: 20) is used for holdings with no PE data or remaining holdings

## Requirements

- agent-browser skill (for web automation)
- Python 3.x (for calculation functions)

## Resources

### scripts/get_kweb_pe.py

Python helper functions for parsing and calculating weighted PE. Use in conjunction with agent-browser skill for web data extraction.
