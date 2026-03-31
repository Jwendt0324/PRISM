---
description: Set up and optimize an Obsidian vault as a visual interface for the PRISM knowledge system
category: file-management
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
canon_compliance: 10-anti-vandalism-checklist.md
triangles: [PPP]
triangles_served: [PPP]
human_gates: yes
canon_sources: [10-anti-vandalism-checklist.md]
tags: [type/sop, topic/system]
---

# Obsidian Vault Setup & Maintenance SOP

## Purpose
Configure and maintain the PRISM as a fully connected, visually navigable Obsidian vault for browsing, demoing, and auditing the knowledge system.

## When to Use
- First-time Obsidian setup for the PRISM
- After major PRISM restructuring (new folders, bulk file creation, SOP overhaul)
- When orphan files accumulate (new content campaigns, log rotation, new skills added)
- Before demoing the PRISM to clients, partners, or team members
- Quarterly vault health check

## Process

### Phase 1: Vault Configuration

1. Create `.obsidian/` directory inside `~/Documents/Claude/PRISM/` with these config files:
   - `app.json` — Set `useMarkdownLinks: true`, `newLinkFormat: "relative"`, `showFrontmatter: true`
   - `appearance.json` — Dark theme, base font 16px
   - `graph.json` — Color groups for each folder, physics tuned for clustering
   - `core-plugins.json` — Enable: file-explorer, global-search, graph, backlink, outgoing-link, tag-pane, outline, bookmarks, canvas
   - `bookmarks.json` — Organized into groups: Command Center, Visual Maps, Canon, Skills, Intelligence, Team, Active Content
   - `snippets/PRISM.css` — Folder icons, callout styling, dashboard formatting

2. Register the vault in Obsidian's config at `~/Library/Application Support/obsidian/obsidian.json` — add an entry with `"path": "/Users/[your-username]/Documents/Claude/PRISM"`.

3. Create `_Dashboard.md` at vault root as the home note with links to every major section.

### Phase 2: Cross-Linking (Connect Everything)

4. **Wire canon files forward** — Append `## See Also` sections to each `blitzmetrics-canon/` file linking to the SOPs and skills that implement it.

5. **Wire SOPs bidirectionally** — Append `## Related` sections to each SOP linking to: related SOPs, canon sources, corresponding skill, relevant memory-bank files.

6. **Wire skills bidirectionally** — Append `## Connected` sections to each skill linking to: canon, full SOP, related skills, memory-bank files.

7. **Wire memory-bank forward** — Append `## See Also` to each memory-bank file linking to SOPs and skills it informs.

8. **Wire team-ops** — Append `## See Also` to each team-ops file linking to related SOPs, memory-bank, and canon.

9. **Wire external skills** — Link each `SKILL.md` to its `references/` sub-files and back. Link each SKILL.md back to relevant PRISM skills/canon.

10. **Wire content artifacts** — Link campaign manifests to all articles, social posts, video scripts. Link each content file back to its manifest.

11. **Bulk-link auto-generated files** — Create INDEX.md files for log categories (conversations, sessions, archive, dream reports). Append `## See Also` linking every log file to its index. Use bash scripts for bulk operations:
    ```bash
    cd ~/Documents/Claude/PRISM/logs/conversations/2026-03
    for f in conversation-*.md; do
      if ! grep -q "See Also" "$f"; then
        printf '\n---\n## See Also\n- [Index](INDEX.md)\n' >> "$f"
      fi
    done
    ```

### Phase 3: Visual Polish

12. **Create Canvas boards** — Build `.canvas` files for key frameworks:
    - `_Content-Factory.canvas` — 6-stage pipeline flow
    - `_Nine-Triangles.canvas` — WHY/HOW/WHAT grid
    - `_KP-Sprint.canvas` — 4-week sprint workflow

13. **Add tags to frontmatter** — Tag key files with nested tags: `triangle/GCT`, `type/skill`, `type/canon`, `type/intel`, `topic/clients`, `status/active`.

14. **Tune graph aesthetics** — Use a monochromatic color palette (blue-violet range). Key settings:
    - `hideUnresolved: true`, `showOrphans: false` — clean graph
    - `textFadeMultiplier: -1.5` — labels on hover only
    - `nodeSizeMultiplier: 1.5`, `lineSizeMultiplier: 0.6` — big nodes, thin lines
    - `linkDistance: 40`, `repelStrength: 8` — tight clusters

### Phase 4: Verification

15. Run an orphan audit to confirm zero unlinked files:
    ```bash
    cd ~/Documents/Claude/PRISM
    find . -name "*.md" ! -path "./.obsidian/*" ! -path "./.backups/*" | while read f; do
      if ! grep -qE '\]\(' "$f"; then echo "$f"; fi
    done | wc -l
    ```

16. Relaunch Obsidian. Open Graph View (Cmd+G) and verify: all nodes connected, color groups distinct, no floating orphans.

## Quality Checks
- [ ] Zero orphan .md files (every file has at least one outgoing link)
- [ ] Graph view shows dense, interconnected clusters with clear color coding
- [ ] All canvas boards render correctly with file nodes resolving
- [ ] Bookmarks sidebar shows organized groups
- [ ] Tags appear in the Tags pane (right sidebar)
- [ ] Dashboard links all resolve (no broken links)

## Common Pitfalls
- **Obsidian overwrites graph.json** when you manually change graph settings in the UI. If colors reset, close Obsidian and rewrite the file, then reopen.
- **Relative paths must be exact.** A file in `sops/client-work/` links to canon with `../../blitzmetrics-canon/`, not `../blitzmetrics-canon/`. Count the directory depth.
- **Don't use wiki links `[[]]`.** The vault is configured for markdown links `[text](path.md)`. Mixing formats breaks backlink detection.
- **Bulk append scripts must check for existing sections.** Always `grep -q "See Also"` before appending or you'll get duplicate sections.
- **Canvas file references must match exact file paths.** If a referenced file doesn't exist, the node shows as unresolved.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| 14 | Review | Color palette and graph physics are subjective — human must verify visual appeal |
| 16 | Review | Final visual check of graph, canvas boards, and bookmarks before using in demos |

## Anti-Vandalism Checks
- **Check what already exists:** Before creating `.obsidian/` config, check if one exists. Before appending See Also sections, check if they already exist.
- **Verify internal link structure:** Run orphan audit (Step 15) to confirm no orphans created.
- **Preserve what's working:** Never modify existing file content — only append See Also/Related sections at the bottom.
- **Reference canonical source:** All links use existing file paths. Verify targets exist before adding links.
- **Don't link auto-generated noise:** Log files link to indexes, not to each other. KP book drafts link to progress-log, not cross-linked.

## Canon Compliance
- **Content Factory stage(s):** N/A — this is a system/infrastructure SOP
- **9 Triangles served:** PPP (People, Process, Platform) — this SOP builds the platform layer that makes all other processes visible and navigable
- **Canon documents:** `10-anti-vandalism-checklist.md` (don't break what exists when wiring links)
- **Last canon audit:** 2026-03-30

## Learnings Log
- **2026-03-30:** Obsidian reads `.obsidian/` config only on startup — must relaunch after config changes. Graph settings in UI overwrite graph.json.
- **2026-03-30:** Monochromatic color palette looks much better than rainbow. Multi-hue palettes look cluttered per user feedback.
- **2026-03-30:** Bulk bash scripts are 10x faster than agent-per-file for linking 300+ log/draft files. Use agents for complex cross-referencing, scripts for uniform append operations.
- **2026-03-30:** Canvas boards are high-impact for demos — create them for any framework that has a visual flow (pipeline, matrix, workflow).
- **2026-03-30 (retro):** Session 57d3307d launched 19 sub-agents for structural mapping and interconnection. This was effective for initial setup but overkill for maintenance. Future vault maintenance should use targeted scripts, not mass agent deployment. Tab names in Obsidian weren't displaying until user selected them — this appears to be an Obsidian rendering issue, not a config problem.

---

## See Also
- [[file-organization-rules|File Organization Rules]]
- [[logging-discipline|Logging Discipline]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Canon: Anti-Vandalism]]
- [[skills/PRISM-core|PRISM Core Skill]]
- [[_Dashboard|Dashboard]]
- [[skills/PRISM-core|PRISM Core]]
- [[_Dashboard|Dashboard]]
