---
title: API Security & Access Management
version: 1.0
last_updated: 2026-03-21
category: business-ops
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/security
canon_compliance: [human-requirements, anti-vandalism]
human_gates: [token creation, token rotation, access review]
---

# API Security & Access Management

## Purpose
Prevent token and password exposure, manage access securely, and ensure rotation happens regularly. This SOP exists because a WordPress password was found in plaintext in a settings file — that must never happen again.

## When to Use
- Setting up any new API integration (WordPress, Stripe, YouTube, etc.)
- Sharing access tokens with Claude Code or any automation
- Onboarding a new team member to tools
- Quarterly access rotation

## Process

### 1. Generating Access Tokens
- **WordPress:** Use Application Passwords (Settings → Users → Application Passwords), NOT your login password
- **APIs:** Use API keys or OAuth tokens, NEVER account passwords
- **MCP integrations:** Use dedicated service accounts with minimal permissions

### 2. Storing Tokens Securely (see [[memory-bank/05-vendor-and-partner-map|Vendor Map]] for active integrations)
- **NEVER** store in plain text in .md files, settings.json, conversation logs, or git-tracked files
- **DO** store in environment variables, .env files (chmod 600), macOS Keychain, or 1Password

### 3. Sharing with Claude Code
- Pass via environment variable (`$ENV_VAR`) from Bash
- If you must type a token in a prompt, rotate it immediately after the session
- Never paste tokens into conversations that get exported to logs

### 4. Rotation Schedule
| Type | Frequency |
|---|---|
| WordPress Application Passwords | Every 90 days |
| API keys (Stripe, YouTube, etc.) | Every 90 days |
| Server passwords (Vultr, [Field Service Platform]) | Every 60 days |
| MCP server tokens | Every 90 days |

### 5. Emergency: Token Exposed
1. Revoke the exposed token IMMEDIATELY
2. Generate a new one
3. Update all systems using the old token
4. Check logs for unauthorized access
5. Document the incident in this SOP's learnings log

## Quality Checks
- [ ] No passwords or tokens in plaintext in any tracked file
- [ ] All .env files have chmod 600 permissions
- [ ] Rotation schedule followed
- [ ] Claude settings files contain zero passwords

## Human Gates
- Token creation requires human action
- Rotation decision is human-only
- Access review (who has what) is human-only

## Anti-Vandalism
- NEVER delete existing tokens without creating replacements first
- NEVER modify token storage without confirming new token works

## Learnings Log
- 2026-03-21: Created after audit discovered WordPress password in plaintext in ~/.claude/settings.local.json

---

## Related

- [Tool Stack & Access](../templates/team-ops/09-tool-stack-and-access.md)
- [Vendor & Partner Map](../../memory-bank/05-vendor-and-partner-map.md)
- [Canon: Data Connections](../../blitzmetrics-canon/09-data-connections-needed.md)

## See Also

- [[memory-bank/05-vendor-and-partner-map|Vendor Map]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[blitzmetrics-canon/09-data-connections-needed|Data Connections]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]