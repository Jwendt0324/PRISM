#!/usr/bin/env python3
"""
dashboard.py — Web dashboard for D3S Service scheduling agent.
Python standard library only (http.server). Serves on localhost:8051.
Leaflet map with real tech data, routes, before/after comparison.
"""

import csv
import http.server
import json
import socketserver
from pathlib import Path

PORT = 8051
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "output"
PARSED_DIR = BASE_DIR / "data" / "parsed"


def load_dashboard_data():
    """Load all data needed for the dashboard."""
    data = {"techs": [], "metrics": {}, "optimized_schedule": [], "zones": {}}

    # Techs
    techs_file = PARSED_DIR / "techs.csv"
    if techs_file.exists():
        with open(techs_file) as f:
            for r in csv.DictReader(f):
                if r.get("is_fake") == "1":
                    continue
                lat = float(r["lat"]) if r.get("lat") else 0
                lon = float(r["lon"]) if r.get("lon") else 0
                if lat == 0 or lon == 0:
                    continue
                data["techs"].append({
                    "name": r["name"],
                    "code": r["code"],
                    "lat": lat,
                    "lon": lon,
                    "capacity": int(r["capacity"]) if r.get("capacity") else 10,
                    "avg_minutes": int(r["avg_minutes"]) if r.get("avg_minutes") else 45,
                    "address": r["address"],
                    "phone": r.get("phone", ""),
                })

    # Metrics
    metrics_file = OUTPUT_DIR / "metrics.json"
    if metrics_file.exists():
        with open(metrics_file) as f:
            data["metrics"] = json.load(f)

    # Optimized schedule
    sched_file = OUTPUT_DIR / "optimized_schedule.csv"
    if sched_file.exists():
        with open(sched_file) as f:
            data["optimized_schedule"] = list(csv.DictReader(f))

    return data


def build_html(data):
    """Build the complete dashboard HTML."""
    techs_json = json.dumps(data["techs"])
    metrics_json = json.dumps(data.get("metrics", {}))
    schedule_json = json.dumps(data.get("optimized_schedule", []))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>D3S Service — Scheduling Agent</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a1a; color: #e0e0e0; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }}

/* ── HEADER ── */
.header {{
  background: #242424; padding: 14px 24px; border-bottom: 1px solid #333;
  display: flex; align-items: center; justify-content: space-between; flex-shrink: 0;
}}
.header-left h1 {{ font-size: 18px; font-weight: 700; color: #fff; letter-spacing: -0.3px; }}
.header-left .subtitle {{ color: #888; font-size: 12px; margin-top: 2px; }}
.header-right {{ display: flex; gap: 4px; }}
.toggle-btn {{
  padding: 6px 16px; border: 1px solid #444; background: transparent;
  color: #888; font-size: 12px; font-weight: 600; cursor: pointer;
  transition: all 0.15s; letter-spacing: 0.5px;
}}
.toggle-btn:first-child {{ border-radius: 4px 0 0 4px; }}
.toggle-btn:last-child {{ border-radius: 0 4px 4px 0; }}
.toggle-btn.active {{ background: #1D9E75; color: #fff; border-color: #1D9E75; }}

/* ── METRICS ROW ── */
.metrics-row {{
  display: flex; gap: 12px; padding: 12px 24px; background: #1a1a1a;
  border-bottom: 1px solid #333; flex-shrink: 0; overflow-x: auto;
}}
.metric-card {{
  flex: 1; min-width: 140px; background: #242424; border-radius: 8px;
  padding: 12px 16px; border: 1px solid #333;
}}
.metric-card .mc-label {{ font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }}
.metric-card .mc-row {{ display: flex; align-items: baseline; gap: 8px; margin-top: 6px; }}
.metric-card .mc-before {{ font-size: 14px; color: #666; font-family: 'SF Mono', 'Fira Code', monospace; text-decoration: line-through; }}
.metric-card .mc-arrow {{ color: #555; font-size: 12px; }}
.metric-card .mc-after {{ font-size: 22px; font-weight: 700; color: #fff; font-family: 'SF Mono', 'Fira Code', monospace; }}
.metric-card .mc-diff {{ font-size: 12px; font-weight: 600; margin-top: 4px; font-family: 'SF Mono', 'Fira Code', monospace; }}
.mc-diff.green {{ color: #1D9E75; }}
.mc-diff.red {{ color: #E24B4A; }}

/* ── MAIN LAYOUT ── */
.main {{ display: flex; flex: 1; min-height: 0; }}

/* ── LEFT SIDEBAR ── */
.sidebar {{
  width: 300px; flex-shrink: 0; background: #1e1e1e; border-right: 1px solid #333;
  display: flex; flex-direction: column; overflow: hidden;
}}
.sidebar-header {{ padding: 12px; border-bottom: 1px solid #333; flex-shrink: 0; }}
.sidebar-header .sb-title {{ font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }}
.clear-btn {{
  display: none; margin-top: 8px; padding: 5px 12px; border: 1px solid #444;
  background: transparent; color: #888; font-size: 11px; border-radius: 4px;
  cursor: pointer; width: 100%;
}}
.clear-btn:hover {{ border-color: #E24B4A; color: #E24B4A; }}
.clear-btn.visible {{ display: block; }}
.tech-list {{ flex: 1; overflow-y: auto; padding: 8px; }}
.tech-card {{
  background: #242424; border: 1px solid #333; border-radius: 6px;
  padding: 10px 12px; margin-bottom: 6px; cursor: pointer; transition: all 0.12s;
}}
.tech-card:hover {{ border-color: #555; background: #2a2a2a; }}
.tech-card.selected {{ border-color: #1D9E75; background: #1a2e26; box-shadow: inset 3px 0 0 #1D9E75; }}
.tc-top {{ display: flex; align-items: center; gap: 8px; }}
.tc-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.tc-name {{ font-weight: 600; font-size: 13px; color: #e0e0e0; }}
.tc-code {{ font-size: 11px; color: #666; margin-left: 4px; }}
.tc-stats {{ display: flex; gap: 12px; margin-top: 6px; font-size: 11px; color: #888; }}
.tc-stats strong {{ color: #ccc; font-family: 'SF Mono', 'Fira Code', monospace; }}

/* ── RIGHT CONTENT ── */
.right-content {{ flex: 1; display: flex; flex-direction: column; min-width: 0; }}
#map {{ flex: 1; min-height: 400px; }}

/* ── JOB TABLE (below map) ── */
.job-table-wrap {{
  display: none; max-height: 220px; overflow-y: auto; background: #1e1e1e;
  border-top: 1px solid #333; flex-shrink: 0;
}}
.job-table-wrap.visible {{ display: block; }}
.job-table-header {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 16px; background: #242424; border-bottom: 1px solid #333;
  position: sticky; top: 0; z-index: 1;
}}
.job-table-header h3 {{ font-size: 13px; color: #1D9E75; font-weight: 600; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
thead th {{
  text-align: left; padding: 6px 12px; color: #888; font-weight: 600;
  text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px;
  background: #242424; position: sticky; top: 36px; z-index: 1;
}}
tbody td {{ padding: 6px 12px; border-top: 1px solid #2a2a2a; color: #ccc; font-family: 'SF Mono', 'Fira Code', monospace; font-size: 11px; }}
tbody tr:hover {{ background: #2a2a2a; }}
tbody tr.late td {{ color: #E24B4A; }}

/* ── LEAFLET LAYER CONTROL DARK THEME ── */
.leaflet-control-layers {{
  background: #242424 !important; border: 1px solid #444 !important;
  border-radius: 6px !important; color: #ccc !important;
}}
.leaflet-control-layers-toggle {{
  background-color: #242424 !important;
  border: 1px solid #444 !important;
  border-radius: 6px !important;
}}
.leaflet-control-layers label {{ color: #ccc !important; font-size: 12px; }}
.leaflet-control-layers-separator {{ border-top-color: #444 !important; }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-left">
    <h1>D3S Service — Scheduling Agent</h1>
    <div class="subtitle">31 Technicians &middot; 58 Zones &middot; East Texas + Oklahoma</div>
  </div>
  <div class="header-right">
    <button class="toggle-btn" id="btnOriginal" onclick="setView('original')">ORIGINAL</button>
    <button class="toggle-btn active" id="btnOptimized" onclick="setView('optimized')">OPTIMIZED</button>
  </div>
</div>

<!-- METRICS ROW -->
<div class="metrics-row" id="metricsRow"></div>

<!-- MAIN -->
<div class="main">
  <!-- LEFT SIDEBAR -->
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="sb-title">Technicians &middot; <span id="techCount">0</span> active</div>
      <button class="clear-btn" id="clearBtn" onclick="clearSelection()">Clear Selection</button>
    </div>
    <div class="tech-list" id="techList"></div>
  </div>

  <!-- RIGHT SIDE -->
  <div class="right-content">
    <div id="map"></div>
    <div class="job-table-wrap" id="jobTableWrap">
      <div class="job-table-header">
        <h3 id="jobTableTitle">Route Details</h3>
      </div>
      <table>
        <thead>
          <tr>
            <th>Stop</th><th>Customer</th><th>Zip</th><th>Date</th><th>Time Window</th>
            <th>Est. Arrive</th><th>Drive Miles</th><th>Duration</th>
          </tr>
        </thead>
        <tbody id="jobTableBody"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
const TECHS = {techs_json};
const METRICS = {metrics_json};
const SCHEDULE = {schedule_json};

const COLORS = [
  '#58a6ff','#3fb950','#f0883e','#bc8cff','#f778ba',
  '#79c0ff','#56d364','#d29922','#db61a2','#ff7b72',
  '#a5d6ff','#7ee787','#e3b341','#d2a8ff','#ffa198',
  '#39d353','#2ea043','#f78166','#b392f0','#ffdf5d',
  '#8b949e','#da3633','#1f6feb','#238636','#d29922',
  '#8957e5','#bf4b8a','#3fb950','#58a6ff','#f0883e','#bc8cff'
];

let map, selectedTech = null, selectedDate = null, currentView = 'optimized';
let techMarkers = {{}}, routeLayer = null, stopMarkers = [];
let jobsLayer = null, layerControl = null;

// ── INIT ──
function init() {{
  initMap();
  buildMetrics();
  buildTechList();
}}

function initMap() {{
  map = L.map('map', {{ zoomControl: true }}).setView([30.5, -95.5], 7);
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    attribution: '&copy; CartoDB', maxZoom: 18
  }}).addTo(map);
  plotTechHomes();
  buildJobsLayer();
}}

function plotTechHomes() {{
  // Clear existing
  Object.values(techMarkers).forEach(m => map.removeLayer(m));
  techMarkers = {{}};

  const bounds = [];
  TECHS.forEach((tech, i) => {{
    const color = COLORS[i % COLORS.length];
    const marker = L.circleMarker([tech.lat, tech.lon], {{
      radius: 7, fillColor: color, color: '#fff', weight: 2, opacity: 1, fillOpacity: 0.9
    }}).addTo(map);
    marker.bindTooltip(tech.name, {{ permanent: false, direction: 'top', offset: [0, -10] }});
    marker.on('click', () => selectTech(tech.code));
    marker._techColor = color;
    techMarkers[tech.code] = marker;
    bounds.push([tech.lat, tech.lon]);
  }});

  if (bounds.length > 0) map.fitBounds(bounds, {{ padding: [40, 40] }});
}}

// ── JOBS LAYER ──
function buildJobsLayer() {{
  // Build a lookup: tech_code -> color index
  const techColorMap = {{}};
  TECHS.forEach((t, i) => {{ techColorMap[t.code] = COLORS[i % COLORS.length]; }});

  jobsLayer = L.layerGroup();

  SCHEDULE.forEach(job => {{
    const lat = parseFloat(job.lat);
    const lon = parseFloat(job.lon);
    if (!lat || !lon) return;

    const color = techColorMap[job.tech_code] || '#8b949e';
    const marker = L.circleMarker([lat, lon], {{
      radius: 4,
      fillColor: color,
      color: color,
      weight: 1,
      opacity: 0.7,
      fillOpacity: 0.5,
    }});

    marker.bindPopup(`
      <div style="font-family:sans-serif;min-width:150px;">
        <b>${{job.customer}}</b><br>
        ZIP: ${{job.zip_code}}<br>
        Date: ${{job.date || '—'}} ${{job.day || ''}}<br>
        Window: ${{job.time_window || '—'}}<br>
        Tech: ${{job.tech_name}} (${{job.tech_code}})<br>
        Stop #${{job.stop_order}}<br>
        Arrive: ${{job.arrive_time_display}}<br>
        Leg: ${{job.leg_miles}} mi
      </div>
    `);

    jobsLayer.addLayer(marker);
  }});

  // Create layer control with tech homes (always on) and jobs (toggleable)
  const techHomesLayer = L.layerGroup(Object.values(techMarkers));
  const overlays = {{
    ['All Jobs (' + SCHEDULE.length + ')']: jobsLayer,
  }};
  layerControl = L.control.layers(null, overlays, {{ collapsed: false, position: 'topright' }}).addTo(map);
}}

// ── METRICS ──
function buildMetrics() {{
  const s = METRICS.summary || {{}};
  const row = document.getElementById('metricsRow');
  const origMi = s.original_total_miles || 0;
  const optMi = s.optimized_total_miles || 0;
  const origDrH = Math.round((s.original_drive_minutes || 0) / 60);
  const optDrH = Math.round((s.optimized_drive_minutes || 0) / 60);

  // Compute savings excluding JK misassignment to show honest route optimization
  const jkOrig = (METRICS.original_by_tech?.JK?.miles) || 0;
  const routeOnlySaved = origMi - jkOrig - optMi;
  const routeOnlyPct = ((routeOnlySaved) / Math.max(origMi - jkOrig, 1) * 100);

  const cards = [
    {{ label: 'Total Miles', before: origMi.toLocaleString(), after: optMi.toLocaleString(), diff: `-${{(s.miles_saved||0).toFixed(0)}} mi (${{(s.miles_saved_pct||0).toFixed(1)}}%)`, green: true }},
    {{ label: 'Route Optimization', before: `${{Math.round(origMi - jkOrig)}}`, after: optMi.toLocaleString(), diff: `${{Math.round(routeOnlySaved)}} mi saved (${{routeOnlyPct.toFixed(1)}}%) excl. reassign`, green: routeOnlySaved > 0 }},
    {{ label: 'Drive Time', before: `${{origDrH}}h`, after: `${{optDrH}}h`, diff: `-${{Math.round((s.time_saved_minutes||0)/60)}}h (${{(s.time_saved_pct||0).toFixed(1)}}%)`, green: true }},
    {{ label: 'Active Techs', before: `${{s.techs_active_original||0}}`, after: `${{s.techs_active_optimized||0}}`, diff: `${{(s.optimized_jobs||0)}} jobs across ${{s.techs_active_optimized||0}} techs`, green: true }},
    {{ label: 'On-Time', before: '—', after: `${{s.on_time_pct||0}}%`, diff: `within time window`, green: (s.on_time_pct||0) >= 80 }},
    {{ label: 'Workload Balance', before: `\\u03C3=${{(s.original_balance_stddev||0).toFixed(1)}}`, after: `\\u03C3=${{(s.optimized_balance_stddev||0).toFixed(1)}}`, diff: `${{(((s.original_balance_stddev||1)-(s.optimized_balance_stddev||0))/(s.original_balance_stddev||1)*100).toFixed(1)}}% more even`, green: true }},
  ];

  row.innerHTML = cards.map(c => `
    <div class="metric-card">
      <div class="mc-label">${{c.label}}</div>
      <div class="mc-row">
        <span class="mc-before">${{c.before}}</span>
        <span class="mc-arrow">&#8594;</span>
        <span class="mc-after">${{c.after}}</span>
      </div>
      <div class="mc-diff ${{c.green ? 'green' : 'red'}}">${{c.diff}}</div>
    </div>
  `).join('');
}}

// ── TECH LIST ──
function buildTechList() {{
  const list = document.getElementById('techList');
  const orig = METRICS.original_by_tech || {{}};
  const opt = METRICS.optimized_by_tech || {{}};

  // Sort by miles saved (descending)
  const sorted = [...TECHS].sort((a, b) => {{
    const aSaved = (orig[a.code]?.miles || 0) - (opt[a.code]?.miles || 0);
    const bSaved = (orig[b.code]?.miles || 0) - (opt[b.code]?.miles || 0);
    return bSaved - aSaved;
  }});

  // Count active techs
  const active = sorted.filter(t => (opt[t.code]?.jobs || 0) > 0).length;
  document.getElementById('techCount').textContent = active;

  list.innerHTML = sorted.map(tech => {{
    const i = TECHS.indexOf(tech);
    const color = COLORS[i % COLORS.length];
    const n = opt[tech.code] || {{}};
    const oo = orig[tech.code] || {{}};
    const driveH = ((n.drive_min || 0) / 60).toFixed(1);
    const milesSaved = (oo.miles || 0) - (n.miles || 0);
    const milesDiff = milesSaved > 0 ? `<span style="color:#1D9E75">-${{milesSaved.toFixed(0)}}</span>`
                    : milesSaved < 0 ? `<span style="color:#E24B4A">+${{Math.abs(milesSaved).toFixed(0)}}</span>` : '';
    // Per-day breakdown
    const techJobs = SCHEDULE.filter(s => s.tech_code === tech.code);
    const byDate = {{}};
    techJobs.forEach(j => {{ byDate[j.date] = (byDate[j.date] || 0) + 1; }});
    const dateKeys = Object.keys(byDate).sort((a, b) => {{
      const pa = a.split('/').map(Number), pb = b.split('/').map(Number);
      return (pa[0]*100+pa[1]) - (pb[0]*100+pb[1]);
    }});
    const daySummary = dateKeys.map(d => `${{d}}: ${{byDate[d]}}`).join(' · ');
    return `
      <div class="tech-card" id="card-${{tech.code}}" onclick="selectTech('${{tech.code}}')">
        <div class="tc-top">
          <span class="tc-dot" style="background:${{color}}"></span>
          <span class="tc-name">${{tech.name}}</span>
          <span class="tc-code">${{tech.code}}</span>
        </div>
        <div class="tc-stats">
          <span><strong>${{n.jobs||0}}</strong> jobs / ${{dateKeys.length}} days</span>
          <span><strong>${{(n.miles||0).toFixed(0)}}</strong> mi ${{milesDiff}}</span>
          <span><strong>${{driveH}}</strong>h</span>
        </div>
        <div style="font-size:10px;color:#666;margin-top:4px;">${{daySummary}}</div>
      </div>
    `;
  }}).join('');
}}

// ── SELECT TECH ──
function selectTech(code) {{
  // Deselect previous
  if (selectedTech) {{
    const prev = document.getElementById('card-' + selectedTech);
    if (prev) prev.classList.remove('selected');
  }}
  clearRoute();

  if (selectedTech === code) {{
    selectedTech = null;
    document.getElementById('clearBtn').classList.remove('visible');
    document.getElementById('jobTableWrap').classList.remove('visible');
    plotTechHomes();
    return;
  }}

  selectedTech = code;
  const card = document.getElementById('card-' + code);
  if (card) {{
    card.classList.add('selected');
    card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
  }}
  document.getElementById('clearBtn').classList.add('visible');

  // Find the tech's dates and default to the first one
  const techJobs = SCHEDULE.filter(s => s.tech_code === code);
  const dates = [...new Set(techJobs.map(j => j.date))].sort((a, b) => {{
    const pa = a.split('/').map(Number), pb = b.split('/').map(Number);
    return (pa[0]*100+pa[1]) - (pb[0]*100+pb[1]);
  }});
  selectedDate = dates[0] || null;

  drawRoute(code, selectedDate);
  buildJobTable(code);
}}

function clearSelection() {{
  if (selectedTech) {{
    const card = document.getElementById('card-' + selectedTech);
    if (card) card.classList.remove('selected');
  }}
  clearRoute();
  selectedTech = null;
  document.getElementById('clearBtn').classList.remove('visible');
  document.getElementById('jobTableWrap').classList.remove('visible');
  plotTechHomes();
}}

function clearRoute() {{
  if (routeLayer) {{ map.removeLayer(routeLayer); routeLayer = null; }}
  stopMarkers.forEach(m => map.removeLayer(m));
  stopMarkers = [];
}}

// ── DRAW ROUTE ──
function drawRoute(code, dateFilter) {{
  const techInfo = TECHS.find(t => t.code === code);
  if (!techInfo) return;

  const techIdx = TECHS.indexOf(techInfo);
  const color = COLORS[techIdx % COLORS.length];

  let stops = SCHEDULE.filter(s => s.tech_code === code);
  if (dateFilter) stops = stops.filter(s => s.date === dateFilter);
  stops.sort((a, b) => parseInt(a.stop_order) - parseInt(b.stop_order));

  if (stops.length === 0) return;

  // Build route points: home -> stops -> home
  const points = [[techInfo.lat, techInfo.lon]];
  stops.forEach(s => {{
    const lat = parseFloat(s.lat);
    const lon = parseFloat(s.lon);
    if (lat && lon) points.push([lat, lon]);
  }});
  points.push([techInfo.lat, techInfo.lon]);

  // Draw polyline
  routeLayer = L.polyline(points, {{
    color: color, weight: 3, opacity: 0.8, dashArray: '8,6'
  }}).addTo(map);

  // Home marker
  const homeMarker = L.circleMarker([techInfo.lat, techInfo.lon], {{
    radius: 10, fillColor: color, color: '#fff', weight: 3, opacity: 1, fillOpacity: 0.9
  }}).addTo(map);
  homeMarker.bindTooltip('HOME: ' + techInfo.name, {{ permanent: false, direction: 'top' }});
  stopMarkers.push(homeMarker);

  // Numbered stop markers (using per-day stop_order)
  stops.forEach((s, idx) => {{
    const lat = parseFloat(s.lat);
    const lon = parseFloat(s.lon);
    if (!lat || !lon) return;

    const stopNum = parseInt(s.stop_order) || (idx + 1);
    const marker = L.marker([lat, lon], {{
      icon: L.divIcon({{
        className: '',
        html: `<div style="
          background:${{color}}; color:#fff; width:22px; height:22px;
          border-radius:50%; display:flex; align-items:center; justify-content:center;
          font-size:11px; font-weight:700; border:2px solid #fff;
          font-family:'SF Mono','Fira Code',monospace;
        ">${{stopNum}}</div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11],
      }})
    }}).addTo(map);

    marker.bindPopup(`
      <div style="font-family:sans-serif;min-width:160px;">
        <b>Stop #${{stopNum}}</b><br>
        ${{s.customer}}<br>
        ZIP: ${{s.zip_code}}<br>
        Date: ${{s.date || '—'}} ${{s.day || ''}}<br>
        Window: ${{s.time_window || '—'}}<br>
        Arrive: ${{s.arrive_time_display}}<br>
        Drive: ${{s.leg_miles}} mi (${{s.leg_minutes}} min)
      </div>
    `);
    stopMarkers.push(marker);
  }});

  map.fitBounds(routeLayer.getBounds().pad(0.15));
}}

// ── JOB TABLE ──
function buildJobTable(code) {{
  const techInfo = TECHS.find(t => t.code === code);
  if (!techInfo) return;

  const allStops = SCHEDULE.filter(s => s.tech_code === code);
  const dates = [...new Set(allStops.map(j => j.date))].sort((a, b) => {{
    const pa = a.split('/').map(Number), pb = b.split('/').map(Number);
    return (pa[0]*100+pa[1]) - (pb[0]*100+pb[1]);
  }});

  // Date tab buttons
  const dateTabs = dates.map(d => {{
    const cnt = allStops.filter(s => s.date === d).length;
    const active = d === selectedDate ? 'background:#1D9E75;color:#fff;border-color:#1D9E75;' : '';
    return `<button onclick="switchDate('${{d}}')" style="
      padding:3px 10px;border:1px solid #444;background:transparent;color:#888;
      font-size:11px;border-radius:4px;cursor:pointer;${{active}}
    ">${{d}} (${{cnt}})</button>`;
  }}).join('');

  document.getElementById('jobTableTitle').innerHTML =
    `${{techInfo.name}} (${{code}}) &nbsp; ${{dateTabs}}`;

  // Filter to selected date
  const stops = allStops
    .filter(s => s.date === selectedDate)
    .sort((a, b) => parseInt(a.stop_order) - parseInt(b.stop_order));

  const tbody = document.getElementById('jobTableBody');
  tbody.innerHTML = stops.map(s => {{
    const arriveMin = parseFloat(s.arrive_time_min) || 0;
    const isLate = arriveMin > (17 * 60);
    const stopNum = parseInt(s.stop_order) || 0;
    return `
      <tr class="${{isLate ? 'late' : ''}}">
        <td>${{stopNum}}</td>
        <td>${{s.customer || '—'}}</td>
        <td>${{s.zip_code || '—'}}</td>
        <td>${{s.date || '—'}} ${{s.day || ''}}</td>
        <td>${{s.time_window || '—'}}</td>
        <td>${{s.arrive_time_display || '—'}}</td>
        <td>${{parseFloat(s.leg_miles || 0).toFixed(1)}}</td>
        <td>${{Math.round(parseFloat(s.leg_minutes || 0))}} min</td>
      </tr>
    `;
  }}).join('');

  document.getElementById('jobTableWrap').classList.add('visible');
}}

function switchDate(date) {{
  selectedDate = date;
  clearRoute();
  drawRoute(selectedTech, selectedDate);
  buildJobTable(selectedTech);
}}

// ── VIEW TOGGLE ──
function setView(view) {{
  currentView = view;
  document.getElementById('btnOriginal').classList.toggle('active', view === 'original');
  document.getElementById('btnOptimized').classList.toggle('active', view === 'optimized');
  // Rebuild tech list with appropriate data view
  buildTechList();
}}

// ── BOOT ──
init();
</script>
</body>
</html>"""


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, dashboard_html="", **kwargs):
        self.dashboard_html = dashboard_html
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(self.dashboard_html.encode())))
            self.end_headers()
            self.wfile.write(self.dashboard_html.encode())
        elif self.path == "/api/data":
            data = load_dashboard_data()
            payload = json.dumps(data).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def start_dashboard():
    data = load_dashboard_data()
    html = build_html(data)
    handler = lambda *args, **kwargs: DashboardHandler(
        *args, dashboard_html=html, **kwargs)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Dashboard running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")


if __name__ == "__main__":
    start_dashboard()
