# PRISM — Apprentice Quickstart

Welcome. In about 10 minutes, you'll have a Claude Code setup that knows who you are, loads your SOPs automatically, and gets smarter every time you use it.

---

## Step 1 — Install Claude Code (skip if you already have it)

Download and install from: **https://claude.ai/download**

After install, open your Terminal (macOS: press `Cmd+Space`, type `Terminal`, hit Enter) and verify:

```bash
claude --version
```

If that prints a version number, you're good. If it says "command not found," follow the install instructions on the download page and try again.

---

## Step 2 — Install PRISM (one command)

Paste this into your Terminal and press Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/Jwendt0324/PRISM/main/quick-install.sh | bash
```

This installer will:

1. Check for `git`, `brew`, and `jq` — and offer to install anything missing
2. Clone PRISM to `~/Documents/Claude/PRISM`
3. Ask for your name, email, and agency name (this personalizes your system)
4. Wire PRISM into Claude Code so it loads automatically on every session

When it asks about auto-updates, answer `Y` — this keeps your PRISM in sync with improvements as we ship them.

---

## Step 3 — Run the Identity Scan

This is the step that makes PRISM know who *you* are. It scans your local files, Gmail, Calendar, and GitHub (whichever sources you approve) and builds a `CONTEXT.md` file that Claude loads on every session.

Open Claude Code:

```bash
cd ~/Documents/Claude/PRISM
claude
```

Then paste this into Claude:

> Run the identity scan.

Claude will ask which sources you want to include. You choose. Everything stays local in a `.personal/` folder that never gets pushed to git.

The scan takes 10–20 minutes depending on how many sources you connect. When it's done, you have a real context file — Claude now knows your role, your clients, what you work on, and how you work.

---

## Step 4 — Run Your First Real Task

Still inside Claude Code, try one of these:

- **"Run a health check on my PRISM."** — Claude will audit your hooks, logs, and configuration and report back.
- **"List all the skills available in PRISM and when I'd use each one."** — Good for learning what the system can do.
- **"Create a new SOP for something I did today."** — Claude walks you through documenting a repeated process.

---

## If Something Goes Wrong

**"command not found: claude"** — Claude Code isn't installed or isn't on your PATH. Go back to Step 1.

**"jq is required"** — The installer didn't manage to install jq. Run: `brew install jq` and then re-run `~/Documents/Claude/PRISM/setup.sh`.

**"Permission denied"** on setup.sh — Run: `chmod +x ~/Documents/Claude/PRISM/setup.sh` and try again.

**The identity scan gets stuck** — You can fill in `~/Documents/Claude/PRISM/.personal/CONTEXT.md` manually. It has a template. Skip the scan entirely if you want.

**Something else broke** — Message Jack directly with a screenshot of the terminal output.

---

## What's Actually Installed

- **15 skills** — Claude loads these automatically based on what you ask it to do (article writing, KP sprints, content repurposing, Dollar-a-Day, prospect follow-up, etc.)
- **34 SOPs** — Deeper reference docs behind the skills
- **26 canonical frameworks** — The methodology source of truth (Content Factory, Topic Wheel, Nine Triangles, MAA, GCT, LDT, etc.)
- **13 automation hooks** — Background guards, logging, file backups, confidentiality filters
- **12 utility scripts** — EOD reports, health checks, log rotation, memory refresh
- **19 team-ops templates** — Onboarding, roles, decision rights, delegation frameworks

Read [`README.md`](README.md) for the full architecture, or [`CUSTOMIZATION.md`](CUSTOMIZATION.md) for how to adapt PRISM to your specific workflow.

---

## One Rule

Every time Claude discovers a better way to do something, it updates the SOP. That's how the system compounds. Don't fight this — if you get a better output, let the SOP update. If you don't like a change, roll it back with `git diff` and `git checkout`.

Compound. Don't campaign.
