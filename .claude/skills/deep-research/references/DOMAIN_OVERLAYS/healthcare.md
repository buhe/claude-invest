# Healthcare Domain Overlay

**Load this overlay when research involves medical, clinical, pharmaceutical, or health-related topics.**

---

## Mandatory Citation Elements

For healthcare research, every C1 claim must include:

| Element | Requirement |
|---------|-------------|
| **PubMed ID (PMID)** | Required for all medical literature claims |
| **FDA Approval Status** | Required for drugs/devices |
| **Clinical Trial Phase** | Required for emerging treatments |
| **ClinicalTrials.gov Number** | Required for trial-related claims (NCT#) |
| **ICD-10 Codes** | Include when discussing diagnoses |
| **Version/Update Date** | Required for clinical guidelines |

---

## Required Verification Checks

Before finalizing healthcare research, verify:

- [ ] Check RetractionWatch for all cited papers
- [ ] Verify FDA approval status for drugs/devices mentioned
- [ ] Note if any treatment is off-label use
- [ ] Include adverse event data when discussing treatments
- [ ] Check for conflicts of interest in cited studies
- [ ] Verify clinical trial registration status
- [ ] Check if studies have been replicated

---

## Source Priority (Healthcare)

Rank sources in this order:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| **1** | Cochrane Reviews | Cochrane Database of Systematic Reviews |
| **2** | Clinical Guidelines | NICE, USPSTF, WHO, specialty society guidelines |
| **3** | Peer-reviewed RCTs | Published in high-impact journals (NEJM, Lancet, JAMA, BMJ) |
| **4** | Cohort/Case-control | Well-designed observational studies |
| **5** | Expert Consensus | Professional society statements |
| **6** | Case Reports | Published case series |
| **7** | Mechanistic Studies | Basic science supporting clinical claims |

---

## Quality Grade Modifiers (Healthcare-Specific)

Upgrade or downgrade base quality grades:

| Modifier | Effect |
|----------|--------|
| Large RCT (n > 1000) | +1 grade |
| Multi-center study | +0.5 grade |
| Industry-funded without disclosure | -1 grade |
| Preprint not yet peer-reviewed | -1 grade |
| Retracted or with expression of concern | Grade E (unusable) |
| Animal study presented as human evidence | -2 grades |

---

## Red Flags for Healthcare Sources

Automatically flag and investigate:

- Claims without PMID or DOI
- Publications in predatory journals (check Beall's List)
- Industry-funded studies without disclosed conflicts
- Animal studies cited as human evidence
- In vitro studies cited as clinical evidence
- Single-center small studies for major claims
- Observational studies claiming causation
- Press releases without underlying paper
- Supplement/alternative medicine promotional content

---

## Special Claim Categories

### Drug Efficacy Claims (C1-DRUG)
```
Required: Drug name, indication, effect size (NNT/NNH preferred),
95% CI, p-value, sample size, study duration, PMID, FDA approval status
```

### Diagnostic Accuracy Claims (C1-DX)
```
Required: Test name, sensitivity, specificity, PPV/NPV,
prevalence in study population, gold standard used, PMID
```

### Safety Claims (C1-SAFETY)
```
Required: Adverse event type, incidence rate, comparison group rate,
relative risk or odds ratio, 95% CI, source (trial or post-market)
```

### Guideline Claims (C1-GUIDE)
```
Required: Guideline name, issuing organization, publication year,
recommendation strength (e.g., Grade A/B/C), evidence quality rating
```

---

## Evidence Synthesis Standards

### For Systematic Reviews/Meta-analyses:
- Report I² heterogeneity statistic
- Note publication bias assessment (funnel plot, Egger's test)
- Report quality assessment method (GRADE, Cochrane RoB)

### For Clinical Trials:
- Report ITT vs per-protocol analysis
- Note dropout rates and reasons
- Report blinding status (single, double, open-label)
- Note allocation concealment method

---

## Regulatory Context

Include relevant regulatory information:

| Jurisdiction | Regulatory Body | Key Considerations |
|--------------|-----------------|---------------------|
| USA | FDA | Approval status, black box warnings, REMS |
| EU | EMA | Marketing authorization status |
| UK | MHRA | License status post-Brexit |
| Global | WHO | Essential medicines list, prequalification |

---

## Citation Format (Healthcare)

**Standard format for medical claims:**

```
"[Claim text]" [CONFIDENCE: High/Med/Low]
(Author et al., Year, Journal, PMID: XXXXXXXX, DOI: XX.XXXX/XXXXX)
Additional: [FDA Status] | [Trial Phase] | [NCT Number if applicable]
```

**Example:**

> "Metformin reduces diabetes incidence by 31% in high-risk individuals over 2.8 years" [HIGH CONFIDENCE: RCT, n=3,234, replicated]
> (Knowler et al., 2002, NEJM, PMID: 11832527, DOI: 10.1056/NEJMoa012512)
> FDA: Approved for T2DM | Off-label for prevention

---

## Agent Instructions (Healthcare)

When deploying research agents for healthcare topics, include:

```
"This is healthcare research. For every medical claim:
1. Include PMID or DOI
2. Note study type (RCT, cohort, case-control, etc.)
3. Include sample size and confidence intervals
4. Check FDA/EMA approval status for drugs
5. Flag any industry funding or conflicts of interest
6. Verify paper is not retracted (check RetractionWatch)
7. Note if evidence is from humans vs animals
8. For guidelines, note recommendation strength"
```

---

## Common Pitfalls to Avoid

1. **Surrogate endpoint confusion**: Lab values ≠ clinical outcomes
2. **Relative vs absolute risk**: Always report both
3. **Healthy user bias**: Observational studies may overstate benefits
4. **Publication bias**: Positive trials more likely published
5. **Time lag bias**: Guidelines may not reflect latest evidence
6. **Indication creep**: Approved use ≠ all promoted uses

---

*Healthcare Domain Overlay — Version 3.0*
