---
name: KP Sprint
version: 1.1
description: Deliver a Knowledge Panel Sprint — $6,000, 30 days, fixed scope, 5
  deliverable categories
triggers:
  - Knowledge Panel
  - KP Sprint
  - KP delivery
  - 30-day sprint
  - knowledge panel sprint
canon_source: blitzmetrics-canon/02-content-factory-process.md
full_sop: sops/client-work/knowledge-panel-sprint.md
triangles:
  - CCS
  - ACC
  - GCT
tags:
  - status/active
  - triangle/ACC
  - triangle/GCT
  - triangle/MAA
  - type/skill
---

# KP Sprint — Executable Skill

## The Product

$6,000. 30 days. Fixed scope. Zero custom detours. Grounded in the [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]] and the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] methodology. 50% to start, 50% on delivery. Clock pauses if client blocks prerequisites. Extra wants go to Phase 2 list — no exceptions.

## Qualification Gate (MUST Pass Before Starting)

| Criteria | Threshold |
|----------|-----------|
| Business type | LSA (Local Service Ad) category |
| Revenue | $100k+/month |
| Reviews | 100+ five-star Google reviews |
| Willingness to film | Confirmed |

**If they don't qualify:** Route to LSS $300 tier. Do not start a Sprint for unqualified clients.

## KP Acquisition Process (5 Steps -- In Order, No Skipping)

The Knowledge Panel acquisition follows a strict 5-step sequence. Skipping steps causes rejection.

### Step 1: Audit
- Search the person's name on Google. Do they control top results?
- Check all social profiles for consistency (name, title, photo, bio)
- Use BlitzMetrics Knowledge Graph Explorer to find existing entity
- Record **KGMID** (format: `/g/11xxxxxxxxx`) and **confidence score** as baseline
- Use Gemini, Grok, and ChatGPT to map how Google currently perceives them
- **Confidence Score vs Display = "entity gap":** Having a KGMID does NOT guarantee a visible panel. [Client Name] had score 497 but no public panel.

### Step 2: Assemble E-E-A-T Proof
- **Experience:** Speaking engagements, interviews, case studies
- **Expertise:** Articles, training, certifications, published content
- **Authority:** Third-party mentions from credible sources
- **Trust:** Consistent branding and citations across all platforms

### Step 3: Build Entity Foundation
- Personal brand site (WordPress, entity-first architecture)
- Schema.org Person markup with `sameAs` array pointing to all profiles
- Google properties (Search Console, Analytics, YouTube)
- Internal linking across bios, interviews, blog posts
- Content Factory: WHY stories, HOW expertise articles, WHAT service pages
- **Wikidata entry:** Primary structured data source for KG AND LLMs. Every claim needs 2+ references from different domains. Add Google Knowledge Graph ID (P2671) to tighten reconciliation.

### Step 4: Claim the Panel
**Pre-claim checklist (assemble ALL of these before clicking anything):**
- [ ] Gmail account for panel management
- [ ] KGMID from Knowledge Graph Explorer
- [ ] Government-issued ID + clear selfie holding it (passport preferred, JPEG not HEIC)
- [ ] Official website URL (Entity Home)
- [ ] 5+ social profile URLs (LinkedIn, Facebook, Instagram, YouTube, TikTok)
- [ ] **LOGGED-IN screenshots** of each social account (homepage shots do NOT count -- must show admin/logged-in state)
- [ ] Written explanation of why you are claiming the panel

**Save everything in a Google Drive folder labeled with submission date.** Google does NOT provide a copy of your request.

**Writing the claim explanation (this is where most people get rejected):**
- BAD: "I want to claim this panel because it's mine."
- GOOD: Detail every affiliation, academy membership, certification, podcast appearance, and published work. Every statement should link to a verifiable source. Use ChatGPT to draft, then verify every claim has a URL.

### Step 5: Submit and Wait
- Upload everything, agree to terms, submit
- Google usually responds within 1-3 days

### Two Dimensions of Every Trust Signal
1. **Power:** Raw strength of the entity voting for you (domain rating, followers, engagement, traffic)
2. **Relevance:** Topical alignment with what you do
- A link from a high-authority site about romance novels does NOT help an HVAC company. Power without relevance is worthless.

---

## 5 Fixed Deliverables

### 1. Personal Brand Site
- Entity-first architecture (see [[skills/personal-brand-site|Personal Brand Site]]): Home, About, Media/Press, Speaking, Services, Contact
- schema.org Person/Organization + social/knowledge graph linking
- Citation hub with outbound links to verified profiles and press

### 2. Entity Foundations
- 10-20 citations/mentions cleaned and published (associations, press, directories)
- Unified NAP/handles + indexable profiles

### 3. Authority Content
- 1 recorded interview (60 min) turned into 3 authority articles (edited, SEO'd)
- 6 short-form videos (subtitled, branded, hooks + CTAs)

### 4. Distribution Mini-Plan
- Posting plan + Dollar-a-Day starter plan and budget map

### 5. Entity Health Snapshot
- "Panel likelihood" score + checklist of next moves

## 30-Day Timeline

| Days | Phase | Key Actions |
|------|-------|-------------|
| 0-2 | Intake | Send intake checklist, collect prerequisites, set up PM, confirm interview date |
| 3-7 | Foundation | Site scaffold on templated theme, schema markup, record 60-min interview, begin citation research |
| 8-20 | Production | 3 articles from transcript, 6 short-form videos, 10-20 citations, profiles unified, internal linking |
| 21-26 | QA | Technical QA on site/schema/citations, distribution plan, Dollar-a-Day budget map, deliverable review |
| 27-30 | Handoff | Client review, fixes applied, Entity Health Snapshot, next-step plan, case study drafted |

**Client must-dos:** Provide brand assets/bios/access on time. Attend 60-min interview. Approve copy quickly (delays pause the clock).

## Comp Structure (Per $6,000 Sprint)

| Role | % | Amount | Notes |
|------|---|--------|-------|
| Sales Commission (Closer) | 15% | $900 | Requires CRM evidence |
| Delivery Lead (PM) | 10% | $600 | Paid on on-time delivery (<=30 days) |
| Delivery Labor Pool | 35% | $2,100 | Writers, editors, designers, VAs. Paid by task per rate card |
| QA/On-Time Bonus | 5% | $300 | Released ONLY if on-time + zero critical defects |
| Company Retained | 35% | $2,100 | Ops, software, R&D, runway |

## Quality Checks

- [ ] All 5 deliverable categories complete before handoff
- [ ] Schema markup validates (Google Rich Results Test)
- [ ] All citations live and indexable
- [ ] Articles pass E-E-A-T standards
- [ ] Short-form videos have subtitles, branding, hooks, CTAs
- [ ] Dollar-a-Day plan includes specific budget allocation and content selection
- [ ] Entity Health Snapshot includes actionable next steps
- [ ] Case study drafted (if not published, Sprint is not done)
- [ ] Client signed off on all deliverables
- [ ] CRM updated with final status

## Known Pitfalls

- **Accepting unqualified clients.** Enforce the gate. Misfits waste 30 days and create bad case studies.
- **Scope creep inside the Sprint.** All custom requests go to Phase 2 list. No exceptions, no matter how small.
- **Client delays killing the timeline.** Document delays immediately. Pause clock with written notice.
- **Skipping the case study.** "If it's not published, it's not done." Build case study creation into Day 27-30.
- **Paying comp without CRM evidence.** Require lead source, call notes, proposal, signature before releasing sales commission.
- **QA bonus released despite defects.** Zero critical defects means zero. Hold the standard.

## Connected Skills

Use these skills at each phase of the Sprint:

| Phase | Skills to Use |
|-------|--------------|
| Intake | `/entity-builder` (entity audit), `/competitor-intel` (market positioning) |
| Foundation | `/schema-markup` (Person/Org schema), `/seo-audit` (site baseline) |
| Production | `/article-quality-gate` (18-step QA), `/keyword-research` (content targeting), `/batch-content` (parallel articles) |
| Distribution | `/content-calendar` (posting plan), `/social-content` (social posts from articles) |
| QA | `/geo-optimizer` (AI citability check), `/gsc-insights` (indexing verification) |
| Handoff | `/client-report` (Entity Health Snapshot), `/basecamp-ops` (status update) |

### Cross-References

- [Canon: Nine Triangles](../blitzmetrics-canon/01-nine-triangles.md)
- [Canon: Entity Linking Decision Tree](../blitzmetrics-canon/17-entity-linking-decision-tree.md)
- [Canon: GCT Discovery](../blitzmetrics-canon/11-gct-discovery-framework.md)
- [Canon: Topic Wheel](../blitzmetrics-canon/06-topic-wheel.md)
- [Full SOP: Knowledge Panel Sprint](../sops/client-work/knowledge-panel-sprint.md)
- [Personal Brand Site Skill](personal-brand-site.md)
- [Content Factory Skill](content-factory.md)
- [Influence Report Card Skill](influence-report-card.md)
- [Entity Builder Skill](entity-builder.md) (for Wikidata and schema work)

## See Also

- [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[skills/influence-report-card|Influence Report Card]]
- [[skills/personal-brand-site|Personal Brand Site]]
- [[skills/article-writer|Article Writer]]
- [[sops/client-work/knowledge-panel-sprint|KP Sprint SOP]]
- [[blitzmetrics-canon/11-gct-discovery-framework|GCT Discovery]]

## Post-Sprint Measurement (30/60/90 Day)

After Sprint delivery, verify entity visibility and organic traffic uplift using GA4 and GSC:

**GSC (via `/gsc-insights`):**
- Verify personal brand site pages are indexed (check indexing status)
- Track branded keyword impressions and position (entity name, entity name + topic)
- Monitor Knowledge Panel-related queries (impressions for "[name]" and "[name] [industry]")
- Compare pre-Sprint vs post-Sprint: impressions, clicks, CTR for branded terms

**GA4 (your analytics property):**
- Track organic sessions to the personal brand site (30/60/90 day comparison)
- Measure traffic to authority articles from the Sprint
- Check traffic sources — organic search should grow as entity signals strengthen
- Monitor engagement metrics on Sprint-produced content (time on page, pages/session)

**Cadence:** Pull at 30, 60, and 90 days post-delivery. Include in the Entity Health Snapshot update and the client's MAA report. If branded impressions haven't increased by day 60, diagnose — likely a citation or schema issue.

## Human Gates

- Qualification gate review (human reviews revenue, reviews, willingness to film)
- Client interview (60-min recorded, client participates in person)
- Client approval of all written content before publishing
- Technical QA passes (schema, citations, site validated by human)
- Client sign-off on all deliverables at handoff
- Advisor approves any compensation exceptions
- Case study publication (human writes and publishes)
