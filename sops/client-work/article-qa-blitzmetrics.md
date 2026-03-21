---
description: Full BlitzMetrics 18-step article quality gate with PASS/PARTIAL/FAIL scoring and meta-article generation
category: client-work
created: 2026-03-19
last_updated: 2026-03-21
version: 1.2
canon_compliance: 03-article-guidelines.md, 07-quality-standards.md, 10-anti-vandalism-checklist.md
triangles: CCS (checklist implementation), MAA (quality measurement), LDT (meta-article teaches the process)
canon_sources: [03-article-guidelines.md, 07-quality-standards.md, 10-anti-vandalism-checklist.md]
---

# Article QA — BlitzMetrics 18-Step Quality Gate

## Purpose

Every article produced by the Content Engine, Content Repurposing Pipeline, or any Claude session must pass this quality gate before being marked "done." This SOP implements the FULL BlitzMetrics 18-step article quality checklist as documented in ~/Documents/Claude/Mainframe/blitzmetrics-canon/03-article-guidelines.md.

## When to Use

- After any article is written (by AI or human)
- Before any article is published to WordPress
- During batch QA audits of previously published content
- As a training tool for new team members (LDT: they learn by checking, do by fixing, teach by documenting)

## Canon Reference

This SOP implements the canonical article guidelines from blitzmetrics.com/blog-posting-guidelines/ and the BlitzMetrics Master Content Factory Guides. Every check traces to a canonical source.

## Automated Mechanical Checks (Pre-QA)

Before running the 18-step gate on a batch of articles, run these automated mechanical checks first. They catch the majority of violations faster than manual review.

### 1. Write and Run the QA Audit Script

Create `qa_audit.py` to scan every `.docx` file in the target folder. The script checks:

- **Banned words** (zero tolerance): `delve, landscape, realm, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, utilize, facilitate, leverage` (as verb), `streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt`
- **Banned AI patterns** (zero tolerance — regex required):
  - "not because X, but because Y"
  - "this is where X comes in"
  - "put it this way"
  - "here's the thing"
  - "it's not just X, it's Y"
  - "let that sink in"
  - "full stop"
  - "in today's [anything]"
  - "at the end of the day"
- **Banned salesy language:** "limited time", "what are you waiting for", "act now", "don't miss out", "sign up today"
- **Structural checks:** em dashes (zero allowed unless voice profile specifies), word count vs. target, first sentence under 10 words, internal links (2+), signature phrase present, contraction count (15+), no "In conclusion" or equivalent

Run: `python3 qa_audit.py` — output is pass/fail per article with specific violations.

### 2. Categorize Violations by Fix Type

- **Mechanical fixes** (automated): Banned words, missing contractions, em dashes. Fix with Python find-and-replace.
- **Pattern fixes** (semi-automated): Banned AI patterns. The sentence must be rewritten entirely, not just the phrase swapped. Use parallel repair agents.
- **Editorial fixes** (agent-assisted): Word count expansion, missing signature phrases, missing internal links. Requires reading the transcript and adding real content.

### 3. Fix Mechanical Issues with Python

Contraction replacement map:
```
"do not" → "don't", "is not" → "isn't", "did not" → "didn't"
"does not" → "doesn't", "was not" → "wasn't", "has not" → "hasn't"
"cannot" → "can't", "will not" → "won't", "would not" → "wouldn't"
"could not" → "couldn't", "should not" → "shouldn't"
"that is" → "that's", "it is" → "it's", "there is" → "there's"
"I am" → "I'm", "you are" → "you're", "we are" → "we're"
"they are" → "they're", "he is" → "he's", "she is" → "she's"
"I have" → "I've", "we have" → "we've", "you have" → "you've"
"I would" → "I'd", "you would" → "you'd"
"I will" → "I'll", "you will" → "you'll", "we will" → "we'll"
"let us" → "let's"
```

**Post-contraction artifact scan (CRITICAL):** After running contractions, scan for broken artifacts:
- "you've a pile" (should remain "you have a pile" — exclude "you have" when followed by a noun without "got")
- "doesn'thing" (broken from "does nothing")
- Lowercase "i " at start of sentences

### 4. Fix Pattern & Editorial Violations with Parallel Agents

- Group flagged articles by violation type
- Launch parallel repair agents: each reads the article, finds the flagged sentence, rewrites with a completely different construction
- For short articles, agents read the original transcript, identify expandable sections, add 200-500 words grounded in the transcript

### 5. Re-Run Audit Until Clean

Repeat until the audit returns 0 violations. Log the final scorecard.

### Mechanical Check Pitfalls

- **Contraction scripts break compound words.** "does nothing" → "doesn'thing." Always run a post-contraction artifact scan. This happened on 59 instances in the Ryan D. Lee project.
- **"Not because X, but because Y" is the stealthiest pattern.** It reads naturally so writers (human and AI) default to it. Appeared in 10/54 articles even with explicit instructions to avoid it.
- **"Limited time" false positives.** "I don't have unlimited time" contains "limited time" as a substring but is legitimate. Check the full sentence context before flagging.
- **Contraction of "you have" creates British English.** "You've got" is fine. "You've a pile" sounds British and wrong for American voice profiles.
- **Em dash check must catch all Unicode variants.** Check for `—` (em dash), `–` (en dash), and ` -- ` (double hyphen used as em dash).

---

## The 18-Step Quality Gate

### Pre-Writing Phase

#### Step 1: Requirements Gathered
- [ ] GCT (Goals, Content, Targeting) documented for this client
- [ ] Raw video source identified and accessible
- [ ] Text editor and tools accessible
- **PASS:** All three confirmed
- **PARTIAL:** GCT exists but video source unclear
- **FAIL:** No GCT or no source material
- **Human Required:** Client provides GCT

#### Step 2: Transcription Complete
- [ ] Video uploaded to Drive and transcribed
- [ ] Transcript reviewed and corrected
- [ ] Exported to shared drive
- **PASS:** Clean, reviewed transcript available
- **PARTIAL:** Raw transcript used without review
- **FAIL:** No transcription — article written from scratch without source
- **Human Required:** Verifying name spellings in transcript

#### Step 3: Source Video Watched
- [ ] Writer watched complete source video
- [ ] Names, brands, tools spelled correctly
- [ ] Filler words identified and removed from transcript
- [ ] Core message and key takeaways identified
- **PASS:** Video watched, notes documented
- **PARTIAL:** Transcript reviewed but video not watched
- **FAIL:** Neither done
- **Human Required:** YES — watching video is a human task. AI cannot watch video.

#### Step 4: Research & Anti-Vandalism Check
- [ ] Searched client's existing site for similar content
- [ ] Searched Google for target keyword + site:domain
- [ ] If existing content found: enhancing, NOT duplicating
- [ ] 6-12 sub-topics identified from source
- [ ] Multimedia gathered (photos, clips, headshots)
- **PASS:** Research complete, no duplication risk
- **PARTIAL:** Partial research, duplication risk unknown
- **FAIL:** No research done — potential keyword cannibalization
- **Human Required:** Judgment on whether to enhance existing vs. create new

### Writing Phase

#### Step 5: Article Written from Source
- [ ] Minimum 200 words
- [ ] Point-of-view matches site type (1st person = personal brand, 3rd person = agency)
- [ ] Evergreen (no specific dates or limited-time references)
- [ ] Uses speaker's actual words and stories (E-E-A-T)
- [ ] Not generic AI output — specifically tied to source material
- **PASS:** Article clearly sourced from transcript, proper POV, proper length
- **FAIL:** Generic content disconnected from source

#### Step 6: Title & Headings
- [ ] Title starts with main keyword
- [ ] Title is specific, sharp, searchable
- [ ] Single H1 (auto-generated by WordPress)
- [ ] H2s for sections, H3s for subsections
- [ ] No heading abuse (headings not every 3-4 lines)
- **PASS:** SEO-friendly title, clean heading hierarchy
- **FAIL:** Vague title or broken heading structure

#### Step 7: Engaging Hook
- [ ] First line grabs attention
- [ ] Context provided (who's featured, how connected, event)
- [ ] If figurehead: why they're worth listening to
- [ ] Central question answered in first paragraph
- [ ] First sentence under 10 words
- **PASS:** Strong hook with context
- **PARTIAL:** Good hook but missing context
- **FAIL:** Generic opening (banned patterns: "In today's...", "In the world of...")
- **Human Required:** Verifying relationship context between people

#### Step 8: Multimedia Elements
- [ ] Featured image directly related to topic
- [ ] 2+ inline images with alt text and captions
- [ ] Real photos (not stock — Google Photos, event photos)
- [ ] Images uploaded via WordPress Media Library
- **PASS:** Featured image + 2+ inline with alt text
- **PARTIAL:** Featured image only
- **FAIL:** No images
- **Human Required:** Photo selection, WordPress upload

#### Step 9: Internal Linking
- [ ] 2+ internal links to related content on client sites
- [ ] Anchor text is 3-6 words, specific, descriptive
- [ ] No "click here" or generic anchor text
- [ ] No repeated links
- [ ] Links go to web pages only (not PDFs or video files)
- **PASS:** 2+ quality internal links
- **FAIL:** No internal links or generic anchors

#### Step 10: Source Video Embedded
- [ ] Source video placed at top of article
- [ ] Context paragraph explaining video origin
- **PASS:** Video embedded with context
- **PARTIAL:** Video linked but not embedded
- **FAIL:** No video reference
- **Human Required:** YouTube upload, WordPress embed

### Quality Assurance Phase

#### Step 11: Proofread — Language Quality
- [ ] Zero banned words (delve, landscape, realm, paradigm, synergy, game-changer, revolutionize, cutting-edge, harness, utilize, facilitate, leverage-as-verb, streamline, robust, foster, spearhead, holistic, ecosystem, empower, pivot, disrupt, beacon)
- [ ] Zero banned AI patterns ("In today's [noun]...", "It's important to note...", "Whether you're a... or a...", "At the end of the day...", "In the world of...", "[Topic] is not just about...", "When it comes to...", "In conclusion...", "As we navigate...")
- [ ] Zero banned salesy language ("Don't miss out!", "Act now!", "Limited time!", "You won't believe...", "Secret to...")
- [ ] Active voice throughout
- [ ] Paragraphs 3-5 lines
- [ ] No rhetorical questions
- [ ] No sentences ending with prepositions
- [ ] 15+ contractions (natural speech)
- [ ] No broken contraction artifacts
- **PASS:** Zero violations across all categories
- **FAIL:** Any violation present

#### Step 12: Posted to WordPress
- [ ] Title, body, featured image, metadata all present
- [ ] Saved as draft, previewed before publish
- [ ] URL slug is clean and keyword-rich
- **PASS:** Correctly posted and previewed
- **Human Required:** WordPress login, visual preview, publish button

#### Step 13: Categorized & Tagged
- [ ] WordPress category aligned to Topic Wheel
- [ ] Relevant tags added (not excessive)
- [ ] RankMath/Yoast focus keyword set
- [ ] Meta description written (not auto-generated)
- **PASS:** All four items complete
- **PARTIAL:** Categorized but missing meta description
- **Human Required:** Topic Wheel alignment judgment

### Publishing Phase

#### Step 14: Cross-Posted to Social
- [ ] Shared on Facebook (profile + page)
- [ ] Shared on LinkedIn (broetry format)
- [ ] Shared on Twitter
- [ ] Relevant people tagged
- [ ] Tracked in Content Library
- **PASS:** Cross-posted to 3+ platforms
- **Human Required:** Platform logins, formatting per platform

#### Step 15: Added to Content Library
- [ ] Article logged with URL, title, date, category
- [ ] Topic Wheel position tagged
- [ ] Authority score (What/Who/Where) assigned
- [ ] Dollar-a-Day candidate flagged if high-authority
- **PASS:** Complete entry with scoring

#### Step 16: Dollar-a-Day Evaluation
- [ ] Organic performance checked (1,000 views OR 100+ engagements)
- [ ] If qualifies: added to Dollar-a-Day testing queue
- [ ] If not yet: scheduled for re-evaluation in 2 weeks
- **PASS:** Evaluated and actioned
- **Human Required:** Budget decisions for Dollar-a-Day spend

#### Step 17: MAA Tracking
- [ ] Article metrics included in next weekly MAA report
- [ ] Page views, time on page, bounce rate tracked
- [ ] Compared against same Topic Wheel category
- **PASS:** Included in MAA with metrics

#### Step 18: Iterate
- [ ] Performance reviewed after 2 weeks
- [ ] If underperforming: title updated, multimedia added, linking improved
- [ ] If performing: repurposed into additional formats
- [ ] Fed back into Content Factory loop (Perform → Process)
- **PASS:** Action taken based on data
- **Human Required:** Strategic judgment on iteration approach

---

## Scoring Summary

For each article, produce a scorecard:

| Step | Status | Notes |
|------|--------|-------|
| 1. Requirements | PASS/PARTIAL/FAIL/NEEDS HUMAN | |
| 2. Transcription | PASS/PARTIAL/FAIL/NEEDS HUMAN | |
| ... | ... | ... |
| 18. Iterate | PASS/PARTIAL/FAIL/NEEDS HUMAN | |

**Overall score:** X/18 PASS, Y PARTIAL, Z FAIL, W NEEDS HUMAN

**Publication decision:**
- 18/18 PASS → Ready to publish
- Any PARTIAL → Fix before publishing
- Any FAIL → Must fix, cannot publish
- NEEDS HUMAN items → Route to human for completion

---

## Meta-Article Generation (Dennis's Concept)

After every article passes QA, generate a companion meta-article documenting:

1. **Source material:** What video/transcript was used, length, date
2. **Process:** How the article was created (AI-assisted? Fully manual?)
3. **Decisions made:** Why this angle? Why this title? What was cut?
4. **Effort comparison:** Time to create vs. manual equivalent
5. **What the agent couldn't do:** What required human intervention and why
6. **Quality scorecard:** Full 18-step scorecard results
7. **Lessons learned:** What should improve for next article

Save meta-articles to: ~/Documents/Claude/Mainframe/content-pipeline/meta/[client]/[article-slug]-meta.md

This implements Dennis's LDT principle: each article teaches the next person how to create one.

---

## Self-Reinforcing QA Loop

1. Every article checked against 18-step guidelines → scorecard
2. Failed checks logged to: ~/Documents/Claude/Mainframe/content-pipeline/qa-failures.md
3. Weekly retrospective reads QA failures → identifies patterns
4. Patterns become SOP updates (e.g., "articles keep failing Step 7 → update Content Engine prompt for stronger hooks")
5. Updated SOPs produce better articles on next run
6. Better articles produce fewer QA failures
7. The loop compounds

---

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Step 1: Client provides GCT | Execute | Client must articulate goals themselves |
| Step 3: Source video watched | Execute | AI cannot watch video — human must verify context, tone, intent |
| Step 4: Anti-vandalism judgment | Review | Deciding whether to enhance existing vs. create new requires editorial judgment |
| Step 7: Relationship context verification | Review | Verifying figurehead relationships between people mentioned |
| Step 8: Photo selection and WordPress upload | Execute | Featured image must be real photo, uploaded via WordPress |
| Step 10: YouTube upload and embed | Execute | Video must be uploaded and embedded by human |
| Step 12: WordPress publishing | Execute | Human login, visual preview, publish button |
| Step 13: Topic Wheel alignment | Review | Category/tag selection requires strategic judgment |
| Step 16: Dollar-a-Day budget decisions | Approve | Financial decisions on ad spend |
| Step 18: Iteration strategy | Review | Strategic judgment on whether to update, repurpose, or archive |

## Anti-Vandalism Checks
- [ ] Search client's existing site for similar content before writing (Step 4)
- [ ] Search Google for target keyword + site:domain to check for cannibalization
- [ ] If existing content found: enhance, do not duplicate
- [ ] Verify internal linking structure maintained (no orphaned or broken links)
- [ ] Confirm Topic Wheel position does not conflict with existing published content

## Learnings Log

- **2026-03-18 (Ryan D. Lee):** First audit found 27 violations across 54 articles. After two repair rounds: 0. Most common: "not because X, but because Y" (10 articles), word count under 1200 (11 articles).
- **2026-03-18:** Mechanical fixes (contractions + banned words) should always be done first as a Python script. Pattern and editorial fixes require agent-level reasoning. Don't try to automate pattern rewrites with regex replacement.
- **2026-03-18:** Running the QA audit as a Python script (not asking Claude to read each article) is 100x faster and catches everything. Build the script once, reuse across clients.
- **2026-03-21:** Merged article-qa-compliance.md (mechanical checks SOP) into this file as the "Automated Mechanical Checks (Pre-QA)" section. Single source of truth for all article QA.
