#!/bin/bash
# Claude Mainframe — Stop Hook v3
# Tells Claude to fill in learnings on the auto-generated session log.
# The hooks auto-capture tool usage, files, and commands.
# Claude's job is ONLY to add the human-insight sections.

cat << 'EOF'
{
  "decision": "approve",
  "systemMessage": "MAINFRAME AUTO-LOG: Hooks have captured your tool usage, files created/modified/read, and commands run. If this session had 10+ messages or modified files, open ~/Documents/Claude/Mainframe/logs/sessions/YYYY-MM/session-{SESSION_ID}.md (the auto-generated log) and fill in ONLY the 'What Was Learned' section (2+ actionable learnings in Discovery/Insight/Action format) and the 'Related SOPs' section. Do NOT rewrite the auto-captured sections. Do NOT create a separate log file. If this was a trivial session (under 10 messages, no file changes), skip logging entirely."
}
EOF

exit 0
