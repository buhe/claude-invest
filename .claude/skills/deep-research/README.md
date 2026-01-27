# Deep Research Skill

A 7-phase research system for Claude Code that produces decision-grade, auditable, hallucination-resistant research outputs.

## What Makes This Different?

| Traditional AI Research | Deep Research |
|------------------------|---------------|
| Single search query | 5-10 parallel searches |
| Trust first result | Verify with 2+ sources |
| No citations | Every claim cited with URL |
| Hidden contradictions | Conflicts documented and explained |
| Generic answers | Hypothesis-driven investigation |

## Installation

### Option 1: Clone to Skills Directory

```bash
cd ~/.claude/skills
git clone https://github.com/YOUR_USERNAME/deep-research-skill.git deep-research
```

### Option 2: Manual Installation

1. Download this repository as a ZIP
2. Extract to `~/.claude/skills/deep-research/`
3. Restart Claude Code

## Usage

Simply say: **"Deep research [your topic]"**

Examples:
- "Deep research the current state of quantum computing"
- "Deep research best practices for SaaS pricing"
- "Research AI regulation in Europe thoroughly"

## Research Types

The system automatically classifies your question:

| Type | Time | Use Case |
|------|------|----------|
| **A: Lookup** | 1-2 min | Single fact from authoritative source |
| **B: Synthesis** | 15-30 min | Aggregating multiple sources |
| **C: Analysis** | 30-60 min | Judgment and multiple perspectives |
| **D: Investigation** | 2-4 hours | Novel questions, conflicting evidence |

## The 7 Phases

```
0. Classify    → What type of research is this?
1. Scope       → What exactly are we researching?
1.5 Hypothesize → What are the likely answers?
2. Plan        → How will we find information?
3. Query       → Execute parallel searches
4. Triangulate → Verify claims across sources
5. Synthesize  → Combine into coherent findings
6. QA          → Verify citations and claims
7. Package     → Deliver structured output
```

## Output Structure

All research is saved to `/RESEARCH/[topic_name]/`:

```
RESEARCH/
└── [topic_name]/
    ├── README.md                    # Navigation guide
    ├── 00_research_contract.md      # Scope agreement
    ├── 01_research_plan.md          # Subquestions, queries
    ├── 02_query_log.csv             # All searches
    ├── 03_source_catalog.csv        # Sources with ratings
    ├── 04_evidence_ledger.csv       # Claims → Sources
    ├── 08_report/
    │   ├── 00_executive_summary.md
    │   ├── 01_findings.md
    │   └── 02_recommendations.md
    └── 09_qa/
        └── qa_report.md
```

## Key Principles

1. **No claim without evidence** - Mark unsourced claims as `[Source needed]`
2. **2-source rule** - Critical claims need independent verification
3. **Independence matters** - 5 articles citing 1 report = 1 source
4. **Contradictions are data** - Document and explain, don't hide
5. **Track everything** - Query logs, source catalogs, evidence ledgers

## File Structure

```
deep-research/
├── SKILL.md                 # Main skill file
├── README.md                # This file
└── references/
    ├── full-methodology.md  # Complete 7-phase specification
    └── DOMAIN_OVERLAYS/     # Specialized research requirements
        ├── healthcare.md    # PMID, FDA, clinical trials
        ├── financial.md     # SEC filings, EDGAR
        ├── legal.md         # Case citations, jurisdiction
        └── market.md        # Market sizing, competitive intel
```

## Domain Overlays

For specialized research, the system can load domain-specific requirements:

- **Healthcare**: PMID citations, FDA references, clinical trial registrations
- **Financial**: SEC filings, EDGAR links, audited sources
- **Legal**: Case citations, jurisdiction requirements
- **Market**: Market sizing methodology, competitive intelligence standards

## Credits

Based on [Claude Code Deep Research](https://github.com/anthropics/claude-code-deep-research)
- Graph of Thoughts from [SPCL, ETH Zürich](https://github.com/spcl/graph-of-thoughts)
- Methodologies inspired by OpenAI and Google Gemini deep research
- Developed by Ankit at [MyBCAT](https://mybcat.com)

## License

MIT License - Use freely, modify as needed.
