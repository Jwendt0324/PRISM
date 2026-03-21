#!/usr/bin/env python3
"""
D3S Parts Pricing Agent — Production Entry Point

Usage:
    python3 run.py                          # Process all active parts from PrtsPrcs
    python3 run.py --test 10                # Test mode: process first 10 parts only
    python3 run.py --prtsprcs /path/to/file # Use specific PrtsPrcs file
    python3 run.py --headless               # Force headless browser
    python3 run.py --headed                 # Force visible browser (debugging)
    python3 run.py --resume                 # Auto-resume incomplete run
    python3 run.py --dry-run                # Show what would be processed
    python3 run.py --dashboard-only         # Just start the dashboard, no processing
    python3 run.py --parse-only             # Parse PrtsPrcs and save CSV, no lookups

Combine flags as needed:
    python3 run.py --test 10 --headed       # Test 10 parts with visible browser
    python3 run.py --headless --resume      # Headless + auto-resume
"""

import argparse
import sys
from pathlib import Path

# Ensure the project root is on the Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import ProductionAgent
from src.dashboard import DashboardServer
from src.binary_parser import BinaryParser


def main():
    parser = argparse.ArgumentParser(
        description="D3S Parts Pricing Agent — Production"
    )
    parser.add_argument(
        "--test", type=int, metavar="N",
        help="Test mode: only process first N parts"
    )
    parser.add_argument(
        "--prtsprcs", type=str,
        help="Path to PrtsPrcs binary file (overrides config)"
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run browser in headless mode (no visible window)"
    )
    parser.add_argument(
        "--headed", action="store_true",
        help="Run browser with visible window (for debugging)"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Automatically resume incomplete runs without prompting"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be processed without running searches"
    )
    parser.add_argument(
        "--dashboard-only", action="store_true",
        help="Only start the dashboard server, don't process parts"
    )
    parser.add_argument(
        "--parse-only", action="store_true",
        help="Only parse PrtsPrcs and save CSV, don't do Marcone lookups"
    )
    parser.add_argument(
        "--port", type=int, default=8050,
        help="Dashboard port (default: 8050)"
    )
    parser.add_argument(
        "--no-dashboard", action="store_true",
        help="Skip starting the dashboard after processing"
    )
    args = parser.parse_args()

    # Dashboard-only mode
    if args.dashboard_only:
        server = DashboardServer(PROJECT_ROOT, port=args.port)
        server.start()
        return

    # Parse-only mode
    if args.parse_only:
        prtsprcs_path = args.prtsprcs or str(PROJECT_ROOT / "data" / "input" / "PrtsPrcs")
        log = lambda msg: print(f"[PARSE] {msg}")
        bp = BinaryParser(log)
        records = bp.parse_file(prtsprcs_path, filter_active=True)
        if records:
            output = PROJECT_ROOT / "data" / "output" / "parsed_parts_queue.csv"
            bp.save_parsed_csv(records, output)
            unique, _ = bp.get_unique_part_numbers(records)
            if args.test:
                print(f"\nFirst {args.test} parts:")
                for i, p in enumerate(unique[:args.test], 1):
                    print(f"  {i}. {p}")
            print(f"\nTotal active records: {len(records)}")
            print(f"Unique part numbers: {len(unique)}")
        return

    # Determine headless setting
    headless = None
    if args.headless:
        headless = True
    elif args.headed:
        headless = False

    # Start dashboard in background (unless --no-dashboard)
    if not args.no_dashboard:
        try:
            server = DashboardServer(PROJECT_ROOT, port=args.port)
            server.start_background()
        except Exception as e:
            print(f"WARNING: Could not start dashboard: {e}")

    # Run the agent
    agent = ProductionAgent(
        project_root=PROJECT_ROOT,
        prtsprcs_path=args.prtsprcs,
        headless=headless,
        auto_resume=args.resume,
        dry_run=args.dry_run,
        test_limit=args.test,
    )
    agent.run()

    # Keep dashboard running after processing (if started)
    if not args.no_dashboard and not args.dry_run:
        print(f"\nDashboard still running at http://localhost:{args.port}")
        print("Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down.")


if __name__ == "__main__":
    main()
