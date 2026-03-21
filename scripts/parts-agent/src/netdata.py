"""
NetData Intelligence — Enrichment layer using operational data from NetData.

Loads warehouse locations, quality return flags, model-based recommendations,
vendor lists, and supplier mappings from the NetData folder on Google Drive.
All lookups are in-memory after initial load — no network calls.
"""

import csv
from pathlib import Path


class NetData:
    """Loads and indexes NetData files for part enrichment."""

    def __init__(self, netdata_path, log_fn):
        """
        Args:
            netdata_path: Path to the NetData folder (string or Path).
            log_fn: callable for logging.
        """
        self.root = Path(netdata_path)
        self.log = log_fn
        self.available = self.root.exists()

        # Data stores
        self._warehouse_locations = {}   # part_number -> bin location
        self._quality_returns = {}       # part_number -> description
        self._model_recommendations = {} # model_number -> recommendation text
        self._vendors = []               # list of {abbr, name, account, mfr_account}
        self._suppliers = {}             # brand_code -> supplier_name

        if not self.available:
            self.log(f"NetData folder not found at {self.root}. Enrichment disabled.")
            return

        self.log(f"NetData folder found: {self.root}")
        self._load_all()

    def _load_all(self):
        """Load all NetData files."""
        loaded = 0
        loaded += self._load_parts_hotlist()
        loaded += self._load_wp_quality_returns()
        loaded += self._load_models_hotlist()
        loaded += self._load_vendors()
        loaded += self._load_suppliers()
        self.log(f"NetData loaded: {loaded} data sources active.")

    def _load_parts_hotlist(self):
        """Load PartsHotList.csv — part numbers to warehouse bin locations."""
        path = self.root / "PartsHotList.csv"
        if not path.exists():
            return 0

        count = 0
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Format: part_number<tab or comma>location_code
                    parts = None
                    for sep in ["\t", ","]:
                        if sep in line:
                            parts = [p.strip() for p in line.split(sep)]
                            break
                    if parts and len(parts) >= 2 and parts[0]:
                        part_num = parts[0].strip()
                        location = parts[1].strip()
                        if part_num and location:
                            self._warehouse_locations[part_num.upper()] = location
                            count += 1
        except Exception as e:
            self.log(f"  Warning: Could not load PartsHotList.csv: {e}")
            return 0

        self.log(f"  PartsHotList: {count} parts with warehouse locations.")
        return 1

    def _load_wp_quality_returns(self):
        """Load WpPartsHotList.csv — Whirlpool quality return flagged parts."""
        path = self.root / "WpPartsHotList.csv"
        if not path.exists():
            return 0

        count = 0
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        part_num = row[0].strip()
                        desc = row[1].strip() if len(row) > 1 else ""
                        if part_num:
                            self._quality_returns[part_num.upper()] = desc
                            count += 1
        except Exception as e:
            self.log(f"  Warning: Could not load WpPartsHotList.csv: {e}")
            return 0

        self.log(f"  WpPartsHotList: {count} Whirlpool quality return parts.")
        return 1

    def _load_models_hotlist(self):
        """Load ModelsHotList.txt — model number to pre-order recommendations."""
        path = self.root / "ModelsHotList.txt"
        if not path.exists():
            return 0

        count = 0
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Format: model_number<tab>recommendation_text
                    if "\t" in line:
                        model, rec = line.split("\t", 1)
                        model = model.strip()
                        rec = rec.strip()
                        if model and rec:
                            self._model_recommendations[model.upper()] = rec
                            count += 1
        except Exception as e:
            self.log(f"  Warning: Could not load ModelsHotList.txt: {e}")
            return 0

        self.log(f"  ModelsHotList: {count} model-specific recommendations.")
        return 1

    def _load_vendors(self):
        """Load VendorsList.csv and VendorsList_x.csv — all known vendors."""
        vendors_seen = set()
        for filename in ["VendorsList.csv", "VendorsList_x.csv"]:
            path = self.root / filename
            if not path.exists():
                continue

            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)  # skip header
                    for row in reader:
                        if len(row) >= 2:
                            abbr = row[0].strip()
                            name = row[1].strip()
                            account = row[2].strip() if len(row) > 2 else ""
                            mfr_account = row[3].strip() if len(row) > 3 else ""
                            if abbr and abbr not in vendors_seen:
                                vendors_seen.add(abbr)
                                self._vendors.append({
                                    "abbr": abbr,
                                    "name": name,
                                    "account": account,
                                    "mfr_account": mfr_account,
                                })
            except Exception as e:
                self.log(f"  Warning: Could not load {filename}: {e}")

        if self._vendors:
            self.log(f"  Vendors: {len(self._vendors)} distributors loaded.")
            return 1
        return 0

    def _load_suppliers(self):
        """Load SpplrLst — brand code to supplier name mapping."""
        path = self.root / "SpplrLst"
        if not path.exists():
            return 0

        count = 0
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            # Format is fixed-width: 2-3 char code followed by supplier name, repeated
            # Parse by splitting on known pattern: "XX NAME" pairs separated by spaces
            import re
            # Match patterns like "EL ELECTROLUX" or "1S 1ST SOURCE"
            pairs = re.findall(r'(\S{1,3})\s+([A-Z][A-Z0-9 ]+?)(?=\s{2,}|\s+\S{1,3}\s+[A-Z]|$)', content)
            for code, name in pairs:
                code = code.strip()
                name = name.strip()
                if code and name:
                    self._suppliers[code.upper()] = name
                    count += 1
        except Exception as e:
            self.log(f"  Warning: Could not load SpplrLst: {e}")
            return 0

        if count > 0:
            self.log(f"  SpplrLst: {count} brand-to-supplier mappings.")
            return 1
        return 0

    # --- Public enrichment methods ---

    def get_warehouse_location(self, part_number):
        """Return warehouse bin location for a part, or empty string."""
        return self._warehouse_locations.get(part_number.upper().strip(), "")

    def is_quality_return(self, part_number):
        """Check if a part is flagged as a Whirlpool quality return.

        Returns:
            tuple (is_flagged: bool, description: str)
        """
        pn = part_number.upper().strip()
        if pn in self._quality_returns:
            return True, self._quality_returns[pn]
        return False, ""

    def get_model_recommendation(self, model_number):
        """Get pre-order recommendation for a model number.

        Tries exact match first, then prefix match (model numbers
        in the hotlist sometimes omit color suffixes).

        Returns:
            recommendation string, or empty string if not found.
        """
        if not model_number:
            return ""

        model = model_number.upper().strip()

        # Exact match
        if model in self._model_recommendations:
            return self._model_recommendations[model]

        # Prefix match — the hotlist has entries like "MVW6500MW" but the
        # actual model might be "MVW6500MW0" with a suffix
        for hotlist_model, rec in self._model_recommendations.items():
            if model.startswith(hotlist_model) or hotlist_model.startswith(model):
                return rec

        return ""

    def get_alternate_vendors(self, exclude_code="MA"):
        """Return list of alternate vendor names, excluding the current distributor.

        Args:
            exclude_code: vendor abbreviation to exclude (default "MA" for Marcone).

        Returns:
            list of vendor name strings.
        """
        return [
            v["name"] for v in self._vendors
            if v["abbr"].strip().upper() != exclude_code.strip().upper()
            and v["name"].upper() not in ("HOT LIST", "NEW", "UNKNOWN", "1 YEAR PARTS WARRANTY")
        ]

    def get_vendor_list(self):
        """Return the full vendor list."""
        return self._vendors

    def enrich_result(self, part_number, model_number=""):
        """Enrich a single part lookup result with all NetData intelligence.

        Args:
            part_number: the part being looked up.
            model_number: optional appliance model number.

        Returns:
            dict with enrichment fields:
                warehouse_location, quality_return, quality_return_desc,
                model_recommendation, alternate_vendors
        """
        if not self.available:
            return {
                "warehouse_location": "",
                "quality_return": False,
                "quality_return_desc": "",
                "model_recommendation": "",
                "alternate_vendors": "",
            }

        qr_flag, qr_desc = self.is_quality_return(part_number)
        alt_vendors = self.get_alternate_vendors()

        return {
            "warehouse_location": self.get_warehouse_location(part_number),
            "quality_return": qr_flag,
            "quality_return_desc": qr_desc if qr_flag else "",
            "model_recommendation": self.get_model_recommendation(model_number),
            "alternate_vendors": ", ".join(alt_vendors),
        }

    def get_stats(self):
        """Return counts of loaded data for status reporting."""
        return {
            "available": self.available,
            "warehouse_locations": len(self._warehouse_locations),
            "quality_return_parts": len(self._quality_returns),
            "model_recommendations": len(self._model_recommendations),
            "vendors": len(self._vendors),
            "suppliers": len(self._suppliers),
        }
