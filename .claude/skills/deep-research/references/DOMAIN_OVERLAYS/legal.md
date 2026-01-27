# Legal Domain Overlay

**Load this overlay when research involves legal analysis, regulatory compliance, case law, statutory interpretation, or legal risk assessment.**

---

## Mandatory Citation Elements

For legal research, every C1 claim must include:

| Element | Requirement |
|---------|-------------|
| **Jurisdiction** | Federal/State/International + specific court/body |
| **Case Citation** | Standard legal citation format (Bluebook) |
| **Case Status** | Pending, decided, appealed, overruled |
| **Statutory Authority** | U.S.C., C.F.R., state code citations |
| **Effective Date** | When law/regulation took effect |
| **Subsequent History** | Later developments affecting precedent |

---

## Required Verification Checks

Before finalizing legal research, verify:

- [ ] Verify case status via Westlaw/LexisNexis/CourtListener
- [ ] Check for subsequent history (appealed, reversed, overruled)
- [ ] Identify circuit splits or conflicts between jurisdictions
- [ ] Distinguish binding vs persuasive authority
- [ ] Flag areas of unsettled law
- [ ] Note any pending legislation that could change analysis
- [ ] Check for superseding regulations
- [ ] Verify statutory text is current (amendments)

---

## Source Priority (Legal)

Rank sources in this order:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| **1** | Primary Sources | Statutes, regulations, constitutions, case law |
| **2** | Official Agency Guidance | DOJ memos, SEC no-action letters, IRS rulings |
| **3** | Legal Treatises | Restatements, Williston, Corbin, Wright & Miller |
| **4** | Law Review Articles | Peer-reviewed legal scholarship |
| **5** | Practitioner Publications | ABA journals, PLI materials |
| **6** | Legal News | Law360, Legal Intelligencer, Bloomberg Law |

---

## Quality Grade Modifiers (Legal-Specific)

Upgrade or downgrade base quality grades:

| Modifier | Effect |
|----------|--------|
| Supreme Court / highest court decision | +1 grade |
| Binding precedent in jurisdiction | +1 grade |
| Persuasive authority only | -0.5 grade |
| Dicta (not holding) | -1 grade |
| Overruled or superseded | Grade E (unusable as authority) |
| Unpublished opinion | -0.5 grade |
| Legal blog / commentary | -1 grade (use for context only) |

---

## Red Flags for Legal Sources

Automatically flag and investigate:

- Overruled, vacated, or superseded cases
- Dicta cited as holding
- Wrong jurisdiction applied (e.g., citing NY law for CA issue)
- Missing subsequent history
- Outdated statutory citations (check amendments)
- Agency guidance withdrawn or superseded
- Split circuits without acknowledgment
- Advocacy pieces presented as neutral analysis
- Missing effective dates for regulations

---

## Special Claim Categories

### Case Law Claims (C1-CASE)
```
Required: Case name, citation (volume, reporter, page), court, year,
holding (not dicta), subsequent history, binding/persuasive status
```

### Statutory Claims (C1-STAT)
```
Required: Statute name, citation (Title U.S.C. § Section),
subsection if applicable, effective date, any relevant amendments
```

### Regulatory Claims (C1-REG)
```
Required: Agency, regulation citation (C.F.R.),
effective date, any pending amendments or proposed rules
```

### Legal Risk Claims (C1-RISK)
```
Required: Legal basis for risk, jurisdiction,
likelihood assessment, potential consequences, mitigating factors
Mark as: [LEGAL ANALYSIS - NOT LEGAL ADVICE]
```

---

## Citation Formats (Legal)

### Case Citations (Bluebook format)

**Federal:**
```
[Case Name], [Volume] [Reporter] [Page] ([Court] [Year])
Example: Brown v. Board of Education, 347 U.S. 483 (1954)
```

**State:**
```
[Case Name], [Volume] [Reporter] [Page] ([State Court] [Year])
Example: Palsgraf v. Long Island R.R. Co., 248 N.Y. 339 (1928)
```

### Statutory Citations

**Federal:**
```
[Title] U.S.C. § [Section] ([Year])
Example: 15 U.S.C. § 78j(b) (2018)
```

**Federal Regulations:**
```
[Title] C.F.R. § [Section] ([Year])
Example: 17 C.F.R. § 240.10b-5 (2023)
```

---

## Jurisdictional Analysis Framework

For multi-jurisdictional issues:

| Question | Analysis Required |
|----------|-------------------|
| **Which law applies?** | Choice of law analysis |
| **Which court has jurisdiction?** | Personal + subject matter jurisdiction |
| **Is there a circuit split?** | Map positions across circuits |
| **Federal vs state?** | Preemption analysis |
| **International?** | Treaty obligations, comity |

---

## Binding vs Persuasive Authority

**Always clarify:**

| Authority Type | Description | Weight |
|----------------|-------------|--------|
| **Mandatory/Binding** | Must follow (same jurisdiction, higher court) | High |
| **Persuasive** | May follow (different jurisdiction, same level) | Medium |
| **Secondary** | Treatises, law reviews, restatements | Low (supports, not controls) |
| **Dicta** | Statements not necessary to holding | Minimal |

---

## Subsequent History Notation

Always check and note:

| Notation | Meaning |
|----------|---------|
| `aff'd` | Affirmed on appeal |
| `rev'd` | Reversed on appeal |
| `vacated` | Decision vacated |
| `overruled` | No longer good law |
| `distinguished` | Later court limited scope |
| `cert. denied` | Supreme Court declined review |
| `cert. granted` | Supreme Court will review |

---

## Legal Disclaimer Requirements

Include in all legal research outputs:

```
DISCLAIMER: This research is for informational purposes only and does
not constitute legal advice. Laws vary by jurisdiction and change over
time. Consult a qualified attorney for advice on specific legal matters.
```

---

## Agent Instructions (Legal)

When deploying research agents for legal topics, include:

```
"This is legal research. For every legal claim:
1. Cite primary sources (statutes, cases, regulations)
2. Include full legal citation in Bluebook format
3. Note jurisdiction and whether authority is binding or persuasive
4. Check case status - is it still good law?
5. Note any circuit splits or conflicting authority
6. Distinguish holding from dicta
7. Include effective dates for statutes/regulations
8. Flag areas of unsettled law
9. This is NOT legal advice - include disclaimer"
```

---

## Regulatory Context

Include relevant regulatory information:

| Jurisdiction | Key Bodies | Resources |
|--------------|------------|-----------|
| US Federal | Congress, Courts, Agencies | PACER, EDGAR, regulations.gov |
| US State | State legislature, courts | State-specific legal databases |
| EU | Commission, ECJ, Parliament | EUR-Lex, CURIA |
| UK | Parliament, Courts | legislation.gov.uk, BAILII |
| International | UN, WTO, treaties | UN Treaty Collection |

---

## Common Pitfalls to Avoid

1. **Citing dicta as holding**: Distinguish what court decided vs said
2. **Ignoring subsequent history**: Cases get reversed, overruled
3. **Wrong jurisdiction**: State law varies significantly
4. **Missing circuit splits**: Federal law may differ by circuit
5. **Outdated statutes**: Check for amendments
6. **Overreliance on secondary sources**: Always verify against primary
7. **Confusing proposed with final rules**: Check Federal Register status

---

## Legal Research Workflow

1. **Identify legal issue** and relevant jurisdiction(s)
2. **Find controlling statute/regulation** if applicable
3. **Search for on-point case law** interpreting the law
4. **Check case validity** (KeyCite, Shepard's, or equivalent)
5. **Note any circuit splits** or conflicting authority
6. **Review secondary sources** for context and analysis
7. **Update search** for very recent developments
8. **Synthesize with appropriate disclaimers**

---

*Legal Domain Overlay — Version 3.0*
