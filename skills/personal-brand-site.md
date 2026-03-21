---
name: Personal Brand Site
version: 1.0
description: Build WordPress personal brand sites with Topic Wheel integration, schema markup, and E-E-A-T optimization
triggers:
  - personal brand site
  - WordPress site
  - site build
  - KP site
  - personal website
canon_source: blitzmetrics-canon/06-topic-wheel.md
full_sop: sops/client-work/personal-brand-site-build.md
triangles: [CCS, GCT]
---

# Personal Brand Site — Executable Skill

## Phase 0: Strategy (Before Touching WordPress)

### Step 1: Define Topic Wheel (2-3 hours)
Interview client to build the Why-How-What framework:
- **WHY** (outer ring): Core beliefs, philosophy, worldview — "What do you believe about your industry?"
- **HOW** (middle ring): 3-5 methodologies, frameworks, processes
- **WHAT** (center): Services, products, offers

### Step 2: Content Audit (1-2 hours)
- Inventory existing content: blog, videos, podcasts, case studies
- Map each piece to Topic Wheel theme
- Identify content gaps (expect 20-30% new content needed)
- **Anti-vandalism:** Check what exists before creating anything new

### Step 3: Site Architecture
Standard entity-first structure:
```
Home
├── About (bio, story, beliefs, credentials)
│   ├── Speaking (talks, events, videos)
│   └── Media (press, testimonials)
├── Blog/Articles (organized by Topic Wheel theme)
├── Services/Offers (What center)
├── Case Studies (2-4 with quantified results)
├── Resources (free tools, templates)
├── Contact/Work Together
└── Newsletter signup
```

URL strategy: `/about`, `/blog`, `/topic/how-systems`, `/services`, `/case-studies`, `/subscribe`

## Phase 1: WordPress Setup

1. **Domain:** Client's name (firstname.com or firstname-lastname.com). Avoid company domains.
2. **Hosting:** BlitzMetrics managed WP or WP Engine/Kinsta. SSL mandatory.
3. **Theme:** BlitzMetrics proprietary theme. Alternatives: Neve Pro, Astra Pro. Avoid heavy animated templates.
4. **Essential plugins (install only these):**
   - SEO: Rank Math OR Yoast (one, not both)
   - Analytics: MonsterInsights (GA4)
   - Backup: UpdraftPlus
   - Security: Wordfence
   - Forms: Gravity Forms or WPForms
   - Cache: WP Super Cache or W3 Total Cache
5. **Settings:** Static homepage, `/%postname%/` permalinks, search indexing enabled, sitemap via Rank Math
6. **Tracking:** GA4 connected, Search Console verified, Facebook Pixel (if running ads), conversion events set (subscribe, contact, download)

## Phase 2: Content Architecture

### Homepage (5 sections)
1. **Hero:** Clear headline tied to value prop, subheadline, primary CTA, real photo (not stock), loads under 2 seconds
2. **Value Props:** 3 columns answering "Why you?"
3. **Social Proof:** 3-5 testimonials with headshot/name/title OR "As seen in" logos OR stats
4. **CTA Section:** Single focused action (subscribe, book, download). Contrasting button color.
5. **Blog Preview:** 3 recent posts as grid cards

### About Page: Bio, origin story, core beliefs (tied to WHY), key metrics/proof, credentials, testimonials, CTA
### Blog: Category structure matches Topic Wheel. Each post has featured image (1200x630), author bio, reading time, Topic Wheel category tag.
### Services: Clear pricing, what is included, testimonial/case study, FAQ, CTA
### Case Studies: Challenge > Approach > Results (quantified metrics, not "significant growth") > Key Lessons > CTA

## Phase 3: Schema & SEO

### Schema Markup
- schema.org Person/Organization on About page
- Article schema on all blog posts
- Validate via Google Rich Results Test before launch

### On-Page SEO (per blog post)
- Primary keyword in title (first 60 chars), meta description (155 chars), H1, first 100 words
- 2-3 internal links with descriptive anchors
- 1-2 external links to high-authority sources
- Keyword density 1-2%, short paragraphs, subheadings

### Internal Linking Strategy
- How posts link to Why posts (philosophy)
- How posts link to What pages (services)
- What pages link to Case Studies (proof)
- Every blog post: 2-3 internal links. Every service page: 3-5. Every case study: 2-3.

### E-E-A-T Optimization
- **Experience:** Real stories, case studies, personal lessons
- **Expertise:** Data, frameworks, proven methodologies
- **Authoritativeness:** Credentials, speaking, media in author bio
- **Trustworthiness:** Source citations, disclosed affiliations, testimonials

## Pre-Launch Checklist

- [ ] All pages have unique meta titles and descriptions
- [ ] All internal links tested (no 404s)
- [ ] Images optimized (compressed, alt text)
- [ ] Mobile responsive (tested on real devices)
- [ ] Site loads under 3 seconds
- [ ] Schema validates via Google Rich Results Test
- [ ] GA4 and Search Console connected and firing
- [ ] Contact form and newsletter signup tested
- [ ] Topic Wheel categories match WordPress categories
- [ ] No keyword cannibalization between posts

## Known Pitfalls

- **Corporate/impersonal feel.** Use real photos, write in client's voice, share real stories.
- **Cluttered design.** Showcase top 20% of expertise. White space is good. One CTA per section.
- **Content doesn't align with services.** Map all content to Topic Wheel first. No posts outside the framework.
- **Old content decays.** Revisit top 10 posts quarterly. Update stats, examples, links. Republish.
- **Topic Wheel created but not implemented.** Make it visible in navigation. Create category pages. Link by theme.

## Human Gates

- Client interview for Topic Wheel definition
- Client approval of site architecture before build starts
- Content review for voice, accuracy, brand alignment before launch
- WordPress publishing and technical setup (plugin install, theme config)
- Real photo selection (not stock)
- Post-launch client sign-off
- Monthly content review and updates based on analytics
