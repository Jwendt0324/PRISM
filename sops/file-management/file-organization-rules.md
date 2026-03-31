---
description: Define file type routing, naming conventions, and folder structures
  for organizing all files consistently
category: file-management
created: 2026-03-18
last_updated: 2026-03-21
version: 1.3
canon_compliance: 07-quality-standards.md
triangles: CCS
canon_sources:
  - 07-quality-standards.md
tags:
  - domain/filemanagement
  - status/active
  - type/sop
---

# File Organization Rules SOP

## Purpose
Establish a single source of truth for where every file type goes, so files can be routed automatically and found predictably without hunting.

## When to Use
- File Organizer scheduled task runs daily
- After manual file downloads or client file deliverables
- When desktop or Downloads folder exceeds clean thresholds
- When organizing a new client folder structure
- When identifying where a specific file should live

## File Type Routing Rules

### Screenshots
**Route to:** `~/Documents/Screenshots/YYYY-MM-DD/`

Rules:
- Create a folder for each date (YYYY-MM-DD format)
- Rename files to include context: `screenshot-HH-MM--context.png`
  - Example: `screenshot-14-32--figma-component-library.png`
- Keep full-resolution originals
- Move any duplicate screenshots to same-date folder

### PDFs
**Route to:**
- If client-identifiable: `~/Documents/Clients/[ClientName]/[ProjectFolder]/filename.pdf`
- If type-specific: `~/Documents/PDFs/[Category]/filename.pdf`
  - Categories: Invoices, Contracts, Research, Articles, Reference
- If unidentifiable: `~/Documents/PDFs/Inbox/filename-YYYY-MM-DD.pdf`

Rules:
- Extract and rename to content: "Invoice-Acme-2026-03-Q1.pdf" not "document-123.pdf"
- If two clients share a PDF, save in shared folder structure (see Client Structure below)
- Archive old invoices (>1 year) to: `~/Documents/Archive/PDFs/YYYY/`

### Documents (.docx, .pptx, .xlsx, .txt, .md)
**Route to:**
- If client-related: `~/Documents/Clients/[ClientName]/[ProjectFolder]/filename`
- If project-specific: `~/Documents/Projects/[ProjectName]/filename`
- If reference/template: `~/Documents/Templates/[Category]/filename`
- If active work: `~/Documents/Active/filename`
- If personal: `~/Documents/Personal/filename`

Rules:
- Use hyphenated filenames: `project-proposal-v2.docx` not `Project Proposal v2.docx`
- Version numbers: suffix with `-v1`, `-v2` (not in filename, just v-number before extension)
- Include date for time-sensitive docs: `meeting-notes-2026-03-15.md`

### Code Files (.js, .ts, .py, .go, .rs, .java, etc.)
**Route to:** Appropriate project folder in `~/Documents/Projects/[ProjectName]/src/`

Rules:
- Never leave code in Downloads or Desktop
- If orphaned code (no project): `~/Documents/Code-Snippets/[Language]/filename`
- If client deliverable: `~/Documents/Clients/[ClientName]/code/filename`
- Use project's existing folder structure (don't reorganize within project)

### Images (.jpg, .png, .gif, .svg)
**Route to:**
- If design asset: `~/Documents/Clients/[ClientName]/[ProjectFolder]/assets/images/`
- If reference/inspiration: `~/Documents/Reference/Images/[Category]/`
- If screenshot: apply screenshot routing rules above
- If to-be-deleted: `~/Documents/Trash/Images/` (review before permanent delete)

Rules:
- Organize by date or category within destination folder
- Rename unclear filenames: `img_001.jpg` → `design-mockup-homepage-v1.jpg`

### Audio/Video Files (.mp3, .mp4, .mov, .wav)
**Route to:**
- If client deliverable: `~/Documents/Clients/[ClientName]/[ProjectFolder]/media/`
- If personal recording: `~/Documents/Personal/Media/[Category]/YYYY-MM-DD--description.mp4`
- If reference: `~/Documents/Reference/Media/`

Rules:
- Large files (>500MB): keep in external storage reference only, link from folder
- Include date for recordings: `standup-2026-03-18.mp3`

### Archives (.zip, .tar, .gz, .7z)
**Route to:** `~/Documents/Archives/[Context]--YYYY-MM-DD.zip`

Rules:
- Extract and organize contents, then delete archive (unless it's a backup)
- If archive is a backup/snapshot: store in `~/Documents/Backups/[ProjectName]/`
- Rename to include date extracted: `acme-project-backup-2026-03-18.zip`
- Do not leave unexamined archives in Downloads or Desktop

### Downloads (Mixed Types, Age-Based)
**Rule:** Move files older than 7 days to `~/Documents/Inbox/downloads-triage/`

Process for items in downloads-triage:
1. Identify file type and intended destination
2. Move to appropriate folder per routing rules above
3. If purpose unclear: move to `~/Documents/Inbox/unknown/` with date suffix
4. After 30 days in unknown/: delete with log entry

## Naming Conventions

### Global Rules
- Use hyphenated-names, not underscores or spaces: `client-proposal-v2.docx`
- Use lowercase except proper nouns: `acme-system-architecture.md` not `Acme-System-Architecture.md`
- Date format: YYYY-MM-DD when including dates (ISO 8601)
- Version format: `-v1`, `-v2` suffix before file extension
- No special characters except hyphens and underscores

### Examples
| Bad | Good |
|-----|------|
| `Project Proposal V2.docx` | `project-proposal-v2.docx` |
| `Screenshot 2026-03-18 at 2.32.45 PM.png` | `screenshot-14-32--design-review.png` |
| `Acme_Meeting_Notes_March_18.md` | `acme-meeting-notes-2026-03-18.md` |
| `FINAL_FINAL_invoice.pdf` | `invoice-acme-2026-03-q1-final.pdf` |
| `client file (1) (1).docx` | `acme-contract-v3-signed.docx` |

## Client File Structure (Folder Template)

When setting up a new client folder, use this structure:

```
~/Documents/Clients/[ClientName]/
├── README.md (client overview, key contacts, project list)
├── active/
│   ├── [ProjectName]/
│   │   ├── docs/
│   │   ├── assets/
│   │   ├── code/ (if applicable)
│   │   └── notes/
│   └── [AnotherProject]/
├── archive/
│   └── [Completed Project]/
├── contracts/
│   └── client-agreement.pdf
├── invoices/
│   ├── 2026-Q1/
│   └── 2025-Q4/
└── reference/
    ├── brand-guidelines.pdf
    └── style-guide.md
```

Rules:
- Create active/ and archive/ folders only when needed
- Move completed projects from active/ to archive/[ProjectName]/ with completion date
- Client README should list all projects, key stakeholders, and ongoing items
- Within each project: use only `docs/`, `assets/`, `code/`, `notes/` (no proliferation of subfolders)

## Desktop Cleanup Rules

**Desktop should be minimal at all times.**

Rule: Any file on desktop older than 3 days → move to `~/Documents/Inbox/desktop-triage/`

Process:
1. Check desktop daily (or when triage folder is examined)
2. If item has a clear destination per routing rules: move it
3. If purpose unclear: move to `~/Documents/Inbox/unknown/YYYY-MM-DD--filename`
4. Do not accumulate files on desktop waiting for "later"

Exception: Active work in progress (current day only)
- Label active files: `[WIP] filename` prefix
- Remove [WIP] once moved to proper folder or delete

## Inbox Folder Structure

`~/Documents/Inbox/` is a holding area for triage, not a long-term dump.

### Structure
```
~/Documents/Inbox/
├── downloads-triage/    (files >7 days old from Downloads)
├── desktop-triage/      (files >3 days old from Desktop)
├── unknown/             (files with unclear purpose)
└── manual-review/       (files needing manual decision)
```

Rules:
- **downloads-triage**: Review weekly, move to proper folders or delete
- **desktop-triage**: Review within 3 days of arrival
- **unknown**: Review monthly, delete after 30 days if still unclear
- **manual-review**: For edge cases (e.g., "Is this client A or B?") — decide within 5 days

Log every file moved from inbox with: `inbox-log.txt` (see Logging section)

## Logging Format

Create and maintain `~/Documents/Inbox/organizing-log.txt` with entries like:

```
2026-03-18 14:32 MOVED screenshot-14-32--figma-review.png → Documents/Screenshots/2026-03-18/
2026-03-18 14:33 MOVED project-proposal-v2.docx → Documents/Clients/Acme/active/Website-Redesign/docs/
2026-03-18 14:35 MOVED unknown-document.pdf → Documents/Inbox/unknown/2026-03-18--unknown-document.pdf
2026-03-18 14:38 MOVED old-backup.zip → Documents/Backups/ (extracted and original deleted)
2026-03-18 15:00 DELETED 12 duplicate screenshots from inbox/downloads-triage/
```

Format: `YYYY-MM-DD HH:MM ACTION file → destination [notes]`

Use log to track:
- What was organized
- Where it went
- Any decisions made (e.g., "client identified as Acme")
- Files deleted (with count)
- Time spent (summary at end of day)

## Quality Checks

- [ ] All client files live in `~/Documents/Clients/[ClientName]/`
- [ ] Screenshots are organized by date in `~/Documents/Screenshots/YYYY-MM-DD/`
- [ ] No PDFs, images, or code files remain in Desktop or Downloads >7 days
- [ ] All files follow hyphenated naming convention (no spaces, camelCase, or SCREAMING_CASE)
- [ ] Client folders include README.md with project overview
- [ ] Inbox triage folders reviewed at least weekly
- [ ] Organizing log updated with all moves
- [ ] Archive folders for old projects exist (not all in active/)
- [ ] No [WIP] prefixes left on desktop files

## Common Pitfalls

**"I'll organize this later"** → Files left in Downloads grow into a mess. Set a rule: 7-day cleanup is automatic.

**Inconsistent naming** → Mix of spaces, underscores, camelCase makes files hard to find. Pick hyphenated-names and stick to it.

**Nested folders too deep** → `~/Documents/Clients/Acme/projects/2026/Q1/Website-Redesign/deliverables/final/` is too deep. Use max 4 levels below client name.

**Client folders without structure** → Files scattered randomly in one folder. Use the template structure above even for small projects.

**Leaving archives unexamined** → Downloads fill with old .zip files. Always extract, check contents, and delete or move to Backups/.

**Duplicates left behind** → When organizing, old versions stay in original location. Check the source folder is empty before moving on.

**Logging skipped** → No record of what was organized means patterns aren't visible. Log every session.

**Cross-mount moves fail silently** → When moving files between mounted volumes (e.g., Google Drive Desktop/Downloads to Documents), `mv` may copy but fail to remove the source. Always verify source removal and log originals needing manual cleanup.

**macOS unicode in filenames** → Screenshot filenames contain U+202F (narrow no-break space) before AM/PM. Use `find -name` with glob patterns rather than hardcoded strings to handle this reliably.

## Canon Compliance

- **Canon source:** 07-quality-standards.md
- **Triangles served:** CCS (process checklist — systematic file routing, naming conventions, and folder structure enforcement)
- **Human checkpoints:** Manual review of unknown/ folder items before deletion (30-day rule); manual-review/ folder requires human decision within 5 days; client identification for ambiguous files
- **Anti-vandalism:** Organizing log tracks every move with timestamp and destination; no files deleted without log entry; archives always extracted and examined before deletion; prior folder contents verified empty before moving on; 7-day and 3-day automated cleanup thresholds prevent accumulation
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log

- **2026-03-18:** Created initial SOP. No learnings yet—this is the baseline.
- **2026-03-20:** First automated run. Key learnings:
  - macOS screenshot filenames contain Unicode narrow no-break space (U+202F) before AM/PM. Standard shell quoting doesn't handle this — use `find -name` glob matching instead of hardcoded filenames.
  - Google Drive-mounted directories (Desktop, Downloads) have cross-mount permission restrictions. `mv` copies the file but cannot remove the source. Workaround: copy to destination, log originals for manual deletion.
  - Desktop accumulates organizational folders (PDFs/, Videos/, etc.) that duplicate Documents structure. SOP should clarify: desktop folder cleanup is separate from file cleanup — folders should be consolidated during manual triage, not automated runs.
  - Downloads had pre-existing organizational subfolders from a previous manual sort. Automated runs should skip files already inside categorized subfolders and only target loose files at Downloads root.
  - New client folder created: [Client-Name] (Knowledge Panel project). Multiple related docs identified across Downloads.
- **2026-03-21:** Second automated run. Key learnings:
  - Cross-mount leftovers accumulate between runs. Previous run's originals (3 [Client Name] files) were still in Downloads because [Your Name] hadn't manually deleted them yet. Automated runs should detect and skip these rather than re-copying.
  - Desktop accumulates AI-generated .md files (meeting notes, drafts, reports, EODs) from Claude sessions. These are active work products and should not be moved prematurely. The 3-day threshold works well — most become stale within that window.
  - Multiple duplicate downloads are common (e.g., 3 copies of CapCut installer, 4 copies of Claude PRISM guide). When organizing, copy only one to destination and flag all originals for manual deletion.
  - Large video files (500MB+) should be logged for manual triage rather than copied across mounts — doubling disk usage and copy time isn't worth it for files that need human context to route properly.

---

## See Also

- [[sops/file-management/logging-discipline|Logging Discipline]]
- [[sops/file-management/mcp-tool-integration|MCP Tool Integration]]
- [[sops/templates/team-ops/09-tool-stack-and-access|Tool Stack & Access]]
- [[blitzmetrics-canon/07-quality-standards|Canon: Quality Standards]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Canon: Anti-Vandalism]]