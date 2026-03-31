# Automation Status Report
Last verified: 2026-03-30 (full audit + bug fixes)

---

## Active Hooks (10 events in ~/.claude/settings.json)

| Hook Event | Script | Status | Notes |
|---|---|---|---|
| **SessionStart** | `session-start.sh` | **ACTIVE** | Logs session event, injects daily context, sets tab title. Fixed: session count now accurate (was 2x inflated), retrospective check now uses correct filename pattern. |
| **PreToolUse** | `pre-tool-guard.sh` | **ACTIVE** | Security guard — blocks recursive rm on home/root, force pushes, credential writes, system file writes. **Fixed 2026-03-30: block messages now go to stdout (were going to stderr, making guard a no-op).** Fixed: rm regex no longer blocks single-file deletions. |
| **PreToolUse** | `enforce-naming.sh` | **ACTIVE** | Auto-corrects content filenames (spaces→hyphens, uppercase→lowercase). Uses updatedInput merge. |
| **PostToolUse** | `post-tool.sh` | **ACTIVE** | Writes JSONL metadata to `logs/actions/YYYY-MM-DD.jsonl`. Fixed: removed `set -euo pipefail` (was silently killing logging), added backslash escaping to JSON serializer. |
| **PostToolUse** | `post-tool-backup.sh` | **ACTIVE** | Auto-creates .bak copies for Write/Edit >1KB. Fixed: backup cleanup now conditional on backup success. |
| **UserPromptSubmit** | `prompt-guard.sh` | **ACTIVE** | Detects confidential topics, injects privacy reminder. Updated ralph-loop skip logic. |
| **UserPromptSubmit** | `auto-skill-router.sh` | **ACTIVE** | Analyzes prompts and injects skill-loading directives. Updated ralph-loop skip logic. |
| **Notification** | `notify-telegram.sh` | **REQUIRES CONFIG** | Needs `config/telegram.json` with bot_token and chat_id. Fixed: uses --data-urlencode for special characters, removed Markdown parse_mode (was breaking on special chars). |
| **TaskCompleted** | `task-completed.sh` | **ACTIVE** | Logs completed tasks to `logs/tasks/YYYY-MM-DD.jsonl`. Clean, no issues. |
| **Stop** | `stop-summary.sh` | **ACTIVE** | Injects reminder for Claude to fill in session log learnings. |
| **StopFailure** | `stop-failure.sh` | **ACTIVE** | Logs API errors, provides recovery context. Fixed: JSON injection vulnerability patched (uses jq for safe encoding). |
| **SessionEnd** | `session-end.sh` | **ACTIVE** | Calls parse-session.py + export-conversation.py. **Fixed: now cleans up tab title enforcer process (was leaking zombies).** Added null check on input. |
| **PostCompact** | `post-compact.sh` | **ACTIVE** | Logs compaction events, injects context preservation reminder. Fixed: now reads session ID from stdin instead of nonexistent env var. |

### Inactive Script
| Script | Status | Notes |
|---|---|---|
| `file-changed.sh` | **INACTIVE** | "FileChanged" is not a supported Claude Code hook event. Dead code kept for future use. |

---

## Scripts (~/Documents/Claude/PRISM/scripts/)

| Script | Status | Notes |
|---|---|---|
| `parse-session.py` | **WORKING** | Fixed: eliminated double call to enrich_from_actions_log. |
| `export-conversation.py` | **WORKING** | Fixed: confidential detection no longer false-positives on "dennis" alone. |
| `generate-eod-report.py` | **WORKING** | Fixed: files_touched now checks both "target" and "file" keys. Fixed: learnings check now filters by target date (was showing entire month). |
| `generate-weekly-report.py` | **WORKING** | Minor: has dead code in sessions_by_day counter, import inside function. Low priority. |
| `convert-all-to-docx.py` | **WORKING** | Fixed: table cell font size no longer corrupts document-wide style. |
| `rotate-logs.sh` | **WORKING** | Clean, no issues found. |
| `deploy_all.py` | **SECURITY WARNING** | Contains plaintext credentials for [Parts Distributor], [Field Service Platform], RSS. See SECURITY-WARNING.md. Not for public repos. |
| `deploy_parts_agent.py` | **DELETED** | Was completely broken (template placeholder, not real base64 data). Removed 2026-03-30. |

---

## Auto-Reports (First Session of Day) — Added 2026-03-30

Runs via `session-start.sh` on first weekday session. Zero effort.

| Report | Script | Output |
|---|---|---|
| Health Check | `scripts/generate-health-check.py` | `logs/reports/health-YYYY-MM-DD.md` |
| Content Pipeline | `scripts/generate-content-pipeline.py` | `logs/reports/content-pipeline-YYYY-MM-DD.md` |
| Yesterday's EOD | `scripts/generate-eod-report.py` | `logs/reports/eod-YYYY-MM-DD.md` (if missing) |

Smart reminders also fire: Monday → `/mission`, Friday → `/review`, Mon/Wed/Fri → `/refresh` if memory bank >5d stale.

---

## Manual Tasks

| Task | Prompt File | Status | Last Run |
|---|---|---|---|
| Memory Bank Refresh | [[claude-code/scheduled-memory-refresh|scheduled-memory-refresh.md]] | **MANUAL** (hook reminds Mon/Wed/Fri) | 2026-03-18 |
| Weekly Briefing | [[claude-code/weekly-briefing|weekly-briefing.md]] | **MANUAL** (hook reminds Monday) | 2026-03-25 |
| Weekly Retrospective | [[claude-code/weekly-retrospective|weekly-retrospective.md]] | **MANUAL** (hook reminds Friday) | Never |
| Daily PRISM Sync | [[claude-code/daily-PRISM-sync|daily-PRISM-sync.md]] | **MANUAL** | Unknown |
| Monthly Log Rotation | [[claude-code/monthly-log-rotation|monthly-log-rotation.md]] | **MANUAL** | Never |
| Weekly SOP Health Check | [[claude-code/weekly-sop-health-check|weekly-sop-health-check.md]] | **MANUAL** | Never |
| Content Pipeline Runner | [[claude-code/run-content-pipeline|run-content-pipeline.md]] | **REPLACED** by auto-report | N/A |
| Google Drive Sync | `scripts/convert-all-to-docx.py` | **NOT SCHEDULED** | Never |
| Basecamp Scan | No prompt file | **NOT IMPLEMENTED** | Never |
| File Organizer | launchd (`com.user.organize-files`) | **LOADED, UNVERIFIED** | Unknown |

---

## Bugs Fixed in 2026-03-30 Audit

### Critical
1. **pre-tool-guard.sh** — All 9 block messages went to stderr instead of stdout. Security guard was completely non-functional. **FIXED.**
2. **pre-tool-guard.sh** — rm regex blocked ALL file deletions under /Users/, not just recursive deletes. **FIXED.**
3. **session-start.sh** — Zombie tab title enforcer processes leaked on every session. **FIXED** (cleanup in session-end.sh).
4. **deploy_parts_agent.py** — Completely broken template (fake base64 payload). **DELETED.**

### High
5. **post-tool.sh** — `set -euo pipefail` silently killed logging on any non-zero exit. **FIXED.**
6. **post-tool.sh** — Backslashes in file paths produced malformed JSONL (131 bad entries). **FIXED.**
7. **stop-failure.sh** — JSON injection vulnerability from unescaped error details. **FIXED.**
8. **session-start.sh** — Session count inflated ~2x (counted all events, not just starts). **FIXED.**
9. **session-start.sh** — Retrospective check used wrong filename pattern, always fired. **FIXED.**
10. **generate-eod-report.py** — Wrong key name ("target" vs "file") made files_touched always empty. **FIXED.**
11. **convert-all-to-docx.py** — Table cell style change corrupted font size for all subsequent text. **FIXED.**
12. **post-compact.sh** — Used nonexistent CLAUDE_SESSION_ID env var, session always "unknown". **FIXED.**

### Medium
13. **export-conversation.py** — "dennis" keyword over-triggered CONFIDENTIAL classification. **FIXED.**
14. **post-tool-backup.sh** — Deleted old backups even if new backup copy failed. **FIXED.**
15. **notify-telegram.sh** — curl -d didn't URL-encode, special chars broke POST. **FIXED.**
16. **session-end.sh** — No null check on INPUT before piping to Python parser. **FIXED.**
17. **prompt-guard.sh** + **auto-skill-router.sh** — Ralph-loop marker file path may not exist. **IMPROVED** (checks multiple locations).

### Files Created/Deleted
- **CREATED:** `content-pipeline/qa-failures.md` (was missing, QA skill/SOP actively log here)
- **CREATED:** `scripts/SECURITY-WARNING.md` (documents credential exposure in deploy_all.py)
- **DELETED:** `scripts/deploy_parts_agent.py` (broken template)
- **ARCHIVED:** Legacy debug logs moved to `logs/archive/`
- **UPDATED:** `team-ops/00-team-os-overview.md` (fixed broken link to 06-client-intake-process.md)
- **UPDATED:** `sops/templates/sop-creation-template.md` (fixed reference to nonexistent sops/INDEX.md)
- **UPDATED:** `claude-code/overnight-content-audit.md` (stale SOP reference)
- **UPDATED:** `claude-code/overnight-full-overhaul.md` (stale SOP reference)
- **UPDATED:** `~/.claude/CLAUDE.md` (added 10 missing external skills, count 24→34)
- **ANNOTATED:** `file-changed.sh` (marked as inactive dead code)

---

## See Also
- [[_Dashboard]]
- [[sops/file-management/logging-discipline|Logging Discipline SOP]]
- [[skills/PRISM-core|PRISM Core Skill]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[claude-code/scheduled-tasks-migration|Scheduled Tasks Migration]]
- [[claude-code/scheduling-upgrade-plan|Scheduling Upgrade Plan]]