---
name: Article Writer
version: 1.1
description: Write batches of SEO-optimized articles from transcripts using the HRI Content Engine v5 pipeline
triggers:
  - write articles
  - batch articles
  - transcript to article
  - article writing
  - article production
  - content engine
canon_source: blitzmetrics-canon/03-article-guidelines.md
full_sop: sops/client-work/article-writing-from-transcripts.md
triangles: [CCS, ACC, GCT]
---

# Article Writer — Executable Skill

## Phase 1: Setup (First Time Per Client)

1. **Build voice profile.** Read 6-10 transcripts. Capture: sentence patterns, signature phrases, contraction usage, recurring analogies, anti-positions, named references. Save to `~/Documents/Claude/Mainframe/content-pipeline/voice-profiles/voice-profile-[client].md`
2. **Set up client config.** Author, site, revenue pages, internal link targets, existing content (for anti-cannibalization), Topic Wheel categories, default article length (typically 1,200-1,500 words)
3. **Create .docx generator** using python-docx (Requires: `pip install python-docx`): SOURCE VIDEO block at top, meta description italic, H1 (16pt bold), H2s (14pt bold, verb-first), body (11pt, 1.15 spacing), bold key phrases, `[IMAGE: description]` placeholders

## Phase 2: Content Tree Verification (EVERY Batch)

1. Search `site:clientdomain.com [topic]` for existing content
2. Search ARTICLE_INDEX.csv from prior batches for overlap
3. **If article exists on topic:** ENHANCE existing, do not duplicate
4. Rate transcripts: GREEN (1000+ words, substantive), YELLOW (mid-depth), RED (short, skip or brief framing)
5. Identify E-E-A-T signals in each transcript: real stories, named people, credentials

## Phase 3: Writing

1. Launch parallel writing agents (~5 articles per agent, 10 agents = sweet spot)
2. Every article MUST include:
   - At least one real story/anecdote from transcript (not fabricated)
   - Real names of people, places, events
   - Speaker's actual credentials
   - `[IMAGE: real photo description]` placeholders
   - Topic Wheel category tag
3. Run QA audit after all articles written. Check for:
   - Zero em dashes, zero banned words, zero banned AI patterns, zero salesy language
   - 15+ contractions, signature phrases present, word count above minimum
   - 2+ internal links, first sentence under 10 words
   - No rhetorical questions, no sentences ending with prepositions
   - Paragraphs 3-5 lines max, active voice throughout
4. Fix ALL violations with repair agents. Re-run until 100% pass

## Banned Words (Grep for These)

delve, landscape, leverage (as verb), utilize, facilitate, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon, realm

## Banned AI Patterns (Sentence-Level)

"not because X, but because Y" | "this is where X comes in" | "put it this way" | "In today's [noun]..." | "It's important to note..." | "Whether you're a... or a..." | "At the end of the day..." | "In the world of..." | "[Topic] is not just about..." | "When it comes to..." | "In conclusion..." | "As we navigate..."

## Phase 4: Run 18-Step QA Gate

Run every article through the Article QA skill. Automated checks (steps 4-7, 9, 11, 13) must be 100% pass. Flag human-required steps (8, 10, 12, 14-18) in handoff doc.

## Phase 5: Human Review Gate (MANDATORY)

Prepare handoff package:
- All .docx files named uniformly: `NNN - Title.docx`
- `ARTICLE_INDEX.csv`: #, Filename, Title, Source Transcript, YouTube URL, Topic Wheel Category, Tier, E-E-A-T Score
- `QA_REPORT.md`: pass/fail on all automated checks
- `HUMAN_REVIEW_CHECKLIST.md`: what reviewer must verify per article

**Human reviewer checks:** Voice authenticity, real stories (traceable to transcript), no fabricated content, name/brand spellings, Topic Wheel alignment, no cannibalization, figurehead context accuracy

## Phase 6: Package & Deliver

1. Generate ARTICLE_INDEX.csv
2. Archive articles under 750 words to `_archived_short/`, renumber remaining
3. Generate meta-article: how many transcripts processed, voice profile used, articles produced vs archived, QA violations caught, human reviewer flags, time estimate, lessons learned

## Known Pitfalls

- Automated contraction scripts create broken words ("doesn'thing"). Always audit.
- "Not because X, but because Y" is the #1 escaped pattern. Add to every QA run.
- Check for duplicate opening sentences across the full batch.
- Short transcripts (under 500 words) cannot become 1,500-word articles without fabricating. Classify RED, archive or write brief framing piece.
- Podbean episodes often duplicate YouTube content. Cross-reference first.
- **Never skip human review because automated QA passed.** Automated catches mechanics; humans catch voice, fabrication, and strategy.
