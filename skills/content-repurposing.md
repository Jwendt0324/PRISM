---
name: Content Repurposing
version: 1.1
description: Transform any raw content into 10-15 multi-platform outputs across 5 tiers
triggers:
  - repurpose content
  - content repurposing
  - long-form to short-form
  - content pipeline
  - repurpose video
  - repurpose transcript
  - multi-platform content
  - content suite
canon_source: blitzmetrics-canon/02-content-factory-process.md
full_sop: sops/client-work/content-repurposing-pipeline.md
triangles: [CCS, ACC, GCT]
---

# Content Repurposing — Executable Skill

## What This Does

One input (transcript, article, notes, recording) becomes 10-15 outputs across 5 tiers. This is the multiplication engine of the Content Factory.

## Step 1: INTAKE

1. Read raw content in full (do not skim)
2. Check viability: publishable? Not confidential? Not copyrighted?
3. Extract: speaker(s), core topic, 3-5 key insights, memorable quotes (exact words), actionable advice, stories/anecdotes
4. Determine Topic Wheel position: WHY (personal story) / HOW (methodology) / WHAT (product/service)
5. Rate richness:
   - **RICH** (all 5 tiers): Substantial, multiple insights, stories, actionable advice
   - **MODERATE** (Tiers 1-3): Good depth, limited stories
   - **LIGHT** (Tiers 2-3 only): Single insight, no real narrative
6. Do NOT fabricate content to fill tiers the source can't support

## Step 2: PRODUCE (Tier by Tier)

### Tier 1 — Long-Form (1-2 pieces)

**Authority Article (1,200-1,800 words)**
- Follow Article Writer skill exactly
- Hook (first sentence under 10 words) > H2 subheadings (verb-first) > actionable takeaways > CTA
- Must pass Article QA skill before marking done
- Bold key phrases, `[IMAGE: description]` placeholders, 2+ internal links

**Blog Post (800-1,200 words)**
- Different angle on same topic, not just a shorter version
- More conversational, more personal voice, less SEO structure

### Tier 2 — Short-Form Social (3-5 pieces)

**LinkedIn (150-300 words):** Hook > story > lesson > engagement question. No hashtags in body, 3-5 at end only.

**Twitter/X Thread (5-8 tweets):** First tweet stands alone as hook. One idea per tweet. Last tweet: summary + CTA.

**Instagram Caption (100-200 words):** Punchier than LinkedIn. First line is hook (visible before "more"). 15-20 hashtags in separate paragraph.

### Tier 3 — Video Scripts (3-5 pieces)

**Short-Form (60-90 seconds):** HOOK (text overlay, 3 sec max) > BODY (conversational) > CTA. For Reels/Shorts/TikTok. Include b-roll notes.

**Long-Form Outline (5+ min, only if source supports):** Hook > context > 3-5 key points with examples > takeaway > CTA. Structure for [Your Name] to speak naturally, not read.

### Tier 4 — Email & Nurture (1-2 pieces)

**Email Snippet (200-400 words):** Compelling subject line, one insight, one story, one CTA. Written as [Your Name] emailing a friend. Sign-off: "Love Always, [Your Name]"

**Lead Magnet Excerpt (if applicable):** Standalone tip/framework/checklist. Only if content has self-contained methodology.

### Tier 5 — Internal (1 piece)

**SOP Update Recommendation:** If content reveals a process/lesson for the Mainframe. Note which SOP to update and with what. Never published.

## Step 3: QUALITY CHECK

**Articles:** Run Article QA skill (zero banned words/patterns, E-E-A-T, 15+ contractions, 2+ internal links)

**Video Scripts:** Hook in first 3 seconds, natural speaking voice, 60-90 sec = 150-225 words

**LinkedIn:** Tells a story (not just opinion), specific lesson, ends with question, 150-300 words

**Twitter:** First tweet hooks alone, one idea per tweet, 5-8 tweets

**Email:** Subject line compelling, body scannable, one clear CTA

**ALL outputs:** Traces to real content, [Your Name]'s voice consistent, no sensitive content leaked, enough variety across outputs

## Step 4: OUTPUT

Save to structured folder:
```
~/Documents/Claude/Mainframe/content-pipeline/[YYYY-MM-DD]-[topic-slug]/
├── source.md
├── manifest.md
├── articles/
├── social-posts/
├── video-scripts/
└── email-snippets/
```

Generate manifest with: source, topic, Topic Wheel position, richness rating, all pieces with status, Dollar-a-Day candidates, publishing sequence.

See `~/Documents/Claude/Mainframe/content-pipeline/HOW-TO-USE.md` for full pipeline folder structure and delivery conventions.

## Step 5: DISTRIBUTION RECOMMENDATIONS

1. **Platform assignments:** [Your Agency] channel vs [Your Name] personal, LinkedIn vs Twitter, blog vs email
2. **Dollar-a-Day candidates:** 2-3 pieces most likely to perform in paid (strong hook, universal insight, emotional resonance)
3. **Publishing sequence:** LinkedIn post first > article > email > video scripts as [Your Name] films
4. **Cross-promotion:** How pieces link to each other

## [Your Name]'s Voice (Apply to All Outputs)

- Direct. No hedging.
- Confident but not arrogant. Backs claims with examples.
- Grounded. Real stories, real numbers, real people.
- Young but serious. No corporate speak, no "fellow kids" energy.
- Anti-patterns: No jargon, no hype, no "in today's fast-paced world," no "let's dive in"

## Human Gates

| Step | Gate |
|---|---|
| Viability check | Review — publishable? confidential? |
| Topic Wheel positioning | Review — WHY/HOW/WHAT classification |
| Voice/tone review (all outputs) | Review — "Would [Your Name] actually say this?" |
| E-E-A-T verification | Review — real stories trace to source |
| Sensitive content screening | Review — meeting transcripts may contain internal info |
| Platform assignment | Review — strategic judgment |
| Dollar-a-Day candidate selection | Review — experience with paid performance |

## Key Pitfall

Do NOT turn every transcript into an article. Short transcripts (under 500 words substantive) cannot support Tier 1. Classify LIGHT and produce Tiers 2-3 only. Fabricating content to fill tiers violates E-E-A-T.
