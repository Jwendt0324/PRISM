---
description: Routes Claude to the correct skill or SOP based on task type. Read this at session start to know which skill/SOP applies.
category: system
created: 2026-03-18
last_updated: 2026-03-21
version: 3.0
---

# SOP Router

When starting a task, match it against these triggers. **Load the SKILL first if one exists** — skills are condensed, action-oriented versions optimized for execution. Fall back to the full SOP only when you need detailed reference or edge-case guidance.

## Skills (Preferred Execution Path)

10 skills cover the highest-frequency tasks. Load these INSTEAD of the full SOP for faster execution.

| Trigger | Skill | Path | Full SOP Fallback |
|---------|-------|------|-------------------|
| Content Factory, content production, Topic Wheel, content strategy, monthly content cycle, plumbing setup | **Content Factory** | skills/content-factory.md | sops/client-work/content-factory-execution.md |
| Write articles, batch articles, transcript to article, article writing, content engine | **Article Writer** | skills/article-writer.md | sops/client-work/article-writing-from-transcripts.md |
| Article QA, compliance check, 18-step gate, proofread, [Your Mentor/Advisor] review | **Article QA** | skills/article-qa.md | sops/client-work/article-qa-blitzmetrics.md |
| Dollar-a-Day, $1/day ads, boosting content, paid social, Facebook/Instagram ads, promote content | **Dollar-a-Day** | skills/dollar-a-day.md | sops/client-work/dollar-a-day-campaign.md |
| Content repurposing, repurpose video, long-form to short-form, content pipeline, multi-platform | **Content Repurposing** | skills/content-repurposing.md | sops/client-work/content-repurposing-pipeline.md |
| MAA report, weekly report, metrics analysis action, Friday report | **Weekly MAA Report** | skills/weekly-maa-report.md | sops/client-work/weekly-maa-report.md |
| Knowledge Panel, KP Sprint, Google Knowledge Panel, 30-day sprint | **KP Sprint** | skills/kp-sprint.md | sops/client-work/knowledge-panel-sprint.md |
| Influence Report Card, authority score, online presence audit, Quick Audit | **Influence Report Card** | skills/influence-report-card.md | sops/client-work/influence-report-card.md |
| Personal brand site, website build, WordPress site for founder, KP site | **Personal Brand Site** | skills/personal-brand-site.md | sops/client-work/personal-brand-site-build.md |
| Prospect follow-up, lead follow-up, discovery call scheduling, prospect qualification, new lead | **Prospect Follow-Up** | skills/prospect-followup.md | sops/client-work/prospect-followup.md |

## Client Work (SOP-Only — No Skill Yet)

| Trigger | SOP | Path |
|---------|-----|------|
| New client onboarding, GCT form, access setup, Basecamp project creation, new engagement | Client Onboarding | sops/client-work/client-onboarding.md |
| YouTube transcript, scrape YouTube, pull video transcript | YouTube Transcript Scraping | sops/client-work/youtube-transcript-scraping.md |
| Podcast transcript, scrape podcast, pull audio transcript | Podcast Transcript Scraping | sops/client-work/podcast-transcript-scraping.md |
| Guest appearance, podcast guesting, speaking opportunity research | Guest Appearance Research | sops/client-work/guest-appearance-research.md |
| AI Apprentice onboarding, new apprentice, apprentice qualification task, Academy access | AI Apprentice Onboarding | sops/client-work/ai-apprentice-onboarding.md |

## Business Ops

| Trigger | SOP | Path |
|---------|-----|------|
| [Your Agency] offer, pricing, GTM, go-to-market, service packages, offer ladder | [Your Agency] Offer Ladder & GTM Blueprint | sops/business-ops/hri-offer-ladder-and-gtm.md |
| Event planning, [Your Speaker Event], in-person event, speaker event, conference | Event Planning ([Your Speaker Event]) | sops/business-ops/event-planning.md |
| P&L, profit and loss, monthly financials, revenue reporting, Stripe revenue, expense tracking | P&L Reporting | sops/business-ops/pl-reporting.md |
| Refund, client refund, payment dispute, chargeback, escalation to [Your Mentor/Advisor] | Refund & Escalation | sops/business-ops/refund-escalation.md |
| University speaking, guest lecture, professor outreach, academic engagement | University Speaking Outreach | sops/business-ops/university-speaking-outreach.md |

## Team Ops

| Trigger | SOP | Path |
|---------|-----|------|
| New hire, onboarding a team member, tool provisioning, Day 1 setup | New Hire Onboarding SOP | team-ops/06-new-hire-onboarding-sop.md |
| [Your Content Specialist] onboarding, [Your Content Specialist]'s tasks, [Your Content Specialist] success metrics | [Your Content Specialist] Onboarding Kit | team-ops/07-jackson-onboarding-kit.md |
| KP Sprint project management, Sprint timeline, red/amber/green status | KP Sprint Project Management | team-ops/10-project-management-sop.md |
| Client communication, Basecamp updates, client-facing messages | Client Communication | team-ops/11-client-communication-sop.md |
| Escalation, client unhappy, late deliverable, team unresponsive, scope creep, quality issue | Escalation Playbook | team-ops/12-escalation-playbook.md |
| Hiring plan, scaling team, next hire, revenue triggers for hiring | Team Scaling Plan | team-ops/13-team-scaling-plan.md |
| Pain points, friction, systemic issues, what's broken at [Your Agency] | Current Pain Points | team-ops/14-current-pain-points.md |

## File Management

| Trigger | SOP | Path |
|---------|-----|------|
| File organization, naming conventions, folder structure, where to save files | File Organization Rules | sops/file-management/file-organization-rules.md |

## Templates

| Trigger | SOP | Path |
|---------|-----|------|
| Create a new SOP, SOP template, document a process | SOP Creation Template | sops/templates/sop-creation-template.md |
| Write a session log, log format, end-of-session documentation | Session Log Format | sops/templates/session-log-format.md |

---

## How to Use This Router

1. Read the user's request
2. Scan the trigger phrases above for a match
3. **If a SKILL exists:** Load the skill file and execute from it. Only reference the full SOP if you need detailed edge-case guidance or learnings log context.
4. **If only an SOP exists:** Load the SOP file and follow its process
5. If multiple skills/SOPs match, load all relevant ones
6. If no skill or SOP matches, execute the task and consider creating a new SOP afterward

**Skills vs SOPs:**
- **Skills** (in `skills/`) are condensed, action-oriented instruction sets designed to be loaded and followed during execution. They are 2-4KB max.
- **SOPs** (in `sops/`) are the detailed reference documents with full context, learnings logs, common pitfalls, and edge cases. They are the source of truth.
- When in doubt, start with the skill. Escalate to the SOP if you hit a situation the skill doesn't cover.

All paths are relative to `~/Documents/Claude/Mainframe/`.
