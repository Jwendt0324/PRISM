# Claude Mainframe

A plug-and-play operating system for Claude Code. SOPs, skills, frameworks, and automation — personalized to you through an identity scan.

## What This Is

The Mainframe gives Claude Code:
- **Skills** — action-oriented prompts for common tasks (article writing, content repurposing, QA, etc.)
- **SOPs** — step-by-step procedures for business operations
- **Canon** — source-of-truth frameworks (Content Factory, Topic Wheel, Dollar-a-Day, etc.)
- **Identity** — your personal context, auto-generated from scanning your environment

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Jwendt0324/mainframe.git ~/Documents/Claude/Mainframe

# 2. Run setup
cd ~/Documents/Claude/Mainframe
chmod +x setup.sh
./setup.sh

# 3. Start Claude Code — it will find and use the Mainframe automatically
```

The setup script will:
1. Create your personal identity folder
2. Generate a CLAUDE.md that tells Claude Code how to use the Mainframe
3. Prompt you to run the identity scan (optional but recommended)

## Identity Scan

The identity scan builds your personal context by reading sources you choose:

| Source | What It Finds | Access Needed |
|--------|--------------|---------------|
| Local files | Projects, documents, code repos | File system (automatic) |
| Gmail | Communication patterns, contacts, priorities | Gmail MCP or OAuth |
| Google Drive | Shared docs, client files, business context | Drive MCP or mount |
| Calendar | Meeting patterns, key relationships | Calendar MCP |
| GitHub | Repos, contributions, collaborators | `gh` CLI auth |

**You control what gets scanned.** The setup script asks before scanning each source. All results stay local in `.personal/` (gitignored).

To run the identity scan later:
```
Open Claude Code in ~/Documents/Claude/Mainframe
Then say: "Run the identity scan" or paste the contents of identity-scan.md
```

## Structure

```
mainframe/
├── skills/              ← Claude-loadable action prompts (shared)
├── sops/                ← Step-by-step procedures (shared)
│   ├── client-work/
│   ├── business-ops/
│   ├── file-management/
│   └── templates/
├── blitzmetrics-canon/  ← Source-of-truth frameworks (shared)
├── scripts/             ← Utility scripts (shared)
├── team-ops/            ← Team operating docs (shared)
├── claude-code/         ← Hooks, automation prompts (shared)
├── .personal/           ← YOUR identity layer (gitignored)
│   ├── CONTEXT.md       ← Auto-generated from identity scan
│   ├── memory-bank/     ← Your personal knowledge base
│   └── config.yml       ← Your scan preferences
├── setup.sh             ← One-time setup
├── identity-scan.md     ← Claude prompt for deep environment scan
├── CONTEXT-TEMPLATE.md  ← Template for personal context
└── CLAUDE.md            ← Instructions Claude loads on boot
```

## For Teams

Each team member clones the same repo, runs setup, and gets their own identity layer. SOPs and skills stay in sync. Personal context stays private.

To update shared content:
```bash
git pull origin main
```

To contribute improvements:
```bash
# Edit an SOP or skill, then:
git add -p
git commit -m "Update article-qa skill with new checklist item"
git push
```

## Requirements

- [Claude Code CLI](https://claude.ai/claude-code) installed
- macOS, Linux, or WSL
- Optional: `gh` CLI for GitHub scanning, Gmail/Calendar/Drive MCP servers for deeper identity scan
