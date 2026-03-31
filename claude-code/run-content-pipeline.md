# Run Content Pipeline — Ready-to-Use Prompt

**Use this prompt to process new content through the Content Repurposing Pipeline.**

---

## Prompt

You are running the Content Repurposing Pipeline for [Your Name]'s Claude PRISM. Follow the pipeline SOP exactly.

### Step 1: Load the Pipeline SOP
Read `~/Documents/Claude/PRISM/sops/client-work/content-repurposing-pipeline.md` — this defines the full process, output matrix, voice requirements, and quality checks.

### Step 2: Identify the Source Content
The user will provide one of:
- A file path to a transcript, article, or notes
- A description of content to process
- A link or reference to content

Read the source content in full. Do not skim.

### Step 3: Check Viability
- Is this content publishable? (Not confidential, not internal-only, not someone else's copyrighted material)
- Check `~/Documents/Claude/PRISM/content-audit/00-executive-summary.md` for any flagged files
- If marked "No" or "Needs clarification" — skip or ask [Your Name]

### Step 4: Run the Pipeline
Follow the pipeline SOP process steps:
1. **INTAKE** — Extract core elements, determine Topic Wheel position, rate content richness
2. **PRODUCE** — Generate outputs across all 5 tiers (articles, social posts, video scripts, emails, SOP recommendations)
3. **QUALITY CHECK** — Run every output through the defined checks
4. **OUTPUT** — Save to structured folder at `~/Documents/Claude/PRISM/content-pipeline/[YYYY-MM-DD]-[topic-slug]/`
5. **DISTRIBUTION** — Include platform assignments, Dollar-a-Day candidates, publishing sequence

### Step 5: Create Manifest
Write manifest.md listing all pieces with status, type, title, file path, and platform target.

### Step 6: Create Source Reference
Write source.md linking to the original content location.

### Voice Requirements
- [Your Name]'s voice: direct, confident, grounded, not arrogant
- Sign-off: "Love Always, [Your Name]" on emails only
- Reference [Your Mentor/Advisor] by name when quoting him
- Reference Content Factory methodology where relevant
- Anti-patterns: No jargon, no hype, no "in today's fast-paced world," no "let's dive in"

---

## Usage

Drop a transcript or content file into `~/Documents/Claude/PRISM/inbox/` and run this prompt, or provide the file path directly.

**Example:** "Run the content pipeline on ~/Documents/Claude/PRISM/inbox/podcast-interview-2026-03-25.vtt"

---

## See Also
- [[skills/content-factory|Content Factory]]
- [[blitzmetrics-canon/02-content-factory-process|Content Factory Process]]
- [[skills/content-repurposing|Content Repurposing Skill]]
- [[skills/article-writer|Article Writer Skill]]
- [[sops/client-work/content-repurposing-pipeline|Content Repurposing Pipeline SOP]]
