---
title: Transcription Pipeline — Multi-Source Audio/Video to Text
version: 1.0
last_updated: 2026-03-21
category: client-work
canon_compliance: [content-factory-process, human-requirements]
human_gates: [transcript accuracy review, source selection]
---

# Transcription Pipeline

## Purpose
Convert any audio/video source (YouTube, podcasts, meetings, uploads) into clean transcripts ready for the [[skills/article-writer|article writing]] pipeline as part of the [[blitzmetrics-canon/02-content-factory-process|Content Factory]] Process stage.

## When to Use
- Before writing articles from video/podcast content
- After recording meetings or calls
- When a client provides raw video for repurposing

## Method Priority Matrix

| Source | Method | Speed | Accuracy | Cost |
|---|---|---|---|---|
| YouTube (with captions) | yt-dlp --write-auto-sub | Fast (seconds) | 85-90% | Free |
| YouTube (no captions) | yt-dlp download + Whisper | Medium (5min/hour of audio) | 90-95% | Free |
| Podcast (Podbean/Apple/Spotify) | Download MP3 + Whisper | Medium | 90-95% | Free |
| Meeting recording (.m4a/.mp4) | Whisper directly | Medium | 90-95% | Free |
| Low-quality audio | Whisper medium model | Slow (15min/hour) | 95%+ | Free |

**Always try the fastest method first. Fall back to Whisper only when auto-subs aren't available or are low quality.**

## Process

### YouTube Transcripts
```bash
# Method 1: Auto-subs (preferred — fastest)
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "%(title)s" [URL]

# Method 2: Download audio + Whisper (fallback)
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" [URL]
python3 -m whisper "file.mp3" --model base --language en --output_format txt
```

### Podcast Transcripts
```bash
# Download the MP3 from feed URL or website
curl -o episode.mp3 [DIRECT_MP3_URL]

# Transcribe with Whisper
python3 -m whisper episode.mp3 --model base --language en --output_format txt

# Clean up audio after transcription
rm episode.mp3
```

### Meeting Recordings
```bash
python3 -m whisper ~/Desktop/recording.m4a --model base --language en --output_format txt --output_dir /tmp/whisper_out
```

### Batch Processing (10+ videos)
```bash
# Create a file with one URL per line
cat urls.txt | while read url; do
    yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcripts/%(title)s" "$url"
done
```

**Rate limiting note:** YouTube blocks after 20-40 requests. If hitting limits:
- Add 5-second delays between requests
- Or use the VPN rotation approach (Proton VPN MCP)
- Or request API rate limit increase from Google ([Your Mentor/Advisor] has contacts)

## Output Format
- Save transcripts to: `~/Documents/Claude/PRISM/content-pipeline/[client-name]/transcripts/`
- One file per video/episode
- Filename: `[title-slug].txt`
- Include source URL as first line of transcript

## Quality Checks
- [ ] Transcript is at least 500 words (if shorter, source may not have real content)
- [ ] Speaker names are identified (if multi-speaker)
- [ ] No garbled sections longer than 2 sentences
- [ ] Source URL documented

## Human Gates
- Transcript accuracy should be spot-checked by a human (especially for technical terms)
- Source selection (which videos to transcribe) requires human judgment

## Anti-Vandalism
- Never delete source audio/video until transcript is verified
- Never overwrite an existing transcript without renaming the old one

## Learnings Log
- 2026-03-21: Whisper base model is cached on [Your Name]'s Mac and runs well for most content. Medium model needed only for low-quality audio or heavy accents.
- 2026-03-21: YouTube auto-subs are available on ~70% of videos. Always try auto-subs first.

---

## Related

- [Article Writing SOP](article-writing-from-transcripts.md)
- [YouTube Transcript SOP](youtube-transcript-scraping.md)
- [Podcast Transcript SOP](podcast-transcript-scraping.md)
- [Canon: Content Factory Process](../../blitzmetrics-canon/02-content-factory-process.md)

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[skills/article-writer|Article Writer]]
- [[skills/content-factory|Content Factory Skill]]
