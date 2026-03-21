---
description: Monthly P&L reporting process for HRI and BlitzMetrics distribution tracking
category: business-ops
created: 2026-03-18
last_updated: 2026-03-20
version: 1.1
skill_linked: Yes
canon_compliance: 09-data-connections-needed.md
triangles: MOF
canon_sources: [09-data-connections-needed.md]
---

# P&L Reporting SOP

## Purpose
Establish consistent monthly P&L tracking so Dennis, Dylan, and Jack have clear visibility into HRI revenue, expenses, and distributions — eliminating the repeated asks for formal financial reporting.

## When to Use
- First week of every month (report due by the 5th)
- When Dennis or Dylan requests financial updates
- When evaluating whether to add a new tool or team member
- When preparing for quarterly strategy conversations

## Process

1. **Pull monthly revenue from Stripe.** Log into the HRI Stripe dashboard. Export all transactions for the prior month. Note gross revenue before fees.

2. **Categorize expenses into three buckets:**
   - **Tools:** ChatGPT (~$2,325/mo), Claude (~$200/mo), Descript, WP Engine, Basecamp, and any other active subscriptions. Check credit card statements — subscriptions creep.
   - **Team:** Muzamil ($674/week = ~$2,696/mo), Jackson (paid from Jack's comp), Hezekiah (per-invoice). Pull exact amounts from payment records.
   - **Platform:** 20% LSS revenue-share on applicable revenue.

3. **Calculate gross profit.** Gross profit = Monthly revenue - All direct expenses (tools + team + platform).

4. **Calculate net after distributions.** Net = Gross profit - BlitzMetrics 70% share - Jack's compensation. BlitzMetrics gets 70% of distributions. Document Jack's draw separately.

5. **Document in shared Google Sheet or Basecamp thread.** Use a consistent format: Revenue line, expense categories, gross profit, distributions, net. One tab/entry per month. Never overwrite prior months.

6. **Share with Dennis and Dylan by the 5th of each month.** Post in Basecamp and/or email. No exceptions on timing — this is the commitment Dennis asked for.

7. **Flag any month where expenses exceed revenue.** If the month is net negative, call it out explicitly in the report with a one-line explanation and recommended action.

## Quality Checks
- [ ] All Stripe transactions for the month are accounted for (cross-reference transaction count)
- [ ] Every expense is categorized into Tools, Team, or Platform — nothing left in "uncategorized"
- [ ] Report shared with Dennis and Dylan by the 5th
- [ ] No missing months in the running spreadsheet/thread

## Common Pitfalls
- **Tool subscriptions add up fast.** ChatGPT alone was $13,947 over 6 months. Audit the full tool stack monthly — don't assume last month's number is still right.
- **Refunds are expenses.** The Ed Strachar $1,494 refund must appear as an expense in the month it was processed, not hidden or netted against revenue.
- **Mixing personal and business expenses.** Keep HRI expenses on the HRI card/account. If a personal card was used, log it immediately or it gets lost.
- **Muzamil's cost is weekly, not monthly.** $674/week x number of weeks in the month. Some months have 5 pay periods.
- **LSS is functionally bankrupt.** Do not assume LSS account balances cover obligations. Track LSS-related revenue and expenses separately so the picture is clear.

## Canon Compliance

- **Canon source:** 09-data-connections-needed.md
- **Triangles served:** MOF (Finance — revenue tracking, expense categorization, distribution reporting)
- **Human checkpoints:** Jack approves refunds under $500; Jack + Dennis approve over $500; Dennis and Dylan receive report by 5th of each month; net-negative months require explicit flag and recommended action
- **Anti-vandalism:** Never overwrite prior months in the spreadsheet; refunds must appear as expenses (not netted); LSS tracked separately due to insolvency risk; all Stripe transactions cross-referenced by count
- **Last audited:** 2026-03-20 (BlitzMetrics Canon Alignment run)

## Learnings Log
- 2026-03-18: SOP created. HRI revenue since Jul 2025 is ~$50K total. Dennis has repeatedly requested formal P&L tracking — this formalizes the process.
