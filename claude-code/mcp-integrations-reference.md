# MCP Integrations Reference — Available & Recommended

**Last Updated:** 2026-03-30
**Purpose:** Track MCP servers available for the PRISM, with install commands and priority.

---

## Currently Connected

| MCP Server | Purpose | Status |
|-----------|---------|--------|
| Basecamp | Project management, to-dos, messages | Active |
| Ahrefs | Keyword research, backlinks, domain analysis | Active |
| Chrome (claude-in-chrome) | Browser automation, page reading | Active |
| Playwright | Headless browser automation | Active |
| Context7 | Live library/framework documentation | Active |

---

## Recommended — Not Yet Connected

### 1. WordPress MCP Adapter (HIGH PRIORITY)
**Why:** [Your Name] publishes articles for 5+ clients on WordPress. MCP would automate draft creation, category assignment, tag management — human just clicks Publish.

**Install on each client WordPress site:**
1. Install WordPress MCP Adapter plugin: `composer require wordpress/mcp-adapter` or download from https://github.com/WordPress/mcp-adapter
2. Generate application password in WordPress (Users > Your Profile > Application Passwords)
3. Connect to Claude Code:
```bash
claude mcp add client-wordpress https://[client-website.com]/wp-json/mcp/v1/http --transport http --header "Authorization: Bearer APP_PASSWORD"
```

**Canon compliance:** Human gate still required for final Publish action. MCP handles draft creation, metadata, schema insertion.

### 2. Google Search Console — mcp-gsc (HIGH PRIORITY)
**Why:** GSC data feeds MAA reports, content strategy, and KP Sprint tracking. Currently manual.

**Install:**
```bash
# Via Composio
claude mcp add gsc -- npx -y @anthropic-ai/composio-mcp google_search_console

# Via community mcp-gsc (more features, 20 tools)
# See: https://github.com/AminForou/mcp-gsc
claude mcp add gsc -- npx -y mcp-gsc
```
Requires Google OAuth setup. Follow: https://suganthan.com/blog/google-search-console-mcp-server/

### 3. Google Analytics MCP (MEDIUM PRIORITY)
**Why:** GA4 data for MAA reports, traffic analysis, conversion tracking.

**Install:**
```bash
# Official Google MCP
# See: https://developers.google.com/analytics/devguides/MCP
claude mcp add ga4 -- npx -y @anthropic-ai/google-analytics-mcp
```
Requires Google Cloud project with Analytics API enabled.

### 4. n8n MCP (LOW PRIORITY — when moving from Zapier)
**Why:** Read/write access to n8n workflow automation. [Your Automation Lead] currently building with Zapier.

**Install when ready:**
```bash
claude mcp add n8n -- npx -y @anthropic-ai/n8n-mcp
```

### 5. Firecrawl MCP (LOW PRIORITY — for bulk crawling)
**Why:** Bulk URL crawling when processing 100+ pages. Playwright handles small batches.

**Install when ready:**
```bash
claude mcp add firecrawl -- npx -y firecrawl-mcp
```
Free tier: 10 scrapes/min, 10 maps/min.

---

## Recommended Official Plugins (from anthropics/claude-plugins-official)

These are installable via `/plugin install <name>@claude-plugins-official`:

### HIGH PRIORITY

| Plugin | Install Command | Why |
|--------|----------------|-----|
| **wordpress.com** | `/plugin install wordpress.com@claude-plugins-official` | Direct WordPress content management. Complements WP MCP Adapter. |
| **zapier** | `/plugin install zapier@claude-plugins-official` | 8,000+ app connections. [Your Automation Lead] building Zapier automations — Claude could control them. |
| **adspirer-ads-agent** | `/plugin install adspirer-ads-agent@claude-plugins-official` | Cross-platform ad management (Google, Meta, TikTok, LinkedIn). Automates Dollar-a-Day. |

### MEDIUM PRIORITY

| Plugin | Install Command | Why |
|--------|----------------|-----|
| **searchfit-seo** | `/plugin install searchfit-seo@claude-plugins-official` | SEO toolkit. Supplements existing custom SEO skills. |
| **circleback** | `/plugin install circleback@claude-plugins-official` | Meeting, email, calendar context. Enhances /meeting-capture. |
| **frontend-design** | `/plugin install frontend-design@claude-plugins-official` | Production-grade frontend for KP Sprint personal brand sites. |
| **postiz** | `/plugin install postiz@claude-plugins-official` | Social media automation CLI. Automates Promote stage. |
| **zoominfo** | `/plugin install zoominfo@claude-plugins-official` | B2B contact search for prospect research. |

### Already Installed (15 active + 2 disabled)
**Active:** context7, code-review, code-simplifier, claude-md-management, feature-dev, github, hookify, mcp-server-dev, playwright, plugin-dev, ralph-loop, security-guidance, skill-creator, superpowers, telegram
**Disabled:** slack, claude-mem

---

## Additional MCP Servers (Community)

| Server | Install | Priority | Why |
|--------|---------|----------|-----|
| **Google Ads MCP** | `claude mcp add google-ads -- npx -y mcp-google-ads` | LOW (when using Google Ads) | Campaign analysis, budget optimization, keyword analytics via natural language. See: github.com/cohnen/mcp-google-ads |
| **Pipeboard** | See pipeboard.co | LOW | Connects ad platforms (Meta, Google, TikTok) to Claude via MCP |

## Community Skill to Consider

- **claude-ads** (github.com/AgriciDaniel/claude-ads) — 186-check paid ad audit across Google, Meta, YouTube, LinkedIn, TikTok, Microsoft. Weighted scoring + parallel agents. Alternative to building custom ad audit skills.

---

## Decision Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-03-30 | Skip claude-email plugin | Custom outreach-sequence skill + inbox-triage cover [Your Agency] needs |
| 2026-03-30 | Skip claude-seo plugin | Custom SEO skills (seo-audit, schema-markup, geo-optimizer) are better tailored |
| 2026-03-30 | Skip Firecrawl for now | Playwright + Chrome MCP sufficient for current scraping volume |
| 2026-03-30 | Prioritize WP MCP + GSC MCP | Highest ROI for content agency workflow automation |

---

## See Also
- [[memory-bank/05-vendor-and-partner-map|Vendor Map]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[sops/business-ops/api-security-and-access|API Security SOP]]
- [[claude-code/AUTOMATION-STATUS|Automation Status]]
