# Overnight Task: PRISM Upgrade — Memory Refresh + Content Pipeline + Search Index

## Instructions for Claude Code

Copy everything below the line into Claude Code and let it run overnight.

---

You are running three major upgrades to [Your Name]'s Claude PRISM in a single overnight session. Complete them in order — each one builds on the last.

**CRITICAL: Only scan the Gmail account [your-email@your-agency.com]. Do NOT access, read, or search any other Gmail account.**

## Step 0: Load the PRISM

Read these files first to understand the current system:
- ~/Documents/Claude/PRISM/INDEX.md
- ~/Documents/Claude/PRISM/memory-bank/INDEX.md
- ~/Documents/Claude/PRISM/claude-code/CLAUDE.md
- ~/Documents/Claude/PRISM/sops/templates/sop-creation-template.md

---

# UPGRADE 1: MEMORY BANK AUTO-REFRESH SYSTEM

The memory bank was built once on March 18, 2026 from a full Gmail scan. It needs a system that keeps it current automatically. You will build the refresh infrastructure AND run the first refresh right now.

## 1A: Build the Refresh Script

Create ~/Documents/Claude/PRISM/memory-bank/refresh-protocol.md — an SOP that defines exactly how the memory bank gets refreshed:

### What Gets Refreshed
For each memory bank file, define what "refresh" means:

**04-client-directory.md** — Scan Gmail for new client conversations since the last refresh date (stored in memory-bank/last-refresh.txt). Add new clients, update status of existing ones (active → completed, prospect → active, etc.), add new deal terms or scope changes.

**03-team-directory.md** — Scan for new team members, role changes, comp discussions, new contractors or VAs mentioned. Update contact info, availability patterns, and relationship dynamics.

**06-deal-history.md** — Scan for new proposals sent, deals closed, payments received, invoices mentioned. Add to chronological deal record.

**07-relationship-map.md** — Scan for new introductions, referrals, partnership discussions, conference connections. Update relationship health indicators.

**12-strategic-context.md** — Scan for strategy discussions, pivot conversations, new priorities, decision outcomes. This is the most important file to keep current — it drives what Claude focuses on.

**13-gmail-insights.md** — Scan for new patterns: email volume trends, response time changes, new frequent contacts, unresolved threads.

**09-project-history.md** — Scan for project completions, new project starts, milestone updates.

**11-content-assets.md** — Scan for newly published content, podcast episodes, speaking engagements, press mentions.

### What Stays Static (refresh only if major changes detected)
- 00-[your-username].md — Only update if new personal milestones found
- 01-hri-overview.md — Only update if structural changes (new products, pricing changes)
- 02-blitzmetrics-overview.md — Only update if relationship changes
- 05-vendor-and-partner-map.md — Only update if new tools or vendor changes
- 08-communication-patterns.md — Only update if patterns shift significantly
- 10-financial-context.md — Only update if new financial data found

### Refresh Process
1. Read last-refresh.txt for the date of the last refresh
2. Search Gmail for messages after that date across all the search categories
3. For each memory bank file that needs updating:
   - Read the current file
   - Identify what's new since last refresh
   - Append new entries or update existing entries (never delete — only add or modify)
   - Bump the "Last Updated" date in the file
4. Write the current date to last-refresh.txt
5. Write a refresh log to ~/Documents/Claude/PRISM/logs/YYYY-MM/memory-refresh-YYYYMMDD.md

## 1B: Run the First Refresh Now

Even though the memory bank was just built today, run the refresh protocol as a test:
1. Write today's date to ~/Documents/Claude/PRISM/memory-bank/last-refresh.txt
2. Scan Gmail for the last 48 hours (to catch anything the original build might have missed during rate limiting)
3. Cross-reference with existing memory bank files
4. Update any files that need it
5. Write the refresh log

## 1C: Create the Scheduled Task Prompt

Create ~/Documents/Claude/PRISM/claude-code/scheduled-memory-refresh.md with a prompt that can be used as a Cowork scheduled task. It should:
- Mount ~/Documents
- Read the refresh protocol
- Execute the refresh for messages since last-refresh.txt date
- Use Gmail MCP tools (gmail_search_messages, gmail_read_thread)
- Update memory bank files
- Write refresh log
- Update last-refresh.txt

---

# UPGRADE 2: CONTENT REPURPOSING PIPELINE

Build a complete, reusable pipeline that takes ANY piece of raw content and produces multiple outputs. This should work for transcripts, articles, audio notes, meeting recordings — anything.

## 2A: Build the Pipeline SOP

Create ~/Documents/Claude/PRISM/sops/client-work/content-repurposing-pipeline.md

This SOP defines the complete pipeline:

### Input Types Supported
- Video/audio transcript (.vtt, .srt, .txt)
- Meeting transcript (Zoom, Google Meet)
- Existing blog post or article
- Podcast episode transcript
- Raw notes or brain dump
- Interview recording transcript
- Presentation/deck content

### Output Matrix

For EVERY input, the pipeline produces:

**Tier 1 — Long-form (1-2 pieces)**
- Authority Article (1,200-1,800 words): SEO-optimized, E-E-A-T compliant, follows the Article Writing from Transcripts SOP. Structured with hook, key insights, actionable takeaways, and CTA.
- Blog Post (800-1,200 words): Lighter version, more conversational, designed for [your-agency-domain.com]/blog

**Tier 2 — Short-form (3-5 pieces)**
- LinkedIn Post: Hook + story + lesson + CTA format. 150-300 words. Written in [Your Name]'s voice.
- Twitter/X Thread: 5-8 tweets breaking down the core insight. First tweet is the hook.
- Instagram Caption: Shorter, punchier. Includes relevant hashtags.

**Tier 3 — Video Scripts (3-5 pieces)**
- Short-form Video Script (60-90 sec): Hook text overlay, body, CTA. Designed for Reels/Shorts/TikTok.
- Long-form Video Outline: If the source material supports 5+ minutes, create a structured outline with timestamps, key points, and b-roll suggestions.

**Tier 4 — Email & Nurture (1-2 pieces)**
- Email Snippet: Subject line, preview text, body (200-400 words). Can slot into a newsletter or drip sequence.
- Lead Magnet Excerpt: If the content supports it, a standalone tip or framework that could be gated.

**Tier 5 — Internal/Operational (1 piece)**
- SOP Update Recommendation: If the content reveals a process, technique, or lesson that should be captured, note which PRISM SOP should be updated and with what.

### Pipeline Process

Step 1: INTAKE
- Read the raw content
- Identify the source type (transcript, article, notes, etc.)
- Extract: speaker(s), topic, key insights (3-5), memorable quotes, actionable advice, stories/anecdotes
- Determine the Topic Wheel position: is this a WHY (personal story), HOW (expertise), or WHAT (product/service) piece?
- Rate content richness: how many output tiers can this source realistically support? (Some short notes might only support Tier 2-3, not full articles)

Step 2: PRODUCE
- Generate all outputs the source supports, starting with Tier 1 and working down
- Each output follows its format requirements above
- All outputs written in [Your Name]'s voice: confident, real, grounded, not arrogant
- All outputs reference the Content Factory methodology where relevant
- Articles follow the Article Writing from Transcripts SOP
- Articles pass the Article QA & Compliance SOP

Step 3: QUALITY CHECK
- Every article: Does it pass E-E-A-T? Is it original (not just transcript reformatted)? Does it have a clear takeaway?
- Every video script: Does it have a hook in the first 3 seconds? Is the CTA clear?
- Every LinkedIn post: Does it tell a story, not just share an opinion? Is there a lesson?
- Every email: Is the subject line compelling? Would [Your Name] actually send this?

Step 4: OUTPUT
- Save all outputs to a structured folder:
  ```
  ~/Documents/Claude/PRISM/content-pipeline/[date]-[topic-slug]/
  ├── source.md (original transcript/content for reference)
  ├── articles/
  ├── video-scripts/
  ├── social-posts/
  └── email-snippets/
  ```
- Generate a manifest.md in each folder listing all pieces produced with status (draft/ready/published)

Step 5: DISTRIBUTION RECOMMENDATIONS
- For each piece, suggest which platform(s) it should go to
- Suggest Dollar-a-Day test candidates (which pieces are most likely to perform?)
- Suggest posting sequence (what order maximizes reach?)

### Quality Checks
- Does every piece trace back to real content [Your Name] or [Your Mentor/Advisor] actually said/wrote?
- Is [Your Name]'s voice consistent across all outputs?
- Are CTAs appropriate for each platform?
- Is there enough variety that the same insight doesn't feel repetitive across outputs?
- Does the Topic Wheel position match the content?

### Common Pitfalls
- Turning every transcript into an article without checking if the content is rich enough
- Generic LinkedIn posts that could be from anyone (make them [Your Name]'s voice with specific stories)
- Video scripts without hooks — the first 3 seconds determine everything
- Email snippets that are too long — keep them scannable
- Forgetting to check if sensitive/internal content leaked into public-facing outputs

## 2B: Process All Unprocessed Content

Now use the pipeline to process everything in the content-audit that hasn't been fully repurposed:

1. Read ~/Documents/Claude/PRISM/content-audit/01-local-media-inventory.md
2. Identify all transcripts and content sources marked as "unprocessed" or partially processed
3. For each usable source (skip confidential/internal content):
   - Run it through the full pipeline
   - Save outputs to ~/Documents/Claude/PRISM/content-pipeline/[date]-[topic-slug]/
4. Also check ~/Documents/Claude/PRISM/content-audit/drafts/ — the content audit already produced some drafts. Expand those into the full output matrix (they currently only have articles, video scripts, LinkedIn posts, and email snippets — add Twitter threads, Instagram captions, and blog post variants)

5. Read the memory bank file ~/Documents/Claude/PRISM/memory-bank/11-content-assets.md and cross-reference: what content has already been published vs what's still in draft?

## 2C: Build the Quick-Run Pipeline Prompt

Create ~/Documents/Claude/PRISM/claude-code/run-content-pipeline.md — a ready-to-use prompt for future pipeline runs:

```
claude "Read ~/Documents/Claude/PRISM/sops/client-work/content-repurposing-pipeline.md and follow the pipeline process. The input content is: [PASTE TRANSCRIPT OR FILE PATH HERE]. Process it through all 5 tiers and save outputs to ~/Documents/Claude/PRISM/content-pipeline/"
```

Also create a version for Cowork:
~/Documents/Claude/PRISM/content-pipeline/HOW-TO-USE.md explaining:
- How to drop a transcript into the pipeline
- Where outputs go
- How to mark pieces as published
- How to trigger a pipeline run

---

# UPGRADE 3: PRISM SEARCH INDEX (COMPRESSED CONTEXT FILE)

Build a single file that gives any Claude session instant full-context loading. Right now Claude has to read INDEX.md, then memory-bank/INDEX.md, then individual files — that's slow and uses a lot of context. The search index compresses everything into one fast-loading file.

## 3A: Build the Compressed Context File

Create ~/Documents/Claude/PRISM/CONTEXT.md — a single file (target: 3,000-5,000 words) that contains:

### Section 1: Who [Your Name] Is (200 words max)
Compressed from memory-bank/00-[your-username].md. Key facts only: name, age, location, military service, founding story, strengths, voice/style, current focus.

### Section 2: The Business (300 words max)
Compressed from memory-bank/01-hri-overview.md and sops/business-ops/hri-offer-ladder-and-gtm.md:
- What [Your Agency] is and isn't
- The four-tier offer ladder with exact pricing
- The flywheel: Apprentices → capacity + content; Sprints → cash + case studies
- Revenue model and YCF relationship
- Current financial state (from memory-bank/10-financial-context.md)

### Section 3: The Team (300 words max)
Compressed from memory-bank/03-team-directory.md and team-ops/01-team-directory.md:
- Every active team member: name, role, one-line description, how to reach them
- Key dynamics ([Your Mentor/Advisor] = product owner/closer, [Your AgentBuilder Partner] = delivery lead, [Your Name] = content + community + BD)
- Current pain points (from team-ops/14-current-pain-points.md)

### Section 4: Active Clients (200 words max)
Compressed from memory-bank/04-client-directory.md:
- Every active client: name, service, status, key contact
- Pipeline: prospects in discussion

### Section 5: Key Relationships (200 words max)
Compressed from memory-bank/07-relationship-map.md:
- Top 10 relationships by importance
- Current status of each

### Section 6: Current Strategy & Priorities (300 words max)
Compressed from memory-bank/12-strategic-context.md:
- Top 3 priorities right now
- Pending decisions
- Opportunities being pursued
- Risks on the horizon

### Section 7: Available SOPs (200 words max)
List every SOP with one-line description. This is the "table of contents" for the PRISM — Claude reads this to know which SOP to load for any task.

### Section 8: Scheduled Tasks (100 words max)
List all automated tasks with schedule and one-line description.

### Section 9: Content Status (200 words max)
Compressed from content-audit/00-executive-summary.md and memory-bank/11-content-assets.md:
- What's published, what's in draft, what's missing
- Current publishing cadence vs target
- Top priority content to produce next

### Section 10: Quick Reference (200 words max)
- Key URLs ([your-agency-domain.com], [your-username].com, etc.)
- Key pricing ($2,500 cert, $6,000 KP Sprint, $300/mo PAL)
- Key KPIs (10 intros/week, 4 closes/month, 90% on-time delivery)
- Key dates/deadlines if any

## 3B: Update CLAUDE.md to Load CONTEXT.md First

Edit ~/Documents/Claude/PRISM/claude-code/CLAUDE.md to add this at the very top of the "ON SESSION START" section:

"FAST CONTEXT LOAD: Start by reading ~/Documents/Claude/PRISM/CONTEXT.md — this is a compressed snapshot of [Your Name], his business, team, clients, strategy, and available SOPs. For most tasks this gives you enough context in under 30 seconds. Only read individual memory bank files or SOPs if you need deeper detail on a specific topic."

## 3C: Build the Context Refresh Logic

The CONTEXT.md file needs to stay current. Add a section to the bottom of CONTEXT.md:

```
---
## Meta
Last generated: [today's date]
Generated from: memory-bank/, sops/, team-ops/, content-audit/
To regenerate: Run `claude "Read all files in ~/Documents/Claude/PRISM/memory-bank/ and ~/Documents/Claude/PRISM/INDEX.md and regenerate ~/Documents/Claude/PRISM/CONTEXT.md following the compression format defined in the file's comments. Keep it under 5,000 words."`
```

Also add CONTEXT.md regeneration as a step in the weekly retrospective — after SOPs are updated, CONTEXT.md should be regenerated to reflect any changes.

---

# FINAL STEPS

## Update the PRISM INDEX

Add entries for:
- Content Repurposing Pipeline SOP (client-work)
- Memory Bank Refresh Protocol (templates)
- CONTEXT.md (root level)
- content-pipeline/ directory in architecture diagram
- Memory Bank Auto-Refresh scheduled task recommendation

## Write Session Log

Create a session log in ~/Documents/Claude/PRISM/logs/YYYY-MM/ documenting:
- All three upgrades completed
- Files created and modified
- Content pieces produced through the pipeline
- Memory bank files refreshed
- CONTEXT.md generated

## Regenerate .docx Copies

Run the converter to update readable copies:
```bash
cd ~/Documents/Claude/PRISM/sops && python3 convert_sops_to_docx.py
```

## Rules

- This runs overnight. Be exhaustive on all three upgrades.
- The Content Repurposing Pipeline SOP is the most important deliverable — it needs to be thorough enough that an apprentice could follow it.
- CONTEXT.md must stay under 5,000 words. Compression is the whole point.
- When refreshing the memory bank, never delete existing entries — only add or update.
- All content produced through the pipeline must be in [Your Name]'s voice.
- Skip confidential/internal transcripts when running the pipeline (check the content audit's viability table).
- If you hit Gmail rate limits during memory refresh, pause and retry.
- Log everything.

---

## See Also
- [[skills/PRISM-core|PRISM Core]]
- [[_Dashboard|Dashboard]]
- [[INDEX|Master Index]]
- [[SETUP-GUIDE]]
- [[claude-code/scheduled-memory-refresh|Memory Refresh]]
- [[sops/client-work/content-repurposing-pipeline|Content Repurposing Pipeline]]
