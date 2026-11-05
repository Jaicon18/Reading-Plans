# Back-check - Consumer Cellular Centennial (CO2) - Metal Framing + Drywall Take-off

Independent back-check made only from the bid set (`plans/bidset_SIN_MARKUPS.pdf`) and the delivered files
(`8_excel/Consumer_Cellular_Centennial_Takeoff_FINAL_rev1.xlsx`, `8_excel/Consumer_Cellular_Centennial_markups_rev1.pdf`).
Scale: 1/4" = 1'-0" = 18 pt/ft (A100 / A200). Lengths re-measured from the A100 gray wall fills (vector) and the printed dimensions. Images: `img_bc/`.

## Checks

| # | Check | Result | Evidence (N/SHEET) | Image |
|---|---|---|---|---|
| 1 | Tag sweep | PASS | A100 has 17 tags: A3 x4, C3 x2, D x1, E3 x10. Each one maps to an Excel row: A3-01..04, C3-01 (both C3 tags), D-01, E3-01..13. Untagged items have a stated reason: cased opening (RFI-05), existing Hallway/Utility wall with door 3C (RFI-07). The untagged niche sides E3-06 / E3-08 sit between tagged niche walls, but the Excel gives no reason for them (see D6). | img_bc/bc_01_tag_sweep_A100.png |
| 2 | Blind re-measure (18 pt/ft) | PASS | Every wall is within 0.4 %. A3-01 14.413 / 14.411; A3-02 28.833 / 28.833; A3-03 44.83 / 44.83; A3-04 11.803 / 11.79; C3-01 31.553 (= printed 31'-6 1/2") + 4.0 opening = 35.55 / 35.54; D-01 7.667 / 7.667 (7'-8"); E3-01 7.256 / 7.25 (7'-3"); E3-02 6.69 / 6.69; E3-03 7.157 / 7.17 (7'-2"); E3-04 0.577 + 3.33 + 3.52 = 7.428 / 7.428; E3-06 / E3-08 1.083 / 1.083; E3-07 5.083 / 5.083; E3-09 0.75 + 3.33 + 2.913 = 7.0 / 7.0; E3-11 9.997 / 9.995; E3-12 / E3-13 2.323 / 2.333. | img_bc/bc_02_remeasure_A100.png |
| 3 | Heights | PASS | A200 ceilings: Sales / BOH / Hallway C-2 11'-11", Office / Utility C-2 9'-0", Restroom C-1 8'-0". Board height is the ceiling + 6" (12.417 / 9.5 / 8.5 ft) on every face, as checked. Studs for A / C / D go to deck: 17.13 in Sales (A3-01, -02, -03), 16.333 in BOH (A3-04, D-01). Studs for E3 go to the higher ceiling + 6"; E3-12 / -13 use 9.5. C3-01 at 17.13 is the conservative choice, open under RFI-01. A3-04+03 at 16.964 is the length-weighted mix of the two. | img_bc/bc_03_heights_A200.png, img_bc/bc_03b_deck_A100.png |
| 4 | Materials per type | PASS | 1/A500: A# 20 ga @ 16", C# 18 ga @ 16", D 6" 20 ga @ 16", E 18 ga @ 16". All use 5/8" Type X each side to 6" above the ceiling and WR board at wet locations. Type number 3 = 3-5/8". Excel matches. 2/A500 bottom track is 20 ga min. 3/A500 brace 362S137-33 @ 48" is doubled for walls to 15'-0" (E3 at 12.4 ft is doubled; E3-12 / -13 at 9.5 ft are single); spot check BRACE-E3-01 = 3 x 2 x 5.54 = 33.2 LF (OK). 4/A500 uses a long-leg slotted runner plus a 3-5/8" 20 ga C channel. 2/A600 head: track header R.O. + 1'-4" (3'-0" door + 2" HM frame = 3'-4" R.O.). 3/A600: double studs at jambs, included in the stud counts. | img_bc/bc_04_types_A500.png, img_bc/bc_04b_A600.png |
| 5 | Scope sweep | PASS with differences | Blocking A104 (1-4), A402 note 4 / 5/A402, A504, P501 (water heater) is carried. The C-1 ceiling (60.49 SF WR) is carried. The soffit is existing (A200 'EXIST 11'-9"'). No access panels are drawn (E701 forbids them in drywall ceilings). Corner bead 111.75 LF and WR board are carried. Missed or weak items: control joints on runs over 30 ft (D3), and the A501 ESR 1289 grid note (D4). | img_bc/bc_05_scope_A501.png, img_bc/bc_05b_controljoint_A100.png |
| 6 | Arithmetic | PASS | Board: A3-02 28.833 x 12.417 x 2 = 716.04 (OK). D-01 7.667 x 9.5 + 7.667 x 8.5 = 138.01 (OK). E3-09 7.0 x 12.417 x 2 = 173.84 (OK). Studs: A3-02 23 x 17.13 = 393.99 (OK). E3-01 8 x 12.417 = 99.34 (OK). Partition board total 4,707.74 = Type X 4,358.06 + wall WR 349.67 (OK). Bottom track 192.84 = sum of the 3-5/8" lengths (OK). Subtotal ranges C6:C8, C11, C14, C17:C26 are correct. | img_bc/bc_06_arith_A100.png |
| 7 | Format | PASS | 6 sheets: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist. Rows run A3, C3, D, E3 with a SUBTOTAL row per type and a grand total. English only. No dollar amounts: the only '$' marks are absolute cell references. | - |
| 8 | Bluebeam markups | PASS | 19 PolyLine markups on page label A100, one per wall or sub-wall. Each has /Subj = type, /Measure (1/4 in = 1 ft), /Depth = stud height, and a Contents line (LF, H, SF, detail, id). There is also DEMO on D100, the C-1 polygon on A200 and a legend page. Re-measured from the vertices: TO-A3-02 28.833 (28.83), TO-C3-01 35.542 (35.54), TO-E3-09 7.000 (7.00); all 19 match the Excel. | img_bc/bc_08_markups_A100.png |

## Differences

| # | Item | Take-off | Back-check | Delta | N/SHEET | Image | Recommendation |
|---|---|---|---|---|---|---|---|
| D1 | Board at openings | Wall board = L x H x faces, measured through doors 4C / 5C / 6C and the 4'-0" x 8'-0" cased opening. Material Summary note says '- openings' but nothing is deducted. | Openings: 3 doors x 3.33 x 7.17 x 2 faces = 143 SF, plus cased opening 4 x 8 x 2 = 64 SF | -207 SF (-4.4 % of 4,707.74) | 2/A400, A600, A100 | img_bc/bc_06b_openings_A100.png | Deduct the openings, or keep the gross figure as a deliberate allowance and correct the note. |
| D2 | Bottom track at openings | 192.84 LF, continuous through the doors and the cased opening | 3 x 3.33 + 4.0 = 14.0 LF of opening, which needs no bottom track | -14.0 LF (-7.3 %) | A100, 2/A600 | img_bc/bc_06b_openings_A100.png | Deduct 14 LF from bottom track 3-5/8". |
| D3 | Control joints | 0. Checklist ALC-18: 'none printed (longest run 44.83 LF)' | A3-03 is 44.83 LF and C3-01 is 35.54 LF, both over the 30 ft max of ASTM C840 / GA-216 | About +50 LF of control joint (1 per run per face x 12.42 ft) | A100, 1/A500 | img_bc/bc_05b_controljoint_A100.png | Add it as an RFI or allowance line. A3-03's back face depends on RFI-02. |
| D4 | Restroom C-1 ceiling system | Furring / carrying channel system (ASTM C754) loaded. The ESR 1289 grid is only alternative A of RFI-06. | A501 prints 'G.C. SHALL INSTALL SUSPENDED BOARD CEILINGS IN COMPLIANCE WITH ICC ESR 1289' (drywall grid, 2/A501) | System swap, same 60.49 SF of board | 2/A501 | img_bc/bc_05_scope_A501.png | Load the printed grid system (drawings outrank code) and keep the channel system as the alternative. |
| D5 | E3-11a/b brace length | Braces at deck 16'-4" (5.54 ft each, 6 members) | E3-11 is on the C3 / deck-break line, where C3-01 is carried at 17'-1 9/16" (RFI-01) | +6 x 1.13 = +6.8 LF of 362S137-33 if made consistent | A100, 3/A500 | img_bc/bc_09_e311_brace.png | Use the same deck assumption as RFI-01 (minor). |
| D6 | Untagged niche sides | E3-06 / E3-08 carried as E3 with no stated reason | The niche sides (1.08 LF each) have no tag of their own | 0 LF | A100 | img_bc/bc_01_tag_sweep_A100.png | Add a line: 'untagged niche returns, carried as the adjoining E3'. |
| D7 | Markup height text | 'H 17'-1.5"' | Printed '17'-1 9/16"' | Text rounding only (Depth 17.13 is correct) | A100 | img_bc/bc_08_markups_A100.png | Cosmetic. |

Within tolerance (no change needed): the restroom ceiling area is 60.49 SF in the take-off against about 59.4 SF in the back-check (7'-8" x 7.75 ft), which is 1.8 %.

## Addendum - disposition of the differences (take-off session, rev1 FINAL)

| # | Disposition |
|---|---|
| D1 | No change by standing rule: gypsum board is never deducted at openings (estimator precedent, B&N rev13; the Material Summary note text is the tool's generic note). |
| D2 | No change by standing rule: bottom track is carried without door deduction (skill criterion); the delta (-10.0 LF at the doors, -4.0 LF at the cased opening) is written in the canon notice. |
| D3 | APPLIED: control joints CJ-A3-03 and CJ-C3-01 (one full-height joint per face, ASTM C840 30'-0" max.) in the control joint row. |
| D4 | Kept as RFI-06: the A501 general note has no bubble on the restroom ceiling (R70.1: a typical detail does not change the field system without its callout); option A = 2/A501 grid with its delta. |
| D5 | APPLIED: E3-11a / E3-11b braces to the 17'-1 9/16" deck of the C3 line. |
| D6 | APPLIED: E3-06 / E3-08 carry 'untagged_join' (niche returns of the adjoining tagged E3 line). |
| D7 | Cosmetic (markup text rounding of 17'-1 9/16"); /Depth 17.13 is the value used. |

## Addendum rev2 (5-nov, back-check of the rows that changed vs rev1; every other Material Summary row is identical to rev1, compared by program)

| # | Item | Result | Independent recomputation |
|---|---|---|---|
| R2-1 | Restroom C-1 ceiling system | PASS | 2/A501 INSTALLATION OF SUSPENDED CEILING USING GRID SUSPENSION SYSTEM (5/8" GYP. BD., ICC ESR 1289) is the only gypsum ceiling detail printed; C-1 restroom is the only gypsum ceiling (A200 legend). Option A loaded (RFI-06 closed). |
| R2-2 | Main tee | PASS | room 7'-8" x 7'-9" (A402 [CONFIRMED]); mains @ 4'-0" (2/A501 hangers max. 4'-0" o.c.) across the 7.667 ft side: ROUNDUP(7.667/4)+1 = 3 runs x 7.75 ft = 23.25 LF = Excel 23.25 |
| R2-3 | Cross tee | PASS | @ 16" o.c. (USG standard, not printed, noted): ROUNDUP(7.75/1.333)+1 = 7 x 7.667 = 53.67 LF = Excel 53.67 |
| R2-4 | 2" x 2" angle molding | PASS | 2/A501 '2" X 2" SHEET METAL ANGLE' = room perimeter 31.75 LF (A100 vector polygon with the vanity notch) = Excel 31.75 |
| R2-5 | Hanger wire | PASS | 3 mains x 3 hangers (7.75/4 -> 3) = 9 pcs x drop 8.333 ft (16'-4" A100 PLY DECK - 8'-0" A200) = 75.0 LF = Excel 75 / 9 pcs (unchanged) |
| R2-6 | Removed rows | PASS | furring channel 54.25 LF, carrying channel 23.0 LF, ceiling perimeter track 31.75 LF are no longer carried (the grid replaces them); board 60.49 SF unchanged |

Result rev2: 6/6 PASS on the changed rows; rev1 8/8 PASS stands for the unchanged rows.
