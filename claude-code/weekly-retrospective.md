# Weekly Retrospective — Master Friday Workflow

**Trigger:** Say "run the weekly review" or "Friday retrospective"
**Duration:** 15-30 minutes
**When:** Fridays (or whenever {{USER_NAME}} wants to review the week)

This is the master workflow that combines everything into one session. It reads all conversations from the week, extracts everything important, generates the MAA report, updates SOPs, and produces a comprehensive weekly review. Nothing gets deleted — everything is archived and referenced.

---

## Prompt

You are running the Weekly Retrospective for the Claude PRISM. This is the most important recurring task — it closes the learning loop by turning raw conversation logs into structured knowledge.

**CRITICAL RULE: Never delete, overwrite, or modify any source files (conversations, session logs, action logs). You are READING from them and WRITING new summary files. Source data is sacred.**

---

### Phase 1: Gather Everything (Read Only)

Read all of these in parallel:

**Context:**
- `~/Documents/Claude/PRISM/CONTEXT.md`
- `~/Documents/Claude/PRISM/memory-bank/04-client-directory.md`
- `~/Documents/Claude/PRISM/memory-bank/10-financial-context.md`
- `~/Documents/Claude/PRISM/memory-bank/12-strategic-context.md`

**This week's conversations (THE MAIN SOURCE):**
- Read every file in `~/Documents/Claude/PRISM/logs/conversations/YYYY-MM/` with a modification date in the last 7 days
- These are the full readable conversations between {{USER_NAME}} and Claude
- Read ALL of them — do not skip any, do not skim

**This week's session logs:**
- Read every file in `~/Documents/Claude/PRISM/logs/sessions/YYYY-MM/` from the last 7 days
- These have structured data: tool usage, files created/modified, commands run

**This week's manual session logs:**
- Read every file in `~/Documents/Claude/PRISM/logs/YYYY-MM/session-*.md` from the last 7 days

**Action logs:**
- Read `~/Documents/Claude/PRISM/logs/actions/YYYY-MM-DD.jsonl` for each day this week
- Count total tool calls, most-used tools, most-touched files

**Previous retrospective (if exists):**
- Check for last week's retrospective in `~/Documents/Claude/PRISM/logs/YYYY-MM/weekly-retrospective-*.md`
- Compare: were last week's action items completed?

---

### Phase 2: Classify & Extract from Conversations

**STEP 2A — CLASSIFY EACH CONVERSATION**

Before extracting anything, classify each conversation into one of two categories:

**OPERATIONAL** — Technical work, client deliverables, tool building, SOP creation, content production, system improvements. These are safe to reference in SOPs, memory bank, and shared files.

**CONFIDENTIAL** — Personal strategy discussions, relationship dynamics ([Your Mentor/Advisor], partners, mentors), financial negotiations, equity/compensation discussions, emotional processing, business positioning that {{USER_NAME}} wouldn't want visible to team members or partners.

**How to identify CONFIDENTIAL conversations:**
- Discusses interpersonal dynamics with [Your Mentor/Advisor], [Your Ops Partner], or other partners by name
- Contains financial analysis of the [Your Agency]/[Methodology Partner] relationship or power dynamics
- Discusses {{USER_NAME}}'s personal strategy for independence, separation, or leverage
- Contains candid assessments of other people's behavior or motivations
- Discusses equity splits, compensation negotiations, or deal structures
- {{USER_NAME}} explicitly says something is private, off the record, or confidential
- Contains draft emails or messages that haven't been sent yet

**CONFIDENTIAL conversations get different treatment:**
- Extract action items and decisions → put in the retrospective (these are {{USER_NAME}}'s eyes only)
- Extract process improvements → can become SOPs IF the source context is stripped
- NEVER quote {{USER_NAME}} directly from confidential conversations in any shared file
- NEVER reference relationship dynamics in SOPs, memory bank, or any file that could be shared
- NEVER include confidential insights in the GitHub repo version of anything
- The retrospective file itself lives in `logs/` which is gitignored — it's safe there

**STEP 2B — EXTRACT FROM EACH CONVERSATION**

For OPERATIONAL conversations, extract everything freely:

1. **Decisions Made** — Include exact quotes and context.

2. **Action Items Committed** — Track completion by checking later conversations.

3. **Key Insights & Realizations** — Non-obvious findings worth remembering.

4. **Problems Discovered** — Bugs, broken processes, client issues.

5. **New Projects or Ideas** — New initiatives that emerged.

6. **SOP Gaps Identified** — Processes that should be documented but aren't.

For CONFIDENTIAL conversations, extract only:

1. **Decisions Made** — Summarize the decision without the personal context that led to it. "Decided to form separate LLC for appliance repair business" — not "Decided to form separate LLC because [Your Mentor/Advisor]'s control is unsustainable."

2. **Action Items** — What needs to happen, stripped of interpersonal reasoning.

3. **Process Improvements** — If a confidential conversation revealed a better way to do something, the process improvement can become an SOP. The reasoning stays private.

4. **Financial Decisions** — Track decisions but not the negotiation dynamics behind them.

**NEVER extract from confidential conversations:**
- Relationship assessments or interpersonal analysis
- Direct quotes about other people's behavior or motivations
- {{USER_NAME}}'s strategic positioning relative to partners
- Emotional context or personal processing

---

### Phase 3: Generate the Weekly Review

Write to `~/Documents/Claude/PRISM/logs/YYYY-MM/weekly-retrospective-YYYYMMDD.md`:

```markdown
---
date: YYYY-MM-DDTHH:MM:SSZ
category: system
task_type: weekly-retrospective
week_of: YYYY-MM-DD
conversations_reviewed: [count]
sessions_reviewed: [count]
total_tool_calls: [count]
version: 1.0
---

# Weekly Retrospective — Week of [Date]

## Executive Summary
[3-5 sentences: What was the most important thing that happened this week? What changed? What's different now than 7 days ago?]

## Conversations Reviewed
| File | Date | Messages | Topic |
|------|------|----------|-------|
| conversation-XXXX.md | Mon | 45 | [Your Mentor/Advisor] P&L discussion |
| ... | ... | ... | ... |

## Decisions Made This Week
| Decision | Context | Conversation | Status |
|----------|---------|--------------|--------|
| "Build parts agent as separate LLC" | [Client Contact] deal, separate from [Your Agency] | conversation-XXXX.md | In progress |
| ... | ... | ... | ... |

## Action Items Tracker
| Action Item | Committed In | Owner | Deadline | Status |
|-------------|-------------|-------|----------|--------|
| Sign agreement with [Client Contact] | conversation-XXXX.md | {{USER_NAME}} | This week | Not done |
| Reply to [Your Mentor/Advisor]'s 7 threads | conversation-XXXX.md | {{USER_NAME}} | Today | Not done |
| ... | ... | ... | ... | ... |

### Carried Over from Last Week
[Check previous retrospective — what was committed but not completed?]

## Key Insights
1. **[Insight title]** — [Exact finding with context]. Source: conversation-XXXX.md
2. ...

## Projects Status
| Project | Status | Key Movement This Week | Next Step |
|---------|--------|----------------------|-----------|
| Parts Agent ([Client-ID]) | Building | Tested 10/10 on [Parts Distributor], server data extracted | Deploy to Vultr |
| [Your Agency] Content | Maintaining | 378 articles [Client — Local Retail Business], 54 [Client Name] | Publish [Client Initials] articles |
| ... | ... | ... | ... |

## Financial Summary
- Revenue received this week: $[amount]
- Expenses this week: $[amount]
- Key financial decisions: [list]
- Outstanding invoices: [list]

## Relationship Health
| Person | Status | Notable Events | Action Needed |
|--------|--------|----------------|---------------|
| [Your Mentor/Advisor] | Tense | 7 unanswered threads, P&L pressure | Reply to all threads |
| [Client Contact] | Strong | Deal in progress, data extracted | Get agreement signed |
| ... | ... | ... | ... |

## Problems & Risks
1. **[Problem]** — [Impact] — [Proposed solution]
2. ...

## Content & Deliverables Produced
- [List everything created this week with file paths]

## SOP Updates Needed
| SOP | What Changed | Priority |
|-----|-------------|----------|
| [SOP name] | [Why it needs updating] | High/Med/Low |

## New SOP Candidates
| Process | Times Done This Week | Why It Needs an SOP |
|---------|---------------------|-------------------|
| [process] | [count] | [reason] |

## Tool Usage Stats
- Total tool calls: [number]
- Most used: [tool]: [count], [tool]: [count]
- Files most touched: [file]: [count]
- Sessions: [count] total, [count] non-trivial

## What to Focus on Next Week
1. [Priority 1 — why]
2. [Priority 2 — why]
3. [Priority 3 — why]
```

---

### Phase 4: Update Memory Bank

Based on what you extracted, update these memory files if the information has changed:

- `memory-bank/04-client-directory.md` — new clients, status changes
- `memory-bank/06-deal-history.md` — new deals, price changes
- `memory-bank/10-financial-context.md` — revenue, expenses, payments
- `memory-bank/12-strategic-context.md` — strategy shifts, new priorities
- `memory-bank/last-refresh.txt` — update timestamp

**Rules for memory updates:**
- ADD new information, don't remove old information
- If something changed, note the old value and new value with date
- If a memory file is getting too long, summarize old sections but keep the data accessible
- Never delete financial records or relationship notes

---

### Phase 5: Update SOPs

For each SOP gap identified:
- If an existing SOP needs updating: update it, bump version, note what changed in learnings log
- If a new SOP is needed: create it using `sops/templates/sop-creation-template.md`
- Update `INDEX.md` with any changes

---

### Phase 6: Generate MAA Report

Using the data from the retrospective, generate the weekly MAA report for each active client following the format in `skills/weekly-maa-report.md`. Save each to:

`~/Documents/Claude/PRISM/logs/YYYY-MM/maa-[client-name]-YYYYMMDD.md`

---

### Phase 7: Summary to {{USER_NAME}}

After everything is written, give {{USER_NAME}} a verbal summary:
- "Here's what you accomplished this week" (wins)
- "Here's what fell through the cracks" (missed items)
- "Here's what I recommend focusing on next week" (priorities)
- "I updated these SOPs and memory files" (system improvements)

---

## Data Flow Diagram

```
Conversations (source, never modified)
    ↓ READ
Session Logs (source, never modified)
    ↓ READ
Action Logs (source, never modified)
    ↓ READ
    ↓
[Weekly Retrospective] ← NEW FILE (written to logs/)
    ↓
[Memory Bank Updates] ← APPEND ONLY (add new info, never delete)
    ↓
[SOP Updates] ← VERSION BUMPED (old content preserved in version history)
    ↓
[MAA Reports] ← NEW FILES (one per client, written to logs/)
```

**Nothing gets deleted. Everything is additive. Source data is sacred.**

---

## Configuration
- **Frequency:** Fridays (or on demand)
- **Duration:** 15-30 minutes
- **Gmail required:** Optional (helps with relationship tracking)
- **Trigger phrase:** "run the weekly review" or "Friday retrospective"
- **Dependencies:** Conversation exports must exist (auto-generated by SessionEnd hook)

---

## See Also
- [[skills/PRISM-core|PRISM Core]]
- [[_Dashboard|Dashboard]]
- [[memory-bank/12-strategic-context|Strategic Context]]
- [[memory-bank/09-project-history|Project History]]
- [[claude-code/weekly-briefing|Weekly Briefing]]
- [[claude-code/weekly-sop-health-check|SOP Health Check]]
