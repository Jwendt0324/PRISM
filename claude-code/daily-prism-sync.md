# Daily PRISM Sync — Automated Prompt

**Runs unattended via launchd. No Gmail access — local files only.**

---

## Prompt

You are running the Daily PRISM Sync. This is an automated maintenance task that keeps the PRISM healthy between manual Gmail refreshes. You have NO access to Gmail or Calendar MCP tools — work with local files only.

### Step 1: Check Session Logs

Read the most recent session logs from `~/Documents/Claude/PRISM/logs/` (current month directory). Look at any sessions from the past 24 hours.

For each recent session, extract:
- New client information mentioned
- New team changes mentioned
- Financial data mentioned
- Strategic decisions made
- Content produced or published
- SOPs created or updated

### Step 2: Update Memory Bank (Local Data Only)

If session logs contain new information that should be persisted:

1. Read the relevant memory bank file(s) in `~/Documents/Claude/PRISM/memory-bank/`
2. Append new entries with `[Added YYYY-MM-DD from session logs]` date stamps
3. Never delete existing entries — only add or update

Common updates from session logs:
- New articles written → update `11-content-assets.md`
- Client work done → update `04-client-directory.md` status
- SOPs changed → note in `09-project-history.md`

### Step 3: Verify CONTEXT.md Freshness

1. Read `~/Documents/Claude/PRISM/CONTEXT.md`
2. Read `~/Documents/Claude/PRISM/memory-bank/last-refresh.txt`
3. If last Gmail refresh was more than 5 days ago, note this in the sync log as a warning
4. If 3+ memory bank files were updated in Step 2, regenerate CONTEXT.md following its 11-section structure

### Step 4: Check for Stale Data

Scan memory bank files for anything that looks outdated:
- Client statuses that reference dates more than 2 weeks old without recent updates
- Upcoming events that have now passed (check dates against today)
- Action items marked as pending that are overdue

Flag stale items in the sync log.

### Step 5: Write Sync Log

Create a brief log at `~/Documents/Claude/PRISM/logs/YYYY-MM/daily-sync-YYYYMMDD.md`:

```markdown
---
date: YYYY-MM-DDTHH:MM:SSZ
category: system
task_type: daily-PRISM-sync
---

# Daily PRISM Sync — YYYY-MM-DD

## Sessions Since Last Sync
- [count] sessions found
- Key activity: [1-2 sentence summary]

## Memory Bank Updates
- [list files updated and what changed, or "No updates needed"]

## Stale Data Warnings
- [list any stale items found, or "None"]

## Gmail Refresh Status
- Last Gmail refresh: [date from last-refresh.txt]
- Days since refresh: [N]
- Status: [CURRENT / STALE — manual refresh recommended]

## CONTEXT.md
- Regenerated: [yes/no]
```

Keep the log concise. If nothing happened since yesterday, still write the log but note "No new activity."

---

## Configuration
- **Frequency:** Daily, Monday-Friday
- **Duration:** 1-3 minutes
- **Dependencies:** None (local files only)
- **Gmail required:** NO

---

## See Also
- [[CONTEXT|Context]]
- [[_Dashboard|Dashboard]]
- [[memory-bank/INDEX|Memory Bank Index]]
- [[sops/file-management/logging-discipline|Logging Discipline SOP]]
- [[claude-code/scheduled-memory-refresh|Scheduled Memory Refresh]]
