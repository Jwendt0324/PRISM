---
name: Article Writer
version: 1.3
description: Write batches of SEO-optimized articles from transcripts using the
  Content Engine pipeline
triggers:
  - write articles
  - batch articles
  - transcript to article
  - article writing
  - article production
  - content engine
canon_source: blitzmetrics-canon/03-article-guidelines.md
full_sop: sops/client-work/article-writing-from-transcripts.md
triangles:
  - CCS
  - ACC
  - GCT
tags:
  - status/active
  - triangle/CCS
  - triangle/LDT
  - type/skill
---

# Article Writer — Executable Skill

## Phase 0: Load Good Examples (Every Batch)

Before writing any articles, check your good-examples library for approved reference articles. If examples exist, read them all. Study the tone, structure, transitions, heading style, and depth. Your output should match or exceed the quality of these approved examples. If no examples exist yet, proceed with the guidelines below — but flag the first approved article as a candidate for the good-examples library.

This skill follows the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] methodology and the [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]. Articles are organized around the [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]].

## Phase 1: Setup (First Time Per Client)

1. **Build voice profile.** Read 6-10 transcripts. Capture: sentence patterns, signature phrases, contraction usage, recurring analogies, anti-positions, named references. Save to your voice profiles directory.
2. **Set up client config.** Author, site, revenue pages, internal link targets, existing content (for anti-cannibalization), Topic Wheel categories, default article length (typically 1,200-1,500 words)
3. **Create .docx generator** using python-docx (Requires: `pip install python-docx`): SOURCE VIDEO block at top, meta description italic, H1 (16pt bold), H2s (14pt bold, verb-first), body (11pt, 1.15 spacing), bold key phrases, `[IMAGE: description]` placeholders

## Phase 2: Content Tree Verification (EVERY Batch)

1. Search `site:clientdomain.com [topic]` for existing content
2. Search ARTICLE_INDEX.csv from prior batches for overlap
3. **If article exists on topic:** ENHANCE existing, do not duplicate
4. Rate transcripts: GREEN (1000+ words, substantive), YELLOW (mid-depth), RED (short, skip or brief framing)
5. Identify E-E-A-T signals in each transcript: real stories, named people, credentials
6. **SEO Tree classification:** For each article, determine its position in the content architecture:
   - **Trunk:** Core concept definitive article (e.g., "What is Dollar-a-Day?"). One per major topic. Rarely created new -- enhance existing.
   - **Branch:** Sub-topic definitive article (e.g., "3x3 Video Grid for Dollar-a-Day"). Links up to trunk.
   - **Leaf:** Specific instance article, case study, or meta-article (e.g., "How We Built [Client Name]'s Video Funnel"). Links up to its branch AND trunk.
   - Classification determines internal linking strategy: leaves link to branches, branches link to trunk, trunk links to other trunks.

## Phase 3: Writing

1. Launch parallel writing agents (~5 articles per agent, 10 agents = sweet spot)
2. **CRITICAL: Sub-agents cannot load PRISM skill files by path.** You MUST embed the banned lists and QA rules directly in each sub-agent's prompt. Copy the "Sub-Agent QA Embed" section below into every writing agent prompt. File path references like "see article-qa.md" are silently ignored by sub-agents.
3. Every article MUST include:
   - At least one real story/anecdote from transcript (not fabricated)
   - Real names of people, places, events
   - Speaker's actual credentials
   - `[IMAGE: real photo description]` placeholders
   - Topic Wheel category tag
4. Run QA audit after all articles written (use `scripts/qa_audit.py` for batch, or manual check for small batches):
   - **BLOCK (zero tolerance):** Zero banned words, zero banned AI patterns, zero salesy language
   - **WARN (fix or document):** Zero em dashes (unless voice profile permits), 2+ internal links, no text walls (8+ line paragraphs), no stacked rhetorical questions (2+ in a row), contractions used naturally (flag if zero in 500+ words)
   - **STYLE (author judgment):** Paragraph rhythm should vary (one-liners for punch, longer for complex ideas). Single rhetorical questions are fine. Passive voice is fine when the subject isn't the point. Don't flatten voice to pass a checklist.
5. Fix all BLOCK violations with repair agents. Address WARN violations. Re-run until 0 BLOCK

### Sub-Agent QA Embed (Copy This Into Every Writing Agent Prompt)

```
QUALITY RULES — FOLLOW THESE EXACTLY:

BANNED WORDS (zero tolerance — never use): delve, landscape, realm, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, utilize, facilitate, leverage (as verb), streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon

BANNED AI PATTERNS (zero tolerance — if you catch yourself writing these, rewrite the entire sentence):
- "In today's [anything]..."
- "It's important to note..."
- "Whether you're a... or a..."
- "At the end of the day..."
- "In the world of..."
- "[Topic] is not just about..."
- "When it comes to..."
- "In conclusion..."
- "As we navigate..."
- "Not because X, but because Y"
- "This is where X comes in"
- "Let that sink in"
- "Full stop." (as emphasis)
- "Here's the thing"
- "Put it this way"

BANNED SALESY LANGUAGE: "limited time", "what are you waiting for", "act now", "don't miss out", "sign up today"

WRITING STYLE:
- Use contractions naturally throughout (don't, isn't, can't, etc.)
- No em dashes (—) unless told otherwise
- Vary paragraph length — one-sentence punches for emphasis, longer paragraphs for complex ideas
- Active voice is the default, but passive is fine when the subject isn't the point
- Single rhetorical questions are fine. Do NOT stack 2+ in a row.
- Every claim must trace to the source transcript. Do not fabricate stories or quotes.
- 2+ internal links with descriptive anchor text (3-6 words, never "click here")
```

## Entity Linking Decision Tree (Canon 17 -- Apply to EVERY Article)

For every person, business, concept, or organization mentioned, follow this tree to determine the link target:

| Entity Type | Link To | NEVER Link To |
|---|---|---|
| **Person** (anyone with a personal brand site) | Their personal brand site (e.g., [mentor-site].com) | LinkedIn, social media profiles, or articles ABOUT them |
| **Network business/organization** | Their primary website | Case studies or articles about them |
| **BlitzMetrics concept** (Content Factory, Dollar-a-Day, etc.) | The definitive article on blitzmetrics.com | Competitor articles or generic explainers |
| **External concept or public figure** | Most authoritative source (official page, industry authority) | Wikipedia (unless literally no alternative), LinkedIn for people |

**Rules:** Link on first meaningful mention only. Descriptive anchor text (3-6 words), never bare URLs. Don't re-link same entity in same section.

**Sub-agents:** Copy the table above into every writing agent prompt alongside the banned words. Sub-agents cannot access canon files by path.

## Banned Words (Grep for These)

delve, landscape, leverage (as verb), utilize, facilitate, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon, realm

## Banned AI Patterns (Sentence-Level — Rewrite Entire Sentence, Don't Swap Phrases)

"not because X, but because Y" | "this is where X comes in" | "put it this way" | "here's the thing" | "In today's [noun]..." | "It's important to note..." | "Whether you're a... or a..." | "At the end of the day..." | "In the world of..." | "[Topic] is not just about..." | "When it comes to..." | "In conclusion..." | "As we navigate..." | "Let that sink in" | "Full stop." (as emphasis)

## Phase 4: Run Quality Gate

Run every article through the [[skills/article-qa|Article QA]] skill (`/qa`). All BLOCK-tier checks must pass. WARN-tier checks should pass or have documented exceptions. STYLE items are author judgment — don't over-correct. Flag human-required steps (3, 8, 10, 12) in handoff doc. Post-publish steps (14-18) are tracked separately and don't block delivery.

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

## Connected Skills

| After Writing | Skill | Purpose |
|--------------|-------|---------|
| QA each article | `/article-quality-gate` or `/qa` | Run 18-step BlitzMetrics gate |
| Document the process | `/meta-article` | Publishable process article with real metrics |
| Prep for WordPress | `/wp-publisher` | Generate meta, schema, RankMath brief |
| Optimize for AI search | `/geo-optimizer` | Check AI citability and entity signals |
| Create social posts | `/social-content` | Transform articles to LinkedIn/Facebook/X |
| Batch production | `/batch-content` | Parallel production with subagents |
| Track in Basecamp | `/basecamp-ops` | Post completion update |

### Cross-References

- [Canon: Article Guidelines](../blitzmetrics-canon/03-article-guidelines.md)
- [Canon: Content Factory Process](../blitzmetrics-canon/02-content-factory-process.md)
- [Full SOP: Article Writing](../sops/client-work/article-writing-from-transcripts.md)
- [Article QA Skill](article-qa.md)
- [Content Factory Skill](content-factory.md)
- [Transcription Pipeline SOP](../sops/client-work/transcription-pipeline.md)

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]]
- [[skills/article-qa|Article QA]]
- [[skills/content-repurposing|Content Repurposing]]

## Post-Publish Tracking

After articles are published, track performance via GA4 and GSC:
- **GA4:** Monitor page sessions, engagement time, and organic traffic share for each article URL
- **GSC:** Run `/gsc-insights` at 7 and 14 days post-publish to verify indexing, check target keyword impressions, clicks, CTR, and average position
- Flag any article not indexed after 14 days — request indexing via GSC
- Feed performance data back into the next batch: high-performing topics get more articles, low performers get diagnosed

## Known Pitfalls

- Automated contraction scripts create broken words ("doesn'thing"). Always audit.
- "Not because X, but because Y" is the #1 escaped pattern. Add to every QA run.
- Check for duplicate opening sentences across the full batch.
- Short transcripts (under 500 words) cannot become 1,500-word articles without fabricating. Classify RED, archive or write brief framing piece.
- Podbean episodes often duplicate YouTube content. Cross-reference first.
- **Never skip human review because automated QA passed.** Automated catches mechanics; humans catch voice, fabrication, and strategy.
