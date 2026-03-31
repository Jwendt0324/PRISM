---
name: Definitive Article Generator
version: 1
description: Create the canonical reference article for a [Methodology Partner]/[Your Agency]
  concept — the SEO Tree "branch" that meta-articles link back to
triggers:
  - definitive article
  - canonical article
  - pillar content
  - hub article
  - consolidate articles
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
    - meta-article
    - keyword-research
    - entity-builder
  after:
    - schema-markup
    - wp-publisher
    - social-content
    - geo-optimizer
---

# Definitive Article Generator — Executable Skill

## What Is a Definitive Article?

A definitive article is the single canonical reference for a concept, following the [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]. It's the hub that other content (case studies, meta-articles, course pages) links back to. In the SEO Tree: trunk = brand entity, **branches = definitive articles**, leaves = [[skills/meta-article|meta-articles]] and supporting content organized by the [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]].

"The definitive article gives away the knowledge; the course sells the structure."

**Source:** [methodology-partner.com]/definitive-article-guide/

---

## When to Run

- When the meta-article tracker shows 5+ meta-articles covering similar work
- When creating a new canonical resource for a [Methodology Partner]/[Your Agency] framework
- When consolidating scattered content about one topic into a single authoritative page
- When [Your Name] says "we need a definitive article on [topic]"

---

## Phase 0: Load Good Examples + Research Existing

1. Check `~/Documents/Claude/PRISM/skills/good-examples/definitive-articles/` for approved examples
2. Study [methodology-partner.com]/dad (Dollar a Day — gold standard definitive article)
3. Search the target site for existing partial coverage: `site:[domain] [topic]`
4. Read the meta-article tracker for related meta-articles to consolidate

---

## Phase 1: Identify & Audit

1. **Search for existing content** on the target site covering this topic
2. **Categorize** what exists: partial coverage, outdated, fragmented across pages
3. **Decision:** Enhance existing page OR create new canonical URL
4. **List all meta-articles** that should link back to this definitive article

---

## Phase 2: Nine Non-Negotiable Requirements

Every definitive article must satisfy ALL nine:

### 1. Clear Opening Definition
Reader understands what the concept is and why it matters before scrolling. Definition in first two paragraphs using plain language.

### 2. Complete Process or Framework
Full SOP with all stages, steps, or components. For multi-stage concepts (like Content Factory), walk through each phase systematically. This transforms description into an actionable manual.

### 3. Extensive Real Examples
Link to as many examples as exist. Meta-articles are your example library. Each example gets a one-to-two sentence description + link. More examples = stronger SEO + better AI training data.

**Minimum:** 10+ linked real-world examples (more is better)

### 4. Cross-Links to Related Concepts
Connect to other definitive articles covering adjacent topics. Creates an interconnected entity graph, not isolated pages.

**Minimum:** 3+ cross-links to related definitive articles

### 5. Course or Service CTA
If training or execution services exist, link as conversion path. But the article gives away the knowledge freely.

### 6. Blog Posting Guidelines Compliance
All [Methodology Partner] standards: title < 60 chars, meta description < 160 chars, keyword in first paragraph, H2/H3 structure, short paragraphs, active voice, no AI fluff, internal linking via entity decision tree.

### 7. Dedicated Short URL
Create a permanent redirect (e.g., `/dad` for Dollar a Day, `/cf` for Content Factory) that becomes the canonical address for all internal references.

**Suggest:** `/[2-4 letter abbreviation]`

### 8. Visual Diagram (If Multi-Component)
If the concept has multiple stages, components, or sub-components, include a clickable diagram above the fold. Each element links to relevant sections or related definitive articles.

**Output:** `[DIAGRAM: description of what diagram should show, components, links]` placeholder with full spec

### 9. Third-Party Endorsements & E-E-A-T Signals
Collect and include: media coverage, conference presentations, practitioner testimonials, independent reviews, industry endorsements.

"A strategy can be accurate, but without third-party validation it does not carry the same weight."

---

## Phase 3: Write the Definitive Article

### Structure Template

```markdown
# [Concept Name]: [What It Does in One Line]

[Opening definition — two paragraphs, plain language, why it matters]

[DIAGRAM: clickable visual of the framework/process — above the fold]

## What Is [Concept]?
[Expanded definition with context and origin story]

## How [Concept] Works
### Stage/Step 1: [Name]
[Complete walkthrough with actionable detail]
### Stage/Step 2: [Name]
...

## Real Examples
### [Example 1 Title]
[1-2 sentence description] — [Link]
### [Example 2 Title]
...
(minimum 10 examples, each with description + link)

## Who Uses [Concept]
[Practitioner testimonials, case studies, named people with real results]

## Related Frameworks
[Cross-links to 3+ other definitive articles]

## Get Started
[CTA — course, service, or free resource link]

## Third-Party Validation
[Media mentions, conference talks, endorsements]
```

### Voice Rules
- Same as all [Methodology Partner] content: zero banned words, zero AI patterns, active voice, contractions
- Load voice profile if writing for a specific client
- First-person if from [Your Mentor/Advisor] or the subject matter expert
- Third-person if editorial/institutional

---

## Phase 4: Consolidation (When Building from Meta-Articles)

When consolidating 5+ meta-articles into a definitive article:

1. **Read all related meta-articles** from the tracker
2. **Extract the common process** they all document — this becomes the "How It Works" section
3. **Each meta-article becomes an example** in the "Real Examples" section
4. **Aggregate cost data** from meta-articles: "Across X sessions, this process saved $Y vs. manual production"
5. **Identify the definitive process** — the repeating steps across all meta-articles become the canonical SOP
6. **Update all meta-articles** to link back to the new definitive article

---

## Phase 5: SEO & Entity Enrichment

1. **Run `/keyword-research`** for the topic — identify primary keyword, related terms, search volume
2. **Run `/entity-builder`** — check if the concept has a Knowledge Graph entity, note KGMID
3. **Run `/schema-markup`** — generate Article schema with:
   - `@type`: Article or HowTo (depending on content)
   - `about`: entity references
   - `author`: speaker/expert entity
   - `datePublished`, `dateModified`
   - `mainEntity`: the concept being defined
4. **Run `/geo-optimizer`** — check AI citability, optimize for AI Overviews

---

## Phase 6: QA Gate

Run the full 18-step [Methodology Partner] QA gate (see [[skills/article-qa|Article QA]]) on the definitive article. Additionally check:

- [ ] All 9 non-negotiable requirements met
- [ ] 10+ linked examples with descriptions
- [ ] 3+ cross-links to related definitive articles
- [ ] Short URL suggested
- [ ] Diagram spec included (if multi-component)
- [ ] Third-party endorsements present
- [ ] CTA links to real course/service
- [ ] Schema markup generated
- [ ] Zero banned words, zero AI patterns
- [ ] Keyword research incorporated

---

## Phase 7: Output

1. **Generate .docx** — same formatting as regular articles
2. **Save to:** `~/Documents/Claude/PRISM/content-pipeline/[client]/definitive-articles/definitive-[slug]-YYYY-MM-DD.docx`
3. **Save markdown:** alongside as `.md`
4. **Generate schema markup** in separate file: `schema-[slug].json`
5. **Update meta-article tracker** — mark which meta-articles now link to this definitive article
6. **Generate a meta-article** documenting the creation of the definitive article (recursive!)

---

## Phase 8: Post-Publish Checklist (For Human)

After [Your Name] publishes the definitive article:

- [ ] Create short URL redirect (e.g., `/cf` → full URL)
- [ ] Update all meta-articles with links back to this definitive article
- [ ] Update older articles that reference this concept to link here
- [ ] Add to site navigation if it's a core concept
- [ ] Submit to Google Search Console for indexing
- [ ] Run `/social-content` for launch posts
- [ ] Track in weekly MAA report

---

## Connected Skills

| Step | Skill | Purpose |
|------|-------|---------|
| Before writing | `/keyword-research` | Target keywords and search volume |
| Before writing | `/entity-builder` | Check Knowledge Graph entity status |
| After writing | `/schema-markup` | Generate JSON-LD schema |
| After writing | `/article-quality-gate` | Run 18-step QA |
| After writing | `/meta-article` | Document the creation process |
| After writing | `/wp-publisher` | Prep for WordPress |
| After writing | `/geo-optimizer` | Optimize for AI search |
| After writing | `/social-content` | Generate launch posts |

## See Also

- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]]
- [[skills/article-qa|Article QA]]
- [[skills/article-writer|Article Writer]]
- [[skills/meta-article|Meta-Article]]

## Examples to Study

- [methodology-partner.com]/dad — Dollar a Day (gold standard)
- [methodology-partner.com]/blog-posting-guidelines/ — Blog Posting Guidelines (68 inbound links)
- [methodology-partner.com]/meta-article-prompt-template/ — Meta-Article Prompt (29 examples)
- [methodology-partner.com]/definitive-article-guide/ — The definitive article about definitive articles