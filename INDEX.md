# CLAUDE PRISM — MASTER INDEX

**Owner:** [Your Name]
**Created:** 2026-03-18
**Last Updated:** 2026-03-21 (Full overhaul: 5 new skills, 4 skills refined, Article QA consolidated, stale files cleaned, duplicates removed, routing updated)

---

## What This Is

The PRISM is a self-improving knowledge system. Every task Claude executes generates session logs. Those logs feed into living SOPs. Those SOPs are formatted as Claude skills, which means Claude automatically loads and follows them on future tasks. The system compounds — Claude gets better at your work every time it works for you.

---

## Architecture

```
PRISM/
├── CONTEXT.md           ← Compressed context file (all memory bank + SOPs in <5K words)
├── skills/              ← Active SKILL.md files Claude loads automatically (12 files)
│   ├── PRISM-core.md       ← System operations, logging, SOP management
│   ├── sop-router.md           ← Routes tasks to correct SOP/skill
│   ├── content-factory.md      ← 6-stage Content Factory execution
│   ├── article-writer.md       ← Batch article writing from transcripts
│   ├── article-qa.md           ← [Methodology Partner] 18-step quality gate
│   ├── dollar-a-day.md         ← 3-phase paid social campaigns
│   ├── content-repurposing.md  ← Raw content to 10-15 multi-platform outputs
│   ├── weekly-maa-report.md    ← Friday MAA reporting for all clients
│   ├── kp-sprint.md            ← 30-day Knowledge Panel Sprint execution
│   ├── influence-report-card.md ← 5-axis authority assessment
│   ├── personal-brand-site.md  ← WordPress personal brand site builds
│   └── prospect-followup.md    ← Lead qualification and follow-up cadence
├── sops/                ← Living SOPs (human-readable + skill-formatted)
│   ├── client-work/     ← Content Factory, audits, site builds, Dollar-a-Day, Content Repurposing Pipeline
│   ├── business-ops/    ← Outreach, proposals, internal processes
│   ├── file-management/ ← How files get organized (the organizer's own rules)
│   └── templates/       ← Reusable templates for common deliverables
├── logs/                ← Auto-captured session logs from Claude Code
│   └── YYYY-MM/         ← Organized by month
├── team-ops/            ← Team Operating System (onboarding, roles, processes, scaling)
├── memory-bank/         ← Shared Memory Bank ([Your Name], [Your Agency], clients, deals, relationships)
│   └── refresh-protocol.md ← Defines how memory bank gets refreshed
├── content-pipeline/    ← Output from Content Repurposing Pipeline runs
│   └── HOW-TO-USE.md    ← Instructions for running the pipeline
├── blitzmetrics-canon/  ← Canonical [Methodology Partner] frameworks (9 Triangles, CF Process, Article Guidelines, etc.)
├── content-audit/       ← Content inventory and gap analysis
├── claude-code/         ← Claude Code operating instructions and scheduled prompts
├── inbox/               ← Staging area for files being triaged
└── INDEX.md             ← This file
```

---

## Active SOPs

| SOP | Category | Status | Last Updated | Skill Linked |
|-----|----------|--------|--------------|--------------|
| Content Factory Execution | client-work | Active | 2026-03-20 | Yes |
| Influence Report Card | client-work | Active | 2026-03-20 | Yes |
| Personal Brand Site Build | client-work | Active | 2026-03-20 | Yes |
| Dollar-a-Day Campaign Setup | client-work | Active | 2026-03-20 | Yes |
| YouTube Transcript Scraping | client-work | Active | 2026-03-20 | Yes |
| Podcast Transcript Scraping | client-work | Active | 2026-03-20 | Yes |
| Article Writing from Transcripts | client-work | Active | 2026-03-20 | Yes |
| Article QA — [Methodology Partner] 18-Step (consolidated) | client-work | Active | 2026-03-21 | Yes |
| Guest Appearance Research | client-work | Active | 2026-03-20 | Yes |
| AI Apprentice Onboarding | client-work | Active | 2026-03-20 | Yes |
| Client Onboarding | client-work | Active | 2026-03-20 | Yes |
| Knowledge Panel Sprint | client-work | Active | 2026-03-20 | Yes |
| Prospect Follow-Up | client-work | Active | 2026-03-20 | Yes |
| Weekly MAA Report | client-work | Active | 2026-03-20 | Yes |
| KP Sprint Project Management | team-ops | Active | 2026-03-18 | Yes |
| Client Communication | team-ops | Active | 2026-03-18 | Yes |
| [Your Agency] Offer Ladder & GTM Blueprint | business-ops | Active | 2026-03-18 | Yes |
| Event Planning ([Your Speaker Event]) | business-ops | Active | 2026-03-18 | Yes |
| P&L Reporting | business-ops | Active | 2026-03-18 | Yes |
| Refund & Escalation | business-ops | Active | 2026-03-18 | Yes |
| University Speaking Outreach | business-ops | Active | 2026-03-18 | Yes |
| File Organization Rules | file-management | Active | 2026-03-18 | Yes |
| Logging Discipline | file-management | Active | 2026-03-20 | Yes |
| Content Repurposing Pipeline | client-work | Active | 2026-03-20 | Yes |
| SOP Creation Template | templates | Active | 2026-03-18 | Yes |
| Session Log Format | templates | Active | 2026-03-18 | Yes |
| New Hire Onboarding SOP | team-ops | Active | 2026-03-18 | Yes |
| [Your Content Specialist] Onboarding Kit | team-ops | Active | 2026-03-18 | Yes |
| Escalation Playbook | team-ops | Active | 2026-03-18 | Yes |
| Team Scaling Plan | team-ops | Active | 2026-03-18 | Yes |
| Current Pain Points | team-ops | Active | 2026-03-18 | Yes |

---

## Team Operating System

Full team OS lives in `team-ops/`. See [team-ops/INDEX.md](team-ops/INDEX.md) for the master index.

Key documents: Team directory, communication protocols, decision rights matrix, meeting cadence, delegation framework, onboarding SOPs (generic + [Your Content Specialist]-specific), role scorecards, tool stack, project management SOP, client communication SOP, escalation playbook, scaling plan, pain points analysis. Plus ready-to-send [Your Content Specialist] welcome email and team announcement.

---

## Automated Tasks

> **Status Report:** See [`claude-code/AUTOMATION-STATUS.md`](claude-code/AUTOMATION-STATUS.md) for a verified audit of what is actually running vs. defined on paper. Last verified: 2026-03-20.

| Task | Frequency | Scheduling | Status | What It Does |
|------|-----------|------------|--------|--------------|
| SessionStart Hook | Every session | `~/.claude/settings.json` | **ACTIVE** | Logs session start to `logs/session-events.log` and `logs/hook-debug.log` |
| PostToolUse Hook | Every tool use | `~/.claude/settings.json` | **ACTIVE** | Logs tool name + session ID to `logs/tool-usage.log` |
| Stop Hook | Every response | `~/.claude/settings.json` | **ACTIVE** | Injects systemMessage prompting Claude to write a session log |
| SessionEnd Hook | Every session end | `~/.claude/settings.json` | **ACTIVE** | Calls `scripts/parse-session.py` to generate structured session logs |
| Daily PRISM Sync | Mon-Fri [Schedule Time] | launchd (`com.yourname.memory-refresh`) | **ACTIVE** | Reviews session logs, updates memory bank from local data, flags stale items. No Gmail. |
| Weekly Briefing | Monday [Schedule Time] | launchd (`com.yourname.weekly-briefing`) | **ACTIVE** | Full state-of-business snapshot. Emailed to [your-email@your-agency.com] via Apple Mail. |
| Weekly SOP Health Check | Friday [Schedule Time] | launchd (`com.yourname.sop-health-check`) | **ACTIVE** | Reviews session logs for SOP usage, checks freshness, identifies new SOP candidates. |
| File Organizer | Nightly [Schedule Time] | launchd (`com.yourname.organize-files`) | **ACTIVE** | Organizes Downloads/Desktop/Documents by file type. |
| Monthly Log Rotation | 1st of month, [Schedule Time] | launchd (`com.yourname.log-rotation`) | **ACTIVE** | Rotates large logs, archives old monthly dirs, cleans up old backups. |
| Gmail Memory Refresh | Manual | Prompt at `claude-code/scheduled-memory-refresh.md` | **MANUAL** | Full Gmail scan — requires interactive session. Say "refresh the memory bank" 2-3x/week. |
| Google Drive Sync | Not implemented | `scripts/convert-all-to-docx.py` exists | **NOT IMPLEMENTED** | Script ready but not scheduled. |
| Basecamp Scan | Not implemented | No prompt file exists | **NOT IMPLEMENTED** | Requires Basecamp API integration. |

---

## How SOPs Get Created and Updated

1. **Claude executes a task** (in Claude Code or Cowork)
2. **Post-session hook** writes a structured log entry to `logs/YYYY-MM/`
3. **Weekly Retrospective task** reads logs, identifies repeating patterns
4. **New SOP is drafted** or existing SOP is updated with new learnings
5. **SOP is formatted as a SKILL.md** and placed in `skills/` so Claude auto-loads it
6. **INDEX.md is updated** with the new/changed SOP entry

---

## How to Use This System

**As [Your Name] (human):**
- Drop files into `inbox/` when you want them triaged
- Read SOPs in `sops/` to see how your systems work
- Check `INDEX.md` for an overview of everything

**As Claude:**
- Always check `skills/` for relevant skills before starting any task
- After completing a task, write a session log to `logs/`
- When you notice a repeating pattern without an SOP, create one
- When an SOP is outdated or incomplete, update it directly
- Update `INDEX.md` whenever SOPs change

---

## Memory Bank

The Shared Memory Bank lives in `memory-bank/`. See [memory-bank/INDEX.md](memory-bank/INDEX.md) for the master index.

**14 files** covering: [Your Name]'s personal profile, [Your Agency] company overview, [Methodology Partner] relationship, team directory ([N people]), client directory ([N engagements]), vendor/partner map, deal history ([$Revenue] revenue), relationship map, communication patterns, project history ([N projects]), financial context, content assets, strategic context, and Gmail insights.

**Built from:** Full Gmail scan of [your-email@your-agency.com] ([X messages] / [Y threads]), all PRISM SOPs, operating documents, and PDFs.

**Refresh Protocol:** `memory-bank/refresh-protocol.md` — defines how the memory bank gets updated weekly. Last refresh: 2026-03-18.

**Compressed Context:** `CONTEXT.md` (root level) — all 14 memory bank files compressed into <5,000 words for fast session loading.

---

## [Methodology Partner] Canon

The canonical [Methodology Partner] frameworks live in `blitzmetrics-canon/`. These are the SOURCE OF TRUTH for all methodology. If a PRISM SOP contradicts a canon file, the SOP is wrong.

| File | Description |
|------|-------------|
| 00-drive-index.md | Master index of [Methodology Partner] Shared Drive documents |
| 01-nine-triangles.md | The complete 9 Triangles framework (WHY/HOW/WHAT tiers) |
| 02-content-factory-process.md | The canonical 6-stage Content Factory process |
| 03-article-guidelines.md | 18-step article quality checklist |
| 04-dollar-a-day.md | Dollar-a-Day strategy with phases and budgets |
| 05-maa-framework.md | Metrics, Analysis, Action framework and templates |
| 06-topic-wheel.md | Topic Wheel methodology (WHY→HOW→WHAT) |
| 07-quality-standards.md | All quality standards across content types |
| 08-human-requirements.md | Where humans are REQUIRED in every process |
| 09-data-connections-needed.md | Data systems to connect and their priority |
| 10-anti-vandalism-checklist.md | Rules to prevent unintentional damage |
| 11-gct-discovery-framework.md | GCT implementation guide — how to facilitate discovery, question sets, scoping matrix, output template |
| 12-ldt-implementation-guide.md | Learn, Do, Teach implementation guide — phases, skill levels, tracking, MICRO courses, human gates |
| honest-assessment.md | Brutally honest PRISM self-assessment |
| sop-audit-report.md | Full audit of every SOP against the canon |

**Built from:** Full ingestion of [Methodology Partner] Shared Drive documents, Master Content Factory Guides (v9.9, v1.2, v1.7, v1.9), Course Builder Guide v9.1, Operations Guide v12.5, Video Editing Guide v1.5, Dollar-a-Day materials, and [methodology-partner.com]/blog-posting-guidelines/.

---

## Principles

- **SOPs are living documents.** They change every time Claude learns something.
- **Every SOP is a skill.** If it's not formatted for Claude to load, it's not done.
- **Log everything.** Sessions without logs are wasted learning.
- **Compound, don't campaign.** Build systems that get better, not docs that sit there.
