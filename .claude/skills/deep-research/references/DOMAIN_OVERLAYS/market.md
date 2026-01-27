# Market Research Domain Overlay

**Load this overlay when research involves market analysis, competitive intelligence, industry trends, consumer behavior, or market sizing.**

---

## Mandatory Citation Elements

For market research, every C1 claim must include:

| Element | Requirement |
|---------|-------------|
| **Report Publisher** | Name of research firm or organization |
| **Publication Date** | When the data was published |
| **Data Collection Period** | When the underlying data was gathered |
| **Sample Size/Methodology** | How data was collected (survey n=X, interviews, etc.) |
| **Geographic Scope** | Markets/regions covered |
| **Market Definition** | How the market segment is defined |

---

## Required Verification Checks

Before finalizing market research, verify:

- [ ] Check if market sizing methodology is disclosed
- [ ] Verify sample sizes are adequate for claims made
- [ ] Note any sponsor bias (vendor-funded research)
- [ ] Check for conflicting estimates across sources
- [ ] Identify if projections are based on historical data or assumptions
- [ ] Verify currency and year for all financial figures
- [ ] Check if market definitions are consistent across sources

---

## Source Priority (Market Research)

Rank sources in this order:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| **1** | Industry Associations | Trade associations with member data access |
| **2** | Government Statistics | Census Bureau, BLS, Eurostat, national statistics offices |
| **3** | Tier 1 Research Firms | Gartner, IDC, Forrester, McKinsey, BCG |
| **4** | Tier 2 Research Firms | MarketsandMarkets, Grand View, Allied Market Research |
| **5** | Company Filings | 10-K market discussions, investor presentations |
| **6** | Trade Publications | Industry-specific journals and news |
| **7** | News Sources | WSJ, FT, Bloomberg, Reuters |

---

## Quality Grade Modifiers (Market-Specific)

Upgrade or downgrade base quality grades:

| Modifier | Effect |
|----------|--------|
| Primary research (surveys, interviews) disclosed | +1 grade |
| Large sample size (n > 1000) | +0.5 grade |
| Methodology not disclosed | -1 grade |
| Vendor-sponsored without disclosure | -1 grade |
| Projections beyond 3 years | -0.5 grade |
| Market definition unclear | -0.5 grade |
| Single-source estimate | -0.5 grade |

---

## Red Flags for Market Research Sources

Automatically flag and investigate:

- Market size estimates without methodology
- CAGR projections without base year data
- Conflicting market sizes (>30% variance) across sources
- Vendor-sponsored research cited as independent
- Projections extending beyond 5 years
- Press releases without underlying report
- "Market expected to reach $X billion" without source
- TAM/SAM/SOM confusion
- Geographic scope mismatch

---

## Special Claim Categories

### Market Size Claims (C1-MARKET)
```
Required: Market definition, size (value/volume), currency, year,
geographic scope, methodology (top-down/bottom-up), source with page number
```

### Growth Rate Claims (C1-GROWTH)
```
Required: CAGR percentage, base year, forecast year,
underlying assumptions, source methodology, confidence interval if available
```

### Market Share Claims (C1-SHARE)
```
Required: Company/product, share percentage, market definition,
measurement basis (revenue/units), time period, source
```

### Competitive Intelligence Claims (C1-COMP)
```
Required: Competitor name, claim type (pricing/features/strategy),
source type (primary/secondary), verification status
```

---

## Market Sizing Standards

### Always Include:
- Base year actual vs. forecast year projected
- Currency (USD, EUR, etc.) with year (e.g., "USD 2024")
- Geographic scope clearly stated
- Market definition (what's included/excluded)
- Methodology (top-down from macro data vs. bottom-up from company data)

### Handle Conflicting Estimates:
1. Present range from multiple sources
2. Explain methodology differences
3. Weight by source quality
4. Note which estimate you use for analysis and why

**Example:**

> "The global AI in healthcare market was valued at $15.1B in 2023 (MarketsandMarkets) to $20.9B (Grand View Research). The variance stems from different market definitions: MarketsandMarkets excludes medical imaging AI while Grand View includes it. Using the narrower definition for comparability with historical data: $15.1B (2023), projected CAGR 37.5% to reach $187.7B by 2030."

---

## Projection Credibility Framework

| Timeframe | Credibility | Handling |
|-----------|-------------|----------|
| **1-2 years** | High | Can cite with standard confidence |
| **3-5 years** | Medium | Note assumptions, present range |
| **5-10 years** | Low | Present as scenario, not forecast |
| **10+ years** | Speculative | Use only for directional indication |

---

## Citation Format (Market Research)

**Standard format for market claims:**

```
"[Claim text]" [CONFIDENCE: High/Med/Low]
(Publisher, Report Title, Publication Date, p. XX)
Methodology: [Top-down/Bottom-up/Survey n=X]
Data period: [When data was collected]
```

**Example:**

> "The enterprise software market reached $295B in 2023" [HIGH CONFIDENCE: Multiple sources agree]
> (Gartner, "Market Share Analysis: Enterprise Software, Worldwide, 2023", March 2024, p. 12)
> Methodology: Bottom-up from vendor revenue disclosures
> Data period: Full year 2023 actuals

---

## Agent Instructions (Market Research)

When deploying research agents for market topics, include:

```
"This is market research. For every market claim:
1. Include publisher and publication date
2. Note methodology (survey, modeling, aggregation)
3. Specify geographic scope and market definition
4. Include sample size for survey-based data
5. Note data collection period vs publication date
6. Flag any vendor sponsorship or potential bias
7. When estimates conflict, present range and explain variance
8. Distinguish actuals from projections
9. Use consistent currency and year across comparisons"
```

---

## Common Pitfalls to Avoid

1. **TAM vs SAM vs SOM confusion**: Total Addressable ≠ Serviceable ≠ Obtainable
2. **Currency/year mismatch**: Always normalize to same currency-year
3. **Conflating revenue with market size**: Company revenue ≠ market they serve
4. **Ignoring methodology**: Top-down vs bottom-up can give very different numbers
5. **Projection optimism**: Research firms often overestimate growth rates
6. **Sponsor bias**: Vendor-funded research may overstate their market
7. **Definition drift**: Market definitions change between reports

---

## Competitive Intelligence Ethics

When gathering competitive intelligence:

- Use only publicly available information
- Do not misrepresent identity to gather information
- Respect confidentiality agreements
- Note information source (public filing, news, industry event, etc.)
- Distinguish facts from speculation
- Date-stamp all competitive information

---

*Market Research Domain Overlay — Version 3.0*
