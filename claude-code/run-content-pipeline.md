# Run Content Pipeline — Ready-to-Use Prompt

**Use this prompt to process new content through the Content Repurposing Pipeline.**

---

## Prompt

You are running the Content Repurposing Pipeline for the Claude Mainframe. Follow the pipeline SOP exactly.

### Step 1: Load the Pipeline SOP
Read `~/Documents/Claude/Mainframe/sops/client-work/content-repurposing-pipeline.md` — this defines the full process, output matrix, voice requirements, and quality checks.

### Step 2: Identify the Source Content
The user will provide one of:
- A file path to a transcript, article, or notes
- A description of content to process
- A link or reference to content

Read the source content in full. Do not skim.

### Step 3: Check Viability
- Is this content publishable? (Not confidential, not internal-only, not someone else's copyrighted material)
- Check `~/Documents/Claude/Mainframe/content-audit/00-executive-summary.md` for any flagged files
- If marked "No" or "Needs clarification" — skip or ask [Your Name]

### Step 4: Run the Pipeline
Follow the pipeline SOP process steps:
1. **INTAKE** — Extract core elements, determine Topic Wheel position, rate content richness
2. **PRODUCE** — Generate outputs across all 5 tiers (articles, social posts, video scripts, emails, SOP recommendations)
3. **QUALITY CHECK** — Run every output through the defined checks
4. **OUTPUT** — Save to structured folder at `~/Documents/Claude/Mainframe/content-pipeline/[YYYY-MM-DD]-[topic-slug]/`
5. **DISTRIBUTION** — Include platform assignments, Dollar-a-Day candidates, publishing sequence

### Step 5: Create Manifest
Write manifest.md listing all pieces with status, type, title, file path, and platform target.

### Step 6: Create Source Reference
Write source.md linking to the original content location.

### Voice Requirements
- [Your Name]'s voice: direct, confident, grounded, not arrogant
- Sign-off: Use the sign-off defined in .personal/CONTEXT.md
- Reference [Your Mentor/Advisor] by name when quoting him
- Reference Content Factory methodology where relevant
- Anti-patterns: No jargon, no hype, no "in today's fast-paced world," no "let's dive in"

---

## Usage

Drop a transcript or content file into `~/Documents/Claude/Mainframe/inbox/` and run this prompt, or provide the file path directly.

**Example:** "Run the content pipeline on ~/Documents/Claude/Mainframe/inbox/podcast-interview-2026-03-25.vtt"
