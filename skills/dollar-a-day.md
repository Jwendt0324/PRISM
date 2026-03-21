---
name: Dollar-a-Day
version: 1.1
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
triangles: [ACC, MAA, GCT]
---

# Dollar-a-Day — Executable Skill

## Core Principle

Test small ($1-5/day) > Scale winners ($5-20/day) > Rotate evergreen ($20-50/day). Never promote content that hasn't proven itself organically first.

## Phase 0: Pre-Campaign Assessment

### Organic Thresholds (MUST meet before any spend)

| Content Type | Minimum Organic Performance |
|---|---|
| Video | 1,000+ views, 100+ engagements, 1+ min avg watch time |
| Blog post | 500+ visitors, 50+ shares, 1+ min session duration |
| Social post | 100+ reactions/comments/shares, 3%+ engagement rate |
| Email | 25%+ open rate |

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

## Three Ways Dollar-a-Day Fails

1. **Impatience:** Scaling before Phase 1 learning is clear
2. **Unclear thresholds:** No kill rules, hope-based decisions
3. **Set-and-forget:** No monthly review or rotation
