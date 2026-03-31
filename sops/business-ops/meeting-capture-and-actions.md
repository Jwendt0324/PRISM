---
title: Meeting Capture & Action Items Processing
version: 1.0
last_updated: 2026-03-21
category: business-ops
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/meetings
canon_compliance: [maa-framework, human-requirements]
human_gates: [action item ownership, sending replies, relationship decisions]
---

# Meeting Capture & Action Items Processing

## Purpose
Turn meeting recordings into structured action items and deliverables within 2 hours of the meeting ending. Follow [[memory-bank/08-communication-patterns|Communication Patterns]] for channel-appropriate distribution.

## When to Use
- After any 1:1 with [Your Mentor/Advisor]
- After client calls
- After office hours
- After any meeting where commitments are made

## Process

### Step 1: Transcribe (5 minutes)
```bash
python3 -m whisper ~/Desktop/[recording].m4a --model base --language en --output_format txt --output_dir /tmp/whisper_out
```
- Whisper base model is cached and fast
- If medium model is needed (better accuracy), use `--model medium` but expect 3x longer runtime
- Save transcript to `~/Documents/Claude/PRISM/logs/meeting-transcripts/YYYY-MM-DD-[who].txt`

### Step 2: Extract Action Items (10 minutes)
Have Claude read the transcript and extract:
1. **Action items** — What was committed to, by whom, by when
2. **Decisions made** — What was decided and the reasoning
3. **Feedback received** — Specific critiques or direction changes
4. **Follow-ups needed** — Things to check on or respond to later

Format as a table:
| Action Item | Owner | Deadline | Status |
|---|---|---|---|
| Reply to New Hire thread | [Your Name] | Today | Not started |

### Step 3: Classify & Separate
- **Claude can do now:** Draft replies, build analyses, create documents, run searches
- **[Your Name] must do:** Send emails, make calls, relationship decisions, financial commitments
- **Behavioral changes:** Communication improvements, process changes (track but don't automate)

### Step 4: Execute What Claude Can Do
Run in parallel: draft replies, build reports, create deliverables. Save all outputs to Desktop or relevant project folder.

### Step 5: Track & Follow Up
- Save the action items list to `~/Documents/Claude/PRISM/logs/meeting-actions/YYYY-MM-DD-[who].md`
- Check off items as completed
- Roll uncompleted items into the next weekly review

## Quality Checks
- [ ] Every action item has an owner and deadline
- [ ] Behavioral items are separated from executable items
- [ ] Transcript saved for reference
- [ ] Deliverables are ready to use, not drafts of drafts

## Human Gates
- Action item ownership assignment requires human judgment
- Sending any reply or communication requires human review
- Relationship-sensitive decisions ([Your Mentor/Advisor] dynamics, client tension) require human decision

## Anti-Vandalism
- Never send a reply without human review
- Never commit to deadlines on behalf of [Your Name] without confirmation
- Save the original transcript — never delete it

## Learnings Log
- 2026-03-21: Created after [Your Mentor/Advisor] meeting (Mar 19) was transcribed and 10 action items extracted successfully. Process took ~25 minutes total including transcription.

---

## Related

- [Communication Protocol](../templates/team-ops/02-communication-protocol.md)
- [Meeting Cadence](../templates/team-ops/04-meeting-cadence.md)
- [Decision Rights Matrix](../templates/team-ops/03-decision-rights-matrix.md)

## See Also

- [[memory-bank/08-communication-patterns|Communication Patterns]]
- [[sops/templates/team-ops/04-meeting-cadence|Meeting Cadence]]
- [[sops/templates/team-ops/02-communication-protocol|Communication Protocol]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]