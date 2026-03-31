---
description: Scorecard template for the [Methodology Partner] article quality gate with
  severity-tiered scoring
category: templates
created: 2026-03-19
last_updated: 2026-03-30
version: 2
tags:
  - domain/templates
  - status/active
  - type/template
---

# Article QA Scorecard

## Article Information

- **Title:** [Article title]
- **Client:** [Client name]
- **Author:** [Human / AI-assisted / Fully AI]
- **Source:** [Video URL or transcript reference]
- **Date:** [YYYY-MM-DD]
- **Topic Wheel Position:** [WHY / HOW / WHAT — specific topic]
- **Voice Profile:** [Client voice profile used, or "default"]

---

## Pre-Publish Gate (Steps 1-13)

| # | Step | Tier | Status | Notes |
|---|------|------|--------|-------|
| 1 | Requirements Gathered | BLOCK | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 2 | Transcription Complete | BLOCK | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 3 | Source Video Watched | BLOCK | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 4 | Research & Anti-Vandalism | BLOCK | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 5 | Written from Source | BLOCK | ⬜ PASS / ⬜ FAIL | |
| 6 | Title & Headings | WARN | ⬜ PASS / ⬜ FAIL | |
| 7 | Strong Opening | WARN | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 8 | Multimedia Elements | WARN | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 9 | Internal Linking | WARN | ⬜ PASS / ⬜ FAIL | |
| 10 | Source Video Embedded | WARN | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 11 | Language Quality | BLOCK/WARN | ⬜ PASS / ⬜ FAIL | |
| 12 | WordPress Post | BLOCK | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |
| 13 | Categorized & Tagged | WARN | ⬜ PASS / ⬜ FAIL / ⬜ NEEDS HUMAN | |

## Post-Publish Workflow (Steps 14-18)

Track separately. These do NOT block publication.

| # | Step | Status | Notes |
|---|------|--------|-------|
| 14 | Cross-Posted to Social | ⬜ DONE / ⬜ PENDING / ⬜ NEEDS HUMAN | |
| 15 | Added to Content Library | ⬜ DONE / ⬜ PENDING | |
| 16 | Dollar-a-Day Evaluation | ⬜ DONE / ⬜ PENDING / ⬜ NEEDS HUMAN | |
| 17 | MAA Tracking | ⬜ DONE / ⬜ PENDING | |
| 18 | Iterate (2-week review) | ⬜ DONE / ⬜ PENDING / ⬜ NEEDS HUMAN | |

---

## Summary

**Pre-Publish:**
- **BLOCK violations:** _ → [list each]
- **WARN violations:** _ → [list each]
- **STYLE notes:** _ → [informational only]
- **NEEDS HUMAN:** _ steps → [list each]

**Publication Decision:**
- ⬜ **Publish** — 0 BLOCK, 0 WARN (or WARN documented)
- ⬜ **Fix Required** — WARN violations to address
- ⬜ **Cannot Publish** — BLOCK violations present
- ⬜ **Route to Human** — Human gates pending

---

## Detailed Findings

### BLOCK Violations
- [Banned words, banned AI patterns, salesy language, missing source, etc.]

### WARN Violations
- [Text walls, zero contractions, stacked rhetorical questions, missing links, etc.]

### STYLE Notes (Informational)
- [Paragraph rhythm, single rhetorical questions, passive voice usage, etc.]

### Strengths
- [What the article does well — E-E-A-T signals, strong opening, real stories, etc.]

---

## Meta-Article (Post-QA)

### Source Material
- Video: [URL, length, date]
- Transcript: [file path]

### Creation Process
- Method: [AI-assisted / manual / hybrid]
- Voice profile: [which profile used]

### Decisions Made
- [Why this angle, title, structure]

### What Required Human Intervention
- [List items the agent couldn't complete]

### Lessons for Next Article
- [Improvements to apply next time]

---

## References

- **SOP:** [Article QA — [Methodology Partner] Quality Gate](../client-work/article-qa-blitzmetrics.md)
- **Skill:** [Article QA](../../skills/article-qa.md)
- **Canon:** [Article Guidelines](../../blitzmetrics-canon/03-article-guidelines.md)

## See Also

- [[sops/templates/sop-creation-template|SOP Creation Template]]
- [[sops/templates/session-log-format|Session Log Format]]
- [[blitzmetrics-canon/03-article-guidelines|Canon: Article Guidelines]]
- [[blitzmetrics-canon/07-quality-standards|Canon: Quality Standards]]
- [[memory-bank/04-client-directory|Client Directory]]