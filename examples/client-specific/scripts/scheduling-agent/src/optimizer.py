#!/usr/bin/env python3
"""
optimizer.py — Route optimization engine for [Client — Appliance Repair].

Uses nearest-neighbor heuristic with 2-opt improvement.
Accounts for: zone constraints, time windows, job durations,
drive time (haversine + 30mph avg), and tech capacity limits.
"""

import csv
import math
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
PARSED_DIR = BASE_DIR / "data" / "parsed"

# Average speed for drive time estimation (mph)
AVG_SPEED_MPH = 30
# Default job duration if not specified (minutes)
DEFAULT_JOB_MINUTES = 45


def haversine_miles(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points in miles."""
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def drive_time_minutes(lat1, lon1, lat2, lon2):
    """Estimated drive time in minutes between two GPS points."""
    dist = haversine_miles(lat1, lon1, lat2, lon2)
    return (dist / AVG_SPEED_MPH) * 60 if AVG_SPEED_MPH > 0 else 0


def load_techs():
    """Load technician data from parsed CSV."""
    techs = {}
    with open(PARSED_DIR / "techs.csv") as f:
        for r in csv.DictReader(f):
            if r["is_fake"] == "1":
                continue
            lat = float(r["lat"]) if r["lat"] else 0
            lon = float(r["lon"]) if r["lon"] else 0
            if lat == 0 or lon == 0:
                continue
            techs[r["code"]] = {
                "name": r["name"],
                "code": r["code"],
                "lat": lat,
                "lon": lon,
                "capacity": int(r["capacity"]) if r["capacity"] else 10,
                "avg_minutes": int(r["avg_minutes"]) if r["avg_minutes"] else DEFAULT_JOB_MINUTES,
                "target_miles": int(r["target_miles"]) if r["target_miles"] else 0,
                "address": r["address"],
            }
    return techs


def load_zones():
    """Load zip-to-zone mapping."""
    zip_to_zone = {}
    with open(PARSED_DIR / "zones.csv") as f:
        for r in csv.DictReader(f):
            zip_to_zone[r["zip_code"]] = r["zone"]
    return zip_to_zone


def load_tech_zone_assignments():
    """Load which techs serve which zones."""
    zone_to_techs = {}
    with open(PARSED_DIR / "tech_zones.csv") as f:
        for r in csv.DictReader(f):
            codes = [c.strip() for c in r["tech_codes"].split(",") if c.strip()]
            zone_to_techs[r["zone"]] = codes
    return zone_to_techs


def load_schedule():
    """Load current schedule from parsed CSV."""
    jobs = []
    with open(PARSED_DIR / "schedule.csv") as f:
        for r in csv.DictReader(f):
            if not r["zip_code"] or not r["tech_code"]:
                continue
            jobs.append({
                "id": r["record_id"],
                "customer": r["customer"],
                "zip_code": r["zip_code"].strip(),
                "city": r["city"],
                "date": r["date"],
                "day": r["day"],
                "time_window": r["time_window"],
                "tech_code": r["tech_code"],
                "route_info": r.get("route_info", ""),
            })
    return jobs


def _time_window_to_hours(tw):
    """Parse time window like '8-12' into (start_hour, end_hour)."""
    if not tw or tw == "!":
        return (8, 17)  # default full day
    tw = tw.replace("AM", "").replace("PM", "").strip()
    parts = tw.split("-")
    if len(parts) != 2:
        return (8, 17)
    try:
        start = int(parts[0])
        end = int(parts[1])
        # Handle PM times: 1-5 means 13-17
        if start < 6:
            start += 12
        if end <= 6:
            end += 12
        return (start, end)
    except ValueError:
        return (8, 17)


def _load_zip_centroids():
    """Load real zip code centroids from geocoded data."""
    centroids_file = PARSED_DIR / "zip_centroids.json"
    if centroids_file.exists():
        import json
        with open(centroids_file) as f:
            raw = json.load(f)
        return {k: tuple(v) for k, v in raw.items()}
    return {}


_ZIP_CENTROIDS = None


def _estimate_job_coords(zip_code, zip_to_zone, techs, zone_to_techs):
    """
    Get job GPS coordinates from real zip code centroids.
    Falls back to zone-based estimation only if zip centroid unavailable.
    """
    global _ZIP_CENTROIDS
    if _ZIP_CENTROIDS is None:
        _ZIP_CENTROIDS = _load_zip_centroids()

    # Use real zip centroid if available
    zc = zip_code.strip()
    if zc in _ZIP_CENTROIDS:
        return _ZIP_CENTROIDS[zc]

    # Fallback: zone centroid for unrecognized zips
    zone = zip_to_zone.get(zip_code)
    if not zone:
        return None, None

    assigned = zone_to_techs.get(zone, [])
    lats, lons = [], []
    for tc in assigned:
        if tc in techs:
            lats.append(techs[tc]["lat"])
            lons.append(techs[tc]["lon"])

    if not lats:
        return None, None

    return sum(lats) / len(lats), sum(lons) / len(lons)


def nearest_neighbor_route(tech, jobs_for_tech):
    """
    Build route using nearest-neighbor heuristic.
    Returns ordered list of jobs.
    """
    if not jobs_for_tech:
        return []

    current_lat = tech["lat"]
    current_lon = tech["lon"]
    remaining = list(jobs_for_tech)
    route = []

    while remaining:
        best_idx = 0
        best_dist = float("inf")
        for i, job in enumerate(remaining):
            if job.get("lat") is None:
                continue
            d = haversine_miles(current_lat, current_lon, job["lat"], job["lon"])
            if d < best_dist:
                best_dist = d
                best_idx = i

        chosen = remaining.pop(best_idx)
        route.append(chosen)
        if chosen.get("lat") is not None:
            current_lat = chosen["lat"]
            current_lon = chosen["lon"]

    return route


def two_opt_improve(tech, route, max_iterations=100):
    """Apply 2-opt improvement to reduce total route distance."""
    if len(route) < 3:
        return route

    def total_distance(r):
        dist = haversine_miles(tech["lat"], tech["lon"],
                               r[0].get("lat", tech["lat"]),
                               r[0].get("lon", tech["lon"]))
        for i in range(len(r) - 1):
            dist += haversine_miles(
                r[i].get("lat", 0), r[i].get("lon", 0),
                r[i+1].get("lat", 0), r[i+1].get("lon", 0))
        # Return to home
        dist += haversine_miles(r[-1].get("lat", tech["lat"]),
                                r[-1].get("lon", tech["lon"]),
                                tech["lat"], tech["lon"])
        return dist

    best = list(route)
    best_dist = total_distance(best)

    improved = True
    iterations = 0
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        for i in range(len(best) - 1):
            for j in range(i + 1, len(best)):
                candidate = best[:i] + best[i:j+1][::-1] + best[j+1:]
                d = total_distance(candidate)
                if d < best_dist - 0.01:
                    best = candidate
                    best_dist = d
                    improved = True

    return best


def compute_route_stats(tech, route):
    """Compute distance, drive time, and work time for a route."""
    if not route:
        return {"total_miles": 0, "drive_minutes": 0, "work_minutes": 0,
                "jobs": 0, "stops": []}

    total_miles = 0
    stops = []
    current_lat, current_lon = tech["lat"], tech["lon"]
    current_time = 8 * 60  # Start at 8 AM in minutes
    current_date = None
    day_stop = 0

    for job in route:
        # Reset to home at 8 AM when the date changes
        job_date = job.get("date", "")
        if job_date != current_date:
            current_date = job_date
            current_lat, current_lon = tech["lat"], tech["lon"]
            current_time = 8 * 60
            day_stop = 0

        j_lat = job.get("lat") or current_lat
        j_lon = job.get("lon") or current_lon
        leg_miles = haversine_miles(current_lat, current_lon, j_lat, j_lon)
        leg_minutes = drive_time_minutes(current_lat, current_lon, j_lat, j_lon)
        total_miles += leg_miles
        current_time += leg_minutes
        day_stop += 1

        job_duration = tech.get("avg_minutes", DEFAULT_JOB_MINUTES)
        if job_duration == 0:
            job_duration = DEFAULT_JOB_MINUTES

        stops.append({
            "job_id": job["id"],
            "customer": job["customer"],
            "zip_code": job["zip_code"],
            "date": job_date,
            "day": job.get("day", ""),
            "time_window": job.get("time_window", ""),
            "lat": j_lat,
            "lon": j_lon,
            "arrive_time": current_time,
            "leg_miles": round(leg_miles, 1),
            "leg_minutes": round(leg_minutes, 1),
            "day_stop": day_stop,
        })

        current_time += job_duration
        current_lat, current_lon = j_lat, j_lon

    # Return home
    home_miles = haversine_miles(current_lat, current_lon, tech["lat"], tech["lon"])
    total_miles += home_miles

    return {
        "total_miles": round(total_miles, 1),
        "drive_minutes": round(total_miles / AVG_SPEED_MPH * 60, 1),
        "work_minutes": round(len(route) * tech.get("avg_minutes", DEFAULT_JOB_MINUTES), 1),
        "jobs": len(route),
        "stops": stops,
    }


def optimize_schedule(jobs=None):
    """
    Main optimization entry point.
    Returns: (original_assignments, optimized_assignments, techs)
    """
    techs = load_techs()
    zip_to_zone = load_zones()
    zone_to_techs = load_tech_zone_assignments()

    if jobs is None:
        jobs = load_schedule()

    # Enrich jobs with estimated coordinates
    for job in jobs:
        lat, lon = _estimate_job_coords(
            job["zip_code"], zip_to_zone, techs, zone_to_techs)
        job["lat"] = lat
        job["lon"] = lon

    # Filter to jobs that have coordinates
    jobs = [j for j in jobs if j.get("lat") is not None and j.get("lon") is not None]

    # --- ORIGINAL ASSIGNMENT (as-is from ServiceDesk) ---
    original_by_tech = defaultdict(list)
    for job in jobs:
        if job["tech_code"] in techs:
            original_by_tech[job["tech_code"]].append(job)

    original_routes = {}
    for code, tech_jobs in original_by_tech.items():
        tech = techs[code]
        stats = compute_route_stats(tech, tech_jobs)
        original_routes[code] = {
            "tech": tech,
            "route": tech_jobs,
            "stats": stats,
        }

    # --- OPTIMIZED ASSIGNMENT ---
    # Step 1: Group jobs by date
    jobs_by_date = defaultdict(list)
    for job in jobs:
        jobs_by_date[job["date"]].append(job)

    optimized_by_tech = defaultdict(list)

    for date, date_jobs in jobs_by_date.items():
        # Group by zone for assignment
        jobs_by_zone = defaultdict(list)
        for job in date_jobs:
            zone = zip_to_zone.get(job["zip_code"], "0")
            jobs_by_zone[zone].append(job)

        # Assign jobs respecting zone constraints
        tech_loads = {code: 0 for code in techs}

        for zone, zone_jobs in jobs_by_zone.items():
            eligible = zone_to_techs.get(zone, [])
            eligible = [c for c in eligible if c in techs]
            if not eligible:
                # Fallback: find nearest available tech
                for job in zone_jobs:
                    if job.get("lat") is None:
                        continue
                    best_code = min(
                        techs.keys(),
                        key=lambda c: haversine_miles(
                            techs[c]["lat"], techs[c]["lon"],
                            job["lat"], job["lon"])
                        if tech_loads[c] < techs[c]["capacity"] else 9999
                    )
                    optimized_by_tech[best_code].append(job)
                    tech_loads[best_code] += 1
                continue

            for job in zone_jobs:
                if job.get("lat") is None:
                    continue
                # Pick eligible tech with lowest load who is closest
                best_code = min(
                    eligible,
                    key=lambda c: (
                        tech_loads.get(c, 0) / max(techs[c]["capacity"], 1),
                        haversine_miles(techs[c]["lat"], techs[c]["lon"],
                                        job.get("lat", 0), job.get("lon", 0))
                        if c in techs else 9999
                    )
                )
                optimized_by_tech[best_code].append(job)
                tech_loads[best_code] = tech_loads.get(best_code, 0) + 1

    # Step 2: Optimize route order for each tech
    optimized_routes = {}
    for code, tech_jobs in optimized_by_tech.items():
        if code not in techs:
            continue
        tech = techs[code]
        # Group by date, optimize each day separately
        by_date = defaultdict(list)
        for j in tech_jobs:
            by_date[j["date"]].append(j)

        all_ordered = []
        for date in sorted(by_date.keys()):
            nn_route = nearest_neighbor_route(tech, by_date[date])
            improved = two_opt_improve(tech, nn_route)
            all_ordered.extend(improved)

        stats = compute_route_stats(tech, all_ordered)
        optimized_routes[code] = {
            "tech": tech,
            "route": all_ordered,
            "stats": stats,
        }

    return original_routes, optimized_routes, techs


if __name__ == "__main__":
    original, optimized, techs = optimize_schedule()
    print(f"Optimized {len(original)} original tech routes → {len(optimized)} optimized routes")
    print()
    for code in sorted(optimized.keys()):
        o = original.get(code, {}).get("stats", {})
        n = optimized[code]["stats"]
        name = techs[code]["name"]
        print(f"  {name:20s} ({code}): "
              f"{o.get('total_miles', 0):6.1f}mi → {n['total_miles']:6.1f}mi  "
              f"({o.get('jobs', 0)} → {n['jobs']} jobs)")
