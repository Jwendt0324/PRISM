---
description: Handle client refund requests with proper logging, approval, and root cause analysis
category: business-ops
created: 2026-03-18
last_updated: 2026-03-20
version: 1.1
tags:
  - type/sop
  - status/active
  - domain/business-ops
  - domain/finance
  - domain/client-ops
skill_linked: Yes
canon_compliance: 08-human-requirements.md
triangles: MOF, CID
canon_sources: [08-human-requirements.md]
---

# Refund & Escalation SOP

## Purpose
Ensure every refund request is handled quickly, documented properly, and analyzed for root cause — so no client has to ask "what happened to my refund?" again.

## When to Use
- A client requests a refund (email, Basecamp, verbal, or any channel)
- A service was not delivered as promised and refund is likely
- A payment dispute or chargeback appears in Stripe/SPP
- [Your Mentor/Advisor] or [Your Ops Partner] flags a client satisfaction issue requiring financial resolution

## Process

1. **Acknowledge the refund request within 24 hours.** Reply to the client (check [[memory-bank/04-client-directory|Client Directory]] for contact details) confirming you received the request and are reviewing it. Do not leave them waiting.

2. **Log the request immediately.** Record: date received, client name, amount, reason for refund, original payment method, and who submitted the request. Use a Basecamp thread or shared tracker.

3. **Pull original transaction details from SPP and Stripe.** Verify the charge amount, date, and payment method. Check for SPP/Stripe sync issues — they sometimes disconnect.

4. **Determine if the refund is warranted.** Review the service agreement. Did the client receive what was promised? Was the issue on [Your Agency]'s side or the client's? Document your assessment.

5. **Get approval.**
   - Under $500: [Your Name] approves.
   - Over $500: [Your Name] **and** [Your Mentor/Advisor] approve.
   - Document who approved and when.

6. **Check account balance before processing.** Verify the originating account ([Your Agency] Stripe, [Partner Platform], etc.) has sufficient funds. If not, escalate to [Your Mentor/Advisor] immediately — do not wait.

7. **Process the refund via original payment method.** Stripe refund is preferred. If Stripe refund is not possible, use Zelle.

8. **Know Zelle limits.** Zelle caps at $1,000/day for new recipients. If the refund exceeds $1,000, plan multi-day transfers and communicate the timeline to the client upfront.

9. **Offer to deliver the service anyway.** As a goodwill gesture, offer to do the session or service the client paid for — even after processing the refund. This preserves the relationship.

10. **Document the outcome in Basecamp.** Final entry in the thread: amount refunded, method, date processed, and whether the client accepted a goodwill service offer.

11. **Analyze root cause.** Why did this refund happen? Update onboarding, service delivery, or communication processes to prevent recurrence. If it's a systemic issue, flag it for the next strategy conversation with [Your Mentor/Advisor].

## Quality Checks
- [ ] Refund request logged within 24 hours of receipt
- [ ] Refund processed within 48 hours of approval
- [ ] Client notified at every stage (acknowledgment, processing, completion)
- [ ] Root cause documented and process improvement identified

## Common Pitfalls
- **Delay kills trust.** [Client Name] had to ask "what happened to my refund?" — that should never happen. Acknowledge immediately, even if you can't process immediately.
- **Insufficient account balance.** [Partner Platform] had no money when the [Client Name] refund was needed. [Your Mentor/Advisor] personally Zelle'd [$Amount]. Always check the balance **before** promising a timeline.
- **SPP/Stripe disconnect.** Transactions sometimes don't sync between SPP and Stripe. Check both systems to get the full picture.
- **Not offering service recovery.** A refund is a failure. Offering to deliver the service anyway turns a negative into a potential save. Always offer.
- **Forgetting to log it as an expense.** Every refund must appear in the monthly P&L report (see `pl-reporting.md`).

## Canon Compliance

- **Canon source:** 08-human-requirements.md
- **Triangles served:** MOF (financial controls, refund as expense in P&L), CID (client identity and relationship preservation)
- **Human checkpoints:** [Your Name] approves all refunds under $500; [Your Name] + [Your Mentor/Advisor] approve over $500; account balance verified before processing; client notified at every stage (acknowledgment, processing, completion)
- **Anti-vandalism:** 24-hour acknowledgment SLA; approval documented with who and when; refund logged as expense in monthly P&L; root cause analysis required for every refund; goodwill service offer preserves relationship
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log
- 2026-03-18: SOP created based on [Client Name] [$Amount] refund incident. Key lesson: ad hoc handling creates confusion and delays. Formalize immediately.

---

## Related

- [Client Communication SOP](../templates/team-ops/11-client-communication-sop.md)
- [Escalation Playbook](../templates/team-ops/12-escalation-playbook.md)
- [Canon: Human Requirements](../../blitzmetrics-canon/08-human-requirements.md)

## See Also

- [[memory-bank/04-client-directory|Client Directory]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[sops/business-ops/pl-reporting|P&L Reporting]]
- [[sops/templates/team-ops/12-escalation-playbook|Escalation Playbook]]
- [[sops/templates/sop-creation-template|SOP Creation Template]]