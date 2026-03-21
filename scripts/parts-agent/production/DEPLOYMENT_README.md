# [Client — Appliance Repair] Parts Agent - Windows Deployment Guide

## Overview

This deployment package creates a complete parts pricing automation system at `C:\HRIAutomation\parts-agent\` on Windows Server.

## Generated Artifacts

Two main deployment scripts have been created:

### 1. `deploy_files.ps1` (PowerShell)
- Creates all 9 directories
- Deploys files 1-8 using PowerShell here-strings:
  - Configuration files (config.json, marcone.json)
  - 6 core Python modules (binary_parser, scraper, session_manager, rate_limiter, resume_engine)
  - Empty __init__.py

**Size**: ~1,100 lines
**Execution**: `powershell -ExecutionPolicy Bypass -File deploy_files.ps1`

### 2. `deploy_remaining.py` (Python)
- Copies the 7 large files that cannot fit in PowerShell script:
  - agent.py (main orchestrator)
  - dashboard.py (web server)
  - rss_key.py ([Field Service Platform] auth)
  - rdp_fetch.py (file transfer)
  - run.py (entry point)
  - fetch_and_run.py (pipeline)
  - static/index.html (dashboard UI)

**Prerequisites**: Python 3.6+
**Execution**: `python deploy_remaining.py C:\HRIAutomation\parts-agent`

## Deployment Steps

### Step 1: Run PowerShell Script

```powershell
# From the source directory containing deploy_files.ps1
powershell -ExecutionPolicy Bypass -File deploy_files.ps1
```

This creates:
- Directory structure at C:\HRIAutomation\parts-agent\
- Files 1-8 with complete content
- All configuration and base modules

### Step 2: Run Python Helper

```powershell
# From the same source directory
python deploy_remaining.py C:\HRIAutomation\parts-agent
```

This copies:
- All large Python modules (9-12)
- Entry point scripts (13-14)
- Static HTML dashboard (15)

### Step 3: Verify Installation

```powershell
# Check that all files exist
Get-ChildItem C:\HRIAutomation\parts-agent -Recurse -File | Measure-Object

# Expected: ~25 files total
# - 2 JSON config files
# - 11 Python files (.py)
# - 1 HTML file
# - Plus __pycache__ and other generated files
```

### Step 4: Configure Credentials

Edit `C:\HRIAutomation\parts-agent\config\config.json`:

```json
{
  "distributor": "marcone",
  "username": "YOUR_MARCONE_ID",        // Change this
  "password": "YOUR_MARCONE_PASSWORD",  // Change this
  "headless": true,
  ...
  "marcone_accounts": {
    "d3s": {
      "username": "YOUR_ID",
      "password": "YOUR_PASSWORD"
    },
    ...
  },
  "field_service_platform": {
    "host": "[client-server.example.com]",
    "username": "YOUR_RDP_USERNAME",    // Change this
    "password": "YOUR_RDP_PASSWORD",    // Change this
    ...
  },
  "rss_key": {
    "username": "YOUR_BUSINESS_ID",     // Change this
    "password": "YOUR_BUSINESS_PASSWORD" // Change this
  }
}
```

### Step 5: Install Python Dependencies

```powershell
cd C:\HRIAutomation\parts-agent

# Install required packages
pip install playwright

# Install browser
python -m playwright install chromium
```

### Step 6: Test the Installation

```powershell
# Test imports
python -c "from src.agent import ProductionAgent; print('OK')"

# Run with test limit
python run.py --test 5 --dry-run

# Start dashboard only
python run.py --dashboard-only
```

## Running the Agent

### Full Automated Pipeline

```powershell
python fetch_and_run.py
```

This runs:
1. RSS Key authentication (whitelists your IP)
2. RDP fetch of PrtsPrcs file
3. Parts pricing lookups on [Parts Distributor]
4. Dashboard serving results

### Individual Operations

```powershell
# Just parse PrtsPrcs, no lookups
python run.py --parse-only

# Dashboard only (no processing)
python run.py --dashboard-only --port 8050

# Test with 10 parts
python run.py --test 10

# Resume incomplete run
python run.py --resume

# Dry run (preview what would happen)
python run.py --dry-run

# Force visible browser (debugging)
python run.py --headed
```

## Output Files

After running, check these directories:

```
C:\HRIAutomation\parts-agent\data\
├── input\
│   └── PrtsPrcs          (binary file from [Field Service Platform])
├── output\
│   ├── results_YYYYMMDD_HHMMSS.csv   (results in CSV)
│   ├── results_YYYYMMDD_HHMMSS.json  (results in JSON)
│   └── parsed_parts_queue.csv        (parsed parts)
└── session\
    └── marcone_session.json          (saved cookies)

logs\
├── runs\
│   └── run_YYYYMMDD_HHMMSS.log      (execution logs)
└── errors\
    └── errors_YYYYMMDD.log          (error details)
```

## Troubleshooting

### PowerShell Execution Policy

If you get "cannot be loaded because running scripts is disabled":

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Not Found

Ensure Python 3.9+ is installed and in PATH:

```powershell
python --version
```

If not in PATH, add it or use full path:
```powershell
C:\Python39\python.exe deploy_remaining.py C:\HRIAutomation\parts-agent
```

### Playwright Browser Issues

If browser doesn't install:

```powershell
python -m playwright install chromium --with-deps
```

### Connection Issues to [Parts Distributor]

Check that:
- Internet connectivity is available
- Firewall allows HTTPS (port 443)
- Credentials in config.json are correct
- Session file is not corrupted: delete `data\session\marcone_session.json`

### RDP Connection Issues

Check that:
- [Field Service Platform] host is reachable: `ping [client-server.example.com]`
- RSS Key credentials are correct
- You have RDP client installed (comes with Windows)
- Admin access may be required for cmdkey/mstsc

## File Manifest

Total: 15 files across 3 categories

**Configuration (2 files)**
- config/config.json
- config/distributors/marcone.json

**Python Modules (11 files)**
- src/__init__.py
- src/binary_parser.py
- src/scraper.py
- src/session_manager.py
- src/rate_limiter.py
- src/resume_engine.py
- src/agent.py
- src/dashboard.py
- src/rss_key.py
- src/rdp_fetch.py
- run.py
- fetch_and_run.py

**Static Assets (1 file)**
- static/index.html

**Directories Created (8)**
- config/distributors/
- src/
- static/
- data/{input,output,session,archive}/
- logs/{runs,errors}/

## Support

For issues with:
- **Parsing**: Check `logs/runs/` for parsing errors
- **Lookups**: Check `logs/errors/` for lookup failures
- **Deployment**: See DEPLOYMENT_SUMMARY.md

## Security Notes

This deployment includes:
- Credentials stored in JSON (not encrypted)
- Session cookies saved to disk
- RDP credentials stored via cmdkey

For production use:
1. Encrypt config.json or use environment variables
2. Restrict file permissions: `icacls C:\HRIAutomation\parts-agent /grant:r "YOUR_USER:F"`
3. Consider running as service with limited account
4. Rotate credentials periodically

---

**Last Updated**: March 2026
**Version**: Production v1.0
