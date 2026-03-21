#!/usr/bin/env python3
"""
metrics.py — Before/after comparison stats for schedule optimization.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"


def compute_comparison(original_routes, optimized_routes, techs):
    """
    Compute before vs after metrics.
    Returns dict with summary and per-tech details.
    """
    # Aggregate original stats
    orig_total_miles = 0
    orig_total_drive_min = 0
    orig_total_jobs = 0
    orig_tech_details = {}

    for code, data in original_routes.items():
        s = data["stats"]
        orig_total_miles += s["total_miles"]
        orig_total_drive_min += s["drive_minutes"]
        orig_total_jobs += s["jobs"]
        orig_tech_details[code] = {
            "name": data["tech"]["name"],
            "miles": s["total_miles"],
            "drive_min": s["drive_minutes"],
            "work_min": s["work_minutes"],
            "jobs": s["jobs"],
            "capacity": data["tech"]["capacity"],
            "utilization": round(s["jobs"] / max(data["tech"]["capacity"], 1) * 100, 1),
        }

    # Aggregate optimized stats
    opt_total_miles = 0
    opt_total_drive_min = 0
    opt_total_jobs = 0
    opt_tech_details = {}

    for code, data in optimized_routes.items():
        s = data["stats"]
        opt_total_miles += s["total_miles"]
        opt_total_drive_min += s["drive_minutes"]
        opt_total_jobs += s["jobs"]
        opt_tech_details[code] = {
            "name": data["tech"]["name"],
            "miles": s["total_miles"],
            "drive_min": s["drive_minutes"],
            "work_min": s["work_minutes"],
            "jobs": s["jobs"],
            "capacity": data["tech"]["capacity"],
            "utilization": round(s["jobs"] / max(data["tech"]["capacity"], 1) * 100, 1),
            "stops": s.get("stops", []),
        }

    # Workload balance
    orig_jobs_per_tech = [d["jobs"] for d in orig_tech_details.values()]
    opt_jobs_per_tech = [d["jobs"] for d in opt_tech_details.values()]

    def _std_dev(vals):
        if len(vals) < 2:
            return 0
        mean = sum(vals) / len(vals)
        return (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5

    orig_balance_std = _std_dev(orig_jobs_per_tech) if orig_jobs_per_tech else 0
    opt_balance_std = _std_dev(opt_jobs_per_tech) if opt_jobs_per_tech else 0

    # Miles saved
    miles_saved = orig_total_miles - opt_total_miles
    miles_pct = (miles_saved / orig_total_miles * 100) if orig_total_miles > 0 else 0

    # Time saved
    time_saved = orig_total_drive_min - opt_total_drive_min
    time_pct = (time_saved / orig_total_drive_min * 100) if orig_total_drive_min > 0 else 0

    # Capacity freed up
    total_capacity = sum(t["capacity"] for t in techs.values())
    orig_capacity_used = orig_total_jobs
    opt_capacity_used = opt_total_jobs
    extra_capacity = total_capacity - opt_capacity_used

    # On-time estimation (jobs arriving within time window)
    on_time_count = 0
    total_with_window = 0
    for code, data in optimized_routes.items():
        for stop in data["stats"].get("stops", []):
            total_with_window += 1
            # Assume on-time if arrive before end of shift (5 PM = 1020 min)
            if stop["arrive_time"] <= 1020:
                on_time_count += 1

    on_time_pct = round(on_time_count / max(total_with_window, 1) * 100, 1)

    comparison = {
        "summary": {
            "original_total_miles": round(orig_total_miles, 1),
            "optimized_total_miles": round(opt_total_miles, 1),
            "miles_saved": round(miles_saved, 1),
            "miles_saved_pct": round(miles_pct, 1),
            "original_drive_minutes": round(orig_total_drive_min, 1),
            "optimized_drive_minutes": round(opt_total_drive_min, 1),
            "time_saved_minutes": round(time_saved, 1),
            "time_saved_pct": round(time_pct, 1),
            "original_jobs": orig_total_jobs,
            "optimized_jobs": opt_total_jobs,
            "total_tech_capacity": total_capacity,
            "extra_capacity_slots": extra_capacity,
            "original_balance_stddev": round(orig_balance_std, 2),
            "optimized_balance_stddev": round(opt_balance_std, 2),
            "on_time_pct": on_time_pct,
            "techs_active_original": len(orig_tech_details),
            "techs_active_optimized": len(opt_tech_details),
        },
        "original_by_tech": orig_tech_details,
        "optimized_by_tech": opt_tech_details,
    }

    return comparison


def save_metrics(comparison):
    """Save metrics to JSON file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dst = OUTPUT_DIR / "metrics.json"
    with open(dst, "w") as f:
        json.dump(comparison, f, indent=2, default=str)
    print(f"  Metrics saved to {dst}")
    return dst


def print_summary(comparison):
    """Print human-readable summary."""
    s = comparison["summary"]
    print()
    print("=" * 60)
    print("  [Client — Appliance Repair] SERVICE — SCHEDULE OPTIMIZATION RESULTS")
    print("=" * 60)
    print()
    print(f"  Total Jobs:           {s['original_jobs']} → {s['optimized_jobs']}")
    print(f"  Active Techs:         {s['techs_active_original']} → {s['techs_active_optimized']}")
    print()
    print(f"  Total Miles:          {s['original_total_miles']:,.1f} → {s['optimized_total_miles']:,.1f}")
    print(f"  Miles Saved:          {s['miles_saved']:,.1f} ({s['miles_saved_pct']:.1f}%)")
    print()
    print(f"  Total Drive Time:     {s['original_drive_minutes']:,.0f} min → {s['optimized_drive_minutes']:,.0f} min")
    print(f"  Time Saved:           {s['time_saved_minutes']:,.0f} min ({s['time_saved_pct']:.1f}%)")
    print()
    print(f"  Workload Balance:     σ={s['original_balance_stddev']:.1f} → σ={s['optimized_balance_stddev']:.1f}")
    print(f"  On-Time Arrivals:     {s['on_time_pct']}%")
    print(f"  Extra Capacity:       {s['extra_capacity_slots']} job slots available")
    print()

    # Per-tech comparison
    print("  Per-Tech Breakdown:")
    print(f"  {'Tech':<22s} {'Orig Mi':>8s} {'Opt Mi':>8s} {'Saved':>8s} {'Jobs':>5s} {'Util':>6s}")
    print("  " + "-" * 57)

    orig = comparison["original_by_tech"]
    opt = comparison["optimized_by_tech"]
    all_codes = sorted(set(list(orig.keys()) + list(opt.keys())))

    for code in all_codes:
        o = orig.get(code, {})
        n = opt.get(code, {})
        name = n.get("name", o.get("name", code))
        o_mi = o.get("miles", 0)
        n_mi = n.get("miles", 0)
        saved = o_mi - n_mi
        jobs = n.get("jobs", 0)
        util = n.get("utilization", 0)
        print(f"  {name:<22s} {o_mi:>7.1f} {n_mi:>7.1f} {saved:>+7.1f} {jobs:>5d} {util:>5.1f}%")

    print()


if __name__ == "__main__":
    from optimizer import optimize_schedule
    original, optimized, techs = optimize_schedule()
    comparison = compute_comparison(original, optimized, techs)
    save_metrics(comparison)
    print_summary(comparison)
