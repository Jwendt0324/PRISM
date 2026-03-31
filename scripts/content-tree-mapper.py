#!/usr/bin/env python3
"""
Claude PRISM — Content Tree Mapper
Scans all articles across clients and detects keyword/topic overlap (cannibalization risk).
Maps the SEO Tree: definitive articles (branches) → meta-articles (leaves).

Usage:
    python3 content-tree-mapper.py                    # Full scan
    python3 content-tree-mapper.py --client "[Client — Local Retail Business]"  # Single client
    python3 content-tree-mapper.py --check "hearing aids"       # Check specific topic

Output: content-tree-YYYY-MM-DD.md in logs/reports/
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

PRISM_DIR = os.path.expanduser("~/Documents/Claude/PRISM")


def extract_title(filepath):
    """Extract title from markdown file (first H1 or filename)."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# ") and not line.startswith("##"):
                    return line[2:].strip()
        return Path(filepath).stem.replace("-", " ").title()
    except Exception:
        return Path(filepath).stem


def extract_keywords(filepath, max_words=200):
    """Extract significant words from a file for overlap detection."""
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above", "below",
        "between", "out", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "both",
        "each", "few", "more", "most", "other", "some", "such", "no", "nor",
        "not", "only", "own", "same", "so", "than", "too", "very", "just",
        "don", "now", "and", "but", "or", "if", "while", "that", "this",
        "these", "those", "it", "its", "they", "them", "their", "we", "our",
        "you", "your", "he", "him", "his", "she", "her", "i", "me", "my",
        "what", "which", "who", "whom", "up", "about", "also", "like",
        "even", "because", "but", "still", "get", "got", "one", "two",
        "three", "first", "new", "way", "make", "well", "back", "much",
    }
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Strip markdown formatting
        text = re.sub(r'[#*\[\]()_`>|]', ' ', text)
        text = re.sub(r'https?://\S+', '', text)
        words = re.findall(r'[a-z]{3,}', text.lower())
        # Get significant words (not stopwords, appear 2+ times)
        word_counts = defaultdict(int)
        for w in words:
            if w not in stopwords:
                word_counts[w] += 1
        significant = sorted(word_counts.items(), key=lambda x: -x[1])[:max_words]
        return {w for w, c in significant if c >= 2}
    except Exception:
        return set()


def find_content_files(base_dir=None, client_filter=None):
    """Find all article/content markdown and docx files."""
    if base_dir is None:
        base_dir = PRISM_DIR

    content_files = []
    search_dirs = [
        os.path.join(base_dir, "content-pipeline"),
        os.path.join(os.path.expanduser("~"), "Documents", "Claude"),
    ]

    skip_dirs = {"logs", "scripts", "__pycache__", ".backups", "node_modules",
                 ".git", "hooks", "claude-code", "blitzmetrics-canon", "team-ops",
                 "sops", "memory-bank", "external-skills", "skills", "good-examples",
                 "kp-book", "archive", "_archived_short", "LifeOS"}

    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
            for f in files:
                if not f.endswith(".md"):
                    continue
                # Skip non-article files
                if f in ("HOW-TO-USE.md", "README.md", "INDEX.md", "CONTEXT.md",
                         "manifest.md", "HUMAN_REVIEW_CHECKLIST.md", "QA_SCORECARDS.md",
                         "MEMORY.md", "_Dashboard.md", "AUTOMATION-STATUS.md",
                         "SETUP-GUIDE.md", "SECURITY-WARNING.md"):
                    continue
                # Skip versioned files (kp-book-v001.md etc)
                if re.match(r'.*-v\d{2,3}\.md$', f):
                    continue
                # Skip config/tracker files
                if f.endswith(("-tracker.md", "-protocol.md", "-template.md")):
                    continue
                fpath = os.path.join(root, f)
                # Detect client from path
                lower_path = fpath.lower()
                client = "Unknown"
                markers = {
                    "acoustic": "[Client — Local Retail Business]",
                    "discover-strength": "[Client — Fitness Brand]",
                    "[client-id]": "[Client — Appliance Repair]",
                    "sloan": "[Client — Appliance Repair]",
                    "ryan": "[Client Name]",
                    "blitz": "[Methodology Partner]",
                    "hri": "[Your Agency]",
                }
                for marker, name in markers.items():
                    if marker in lower_path:
                        client = name
                        break

                if client_filter and client != client_filter:
                    continue

                content_files.append({
                    "path": fpath,
                    "name": f,
                    "client": client,
                    "title": extract_title(fpath),
                })

    return content_files


def detect_overlap(files):
    """Detect keyword overlap between files (cannibalization risk)."""
    # Extract keywords for each file
    file_keywords = {}
    for f in files:
        kws = extract_keywords(f["path"])
        if kws:
            file_keywords[f["path"]] = {
                "keywords": kws,
                "title": f["title"],
                "client": f["client"],
                "name": f["name"],
            }

    # Compare all pairs within the same client
    overlaps = []
    paths = list(file_keywords.keys())
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            f1 = file_keywords[paths[i]]
            f2 = file_keywords[paths[j]]

            # Only compare within same client
            if f1["client"] != f2["client"]:
                continue

            shared = f1["keywords"] & f2["keywords"]
            total = f1["keywords"] | f2["keywords"]
            if not total:
                continue

            overlap_pct = len(shared) / len(total) * 100
            if overlap_pct >= 40:  # 40%+ overlap = high risk
                overlaps.append({
                    "file1": f1["name"],
                    "file2": f2["name"],
                    "client": f1["client"],
                    "overlap_pct": round(overlap_pct, 1),
                    "shared_keywords": sorted(list(shared))[:20],
                    "title1": f1["title"],
                    "title2": f2["title"],
                })

    return sorted(overlaps, key=lambda x: -x["overlap_pct"])


def classify_content(files):
    """Classify files as definitive articles, meta-articles, or supporting content."""
    classified = {
        "definitive": [],
        "meta": [],
        "supporting": [],
    }

    for f in files:
        name_lower = f["name"].lower()
        title_lower = f["title"].lower()
        if "definitive" in name_lower or "definitive" in title_lower:
            classified["definitive"].append(f)
        elif "meta-" in name_lower or "how we " in title_lower or "how-we-" in name_lower:
            classified["meta"].append(f)
        else:
            classified["supporting"].append(f)

    return classified


def generate_report(client_filter=None, topic_check=None):
    """Generate the content tree map report."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    files = find_content_files(client_filter=client_filter)

    if topic_check:
        # Filter to files mentioning the topic
        topic_files = []
        for f in files:
            try:
                with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                    if topic_check.lower() in fh.read().lower():
                        topic_files.append(f)
            except Exception:
                continue
        files = topic_files

    classified = classify_content(files)
    overlaps = detect_overlap(files)

    # Group by client
    by_client = defaultdict(list)
    for f in files:
        by_client[f["client"]].append(f)

    report = f"""# Content Tree Map — {date_str}

## Overview
- Total content files scanned: {len(files)}
- Definitive articles: {len(classified['definitive'])}
- Meta-articles: {len(classified['meta'])}
- Supporting content: {len(classified['supporting'])}
- Cannibalization risks (40%+ overlap): {len(overlaps)}

## SEO Tree Structure

"""
    for client in sorted(by_client.keys()):
        client_files = by_client[client]
        client_classified = classify_content(client_files)
        report += f"### {client} ({len(client_files)} files)\n"
        if client_classified["definitive"]:
            report += "**Definitive (branches):**\n"
            for f in client_classified["definitive"]:
                report += f"- {f['title']}\n"
        if client_classified["meta"]:
            report += f"**Meta-articles (leaves):** {len(client_classified['meta'])}\n"
            for f in client_classified["meta"][:5]:
                report += f"- {f['title']}\n"
            if len(client_classified["meta"]) > 5:
                report += f"- ... and {len(client_classified['meta']) - 5} more\n"
        if client_classified["supporting"]:
            report += f"**Supporting:** {len(client_classified['supporting'])} articles\n"
        report += "\n"

    if overlaps:
        report += "## Cannibalization Risks\n\n"
        report += "| Client | File 1 | File 2 | Overlap | Top Shared Keywords |\n"
        report += "|--------|--------|--------|---------|--------------------|\n"
        for o in overlaps[:20]:
            kws = ", ".join(o["shared_keywords"][:5])
            report += f"| {o['client']} | {o['file1'][:30]} | {o['file2'][:30]} | {o['overlap_pct']}% | {kws} |\n"

        report += "\n**Action required:** For each pair above, decide:\n"
        report += "1. **Merge** — combine into one stronger article\n"
        report += "2. **Differentiate** — sharpen each article's unique angle\n"
        report += "3. **Redirect** — 301 the weaker article to the stronger one\n"
    else:
        report += "## Cannibalization Risks\n\nNo high-overlap pairs detected.\n"

    report += f"\n---\n*Generated {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}*\n"

    reports_dir = os.path.join(PRISM_DIR, "logs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    suffix = f"-{client_filter.lower().replace(' ', '-')}" if client_filter else ""
    report_file = os.path.join(reports_dir, f"content-tree{suffix}-{date_str}.md")

    with open(report_file, "w") as f:
        f.write(report)

    print(f"Content tree map written to {report_file}")
    return report_file


if __name__ == "__main__":
    client = None
    topic = None

    if "--client" in sys.argv:
        idx = sys.argv.index("--client")
        client = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
    if "--check" in sys.argv:
        idx = sys.argv.index("--check")
        topic = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

    generate_report(client_filter=client, topic_check=topic)
