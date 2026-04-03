---
description: Process parts inquiry tickets in [Field Service Platform] — verify part numbers, price in [Parts Distributor], submit warranty Smartsheets
category: client-work
created: 2026-03-30
last_updated: 2026-03-30
version: 1.0
canon_compliance: N/A (operational SOP, not content production)
triangles: DDD
triangles_served: [DDD]
human_gates: yes
canon_sources: []
---

# [Field Service Platform] Parts Inquiry & Ordering SOP

## Purpose
Standardize how [Client — Appliance Repair] processes parts inquiry tickets in [Field Service Platform] following [[blitzmetrics-canon/10-anti-vandalism-checklist|anti-vandalism]] verification principles — from verifying tech-submitted part numbers through pricing, ordering, and warranty Smartsheet submission.

## When to Use
- A ticket appears in the "Items Needing Inquiry/Order" queue in [Field Service Platform]
- A technician has submitted a service ticket with parts that need to be verified, priced, and ordered
- Any [Field Service Platform] parts inquiry for [Client — Appliance Repair] or [Client — Appliance Repair]

## Process

### Phase 1: Open the Ticket

1. **Launch [Field Service Platform]** and navigate to the **[Client — Appliance Repair] desk**.
2. Press **F8** to open the main menu.
3. Click **"Items Needing Inquiry/Order"**.
4. Use **Page Down** to find the first unprocessed ticket.
5. **Right-click** in the green section of the ticket to open the ticket view.
6. **Right-click → Order Parts** to bring up all parts for this ticket.

### Phase 2: Verify Part Numbers

7. **Right-click the ticket view** to access the UIS (Unit Information Section).
8. **Copy the model number** from the UIS.
9. **Open the manufacturer's parts lookup site** in Google:
   - Electrolux → `Electrolux Service Tips` (parts breakdown/exploded view)
   - Other brands → use the appropriate manufacturer parts portal
10. **Enter the model number** to pull up the parts breakdown.
11. **For each part the tech entered**, use **Ctrl+F** to search the breakdown:
    - If found → part number is **verified**.
    - If NOT found → locate the correct part on the exploded view, identify the right part number, and **correct it in the [Field Service Platform] ticket**.

> **Common issue:** Techs frequently enter part numbers with one digit off. Always verify every part, even if it looks right.

### Phase 3: Price Parts in [Parts Distributor]

12. **Open [Parts Distributor]** ([parts-distributor-url.com]) in the browser.
13. **Search each verified part number** in [Parts Distributor]:
    - If **in stock** → record the price in the **Cost box** in [Field Service Platform], set **Vendor = [Parts Distributor]**.
    - If [Parts Distributor] **substitutes** a new part number → copy the substituted number back into [Field Service Platform]'s part number field, then record the price.
    - If **out of stock** → mark the part for **Smartsheet** (see Phase 5), set **Vendor = WCI** (for Electrolux) or the appropriate manufacturer code.

### Phase 4: Check Local Inventory & Set Shipping

14. **Check for local inventory popups** — if [Field Service Platform] shows **"comm wall"** or another local location, the part is already at the office.
    - Change **Vendor = [Client-ID]** for locally stocked parts.
    - Physically verify the part is at the indicated location.
15. **Set the ship-to for each part:**
    - **Local technicians** (e.g., TP) → set to **OR** (office/received at office).
    - **Remote technicians** → set to tech's address or job site as appropriate.

### Phase 5: Submit Warranty Smartsheet (When Required)

16. **Navigate to the warranty part request form** at **app.smartsheet.com**.
17. **Fill out the form** with the following information:

| Field | Source |
|-------|--------|
| Servicer Number | [Client-ID] account number |
| Servicer Name | [Client — Appliance Repair] |
| Servicer Email | parts@[client-id]service.com |
| Customer Name | From [Field Service Platform] ticket |
| Model Number | From ticket UIS |
| Serial Number | From ticket UIS |
| Purchase Date | From ticket (must be within warranty period) |
| Dispatch Number | Top-right corner of ticket information box |
| Complaint/Diagnosis | Copy tech's notes from ticket |
| Part Number(s) | The part(s) that need warranty ordering |
| Part Quantity | Usually 1 per line |
| Recipient Name | **[Client — Appliance Repair] - [ticket number]** (e.g., [Client — Appliance Repair] - 235934) |
| Recipient Phone | **[555-000-0000]** |
| Recipient Address | **[123 Example Street, City, ST]** |
| Send Copy To | parts@[client-id]service.com |

18. **Submit the form**.
19. **Add a note in the [Field Service Platform] ticket:** "Submitted smart sheet".

### Phase 6: Close Out

20. **Verify all parts** have a cost, vendor, and ship-to assigned.
21. **For locally stocked parts** (comm wall), physically locate and check in the part.
22. Ticket is complete once all parts are accounted for.

## Quality Checks
- [ ] Every part number has been verified against the manufacturer parts breakdown
- [ ] Every part has a cost entered in [Field Service Platform]
- [ ] Every part has a vendor assigned ([Parts Distributor], [Client-ID], WCI, etc.)
- [ ] Every part has a ship-to destination
- [ ] Smartsheet submitted for any out-of-stock warranty parts
- [ ] Notes added to ticket for any corrections or Smartsheet submissions

## Common Pitfalls

- **Techs enter wrong part numbers.** Don't trust them — verify every single one against the exploded view. One digit off is the most common error.
- **[Parts Distributor] substitutions.** When [Parts Distributor] auto-substitutes a part number, you MUST copy the new number back into [Field Service Platform]. Otherwise the ticket has a part number that doesn't match what ships.
- **Forgetting to check local inventory.** If "comm wall" shows up in the popup, the part is already in the office. Don't order a duplicate from [Parts Distributor].
- **Wrong vendor code.** Use **[Parts Distributor]** for [Parts Distributor] orders, **WCI** for Electrolux warranty/direct, **[Client-ID]** for local stock. Getting this wrong messes up purchasing reports.
- **Not verifying warranty eligibility.** Check the purchase date before submitting a Smartsheet. If the unit is out of warranty, the request will be rejected.

## Human Gates

| Step | Gate Type | Reason |
|------|-----------|--------|
| 11 — Correct part numbers | Execute | Requires judgment to identify correct part from exploded view |
| 13 — Price and availability decisions | Execute | Requires checking live [Parts Distributor] inventory and making sourcing decisions |
| 14 — Local inventory check | Execute | Requires physical verification of parts on comm wall |
| 17 — Smartsheet submission | Review | Must verify all warranty claim data is accurate before submitting to manufacturer |

## Anti-Vandalism Checks
- **Check what already exists:** Before ordering parts, verify no duplicate orders exist for the same ticket.
- **Preserve what's working:** Do not modify part numbers the tech entered without first verifying they're wrong — some non-standard parts won't appear in the standard breakdown but may be correct (e.g., Electrolux tech support approved parts).
- **Reference canonical source:** Always use the manufacturer's official parts breakdown as the source of truth, not third-party parts sites.

## Canon Compliance
- **Content Factory stage(s):** N/A — this is an operational/service SOP, not content production.
- **9 Triangles served:** DDD (Dollar-a-Day is the closest mapping — this SOP serves operational efficiency for [Client — Appliance Repair], a client business).
- **Canon documents:** None directly — this is a client-specific operational procedure.
- **Last canon audit:** 2026-03-30

## Key Reference Info

| Item | Value |
|------|-------|
| [Client-ID] Office Address | [123 Example Street, City, ST] |
| [Client-ID] Parts Email | parts@[client-id]service.com |
| [Client-ID] Office Phone | [555-000-0000] |
| Smartsheet URL | app.smartsheet.com (warranty part request form) |
| [Parts Distributor] | [parts-distributor-url.com] |
| Electrolux Parts Lookup | Electrolux Service Tips |

## Learnings Log
- **2026-03-30:** Initial SOP created from video walkthrough of ticket #235934 (Electrolux fridge). Key finding: tech had one digit wrong on dryer assembly part number — verification step is critical.

## See Also

- [[blitzmetrics-canon/10-anti-vandalism-checklist|Anti-Vandalism]]
- [[blitzmetrics-canon/08-human-requirements|Human Requirements]]
- [[memory-bank/04-client-directory|Client Directory]]
