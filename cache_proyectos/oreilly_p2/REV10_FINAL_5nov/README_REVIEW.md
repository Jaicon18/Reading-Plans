# O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 — Metal framing & drywall take-off, rev10 FINAL

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

- `Take-off/OReilly_Evans_Takeoff_FINAL_rev10.xlsx` — fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Waste is applied once, in the Material Summary.
- `Planos marcados/OReilly_Evans_FINAL_markups_rev10.pdf` — Bluebeam markups on A1.1 (Subject = type, Page Label, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · board SF · DETAIL · Wall ID) + one PNG per type.
- `SEGUIMIENTO.md` — RFI follow-up (open and closed).
- Review-first notes for the estimator (the separate notes file in this folder).
- `Auditoria/` — delivery gate (ENTREGA_OK.json), materials vs Partition Type Schedule, markup review.

## Basis of this revision

rev10 FINAL = rev9 + (1) every trade schedule reviewed (user rule 2026-11-05): partition / wall types, door, window, glazing, interior finish schedule and finish types; each type / row is marked (red circle + check + number) on its schedule sheet in `Planos marcados/SCHEDULES_REVISADOS.pdf` and every material is listed in SCHEDULES_MATERIALES (at the end of this README) with its Material Summary row or its out-of-scope reason; (2) demolition rule (user rule 2026-11-05): demolition is carried as SF only, its materials are not quantified (none in this set); (3) the corrected DETALLES_REVISADOS_INDEX is inside this README. Quantities identical to rev8 and rev9. rev9 = rev8 + every reviewed detail bubble circled and numbered in red on its calling sheet and on its destination view (user rule 2026-11-05): `Planos marcados/DETALLES_REVISADOS.pdf` + the DETALLES_REVISADOS_INDEX at the end of this README. Quantities identical to rev8. rev8 = rev7 + the user decisions of 2026-11-05: (1) RFI-34 = option A (sheathing return at 2 head wall ends, 6/A3.1 and 6/A3.4, as carried); (2) wood EXCLUDED (R-ALC-01): FRT 2x blocking, FRT plywood and nailers = 0 with the note 'EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01' in the Material Summary and the Scope Checklist; this supersedes the estimator decisions of 2026-11-01 RFI-12 / RFI-24 / RFI-25. Every other quantity is identical to rev7. 0 open RFIs. Re-run end to end with skill v81cf45 (quantities from the rev8 run, unchanged); quantities are produced by the programs from the canon; nothing is typed in the Excel.

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
| 5/8" glass mat sheathing (exterior face of the stud) | SF | 543.21 | N/SHEET: 1/A3.1, 1/A3.4, 6/A3.1 | Breakdown [DERIVED]: GLASSMAT-EXT-MS 248 + GLASSMAT-CORN-S 286.88 + GLASSMAT |
| Blocking FRT / 2X FRT wood | LF | 0.00 | N/SHEET: 6/A4.2, 1/A5.1, 12/A5.2, 10/A4.1, 1A/A4.1, 13/A4.1, 2/A3.1, 10/A4.2, 14/A4.1 | EXCLUDED - wood blocki |
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
| FRT plywood substrate (5/8 in.) | SF | 0.00 | N/SHEET: 4/A4.2, 2/A3.1, 1/A5.2 | EXCLUDED - wood blocking / plywood by others (Div. 06) (user decision 2026-1 |
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
| Glass mat sheathing | SF | 534.88 | 543.21 | +8.33 | +1.6 % |
| FRT blocking | LF | 539.75 | 0.00 | -539.75 | -100.0 % |
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
| FRT plywood | SF | 420.25 | 0.00 | -420.25 | -100.0 % |
| Additional head track | LF | 32.73 | 0.00 | -32.73 | -100.0 % |
| Jamb return | SF | 7.24 | 11.78 | +4.54 | +62.7 % |
| Joint compound | LB | 605.37 | 586.27 | -19.10 | -3.2 % |
| Joint tape | LF | 3,110.93 | 3,012.77 | -98.16 | -3.2 % |
| Level 5 | SF | 7,673.76 | 6,440.16 | -1,233.60 | -16.1 % |

## DETALLES_REVISADOS_INDEX

Every detail bubble reviewed (U-141), circled and numbered in red on its calling sheet and on its destination view in `Planos marcados/DETALLES_REVISADOS.pdf`.

| # | Bubble | Calling sheet | Destination view | Take-off row / out of scope |
|---|---|---|---|---|
| 1 | 1/A4.1 | A1.1 | 1/A4.1 | cited: cited in its governing row (Excel / canon) |
| 2 | 3/A3.4 | A1.1 | 3/A3.4 | cited: cited in its governing row (Excel / canon) |
| 3 | 2/A3.2 | A1.1 | 2/A3.2 | cited: cited in its governing row (Excel / canon) |
| 4 | 2/A3.4 | A1.1 | 2/A3.4 | cited: cited in its governing row (Excel / canon) |
| 5 | 3/A2.1 | A1.1 | 3/A2.1 | out of scope: East exterior elevation: CMU (2A / 2B), stucco cornice (5) on masonry, PEMB gutter / downspouts and roof access ladder (27); no cold-formed framing or gypsum bo |
| 6 | 4/A3.2 | A1.1 | 4/A3.2 | cited: cited in its governing row (Excel / canon) |
| 7 | 7/A4.2 | A1.1 | 7/A4.2 | cited: cited in its governing row (Excel / canon) |
| 8 | 7/A4.2 | A1.1 | 7/A4.2 | cited: cited in its governing row (Excel / canon) |
| 9 | 6/A4.2 | A1.1 | 6/A4.2 | cited: cited in its governing row (Excel / canon) |
| 10 | 5/A4.2 | A1.1 | 5/A4.2 | cited: cited in its governing row (Excel / canon) |
| 11 | 2/A4.2 | A1.1 | 2/A4.2 | cited: cited in its governing row (Excel / canon) |
| 12 | 2/A2.1 | A1.1 | 2/A2.1 | out of scope: North exterior elevation: CMU (2A / 2B) with the stucco cornice (5) on masonry and PEMB flashing; no cold-formed framing or gypsum board on this facade (its sec |
| 13 | 4/A3.2 | A1.1 | 4/A3.2 | cited: cited in its governing row (Excel / canon) |
| 14 | 4/A2.1 | A1.1 | 4/A2.1 | cited: cited in its governing row (Excel / canon) |
| 15 | 3/A3.2 | A1.1 | 3/A3.2 | cited: cited in its governing row (Excel / canon) |
| 16 | 2/A3.4 | A1.1 | 2/A3.4 | cited: cited in its governing row (Excel / canon) |
| 17 | 2/A4.2 | A1.1 | 2/A4.2 | cited: cited in its governing row (Excel / canon) |
| 18 | 1/A3.4 | A1.1 | 1/A3.4 | cited: cited in its governing row (Excel / canon) |
| 19 | 14/A4.1 | A1.1 | 14/A4.1 | cited: cited in its governing row (Excel / canon) |
| 20 | 6/A4.2 | A1.1 | 6/A4.2 | cited: cited in its governing row (Excel / canon) |
| 21 | 2/A4.2 | A1.1 | 2/A4.2 | cited: cited in its governing row (Excel / canon) |
| 22 | 1/A4.2 | A1.1 | 1/A4.2 | out of scope: Column detail: FIRE TREATED 2X NAILERS (key note 10) inside the sheet metal column enclosure (key note 16) of the storefront PEMB column = wood blocking / naile |
| 23 | 7/A3.2 | A1.1 | 7/A3.2 | cited: cited in its governing row (Excel / canon) |
| 24 | 5/A4.2 | A1.1 | 5/A4.2 | cited: cited in its governing row (Excel / canon) |
| 25 | 2/A3.1 | A1.1 | 2/A3.1 | cited: cited in its governing row (Excel / canon) |
| 26 | 1/A3.2 | A1.1 | 1/A3.2 | cited: cited in its governing row (Excel / canon) |
| 27 | 1/A3.1 | A1.1 | 1/A3.1 | cited: cited in its governing row (Excel / canon) |
| 28 | 3/A3.1 | A1.1 | 3/A3.1 | cited: cited in its governing row (Excel / canon) |
| 29 | 1/A2.1 | A1.1 | 1/A2.1 | cited: cited in its governing row (Excel / canon) |
| 30 | 10/A5.2 | A1.1 | 10/A5.2 | cited: cited in its governing row (Excel / canon) |
| 31 | 11/A4.1 | A4.1 | 11/A4.1 | same sheet: references another view of the same sheet |
| 32 | 6/A4.1 | A4.1 | 6/A4.1 | same sheet: references another view of the same sheet |
| 33 | 2/A4.1 | A4.1 | 2/A4.1 | same sheet: references another view of the same sheet |
| 34 | 12/A4.1 | A4.1 | 12/A4.1 | same sheet: references another view of the same sheet |
| 35 | 7/A4.1 | A4.1 | 7/A4.1 | same sheet: references another view of the same sheet |
| 36 | 9/A4.1 | A4.1 | 9/A4.1 | same sheet: references another view of the same sheet |
| 37 | 5/A4.1 | A4.1 | 5/A4.1 | same sheet: references another view of the same sheet |
| 38 | 3/A4.1 | A4.1 | 3/A4.1 | same sheet: references another view of the same sheet |
| 39 | 8/A4.1 | A4.1 | 8/A4.1 | same sheet: references another view of the same sheet |
| 40 | 4/A4.1 | A4.1 | 4/A4.1 | same sheet: references another view of the same sheet |
| 41 | 13/A4.1 | A4.1 | 13/A4.1 | same sheet: references another view of the same sheet |
| 42 | 11/A4.1 | A4.1 | 11/A4.1 | same sheet: references another view of the same sheet |
| 43 | 7/A4.2 | A4.1 | 7/A4.2 | cited: cited in its governing row (Excel / canon) |
| 44 | 7/A4.2 | A4.1 | 7/A4.2 | cited: cited in its governing row (Excel / canon) |
| 45 | 7/A4.2 | A4.1 | 7/A4.2 | cited: cited in its governing row (Excel / canon) |
| 46 | 6/A4.2 | A4.1 | 6/A4.2 | cited: cited in its governing row (Excel / canon) |
| 47 | 6/A4.2 | A4.1 | 6/A4.2 | cited: cited in its governing row (Excel / canon) |
| 48 | 2/A4.2 | A4.1 | 2/A4.2 | cited: cited in its governing row (Excel / canon) |
| 49 | 2/A4.2 | A4.1 | 2/A4.2 | cited: cited in its governing row (Excel / canon) |
| 50 | 2/A3.2 | A3.4 | 2/A3.2 | cited: cited in its governing row (Excel / canon) |
| 51 | 4/A3.4 | A3.4 | 4/A3.4 | same sheet: references another view of the same sheet |
| 52 | 5/A3.4 | A3.4 | 5/A3.4 | same sheet: references another view of the same sheet |
| 53 | 5/A3.1 | A3.4 | 5/A3.1 | out of scope: Section at the CMU parapet cap: CMU bond beam (5), FRT 2x nailer (11) = Div. 06 (estimator decision RFI-12), PEMB coping flashing (29 / 17): no framing or gypsu |
| 54 | 11/A5.2 | A3.4 | 11/A5.2 | cited: cited in its governing row (Excel / canon) |
| 55 | 12/A5.2 | A3.4 | 12/A5.2 | cited: cited in its governing row (Excel / canon) |
| 56 | 13/A5.2 | A3.4 | 13/A5.2 | cited: cited in its governing row (Excel / canon) |
| 57 | 6/A3.1 | A3.4 | 6/A3.1 | cited: cited in its governing row (Excel / canon) |
| 58 | 3/A3.2 | A3.2 | 3/A3.2 | same sheet: references another view of the same sheet |
| 59 | 5/A3.2 | A3.2 | 5/A3.2 | same sheet: references another view of the same sheet |
| 60 | 5/A3.2 | A3.2 | 5/A3.2 | same sheet: references another view of the same sheet |
| 61 | 5/A3.2 | A3.2 | 5/A3.2 | same sheet: references another view of the same sheet |
| 62 | 5/A3.2 | A3.2 | 5/A3.2 | same sheet: references another view of the same sheet |
| 63 | 1/A3.3 | A3.2 | 1/A3.3 | out of scope: Thru wall scupper detail (PEMB sheet metal scupper through the CMU parapet): sheet metal / masonry, no framing or gypsum board |
| 64 | 5/A5.1 | A3.2 | 5/A5.1 | cited: cited in its governing row (Excel / canon) |
| 65 | 1/A5.1 | A3.2 | 1/A5.1 | cited: cited in its governing row (Excel / canon) |
| 66 | 2/A5.1 | A3.2 | 2/A5.1 | cited: cited in its governing row (Excel / canon) |
| 67 | 6/A5.1 | A3.2 | 6/A5.1 | cited: cited in its governing row (Excel / canon) |
| 68 | 5/A6.1 | A3.2 | 5/A6.1 | out of scope: Stucco joint detail: exterior plaster system (lath, scratch / brown coats, expansion joint) = plaster trade, excluded (Scope Checklist); the sheathing behind it |
| 69 | 2/A3.1 | A2.1 | 2/A3.1 | cited: cited in its governing row (Excel / canon) |
| 70 | 3/A3.1 | A2.1 | 3/A3.1 | cited: cited in its governing row (Excel / canon) |
| 71 | 1/A3.2 | A2.1 | 1/A3.2 | cited: cited in its governing row (Excel / canon) |
| 72 | 1/A3.1 | A2.1 | 1/A3.1 | cited: cited in its governing row (Excel / canon) |
| 73 | 2/A3.4 | A2.1 | 2/A3.4 | cited: cited in its governing row (Excel / canon) |
| 74 | 3/A3.2 | A2.1 | 3/A3.2 | cited: cited in its governing row (Excel / canon) |
| 75 | 4/A3.2 | A2.1 | 4/A3.2 | cited: cited in its governing row (Excel / canon) |
| 76 | 2/A3.4 | A2.1 | 2/A3.4 | cited: cited in its governing row (Excel / canon) |
| 77 | 2/A3.2 | A2.1 | 2/A3.2 | cited: cited in its governing row (Excel / canon) |
| 78 | 3/A3.4 | A2.1 | 3/A3.4 | cited: cited in its governing row (Excel / canon) |
| 79 | 6/A3.2 | A2.1 | 6/A3.2 | out of scope: Section at the CMU pier cap: CMU (4), FRT 2x nailer (11) = Div. 06 (estimator decision RFI-12), PEMB flashing (29), sealant (23): no framing or gypsum board |
| 80 | 1/A3.4 | A2.1 | 1/A3.4 | cited: cited in its governing row (Excel / canon) |
| 81 | 2/A3.4 | A2.1 | 2/A3.4 | cited: cited in its governing row (Excel / canon) |
| 82 | 4/A3.2 | A2.1 | 4/A3.2 | cited: cited in its governing row (Excel / canon) |
| 83 | 8/A3.2 | A3.1 | 8/A3.2 | cited: cited in its governing row (Excel / canon) |
| 84 | 8/A3.2 | A3.1 | 8/A3.2 | cited: cited in its governing row (Excel / canon) |
| 85 | 8/A3.2 | A3.1 | 8/A3.2 | cited: cited in its governing row (Excel / canon) |
| 86 | 6/A3.1 | A3.1 | 6/A3.1 | same sheet: references another view of the same sheet |
| 87 | 2/A3.1 | A3.1 | 2/A3.1 | same sheet: references another view of the same sheet |
| 88 | 4/A3.1 | A3.1 | 4/A3.1 | same sheet: references another view of the same sheet |
| 89 | 1/A5.2 | A3.1 | 1/A5.2 | cited: cited in its governing row (Excel / canon) |
| 90 | 3/A5.2 | A3.1 | 3/A5.2 | cited: cited in its governing row (Excel / canon) |
| 91 | 1/A5.2 | A3.1 | 1/A5.2 | cited: cited in its governing row (Excel / canon) |
| 92 | 1/A4.2 | A3.1 | 1/A4.2 | out of scope: Column detail: FIRE TREATED 2X NAILERS (key note 10) inside the sheet metal column enclosure (key note 16) of the storefront PEMB column = wood blocking / naile |
| 93 | 4/A3.1 | A3.1 | 4/A3.1 | same sheet: references another view of the same sheet |
| 94 | 2/A5.2 | A3.1 | 2/A5.2 | cited: cited in its governing row (Excel / canon) |
| 95 | 2/A5.2 | A3.1 | 2/A5.2 | cited: cited in its governing row (Excel / canon) |
| 96 | 6/A5.2 | A3.1 | 6/A5.2 | cited: cited in its governing row (Excel / canon) |
| 97 | 6/A5.2 | A3.1 | 6/A5.2 | cited: cited in its governing row (Excel / canon) |
| 98 | 6/A5.2 | A3.1 | 6/A5.2 | cited: cited in its governing row (Excel / canon) |
| 99 | 6/A3.4 | A3.1 | 6/A3.4 | cited: cited in its governing row (Excel / canon) |
| 100 | 6/A3.4 | A3.1 | 6/A3.4 | cited: cited in its governing row (Excel / canon) |
| 101 | 3/A5.2 | A5.2 | 3/A5.2 | same sheet: references another view of the same sheet |
| 102 | 1/A5.2 | A5.2 | 1/A5.2 | same sheet: references another view of the same sheet |
| 103 | 3/A5.2 | A5.2 | 3/A5.2 | same sheet: references another view of the same sheet |
| 104 | 3/A5.2 | A5.2 | 3/A5.2 | same sheet: references another view of the same sheet |
| 105 | 11/A5.2 | A5.2 | 11/A5.2 | same sheet: references another view of the same sheet |
| 106 | 2/A5.2 | A5.2 | 2/A5.2 | same sheet: references another view of the same sheet |
| 107 | 2/A5.2 | A5.2 | 2/A5.2 | same sheet: references another view of the same sheet |
| 108 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 109 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 110 | 12/A5.2 | A5.2 | 12/A5.2 | same sheet: references another view of the same sheet |
| 111 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 112 | 8/A5.2 | A5.2 | 8/A5.2 | same sheet: references another view of the same sheet |
| 113 | 7/A5.2 | A5.2 | 7/A5.2 | same sheet: references another view of the same sheet |
| 114 | 9/A5.2 | A5.2 | 9/A5.2 | same sheet: references another view of the same sheet |
| 115 | 9/A5.2 | A5.2 | 9/A5.2 | same sheet: references another view of the same sheet |
| 116 | 7/A5.2 | A5.2 | 7/A5.2 | same sheet: references another view of the same sheet |
| 117 | 6/A5.2 | A5.2 | 6/A5.2 | same sheet: references another view of the same sheet |
| 118 | 8/A5.2 | A5.2 | 8/A5.2 | same sheet: references another view of the same sheet |
| 119 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 120 | 9/A5.2 | A5.2 | 9/A5.2 | same sheet: references another view of the same sheet |
| 121 | 13/A5.2 | A5.2 | 13/A5.2 | same sheet: references another view of the same sheet |
| 122 | 5/A5.2 | A5.2 | 5/A5.2 | same sheet: references another view of the same sheet |
| 123 | 6/A5.2 | A5.2 | 6/A5.2 | same sheet: references another view of the same sheet |
| 124 | 6/A5.2 | A5.2 | 6/A5.2 | same sheet: references another view of the same sheet |
| 125 | 6/A5.2 | A5.2 | 6/A5.2 | same sheet: references another view of the same sheet |
| 126 | 6/A5.2 | A5.2 | 6/A5.2 | same sheet: references another view of the same sheet |
| 127 | 5/A5.2 | A5.2 | 5/A5.2 | same sheet: references another view of the same sheet |
| 128 | 9/A5.2 | A5.2 | 9/A5.2 | same sheet: references another view of the same sheet |
| 129 | 7/A5.2 | A5.2 | 7/A5.2 | same sheet: references another view of the same sheet |
| 130 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 131 | 4/A5.2 | A5.2 | 4/A5.2 | same sheet: references another view of the same sheet |
| 132 | 8/A5.2 | A5.2 | 8/A5.2 | same sheet: references another view of the same sheet |
| 133 | 9/A5.2 | A5.2 | 9/A5.2 | same sheet: references another view of the same sheet |
| 134 | 3/A3.3 | A3.3 | 3/A3.3 | same sheet: references another view of the same sheet |
| 135 | 5/A3.3 | A3.3 | 5/A3.3 | same sheet: references another view of the same sheet |
| 136 | 4/A3.3 | A3.3 | 4/A3.3 | same sheet: references another view of the same sheet |
| 137 | 2/A5.1 | A5.1 | 2/A5.1 | same sheet: references another view of the same sheet |
| 138 | 1/A5.1 | A5.1 | 1/A5.1 | same sheet: references another view of the same sheet |

## SCHEDULES_MATERIALES

Every trade schedule reviewed (U-142): each partition type / row is marked (red circle + check + number) on its schedule sheet in `Planos marcados/SCHEDULES_REVISADOS.pdf`; each material is matched to its Material Summary row or declared out of scope with its reason. Read independently from the drawings (fichas.json / schedules_indep.json, U-111).

| # | Schedule | Type / row | Sheet | Material | Value | Material Summary row / out of scope |
|---|---|---|---|---|---|---|
| 1 | Partition / wall types | S21 | A1.1 | stud: Z-furring | 1-1/2" Z-furring (no studs) 150ZF125-18 25 ga @ 24" O.C. | 1-1/2" Z-furring channel (LF of material) |
| 1 | Partition / wall types | S21 | A1.1 | board (one side (furring face; side wording not printed in the type)) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 1 | Partition / wall types | S21 | A1.1 | extra: Z-furring | 1-1/2" foil face polyisocyanurate insulation (min R-9) between Z-furring | 1-1/2" Z-furring channel (LF of material) |
| 1 | Partition / wall types | S21 | A1.1 | extra: polyiso | 1-1/2" foil face polyisocyanurate insulation (min R-9) between Z-furring | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 1 | Partition / wall types | S21 | A1.1 | extra: CMU | applied to exterior CMU (refer wall sections) | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 1 | Partition / wall types | S21 | A1.1 | extra: MR | A1.1 Interior Wall Notes 3.B: MR Type X board at wet locations | 5/8" gypsum board, Type X W.R. (water resistant) |
| 1 | Partition / wall types | S21 | A1.1 | extra: Type X board | A1.1 Interior Wall Notes 3.B: MR Type X board at wet locations | 5/8" gypsum board, Type X |
| 1 | Partition / wall types | S21 | A1.1 | extra: sealant | A1.1 Interior Wall Notes 4.B: sealant both sides of bottom track at acoustical insulated walls (not applicable to type as printed) | OUT OF SCOPE: ALC-19: EXCLUDED: acoustical sealant excluded in all projects (estimator standing order); sound attenuation insulation |
| 2 | Partition / wall types | S24 | A1.1 | stud | 3-5/8" 362S162-33 20 ga @ 24" O.C. | 3-5/8" metal stud (LF of material) - 362S162-33 |
| 2 | Partition / wall types | S24 | A1.1 | track (bottom / top) | 3-5/8" track (type S24) | Bottom track 3-5/8" |
| 2 | Partition / wall types | S24 | A1.1 | board (interior side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 2 | Partition / wall types | S24 | A1.1 | height | studs to 8'-6" A.F.F.; board interior side to 8'-6" A.F.F. | Partition Takeoff (Height) |
| 2 | Partition / wall types | S24 | A1.1 | extra: 150ZF | 150ZF125-18 Z-furring @24" O.C. on CMU with 1-1/2" foil face polyisocyanurate insulation (min R-9) between | 1-1/2" Z-furring channel (LF of material) |
| 2 | Partition / wall types | S24 | A1.1 | extra: polyiso | 150ZF125-18 Z-furring @24" O.C. on CMU with 1-1/2" foil face polyisocyanurate insulation (min R-9) between | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 2 | Partition / wall types | S24 | A1.1 | extra: CMU | 150ZF125-18 Z-furring @24" O.C. on CMU with 1-1/2" foil face polyisocyanurate insulation (min R-9) between | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 2 | Partition / wall types | S24 | A1.1 | extra: CMU | exterior CMU construction (refer wall sections) | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 3 | Partition / wall types | S41 | A1.1 | stud | 3-5/8" 362S162-33 20 ga @ 24" O.C. | 3-5/8" metal stud (LF of material) - 362S162-33 |
| 3 | Partition / wall types | S41 | A1.1 | track (bottom / top) | 3-5/8" track (type S41) | Bottom track 3-5/8" |
| 3 | Partition / wall types | S41 | A1.1 | board (interior side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 3 | Partition / wall types | S41 | A1.1 | height | studs to 12'-0" A.F.F.; board interior side to 12'-0" A.F.F. | Partition Takeoff (Height) |
| 4 | Partition / wall types | S42 | A1.1 | stud | 3-5/8" | 3-5/8" metal stud (LF of material) - 362S162-33 |
| 4 | Partition / wall types | S42 | A1.1 | track (bottom / top) | 3-5/8" track (type S42) | Bottom track 3-5/8" |
| 4 | Partition / wall types | S42 | A1.1 | slip track: deflection channel | deflection channels at top track for 1-1/2" minimum deflection (A1.1 Interior Wall Notes 2.C, where framing extends to roof deck/structure) | Deep-leg slotted deflection track - printed product (see Where it comes from) - 3-5/8" web |
| 4 | Partition / wall types | S42 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 4 | Partition / wall types | S42 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 4 | Partition / wall types | S42 | A1.1 | height | studs to roof framing above; board each side: Parts Area "A" to 12'-0" A.F.F., Parts Areas "B" and "C" to bottom of roof framing | Partition Takeoff (Height) |
| 4 | Partition / wall types | S42 | A1.1 | extra: 362S162-33 | A4.2 sections 5 & 6 (not tagged S42): 362S162-33 framing attached to roof structure (keynote 2/A4.2, refer structural), 5/8" Type X both sides to 6" above finis | 3-5/8" metal stud (LF of material) - 362S162-33 |
| 5 | Partition / wall types | S43 | A1.1 | stud | 3-5/8" 362S162-33 20 ga @ 24" O.C. | 3-5/8" metal stud (LF of material) - 362S162-33 |
| 5 | Partition / wall types | S43 | A1.1 | track (bottom / top) | 3-5/8" track (type S43) | Bottom track 3-5/8" |
| 5 | Partition / wall types | S43 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 5 | Partition / wall types | S43 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 5 | Partition / wall types | S43 | A1.1 | height | studs to 8'-6" A.F.F.; board height not printed in the type | Partition Takeoff (Height) |
| 5 | Partition / wall types | S43 | A1.1 | extra: batt | 3-1/2" unfaced sound batt insulation | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 5 | Partition / wall types | S43 | A1.1 | extra: sealant | sealant both sides of bottom track at acoustical insulated walls (A1.1 Interior Wall Notes 4.B) | OUT OF SCOPE: ALC-19: EXCLUDED: acoustical sealant excluded in all projects (estimator standing order); sound attenuation insulation |
| 5 | Partition / wall types | S43 | A1.1 | extra: MR | MR Type X at wet locations - restrooms (A1.1 Interior Wall Notes 3.B) | 5/8" gypsum board, Type X W.R. (water resistant) |
| 5 | Partition / wall types | S43 | A1.1 | extra: batt | 7/A4.2 (not tagged): 8'-6" wall with 600S162-54 ceiling joists @24" O.C., 6" sound batt above, 5/8" Type X wraps to B.O. framing EL 108'-6" | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 5 | Partition / wall types | S43 | A1.1 | extra: Type X wraps | 7/A4.2 (not tagged): 8'-6" wall with 600S162-54 ceiling joists @24" O.C., 6" sound batt above, 5/8" Type X wraps to B.O. framing EL 108'-6" | 5/8" gypsum board, Type X |
| 5 | Partition / wall types | S43 | A1.1 | extra: 600S162-54 | 7/A4.2 (not tagged): 8'-6" wall with 600S162-54 ceiling joists @24" O.C., 6" sound batt above, 5/8" Type X wraps to B.O. framing EL 108'-6" | 6" metal stud (LF of material) - 600S162-54 |
| 6 | Partition / wall types | S61 | A1.1 | stud | 6" 600S162-33 20 ga @ 24" O.C. | 6" metal stud (LF of material) - 600S162-33 |
| 6 | Partition / wall types | S61 | A1.1 | track (bottom / top) | 6" track (type S61) | Bottom track 6" - 600T125-33 |
| 6 | Partition / wall types | S61 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 6 | Partition / wall types | S61 | A1.1 | board (each side) x1: 5/8" Type X | 5/8" Type X | 5/8" gypsum board, Type X |
| 6 | Partition / wall types | S61 | A1.1 | height | studs to 8'-6" A.F.F.; board height not printed in the type | Partition Takeoff (Height) |
| 6 | Partition / wall types | S61 | A1.1 | extra: batt | 3-1/2" unfaced sound batt insulation | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 6 | Partition / wall types | S61 | A1.1 | extra: sealant | sealant both sides of bottom track at acoustical insulated walls (A1.1 Interior Wall Notes 4.B) | OUT OF SCOPE: ALC-19: EXCLUDED: acoustical sealant excluded in all projects (estimator standing order); sound attenuation insulation |
| 6 | Partition / wall types | S61 | A1.1 | extra: MR | MR Type X at wet walls (A1.1 note 3.B) | 5/8" gypsum board, Type X W.R. (water resistant) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | stud | 8" + 6" (two stud layers) | 8" stud (all gauges) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | track (bottom / top) | 8" track (type EXT_1-A3.1) | Bottom track 8" |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | board (exterior side) x1: fiberglass reinforced sheathing | 5/8" exterior fiberglass reinforced sheathing w/ continuous weather barrier (glass mat) | 5/8" glass mat sheathing (exterior face of the stud) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | board (interior side) x1: 1/4" gyp | 5/8" Type X (keynote 20) and 1/4" gypsum board (keynote 35) over 087F125-33 resilient channel | 1/4" gypsum board - printed (see Where it comes from) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | board (interior side) x1: 087F125 | 5/8" Type X (keynote 20) and 1/4" gypsum board (keynote 35) over 087F125-33 resilient channel | Resilient channel - printed product (see Where it comes from) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | height | studs FF EL 100'-0" to T.O. metal stud EL 120'-8" (dims 5'-8"+5'-8"+...+5'-0 3/4"+4'-3 1/4" printed); interior board stops just above ACT ceiling - elevation no | Partition Takeoff (Height) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: R-19 | 6" (R-19) batt with foil face vapor barrier (kn 16) | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: 087F125 | 087F125-33 double leg resilient channel @24" O.C. horizontal (kn 33) | Resilient channel - printed product (see Where it comes from) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: stucco | stucco over self-furring lath (kn 13) | OUT OF SCOPE: ALC-STUCCO: EXCLUDED: plaster / masonry trades (A3.1 keys 13 / 14 / 18, 1/A5.2, A2.1) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: nailer | FT 2x nailer continuous at top (kn 11) | OUT OF SCOPE: ALC-FRT-NAILERS: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: FRT parapet / T.O. |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: FT 2x | FT 2x nailer continuous at top (kn 11) | OUT OF SCOPE: ALC-16: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: FRT 2x blocking (S |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: framing clips | CFMF framing clips (kn 9) | Framing clips per stud - printed product (see Where it comes from) |
| 7 | Partition / wall types | EXT_1-A3.1 | A3.1 | extra: insulation | rigid insulation R-10 at slab edge (kn 36) | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | stud | 6" + 8" (side by side, 1'-2" overall) 600S162-54 + 800S162-54 16 ga @ 16" O.C. | 6" metal stud (LF of material) - 600S162-54 |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | track (bottom / top) | 6" track (type EXT_3-S5.3) | Bottom track 6" - 600T125-54 |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | board (exterior side) x1: sheathing per arch | sheathing per architectural (kn 8: fasten @8" O.C. w/ #6x1-1/4" screws) | 5/8" glass mat sheathing (exterior face of the stud) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | board (exterior side) x1: fasten | sheathing per architectural (kn 8: fasten @8" O.C. w/ #6x1-1/4" screws) | OUT OF SCOPE: ALC-FASTENERS: EXCLUDED: all fasteners excluded by estimator order (S1.1 notes not carried) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | height | EL. see arch (top and bottom not dimensioned on S5.3); storefront head below | Partition Takeoff (Height) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: 362S162-43 | 362S162-43 (3-5/8" x 18 ga) stud ties @48" O.C., min (2) #8 screws each stud (kn 19) | 3-5/8" metal stud (LF of material) - 362S162-43 |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: screws | 362S162-43 (3-5/8" x 18 ga) stud ties @48" O.C., min (2) #8 screws each stud (kn 19) | OUT OF SCOPE: ALC-FASTENERS: EXCLUDED: all fasteners excluded by estimator order (S1.1 notes not carried) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: fasten | studs fastened together w/ #10 screws @24" O.C. (kn 20) | OUT OF SCOPE: ALC-FASTENERS: EXCLUDED: all fasteners excluded by estimator order (S1.1 notes not carried) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: FCB43 | Simpson FCB43.5 clips to PEMB wind beam (kn 16) | Framing clips per stud - printed product (see Where it comes from) |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: cornice | cornice per architectural (kn 21) | 6" metal stud (LF of material) - 600S162-43 |
| 8 | Partition / wall types | EXT_3-S5.3 | S5.3 | extra: 600S162-43 | related: kn 22 6"x18ga min 600S162-43 @16" O.C. (other sections) | 6" metal stud (LF of material) - 600S162-43 |
| 9 | DOOR SCHEDULE | 1 | A5.1 | trade: Storefront | Storefront door in aluminum storefront; 4/A5.2 head/jamb shows no metal framing or gyp board (storefront only) | OUT OF SCOPE: not our trade: aluminum storefront, Div. 08 41 (by the glazing contractor) |
| 9 | DOOR SCHEDULE | 1 | A5.1 | trade | no CFMF / drywall item at this opening from schedule | OUT OF SCOPE: no trade material printed in this row |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: 150ZF | Exterior CMU wall: per 1/A5.1 and 2/A5.1 150ZF125-18 cold form metal Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gypsum board returning to HM frame | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: polyiso | Exterior CMU wall: per 1/A5.1 and 2/A5.1 150ZF125-18 cold form metal Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gypsum board returning to HM frame | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: 5/8" Type X gyp | Exterior CMU wall: per 1/A5.1 and 2/A5.1 150ZF125-18 cold form metal Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gypsum board returning to HM frame | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: HM frame | Exterior CMU wall: per 1/A5.1 and 2/A5.1 150ZF125-18 cold form metal Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gypsum board returning to HM frame | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: CMU | Exterior CMU wall: per 1/A5.1 and 2/A5.1 150ZF125-18 cold form metal Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gypsum board returning to HM frame | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: fire treated 2x | fire treated 2x4 wood blocking anchored to masonry (not CFMF, note only) | OUT OF SCOPE: ALC-16: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: FRT 2x blocking (S |
| 10 | DOOR SCHEDULE | 2 | A5.1 | trade: masonry | fire treated 2x4 wood blocking anchored to masonry (not CFMF, note only) | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: 150ZF | Overhead door 6'-0" x 8'-0" in CMU: per 5/A5.1 & 6/A5.1 150ZF125-18 Z-furring at 24" o.c. + 5/8" Type X gyp board at head and jambs; sheet metal 24 ga cladding  | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: 5/8" Type X gyp | Overhead door 6'-0" x 8'-0" in CMU: per 5/A5.1 & 6/A5.1 150ZF125-18 Z-furring at 24" o.c. + 5/8" Type X gyp board at head and jambs; sheet metal 24 ga cladding  | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: sheet metal | Overhead door 6'-0" x 8'-0" in CMU: per 5/A5.1 & 6/A5.1 150ZF125-18 Z-furring at 24" o.c. + 5/8" Type X gyp board at head and jambs; sheet metal 24 ga cladding  | OUT OF SCOPE: not our trade: sheet metal cladding / flashing, Div. 07 62 (not metal framing / drywall) |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: CMU | Overhead door 6'-0" x 8'-0" in CMU: per 5/A5.1 & 6/A5.1 150ZF125-18 Z-furring at 24" o.c. + 5/8" Type X gyp board at head and jambs; sheet metal 24 ga cladding  | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: fire treated blocking | detail note: provide additional metal framing or fire treated blocking as required for door/track mounting | OUT OF SCOPE: ALC-16: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: FRT 2x blocking (S |
| 11 | DOOR SCHEDULE | 3 | A5.1 | trade: additional metal framing or fire treated blocking | detail note: provide additional metal framing or fire treated blocking as required for door/track mounting | OUT OF SCOPE: RFI-21 closed (estimator decision) |
| 12 | DOOR SCHEDULE | 4 | A5.1 | trade: box header | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | Header / metal stud box beam |
| 12 | DOOR SCHEDULE | 4 | A5.1 | trade: HM frame | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 12 | DOOR SCHEDULE | 4 | A5.1 | trade: 5/8" gyp | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 12 | DOOR SCHEDULE | 4 | A5.1 | trade: 362S162-33 | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 3-5/8" metal stud (LF of material) - 362S162-33 [material match: this element is not itemized under its own ID] |
| 12 | DOOR SCHEDULE | 4 | A5.1 | trade: hollow metal | Frame type 2 = hollow metal frame 16 ga, (3) min anchors per jamb (frame by others; anchoring into studs) | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 13 | DOOR SCHEDULE | 5 | A5.1 | trade: box header | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | Header / metal stud box beam |
| 13 | DOOR SCHEDULE | 5 | A5.1 | trade: HM frame | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 13 | DOOR SCHEDULE | 5 | A5.1 | trade: 5/8" gyp | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 13 | DOOR SCHEDULE | 5 | A5.1 | trade: 362S162-33 | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 3-5/8" metal stud (LF of material) - 362S162-33 [material match: this element is not itemized under its own ID] |
| 13 | DOOR SCHEDULE | 5 | A5.1 | trade: hollow metal | Frame type 2 = hollow metal frame 16 ga, (3) min anchors per jamb (frame by others; anchoring into studs) | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 14 | DOOR SCHEDULE | 6 | A5.1 | trade: box header | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | Header / metal stud box beam |
| 14 | DOOR SCHEDULE | 6 | A5.1 | trade: HM frame | Interior HM frame: per 7/A5.1 head = 600S162-33 cold form metal box header | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 14 | DOOR SCHEDULE | 6 | A5.1 | trade: 5/8" gyp | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 14 | DOOR SCHEDULE | 6 | A5.1 | trade: 362S162-33 | per 8/A5.1 jamb = 362S162-33 CFMF studs at 24" o.c., DOUBLE studs at jambs; 5/8" gyp board shown each side of stud wall (wall per interior wall types) | 3-5/8" metal stud (LF of material) - 362S162-33 [material match: this element is not itemized under its own ID] |
| 14 | DOOR SCHEDULE | 6 | A5.1 | trade: hollow metal | Frame type 2 = hollow metal frame 16 ga, (3) min anchors per jamb (frame by others; anchoring into studs) | OUT OF SCOPE: not our trade: hollow metal frame and its anchors, Div. 08 11 (by the frame installer) |
| 15 | DOOR SCHEDULE | 7 | A5.1 | trade: 150ZF | Exterior CMU wall: per 3/A5.1 & 4/A5.1 150ZF125-18 Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gyp board (3/A5.1 also shows sheet metal 24 ga cladding | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 15 | DOOR SCHEDULE | 7 | A5.1 | trade: polyiso | Exterior CMU wall: per 3/A5.1 & 4/A5.1 150ZF125-18 Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gyp board (3/A5.1 also shows sheet metal 24 ga cladding | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 15 | DOOR SCHEDULE | 7 | A5.1 | trade: 5/8" Type X gyp | Exterior CMU wall: per 3/A5.1 & 4/A5.1 150ZF125-18 Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gyp board (3/A5.1 also shows sheet metal 24 ga cladding | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 15 | DOOR SCHEDULE | 7 | A5.1 | trade: sheet metal | Exterior CMU wall: per 3/A5.1 & 4/A5.1 150ZF125-18 Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gyp board (3/A5.1 also shows sheet metal 24 ga cladding | OUT OF SCOPE: not our trade: sheet metal cladding / flashing, Div. 07 62 (not metal framing / drywall) |
| 15 | DOOR SCHEDULE | 7 | A5.1 | trade: CMU | Exterior CMU wall: per 3/A5.1 & 4/A5.1 150ZF125-18 Z-furring at 24" o.c. w/ 1 1/2" polyiso + 5/8" Type X gyp board (3/A5.1 also shows sheet metal 24 ga cladding | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 16 | DOOR SCHEDULE | 8 | A5.1 | trade: Storefront | Storefront door; 4/A5.2 shows no CFMF/gyp; no trade item from schedule | OUT OF SCOPE: not our trade: aluminum storefront, Div. 08 41 (by the glazing contractor) |
| 17 | WINDOW TYPES | A | A5.2 | trade: R-19 | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 17 | WINDOW TYPES | A | A5.2 | trade: 1/4" gyp | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | 1/4" gypsum board - printed (see Where it comes from) |
| 17 | WINDOW TYPES | A | A5.2 | trade: 5/8" Type X gyp | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | 5/8" gypsum board, Type X |
| 17 | WINDOW TYPES | A | A5.2 | trade: resilient channel | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | Resilient channel - printed product (see Where it comes from) [material match: this element is not itemized under its own ID] |
| 17 | WINDOW TYPES | A | A5.2 | trade: plywood | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | OUT OF SCOPE: ALC-10: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: 5/8" FRT plywood a |
| 17 | WINDOW TYPES | A | A5.2 | trade: and 8" CFMF | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | 8" stud (all gauges) |
| 17 | WINDOW TYPES | A | A5.2 | trade: 6" and 8" CFMF | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | 6" metal stud (LF of material) - 600S162-54 |
| 17 | WINDOW TYPES | A | A5.2 | trade: suspended acoust | Head 1/A5.2: 6" and 8" CFMF, 6" R-19 batt, 7/8" cold form resilient channel, 1/4" gypsum board + 5/8" Type X gypsum board, 5/8" ext FT plywood sheathing, suspen | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 17 | WINDOW TYPES | A | A5.2 | trade: 1/4" Type X gyp | Jamb 2/A5.2: 6" and 8" CFMF, DOUBLE studs at jambs, 5/8" Type X + 1/4" Type X gyp board, 7/8" resilient channel, 5/8" fiberglass reinforced sheathing | 1/4" gypsum board - printed (see Where it comes from) |
| 17 | WINDOW TYPES | A | A5.2 | trade: resilient channel | Jamb 2/A5.2: 6" and 8" CFMF, DOUBLE studs at jambs, 5/8" Type X + 1/4" Type X gyp board, 7/8" resilient channel, 5/8" fiberglass reinforced sheathing | Resilient channel - printed product (see Where it comes from) [material match: this element is not itemized under its own ID] |
| 17 | WINDOW TYPES | A | A5.2 | trade: fiberglass reinforced sheathing | Jamb 2/A5.2: 6" and 8" CFMF, DOUBLE studs at jambs, 5/8" Type X + 1/4" Type X gyp board, 7/8" resilient channel, 5/8" fiberglass reinforced sheathing | 5/8" glass mat sheathing (exterior face of the stud) [material match: this element is not itemized under its own ID] |
| 17 | WINDOW TYPES | A | A5.2 | trade: and 8" CFMF | Jamb 2/A5.2: 6" and 8" CFMF, DOUBLE studs at jambs, 5/8" Type X + 1/4" Type X gyp board, 7/8" resilient channel, 5/8" fiberglass reinforced sheathing | 8" stud (all gauges) |
| 17 | WINDOW TYPES | A | A5.2 | trade: 6" and 8" CFMF | Jamb 2/A5.2: 6" and 8" CFMF, DOUBLE studs at jambs, 5/8" Type X + 1/4" Type X gyp board, 7/8" resilient channel, 5/8" fiberglass reinforced sheathing | 6" metal stud (LF of material) - 600S162-54 |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: R-19 | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: 5/8" Type X gyp | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 5/8" gypsum board, Type X |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: diagonal bracing | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: 6" CFMF | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: suspended acoust | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 18 | WINDOW TYPES | B1 | A5.2 | trade: storefront | Jambs 7/8/9 A5.2: storefront only, no CFMF/gyp printed | OUT OF SCOPE: not our trade: aluminum storefront, Div. 08 41 (by the glazing contractor) |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: R-19 | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: 5/8" Type X gyp | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 5/8" gypsum board, Type X |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: diagonal bracing | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: 6" CFMF | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: suspended acoust | Head 3/A5.2: 6" CFMF with diagonal bracing (per structural), 5/8" Type X gyp board, 6" R-19 batt, suspended acoustical lay-in ceiling | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 19 | WINDOW TYPES | B2 | A5.2 | trade: storefront | Jambs 7/8/9 A5.2: storefront only, no CFMF/gyp printed | OUT OF SCOPE: not our trade: aluminum storefront, Div. 08 41 (by the glazing contractor) |
| 20 | WINDOW TYPES | C | A5.2 | trade: 5/8" Type X gyp | Head 3/A5.2: 6" CFMF w/ diagonal bracing, 5/8" Type X gyp board, suspended ceiling | 5/8" gypsum board, Type X |
| 20 | WINDOW TYPES | C | A5.2 | trade: diagonal bracing | Head 3/A5.2: 6" CFMF w/ diagonal bracing, 5/8" Type X gyp board, suspended ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 20 | WINDOW TYPES | C | A5.2 | trade: 6" CFMF | Head 3/A5.2: 6" CFMF w/ diagonal bracing, 5/8" Type X gyp board, suspended ceiling | 6" metal stud (LF of material) - 600S162-43 |
| 20 | WINDOW TYPES | C | A5.2 | trade: suspended ceiling | Head 3/A5.2: 6" CFMF w/ diagonal bracing, 5/8" Type X gyp board, suspended ceiling | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: Z-furring | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: polyiso | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: 5/8" Type X gyp | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: plywood | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | OUT OF SCOPE: ALC-10: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: 5/8" FRT plywood a |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: 6" CFMF | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 6" metal stud (LF of material) - 600S162-54 [material match: this element is not itemized under its own ID] |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: Z-furring | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: 5/8" Type X gyp | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 21 | WINDOW TYPES | D1 | A5.2 | trade: CMU | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: Z-furring | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: polyiso | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: 5/8" Type X gyp | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: plywood | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | OUT OF SCOPE: ALC-10: EXCLUDED - wood blocking / plywood by others (Div. 06), user decision 2026-11-05, R-ALC-01: 5/8" FRT plywood a |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: 6" CFMF | Head 11/A5.2: 1 1/2" (25 ga) CFM Z-furring at 24" o.c. w/ 1 1/2" polyiso, 6" CFMF, 5/8" Type X gyp board, 5/8" FT plywood | 6" metal stud (LF of material) - 600S162-54 [material match: this element is not itemized under its own ID] |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: Z-furring | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | 1-1/2" Z-furring channel (LF of material) [material match: this element is not itemized under its own ID] |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: 5/8" Type X gyp | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | 5/8" gypsum board, Type X [material match: this element is not itemized under its own ID] |
| 22 | WINDOW TYPES | D2 | A5.2 | trade: CMU | Jamb 12/A5.2 and sill 13/A5.2: 1 1/2" (25 ga) Z-furring at 24" o.c. + 5/8" Type X gyp board at CMU opening | OUT OF SCOPE: not our trade: CMU / masonry, Div. 04 (the furring on it is carried as its own material) |
| 23 | GLAZING SCHEDULE | 1 | A5.2 | trade: glazing | none (glazing, not CFMF/drywall) | OUT OF SCOPE: not our trade: glazing, Div. 08 80 |
| 24 | GLAZING SCHEDULE | 2 | A5.2 | - | no trade material printed | OUT OF SCOPE: noted |
| 25 | INTERIOR FINISH SCHEDULE | 100 | A1.2 | trade: paint | Walls paint W-2/W-3 (gyp board type not printed in schedule) | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 25 | INTERIOR FINISH SCHEDULE | 100 | A1.2 | trade: C-1 | C-1 ACT 24x48x5/8 lay-in at 11'-6" (not drywall; note only) | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 26 | INTERIOR FINISH SCHEDULE | 100A | A1.2 | trade: C-3 | C-3 = PAINT ceiling at 11'-4" -> painted (hard) ceiling, substrate not printed (likely gyp board, verify) | 5/8" gypsum board, Type X |
| 26 | INTERIOR FINISH SCHEDULE | 100A | A1.2 | trade: PAINT | C-3 = PAINT ceiling at 11'-4" -> painted (hard) ceiling, substrate not printed (likely gyp board, verify) | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 27 | INTERIOR FINISH SCHEDULE | 101 | A1.2 | trade: insulation | C-2 exposed insulation/exposed steel framing - no ceiling board | OUT OF SCOPE: ALC-INSUL: EXCLUDED: estimator standing order (skill standing rule: insulation always excluded); printed: 1-1/2" foil-fac |
| 27 | INTERIOR FINISH SCHEDULE | 101 | A1.2 | trade: C-2 | C-2 exposed insulation/exposed steel framing - no ceiling board | OUT OF SCOPE: not our trade: C-2 exposed structure: no ceiling board printed, nothing to frame or board (A1.2 finish types) |
| 27 | INTERIOR FINISH SCHEDULE | 101 | A1.2 | trade: paint | walls paint, gyp board not printed | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 28 | INTERIOR FINISH SCHEDULE | 102 | A1.2 | trade: C-3 | C-3 painted ceiling at 8'-6" (substrate not printed) | 5/8" gypsum board, Type X |
| 28 | INTERIOR FINISH SCHEDULE | 102 | A1.2 | trade: paint | C-3 painted ceiling at 8'-6" (substrate not printed) | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 28 | INTERIOR FINISH SCHEDULE | 102 | A1.2 | trade: paint | walls W-2 paint (interior wall types elsewhere) | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 28 | INTERIOR FINISH SCHEDULE | 102 | A1.2 | trade: paint | Note 1: paint exterior of office with W-3 | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 29 | INTERIOR FINISH SCHEDULE | 103 | A1.2 | trade: W-4 | W-4 sanitary wall and ceiling panel system (FRP-type, note only) over walls | Sanitary wall panel system W-4 (see Where it comes from) |
| 29 | INTERIOR FINISH SCHEDULE | 103 | A1.2 | trade: C-3 | C-3 painted ceiling at 8'-6" | 5/8" gypsum board, Type X W.R. (water resistant) |
| 29 | INTERIOR FINISH SCHEDULE | 103 | A1.2 | trade: paint | C-3 painted ceiling at 8'-6" | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 30 | INTERIOR FINISH SCHEDULE | 104 | A1.2 | trade: W-4 | W-4 sanitary wall panel system (FRP-type, note only) | Sanitary wall panel system W-4 (see Where it comes from) |
| 30 | INTERIOR FINISH SCHEDULE | 104 | A1.2 | trade: C-3 | C-3 painted ceiling at 8'-6" | 5/8" gypsum board, Type X W.R. (water resistant) |
| 30 | INTERIOR FINISH SCHEDULE | 104 | A1.2 | trade: paint | C-3 painted ceiling at 8'-6" | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 31 | INTERIOR FINISH SCHEDULE | 105 | A1.2 | trade: C-2 | C-2 exposed structure, no ceiling board | OUT OF SCOPE: not our trade: C-2 exposed structure: no ceiling board printed, nothing to frame or board (A1.2 finish types) |
| 31 | INTERIOR FINISH SCHEDULE | 105 | A1.2 | trade: paint | walls paint, gyp board not printed | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 32 | INTERIOR FINISH TYPES | W-1 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 33 | INTERIOR FINISH TYPES | W-2 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 34 | INTERIOR FINISH TYPES | W-3 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 35 | INTERIOR FINISH TYPES | W-4 | A1.2 | trade: sanitary panel | FRP-type sanitary panel (note only) | Sanitary wall panel system W-4 (see Where it comes from) [material match: this element is not itemized under its own ID] |
| 36 | INTERIOR FINISH TYPES | C-1 | A1.2 | trade: ACT | ACT, not drywall (note only) | OUT OF SCOPE: ALC-ACT: EXCLUDED: by the acoustical ceiling installer (A1.2 finish legend C-1, A1.2 general note D, 9/A4.2) |
| 37 | INTERIOR FINISH TYPES | C-2 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 38 | INTERIOR FINISH TYPES | C-3 | A1.2 | trade: painted ceiling | painted ceiling - gyp board ceiling implied, not printed | 5/8" gypsum board, Type X |
| 38 | INTERIOR FINISH TYPES | C-3 | A1.2 | trade: paint | painted ceiling - gyp board ceiling implied, not printed | OUT OF SCOPE: not our trade: painting, Div. 09 91 (separate trade; the board under it is carried by its wall type) |
| 39 | INTERIOR FINISH TYPES | D-1 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 40 | INTERIOR FINISH TYPES | D-2 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
| 41 | INTERIOR FINISH TYPES | D-3 | A1.2 | trade | none / finish only | OUT OF SCOPE: no trade material printed in this row |
