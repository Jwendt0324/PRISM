---
description: End-to-end process for onboarding a new client into the [Your Agency]/[Methodology Partner] system
category: client-work
created: 2026-03-18
last_updated: 2026-03-20
version: 1.2
skill_linked: Yes
canon_compliance: 02-content-factory-process.md (Stage 0: Plumbing)
triangles: GCT, CID
canon_sources: [02-content-factory-process.md, 11-gct-discovery-framework.md]
tags:
  - type/sop
  - status/active
  - domain/client-work
  - topic/onboarding
  - topic/client-setup
---

# Client Onboarding SOP

## Purpose
Ensure every new client is fully set up across all systems within the first week, with no gaps in access, communication, or reporting cadence.

## When to Use
- A new client signs an engagement with [Your Agency] or [Methodology Partner]
- A client re-engages after a pause and needs systems re-provisioned
- Transitioning a prospect to active client status after payment

## Process

1. **Have the client fill out the [[blitzmetrics-canon/11-gct-discovery-framework|GCT]] (Goal, Content, Targeting) form.** This captures their business goals, existing content assets, and target audience. Do not proceed until GCT is complete — it drives everything downstream.

2. **Set up access permissions via `[methodology-partner.com]/acl`.** [Your Repurposing Specialist] team members appropriate access to the client's ad accounts, analytics, social pages, and any other platforms. Document all access in the Basecamp Access thread (Step 4).

3. **Create a shared Google Drive folder.** Follow the process at `[methodology-partner.com]/share`. Structure the folder with subfolders for: Content, Analytics, Creative Assets, Reports. Share with the client and all assigned team members.

4. **Create a Basecamp project with standard threads:**
   a. **Updates** — Client-visible. Weekly MAA reports go here.
   b. **Access** — Client-visible. All login credentials, permissions, and platform access documented here.
   c. **Meetings** — Client-visible. Meeting notes, agendas, and recordings.
   d. **Internal** — Team-only. Strategy discussions, internal notes, escalations. **Do not invite the client to this thread.**
   e. Invite the client to the Basecamp project. Confirm they can see Updates, Access, and Meetings threads.

5. **Run an initial SEO/YouTube/content inventory analysis.** Audit current rankings, YouTube channel performance (if applicable), existing content library, and social presence. Document findings in the Internal thread and summarize key points for the client in Updates.

6. **Set up the weekly [[blitzmetrics-canon/05-maa-framework|MAA]] cadence.** MAA reports are due every **Friday**. Add a recurring reminder. See `~/Documents/Claude/PRISM/sops/client-work/weekly-maa-report.md` for MAA format.

7. **Deliver the first MAA report within 1 week of onboarding.** This establishes the reporting rhythm immediately and sets expectations. Do not let the first week pass without a report — even if it is primarily baseline metrics.

## Quality Checks
- [ ] All platform access granted and documented in Access thread
- [ ] Google Drive folder created, structured, and shared with client + team
- [ ] Basecamp project created with all 4 threads (Updates, Access, Meetings, Internal)
- [ ] Client invited to Basecamp and confirmed visible on client-facing threads
- [ ] Initial analysis complete and posted to Internal thread
- [ ] MAA cadence set (Fridays) and first MAA delivered within 1 week

## Common Pitfalls
- **Forgetting the Internal thread.** Every Basecamp project needs a team-only Internal thread. If you skip it, sensitive strategy discussions end up in client-visible threads or get lost in Slack/DMs.
- **Not setting the MAA cadence from day 1.** If you wait until "things settle in" to start reporting, weeks slip. Set the Friday cadence during onboarding and deliver the first MAA within 7 days.
- **Client chasing for updates.** If the client has to ask "what's happening?" you've already failed. The Ryan D. Lee lesson: proactive communication prevents client anxiety. Post updates before they ask.

## Human Gates
| Step | Gate Type | Reason |
|------|-----------|--------|
| GCT form completion (Step 1) | Execute | Client must articulate goals, content, and targeting themselves |
| Access permissions setup (Step 2) | Execute | Team verifies all platform access is granted and documented |
| Client Basecamp invitation (Step 4e) | Review | Confirm client can see correct threads (not Internal) |
| Initial analysis delivery (Step 5) | Review | Human judgment on what findings to share with client vs. keep internal |
| First MAA delivery (Step 7) | Execute | Human writes and delivers first MAA within 1 week |

## Anti-Vandalism Checks
- [ ] Verify Internal thread is NOT visible to client before inviting them to Basecamp
- [ ] Confirm no duplicate Basecamp projects exist for this client
- [ ] Verify all platform access is documented in Access thread (not scattered in DMs/Slack)
- [ ] Confirm MAA cadence is set from Day 1 (not deferred)

## Canon Compliance

- **Canon source:** 02-content-factory-process.md (Stage 0: Plumbing) — client onboarding IS the plumbing stage: setting up access, systems, and reporting before any content production begins
- **Triangles served:** GCT (first step) — the GCT form IS Step 1 of the process, capturing Goals, Content inventory, and Targeting before anything else; CID — the entire process is Communicate (Basecamp threads, welcome emails), Iterate (initial analysis feeds first MAA), Delegate (access permissions, team assignments)
- **Human checkpoints:** Client fills out GCT form personally; team access permissions verified by human; client invited to Basecamp and confirmed visible; first MAA delivered and reviewed within 1 week
- **Anti-vandalism:** GCT form gates all downstream work (no form = no progress); Internal thread separated from client-visible threads prevents accidental exposure; MAA cadence set from Day 1 prevents reporting gaps; proactive communication prevents client anxiety (Ryan D. Lee lesson)
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log
- *2026-03-18* — SOP created based on [Your Agency]/[Methodology Partner] onboarding patterns and documented lessons from Ryan D. Lee engagement.

---

## Related

- [Weekly MAA Report SOP](weekly-maa-report.md)
- [Content Factory SOP](content-factory-execution.md)
- [Prospect Follow-Up SOP](prospect-followup.md)
- [Canon: GCT Discovery](../../blitzmetrics-canon/11-gct-discovery-framework.md)
- [Canon: Human Requirements](../../blitzmetrics-canon/08-human-requirements.md)
- [Team: New Hire Onboarding](../templates/team-ops/06-new-hire-onboarding-sop.md)
- [Client Directory](../../memory-bank/04-client-directory.md)
- [Tool Stack](../templates/team-ops/09-tool-stack-and-access.md)

## See Also

- [[blitzmetrics-canon/02-content-factory-process|Content Factory]]
- [[blitzmetrics-canon/11-gct-discovery-framework|GCT Discovery]]
- [[blitzmetrics-canon/05-maa-framework|MAA Framework]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[skills/prospect-followup|Prospect Follow-Up]]
- [[skills/weekly-maa-report|Weekly MAA Report Skill]]
- [[memory-bank/04-client-directory|Client Directory]]