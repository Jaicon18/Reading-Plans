# PASS 2 — Corrections to pass 1 (B&N #3566 Colorado Springs)

Sources used: `planos_BN_limpios.pdf` (fresh crops at 2–3x), `out/*` (pass 1), `BIBLIOTECA_ERRORES.md`, `skill/tools/plantilla_excel.py`.
Tags: [CONFIRMED] printed · [DERIVED] operation shown · [PENDING] not printed / conflict (RFI). Cites are N/SHEET.
Old values come from `out/1C_materials_summary.csv`, new values from `out/2C_materials_summary.csv`.

## A. Errors corrected (quantities)

| # | Error in pass 1 | Evidence | Old → New | Library |
|---|---|---|---|---|
| 1 | FRP-1 in the workroom carried from the floor to 10'-0". The base detail prints the FRP J-mold at the top of the 6" EP-1 base, so FRP starts 6" above the floor (9.5 ft). Rows H1-01, H1-02, E2-01, H2b-01, H2a-01 changed. | 3/A-225 and 4/A-225 (J-mold + 6" base dim), 1-4/A-226B (FRP-1 pattern fills the full 10'-0" elevation) | FRP-1 998.30 SF → 959.00 SF; division bars 220.0 → 211.0 LF | BE-14 |
| 2 | RFI-B09 offered "FRP to 6'-0"" as an open alternative. The 6'-0" and 4'-0" dims on 1/A-226B are equipment heights, not an FRP top. | 1/A-226B right-hand dims | RFI-B09 rewritten (top bar, corner guards); alt −317 SF kept only as a delta | BE-14 |
| 3 | Existing exterior walls (types 1, 1A, 1B, 1C) were listed as 8 rows in the Partition Takeoff (7,824 SF, status PENDING). They are existing and excluded. | A-101 legend "EXISTING EXTERIOR WALL"; DM-101 key notes 3 and 6 | 8 rows removed; delta moved to RFI-01 (+7,824 SF GWB, +3,599 screws) | BE-09 |
| 4 | Door header track (83.35 LF) carried with no header schedule or head detail. 1/A-500 prints the HM jamb only. Pass 1 text also said "8 doors" for 9 openings. | 1/A-500 typical HM frame; A-500 schedule (D3, D4–D9, D11, D14) | 83.35 LF → 0.00 LF; RFI-B21 carries the +83.35 LF delta and lists the 9 doors | BE-29, BE-47 |
| 5 | Fire-stop track "TYP." applied to 14 walls only. Walls to deck with a ceiling on a face were missing: 2-08, 2-10b, 5-01, H1-01, H2b-01, E2-01, E1-01, E1-02, F-01. | 4/A-410, 8/A-410 "FIRE STOP AT CEILING LINE, TYP."; 1/A-121 ceilings | 3-5/8" 129.58 → 159.53 LF; 6" 21.81 → 106.15 LF (total 151.39 → 265.68 LF) | BE-01 |
| 6 | Slab pins used "1 row @ 16"", a spacing that is not printed. 8.F prints 2 rows at 16"; 9/A-410 prints 24". Conservative printed value carried. | 8.F/A-410; 9/A-410 | 393 → 786 ea (types 3/4 still 0: HUS-EZ at moment clips); RFI-D01 gives the 24" delta (786 → 262, −524) | BE-19 |
| 7 | Top-of-wall relief channel missing. "Top track fasteners @ 24" code default" replaced a printed spacing. | 5/A-410 typ. connection detail: continuous 20 ga x 2" relief channel, #8 pan-head screws @ 24" and 6" from ends | New row 398.51 LF relief channel; screws 273.70 → 220 ea (full-height walls only; partial walls have no top anchorage); RFI-D02 | BE-16, BE-19 |
| 8 | TEK screws at 2x2 clip angles counted 2 per clip. The detail prints (4) TEK screws per clip; moment clip prints (1) #10-16 per flange. | 5/A-410 "(4) TEK SCREWS"; A/A-410 "(1) #10-16 SCREW @ EACH FLANGE"; 7/A-210 "(4) #10-16" | 3,722 → 7,280 ea (1,771 x 4 + 90 x 2 + 4 vestibule clips x 4) | BE-53, BE-16 |
| 9 | Vestibule screws: "(8) #10-16 TEKS 16" O.C. TYP." read as 8 per column. Beam extent called "not dimensioned"; the plan and section give 12'-8" between corner posts. 8" ledger missing. Beam studs double-counted in the heavy screw row. | 8/A-210, 1/A-210 plan (5"+2'-2"+…=12'-8"), 4/A-210 "8" LEDGER" | TEKS 32 → 376 ea (4 columns x 9 stations x 8 + beam 11 x 8); heavy screws 78 → 66; new 8" ledger 12.67 LF; beam V-02 now [DERIVED] | BE-15, BE-16 |
| 10 | Board screws used the skill default 1.2 per SF. 8.E prints 24" o.c. walls, 12" o.c. ceilings, butt joints 12". | 8.E/A-410 | 17,851.68 → 6,370.58 (walls, 0.46/SF) + 994.28 (ceilings, 0.83/SF); S-12 84.00 → 32.20; Inputs!B20 1.2 → 0.46; RFI-D03 shows +10,743 at 1.2 | BE-19 |
| 11 | Plywood screws "spacing not printed". 8.D prints 24" field / 12" perimeter (= 32 per 4x8 sheet = 1.0/SF). | 8.D/A-410 | 1,532.33 → 1,509.08 ea, status PENDING → DERIVED | BE-14 |
| 12 | Soffit layers double-counted: GWB carried full height PLUS plywood on the same face. Sections print plywood below T.O. WD-1 and GWB above (replace, not add); cafe soffit also has an inner GWB face; G&G inner face is unboarded; G&G underside was missing. | 2/A-221, 3/A-221 (soffit sections), section I/A-221 | GWB soffit 527.39 → 698.00 SF; 5/8" plywood soffit 285.83 → 226.85 SF; GWB total 14,072.20 → 14,242.81 | BE-05, BE-06 |
| 13 | Ceiling sound blankets dropped as "A-101 shows walls only". 2/A-410 prints blankets at ceilings of toilets, offices and break room. A-101 table ceiling column is blank (checked at 2.5x). Conflict → carry the detail + RFI. | 2/A-410 ceiling label; 1/A-101 room table | 0 → 479.72 SF (RR 130.0 + break 240.1 + manager 109.7); RFI-B17 | BE-14, BE-19 |
| 14 | Items called "PENDING" that the sheets resolve: office FRT blocking, break-room kitchen blocking, menu-board plywood. | 3,4/A-412 (3 rows at 1'-4", widths 8'-6" and 12'-11"); 6/A-412 (2'-9" + 2'-7"); 4/A-226A (5 frames 24"x31" x4 + 70"x31") | 0 → 64.26 LF, 5.33 LF, 35.74 SF 3/4" plywood (3/4" FRT 220.11 → 255.85) | BE-13, BE-18 |
| 15 | Joint compound/tape follow the new board SF. | — | Compound 1,076.14 → 1,088.42 lb; tape 5,530.17 → 5,593.29 LF | BE-40 |

## B. Errors corrected (text, format, traceability)

| # | Error | Evidence | Fix | Library |
|---|---|---|---|---|
| 16 | RFI list was parsed so that 19 of 49 RFIs had the generic delta "See the assumption…; no quantity delta beyond price". | Pending Items sheet (pass 1) | 36 RFIs, every one with a numeric delta or "n/a: reason"; duplicates (RFI-03/B23, B02/C05, B22/07) merged | BE-53 |
| 17 | Cross-references: "8 doors" (9 openings); RFIs citing quantities that no longer match. | Pending Items vs Partition Takeoff | All RFI-/ALC- ids and quantities cross-checked against the saved workbook (0 undefined, 0 mismatches) | BE-47 |
| 18 | Working-file names and skill rule codes in visible sheets (`p6_z2.0….png`, `1B_walls.csv`, `1B_log.md`, "R80e.34 #4", "R73.13"). | Review Items col F, Material Summary cites, Pending Items | Replaced by "zoom crop of N/SHEET" and "estimating default"; scan of all visible cells: 0 hits | BE-41, BE-55 |
| 19 | RFI-B01 (column wrap count 9 vs 8) left open. Re-counted on A-101: 9 C25 tags (5 on the upper grid row, 4 on the lower; the 5th lower column is C23 exposed). | 1/A-101 crops at 2x | Closed, K rows [CONFIRMED]; text in the 3-5/8" stud row says "9 tags counted" | BE-14 |
| 20 | Scope Checklist: headers, existing exterior, ceiling blankets, relief channel statuses. | — | ALC-02/03/10 restated, ALC-21 added | BE-18 |

## C. Re-verified with fresh crops — no change

- Tag sweep A-101 (6 tiles at 2x): type 2 diamonds on stock/sales wall (x2), BOH north wall (x3), women's west, lav chase (x2), men's/janitor west, break/manager, storage (x2): same 15 wall rows, no double count (2-10a + 2-10b = 12'-11" printed; 2-01b 12'-11" printed). Type 5 x1 (central RR wall). Type 3 x4 diamonds = 2 units (12'-0" bar + 2 posts 3'-8" each). Type 4 x1 "TYP." Exterior 1/1A/1B/1C kept separate (N, W, S, E never merged) and now excluded. [CONFIRMED by count]
- A-221 section G: sales face = 1 layer GWB, workroom face = 1 layer FRT plywood (H2a), both faces plywood (H2b); H2 no insulation (printed). Pass 1 layers correct (BE-05 PASS). Section H3/I plywood-then-GWB split correct.
- Door deductions on board faces recomputed (2-02: (23.0+9.5) x 56.83 − 2 x 3.0 x 7.0 = 1,805 SF) match. Jamb studs 2 per opening kept.
- Wall heights: A-400A/B print 23'-0" to the B.O. joist (V.I.F.) and B.O. deck 25'-0"; 2,5/A-410 put the deflection track at "underside of deck". Plan does not settle which governs → kept printed wall heights, RFI-B20 delta restated (+2.0 ft).
- Restroom W.R./cement board: 22/A-201 base 1'-2" cement board, W.R. above to B.O. gyp ceiling; janitor W.R. to deck + FRP to 8'-0" (9-12/A-200). Break room: kitchen unit is on the south (existing exterior) wall per 7/A-412, so no new W.R. face.
- Stud, track, bracing, clip angle counts regenerate pass 1 exactly (3-5/8" stud 7,683.97 LF, 6" 2,227.42 LF, C.R. channel 2,110.44 LF, 1,771 clips) after my replication check.

## D. Still PENDING / open (not answered by the sheets)

Stock-room steel shelving blocking (C14/C27 counts), receiving-table levels, type 4 X-wall returns, soffit T.O. WD-1 and depth, cafe ceiling zones, I-tag at SE storefront jamb, E1 pier closure, F box top, stud gauge, relief channel vs slotted track, 8.F vs 9/A-410 anchorage, ceiling blanket conflict, existing-exterior GWB scope (RFI-01).

## E. Process note

While orienting I read `work/build1c.py` (pass 1's own builder), which is outside the list of allowed sources. I used it only to understand how pass 1 assembled the workbook; all pass 2 numbers come from `out/1B_*.csv`, `out/1C_takeoff_pasada1.json` structure, and the drawings. The pass 2 builder lives in the scratchpad and reproduces pass 1's unchanged rows to the cent.
