# INFORME_AUDITORIA U-181 — 2026-11-13 21:46 PST (California)

Independent auditor (did NOT do the take-off). Sources used: bid set only (`CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf`, SHEET_MAP) and the deliverables. The canon, the readers' fragments and the resolution files were not opened. Nothing was corrected.

Audited files:
- Excel `Take-off/CR_City_Hotel_Takeoff_rev1.xlsx`: sha256 `9b99ae22ed5cc331005c677536e6cee908a03066e61ce2f07322deb86022c447`
- Markups `Planos marcados/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf`: sha256 `b95819b89e2c21b4e419874f06bf134d22681bb3f01e8818ed627c199ecac7ff`
- Also read: `Proposal/CR_Proposal_rev1.xlsx`, `README_REVIEW.md`.

## Block results

| Block | Result | Basis |
|---|---|---|
| A1 walls | **FAIL** | Wall vs markup sweep (tag positions from the vectors vs the 1,155 polylines): no tagged gypsum wall without a markup was confirmed (the outliers are leader tags or walls loaded on the enlarged sheets A7.30/A7.45/A7.50). Lengths re-measured blind from the vectors (15 walls, see F16): 10 within 2 %, and 5 differ only by the end convention or a window. FAIL comes from board type and openings: F05, F06 and F07. |
| A2 heights | PASS with observation | Every height group in the Partition Takeoff (1,119 rows) was checked against the printed dims: 9'-2" + 1'-10" assembly = 11'-0" (1/A5.06, 1/A5.03); 8'-11 1/4" at L4 (1/A5.06, 1/A5.03); 12'-1 3/8" and 11'-2 5/8" at L1 (1/A5.03, A5.04); 11'-0" and 14'-0" floor to floor (A4.03-A4.05); 8'-6" bath GYP-1 (A7.00-A7.16); 8'-11" corridor GYP-1 (A7.23). One inconsistency in criteria: F13. |
| A3 RCP | **FAIL** | A3.01-A3.04 were reviewed completely, room by room. Stacked ceilings (FS-1 + GYP-1 in corridors, L1 toilets and unit baths) are both loaded (PASS). Failures: F01, F10, F11 and F12. A fully independent re-measure of 10 areas from the drawing vectors was **not** completed. The polygon areas were recomputed from the vertices and checked against the Excel instead (F03). |
| A4 materials / scope | **FAIL** | F04, F07, F08 and F09. The spec sections 09 21 16.23, 09 22 16, 09 29 00 and 09 30 00 were **not** opened in this audit (pending). |
| A5 PDF / Bluebeam | **FAIL** (ceilings) / PASS (walls) | All 1,119 wall rows match their markup (Length and Depth equal, 0 mismatches; 6 walls are drawn as multi-segment and sum exactly). Subject, Label, Length and Depth are present. Wall Area is shown in the Contents text, which Bluebeam computes as Length × Depth. Scales are 1/8" on A2/A3 and 1/4" on A6/A7, consistent with the printed scales. Ceiling polygons do not reconcile with the Excel: F02 and F03. Labels: F15. |

## Findings

| id | block | finding | N/SHEET | crop | severity | quantity delta |
|---|---|---|---|---|---|---|
| F08 | A4 | The Proposal carries loaded rows at $0 ("PRICE / RATE TO CONFIRM"). These are: 5/8" regular board 8,263.9 SF (material), angle molding DGWM24 4,409.8 LF, hanger wire 1,253 LF, Level 5 13,123 SF (material and labor), and resilient channel install labor 22,410.5 LF. Fields marked [TO BE COMPLETED] are still in the header. The base bid of $497,600 / $541,439 is understated. | Proposal PRICING sheet; A0.08 FS-1; 7/A7.23 | n/a (Excel) | HIGH | qty OK; price $0 on 5 loaded items |
| F02 | A5 | L1 Lobby GYP-1 dropped soffit grid: the markup polygon measures 1,484.6 SF (the same polygon as the FS-1 membrane), but the Excel loads 742.9 SF ("net of coffers"). The markup does not show what was loaded. | 1/A3.01, 1/A7.31 | img_auditoria/F02_A3.01_lobby_GYP1_vs_membrane.png | HIGH | markup − Excel = +741.7 SF |
| F03 | A5 | Corridor GYP-1 polygons do not match the Excel. L3 N-S leg: markup 330.7 vs Excel 443.8. L4 N-S: 339.7 vs 452.3. E-W legs at L2, L3 and L4: markup is 39.9 SF above the Excel on each (the WS-1 deduction is not drawn). L3 309 membrane: markup 94.7 vs Excel 111.7. Review Items 87/91 state "loaded the RCP polygon (what Bluebeam measures)", which is false for L3 and L4. | 1/A3.03, 1/A3.04, 1/A3.02, 1-3/A7.23 | img_auditoria/F03_A3.03_corridor_GYP1_polygons.png | HIGH | N-S −225.7 SF, E-W +119.7 SF, 309 −17.0 SF (net on ceilings incl. F02 = +618.7 SF markup over Excel) |
| F04 | A4 | Joint compound, tape and Level 4 finishing labor are applied to 125,159 SF. That total includes about 24,852 SF of concealed base layers (half of every 2-layer face) and about 9,600 SF of membranes concealed above dropped or ACT ceilings: FS-1 over L2/L3 corridors, L1 west wing, Corridor 101, Kitchen 100, staff core, toilets zone and lobby, plus the membranes above unit bath dropped ceilings. These need fire-taping at most, not Level 4. | A0.06 types (2 layers), A0.08 FS-1 "dropped ceiling is not a component" | n/a (Excel) | MEDIUM | finishing −24,852 to −34,500 SF; JC −1,789 to −2,484 lb; tape −9,195 to −12,765 LF |
| F05 | A1 | Exterior walls run gross through the window openings. On L2 both the interior Type X faces and the exterior gyp sheathing continue across the window (e.g. XW.6.3-L2-05 B/F at room 206). On L3 the interior face stops at the jamb (XW.6.3-L3-16 A) but the exterior band (XW.6.3-L3-05 A 77.84 LF) is continuous. The criterion is inconsistent, and the README claims "- openings". | 1/A2.02, 1/A2.03, A8.01 window types 1/3 (about 6'x6') | img_auditoria/F05_A2.02_206_window_gross.png, F05b_A2.03_L3_window_net.png | MEDIUM | est. −3,200 SF (about −2,200 SF exterior sheathing and −1,000 SF Type X; verify window count) |
| F06 | A1 | The XW.6.6 0 tags (no row on A0.07) are loaded as XW.6.6 1, including 5/8" exterior gyp sheathing. The 0-rated XW rows that are printed (XW.6.3 0 / XW.6.4 0) carry FRT plywood with no exterior gypsum. Affected rows: XW.6.6-L4-06 B 1,005.2 SF and XW.6.6-L3-01 B 59.5 SF. | 1/A2.04, 1/A2.03, A0.07 | img_auditoria/F06_A2.04_XW66_0_tag.png, F06b_A0.07_XW63_0_no_ext_gyp.png | MEDIUM | −1,064.7 SF exterior sheathing |
| F01 | A3 | Mech & Water Heater Mezzanine 219 is excluded with "RFI-05 (no ceiling loaded)", but README and Proposal state "Open RFIs (0)". The exclusion cites an RFI that does not exist, and the ceiling is neither loaded nor carried as an RFI or clarification. | 1/A3.02 | img_auditoria/F01_A3.02_mezz219_RFI05.png | MEDIUM | +450.5 SF (board + RC) or open RFI |
| F09 | A4 | Scope is treated inconsistently on tenant spaces. The tenant faces of rated perimeter walls are loaded in Retail 124 (XW.6.4-L1-02 B, -03 B and XW.6.3-L1-02 B: 1,095.7 SF) and in F&B 410/411/419 (4,167.6 SF). This goes against the printed notes "GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT" (A2.01) and "INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE" (A7.55, 3/A7.50), while the ceilings of the same spaces are excluded under those same notes. The proposal does not clarify this. | 1/A2.01, A7.55, 3/A7.50 | img_auditoria/F09_A2.01_retail_tenant_note.png | MEDIUM | −5,263.3 SF if the notes govern (or a clarification is needed) |
| F10 | A3 | Bar 107 has no ceiling tag on A3.01 or A7.31, yet 2,205 SF of 5/8" regular board on drywall grid is loaded (171 hangers, 201 LF wire). Section 3/A7.31 (BAR CEILING EAST WEST) prints "1'-11 1/4" RATED ASSEMBLY" over part of the bar, so the board type and the membrane are unresolved. No RFI is listed. | 1/A3.01, 1/A7.31, 3/A7.31 | img_auditoria/F10_A7.31_sec3_bar_ceiling.png | MEDIUM | 2,205 SF regular unresolved (type C/X?) |
| F07 | A1/A4 | Faces of non-rated W.4 0 / W.6 0 walls are loaded as 5/8" Type X / Type X W.R. A0.06 general note 10 reads "USE 5/8" GYPSUM BOARD AT ALL OTHER LOCATIONS UNLESS NOTED OTHERWISE" (regular / MR). The deliverable's own Review Items 39/49/73 quantify 3,900-4,885 SF. | A0.06 GN 10, GN 11 | img_auditoria/F07_A0.06_GN10_regular_board.png | MEDIUM | about 3,900-4,885 SF Type X → regular/MR (product, same SF) |
| F12 | A3 | Resilient channel is loaded under the L4 roof ceilings (401-405, 406, 417, 418, 421) at 0.75 LF/SF. The roof assemblies RS-1/RS-2 on A0.08 print "CEILING RE: RCP" with no RC; RC is printed only in FS-1 (L546). | A0.08, 1/A3.04 | n/a | LOW | −2,007.5 LF RC (or RFI) |
| F11 | A3 | Some RCP rooms have neither a ceiling markup nor an EXCLUDED markup with a printed reason: Retail 124 (its 275 SF GYP-1 band and FS-1/beam wraps are excluded only in the Excel), Stair 2 126 / FACP 125 and Water Entry 128 on A3.01, Lobby 317 WS-1 on A3.03, and the L4 Corridor 412 elevator lobby (WS-1 8'-0 1/2", A7.23) on A3.04. A3.02 has the equivalent EXCLUDED markup at Lobby 217. | 1/A3.01, 1/A3.03, 1/A3.04, A7.23 | img_auditoria/F11_A3.04_412_elev_lobby_unmarked.png, F11b_A3.01_WaterEntry128_unmarked.png, F11c_A3.01_Retail124_Stair126_no_EXCLUDED.png | LOW | ~0 SF (process; Water Entry 128 182 SF unresolved) |
| F13 | A2 | Height criteria differ between levels. L2/L3 faces go to 9'-3 1/2" (the printed 9'-2" ceiling + RC + board, i.e. line of structure). L4 faces stop at the printed 8'-11 1/4" ceiling line, with no RC/board allowance, although the same RC is loaded on L4 (F12). | 1/A5.06, 1/A5.03 | img_auditoria/F13_A5.06_heights_9-2_and_8-11.25.png | LOW | about +277 SF on L4 if the L2/L3 criterion applies (or −1,150 SF on L2/L3 if the L4 criterion applies) |
| F16 | A1 | Blind re-measure from the vectors, face to face of the abutting walls, on 15 walls of 13 types and levels. Within ±2 %: W.4-L2-42 D, W.62-L3-02 A, W.62-L2-08.2 A, FW.6-L4-03, DW.4-L3-06 A, FW.2-L3-C23, XW.6.3-L2-03 A, FW.6-L3-06 B, W.4-L4-19, W.4-L3-08 A. Outside: CH.6-L1-01 A +4.6 %, W.6-L1-15 B +2.8 %, W.6-L1-09 B +5.1 %, DW.4-L2-04 B +3.0 % (markup 0.19-0.52 ft shorter than face to face; end convention), and XW.6.3-L3-16 A +13.8 % (verified visually: the markup is net of a window, so correct). | A2.02, A2.03, A2.04, A6.02, A7.50 | img_auditoria/F05b_A2.03_L3_window_net.png | LOW | about +10 SF on the 4 walls |
| F14 | A4 | C-H stud spacing is contradictory in the Review Items: #43 says "24" o.c. loaded" while #54 and #68 say "16" o.c. loaded". The Material Summary is computed at 16" (e.g. CH.2-L2-01: 55 LF = 5 studs × 11 ft). | A0.06 GN 6, 7/A9.03 | n/a | LOW | 0 (text only) |
| F15 | A5 | Wrong page labels in the markups PDF: pages 45, 48 = "WD-1"; 46, 47, 50, 51, 54-56, 58, 59, 61-63 = numeric; page 73 = "A7.39" (A7.35 per the SHEET_MAP). None of these pages carry markups. | markups PDF | n/a | LOW | 0 |

## COBERTURA

Detail N/SHEET that governs quantity, opened in this audit:
- A0.06 (interior types W, DW, FW, FI, C-H; general notes 4, 6, 7, 10-13, 21; stud schedule)
- A0.07 (XW.6.2 2, XW.6.3 0/2, XW.6.4 0/2, XW.6.6 1/2)
- A0.08 (FS-1 L546 levels 2/3/4 throughout; FS-1 above parking; MB-1/GYP-2; RS-1 to RS-7)
- 1/A5.06 and 1/A5.03 (9'-2", 1'-10", 8'-11 1/4", 12'-1 3/8", 11'-0")
- A4.03-A4.05 (level datums, text)
- 1/A7.00, 2/A7.00, 5/A7.00, 6/A7.00, 9/A7.00, 10/A7.00 (unit plan and RCP, unit general note 1)
- A7.05, A7.09, A7.13 and A7.16 (text only: 8'-6" GYP-1)
- 1-3/A7.23 (text: GYP-1 8'-11", WS-1 8'-0 1/2")
- 1/A7.31, 2/A7.31, 3/A7.31 and 7/A7.31 (lobby and bar)
- 1/A7.45, 2/A7.45, 3/A7.45 and 4/A7.45
- 1/A2.01, 1/A2.02, 1/A2.03 and 1/A2.04 (tag sweep plus crops)
- 1-12/A6.00, 1-11/A6.01 and 1-5/A6.02 (tag sweep plus page view of A6.01)
- 1/A7.30 and 1-3/A7.50 (tag sweep)
- A8.01 (window types, text)

RCP sheets reviewed completely (room by room against the markups): A3.01, A3.02, A3.03, A3.04.

RCP sheets reviewed partially:
- A7.00 (whole page viewed)
- A7.31 (whole page viewed)
- A7.45 (whole page viewed)
- A7.23 (text only)

RCP sheets NOT reviewed in this audit (pending): A7.24, A7.50 RCP views, unit RCPs A7.01-A7.04, A7.05-A7.19 (graphic) and raster sheets 45-63. Spec sections 09 21 16.23, 09 22 16, 09 29 00 and 09 30 00 were not opened.

abiertos: 16
