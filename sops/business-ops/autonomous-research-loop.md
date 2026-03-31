---
description: Framework for running Ralph Loop and other autonomous research/improvement sessions with clear scope, stop conditions, and output expectations
category: business-ops
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/automation
canon_compliance: 02-content-factory-process.md
triangles: [LDT, DDD]
triangles_served: [LDT — autonomous learning loops embody Learn/Do/Teach, DDD — research produces data-driven recommendations]
human_gates: yes
canon_sources: [02-content-factory-process.md, 12-ldt-implementation-guide.md]
---

# Autonomous Research Loop (Ralph Loop) SOP

## Purpose
Define how to run autonomous, multi-iteration research and improvement sessions (Ralph Loop) that compound PRISM capabilities without manual supervision — including scope control, output standards, and stop conditions.

## When to Use
- [Your Name] triggers a Ralph Loop (`/ralph-loop` command)
- An overnight research task is scheduled
- System improvement work needs to run unattended
- A topic requires deep web research with implementation

## Process

1. **Define scope and constraints.** Before starting the loop, confirm:
   - **Research topic:** What specifically to research (e.g., "new Claude Code skills for SEO")
   - **Max iterations:** How many cycles to run (default: 50, but user may specify)
   - **Output type:** What to produce (skills, SOPs, reports, code)
   - **Boundaries:** What NOT to touch (e.g., "don't modify existing hooks")

2. **Load current state.** Read the relevant PRISM context:
   - `~/Documents/Claude/PRISM/CONTEXT.md` for system overview
   - `~/Documents/Claude/PRISM/INDEX.md` for current SOP/skill inventory
   - Any domain-specific files related to the research topic
   - `~/Documents/Claude/PRISM/claude-code/mcp-integrations-reference.md` for tool ecosystem

3. **Execute research cycles.** Each iteration follows:
   a. **Search** — Web search for new information, tools, techniques
   b. **Evaluate** — Assess relevance and quality of findings
   c. **Implement** — Create or update skills, SOPs, configs, or documentation
   d. **Log** — Record what was found and what was done
   e. **Check stop conditions** — Should the loop continue?

4. **Apply stop conditions.** Stop the loop when:
   - Max iterations reached
   - No new relevant findings in 3 consecutive cycles
   - User sends `/exit` or interrupts
   - A critical error or security concern is encountered
   - The research topic is exhausted

5. **Produce summary output.** At loop completion, create:
   - A research summary with all findings organized by topic
   - List of skills/SOPs created or updated (with file paths)
   - List of recommendations that need human decision
   - Next steps for future research loops

6. **Update PRISM.** After the loop:
   - Update INDEX.md if new SOPs/skills were created
   - Update CONTEXT.md if major capabilities were added
   - Write a session log entry documenting the loop's results

## Quality Checks
- [ ] All new skills follow the skill format requirements
- [ ] All new SOPs follow the SOP creation template
- [ ] No existing functionality was broken by changes
- [ ] Research summary is specific and actionable (not vague)
- [ ] Stop conditions were respected

## Common Pitfalls
- **Scope creep.** Ralph Loops can drift from the original topic. Check the original scope definition at each iteration. If the loop discovers something interesting but off-topic, note it for a future loop — don't chase it now.
- **Plugin/command failures.** Sessions 091d3785 and d731a504 both encountered Ralph Loop plugin shell command errors. If the loop mechanism fails, fall back to manual task-based iteration rather than retrying endlessly.
- **Overwriting good work.** Research sessions can overwrite existing skills or configs that are already working well. Always check what exists before creating new files. Prefer updating over replacing.
- **Skill bloat.** Session 6cda0712 installed 22 new skills in one session. More skills isn't always better — each one adds context loading overhead. Prioritize quality and relevance over quantity.
- **Missing documentation.** The loop produces artifacts but sometimes skips updating INDEX.md and CONTEXT.md. Step 6 is mandatory, not optional.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| Step 1 — Scope definition | Approve | [Your Name] defines what to research and sets boundaries |
| Step 5 — Summary review | Review | [Your Name] should review findings and decide which recommendations to act on |

## Anti-Vandalism Checks
- **Check what already exists:** Before creating new skills or SOPs, search for existing ones covering the same territory. Enhance rather than duplicate.
- **Preserve what's working:** Never remove or replace a skill/SOP that's currently in use and working correctly.
- **Reference canonical source:** All new skills must align with [Methodology Partner] canon where applicable.

## Canon Compliance
- **Content Factory stage(s):** Plumbing (infrastructure improvement), Process (creating reusable knowledge)
- **9 Triangles served:** LDT (Learn/Do/Teach — the loop embodies continuous learning), DDD (Data-Driven Decisions — research produces evidence-based recommendations)
- **Canon documents:** `02-content-factory-process.md`, `12-ldt-implementation-guide.md`
- **Last canon audit:** 2026-03-30

## See Also

- [[memory-bank/12-strategic-context|Strategic Context]]
- [[memory-bank/01-hri-overview|[Your Agency] Overview]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory Process]]
- [[blitzmetrics-canon/12-ldt-implementation-guide|LDT Implementation Guide]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]

## Learnings Log
- **2026-03-30:** Created from analysis of 4 Ralph Loop sessions this week (6cda0712, 021213dc, 091d3785, d731a504). Average session installed 10+ new artifacts. Key finding: loops need explicit scope boundaries to prevent drift and bloat.
- **2026-03-30:** Plugin errors caused Ralph Loop failures in sessions 091d3785 and d731a504. Workaround: switch to manual task-based iteration when the loop mechanism breaks.
- **2026-03-30:** Session 6cda0712 discovered that skills should be preferred over commands for reusable behaviors. Commands are one-shot; skills compound.