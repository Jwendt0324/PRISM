# Overnight Task: [Methodology Partner] Drive Ingestion + 9 Triangles Alignment + Full QA System

## Instructions for Claude Code

Copy everything below the line into Claude Code and let it run overnight. This is the most important upgrade to the PRISM since it was built. It aligns everything with [Your Mentor/Advisor]'s canonical frameworks.

---

You are performing a comprehensive upgrade to [Your Name]'s Claude PRISM. [Your Mentor/Advisor] ([Your Name]'s co-founder and mentor) reviewed the PRISM and identified critical gaps. This overnight run addresses ALL of his feedback by ingesting the canonical [Methodology Partner] training materials, aligning every SOP with the 9 Triangles framework, and building a self-reinforcing QA system.

**CRITICAL: Only scan the Gmail account [your-email@your-agency.com] for any Gmail operations.**

## [Your Mentor/Advisor]'s Feedback (Address Every Point)

1. "Consider centralizing certain functions in the cloud to avoid duplicate setup" — Document what should be local vs cloud. Add backup recommendations.
2. "Where are the QA checks beyond mechanical gating?" — Build real quality gates against [Methodology Partner] article guidelines.
3. "Watch for accidental vandalism; this document contains many assumptions that contradict what we teach" — Audit every SOP against the 9 Triangles and canonical Content Factory processes. Fix contradictions.
4. "You'd need to connect other data systems and tools" — Document what data connections are needed and which are available.
5. "Consider whether this can operate without humans in the loop" — Explicitly define where humans are required in every process.
6. "Ask Claude what you might be missing or what you might not want to hear" — Run a brutally honest self-assessment of the PRISM.

---

## PHASE 1: INGEST THE BLITZMETRICS CANON (2-4 hours)

The entire [Methodology Partner] shared drive is synced locally via Google Drive for Desktop at:
~/Library/CloudStorage/GoogleDrive-[your-email@your-agency.com]/Shared drives/[Methodology Partner] Drive/

**IMPORTANT:** This is a HUGE drive with hundreds of files including videos, audio, images, and documents. This overnight run focuses ONLY on readable text documents (PDFs, .docx, .txt, .md). Do NOT attempt to read, download, or process any video or audio files. Those will be handled in a future run.

### Step 1A: Build a File Index (Documents Only — Skip All Media)

Scan the drive for READABLE DOCUMENTS ONLY. Create a master index at ~/Documents/Claude/PRISM/blitzmetrics-canon/00-drive-index.md.

**SKIP ENTIRELY (do not list, do not index, do not attempt to read):**
- All video files: .mp4, .mov, .MP4, .MOV, .m4a, .mp3, .wav
- All image files: .jpg, .jpeg, .png, .HEIC, .gif, .bmp
- All installer files: .dmg, .zip, .7z
- All iphone backup folders
- All folders that are clearly personal media (photo albums, "[Your Mentor/Advisor]'s Zoom Recordings", etc.)

**INDEX AND READ these file types only:**
- .pdf (the Master Guides and training docs live here)
- .docx (SOWs, guides, training materials)
- .doc (older training docs)
- .txt and .md (notes, scripts, guides)
- .gdoc and .gsheet files: these are Google-native format link stubs on disk. Run `cat` on each one — if it contains a URL, log the URL and title. The actual content lives online and can't be read from the filesystem. Just note what they are.

**For the index, organize by category:**
- Training & Curriculum (guides, courses, workbooks)
- Client SOPs & Templates (access audits, content libraries, SOWs)
- Marketing & Sales (presentations, sales decks, proposals)
- Legal & Business (agreements, contracts, articles of organization)
- Process & Operations (checklists, trackers, workflows)

Flag the top 20-30 most important documents for deep reading in Step 1B.

### Step 1B: Deep-Read Priority Documents (Training & Frameworks First)

**READ ORDER:** Start with the Master Guides and training PDFs — these contain the canonical frameworks. Then read templates and SOPs. Skip individual client folders for now (e.g., "[Client — Local Retail Business] - Jeremy Chapman", "American Classic Painters") — those are implementations, not the source methodology.

Read these files IN FULL (they contain the canonical frameworks):

**Master Guides (read all versions, use the latest):**
- Master Content Factory Guide - CoachYu.pdf
- Master Content Factory Guide - Content Factory (2).pdf
- Master Content Factory Guide - Content Factory (3).pdf
- Master Content Factory Guide - Content Factory (4).pdf
- Master Content Factory Workbook - Content Factory.pdf
- Master Operations Process Guide - Content Factory.pdf
- Master Video Editing Process Guide .pdf
- content_factory_course_builder_guide_v9.1_2023_0822.pdf
- master_content_factory_guide_v1.2_2023_1229.pdf

**Dollar-a-Day:**
- blitz_facebook_for_a_dollar_a_day_guide_v13.9_2020_0717.gdoc (or .pdf version)
- dollar_a_day_webinar_deck_guide_v1.1_2023_0419.gslides
- dollar_a_day_webinar_deck_presentation_v1.2_2023_0420.pdf
- content_factory_dollar-a-day_program_presentation_v1.4_2023_0503.pdf

**Design & Style:**
- coachyu_design_style_guide_v3.6_2022_0121.gdoc

**Templates & SOPs:**
- Master Access Checklist - Content Factory.pdf
- MAA Weekly Report Template.gdoc
- Example MAA for Local Services.gdoc
- FullFunnels Public - Checklist Standardized Template.gdoc
- Sample TEMPLATE [Methodology Partner] Access Audit April 6, 2023.gdoc
- Local Citations Guide & Checklist .gdoc

**Training Materials:**
- [Industry Conference] 2025_ Content Factory Guide.pdf
- NYC [Industry Conference] 2024_ Content Factory Guide (1).pdf
- Applied Digital Marketing: Collaborations with Local Businesses.gdoc
- Book: How to Produce a Best-Seller Book.gdoc
- The Art of Personal Branding: Define , Develop, and Deliver.gdoc

**Client Examples (to understand how processes are applied):**
- Any SOW files (Statement of Work) — these show the actual deliverables
- Any Content Library .gsheet files — these show how content is tracked
- Any Access Audit .gdoc files — these show the audit process

**Folders to explore deeply:**
- [Methodology Partner] Assets & Processes/
- TEMPLATES/
- Marketing Mechanic/
- Grokipedia Training/
- [Your Agency] - Training Content Webinars/
- Local Service Spotlight/

### Step 1C: Extract and Document Every Framework

Create these files in ~/Documents/Claude/PRISM/blitzmetrics-canon/:

**01-nine-triangles.md** — The complete 9 Triangles framework:
- WHY tier: SBP (Specialist, Business, Partner)
- HOW tier: ACC (Awareness, Consideration, Conversion), MAA (Metrics, Analysis, Action), GCT (Goals, Content, Targeting)
- WHAT tier: DDD (Do, Delegate, Delete), CID (Communicate, Iterate, Delegate), LDT (Learn, Do, Teach), CCS (Content, Checklist, Software), MOF (Marketing, Operations, Finance)
- For each triangle: definition, when to apply, how it connects to the others, common violations

**02-content-factory-process.md** — The canonical 4+1 stage Content Factory:
- Plumbing (Stage 0): GMB, tracking, analytics, workflows
- Produce: Capture from existing activities
- Process: Transform using AI tools
- Post: Distribute across channels
- Promote: Dollar-a-Day amplification
- Include exact steps, quality gates, and handoff points from the Master Guide

**03-article-guidelines.md** — The complete 18-step article quality checklist from [methodology-partner.com]/blog-posting-guidelines/, plus any additional rules found in the Drive docs:
1. Upload video
2. Transcribe
3. Watch video
4. Research & prepare
5. Write article from transcript
6. Craft title & headings
7. Write engaging hook
8. Include multimedia
9. Link to relevant content
10. Embed source video
11. Proofread thoroughly
12. Post on WordPress
13. Categorize & add keywords
14-18. [Extract remaining steps from Drive docs]

**04-dollar-a-day.md** — The canonical Dollar-a-Day strategy with exact phases, budgets, metrics

**05-maa-framework.md** — Metrics, Analysis, Action framework in full detail with templates

**06-topic-wheel.md** — The Topic Wheel methodology (WHY outer → HOW middle → WHAT center)

**07-quality-standards.md** — Every quality standard found across all [Methodology Partner] docs:
- Article quality standards
- Video quality standards
- Site build quality standards
- Client communication standards
- Reporting standards

**08-human-requirements.md** — Where humans are REQUIRED in every process (addressing [Your Mentor/Advisor]'s point #6):
- Client relationships and communication
- Operations management and payroll
- WordPress publishing (login, featured image, RankMath)
- Content approval before publishing
- Financial decisions and pricing
- Quality review and final sign-off
- Photography and real-world content capture
- Strategic pivots and business decisions

**09-data-connections-needed.md** — What data systems the PRISM should connect to (addressing [Your Mentor/Advisor]'s point #5):
- YouTube Analytics API (video performance)
- Google Analytics (site traffic)
- Google Search Console (ranking data)
- Stripe (revenue tracking)
- Basecamp (project management)
- WordPress (content publishing)
- Facebook Ads Manager (Dollar-a-Day performance)
- For each: what data it provides, how to access it, cost, complexity

**10-anti-vandalism-checklist.md** — Rules to prevent "unintentional well-meaning vandalism":
- Always check what already exists before creating new content
- Never cannibalize existing ranking pages
- SOPs must reference the canonical source, not approximations
- Content tree structure must be verified before publishing
- Changes to methodology require [Your Mentor/Advisor]'s review
- Agent output must be QA'd against article guidelines before publishing
- If unsure whether something contradicts the canon, flag it for human review

---

## PHASE 2: AUDIT AND REWRITE EVERY PRISM SOP (2-3 hours)

### Step 2A: Load the Canon
Read all files in ~/Documents/Claude/PRISM/blitzmetrics-canon/ that you just created.

### Step 2B: Audit Every SOP
For each SOP in ~/Documents/Claude/PRISM/sops/:

1. Read the SOP
2. Cross-check EVERY claim, process step, and recommendation against the [Methodology Partner] canon
3. Check for:
   - Contradictions with the 9 Triangles (does this SOP violate any triangle's principles?)
   - Missing MAA loops (does this SOP measure its own success?)
   - Missing human checkpoints (does this SOP assume full automation where humans are needed?)
   - Incorrect Content Factory stages (are the stages right? Is the order right?)
   - Missing quality gates (does this SOP have real QA, not just mechanical checks?)
   - Anti-vandalism risks (could following this SOP create unintentional damage?)
   - LDT violations (does this SOP teach without doing first? Does it claim mastery without evidence?)

4. For each issue found:
   - Document the specific violation
   - Reference the canonical source that it contradicts
   - REWRITE the SOP to fix the violation
   - Add a "Canon Compliance" section to the SOP noting which [Methodology Partner] standards it follows
   - Bump the version number

### Step 2C: Save the Audit Report
Create ~/Documents/Claude/PRISM/blitzmetrics-canon/sop-audit-report.md:
- Every SOP audited with pass/fail per category
- Every violation found with the specific fix applied
- SOPs that were rewritten vs unchanged
- Remaining risks or ambiguities

---

## PHASE 3: BUILD THE ARTICLE QA SYSTEM (1-2 hours)

### Step 3A: Create the Article QA SOP
Create ~/Documents/Claude/PRISM/sops/client-work/article-qa-blitzmetrics.md

This SOP implements the FULL [Methodology Partner] 18-step article quality checklist as an automated gate. Every article produced by the Content Engine or any Claude session must pass this before being marked "done."

For each of the 18 steps:
- Define what "PASS" looks like
- Define what "PARTIAL" looks like
- Define what "FAIL" looks like
- Define what requires HUMAN input (cannot be automated)
- Include the specific check to run

Add [Your Mentor/Advisor]'s meta-article concept: after every article is written and passes QA, generate a companion document explaining how it was created, what decisions were made, effort comparison, and what the agent couldn't do.

### Step 3B: Update the Content Engine Integration
Read ~/Documents/Claude/PRISM/sops/client-work/content-repurposing-pipeline.md and add:
- A mandatory "[Methodology Partner] QA Gate" step after article writing
- Reference to the article-qa-blitzmetrics.md SOP
- The meta-article generation step
- Anti-vandalism check (verify against existing content tree before publishing)

### Step 3C: Create the Self-Reinforcing QA Loop
This is the key innovation [Your Mentor/Advisor] is pushing for. Build a system where:

1. Every article is checked against the 18-step guidelines
2. Every check produces a scorecard (PASS/PARTIAL/NEEDS HUMAN per item)
3. Failed checks are logged to a QA failures file
4. The weekly retrospective reads QA failures and identifies patterns
5. Patterns become SOP updates (e.g., "articles keep failing step 7 because hooks are too generic" → update Content Engine prompt)
6. Updated SOPs produce better articles on the next run
7. Better articles produce fewer QA failures
8. The loop compounds

Create ~/Documents/Claude/PRISM/sops/templates/qa-scorecard-template.md with:
- All 18 [Methodology Partner] article guidelines as checkable items
- PASS / PARTIAL / NEEDS HUMAN scoring
- Space for specific notes on each item
- Link to the canonical source for each guideline

---

## PHASE 4: HONEST SELF-ASSESSMENT (30 min)

[Your Mentor/Advisor] said "ask Claude what you might be missing or what you might not want to hear."

Create ~/Documents/Claude/PRISM/blitzmetrics-canon/honest-assessment.md

Be brutally honest about:

1. **What the PRISM does well:** What actually works and produces value?
2. **What the PRISM gets wrong:** Where does it contradict [Methodology Partner] methodology? Where are the approximations that could cause harm?
3. **What's missing:** What capabilities does it need that it doesn't have?
4. **Where humans are still essential:** What does the PRISM pretend to automate but actually can't?
5. **The biggest risk:** What's the most dangerous thing the PRISM could do if left unchecked?
6. **What [Your Name] might not want to hear:** Is the PRISM solving real business problems or creating the feeling of progress? Is it producing publishable content or just drafts that need extensive human review? Is the time spent building infrastructure being offset by actual revenue?
7. **Comparison to [Your Mentor/Advisor]'s meta-article approach:** How does the PRISM's approach compare? Where is [Your Mentor/Advisor]'s approach better? What should [Your Name] adopt from it?
8. **The gap between building and executing:** [Your Mentor/Advisor]'s key message was "shift from idea to execution." Is the PRISM helping with execution or delaying it?

---

## PHASE 5: UPDATE EVERYTHING (30 min)

### Update INDEX.md
- Add blitzmetrics-canon/ section
- Update SOP dates for any rewritten SOPs
- Add the Article QA SOP to the active list

### Update CLAUDE.md
Add to the "ON SESSION START" section:
"CANON COMPLIANCE: All SOPs and content must comply with the [Methodology Partner] 9 Triangles framework documented in ~/Documents/Claude/PRISM/blitzmetrics-canon/. When in doubt, check the canon before proceeding. Never create content that contradicts the canonical Content Factory process, MAA framework, or article guidelines."

### Update CONTEXT.md
Regenerate the compressed context file to include:
- 9 Triangles summary
- Article QA gate requirement
- Human-required checkpoints
- Anti-vandalism rules

### Regenerate .docx Copies
```bash
cd ~/Documents/Claude/PRISM/sops && python3 convert_sops_to_docx.py
```

### Write Session Log
Document everything that was done, every SOP that was rewritten, every violation found.

---

## Rules

- This runs overnight. Be exhaustive.
- The [Methodology Partner] canon is the SOURCE OF TRUTH. If a PRISM SOP contradicts a [Methodology Partner] document, the PRISM SOP is wrong.
- [Your Mentor/Advisor]'s feedback is not optional — every point must be addressed.
- The honest self-assessment must be genuinely honest, not diplomatic. [Your Name] needs to hear the hard truths.
- For .gdoc/.gsheet files on the Drive: these are link files, not readable documents. Try `cat` on them — if they contain a URL, note the URL. The actual content lives in Google Docs online and is not accessible from the filesystem. Focus on .pdf, .docx, .txt, and .md files.
- Videos (.mp4, .mov) cannot be read. Note their existence in the index but don't try to process them.
- If you find conflicting information in different versions of [Methodology Partner] docs, use the LATEST version.
- When rewriting SOPs, preserve any valid learnings and processes — only change what contradicts the canon.
- Log everything.

---

## See Also
- [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]
- [[INDEX|Master Index]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory Process]]
- [[blitzmetrics-canon/sop-audit-report|SOP Audit Report]]
- [[blitzmetrics-canon/03-article-guidelines|Article Guidelines]]
- [[claude-code/overnight-full-overhaul|Full Overhaul]]
