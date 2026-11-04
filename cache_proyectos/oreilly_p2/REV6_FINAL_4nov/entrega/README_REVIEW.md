# O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 — Metal framing & drywall take-off, rev6 FINAL

## PROJECT DATA

| Field | Value | Source |
|---|---|---|
| project name / city | New O'Reilly Auto Parts Store, 23rd Ave., Evans, CO #1 | T1.1 cover (project title + title block) |
| address | 23rd Ave., Evans, CO #1 (no street number printed); survey title: '23RD AVENUE, EVANS, CO 80620' | T1.1 title block; SV1 survey title block |
| type of project | New construction, single-story retail auto parts store (mercantile); pre-engineered metal building (PEMB) structure with CMU exterior walls and cold-formed metal stud interior framing | T1.1 title 'New O'Reilly Auto Parts Store'; G1.1 code analysis (M, 1 story); T1.2 scope 13 34 19 PEMB system (Butler Manufacturing); S5.2 keynote 1 PEMB; S4.1 keynote 1 masonry exterior wall |
| owner / tenant | O'Reilly Auto Enterprises, LLC, Corporate Offices, 233 South Patterson, Springfield, Missouri 65802, 417-862-2674 | T1.1 cover 'Owner or Tenant' |
| architect | Timothy M. Guillot, Architect, 1736 East Sunshine, Suite 417, Springfield, Missouri 65804, 417.862.0558 (structural: J.S. Smith Consulting Engineers, P.C.; MEP: Smith-Goth Engineers, Inc.; civil: Tait & Associates) | T1.1 cover |
| general contractor (GC) | [PENDIENTE] not printed in the set (T1.1 bidding information: invited general contractors listed on owner's website www.oreillyplanroom.com; sub-contractor bids to invited GCs only) (R-ALC-09: a project datum not printed is carried as [PENDING]; no quantity depends on it) | - |
| bid date | [PENDIENTE] not printed in the set. Issue dates printed: T1.1 DATE 7-19-24, revision dates 5-6-25 and 9-17-25; G1.1/A1.1/A5.2 revision 4-18-25; A1.2 revisions 4-18-25, 9-9-25; S4.1/S5.2 revision 3-20-25. No 'Conformed Set 11-20-2025' label found printed on any sheet (R-ALC-09: a project datum not printed is carried as [PENDING]; no quantity depends on it) | - |
| bid set | 68-page PDF: pages 1-3 blank, T1.1-A6.1 (pages 4-48), MEP/utility/signage (pages 49-68); COMM # 4838; sheet index on T1.1. No set name ('bid'/'conformed') printed; PDF received from the estimator: "EV1 Current Conformed Set 11-20-2025" (file name) | T1.1 sheet index + title block |
| total building area SF | 7,453 SF gross (building interior area 6,955 SF); building 86'-4" x 86'-4" | G1.1 code analysis (Actual Height & Building Area; Project Data); G1.1/A1.1 overall dims |
| stories | 1 story (allowable 2 stories); building height 20'-8" | G1.1 code analysis |
| construction type / classification | Type II-B (non-combustible / unprotected) | G1.1 code analysis |
| occupancy group | M (Mercantile), mixed use nonseparated | G1.1 code analysis |
| codes | 2018 IBC, 2018 IPC, 2018 IMC, 2020 NEC, 2018 IFC, 2012 IECC, 2018 ICC A117.1; amending ordinance: Evans, CO Municipal Code | G1.1 code analysis 'Governing Codes and Ordinances' |
| occupant load | 69 total (Parts Area A 56, Parts Area B 7, Office 1, Parts Area C 5) | G1.1 Occupancy Load Summary |
| sprinklered | No - automatic sprinkler system NOT REQUIRED; automatic sprinkler increase NOT PROVIDED | G1.1 code analysis 'Fire Protection Systems' |
| demolition | No building demolition (new building; no demolition sheets). Site only: 'DEMOLITION OF EXISTING SITE IMPROVEMENTS' in Phase 1 (pre-construction) sequence | C1.2 erosion control sequence, Phase 1 item 2 |
| specs | [PENDIENTE] not printed in the set - specs are in a separate Project Manual that is referenced but not included (e.g. 'Refer to Project Manual, Section 01 45 16 - Quality Control Procedures'; CSI sections listed on T1.2 scope of work schedule) (R-ALC-09: a project datum not printed is carried as [PENDING]; no quantity depends on it) | - |

**Mandatory sheets reviewed**

| Category | Status |
|---|---|
| cover / index | reviewed: T1.1, T1.2 |
| code analysis / G | reviewed: G1.1 |
| general notes | reviewed: T1.1, A1.1, S1.1 |
| demolition + notes | not in the set |
| specs | not in the set |
| partition types + details | reviewed: A1.1, A4.2, A5.1, A5.2 |
| floor plans | reviewed: A1.1, A1.2 |
| RCP (reflected ceiling plan) | not in the set |
| elevations / sections | reviewed: A2.1, A3.1, A3.2, A3.3, A3.4 |
| enlarged / interior elevations | reviewed: A4.1, A4.2 |
| schedules | reviewed: A1.2, A5.1, A5.2 |
| structural | reviewed: S1.1, S2.1, S3.1, S3.2, S4.1, S5.1, S5.2, S5.3, S5.3 |
| MEP | reviewed: US1, SP1, SP2, SP3, P1, P2, M1, M2, M3, E1, E2, E3, E4, EM1.0, EM1.1, EM1.2, EM1.3 (excluded by estimator order: MEP) |

## What is in this folder

- `Take-off/OReilly_Evans_Takeoff_FINAL_rev6.xlsx` — fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Waste is applied once, in the Material Summary.
- `Planos marcados/OReilly_Evans_FINAL_markups_rev6.pdf` — Bluebeam markups on A1.1 (Subject = type, Page Label, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · board SF · DETAIL · Wall ID) + one PNG per type.
- `SEGUIMIENTO.md` — RFI follow-up (open and closed).
- Review-first notes for the estimator (the separate notes file in this folder).
- `Auditoria/` — delivery gate (ENTREGA_OK.json), materials vs Partition Type Schedule, markup review.

## Basis of this revision

rev6 = rev5 (pass 2 FINAL, all estimator answers RFI-01..RFI-32 applied) re-run end to end with skill v81cf27 = v81cf26 + Review Items image name fix (delivery gate with the day-1 rules U-114..U-125). **rev6 replaces rev5; quantities are identical to rev5** (67 Material Summary rows, checked by program). Added: [CONFIRMED] / [DERIVED] status on every face height, numbered tag sweep of A1.1 (29 tags, circled crops), circled height evidence per wall. Quantities are produced by the programs from the canon; nothing is typed in the Excel.

## Material Summary (net, before waste)

| Material | Unit | Net | Where it comes from |
|---|---|---|---|
| Bottom track 8" | LF | 12.00 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: EXT-MS1-8 6 + EXT-MS2-8 6 = 12 LF (wall length x rows) | Track gauge =  |
| Bottom track 6" - 600T125-54 | LF | 12.00 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: EXT-MS1-6 6 + EXT-MS2-6 6 = 12 LF |
| Bottom track 6" - 600T125-43 | LF | 36.00 | N/SHEET: 1/S5.3 | Breakdown [DERIVED]: CORN-S 36 = 36 LF |
| Bottom track 6" - 600T125-33 | LF | 8.50 | N/SHEET: S61/A1.1 | Breakdown [DERIVED]: S61-RR 8.5 = 8.5 LF |
| Bottom track - other framing (not a partition type, see source) - 800T125-54 | LF | 38.67 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: HEAD-A-8 38.67 = 38.67 LF |
| Bottom track - other framing (not a partition type, see source) - 600T125-54 | LF | 38.67 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: HEAD-A-6 38.67 = 38.67 LF |
| Bottom track 3-5/8" | LF | 219.68 | N/SHEET: S24/A1.1, S43/A1.1, S41/A1.1, 5/A4.2, 6/A4.2 | Breakdown [DERIVED]: S24-OF 11.71 + S24-RR 16.82 + S24 |
| Bottom track - roof step and heads (vestibule / bulkhead) | LF | 20.09 | N/SHEET: 3/A3.1 | Breakdown [DERIVED]: VH-C 8.75 + VH-B2 5.67 + VH-B1 5.67 = 20.09 LF (wall length x rows) | T |
| Top / deflection track 8" | LF | 12.00 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: EXT-MS1-8 6 + EXT-MS2-8 6 = 12 LF (wall length x rows) | Track gauge =  |
| Top / deflection track 6" - 600T125-54 | LF | 12.00 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: EXT-MS1-6 6 + EXT-MS2-6 6 = 12 LF |
| Top / deflection track 6" - 600T125-43 | LF | 36.00 | N/SHEET: 1/S5.3 | Breakdown [DERIVED]: CORN-S 36 = 36 LF |
| Top / deflection track 6" - 600T125-33 | LF | 8.50 | N/SHEET: S61/A1.1 | Breakdown [DERIVED]: S61-RR 8.5 = 8.5 LF |
| Top / deflection track - other framing (not a partition type, see source) - 800T125-54 | LF | 38.67 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: HEAD-A-8 38.67 = 38.67 LF |
| Top / deflection track - other framing (not a partition type, see source) - 600T125-54 | LF | 38.67 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: HEAD-A-6 38.67 = 38.67 LF |
| Top / deflection track 3-5/8" | LF | 96.57 | N/SHEET: S24/A1.1, S43/A1.1, S41/A1.1 | Breakdown [DERIVED]: S24-OF 11.71 + S24-RR 16.82 + S24-RRS 8.85 + S43- |
| 1-1/2" Z-furring channel (LF of material) | LF | 2,220.63 | N/SHEET: S21/A1.1 | Breakdown [DERIVED]: S21-N 629.65 + S21-E 642.07 + S21-S 634.33 + S21-W1 94.37 + S21-W2 22 |
| 8" stud (all gauges) | LF | 537.32 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: EXT-MS1-8 124 + EXT-MS2-8 124 + HEAD-A-8 289.32 = 537.32 LF (per wall:  |
| 6" metal stud (LF of material) - 600S162-54 | LF | 687.32 | N/SHEET: 3/S5.3, 7/A4.2 | Breakdown [DERIVED]: EXT-MS1-6 124 + EXT-MS2-6 124 + HEAD-A-6 289.32 + CJ-OFFICE-102 |
| 6" metal stud (LF of material) - 600S162-43 | LF | 340.72 | N/SHEET: 1/S5.3, 3/A3.1 | Breakdown [DERIVED]: CORN-S 223.13 + VH-C 34.29 + VH-B2 17.14 + VH-B1 17.14 + CJ-VES |
| 6" metal stud (LF of material) - 600S162-33 | LF | 68.00 | N/SHEET: S61/A1.1 | Breakdown [DERIVED]: S61-RR 68 = 68 LF |
| 6" metal stud (LF of material) - 600S200-54 | LF | 276.00 | N/SHEET: 2/S5.1, 1/S5.1, 4/S5.1 | Breakdown [DERIVED]: CONT-6IN-S42-03 100.67 + PEMB-6IN-S42-02 70 + PEMB-6IN- |
| 3-5/8" metal stud (LF of material) - 362S162-33 | LF | 1,912.02 | N/SHEET: S24/A1.1, S43/A1.1, S41/A1.1, 5/A4.2, 6/A4.2, 1/S5.1, 5/S5.1, 2/A4.2 | Breakdown [DERIVED]: S24-OF 59 |
| 3-5/8" metal stud (LF of material) - 362S162-43 | LF | 140.00 | N/SHEET: 3/S5.3 | Breakdown [DERIVED]: TIES-HEAD-A 140 = 140 LF |
| Ceiling / soffit track (size per source, see Where it comes from) | LF | 72.00 | N/SHEET: 7/A4.2, 3/A3.1 | Breakdown [DERIVED]: CT-OFFICE-102 22 + CT-RR-103-104 34 + CT-VEST-100A 16 = 72 LF |
| Bracing 1-1/2" C.R. channel @ 48" O.C. | LF | 808.01 | N/SHEET: 3/S5.3, 1/S5.3, S24/A1.1, S43/A1.1, S61/A1.1, S41/A1.1, 5/A4.2, 6/A4.2, 3/A3.1 | Breakdown [DERIVED]: |
| Header / metal stud box beam | LF | 56.00 | N/SHEET: 7/A5.1 | Breakdown [DERIVED]: Door 4 (S43-OF-S) 18.66 + Door 5 (S43-RR-S) 18.66 + Door 6 (S43-RR-S) 1 |
| 5/8" glass mat sheathing (exterior face of the stud) | SF | 534.88 | N/SHEET: 1/A3.1, 1/A3.4 | Breakdown [DERIVED]: GLASSMAT-EXT-MS 248 + GLASSMAT-CORN-S 286.88 = 534.88 SF | 2 wa |
| Blocking FRT / 2X FRT wood | LF | 600.79 | N/SHEET: 6/A4.2, 1/A5.1, 12/A5.2, 10/A4.1, 1A/A4.1, 13/A4.1, 2/A3.1, 10/A4.2, 14/A4.1 | Breakdown [DERIVED]: B |
| 5/8" gypsum board, Type X | SF | 7,421.40 | N/SHEET: S21/A1.1, 3/S5.3, S24/A1.1, S43/A1.1, S41/A1.1, 5/A4.2, 6/A4.2, 3/A3.1, 7/A4.2, 1/A5.2, 3/A5.2, 12/A4 |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 721.21 | N/SHEET: S24/A1.1, S43/A1.1, S61/A1.1, 7/A4.2 | Breakdown [DERIVED]: S24-RR 142.99 + S24-RRS 75.26 + S43-RR-W  |
| Clip angles and framing clips (see Where it comes from) - 2"x2"x14ga clip | PCS | 22.00 | N/SHEET: 2/S5.1 | Breakdown [DERIVED]: CLIP-2X2-S42-03 22 = 22 PCS |
| Clip angles and framing clips (see Where it comes from) - L4x4x3/16 x 1'-0" clip angle | PCS | 19.00 | N/SHEET: 2/S5.1 | Breakdown [DERIVED]: L4X4-S42-03 19 = 19 PCS |
| Deep-leg slotted deflection track - printed product (see Where it comes from) - 3-5/8" web | LF | 123.11 | N/SHEET: 4/S5.1, 3/S5.1, 1/S5.1, 2/S5.1 | Breakdown [DERIVED]: DLT-S42-01 38.67 + DLT-S42-04 8.17 + DLT-S42-02 |
| Deep-leg slotted deflection track - printed product (see Where it comes from) - 6" web | LF | 20.09 | N/SHEET: 3/A3.1 | Breakdown [DERIVED]: DLT-VH-C 8.75 + DLT-VH-B1 5.67 + DLT-VH-B2 5.67 = 20.09 LF |
| Framing clips per stud - printed product (see Where it comes from) | PCS | 144.00 | N/SHEET: 1/S5.3, 3/S5.3 | Breakdown [DERIVED]: FCB-CORN-S 84 + FCB-WB-HEAD-A 60 = 144 PCS | one FCB43.5 per st |
| Resilient channel - printed product (see Where it comes from) | LF | 128.51 | N/SHEET: 1/A3.1 | Breakdown [DERIVED]: RC-EXT-MS 128.51 = 128.51 LF | rows @ 24": EXT-MS1 (ROUNDUP(12.0/2)+1 = |
| 1/4" gypsum board - printed (see Where it comes from) | SF | 195.58 | N/SHEET: 1/A3.1, 1/A5.2 | Breakdown [DERIVED]: QTR-GYP-EXT-MS 180.68 + QTR-GYP-HEAD-A-UNDERSIDE 14.9 = 195.58  |
| Diagonal flat strap bracing - printed (see Where it comes from) | LF | 96.91 | N/SHEET: B/A1.1 | Breakdown [DERIVED]: STRAP-S41 96.91 = 96.91 LF | A1.1 Interior Wall Notes 2.B 3" x 16 ga di |
| Z-furring runner track 1-1/2" top and bottom (see Where it comes from) | LF | 577.25 | N/SHEET: S21/A1.1 | Breakdown [DERIVED]: ZF-RUNNER-S21 577.25 = 577.25 LF | 1-1/2" runner top and bottom of th |
| Sanitary wall panel system W-4 (see Where it comes from) | SF | 555.34 | N/SHEET: A1.2 | Breakdown [DERIVED]: W4-PANELS-103 277.67 + W4-PANELS-104 277.67 = 555.34 SF | R.R. 103 4 wall |
| Track brace at strut splice - printed product (see Where it comes from) | LF | 6.00 | N/SHEET: 5/S5.1 | Breakdown [DERIVED]: TRACK-BRACE-STRUT-SPLICE 6 = 6 LF | 5/S5.1 prints '2'-0" LONG 3-5/8"x20 |
| W-4 panel trim and edge molding - printed (see Where it comes from) | LF | 100.67 | N/SHEET: A4.1 | Breakdown [DERIVED]: W4-TRIM-EDGE 100.67 = 100.67 LF | A4.1 key note 8, top edge and door edge |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead | LF | 474.62 | N/SHEET: 7/A4.2, 4/A4.2, 6/A4.2, 2/A5.2, 3/A5.2, 1/A5.1, 1/A5.2 | Breakdown [DERIVED]: CB-7A42-TOP 79.73 + CB- |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - Fry JDM-625 J molding | LF | 41.30 | N/SHEET: 2/A4.2 | Breakdown [DERIVED]: JDM-S42-JOINTS 41.3 = 41.3 LF |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - Fry DRMF-625-75 reveal molding | LF | 41.30 | N/SHEET: 2/A4.2 | Breakdown [DERIVED]: DRMF-S42-JOINTS 41.3 = 41.3 LF |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - casing (J) bead | LF | 194.25 | N/SHEET: 1/A5.2, 3/A5.2, 2/A5.1 | Breakdown [DERIVED]: CSB-SF-A-FRAME 53.33 + CSB-VEST-FRAMES 46.67 + CSB-DOOR |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - J molding | LF | 375.79 | N/SHEET: 6/A5.1, A1.1 | Breakdown [DERIVED]: J-DOOR-3-CLADDING 22 + J-ROOF-EXPOSED 353.79 = 375.79 LF |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 340.24 | N/SHEET: 7/A3.2, 7/A4.2, A1.1 | Breakdown [DERIVED]: CJ-DIR-CHANGE 69.71 + CJ-S21 87.29 + CJ-S42-01 26.51 + CJ |
| FRT plywood substrate (5/8 in.) | SF | 407.63 | N/SHEET: 4/A4.2, 2/A3.1, 1/A5.2 | Breakdown [DERIVED]: S41-B1V-FRT 4.33 + S41-B1H-FRT 2.63 + S41-B2H-FRT 3.33  |
| Additional head track at openings over 4'-0" wide | LF | 0.00 | [DERIVED] N/SHEET: 7/A5.1 | none in the set |
| Stud reinforcement at MEP penetrations | PCS | 0.00 | N/SHEET: A1.1 | none: estimator order: MEP / electrical / civil / cabinets excluded (estimator order 2026-10-3 |
| Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its type) | LF | 0.00 | [DERIVED] N/SHEET: A1.1 | none: No ATM / equipment recess in the set (A1.1, A5.1, A5.2 reviewed) (A1.1) |
| 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | LF | 0.00 | N/SHEET: A5.2 | none: no coiling grille / grille head detail in the set; security shutters (A5.2 general note  |
| Gypsum board jamb return at openings | SF | 11.78 | N/SHEET: 12/A5.2, 13/A5.2 | edges 58.92 LF x 0.2 ft = 11.78 SF [Window D1 29.46 [12/A5.2 jamb detail: 5/8" TYP |
| PVC trim - edge trim molding and inside corner molding at the FRP | LF | 0.00 | [DERIVED] N/SHEET: A1.2 | none: No FRP in the set; restroom walls W-4 'SANITARY WALL AND CEILING PANEL SYSTEM' |
| Power-driven fasteners and duct sleeves | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Access panel | PCS | 0.00 | [DERIVED] N/SHEET: A1.2 | none: No access panel shown on A1.1, A1.2 or A4.1 (MEP sheets excluded by estimator  |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Power-driven fasteners, slab pins for the bottom track | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Joint compound, all purpose | LB | 586.27 | [DERIVED] N/SHEET: driver = the board / stud / bottom track rows of this sheet | Inputs!B23 (Joint compound (l |
| Joint tape, paper | LF | 3,012.77 | [DERIVED] N/SHEET: driver = the board / stud / bottom track rows of this sheet | Inputs!B24 (Joint tape (LF pe |
| Level 5 finish | SF | 6,440.16 | [DERIVED] N/SHEET: A1.2 | L5-S21-N-B0 387.38 SF; L5-S21-N-B1 677.38 SF; L5-S21-E-A0 783.25 SF; L5-S21-E-A1 58. |
| Deflection clips at non-load-bearing walls to structure | PCS | 0.00 | [DERIVED] N/SHEET: A1.1 | none: A1.1 note 2.C deflection channels at the top track are carried as the printed  |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 0.00 | [DERIVED] N/SHEET: E/S1.1, F/S1.1 | EXCLUDED - estimator order 2026-10-31: all fasteners excluded (7.E/S1.1 an |

## Changes vs rev4

| Material | Unit | rev4 | rev5 | Delta | Delta % |
|---|---|---|---|---|---|
| Bottom track 3-5/8" | LF | 218.32 | 219.68 | +1.36 | +0.6 % |
| Bottom track 6" (all) | LF | 95.17 | 56.50 | -38.67 | -40.6 % |
| Bottom track 8" (all) | LF | 50.67 | 50.67 | +0.00 | +0.0 % |
| Bottom track 6" other framing (600T) | LF | 0.00 | 38.67 | +38.67 | new |
| Bottom track roof step / heads | LF | 20.57 | 20.09 | -0.48 | -2.3 % |
| Top track 3-5/8" | LF | 171.48 | 96.57 | -74.91 | -43.7 % |
| Top track 6" (all) | LF | 95.17 | 56.50 | -38.67 | -40.6 % |
| Top track 8" (all) | LF | 50.67 | 50.67 | +0.00 | +0.0 % |
| Top track 6" other framing (600T) | LF | 0.00 | 38.67 | +38.67 | new |
| Top track roof step / heads | LF | 20.57 | 0.00 | -20.57 | -100.0 % |
| Deep-leg slotted deflection track | LF | 46.83 | 143.20 | +96.37 | +205.8 % |
| Z-furring 1-1/2" | LF | 2,570.64 | 2,220.63 | -350.01 | -13.6 % |
| 8" stud | LF | 537.32 | 537.32 | +0.00 | +0.0 % |
| 6" stud (all) | LF | 1,148.07 | 1,372.04 | +223.97 | +19.5 % |
| 3-5/8" stud (all) | LF | 2,165.17 | 2,052.02 | -113.15 | -5.2 % |
| Ceiling / soffit track | LF | 0.00 | 72.00 | +72.00 | new |
| Bracing C.R. channel | LF | 806.26 | 808.01 | +1.75 | +0.2 % |
| Header / box beam | LF | 56.00 | 56.00 | +0.00 | +0.0 % |
| Glass mat sheathing | SF | 534.88 | 534.88 | +0.00 | +0.0 % |
| FRT blocking | LF | 539.75 | 600.79 | +61.04 | +11.3 % |
| Metal stud blocking | LF | 6.00 | 0.00 | -6.00 | -100.0 % |
| 5/8" Type X | SF | 7,673.76 | 7,421.40 | -252.36 | -3.3 % |
| 5/8" Type X W.R. | SF | 734.15 | 721.21 | -12.94 | -1.8 % |
| Clips + clip angles | PCS | 38.00 | 41.00 | +3.00 | +7.9 % |
| FCB43.5 framing clips | PCS | 144.00 | 144.00 | +0.00 | +0.0 % |
| Resilient channel | LF | 243.00 | 128.51 | -114.49 | -47.1 % |
| 1/4" gypsum board | SF | 385.00 | 195.58 | -189.42 | -49.2 % |
| Flat strap bracing | LF | 98.00 | 96.91 | -1.09 | -1.1 % |
| Z-furring runner | LF | 501.41 | 577.25 | +75.84 | +15.1 % |
| W-4 panels | SF | 555.33 | 555.34 | +0.01 | +0.0 % |
| W-4 trim | LF | 0.00 | 100.67 | +100.67 | new |
| Track brace strut splice | LF | 0.00 | 6.00 | +6.00 | new |
| Metal trim (all) | LF | 709.63 | 1,127.26 | +417.63 | +58.9 % |
| Control joints | LF | 73.34 | 340.24 | +266.90 | +363.9 % |
| FRT plywood | SF | 420.25 | 407.63 | -12.62 | -3.0 % |
| Additional head track | LF | 32.73 | 0.00 | -32.73 | -100.0 % |
| Jamb return | SF | 7.24 | 11.78 | +4.54 | +62.7 % |
| Joint compound | LB | 605.37 | 586.27 | -19.10 | -3.2 % |
| Joint tape | LF | 3,110.93 | 3,012.77 | -98.16 | -3.2 % |
| Level 5 | SF | 7,673.76 | 6,440.16 | -1,233.60 | -16.1 % |

