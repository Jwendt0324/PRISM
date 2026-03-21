#!/usr/bin/env python3
"""
run.py — Entry point for D3S Service Scheduling Agent.
Parses data, runs optimizer, launches dashboard.

Usage:
  python3 run.py           # Full pipeline + dashboard
  python3 run.py --parse   # Parse only
  python3 run.py --optimize # Parse + optimize (no dashboard)
  python3 run.py --dashboard # Dashboard only (uses existing data)
"""

import sys
import os

# Add src/ to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))


def main():
    args = sys.argv[1:]

    if "--dashboard" in args:
        from dashboard import start_dashboard
        start_dashboard()
        return

    if "--parse" in args:
        from parser import run_all
        run_all()
        return

    # Default: full pipeline
    from scheduler import run_full_pipeline
    comparison = run_full_pipeline()

    if "--no-dashboard" not in args:
        print()
        print("Starting dashboard...")
        from dashboard import start_dashboard
        start_dashboard()


if __name__ == "__main__":
    main()
