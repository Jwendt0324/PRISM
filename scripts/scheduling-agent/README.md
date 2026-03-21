# D3S Service Scheduling Agent

Route optimization and scheduling engine for D3S Service (appliance repair).
31 technicians, 58 zones, covering East Texas + Oklahoma.

## Data Sources (ServiceDesk exports)

| File | Format | Records | Description |
|------|--------|---------|-------------|
| TechList.txt | TSV (tab-delimited, CRLF) | 31 techs + header | Technician roster: names, GPS coords, home addresses, job capacity, truck numbers, two-letter codes |
| ZoneList.txt | Plain text (zip\tzone) | 475 zip codes | Maps zip codes to 58 zone numbers |
| WhchTechToWhchZone.CSV | CSV | 58 zones | Maps each zone to assigned technicians (by two-letter code) |
| PrtsPrcs | Binary fixed-record (256 bytes/record) | ~2,220 records | Parts process queue: work orders, part numbers, approval status, vendor returns |
| SchdList | Binary fixed-record (96 bytes/record) | ~430 records | Active schedule: customer names, zip codes, dates, time slots, tech assignments |

## Project Structure

```
data/
  raw/          # Original ServiceDesk exports (READ ONLY - never modify)
  parsed/       # Cleaned CSV versions
  output/       # Optimized schedule output
src/
  parser.py     # Reads ServiceDesk formats into clean CSVs
  optimizer.py  # Route optimization (TSP/VRP solver)
  scheduler.py  # Main scheduling engine
  metrics.py    # Before/after comparison stats
dashboard.py    # Web dashboard
run.py          # Entry point
```

## Key Data Fields

### TechList columns
TechName, ShortName, TwoLttrCd, ThreeLttrCd, FocusGroup, TelNmbr, EmailAddress,
MapColor, MapHomePos, TruckNumber, UsingSdm?, Password, MapListPos, JobCapacity,
AddrsLn1, AddrsLn2, AvgMnsOnJb, TechID, TechNotAssmdInvntry, DefaultToDefinite,
StartNode, EndNode, TargetMiles, IsTechFake, SdmPrtclrToTechSttngsMtrx,
Latitude, Longitude, AltReturnToLoc, VectorStyle

### SchdList decoded fields (96-byte records)
- Bytes 0-3: Record ID (uint32 LE)
- Bytes 4-15: Customer/type (e.g., "ELE/RODR&", "CPS/BRISC", "GE/MARTI")
- Bytes 16-27: Zip code (space-padded)
- Bytes 28-31: City abbreviation (3 chars)
- Bytes 31-48: Date + day + time slot (e.g., "3/23 MON 8-12")
- Bytes 48-62: Tech code + route info
- Bytes 78-84: Secondary date field
- Remaining: Binary metadata

### PrtsPrcs decoded fields (256-byte records)
- Status text: "Ship if I/SMA", "CORE", etc.
- Work order numbers: W-prefixed (e.g., "W11171748EXCR")
- Approval status: "APPROVED", "RETURN"
- Phone numbers embedded
- Vendor return codes: "RtToVndr" + part numbers
