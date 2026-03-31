#!/bin/bash
# Claude PRISM — Log Rotation
# Compresses old action logs and cleans up legacy files.
# Run weekly via cron.

PRISM_DIR="$HOME/Documents/Claude/PRISM"
ACTIONS_DIR="$PRISM_DIR/logs/actions"

echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") — Starting log rotation"

# Compress action logs older than 7 days
if [ -d "$ACTIONS_DIR" ]; then
    find "$ACTIONS_DIR" -name "*.jsonl" -mtime +7 -exec gzip -q {} \; 2>/dev/null
    echo "  Compressed action logs older than 7 days"
fi

# Delete compressed action logs older than 90 days
if [ -d "$ACTIONS_DIR" ]; then
    COUNT=$(find "$ACTIONS_DIR" -name "*.jsonl.gz" -mtime +90 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        find "$ACTIONS_DIR" -name "*.jsonl.gz" -mtime +90 -delete 2>/dev/null
        echo "  Deleted $COUNT compressed logs older than 90 days"
    fi
fi

# Clean up legacy files that are no longer written to
for LEGACY in "$PRISM_DIR/logs/hook-debug.log" "$PRISM_DIR/logs/tool-usage.log"; do
    if [ -f "$LEGACY" ]; then
        SIZE=$(stat -f%z "$LEGACY" 2>/dev/null || stat -c%s "$LEGACY" 2>/dev/null || echo 0)
        echo "  Found legacy file $LEGACY ($SIZE bytes) — removing"
        rm -f "$LEGACY"
    fi
done

# Report storage usage
if [ -d "$PRISM_DIR/logs" ]; then
    TOTAL=$(du -sh "$PRISM_DIR/logs" 2>/dev/null | cut -f1)
    echo "  Total logs storage: $TOTAL"
fi

echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") — Log rotation complete"
