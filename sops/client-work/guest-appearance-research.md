---
description: Find and scrape a client's guest appearances on other YouTube channels and podcasts for article source material
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
canon_compliance: 06-topic-wheel.md
triangles: ACC
canon_sources: [06-topic-wheel.md]
---

# Guest Appearance Research & Scraping

## Purpose
Find every YouTube and podcast guest appearance for a client, pull transcripts, and create articles that build authority signals and E-E-A-T through third-party association.

## When to Use
- A client's own channel transcripts have been exhausted
- [Your Name] wants guest appearance articles for SEO/authority building
- Building out the "[KP Sprint Client] on [Podcast Name]" style recap articles
- Searching for third-party proof points and quotes for existing articles

## Process

1. **Search YouTube via browser automation.** Open Chrome and run these search queries (replace `[CLIENT NAME]` with the client's name):
   - `"[CLIENT NAME]" financial freedom` (or their core topic)
   - `"[CLIENT NAME]" interview`
   - `"[CLIENT NAME]" podcast`
   - `"[CLIENT NAME]" guest`
   - `"[CLIENT NAME]" [their company/brand name]`
   - `"[CLIENT NAME]" [key topic 1]`

2. **For each search result page,** use JavaScript extraction to pull video IDs, titles, and channel names:
   ```javascript
   document.querySelectorAll('ytd-video-renderer').forEach(el => {
       const title = el.querySelector('#video-title')?.textContent?.trim();
       const channel = el.querySelector('ytd-channel-name')?.textContent?.trim();
       const href = el.querySelector('#video-title')?.getAttribute('href');
       // Extract video ID from href
   });
   ```

3. **Filter OUT the client's own channels.** Remove any videos from channels owned by the client. Keep only videos where the client appears as a **guest** on someone else's platform.

4. **Supplement with web search.** Search for `"[CLIENT NAME]" guest episode podcast youtube [year]` to catch appearances not surfaced by YouTube search.

5. **Save the URL list** to `~/[client]-articles/[client]_guest_youtube_urls.txt`:
   ```
   [URL] | [Channel Name] | [Video Title]
   ```

6. **Pull transcripts** using the same yt-dlp method from the YouTube Transcript Scraping SOP. Use the `fetch_transcript()` function with `cookiesfrombrowser: ("chrome",)`.

7. **Write articles from guest transcripts.** These articles have a different angle than own-channel articles:
   - Frame as "[KP Sprint Client] on [Podcast Name]: [Key Insight]"
   - Emphasize what the host asked and what the client revealed
   - Include the host's reactions and follow-up questions as social proof
   - Link to both the client's site AND the host's platform

8. **Save summary** to `~/[client]-articles/[client]_guest_appearances_summary.txt` showing total found, channels, transcript status.

## Quality Checks
- [ ] Client's own channels are completely filtered out
- [ ] Every found appearance has a transcript or documented reason for failure
- [ ] URL list is saved with channel names for attribution
- [ ] Guest appearance articles have a different angle than own-channel articles

## Common Pitfalls

- **Clients have fewer guest appearances than expected.** [KP Sprint Client] had only 4 YouTube guest appearances across 6 search queries. Most creators publish primarily on their own channels. Don't promise a specific number before searching.
- **Some podcast appearances exist only on Spotify/Buzzsprout with no YouTube version.** The [Guest Appearance Host] (Blueprint Podcast) and [Guest Appearance Host] (As The Leader Grows) episodes with [KP Sprint Client] were audio-only. Flag these and offer to scrape audio via RSS if the client wants them.
- **YouTube search results change with VPN.** Different VPN servers return different results. Run searches both with and without VPN for maximum coverage.
- **Browser automation can trigger dialog boxes.** Avoid clicking anything that might trigger a JavaScript alert. Use `navigate` and `javascript_tool` instead of `computer` clicks when possible.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Search scope definition | Execute | [Your Name] specifies client name and search parameters |
| Filtering out client's own channels (Step 3) | Review | Distinguishing own vs. guest channels requires human judgment |
| Article angle for guest appearances (Step 7) | Review | Guest articles need different framing than own-channel content — editorial direction required |
| Audio-only episode decision | Approve | [Your Name] decides whether to invest time scraping audio-only appearances |

## Anti-Vandalism Checks
- [ ] URL list saved with channel names for attribution audit
- [ ] Every appearance has a transcript or documented reason for failure
- [ ] Cross-reference guest appearance topics against existing articles to avoid duplication
- [ ] Guest articles use distinct framing from own-channel articles (not generic rewrites)

## Canon Compliance

- **Canon source:** 06-topic-wheel.md — guest appearances build authority around the client's Topic Wheel themes through third-party association
- **Triangles served:** ACC (authority building) — guest appearances create Awareness (third-party audience exposure), build Consideration (E-E-A-T signals from host endorsement), and support Conversion (backlinks and social proof driving site traffic)
- **Human checkpoints:** [Your Name] initiates research by specifying client name and search scope; filtering out client's own channels requires human judgment; article angle for guest appearances differs from own-channel content and needs human editorial direction
- **Anti-vandalism:** URL list saved with channel names for attribution audit; every appearance must have a transcript or documented failure reason; guest articles require different framing than own-channel articles to prevent generic output
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log

- **2026-03-18 ([KP Sprint Client]):** Found 4 guest appearances: Limitless Grit, [Guest Appearance Host], Richardson Law Offices, [Guest Appearance Host]. All 4 transcripts pulled successfully via yt-dlp with Chrome cookies.
- **2026-03-18:** Browser automation for YouTube search works but is slow (6 queries took ~5 minutes with waits). Web search (`WebSearch` tool) is faster for initial discovery, then confirm with direct YouTube URL checks.
