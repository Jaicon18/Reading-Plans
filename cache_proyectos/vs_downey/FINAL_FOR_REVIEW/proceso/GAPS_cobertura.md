# Gap closure: takeoff_canon_AB.json (VS #679 Downey)

| # | Gap | What was done | Qty | Source (N/SHEET) | Status / RFI |
|---|---|---|---|---|---|
| 1 | P-224 3/4"x3/4" black metal reveal | Added misc_items row "metal reveal trim (printed)": 2 pier verticals x 13'-8 1/2" + the bulkhead from pier to pier (printed plan chain 58.73 + 2 x 3/4") | 86.27 LF | A08.01 KN4, R/P/L A08.10, A/A08.01, A00.01 (O/G) | DERIVADO |
| 2 | Paging button blocking | Added blocking_items row: 6 fitting rooms x one 16" stud bay | 8.0 LF | A07.04 KN42 (J3, K3), G/A10.07 | DERIVADO |
| 3 | Go-back heavy-duty backing | Added blocking_items row: 4 dashed backing rows x 4'-6" shelving | 18.0 LF | E/A10.07 | DERIVADO |
| 4 | Fitting room signage blocking | Added blocking_items row: 1 sign at TRANS #4 x 3'-8" | 3.67 LF | A06.01 KN9, A07.04 KN53, P/A10.03, A00.01 | PENDIENTE, RFI-25 |
| 5 | Locker bank blocking | Added blocking_items row: 2 rows x 6 banks x 1'-3" (assumed width) | 15.0 LF | A14.02 KN12 (5) + KN13 (1), J/A14.02 note 3, A15.06 105100 | PENDIENTE, RFI-25 |
| 6 | Service door 12 lintel + jambs | Added an openings_extra "12" entry (DBL 3-5/8" lintel, 3 pcs; jambs on I07: 4 studs 48.33 LF + 2 cripples 10.08 LF + track 2 x 3.33 LF); R.O. 3.333 / head 7.042 are assumed; removed "12" from opening_schedule.none | 1 opening (header +14.0 LF) | M/A10.08, A00.02 | PENDIENTE, RFI-24 |
| 7 | 24x24x20 ga sheet metal at strike | Added misc_items row "sheet metal backing plate (printed)" | 1 PCS | M/A10.08, A00.02 door 12 | CONFIRMADO |
| 8 | RFID foil-backed board | No change (gap_closure_info) | - | A02.01, A15.04 | RFI-05 |
| 9 | 24"x24" access panel | No change: access_panels already has a separate "RCP keynote 8" 24x24 entry with qty 1 | - | A03.01 KN8 | RFI-22 |
| 10 | Display window platform framing | Added misc_items rows: joists 2 x 12 x 3'-7 7/8" @16"; edge track 2 x 2 x 13.49 | 87.74 LF 3-5/8" stud + 53.96 LF track | E, J/A08.05, D/A08.15, F, K/S02.01 | PENDIENTE, RFI-26 |
| 11 | Marketing pipe rail blocking | No change: the rail fixes to the 8'-3" C/L blocking row (B/A10.02 -> N/A10.01). That row is one of the 4 Garcy rows already carried on every KN5 run, so adding it would count it twice | 0 | A06.01 KN5, N/A10.01, B/A10.02 | covered |
| 12 | Beauty valance face board | No change: all 6 VAL soffit_side walls already carry one 5/8" face 2.167 ft on 1-5/8" studs | - | B/A10.03 | verified |
| 13 | 3-5/8" track at P8 fixtures | Added misc_items row: 7 P8 x 4'-0" main-beam span | 28.0 LF | L/A12.02, A04.01 KN2, N/A12.02 | DERIVADO |
| 14 | Recessed traffic counter framing | Added misc_items rows: 2 counters x 1'-4" stud laid on back, plus 4 angles | 2.67 LF + 4 EA | B/A12.02, J/A08.10, B/S02.01 | DERIVADO |
| 15 | Ceiling transitions | Added misc_items rows for E (break room ACT 10'-0" / corridor 8'-0", 3.65 ft) and A (corridor / hallway, 6.17 ft): hanger stud, U track, and board (step + 4 7/8" bottom) | 9.81 LF stud + 9.81 LF track + 17.44 SF | E, A/A12.02, A03.01, A14.02 | PENDIENTE, RFI-27 |
| 16 | Metal FRP top + edge trim (PVC replaced) | Added "metal FRP trim (printed)": 2 x 166.32 net perimeter + 2 x 6 doors x 4.0. The frp block moved to frp_info. FRP is now carried as 5 misc_items rows (same 665.28 SF), with frp_none_reason set and pvc_trim_items [] | 380.64 LF; PVC 460.64 -> 0 | E, A/A13.02 | DERIVADO |
| 17 | Communication board blocking | Added blocking_items row: 3 boards x 2 rows x 4'-0" (assumed) | 24.0 LF | A14.02 KN21-23, J/A14.02 note 3 | PENDIENTE, RFI-25 |
| 18 | F, K/S02.01 2-1/2" 20 ga studs | Added misc_items row "2-1/2\" stud": 2 x 12 studs x (11'-2" - 10'-6") | 16.0 LF | F, K/S02.01, E/A08.05 | PENDIENTE, RFI-17 (d) |
| 19 | R/S03.01 bridging clip at every stud | Added misc_items rows: clips = sum of pcs_full x rows over the 65 walls with an unsheathed zone > 4'-0" (rows = ROUNDUP(zone/4) - 1); C.R. channel = sum of length x rows | 1006 EA clips + 872.88 LF C.R. channel | R/S03.01 | DERIVADO |

Validation: `python3 validar_canon.py takeoff_canon_AB.json tools` -> CANON OK. The original canon is in _w/takeoff_canon_AB.orig.json.
