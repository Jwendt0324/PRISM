#!/usr/bin/env python3
"""
Parts Lookup Agent for [Parts Distributor].com
Reads part numbers from parts_list.csv, searches each on [parts-distributor-url.com],
and writes pricing/availability results to parts_results.csv.
"""

import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: Playwright is not installed.")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# All paths relative to this script's directory
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
INPUT_CSV = SCRIPT_DIR / "parts_list.csv"
OUTPUT_CSV = SCRIPT_DIR / "parts_results.csv"
LOG_FILE = SCRIPT_DIR / "agent_log.txt"


def log(message):
    """Print to terminal and append to log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_config():
    """Load configuration from config.json."""
    if not CONFIG_PATH.exists():
        log("FATAL: config.json not found. Cannot continue.")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    # Validate required fields
    for field in ["distributor_url", "username", "password"]:
        if not config.get(field) or config[field].startswith("YOUR_"):
            log(f"WARNING: config.json field '{field}' is not set. Update it with real values before running against the live site.")
    return config


def load_parts_list():
    """Read part numbers from the input CSV."""
    if not INPUT_CSV.exists():
        log("FATAL: parts_list.csv not found. Cannot continue.")
        sys.exit(1)
    parts = []
    with open(INPUT_CSV, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parts.append(row)
    return parts


def init_results_csv():
    """Create or overwrite the results CSV with headers."""
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "part_number", "description", "marcone_name",
            "price", "availability", "status", "lookup_timestamp"
        ])


def write_result(part_number, description, marcone_name, price, availability, status):
    """Append one result row to the output CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            part_number, description, marcone_name,
            price, availability, status, timestamp
        ])


def login_to_distributor(page, config):
    """Navigate to [parts-distributor-url.com] login page and authenticate."""
    login_url = config.get("login_url", "https://[parts-distributor-url.com]/UserLogin")
    log(f"Navigating to login page: {login_url}")
    page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
    log(f"Page loaded: {page.title()}")

    # Use exact selectors from config (discovered by inspecting [parts-distributor-url.com])
    selectors = config.get("login_selectors", {})
    username_sel = selectors.get("username_field", "#UserName")
    password_sel = selectors.get("password_field", "#Password")
    submit_sel = selectors.get("submit_button", "#loginbtn")

    username_field = page.locator(username_sel)
    password_field = page.locator(password_sel)

    if username_field.count() > 0 and password_field.count() > 0:
        log("Found login form. Entering credentials...")
        username_field.first.fill(config["username"])
        password_field.first.fill(config["password"])

        submit_btn = page.locator(submit_sel)
        if submit_btn.count() > 0:
            submit_btn.first.click()
            # Wait for navigation away from the login page
            try:
                page.wait_for_url(lambda url: "UserLogin" not in url, timeout=15000)
            except PlaywrightTimeout:
                log("WARNING: Still on login page after 15s — credentials may be incorrect.")
                return
            time.sleep(2)
            page.wait_for_load_state("domcontentloaded")
            log(f"Login successful. Current page: {page.url}")
            # Wait for dashboard to fully load (JS, search bar, etc.)
            log("Waiting for dashboard to fully load...")
            time.sleep(3)
            try:
                page.wait_for_selector("#searchPartOrModel", timeout=10000)
                log("Dashboard ready — search field found.")
            except PlaywrightTimeout:
                log("WARNING: Search field not found after waiting. Dashboard may not have loaded fully.")
        else:
            log(f"WARNING: Could not find submit button with selector: {submit_sel}")
    else:
        log(f"WARNING: Could not find login form fields.")
        log(f"  Username selector '{username_sel}' found: {username_field.count()}")
        log(f"  Password selector '{password_sel}' found: {password_field.count()}")
        log(f"Current URL: {page.url}")
        log("The agent will continue and attempt searches — they may fail if login is required.")


def search_part(page, config, part_number):
    """Search for a single part number on [parts-distributor-url.com] and return results."""
    result = {
        "marcone_name": "",
        "price": "",
        "availability": "",
        "status": "NOT FOUND"
    }

    search_selectors = config.get("search_selectors", {})
    search_input_sel = search_selectors.get("search_input", "#searchPartOrModel")
    go_button_sel = search_selectors.get("go_button", "#mc-embedded-subscribe")
    js_function = search_selectors.get("js_search_function", "My[Parts Distributor].Seach.RunSearchPartModelList(1);")

    try:
        search_input = page.locator(search_input_sel)

        if search_input.count() == 0:
            log(f"  ERROR: Cannot find search field '{search_input_sel}' on page. URL: {page.url}")
            result["status"] = "ERROR - NO SEARCH FIELD"
            return result

        # Clear the field and type the part number
        search_input.first.click()
        search_input.first.fill("")
        search_input.first.fill(part_number)
        time.sleep(0.5)

        # Trigger search via the GO button click (Enter key doesn't work on this site)
        go_button = page.locator(go_button_sel)
        if go_button.count() > 0:
            go_button.first.click()
        else:
            # Fallback: call the JS search function directly
            log(f"  GO button not found, calling JS function directly...")
            page.evaluate(js_function)

        # Wait for results to load (the site uses AJAX, not full page reload)
        time.sleep(3)
        page.wait_for_load_state("domcontentloaded")

        log(f"  Search submitted. Current URL: {page.url}")

        # Check for "no results" indicators
        no_results = page.locator(
            "text='No results found', "
            "text='no results', "
            "text='No Result Found', "
            "text='0 results', "
            "text='did not match', "
            "#dvSearchNoResult:visible"
        )
        if no_results.count() > 0:
            visible_no_results = False
            for i in range(no_results.count()):
                if no_results.nth(i).is_visible():
                    visible_no_results = True
                    break
            if visible_no_results:
                log(f"  Part {part_number}: No results found on page.")
                result["status"] = "NOT FOUND"
                return result

        # Wait for any AJAX content to finish loading
        time.sleep(2)

        # Detect which page type we landed on
        is_detail_page = "Product/Detail" in page.url
        is_search_results = "RunSearchPartModelList" in page.url

        if is_detail_page:
            # === PRODUCT DETAIL PAGE (exact match) ===
            # Product name
            name_el = page.locator("h4.cross")
            if name_el.count() > 0:
                result["marcone_name"] = name_el.first.inner_text().strip()

            # Your Price (dealer price)
            price_el = page.locator("td.priceblock_ourprice")
            if price_el.count() > 0:
                result["price"] = price_el.first.inner_text().strip()

            # Stock status
            stock_el = page.locator("span.a-color-success")
            if stock_el.count() > 0:
                result["availability"] = stock_el.first.inner_text().strip()

        elif is_search_results:
            # === SEARCH RESULTS PAGE (multiple matches) ===
            first_item = page.locator("li.searchResult_li_items").first

            # Part number
            part_link = first_item.locator("h4.cross11 a.cursor")
            marcone_part = part_link.first.inner_text().strip() if part_link.count() > 0 else ""

            # Brand
            brand_el = first_item.locator("span.spanBrand")
            brand = brand_el.first.inner_text().strip() if brand_el.count() > 0 else ""

            # Description
            coad_spans = first_item.locator("span.coad:not(.spanBrand):not(.spanInstock)")
            desc_parts = []
            for i in range(coad_spans.count()):
                text = coad_spans.nth(i).inner_text().strip()
                if text and text != brand:
                    desc_parts.append(text)
            description = " ".join(desc_parts)

            name_parts = [p for p in [brand, marcone_part, description] if p]
            result["marcone_name"] = " - ".join(name_parts) if name_parts else ""

            # Price
            price_el = first_item.locator("span.spanPrice")
            if price_el.count() > 0:
                result["price"] = price_el.first.inner_text().strip()

            # Availability
            stock_el = first_item.locator("span.spanInstock")
            if stock_el.count() > 0:
                result["availability"] = stock_el.first.inner_text().strip()

        # If we found at least a name or price, mark as found
        if result["marcone_name"] or result["price"]:
            result["status"] = "FOUND"
        else:
            # Page loaded but we couldn't parse results — might need selector updates
            # Take a screenshot of what we see for debugging
            result["status"] = "FOUND - COULD NOT PARSE"
            log(f"  Part {part_number}: Page loaded but could not extract product details.")
            log(f"  You may need to update the CSS selectors for this site's layout.")
            log(f"  Page title: {page.title()}")

    except PlaywrightTimeout:
        log(f"  ERROR: Timeout while searching for {part_number}")
        result["status"] = "ERROR - TIMEOUT"
    except Exception as e:
        log(f"  ERROR: Unexpected error searching for {part_number}: {e}")
        result["status"] = f"ERROR - {str(e)[:100]}"

    return result


def main():
    log("=" * 60)
    log("PARTS LOOKUP AGENT STARTING")
    log("=" * 60)

    # Step 1: Load config
    config = load_config()
    log(f"Config loaded. Target site: {config['distributor_url']}")
    delay = config.get("[google-doc-id]", 3)

    # Step 2: Load parts list
    parts = load_parts_list()
    total = len(parts)
    log(f"Loaded {total} parts from parts_list.csv")

    if total == 0:
        log("No parts to look up. Exiting.")
        return

    # Step 3: Show what we're about to do
    log(f"Plan: Search {total} part numbers on {config['distributor_url']}")
    log(f"Delay between searches: {delay} seconds")
    log(f"Results will be written to: {OUTPUT_CSV}")
    log("-" * 60)

    # Step 4: Initialize results CSV
    init_results_csv()

    # Step 5: Launch browser and do the work
    found_count = 0
    not_found_count = 0
    error_count = 0

    with sync_playwright() as p:
        log("Launching browser (headed mode)...")
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Step 6: Login
        login_to_distributor(page, config)

        # Step 7: Search each part
        for i, part in enumerate(parts, 1):
            part_number = part.get("part_number", "").strip()
            description = part.get("description", "").strip()

            if not part_number:
                log(f"[{i}/{total}] Skipping empty part number row.")
                continue

            log(f"[{i}/{total}] Searching for part: {part_number} ({description})")

            result = search_part(page, config, part_number)

            # Write result immediately
            write_result(
                part_number, description,
                result["marcone_name"], result["price"],
                result["availability"], result["status"]
            )

            # Track counts
            if result["status"] == "FOUND":
                found_count += 1
                log(f"  FOUND — Name: {result['marcone_name']}, Price: {result['price']}, Availability: {result['availability']}")
            elif "ERROR" in result["status"]:
                error_count += 1
                log(f"  {result['status']}")
            else:
                not_found_count += 1
                log(f"  {result['status']}")

            # Wait before next search (skip delay on last item)
            if i < total:
                log(f"  Waiting {delay} seconds before next search...")
                time.sleep(delay)

        # Done — close browser
        log("All parts processed. Closing browser...")
        browser.close()

    # Step 8: Print summary
    log("=" * 60)
    log("AGENT RUN COMPLETE")
    log(f"  Total parts searched: {total}")
    log(f"  Found:     {found_count}")
    log(f"  Not found: {not_found_count}")
    log(f"  Errors:    {error_count}")
    log(f"  Results saved to: {OUTPUT_CSV}")
    log(f"  Full log saved to: {LOG_FILE}")
    log("=" * 60)


if __name__ == "__main__":
    main()
