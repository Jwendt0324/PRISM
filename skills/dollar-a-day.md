---
name: Dollar-a-Day
version: 1.2
description: Set up and scale Dollar-a-Day paid social campaigns across 3 phases
triggers:
  - dollar a day
  - $1/day ads
  - boosting content
  - paid social campaign
  - facebook ads
  - instagram ads
  - ad campaign setup
  - promote content
canon_source: blitzmetrics-canon/04-dollar-a-day.md
full_sop: sops/client-work/dollar-a-day-campaign.md
triangles:
  - ACC
  - MAA
  - GCT
tags:
  - status/active
  - triangle/DDD
  - triangle/MAA
  - type/skill
---

# Dollar-a-Day — Executable Skill

## Core Principle

Test small ($1-5/day) > Scale winners ($5-20/day) > Rotate evergreen ($20-50/day). Never promote content that hasn't proven itself organically first. This skill follows the [[blitzmetrics-canon/04-dollar-a-day|Dollar-a-Day Canon]] and ties into the [[blitzmetrics-canon/05-maa-framework|MAA Framework]] for performance tracking.

## Disqualification Criteria (Check BEFORE Starting)

**Dollar-a-Day is NOT for:**
- Beginners with no proven offers or happy customers
- Businesses unwilling to record themselves or without testimonials they can obtain
- People chasing quick wins over providing real value to customers

**Dollar-a-Day IS for:** Small businesses with happy customers, growing personal brands, agencies, coaches, course sellers, SaaS, sports teams -- anyone with real content and real results to amplify.

If the prospect fails these criteria, do not proceed. Route to Content Factory production first.

## Cross-Platform Minimum Spend

| Platform | Daily Minimum | Notes |
|---|---|---|
| Facebook | $1 | Via Business Manager, vertical video preferred |
| Instagram | $1 | Managed through Facebook Ads Manager |
| YouTube | $1 | Pre-roll / in-feed video ads |
| LinkedIn | $10 | Professional targeting (job title, employer, industry) |
| Snapchat | $5 | Higher minimum, younger demo |
| TikTok | $20 | Use **Spark Ads** (boost existing organic TikTok posts as ads -- the TikTok equivalent of Dollar-a-Day boosting) |

Plan budget accordingly. A true cross-platform $1/day test costs ~$38/day minimum across all six platforms.

## Rule of 10

Three heuristics that govern the entire DAD system:

1. **10% engagement rate** -- Target benchmark. Content + audience hitting 10%+ = winner. Below 10% = diagnose using the troubleshooting framework below.
2. **10 snippets per video** -- Every long-form video yields at least 10 short-form snippets (2 edification, 5 problem/solution, 3 hooks).
3. **1 in 10 ads wins** -- Only 1 of 10 ads will perform. This is expected. Run 10, find the winner, kill the rest.

## 3x3 Video Grid (Content Structure That Feeds DAD)

Nine videos organized into three funnel stages. This is the content you are amplifying.

| Stage | Videos | Content | Audience |
|---|---|---|---|
| **WHY** (1-3) | Founder stories, testimonials, endorsements | Emotional connection, trust | Cold (lookalikes, interests) |
| **HOW** (4-6) | Teach solutions WITHOUT mentioning product | Demonstrate expertise | Warm (engaged with WHY 15+ sec) |
| **WHAT** (7-9) | Services, pricing, results, direct CTA | Convert to customer | Hot (engaged with HOW 15+ sec) |

### Retargeting Sequence
- **Ad Set 1:** WHY videos to cold audiences, EXCLUDING WHAT video viewers
- **Ad Set 2:** HOW videos to WHY engagers, EXCLUDING WHAT viewers
- **Ad Set 3:** WHAT videos to HOW engagers, no exclusions
- **Ad Set 4:** Continued WHAT until conversion

Build custom audiences using Facebook "people who watched 15+ seconds" (ThruPlay). Create audiences from each video to enable stage progression.

### Performance Benchmarks
- $0.02 per video view | $3 per lead | $10 per conversion

## Phase 0: Pre-Campaign Assessment

### Organic Thresholds (MUST meet before any spend)

| Content Type | Minimum Organic Performance | Where to Check |
|---|---|---|
| Video | 1,000+ views, 100+ engagements, 1+ min avg watch time | YouTube Analytics |
| Blog post | 500+ visitors, 50+ shares, 1+ min avg session duration | **GA4** — filter by page path, check sessions, engagement time, and traffic source |
| Social post | 100+ reactions/comments/shares, 3%+ engagement rate | Native platform analytics |
| Email | 25%+ open rate | Email platform |

**For blog posts:** Pull GA4 data directly — filter Pages report by the article URL. Check sessions (not just pageviews), average engagement time, and what percentage is organic search vs. referral. Also run `/gsc-insights` to check if the article is ranking for any keywords and pulling impressions.

**If thresholds not met:** Put asset back in production. Do not spend money on unproven content.

### Asset Quality Check
- Video: 720p min, captions, 30-120 seconds ideal
- Image: 1200px+ width, legible text
- Copy: Clear, benefit-focused, fits platform tone
- Landing page: Matches ad promise, loads fast, clear CTA

### Campaign Structure
```
Campaign: [Q_ Content Promotion]
├── Adset: Phase 1 Testing ($1-5/day)
├── Adset: Phase 2 Winners ($5-20/day)
└── Adset: Phase 3 Evergreen ($20-50/day)
```

Budget split: 20% Phase 1 (testing) / 50% Phase 2 (scaling) / 30% Phase 3 (evergreen)

## Phase 1: 7-Day Testing ($1-5/day)

1. Select 1-3 organic winners
2. Create 2-3 ad copy variations per asset (Curiosity / Direct / Story angles)
3. Set targeting: location (GCT), 5-10 interests, custom audience if available. Aim 50K-500K audience size
4. Budget: $1-2 per variation. Run exactly 7 days (Tuesday to Monday)
5. Track daily: CPC, CTR, cost per view/engagement, total spend

### Daily Decision Rules

| Signal | Action |
|---|---|
| CPC > $2.50 OR CTR < 1.5% (video) / < 3% (image) OR engagement < 2% | **KILL** — pause immediately |
| CPC < $1 AND CTR > 3% (image) / > 2% (video) AND positive engagement | **ADVANCE** — move to Phase 2 |
| CPC $1-$1.50, CTR 2-3%, unclear outcome | **TEST NEW** — swap copy or image, keep running |
| Negative comments | **KILL** — pause immediately, do not wait |

**No-winners edge case:** If Phase 1 produces zero winners after testing 5+ pieces: pivot creative (new angles/hooks from same content), test different audiences, or pause and produce new raw content before spending more.

**HUMAN GATE:** Daily kill/keep decisions require human judgment in context

## Phase 2: 30-Day Scaling ($5-20/day per winner)

1. Consolidate Phase 1 winners (best copy + best creative + best audience)
2. Scale budget 2-4x Phase 1 level
3. Create 3-5 ad variations to test
4. Audience expansion schedule:
   - Days 1-10: Keep original targeting, establish baseline
   - Days 11-20: Add lookalike + custom audiences
   - Days 21-30: Expand interests, test retargeting
5. Set up conversion tracking (pixel, forms, CallRail)
6. Optimize every 3 days. Daily monitoring first 10 days

### Phase 2 Decision Rules

| Signal | Action |
|---|---|
| CPA > 50% of CLV | **PAUSE** |
| CTR declining 3+ days | **REFRESH CREATIVE** |
| CPA < 30% of CLV, ROAS > 2:1 | **DOUBLE BUDGET** |
| Negative comments or brand safety | **PAUSE IMMEDIATELY** |

### End-of-Phase Decision

| Outcome | Criteria | Action |
|---|---|---|
| Promote to Phase 3 | CPA < 40% CLV, stable conversions, positive sentiment | Move to Evergreen |
| Kill | CPA > 50% CLV, declining conversions | Archive campaign |
| Iterate | CPA marginally profitable | Back to Phase 1 with new creative |

**HUMAN GATE:** Budget scaling approval, Phase 2 > Phase 3 promotion decision

## Phase 3: Evergreen Greatest Hits ($20-50/day)

1. Consolidate 5-10 Phase 2 winners into rotation pool
2. Budget: $20-50/day total, divided across assets in round-robin
3. Monthly refresh cycle:
   - Review all assets. Keep top 5, retire bottom 2-3
   - Add 1-2 new creative variations from latest Phase 2 graduates
   - Rest tired creatives for 2-3 weeks, bring back later
4. Monitor for ad fatigue: declining CTR, increasing CPC week-over-week
5. Quarterly audience refresh: new geographies, interests, lookalikes

### Monthly Reporting

Track per asset: CPC, CPA, conversions, ROAS, status (Scale/Hold/Rotate/Pause)
Track overall: total spend vs budget, total conversions, avg CPA, avg ROAS, fatigue indicators

**HUMAN GATE:** Monthly performance review, rotation decisions, quarterly audience expansion

## Anti-Vandalism (Hard Rules)

- Never promote content that hasn't met organic thresholds
- Always set hard kill rules BEFORE campaign launch
- Ad creative must match landing page (no bait-and-switch)
- Frequency cap: 12-15 impressions/person/week max
- Monthly ROAS review mandatory (prevent budget creep with declining returns)
- If ROAS < 1.5:1, reduce budget immediately

## Automation Opportunities (2026)

When ready to automate Dollar-a-Day execution:
- **adspirer-ads-agent plugin** — Cross-platform ad creation (Google, Meta, TikTok, LinkedIn). Install: `/plugin install adspirer-ads-agent@claude-plugins-official`
- **Pipeboard MCP** — Connect ad platform data to Claude for real-time performance monitoring
- **Auto-kill script pattern:** Pull yesterday's ROAS via API, auto-pause ad sets below threshold

**Canon reminder:** Human gates still required for budget scaling, Phase promotion, and kill decisions. Automation handles data pull and reporting; humans make the calls.

## Troubleshooting Framework (When Engagement < 10%)

Diagnose in this order. Fix the root cause, not the symptom.

| # | Category | Diagnostic | Fix |
|---|---|---|---|
| 1 | **Authority not high enough** | Check 3 Components: Proof (certs, awards, case studies), People (who endorses you?), Properties (where does content live?) | Build authority FIRST via Content Factory. No amount of targeting fixes weak authority. |
| 2 | **Weak/missing hook** | Are viewers dropping before 3 seconds? Check the 4-component one-minute video formula: Hook (0-3s), Pain/Pleasure (3-15s), Solution (15-50s), CTA (50-60s) | Re-cut video with stronger hook. No bumper, no name intro, get right to the point. |
| 3 | **Production issues** | Poor audio, bad lighting, distracting background, unprofessional editing | Re-record or re-edit. This is a Process-stage fix. |
| 4 | **Campaign setup** | Wrong objective, budget too low for audience size, incorrect placement, missing exclusions causing overlap | Audit campaign settings against the SAE Phase 5 checklist. |

## Three Ways Dollar-a-Day Fails

1. **Impatience:** Scaling before Phase 1 learning is clear
2. **Unclear thresholds:** No kill rules, hope-based decisions
3. **Set-and-forget:** No monthly review or rotation

## Case Study Reference Table

| Client | Result | Strategy | Key Metric |
|---|---|---|---|
| Golden State Warriors | $38-40M ticket revenue from ~$1M spend | DAD retargeting, 3-stage funnel | $1 into $38 ROAS |
| LA Lakers | 631 fans acquired | 3-stage funnel (Awareness > Commitment > Conversion) | < $1 per fan |
| Bryan Eisenberg / Sears | 50% discount settlement | Targeted executives in HQ city (+/- 50 miles) with blog post | Pressure campaign |
| Caleb Guillams | 38% link click rate | Content about audience targeted to people who know him | 200%+ above industry avg |
| Jason Wiser | 1M+ software installs | DAD + light coaching | $0.01 per video view |
| Dennis Yu | 651% ROI | Facebook ads, SiteTuners case study | Documented ROI |
| Rosetta Stone | Scaled $1/day testing to $1M/day on Black Friday | DAD as testing methodology, then scale | Testing methodology proof |

---

## Connected

- [Canon: Dollar-a-Day](../blitzmetrics-canon/04-dollar-a-day.md)
- [Canon: MAA Framework](../blitzmetrics-canon/05-maa-framework.md)
- [Full SOP: Dollar-a-Day Campaign](../sops/client-work/dollar-a-day-campaign.md)
- [Content Factory Skill](content-factory.md)
- [Content Repurposing Skill](content-repurposing.md)
- [Weekly MAA Report Skill](weekly-maa-report.md)

## See Also

- [[blitzmetrics-canon/04-dollar-a-day|Dollar-a-Day Canon]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[skills/weekly-maa-report|Weekly MAA Report]]
- [[sops/client-work/dollar-a-day-campaign|Dollar-a-Day SOP]]
- [[skills/content-factory|Content Factory Skill]]
