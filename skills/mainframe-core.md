---
description: Core skill that enables Claude Code to operate as a Mainframe system with SOPs, logging, and continuous improvement
category: system
created: 2026-03-18
last_updated: 2026-03-20
version: 2.1
---

# Mainframe Core Skill

## System Overview

You operate within the **Claude Mainframe**, a system designed to:
- Preserve knowledge through SOPs (Standard Operating Procedures)
- Compound improvements over time instead of rediscovering solutions
- Maintain clarity about what was done, when, and what was learned
- Enable delegation and handoff with clear, actionable instructions

The Mainframe lives at: `~/Documents/Claude/Mainframe/`

The operating instructions that Claude Code loads every session live at `~/.claude/CLAUDE.md`. This skill file is the deeper reference for how the system works internally.

## Always Do This

### 1. Load Context First

Before starting any non-trivial task:

1. Read `~/Documents/Claude/Mainframe/CONTEXT.md` — this is a compressed snapshot (~4,000 words) of Jack, his business, team, clients, strategy, canon frameworks, and available SOPs. This single file gives you 90% of the context you need.
2. Match the task to a **skill** or **SOP** using the routing table in `~/.claude/CLAUDE.md`
3. If a skill exists in `~/Documents/Claude/Mainframe/skills/`, load and follow it (skills are condensed, action-oriented)
4. If no skill exists, check `~/Documents/Claude/Mainframe/INDEX.md` for the full SOP list and load the relevant SOP
5. If no SOP exists: execute the task normally, then consider creating one

For deep dives into specific areas, read the detailed files in `~/Documents/Claude/Mainframe/memory-bank/` (16 intelligence files covering Jack, HRI, clients, deals, team, relationships, strategy, Gmail insights, plus refresh protocols).

### 2. Write a Session Log After Every Task

When a task completes (whether it took 10 minutes or 5 hours):

1. Create: `~/Documents/Claude/Mainframe/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`
2. Use the template at: `~/Documents/Claude/Mainframe/sops/templates/session-log-format.md`
3. Fill in:
   - Task summary (1-2 sentences)
   - Category (client-work, business-ops, file-management, dev, system)
   - What was done (specific actions, tools used, files moved/created)
   - What was learned (discoveries, patterns, better approaches)
   - Related SOPs (which SOPs were used, which need updating)
   - Time estimate
4. Create the month directory if it doesn't exist (`mkdir -p`)

**Never create stub logs.** Either write a complete log or don't write one.

See the Logging Discipline SOP at `~/Documents/Claude/Mainframe/sops/file-management/logging-discipline.md` for full logging standards.

### 3. Spot Patterns -> Create SOPs

When you notice something repeating:
- Same task done multiple ways across sessions
- Steps discovered by trial and error that should be documented
- A decision made repeatedly that should be standardized
- A gotcha learned the hard way

**Create a new SOP immediately using:** `~/Documents/Claude/Mainframe/sops/templates/sop-creation-template.md`

Then:
1. Write the SOP with clear purpose, when-to-use, process, quality checks, and pitfalls
2. Include Human Gates, Anti-Vandalism Checks, and Canon Compliance sections
3. Update `~/Documents/Claude/Mainframe/INDEX.md` to list it
4. Note in your session log that a new SOP was created

**Example trigger:** "I've now organized client files three different ways. Time to document the standard structure."

### 4. Update Outdated SOPs

If you discover an SOP is incomplete, wrong, or has a better way:

1. Note what needs to change
2. Edit the SOP file
3. Add your learning to the Learnings Log section (date + what you discovered)
4. Bump the version (minor bump for improvements: v1.0 -> v1.1)
5. Update last_updated date in frontmatter
6. Update `~/Documents/Claude/Mainframe/INDEX.md` whenever SOPs change
7. Note in your session log which SOP was updated and why

Don't create a new SOP to replace an old one. Update the existing one and version it.

## Core Principles

### Compound, Don't Campaign

Each SOP is a compound gain. You're not "documenting once and forgetting" — you're building a system where:
- Future versions of yourself find the answer without re-solving
- Patterns become visible because they're logged
- Improvements accumulate (v1.0 -> v1.1 -> v1.2)
- The system gets smarter as you use it

### Every SOP Is a Skill

SOPs are stored as markdown files in `~/Documents/Claude/Mainframe/sops/` with SKILL.md frontmatter. The top SOPs are also extracted into dedicated skill files in `~/Documents/Claude/Mainframe/skills/` for fast loading. When you reference an SOP, you're not just reading advice — you're following a documented procedure that Claude can execute.

### Canon Is Source of Truth

The canonical BlitzMetrics frameworks live in `~/Documents/Claude/Mainframe/blitzmetrics-canon/` (15 canon files). These are the SOURCE OF TRUTH for all methodology. If a Mainframe SOP contradicts a canon file, the SOP is wrong and must be corrected.

### Log Everything

You can't improve what you don't measure. Logging tells you:
- What tasks recur (signal to create an SOP)
- What takes longer than expected (signal to optimize)
- What problems keep happening (signal that an SOP needs updating)
- What was learned (preserves knowledge)

## Directory Structure

```
~/Documents/Claude/Mainframe/
├── INDEX.md (master index)
├── CONTEXT.md (compressed context — load this first)
├── blitzmetrics-canon/ (15 canon files)
├── memory-bank/ (16 intelligence files + protocols)
├── team-ops/ (19 team operating docs)
├── sops/
│   ├── client-work/ (16 SOPs)
│   ├── business-ops/ (5 SOPs)
│   ├── file-management/ (2 SOPs)
│   └── templates/ (3 templates)
├── skills/ (7 callable skills)
├── logs/ (session logs by month)
├── content-pipeline/ (content output)
├── content-audit/ (content analysis)
├── claude-code/ (automation definitions + hooks)
└── scripts/ (utility scripts)
```

## Key Files and What They Do

| File | Purpose |
|------|---------|
| `CONTEXT.md` | Compressed context (~4K words). Load this first every session for 90% of what you need. |
| `INDEX.md` | Master index of all SOPs, skills, automation status, and architecture. |
| `~/.claude/CLAUDE.md` | Operating instructions loaded automatically by Claude Code. Contains the skill/SOP router. |
| `skills/*.md` | Callable skill files (7 total). Condensed, action-oriented versions of the top SOPs. |
| `memory-bank/*.md` | Deep context files (16 total). Jack, HRI, clients, deals, team, relationships, strategy. |
| `blitzmetrics-canon/*.md` | Canonical frameworks (15 total). Source of truth for all methodology. |
| `sops/templates/sop-creation-template.md` | Template for creating new SOPs. |
| `sops/templates/session-log-format.md` | Template for session logs. |
| `sops/file-management/logging-discipline.md` | Standards for when and how to write session logs. |

## How to Create or Update INDEX.md

The master INDEX lives at `~/Documents/Claude/Mainframe/INDEX.md`. Update it whenever:
- A new SOP is created
- An existing SOP is updated (change the Last Updated date)
- A new skill is created
- Architecture changes

Keep entries:
- Alphabetical within each category
- With one-line descriptions
- Pointing to the correct relative path

## Quick Checklist Before Closing a Session

- [ ] Task completed
- [ ] Session log written and filed at `~/Documents/Claude/Mainframe/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`
- [ ] If SOP was created: filed and INDEX.md updated
- [ ] If SOP was updated: version bumped, last_updated changed, learnings logged
- [ ] All file paths in logs are absolute (starts with ~/)
- [ ] Log describes specifically what was done (not just "task completed")
- [ ] Learnings section is not empty (2+ specific items)

---

**Core Belief:** Every task is an opportunity to improve the system. You're not just doing work — you're building the instructions for the next version of yourself to do it better.
