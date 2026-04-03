---
name: Article QA
version: 2
description: Run the BlitzMetrics article quality gate on any article
triggers:
  - article QA
  - article quality check
  - compliance check
  - quality gate
  - proofread article
  - article review
  - Dennis review
canon_source: blitzmetrics-canon/03-article-guidelines.md
full_sop: sops/client-work/article-qa-blitzmetrics.md
triangles:
  - CCS
  - MAA
  - LDT
tags:
  - status/active
  - triangle/CCS
  - triangle/MAA
  - type/skill
---

# Article QA — Executable Skill

## When to Run

- After any article is written (by AI or human)
- Before any article is published to WordPress
- During batch QA audits of existing content
- As final gate before handoff to human reviewer

## Philosophy

The goal is articles that read like a knowledgeable person wrote them — not articles that survived a compliance checklist. Rules catch AI slop. Judgment catches everything else. When a rule and a good example conflict, study the example. This skill enforces the [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]] and [[blitzmetrics-canon/07-quality-standards|Quality Standards]].

**Before running QA:** Load approved examples from your good-examples library. These are the real standard.

---

## Severity Tiers

Every check falls into one of three tiers:

| Tier | Meaning | Action |
|------|---------|--------|
| **BLOCK** | Cannot publish. Always a real problem. | Must fix before publishing |
| **WARN** | Likely a problem. Fix unless you have a good reason not to. | Fix or document why it's intentional |
| **STYLE** | Judgment call. Depends on voice, context, intent. | Author's discretion |

---

## Pre-Publish Gate (Steps 1-13)

These must be checked before an article can be published.

### Source & Setup (Steps 1-4)

| # | Check | PASS Criteria | Tier | Human? |
|---|-------|---------------|------|--------|
| 1 | Requirements | GCT documented, video source identified | BLOCK | Client provides GCT |
| 2 | Transcription | Clean, reviewed transcript available | BLOCK | Verify name spellings |
| 3 | Source Video Watched | Video watched, names/brands verified, core message identified (see [[blitzmetrics-canon/08-human-requirements|Human Requirements]]) | BLOCK | YES — AI cannot watch video |
| 4 | Anti-Vandalism | Searched site for existing content, no duplication risk, sub-topics identified (see [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]) | BLOCK | Judgment on enhance vs. create new |

### Content Quality (Steps 5-10)

| # | Check | PASS Criteria | Tier | Human? |
|---|-------|---------------|------|--------|
| 5 | Written from Source | 200+ words, correct POV, evergreen, uses speaker's real words and stories (E-E-A-T) | BLOCK | No |
| 6 | Title & Headings | Keyword-forward title, clean H1/H2/H3 hierarchy | WARN | No |
| 7 | Strong Opening | Opening grabs attention, provides context, establishes why the reader should care | WARN | Verify relationship context |
| 8 | Multimedia | Featured image + 2 inline images with alt text, real photos not stock | WARN | YES — photo selection, WP upload |
| 9 | Internal Links | 2+ internal links, descriptive anchors (3-6 words), no "click here" | WARN | No |
| 10 | Source Video Embed | Video embedded at top with context paragraph | WARN | YES — YouTube upload, WP embed |

### Language & Publishing Prep (Steps 11-13)

| # | Check | PASS Criteria | Tier | Human? |
|---|-------|---------------|------|--------|
| 11 | Language Quality | Zero banned words, zero banned AI patterns, zero salesy language. Natural voice throughout. (See Language Quality detail below.) | BLOCK/WARN/STYLE | No |
| 12 | WordPress Post | Title, body, featured image, metadata present, draft previewed | BLOCK | YES — WP login, visual preview |
| 13 | Categorized & Tagged | Category aligned to Topic Wheel, RankMath focus keyword, meta description written | WARN | Topic Wheel alignment judgment |

---

## Post-Publish Workflow (Steps 14-18)

These happen AFTER publishing. They do NOT block publication.

| # | Check | What Happens | Human? |
|---|-------|-------------|--------|
| 14 | Cross-Post to Social | Share on Facebook, LinkedIn, Twitter. Tag relevant people. | YES — platform logins |
| 15 | Content Library | Log URL, title, date, category, Topic Wheel position, authority score | No |
| 16 | Dollar-a-Day Eval | Check organic performance (1,000 views OR 100+ engagements). Queue if qualifies. | YES — budget decisions |
| 17 | MAA Tracking | Include in next weekly MAA report | No |
| 18 | Iterate | Review after 2 weeks. Update, repurpose, or archive based on data. | YES — strategic judgment |
| 19 | GA4/GSC Validation | After 7-14 days: check GA4 for article page sessions and engagement (avg time on page, bounce rate). Run `/gsc-insights` to verify target keywords are indexed, check impressions, clicks, CTR, and average position. Flag articles with zero impressions after 14 days for indexing issues. | No — data pull is automated |

---

## Step 11 Detail: Language Quality

This is where most QA gets too robotic. Here's how to think about it:

### BLOCK — Always Fix (Zero Tolerance)

**Banned words:** delve, landscape, realm, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, utilize, facilitate, leverage (as verb), streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon

**Banned AI patterns:**
- "In today's [noun]..."
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

**Banned salesy language:** "limited time", "what are you waiting for", "act now", "don't miss out", "sign up today"

### WARN — Fix Unless Intentional

- **Walls of text:** Paragraphs over 8 lines with no break
- **Zero contractions** in 500+ words (sounds robotic)
- **Generic content** disconnected from the source transcript
- **Stacked rhetorical questions** (2+ in a row = AI pattern)
- **Em dashes** — zero allowed unless client voice profile explicitly permits them

### STYLE — Author's Judgment

- **Paragraph length variation.** One-sentence paragraphs for emphasis are good. Vary the rhythm. Don't flatten everything to the same length.
- **Single rhetorical question.** One well-placed question in a 1000+ word article can be powerful.
- **Passive voice.** Default to active, but passive is fine when the subject isn't the point. "The store was founded in 1985" is better than forcing active.
- **Sentence-ending prepositions.** This is not a real rule. Write naturally.
- **Contraction density.** Use contractions the way the speaker would talk. Don't count them.

---

## Automated Pre-QA (For Batch Processing)

Before running the full gate on a batch, run automated mechanical checks. Full details including the Python QA audit script spec, contraction replacement map, artifact scan, and parallel repair workflow are in the full SOP: `sops/client-work/article-qa-blitzmetrics.md`.

Summary:
1. Run `qa_audit.py` — scans .docx files for BLOCK-tier violations
2. Fix mechanical issues (banned words, missing contractions) via Python
3. Fix pattern violations via parallel repair agents (rewrite, don't regex-swap)
4. Fix editorial issues (short articles, missing links) — agents read transcript
5. Re-run audit until 0 BLOCK violations
6. Anti-vandalism: search for topic overlap with existing content

---

## Scoring

```
Article: [Title]
Source: [Transcript/Video]

BLOCK violations: X (must be 0 to publish)
WARN violations: Y (fix or document)
STYLE notes: Z (author discretion)
NEEDS HUMAN: W steps

Decision:
- 0 BLOCK + 0 WARN = Publish
- 0 BLOCK + WARN present = Fix warnings or document why they're intentional, then publish
- Any BLOCK = Must fix, cannot publish
- NEEDS HUMAN = Route to reviewer
```

---

## Self-Reinforcing Loop

1. QA failures get logged to a qa-failures tracker
2. Weekly retrospective reads failures and identifies patterns
3. Patterns become skill/SOP updates
4. Better prompts result in fewer failures — the loop compounds

---

## Connected Skills

| After QA | Skill |
|----------|-------|
| Document the process | `/meta-article` |
| Prep for WordPress | `/wp-publisher` |
| Generate social posts | `/social-content` |
| Update Basecamp | `/basecamp-ops` |
| Batch more articles | `/batch-content` |

## References

- [Canon: Article Guidelines](../blitzmetrics-canon/03-article-guidelines.md)
- [Canon: Quality Standards](../blitzmetrics-canon/07-quality-standards.md)
- [Full SOP: Article QA](../sops/client-work/article-qa-blitzmetrics.md)
- [Article Writer Skill](article-writer.md)

## See Also

- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/07-quality-standards|Quality Standards]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[skills/article-writer|Article Writer]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[sops/client-work/article-qa-blitzmetrics|Article QA SOP]]
