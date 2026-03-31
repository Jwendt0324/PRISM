---
description: End-to-end onboarding flow for new AI Apprentice Program participants, from qualification to first MAA
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
skill_linked: Yes
canon_compliance: 01-nine-triangles.md
triangles: LDT, SBP, GCT
canon_sources: [01-nine-triangles.md, 11-gct-discovery-framework.md, 12-ldt-implementation-guide.md]
tags:
  - type/sop
  - status/active
  - domain/client-work
  - topic/onboarding
  - topic/ai-apprentice
---

# AI Apprentice Onboarding SOP

## Purpose
Ensure every new AI Apprentice is properly qualified, provisioned across all systems, and producing their first MAA within one week of payment.

## When to Use
- A new prospect expresses interest in the AI Apprentice Program
- An apprentice completes payment and needs system provisioning
- Re-onboarding an apprentice who lapsed and is re-enrolling

## Process

### Qualification (Pre-Payment)

1. **Assign the qualification task.** The prospect must repurpose the latest Marketing Mechanic video into:
   a. A written article (no AI-sounding language — must read as human-written)
   b. A 1-minute video summarizing the key points
   c. Post both to the Facebook group
   - **All three deliverables are required.** Do not bypass this step. The [Your Content Specialist] lesson: [Your Mentor/Advisor] will push back hard if someone is admitted without meeting all qualification criteria.

2. **Review the deliverables.** Check for AI language patterns (generic phrasing, overly polished structure, no personal voice). If the article reads like ChatGPT output, send it back for revision.

### Payment & Automated Provisioning

3. **Process payment via Stripe.** Payment triggers the Zapier automation chain:
   a. Zapier creates or updates a **Keap contact** with Academy access tags
   b. Zapier creates an **SPP client record**
   c. Zapier auto-creates a **Basecamp project** from the standard template (6 sections)

4. **Verify the Zapier automations fired correctly.** Check that all three systems (Keap, SPP, Basecamp) have the new apprentice's records. If any step failed, manually create the missing records.

### Manual Setup

5. **[Your Ops Admin] sends Academy credentials.** The apprentice gets login access to `academy.[content-platform.com]`. Confirm credentials are sent within 24 hours of payment.

6. **Keap sends the welcome email sequence:**
   a. Welcome video from [Your Mentor/Advisor]
   b. Academy login credentials
   c. Onboarding article (how to get started)
   d. Free training videos
   - Verify the sequence is triggering. If emails are not sending, check the Keap automation tags.

7. **Invite the apprentice to the weekly Thursday session.**
   - Time: **2pm PST every Thursday**
   - Zoom ID: **895 4884 7054**
   - Add them to the calendar invite or recurring Zoom registration.

8. **Set the first MAA deadline.** The apprentice's first [[blitzmetrics-canon/05-maa-framework|MAA]] report is due **within 1 week of onboarding**. Communicate this clearly — it is their first accountability checkpoint. See `~/Documents/Claude/PRISM/sops/client-work/weekly-maa-report.md` for MAA format.

### Engagement Monitoring (Ongoing)

9. **Monitor MAA submissions weekly.** Track whether each apprentice is submitting their Friday MAA:
   - **1 week missed:** Ops team sends a follow-up message. Ask if they need help, identify blockers.
   - **2 weeks missed:** Escalate to [Your Name] or [Your Mentor/Advisor]. Direct outreach to the apprentice.
   - **3+ months inactive:** Contact the apprentice's parent or sponsor if applicable. The Morgan Gopaul case: long-inactive apprentices do not self-recover — someone else needs to intervene.

## Quality Checks
- [ ] Qualification task completed with all 3 deliverables (article, video, Facebook post) — no exceptions
- [ ] Basecamp project created with 6 standard sections
- [ ] Academy access confirmed at `academy.[content-platform.com]`
- [ ] Apprentice added to Thursday Zoom (2pm PST, ID: 895 4884 7054)
- [ ] First MAA submitted within 1 week of onboarding
- [ ] Engagement monitoring active (weekly MAA check)

## Common Pitfalls
- **Admitting apprentices who did not complete all qualification criteria.** The [Your Content Specialist] lesson: [Your Mentor/Advisor] pushed back when qualification standards were bypassed. The qualification task is the filter — it proves the apprentice can execute. Do not shortcut it.
- **AI language in the initial article.** If the qualification article reads like raw AI output, the apprentice is not demonstrating the skill. Send it back. The whole point of the program is human-directed AI, not AI-generated slop.
- **Inactive apprentices not caught early.** If you wait until someone has been silent for 3 months, recovery is nearly impossible. The weekly MAA check catches disengagement at 1 week, not 3 months. Follow the escalation ladder.
- **Zapier automation failures going unnoticed.** Always verify Keap, SPP, and Basecamp records exist after payment. Automation is not a guarantee — spot-check every new onboard.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| Qualification task review (Step 2) | Review | Human must assess article for AI language patterns — subtle AI tells require trained eye |
| [Your Mentor/Advisor] approval before admission | Approve | The [Your Content Specialist] lesson — [Your Mentor/Advisor] must sign off on every new apprentice |
| Weekly MAA review (Step 9) | Review | Ops team evaluates MAA quality and engagement weekly |
| Escalation at 2+ weeks inactive | Execute | Direct human outreach required — disengaged apprentices don't self-recover |

## Anti-Vandalism Checks
- [ ] Verify qualification task includes all 3 deliverables before admitting (no exceptions)
- [ ] Confirm Zapier automations fired correctly after payment (check Keap, SPP, Basecamp)
- [ ] Verify no duplicate Basecamp projects or Keap contacts exist for the same apprentice
- [ ] Confirm Academy credentials were actually sent (not just triggered)

## Canon Compliance

- **Canon source:** 01-nine-triangles.md — the apprentice program embodies [[blitzmetrics-canon/12-ldt-implementation-guide|Learn-Do-Teach]] as its core pedagogy
- **Triangles served:** LDT — apprentices Learn via Marketing Mechanic video repurposing, Do via qualification task execution and weekly MAA reports, Teach via content creation and community contribution; SBP — program scoped to Specialist (apprentices learning the craft), with pathway to Business and Partner tiers; GCT — qualification task tests all three: Goals (can they identify the key points?), Content (can they create an article and video?), Targeting (can they post to the right audience in the Facebook group?)
- **Human checkpoints:** Qualification review — human must assess article for AI language patterns; [Your Mentor/Advisor] approval required before admission (the [Your Content Specialist] lesson); weekly MAA review by ops team; escalation ladder at 1 week, 2 weeks, 3+ months inactive
- **Anti-vandalism:** Three-deliverable qualification gate (article + video + Facebook post) prevents unqualified admissions; Zapier automation verified manually after every payment; weekly MAA submission tracking catches disengagement at 1 week, not 3 months
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log
- *2026-03-18* — SOP created based on AI Apprentice Program operations, [Your Content Specialist] qualification incident, and Morgan Gopaul engagement recovery case.

---

## Related

- [Client Onboarding SOP](client-onboarding.md)
- [Weekly MAA Report SOP](weekly-maa-report.md)
- [Canon: LDT Implementation](../../blitzmetrics-canon/12-ldt-implementation-guide.md)
- [Canon: Human Requirements](../../blitzmetrics-canon/08-human-requirements.md)
- [Team Directory](../../memory-bank/03-team-directory.md)

## See Also

- [[blitzmetrics-canon/01-nine-triangles|Nine Triangles]]
- [[blitzmetrics-canon/12-ldt-implementation-guide|LDT Guide]]
- [[blitzmetrics-canon/11-gct-discovery-framework|GCT Discovery]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[skills/weekly-maa-report|Weekly MAA Report Skill]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[memory-bank/04-client-directory|Client Directory]]