---
description: Run a comprehensive overnight strategic analysis of the entire business across 8+ dimensions
category: business-ops
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/strategy
canon_compliance: 05-maa-framework.md, 08-human-requirements.md
triangles: MAA, CID, MOF, DDD
triangles_served: [MAA, CID, MOF, DDD]
human_gates: yes
canon_sources: [05-maa-framework.md, 08-human-requirements.md, 10-anti-vandalism-checklist.md]
---

# Deep Dream -- Overnight Strategic Analysis SOP

## Purpose
Produce a comprehensive, brutally honest business analysis ([[memory-bank/01-hri-overview|[Your Agency] Overview]]) [Your Name] can wake up to -- covering revenue, relationships, content delivery, systems, opportunities, threats, and a weekly action plan -- using real data from all available sources.

## When to Use
- Sunday night before a big week (especially pre-travel)
- After 7+ days without a weekly review
- When [Your Name] says "run the dream" or `/dream`
- Quarterly deep dives or whenever strategic clarity is needed
- When multiple dimensions feel unclear simultaneously (revenue + clients + pipeline)

## Process

### Phase 1: Context Loading (5 min)
1. Read `~/Documents/Claude/PRISM/CONTEXT.md` for compressed business state.
2. Read ALL files in `~/Documents/Claude/PRISM/memory-bank/` (14-16 files).
3. Read last 7 days of session logs from `~/Documents/Claude/PRISM/logs/sessions/`.
4. Read last 7 days of conversation logs from `~/Documents/Claude/PRISM/logs/conversations/`.
5. Read any existing reports from `~/Documents/Claude/PRISM/logs/reports/`.
6. Check `memory-bank/last-refresh.txt` for staleness.

### Phase 2: 8-Mode Analysis (bulk of work)
Execute each mode sequentially, saving a report after each:

7. **Mode 1 -- Business Health Scan:** Revenue/MRR, client health scorecard (GREEN/YELLOW/RED for each), pipeline status, parts agent deal status, cash flow projection. Save to `dream-business-health-{date}.md`.

8. **Mode 2 -- Relationship Audit:** [Your Mentor/Advisor] (undelivered commitments, temperature), [Your Ops Partner], [Client Contact]/[Client-ID], each client (last contact, neglect risk), team (blocked?), prospects (cold?). Save to `dream-relationships-{date}.md`.

9. **Mode 3 -- Content & Delivery Audit:** Promised vs delivered per client, unpublished content, book progress, content gaps (personal brand, clients), Content Factory stage analysis (which stages are weak). Save to `dream-content-audit-{date}.md`.

10. **Mode 4 -- PRISM System Audit:** Hook health, memory bank staleness, SOP usage, skill router gaps, security (credentials, exposed data), CONTEXT.md accuracy, session learnings debt. Save to `dream-system-audit-{date}.md`.

11. **Mode 5 -- Opportunity Brainstorm:** CEO-level thinking. New revenue streams, upsells, scaling plays, event leverage, partnership optimization, personal brand closing gap. Every opportunity gets a specific action. Save to `dream-opportunities-{date}.md`.

12. **Mode 6 -- Threat Assessment:** 30/60/90 day threats ranked by probability and impact. Client churn, relationship regression, cash flow, deal failure, team gaps, technology risk. Save to `dream-threats-{date}.md`.

13. **Mode 7 -- Weekly Plan:** Top 5 priorities (revenue-ranked), top 3 fires, top 3 opportunities, daily plan Mon-Fri, what to say NO to. Save to `dream-weekly-plan-{date}.md`.

14. **Mode 8 -- Implement Fixes:** Update stale memory bank files, fix CONTEXT.md inaccuracies, draft replies for unanswered threads (save to `~/Desktop/DRAFT-*.md`), update client directory, populate empty tracker files.

### Phase 3: Cross-Reference (iterations 2+)
15. Scan conversation logs for data that contradicts or enriches Mode 1-8 findings. Key searches: financial data, prospect outcomes, deal status, pricing info.
16. Use **Basecamp MCP** to pull live project data: `basecamp_list_projects`, `basecamp_list_messages`, `basecamp_search`. Compare against memory bank assumptions.
17. Write correction report with every finding that changes a prior assessment. Save to `dream-deep-dive-{date}.md`.

### Phase 4: Deliverables
18. Generate **Master Brief** with 9 sections: Executive Summary (5 sentences), Fires, Opportunities, Client Scorecard, Relationship Status, Revenue Snapshot, Weekly Plan, Overnight Fixes, Long-Term Notes. Save to `dream-master-{date}.md`.
19. Generate **Action Checklist** with daily checkboxes Mon-Fri. Save to `~/Desktop/DREAM-ACTION-CHECKLIST-{date}.md`.
20. Draft any urgent replies (e.g., cooling prospects). Save to `~/Desktop/DRAFT-*.md`.
21. Create a **Pipeline Tracker** if none exists. Save to `dream-pipeline-tracker-{date}.md`.

### Phase 5: Package & Deliver
22. Create folder `~/Documents/Claude/PRISM/logs/reports/dream-{date}/`.
23. Move all dream reports into the folder.
24. Create `INDEX.md` in the folder with navigation table and top 10 discoveries.
25. Consolidate all reports into a single `.docx` using python-docx (title page, section per report, tables formatted).
26. Copy `.docx` to Google Drive: `~/Library/CloudStorage/GoogleDrive-[your-email@your-agency.com]/My Drive/`.
27. Open the file for [Your Name]: `open "{path_to_docx}"`.

## Quality Checks
- [ ] Every client has a GREEN/YELLOW/RED health rating with specific reasoning
- [ ] Every finding has a SPECIFIC action attached (not vague advice)
- [ ] Revenue numbers cite sources (Stripe confirmation dates, memory bank entries)
- [ ] Data gaps are explicitly called out ("NO DATA" not assumptions)
- [ ] Master brief fits on ~2 printed pages
- [ ] Action checklist has checkboxes and daily grouping
- [ ] At least one iteration of cross-referencing was done (conversation logs or Basecamp live data)

## Common Pitfalls
- **Assuming revenue is recurring.** Always verify one-time vs recurring. AI Apprentice enrollments are one-time at [$Price].
- **Not checking Basecamp live data.** Memory bank files can be 10+ days stale. The Basecamp MCP gives real-time truth. Use `basecamp_list_projects` and `basecamp_list_messages`.
- **Treating all Basecamp projects as [Your Agency] clients.** Many are [Methodology Partner]/[Partner Platform] clients (Prosperity Thinkers, ChurchCandy, etc.). Check project creation dates and who is active on them.
- **Missing conversation log data.** Conversation logs contain discovery call outcomes, payment confirmations, and deal updates that never made it to the memory bank.
- **Forgetting to update the master brief with corrections.** Each iteration should update the master brief, not just add a new report.
- **Making the reports too long for [Your Name] to read.** Lead with the action checklist and master brief. Everything else is supporting detail.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| Review Master Brief | Review | [Your Name] must read and prioritize -- the Dream suggests, [Your Name] decides |
| Send draft replies | Approve | Emails go out under [Your Name]'s name -- tone and content must be verified |
| Verify financial data | Execute | Only [Your Name] can log into Stripe to confirm payment attribution |
| Act on relationship findings | Execute | Client and partner relationships require human judgment |

## Anti-Vandalism Checks
- **Check what already exists:** Before writing a new dream report, check if one exists for the same date. Append or update, don't duplicate.
- **Preserve working data:** Do NOT overwrite memory bank entries that are correct. Only update stale or incorrect data.
- **Reference canonical source:** Financial figures must cite source (Stripe confirmation, Gmail thread, conversation log). Never assume.
- **Verify before correcting:** If a finding contradicts the memory bank, verify with a second source before updating.
- **Don't touch client-facing systems:** Dream analysis is internal only. Never post to Basecamp, send emails, or modify client files.

## Canon Compliance
- **Content Factory stage(s):** Perform (MAA reporting cycle -- analyzing what happened and what to do next)
- **9 Triangles served:**
  - **MAA** -- The entire Dream is Metrics (real data), Analysis (what it means), Action (what to do)
  - **CID** -- Communicate findings, Iterate on corrections, Delegate via action checklist
  - **MOF** -- Covers Marketing (content/brand gaps), Operations (system health), Finance (revenue/cash flow)
  - **DDD** -- Identifies what to Do this week, what to Delegate to [Your Content Specialist], what to Delete (say NO to)
- **Canon documents:** `05-maa-framework.md` (MAA structure), `08-human-requirements.md` (human gates), `10-anti-vandalism-checklist.md` (data protection)
- **Last canon audit:** 2026-03-30

## Learnings Log
- **2026-03-30:** First run. Key discovery: Basecamp MCP provides dramatically better data than memory bank alone. Always use it. Also: conversation logs contain payment/deal data that memory bank misses -- cross-reference is essential, not optional. File consolidation into .docx + Google Drive is the right delivery format for [Your Name].
- **2026-03-30 (retro):** Session d7497497 completed a full Dream run producing 14 reports and creating 15 scheduled tasks for action items. Key additions: (1) Creating scheduled tasks directly from Dream findings is high-leverage — converts insight into accountability. Add this as a standard Phase 4 step. (2) The Dream session used 137 tool calls across 401 messages — this is a heavy session. Consider breaking into smaller focused runs if context window becomes an issue. (3) Two Dream sessions ran on the same day (4f6ae3b5 and d7497497) — the second was more thorough because it had conversation context from the first. Running Dream as a 2-pass process (quick scan → deep dive) may be more effective than one long run.

---

## See Also

- [[memory-bank/10-financial-context|Financial Context]]
- [[memory-bank/01-hri-overview|[Your Agency] Overview]]
- [[memory-bank/12-strategic-context|Strategic Context]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]