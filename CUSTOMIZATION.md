# Customizing Your PRISM

After running `setup.sh`, your PRISM is ready to use. Here's how to make it yours.

## The Personal Layer

Your identity lives in `.personal/` (gitignored — never shared):
- `.personal/CONTEXT.md` — Your auto-generated context (created by identity scan)
- `.personal/memory-bank/` — Your personal knowledge base
- `.personal/config.yml` — Your scan preferences

Run the identity scan to populate these: open Claude Code and say "Run the identity scan."

## Template Variables

The automation scripts use `{{VARIABLES}}` that get replaced during setup:
- `[your-email@your-agency.com]` — Your primary email (for Gmail/calendar scanning)
- `{{USER_NAME}}` — Your name
- `{{AGENCY_NAME}}` — Your company/agency name
- `{{PRISM_PATH}}` — Where your PRISM is installed

These are set automatically by `setup.sh`.

## Files to Customize

### Must Edit
- `.personal/CONTEXT.md` — Run the identity scan or fill in manually

### Should Edit (for your business)
- `team-ops/` — Replace example data with your team's info, or delete files you don't need
- `sops/business-ops/offer-ladder-and-gtm.md` — Adapt the pricing framework to your services

### Optional
- `claude-code/hooks/prompt-submit.sh` — Add your own confidentiality topic guards
- `claude-code/overnight-*.md` — The automation prompts work as-is after setup

## Example Files

The `team-ops/` directory contains example files from a real agency. They show what filled-in templates look like. Each file has an EXAMPLE banner at the top.

The `examples/` directory contains client-specific SOPs and scripts that show real-world implementations. These are for reference only.

## Adding Your Own Content

### New Skills
Add `.md` files to `skills/` following the existing format (YAML frontmatter + actionable instructions).

### New SOPs
Use `sops/templates/sop-creation-template.md` as your starting point. File in the appropriate subdirectory.

### New Hooks
Add shell scripts to `claude-code/hooks/` and register them in `~/.claude/settings.json`.

## Canon Frameworks

The `blitzmetrics-canon/` directory contains methodology frameworks. These are reference material — read them, learn from them, but don't modify them unless you're adapting the methodology for your own use.
