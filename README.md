# Claude PRISM

A plug-and-play operating system for Claude Code. Drop it into any business and Claude becomes a self-improving operator — not just an assistant.

## What This Is

The PRISM (Personal Reference & Intelligence System for Management) turns Claude Code from a blank-slate coding tool into a structured business operator. It gives Claude persistent memory, living SOPs, methodology frameworks, automation hooks, and a personal identity layer — all wired together so the system compounds over time.

Every task Claude executes generates session logs. Those logs feed into living SOPs. Those SOPs are formatted as skills that Claude automatically loads on future tasks. The result: Claude gets measurably better at your work every time it works for you.

## What You Get

- **14 action-oriented skills** — Article writing, KP Sprints, content repurposing, Dollar-a-Day campaigns, prospect follow-up, influence audits, and more. Each is a Claude-loadable prompt with step-by-step execution logic.
- **25+ SOPs** across client work, business ops, and file management — living documents that update themselves as Claude learns.
- **15 canonical frameworks** — Content Factory (6-stage), Dollar-a-Day, Topic Wheel, Nine Triangles, MAA, GCT Discovery, LDT, and more. These are your methodology source of truth.
- **12 automation hooks** — Pre-tool guards, session logging, file backups, confidentiality filters, and post-compaction preservation rules. All configured through Claude Code's native hook system.
- **13+ utility scripts** — EOD reports, SOP health checks, content tree mapping, session parsing, log rotation, and memory bank refresh.
- **Team operating system templates** — 19 files covering onboarding, roles, communication protocols, decision rights, delegation frameworks, and scaling plans.
- **Identity scan** — An automated process that reads your local files, email, calendar, GitHub, and Drive to generate a personal context file. Claude knows who you are from the first message.
- **Overnight automation prompts** — Deep analysis jobs you kick off before bed and review in the morning.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/[your-username]/PRISM.git ~/Documents/Claude/PRISM

# 2. Run setup
cd ~/Documents/Claude/PRISM
chmod +x setup.sh
./setup.sh

# 3. Start Claude Code — it will find and use the PRISM automatically
```

The setup script will:
1. Create your personal identity folder (`.personal/`, gitignored)
2. Generate a CONTEXT.md from the template
3. Ask for your name, email, and company to personalize automation scripts
4. Set up CLAUDE.md so Claude Code loads the PRISM on boot
5. Prompt you to run the identity scan (optional but recommended)

## How It Works

The PRISM uses a two-layer architecture:

**Shared layer** (version-controlled, synced across team) — Skills, SOPs, canon frameworks, hooks, scripts, and templates. This is the repo itself.

**Personal layer** (`.personal/`, gitignored) — Your identity context, memory bank, and scan preferences. Created during setup, never shared.

When Claude Code starts, it reads CLAUDE.md, which points to your personal CONTEXT.md. That file tells Claude who you are, what you do, and how your business works. From there, Claude routes tasks to the right skill or SOP automatically.

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
Open Claude Code in ~/Documents/Claude/PRISM
Then say: "Run the identity scan" or paste the contents of identity-scan.md
```

## Structure

```
PRISM/
├── skills/              <- Claude-loadable action prompts (shared)
├── sops/                <- Step-by-step procedures (shared)
│   ├── client-work/
│   ├── business-ops/
│   ├── file-management/
│   └── templates/
├── blitzmetrics-canon/  <- Source-of-truth frameworks (shared)
├── scripts/             <- Utility scripts (shared)
├── team-ops/            <- Team operating docs (shared, example data)
├── claude-code/         <- Hooks, automation prompts (shared)
├── .personal/           <- YOUR identity layer (gitignored)
│   ├── CONTEXT.md       <- Auto-generated from identity scan
│   ├── memory-bank/     <- Your personal knowledge base
│   └── config.yml       <- Your scan preferences
├── setup.sh             <- One-time setup
├── identity-scan.md     <- Claude prompt for deep environment scan
├── CONTEXT-TEMPLATE.md  <- Template for personal context
├── CUSTOMIZATION.md     <- Guide to adapting the PRISM
└── CLAUDE.md            <- Instructions Claude loads on boot
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

## Auto-Updates

If you enabled auto-updates during setup, PRISM quietly pulls the latest improvements every time you start Claude Code. Your personal data in `.personal/` is never affected.

To disable auto-updates:
```bash
rm ~/Documents/Claude/PRISM/.personal/auto-update-enabled
```

To re-enable:
```bash
touch ~/Documents/Claude/PRISM/.personal/auto-update-enabled
```

## Customization

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for how to adapt the PRISM to your business — which files to edit, how template variables work, and how to add your own skills, SOPs, and hooks.

## Requirements

- [Claude Code CLI](https://claude.ai/claude-code) installed
- macOS, Linux, or WSL
- Optional: `gh` CLI for GitHub scanning, Gmail/Calendar/Drive MCP servers for deeper identity scan
