---
name: Weekly MAA Report
version: 1
description: Produce the weekly Metrics-Analysis-Action report for active
  clients every Friday
triggers:
  - weekly report
  - Friday report
  - MAA
  - metrics analysis action
  - client status update
canon_source: blitzmetrics-canon/05-maa-framework.md
full_sop: sops/client-work/weekly-maa-report.md
triangles:
  - MAA
tags:
  - status/active
  - triangle/MAA
  - type/skill
---

# Weekly MAA Report — Executable Skill

## Core Principle

The MAA is analysis, not a task list. It implements the [[blitzmetrics-canon/05-maa-framework|MAA Framework]] and connects to the [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]. "We published 3 articles" is a task. "The 3 articles targeting long-tail hearing aid keywords drove 340 new organic sessions, up from 180 last week" is analysis. [Your Mentor/Advisor] will push back on task-list-style reports every time.

## Phase 1: Pull Metrics (Actual Numbers Only)

1. **Gather from native platforms** — not automated dashboards alone:
   - Website traffic: sessions, users, top pages (GA4)
   - Search rankings: target keywords, position changes (SEMrush/Ahrefs)
   - Content published: count, titles, platforms
   - Engagement: social likes, comments, shares, video views
   - Campaign KPIs: ad spend, conversions, CPL (if running ads)
2. Every metric needs a **number** and a **week-over-week comparison**
   - Bad: "Traffic increased this week"
   - Good: "Traffic increased 23% to 1,240 sessions (vs. 1,008 last week)"
3. If metrics are incomplete, report what you have and note what is missing and when it will be updated. **Never skip a week silently.**

## Phase 2: Write the Report

Use this exact format:

```
## MAA Report — [Client Name] — Week of [Date]

### Metrics
- Website sessions: [number] ([+/- %] vs. last week)
- Top keyword rankings: [keyword]: [position] ([change])
- Content published: [count] ([list titles])
- Engagement: [platform]: [numbers]
- [Campaign KPI]: [number]

### Analysis
[2-4 sentences connecting metrics to actions taken. What is working and why.
What is flat or declining and why. Identify the weakest area explicitly.]

### Action
- [Action item] — [Owner] — [Deadline]
- [Action item] — [Owner] — [Deadline]
- [Action item] — [Owner] — [Deadline]
```

## Phase 3: Analysis Quality Gate

Before posting, verify:
- [ ] Metrics section has actual numbers with week-over-week comparisons
- [ ] Analysis explains the **why** behind numbers — cause connected to effect
- [ ] Analysis calls out the weakest area explicitly (do not bury bad news)
- [ ] Action section has 3+ items, each with a **named owner** and a **deadline**
- [ ] At least one action item targets the weakest metric area
- [ ] No task-list language masquerading as analysis

## Phase 4: Post & Distribute

1. Post the MAA to the **Basecamp Updates thread** (client-visible)
2. Client and [Your Mentor/Advisor] should see it without having to ask
3. Due by **Friday EOD** every week for every active client

## Known Pitfalls

- **Task list disguised as analysis.** The #1 failure. [Your Mentor/Advisor] catches this every time. Connect output to outcomes.
- **Missing a week without notice.** Post a note saying when the report will come. Going silent destroys trust faster than a bad report.
- **Vague metrics.** "Traffic increased" is useless. Include the actual number and the comparison — always.
- **Action items with no owner.** Every action needs a person's name and a date. "Improve SEO" is not an action item. "Publish 2 articles targeting [keyword] — [Your Name] — by Wednesday" is.
- **Ignoring the weakest area.** If organic traffic is flat but all your actions are about content, you are avoiding the problem. The Action section must address whatever is underperforming.

## Human Gates

- Analyst pulls metrics from native platforms (not automated dashboards alone)
- Analysis section requires human judgment — connecting cause to effect
- Action items require human assignment of owners and deadlines
- [Your Mentor/Advisor] reviews MAA quality and pushes back on task-list-style reports
- Posted to Basecamp for client and [Your Mentor/Advisor] visibility — human verifies content is client-appropriate

---

## Connected

- [Canon: MAA Framework](../blitzmetrics-canon/05-maa-framework.md)
- [Full SOP: Weekly MAA Report](../sops/client-work/weekly-maa-report.md)
- [Influence Report Card Skill](influence-report-card.md)
- [Content Factory Skill](content-factory.md)
- [Dollar-a-Day Skill](dollar-a-day.md)
- [Client Directory](../memory-bank/04-client-directory.md)
- [Basecamp Status](../memory-bank/15-basecamp-status.md)

## See Also

- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]
- [[skills/content-factory|Content Factory Skill]]
- [[memory-bank/04-client-directory|Client Directory]]