---
description: Meta-SOP for creating and updating Standard Operating Procedures in the Mainframe
category: system
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
canon_compliance: required-field
triangles: required-field
triangles_served: [list which of the 9 triangles — GCT, MAA, ACC, CCS, LDT, SBP, DDD, CID, MOF — this SOP serves]
human_gates: yes/no
canon_sources: [list of canon files this SOP derives from, e.g. 01-nine-triangles.md, 08-human-requirements.md]
---

# SOP Creation Template

## When to Create vs Update

**Create a new SOP when:**
- You notice a repeating task pattern without an SOP
- A process takes more than one session to complete
- Knowledge needs to be preserved for future use or delegation
- Multiple steps are required consistently

**Update an existing SOP when:**
- You discover a better approach than what's documented
- A step becomes obsolete or problematic
- You learn something that prevents common pitfalls
- The process changes due to tool updates or workflow shifts
- Version bump: increment minor version for improvements, major for fundamental changes

## SOP Structure (Required Sections)

Every SOP must include these sections in this order:

### Frontmatter
```yaml
---
description: One sentence describing what this SOP does
category: [client-work|business-ops|file-management|dev|system]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
version: X.Y
canon_compliance: [which blitzmetrics-canon files this SOP aligns with, e.g. 02-content-factory-process.md]
triangles: [which of the 9 Triangles this SOP maps to, e.g. MAA, CCS, GCT]
triangles_served: [list which of the 9 triangles — GCT, MAA, ACC, CCS, LDT, SBP, DDD, CID, MOF — this SOP serves]
human_gates: [yes/no — whether this SOP has human-required steps]
canon_sources: [list of canon files this SOP derives from, e.g. 01-nine-triangles.md, 08-human-requirements.md]
---
```

### 1. Purpose
One sentence. Why does this SOP exist? What problem does it solve?

### 2. When to Use
- Bullet points describing the conditions/signals that trigger this SOP
- Be specific: "When a client sends a Figma file" not "When you get files"

### 3. Process
Step-by-step numbered instructions. Each step should be:
- Actionable (start with a verb)
- Specific (include file paths, tool names, exact commands)
- Concise (one thought per step)

Use sub-steps (a, b, c) only when a parent step has multiple distinct actions.

### 4. Quality Checks
Verification steps before marking the task complete:
- What should be true after this SOP is executed?
- List 2-4 checkpoints
- Include any spot-checks or validations

### 5. Common Pitfalls
Things that go wrong and how to avoid them:
- Document real mistakes observed during execution
- Include the fix
- Be direct: "People forget X. Don't. Always check Y first."

### 6. Canon Compliance (Summary)
Map this SOP to the [Methodology Partner] canon:
- **Canon source:** Which blitzmetrics-canon files this SOP aligns with
- **Triangles served:** Which of the 9 Triangles (GCT, MAA, ACC, CCS, LDT, SBP, DDD, CID, MOF) with brief explanation
- **Human checkpoints:** Where humans are required in this process
- **Anti-vandalism:** Any anti-vandalism protections in this process
- **Last audited:** Date of last canon alignment audit

### 7. Human Gates
List every step in this SOP where a human must review, approve, or perform the action. Reference `~/Documents/Claude/Mainframe/blitzmetrics-canon/08-human-requirements.md` for guidance on which tasks require human involvement. Format as a table:

| Step | Gate Type (Review/Approve/Execute) | Reason |
|------|------------------------------------|--------|
| [Step number and name] | [Review, Approve, or Execute] | [Why a human is required — e.g., judgment call, client relationship, financial decision] |

If this SOP has NO human gates, state that explicitly and explain why full automation is safe.

### 8. Anti-Vandalism Checks
List the checks this SOP performs to prevent unintentional well-meaning vandalism. Reference `~/Documents/Claude/Mainframe/blitzmetrics-canon/10-anti-vandalism-checklist.md` for the full framework. At minimum, every SOP must address:

- **Check what already exists:** Before creating new content, articles, pages, or documents, search for existing material on the same topic. Enhance rather than duplicate.
- **Verify internal link structure:** Ensure no orphan pages are created and all new content links to and from related existing content.
- **Confirm no keyword cannibalization:** Check that new content does not target the same keywords as existing ranking pages.
- **Preserve what's working:** Do not remove processes or content that are currently producing results.
- **Reference canonical source:** Ensure all process descriptions match the [Methodology Partner] canon exactly — no approximations.

Add any SOP-specific anti-vandalism checks beyond these minimums.

### 9. Canon Compliance
Map this SOP to the [Methodology Partner] canon:

- **Content Factory stage(s):** Which of the 6 stages does this SOP cover? (Plumbing, Produce, Process, Post, Promote, Perform)
- **9 Triangles served:** Which triangles does this SOP serve? (GCT, MAA, ACC, CCS, LDT, SBP, DDD, CID, MOF) — explain why for each.
- **Canon documents (source of truth):** List the specific `blitzmetrics-canon/` files that govern this SOP's domain. These are the authoritative references. If the SOP ever contradicts these documents, the SOP is wrong.
- **Last canon audit:** Date this SOP was last verified against its canon sources.

### 10. Learnings Log
Living section for discoveries:
- Date what was learned
- Keep it concise
- Link to updated process steps if the learning led to a change

## Writing Style Requirements

- **Voice:** Direct, confident, real. Match [Your Name]'s tone: grounded, no fluff, actionable.
- **Tense:** Imperative (Use X, Check Y, Do Z)
- **Length:** Process section ideally 5-12 steps. Longer = break into sub-SOPs.
- **Specificity:** Always include file paths, exact commands, tool names. "Open the project file at ~/Documents/Projects/Acme/design-system/" not "Open the file."
- **Format:** Use backticks for file paths, command syntax, and exact inputs. Use **bold** for emphasis on critical words.

Example: "Navigate to **~/Documents/Claude/Mainframe/sops/** and open **INDEX.md**"

> **Path format rule:** All file paths in SOPs must be absolute, starting with `~/`. Never use session-specific or container paths.

## Skill Format Requirement

Every SOP is simultaneously:
1. A markdown document in the sops/ folder
2. A Claude skill (loadable with skill file)

This means:
- The file itself IS the skill (no separate .skill file needed)
- The frontmatter IS the skill metadata
- The markdown structure IS the skill content
- When loaded, Claude sees the full SOP as callable instructions

## Updating INDEX.md

When you create or update an SOP:

1. Open `~/Documents/Claude/Mainframe/sops/INDEX.md`
2. Add/update the entry in the relevant category section
3. Format: `- [SOP Name](./category/filename.md) — Brief description`
4. Keep entries alphabetical within each category
5. Update the "Last Updated" date at the top of INDEX.md
6. Version bump in INDEX.md frontmatter if structure changes

## Example SOP Header

```markdown
---
description: Organize files by type and client into proper folders
category: file-management
created: 2026-03-18
last_updated: 2026-03-18
version: 1.0
canon_compliance: [relevant canon file]
triangles: [relevant triangles]
triangles_served: [e.g. GCT, CCS, DDD]
human_gates: [yes/no]
canon_sources: [e.g. 01-nine-triangles.md, 02-content-factory-process.md]
---

# File Organization SOP

## Purpose
Ensure all files end up in the correct location based on type and context, reducing inbox clutter and enabling faster retrieval.

## When to Use
- Daily file organization task runs
- After a client project completes
- When desktop or Downloads folder exceeds acceptable file count
- Quarterly cleanup of archived materials
```

## Quick Checklist for SOP Creation

- [ ] Frontmatter complete with all fields
- [ ] Purpose is one sentence
- [ ] When to Use has specific triggers (not vague)
- [ ] Process has 5-12 numbered steps
- [ ] Each step starts with a verb and is actionable
- [ ] Quality Checks section has 2-4 verifiable checkpoints
- [ ] Common Pitfalls includes real gotchas observed
- [ ] Canon Compliance section complete (canon source, triangles, human checkpoints, anti-vandalism)
- [ ] Frontmatter includes canon_compliance, triangles, triangles_served, human_gates, and canon_sources fields
- [ ] Human Gates section lists all human-required steps (or states why none exist)
- [ ] Anti-Vandalism Checks section addresses all 5 minimum checks
- [ ] Canon Compliance section maps to Content Factory stages, 9 Triangles, and canon source docs
- [ ] Learnings Log started (even if empty initially)
- [ ] Writing style is direct, specific, no fluff
- [ ] File paths use backticks and are absolute
- [ ] INDEX.md updated with new/updated entry
- [ ] Filename matches category/hyphenated-sop-name.md pattern
