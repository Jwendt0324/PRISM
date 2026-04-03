---
name: Quick Audit
version: 1
description: Run a 12-point quick audit on any website/person with D-A grading and
  one-page summary output. Entry product feeding KP Sprint pipeline.
triggers:
  - Quick Audit
  - quick audit
  - website audit
  - site review
  - presence check
  - online presence audit
canon_source: blitzmetrics-canon/07-quality-standards.md
full_sop: sops/blitzmetrics-imported/INDEX.md
triangles:
  - GCT
  - MAA
  - ACC
tags:
  - status/active
  - triangle/GCT
  - triangle/MAA
  - type/skill
---

# Quick Audit — Executable Skill

## Core Principle

The Quick Audit is a 12-point assessment of a person or business's online presence, graded D through A. It takes 30-60 minutes and serves as the entry point into your engagement ladder. Every Quick Audit should naturally surface the need for a KP Sprint or ongoing services when appropriate. Built on Dennis Yu's Quick Audit framework (auth-08, Nicole Kelly case study) and the E-E-A-T scorecard methodology (auth-06).

**Upsell path:** Quick Audit -> KP Sprint -> Ongoing Services -> AI Apprentice
**Delivery:** One-page summary + 15-minute walkthrough call

---

## The 12-Point Audit

### Category 1: Website Foundation (3 points)

| # | Audit Point | What to Check | Grade Criteria |
|---|-------------|---------------|----------------|
| 1 | **Contact Page** | H1 with brand + service + geo. City names listed. Entity authority block. FAQ with schema. Full schema markup. Map embed with city text. Trust signals near form. (Joel Headley: "Contact page is the most important SEO asset.") | **A:** All 7 elements present. **B:** 5-6 elements. **C:** 3-4 elements. **D:** Basic contact form only or missing entirely. |
| 2 | **Site Health** | Load speed (Core Web Vitals), mobile responsive, SSL active, no broken links, proper heading hierarchy (H1>H2>H3), meta descriptions written (not auto-generated). | **A:** All CWV passing + mobile-first + clean structure. **B:** CWV mostly passing, minor issues. **C:** Slow load or mobile issues, sloppy structure. **D:** Major speed/mobile problems, no SSL, broken pages. |
| 3 | **Schema Markup** | JSON-LD Person/Organization/LocalBusiness schema, sameAs links to social profiles, validated via Google Rich Results Test. Wikidata KGMID connected if applicable. | **A:** Full schema, validated, sameAs complete, KGMID connected. **B:** Basic schema present, partially complete sameAs. **C:** Minimal or broken schema. **D:** No schema markup at all. |

### Category 2: Content & Authority (3 points)

| # | Audit Point | What to Check | Grade Criteria |
|---|-------------|---------------|----------------|
| 4 | **Blog / Content** | Active blog with regular publishing, organized by Topic Wheel, internal linking between posts, E-E-A-T signals (real stories, real photos, author bio). No AI slop (check banned word list). | **A:** 50+ quality posts, Topic Wheel organized, strong internal linking, clear E-E-A-T. **B:** 20-50 posts, some organization, decent quality. **C:** Under 20 posts or irregular publishing. **D:** No blog or content is clearly AI-generated/thin. |
| 5 | **Video Presence** | YouTube channel, video count, subscriber count, WHY video exists, one-minute videos in rotation, videos embedded on website. | **A:** Active YouTube (50+ videos), WHY video, regular uploads, embedded on site. **B:** YouTube exists with 10-50 videos, some embedding. **C:** YouTube exists but sparse or abandoned. **D:** No video presence. |
| 6 | **E-E-A-T Signals** | Real photos (not stock), real testimonials, credentials visible, about page with personal story, author bios on content, no arms-crossed headshots, no red CTA buttons on key pages. | **A:** Strong E-E-A-T across all pages — real photos, real stories, credentials visible. **B:** Most pages have E-E-A-T, some gaps. **C:** Thin E-E-A-T, stock photos, generic bios. **D:** No E-E-A-T signals — could be anyone's site. |

### Category 3: Social & Visibility (3 points)

| # | Audit Point | What to Check | Grade Criteria |
|---|-------------|---------------|----------------|
| 7 | **Social Profiles** | All social buttons link to active profiles (not broken). Native content on each platform (not cross-posted YouTube links). Profile photos match across platforms. Bios are consistent. LinkedIn headline follows XYZ format ("I help X do Y through Z"). | **A:** 4+ active platforms, native content, consistent branding, XYZ headline. **B:** 2-3 active platforms, mostly consistent. **C:** Profiles exist but dormant or inconsistent. **D:** Missing profiles, broken links, or zero activity. |
| 8 | **Google Business Profile** | Verified, categories correct, regular posts, 50+ reviews (4.5+ stars), photos uploaded, Q&A answered, products/services listed. | **A:** Verified, optimized, 100+ reviews, active posting. **B:** Verified, 50+ reviews, occasional posts. **C:** Verified but sparse or under 50 reviews. **D:** Not verified, not claimed, or nonexistent (n/a for non-local). |
| 9 | **Cross-Channel Traffic** | Evidence of driving traffic between channels (social to website, website to YouTube, email to content). "No subscribe CTAs on homepage" rule. Social links functional. | **A:** Clear cross-traffic strategy, CTAs drive between channels, email captures to content. **B:** Some cross-traffic, basic CTAs present. **C:** Channels exist in silos, no connecting strategy. **D:** No evidence of cross-channel strategy. |

### Category 4: Authority & Entity (3 points)

| # | Audit Point | What to Check | Grade Criteria |
|---|-------------|---------------|----------------|
| 10 | **Google Knowledge Panel** | Does a Knowledge Panel appear? Is it claimed? Accurate? Connected to Wikidata? Entity shows in Knowledge Graph Search API? | **A:** KP live, claimed, accurate, Wikidata connected. **B:** KP live but unclaimed or partially accurate. **C:** No KP but entity signals exist (could trigger with work). **D:** No KP and no entity foundation. |
| 11 | **Backlink Profile** | Referring domains count, domain authority/rating, quality of links (edu, gov, news, industry), toxic link ratio. | **A:** DA 40+, 100+ quality referring domains, press/edu links. **B:** DA 25-40, 50-100 referring domains. **C:** DA 15-25, under 50 referring domains. **D:** DA under 15, few or toxic backlinks. |
| 12 | **Search Visibility** | Organic traffic estimate, keywords ranking top 10/50, brand name SERP ownership (do they own page 1 for their own name?), People Also Ask presence. | **A:** 1,000+ organic visitors/mo, owns brand SERP, top-10 for primary keywords. **B:** 500-1,000 visitors, partial brand SERP ownership. **C:** 200-500 visitors, limited keyword presence. **D:** Under 200 visitors, does not own brand SERP. |

---

## Grading Scale

| Grade | Meaning | Score Range |
|-------|---------|-------------|
| **A** | Strong — maintain and optimize | 4 points |
| **B** | Good — minor improvements needed | 3 points |
| **C** | Weak — significant gaps to address | 2 points |
| **D** | Critical — needs immediate attention | 1 point |

**Overall Score:** Sum of all 12 points (max 48)
- **A (37-48):** Strong online presence. Optimize and scale.
- **B (25-36):** Solid foundation with clear gaps. Targeted improvements.
- **C (13-24):** Significant weaknesses. Needs structured engagement.
- **D (1-12):** Starting from scratch. Full build required.

---

## Execution Process

### Step 1: Pre-Audit Research (15-20 min, AI can do this)

Pull data from native platforms and public tools:

1. **Website:** Run through PageSpeed Insights, check SSL, validate schema via Rich Results Test
2. **SEO:** Pull organic traffic estimate, keyword rankings, backlink profile (Ahrefs/SEMrush or free alternatives)
3. **Social:** Check all major platforms (Facebook, LinkedIn, YouTube, Instagram, TikTok, X)
4. **Google:** Search brand name, check for Knowledge Panel, search Knowledge Graph API
5. **GBP:** Check Google Maps listing (if local business)
6. **Content:** Count blog posts, check publishing frequency, scan for AI language

### Step 2: Score Each Point (10-15 min)

Grade each of the 12 points against the rubric. Use objective data, not feelings.

### Step 3: Write One-Page Summary (10-15 min)

Use this template:

```
# Quick Audit: [Client/Business Name]
**Date:** [Date] | **Auditor:** [Name] | **Overall Grade:** [A/B/C/D] ([score]/48)

## Scorecard

| # | Area | Grade | Key Finding |
|---|------|-------|-------------|
| 1 | Contact Page | | |
| 2 | Site Health | | |
| 3 | Schema Markup | | |
| 4 | Blog / Content | | |
| 5 | Video Presence | | |
| 6 | E-E-A-T Signals | | |
| 7 | Social Profiles | | |
| 8 | Google Business Profile | | |
| 9 | Cross-Channel Traffic | | |
| 10 | Knowledge Panel | | |
| 11 | Backlink Profile | | |
| 12 | Search Visibility | | |

## Top 3 Strengths
1.
2.
3.

## Top 3 Gaps (Biggest Opportunities)
1.
2.
3.

## Recommended Next Step

[Based on the audit findings, recommend ONE clear next step from the engagement ladder]

| If Score Is... | Recommended Engagement |
|----------------|----------------------|
| D overall or no entity foundation | **KP Sprint** — Build entity from scratch, establish Knowledge Panel |
| C overall with content gaps | **Ongoing Content Services** — Full Content Factory execution |
| B overall, needs amplification | **Dollar-a-Day** — Promote existing content winners |
| A overall, wants to scale | **AI Apprentice** — Learn to run Content Factory internally |

**Your recommended engagement:** [specific recommendation with rationale tied to audit findings]
```

### Step 4: Deliver (15-min call, human required)

- Walk through the one-page summary
- Explain top 3 gaps with specific examples from their audit
- Present recommended next step with pricing
- Answer questions
- If they want to proceed: schedule GCT discovery call

---

## Upsell Logic

The Quick Audit is NOT just an audit. It is a diagnostic that naturally reveals the need for deeper engagement.

**Key principle:** The audit should show the client their gaps so clearly that the recommended engagement feels obvious, not salesy.

| Audit Finding | Natural Upsell |
|---------------|---------------|
| No Knowledge Panel + weak entity | KP Sprint — "You're invisible to Google's entity system" |
| Content exists but not organized/promoted | Ongoing Services — "You have gold sitting in a drawer" |
| Strong content, no amplification | Dollar-a-Day — "Your best content is reaching 1% of the people it should" |
| Everything is weak, owner wants to learn | AI Apprentice — "We'll teach you to build this yourself" |
| Just needs a quick strategy session | Power Hour — "Let's map out your next 90 days" |

**Never hard-sell.** The audit data sells. If the client says "what should I do about this?" — that is the upsell moment.

---

## Data Sources

| Data Point | Tool | Free Alternative |
|-----------|------|-----------------|
| Organic traffic, keywords | Ahrefs / SEMrush | Ubersuggest, Google Search Console (if access granted) |
| Backlink profile | Ahrefs / SEMrush | Ubersuggest, Moz Link Explorer (free tier) |
| Site speed / CWV | PageSpeed Insights | GTmetrix |
| Schema validation | Google Rich Results Test | Schema.org validator |
| Knowledge Panel check | Google Search | Knowledge Graph Search API |
| Social metrics | Native platform analytics | Manual check |
| GBP status | Google Maps | Manual search |

---

## Human Gates

| Step | Who | Why |
|------|-----|-----|
| Pre-audit research | AI or VA | Data gathering is delegatable |
| Scoring against rubric | AI or VA with human review | Rubric is objective but edge cases need judgment |
| One-page summary writing | AI draft, human review | Template-driven but findings need human context |
| 15-minute delivery call | Senior team member | Relationship building, answering questions, reading buying signals |
| Upsell recommendation | Agency owner | Pricing and engagement decisions require business judgment |
| GCT scheduling | Owner or VA | Administrative but sets expectations |

---

## Known Pitfalls

- **Spending too long on the audit.** This is an entry product. 60 minutes max. If it takes longer, your process is broken.
- **Inflating grades.** Use the rubric. A D is a D. Clients need honesty, not comfort.
- **Auditing without delivering.** The 15-minute call is non-negotiable. A PDF without a walkthrough has 10x lower conversion.
- **Forgetting the upsell.** Every Quick Audit should end with a clear recommended next step. Not pushy — just clear.
- **Using third-party estimates as facts.** Always label estimated data as estimated. Native platform data is preferred.

---

## Anti-Vandalism

- Never fabricate audit data. If you cannot verify a metric, mark it as "Unable to verify — [reason]."
- Never skip the human delivery call. The audit report alone does not convert.
- Never promise specific outcomes ("You will get a Knowledge Panel in 30 days").
- Never present the Quick Audit as a comprehensive strategy document. It is a diagnostic snapshot.
- Always check existing content before recommending "create new." Enhance first.

---

## Canon Compliance

| Element | Canon Reference |
|---------|----------------|
| GCT triangle | 11-gct-discovery-framework.md — Quick Audit can inform pre-GCT research |
| E-E-A-T standards | 07-quality-standards.md — grading rubric based on canon quality standards |
| MAA framework | 05-maa-framework.md — audit follows Metrics (data), Analysis (grading), Action (recommendation) |
| Anti-vandalism | 10-anti-vandalism-checklist.md — check what exists before recommending creation |
| Human requirements | 08-human-requirements.md — delivery call and pricing decisions require human |
| Quick Audit 12-point checklist | auth-08.txt (Nicole Kelly case study) — no subscribe CTAs, real photos, XYZ headline |
| E-E-A-T scorecard | auth-06.txt — D/C/B/A grading methodology for national roofing audit |
| Gemini Audit Model | meta-01.txt — GCT-aligned 6-section audit format, scoring table |
| Contact page checklist | honor-01.txt — 7-point contact page optimization, Joel Headley confirmation |

**Triangles served:** GCT (pre-discovery diagnostic), MAA (metrics/analysis/action structure), ACC (identifies funnel gaps)

---

## Connected

- [Influence Report Card Skill](influence-report-card.md) — Monthly ongoing version of authority tracking
- [KP Sprint Skill](kp-sprint.md) — Primary upsell from Quick Audit
- [Prospect Follow-Up Skill](prospect-followup.md) — Post-audit prospect management

## See Also

- [[blitzmetrics-canon/07-quality-standards|Quality Standards (Canon)]]
- [[blitzmetrics-canon/11-gct-discovery-framework|GCT Discovery Framework]]
- [[skills/influence-report-card|Influence Report Card]]
- [[skills/kp-sprint|KP Sprint]]
