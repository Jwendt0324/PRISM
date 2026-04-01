---
description: Operate, deploy, troubleshoot, and extend the automated parts pricing agent for appliance repair clients using [Field Service Platform] ServiceDesk
category: client-work
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
canon_compliance: N/A (operational automation SOP, not content production)
triangles: DDD
triangles_served: [DDD]
human_gates: yes
canon_sources: []
---

# Parts Agent Operations SOP

## Purpose

Document the full lifecycle of the automated parts pricing agent — from how it works, to how to deploy it, run it, troubleshoot it, and add new clients — so anyone on the team can operate it without tribal knowledge.

## When to Use

- Deploying the parts agent to a new Vultr server or client environment
- Adding a new appliance repair client to the agent
- Troubleshooting a failed run (pricing errors, connection failures, CSV import issues)
- Understanding the end-to-end pipeline before making code changes
- Onboarding someone (e.g., [Your Content Specialist]) to manage the agent day-to-day
- Reviewing agent status or investigating a missed pricing cycle

## Related SOPs

- **`sops/client-work/field-service-parts-inquiry.md`** — The manual process this agent automates. Read that SOP first to understand what the agent replaces.
- **`sops/business-ops/api-security-and-access.md`** — Credential management for [Parts Distributor], SmartSheet, [Field Service Platform].

---

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────┐     ┌───────────────┐
│  [Field Service Platform]    │     │  Binary      │     │  Warehouse Check  │     │  [Parts Distributor]       │
│  PrtsPrcs    │────▶│  Parser      │────▶│  (PartsHotList)   │────▶│  Lookup        │
│  (RDP pull)  │     │              │     │                   │     │  ([parts-distributor-url.com]) │
└─────────────┘     └──────────────┘     └───────────────────┘     └───────┬───────┘
                                                                           │
                    ┌──────────────┐     ┌───────────────────┐             │
                    │  CSV Export   │◀────│  Markup Engine    │◀────────────┘
                    │  (Shift+F8)  │     │  (tiered pricing) │
                    └──────┬───────┘     └───────────────────┘
                           │                      │
                    ┌──────▼───────┐     ┌────────▼──────────┐
                    │  Push CSV to │     │  SmartSheet        │
                    │  Server via  │     │  Warranty Submit   │
                    │  RDP/SCP     │     │  (OOS parts only)  │
                    └──────────────┘     └───────────────────┘
```

**Pipeline flow:** PrtsPrcs binary → Parse → Warehouse Check → [Parts Distributor] Lookup → Vendor Routing → Markup → SmartSheet (OOS) → CSV Export → Push to Server

---

## Key Files & Locations

| Item | Path |
|------|------|
| **v3 source (active)** | `~/Documents/parts-agent-v3/` |
| Entry point | `~/Documents/parts-agent-v3/run.py` |
| Pipeline orchestrator | `~/Documents/parts-agent-v3/src/pipeline.py` |
| Binary parser | `~/Documents/parts-agent-v3/src/binary_parser.py` |
| [Parts Distributor] client | `~/Documents/parts-agent-v3/src/distributor_client.py` |
| Warehouse checker | `~/Documents/parts-agent-v3/src/warehouse_checker.py` |
| Markup engine | `~/Documents/parts-agent-v3/src/markup.py` |
| SmartSheet client | `~/Documents/parts-agent-v3/src/smartsheet_client.py` |
| CSV exporter | `~/Documents/parts-agent-v3/src/csv_exporter.py` |
| RDP/file transfer | `~/Documents/parts-agent-v3/src/rdp_transfer.py` |
| Session manager | `~/Documents/parts-agent-v3/src/session_manager.py` |
| Rate limiter | `~/Documents/parts-agent-v3/src/rate_limiter.py` |
| Resume engine | `~/Documents/parts-agent-v3/src/resume_engine.py` |
| RSS Key handler | `~/Documents/parts-agent-v3/src/rss_key.py` |
| Dashboard (Flask) | `~/Documents/parts-agent-v3/src/dashboard.py` |
| Client config | `~/Documents/parts-agent-v3/config/clients.json` |
| Agent config | `~/Documents/parts-agent-v3/config/config.json` |
| [Parts Distributor] config | `~/Documents/parts-agent-v3/config/distributor.json` |
| Tests (17 files) | `~/Documents/parts-agent-v3/tests/` |
| Vultr deploy package | `~/Documents/parts-agent-vultr-deploy/` |
| [Your Content Specialist]'s setup guide | `~/Desktop/Parts Agent - Vultr Setup Guide for [Your Content Specialist].docx` |
| v2 reference (legacy) | `~/Documents/parts-agent/` |

---

## Client Configuration

### [Client — Appliance Repair] (Active)

| Parameter | Value |
|-----------|-------|
| [Field Service Platform] host | `[client-id].[field-service-hosting.com]` |
| RDP user | `[Your Name]` |
| PrtsPrcs remote path | `C:\SD\NetData\PrtsPrcs` |
| CSV import dir | `C:\SD\Import` |
| RSS Key business_id | `1696` |
| [Parts Distributor] account | `[account-number-1]` |
| [Parts Distributor] password | **BLOCKED** — waiting on [Client Contact] |
| Warehouse file | `PartsHotList.csv` |
| SmartSheet API token | **BLOCKED** — waiting on [Client Contact] |
| Vendor routing | In-stock = MA, Warehouse = [Client-ID], OOS = WCI |
| Default hold_loc | OR |
| SmartSheet static: phone | 832-804-8980 |
| SmartSheet static: address | 32702 1-A Creek Road, Magnolia TX |
| SmartSheet static: email | parts@[client-id]service.com |

### [Client — Appliance Repair] (Configured, Not Active)

| Parameter | Value |
|-----------|-------|
| [Parts Distributor] account | `[account-number-2]` |
| Vendor code | `SL` |
| All other fields | Empty — needs [Field Service Platform] host, RSS Key, etc. |

---

## Process

### Phase 1: Understand the Pipeline (Reference)

The agent automates 22 of 26 steps from the manual parts inquiry process (`field-service-parts-inquiry.md`). Here is what each module does:

1. **`rdp_transfer.py`** connects to the [Field Service Platform] server via RDP/SCP and downloads the `PrtsPrcs` binary file to local storage.
2. **`binary_parser.py`** parses the [Field Service Platform] PrtsPrcs binary format into structured part records (ticket number, part number, quantity, current vendor, cost, etc.).
3. **`warehouse_checker.py`** checks each part against the local `PartsHotList.csv` file. If found with qty > 0, the part is flagged as warehouse-available with its bin location.
4. **`distributor_client.py`** logs into [parts-distributor-url.com] using `session_manager.py` for cookie/session persistence and `rate_limiter.py` to avoid getting blocked. Looks up each non-warehouse part for price and availability.
5. **`pipeline.py`** applies vendor routing logic (see below) and calls the **`markup.py`** engine for tiered sell-price calculation.
6. **`smartsheet_client.py`** submits warranty requests for OOS parts to SmartSheet via API, populating all 12+ required fields.
7. **`csv_exporter.py`** generates a [Field Service Platform]-compatible CSV for Shift+F8 bulk import (columns: part_number, vendor, cost, sell_for, hold_loc, etc.).
8. **`rdp_transfer.py`** pushes the CSV back to the server at `C:\SD\Import`.
9. **`resume_engine.py`** handles interrupted runs — if the agent crashes mid-lookup, it picks up where it left off on the next cycle.
10. **`dashboard.py`** serves a Flask web dashboard on port 5050 showing run history, part counts, error rates, and client status.

### Phase 2: Vendor Routing Logic

Apply this decision tree for each part (derived from [Client Contact]'s employee training video):

1. **Part found in warehouse** (PartsHotList, qty > 0):
   - `vendor` = [Client-ID] (or client vendor code)
   - `hold_loc` = bin location from PartsHotList
   - `cost` = warehouse cost (if tracked) or $0
   - Skip [Parts Distributor] lookup for this part

2. **[Parts Distributor] in stock** (status = available):
   - `vendor` = MA
   - `cost` = [Parts Distributor] wholesale price
   - `sell_for` = markup(cost) using tiered markup table
   - `hold_loc` = OR (office received)

3. **[Parts Distributor] substituted part** ([Parts Distributor] returns a different part number):
   - `vendor` = MA
   - `new_part_number` = [Parts Distributor]'s substituted number (write back to record)
   - `cost` = substituted part's price
   - `sell_for` = markup(cost)
   - `hold_loc` = OR

4. **[Parts Distributor] OOS or not found:**
   - `vendor` = WCI (or OEM-specific code)
   - Flag for SmartSheet warranty submission
   - `cost` = $0 (to be filled after warranty approval)
   - `sell_for` = $0

### Phase 3: Deploy to Vultr

11. **Provision a Vultr Windows Server 2022 instance** ($56/month plan).
12. **RDP into the server** and create `C:\HRIAutomation\parts-agent\`.
13. **Copy the deploy package** from `~/Documents/parts-agent-vultr-deploy/` to the server (drag-drop via RDP or SCP).
14. **Install Python 3.11+** on the server if not already present.
15. **Run `pip install -r requirements.txt`** inside the deploy directory.
16. **Copy `config/clients.json`** with real credentials ([Parts Distributor] password, SmartSheet token) — **never commit credentials to git**.
17. **Test the agent manually:** `python run.py --client [client-id] --dry-run` to verify connectivity and parsing without writing CSV.
18. **Run a live test:** `python run.py --client [client-id]` and verify the output CSV is correct.
19. **Set up Windows Task Scheduler** to run `python C:\HRIAutomation\parts-agent\run.py --client [client-id]` every 4 hours.
20. **Start the dashboard:** `python -m src.dashboard` — verify accessible on port 5050.

### Phase 4: Add a New Client

21. **Add a new JSON block** to `config/clients.json` using the existing `[client-id]` block as a template.
22. **Fill in all required fields:** [Field Service Platform] host, RDP credentials, RSS Key, [Parts Distributor] account, vendor routing codes, SmartSheet static fields.
23. **Create the client's `PartsHotList.csv`** (or set `warehouse_parts_file` to empty if no local warehouse).
24. **Test with dry-run:** `python run.py --client <new_client_key> --dry-run`.
25. **Add a Task Scheduler entry** for the new client on the Vultr server.
26. **Update this SOP** with the new client's configuration table.

### Phase 5: Daily Operations

27. **Check the dashboard** at `http://<vultr-ip>:5050` to verify runs are completing.
28. **Review the CSV output** before triggering Shift+F8 import in [Field Service Platform] (human gate).
29. **Check SmartSheet submissions** for parts that need manual data fill (customer name, model#, serial# are sometimes missing from tickets).
30. **Monitor logs** at `C:\HRIAutomation\parts-agent\logs\` for errors — common ones are [Parts Distributor] session expiry, RDP connection timeout, and malformed PrtsPrcs records.

---

## SmartSheet Warranty Fields Reference

All 12+ fields submitted for OOS parts:

| Field | Source | Notes |
|-------|--------|-------|
| servicer_number | `clients.json` → smartsheet.static_fields | [Client-ID] = 1696 |
| servicer_name | `clients.json` → smartsheet.static_fields | [Client — Appliance Repair] |
| email | `clients.json` → smartsheet.static_fields | parts@[client-id]service.com |
| customer_name | PrtsPrcs record | **Often missing — human gate** |
| model_number | PrtsPrcs record | **May need human verification** |
| serial_number | PrtsPrcs record | **May need human verification** |
| purchase_date | PrtsPrcs record | Must be within warranty period |
| dispatch_number | PrtsPrcs record | Ticket number |
| diagnosis | PrtsPrcs record (tech notes) | Complaint/diagnosis field |
| part_number | Pipeline output | The OOS part |
| quantity | PrtsPrcs record | Usually 1 |
| recipient_name | Generated | Format: `[Client-ID]-{ticket_number}` |
| phone | `clients.json` → smartsheet.static_fields | 832-804-8980 |
| address | `clients.json` → smartsheet.static_fields | 32702 1-A Creek Road, Magnolia TX |

---

## Quality Checks

- [ ] All 103 tests pass: `cd ~/Documents/parts-agent-v3 && python -m pytest`
- [ ] Dry-run produces valid CSV with correct columns and no blank vendor/cost fields
- [ ] Vendor routing matches the decision tree (warehouse > [Parts Distributor] > WCI)
- [ ] SmartSheet submissions populate all required fields (flag missing customer_name/model/serial for human fill)
- [ ] CSV imports cleanly via Shift+F8 in [Field Service Platform] (no field misalignment)
- [ ] Dashboard loads on port 5050 and shows recent run history
- [ ] Resume engine handles interrupted runs (kill mid-run, restart, verify no duplicates)
- [ ] Rate limiter prevents [Parts Distributor] session blocks (check logs for 429/403 errors)

---

## Common Pitfalls

- **[Parts Distributor] session expiry.** Sessions time out after ~30 minutes of inactivity. The `session_manager.py` handles re-authentication, but if the [Parts Distributor] password is wrong or expired, every lookup fails silently with "not found." Check `distributor.json` credentials first.
- **PrtsPrcs binary format changes.** [Field Service Platform] updates occasionally change the binary layout. If the parser starts returning garbage data (wrong part numbers, nonsensical costs), compare the raw binary against the expected format in `test_binary_parser.py` fixtures.
- **Wrong [Parts Distributor] account.** [Client-ID] uses account `[account-number-1]`, [Client-B] uses `[account-number-2]`. If parts come back with unexpected pricing, verify `clients.json` has the right account for the client.
- **CSV column order.** [Field Service Platform]'s Shift+F8 import expects a specific column order. If someone edits `csv_exporter.py`, verify the output matches the expected import format. One misaligned column corrupts the entire import.
- **SmartSheet missing data.** The agent populates what it can from PrtsPrcs, but `customer_name`, `model_number`, and `serial_number` are frequently blank in the source data. These must be filled manually before the warranty claim is accepted.
- **RDP connection failures.** The [Field Service Platform] hosting server (`[client-id].[field-service-hosting.com]`) occasionally drops RDP connections. The `resume_engine.py` handles this, but persistent failures mean the hosting server is down — contact [Field Service Platform] support.
- **Duplicate CSV pushes.** If the agent runs twice on the same PrtsPrcs file (e.g., Task Scheduler fires while a manual run is active), the CSV will contain duplicates. The resume engine deduplicates, but verify by checking the CSV row count against expected part count.
- **[Parts Distributor] substitutions not written back.** If a [Parts Distributor] lookup returns a substituted part number, it must be written into the CSV as the new part number. If this fails, the [Field Service Platform] ticket will have a part number that doesn't match what ships.

---

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| All [Parts Distributor] lookups return "not found" | Session expired or wrong password | Check `config/distributor.json`, test login manually at [parts-distributor-url.com] |
| CSV has 0 rows | PrtsPrcs file is empty or parser failed | Check `data/` for downloaded PrtsPrcs file, run parser standalone |
| Dashboard won't start | Port 5050 in use or Flask not installed | `netstat -an | findstr 5050`, kill conflicting process |
| RDP transfer fails | [Field Service Platform] server down or creds changed | Test RDP manually, check `config/clients.json` field service platform block |
| SmartSheet returns 401 | API token expired or revoked | Get new token from [Client Contact], update `clients.json` |
| Parts show wrong prices | Markup table misconfigured | Check `src/markup.py` tiered pricing logic |
| Resume engine creates duplicates | Corrupted resume state file | Delete `data/resume_state.json` and re-run |
| Rate limiter too aggressive | [Parts Distributor] blocking requests | Increase delay in `config/config.json`, check for IP bans |

---

## Blocking Items (as of 2026-03-30)

| Blocker | Owner | Status |
|---------|-------|--------|
| [Parts Distributor] password for account [account-number-1] | [Client Contact] | Waiting — need real password to replace PLACEHOLDER |
| SmartSheet API token | [Client Contact] | Waiting — required for warranty submission automation |
| [Client — Appliance Repair] [Field Service Platform] host + credentials | [Client Contact] | Not started — need full config before activating second client |

---

## Human Gates

| Step | Gate Type (Review/Approve/Execute) | Reason |
|------|------------------------------------|--------|
| 17 — Dry-run review | Review | Verify CSV output looks correct before going live |
| 28 — Shift+F8 bulk import | Execute | Human must review CSV and trigger import in [Field Service Platform] — agent cannot press Shift+F8 |
| 29 — SmartSheet data gaps | Execute | customer_name, model#, serial# frequently missing — human must fill before manufacturer accepts warranty claim |
| [Parts Distributor] password entry | Execute | Credential must come from [Client Contact] — never hardcode in git |
| SmartSheet API token entry | Execute | Token must come from [Client Contact] — never hardcode in git |
| Part number verification (edge cases) | Review | Techs sometimes enter wrong numbers; [Parts Distributor] catches most via NOT FOUND, but edge cases need human judgment |

---

## Anti-Vandalism Checks

- **Check what already exists:** Before deploying to a new server, verify no existing parts agent instance is running for that client. Running two agents against the same PrtsPrcs file creates duplicate orders.
- **Verify internal link structure:** N/A — this is a backend automation, not content.
- **Confirm no keyword cannibalization:** N/A — not content production.
- **Preserve what's working:** Never overwrite a working `clients.json` on the server without backing it up first. Never update the binary parser without running the full test suite (`python -m pytest tests/test_binary_parser.py`).
- **Reference canonical source:** The vendor routing logic is derived from [Client Contact]'s employee training video. Any changes to routing must be approved by [Client Contact] or validated against the video.
- **SOP-specific: Credential safety.** Never commit real passwords, API tokens, or [Parts Distributor] credentials to git. The `clients.json` on the deploy server has real credentials; the repo version has PLACEHOLDERs. Verify this before every push.
- **SOP-specific: Test before deploy.** Every code change must pass all 103+ tests before deploying to the Vultr server. Run `python -m pytest` from `~/Documents/parts-agent-v3/` and verify 0 failures.

---

## Canon Compliance

- **Content Factory stage(s):** N/A — this is an operational automation SOP, not content production. The parts agent is a client service automation tool.
- **9 Triangles served:** **DDD** (Do-Do-Do) — this SOP serves operational execution for [Client — Appliance Repair]. The agent automates repetitive doing-work (parts pricing) so the team can focus on higher-value tasks.
- **Canon documents (source of truth):** None directly — this is a client-specific operational procedure outside the [Methodology Partner] content canon. The manual process is documented in `sops/client-work/field-service-parts-inquiry.md`.
- **Last canon audit:** 2026-03-30

---

## Current Status (2026-03-30)

| Metric | Value |
|--------|-------|
| Workflow coverage | 85% (22/26 steps automated) |
| Tests passing | 103 |
| Source modules | 15 (in `src/`) |
| Test files | 17 (in `tests/`) |
| Vultr deploy package | Ready at `~/Documents/parts-agent-vultr-deploy/` |
| Dashboard | Flask on port 5050 |
| Schedule target | Every 4 hours via Windows Task Scheduler |
| Server cost | $56/month (Vultr Windows Server 2022) |
| Blocking | [Parts Distributor] password + SmartSheet API token from [Client Contact] |

---

## Learnings Log

- **2026-03-30:** Initial SOP created. v3 codebase has 16 modules and 103 passing tests. Vultr deploy package ready but blocked on two credentials from [Client Contact]. The manual SOP (`field-service-parts-inquiry.md`) documents the human process this agent replaces — read it for full context on what each automated step is doing.
- **2026-03-30:** Address discrepancy noted: SmartSheet config says "32702 1-A Creek Road" but manual SOP says "32702 Walnut Creek Road." Verify correct address with [Client Contact] before first live SmartSheet submission.
