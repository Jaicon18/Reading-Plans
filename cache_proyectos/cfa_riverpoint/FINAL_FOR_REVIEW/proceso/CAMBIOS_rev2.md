# CAMBIOS rev2 - CFA #2284 River Point (audit step 11 + coverage step 12 corrections)

Excel produced by plantilla_excel.py armar (skill v81cf4) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon. rev1 files untouched.

| # | Item | rev1 | rev2 | Delta | N/SHEET | Rule / decision |
|---|---|---|---|---|---|---|
| 1 | C.R. channel 'bracing' on M2.1-01 / M3.5-01 / M3.5-02 / MB-01 | 56.79 LF (28.33 + 14.29 + 7.5 + 6.67) | 0 LF | -56.79 LF C.R. channel | A1/A-605, A2/A-605, C2/S-801; C09111 3.2.C / A-909 | decision 1 (bracing only where printed) |
| 2 | Wall braces 362S162-33 @ 48" (D1/S-801 schedule) at M3.5-01 / M3.5-02 / MB-01 | 0 | 16.96 LF 3-5/8" (7 pcs) | +16.96 LF | D1/S-801, C2/S-801, A-202 note C.4 | decision 1 (printed schedule) |
| 3 | 54 mil bent plates at braces | 0 | 7 pcs | +7 pcs | D1/S-801 | decision 1 |
| 4 | L1-1/2x1-1/2x33 mil continuous angle at MB-01 | 0 | 3.333 LF | +3.333 LF | C2/S-801 | decision 1 |
| 5 | Menu board 33 mil blocking T&B (C2/S-801) | 3.333 LF (one row) | 6.666 LF (2 rows) | +3.333 LF | C2/S-801 | decision 1 |
| 6 | Soffit cross brace 362S162-33 @ 32" (serving L + gathering) | 0 | 67.56 LF (16 pcs) | +67.56 LF 3-5/8" | C4/A-624, C3/S-801 | decision 2 |
| 7 | Play-bay gyp ceiling 6" rim track | 0 | 29.77 LF | +29.77 LF 6" track | A3/S-241, A-221 | decision 3 |
| 8 | MB-01 stud size (menu board infill) | 3-5/8" (C2/S-801) | 6" @ 16" (D3/A-624) | studs + tracks of MB-01 move from 3-5/8" to 6" | D3/A-624 | decision 4 (metal-or-wood = metal) |
| 9 | Roof hatch shaft top runner | 24 LF standard track (top + bottom) | 12 LF standard (bottom) + 12 LF 3" long-leg slotted (top, C1/S-801) | -12 LF standard track, +12 LF slotted track | C1/S-801, A1/A-604 | decision 5 (two track kinds in separate rows) |
| 10 | Gauge plans 33 mil vs S-902 C05000-C 2.5.A.1 0.0538 in | no note | RFI-18 closed (option A = plans 33 mil) | 0 LF (gauge alternative = same LF at 54 mil) | S-902, S-801, S-241 | decision 6 (plan-vs-spec conflict) |
| 11 | Ceiling board product (332.06 SF) | 5/8" gypsum board, regular | 5/8" sag-resistant gypsum ceiling board (C09250 2.1.E) | 0 SF (product) | C09250 2.1.E / A-909 | decision 7 |
| 12 | Restroom gyp faces above tile (EX-RRM-01-GB, EX-RRW-01-GB) | 1/2" regular 148.02 SF | 1/2" moisture resistant 148.02 SF (plan thickness, spec product) + RFI-21 closed | -148.02 SF 1/2" regular, +148.02 SF 1/2" MR; spec alternative same 148.02 SF as 5/8" Type X W.R. | A-202 notes G.1 / H.3, C09250 2.2.A.2 / A-909, A-611 | decision 8 rev (plan-vs-spec conflict: plan thickness, spec product, RFI-21 closed) |
| 13 | J-bead at menu board exposed gyp edge | 0 | 13.683 LF | +13.683 LF | D3/A-624 | decision 10 |
| 14 | J trim at play area wall base | 0 | 59.69 LF | +59.69 LF | A2/A-624 | decision 10 |
| 15 | Patch of existing draftstop wall at new beverage chases | not addressed | 16 SF 1/2" gyp (allowance) + RFI-20 | +16 SF | A-052 note 9, P-211 | decision 12 |
| 16 | Demolition of existing board under new restroom cement board (DEMO-14) | 0 SF | 617.08 SF + RFI-19 | +617.08 SF demolition | A-050 KN10, A-611 | decision 13 |
| 17 | W6-04-KIT length | 2.317 LF | 2.229 LF (printed 2'-2 3/4") | -0.088 LF x 1.5 ft x 2 faces = -0.26 SF cement board | A-202 | decision 15 |
| 18 | Strongback 362T125-54 (26.51 LF) | inside the ceiling / soffit track row | own row (product split) | 0 LF | C3/S-801 | decision 17 |
| 19 | RFI-17 (MB-01 type) | open - 'printed nowhere' | closed - D3/A-624 prints 2x6 wood or 6" metal -> 6" metal | see MB-01 | D3/A-624 | decision 4 / 17 |
| 20 | Kitchen base rows RFI reference | -> RFI-02 | -> RFI-03 (closed) | text | A-050 KN16 | decision 17 |
| 21 | Roof hatch 3x3x1/4 clip angles | not addressed | EXCLUDED note (misc steel) | 0 | A1/A-604 | decision 11 |
| 22 | K-001 note 6 Unistrut | not addressed | EXCLUDED note | 0 | K-001 | decision 14 |
| 23 | Spec section on every framing / board row; notes on Z channel, ceiling board, compound / tape driver | missing | constants.ms_notes | text | C09111 / C09250 / A-909, S-902 | decisions 7, 9, 17, 18 |
| 24 | Citations / internal codes in client text | G.2/A-202 style, WD-3/CT-73B, R-ALC-xx, resolver, PT00xx | A-202 note G.2, sheet + note, no internal codes | 305 text fields | all | decision 18 |
| 25 | Bluebeam PDF | Page Labels 6 / 7 on demo pages; DEMO contents in Spanish; MB-01 Subject M3.5; markup SF = L x H; no area markups | Page Label = A-050 / A-052 / A-202 / A-221; English states; MB-01 Subject INFILL; Excel board SF of every metal wall / soffit side listed on the legend page (verificar keeps the tool's LF x H Contents); polygons for 5 gyp ceilings, 2 soffit bottoms, Level 5, hatch shaft, 2 pin & sleeve recesses | format | A-050, A-052, A-202, A-221 | decision 19 |
| 26 | Cement board joints (1,800.27 SF) | no joint treatment | alkali-resistant mesh tape 666.1 LF (own row) + setting-type compound 129.62 lb (note on that row: no LB row in the template) | +666.1 LF mesh tape, +129.62 lb setting compound | C09250 2.4.B.2 / 2.4.D.2 / 3.5.E (A-909) | decision 9 |
| 27 | Joint compound / tape driver | gyp board only, unexplained | note: driver = gypsum board SF only; cement board joints in the mesh tape row | text | C09250 2.4 / A-909 | decision 9 |
| 28 | 1/2" gyp row breakdown | cut off after 3 sources | full breakdown in proceso/BREAKDOWN_half_inch_gyp_rev2.md (tool cuts the Excel cell at 500 characters) | - | - | decision 17 (tool limit) |
| 29 | Joint compound / tape driver after the MR board change | driver without the 148.02 SF of 1/2" MR board (tool driver list) | tool fix BE-CF14 (v81cf4 accesorios.BOARD_DRIVER includes 1/2" MR and 5/8" foil-backed): driver = 1/2" regular + 5/8" ceiling + 1/2" MR | compound 128.43 -> 139.08 lb, tape 659.97 -> 714.74 LF | C09250 2.4 / A-909 | BE-CF14 |
| 30 | Partition Takeoff MB-01 | merged in row M3.5-01+MB-01 (type M3.5) | own type INFILL (6" metal, D3/A-624) | row split | D3/A-624 | decision 4 / 17 |
| 31 | OTHER FRAMING block subtotal | no subtotal | unchanged: the fixed template prints no subtotal for OTHER FRAMING (tool limit, see TOOL_LIMITS) | - | - | decision 17 (tool limit) |
| 32 | Hidden sheet _reglas | present | kept: it is the plantilla_excel.py seal of the reglas.py gate (same fixed format in every project; bitacora.py rejects a workbook without it); the 6 visible sheets are unchanged | - | - | decision 20 |
| 33 | Inputs C26 lumber stock note | precedent of another project (estimator decision 2026-10-27) | estimator standing input | text | - | decision 18 |
| 34 | Demolition vs new plan cross table | missing | proceso/DEMO_CRUCE.md | - | A-050, A-052, A-202 | decision 16 |
| 35 | Review items 1 / 7 wording | MB-01 3-5/8"; M3.5 'A 3-5/8"' | MB-01 6" (RFI-17 closed); M3.5 'A 8" (as loaded)' | text | D3/A-624, A2/A-605 | decision 17 |

## Material Summary NET rev1 -> rev2

| Row | Unit | rev1 | rev2 | Delta |
|---|---|---|---|---|
| Bottom track 3-5/8" | LF | 3.33 | - | -3.33 |
| Top track 3-5/8" - standard (walls not reaching structure) | LF | 3.33 | - | -3.33 |
| 6" metal stud (LF of material) | LF | 304.5 | - | -304.5 |
| 3-5/8" metal stud (LF of material) | LF | 165.84 | - | -165.84 |
| Ceiling / soffit track (size per source, see Where it comes from) | LF | 197.39 | - | -197.39 |
| Bracing 1-1/2" C.R. channel | LF | 107.66 | 50.87 | -56.79 |
| 1/2" gypsum board regular | SF | 1583.66 | 1451.64 | -132.02 |
| Demolition - gypsum board and metal stud framing (SF = length x height x layers) | SF | 2646.57 | 3263.65 | +617.08 |
| Metal stud blocking at wall-mounted items (notes) | LF | 10.6 | 13.94 | +3.34 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim | LF | 73.44 | - | -73.44 |
| 1/2" cement board / cementitious backer | SF | 1800.53 | 1800.27 | -0.26 |
| Track 6" (gauge per source) at soffits, fire stop at ceiling line and nested beam | LF | 143.19 | 172.97 | +29.78 |
| Joint compound, all purpose | LB | 137.93 | 139.08 | +1.15 |
| Joint tape, paper | LF | 708.82 | 714.74 | +5.92 |
| Bottom track 6" | LF | - | 3.33 | +3.33 |
| Top track 6" - standard (walls not reaching structure) | LF | - | 3.33 | +3.33 |
| 6" metal stud (LF of material) - per source | LF | - | 42 | +42.0 |
| 6" metal stud (LF of material) - 600S162-33 | LF | - | 304.5 | +304.5 |
| 3-5/8" metal stud (LF of material) - per source | LF | - | 123.84 | +123.84 |
| 3-5/8" metal stud (LF of material) - 362S162-33 | LF | - | 84.52 | +84.52 |
| Ceiling / soffit track (size per source, see Where it comes from) - per source | LF | - | 158.87 | +158.87 |
| Ceiling / soffit track (size per source, see Where it comes from) - 362T125-54 strongback to each truss @ 48" (C3/S-801) | LF | - | 26.51 | +26.51 |
| Ceiling / soffit track (size per source, see Where it comes from) - L1-1/2" x 1-1/2" x 33 mil continuous angle (C2/S-801) | LF | - | 3.33 | +3.33 |
| 1/2" gypsum board, MOISTURE RESISTANT | SF | - | 148.02 | +148.02 |
| Clip angles and framing clips (see Where it comes from) | PCS | - | 7 | +7.0 |
| Deep-leg slotted deflection track - printed product (see Where it comes from) | LF | - | 12 | +12.0 |
| Alkali-resistant glass-fiber mesh tape at cement backer board joints - printed product (see Where it comes from) | LF | - | 666.1 | +666.1 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead | LF | - | 73.44 | +73.44 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - LC-bead (J) at exposed gypsum edge (D3/A-624) | LF | - | 13.68 | +13.68 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - J trim at top of cement board base (A2/A-624) | LF | - | 59.69 | +59.69 |
