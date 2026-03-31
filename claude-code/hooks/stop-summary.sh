#!/bin/bash
# Claude PRISM — Stop Hook v4
# Ralph-loop aware: stays silent when ralph-loop is active to prevent
# context pollution and "." response loops.

# Detect ralph-loop by checking for its marker file
if [ -f "$HOME/.claude/ralph-loop.local.md" ]; then
    # Ralph-loop is active — output minimal approval with no systemMessage
    # This prevents the stop hook from eating context every iteration
    echo '{"decision":"approve"}'
    exit 0
fi

# Normal mode — prompt Claude to fill in learnings
cat << 'EOF'
{
  "decision": "approve",
  "systemMessage": "PRISM AUTO-LOG: Hooks have captured your tool usage, files created/modified/read, and commands run. If this session had 10+ messages or modified files, open ~/Documents/Claude/PRISM/logs/sessions/YYYY-MM/session-{SESSION_ID}.md (the auto-generated log) and fill in ONLY the 'What Was Learned' section (2+ actionable learnings in Discovery/Insight/Action format) and the 'Related SOPs' section. Do NOT rewrite the auto-captured sections. Do NOT create a separate log file. If this was a trivial session (under 10 messages, no file changes), skip logging entirely."
}
EOF

exit 0
