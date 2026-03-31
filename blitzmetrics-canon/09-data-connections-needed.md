---
tags:
  - status/active
  - triangle/PPP
  - type/canon
---

# Data Connections Needed — [Methodology Partner] Canon

**Source:** [Your Mentor/Advisor] feedback point #4, Operations Guide, Digital Plumbing course
**Version:** 1.0 | **Extracted:** 2026-03-19

---

## Purpose

[Your Mentor/Advisor]'s directive: "You'd need to connect other data systems and tools." This document maps what data systems the PRISM should connect to, what data they provide, and the current connection status.

---

## Priority 1: Connected or Readily Available

### Gmail ([your-email@your-agency.com])
- **Data:** Client communications, team updates, prospect threads, financial transactions
- **Access:** Gmail API via MCP integration
- **Status:** CONNECTED — Weekly memory bank refresh scans Gmail
- **Value:** Client health signals, dropped action items, relationship tracking

### Google Drive ([Methodology Partner] Shared Drive)
- **Data:** Master Guides, SOPs, templates, Content Libraries, client folders
- **Access:** Google Drive for Desktop (local sync)
- **Status:** CONNECTED — Synced to ~/Library/CloudStorage/
- **Value:** Canonical framework source, client deliverables

### Basecamp (basecamp.com/4057320)
- **Data:** Project threads, to-dos, client updates, MAA reports, team communication
- **Access:** Basecamp email notifications → Gmail scan
- **Status:** PARTIAL — Scanning email notifications, not direct API
- **Needed:** Direct Basecamp API access for real-time project health
- **Value:** Project status, blocked items, client satisfaction signals

---

## Priority 2: Needed for MAA and Performance Tracking

### Google Analytics
- **Data:** Website traffic, user behavior, conversion tracking, audience demographics
- **Access:** GA4 API (requires service account)
- **Status:** NOT CONNECTED
- **Needed:** API credentials for client sites ([Client — Local Retail Business], [your-username].com, funeralhomeexit.com)
- **Value:** Automated Metrics section of [[blitzmetrics-canon/05-maa-framework|MAA]] reports
- **Complexity:** Medium — API setup + per-site configuration

### Google Search Console
- **Data:** Search queries, impressions, clicks, CTR, average position, indexing status
- **Access:** Search Console API
- **Status:** NOT CONNECTED
- **Needed:** Verified ownership or delegated access per site
- **Value:** SEO performance tracking, content ranking validation
- **Complexity:** Medium

### YouTube Analytics
- **Data:** Video views, watch time, subscriber growth, engagement, traffic sources
- **Access:** YouTube Data API v3
- **Status:** NOT CONNECTED
- **Needed:** OAuth credentials for client YouTube channels
- **Value:** Video performance in MAA, identifying Dollar-a-Day candidates
- **Complexity:** Medium

### Facebook Ads Manager
- **Data:** Ad spend, CPA, ROAS, audience performance, creative performance
- **Access:** Facebook Marketing API
- **Status:** NOT CONNECTED
- **Needed:** Business Manager admin access, API tokens
- **Value:** Dollar-a-Day campaign tracking, automated campaign health dashboard
- **Complexity:** High — Facebook API is complex and frequently changes

---

## Priority 3: Needed for Business Operations

### Stripe
- **Data:** Revenue, payments, subscriptions, refunds, customer records
- **Access:** Stripe API
- **Status:** NOT CONNECTED
- **Needed:** API keys (restricted to read-only)
- **Value:** Automated P&L tracking, revenue reporting (addressing [Your Mentor/Advisor]'s financial transparency push). Feeds into [[blitzmetrics-canon/02-content-factory-process|Content Factory]] performance tracking.
- **Complexity:** Low — well-documented API

### WordPress (Client Sites)
- **Data:** Published content, drafts, categories, tags, comments, page performance
- **Access:** WordPress REST API
- **Status:** NOT CONNECTED
- **Needed:** Application passwords per site
- **Value:** Content publishing automation, content tree verification, anti-vandalism checks
- **Complexity:** Low-Medium

### Keap (Infusionsoft)
- **Data:** Contact records, email sequences, campaign performance, sales pipeline
- **Access:** Keap API
- **Status:** NOT CONNECTED ([Your Automation Lead] building Zapier → Keap automation)
- **Value:** Lead tracking, onboarding automation verification
- **Complexity:** Medium

---

## Priority 4: Nice-to-Have

### SPP (Service Provider Pro)
- **Data:** Client portal activity, project status
- **Access:** API (if available)
- **Status:** NOT CONNECTED
- **Value:** Client onboarding verification

### Calendly
- **Data:** Scheduled calls, availability
- **Access:** Calendly API
- **Status:** NOT CONNECTED
- **Value:** Prospect follow-up automation

### TimeCamp
- **Data:** Team time tracking, billable hours
- **Access:** TimeCamp API
- **Status:** NOT CONNECTED
- **Value:** Team utilization tracking

---

## Recommendations

1. **Start with Stripe** — Easiest to connect, highest value (P&L tracking [Your Mentor/Advisor] is pushing for)
2. **Add Google Analytics + Search Console** — Automates the Metrics section of MAA
3. **Add YouTube Analytics** — Completes content performance picture
4. **Basecamp direct API** — Replaces email scanning with real-time data
5. **WordPress API** — Enables content publishing verification and anti-vandalism
6. **Facebook Ads** — Save for when Dollar-a-Day campaigns are actively running at scale

---
## See Also
- [[blitzmetrics-canon/02-content-factory-process|Content Factory Process]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[memory-bank/05-vendor-and-partner-map|Vendor and Partner Map]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[sops/business-ops/api-security-and-access|API Security SOP]]