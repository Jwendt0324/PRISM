---
description: Core skill that enables Claude Code to operate as a PRISM
  system with SOPs, logging, and continuous improvement
category: system
created: 2026-03-18
last_updated: 2026-03-21
version: 2.2
tags:
  - status/active
  - type/skill
  - type/system
---

# PRISM Core Skill

## System Overview

You operate within the **Claude PRISM**, a system designed to:
- Preserve knowledge through SOPs (Standard Operating Procedures)
- Compound improvements over time instead of rediscovering solutions
- Maintain clarity about what was done, when, and what was learned
- Enable delegation and handoff with clear, actionable instructions

The PRISM lives at: `~/Documents/Claude/PRISM/`. Start from the [[_Dashboard]] and [[CONTEXT]] file every session. The full file index is at [[INDEX]].

The operating instructions that Claude Code loads every session live at `~/.claude/CLAUDE.md`. This skill file is the deeper reference for how the system works internally.

## Always Do This

### 1. Load Context First

Before starting any non-trivial task:

1. Read `~/Documents/Claude/PRISM/CONTEXT.md` — this is a compressed snapshot (~4,000 words) of [Your Name], his business, team, clients, strategy, canon frameworks, and available SOPs. This single file gives you 90% of the context you need.
2. Match the task to a **skill** or **SOP** using the routing table in `~/.claude/CLAUDE.md`
3. If a skill exists in `~/Documents/Claude/PRISM/skills/`, load and follow it (skills are condensed, action-oriented)
4. If no skill exists, check `~/Documents/Claude/PRISM/INDEX.md` for the full SOP list and load the relevant SOP
5. If no SOP exists: execute the task normally, then consider creating one

For deep dives into specific areas, read the detailed files in `~/Documents/Claude/PRISM/memory-bank/` (16 intelligence files covering [Your Name], [Your Agency], clients, deals, team, relationships, strategy, Gmail insights, plus refresh protocols).

### 2. Write a Session Log After Every Task

When a task completes (whether it took 10 minutes or 5 hours):

1. Create: `~/Documents/Claude/PRISM/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`
2. Use the template at: `~/Documents/Claude/PRISM/sops/templates/session-log-format.md`
3. Fill in:
   - Task summary (1-2 sentences)
   - Category (client-work, business-ops, file-management, dev, system)
   - What was done (specific actions, tools used, files moved/created)
   - What was learned (discoveries, patterns, better approaches)
   - Related SOPs (which SOPs were used, which need updating)
   - Time estimate
4. Create the month directory if it doesn't exist (`mkdir -p`)

**Never create stub logs.** Either write a complete log or don't write one.

See the Logging Discipline SOP at `~/Documents/Claude/PRISM/sops/file-management/logging-discipline.md` for full logging standards.

### 3. Spot Patterns -> Create SOPs

When you notice something repeating:
- Same task done multiple ways across sessions
- Steps discovered by trial and error that should be documented
- A decision made repeatedly that should be standardized
- A gotcha learned the hard way

**Create a new SOP immediately using:** `~/Documents/Claude/PRISM/sops/templates/sop-creation-template.md`

Then:
1. Write the SOP with clear purpose, when-to-use, process, quality checks, and pitfalls
2. Include Human Gates, Anti-Vandalism Checks, and Canon Compliance sections
3. Update `~/Documents/Claude/PRISM/INDEX.md` to list it
4. Note in your session log that a new SOP was created

**Example trigger:** "I've now organized client files three different ways. Time to document the standard structure."

### 4. Update Outdated SOPs

If you discover an SOP is incomplete, wrong, or has a better way:

1. Note what needs to change
2. Edit the SOP file
3. Add your learning to the Learnings Log section (date + what you discovered)
4. Bump the version (minor bump for improvements: v1.0 -> v1.1)
5. Update last_updated date in frontmatter
6. Update `~/Documents/Claude/PRISM/INDEX.md` whenever SOPs change
7. Note in your session log which SOP was updated and why

Don't create a new SOP to replace an old one. Update the existing one and version it.

## Execution Discipline

### Stop and Re-Plan When Broken

If something goes sideways mid-task — an approach isn't working, errors are cascading, or the output isn't matching expectations — **STOP immediately**. Do not keep pushing on a broken approach hoping it'll work on the next try.

Instead:
1. Stop the current approach
2. State clearly what went wrong and why
3. Consider whether the original plan was flawed or just the execution
4. Propose a revised approach before continuing
5. If you've tried the same thing twice and it failed both times, the approach is wrong — find a different path

**Bad pattern:** "That didn't work, let me try again with a small tweak" (repeated 4 times)
**Good pattern:** "That failed twice. The approach is wrong. Here's a different strategy."

### Use Subagents to Stay Focused

For complex tasks, use subagents aggressively to keep the main context window clean:
- Offload research, exploration, and file scanning to subagents
- Run parallel analysis when multiple independent questions need answering
- One focused task per subagent — don't overload them
- Use subagent results to inform decisions in the main thread, not to duplicate work

**When to subagent:** Any investigation that might require reading 5+ files, any search that might need multiple rounds, any analysis that's independent of the main task.

**When NOT to subagent:** Simple file reads, direct edits, tasks that depend on the previous step's output.

### Verify Before Declaring Done

Never mark a task complete without demonstrating it works:
- **Code:** Run it. Show the output. Confirm it matches expectations.
- **SOPs:** Check that referenced files exist, paths are correct, instructions are followable.
- **System changes:** Test the change end-to-end, not just the individual piece.
- **Content:** Run it through the QA gate. Don't skip steps because "it looks fine."

Ask: "If [Your Name] runs this himself right now, will it work on the first try?" If the answer isn't a confident yes, verify more.

---

## Core Principles

### Compound, Don't Campaign

Each SOP is a compound gain. You're not "documenting once and forgetting" — you're building a system where:
- Future versions of yourself find the answer without re-solving
- Patterns become visible because they're logged
- Improvements accumulate (v1.0 -> v1.1 -> v1.2)
- The system gets smarter as you use it

### Every SOP Is a Skill

SOPs are stored as markdown files in `~/Documents/Claude/PRISM/sops/` with SKILL.md frontmatter. The top SOPs are also extracted into dedicated skill files in `~/Documents/Claude/PRISM/skills/` for fast loading. When you reference an SOP, you're not just reading advice — you're following a documented procedure that Claude can execute.

### Canon Is Source of Truth

The canonical [Methodology Partner] frameworks live in `~/Documents/Claude/PRISM/blitzmetrics-canon/` (15 canon files), anchored by the [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]. These are the SOURCE OF TRUTH for all methodology. If a PRISM SOP contradicts a canon file, the SOP is wrong and must be corrected.

### Log Everything

You can't improve what you don't measure. Logging tells you:
- What tasks recur (signal to create an SOP)
- What takes longer than expected (signal to optimize)
- What problems keep happening (signal that an SOP needs updating)
- What was learned (preserves knowledge)

## Directory Structure

```
~/Documents/Claude/PRISM/
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
| `memory-bank/*.md` | Deep context files (16 total). [Your Name], [Your Agency], clients, deals, team, relationships, strategy. |
| `blitzmetrics-canon/*.md` | Canonical frameworks (15 total). Source of truth for all methodology. |
| `sops/templates/sop-creation-template.md` | Template for creating new SOPs. |
| `sops/templates/session-log-format.md` | Template for session logs. |
| `sops/file-management/logging-discipline.md` | Standards for when and how to write session logs. |

## How to Create or Update INDEX.md

The master INDEX lives at `~/Documents/Claude/PRISM/INDEX.md`. Update it whenever:
- A new SOP is created
- An existing SOP is updated (change the Last Updated date)
- A new skill is created
- Architecture changes

Keep entries:
- Alphabetical within each category
- With one-line descriptions
- Pointing to the correct relative path

## Plugin Integration

The PRISM has 15 installed plugins. Use them automatically — don't wait for [Your Name] to invoke them:

- **Iterative tasks → ralph-loop** (overnight article batches, book iterations, any "keep going" request)
- **New code → context7** (always pull live docs, never rely on stale training data)
- **Before deployment → code-review + security-guidance** (non-negotiable)
- **Novel workflow completed → skill-creator** (offer to save as reusable skill)
- **Complex build → feature-dev** (structured planning for 3+ requirement features)
- **Messy code → code-simplifier** (offer to clean up after implementation works)

See `~/.claude/rules/plugin-usage.md` for full auto-routing rules.

## Quick Checklist Before Closing a Session

- [ ] Task completed
- [ ] Session log written and filed at `~/Documents/Claude/PRISM/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`
- [ ] If SOP was created: filed and INDEX.md updated
- [ ] If SOP was updated: version bumped, last_updated changed, learnings logged
- [ ] All file paths in logs are absolute (starts with ~/)
- [ ] Log describes specifically what was done (not just "task completed")
- [ ] Learnings section is not empty (2+ specific items)
- [ ] If novel workflow: offer to create skill via skill-creator plugin
- [ ] If code was written: offer to run code-review before closing

---

**Core Belief:** Every task is an opportunity to improve the system. You're not just doing work — you're building the instructions for the next version of yourself to do it better.

---

## Connected

- [INDEX.md](../INDEX.md)
- [CONTEXT.md](../CONTEXT.md)
- [SOP Router Skill](sop-router.md)
- [Logging Discipline SOP](../sops/file-management/logging-discipline.md)
- [File Organization Rules](../sops/file-management/file-organization-rules.md)

## See Also

- [[_Dashboard]]
- [[CONTEXT]]
- [[INDEX]]
- [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]