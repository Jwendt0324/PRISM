---
description: Monthly P&L reporting process for [Your Agency] and [Methodology Partner] distribution tracking
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
Establish consistent monthly P&L tracking so [Your Mentor/Advisor], [Your Ops Partner], and [Your Name] have clear visibility into [Your Agency] revenue, expenses, and distributions — eliminating the repeated asks for formal financial reporting.

## When to Use
- First week of every month (report due by the 5th)
- When [Your Mentor/Advisor] or [Your Ops Partner] requests financial updates
- When evaluating whether to add a new tool or team member
- When preparing for quarterly strategy conversations

## Process

1. **Pull monthly revenue from Stripe.** Log into the [Your Agency] Stripe dashboard. Export all transactions for the prior month. Note gross revenue before fees.

2. **Categorize expenses into three buckets:**
   - **Tools:** ChatGPT (~$2,325/mo), Claude (~$200/mo), Descript, WP Engine, Basecamp, and any other active subscriptions. Check credit card statements — subscriptions creep.
   - **Team:** [Your Ops Admin] ([$X/week = ~$X/mo]), [Your Content Specialist] (paid from [Your Name]'s comp), [Your Automation Lead] (per-invoice). Pull exact amounts from payment records.
   - **Platform:** 20% [Partner Platform] revenue-share on applicable revenue.

3. **Calculate gross profit.** Gross profit = Monthly revenue - All direct expenses (tools + team + platform).

4. **Calculate net after distributions.** Net = Gross profit - [Methodology Partner] 70% share - [Your Name]'s compensation. [Methodology Partner] gets 70% of distributions. Document [Your Name]'s draw separately.

5. **Document in shared Google Sheet or Basecamp thread.** Use a consistent format: Revenue line, expense categories, gross profit, distributions, net. One tab/entry per month. Never overwrite prior months.

6. **Share with [Your Mentor/Advisor] and [Your Ops Partner] by the 5th of each month.** Post in Basecamp and/or email. No exceptions on timing — this is the commitment [Your Mentor/Advisor] asked for.

7. **Flag any month where expenses exceed revenue.** If the month is net negative, call it out explicitly in the report with a one-line explanation and recommended action.

## Quality Checks
- [ ] All Stripe transactions for the month are accounted for (cross-reference transaction count)
- [ ] Every expense is categorized into Tools, Team, or Platform — nothing left in "uncategorized"
- [ ] Report shared with [Your Mentor/Advisor] and [Your Ops Partner] by the 5th
- [ ] No missing months in the running spreadsheet/thread

## Common Pitfalls
- **Tool subscriptions add up fast.** ChatGPT alone was [$X over 6 months]. Audit the full tool stack monthly — don't assume last month's number is still right.
- **Refunds are expenses.** The [Refunded Client] [$X — refund amount] refund must appear as an expense in the month it was processed, not hidden or netted against revenue.
- **Mixing personal and business expenses.** Keep [Your Agency] expenses on the [Your Agency] card/account. If a personal card was used, log it immediately or it gets lost.
- **[Your Ops Admin]'s cost is weekly, not monthly.** [$X/week] x number of weeks in the month. Some months have 5 pay periods.
- **[Partner Platform] is functionally bankrupt.** Do not assume [Partner Platform] account balances cover obligations. Track [Partner Platform]-related revenue and expenses separately so the picture is clear.

## Canon Compliance

- **Canon source:** 09-data-connections-needed.md
- **Triangles served:** MOF (Finance — revenue tracking, expense categorization, distribution reporting)
- **Human checkpoints:** [Your Name] approves refunds under $500; [Your Name] + [Your Mentor/Advisor] approve over $500; [Your Mentor/Advisor] and [Your Ops Partner] receive report by 5th of each month; net-negative months require explicit flag and recommended action
- **Anti-vandalism:** Never overwrite prior months in the spreadsheet; refunds must appear as expenses (not netted); [Partner Platform] tracked separately due to insolvency risk; all Stripe transactions cross-referenced by count
- **Last audited:** 2026-03-20 ([Methodology Partner] Canon Alignment run)

## Learnings Log
- 2026-03-18: SOP created. [Your Agency] revenue since Jul 2025 is [~$Total Revenue] total. [Your Mentor/Advisor] has repeatedly requested formal P&L tracking — this formalizes the process.
