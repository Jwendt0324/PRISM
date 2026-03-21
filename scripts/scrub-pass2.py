#!/usr/bin/env python3
"""
Second-pass PII scrub — catches bare first names, remaining domains,
drive index client names, Google Sheet IDs, and broken placeholder patterns.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Bare first names (the big miss from pass 1) ──
FIRST_NAMES = [
    # These get replaced everywhere EXCEPT inside existing placeholders
    ("Dennis", "[Your Mentor/Advisor]"),
    ("Jack", "[Your Name]"),
    ("Dylan", "[Your Ops Partner]"),
    ("Josh", "[Your Site Admin]"),
    ("Jackson", "[Your Content Specialist]"),
    ("Muzamil", "[Your Ops Admin]"),
    ("Hezekiah", "[Your Automation Lead]"),
    ("Fredrick", "[Your Content Ops Lead]"),
    ("Braden", "[Your Client Specialist]"),
    ("Jeffry", "[Your Ads Specialist]"),
    ("Luke", "[Your Local Agency Partner]"),
    ("Daniel", "[Your Team Member]"),
    ("Henry", "[Your Content Monitor]"),
    ("Grant", "[Your Repurposing Specialist]"),
    ("Russell", "[Prospect Name]"),
    ("Michael", "[External Contact]"),
    ("Sam", "[Your AgentBuilder Partner]"),
    ("Caleb", "[Your Former Mentor]"),
    ("Logan", "[Client Team Contact]"),
]

# ── Domains missed in pass 1 ──
DOMAIN_FIXES = [
    ("blitzmetrics.com", "[methodology-partner.com]"),
    ("blitzadmin.com", "[admin-platform.com]"),
    ("DennisYu.com", "[advisor-website.com]"),
    ("dennisyu.com", "[advisor-website.com]"),
    ("DylanHaugen.com", "[ops-partner-website.com]"),
    ("dylanhaugen.com", "[ops-partner-website.com]"),
    ("rossware.com", "[field-service-platform.com]"),
    ("rosswarehosting.com", "[field-service-hosting.com]"),
    ("api.rossware.com", "api.[field-service-platform.com]"),
    ("Rossware", "[Field Service Platform]"),
]

# ── Client/person names in drive index filenames ──
DRIVE_INDEX_NAMES = [
    ("Jason Stephenson", "[Client Name]"),
    ("Jake Dennis", "[Client Name]"),
    ("Jenene Cherney", "[Client Name]"),
    ("Dan McCoy", "[Client Name]"),
    ("Dr Sandi Rocco", "[Client Name]"),
    ("Dr. Sandi Rocco", "[Client Name]"),
    ("Scott Zimmerman", "[Client Name]"),
    ("Shannon Norwood", "[Client Name]"),
    ("Anthony Hilb", "[Partner Name]"),
    ("Rich Cardona", "[Client Name]"),
    ("Richard Cardona", "[Client Name]"),
    ("Justin Martin", "[Client Name]"),
    ("Nick Stover", "[Client Name]"),
    ("Paula Mc Sporran", "[Client Name]"),
    ("Dr. Tim Zelko", "[Client Name]"),
    ("Richard Canfield", "[Client Name]"),
    ("Darryl Isaacs", "[Client Name]"),
    ("Will Palmer", "[Client Name]"),
    ("Sam DeMaio", "[Client Name]"),
    ("Cletus Coffey", "[Client Name]"),
    ("World Gym", "[Client Business]"),
    ("Ashley Furniture", "[Client Business]"),
    ("Mr. Reliable Heating & Air", "[Client Business]"),
    ("Southern Values Cooling and Heating", "[Client Business]"),
    ("PILMMA", "[Industry Association]"),
    ("DigiMarCon", "[Industry Conference]"),
    ("High Rise Academy", "[Your Academy Name]"),
    ("The Forge", "[Your Speaker Event]"),
    ("Marcone", "[Parts Distributor]"),
    ("coachyu_dennisyu", "[advisor-brand]"),
    ("DENNIS YU", "[YOUR MENTOR/ADVISOR]"),
]

# ── Fix broken placeholder patterns ──
BROKEN_PATTERNS = [
    ("{{OWNER_NAME}}son", "[Your Content Specialist]"),
    ("[Your Name]son", "[Your Content Specialist]"),
    # Fix double-bracketed or malformed placeholders from prior passes
    ("{{OPS_ADMIN_NAME}}", "[Your Ops Admin]"),
    ("{{ADVISOR_NAME}}", "[Your Mentor/Advisor]"),
    ("{{OPS_PARTNER_NAME}}", "[Your Ops Partner]"),
    ("{{OWNER_NAME}}", "[Your Name]"),
    ("{{TEAM_MEMBER_NAME}}", "[Your Content Specialist]"),
    ("{{SITE_ADMIN_NAME}}", "[Your Site Admin]"),
    ("{{COMPANY_NAME}}", "[Your Agency Name]"),
    ("{{COMPANY}}", "[Your Agency]"),
    ("{{COMPANY_DOMAIN}}", "[your-agency.com]"),
    ("{{PLATFORM_DOMAIN}}", "[partner-platform.com]"),
    ("{{USER_EMAIL}}", "[your-email@your-agency.com]"),
    ("{{OPS_ADMIN_EMAIL}}", "[ops-admin@partner-platform.com]"),
    ("{{TEAM_MEMBER_EMAIL}}", "[team-member@your-agency.com]"),
    ("{{ADMIN_EMAIL}}", "[admin@methodology-partner.com]"),
    ("{{SHARED_ACCESS_EMAIL}}", "[shared-access@partner-platform.com]"),
    ("{{GOOGLE_DRIVE_PATH}}", "[Your Google Drive Path]"),
]

# ── Google Sheet/Doc URL patterns ──
GSHEET_PATTERN = re.compile(
    r'https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9_-]{25,}/?[^\s)]*'
)


def scrub_file(filepath):
    """Apply second-pass replacements."""
    # Skip the scrub scripts themselves and binary files
    rel = os.path.relpath(filepath, REPO_ROOT)
    if 'scrub-' in rel and rel.endswith('.py'):
        return 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        return 0

    original = content

    # 1. Fix broken placeholder patterns first
    for old, new in BROKEN_PATTERNS:
        if old in content:
            content = content.replace(old, new)

    # 2. Drive index names and client names
    for old, new in DRIVE_INDEX_NAMES:
        if old in content:
            content = content.replace(old, new)

    # 3. Domain fixes
    for old, new in DOMAIN_FIXES:
        if old in content:
            content = content.replace(old, new)

    # 4. Google Sheet URLs
    content = GSHEET_PATTERN.sub('[Google Sheet URL]', content)

    # 5. Bare first names — use word boundary replacement
    # Only in content files, not in code
    is_content_file = any(rel.startswith(d) for d in [
        'team-ops/', 'sops/', 'skills/', 'blitzmetrics-canon/',
        'claude-code/', 'INDEX.md'
    ]) or rel == 'INDEX.md'

    if is_content_file:
        for name, replacement in FIRST_NAMES:
            # Use word boundary to avoid replacing inside other words
            # But skip if already inside a placeholder bracket
            pattern = r'(?<!\[)(?<!\w)' + re.escape(name) + r'(?!\w)(?!\])'
            content = re.sub(pattern, replacement, content)

    # 6. Catch any remaining real Google Doc IDs
    content = re.sub(
        r'(?<=["\s:/])([a-zA-Z0-9_-]{30,})(?=["\s,\)])',
        '[google-doc-id]',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0


def main():
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.personal'}
    skip_extensions = {'.pyc', '.pyo', '.docx', '.xlsx', '.zip', '.mp3',
                       '.wav', '.png', '.jpg', '.gif', '.pdf',
                       '.woff', '.woff2', '.ttf', '.eot', '.ico',
                       '.MDB', '.sample'}

    files_changed = 0
    files_scanned = 0

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1]
            if ext in skip_extensions:
                continue
            if filename in ('PrtsPrcs', 'SchdList'):
                continue

            files_scanned += 1
            result = scrub_file(filepath)
            if result:
                files_changed += 1
                print(f"  [SCRUBBED] {os.path.relpath(filepath, REPO_ROOT)}")

    print(f"\n{'='*50}")
    print(f"  Pass 2 — Files scanned: {files_scanned}")
    print(f"  Pass 2 — Files changed: {files_changed}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
