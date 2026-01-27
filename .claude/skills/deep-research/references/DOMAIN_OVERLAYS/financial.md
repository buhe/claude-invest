# Financial Domain Overlay

**Load this overlay when research involves financial analysis, market research, company analysis, investment topics, or economic data.**

---

## Mandatory Citation Elements

For financial research, every C1 claim must include:

| Element | Requirement |
|---------|-------------|
| **SEC Filing Citation** | 10-K, 10-Q, 8-K, proxy, S-1 with specific section |
| **Reporting Period** | Fiscal year/quarter dates for all financials |
| **As-Of Date** | When the data was current |
| **Bloomberg/Reuters ID** | For market data verification |
| **Analyst Credentials** | For cited analyst opinions |
| **Currency & Year** | USD 2024 vs nominal/local currency |

---

## Required Verification Checks

Before finalizing financial research, verify:

- [ ] Cross-check numbers against SEC EDGAR filings
- [ ] Check for financial restatements or amendments
- [ ] Note accounting method changes (GAAP vs non-GAAP)
- [ ] Include required risk disclosures
- [ ] Identify forward-looking statements (safe harbor)
- [ ] Verify market data against multiple sources
- [ ] Check for material subsequent events
- [ ] Note any ongoing SEC investigations or litigation

---

## Source Priority (Financial)

Rank sources in this order:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| **1** | SEC EDGAR Filings | 10-K, 10-Q, 8-K, DEF 14A, S-1 |
| **2** | Company Earnings Calls | Transcripts from official IR |
| **3** | Central Bank Publications | Fed, ECB, BoE official releases |
| **4** | Major Wire Services | Reuters, Bloomberg, Dow Jones |
| **5** | Institutional Research | Sell-side with disclosed conflicts |
| **6** | Industry Publications | Trade journals, industry associations |
| **7** | News Sources | WSJ, FT, Economist |

---

## Quality Grade Modifiers (Financial-Specific)

Upgrade or downgrade base quality grades:

| Modifier | Effect |
|----------|--------|
| Audited financials (Big 4) | +1 grade |
| Unaudited/preliminary | -0.5 grade |
| Pro forma / non-GAAP without reconciliation | -1 grade |
| Sell-side research with banking relationship | -0.5 grade |
| Anonymous sources | -1 grade |
| Social media / retail forums | -2 grades |
| Promotional content (company IR) | Context only, verify independently |

---

## Red Flags for Financial Sources

Automatically flag and investigate:

- Financial claims without SEC filing reference
- Projections without stated methodology
- Analyst reports without credential disclosure
- Unverified social media claims (Twitter, Reddit)
- Promotional materials from company IR
- Numbers that don't reconcile to filings
- Missing comparables or benchmarks
- Revenue recognition issues
- Related party transactions
- Going concern opinions
- Material weaknesses in internal controls

---

## Special Claim Categories

### Revenue/Earnings Claims (C1-FIN)
```
Required: Metric (Revenue/EBITDA/EPS), period, GAAP vs non-GAAP,
year-over-year change, SEC filing reference (10-K/10-Q, page/exhibit)
```

### Market Data Claims (C1-MKT)
```
Required: Data point, as-of date, source (Bloomberg/Reuters/exchange),
ticker symbol, any adjustments (splits, dividends)
```

### Valuation Claims (C1-VAL)
```
Required: Methodology (DCF/comps/precedents), key assumptions,
sensitivity ranges, comparables used, source credentials
```

### Forecast Claims (C1-FCST)
```
Required: Forecasting entity, date issued, methodology,
historical accuracy track record, confidence interval if available
Mark as: [FORWARD-LOOKING STATEMENT]
```

---

## Numeric Standards

### Currency Normalization
- State all figures in consistent currency (default: USD)
- Note original currency if converted
- Use consistent exchange rate date
- For historical comparisons, inflation-adjust or note nominal

### Time Period Consistency
- Use consistent fiscal periods
- Note fiscal year end if not calendar year
- Align TTM (trailing twelve months) calculations
- Note seasonal effects if relevant

### Per-Share Adjustments
- Use diluted shares for EPS
- Note stock splits and adjustments
- Specify basic vs diluted
- Note share buyback effects

---

## Forward-Looking Statement Protocol

For any projections or forecasts:

1. **Label clearly**: [FORWARD-LOOKING STATEMENT]
2. **State source**: Who made this projection?
3. **Note methodology**: How was it derived?
4. **Include caveats**: What could make this wrong?
5. **Historical accuracy**: Track record of source?

**Example:**

> "Management projects 15-20% revenue growth in FY2025" [FORWARD-LOOKING STATEMENT]
> Source: Q3 2024 Earnings Call, CEO statement
> Caveats: Subject to macro conditions, competitive dynamics, regulatory approval
> Track record: Company met guidance in 6 of last 8 quarters

---

## GAAP vs Non-GAAP Reconciliation

When citing non-GAAP metrics:

- Always include GAAP equivalent
- List adjustments made
- Reference reconciliation in filings
- Note if adjustments are unusual

**Example:**

> "Adjusted EBITDA was $500M (GAAP Net Income: $200M)"
> Adjustments: +$150M D&A, +$50M stock comp, +$100M restructuring
> Source: 10-K FY2024, p. 45, Exhibit 99.1

---

## Citation Format (Financial)

**Standard format for financial claims:**

```
"[Claim text]" [CONFIDENCE: High/Med/Low]
(Company/Source, Filing Type, Period, Page/Section)
As-of: [Date] | Currency: [XXX] | [GAAP/Non-GAAP]
```

**Example:**

> "Apple reported $383.3B in total revenue for FY2023" [HIGH CONFIDENCE: Audited]
> (Apple Inc., 10-K, FY2023, p. 29)
> As-of: September 30, 2023 | Currency: USD | GAAP

---

## Agent Instructions (Financial)

When deploying research agents for financial topics, include:

```
"This is financial research. For every financial claim:
1. Cite SEC filing (10-K, 10-Q, 8-K) with page number
2. Note reporting period and as-of date
3. Distinguish GAAP vs non-GAAP
4. Include currency and any conversions
5. For market data, cite source and timestamp
6. Label forward-looking statements explicitly
7. Note analyst conflicts of interest
8. Reconcile numbers to primary filings"
```

---

## Regulatory Context

Include relevant regulatory information:

| Jurisdiction | Regulatory Body | Key Filings |
|--------------|-----------------|-------------|
| USA | SEC | 10-K, 10-Q, 8-K, DEF 14A |
| USA Banking | OCC, FDIC, Fed | Call Reports, Y-9C |
| EU | ESMA | Annual Reports (IFRS) |
| UK | FCA | Annual Reports (UK GAAP/IFRS) |

---

## Common Pitfalls to Avoid

1. **Mixing periods**: Q1 2024 vs TTM vs FY
2. **GAAP/non-GAAP confusion**: Always clarify
3. **Survivorship bias**: Failed companies excluded from indices
4. **Pro forma adjustments**: May not be comparable across companies
5. **Headline vs recurring**: One-time items distort trends
6. **Currency effects**: FX can mask underlying performance

---

*Financial Domain Overlay — Version 3.0*
