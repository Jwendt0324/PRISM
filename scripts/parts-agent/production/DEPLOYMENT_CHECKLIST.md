# D3S Parts Agent - Deployment Checklist

## Generated Files

### Main Deployment Scripts
- [x] `deploy_files.ps1` (40 KB) - PowerShell script for files 1-8
- [x] `deploy_remaining.py` (2.1 KB) - Python helper for files 9-15
- [x] `DEPLOYMENT_README.md` (6.5 KB) - Complete deployment guide
- [x] `DEPLOYMENT_SUMMARY.md` (4.4 KB) - File summary and options

### Source Files Included in `deploy_files.ps1`

**Configuration**
- [x] config/config.json (32 lines)
- [x] config/distributors/marcone.json (71 lines)

**Python Modules**
- [x] src/__init__.py (1 line - empty)
- [x] src/binary_parser.py (303 lines)
- [x] src/scraper.py (211 lines)
- [x] src/session_manager.py (212 lines)
- [x] src/rate_limiter.py (120 lines)
- [x] src/resume_engine.py (123 lines)

### Files to Copy via `deploy_remaining.py`

**Large Python Modules**
- [ ] src/agent.py (348 lines) - Source verified
- [ ] src/dashboard.py (260 lines) - Source verified
- [ ] src/rss_key.py (160 lines) - Source verified
- [ ] src/rdp_fetch.py (238 lines) - Source verified

**Entry Points**
- [ ] run.py (144 lines) - Source verified
- [ ] fetch_and_run.py (189 lines) - Source verified

**Static Assets**
- [ ] static/index.html (675 lines) - Source verified

## Directory Structure to be Created

```
C:\HRIAutomation\parts-agent\
├── config\
│   ├── config.json                    ← Edit credentials here
│   └── distributors\
│       └── marcone.json
├── src\
│   ├── __init__.py
│   ├── binary_parser.py
│   ├── scraper.py
│   ├── session_manager.py
│   ├── rate_limiter.py
│   ├── resume_engine.py
│   ├── agent.py
│   ├── dashboard.py
│   ├── rss_key.py
│   └── rdp_fetch.py
├── static\
│   └── index.html
├── data\
│   ├── input\
│   ├── output\
│   ├── session\
│   └── archive\
├── logs\
│   ├── runs\
│   └── errors\
├── run.py
└── fetch_and_run.py
```

## Pre-Deployment Checklist

- [ ] Windows Server access confirmed
- [ ] `C:\HRIAutomation\` directory exists or can be created
- [ ] PowerShell execution policy allows scripts (`RemoteSigned` or higher)
- [ ] Python 3.9+ installed and in PATH
- [ ] Network access to internet (for Marcone and dependencies)

## Deployment Execution Steps

### Phase 1: Run PowerShell Script

- [ ] Copy `deploy_files.ps1` to Windows server
- [ ] Open PowerShell as Administrator
- [ ] Run: `powershell -ExecutionPolicy Bypass -File deploy_files.ps1`
- [ ] Verify no errors in output
- [ ] Verify directory structure created:
  ```powershell
  Get-ChildItem C:\HRIAutomation\parts-agent -Recurse
  ```

### Phase 2: Copy Large Files

- [ ] Ensure Python 3.6+ available on deployment server
- [ ] Copy `deploy_remaining.py` to Windows server
- [ ] Run: `python deploy_remaining.py C:\HRIAutomation\parts-agent`
- [ ] Verify all 7 files copied successfully
- [ ] Total file count should be ~25 (including __pycache__)

### Phase 3: Configure Credentials

- [ ] Edit `C:\HRIAutomation\parts-agent\config\config.json`
- [ ] Update `username` and `password` for Marcone
- [ ] Update `marcone_accounts.d3s` credentials
- [ ] Update `rossware` host/username/password for RDP
- [ ] Update `rss_key` username/password
- [ ] Save file (UTF-8 encoding required)

### Phase 4: Install Dependencies

- [ ] Run: `pip install playwright`
- [ ] Run: `python -m playwright install chromium`
- [ ] Verify installation: `python -c "from playwright.sync_api import sync_playwright; print('OK')"`

### Phase 5: Verify Installation

- [ ] Test imports:
  ```powershell
  python -c "from src.agent import ProductionAgent; print('Imports OK')"
  ```
- [ ] Test dry-run:
  ```powershell
  python run.py --test 5 --dry-run
  ```
- [ ] Test dashboard:
  ```powershell
  python run.py --dashboard-only
  ```
  Then navigate to: `http://localhost:8050`

## Post-Deployment Checklist

- [ ] All 15 files present in correct locations
- [ ] config.json updated with production credentials
- [ ] Python dependencies installed
- [ ] Dry-run executes without errors
- [ ] Dashboard accessible at localhost:8050
- [ ] Logs directory exists and is writable
- [ ] Data directory exists and is writable

## Production Readiness

- [ ] Credentials are production-ready (not test accounts)
- [ ] File permissions set appropriately (if multiple users)
- [ ] Backup of config.json created
- [ ] SSL/TLS certificates configured (if needed)
- [ ] Firewall rules allow RDP and HTTPS traffic
- [ ] Administrator notified of deployment completion

## File Size Reference

For verification:
```
deploy_files.ps1              40 KB  (contains files 1-8)
deploy_remaining.py          2.1 KB  (copies files 9-15)
DEPLOYMENT_README.md         6.5 KB  (guide)
DEPLOYMENT_SUMMARY.md        4.4 KB  (summary)
```

## Source File Locations (For Reference)

All source files are located at:
```
/sessions/kind-practical-sagan/mnt/scripts/parts-agent/production/
```

Structure in source:
```
production/
├── config/
│   ├── config.json
│   └── distributors/marcone.json
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── binary_parser.py
│   ├── dashboard.py
│   ├── rate_limiter.py
│   ├── rdp_fetch.py
│   ├── resume_engine.py
│   ├── rss_key.py
│   ├── scraper.py
│   └── session_manager.py
├── static/
│   └── index.html
├── run.py
├── fetch_and_run.py
├── deploy_files.ps1
├── deploy_remaining.py
└── [documentation files]
```

## Troubleshooting Reference

| Issue | Check | Solution |
|-------|-------|----------|
| PowerShell won't run | Execution policy | `Set-ExecutionPolicy RemoteSigned` |
| Python not found | PATH variable | Install Python or add to PATH |
| Playwright fails | Browser installed | `python -m playwright install chromium` |
| Marcone login fails | Credentials | Verify username/password in config.json |
| RDP connection fails | Network access | Check firewall, test `ping d3s.rosswarehosting.com` |
| Files not copied | Permissions | Ensure write access to C:\HRIAutomation\ |

## Next Steps After Deployment

1. Run initial test: `python run.py --test 10`
2. Monitor logs in `logs/runs/` and `logs/errors/`
3. Configure Windows Task Scheduler for periodic runs
4. Set up email notifications for completion
5. Monitor dashboard at `http://localhost:8050` during runs

---

**Deployment Package Version**: 1.0
**Date Prepared**: March 20, 2026
**Status**: Ready for Deployment
