---
name: Article QA
version: 1.1
description: Run the [Methodology Partner] 18-step article quality gate on any article
triggers:
  - article QA
  - article quality check
  - compliance check
  - 18-step gate
  - proofread article
  - article review
  - [Your Mentor/Advisor] review
canon_source: blitzmetrics-canon/03-article-guidelines.md
full_sop: sops/client-work/article-qa-blitzmetrics.md
triangles: [CCS, MAA, LDT]
---

# Article QA — Executable Skill

## When to Run

- After any article is written (by AI or human)
- Before any article is published to WordPress
- During batch QA audits of existing content
- As final gate before handoff to human reviewer

## The 18-Step Gate (Execute in Order)

### Pre-Writing (Steps 1-4)

| # | Check | PASS Criteria | Human? |
|---|-------|---------------|--------|
| 1 | Requirements | GCT documented, video source identified, tools accessible | Client provides GCT |
| 2 | Transcription | Clean, reviewed transcript available and exported | Verify name spellings |
| 3 | Source Video Watched | Video watched, names/brands verified, core message identified | YES — AI cannot watch video |
| 4 | Research & Anti-Vandalism | Searched site for similar content, no duplication risk, 6-12 sub-topics identified | Judgment on enhance vs. create new |

### Writing (Steps 5-10)

| # | Check | PASS Criteria | Human? |
|---|-------|---------------|--------|
| 5 | Article from Source | 200+ words, correct POV, evergreen, uses speaker's real words, tied to source | No |
| 6 | Title & Headings | Keyword-first title, clean H1/H2/H3 hierarchy, no heading abuse | No |
| 7 | Engaging Hook | First sentence under 10 words, context provided, no banned opening patterns | Verify relationship context |
| 8 | Multimedia | Featured image + 2 inline images with alt text, real photos not stock | YES — photo selection, WP upload |
| 9 | Internal Links | 2+ internal links, 3-6 word descriptive anchors, no "click here", no duplicates | No |
| 10 | Source Video Embed | Video at top of article with context paragraph | YES — YouTube upload, WP embed |

### Quality Assurance (Steps 11-13)

| # | Check | PASS Criteria | Human? |
|---|-------|---------------|--------|
| 11 | Proofread | Zero banned words, zero banned patterns, zero salesy language, active voice, 15+ contractions, paragraphs 3-5 lines, no rhetorical questions | No |
| 12 | WordPress Post | Title, body, featured image, metadata present, draft previewed | YES — WP login, visual preview |
| 13 | Categorized & Tagged | Category aligned to Topic Wheel, tags added, RankMath focus keyword, meta description written | Topic Wheel alignment judgment |

### Publishing (Steps 14-18)

| # | Check | PASS Criteria | Human? |
|---|-------|---------------|--------|
| 14 | Cross-Posted | Shared on Facebook, LinkedIn, Twitter, people tagged, tracked in Content Library | YES — platform logins |
| 15 | Content Library | Logged with URL, title, date, category, Topic Wheel position, authority score | No |
| 16 | Dollar-a-Day Eval | Organic performance checked (1,000 views OR 100+ engagements), queued if qualifies | YES — budget decisions |
| 17 | MAA Tracking | Metrics in next weekly MAA report, page views/time/bounce tracked | No |
| 18 | Iterate | Performance reviewed after 2 weeks, action taken (update, repurpose, or archive) | YES — strategic judgment |

## Automated Mechanical Checks (Run These BEFORE the 18-Step Gate)

For batch AI-written articles, run automated pre-QA mechanical checks first. Full details including the Python QA audit script, contraction replacement map, artifact scan, and parallel repair agent workflow are in the consolidated SOP: `sops/client-work/article-qa-blitzmetrics.md` (section: "Automated Mechanical Checks (Pre-QA)").

Summary of automated checks:

1. **Run `qa_audit.py`** — scans all .docx files for banned words (22), banned AI patterns (9 regex), banned salesy language (5), and structural violations (em dashes, word count, first sentence length, contractions, internal links)
2. **Fix mechanical issues** — Python script for contraction replacement + banned word removal. Run post-contraction artifact scan (watch for "doesn'thing", "you've a pile", lowercase "i")
3. **Fix pattern violations** — launch parallel repair agents to rewrite flagged sentences (not regex swap)
4. **Fix editorial issues** — agents read transcript, expand short articles, add missing signature phrases/links
5. **Re-run audit** until 0 violations
6. **Anti-vandalism:** search for topic overlap with existing content

## Scoring

For each article, produce a scorecard:

```
Article: [Title]
Source: [Transcript/Video]

Steps PASS: X/18
Steps PARTIAL: Y
Steps FAIL: Z
Steps NEEDS HUMAN: W

Publication Decision:
- 18/18 PASS = Ready to publish
- Any PARTIAL = Fix before publishing
- Any FAIL = Must fix, cannot publish
- NEEDS HUMAN = Route to [Your Name]
```

## Meta-Article (Generate After QA)

Document for every batch: source material, process used, decisions made, effort comparison, what required human intervention, scorecard results, lessons learned. Save to `~/Documents/Claude/Mainframe/content-pipeline/meta/[client]/[slug]-meta.md`

## Self-Reinforcing Loop

1. QA failures logged to `~/Documents/Claude/Mainframe/content-pipeline/qa-failures.md`
2. Weekly retrospective reads failures, identifies patterns
3. Patterns become SOP/skill updates (e.g., "articles keep failing Step 7 > update prompt for stronger hooks")
4. Better prompts > fewer failures > the loop compounds
