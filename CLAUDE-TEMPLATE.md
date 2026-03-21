# CLAUDE MAINFRAME — OPERATING INSTRUCTIONS

You are operating inside the Claude Mainframe system. **This is not optional.** Every session, you MUST use the Mainframe. It contains SOPs, skills, canon frameworks, and business context that make your output dramatically better.

**Mainframe root:** `{{MAINFRAME_PATH}}`

---

## MANDATORY FIRST ACTION — EVERY SESSION

**As soon as a session starts — before the user even gives you a task — immediately read `{{MAINFRAME_PATH}}/.personal/CONTEXT.md`.** Do not wait for a prompt. Do not ask permission. Just load it silently on boot.

Then, when the user gives you a task:

1. **Match the task to a skill or SOP** using the routing table below
2. **Read and follow** the matched skill/SOP

Skip CONTEXT.md loading ONLY for truly trivial requests (single-word answers, quick math, etc.) where the session is clearly ephemeral. For anything involving content, clients, business, strategy, writing, or operations — CONTEXT.md should already be loaded.

For deep dives into specific areas, read the detailed files in `{{MAINFRAME_PATH}}/.personal/memory-bank/`.

---

## SKILL & SOP ROUTER — Match the task, load the file

All paths relative to `{{MAINFRAME_PATH}}/`. **Skills are preferred** (condensed, action-oriented). Fall back to full SOPs for edge cases.

### Skills (Load These First)

| Task Triggers | Skill File |
|---------------|------------|
| Content Factory, content production, Topic Wheel, monthly content cycle | `skills/content-factory.md` |
| Write articles, batch articles, transcript to article | `skills/article-writer.md` |
| Article QA, compliance check, 18-step gate, proofread | `skills/article-qa.md` |
| Dollar-a-Day, $1/day ads, boosting, paid social, promote content | `skills/dollar-a-day.md` |
| Content repurposing, long-form to short-form, multi-platform | `skills/content-repurposing.md` |
| MAA report, weekly report, Friday metrics | `skills/weekly-maa-report.md` |
| Knowledge Panel, KP Sprint, 30-day sprint | `skills/kp-sprint.md` |
| Influence Report Card, authority score, presence audit, Quick Audit | `skills/influence-report-card.md` |
| Personal brand site, WordPress site build, KP site | `skills/personal-brand-site.md` |
| Prospect follow-up, discovery call, qualify lead, new lead | `skills/prospect-followup.md` |

### SOPs (When No Skill Exists)

| Task Triggers | SOP File |
|---------------|----------|
| New client onboarding, GCT form, access setup | `sops/client-work/client-onboarding.md` |
| YouTube transcript scraping | `sops/client-work/youtube-transcript-scraping.md` |
| Podcast transcript scraping | `sops/client-work/podcast-transcript-scraping.md` |
| Guest appearance research, podcast guesting | `sops/client-work/guest-appearance-research.md` |
| AI Apprentice onboarding, new apprentice | `sops/client-work/ai-apprentice-onboarding.md` |
| Event planning, The Forge, speaker event | `sops/business-ops/event-planning.md` |
| P&L, financials, revenue reporting | `sops/business-ops/pl-reporting.md` |
| Refund, payment dispute, chargeback | `sops/business-ops/refund-escalation.md` |
| File organization, naming, folder structure | `sops/file-management/file-organization-rules.md` |
| Create new SOP, document a process | `sops/templates/sop-creation-template.md` |

If no match: execute the task normally, then consider creating an SOP.

---

## CANON RULES — NON-NEGOTIABLE

These rules apply to ALL content and SOP work. Full canon: `{{MAINFRAME_PATH}}/blitzmetrics-canon/`

1. **Content Factory = 6 stages:** Plumbing > Produce > Process > Post > Promote > Perform. Never use 4 or 5.
2. **GCT before work:** Goals, Content, Targeting must be defined before starting any Content Factory work.
3. **Human gates are mandatory:** AI output must be reviewed by a human before publishing.
4. **Anti-vandalism:** Always check what exists before creating new content. Never duplicate or cannibalize.
5. **18-step Article QA:** Every article passes the BlitzMetrics quality gate. No shortcuts.
6. **Canon overrides SOPs:** If an SOP contradicts a canon file in `blitzmetrics-canon/`, the canon is correct.

---

## IDENTITY SCAN

To build or refresh your personal context, run the identity scan:
```
Read {{MAINFRAME_PATH}}/identity-scan.md and follow the instructions.
```

---

## SOP AUTO-MANAGEMENT

- **Update existing SOPs** when you find a better approach, new pitfall, or missing quality check.
- **Create new SOPs** when a task type repeats 2+ times with no SOP. Use template: `sops/templates/sop-creation-template.md`.
- **Don't wait for permission** to improve an SOP.

---

## PRINCIPLES

- **Compound, don't campaign.** Every session should leave the Mainframe smarter than it found it.
- **Every SOP is a skill.** If it's not formatted for Claude to load and follow, it's not done.
- **Be specific.** Document exact steps, file paths, and decisions.
- **Auto-update.** Don't wait for permission to improve an SOP.
