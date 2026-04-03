---
description: Write batches of SEO-optimized articles from YouTube/podcast transcripts using the [Your Agency] Content Engine v5 pipeline, with full [Methodology Partner] quality gates, human review checkpoints, and E-E-A-T compliance
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 2.1
canon_compliance: 03-article-guidelines.md, 07-quality-standards.md, 08-human-requirements.md, 10-anti-vandalism-checklist.md
triangles:
  CCS: "Article QA checklist, banned words/patterns, 18-step quality gate"
  ACC: "Produce (transcript) → Process (article) → Post (WordPress) → Amplify (Dollar-a-Day)"
  GCT: "Goals: authority content at scale. Content: transcript-based articles. Targeting: Topic Wheel categories"
canon_sources: [03-article-guidelines.md, 07-quality-standards.md, 08-human-requirements.md, 10-anti-vandalism-checklist.md]
tags:
  - type/sop
  - status/active
  - domain/client-work
  - topic/article-writing
  - topic/transcripts
---

# Article Writing from Transcripts

## Purpose

Transform raw video/podcast transcripts into publication-ready .docx articles that pass all [Your Agency] Content Engine v5 quality gates AND the [[skills/article-qa|[Methodology Partner] 18-step QA gate]], formatted for Google Docs import and WordPress publishing. Every article must be reviewed by a human before publishing — no fully automated pipeline.

## When to Use

- Transcripts have been pulled and [Your Name] says "write articles" or "batch [N]"
- A new client's transcripts are ready for article production
- Existing articles need to be rewritten to comply with v5 spec

## Canon Compliance

This SOP implements requirements from the following [Methodology Partner] Canon documents:

| Canon Document | What It Governs |
|----------------|-----------------|
| `03-article-guidelines.md` | 18-step article quality checklist, banned words/patterns, structural requirements |
| `07-quality-standards.md` | Overall quality standards across all content types |
| `08-human-requirements.md` | Where humans are required — no auto-publish without human review |
| `10-anti-vandalism-checklist.md` | Content tree verification, anti-cannibalization rules |

**Non-negotiable canon rules:**
- No article auto-publishes without human review and approval (08-human-requirements)
- All content must trace to real source material — never fabricate quotes or stories (03-article-guidelines, anti-vandalism rule 6)
- Always check what already exists before creating new content (03-article-guidelines, anti-vandalism rule 1)
- AI-assisted pieces must be reviewed by a human who knows the client's voice (08-human-requirements)

## Human-Required Steps

Per `08-human-requirements.md`, these steps CANNOT be fully automated:

| Step | Why Human Required | Who |
|------|--------------------|-----|
| Voice/tone approval | "Would the client actually say this?" | [Your Name] or trained reviewer |
| E-E-A-T compliance review | Ensuring real stories, not fabricated ones | [Your Name] or trained reviewer |
| AI language detection | Subtle AI patterns require trained eye | [Your Name] or trained reviewer |
| Featured image selection | Must be real, relevant photo (not stock) | [Your Name], VA, or client |
| WordPress publishing | Credentials, featured image upload, RankMath | [Your Name] or VA |
| Category/tag selection | Must align with client's Topic Wheel | [Your Name] |
| Content tree verification | Ensuring no keyword cannibalization | [Your Name] or trained reviewer |
| Final publish approval | Strategic judgment on timing and positioning | [Your Name] |

## Process

### Phase 1: Setup (Steps 1-3)

1. **Build the voice profile.** Read 6-10 diverse transcripts from the client. Capture:
   - Sentence length patterns (short punchy vs. long explanatory)
   - Signature phrases and verbal tics ("my friends," "right?," etc.)
   - Contraction usage, filler words, self-corrections
   - Recurring analogies, metaphors, examples
   - Anti-positions (what they argue against)
   - Named people they reference regularly
   Save to `~/Article Machine/voice-profile-[client].md`.

2. **Set up the client config.** Fill the CLIENT SETUP TEMPLATE from the v5 spec:
   - Author, publishing site, revenue pages, internal link targets
   - Existing top content (to avoid cannibalization)
   - Target audience, industry, competitors
   - Default article length (typically 1,200-1,500 words)
   - **[[blitzmetrics-canon/06-topic-wheel|Topic Wheel]] categories** — map all content pillars so each article can be tagged to a category

3. **Create the .docx generator script.** Use `python-docx` to produce properly formatted docs:
   - SOURCE VIDEO block at top (title + YouTube URL)
   - Meta description in italic
   - H1 title (16pt bold)
   - H2 subheadings (14pt bold, verb-first)
   - Body text (11pt, 1.15 line spacing)
   - Bold key phrases inline
   - `[IMAGE: description]` placeholders where relevant
   Save script to `~/[client-name]-articles-v2/create_docx.py` (or client equivalent).

### Phase 2: Content Tree Verification & Topic Mapping (Steps 4-5)

4. **Verify the content tree (anti-vandalism).** Before writing ANY new article:
   - Search Google (`site:clientdomain.com [topic]`) for existing content on the same topic
   - Search the internal blog/CMS for matching keywords
   - Search `ARTICLE_INDEX.csv` from prior batches for overlap
   - **If article exists on topic:** ENHANCE the existing article rather than creating a duplicate (canon anti-vandalism rule 1)
   - **If close overlap:** Differentiate angle clearly or merge with existing
   - Document content tree decisions in `content-tree-decisions-[client].md`

5. **Read all transcripts and map article topics.** For each transcript, identify:
   - Core topic / unique angle
   - **Topic Wheel position** — which content pillar does this article serve?
   - Whether it overlaps with existing articles (cannibalization check from step 4)
   - Content tier: GREEN (substantive, 1000+ word transcript), YELLOW (mid-depth), RED (performance/short, skip or brief framing)
   - **E-E-A-T signals available:** What real stories, experiences, credentials, or named examples does the speaker provide in this transcript?

### Phase 3: Writing (Steps 6-8)

6. **Launch parallel writing agents.** Each agent handles a batch of ~5 articles:
   - Reads its assigned transcripts in full
   - Writes each article following ALL v5 rules (banned words, burstiness, structure randomization, E-E-A-T signals)
   - Outputs .docx files with YouTube source at top
   - 10 agents running simultaneously is the proven sweet spot
   - **E-E-A-T requirement:** Every article MUST include:
     - At least one real story or anecdote from the transcript (not fabricated)
     - Real names of people, places, or events mentioned by the speaker
     - The speaker's actual credentials or experience relevant to the topic
     - `[IMAGE: real photo description]` placeholders for authentic photos (not stock)
   - **Topic Wheel tag:** Each article must note its Topic Wheel category in the document metadata

7. **Run the QA audit script** after all articles are written. The audit checks:
   - Zero em dashes
   - Zero banned words (delve, landscape, leverage-as-verb, utilize, facilitate, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon, realm)
   - Zero banned AI patterns ("not because X, but because Y," "this is where X comes in," "put it this way," "In today's [noun]...," "It's important to note...," "Whether you're a... or a...," "At the end of the day...," "In the world of...," "[Topic] is not just about...," "When it comes to...," "In conclusion...," "As we navigate...")
   - Zero salesy language ("limited time," "what are you waiting for," "act now," "don't miss out," "you won't believe," "secret to")
   - Contractions per article (target: 15+ for natural voice)
   - "My friends" or equivalent signature phrase present
   - Word count above minimum (typically 1,200)
   - Internal links (2+ per article)
   - First sentence under 10 words
   - No rhetorical questions or weasel words
   - No sentences ending with prepositions
   - Paragraphs 3-5 lines maximum
   - Active voice throughout

8. **Fix all violations** using parallel repair agents. Common fixes:
   - Banned patterns: rewrite the entire sentence with a different construction
   - Short articles: expand with deeper anecdotes/examples from the transcript
   - Missing signature phrases: insert naturally near the opening or a key transition
   - Salesy language: replace with conversational phrasing
   - Missing E-E-A-T signals: go back to transcript and extract real stories/names

### Phase 4: [Methodology Partner] 18-Step QA Gate (Step 9)

9. **Run the full [Methodology Partner] 18-step QA gate.** Every article must pass ALL steps in `article-qa-blitzmetrics.md` before being marked as ready for human review. This gate covers:
   - Pre-writing phase (steps 1-4): requirements, transcription, video review, research
   - Writing phase (steps 5-10): article quality, titles, hooks, multimedia, links, video embed
   - QA phase (steps 11-13): proofread, WordPress prep, categorization
   - Publishing phase (steps 14-18): cross-post, content library, Dollar-a-Day, MAA, iteration

   **For batch AI-written articles, the relevant automated checks are steps 4-7, 9, 11, 13.** Steps requiring human action (8, 10, 12, 14-18) are flagged in the handoff document.

   Re-run audit until 100% pass on automatable steps. Do not deliver articles with any violations.

### Phase 5: Human Review Gate (Step 10) — MANDATORY

10. **MANDATORY HUMAN REVIEW.** No article proceeds to publishing without this gate.

    **Prepare the handoff package:**
    - All .docx files organized with uniform naming (`NNN - Title.docx`)
    - `ARTICLE_INDEX.csv` with columns: `#, Filename, Article Title, Source Transcript, YouTube Video URL, Topic Wheel Category, Content Tier, E-E-A-T Score (auto)`
    - `QA_REPORT.md` showing pass/fail on all automated checks
    - `HUMAN_REVIEW_CHECKLIST.md` listing what the reviewer must verify per article

    **Human reviewer must check:**
    - [ ] Voice sounds like the client (not generic AI)
    - [ ] All stories and anecdotes are real (traceable to transcript)
    - [ ] No fabricated quotes, experiences, or credentials
    - [ ] Names and brand references are spelled correctly
    - [ ] Topic Wheel category assignment is correct
    - [ ] No cannibalization with existing published content
    - [ ] Figurehead context is accurate (relationships between people mentioned)
    - [ ] Overall quality — would [Your Name] be comfortable with his name on this?

    **Reviewer marks each article:** APPROVED / NEEDS REVISION / REJECT
    - APPROVED: Proceeds to WordPress publishing
    - NEEDS REVISION: Returns to agent for specific fixes, then re-review
    - REJECT: Transcript is insufficient or topic is redundant — archive

### Phase 6: Packaging & Delivery (Steps 11-12)

11. **Generate the article index.** Save as `ARTICLE_INDEX.csv` in the same folder:
    ```
    #,Filename,Article Title,Source Transcript,YouTube Video URL,Topic Wheel Category,Content Tier,Review Status
    ```

12. **Archive short articles** if applicable. Move articles under 750 words to `_archived_short/` subfolder. Renumber remaining files sequentially.

### Phase 7: Meta-Article Generation (Step 13)

13. **Generate meta-article for each batch.** [Your Mentor/Advisor]'s concept: document HOW each article was created so the process itself becomes teachable content.

    Save as `META-[client]-batch-[N].md` in the same folder. Include:
    - How many transcripts were processed
    - What voice profile was used
    - How many articles were produced vs. archived
    - What QA violations were caught and fixed
    - What the human reviewer flagged
    - Time from transcripts to approved articles
    - Lessons learned for the next batch

    **This meta-article can itself become content** — it demonstrates the Content Factory methodology in action (LDT: learn the process, do the articles, teach via meta-article).

### Phase 8: Post-Publishing & MAA Tracking (Steps 14-15)

14. **After human-approved articles are published to WordPress:**
    - Log each article in the Content Library with: URL, title, date, category, Topic Wheel position, 3 Components of Authority score (What/Who/Where)
    - Flag high-authority articles as Dollar-a-Day candidates
    - Submit to cross-posting pipeline (Facebook, LinkedIn, Twitter)

15. **MAA tracking — feed performance back into process improvement.**
    - Track: page views, time on page, bounce rate, keyword rankings
    - Compare performance across Topic Wheel categories
    - Compare performance across content tiers (GREEN vs. YELLOW)
    - Include in weekly/monthly MAA report
    - **Feedback loop:** If a category consistently underperforms, investigate:
      - Are the transcripts weak on that topic?
      - Is the writing style wrong for that audience?
      - Is there cannibalization with existing content?
    - If performing well: repurpose into additional formats (video script, LinkedIn post, email)
    - Update `content-tree-decisions-[client].md` with performance data

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Voice/tone approval (Phase 5, Step 10) | Review | "Would the client actually say this?" — requires someone who knows the client's voice |
| E-E-A-T compliance review (Phase 5, Step 10) | Review | Ensuring real stories, not fabricated ones |
| AI language detection (Phase 5, Step 10) | Review | Subtle AI patterns require trained eye |
| Featured image selection (post-approval) | Execute | Must be real, relevant photo — not stock |
| WordPress publishing (post-approval) | Execute | Credentials, featured image upload, RankMath settings |
| Category/tag selection (post-approval) | Review | Must align with client's Topic Wheel strategy |
| Content tree verification (Phase 2, Step 4) | Review | Ensuring no keyword cannibalization with existing content |
| Final publish approval | Approve | Strategic judgment on timing and positioning |

## Anti-Vandalism Checks
- [ ] Check what already exists on client's site before writing (Google: site:domain.com [topic])
- [ ] Search ARTICLE_INDEX.csv from prior batches for topic overlap
- [ ] Verify no keyword cannibalization with existing published articles
- [ ] Confirm internal linking structure maintained across batch
- [ ] Document content tree decisions in content-tree-decisions-[client].md
- [ ] No fabricated quotes, stories, or credentials (trace everything to transcript)

## Quality Checks

### Automated (must be 100% before human review)
- [ ] QA audit script returns 0 violations across all articles
- [ ] Every article has YouTube source title + URL at top
- [ ] Every article has meta description
- [ ] Every article has 2+ internal links
- [ ] Word count is above client minimum (typically 1,200)
- [ ] ARTICLE_INDEX.csv is complete and accurate
- [ ] Files are named uniformly: `NNN - Title.docx`
- [ ] No duplicate opening sentences across articles
- [ ] Topic Wheel category assigned to every article
- [ ] Content tree verification completed (no cannibalization)

### Human (must be completed before publishing)
- [ ] Voice/tone review passed for every article
- [ ] E-E-A-T compliance verified (real stories, real people, real credentials)
- [ ] No fabricated content detected
- [ ] Name/brand spellings verified against source material
- [ ] Figurehead relationships and context accurate
- [ ] Category/tag alignment with Topic Wheel confirmed
- [ ] Featured images selected (real photos, not stock)

### [Methodology Partner] Canon
- [ ] Full 18-step QA gate passed (per `article-qa-blitzmetrics.md`)
- [ ] Anti-vandalism rules satisfied (per `10-anti-vandalism-checklist.md`)
- [ ] Human requirements honored (per `08-human-requirements.md`)
- [ ] Meta-article generated for the batch

## Common Pitfalls

- **Automated contraction scripts create broken words.** "you have" → "you've" can produce "you've a pile" (British-sounding) or "doesn'thing" (broken). Always audit contraction replacements and fix artifacts. The [Client Name] project had 59 broken contractions from the automated fix.
- **"Not because X, but because Y" slips through constantly.** This is the most common banned AI pattern. It appeared in 10 of 54 [Client Name] articles despite explicit instructions. Add it to every QA audit.
- **Duplicate opening sentences across articles.** [Client Name] articles 5 and 50 both opened with "My father built our house by hand." Always check for duplicates across the full batch.
- **Agents use inconsistent file naming.** Different parallel agents may name files differently (e.g., `article-203-v5.docx` vs `203.docx` vs `article-203-slug.docx`). Run a normalization pass after all agents complete.
- **Word count target vs. transcript length.** Short transcripts (under 500 words) cannot become 1,500-word articles without fabricating content. Classify these as RED tier and give them brief framing pieces, or archive them entirely. Fabricating content to hit word count violates E-E-A-T.
- **Podbean episodes often duplicate YouTube content.** Cross-reference before writing. On the [Client Name] project, 44 of 45 Podbean episodes were duplicates.
- **Skipping human review "because automated QA passed."** Automated QA catches mechanical issues (banned words, word count, links). It CANNOT catch voice authenticity, fabricated stories, or strategic misalignment. The human gate is mandatory per canon.
- **Creating new articles on topics that already have published content.** Always run content tree verification first. Enhancing an existing article is better than cannibalizing it with a new one.
- **E-E-A-T fabrication under pressure.** When a transcript is thin, agents may invent stories or credentials to fill space. This is worse than a short article. Archive the transcript or write a brief framing piece instead.

## Learnings Log

- **2026-03-18 ([Client Name]):** 54 articles written (50 YouTube + 4 guest appearances). 10 parallel agents produced all 50 YouTube articles simultaneously. QA audit caught 27 violations in first pass, reduced to 0 after two repair rounds.
- **2026-03-18 ([Client — Local Retail Business]):** 378 articles from 400 transcripts. 98 archived for being under 750 words (all from performance/jam videos with minimal dialogue). Voice profile captured the brother dynamic (John sets up tech detail, Jeremy delivers opinion).
- **2026-03-18:** The biggest QA issue is always banned AI patterns, not banned words. Words are easy to grep for. Patterns require sentence-level analysis. Build the QA script with regex patterns for every banned construction.
- **2026-03-20 (v2.0 upgrade):** Added mandatory human review gate, [Methodology Partner] 18-step QA integration, E-E-A-T compliance requirements, content tree verification, meta-article generation, 9 Triangles mapping, Topic Wheel positioning, and MAA tracking feedback loop per SOP audit findings. Previous versions had a fully automated pipeline with no human checkpoint — this was a canon violation.

---

## Related

- [Article QA SOP](article-qa-blitzmetrics.md)
- [Transcription Pipeline SOP](transcription-pipeline.md)
- [YouTube Transcript SOP](youtube-transcript-scraping.md)
- [Podcast Transcript SOP](podcast-transcript-scraping.md)
- [Canon: Article Guidelines](../../blitzmetrics-canon/03-article-guidelines.md)
- [Skill: Article Writer](../../skills/article-writer.md)

## See Also

- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/07-quality-standards|Quality Standards]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]]
- [[skills/article-writer|Article Writer]]
- [[skills/article-qa|Article QA]]
- [[skills/content-factory|Content Factory Skill]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]