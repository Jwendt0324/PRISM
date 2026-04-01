# Overnight Task: Full Content Audit & Backlog Processor

## Instructions for Claude Code

Copy everything below the line into Claude Code and let it run overnight.

---

You are running an overnight content audit and backlog processing task for {{USER_NAME}}'s {{AGENCY_NAME}} business. This is a large, multi-hour task. Be thorough — {{USER_NAME}} will review results in the morning.

## Context

Read these files first to understand the business, SOPs, and publishing targets:
- ~/Documents/Claude/PRISM/INDEX.md
- ~/Documents/Claude/PRISM/sops/business-ops/hri-offer-ladder-and-gtm.md
- ~/Documents/Claude/PRISM/sops/client-work/article-writing-from-transcripts.md
- ~/Documents/Claude/PRISM/sops/client-work/youtube-transcript-scraping.md
- ~/Documents/Claude/PRISM/sops/client-work/podcast-transcript-scraping.md
- ~/Documents/Claude/PRISM/sops/client-work/article-qa-blitzmetrics.md
- ~/Documents/Claude/PRISM/sops/client-work/content-factory-execution.md

## Phase 1: Local Media Inventory (30-60 min)

Scan {{USER_NAME}}'s entire machine for raw content assets. Search these locations:
- ~/Desktop/ (all subfolders)
- ~/Downloads/
- ~/Documents/
- ~/Movies/
- ~/Music/

For each location, catalog:
- Video files (.mp4, .mov, .avi, .mkv, .webm)
- Audio files (.m4a, .mp3, .wav, .aac)
- Transcripts (.vtt, .srt, .txt files that look like transcripts)
- Documents that could be content sources (.docx, .pdf with article/interview content)

Create a master inventory at ~/Documents/Claude/PRISM/content-audit/01-local-media-inventory.md with:
- File path
- File type
- File size
- Last modified date
- Brief description of what it appears to be (based on filename/content)
- Status: "unprocessed" / "partially processed" / "published" (guess based on context)

## Phase 2: Online Presence Audit (60-90 min)

Scrape and catalog {{USER_NAME}}'s existing published content across these channels. Use web search and direct URL fetching:

### YouTube
- Search "{{USER_NAME}}" on YouTube — catalog all videos (title, date, views, URL)
- Search "{{AGENCY_NAME}}" on YouTube — catalog all videos
- Search "[Your Mentor/Advisor] {{USER_NAME}}" — find any collaboration content

### Websites
- Crawl [your-agency-domain.com] — catalog all published pages, blog posts, academy content
- Crawl [your-username].com (if it exists) — catalog everything
- Search [advisor-website.com] for any {{USER_NAME}} mentions/articles
- Search [methodology-partner.com] for any {{USER_NAME}} content
- Search [ops-partner-website.com] for {{USER_NAME}} mentions

### Social & Professional
- Search LinkedIn for {{USER_NAME}} posts/articles (via web search)
- Search SlideShare for {{USER_NAME}} decks
- Search for any podcast appearances (via web search: "{{USER_NAME}} podcast" OR "{{USER_NAME}} interview")

### Press & Mentions
- Search for "{{USER_NAME}}" + "{{AGENCY_NAME}}" across news/press
- Search for any speaking engagements, conference mentions
- Check for Google Knowledge Panel status for {{USER_NAME}}

Create a master online inventory at ~/Documents/Claude/PRISM/content-audit/02-online-presence-audit.md with:
- Platform
- Content title
- URL
- Date published (if available)
- Type (video, article, podcast, deck, etc.)
- Engagement metrics (if visible)

## Phase 3: Gap Analysis vs Publishing Calendar (30-45 min)

Cross-reference the [Your Agency] Standalone Plan's publishing targets against what actually exists:

### Next 20 Videos to Make (from GTM plan):
1. {{USER_NAME}}'s origin story
2. Parent explainer — "Why certification beats a semester"
3. Student pitch — "Get your first paying client (your parents)"
4. Descript demo — transcript → shorts → article
5. OMV + 5 Shorts — real example end-to-end
6. Spotlight Article SOP — write/publish in under an hour
7. Weekly MAA — what it is and how we grade
8. DFY KP overview — scope, timeline, qualification gate
9. KP pillars — entity, citations, profiles, schema, clustering (5 clips)
10. Case proof — before/after review velocity
11. City Captain & safety
12. Micro-agency setup — PAL walkthrough
13. Agency partner highlight — HVACGrowth/mowmoney
14. University credibility — JHU story
15. "What we don't do" — no PBNs, no reciprocal links
16. Ratings & SLAs — quality matters
17. Book teasers — KP Guide + Shitbaggers
18. Travel montage — Europe clips
19. AMA live — parents & students
20. FAQ rapid-fire

For each, determine:
- Does raw material exist locally that could produce this? (transcript, footage, audio)
- Has it already been published somewhere?
- Can Claude produce a draft script/article from existing material?
- What's still needed (filming, recording, etc.)?

Create gap analysis at ~/Documents/Claude/PRISM/content-audit/03-gap-analysis.md

## Phase 4: Content Production from Existing Material (2-4 hours)

For every transcript or raw content source found in Phase 1 that has NOT been processed:

### Transcripts → Articles
1. Read the transcript
2. Follow the Article Writing from Transcripts SOP
3. Draft 1-3 articles per transcript (depending on length/topics covered)
4. Run each through the Article QA & Compliance SOP
5. Save drafts to ~/Documents/Claude/PRISM/content-audit/drafts/articles/

### Transcripts → Video Scripts
1. Identify the strongest 60-90 second segments
2. Write short-form video scripts with hooks, key points, and CTAs
3. Save to ~/Documents/Claude/PRISM/content-audit/drafts/video-scripts/

### Transcripts → LinkedIn Posts
1. Extract the single most compelling insight from each transcript
2. Write a LinkedIn post (hook + story + lesson + CTA format)
3. Save to ~/Documents/Claude/PRISM/content-audit/drafts/linkedin-posts/

### Transcripts → Email Snippets
1. Pull the most actionable takeaway
2. Write a short email snippet that could go in a newsletter or drip
3. Save to ~/Documents/Claude/PRISM/content-audit/drafts/email-snippets/

## Phase 5: Publishing Calendar Draft (30-45 min)

Based on everything discovered, create a realistic 4-week publishing calendar:

~/Documents/Claude/PRISM/content-audit/04-publishing-calendar.md

For each week:
- What can be published from drafted content (articles, posts, scripts)
- What needs {{USER_NAME}} to film/record
- What platforms each piece goes to
- Suggested Dollar-a-Day test candidates ($1-5/day)

Map to the cadence targets from the GTM plan:
- Shorts: 3-5/week per channel ([Your Agency] + {{USER_NAME}} personal)
- Long-form: 1/week per channel
- Lives/Webinars: 2/month

## Phase 6: Executive Summary (15-20 min)

Create a morning briefing at ~/Documents/Claude/PRISM/content-audit/00-executive-summary.md with:

- Total raw assets found (by type)
- Total published content found (by platform)
- Content pieces drafted overnight (by type)
- Biggest gaps in the publishing calendar
- Top 5 quick wins (things that can be published this week from existing material)
- Top 5 things that require {{USER_NAME}} to film/record
- Recommended priority order for the next 7 days

## Phase 7: PRISM Updates

- Write a session log to ~/Documents/Claude/PRISM/logs/2026-03/
- Update any SOPs that need refinement based on what you learned
- If you discover a new repeating pattern, create a new SOP for it
- Update INDEX.md with any changes

## Rules

- Be thorough. This runs overnight. Use the full time.
- Save everything to ~/Documents/Claude/PRISM/content-audit/
- Create the content-audit directory and all subdirectories at the start
- Draft content should be ready to review and publish, not rough outlines
- Follow the existing PRISM SOPs for all content production
- If a transcript is too long to process in one pass, break it into sections
- Log everything you do

---

## See Also
- [[content-audit/00-executive-summary|Content Audit]]
- [[blitzmetrics-canon/07-quality-standards|Quality Standards]]
- [[skills/content-factory|Content Factory Skill]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory Process]]
- [[claude-code/run-content-pipeline|Content Pipeline Runner]]
