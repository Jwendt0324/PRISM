# Scheduled Tasks Migration Plan — launchd → /schedule

**Created:** 2026-03-30
**Purpose:** Replace unreliable launchd + manual prompts with Claude Code's built-in `/schedule` (persistent, survives restarts, runs on Anthropic infrastructure).

---

## Why Migrate

Per memory: launchd + `claude -p` is NOT reliable. The PRISM has 5 manual tasks that should run automatically. Desktop scheduled tasks persist across restarts and auto-expire after 3 days (re-create weekly or use `/schedule` for cloud-hosted cron).

---

## Migration Table

| Task | Current State | Target Schedule | Priority | Command |
|------|--------------|-----------------|----------|---------|
| Memory Bank Refresh | Manual prompt | Mon/Wed/Fri 6:30 AM CT | HIGH | `/schedule create --cron "30 6 * * 1,3,5" --name "memory-refresh" --prompt "Run the memory bank refresh: read ~/Documents/Claude/PRISM/claude-code/scheduled-memory-refresh.md and follow it"` |
| [[claude-code/weekly-briefing|Weekly Briefing]] | Manual prompt | Monday 8:00 AM CT | HIGH | `/schedule create --cron "0 8 * * 1" --name "weekly-briefing" --prompt "Run /briefing"` |
| [[claude-code/weekly-retrospective|Weekly Retrospective]] | Manual prompt | Friday 4:00 PM CT | HIGH | `/schedule create --cron "0 16 * * 5" --name "weekly-review" --prompt "Run /review"` |
| [[claude-code/weekly-sop-health-check|SOP Health Check]] | Manual prompt | Friday 7:00 AM CT | MEDIUM | `/schedule create --cron "0 7 * * 5" --name "sop-health" --prompt "Read ~/Documents/Claude/PRISM/claude-code/weekly-sop-health-check.md and follow it"` |
| Auto-Dream | Manual (/dream) | Daily 2:00 AM CT | MEDIUM | `/schedule create --cron "0 2 * * *" --name "auto-dream" --prompt "Run /dream"` |
| [[claude-code/daily-PRISM-sync|Daily Sync]] | Manual prompt | Mon-Fri 6:30 AM CT | LOW | `/schedule create --cron "30 6 * * 1-5" --name "daily-sync" --prompt "Read ~/Documents/Claude/PRISM/claude-code/daily-PRISM-sync.md and follow it"` |

---

## Setup Steps for [Your Name]

1. Open Claude Code Desktop app
2. Run each `/schedule create` command from the table above
3. Verify with `/schedule list` — all 6 should appear
4. Monitor first runs by checking `~/Documents/Claude/PRISM/logs/reports/` for output

**Note:** Recurring tasks auto-expire after 3 days. You may need to re-create them weekly, or use the cloud-hosted `/schedule` which persists longer.

**Alternative:** If using Claude Code Desktop, scheduled tasks persist as long as the app is open. For always-on scheduling, cloud-hosted triggers via `/schedule` are more reliable.

---

## What to Retire

| Old Method | Action |
|-----------|--------|
| `com.user.organize-files` launchd agent | Keep running (low risk, handles file cleanup) |
| Manual "run the daily sync" prompts | Replace with scheduled trigger |
| Manual "run the weekly briefing" prompts | Replace with scheduled trigger |
| Manual "refresh the memory bank" prompts | Replace with scheduled trigger |

---

## Auto-Dream vs Built-in Auto-Dream

Claude Code is rolling out a built-in "auto-dream" feature (March 2026) that automatically consolidates memory after 5+ sessions every 24h. This handles MEMORY.md auto-memory files.

[Your Name]'s `/dream` command does MORE than auto-dream:
- Session analysis (patterns, failures, discoveries)
- [[memory-bank/INDEX|Memory bank]] curation (14 files in memory-bank/)
- SOP evolution (updating SOPs from learnings)
- Skill quality improvement
- System health checks

**Recommendation:** Keep `/dream` scheduled even if auto-dream activates — they're complementary. Auto-dream handles MEMORY.md; `/dream` handles the full PRISM.

---

## See Also
- [[claude-code/scheduling-upgrade-plan|Scheduling Upgrade Plan]]
- [[claude-code/daily-PRISM-sync|Daily PRISM Sync]]
- [[claude-code/AUTOMATION-STATUS|Automation Status]]
- [[sops/file-management/logging-discipline|Logging Discipline]]
- [[_Dashboard]]