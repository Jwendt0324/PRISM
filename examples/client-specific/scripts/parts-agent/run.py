#!/usr/bin/env python3
"""
Parts Lookup Agent v2 — Entry Point

Usage:
    python3 run.py                  # Normal run (headed browser, visible)
    python3 run.py --headless       # Run without browser window
    python3 run.py --resume         # Auto-resume incomplete run (no prompt)
    python3 run.py --dry-run        # Show what would be processed, don't run
    python3 run.py --headless --resume   # Combine flags

Drop CSV files into data/input/ before running.
"""

import argparse
import sys
from pathlib import Path

# Ensure the project root is on the Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import BatchAgent


def main():
    parser = argparse.ArgumentParser(
        description="Parts Lookup Agent v2 — Batch processing engine"
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run browser in headless mode (no visible window)"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Automatically resume incomplete runs without prompting"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be processed without actually running searches"
    )
    args = parser.parse_args()

    agent = BatchAgent(
        project_root=PROJECT_ROOT,
        headless=args.headless if args.headless else None,
        auto_resume=args.resume,
        dry_run=args.dry_run,
    )
    agent.run()


if __name__ == "__main__":
    main()
