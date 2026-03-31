# Scheduled Memory Bank Refresh — Ready-to-Use Prompt

**Use this prompt manually in an interactive session (Gmail MCP required).**
**For automated daily maintenance, see `daily-PRISM-sync.md` instead.**

---

## Prompt

You are running a full Memory Bank Refresh for the Claude PRISM. This requires Gmail MCP access — if Gmail tools are not available, stop and tell the user to run this in an interactive session.

Follow these steps exactly:

### Step 1: Load the Protocol
Read `~/Documents/Claude/PRISM/memory-bank/refresh-protocol.md` — this defines exactly which files to scan, what queries to run, and how to update each file.

### Step 2: Get the Date Range
Read `~/Documents/Claude/PRISM/memory-bank/last-refresh.txt` to get the last refresh date. All Gmail searches should use `after:YYYY/M/D` with this date to only scan new messages.

### Step 3: Scan Gmail
Search Gmail for **[your-email@your-agency.com] ONLY** — do NOT access any other Gmail account.

Run the search queries defined in the refresh protocol for each active file:
- 04-client-directory.md queries
- 03-team-directory.md queries
- 06-deal-history.md queries
- 07-relationship-map.md queries
- 12-strategic-context.md queries
- 13-gmail-insights.md queries
- 09-project-history.md queries
- 11-content-assets.md queries

Also check static files (00, 01, 02, 05, 08, 10) if the scan reveals significant changes.

For each search result, read the full thread to understand context.

### Step 4: Update Memory Bank Files
For each file that has new information:
1. Read the current file
2. Identify what's new since the last refresh date
3. Append new entries or update existing entries
4. Add `[Added YYYY-MM-DD]` date stamps to all new information
5. **Never delete existing entries** — only add or modify

### Step 5: Update Refresh Metadata
Write today's date to `~/Documents/Claude/PRISM/memory-bank/last-refresh.txt`

### Step 6: Write Refresh Log
Create a log at `~/Documents/Claude/PRISM/logs/YYYY-MM/memory-refresh-YYYYMMDD.md` with:
- Refresh summary (date range, messages scanned, files updated/unchanged)
- Changes made per file
- New insights discovered
- Dropped action items found

### Step 7: Update CONTEXT.md (if significant changes)
If more than 3 files were updated or a major event was discovered (new client, team change, financial event), regenerate `~/Documents/Claude/PRISM/CONTEXT.md` following the 10-section structure defined in its Meta section.

---

## Configuration Notes

- **Frequency:** Weekly (recommended: Mondays before Weekly Retrospective)
- **Account:** [your-email@your-agency.com] ONLY
- **Duration:** Typically 5-15 minutes depending on email volume
- **Trigger:** Can also be run manually by saying "refresh the memory bank"

---

## See Also
- [[memory-bank/INDEX|Memory Bank Index]]
- [[skills/PRISM-core|PRISM Core]]
- [[memory-bank/refresh-protocol|Refresh Protocol]]
- [[memory-bank/13-gmail-insights|Gmail Insights]]
- [[memory-bank/basecamp-scan-protocol|Basecamp Scan Protocol]]
- [[claude-code/daily-PRISM-sync|Daily PRISM Sync]]
