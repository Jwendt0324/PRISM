---
description: Standard format for session logs written by Claude Code after each task
category: system
created: 2026-03-18
last_updated: 2026-03-21
version: 2.0
canon_compliance: 05-maa-framework.md
triangles: MAA
---

# Session Log Format

## Purpose
Create a consistent record of what Claude Code did in each session, enabling pattern recognition, learning capture, and future reference without needing to re-read chat history.

## Template

```markdown
---
date: YYYY-MM-DDTHH:MM:SSZ
session_id: [auto-captured]
cwd: [working directory]
category: [client-work | business-ops | file-management | dev | system]
message_count: N
user_messages: N
total_tool_uses: N
version: 2.0
---

# Session Log: [Task Name]

## Task Summary
1-2 sentences describing what was accomplished. Be specific — "Created 12 articles from [Client — Local Retail Business] transcripts" not "Did content work."

## Tool Usage Breakdown
[Auto-captured: tool name and count]

## Files Created
[Auto-captured: absolute paths of all files created]

## Files Modified
[Auto-captured: absolute paths of all files modified]

## Files Read
[Auto-captured: absolute paths of all files read]

## Commands Run
[Auto-captured: shell commands executed]

## What Was Learned
**THIS SECTION IS MANDATORY — NO STUBS, NO PLACEHOLDERS.**
If you cannot fill this in now, do not create the log file at all.

Minimum 2 learnings (3+ for sessions with 50+ messages or 20+ tool uses).

Format:
- **Discovery:** [What you found out]
- **Insight:** [Why it matters or how to use it]
- **Action:** [If a process change is needed, describe it here]

Example:
- **Discovery:** Bash tool has working directory reset between calls — must use absolute paths
- **Insight:** Relative paths cause "file not found" errors and are hard to debug
- **Action:** Updated SOP-creation-template to require absolute paths everywhere

## Related SOPs
- Used: `sops/file-management/file-organization-rules.md` (moved 8 screenshots)
- Consulted: `sops/client-work/intake-process.md` (validated new client structure)
- Should update: `sops/dev/git-workflow.md` (found edge case with merge conflicts)

## Time Estimate
~X hours (actual time spent)
- Research: X min
- Execution: X min
- Documentation: X min

---
```

## Guidelines

### Auto-Captured Sections (Files Created/Modified/Read, Commands Run, Tool Usage)
- These are generated automatically — include all absolute file paths
- Do NOT include raw terminal output, task notifications, or login banners in any section
- Task Summary must be a real summary, not a copy of the user's first message

### What Was Learned — THE COMPOUNDING ENGINE
- **This is the most valuable section.** It's what makes the Mainframe smarter over time.
- **NEVER write `[To be extracted during retrospective]` or any placeholder.** If you can't write learnings now, don't create the log.
- Include both tactical (how to do X) and strategic (why Y is important)
- Reference specific file paths or line numbers if relevant
- Learnings should trigger SOP updates — flag them in Related SOPs
- Ask yourself: "What would I do differently next time? What surprised me? What took longer than expected?"

### Related SOPs
- List every SOP consulted or used
- For "Should update" SOPs, briefly state why (e.g., "edge case not yet documented")
- For "Used" SOPs, note what part was useful

### Time Estimate
- Be realistic, not ambitious
- Include breakdown only if session took >1 hour
- Use this data to refine future time estimates

## When to Write

- **After every task** Claude Code completes
- **Even if the task took 10 minutes**—the log captures learning and pattern
- **Especially after problem-solving**—the learnings prevent future issues
- Store the log in: `~/Documents/Claude/Mainframe/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`

## Session Log Index

Maintain a master index at `~/Documents/Claude/Mainframe/logs/YYYY-MM/INDEX.md` that lists:
- Date
- Task name
- Category
- One-line summary
- Link to full log

This enables quick scanning of what's been done without opening each file.

## Quality Checks

- [ ] Frontmatter has date, category, message_count, total_tool_uses
- [ ] Task Summary is 1-2 specific sentences (not a copy of the user's prompt)
- [ ] Auto-captured sections (Files Created/Modified/Read, Commands Run) use absolute paths
- [ ] What Was Learned has 2+ real learnings (3+ for complex sessions) — NO PLACEHOLDERS
- [ ] Related SOPs section lists all consulted SOPs with update flags
- [ ] Time Estimate is present
- [ ] File saved to: `~/Documents/Claude/Mainframe/logs/YYYY-MM/session-YYYYMMDD-HHMMSS.md`
- [ ] Monthly INDEX.md updated
- [ ] No raw terminal output, task notifications, or login banners in any section

## Canon Compliance

- **Canon source:** 05-maa-framework.md
- **Triangles served:** MAA (learning measurement — every session log captures discoveries, insights, and actions that compound over time)
- **Human checkpoints:** Task summary reviewed for accuracy; learnings reviewed for SOP update candidates; related SOPs list verified for completeness
- **Anti-vandalism:** Structured format enforces completeness (date, category, summary, actions, learnings all required); index file maintains audit trail; time estimates enable drift detection; "What Was Learned" section is never empty
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)
