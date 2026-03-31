---
description: Full [Methodology Partner] article quality gate — severity-tiered checks, automated pre-QA, voice profile integration, and meta-article generation
category: client-work
created: 2026-03-19
last_updated: 2026-03-30
version: 2.0
canon_compliance: 03-article-guidelines.md, 07-quality-standards.md, 10-anti-vandalism-checklist.md
triangles: CCS (checklist implementation), MAA (quality measurement), LDT (meta-article teaches the process)
canon_sources: [03-article-guidelines.md, 07-quality-standards.md, 10-anti-vandalism-checklist.md]
tags:
  - type/sop
  - status/active
  - domain/client-work
  - topic/article-qa
  - topic/quality-gate
---

# Article QA — [Methodology Partner] Quality Gate (Full SOP)

## Purpose

Every article produced by the Content Engine, [[skills/content-repurposing|Content Repurposing Pipeline]], or any Claude session must pass this quality gate before publishing. This SOP implements the [Methodology Partner] article quality standards with severity-tiered checks that catch AI slop without flattening human voice.

**Skill version:** `skills/article-qa.md` — use the skill for quick execution. This SOP is the comprehensive reference.

## Philosophy

Articles should read like a knowledgeable person wrote them. The quality gate exists to catch two failure modes:
1. **AI slop** — generic, pattern-heavy, disconnected from source material
2. **Vandalism** — duplicate content, keyword cannibalization, broken internal linking

It does NOT exist to enforce arbitrary mechanical rules that make articles sound like they were written by someone trying not to sound like AI. That's its own tell.

**The good examples are the real standard.** When a rule contradicts an approved example in `good-examples/articles/`, the example wins and the rule needs updating.

## When to Use

- After any article is written (by AI or human)
- Before any article is published to WordPress
- During batch QA audits of previously published content
- As a training tool for new team members (LDT: they learn by checking, do by fixing, teach by documenting)

---

## Severity Tiers

Every check falls into one of three tiers. This replaces the old binary PASS/FAIL system.

| Tier | Meaning | Action Required |
|------|---------|----------------|
| **BLOCK** | Real problem. Always wrong. No exceptions. | Must fix before publishing. |
| **WARN** | Likely a problem. Usually needs fixing. | Fix, or document why it's intentional for this article. |
| **STYLE** | Judgment call. Depends on voice, context, article type. | Author's discretion. Not scored. |

**Publication rule:** 0 BLOCK violations required. WARN violations should be resolved or documented. STYLE items are never blockers.

---

## Automated Mechanical Checks (Pre-QA)

Before running the full gate on a batch of articles, run these automated checks. They catch the majority of BLOCK-tier violations faster than manual review.

### Step 1: The QA Audit Script

The `qa_audit.py` script scans every `.docx` file in a target folder. It checks for:

**BLOCK-tier scans:**
- **Banned words** (22 words — zero tolerance):
  `delve, landscape, realm, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, utilize, facilitate, leverage` (as verb), `streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon`

- **Banned AI patterns** (13 patterns — zero tolerance, regex required):
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
  - "Full stop." (as sentence-ending emphasis)

- **Banned salesy language** (5 patterns):
  `"limited time"`, `"what are you waiting for"`, `"act now"`, `"don't miss out"`, `"sign up today"`

**WARN-tier scans:**
- Em dashes (all Unicode variants: `—`, `–`, ` -- `) — zero unless voice profile permits
- Word count vs. target (flag if under 200 words)
- Zero contractions in 500+ words
- Internal links fewer than 2
- Paragraphs over 8 lines without a break

**Not scanned (STYLE tier — human judgment only):**
- Paragraph rhythm and variation
- Single rhetorical questions
- Passive voice usage
- Contraction density beyond the zero-check
- Opening hook quality

### Step 2: Categorize Violations by Fix Type

- **Mechanical fixes** (Python script): Banned words, missing contractions, em dashes
- **Pattern fixes** (parallel repair agents): Banned AI patterns — the entire sentence must be rewritten, not just the phrase swapped
- **Editorial fixes** (agent-assisted): Word count expansion, missing links — requires reading the transcript and adding real content

### Step 3: Fix Mechanical Issues

**Contraction replacement map:**
```
"do not" → "don't"       "is not" → "isn't"        "did not" → "didn't"
"does not" → "doesn't"   "was not" → "wasn't"       "has not" → "hasn't"
"cannot" → "can't"       "will not" → "won't"       "would not" → "wouldn't"
"could not" → "couldn't" "should not" → "shouldn't"
"that is" → "that's"     "it is" → "it's"           "there is" → "there's"
"I am" → "I'm"           "you are" → "you're"       "we are" → "we're"
"they are" → "they're"   "he is" → "he's"           "she is" → "she's"
"I have" → "I've"        "we have" → "we've"        "you have" → "you've"
"I would" → "I'd"        "you would" → "you'd"
"I will" → "I'll"        "you will" → "you'll"      "we will" → "we'll"
"let us" → "let's"
```

**CRITICAL — Post-contraction artifact scan:** After running contractions, scan for broken artifacts:
- `"doesn'thing"` — broken from "does nothing" (happened 59 times in Ryan D. Lee batch)
- `"you've a pile"` — sounds British; exclude "you have" when followed by a noun without "got"
- Lowercase `"i "` at start of sentences
- `"it'self"` or other mid-word breaks
- Run the artifact scan BEFORE proceeding. Every time.

### Step 4: Fix Pattern & Editorial Violations with Parallel Agents

- Group flagged articles by violation type
- Launch parallel repair agents: each reads the article, finds the flagged sentence, rewrites with a completely different construction (not a synonym swap)
- For short articles (<200 words), agents read the original transcript, identify expandable sections, add content grounded in the source material
- For missing internal links, agents search the client's site for related content and add contextual links

### Step 5: Re-Run Audit Until Clean

Repeat until 0 BLOCK violations. Log the final scorecard.

### Mechanical Check Pitfalls (Learned the Hard Way)

- **Contraction scripts break compound words.** "does nothing" → "doesn'thing." Always run artifact scan. (Ryan D. Lee project, 59 instances.)
- **"Not because X, but because Y" is the stealthiest pattern.** It reads naturally, so writers (human and AI) default to it. Appeared in 10/54 articles even with explicit instructions to avoid it.
- **"Limited time" false positives.** "I don't have unlimited time" contains "limited time" as a substring but is legitimate. Check sentence context before flagging.
- **Em dash check must catch all Unicode variants.** `—` (em dash), `–` (en dash), ` -- ` (double hyphen as em dash).
- **"Leverage" is only banned as a verb.** "Financial leverage" (noun) is fine. "Leverage your network" (verb) is banned.

---

## The Quality Gate — Full Detail

### Pre-Publish Gate (Steps 1-13)

All 13 steps must be checked before publishing. BLOCK-tier steps must pass. WARN-tier steps should pass or have documented exceptions.

#### Step 1: Requirements Gathered — BLOCK

- [ ] GCT (Goals, Content, Targeting) documented for this client
- [ ] Raw video source identified and accessible
- [ ] Tools accessible (text editor, WordPress, etc.)
- **PASS:** All three confirmed
- **FAIL:** No GCT or no source material
- **Human gate:** Client provides GCT

#### Step 2: Transcription Complete — BLOCK

- [ ] Video transcribed (Whisper, YouTube captions, or manual)
- [ ] Transcript reviewed and corrected for names, brands, technical terms
- [ ] Exported to shared drive
- **PASS:** Clean, reviewed transcript available
- **FAIL:** No transcription, or article written from scratch without source
- **Human gate:** Verifying name spellings

#### Step 3: Source Video Watched — BLOCK

- [ ] Writer watched complete source video (not just read transcript)
- [ ] Names, brands, tools verified against video
- [ ] Core message and key takeaways identified
- [ ] Filler and repeated content identified for exclusion
- **PASS:** Video watched, notes documented
- **FAIL:** Neither video watched nor transcript thoroughly reviewed
- **Human gate:** YES — watching video is a human task. AI cannot watch video. This is non-negotiable.

#### Step 4: Research & Anti-Vandalism — BLOCK

- [ ] Searched client's existing site for similar content
- [ ] Searched Google: `target keyword site:domain.com`
- [ ] If existing content found: enhancing, NOT duplicating
- [ ] Sub-topics identified from source (6-12 for long-form, 3-5 for short-form)
- **PASS:** Research complete, no duplication risk
- **FAIL:** No research done — potential keyword cannibalization
- **Human gate:** Judgment on whether to enhance existing or create new

#### Step 5: Article Written from Source — BLOCK

- [ ] Minimum 200 words (adjusted for topic depth — some topics warrant 500, some 3000)
- [ ] POV matches site type: 1st person = personal brand, 3rd person = agency/business
- [ ] Evergreen (no "this week," "recently," or other time-bound language unless the content is inherently time-bound)
- [ ] Uses speaker's actual words, stories, credentials, and data (E-E-A-T)
- [ ] Not generic — specifically tied to source material. A reader should be able to tell which video this came from.
- **PASS:** Article clearly sourced from transcript, proper POV, proper length
- **FAIL:** Generic content disconnected from source

#### Step 6: Title & Headings — WARN

- [ ] Title leads with or prominently features the main keyword
- [ ] Title is specific and searchable (not clever-but-vague)
- [ ] Single H1 (auto-generated by WordPress from title)
- [ ] H2s for major sections, H3s for subsections within H2s
- [ ] Headings aren't overused (not every 3-4 lines — they should mark genuine section breaks)
- **PASS:** SEO-forward title, clean heading hierarchy
- **FAIL:** Vague title or broken heading structure

#### Step 7: Strong Opening — WARN

The opening should make someone want to keep reading. How it does that is flexible.

- [ ] First paragraph establishes what the article is about and why it matters
- [ ] Context provided: who's featured, what their credentials are, what the source is
- [ ] No banned opening patterns ("In today's...", "In the world of...")

**What works (from approved examples):**
- Start with a striking fact or number: "$3 million. That's the portfolio you need..."
- Start with a bold claim: "Five myths still dominate the fitness industry."
- Start with a short, punchy sentence that sets the frame

**What doesn't work:**
- Generic preambles that could apply to any article on the topic
- Throat-clearing ("In this article, we'll explore...")
- Buried ledes where the interesting thing is in paragraph 3

- **Human gate:** Verify relationship context between people mentioned

#### Step 8: Multimedia Elements — WARN

- [ ] Featured image directly related to topic (not generic stock)
- [ ] 2+ inline images with alt text
- [ ] Real photos preferred (Google Photos, event photos, headshots)
- [ ] Images uploaded via WordPress Media Library
- **PASS:** Featured image + 2+ inline with alt text
- **Human gate:** Photo selection, WordPress upload

#### Step 9: Internal Linking — WARN

- [ ] 2+ internal links to related content on client's site
- [ ] Anchor text is 3-6 words, specific, descriptive (e.g., "the VAULT strategy" not "click here")
- [ ] No duplicate links (same URL linked twice)
- [ ] Links go to web pages only (not PDFs or raw video files)
- **PASS:** 2+ quality internal links with descriptive anchors

#### Step 10: Source Video Embedded — WARN

- [ ] Source video embedded at or near top of article
- [ ] Context paragraph explaining what the video is and who's in it
- **PASS:** Video embedded with context
- **Human gate:** YouTube upload, WordPress embed

#### Step 11: Language Quality — BLOCK / WARN / STYLE

This is the most nuanced step. See the three-tier breakdown:

**BLOCK — Zero Tolerance:**
- Zero banned words (see list above)
- Zero banned AI patterns (see list above)
- Zero banned salesy language (see list above)

**WARN — Fix Unless Intentional:**
- Walls of text (paragraphs over 8 lines without a break)
- Zero contractions in 500+ words (sounds robotic — use contractions naturally)
- Stacked rhetorical questions (2+ in a row is an AI tell)
- Em dashes present without voice profile authorization
- Generic filler sentences that add no information

**STYLE — Author's Judgment (Not Scored):**
- **Paragraph rhythm.** Vary it. One-sentence paragraphs for emphasis. Longer paragraphs for complex explanations. Don't flatten everything to a uniform length. The Ryan D. Lee example uses everything from one-line punches to six-line explanations — that's the rhythm of good writing.
- **Single rhetorical questions.** A well-placed question can be the strongest line in the piece. "Is that number enough?" works. Three questions in a row doesn't.
- **Passive voice.** Active voice is the default, but passive has legitimate uses. "The store was founded in 1985" is better than contorting the sentence to make it active when the founder isn't the point. Use passive when it serves clarity or emphasis.
- **Sentence-ending prepositions.** Not a real grammar rule. Never was. Write naturally.
- **Contraction frequency.** The old rule said "15+ contractions." The real rule: use contractions the way the speaker would talk. For a personal brand, that's a lot. For a formal business, maybe fewer. Match the voice.

#### Step 12: WordPress Post — BLOCK

- [ ] Title, body, featured image, metadata all present
- [ ] Saved as draft and previewed before publish
- [ ] URL slug is clean and keyword-rich (no WordPress auto-generated gibberish)
- **PASS:** Correctly posted and previewed
- **Human gate:** WordPress login, visual preview, publish decision

#### Step 13: Categorized & Tagged — WARN

- [ ] WordPress category aligned to [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]] (WHY / HOW / WHAT)
- [ ] Relevant tags added (not excessive — 3-7)
- [ ] RankMath/Yoast focus keyword set
- [ ] Meta description written by a human or carefully reviewed AI draft (not auto-generated)
- **PASS:** All four items complete
- **Human gate:** Topic Wheel alignment judgment

---

### Post-Publish Workflow (Steps 14-18)

These are distribution and measurement steps. They happen AFTER publishing and do NOT block publication. Track them separately.

#### Step 14: Cross-Posted to Social

- [ ] Shared on Facebook (profile + page)
- [ ] Shared on LinkedIn
- [ ] Shared on Twitter/X
- [ ] Relevant people tagged
- [ ] Tracked in Content Library
- **Human gate:** Platform logins, per-platform formatting

#### Step 15: Added to Content Library

- [ ] Article logged with URL, title, date, category
- [ ] Topic Wheel position tagged (WHY / HOW / WHAT)
- [ ] Authority score assigned (What/Who/Where from 3 Components of Authority)
- [ ] Dollar-a-Day candidate flagged if high-authority

#### Step 16: Dollar-a-Day Evaluation

- [ ] Organic performance checked after initial posting (1,000 views OR 100+ engagements)
- [ ] If qualifies: added to Dollar-a-Day testing queue
- [ ] If not yet: scheduled for re-evaluation in 2 weeks
- **Human gate:** Budget decisions for ad spend

#### Step 17: MAA Tracking

- [ ] Article metrics included in next weekly MAA report
- [ ] Page views, time on page, bounce rate tracked
- [ ] Compared against same Topic Wheel category

#### Step 18: Iterate

- [ ] Performance reviewed after 2 weeks
- [ ] If underperforming: title updated, multimedia added, linking improved
- [ ] If performing: repurposed into additional formats (social, email, video clips)
- [ ] Fed back into Content Factory loop (Perform → Process)
- **Human gate:** Strategic judgment on iteration approach

---

## Voice Profile Integration

Different clients have different voices. The QA gate should flex accordingly.

**Before running QA on a client's articles, check for a voice profile:**
`~/Documents/Claude/PRISM/content-pipeline/voice-profiles/[client-slug].md`

If a voice profile exists, it may override STYLE-tier defaults:
- Some clients use em dashes (override the default WARN)
- Some clients are more formal (fewer contractions is appropriate)
- Some clients use specific catchphrases or signature phrases that should be present

If no voice profile exists, use these defaults:
- Conversational but professional tone
- Contractions used naturally throughout
- No em dashes
- Active voice preferred

---

## Scoring

For each article, produce a scorecard:

```
Article: [Title]
Client: [Name]
Source: [Transcript/Video]
Date: [YYYY-MM-DD]

BLOCK violations: X → [list each]
WARN violations: Y → [list each]
STYLE notes: Z → [list each, informational only]
NEEDS HUMAN: W steps → [list each]

Decision:
- 0 BLOCK, 0 WARN → Ready to publish
- 0 BLOCK, WARN present → Fix or document, then publish
- Any BLOCK → Must fix, cannot publish
- NEEDS HUMAN → Route to [Your Name] for those steps
```

---

## Meta-Article Generation ([Your Mentor/Advisor]'s LDT Concept)

After every article or batch passes QA, generate a companion meta-article documenting:

1. **Source material:** What video/transcript, length, date
2. **Process:** How the article was created (AI-assisted? Manual? Batch?)
3. **Decisions made:** Why this angle? Why this title? What was cut?
4. **Effort comparison:** Time to create vs. manual equivalent
5. **What required human intervention:** And why AI couldn't do it
6. **Quality scorecard:** Results from the gate
7. **Lessons learned:** What should improve for next batch

Save to: `~/Documents/Claude/PRISM/content-pipeline/meta/[client]/[article-slug]-meta.md`

---

## Human Gates Summary

| Step | Gate Type | Why It Can't Be Automated |
|------|-----------|--------------------------|
| 1 | Execute | Client must articulate their own goals |
| 3 | Execute | AI cannot watch video — human verifies context, tone, intent |
| 4 | Review | Enhance vs. create new requires editorial judgment |
| 7 | Review | Verifying real-world relationships between people mentioned |
| 8 | Execute | Photo selection must use real photos, uploaded via WordPress |
| 10 | Execute | Video must be uploaded to YouTube and embedded by human |
| 12 | Execute | WordPress login, visual preview, publish decision |
| 13 | Review | Topic Wheel category alignment requires strategic judgment |
| 16 | Approve | Financial decisions on ad spend |
| 18 | Review | Strategic judgment on iteration approach |

---

## Anti-Vandalism Checks

Per canon (`10-anti-vandalism-checklist.md`):

- [ ] Search client's existing site for similar content before writing (Step 4)
- [ ] Search Google: `target keyword site:domain.com` to check for cannibalization
- [ ] If existing content found: enhance the existing page, do NOT create a duplicate
- [ ] Verify internal linking structure maintained (no orphaned or broken links)
- [ ] Confirm Topic Wheel position doesn't conflict with existing published content
- [ ] Check Content Library for overlapping topics before creating

**Vandalism vs. Improvement (from canon):**
- **Vandalism:** Creating duplicate articles, diverging from canon, auto-publishing without QA, removing working processes
- **Improvement:** Updating existing articles with fresh content, matching SOPs to canon, running full QA, flagging unclear steps

---

## Self-Reinforcing QA Loop

1. Every article checked → scorecard generated
2. BLOCK and WARN failures logged to: `~/Documents/Claude/PRISM/content-pipeline/qa-failures.md`
3. Weekly retrospective reads failures → identifies recurring patterns
4. Patterns become skill/SOP updates (e.g., "articles keep failing Step 7 → update article-writer prompt for stronger hooks")
5. Updated prompts produce better articles
6. Better articles produce fewer failures
7. The loop compounds

---

## Learnings Log

- **2026-03-18 (Ryan D. Lee):** First audit found 27 violations across 54 articles. After two repair rounds: 0. Most common: "not because X, but because Y" (10 articles), word count under 1200 (11 articles).
- **2026-03-18:** Mechanical fixes (contractions + banned words) should always run as a Python script first. Pattern and editorial fixes require agent-level reasoning. Don't automate pattern rewrites with regex.
- **2026-03-18:** Running the QA audit as a Python script (not asking Claude to read each article) is dramatically faster. Build the script once, reuse across clients.
- **2026-03-18:** Contraction scripts broke 59 instances of "does nothing" → "doesn'thing" in Ryan D. Lee batch. Post-contraction artifact scan is now mandatory.
- **2026-03-21:** Consolidated mechanical checks SOP into this file. Single source of truth.
- **2026-03-30:** v2.0 overhaul. Replaced binary PASS/FAIL with severity tiers (BLOCK/WARN/STYLE). Removed robotic rules that contradicted approved good examples: hard contraction counts, blanket rhetorical question ban, rigid paragraph length rules, sentence-ending preposition ban. Separated pre-publish gate (Steps 1-13) from post-publish workflow (Steps 14-18). Added voice profile integration.
- **2026-03-30 (retro):** Session b7969ae9 ran 4 QA cycles on the "Uber of Digital Marketing" article rewrite. Key finding: multi-cycle QA (write → QA → refine → QA again) produces significantly better results than single-pass. Recommend standardizing at 2 QA passes minimum for client-facing articles. First pass catches BLOCK/WARN violations; second pass catches pattern-level issues that only emerge after mechanical fixes are applied.
- **2026-03-30 (retro):** Session 7387455e ([Client — Local Retail Business] batch) found that sub-agents writing articles in parallel do NOT follow the QA SOP unless the full SOP text is passed inline. File path references are insufficient — sub-agents can't load PRISM skills. Always embed the QA checklist directly in the sub-agent prompt for batch production.

---

## Related

- [Skill: Article QA](../../skills/article-qa.md) — compact executable version
- [Canon: Article Guidelines](../../blitzmetrics-canon/03-article-guidelines.md)
- [Canon: Quality Standards](../../blitzmetrics-canon/07-quality-standards.md)
- [Canon: Anti-Vandalism](../../blitzmetrics-canon/10-anti-vandalism-checklist.md)
- [Article Writer Skill](../../skills/article-writer.md)
- [Content Repurposing Skill](../../skills/content-repurposing.md)
- [Good Examples](../../skills/good-examples/)
- [QA Scorecard Template](../templates/qa-scorecard-template.md)

## See Also

- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[blitzmetrics-canon/07-quality-standards|Quality Standards]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[skills/article-qa|Article QA Skill]]
- [[skills/article-writer|Article Writer]]
- [[skills/content-repurposing|Content Repurposing]]
- [[blitzmetrics-canon/06-topic-wheel|Topic Wheel]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]