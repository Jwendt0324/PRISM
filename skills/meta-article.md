---
name: Meta-Article Generator
version: 2
description: Generate a publishable meta-article documenting how an AI agent
  created content — auto-populated from session data, voice-matched, QA-gated,
  entity-linked
triggers:
  - meta article
  - meta-article
  - document what you just did
  - write a meta article
  - process article
  - how we built
canon_source: blitzmetrics-canon/03-article-guidelines.md
triangles:
  - CCS
  - MAA
  - LDT
tags:
  - status/active
  - triangle/CCS
  - triangle/MAA
  - type/skill
connected_skills:
  before:
    - article-writer
    - article-qa
    - transcript-pipeline
  after:
    - wp-publisher
    - social-content
    - basecamp-ops
---

# Meta-Article Generator v2 — Executable Skill

## What Is a Meta-Article?

A meta-article documents exactly what an AI agent did during a specific task. It follows the [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]] and feeds into [[skills/definitive-article|Definitive Articles]] as linked examples. It shows the decisions made, systems connected, time taken, and outcomes produced. Two purposes:

1. **SEO value** — publishable content proving the Content Factory works (leaves in the SEO Tree linking back to definitive article branches)
2. **Recursive improvement** — process failures revealed in meta-articles feed back into SOP/skill updates

**Source:** Dennis Yu's meta-article framework at blitzmetrics.com/meta-article-prompt-template/

---

## Phase 0: Load Good Examples

Before writing, check your good-examples library for approved reference meta-articles. If examples exist, read them all. Study the tone, structure, and depth. Match or exceed.

---

## Phase 1: Auto-Populate from Session Data

**Do NOT guess numbers. Extract real data.**

### Step 1A: Run the metrics extractor

If you have a session metrics extraction script, run it to get:
- Exact tool call counts and breakdown
- Files read/written/edited (full paths)
- Web fetches and searches performed
- Estimated tokens and cost (using real pricing)
- Pre-built effort comparison table (agent vs. human)
- Session duration from timestamps

**Use this data directly** in Sections 4 and 6. Do not make up numbers.

### Step 1B: Load monthly cumulative stats

Add a "Monthly Context" callout to the meta-article:
> "This month, the system has produced X sessions, Y files, at an estimated cost of $Z — saving approximately $W compared to manual production."

### Step 1C: Gather session context

If running in the same session as the content work, you already have context. Otherwise:
1. Read session logs from your logs directory
2. Read conversation exports
3. Reconstruct what happened from files created/modified

---

## Phase 2: Load Voice Profile

Meta-articles are publishable content — they must match the client's voice.

1. Check for a voice profile for the client
2. If a voice profile exists, apply it to the meta-article writing
3. If writing for BlitzMetrics (no specific client), use Dennis Yu's voice: direct, specific, uses real names and numbers, conversational but authoritative
4. If no voice profile exists, use a neutral professional tone and note in the output that a voice profile should be created

**Voice rules that always apply:**
- Zero banned AI words (delve, landscape, leverage, utilize, harness, tapestry, multifaceted, robust, foster, holistic)
- Zero banned AI patterns ("In today's...", "It's important to note...", "When it comes to...")
- Active voice, short paragraphs (3-5 lines max), 15+ contractions per 1000 words
- Zero em dashes
- First sentence under 10 words

---

## Phase 3: Write the Meta-Article

### Title Format
"How We [Action] [Subject] [Context]"

### Required Sections (All 8 Must Be Present)

#### Section 1: Task Summary
- Assignment description
- Source material type and quantity (video, transcript, recording, existing content)
- Word counts / lengths of source material
- Goal category: honoring someone, repurposing video, topic coverage, authority building, client deliverable
- Client name and context

#### Section 2: Step-by-Step Process
Walk through every phase. Be specific with file names, tool counts, and timing:
- Source ingestion (files read, word counts — from metrics JSON `files.read`)
- Research performed (web searches — from metrics JSON `web.fetches`)
- Structural decisions with reasoning
- Writing and revision cycles
- Guideline compliance verification
- WordPress readiness prep
- Quality assurance checkpoints passed

#### Section 3: Critical Decision-Making
Highlight 3-5 judgment calls with reasoning. Examples:
- Selecting high-E-E-A-T quotes for leads
- Restructuring disorganized transcripts
- Choosing POV (first-person vs. third-person) and why
- Voice preservation vs. grammar cleanup tradeoffs
- Entity linking decisions
- Length decisions (depth-driven, not padding)

#### Section 4: Effort and Cost Comparison
**Auto-populated from metrics extractor.** Use the `effort_table` from the JSON directly:

| Task | Agent Time | Human Time | Agent Cost | Human Cost |
|------|-----------|------------|------------|------------|
| *(rows from your metrics extraction)* |
| **Total** | **Xmin** | **X.Xhrs** | **$X.XX** | **$XXX** |

Add the monthly context callout below the table.

Pricing references:
- Claude Opus 4.6: $15 input / $75 output per million tokens
- US marketer: $35/hour | Trained VA: $8/hour

#### Section 5: What the Agent Can and Cannot Do

**Autonomous:** Research, writing, voice matching, SEO metadata, internal link suggestions, guideline compliance, .docx generation, meta-article generation, QA scoring

**Human required:** WordPress login, featured image selection (real photos only), final approval, RankMath/LinkWhisper config, video embedding, notification to subject/client, social media posting

#### Section 6: Information Ingestion Inventory
**Auto-populated from metrics extractor:**
- Source documents: `files.read` count and list
- Web fetches: `web.fetches` count and URLs
- Searches: `web.searches` count
- Agents spawned: `web.agents_spawned`
- Estimated tokens: `tokens.estimated_total`
- Voice profile loaded: yes/no
- Guidelines/SOPs loaded: list

#### Section 7: Guidelines Compliance Scorecard
**Run the actual QA gate on the meta-article itself.** Load the Article QA skill and score:

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1-18 | *(full 18-step gate)* | PASS/PARTIAL/NEEDS HUMAN | |

Count: X PASS, Y PARTIAL, Z NEEDS HUMAN

#### Section 8: SEO Metadata
Generate for the meta-article itself:
- Title: under 60 characters
- Meta description: under 160 characters
- Primary keyword in first paragraph
- Suggested slug
- Suggested category and tags
- Internal link targets (to source articles and definitive articles)

---

## Phase 4: Entity Linking & SEO Enrichment

After writing, enhance with entity-aware linking:

1. **Identify entities** mentioned in the meta-article (people, companies, tools, frameworks)
2. **Check for existing definitive articles** on the client's site or blitzmetrics.com that cover those entities
3. **Insert 3-5 internal links** using descriptive anchor text (3-6 words, never "click here")
4. **Note external entity links** — if the meta-article mentions a person with a Knowledge Panel, link to their entity page
5. **Suggest schema markup** — meta-articles can carry Article schema with author, datePublished, about entities

---

## Phase 5: QA Gate (Run Article QA on the Meta-Article)

The meta-article is publishable content. It goes through the same quality gate as any article.

1. Load the [[skills/article-qa|Article QA]] skill
2. Run the Pre-Publish Gate (Steps 1-13) on the meta-article
3. Fix any BLOCK violations before outputting
4. Document WARN violations in the compliance scorecard (Section 7)
5. Note NEEDS HUMAN items for the reviewer

**The meta-article must pass QA before being marked complete.**

---

## Phase 6: Format and Output

1. **Generate .docx** using python-docx:
   - SOURCE VIDEO block at top (if applicable)
   - Meta description in italic
   - H1 (16pt bold), H2s (14pt bold), body (11pt, 1.15 spacing)
   - Bold key phrases, formatted tables for cost comparison
   - `[IMAGE: screenshot of process/tool]` placeholders

2. **Save to client content directory:**
   Your content pipeline under `meta-articles/meta-[slug]-YYYY-MM-DD.docx`

3. **Save markdown version:**
   Your content pipeline under `meta-articles/meta-[slug]-YYYY-MM-DD.md`

4. **Update tracking:**
   - Update ARTICLE_INDEX.csv if it exists
   - Log to your meta-article tracker

---

## Phase 7: Recursive Improvement Loop

After completing the meta-article, execute these checks:

### 7A: SOP Gap Detection
- Did the process reveal any SOP gaps or missing steps?
- If yes: update the relevant SOP immediately

### 7B: Pattern Detection
- Read the meta-article tracker
- Has the agent made the same mistake or hit the same friction point as a previous meta-article?
- If yes: update the root skill/SOP that caused the repeated issue

### 7C: Definitive Article Detection
- Count meta-articles per topic/framework in the tracker
- If 5+ meta-articles cover similar work (e.g., "article writing from transcripts"), suggest:
  > "There are now X meta-articles documenting [topic]. Consider consolidating into a definitive article at [client-site]/[topic-slug]/"
- A definitive article needs: clear definition, complete process, 10+ linked examples (the meta-articles), cross-links, CTA, short URL, visual diagram

### 7D: Good Examples Check
- If the owner approves the meta-article, offer to save to your good-examples library
- Max 5-7 examples in the library — replace weakest if at capacity

---

## Phase 8: Cumulative Dashboard Update

After generating, update the meta-article tracker:

```markdown
## Meta-Article Tracker

| Date | Client | Title | Articles Covered | Agent Cost | Human Equiv | Savings |
|------|--------|-------|-----------------|------------|-------------|---------|
| YYYY-MM-DD | Client | How We... | X articles | $X.XX | $XXX | XX% |
```

This creates a running record of how much value the system is producing — useful for client reports and proving ROI.

---

## Quality Gate (Final Checklist)

- [ ] All 8 sections present and substantive
- [ ] Cost/time data from metrics extraction (not estimated)
- [ ] Monthly cumulative context included
- [ ] Voice profile applied (or neutral + note to create one)
- [ ] Entity links inserted (3-5 internal links minimum)
- [ ] QA gate passed (0 BLOCK violations)
- [ ] Compliance scorecard honest (NEEDS HUMAN where applicable)
- [ ] At least 3 critical decisions documented with reasoning
- [ ] Zero banned words, zero banned patterns, zero em dashes
- [ ] .docx and .md generated and saved to correct directory
- [ ] Meta-article tracker updated
- [ ] SOP gap check completed
- [ ] Definitive article suggestion triggered (if 5+ on topic)

---

## Post-Publish Tracking

After the meta-article is published, verify it's contributing to organic visibility:
- **GSC:** Run `/gsc-insights` at 14 days to confirm indexing and check for impressions on the target keyword (typically "how we [action] [subject]" long-tail)
- **GA4:** Check page sessions and traffic source — meta-articles should pull organic traffic over time as they accumulate internal links from related content
- If the meta-article drives measurable organic traffic, flag it as a Dollar-a-Day candidate

## Examples to Study

- blitzmetrics.com/how-we-built-three-articles-three-youtube-videos/
- blitzmetrics.com/how-we-created-an-article-honoring-nathaniel-stevens/
- blitzmetrics.com/how-we-wrote-the-please-and-thank-you-article-using-ai/
- blitzmetrics.com/how-we-repurpose-a-marketing-mechanic-episode-into-a-definitive-article/
- blitzmetrics.com/meta-article-prompt-template/ (the prompt template itself)
- blitzmetrics.com/definitive-article-guide/ (how definitive articles work)

## See Also

- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[skills/article-writer|Article Writer]]
- [[skills/article-qa|Article QA]]
- [[skills/definitive-article|Definitive Article]]
