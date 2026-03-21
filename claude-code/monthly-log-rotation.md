# Monthly Log Rotation — Automated Prompt

**Runs unattended via launchd on the 1st of each month.**

---

## Prompt

You are running the Monthly Log Rotation for the Claude Mainframe. This keeps log files from growing unbounded.

### Step 1: Rotate Large Logs

Check these files and rotate if they exceed thresholds:

1. `~/Documents/Claude/Mainframe/logs/hook-debug.log` — If over 10MB, move to `hook-debug-YYYYMM.log.bak` and create a fresh empty file
2. `~/Documents/Claude/Mainframe/logs/tool-usage.log` — If over 5MB, move to `tool-usage-YYYYMM.log.bak` and create a fresh empty file
3. `~/Documents/Claude/Mainframe/logs/session-events.log` — If over 2MB, move to `session-events-YYYYMM.log.bak` and create a fresh empty file

Use Bash commands like:
```bash
LOG="$HOME/Documents/Claude/Mainframe/logs/hook-debug.log"
SIZE=$(stat -f%z "$LOG" 2>/dev/null || echo 0)
if [ "$SIZE" -gt 10485760 ]; then
    mv "$LOG" "${LOG%.log}-$(date +%Y%m).log.bak"
    touch "$LOG"
fi
```

### Step 2: Archive Old Monthly Log Directories

Check for log directories older than 3 months (e.g., if current month is 2026-06, archive 2026-03 and earlier):
- Compress: `tar -czf logs/archive/YYYY-MM.tar.gz logs/YYYY-MM/`
- Remove the original directory after successful compression
- Create `logs/archive/` if it doesn't exist

### Step 3: Clean Up .bak Files

Delete any `.log.bak` files older than 6 months.

### Step 4: Write Rotation Log

Append to `~/Documents/Claude/Mainframe/logs/maintenance.log`:
```
YYYY-MM-DD | LOG_ROTATION | Files rotated: [list] | Directories archived: [list] | Space freed: [estimate]
```

---

## Configuration
- **Frequency:** 1st of each month, 3:07 AM
- **Duration:** Under 1 minute
- **Gmail required:** NO
