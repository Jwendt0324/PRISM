"""
Scraper — Distributor-specific search and scraping logic.

Reads all selectors and behavior from the distributor JSON config.
Contains no hardcoded selectors — everything is config-driven.

Ported directly from parts-agent v2 (tested 10/10 on real parts).
"""

import time
from datetime import datetime

from playwright.sync_api import TimeoutError as PlaywrightTimeout

from .rate_limiter import RateLimitDetected


class Scraper:
    """Searches a distributor site and scrapes product data."""

    def __init__(self, distributor, log_fn):
        """
        Args:
            distributor: dict from config/distributors/<name>.json
            log_fn: callable for logging
        """
        self.dist = distributor
        self.log = log_fn

    def search_part(self, page, part_number):
        """Search for a single part number and return scraped results.

        Args:
            page: authenticated Playwright page object.
            part_number: string to search.

        Returns:
            dict with keys: marcone_name, marcone_part_number, price,
            availability, status, lookup_timestamp
        """
        result = {
            "marcone_name": "",
            "marcone_part_number": "",
            "price": "",
            "availability": "",
            "status": "NOT FOUND",
            "lookup_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        search_cfg = self.dist["search"]
        search_input = page.locator(search_cfg["input_selector"])

        if search_input.count() == 0:
            raise RuntimeError(
                f"Search field '{search_cfg['input_selector']}' not found. URL: {page.url}"
            )

        # Clear and fill the search field
        search_input.first.click()
        search_input.first.fill("")
        search_input.first.fill(part_number)
        time.sleep(0.5)

        # Submit the search
        submit_sel = search_cfg["submit_selector"]
        go_button = page.locator(submit_sel)
        if go_button.count() > 0:
            go_button.first.click()
        elif search_cfg.get("js_fallback"):
            page.evaluate(search_cfg["js_fallback"])
        else:
            search_input.first.press("Enter")

        # Wait for results
        wait_time = search_cfg.get("wait_after_submit_seconds", 3)
        time.sleep(wait_time)
        page.wait_for_load_state("domcontentloaded")

        # Check for rate limiting
        self._check_rate_limit(page)

        # Check for no results
        if self._check_no_results(page):
            result["status"] = "NOT FOUND"
            return result

        # Wait for AJAX content
        time.sleep(2)

        # Detect page type and scrape accordingly
        results_cfg = self.dist["results"]
        detail_cfg = results_cfg.get("detail_page", {})
        search_results_cfg = results_cfg.get("search_page", {})

        if detail_cfg.get("url_indicator") and detail_cfg["url_indicator"] in page.url:
            self._scrape_detail_page(page, detail_cfg, result)
        elif search_results_cfg.get("url_indicator") and search_results_cfg["url_indicator"] in page.url:
            self._scrape_search_page(page, search_results_cfg, result)
        else:
            result["status"] = "FOUND - UNKNOWN PAGE TYPE"
            self.log(f"  Unknown page type for URL: {page.url}")

        return result

    def _scrape_detail_page(self, page, cfg, result):
        """Scrape a product detail page (exact match)."""
        selectors = cfg.get("selectors", {})

        name_el = page.locator(selectors["name"]) if selectors.get("name") else None
        if name_el and name_el.count() > 0:
            result["marcone_name"] = name_el.first.inner_text().strip()

        price_el = page.locator(selectors["price"]) if selectors.get("price") else None
        if price_el and price_el.count() > 0:
            result["price"] = price_el.first.inner_text().strip()

        avail_el = page.locator(selectors["availability"]) if selectors.get("availability") else None
        if avail_el and avail_el.count() > 0:
            result["availability"] = avail_el.first.inner_text().strip()

        # Extract distributor part number from URL if present
        url = page.url
        if "Part=" in url:
            part_param = url.split("Part=")[1].split("&")[0]
            result["marcone_part_number"] = part_param

        if result["marcone_name"] or result["price"]:
            result["status"] = "FOUND"
        else:
            result["status"] = "FOUND - COULD NOT PARSE"

    def _scrape_search_page(self, page, cfg, result):
        """Scrape a search results page (multiple matches — take first)."""
        container_sel = cfg.get("item_container", "")
        first_item = page.locator(container_sel).first
        selectors = cfg.get("selectors", {})

        # Part link / number
        part_link_el = first_item.locator(selectors["part_link"]) if selectors.get("part_link") else None
        marcone_part = ""
        if part_link_el and part_link_el.count() > 0:
            marcone_part = part_link_el.first.inner_text().strip()
        result["marcone_part_number"] = marcone_part

        # Brand
        brand_el = first_item.locator(selectors["brand"]) if selectors.get("brand") else None
        brand = brand_el.first.inner_text().strip() if brand_el and brand_el.count() > 0 else ""

        # Description
        desc_el = first_item.locator(selectors["description"]) if selectors.get("description") else None
        desc_parts = []
        if desc_el:
            for i in range(desc_el.count()):
                text = desc_el.nth(i).inner_text().strip()
                if text and text != brand:
                    desc_parts.append(text)
        description = " ".join(desc_parts)

        # Build name from format template or fallback
        name_fmt = cfg.get("name_format", "{brand} - {part_link} - {description}")
        result["marcone_name"] = name_fmt.format(
            brand=brand, part_link=marcone_part, description=description
        ).strip(" -")

        # Price
        price_el = first_item.locator(selectors["price"]) if selectors.get("price") else None
        if price_el and price_el.count() > 0:
            result["price"] = price_el.first.inner_text().strip()

        # Availability
        avail_el = first_item.locator(selectors["availability"]) if selectors.get("availability") else None
        if avail_el and avail_el.count() > 0:
            result["availability"] = avail_el.first.inner_text().strip()

        if result["marcone_name"] or result["price"]:
            result["status"] = "FOUND"
        else:
            result["status"] = "FOUND - COULD NOT PARSE"

    def _check_no_results(self, page):
        """Check if the page shows a 'no results' indicator."""
        indicators = self.dist["results"].get("no_results_indicators", [])
        for indicator in indicators:
            try:
                el = page.locator(indicator)
                if el.count() > 0:
                    for i in range(el.count()):
                        if el.nth(i).is_visible():
                            return True
            except Exception:
                continue
        return False

    def _check_rate_limit(self, page):
        """Detect rate limiting and raise if found."""
        rate_limit_signals = [
            "too many requests",
            "rate limit",
            "429",
            "please try again later",
        ]
        try:
            body_text = page.locator("body").first.inner_text()[:2000].lower()
            for signal in rate_limit_signals:
                if signal in body_text:
                    raise RateLimitDetected(f"Rate limit detected: '{signal}' found on page")
        except RateLimitDetected:
            raise
        except Exception:
            pass
