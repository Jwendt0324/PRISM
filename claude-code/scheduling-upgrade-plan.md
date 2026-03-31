# Scheduling Upgrade Plan — Replace launchd with /schedule

**Created:** 2026-03-30
**Status:** Recommendation (not yet implemented)

## Problem
[Your Name]'s launchd-based scheduling is unreliable (per feedback memory). Sessions launched via `claude -p` from launchd don't consistently execute.

## Solution Options

### Option A: Cloud Scheduled Tasks via /schedule (Preferred)
Claude Code's `/schedule` creates persistent, cloud-hosted cron jobs that:
- Run on Anthropic's infrastructure (not your Mac)
- Survive machine restarts and sleep
- Execute against a specified git repository
- Support standard cron expressions or natural language scheduling

### Option B: Headless Mode via launchd (Fallback)
If cloud scheduling isn't available, fix launchd with `--bare` flag:
```bash
claude -p "your prompt" --bare --allowedTools Read,Write,Edit,Grep,Glob,Bash
```
- `--bare` skips auto-discovery for consistent behavior
- `--allowedTools` restricts tool access for safety
- Add `--output-format stream-json` for structured output parsing

## Recommended Scheduled Tasks

### 1. [[claude-code/weekly-briefing|Weekly Briefing]] (Replace launchd)
```
/schedule "every Monday 7:00 AM CT" "Run the weekly briefing. Read ~/Documents/Claude/PRISM/claude-code/weekly-briefing.md and follow all instructions."
```

### 2. [[claude-code/weekly-retrospective|Weekly Retrospective]]
```
/schedule "every Friday 5:00 PM CT" "Run the weekly retrospective. Read ~/Documents/Claude/PRISM/claude-code/weekly-retrospective.md and follow all instructions."
```

### 3. [[claude-code/scheduled-memory-refresh|Memory Bank Refresh]]
```
/schedule "every Wednesday 8:00 AM CT" "Run the memory bank refresh. Read ~/Documents/Claude/PRISM/claude-code/scheduled-memory-refresh.md and follow all instructions."
```

### 4. [[claude-code/weekly-sop-health-check|SOP Health Check]]
```
/schedule "every Sunday 10:00 PM CT" "Run the SOP health check. Read ~/Documents/Claude/PRISM/claude-code/weekly-sop-health-check.md and follow all instructions."
```

### 5. Daily Gmail Scan (NEW)
```
/schedule "every weekday 8:00 AM CT" "Run /inbox-triage and save results to ~/Documents/Claude/PRISM/logs/reports/inbox-triage-$(date +%Y-%m-%d).md"
```

## Alternative: /loop for In-Session Polling
For tasks that only need to run while [Your Name] is working:
```
/loop 30m "Check Basecamp for new activity and summarize anything needing my attention"
```

## Migration Steps
1. [Your Name] runs each `/schedule` command from Claude Code CLI
2. Verify each scheduled task fires correctly
3. Remove old launchd plist files once confirmed
4. Keep launchd only for truly local tasks (file organization)

## Cost Consideration
Each scheduled task execution uses API tokens. Estimated cost:
- Weekly briefing: ~$0.50-1.00 per run
- Weekly retro: ~$0.30-0.50 per run
- Memory refresh: ~$1.00-2.00 per run (scans Gmail)
- SOP health: ~$0.30-0.50 per run
- Daily inbox: ~$0.50-1.00 per run
- **Monthly total: ~$40-60**

---

## See Also
- [[claude-code/scheduled-tasks-migration|Scheduled Tasks Migration]]
- [[claude-code/AUTOMATION-STATUS|Automation Status]]
- [[skills/PRISM-core|PRISM Core Skill]]
- [[sops/file-management/logging-discipline|Logging Discipline]]
- [[_Dashboard]]