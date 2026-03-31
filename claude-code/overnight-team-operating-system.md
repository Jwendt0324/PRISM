# Overnight Task: Build the Team Operating System

## Instructions for Claude Code

Copy everything below the line into Claude Code and let it run overnight.

---

You are building a comprehensive Team Operating System for [Your Name]'s [Your Agency Name]. [Your Name] just hired [Your Content Specialist] and plans to grow the team further. This system needs to work for the current team ([Your Name], [Your Mentor/Advisor], [Your Ops Partner], [Your AgentBuilder Partner], [Your Ops Admin], [Your Content Specialist]) AND scale to 10+ people without breaking.

**CRITICAL: Only scan the Gmail account [your-email@your-agency.com]. Do NOT access, read, or search any other Gmail account.**

## Step 0: Load Context

Read the full PRISM first — especially these files:
- ~/Documents/Claude/PRISM/INDEX.md
- ~/Documents/Claude/PRISM/sops/business-ops/hri-offer-ladder-and-gtm.md
- ~/Documents/Claude/PRISM/sops/client-work/knowledge-panel-sprint.md
- ~/Documents/Claude/PRISM/claude-code/CLAUDE.md
- ~/Desktop/Operating Documents/ (all files — contains equity agreements, KP Sprint team note, standalone plan)

If the memory bank exists, read it too:
- ~/Documents/Claude/PRISM/memory-bank/ (all files)

## Step 1: Reverse-Engineer Current Team Operations from Gmail

Use Gmail MCP tools to understand how the team currently works. Search [your-email@your-agency.com] for:

### Communication Patterns
- "from:dennis" — How does [Your Mentor/Advisor] communicate with [Your Name]? Frequency, tone, topics, decisions
- "to:dennis" — How does [Your Name] communicate with [Your Mentor/Advisor]? What does he escalate vs handle alone?
- "from:sam" OR "to:sam" — [Your AgentBuilder Partner] McLeod delivery coordination patterns
- "from:dylan" OR "to:dylan" — [Your Ops Partner] [Last Name] content ops patterns
- "from:muzamil" OR "to:muzamil" — Ops/finance communication patterns
- "from:jackson" OR "to:jackson" — Any early [Your Content Specialist] communications
- Search for any team-wide emails (multiple recipients from the team)

### Project Coordination
- "basecamp" OR "project" OR "task" OR "checklist" — How work gets assigned and tracked
- "deadline" OR "due" OR "overdue" OR "late" — Where delivery breaks down
- "update" OR "status" OR "standup" — How status gets communicated
- "approval" OR "approve" OR "sign off" — Decision bottlenecks
- "blocked" OR "waiting on" OR "need from you" — Common blockers

### Handoffs & Delegation
- "can you" OR "please handle" OR "take care of" — How [Your Name] delegates
- "here's what I need" OR "deliverables" — How work gets scoped
- "done" OR "finished" OR "completed" OR "shipped" — How completion gets communicated
- "feedback" OR "revision" OR "changes" — Revision cycles and QA patterns

### Onboarding History
- "welcome" OR "onboarding" OR "first day" OR "getting started" — Past onboarding attempts
- "training" OR "SOP" OR "loom" OR "walkthrough" — Training materials shared
- "access" OR "login" OR "credentials" OR "invite" — Tool access patterns

### Conflict & Friction
- "concern" OR "issue" OR "problem" OR "frustrated" — Where friction happens
- "miscommunication" OR "confused" OR "unclear" — Communication breakdowns
- "late" OR "missed" OR "forgot" — Accountability gaps

For each search: use gmail_search_messages with maxResults=30, read the most relevant threads with gmail_read_thread, and extract patterns about how the team operates.

## Step 2: Build the Team Operating System

Create this structure:
```
~/Documents/Claude/PRISM/team-ops/
├── 00-team-os-overview.md           ← Master doc: how the team works
├── 01-team-directory.md             ← Every person, role, contact, KPIs
├── 02-communication-protocol.md     ← Who gets looped on what, through which channel
├── 03-decision-rights-matrix.md     ← Who approves what, escalation paths
├── 04-meeting-cadence.md            ← All recurring meetings, agendas, templates
├── 05-delegation-framework.md       ← What [Your Name] owns vs delegates, handoff protocols
├── 06-new-hire-onboarding-sop.md    ← Generic onboarding SOP for ANY new hire
├── 07-jackson-onboarding-kit.md     ← Specific onboarding for [Your Content Specialist] (immediate use)
├── 08-role-scorecards.md            ← KPIs and success metrics for every role
├── 09-tool-stack-and-access.md      ← Every tool, who has access, how to get access
├── 10-project-management-sop.md     ← How projects get tracked from intake to delivery
├── 11-client-communication-sop.md   ← How we communicate with clients at each stage
├── 12-escalation-playbook.md        ← What to do when things go wrong
├── 13-team-scaling-plan.md          ← Hiring plan, role definitions for next 3-5 hires
├── 14-current-pain-points.md        ← Issues found in Gmail that need fixing
└── INDEX.md                         ← Master index
```

### 00-team-os-overview.md
The master document. Write this as if handing it to a new team member who needs to understand how [Your Agency] operates:
- Company mission and current state
- How the two products work together (KP Sprint + AI Apprentice = flywheel)
- Team structure and reporting lines
- How work flows from sales → delivery → case study
- Communication norms
- Core values and operating principles
- Link to every other doc in the team-ops folder

### 01-team-directory.md
For every team member ([Your Name], [Your Mentor/Advisor], [Your Ops Partner], [Your AgentBuilder Partner], [Your Ops Admin], [Your Content Specialist], plus anyone else found in emails):
- Full name
- Role and title
- Primary responsibilities
- Compensation structure (from the KP Sprint team note)
- KPI gate (if applicable)
- Email address
- Best way to reach them (email, Basecamp, text — determine from email patterns)
- Timezone and availability patterns (determine from email timestamps)
- Strengths (observed from email content)
- What they need from [Your Name] (observed from email requests)

### 02-communication-protocol.md
Based on what you observe in Gmail, define:
- Default channels: What goes in email vs Basecamp vs text vs Zoom
- Response time expectations by channel
- Who gets CC'd on what (based on current patterns, improved where needed)
- Client communication: who talks to clients and when
- Internal updates: how status gets shared
- Urgent issues: how to escalate and to whom
- Rules: no same-day itinerary flips, two protected sleep nights/week (from the Sprint doc)

### 03-decision-rights-matrix.md
Build a RACI-style matrix for common decisions:
- New client acceptance → who decides?
- Pricing exceptions → who approves?
- Scope changes mid-Sprint → who has authority?
- Hiring decisions → who has final say?
- Content publishing → who approves?
- Budget/spending → who approves at what threshold?
- Client escalations → who handles?
- SOP changes → who can modify?
- Tool purchases → who approves?
Base this on the governance structure in the KP Sprint doc and equity agreement, adjusted by what you see in email patterns.

### 04-meeting-cadence.md
Define all recurring meetings:
- Weekly Pipeline & Delivery Standup (Tuesdays, 30 min) — already defined in KP Sprint doc
- Operating Committee (weekly, post-standup) — [Your Mentor/Advisor], [Your AgentBuilder Partner], [Your Ops Partner]
- Agenda templates for each meeting
- Pre-meeting prep requirements
- Post-meeting action item format
- Suggested additions based on gaps found in email (e.g., 1:1s, sprint retros)

### 05-delegation-framework.md
Based on [Your Name]'s email patterns, define:
- What [Your Name] should KEEP doing (based on his strengths: content, community, relationships)
- What [Your Name] should DELEGATE (based on where he's bottlenecking the team)
- For each delegated area: who owns it, how handoff works, what "done" looks like
- Task categories: Urgent/Important matrix for [Your Name]'s time
- The "[Your Content Specialist] can handle this" list — things to immediately hand to [Your Content Specialist]

### 06-new-hire-onboarding-sop.md
Generic onboarding SOP that works for ANY future hire:
- Day 1: Welcome email template, tool access checklist, required reading list
- Day 2-3: PRISM orientation (read SOPs relevant to their role)
- Week 1: Shadow sessions, first small task assignment, meet the team
- Week 2: First independent deliverable with QA review
- Week 3-4: Full workload ramp-up
- 30-day check-in template
- 60-day evaluation criteria
- Tool access checklist (every tool they need, who grants access)
- Required reading: which PRISM SOPs to read first by role
- Communication setup: add to channels, meetings, distribution lists

### 07-jackson-onboarding-kit.md
Specific to [Your Content Specialist], ready to send immediately:
- Welcome message (write in [Your Name]'s voice — confident, real, grounded)
- His specific role and what success looks like in 30/60/90 days
- First week schedule with specific tasks
- Which PRISM SOPs he should read first
- Tool access he needs (list specific tools with who grants each)
- Who he reports to and how to communicate with each team member
- His first deliverable assignment
- Questions to ask [Your Name] in their first 1:1
- Common mistakes new hires make and how to avoid them

### 08-role-scorecards.md
For every role, define:
- Role title and one-line description
- 3-5 Key Results that define success
- Leading indicators (weekly activities that drive results)
- Lagging indicators (monthly outcomes)
- Compensation triggers (what unlocks bonuses/commissions)
- Red flags (what indicates underperformance)
Pull KPIs from the KP Sprint doc and [Your Agency] Standalone Plan.

### 09-tool-stack-and-access.md
Catalog every tool [Your Agency] uses (from emails and documents):
- Tool name and purpose
- URL
- Who has access
- Who is the admin/owner
- Monthly cost (if known)
- How to request access (who to ask)
- Categories: PM, communication, content production, finance, analytics, hosting

### 10-project-management-sop.md
How a Knowledge Panel Sprint moves through the system:
- Sales → Intake → Production → QA → Delivery → Case Study
- Who owns each stage
- Handoff protocol between stages
- Status tracking (red/amber/green definitions)
- Blocker resolution process
- Timeline accountability (the 30-day clock)
- How to document client delays

### 11-client-communication-sop.md
Based on email patterns with clients:
- Initial outreach and qualification
- Proposal and close
- Onboarding communication (intake email template)
- Weekly client updates during Sprint
- Handling client requests/changes
- Delivery and handoff communication
- Post-delivery follow-up
- When to escalate to [Your Mentor/Advisor]

### 12-escalation-playbook.md
What to do when things break:
- Client is unhappy → steps 1-2-3
- Deliverable is late → who to notify, how to recover
- Team member is unresponsive → escalation path
- Scope creep request → how to say no and redirect to Phase 2
- Payment dispute → who handles
- Quality issue found post-delivery → remediation process
- Client wants a refund → policy and process (7-day cooling off from docs)

### 13-team-scaling-plan.md
Based on current bottlenecks and growth targets:
- Next 3 hires: what roles, in what order, why
- Job descriptions for each
- Comp structures that match the existing model
- Where to find candidates (apprentice pipeline, referrals, etc.)
- How each hire unlocks more throughput (tie to Sprint capacity)
- Revenue triggers: "when we hit X Sprints/month, hire Y"
- Team structure at 10 people vs current state

### 14-current-pain-points.md
Everything you found in Gmail that indicates friction:
- Communication breakdowns (specific examples, anonymized if sensitive)
- Dropped balls or missed deadlines
- Unclear ownership
- Decision bottlenecks
- Tool gaps
- Process gaps
- Relationship dynamics that need attention
For each pain point: what happened, root cause, recommended fix.

## Step 3: Generate Onboarding Materials

Create ready-to-send documents:

### [Your Content Specialist]'s Welcome Email
Save to ~/Documents/Claude/PRISM/team-ops/jackson-welcome-email.md
- Write in [Your Name]'s voice
- Include first week expectations
- List tools he needs access to
- Link to relevant SOPs
- Set the tone: high expectations, real support, no BS

### Team Announcement
Save to ~/Documents/Claude/PRISM/team-ops/jackson-team-announcement.md
- Brief intro of [Your Content Specialist] to the team
- His role and what he'll be working on
- How to loop him in
- Write in [Your Name]'s voice

## Step 4: Update the PRISM

- Add team-ops section to ~/Documents/Claude/PRISM/INDEX.md
- Update the CLAUDE.md to reference the team-ops folder
- Create any new SOPs that should exist based on gaps found
- Write a session log

## Step 5: Cross-Reference

Review all existing PRISM SOPs and flag:
- SOPs that need team role assignments added
- SOPs that need handoff protocols added
- Process gaps that don't have SOPs yet
- Save recommendations to ~/Documents/Claude/PRISM/team-ops/sop-recommendations.md

## Rules

- This runs overnight. Be exhaustive.
- [Your Content Specialist]'s onboarding kit should be ready to send by morning. That's the #1 priority.
- Write everything in [Your Name]'s voice: confident, direct, grounded, no corporate jargon.
- When documenting pain points, be specific but constructive. This is about fixing systems, not blaming people.
- The Team OS should make it possible for someone to join [Your Agency] and be productive within a week.
- If you hit Gmail rate limits, pause briefly and continue.
- Sensitive comp details from the KP Sprint doc should be included — this is an internal document.
- Reference the memory bank files if they exist for additional context.

---

## See Also
- [[memory-bank/03-team-directory|Team Directory]]
- [[sops/templates/team-ops/00-team-os-overview|Team OS Overview]]
- [[sops/templates/team-ops/08-role-scorecards|Role Scorecards]]
- [[memory-bank/05-team-and-roles|Team & Roles]]
