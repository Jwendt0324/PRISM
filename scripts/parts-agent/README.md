# Parts Lookup Agent v2

Automated batch processing engine that looks up appliance part numbers on distributor websites (currently [Parts Distributor]), scrapes pricing and availability, and writes ServiceDesk-compatible CSV output.

Handles 500+ parts per run with zero human interaction. Logs in once, reuses the session, retries failures with exponential backoff, and can resume crashed runs from where they left off.

## Quick start

```bash
cd ~/Documents/Claude/PRISM/scripts/parts-agent

# 1. Drop a CSV into data/input/ (needs a "part_number" column at minimum)
# 2. Run:
python3 run.py

# Other modes:
python3 run.py --headless       # No browser window
python3 run.py --resume         # Auto-resume a crashed run
python3 run.py --dry-run        # Preview what would be processed
```

## Project structure

```
parts-agent/
├── config/
│   ├── config.json              # Credentials and run settings
│   ├── config.example.json      # Template (no real credentials)
│   └── distributors/
│       └── marcone.json         # All [Parts Distributor]-specific selectors and URLs
├── data/
│   ├── input/                   # Drop CSV files here to be processed
│   ├── output/                  # Results land here (timestamped)
│   ├── archive/                 # Processed inputs move here automatically
│   └── session/                 # Saved login cookies (auto-managed)
├── logs/
│   ├── runs/                    # One log file per run
│   └── errors/                  # Failed lookups
├── src/
│   ├── agent.py                 # Main batch processing orchestrator
│   ├── scraper.py               # Distributor-specific scraping logic
│   ├── session_manager.py       # Cookie persistence (login once, reuse)
│   ├── csv_handler.py           # Input/output/archive/dedup
│   ├── rate_limiter.py          # Delays, backoff, error thresholds
│   └── resume_engine.py         # Crash recovery
├── run.py                       # Entry point
├── parts_agent_v1.py            # Backup of original working script
└── requirements.txt             # Python dependencies
```

## How to add parts to look up

Create a CSV file and drop it into `data/input/`. The only required column is `part_number`:

```csv
part_number
WP3363394
316489402
WP8544771
```

You can include optional columns and the agent will pass them through to output:

```csv
part_number,description,job_number
WP3363394,Washer Pump,JOB-1001
316489402,Oven Igniter,JOB-1002
```

You can drop multiple CSV files at once. The agent processes all of them and deduplicates part numbers (each unique part is searched once).

## Reading the output

Results are written to `data/output/results_[timestamp].csv`:

| Column | Description |
|---|---|
| part_number | What you searched |
| marcone_part_number | [Parts Distributor]'s internal part number |
| marcone_name | Product name on [Parts Distributor] |
| wholesale_price | Your dealer cost |
| availability | Stock status and quantity |
| vendor | "MC" (for ServiceDesk import) |
| lookup_timestamp | When it was looked up |
| status | FOUND / NOT FOUND / ERROR |
| original_description | Passed through from your input |
| original_job_number | Passed through from your input |

## Updating credentials

Edit `config/config.json`:

```json
{
  "distributor": "marcone",
  "username": "YOUR_ACCOUNT_NUMBER",
  "password": "YOUR_PASSWORD"
}
```

## Resuming a crashed run

If the agent crashes mid-batch, your progress is saved automatically. Next time you run:

```bash
python3 run.py              # Will prompt: "Resume? (y/n)"
python3 run.py --resume     # Auto-resumes without prompting
```

Completed parts are skipped. The agent picks up at the next unfinished part.

## Adding a new distributor

The system is distributor-agnostic. [Parts Distributor] is just the first one. To add another:

1. Create `config/distributors/newdistributor.json` with the site's selectors, URLs, and timeouts (use `marcone.json` as a template)
2. Update `config/config.json`: set `"distributor": "newdistributor"`
3. If the new site's page structure is very different, extend `src/scraper.py`

## Configuration reference

`config/config.json` settings:

| Setting | Default | What it does |
|---|---|---|
| distributor | marcone | Which distributor config to load |
| headless | false | Run without visible browser |
| [google-doc-id] | 2 | Pause between searches |
| max_retries | 4 | Retry attempts per failed part |
| error_abort_threshold_pct | 50 | Abort run if error rate exceeds this |
| rate_limit_pause_minutes | 5 | How long to pause if rate limited |
| session_reuse | true | Reuse saved login cookies |

## Troubleshooting

**"No CSV files found in data/input/"**
Drop a CSV file with a `part_number` column into `data/input/`.

**Login fails**
Check credentials in `config/config.json`. Check `logs/runs/` for the exact error.

**Search works but data is empty**
[Parts Distributor] may have changed their page layout. Inspect the page and update selectors in `config/distributors/marcone.json`.

**Run aborted — error rate too high**
Something is fundamentally broken (session expired, site down, selectors changed). Check the error log in `logs/errors/` and fix the root cause.

**Crashed mid-run**
Just re-run with `python3 run.py --resume`. Progress was saved automatically.

## Setup (one time)

```bash
pip install playwright
playwright install chromium
```
