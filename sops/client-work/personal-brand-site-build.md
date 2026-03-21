---
description: Build personal brand websites using WordPress-based [Methodology Partner] site builder with Topic Wheel integration for SEO and authority positioning
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
canon_compliance: 06-topic-wheel.md, 02-content-factory-process.md
triangles: CCS, GCT
canon_sources: [06-topic-wheel.md, 02-content-factory-process.md]
---

# Personal Brand Site Build

## Purpose
The personal brand website is the hub of a founder's online authority. Unlike corporate websites, personal brand sites showcase expertise, thought leadership, and accessibility. This SOP covers building professional, SEO-optimized personal brand websites using [Methodology Partner]' WordPress-based builder, integrated with Topic Wheel framework for content organization and E-E-A-T positioning.

## When to Use
- At project start when client has no professional website
- When refreshing/redesigning an existing personal brand site
- When pivoting positioning or niche (requires site restructure)
- When expanding to new service offerings or audience
- Monthly maintenance/content updates

## Process

### Phase 0: Strategy & Planning (Before Build)

**Step 1: Define Positioning & Topic Wheel (2-3 hours)**
Before designing anything, establish the Topic Wheel that will organize site content.

**Topic Wheel Structure: Why → How → What**

```
                    [OUTER RING: WHY]
                    Why does this matter?
                    (Core beliefs, philosophy, worldview)

    [MIDDLE RING: HOW]                          [MIDDLE RING: HOW]
    How do you do it?                           How do you do it?
    (Methodologies, frameworks, processes)      (Methodologies, frameworks)

                    [CENTER: WHAT]
                    What do you offer?
                    (Services, products, offers)
```

**Example for Growth Marketing Founder:**
```
                        [WHY]
            Founders can own their
          marketing without agencies.

    [HOW: Systems]              [HOW: DTC Strategy]
    Product-led                 Customer acquisition
    Growth loops                Retention models
    Retention                   Analytics

              [WHAT]
        Growth coaching
        Consulting
        Workshops
```

**Practical Steps:**
1. Interview client: "What do you believe about your industry?" (WHY)
2. List their core methodologies/frameworks (HOW) — aim for 3-5
3. Define current offerings/services (WHAT)
4. Create 3-5 Topic Wheel variants based on different audience segments (if applicable)

**Step 2: Content Audit (1-2 hours)**
Identify existing content that will populate the site.

**Content Inventory Template:**
| Type | Title | Status | Topic Wheel Fit | Length | Channel |
|------|-------|--------|-----------------|--------|---------|
| Blog post | "5 DTC Retention Tactics" | Draft | How-Retention | 2,000w | Website |
| Case study | "How X grew from $1M to $5M ARR" | Final | How-Systems | 1,500w | Website |
| Video | YouTube: "Product-Led Growth Explained" | Publish | How-Systems | 8m | YouTube |
| Podcast guest | "Growth Marketing Trends" | Transcribed | Why | 45m | Podcast |

- Audit client's existing blog, videos, podcasts, case studies
- Assess which pieces align with Topic Wheel
- Identify content gaps (what Topic Wheel themes lack content)
- Plan new content creation to fill gaps (20-30% new content typical)

**Step 3: Site Architecture & Page Hierarchy (1-2 hours)**
Map the site structure aligned to Topic Wheel.

**Standard Personal Brand Site Structure:**

```
Home
├── About (Biography, credibility, story)
│   └── Speaking (talks, events, videos)
│   └── Media (press coverage, testimonials)
├── Blog/Articles (organized by Topic Wheel theme)
│   ├── Topic 1: How-Systems
│   ├── Topic 2: How-Process
│   └── Topic 3: Why-Philosophy
├── Services/Offers (What center)
│   ├── Consulting/Coaching
│   ├── Courses/Workshops
│   └── Speaking/Appearances
├── Case Studies (proof of results)
├── Resources (free tools, templates, guides)
├── Contact/Work Together
└── Newsletter signup
```

**URL Slug Strategy:**
- Home: `/` (not `/index`)
- About: `/about` (not `/about-me`)
- Blog: `/blog` or `/articles` (not `/posts`)
- Topics: `/topic/how-systems`, `/topic/how-process` (Topic Wheel-aligned)
- Services: `/services` or `/offers` (not `/products`)
- Case studies: `/case-studies` (grouped)
- Newsletter: `/subscribe` (clear CTA)

### Phase 1: Technical Setup ([Methodology Partner] WordPress Builder)

**Step 1: Domain & Hosting**
1. Domain: Use client's name (firstname.com, firstname-lastname.com) or personal brand
   - Avoid: Using company domain (too temporary); overly clever domains (hard to remember/spell)
2. Hosting: Use [Methodology Partner] managed WordPress hosting or high-quality provider (WP Engine, Kinsta)
3. SSL certificate: Enable HTTPS (non-negotiable for 2024+)
4. DNS: Point domain to hosting provider

**Step 2: WordPress Installation & Theme**
1. Use [Methodology Partner]' proprietary WordPress theme (optimized for personal brands)
   - Alternative: Neve Pro, Astra Pro (clean, conversion-focused)
   - Avoid: Heavy templates with excessive animations (slow, unprofessional)
2. Install essential plugins:
   - SEO: Rank Math or Yoast SEO (1 only, not both)
   - Analytics: MonsterInsights (GA4 integration)
   - Backup: Updraft Plus
   - Security: Wordfence
   - Forms: Gravity Forms or WPForms
   - Cache/Performance: WP Super Cache or W3 Total Cache
3. Delete unused plugins (every inactive plugin is security/performance risk)

**Step 3: Site Settings & SEO Foundation**
1. General Settings:
   - Site title: "[Client Name] — [Primary Industry/Niche]" (e.g., "Sarah Kim — Growth Marketing Expert")
   - Tagline: One-liner on positioning (e.g., "Helping founders grow without agencies")
2. Reading Settings:
   - Set homepage to static page (not blog feed)
   - Set blog page to custom page (not default posts page)
3. Permalink Settings:
   - Use `/%postname%/` structure (clean URLs)
4. Search Engine Visibility:
   - Ensure "Discourage search engines from indexing this site" is UNCHECKED
5. Create robots.txt (if needed) and sitemap (automatic via Rank Math)

**Step 4: Analytics & Tracking**
1. Connect Google Analytics 4 (GA4) to site
2. Create GA4 events for key actions:
   - Subscribe (newsletter signup)
   - Contact (form submission)
   - Download (lead magnet, resource)
   - Purchase/Inquiry (if applicable)
3. Add Google Search Console (monitor indexing, search performance)
4. Add Facebook Pixel (if running ads)
5. Verify tracking is firing (test via browser console or Supermetrics dashboard)

### Phase 2: Site Build & Content Structure

**Step 1: Homepage Design**
The homepage has 4-5 key sections:

**Section 1: Hero (Above fold)**
- Large, clear headline tied to unique value proposition
- Example: "I help founder-led businesses earn media coverage without agencies"
- Subheadline: Expand on value (one sentence)
- CTA button: Primary action (Subscribe, Work Together, Learn More)
- Background: Professional photo of client (authentic, not stock) or gradient
- No excessive animations; load time under 2 seconds

**Section 2: 3-5 Value Propositions**
Below hero, use 3 columns or cards to answer "Why you?"
```
[Icon/Image] [Icon/Image] [Icon/Image]

Expert Founder        Proven Systems      Real Results
[Description]         [Description]       [Description]
```

**Section 3: Social Proof**
- 3-5 client testimonials with headshot, name, title, company
- OR "As seen in" logos (Forbes, TechCrunch, etc. if applicable)
- OR impressive stats ("Helped 50+ founders," "Generated $2M in attributed revenue")

**Section 4: CTA Section**
Primary call-to-action (singular focus)
- "Subscribe to my weekly insights" (newsletter)
- "Book a consultation" (service sales)
- "Get the free guide" (lead magnet)
Use contrasting button color (not white/gray, use brand primary color)

**Section 5: Blog Preview (Optional)**
3 recent blog posts as grid cards, "Read All Articles" link to /blog

**Step 2: About Page**
The About page builds trust and connection. Structure:

**Section 1: About Hero**
- Large headline: "About [Name]"
- Professional photo (headshot, not selfie)
- One-paragraph bio (70-100 words) focusing on reader benefit, not credentials list

**Section 2: Origin Story**
- 2-3 paragraphs on the journey: Why did you start? What was the pain point?
- Real example: "After struggling to grow my own company, I realized most founders didn't understand growth marketing. That's when I started..."
- Make it personal but professional (not overly casual)

**Section 3: Core Beliefs / Philosophy**
- 3-5 core beliefs tied to Topic Wheel WHY
- Format as statements with brief explanation
- Example: "I believe founders can own their marketing." / "Too many founders hand off marketing to agencies and lose control. I teach founders how to build in-house marketing systems."

**Section 4: Key Metrics / Proof**
- Years in industry / projects completed
- Client results (e.g., "Helped founders grow revenue from X to Y")
- Speaking venues (Forbes, TechCrunch, major conferences)
- Media mentions

**Section 5: Credentials (Brief)**
- Education (degree, school)
- Certifications (if applicable)
- Notable roles (CPO at X, VP Marketing at Y)
- Keep brief — focus on relevance, not comprehensiveness

**Section 6: Social Proof (Testimonials)**
- 3-5 video testimonials preferred (authentic > written)
- If video unavailable, written testimonials with headshot, name, title, company
- Quote should be 1-2 sentences, specific benefit
- Example: "Sarah helped us grow our SaaS from $100K to $1M ARR in 18 months without hiring a marketing team." — [Name], CEO at [Company]

**Section 7: CTA**
- Clear next step: "Ready to work together?" / "Want to learn more?"
- Button to services, contact form, or calendar link

**Step 3: Blog/Article Page Structure**
Create blog post template with:

**Blog Post Structure:**
```
[Featured Image — 1200x630px, optimized]

# Article Title

[Author bio with photo and social links]
[Reading time estimate]
[Publication date]
[Category tags tied to Topic Wheel]

---

## Intro (100-150 words)
- Hook: Question, stat, or bold claim
- Context: Why this matters
- Promise: What reader will learn

## Body (organize using Topic Wheel)
### Section 1: [Topic Wheel theme]
- Key points (use subheadings)
- Supporting data/examples
- Related framework from Topic Wheel

### Section 2: [Related theme]
[Content]

### Section 3: [Related theme]
[Content]

## Conclusion (75-100 words)
- Recap key insights
- Next action (apply what they learned)
- CTA (subscribe, download resource, book call)

## Author Bio
[80-100 word bio, credential-focused, link to author page]

## Related Articles
[3 internal links to related blog posts]

## Call-to-Action
[Prominent button: "Get my free [resource]" or "Subscribe to my newsletter"]
```

**Blog Post Metadata (SEO):**
- Meta title: Primary keyword within first 60 characters
- Meta description: 155 characters, benefit-focused, includes keyword
- Focus keyword: One primary keyword per post (researched via SEMrush/Ahrefs)
- Internal links: 2-3 links to related posts/pages
- External links: 1-2 links to high-authority sources

**Step 4: Services/Offers Page**
Structure based on actual services client offers:

**Option A: Consulting/Coaching**
```
## Services

### 1-on-1 Consulting
[Description of service]
- Price: $X/month
- Duration: [e.g., 3-6 months]
- What's included: [Bullet list]
- [Case study] / [Testimonial]
- CTA: "Book a consultation"

### Group Workshops
[Description]
[Details]
[CTA]

### Speaking/Advisory
[Description]
[Details]
[CTA]
```

**Option B: Courses/Digital Products**
```
## Offerings

### [Course Name]
[Description + video preview]
- Price: $XXX (one-time or subscription)
- Lessons: X modules, Y hours
- Student testimonials
- Satisfaction guarantee
- CTA: "Enroll now"
```

**Key Elements:**
- Clear pricing (no hidden fees)
- What's included (detailed breakdown)
- Testimonial or case study proving the offer works
- FAQ addressing common objections
- Clear CTA (book, buy, contact)

**Step 5: Case Studies Page**
Proof-focused page showing results:

**Case Study Structure (per study):**
```
## Case Study: [Client Name/Project Title]

[Hero image: Before/After, or process flow]

### The Challenge
- [Client's initial situation]
- [Problem they faced]
- [Why it was hard to solve]

### The Approach
- [Your methodology applied]
- [Key steps taken]
- [Timeline]

### The Results
[Quantified metrics, not vanity metrics]
- Revenue growth: $X → $Y
- Time saved: X hours/month
- Market position: [Before] → [After]
- Client testimonial quote

### Key Lessons
- 2-3 takeaways for reader
- How this could apply to them

[CTA: "Let's discuss your situation" → Contact form / Calendar]
```

**Case Study Collection Best Practices:**
- Include 2-4 case studies (more than 4 is overwhelming)
- Vary industries/situations if possible
- Mix of revenue growth, cost savings, and strategic wins
- Always include specific metrics (not "significant growth")

### Phase 3: Topic Wheel Integration

**Step 1: Organize Blog by Topic Wheel**
Create category structure matching your Topic Wheel:

```
Blog Categories:
├── Why (Philosophy, worldview)
│   └── [Articles on core beliefs]
├── How-Systems (Methodology 1)
│   └── [Articles on frameworks, processes]
├── How-Process (Methodology 2)
│   └── [Articles on specific tactics]
└── What (Services, offers)
    └── [Articles on specific solutions]
```

**Implementation:**
1. Create categories in WordPress matching Topic Wheel
2. Assign existing blog posts to categories
3. Create category archive pages (auto-generated) with category description
4. Link internally from How/Why posts to related What services

**Step 2: Internal Linking Strategy**
Link related content within site to improve UX and SEO:

**How-to-Why links:**
"For more on my philosophy on growth systems, see [link to Why article]"

**How-to-What links:**
"Ready to implement this framework? [Link to service page] or [schedule consultation]"

**What-to-Case Study links:**
"Here's how I applied this approach for [Company]:" [Link to case study]

**Blog-to-Blog links:**
2-3 related articles at end of each post or in sidebar

**Ideal internal link count:**
- Per blog post: 2-3 internal links
- Per service page: 3-5 internal links to supporting content
- Per case study: 2-3 links to related services/blog posts

### Phase 4: SEO Optimization

**Step 1: Technical SEO**
- ✓ Site speed: <3 seconds load time (test via PageSpeed Insights)
- ✓ Mobile responsiveness: Test on mobile device
- ✓ SSL certificate: HTTPS on all pages
- ✓ XML sitemap: Submitted to Google Search Console
- ✓ robots.txt: Allows search engines, blocks spam/private pages
- ✓ Structured data: Schema markup (Article, Person, Organization)

**Step 2: On-Page SEO (Per Blog Post)**
- Primary keyword in title (first 60 chars)
- Primary keyword in meta description (first 155 chars)
- Primary keyword in H1 (should match title or be very similar)
- Primary keyword in first 100 words of body
- Internal links: 2-3 contextual links
- Keyword density: 1-2% (natural, not forced)
- Readability: Short paragraphs, subheadings, bullet points

**Step 3: Backlink Strategy (Authority Building)**
Personal brand sites need backlinks to rank. Build through:

1. **Guest posting**: Contribute to industry publications, link back to site
2. **Podcast appearances**: Get links in show notes
3. **Press coverage**: When featured in media, get coverage links
4. **Speaking**: Include website in speaker bios
5. **Resource pages**: Pitch to other sites' resource pages in your niche
6. **LinkedIn + social**: Share articles, drive referral traffic

**Step 4: Keyword Research (Pre-Content)**
Before writing any blog post:
1. Research 3-5 keywords related to topic
2. Check search volume (aim for 100+ monthly searches)
3. Assess difficulty (should be winnable for personal brand)
4. Use SEMrush, Ahrefs, or Ubersuggest
5. Pick ONE primary keyword per post
6. Build secondary keywords into content naturally

**Step 5: Content Optimization for E-E-A-T**
Google prioritizes E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):

- **Experience**: Share real stories, case studies, personal lessons ("I learned this the hard way")
- **Expertise**: Use data, frameworks, proven methodologies (not opinions)
- **Authoritativeness**: Credentials, speaking, media mentions in author bio
- **Trustworthiness**: Link to sources, cite studies, disclose affiliations, show client testimonials

## Quality Checks

### Before Launch Checklist

**Content Quality**
- ✓ All pages have unique, keyword-optimized meta descriptions
- ✓ Spelling/grammar reviewed (no typos)
- ✓ Images optimized (compressed, proper alt text)
- ✓ All internal links tested (no 404s)
- ✓ External links open in new tabs and are high-quality
- ✓ Author bios complete with photo and social links
- ✓ CTA buttons are visible and clickable on all devices

**Design & UX**
- ✓ Mobile responsive (test on iPhone, Android, tablet)
- ✓ Navigation clear and intuitive (menu under 6 items)
- ✓ Color scheme professional (2-3 primary colors, consistent)
- ✓ Typography readable (font size 16pt+ body text, sufficient contrast)
- ✓ No excessive animations or distracting elements
- ✓ Form fields are simple and clear (no more than 5 required fields)

**Technical**
- ✓ Site loads under 3 seconds (all pages)
- ✓ No console errors (check browser dev tools)
- ✓ Google Analytics firing on all pages
- ✓ Conversions tracking set up (newsletter signup, contact form, etc.)
- ✓ Search Console connected and sitemap submitted
- ✓ robots.txt correct (allows good content, blocks admin)
- ✓ Structured data valid (test via Google Structured Data Tool)

**Conversions**
- ✓ Primary CTA clear on homepage
- ✓ Secondary CTAs present on appropriate pages
- ✓ Contact form working (test submission)
- ✓ Newsletter signup functional (check confirmation)
- ✓ Calendar/booking link working (if applicable)
- ✓ Email deliverability tested (check spam folder)

**SEO**
- ✓ Each blog post has unique meta title and description
- ✓ Primary keyword in title and first 100 words
- ✓ Internal links present (2-3 per post)
- ✓ Featured image present on all blog posts (1200x630px)
- ✓ Reading time estimate visible
- ✓ Schema markup valid

### Post-Launch Monitoring (First 30 Days)

**Daily (First Week)**
- Monitor Google Search Console for crawl errors
- Check broken links (404 errors)
- Verify analytics are tracking
- Ensure forms are receiving submissions

**Weekly (Month 1)**
- Check Google Analytics: traffic sources, pages visited
- Monitor user experience: bounce rate, time on page
- Verify indexing in Google Search Console
- Test mobile experience on actual devices
- Check email deliverability (newsletter signup)

**Monthly (Ongoing)**
- Review analytics: top pages, traffic trends, conversions
- Check rankings for target keywords
- Monitor backlinks (use Ahrefs/SEMrush)
- Test site speed (PageSpeed Insights)
- Review user feedback (forms, comments)

## Common Pitfalls

### Design Pitfalls
**Problem**: Site looks impressive but feels corporate/impersonal
- **Why it happens**: Overuse of stock photos, generic copy, no personality
- **Fix**: Use real photos of client. Write in client's voice. Share real stories, not polished case studies.

**Problem**: Too many design elements; cluttered, hard to navigate
- **Why it happens**: Trying to showcase everything; no clear information hierarchy
- **Fix**: Apply 80/20: showcase top 20% of expertise. White space is good. One primary CTA per section.

**Problem**: Slow loading time hurts rankings and UX
- **Why it happens**: Unoptimized images, too many plugins, poor hosting
- **Fix**: Optimize images (use ShortPixel or Imagify). Limit plugins to essentials. Test speed monthly.

### Content Pitfalls
**Problem**: Blog content doesn't align with actual services/business model
- **Why it happens**: Content created without Topic Wheel; scattered topics
- **Fix**: Map all content to Topic Wheel first. No posts outside your framework.

**Problem**: Old content becomes outdated; rankings decline
- **Why it happens**: Publish once, never update
- **Fix**: Revisit top 10 posts quarterly. Update stats, examples, links. Republish with new date.

**Problem**: No clear Topic Wheel; content feels random
- **Why it happens**: Didn't define positioning upfront
- **Fix**: Stop creating content until you've defined Topic Wheel. Use it as gating for every new post.

### SEO Pitfalls
**Problem**: Site isn't ranking for target keywords
- **Why it happens**: No keyword research; competing with high-DA sites; insufficient backlinks
- **Fix**: Target long-tail keywords (less competition). Build backlinks through guest posts + media. Write comprehensive content.

**Problem**: High traffic but low conversion
- **Why it happens**: CTAs unclear or missing; pages optimized for traffic, not conversions
- **Fix**: Add clear CTA to every page. Test form simplicity (fewer fields = more conversions). Align messaging to user intent.

**Problem**: Good rankings but traffic doesn't match
- **Why it happens**: Low CTR in search results (bad title/meta description)
- **Fix**: A/B test titles and descriptions. Include benefit/emotion in meta. Use numbers when relevant.

### Topic Wheel Pitfalls
**Problem**: Topic Wheel is too broad; content gets scattered
- **Why it happens**: Too many How themes; lack of focus
- **Fix**: Limit to 3-5 themes max. Choose themes where you have unique POV/proof.

**Problem**: Topic Wheel isn't reflected in site navigation or content structure
- **Why it happens**: Topic Wheel created but not implemented
- **Fix**: Make Topic Wheel visible in navigation or sidebar. Create category pages. Link by theme.

**Problem**: No new content matching Topic Wheel
- **Why it happens**: Content calendar not aligned to framework
- **Fix**: Plan quarterly content calendar using Topic Wheel structure. Aim for 50% new, 50% existing content per theme.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Client interview for Topic Wheel (Phase 0, Step 1) | Execute | Client must articulate beliefs, methodologies, and offerings |
| Site architecture approval (Phase 0, Step 3) | Approve | Client reviews and approves page hierarchy before build begins |
| Content review before launch (Phase 2) | Review | All content reviewed for voice, accuracy, and brand alignment |
| WordPress publishing and technical setup (Phase 1) | Execute | Plugin installation, theme configuration, analytics setup |
| Featured image and photo selection | Execute | Must be real photos of client — not stock |
| Post-launch client sign-off | Approve | Client confirms site is ready for public |
| Monthly content updates | Review | Human reviews analytics and decides what content to update/add |

## Anti-Vandalism Checks
- [ ] Check what already exists before creating new content pages
- [ ] Verify no keyword cannibalization between blog posts targeting similar terms
- [ ] Confirm internal linking structure is maintained (no orphaned pages)
- [ ] Verify Topic Wheel categories in WordPress match the defined Topic Wheel
- [ ] Test all internal links before launch (no 404s)
- [ ] Structured data validates via Google Rich Results Test
- [ ] Revisit top 10 posts quarterly to prevent content decay

## Canon Compliance

- **Canon source:** 06-topic-wheel.md (Topic Wheel drives site architecture and content organization), 02-content-factory-process.md (site is the hub of the Content Factory output)
- **Triangles served:** CCS — the entire build process IS a checklist (launch checklist, SEO checklist, post-launch monitoring); GCT — Phase 0 starts with defining goals (positioning), content (Topic Wheel audit), and targeting (audience segments)
- **Human checkpoints:** Client interview for Topic Wheel definition (Step 1); client approval of site architecture before build; client review of all content before launch; post-launch client sign-off
- **Anti-vandalism:** Before-launch checklist with 25+ verification points; post-launch daily/weekly/monthly monitoring cadence; SEO validation via Google Search Console; structured data validation via Google Rich Results Test
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log

### Session: [Date]
**What worked well**:
- [E.g., "Client really resonated with the 'Why' section — positioned as thought leader immediately"]
- [E.g., "Internal linking strategy drove 40% of blog traffic to services page"]

**What was challenging**:
- [E.g., "Topic Wheel was too abstract until we made it visual/tangible"]
- [E.g., "Getting client to commit to consistent blog publishing was harder than building the site"]

**Client-specific insights**:
- [E.g., "Testimonial videos converted 2x better than written testimonials"]
- [E.g., "LinkedIn audience responded better to insights than detailed case studies"]

**Next cycle adjustments**:
- [E.g., "Start building personal brand site earlier in client relationship"]
- [E.g., "Use Topic Wheel to gate content creation — don't build without it"]

---

## Quick Reference: Site Launch Checklist

```
[ ] Domain purchased and DNS pointing to host
[ ] WordPress installed with theme and essential plugins
[ ] Google Analytics and Search Console connected
[ ] Homepage designed with hero, value props, social proof, CTA
[ ] About page with bio, story, beliefs, social proof
[ ] Blog page with category structure matching Topic Wheel
[ ] 5-10 blog posts published and optimized
[ ] Services/Offers page with clear pricing and CTA
[ ] 2-4 case studies with quantified results
[ ] Contact form working and tested
[ ] Newsletter signup functional and confirmed
[ ] All pages mobile-responsive and tested
[ ] Site speed under 3 seconds
[ ] All internal links tested (no 404s)
[ ] Meta titles and descriptions unique on all pages
[ ] Images optimized and alt text complete
[ ] Structured data (schema) validated
[ ] robots.txt and sitemap correct
[ ] Analytics tracking verified
[ ] Launch announcement: email, LinkedIn, social
[ ] Initial search console crawl completed
[ ] Post-launch monitoring plan set (daily Week 1, weekly Month 1, monthly ongoing)
```

