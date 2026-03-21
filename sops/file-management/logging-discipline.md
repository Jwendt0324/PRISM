---
description: Define when session logs are required, what quality standard they must meet, and how to prevent stub/empty logs from accumulating
category: file-management
created: 2026-03-20
last_updated: 2026-03-21
version: 2.0
canon_compliance: 05-maa-framework.md
triangles: MAA
triangles_served: [MAA]
human_gates: no
canon_sources: [05-maa-framework.md]
---

# Logging Discipline SOP

## Purpose

Ensure every Claude session is fully documented through a two-tier auto-capture system — and that the human-insight layer (learnings) is never left empty.

## Architecture

The logging system has two tiers:

### Tier 1: Auto-Captured by Hooks (no Claude action needed)
- **PostToolUse hook** → `~/Documents/Claude/Mainframe/logs/actions/YYYY-MM-DD.jsonl` — one JSONL line per tool call with timestamp, tool name, target (file path or command), and session ID. ~150 bytes per event.
- **SessionStart hook** → `~/Documents/Claude/Mainframe/logs/session-events.jsonl` — session start events
- **SessionEnd hook** → calls `parse-session.py` v3, which produces:
  - `~/Documents/Claude/Mainframe/logs/sessions/YYYY-MM/session-{ID}.jsonl` — machine-readable session data + full action sequence
  - `~/Documents/Claude/Mainframe/logs/sessions/YYYY-MM/session-{ID}.md` — human-readable summary with all auto-captured fields

### Tier 2: Claude's Responsibility (learnings + related SOPs)
- Before the session ends, Claude fills in `## What Was Learned` and `## Related SOPs` in the auto-generated markdown log
- Claude does NOT create the log file — hooks do that
- Claude does NOT rewrite auto-captured sections

### Reports (generated from Tier 1 + 2 data)
- **EOD:** `python3 ~/Documents/Claude/Mainframe/scripts/generate-eod-report.py [date]` → `logs/reports/eod-YYYY-MM-DD.md`
- **Weekly:** `python3 ~/Documents/Claude/Mainframe/scripts/generate-weekly-report.py [monday-date]` → `logs/reports/weekly-YYYY-WNN.md`
- **Log rotation:** `bash ~/Documents/Claude/Mainframe/scripts/rotate-logs.sh` — compresses action logs >7 days, deletes >90 days

## When Logging Is Required

- **Auto-logged (always):** Every session gets an action trail in the daily JSONL. Every qualifying session gets a session summary.
- **Trivial sessions are auto-skipped:** Sessions under 3 user messages with <5 tool calls and no file changes produce no session summary (but the action JSONL still captures every tool call).
- **Learnings are required for:** Any session with 10+ messages OR that creates/modifies files OR involves client work.

## Process (What Claude Does)

1. **Do your work.** Hooks capture everything automatically.
2. **Before session ends:** Find the auto-generated log at `~/Documents/Claude/Mainframe/logs/sessions/YYYY-MM/session-{FIRST_8_CHARS_OF_SESSION_ID}.md`
3. **Fill in What Was Learned:** 2+ actionable learnings (3+ for complex sessions). Use Discovery/Insight/Action format. **NEVER write placeholders.**
4. **Fill in Related SOPs:** List SOPs consulted. Flag any that need updates.
5. **Do NOT** create a separate log file, rewrite auto-captured sections, or update an INDEX.

## Quality Checks

### End-of-Session Checklist

- [ ] Auto-generated session log exists in `logs/sessions/YYYY-MM/`
- [ ] `[NEEDS LEARNINGS]` placeholder has been replaced with real learnings
- [ ] `[NEEDS REVIEW]` placeholder in Related SOPs has been replaced
- [ ] Learnings use Discovery/Insight/Action format
- [ ] No raw terminal output or task notifications in any section

### Weekly Review

- [ ] Run `python3 generate-weekly-report.py` and review
- [ ] Check "Sessions Missing Learnings" section — fill in or accept as-is
- [ ] Scan learnings for patterns → create new SOPs if needed
- [ ] Run `bash rotate-logs.sh` to compress old action logs

## Forensic Audit Workflow

If something goes wrong, trace the issue:

1. **Start broad:** `~/Documents/Claude/Mainframe/logs/session-events.jsonl` — find the session by time range
2. **Get the action sequence:** `grep "SESSION_ID" logs/actions/YYYY-MM-DD.jsonl` — every tool call with timestamps and targets
3. **Read the summary:** `logs/sessions/YYYY-MM/session-{ID}.md` — files created/modified, commands run
4. **Deep dive:** `~/.claude/projects/-Users-jackwendt/{session_id}.jsonl` — full conversation transcript with all inputs and outputs

## Storage Budget

| Log type | Per-event | Daily | Monthly |
|----------|-----------|-------|---------|
| Actions JSONL | ~150 B | ~5K events = ~750 KB | ~23 MB |
| Session JSONL | ~2 KB | ~15 sessions = ~30 KB | ~900 KB |
| Session .md | ~5 KB | ~15 sessions = ~75 KB | ~2.2 MB |
| Reports | ~3-5 KB | 1/day | ~150 KB |
| **Total (raw)** | | | **~26 MB** |
| **After rotation** (7-day compress, 90-day delete) | | | **~3 MB** |

## Common Pitfalls

1. **Creating stub files "to fill in later."** You won't. Either write the full log now or don't create the file. Empty stubs pollute the system and create false confidence that logging happened.

2. **Generic learnings.** "Learned how to use the tool better" is useless. Be specific: "Discovered that `Grep` with `multiline: true` catches cross-line patterns that single-line mode misses — used this to find 8 additional instances in `/src/auth/`."

3. **Relative file paths.** Claude Code's working directory resets between Bash calls. Every path in a session log must be absolute (`~/Documents/Claude/Mainframe/...`), never relative (`../sops/...`).

4. **Skipping logs for "small" sessions that modified files.** If you touched a file, log it. A 5-message session that rewrites a critical SOP is more important to log than a 50-message research conversation.

5. **Forgetting the learnings section.** The natural impulse is to document what was done and skip what was learned. The learnings section is the most valuable part — it's what makes the system compound. If you can't think of learnings, ask: "What would I do differently next time? What surprised me? What took longer than expected?"

6. **Not flagging SOP updates.** When you learn something that contradicts or extends an existing SOP, note it in Related SOPs. Don't let the insight die in a log file — it needs to flow back into the SOP.

7. **Writing `[To be extracted during retrospective]` in What Was Learned.** This is the #1 observed violation as of 2026-03-21. Multiple logs across the system have this exact placeholder. No one goes back to fill them in. The rule is absolute: write real learnings at log creation time, or don't create the log.

8. **Logging trivial sessions.** A 1-message, 1-tool-call Q&A session ("how many SOPs are active?") does not need a log. The SOP says under-10-message sessions with no file changes are OPTIONAL. Don't create partial logs for these — they just clutter the INDEX.

9. **Dumping raw terminal output into logs.** Task notifications, login banners, and raw prompt text should never appear in What Was Requested or Task Summary. Summarize what was asked in human-readable form.

## Canon Compliance

- **Canon source:** `~/Documents/Claude/Mainframe/blitzmetrics-canon/05-maa-framework.md`
- **Triangles served:** MAA — Session logs are the Mainframe's measurement system. Metrics = what was done, Analysis = what was learned, Action = SOP updates flagged. Without disciplined logging, the Mainframe has no MAA loop and cannot improve.
- **Human checkpoints:** Jack reviews weekly retrospective output, which is derived from session logs. No human gate on individual log creation.
- **Anti-vandalism:** Minimum file size (500 bytes) prevents stubs. Required sections prevent incomplete logs. Monthly maintenance catches any that slip through. Absolute path requirement prevents broken references.
- **Last audited:** 2026-03-20

## Learnings Log

- **2026-03-20:** Initial creation. Codifies rules that were previously implicit in `CLAUDE.md` and `session-log-format.md`. Key gap addressed: no prior SOP defined when logging is required vs. optional, or what constitutes a "stub" log.
- **2026-03-21:** v1.1 — Audit found widespread `[To be extracted during retrospective]` placeholders in What Was Learned sections across 5+ logs. Added absolute prohibition on placeholder text. Added pitfalls for trivial session logging and raw terminal output dumping. Updated session-log-format.md to v2.0 hybrid format (auto-capture fields + mandatory learnings).
- **2026-03-21:** v2.0 — Complete rewrite. Moved from "Claude writes logs manually" to two-tier auto-capture system. Hooks now capture every tool call to JSONL action logs (~150 bytes each). parse-session.py v3 produces dual output (machine JSONL + human markdown). Claude's only job is filling in learnings. Deleted 20MB legacy hook-debug.log. Added EOD/weekly report generators, log rotation, and forensic audit workflow. Storage drops from ~20MB/day (debug dumps) to ~26MB/month (compressed to ~3MB).
