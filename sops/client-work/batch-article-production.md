---
description: End-to-end batch production of articles from transcripts using sub-agents, QA enforcement, and DOCX delivery
category: client-work
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
canon_compliance: 02-content-factory-process.md, 03-article-guidelines.md
triangles: [CCS, MAA, ACC]
triangles_served: [CCS — produces client-facing content at scale, MAA — enables metric tracking of content output, ACC — article production supports authority content creation]
human_gates: yes
canon_sources: [02-content-factory-process.md, 03-article-guidelines.md, 07-quality-standards.md, 08-human-requirements.md]
tags:
  - type/sop
  - status/active
  - domain/client-work
  - topic/batch-production
  - topic/article-writing
---

# Batch Article Production SOP

## Purpose
Produce multiple articles from transcripts in a single session with consistent quality, parallel sub-agent execution, and automated DOCX conversion — enabling high-volume content delivery as part of the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] pipeline for clients like [Client — Local Retail Business].

## When to Use
- A client has 3+ transcripts ready for article writing
- A batch delivery is due (e.g., weekly content cycle)
- Ralph Loop or overnight task triggers batch article production
- Content pipeline shows backlog of unprocessed transcripts

## Process

1. **Inventory available transcripts.** List all transcript files in the client's transcript folder (e.g., `~/Documents/Claude/PRISM/content-pipeline/<client>/transcripts/`). Count total, identify which have already been processed by checking the articles output folder.

2. **Load all relevant SOPs and guidelines.** Before writing anything, read:
   - `~/Documents/Claude/PRISM/sops/client-work/article-writing-from-transcripts.md`
   - `~/Documents/Claude/PRISM/sops/client-work/article-qa-blitzmetrics.md`
   - `~/Documents/Claude/PRISM/blitzmetrics-canon/03-article-guidelines.md`
   - `~/Documents/Claude/PRISM/blitzmetrics-canon/07-quality-standards.md`
   - Any client-specific good examples in the content pipeline folder

3. **Plan the batch.** Create a numbered list of articles to write. For each: transcript filename, proposed article title, and estimated topic/keyword focus. This becomes the tracking checklist.

4. **Write articles using sub-agents.** Launch one sub-agent per article for parallel execution. Each sub-agent must:
   - Read the transcript
   - Follow the article-writing SOP strictly
   - Apply the [[skills/article-qa|18-step QA checklist]]
   - Output a single markdown file with proper naming: `<client>-<topic-slug>.md`

   **Critical:** Pass the full SOP text to each sub-agent. Do not assume sub-agents have access to PRISM skills — they don't unless explicitly given the content.

5. **Run QA audit on all articles.** After sub-agents complete, run a consolidated QA pass:
   - Check each article against the 18-step [Methodology Partner] article QA checklist
   - Verify no duplicate topics or keyword cannibalization across the batch
   - Flag articles that need rewrite and re-run those specific sub-agents

6. **Fix flagged articles.** Rewrite any articles that failed QA. Do not skip — every article must pass all 18 checks before proceeding.

7. **Convert to DOCX.** Use the batch converter script:
   ```bash
   cd ~/Documents/Claude/PRISM/content-pipeline/<client>/articles/
   python3 ~/Documents/Claude/PRISM/scripts/batch-md-to-docx.py *.md
   ```
   If the batch converter doesn't exist, create it using python-docx. The script should:
   - Convert all .md files in the current directory to .docx
   - Preserve headings, bold, lists, and links
   - Output to a `docx/` subfolder

8. **Deliver.** Move completed DOCX files to the client's delivery folder or Google Drive. Log the delivery in the session log with article count and titles.

## Quality Checks
- [ ] Every article passes the 18-step [Methodology Partner] QA checklist
- [ ] No two articles in the batch target the same primary keyword
- [ ] All DOCX files open correctly and preserve formatting
- [ ] Session log records the full batch: articles written, QA results, delivery location

## Common Pitfalls
- **Sub-agents ignoring SOPs.** Discovered in session 7387455e: sub-agents were not following PRISM SOPs because the guidelines weren't passed to them. Always include the full SOP text in the sub-agent prompt — don't rely on file paths.
- **Duplicate/skipped articles.** Same session found agents skipping articles or creating duplicates. Always cross-reference the tracking checklist after all sub-agents complete. Delete duplicates before proceeding.
- **DOCX conversion failures.** Ensure python-docx is installed (`pip install python-docx --break-system-packages`). Test the converter on one file before batch-running.
- **Keyword cannibalization.** When writing 5+ articles for the same client/topic area, it's easy for articles to overlap. Step 5 explicitly checks for this — don't skip it.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| Step 3 — Batch planning | Review | [Your Name] or client should confirm article topics before production |
| Step 8 — Delivery | Approve | Human reviews final articles before sending to client |

## Anti-Vandalism Checks
- **Check what already exists:** Before writing, search for existing articles on the same topics in the client's folder. Enhance rather than duplicate.
- **Verify internal link structure:** Not applicable for external client articles, but ensure articles reference each other where relevant.
- **Confirm no keyword cannibalization:** Step 5 explicitly checks this across the batch AND against previously published articles.
- **Preserve what's working:** If a client has existing articles performing well, don't create competing articles on the same topics.
- **Reference canonical source:** All articles must comply with `03-article-guidelines.md` and pass the 18-step QA checklist.

## Canon Compliance
- **Content Factory stage(s):** Process (turning transcripts into publishable articles)
- **9 Triangles served:** CCS (content at scale for clients), MAA (trackable deliverables), ACC (authority content for client brands)
- **Canon documents:** `02-content-factory-process.md`, `03-article-guidelines.md`, `07-quality-standards.md`, `08-human-requirements.md`
- **Last canon audit:** 2026-03-30

## Learnings Log
- **2026-03-30:** Created from session 7387455e ([Client — Local Retail Business] batch). 5 articles written from transcripts. Key finding: sub-agents must receive full SOP text inline — they cannot load skills autonomously. Articles that failed QA were rewritten successfully on second pass.
- **2026-03-30:** Python batch converter (markdown → DOCX) was created on the fly in session 7387455e. This should be a permanent script in `~/Documents/Claude/PRISM/scripts/`.
- **2026-03-30:** Session 0260c031 showed 43 iterations of the KP book through edit cycles with changelog tracking. While that was a single-document refinement (not batch), the version-controlled iteration pattern could be applied to batch QA cycles.

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/07-quality-standards|Quality Standards]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[skills/article-writer|Article Writer]]
- [[skills/article-qa|Article QA]]
- [[skills/content-factory|Content Factory Skill]]