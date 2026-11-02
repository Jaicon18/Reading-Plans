# CAMBIOS FINAL2 - Chuze Fitness Austin Bluffs take-off (FINAL -> FINAL2, 2026-11-02)

Source: 8_specs/SPEC_SWEEP.md, spec_sweep.json, RFI_SPECS.md (Project Manual sweep) and the estimator rule R-ALC-09 (project data sheet). FINAL files kept untouched. Built only through the tools.

## 1. Quantity check FINAL -> FINAL2

* Partition Takeoff: 126 rows / 126 rows, **0 differences**.
* Material Summary (rows renamed by the product relabels are matched by family):

| Item | Spec § | FINAL | FINAL2 | Delta |
|---|---|---|---|---|
| Bracing 1-1/2" C.R. channel: one continuous row within 12" of the top of studs at every 2" slip-track wall (tool R80w.43, per wall = its slip-track LF) | 09 22 16 2.2.C.1 | 5,390.39 LF / 388 pcs | 6,301.09 LF / 453 pcs | +910.70 LF (= 409.44 + 397.30 + 103.96 slip-track LF) |
| Alkali-resistant glass-fiber mesh tape at the cement backer joints (new row, 1,209.77 SF x 0.37 LF/SF) | 09 29 00 2.7.B.4; 09 30 13 3.3.K | - | 447.61 LF / 475 | +447.61 LF |
| Foam sealer gasket under the 600T250-54 bottom track (new row, D6F A-A429-6 + A-A429-7) | 05 40 00 2.9.E, 3.1.D; C/S200 | - | 22.41 LF / 24 | +22.41 LF |
| Corner bead split: curved-edge cornerbead on the reception arc (16/A502) | 09 29 00 2.6.A.2.g | 441.22 LF | 379.02 + 62.20 LF curved | 0 (product split) |
| Joint compound -> 'setting-type taping and sandable topping' | 09 29 00 2.7.C | 4,707.99 LB | 4,707.99 LB | 0 (relabel) |
| 600S162-33 studs, 600T250-54 track, 16 ga deep-leg track -> 'ASTM A1003 structural grade, G60' | 05 40 00 2.3.B, 2.6, 2.6.D | 432 / 22.41 + 22.41 / 11 LF | same | 0 (relabel) |
| MR row -> '5/8" gypsum board, Type X MR' | 09 29 00 2.3.E | 5,483.88 SF | 5,483.88 SF | 0 (relabel; tool R80w.45 keeps it in the MR family) |
| Drywall grid = Armstrong in Inputs notes and texts (no USG left) | 09 51 23 2.6; 01 60 00 | text | text | 0 |

## 2. Not loaded (Scope Checklist notes ALC-X48 ... ALC-X52)

* Level 1 joint finish above ceilings (09 29 00 3.1.G.1): share of board above the ceilings not printed -> compound / tape stay at the full yield.
* Isolation strip (09 22 16 2.4.B / 3.2.B): conditional (only where studs touch masonry / dissimilar metal): 0 to +68.40 LF.
* Armstrong DW90CAG / SB12P (09 51 23 2.6): no count on the plans.
* Temporary dust / noise partitions (01 35 16 1.5.A.1): GC general conditions.
* Texture, firestop track, steam-room mockups: none indicated.

## 3. RFIs (OPEN, Pending Items, A / B / C; the conservative option for quantities is loaded = current quantities)

| RFI | Question | (A) plans / specs | (B) code | Loaded |
|---|---|---|---|---|
| RFI-S01 (1 of 3) | stud gauge vs limiting height of 16 type-A walls at 22.83 ft (+ A-A421-15, A6C) | L/240: 362S162-54 @ 12" o.c. +2,371.6 LF net stud + 20 ga on A-A421-15 / A6C + 05 40 00 extras | L/120: 362S162-43 (18 ga) @ 16", 0 LF | current studs @ 16" (0 LF); gauge per B noted |
| RFI-S02 (2 of 3) | hanger wire 12 ga (RCP note 9, 13/A502) vs 0.16" (09 22 16 2.3.C) | A-1 12 ga 0 / A-2 0.16" product only | ASTM C636 12 ga, 0 | 12 ga, 2,428.49 LF / 187 hangers |
| RFI-S03 (3 of 3) | reception arc radius not printed (16/A502) | if R < 5/8" bend limit: +1,347.26 SF 1/4" flexible (2 layers), -673.63 SF 5/8" Type X | ASTM C840, 0 | 5/8" Type X 673.63 SF |

## 4. Tool changes (generic, test fails before, rows in tools/CAMBIOS_tools_v80w.md)

* R80w.41 new printed families: alkali-resistant mesh tape, sealer gasket (own regex, roll purchase, non-metal waste) - `test_spec_items.py`.
* R80w.42 trazabilidad: `trim_items[].product` splits the trim row by printed product; `constants.product_specs` adds grade / coating to a designation row - `test_spec_items.py`.
* R80w.43 canon: `constants.bracing_top_row_at_structure` = +1 bracing row x slip-track LF of each wall to structure - `test_spec_items.py`.
* R80w.44 plantilla: R-ALC-09 project data sheet as informative rows under the Inputs (no new sheets / columns) - `test_project_data.py`.
* R80w.45 familias: 'Type X MR (moisture resistant)' stays in the MR family - `test_mr_typex.py`.
* R80w.46 verificar / bitacora: a canon-renamed accessory row (acc_nombres) and quoted proper names in the project data sheet - `test_verificar_renombre.py`.

## PROJECT DATA SHEET (R-ALC-09)

| Field | Value | Sheet |
|---|---|---|
| Project name & city | Chuze Fitness - Austin Bluffs, Colorado Springs, CO | G001 title block |
| Address | 3630 Austin Bluffs Pkwy, Unit #C190, Colorado Springs, CO 80918 | G001 Project Data and Code Analysis |
| Project type | Interior tenant improvement: new fitness club in an existing retail tenant space, incl. demolition of the existing buildout, carpentry and MEP trades | G001 Project Scope |
| Owner / tenant | Tenant: Chuze Fitness (1011 Camino del Rio South, Suite 350, San Diego, CA 92108). Building owner / landlord: not printed [PENDING] | G001 Project Information (tenant); owner [PENDING] |
| Architect | DXU Architects, Inc., 15150 N. Hayden Rd., Suite 225, Scottsdale, AZ 85260 (Christine Smith) | G001 Project Information |
| GC (bidders) | Hilbers Inc. - bid due 11/04/2026 12:00 PM MST; NNI Construction - bid due 11/02/2026 6:00 PM MST (G001 'Contractor' left blank) | bid invitations (estimator); G001 Contractor = blank |
| Bid set | 25-352 Combined (106 pages); latest revision 8 - 10/12/2026 Owner Changes (35 sheets); G001 revisions 1 6/23/2026 Issue to Permit, 4-6 city / fire comments | G001 / AD101 title blocks (Project No 25-352) |
| Total SF | 37,952 SF (Building Analysis 'Square footage' prints 37,949 SF) | G001 Occupancy / Exit calculations |
| Stories | 1 (building height 30'-0") | G001 Building Analysis |
| Construction classification | III B, automatic sprinklered | G001 Building Analysis |
| Occupancy group(s) | A-3, B, E, I-4, S-1 (occupancy separation not required per IBC 508.3) | G001 Building Analysis |
| Codes (year) | 2023 Pikes Peak Regional Building Code; 2021 IFC; 2021 IEBC (Level 3 Alteration); 2021 IMC; 2021 IPC; 2023 NEC; 2021 IECC; 2021 IFGC; PPRBC Life Safety Plan; Colorado accessibility law (CRS Title 9) | G001 Applicable Codes |
| Occupant load | 662 occupants | G001 Occupancy / Exit calculations |
| Sprinklered | Yes - IBC 903.3.1.1 | G001 Building Analysis |
| Demolition | Yes - AD101 demolition floor plan, AD102 demolition RCP, AD103 demolition roof plan | AD101, AD102, AD103 |
| Specs in the set | Yes - separate Project Manual (1,025 pages; Div. 01, 05 40 00, 09 22 16, 09 29 00, 09 30 13, 09 51 23 read); not inside the 106-page drawing set | Project Manual (spec sweep 2026-11-02) |

## SHEETS REVIEWED

| Group | Sheets read | Not reviewed / not cited |
|---|---|---|
| [x] Cover / sheet index | G001 | - |
| [x] Code analysis / general (G) | G001, G002, G003, G004, G005 | - |
| [x] General notes | A010 (note 27), A000.A, G001 abbreviations | A000.B (interior wall verification plan) not cited |
| [x] Demolition + notes | AD101, AD102, AD103 (keynotes D0.xx) | - |
| [x] Specifications | Project Manual: 01 10 00, 01 25 00, 01 35 16, 01 60 00, 05 40 00, 05 50 00, 06 10 53, 06 16 00, 07 21 00, 07 92 00, 09 22 16, 09 29 00, 09 30 13, 09 51 23 | 05 41 00, 09 21 16, 07 84 00, 06 10 00 not in the manual |
| [x] Partition types + details | A301; A501, A502, A503, A503.C, A504, A505.A, A505.B, A506; A601, A602 | A503.A, A503.B (millwork) not cited |
| [x] Floor plans | A101, A102, A103, A111, A131, A001, A421-A435 | A002 (site details) not cited |
| [x] RCP | A121, A421.A, A422.A, A423.A, A424.A, A425.A, A426-A435 (combined plans) | - |
| [x] Elevations / sections | A201; A421.B-A437.A | - |
| [x] Enlarged / interior elevations | A421.B, A421.C, A422.B, A422.C, A423.B, A424.B, A424.C, A425.B, A425.C, A426.A, A427.B, A428.A, A429.A, A429.B, A431.A, A434.A, A435.A, A437, A437.A | - |
| [x] Schedules | A601, A610, A611; P601; E602 | - |
| [x] Structural | S100, S101, S200, S300 | - |
| [x] MEP | M000, M110, M120, M401, M402; P000, P110, P111, P401, P402, P601, P602; E110, E111, E112, E401, E601 | M601, M602, P120, P501, E000, E120, E402, E501, E603, E604, E605, E700 not reviewed (no partition / framing content expected; MEP is another trade) |
