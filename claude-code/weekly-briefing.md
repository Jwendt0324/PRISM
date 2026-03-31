# Weekly Briefing Generator — Ready-to-Use Prompt

**Runs automatically every Monday via launchd. Can also be triggered manually.**

---

## Prompt

You are generating [Your Name]'s Weekly Briefing for the Claude PRISM. This briefing gives [Your Name] a clear picture of what happened, what's coming, and what needs attention — all in one read.

**IMPORTANT:** This task may run in unattended mode without Gmail/Calendar MCP access. Work with whatever tools are available. If Gmail is not accessible, generate the briefing from local data and note the limitation.

### Step 1: Load Context
Read these files (read all in parallel):
- `~/Documents/Claude/PRISM/CONTEXT.md`
- `~/Documents/Claude/PRISM/memory-bank/last-refresh.txt`
- `~/Documents/Claude/PRISM/memory-bank/04-client-directory.md`
- `~/Documents/Claude/PRISM/memory-bank/12-strategic-context.md`
- `~/Documents/Claude/PRISM/memory-bank/13-gmail-insights.md`
- `~/Documents/Claude/PRISM/memory-bank/10-financial-context.md`
- `~/Documents/Claude/PRISM/memory-bank/06-deal-history.md`
- `~/Documents/Claude/PRISM/memory-bank/15-basecamp-status.md` (may not exist — skip if missing)

### Step 2: Scan Session Logs
- Read all session logs from `~/Documents/Claude/PRISM/logs/` for the past 7 days
- Read any daily-sync logs from the past week for stale data warnings
- Check `~/Documents/Claude/PRISM/content-pipeline/` for draft content awaiting review

### Step 3: Try Gmail + Calendar (Skip If Unavailable)
- **If Gmail MCP is available:** Search [your-email@your-agency.com] for messages from the last 7 days. Read key threads.
- **If Calendar MCP is available:** Pull events for the coming week.
- **If neither is available:** Note "Gmail data as of [last-refresh.txt date]" and proceed with local data only. Do NOT error out.

### Step 4: Generate the Briefing

Output the briefing in this format:

```markdown
# Weekly Briefing — [Date]

## This Week's Numbers
- **Bluevine Balance:** $[amount] (as of last known)
- **Active Clients:** [count] ([list names])
- **Pipeline:** [count] prospects ([list names + stages])
- **Content Pieces in Draft:** [count]
- **Content Published This Week:** [count]

## What Happened Last Week
[3-5 bullet points of the most important things that happened, drawn from Gmail and session logs]

## What's Coming This Week
| Day | What | Who | Notes |
|-----|------|-----|-------|
| Mon | [meeting/task] | [people] | [context] |
| ... | ... | ... | ... |

## Client Health Check
| Client | Status | Last Activity | Needs Attention? |
|--------|--------|--------------|-----------------|
| [Client — Local Retail Business] | [status] | [date] | [yes/no + why] |
| ... | ... | ... | ... |

## Action Items (Overdue or At Risk)
- [ ] [Item] — [context, who owns it, when it was due]
- [ ] ...

## Dropped Balls to Pick Up
[Anything from Gmail insights or Basecamp that looks stalled or forgotten]

## [Your Mentor/Advisor] Watch
[Any directives, feedback, or strategic signals from [Your Mentor/Advisor] in the last 7 days. [Your Mentor/Advisor]'s messages often contain important strategy shifts disguised as casual feedback.]

## Decisions Needed
[Anything that requires [Your Name] to make a call this week]

## Content Pipeline Status
- **Ready to publish:** [list pieces]
- **Dollar-a-Day candidates:** [list pieces with recommended budget]
- **Next pipeline run needed:** [yes/no, what source content is waiting]
```

### Step 5: Save the Briefing
Save to `~/Documents/Claude/PRISM/logs/YYYY-MM/weekly-briefing-YYYYMMDD.md`

### Step 6: Email the Briefing to [Your Name]
After saving, email the briefing to [Your Name] using this Bash command (uses Apple Mail — no Gmail MCP needed):

```bash
BRIEFING_FILE="$HOME/Documents/Claude/PRISM/logs/$(date +%Y-%m)/weekly-briefing-$(date +%Y%m%d).md"
SUBJECT="Weekly Briefing — $(date +%Y-%m-%d)"
BODY=$(cat "$BRIEFING_FILE")

osascript -e "
tell application \"Mail\"
    set newMessage to make new outgoing message with properties {subject:\"$SUBJECT\", content:\"$BODY\", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:\"[your-email@your-agency.com]\"}
    end tell
    send newMessage
end tell
"
```

If the `osascript` command fails (Mail.app not configured), log the error but don't fail the task — the briefing is still saved to disk.

---

## Configuration

- **Frequency:** Mondays 8:17 AM (automated via launchd), also triggerable manually
- **Duration:** 3-8 minutes
- **Trigger:** Say "generate my weekly briefing" or "what's my week look like"
- **Dependencies:** Daily PRISM Sync should run first (6:27 AM) so local data is current
- **Email:** Sent to [your-email@your-agency.com] via Apple Mail

---

## See Also
- [[skills/weekly-maa-report|Weekly MAA Report]]
- [[memory-bank/12-strategic-context|Strategic Context]]
- [[_Dashboard|Dashboard]]
- [[memory-bank/04-client-directory|Client Directory]]
- [[memory-bank/15-basecamp-status|Basecamp Status]]
- [[memory-bank/10-financial-context|Financial Context]]
