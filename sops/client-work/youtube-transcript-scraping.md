---
description: Pull YouTube video transcripts at scale using yt-dlp Python API with browser cookies and VPN rotation
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
canon_compliance: 02-content-factory-process.md (Stage 2: Process)
triangles: CCS
canon_sources: [02-content-factory-process.md]
---

# YouTube Transcript Scraping

## Purpose
Extract transcripts from YouTube channels in bulk, organized by view count, for use as source material in the [[skills/article-writer|article writing]] pipeline. This is a core step in the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] Process stage.

## When to Use
- A new client needs articles written from their YouTube content
- [Your Name] says "pull transcripts from [channel name]"
- A new batch of videos needs to be scraped from an existing client's channel
- Guest appearances on other channels need to be found and scraped

## Process

1. **Install dependencies.** Run `pip3 install yt-dlp youtube-transcript-api` if not already available. Verify with `python3 -c "import yt_dlp; print('ready')"`.

2. **Create the scraper script.** Use yt-dlp as a **Python library** (not CLI subprocess). Key config:
   ```python
   ydl_opts = {
       "extract_flat": "in_playlist",
       "quiet": True,
       "nocheckcertificate": True,
   }
   ```
   Target the channel's `/videos` tab: `CHANNEL_URL + "/videos"`.

3. **Sort by view count, slice by rank.** After extracting the flat playlist, sort `videos` by `view_count` descending and take the target slice (e.g., top 200, ranks 201-400).

4. **Fetch transcripts using yt-dlp subtitle download** (not youtube-transcript-api, which gets IP-blocked fast). Key config:
   ```python
   ydl_opts = {
       "skip_download": True,
       "writesubtitles": True,
       "writeautomaticsub": True,
       "subtitleslangs": ["en.*"],
       "subtitlesformat": "best",
       "ignore_no_formats_error": True,
       "nocheckcertificate": True,
       "cookiesfrombrowser": ("chrome",),
   }
   ```

5. **Parse subtitle files.** Handle both VTT and json3 formats. Strip HTML tags, timestamps, and duplicate lines. Deduplicate text segments using a `seen` set.

6. **Save each transcript** to `~/[client]_transcripts/` as a `.txt` file with this header:
   ```
   Title: [video title]
   Views: [view count]
   Rank: #[N] most viewed
   Video ID: [id]
   URL: https://youtube.com/watch?v=[id]
   Source: [manual|auto-generated]
   [google-doc-id]
   [transcript text]
   ```

7. **Build resume support.** Save progress to a JSON log file after every video. On restart, skip videos already in the log with status `manual` or `auto-generated`.

8. **Apply word count minimums** when specified. If [Your Name] says "at least 2000 words," check `len(text.split())` before saving and log short transcripts as `too_short`.

9. **Run in background.** Use `run_in_background` so there is no timeout. Check progress via the log file: `python3 -c "import json; d=json.load(open('log.json')); print(f'Done: {sum(1 for v in d.values() if v[\"status\"] in (\"manual\",\"auto-generated\"))}')"`.

10. **Use separate folders per batch.** Never mix batches. Naming: `~/[client]_transcripts/` for batch 1, `~/[client]_transcripts_batch2/` for batch 2, etc.

## Quality Checks
- [ ] Every saved transcript has the 6-line header (Title, Views, Rank, Video ID, URL, Source)
- [ ] Log file shows 0 blocked, 0 errors (or errors are explained)
- [ ] File count matches "saved" count in the log
- [ ] No duplicate video IDs in the log

## Common Pitfalls

- **youtube-transcript-api gets IP-blocked fast.** Do not use it for bulk scraping. Use yt-dlp's subtitle download instead. This was learned the hard way on the [Client — Local Retail Business] project (190/200 blocked).
- **yt-dlp CLI command not found on Mac.** Always use `import yt_dlp` as a Python library, never `subprocess.run(["yt-dlp", ...])`. The CLI binary doesn't install to PATH reliably.
- **SSL certificate errors behind VPN.** Add `import ssl; ssl._create_default_https_context = ssl._create_unverified_context` at the top of the script if ProtonVPN is active.
- **"Requested format is not available" error.** Add `"ignore_no_formats_error": True` to ydl_opts. This happens on music/performance videos with no standard formats but the subtitles are still downloadable.
- **YouTube 429 rate limiting.** If blocked, tell [Your Name] to switch VPN IP. The script's resume support means no work is lost. Use 2-second delay between requests (`DELAY_SEC = 2`).
- **`extract_flat: True` returns channel tabs, not videos.** Use `"extract_flat": "in_playlist"` and target `CHANNEL_URL + "/videos"` to get individual video entries.
- **ffmpeg required for Whisper.** If transcribing audio (Podbean/podcast), install via `brew install ffmpeg` before running Whisper.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Initiation — [Your Name] specifies channel and batch parameters | Execute | Human decides which channel, batch size, and rank range to scrape |
| VPN IP switching when rate-limited | Execute | [Your Name] manually switches ProtonVPN IP — script resumes automatically |
| Word count minimum definition | Execute | Human sets per-project threshold (e.g., 2000 words for article-quality transcripts) |

## Anti-Vandalism Checks
- [ ] Resume support via JSON log prevents data loss on interruption
- [ ] 6-line header on every transcript ensures traceability to source video
- [ ] Separate folders per batch prevent mixing (never overwrite prior batches)
- [ ] No duplicate video IDs in the log file
- [ ] Cross-reference transcript topics against existing articles before writing

## Canon Compliance

- **Canon source:** 02-content-factory-process.md (Stage 2: Process) — transcript scraping is the first step in processing raw video content into written articles
- **Triangles served:** CCS — this SOP is a pure checklist/software process: Content (YouTube videos as raw input), Checklist (10-step scraping process with quality gates), Software (yt-dlp, Python, VPN tooling)
- **Human checkpoints:** [Your Name] initiates scraping by specifying channel and batch parameters; [Your Name] switches VPN IP when rate-limited; word count minimums are human-defined per project
- **Anti-vandalism:** Resume support via JSON log prevents data loss on interruption; 6-line header on every transcript ensures traceability; separate folders per batch prevent mixing; log file tracks every video status for audit
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log

- **2026-03-18:** youtube-transcript-api is unreliable for bulk. Switched entirely to yt-dlp subtitle download with Chrome cookies. Zero blocks on 400 [Client — Local Retail Business] videos.
- **2026-03-18:** VPN rotation is the fastest fix for 429s. [Your Name] can switch IPs in ProtonVPN and the resume-supported script picks up instantly.
- **2026-03-18:** Batch 3 ([Client — Local Retail Business] ranks 401+) added a 2000-word minimum filter. This is a good default for article-quality transcripts. Performance/jam videos produce transcripts under 500 words that can't become real articles.

---

## Related

- [Article Writing SOP](article-writing-from-transcripts.md)
- [Transcription Pipeline SOP](transcription-pipeline.md)
- [Podcast Transcript SOP](podcast-transcript-scraping.md)
- [Canon: Content Factory Process](../../blitzmetrics-canon/02-content-factory-process.md)

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[skills/article-writer|Article Writer]]
- [[skills/content-factory|Content Factory Skill]]
