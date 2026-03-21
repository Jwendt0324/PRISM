# Weekly SOP Health Check — Automated Prompt

**Runs unattended via launchd every Friday.**

---

## Prompt

You are running the Weekly SOP Health Check for the Claude Mainframe. This ensures the SOP system stays healthy and identifies improvement opportunities from the week's work.

### Step 1: Read Session Logs from This Week

Read all session logs from `~/Documents/Claude/Mainframe/logs/` for the past 7 days. For each session, note:
- What SOPs were used (look for file paths containing `sops/`)
- What tasks were done that don't have SOPs
- Any errors or workarounds that suggest an SOP needs updating

### Step 2: Check SOP Freshness

Read `~/Documents/Claude/Mainframe/INDEX.md` and check the "Last Updated" column. Flag any SOPs that:
- Haven't been updated in 30+ days AND were used this week
- Are marked as "Superseded" but still appear in routing tables
- Have empty Learnings Logs despite being used multiple times

### Step 3: Check Skill-SOP Alignment

Read `~/Documents/Claude/Mainframe/skills/sop-router.md`. Verify:
- Every skill file referenced actually exists in `skills/`
- Every SOP referenced actually exists in `sops/`
- No broken paths

### Step 4: Identify New SOP Candidates

From the session logs, identify any task patterns that:
- Were performed 2+ times this week
- Don't have an existing SOP
- Would benefit from documentation

### Step 5: Write Health Report

Save to `~/Documents/Claude/Mainframe/logs/YYYY-MM/sop-health-YYYYMMDD.md`:

```markdown
---
date: YYYY-MM-DDTHH:MM:SSZ
category: system
task_type: sop-health-check
---

# SOP Health Check — YYYY-MM-DD

## SOPs Used This Week
- [list with usage count]

## SOPs Needing Updates
- [list with reason]

## Broken References
- [list or "None"]

## New SOP Candidates
- [task pattern] — performed [N] times, no SOP exists

## Learnings Logs Still Empty
- [list of SOPs with empty learnings logs that were used]
```

---

## Configuration
- **Frequency:** Fridays 7:07 AM
- **Duration:** 1-3 minutes
- **Gmail required:** NO
