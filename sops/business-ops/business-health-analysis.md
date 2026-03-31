---
title: Business Health Analysis (P&L + MAA)
version: 1.0
last_updated: 2026-03-21
category: business-ops
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/finance
canon_compliance: [maa-framework, nine-triangles]
human_gates: [financial data verification, distribution decisions, expense allocation]
---

# Business Health Analysis — P&L + MAA

## Purpose
Run a comprehensive financial and operational analysis of [[memory-bank/01-hri-overview|[Your Agency]]] using [Your Mentor/Advisor]'s frameworks: zero-based P&L, subtractive analysis, and MAA. Produces a defensible financial picture that [Your Mentor/Advisor] can review.

## When to Use
- Monthly (1st Monday per meeting cadence)
- When [Your Mentor/Advisor] asks for financial transparency
- Before any distribution or compensation discussion
- Before major business decisions (hiring, new clients, equity changes)

## Process

### Phase 1: Gather Data (Metrics)

1. **Revenue:** Pull from Stripe, bank statements, and client payment records
   - Total revenue for period
   - Revenue by client
   - Revenue by product/service type
   - Month-over-month comparison

2. **Expenses:** Categorize all costs
   - [Your Agency] direct expenses ([Your Name]'s tools, [Your Content Specialist]'s compensation, Google Workspace)
   - Shared/[Partner Platform] expenses allocated to [Your Agency] ([Your Ops Admin] %, ChatGPT %, WP Engine %, etc.)
   - [Your Mentor/Advisor]'s direct out-of-pocket for [Your Agency]

3. **Distribution history:** What's been paid to each party and when

### Phase 2: Zero-Based Analysis

Start everyone at zero. For each person/component, document:
| Person/Component | Value Contributed | Evidence | Monthly Cost |
|---|---|---|---|
| [Your Mentor/Advisor] | Sales pipeline, methodology, client relationships | All clients through his network | $0 direct / $X time value |
| [Your Name] | Execution, article production, AI tooling | 378 articles, 54 QA'd | $X/month |

### Phase 3: Subtractive Analysis

For each component, answer: "What happens if we remove this?"
| If You Remove... | Impact | Severity |
|---|---|---|
| [Your Mentor/Advisor] | Revenue goes to $0 in 2-3 months | CATASTROPHIC |
| [Your Name] | Delivery stops, replaceable short-term | MODERATE |

### Phase 4: MAA (Analysis)

Connect the numbers to causes:
- Why is revenue at $X/month? (not enough clients? pricing too low? churn?)
- Why are expenses at $Y/month? (which costs are growing? which are fixed?)
- Where is the business losing money? (which clients are unprofitable?)
- What's the path to profitability?

### Phase 5: Action Items

Every analysis must produce 3+ specific actions:
- Each with an owner, deadline, and measurable target
- At least one action targets the weakest metric
- No vague actions ("improve revenue" is not an action)

### Phase 6: Report

Save to `~/Documents/Claude/PRISM/logs/reports/pl-analysis-YYYY-MM.md`

## Quality Checks
- [ ] Every number has a source (not estimated without noting it)
- [ ] Zero-based analysis covers every person and major cost
- [ ] Subtractive analysis is honest (even if uncomfortable)
- [ ] MAA connects numbers to causes (not a task list)
- [ ] Action items have owners and deadlines

## Human Gates
- Financial data must be verified by [Your Name] (Claude can estimate but [Your Name] confirms)
- Distribution decisions require human judgment
- Expense allocation percentages require agreement between parties

## Canon Compliance
- MAA framework per blitzmetrics-canon/05-maa-framework.md
- Analysis must explain WHY, not just list WHAT ([Your Mentor/Advisor] rejects task-list-style reports)

## Learnings Log
- 2026-03-21: Created after deep dive showed [Your Name] has sent [Methodology Partner] $35,070 against estimated $9-18K in [Your Agency]-allocable costs. Zero-based and subtractive models were effective at revealing the actual dynamics.

---

## Related

- [P&L Reporting SOP](pl-reporting.md)
- [Weekly MAA Report SOP](../client-work/weekly-maa-report.md)
- [Financial Context](../../memory-bank/10-financial-context.md)
- [Canon: MAA Framework](../../blitzmetrics-canon/05-maa-framework.md)
- [Strategic Context](../../memory-bank/12-strategic-context.md)

## See Also

- [[memory-bank/10-financial-context|Financial Context]]
- [[memory-bank/01-hri-overview|[Your Agency] Overview]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[skills/weekly-maa-report|Weekly MAA Report]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]