#!/usr/bin/env python3
"""
Deep PII scrub for the shared Mainframe repo.
Replaces all personal/confidential data with intuitive placeholders.
Only runs on mainframe-shared/ — never touches the original Mainframe.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Replacement Maps ──
# Format: (pattern, replacement)
# Order matters — longer/more specific patterns first to avoid partial matches

NAME_REPLACEMENTS = [
    # Full names first (before first-name-only patterns)
    ("[Your Content Specialist]", "[Your Content Specialist]"),
    ("[Your Mentor/Advisor]", "[Your Mentor/Advisor]"),
    ("[Your Ops Partner]", "[Your Ops Partner]"),
    ("[Your Ops Admin]", "[Your Ops Admin]"),
    ("[Your Automation Lead]", "[Your Automation Lead]"),
    ("[Your Local Agency Partner]", "[Your Local Agency Partner]"),
    ("[Your Team Member]", "[Your Team Member]"),
    ("[Your Site Admin]", "[Your Site Admin]"),
    ("[Your Content Monitor]", "[Your Content Monitor]"),
    ("[Your Client Project Lead]", "[Your Client Project Lead]"),
    ("[Your Content Writer]", "[Your Content Writer]"),
    ("[Your Content Ops Lead]", "[Your Content Ops Lead]"),
    ("[Your Repurposing Specialist]", "[Your Repurposing Specialist]"),
    ("[Your AgentBuilder Partner]", "[Your AgentBuilder Partner]"),
    ("[Your Client Specialist]", "[Your Client Specialist]"),
    ("[Your Ads Specialist]", "[Your Ads Specialist]"),
    ("[Your Former Mentor]", "[Your Former Mentor]"),
    ("[Your University Contact]", "[Your University Contact]"),
    ("[Your Authority Framework Partner]", "[Your Authority Framework Partner]"),
    ("[Your Industry Advisor]", "[Your Industry Advisor]"),
    ("[Your Industry Association Contact]", "[Your Industry Association Contact]"),
    ("[Your Peer Group Leader]", "[Your Peer Group Leader]"),
    ("[Top-Performing Apprentice]", "[Top-Performing Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Apprentice Sponsor]", "[Apprentice Sponsor]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Active Apprentice]", "[Active Apprentice]"),
    ("[Returning Apprentice]", "[Returning Apprentice]"),
    ("[Apprentice Parent]", "[Apprentice Parent]"),
    ("[Onboarding Prospect]", "[Onboarding Prospect]"),
    ("[Onboarding Prospect]", "[Onboarding Prospect]"),
    ("[KP Sprint Prospect]", "[KP Sprint Prospect]"),
    ("[Industry Lighthouse Prospect]", "[Industry Lighthouse Prospect]"),
    ("[Completed KP Client]", "[Completed KP Client]"),
    ("[Churned Client]", "[Churned Client]"),
    ("[KP Sprint Client]", "[KP Sprint Client]"),
    ("[KP Sprint Client]", "[KP Sprint Client]"),
    ("[Retainer Client]", "[Retainer Client]"),
    ("[Quickstart Client]", "[Quickstart Client]"),
    ("[VIP Client]", "[VIP Client]"),
    ("[Client Team Contact]", "[Client Team Contact]"),
    ("[Industry Contact]", "[Industry Contact]"),
    ("[Refunded Client]", "[Refunded Client]"),
    ("[University Professor Contact]", "[University Professor Contact]"),
    ("[Client Contact]", "[Client Contact]"),
    ("[Client Contact]", "[Client Contact]"),
    ("[Your Name]", "[Your Name]"),
    # Industry names from Drive index
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Industry Speaker]", "[Industry Speaker]"),
    ("[Guest Appearance Host]", "[Guest Appearance Host]"),
    ("[Guest Appearance Host]", "[Guest Appearance Host]"),
    ("[Guest Appearance Host]", "[Guest Appearance Host]"),
    ("[Guest Appearance Host]", "[Guest Appearance Host]"),
    # First-name-only catches (context-dependent, applied after full names)
    # These are trickier — only replace when clearly referring to the person
]

# First-name patterns that need context (only in team-ops and specific files)
FIRST_NAME_CONTEXTUAL = [
    ("Muzamil", "[Your Ops Admin]"),
    ("Hezekiah", "[Your Automation Lead]"),
    ("Jackson", "[Your Content Specialist]"),
    ("Fredrick", "[Your Content Ops Lead]"),
]

CLIENT_COMPANY_REPLACEMENTS = [
    ("[Client — Local Retail Business]", "[Client — Local Retail Business]"),
    ("[Client — Local Retail Business]", "[Client — Local Retail Business]"),
    ("[Client — Financial Advisory]", "[Client — Financial Advisory]"),
    ("[Client — Digital Agency]", "[Client — Digital Agency]"),
    ("[Client — Fitness Brand]", "[Client — Fitness Brand]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Home Services]", "[Client — Home Services]"),
    ("[Client — Local Business]", "[Client — Local Business]"),
    ("[Client — Appliance Repair]", "[Client — Appliance Repair]"),
    ("[Client — Appliance Repair]", "[Client — Appliance Repair]"),
    ("[Client — Legal]", "[Client — Legal]"),
    ("[Client — Niche Advisory]", "[Client — Niche Advisory]"),
    ("[client-niche-advisory.com]", "[client-niche-advisory.com]"),
    ("[Client — E-commerce]", "[Client — E-commerce]"),
    ("[Former Employer]", "[Former Employer]"),
    ("[Peer Group Leader's Company]", "[Peer Group Leader's Company]"),
    ("[Social Media Tool]", "[Social Media Tool]"),
]

COMPANY_REPLACEMENTS = [
    ("[Your Agency Name]", "[Your Agency Name]"),
    # Be careful with [Your Agency] — only replace when it's clearly the company abbreviation
    ("[Partner Platform]", "[Partner Platform]"),
    ("[Methodology Partner]", "[Methodology Partner]"),
]

DOMAIN_REPLACEMENTS = [
    ("[your-agency.com]", "[your-agency.com]"),
    ("[partner-platform.com]", "[partner-platform.com]"),
    ("[content-platform.com]", "[content-platform.com]"),
    ("academy.[content-platform.com]", "[your-academy-url.com]"),
    ("[partner-website.com]", "[partner-website.com]"),
    ("[partner-website.com]", "[partner-website.com]"),
    ("[partner-website.com]", "[partner-website.com]"),
    ("[former-employer.com]", "[former-employer.com]"),
    ("[client-niche-advisory.com]", "[client-website.com]"),
    ("[your-personal-site.com]", "[your-personal-site.com]"),
    ("[client-server.example.com]", "[client-server.example.com]"),
    ("[auth-server.example.com]", "[auth-server.example.com]"),
]

EMAIL_REPLACEMENTS = [
    ("[your-email@your-agency.com]", "[your-email@your-agency.com]"),
    ("[team-member@your-agency.com]", "[team-member@your-agency.com]"),
    ("[advisor-email@example.com]", "[advisor-email@example.com]"),
    ("[ops-partner@partner-platform.com]", "[ops-partner@partner-platform.com]"),
    ("[ops-admin@partner-platform.com]", "[ops-admin@partner-platform.com]"),
    ("[agency-partner@partner-platform.com]", "[agency-partner@partner-platform.com]"),
    ("[team-member@partner-platform.com]", "[team-member@partner-platform.com]"),
    ("[site-admin@partner-platform.com]", "[site-admin@partner-platform.com]"),
    ("[content-monitor@partner-platform.com]", "[content-monitor@partner-platform.com]"),
    ("[automation-lead@example.com]", "[automation-lead@example.com]"),
    ("[content-writer@content-platform.com]", "[content-writer@content-platform.com]"),
    ("[partner-email@example.com]", "[partner-email@example.com]"),
    ("[former-mentor@example.com]", "[former-mentor@example.com]"),
    ("[university-contact@example.com]", "[university-contact@example.com]"),
    ("[authority-partner@example.com]", "[authority-partner@example.com]"),
    ("[industry-advisor@example.com]", "[industry-advisor@example.com]"),
    ("[association-contact@example.org]", "[association-contact@example.org]"),
    ("[client-email@example.com]", "[client-email@example.com]"),
    ("[client-email@example.com]", "[client-email@example.com]"),
    ("[shared-access@methodology-partner.com]", "[shared-access@methodology-partner.com]"),
    ("[operations@methodology-partner.com]", "[operations@methodology-partner.com]"),
    ("[admin@methodology-partner.com]", "[admin@methodology-partner.com]"),
    ("[shared-access@partner-platform.com]", "[shared-access@partner-platform.com]"),
    ("[prospect-email@example.com]", "[prospect-email@example.com]"),
]

URL_REPLACEMENTS = [
    ("[Your Zoom Meeting Link]", "[Your Zoom Meeting Link]"),
    ("[your-basecamp-url.com/project-id]", "[your-basecamp-url.com/project-id]"),
    ("[your-linkedin-url]", "[your-linkedin-url]"),
    ("[advisor-linkedin-url]", "[advisor-linkedin-url]"),
    ("[@your-instagram-handle]", "[@your-instagram-handle]"),
]

FINANCIAL_REPLACEMENTS = [
    # Specific compensation — most sensitive
    ("[$X/week = ~$X/mo]", "[$X/week = ~$X/mo]"),
    ("[$X/week]", "[$X/week]"),
    ("[$X/mo]", "[$X/mo]"),
    ("[$X/mo take-home]", "[$X/mo take-home]"),
    ("[$X/mo]", "[$X/mo]"),
    ("[$X over 6 months]", "[$X over 6 months]"),
    ("[$X — AI tool spend]", "[$X — AI tool spend]"),
    ("[$X — refund amount]", "[$X — refund amount]"),
    # Revenue totals
    ("[$Total Revenue]", "[$Total Revenue]"),
    ("[~$Total Revenue]", "[~$Total Revenue]"),
    ("[~$Total Revenue]", "[~$Total Revenue]"),
    ("[$Partner Share]", "[$Partner Share]"),
    ("[$Your Share]", "[$Your Share]"),
    ("[~$avg monthly]", "[~$avg monthly]"),
    ("[$Current Balance]", "[$Current Balance]"),
    ("[$Recent Payment]", "[$Recent Payment]"),
    ("[$Catch-up Payment]", "[$Catch-up Payment]"),
    # Keep product pricing as-is (those are public offers, not confidential)
]

ADDRESS_REPLACEMENTS = [
    ("[Your Business Address]", "[Your Business Address]"),
    ("[Your City, State]", "[Your City, State]"),
    ("[Your City, State]", "[Your City, State]"),
    ("[Your City, State]", "[Your City, State]"),
    ("[Your City, State]", "[Your City, State]"),
    ("[Event Venue]", "[Event Venue]"),
]

INFRASTRUCTURE_REPLACEMENTS = [
    ("Zoom (ID: [Your Zoom ID])", "Zoom (ID: [Your Zoom ID])"),
    ("[Your Zoom ID]", "[Your Zoom ID]"),
    ("[Your Zoom ID]", "[Your Zoom ID]"),
]

# Equity — replace specific percentages tied to people
EQUITY_REPLACEMENTS = [
    ("[Majority Owner]", "[Majority Owner]"),
    ("[Majority Equity]", "[Majority Equity]"),
    ("[Majority %]", "[Majority %]"),  # only in equity contexts
    ("Jack [Majority %]", "[Founder Majority %]"),
    ("[Advisor Equity %]", "[Advisor Equity %]"),
    ("[Ops Partner Equity %]", "[Ops Partner Equity %]"),
    ("[Advisor Equity %]", "[Advisor Equity %]"),
    ("[Ops Partner Equity %]", "[Ops Partner Equity %]"),
]

# Book titles
BOOK_REPLACEMENTS = [
    ('"[Working Book Title]"', '"[Working Book Title]"'),
    ("[Working Book Title]", "[Working Book Title]"),
]


def scrub_file(filepath):
    """Apply all replacements to a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        return 0

    original = content
    changes = 0

    # Apply replacements in order of specificity
    all_replacements = (
        EMAIL_REPLACEMENTS +
        URL_REPLACEMENTS +
        FINANCIAL_REPLACEMENTS +
        ADDRESS_REPLACEMENTS +
        INFRASTRUCTURE_REPLACEMENTS +
        EQUITY_REPLACEMENTS +
        BOOK_REPLACEMENTS +
        NAME_REPLACEMENTS +
        CLIENT_COMPANY_REPLACEMENTS +
        DOMAIN_REPLACEMENTS +
        COMPANY_REPLACEMENTS
    )

    for old, new in all_replacements:
        if old in content:
            content = content.replace(old, new)

    # Contextual first-name replacements (only in team-ops, sops, skills, canon)
    rel_path = os.path.relpath(filepath, REPO_ROOT)
    if any(rel_path.startswith(d) for d in ['team-ops/', 'sops/', 'skills/', 'blitzmetrics-canon/']):
        for old, new in FIRST_NAME_CONTEXTUAL:
            if old in content:
                content = content.replace(old, new)

    # Scrub Google Doc IDs (32+ char alphanumeric strings in URLs/references)
    content = re.sub(
        r'(doc_id["\s:]+)["\']?([a-zA-Z0-9_-]{25,})["\']?',
        r'\1[google-doc-id]',
        content
    )
    # Also catch standalone doc IDs in drive index format
    content = re.sub(
        r'doc_id: ([a-zA-Z0-9_-]{25,})',
        'doc_id: [google-doc-id]',
        content
    )

    # Replace "[Your Agency]" but only when it's clearly the company abbreviation
    # (surrounded by spaces, punctuation, or at word boundaries — not inside other words)
    content = re.sub(r'\bHRI\b', '[Your Agency]', content)

    # Replace "[Partner Platform]" similarly
    content = re.sub(r'\bLSS\b', '[Partner Platform]', content)

    # Replace "BM" when clearly referring to [Methodology Partner] (not "BM" in other contexts)
    # Only replace when preceded/followed by context clues
    content = re.sub(r'\bBM\b(?=[\s/\'])', '[Methodology Partner]', content)
    content = re.sub(r'(?<=[\s/])\bBM\b', '[Methodology Partner]', content)

    if content != original:
        changes = sum(1 for a, b in zip(content, original) if a != b)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1

    return 0


def main():
    """Walk the repo and scrub all text files."""
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.personal'}
    skip_extensions = {'.pyc', '.pyo', '.docx', '.xlsx', '.zip', '.mp3',
                       '.wav', '.png', '.jpg', '.jpeg', '.gif', '.pdf',
                       '.woff', '.woff2', '.ttf', '.eot', '.ico',
                       '.MDB', '.sample'}

    files_changed = 0
    files_scanned = 0

    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1]

            if ext in skip_extensions:
                continue

            # Skip binary files
            if filename in ('PrtsPrcs', 'SchdList'):
                continue

            files_scanned += 1
            result = scrub_file(filepath)
            if result:
                files_changed += 1
                rel = os.path.relpath(filepath, REPO_ROOT)
                print(f"  [SCRUBBED] {rel}")

    print(f"\n{'='*50}")
    print(f"  Files scanned: {files_scanned}")
    print(f"  Files changed: {files_changed}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
