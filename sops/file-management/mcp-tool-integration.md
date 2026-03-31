---
description: Standard process for researching, installing, configuring, and
  verifying new MCP servers and tool integrations
category: file-management
created: 2026-03-30
last_updated: 2026-03-30
version: 1
canon_compliance: 09-data-connections-needed.md
triangles:
  - CCS
  - DDD
triangles_served:
  - CCS — ensures tooling supports client communication systems
  - DDD — data-driven decisions require connected data sources
human_gates: yes
canon_sources:
  - 09-data-connections-needed.md
  - 10-anti-vandalism-checklist.md
tags:
  - domain/filemanagement
  - status/active
  - type/sop
---

# MCP/Tool Integration SOP

## Purpose
Standardize how new MCP servers, plugins, and external tools are added to the [[skills/PRISM-core|PRISM]] ecosystem — preventing configuration drift, credential leaks, and broken integrations.

## When to Use
- [Your Name] requests a new MCP server or plugin be installed (e.g., "set up the Desktop Control MCP")
- A new data source needs to be connected (Whoop, Obsidian, Telegram, etc.)
- An existing integration needs to be reconfigured or upgraded
- A Ralph Loop research session identifies a new MCP worth installing

## Process

1. **Research the integration.** Search the MCP registry, GitHub, and npm for the server/plugin. Confirm it exists, is actively maintained, and has documentation. Note the repo URL, install method, and any dependencies.

2. **Check for conflicts.** Read the current `.claude/settings.json` and `.mcp.json` to see what's already installed. Verify the new tool doesn't overlap with or break existing integrations. Check `~/Documents/Claude/PRISM/claude-code/mcp-integrations-reference.md` for planned vs. active integrations.

3. **Install the package.** Follow the tool's install instructions exactly:
   - npm-based: `npm install -g <package>` or clone and build locally
   - Python-based: `pip install <package> --break-system-packages`
   - Binary: Download to `~/bin/` or appropriate location
   - Record the exact install command used.

4. **Configure the MCP server.** Add the server entry to `.claude/settings.json` under `mcpServers` with the correct command, args, and env. Use environment variables for any secrets — **never hardcode credentials**.

5. **Create or update credential storage.** If the tool requires API keys or tokens:
   - Store in `~/Documents/Claude/PRISM/config/<tool-name>.json` or `.env`
   - Reference via environment variable in the MCP config
   - **Never commit credentials to Git or include in shared files**

6. **Test the integration.** Run a basic test to verify the tool is working:
   - Use `ToolSearch` to confirm the new tools appear
   - Execute a simple read-only operation to verify connectivity
   - Check for error messages in the terminal output

7. **Update PRISM documentation.** After verified working:
   - Update `~/Documents/Claude/PRISM/claude-code/mcp-integrations-reference.md`
   - Update `~/Documents/Claude/PRISM/CONTEXT.md` if this is a major capability addition
   - Update `~/Documents/Claude/PRISM/INDEX.md` automated tasks section if applicable
   - Update `~/.claude/CLAUDE.md` with any new usage patterns

8. **Document the integration.** Add a brief entry to the session log noting: what was installed, why, how it's configured, and any gotchas discovered during setup.

## Quality Checks
- [ ] New tool appears in `ToolSearch` results
- [ ] A basic read-only operation succeeds without errors
- [ ] No credentials are hardcoded in any configuration file
- [ ] PRISM documentation (CONTEXT.md, mcp-integrations-reference.md) is updated

## Common Pitfalls
- **Hardcoded credentials.** Found in session 3276b8a5: deploy_all.py had plaintext passwords. Always use environment variables or config files outside of version control.
- **Configuration location confusion.** MCP configs can live in `.claude/settings.json` (project) or `~/.claude/settings.json` (global). Know which one you're editing. Project-level is preferred for PRISM-specific integrations.
- **Window popups during desktop automation.** User strongly prefers background/non-intrusive operation. When installing desktop tools (Obsidian, Cursor, Warp), always use `--background` or silent flags. Document this preference in memory.
- **Missing dependencies.** Always check `requirements.txt` or `package.json` before running. Some MCP servers need build steps (e.g., `npm run build`) before they work.
- **Forgetting to test.** Don't mark an integration as done until you've verified it with a real operation, not just confirmed it appears in the tool list.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| Step 1 — Research | Review | [Your Name] should confirm the tool is wanted before installing |
| Step 5 — Credential storage | Approve | Any new API keys or tokens need [Your Name]'s approval |

## Anti-Vandalism Checks
- **Check what already exists:** Before adding a new MCP, verify no existing integration already covers this functionality.
- **Verify internal link structure:** Ensure CONTEXT.md and mcp-integrations-reference.md are updated, not just the config file.
- **Preserve what's working:** Never remove or modify existing MCP entries without explicit instruction.
- **Reference canonical source:** Check `~/Documents/Claude/PRISM/blitzmetrics-canon/09-data-connections-needed.md` for data connection priorities.

## Canon Compliance
- **Content Factory stage(s):** Plumbing — this is infrastructure setup that enables all other stages.
- **9 Triangles served:** CCS (Client Communication Systems — tools enable client work), DDD (Data-Driven Decisions — connected data sources enable analysis).
- **Canon documents:** `09-data-connections-needed.md`, `10-anti-vandalism-checklist.md`
- **Last canon audit:** 2026-03-30

## See Also

- [[sops/file-management/file-organization-rules|File Organization Rules]]
- [[sops/file-management/logging-discipline|Logging Discipline]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[blitzmetrics-canon/09-data-connections-needed|Canon: Data Connections]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Canon: Anti-Vandalism]]

## Learnings Log
- **2026-03-30:** Created from analysis of 5+ sessions this week involving MCP setup (Desktop Control, Whoop, Obsidian, Telegram). Key finding: each integration followed the same research → install → configure → test → document pattern, but without a standard checklist, steps were missed (especially documentation updates and credential security).
- **2026-03-30:** Session 3276b8a5 discovered hardcoded passwords in deploy_all.py during Telegram bot setup. Credential sanitization should be a standard check during any integration work.
- **2026-03-30:** User prefers non-intrusive/background installation. Multiple sessions (2593f5f7, 387bdf7d) showed friction when tools popped up windows during setup.