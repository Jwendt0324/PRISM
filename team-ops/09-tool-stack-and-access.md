---
title: "Tool Stack & Access Directory"
owner: {{OWNER_NAME}}
created: 2026-03-18
last_updated: 2026-03-18
version: 1.0
status: active
category: team-ops
---

# Tool Stack & Access Directory — {{COMPANY_NAME}}

Every tool we use, who owns it, who has access, and how to get in. If it's not on this list, we probably don't use it. If we do use it and it's not here, add it.

**Access gatekeeper for most tools: {{OPS_ADMIN_NAME}}** ({{OPS_ADMIN_EMAIL}}). When in doubt, email him.

---

## Master Tool Table

| Category | Tool | Purpose | Admin/Owner | Access Via |
|----------|------|---------|-------------|------------|
| Project Management | Basecamp | All project work, EODs, MAAs, client comms | {{ADVISOR_NAME}} / {{OPS_ADMIN_NAME}} | {{OPS_ADMIN_NAME}} provisions accounts |
| Communication | Google Workspace | Email (@{{COMPANY_DOMAIN}}) | {{OWNER_NAME}} / {{OPS_ADMIN_NAME}} | {{OPS_ADMIN_NAME}} creates accounts |
| Communication | Zoom | Client calls, Office Hours, standups | {{ADVISOR_NAME}} (host) | Calendar invites |
| Communication | Microsoft Teams | {{OWNER_NAME}}'s personal men's group | {{OWNER_NAME}} | N/A — personal |
| Content Production | Descript | Video/audio editing | Shared account (YCF) | {{OPS_ADMIN_NAME}} provides credentials |
| Content Production | CapCut | Video editing (short-form) | {{TEAM_MEMBER_NAME}} | Self-managed |
| Content Production | Google Photos | Media storage/sharing | {{ADVISOR_NAME}} | {{ADVISOR_NAME}} shares directly |
| Websites / Hosting | WP Engine | Shared WordPress hosting | {{SITE_ADMIN_NAME}} / {{OPS_ADMIN_NAME}} | {{OPS_ADMIN_NAME}} or Josh provisions |
| Websites / Hosting | WordPress (multiple sites) | Client and brand sites | {{OPS_ADMIN_NAME}} | WP Admin credentials via {{OPS_ADMIN_NAME}} |
| Websites / Hosting | GoDaddy | Domain registration (some sites) | {{SITE_ADMIN_NAME}} | Josh manages DNS |
| Websites / Hosting | Amazon Route 53 | DNS management (some sites) | {{SITE_ADMIN_NAME}} | Josh manages records |
| Websites / Hosting | BlitzAdmin (blitzadmin.com) | Centralized credential store | {{SITE_ADMIN_NAME}} | Josh shares credentials |
| Social Media | YouTube | Brand and personal channels | {{OPS_ADMIN_NAME}} manages access | {{OPS_ADMIN_NAME}} provisions |
| Social Media | Facebook Group | facebook.com/groups/highriseacademy | {{OWNER_NAME}} / {{ADVISOR_NAME}} | Request via {{OPS_ADMIN_NAME}} |
| Social Media | Jumper Media | Social media automation | {{OPS_ADMIN_NAME}} (tracking) | Admin: {{ADMIN_EMAIL}} |
| Social Media | LinkedIn | {{OWNER_NAME}}'s profile, {{ADVISOR_NAME}}'s profile | Individual owners | Self-managed |
| Scheduling | Calendly | Discovery calls, AI Apprentice audits | {{OWNER_NAME}} / {{ADVISOR_NAME}} | Self-managed; {{OPS_ADMIN_NAME}} assists setup |
| LMS / Training | Content Factory Academy | AI Apprentice coursework | {{OPS_ADMIN_NAME}} | academy.yourcontentfactory.com |
| Advertising | Google Ads | Paid campaigns (Dollar-a-Day, client) | {{OWNER_NAME}} / Luke Crowson | Account-level access via Google |
| Analytics | Google Search Console | SEO monitoring, indexing | {{OWNER_NAME}} | Google account access |
| Analytics | SPP (Service Provider Pro) | Sales/revenue tracking, weekly reports | {{OPS_ADMIN_NAME}} / Hezekiah | {{OPS_ADMIN_NAME}} provisions |
| Finance | Community Resource Bank | Revenue deposits ({{OWNER_NAME}}'s entity) | {{OWNER_NAME}} | {{OWNER_NAME}} manages directly |
| Finance | Zelle | Refunds, contractor payments | {{ADVISOR_NAME}} / {{OPS_ADMIN_NAME}} | Individual bank accounts |
| Automation | Zapier | Onboarding automation, workflows | Hezekiah / {{OPS_ADMIN_NAME}} | {{OPS_ADMIN_NAME}} provisions |
| AI Tools | Claude (Anthropic) | Content production, operations, Claude Code | {{OWNER_NAME}} | {{OWNER_NAME}}'s subscription |
| AI Tools | ChatGPT (OpenAI) | Site updates, content | {{ADVISOR_NAME}} | {{ADVISOR_NAME}}'s account |
| AI Tools | Vendasta | Voice assistants, local business tools | {{SITE_ADMIN_NAME}} / Michael | Josh manages setup |
| File Storage | Google Drive (shared) | Team file sharing, client folders | {{OPS_ADMIN_NAME}} | {{OPS_ADMIN_NAME}} shares folders |
| File Storage | Google Sheets (Team Roster) | Team tracking | {{OPS_ADMIN_NAME}} | [Team Roster Sheet](https://docs.google.com/spreadsheets/d/1lQT3Ckkxe6wmuews0ES6fw7wPgOLwZ41v4mSBQy7jco/) |

---

## Detailed Tool Notes

### Project Management

#### Basecamp
- **URL:** basecamp.com/4057320
- **What it does:** System of record for all project work. Task assignments, EOD reports, MAA reports, client-visible threads, internal threads, file sharing. Everything about a client or deliverable lives here.
- **Admin:** {{ADVISOR_NAME}}, {{OPS_ADMIN_NAME}}
- **Who has access:** Full team — {{OWNER_NAME}}, {{ADVISOR_NAME}}, {{OPS_PARTNER_NAME}}, {{OPS_ADMIN_NAME}}, {{OWNER_NAME}}son, Josh, Luke, Daniel, Henry, Grant, Hezekiah, Braden, Fredrick, Jeffry, plus clients on their project threads
- **How to get access:** Email {{OPS_ADMIN_NAME}}. He creates accounts and assigns to projects.
- **Key projects:** BlitzMetrics HQ (team-wide), Local Service Spotlight (LSS umbrella), individual client projects (e.g., "{{COMPANY}}'s Google Knowledge Panel: Ryan D. Lee"), AI Apprentice projects per student
- **Notes:** Basecamp sends email notifications from `notifications@3.basecamp.com`. All EOD and MAA reports are posted here. {{ADVISOR_NAME}} is emphatic that project communication belongs in Basecamp, not email.

---

### Communication

#### Google Workspace (highriseinfluence.net)
- **What it does:** Email and productivity suite for {{COMPANY}}.
- **Admin:** {{OWNER_NAME}}, {{OPS_ADMIN_NAME}}
- **Active accounts:** {{USER_EMAIL}}, {{TEAM_MEMBER_EMAIL}}
- **How to get access:** {{OPS_ADMIN_NAME}} creates workspace accounts. {{SITE_ADMIN_NAME}} handles DNS/MX record setup on the hosting side.
- **Notes:** Google Workspace verification requires TXT records added to DNS. Josh handles this via Route 53 or GoDaddy depending on the domain.

#### Zoom
- **What it does:** Video conferencing for client interviews, AI Apprentice Office Hours, weekly standups, and ad-hoc calls.
- **Meeting ID (Office Hours):** 895 4884 7054
- **Schedule:** AI Apprentice Office Hours — Thursdays, 2:00 PM PST. Weekly standup — Tuesdays, 30 minutes.
- **Admin:** {{ADVISOR_NAME}} hosts most recurring meetings via his Zoom account.
- **How to join:** Calendar invites sent via Google Calendar. Zoom links embedded in Calendly bookings for audit calls.
- **Notes:** {{ADVISOR_NAME}} schedules client audit calls (15-minute blocks) through Calendly, which auto-generates Zoom links.

#### Microsoft Teams
- **What it does:** {{OWNER_NAME}}'s personal men's group. Tuesdays.
- **Notes:** Not an {{COMPANY}} tool. Personal use only. Listed here so nobody tries to set up Teams for work — we use Basecamp.

---

### Content Production

#### Descript
- **URL:** web.descript.com
- **What it does:** Video and audio editing. Transcription, screen recording, clip creation.
- **Shared account:** {{SHARED_ACCESS_EMAIL}}
- **How to get access:** Email {{OPS_ADMIN_NAME}} for credentials. Login sends a verification code to the shared email ({{SHARED_ACCESS_EMAIL}}), so you need {{OPS_ADMIN_NAME}} to relay the code or have access to that inbox.
- **Who uses it:** {{TEAM_MEMBER_NAME}}, {{OWNER_NAME}}, broader BM team
- **CRITICAL NOTE:** LSS is under budget constraints. {{OPS_ADMIN_NAME}} explicitly stated (March 2026): "LSS is currently facing budget constraints, and we are not able to cover additional tool subscriptions at this time." Do NOT request new Descript seats or upgrades without clearing it with {{OWNER_NAME}} and {{ADVISOR_NAME}} first.
- **Notes:** This is a shared account across the YCF/BM ecosystem, not an {{COMPANY}}-owned subscription.

#### CapCut
- **What it does:** Video editing, primarily short-form content.
- **Who uses it:** {{TEAM_MEMBER_NAME}}
- **Access:** Self-managed. {{OWNER_NAME}}son uses his own account.
- **Notes:** Free tier is sufficient for current needs. No shared account needed.

#### Google Photos
- **What it does:** {{ADVISOR_NAME}} stores and shares media (photos, videos from events, speaking engagements, client shoots).
- **Admin:** {{ADVISOR_NAME}}
- **How to access:** {{ADVISOR_NAME}} shares albums/folders directly via Google Photos links.
- **Notes:** Not a formal team tool — more of a {{ADVISOR_NAME}} workflow. Content often needs to be pulled from Google Photos links he drops in Basecamp threads.

---

### Websites / Hosting

#### WP Engine
- **What it does:** Managed WordPress hosting for all {{COMPANY}} and client sites.
- **Admin:** {{SITE_ADMIN_NAME}}, {{OPS_ADMIN_NAME}}
- **Who manages:** Josh handles technical issues, server-level changes, support tickets. {{OPS_ADMIN_NAME}} handles WP Admin credentials and user provisioning.
- **Sites hosted:** highriseinfluence.net, localservicespotlight.com, client personal brand sites, academy.yourcontentfactory.com, and others
- **How to get access:** Email {{OPS_ADMIN_NAME}} for WP Admin access to specific sites. Email Josh for hosting-level or DNS issues.
- **Notes:** Josh regularly follows up with WP Engine on support tickets. WP Engine is the shared hosting platform across the entire BM/LSS/{{COMPANY}} ecosystem.

#### Key Websites

| Site | Purpose | WP Admin Access Via |
|------|---------|-------------------|
| highriseinfluence.net | {{COMPANY}} primary site | {{OPS_ADMIN_NAME}} |
| localservicespotlight.com | LSS site | {{OPS_ADMIN_NAME}} |
| academy.yourcontentfactory.com | Content Factory Academy LMS | {{OPS_ADMIN_NAME}} |
| blitzmetrics.com | BlitzMetrics main site | {{ADVISOR_NAME}} / Fredrick |
| Client personal brand sites | KP Sprint deliverables | {{OPS_ADMIN_NAME}} provisions per project |

#### GoDaddy
- **What it does:** Domain registration and DNS for some sites.
- **Admin:** {{SITE_ADMIN_NAME}}
- **Notes:** Josh shared GoDaddy login with {{OPS_PARTNER_NAME}}. Some domains use GoDaddy DNS, others use Route 53.

#### Amazon Route 53
- **What it does:** DNS management for certain domains.
- **Admin:** {{SITE_ADMIN_NAME}}
- **Notes:** Used for domains like funeralhomeexit.com. TXT records for Google Workspace verification, MX records for email routing. Josh manages all DNS changes.

#### BlitzAdmin (blitzadmin.com)
- **What it does:** Centralized credential/password store for the BM ecosystem.
- **Admin:** {{SITE_ADMIN_NAME}}
- **Notes:** Josh references this for WP Admin passwords across sites.

---

### Social Media

#### YouTube
- **What it does:** Video hosting. {{COMPANY}} brand channel, {{OWNER_NAME}}'s personal channel, client channels.
- **Admin:** {{OPS_ADMIN_NAME}} manages access/permissions.
- **How to get access:** Request via {{OPS_ADMIN_NAME}}.

#### Facebook Group — High Rise Academy
- **URL:** facebook.com/groups/highriseacademy
- **What it does:** Community group for AI Apprentice students and {{COMPANY}} audience.
- **Admin:** {{OWNER_NAME}}, {{ADVISOR_NAME}}
- **How to get access:** Request to join on Facebook; admins approve.

#### Jumper Media
- **What it does:** Social media automation (auto-posting, engagement tools).
- **Admin email:** {{ADMIN_EMAIL}}
- **Who manages:** {{OPS_ADMIN_NAME}} tracks access. Setup origin is unclear — team-wide audit in March 2026 could not determine who originally created the dashboard.
- **How to get access:** Email {{OPS_ADMIN_NAME}}. He coordinates with Jumper Media support.
- **Notes:** {{OPS_ADMIN_NAME}} met with Mason (Jumper Media rep) to update admin email without affecting the account. Active effort to clean up ownership.

#### LinkedIn
- **What it does:** Professional networking, content distribution.
- **Key profiles:** {{OWNER_NAME}} (linkedin.com/in/jack-wendt-124293302/), {{ADVISOR_NAME}} (linkedin.com/in/dennisyu)
- **Notes:** Self-managed by individuals. No shared company page admin structure documented yet.

---

### Scheduling

#### Calendly
- **URL:** calendly.com
- **What it does:** Scheduling for discovery calls and AI Apprentice audit calls.
- **Active event types:** "AI Apprenticeship Audit" (15-min blocks, includes Zoom link), "{{COMPANY}} Knowledge Panel Package"
- **Admin:** {{OWNER_NAME}}, {{ADVISOR_NAME}} ({{ADVISOR_NAME}} schedules audit calls that include {{OWNER_NAME}})
- **How to get access:** Self-service — each person manages their own Calendly.
- **Notes:** Calendly notifications go to {{USER_EMAIL}}. {{ADVISOR_NAME}} books calls on {{OWNER_NAME}}'s behalf. Calendly auto-generates Zoom links and calendar invites.

---

### LMS / Training

#### Content Factory Academy
- **URL:** academy.yourcontentfactory.com/wp-admin/
- **What it does:** WordPress-based LMS for AI Apprentice Program coursework. Content Factory certification curriculum.
- **Admin:** {{OPS_ADMIN_NAME}}
- **How to get access:** Email {{OPS_ADMIN_NAME}} with the student's email. He creates credentials and sends login info directly.
- **Notes:** Free access offered to qualified prospects as a sales incentive. {{OPS_ADMIN_NAME}} handles all provisioning.

---

### Advertising

#### Google Ads
- **What it does:** Paid advertising — Dollar-a-Day campaigns, client PMAX campaigns, search campaigns.
- **Admin:** {{OWNER_NAME}} ({{COMPANY}} account), Luke Crowson (client accounts like Plumbing Pros, Ardmor's)
- **Who monitors:** Jeffry de Castro tracks keyword performance, CPC, ad spend, policy violations.
- **Notes:** Ads getting disapproved for Google Ads policy issues (multiple incidents March 2026). Jeffry monitors and reports in EODs. Luke sets up new campaigns and works directly with Google Ads reps.

---

### Analytics

#### Google Search Console
- **What it does:** SEO monitoring, indexing status, disavow file management.
- **Admin:** {{OWNER_NAME}}
- **Key site:** highriseinfluence.net
- **Notes:** Disavow file was updated for highriseinfluence.net in March 2026. Notifications go to {{USER_EMAIL}}.

#### SPP (Service Provider Pro)
- **What it does:** Service and payment portal. Revenue tracking. Weekly reports.
- **Admin:** {{OPS_ADMIN_NAME}}, Hezekiah Orteza
- **URL:** localservicespotlight via SPP
- **Notes:** Hezekiah works on "Personal Brand Website Service in SPP." Weekly reports sent to team. Used for tracking sales pipeline and revenue.

---

### Finance / Admin

#### Community Resource Bank
- **What it does:** {{OWNER_NAME}}'s banking entity for {{COMPANY}} revenue deposits.
- **Admin:** {{OWNER_NAME}}
- **Notes:** {{OWNER_NAME}} manages directly. Revenue distributions tracked separately.

#### Zelle
- **What it does:** Peer-to-peer payments for refunds and contractor payments.
- **Who uses:** {{ADVISOR_NAME}} (sends payments), {{OPS_ADMIN_NAME}} (coordinates)
- **Notes:** $1,000 daily sending limit to new accounts. Used for refunds (e.g., $1,494 refund processed via Zelle in March 2026).

---

### Automation

#### Zapier
- **What it does:** Workflow automation. AI Apprentice onboarding flows, email broadcasts.
- **Admin:** Hezekiah Orteza, {{OPS_ADMIN_NAME}}
- **How to get access:** Email {{OPS_ADMIN_NAME}}.
- **Notes:** Hezekiah manages onboarding automation and documentation workflows. Weekly email broadcasts for AI Apprentice Program run through Zapier.

---

### AI Tools

#### Claude (Anthropic)
- **What it does:** Content production, article writing, operations automation, Claude Code for development and system-building.
- **Admin:** {{OWNER_NAME}}
- **Subscription:** {{OWNER_NAME}} pays for Claude Code personally.
- **Who uses:** {{OWNER_NAME}} (primary), Grant Haugen (got a "Claude 20x subscription" for content repurposing), {{SITE_ADMIN_NAME}} (uses Claude for DNS/MX record work)
- **Notes:** Central to {{COMPANY}} operations. Used for article writing from transcripts, SOP creation, operational automation, and site technical work.

#### ChatGPT (OpenAI)
- **What it does:** Site updates, content generation.
- **Admin:** {{ADVISOR_NAME}}
- **Who uses:** {{ADVISOR_NAME}} (primary — uses it for client site updates via code generation)
- **Notes:** {{ADVISOR_NAME}} mentioned using ChatGPT to make site improvements for client projects. Not a shared team tool.

#### Vendasta
- **What it does:** Voice assistants, local business tools.
- **Admin:** {{SITE_ADMIN_NAME}} coordinates with Michael (external contact)
- **Notes:** Josh testing Vendasta voice assistants for phone-based AI applications. Exploratory — not yet core to {{COMPANY}} delivery.

---

### File Storage

#### Google Drive (Shared)
- **What it does:** Team file sharing. Client content folders. Media assets.
- **Admin:** {{OPS_ADMIN_NAME}} manages access and folder structure.
- **How to get access:** {{OPS_ADMIN_NAME}} shares specific folders via Google Drive links.
- **Notes:** Client-specific folders created during onboarding. AI Apprentice students get their own Google Drive folders for content uploads (e.g., Kayla Scovel folder created March 2026). {{ADVISOR_NAME}} directs students to "get as much content, videos, proof, articles, etc into the Google Drive folder."

#### Google Sheets — Team Roster
- **URL:** [Team Roster](https://docs.google.com/spreadsheets/d/1lQT3Ckkxe6wmuews0ES6fw7wPgOLwZ41v4mSBQy7jco/)
- **What it does:** Team member tracking.
- **Admin:** {{OPS_ADMIN_NAME}}
- **Notes:** Living document. {{OPS_ADMIN_NAME}} maintains.

---

## Shared Email Accounts

These shared emails route through team members. Know who monitors them.

| Email | Purpose | Monitored By |
|-------|---------|-------------|
| {{SHARED_ACCESS_EMAIL}} | Shared tool logins (Descript, etc.) | {{OPS_ADMIN_NAME}} / Hezekiah |
| access@blitzmetrics.com | Shared tool logins | Hezekiah (weekly email log monitoring) |
| {{ADMIN_EMAIL}} | Jumper Media admin, other services | {{OPS_ADMIN_NAME}} |
| operations@blitzmetrics.com | Operations team distribution list | {{OPS_ADMIN_NAME}}, {{OPS_PARTNER_NAME}} |

---

## Access Request Process

1. **New team member needs tool access?** Email {{OPS_ADMIN_NAME}} at {{OPS_ADMIN_EMAIL}} with:
   - Person's name and email
   - Which tools they need
   - Which projects they'll work on
2. **{{OPS_ADMIN_NAME}} provisions** Basecamp, Google Workspace, WP Admin, Academy, Google Drive, and any other tools as needed.
3. **{{SITE_ADMIN_NAME}} handles** anything DNS, hosting, or WP Engine related.
4. **{{OWNER_NAME}} approves** any new tool subscriptions or paid seat additions.

---

## Gaps and Action Items

These are known gaps in the tool stack. Flagged for future resolution.

| Gap | Impact | Recommendation |
|-----|--------|---------------|
| **No formal CRM** | Discovery calls and pipeline tracked informally. No centralized lead tracking. | Evaluate lightweight CRM (HubSpot free, Pipedrive, or even a Google Sheet pipeline tracker) |
| **No shared password manager** | Credentials shared via email. BlitzAdmin exists but is Josh-specific. | Consider 1Password or Bitwarden for team-wide credential management |
| **Jumper Media admin ownership unclear** | Nobody on the team originally set up the dashboard. {{OPS_ADMIN_NAME}} coordinating cleanup. | {{OPS_ADMIN_NAME}} to complete admin email migration with Jumper Media support |
| **LinkedIn — no company page management** | No documented admin structure for an {{COMPANY}} LinkedIn company page | {{OWNER_NAME}} to determine if {{COMPANY}} needs a company page vs. personal brand only |
| **Descript budget constraints** | LSS can't cover new subscriptions. Shared account has friction (verification code relay). | If content production scales, {{OWNER_NAME}} may need to fund an {{COMPANY}}-owned Descript subscription |
| **Calendly setup incomplete** | {{OWNER_NAME}} noted he "needs to set up his link" — may not have all event types configured | {{OWNER_NAME}} to audit Calendly event types and ensure all sales/intake paths are covered |

---

## Learnings Log

- **2026-03-18 (v1.0):** Initial catalog built from Gmail evidence and operating documents. Key finding: {{OPS_ADMIN_NAME}} is the single point of access for nearly every tool. If {{OPS_ADMIN_NAME}} is unavailable, tool provisioning stops. {{SITE_ADMIN_NAME}} is the backup for hosting/DNS specifically. Budget constraints at LSS are real — do not assume LSS will fund new subscriptions without explicit approval.
