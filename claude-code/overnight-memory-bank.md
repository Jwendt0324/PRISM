# Overnight Task: Build the PRISM Shared Memory Bank + Gmail Deep Scan

## Instructions for Claude Code

Copy everything below the line into Claude Code and let it run overnight.

---

You are building a comprehensive Shared Memory Bank for [Your Name]'s Claude PRISM. This is the single source of truth about [Your Name], his businesses, his team, his clients, his relationships, and his history. Every future Claude session (Code, Cowork, Chat) should be able to read this memory bank and immediately have full context without [Your Name] re-explaining anything.

You also have access to [Your Name]'s Gmail via MCP tools. You will scan his ENTIRE inbox to extract context, relationships, deals, patterns, and institutional knowledge.

**CRITICAL: Only scan the Gmail account [your-email@your-agency.com]. Do NOT access, read, or search any other Gmail account. If the MCP connects to multiple accounts, ensure every gmail_search_messages and gmail_read_message call is scoped to [your-email@your-agency.com] only. Verify this before starting the scan.**

## Step 0: Read Existing PRISM

Read everything in the PRISM first so you don't duplicate what already exists:
- ~/Documents/Claude/PRISM/INDEX.md
- All files in ~/Documents/Claude/PRISM/sops/ (recursively)
- All files in ~/Documents/Claude/PRISM/skills/
- ~/Documents/Claude/PRISM/claude-code/CLAUDE.md

Also read the operating documents on [Your Name]'s Desktop for business context:
- ~/Desktop/Operating Documents/ (all files)
- ~/Desktop/PDFs/ (all files)

## Step 1: Build the Core Memory Bank Structure

Create this directory and file structure:
```
~/Documents/Claude/PRISM/memory-bank/
├── 00-[your-username].md              ← Everything about [Your Name] personally
├── 01-hri-overview.md            ← [Your Agency Name]: mission, structure, history
├── 02-blitzmetrics-overview.md   ← [Methodology Partner]: relationship, methodology, shared systems
├── 03-team-directory.md          ← Every person, their role, comp, relationship to [Your Name]
├── 04-client-directory.md        ← Every client past and present, status, history
├── 05-vendor-and-partner-map.md  ← Tools, platforms, service providers, partnerships
├── 06-deal-history.md            ← Every deal/engagement: who, what, when, outcome
├── 07-relationship-map.md        ← Key relationships, how they started, current status
├── 08-communication-patterns.md  ← How [Your Name] communicates, email habits, tone, preferences
├── 09-project-history.md         ← Major projects, timelines, outcomes, lessons
├── 10-financial-context.md       ← Revenue, pricing, comp structures, projections (from docs)
├── 11-content-assets.md          ← Published content, speaking, books, podcasts, authority signals
├── 12-strategic-context.md       ← Current priorities, challenges, opportunities, decisions pending
├── 13-gmail-insights.md          ← Key insights extracted from Gmail scan
└── INDEX.md                      ← Master index of the memory bank
```

## Step 2: Gmail Deep Scan

Use the Gmail MCP tools (gmail_search_messages, gmail_read_message, gmail_read_thread) to scan [Your Name]'s entire inbox. This is the most important and time-consuming phase.

### Scan Strategy (work through these searches systematically):

**Business Relationships:**
- Search: "from:dennis" OR "to:dennis" — Map the full [Your Mentor/Advisor] relationship, key decisions, project discussions
- Search: "from:dylan" OR "to:dylan" — [Your Ops Partner] [Last Name] interactions, platform work, equity discussions
- Search: "from:sam" OR "to:sam" — [Your AgentBuilder Partner] McLeod, delivery work, PM discussions
- Search: "from:muzamil" OR "to:muzamil" — Ops/finance discussions
- Search: "from:caleb" OR "to:caleb" — [Your Former Mentor] Guilliams / BetterWealth relationship

**Clients & Deals:**
- Search: "knowledge panel" — All KP Sprint discussions, client communications
- Search: "proposal" OR "invoice" OR "contract" — Deal history and terms
- Search: "onboarding" OR "kickoff" OR "intake" — Client onboarding patterns
- Search: "$6,000" OR "$2,500" OR "payment" — Financial transactions and pricing discussions
- Search: "close" OR "deal" OR "signed" — Deal closings

**Business Operations:**
- Search: "high rise influence" — All [Your Agency]-related communications
- Search: "blitzmetrics" — All [Methodology Partner] interactions
- Search: "content factory" — Content Factory methodology discussions
- Search: "apprentice" OR "certification" OR "cohort" — AI Apprentice Program communications
- Search: "local service spotlight" OR "[Partner Platform]" — [Partner Platform] development discussions

**Strategic & Planning:**
- Search: "strategy" OR "roadmap" OR "plan" — Strategic discussions
- Search: "equity" OR "vesting" OR "ownership" — Equity and ownership discussions
- Search: "revenue" OR "P&L" OR "profit" — Financial planning
- Search: "hire" OR "contractor" OR "VA" — Team building discussions

**Content & Marketing:**
- Search: "article" OR "blog" OR "publish" — Content production communications
- Search: "podcast" OR "interview" OR "recording" — Media and podcast discussions
- Search: "youtube" OR "video" OR "shorts" — Video content discussions
- Search: "dollar a day" OR "ad spend" OR "boost" — Paid media discussions
- Search: "SEO" OR "knowledge panel" OR "schema" — SEO and authority building

**Events & Speaking:**
- Search: "digimarcon" OR "conference" OR "speaking" — Events and speaking engagements
- Search: "webinar" OR "live" OR "office hours" — Online events

**Tools & Platforms:**
- Search: "basecamp" OR "notion" OR "airtable" — Project management tools
- Search: "stripe" OR "payment" — Payment processing
- Search: "descript" OR "canva" — Content tools
- Search: "wordpress" OR "site build" OR "domain" — Web development

**Personal Context:**
- Search: "army" OR "guard" OR "military" OR "drill" — Military service context
- Search: "nashville" OR "minnesota" — Location context
- Search: "betterwealth" OR "caleb" — Origin story and early career

### For each search:
1. Use gmail_search_messages with maxResults=50 to get the messages
2. For the most important/recent threads, use gmail_read_thread to get full context
3. Extract: who was involved, what was discussed, decisions made, action items, relationship dynamics
4. Paginate through results if there are more (use nextPageToken)
5. Don't read every single email — skim subjects/snippets first, then deep-read the ones that contain strategic context, relationship dynamics, deal terms, or decisions

### Important: Be thorough but smart
- Focus on emails that reveal relationships, decisions, deal terms, strategy, and patterns
- Skip newsletters, automated notifications, and spam
- Pay special attention to threads with [Your Mentor/Advisor], [Your Ops Partner], [Your AgentBuilder Partner], [Your Former Mentor], and any clients
- Look for recurring themes, unresolved discussions, and pending decisions
- Note any tension, disagreements, or pivots — these are important context

## Step 3: Build Each Memory File

### 00-[your-username].md
Compile everything about [Your Name]:
- Full background (Nashville move, BetterWealth, military service, [Your Agency] founding)
- Communication style and preferences
- Strengths and focus areas (content + community per advisor note)
- Current priorities and challenges
- Personal brand assets and authority signals
- Key relationships and how they started
- Decision-making patterns observed in emails

### 01-hri-overview.md
- Mission and positioning
- Full history (founding through present)
- Legal structure (from operating docs)
- Revenue model and current financial state
- Product/service lineup with current pricing
- Where [Your Agency] is today vs where it's going
- Key milestones and pivots

### 02-blitzmetrics-overview.md
- [Your Mentor/Advisor]'s background and role
- [Methodology Partner] methodology (Content Factory, Topic Wheel, Dollar-a-Day)
- How [Your Agency] and [Methodology Partner] relate operationally
- Shared systems and infrastructure (YCF)
- Key [Methodology Partner] clients and case studies relevant to [Your Agency]

### 03-team-directory.md
For EVERY person found in emails and documents:
- Full name
- Role and title
- Compensation structure (if known from docs)
- Email address
- Relationship to [Your Name] (how they met, current dynamic)
- Key contributions
- Communication style/preferences (observed from emails)
- Current status (active, inactive, paused)

### 04-client-directory.md
For EVERY client found in emails:
- Company/person name
- Service provided (KP Sprint, certification, etc.)
- Deal value
- Status (active, completed, churned, prospect)
- Key contact person
- Timeline
- Outcome/results if known
- Any issues or notable interactions

### 05-vendor-and-partner-map.md
- Every tool, platform, and service [Your Name]/[Your Agency] uses
- Every partner agency or referral relationship
- Every contractor or freelancer
- Login details and account ownership (who owns what)

### 06-deal-history.md
- Chronological record of every deal/engagement found
- Who closed it, terms, outcome
- Revenue generated
- Lessons learned

### 07-relationship-map.md
- [Your Name]'s key relationships ranked by importance
- How each relationship started
- Current status and health
- What each person provides/receives
- Any relationship dynamics to be aware of

### 08-communication-patterns.md
- How [Your Name] typically communicates (email tone, response time, preferences)
- Common phrases and language patterns
- How he handles conflict, negotiation, follow-ups
- Email signature and formatting habits

### 09-project-history.md
- Every major project (KP Sprints, site builds, content campaigns, events)
- Timeline and outcome for each
- Who was involved
- What worked and what didn't

### 10-financial-context.md
- Revenue actuals vs projections (from what can be determined)
- Pricing history and changes
- Comp structures for each team member
- Revenue shares and equity arrangements
- Outstanding payments or financial obligations

### 11-content-assets.md
- Every piece of published content found
- Every speaking engagement
- Book status (KP Guide, Shitbaggers)
- Podcast episodes
- Authority signals and press mentions

### 12-strategic-context.md
- Current strategic priorities (from most recent emails/docs)
- Pending decisions that need to be made
- Opportunities identified but not yet pursued
- Risks or challenges on the horizon
- What [Your Mentor/Advisor]/team are pushing for vs where [Your Name] is focused

### 13-gmail-insights.md
- Key patterns discovered in the inbox
- Important threads that are still open/unresolved
- Recurring topics that come up
- People [Your Name] emails most frequently
- Time periods of high vs low activity
- Any action items that appear to be dropped or forgotten

## Step 4: Create the Memory Bank INDEX

~/Documents/Claude/PRISM/memory-bank/INDEX.md should list:
- Every file in the memory bank with a one-line description
- Date compiled
- Gmail scan coverage (date range, number of emails processed)
- Key stats (number of contacts, clients, deals, projects documented)

## Step 5: Update the PRISM

- Add a memory-bank section to ~/Documents/Claude/PRISM/INDEX.md
- Update the CLAUDE.md at ~/Documents/Claude/PRISM/claude-code/CLAUDE.md to tell future Claude sessions to check the memory bank for context
- Write a session log documenting what was done

## Step 6: Cross-Reference with Existing SOPs

Review all existing SOPs and flag:
- SOPs that should be updated with context from the memory bank
- New SOPs that should be created based on patterns found in Gmail
- Client-specific SOPs that would help with active engagements
- Process gaps revealed by the email scan

Save recommendations to ~/Documents/Claude/PRISM/memory-bank/sop-recommendations.md

## Rules

- This runs overnight. Be exhaustive.
- Gmail is the richest source of context. Spend the majority of time there.
- Sensitive information (passwords, bank details, SSN) should NEVER be included in the memory bank. Note that sensitive info exists but don't record the actual values.
- When in doubt about whether something is relevant, include it. More context is better.
- Write in a factual, reference-document style. This is a knowledge base, not a narrative.
- Every file should be self-contained — someone reading just that file should get the full picture of its topic.
- Cross-reference between files where relevant (e.g., "See 03-team-directory.md for [Your AgentBuilder Partner]'s full profile")
- If you hit Gmail rate limits, pause briefly and continue. Don't skip sections.
- The memory bank should make any future Claude session feel like it's been working with [Your Name] for months, not minutes.

---

## See Also
- [[memory-bank/INDEX|Memory Bank Index]]
- [[CONTEXT|Context]]
- [[memory-bank/refresh-protocol|Refresh Protocol]]
- [[memory-bank/13-gmail-insights|Gmail Insights]]
- [[claude-code/scheduled-memory-refresh|Scheduled Memory Refresh]]
