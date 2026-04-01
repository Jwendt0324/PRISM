#!/bin/bash
# Claude PRISM — Session Start Hook v5
# Three jobs:
#   1. Log session start event
#   2. Inject daily context via stdout (Claude sees this)
#   3. Check for urgent items (unanswered threads, overdue tasks)
#
# stdout → injected into Claude's context at session start

INPUT=""
if [ ! -t 0 ]; then
    INPUT=$(cat 2>/dev/null || true)
fi
[ -z "$INPUT" ] && exit 0

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date +"%Y-%m-%d")
DAY_OF_WEEK=$(date +"%A")
PRISM_DIR="$HOME/Documents/Claude/PRISM"
LOG_DIR="$PRISM_DIR/logs"
mkdir -p "$LOG_DIR/actions" "$LOG_DIR/sessions/$(date +%Y-%m)" "$LOG_DIR/conversations/$(date +%Y-%m)"

REPORTS_READY=""
YESTERDAY=""

if command -v jq &>/dev/null; then
    SID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)
    CWD=$(echo "$INPUT" | jq -r '.cwd // "unknown"' 2>/dev/null)
else
    SID="unknown"
    CWD="unknown"
fi

# ─── JOB 1: Log the event ───
printf '{"ts":"%s","event":"start","sid":"%s","cwd":"%s"}\n' \
    "$TS" "$SID" "$CWD" \
    >> "$LOG_DIR/session-events.jsonl"

# ─── JOB 2: Gather daily stats ───
TODAY_SESSIONS=$(grep "$TODAY" "$LOG_DIR/session-events.jsonl" 2>/dev/null | grep -c '"event":"start"' || echo "0")

TODAY_ACTIONS=0
if [ -f "$LOG_DIR/actions/$TODAY.jsonl" ]; then
    TODAY_ACTIONS=$(wc -l < "$LOG_DIR/actions/$TODAY.jsonl" | tr -d ' ')
fi

RECENT_CONVOS=$(find "$LOG_DIR/conversations/" -name "*.md" -mtime -1 2>/dev/null | wc -l | tr -d ' ')

# Parts agent status
PARTS_STATUS="not configured"
if [ -d "$PRISM_DIR/scripts/parts-agent" ]; then
    LATEST_RUN=$(find "$PRISM_DIR/scripts/parts-agent/data" -name "results_*.csv" -mtime -1 2>/dev/null | head -1)
    if [ -n "$LATEST_RUN" ]; then
        PARTS_STATUS="ran in last 24h"
    else
        PARTS_STATUS="installed, no recent run"
    fi
fi

# ─── JOB 3: Check for urgent items ───
URGENT=""

# Check for overdue retrospective (last one older than 7 days)
LAST_RETRO=$(find "$LOG_DIR/reports" -name "weekly-*.md" -mtime -7 2>/dev/null | head -1)
if [ -z "$LAST_RETRO" ]; then
    URGENT="${URGENT}⚠ Weekly retrospective overdue (>7 days). Run /review.\n"
fi

# Check memory bank staleness
if [ -f "$PRISM_DIR/CONTEXT.md" ]; then
    CONTEXT_AGE=$(find "$PRISM_DIR/CONTEXT.md" -mtime +7 2>/dev/null)
    if [ -n "$CONTEXT_AGE" ]; then
        URGENT="${URGENT}⚠ CONTEXT.md is stale (>7 days old). Run /refresh.\n"
    fi
fi

# Check for recent EOD report
LAST_EOD=$(find "$LOG_DIR/reports" -name "eod-*.md" -mtime -1 2>/dev/null | head -1)
if [ -z "$LAST_EOD" ] && [ "$DAY_OF_WEEK" != "Saturday" ] && [ "$DAY_OF_WEEK" != "Sunday" ]; then
    URGENT="${URGENT}⚠ No EOD report today. Run /eod before end of day.\n"
fi

# Day-of-week smart reminders
if [ "$DAY_OF_WEEK" = "Monday" ]; then
    LAST_BRIEFING=$(find "$LOG_DIR/reports" -name "weekly-briefing*" -mtime -7 2>/dev/null | head -1)
    [ -z "$LAST_BRIEFING" ] && URGENT="${URGENT}📋 Monday — run /mission or /briefing to set the week.\n"
fi

if [ "$DAY_OF_WEEK" = "Friday" ]; then
    LAST_REVIEW=$(find "$LOG_DIR/reports" -name "weekly-*" -not -name "weekly-briefing*" -mtime -7 2>/dev/null | head -1)
    [ -z "$LAST_REVIEW" ] && URGENT="${URGENT}📋 Friday — run /review before wrapping up.\n"
fi

# Memory bank staleness (Mon/Wed/Fri)
if [ "$DAY_OF_WEEK" = "Monday" ] || [ "$DAY_OF_WEEK" = "Wednesday" ] || [ "$DAY_OF_WEEK" = "Friday" ]; then
    MB_STALE=$(find "$PRISM_DIR/memory-bank" -name "00-[your-username].md" -mtime +5 2>/dev/null)
    if [ -n "$MB_STALE" ]; then
        URGENT="${URGENT}⚠ Memory bank stale (>5 days). Run /refresh.\n"
    fi
fi

# ─── JOB 4: First-session-of-day auto-reports ───
# Generate health check, content pipeline, and yesterday's EOD on the first session each day
FIRST_SESSION_MARKER="$LOG_DIR/.first-session-$TODAY"
if [ ! -f "$FIRST_SESSION_MARKER" ] && [ "$DAY_OF_WEEK" != "Saturday" ] && [ "$DAY_OF_WEEK" != "Sunday" ]; then
    touch "$FIRST_SESSION_MARKER"

    SCRIPTS_DIR="$PRISM_DIR/scripts"

    # Health check (today)
    python3 "$SCRIPTS_DIR/generate-health-check.py" "$TODAY" >/dev/null 2>&1 &

    # Content pipeline status (today)
    python3 "$SCRIPTS_DIR/generate-content-pipeline.py" "$TODAY" >/dev/null 2>&1 &

    # Yesterday's EOD (if missing)
    YESTERDAY=$(date -v-1d +"%Y-%m-%d" 2>/dev/null || date -d "yesterday" +"%Y-%m-%d" 2>/dev/null)
    if [ -n "$YESTERDAY" ] && [ ! -f "$LOG_DIR/reports/eod-$YESTERDAY.md" ]; then
        python3 "$SCRIPTS_DIR/generate-eod-report.py" "$YESTERDAY" >/dev/null 2>&1 &
    fi

    # Content tree scan (Mondays only — heavier operation)
    if [ "$DAY_OF_WEEK" = "Monday" ]; then
        python3 "$SCRIPTS_DIR/content-tree-mapper.py" >/dev/null 2>&1 &
    fi

    # Wait for all background jobs to finish (they're fast)
    wait 2>/dev/null

    REPORTS_READY="yes"
fi

# ─── JOB 5: Name the terminal tab ───
# Derive a short project descriptor from the working directory
TAB_TITLE=""
case "$CWD" in
    */PRISM*|*/PRISM*)    TAB_TITLE="PRISM" ;;
    */parts-agent*|*/parts_agent*) TAB_TITLE="Parts Agent" ;;
    */[client-name-1]*|*/[Client-Name-1]*)     TAB_TITLE="[Client — Local Retail Business]" ;;
    */[client-id]*|*/[Client-ID]*|*/[client-name-3]*)      TAB_TITLE="[Client — Appliance Repair]" ;;
    */hri*|*/high-rise*|*/highrise*) TAB_TITLE="[Your Agency]" ;;
    *)
        # Use the last 1-2 directory components as the title
        LEAF=$(basename "$CWD")
        PARENT=$(basename "$(dirname "$CWD")")
        if [ "$PARENT" = "$USER" ] || [ "$PARENT" = "Users" ] || [ "$PARENT" = "/" ]; then
            TAB_TITLE="$LEAF"
        else
            TAB_TITLE="$PARENT/$LEAF"
        fi
        ;;
esac

# Persist tab title and launch detached enforcer
echo "$TAB_TITLE" > "$HOME/.claude_tab_title"

# Kill any previous title enforcer
[ -f "$HOME/.claude_tab_title_pid" ] && kill "$(cat "$HOME/.claude_tab_title_pid")" 2>/dev/null

# Fully detached background loop — closes all FDs so the hook exits instantly
nohup bash -c '
    echo $$ > "$HOME/.claude_tab_title_pid"
    while [ -f "$HOME/.claude_tab_title" ]; do
        printf "\033]0;%s\007" "$(cat "$HOME/.claude_tab_title")" > /dev/tty 2>/dev/null
        sleep 2
    done
' </dev/null >/dev/null 2>&1 &

# ─── OUTPUT: Context injection ───
echo "[PRISM DAILY CONTEXT — $DAY_OF_WEEK $TODAY]"
echo "Sessions today: $TODAY_SESSIONS | Tool calls: $TODAY_ACTIONS | Conversations: $RECENT_CONVOS"
echo "Parts agent: $PARTS_STATUS"

if [ -n "$URGENT" ]; then
    echo ""
    echo "URGENT:"
    printf "$URGENT"
fi

if [ "$REPORTS_READY" = "yes" ]; then
    echo ""
    echo "AUTO-REPORTS (first session of the day):"
    [ -f "$LOG_DIR/reports/health-$TODAY.md" ] && echo "  Health check: logs/reports/health-$TODAY.md"
    [ -f "$LOG_DIR/reports/content-pipeline-$TODAY.md" ] && echo "  Content pipeline: logs/reports/content-pipeline-$TODAY.md"
    [ -n "$YESTERDAY" ] && [ -f "$LOG_DIR/reports/eod-$YESTERDAY.md" ] && echo "  Yesterday's EOD: logs/reports/eod-$YESTERDAY.md"
fi

echo ""
echo "Slash commands: /review /refresh /briefing /eod /ship /health"
echo "Remember: Load ~/Documents/Claude/PRISM/CONTEXT.md before any non-trivial task."

exit 0
