---
description: Pull podcast transcripts from Podbean RSS feeds using Whisper for local audio-to-text transcription
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
canon_compliance: 02-content-factory-process.md (Stage 2: Process)
triangles: CCS
canon_sources: [02-content-factory-process.md]
---

# Podcast Transcript Scraping (Podbean/RSS)

## Purpose
Download and transcribe podcast episodes from RSS feeds as part of the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] Process stage when YouTube transcripts are unavailable or when the client publishes audio-only content on Podbean.

## When to Use
- Client has a podcast on Podbean that needs transcripts pulled
- [Your Name] says "pull transcripts from [podcast name] on Podbean"
- YouTube channel has already been scraped and podcast episodes contain unique content not on YouTube

## Process

1. **Install dependencies.** Run `pip3 install openai-whisper requests` and `brew install ffmpeg`. Whisper **requires** ffmpeg to decode audio files.

2. **Fetch the RSS feed.** Podbean feeds follow this pattern: `https://feed.podbean.com/[show-name]/feed.xml`. Note: the `[show-name].podbean.com/feed.xml` URL may 302 redirect to the `feed.podbean.com` URL. Handle redirects or use the `feed.podbean.com` URL directly.

3. **Parse XML for episode data.** Extract from each `<item>`:
   - Episode title (from `<title>`)
   - Publish date (from `<pubDate>`)
   - Audio URL (from `<enclosure url="...">`)

4. **Save episode list** to `~/passive_income_transcripts/podbean_episode_list.txt` with format: `DATE | TITLE | AUDIO_URL`, one per line.

5. **Add SSL fix at top of script** if VPN is active:
   ```python
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   ```

6. **Download and transcribe each episode:**
   a. Download audio to `/tmp/episode.mp3` using `urllib.request.urlretrieve`
   b. Load Whisper model: `model = whisper.load_model("base")`
   c. Transcribe: `result = model.transcribe("/tmp/episode.mp3")`
   d. Save transcript to `~/[client]_transcripts/podbean/[DATE]_[SANITIZED_TITLE].txt`
   e. Delete temp audio file after transcription
   f. Log completion to progress file

7. **Save progress after each episode** to a JSON file. On restart, skip episodes already completed. This is critical because Whisper on CPU is slow (several minutes per episode).

8. **Run in background** with no timeout. 45 episodes took ~45 minutes on M-series Mac with Whisper base model on CPU.

9. **Cross-reference against YouTube transcripts** before writing articles. Many podcasts are audio versions of the same YouTube episodes. Compare titles to avoid duplicate articles.

## Quality Checks
- [ ] ffmpeg is installed before running (`which ffmpeg`)
- [ ] Progress file shows all episodes processed
- [ ] Failure log is empty or failures are explained
- [ ] Each transcript file has the 5-line header (Title, Date, Audio URL, Words, separator)
- [ ] Cross-referenced against existing YouTube transcripts for overlap

## Common Pitfalls

- **ffmpeg not installed.** Whisper silently fails or throws opaque errors without it. Always `brew install ffmpeg` first. This cost 45 minutes of debugging on the [Client Name] project.
- **Whisper FP16 warning on CPU.** "FP16 is not supported on CPU; using FP32 instead" is normal and harmless. It just means slower processing. Ignore it.
- **SSL cert errors behind VPN.** Add the `ssl._create_unverified_context` fix. This blocked the initial run of the [Client Podcast] scraper.
- **RSS feed pagination.** Some Podbean feeds only return 20-50 episodes. Check if there are `<link rel="next">` pagination links. The [Client Podcast] feed returned all 45 episodes without pagination.
- **Most podcast episodes duplicate YouTube content.** On the [Client Name] project, 44 of 45 Podbean episodes matched existing YouTube video transcripts. Always cross-reference before writing articles to avoid SEO cannibalization.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Initiation — [Your Name] specifies podcast and platform | Execute | Human decides which podcast to scrape and scope of work |
| Cross-reference against YouTube (Step 9) | Review | Determining duplicate vs. unique content requires human judgment |
| Article writing decisions from overlap analysis | Approve | [Your Name] decides which unique episodes are worth writing about |

## Anti-Vandalism Checks
- [ ] Cross-reference podcast episodes against existing YouTube transcripts before writing articles
- [ ] Progress file prevents re-processing on restart (no duplicate transcription work)
- [ ] 5-line header on every transcript ensures traceability to source
- [ ] Separate folders per client prevent mixing transcripts across projects

## Canon Compliance

- **Canon source:** 02-content-factory-process.md (Stage 2: Process) — podcast transcription is parallel to YouTube transcript scraping as a content processing step
- **Triangles served:** CCS — Content (podcast audio as raw input), Checklist (9-step process with cross-reference validation), Software (Whisper, ffmpeg, RSS parsing)
- **Human checkpoints:** [Your Name] initiates scraping by specifying podcast and platform; cross-referencing against YouTube transcripts requires human judgment on duplicate vs. unique content; article writing decisions based on overlap analysis
- **Anti-vandalism:** Progress file prevents re-processing on restart; 5-line header on every transcript ensures traceability; cross-reference step against YouTube prevents duplicate article creation and SEO cannibalization
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log

- **2026-03-18:** Whisper base model on CPU processes ~1 episode per minute for 30-minute episodes. Total time for 45 episodes was ~45 minutes.
- **2026-03-18:** The [Client Podcast] podcast (45 episodes) had 44/45 overlap with YouTube content. Only 1 unique episode ("How to Create Tax-Free Income for Life") had material not already covered. Always check overlap before committing to article writing.

---

## Related

- [Article Writing SOP](article-writing-from-transcripts.md)
- [Transcription Pipeline SOP](transcription-pipeline.md)
- [YouTube Transcript SOP](youtube-transcript-scraping.md)
- [Guest Appearance Research SOP](guest-appearance-research.md)
- [Canon: Content Factory Process](../../blitzmetrics-canon/02-content-factory-process.md)

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[skills/article-writer|Article Writer]]
- [[skills/content-factory|Content Factory Skill]]
