# IDENTITY SCAN — Build Your Personal PRISM Context

**Purpose:** This prompt tells Claude Code to scan your environment and auto-generate your personal CONTEXT.md and memory-bank files. Run this once during setup, then periodically to refresh.

---

## Instructions for Claude

You are running the PRISM Identity Scan. Your job is to deeply understand who this person is — their work, their communication style, their projects, their relationships, their priorities — by scanning every source they give you access to.

**Output:** Generate files in `.personal/` that make every future Claude session deeply contextual and useful.

### Phase 1: Discover Available Sources

First, figure out what you can access. Check each source and report what's available:

```
SCAN CHECKLIST — check each one:

[ ] Local filesystem
    - ls ~/Documents ~/Desktop ~/Downloads ~/Projects ~/Code ~/repos 2>/dev/null
    - Find project directories, business docs, content files
    - Look for existing Claude memory files (~/.claude/)

[ ] Git / GitHub
    - gh auth status (are they logged in?)
    - gh repo list --limit 20 (what repos do they work on?)
    - git log in key repos (what are they building?)

[ ] Gmail (if Gmail MCP is connected)
    - gmail_get_profile (who are they?)
    - gmail_search_messages for recent threads
    - Map communication patterns, key contacts, active projects

[ ] Google Calendar (if Calendar MCP is connected)
    - gcal_list_events for upcoming 2 weeks
    - Map meeting patterns, key people, recurring commitments

[ ] Google Drive (if accessible)
    - Look for shared drives, client folders, business docs

[ ] Notion (if Notion MCP is connected)
    - notion-search for workspaces, databases, recent pages

[ ] Browser tabs (if Chrome MCP is connected)
    - tabs_context_mcp to see what they're currently working on
```

**After checking, report:** "Here's what I can access: [list]. Want me to scan all of these, or skip any?"

### Phase 2: Deep Scan Each Source

For each accessible source, extract:

#### From Local Filesystem
- **Project structure:** What repos/projects exist? What languages/frameworks?
- **Business documents:** Proposals, contracts, client files, invoices
- **Content:** Articles, videos, transcripts, drafts
- **Configuration:** What tools are installed? What services are configured?
- **Existing Claude context:** Any `.claude/` files, CLAUDE.md, memory files

#### From Gmail
- **Communication graph:** Who do they email most? Who emails them?
- **Active threads:** What's being discussed right now?
- **Patterns:** When do they respond? How long are their emails? What's their tone?
- **Projects mentioned:** What work is referenced in recent emails?
- **Key relationships:** Categorize contacts into tiers (core business, network, industry)

#### From Calendar
- **Meeting patterns:** What recurring meetings exist? With whom?
- **Upcoming commitments:** What's on the schedule?
- **Time allocation:** How is their week structured?

#### From GitHub
- **Active repos:** What are they building? What languages?
- **Contribution patterns:** When do they code? How often?
- **Collaborators:** Who do they work with?
- **Open issues/PRs:** What's in progress?

#### From Drive / Notion
- **Shared resources:** What drives/workspaces do they have access to?
- **Client folders:** Which clients have dedicated spaces?
- **Templates/SOPs:** Any existing processes documented?

#### From Browser
- **Current focus:** What tabs are open? What tools are they using?
- **Bookmarks/frequent sites:** What services do they rely on?

### Phase 3: Synthesize Identity

From everything you've gathered, build these files:

#### `.personal/CONTEXT.md`
Fill in the CONTEXT-TEMPLATE.md with real data. Be specific — names, numbers, dates, URLs. This file should let any future Claude session understand:
- Who this person is
- What they do
- Who they work with
- What they're working on right now
- What their priorities are
- How they communicate

#### `.personal/memory-bank/` (create these files)

| File | Contents |
|------|----------|
| `00-identity.md` | Name, role, background, communication style, working hours |
| `01-business.md` | Company, products, revenue, legal structure |
| `02-team.md` | Team directory with roles, emails, reporting lines |
| `03-clients.md` | Active clients/projects with status and key contacts |
| `04-relationships.md` | Tiered relationship map (core, network, industry) |
| `05-priorities.md` | Current priority stack with deadlines |
| `06-communication.md` | Email patterns, preferred channels, response style |
| `07-content-assets.md` | Inventory of content, documents, and creative assets |
| `08-tools-and-access.md` | Tools used, services configured, access levels |
| `09-financial.md` | Revenue, expenses, key financial context (if found) |
| `10-strategic.md` | Long-term goals, opportunities, risks |

#### `.personal/config.yml`
Record what was scanned and when:

```yaml
identity:
  name: "{{NAME}}"
  email: "{{EMAIL}}"

scan_history:
  - date: "{{TODAY}}"
    sources:
      filesystem: true
      gmail: true/false
      calendar: true/false
      github: true/false
      drive: true/false
      notion: true/false
      browser: true/false
    files_generated:
      - .personal/CONTEXT.md
      - .personal/memory-bank/00-identity.md
      # ... etc

scan_preferences:
  # Sources the user opted out of
  skip: []
  # Directories to exclude from filesystem scan
  exclude_paths:
    - "node_modules"
    - ".git"
    - "venv"
```

### Phase 4: Verify and Report

After generating all files:

1. **Show a summary** of what was found and generated
2. **Flag gaps** — what couldn't be determined? What should the user fill in manually?
3. **Recommend next steps** — e.g., "Connect Gmail MCP for deeper context" or "Your calendar wasn't accessible — here's how to set that up"

### Privacy Notes

- All identity data stays in `.personal/` which is gitignored
- Nothing leaves the user's machine
- The scan only reads — it never modifies, sends, or publishes anything
- Users can delete `.personal/` at any time to reset

---

## Running the Scan

**First time (during setup):**
```
Claude, run the identity scan. Scan everything you can access.
```

**Refresh (periodic):**
```
Claude, refresh my identity scan. Focus on what's changed since last scan.
```

**Targeted update:**
```
Claude, update my identity scan — just Gmail and Calendar.
```
