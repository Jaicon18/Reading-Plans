# Back-check of rev4 (rev3 to rev4 changes only) - CFA #2284 River Point, Sheridan, CO

**Date:** 2026-11-03.

**Scope:**
- the 35 lines of `CAMBIOS_rev4.md`;
- the RFIs marked RESOLVED;
- the 6 RFIs still open;
- workbook format and README;
- a re-run of `verificar_markups_excel.py`.

**Sources:**
- the bid set `cfa_work/plano/bidset_CLEAN_SIN_MARKUPS.pdf`;
- the rev4 deliverables;
- the RFI evidence in `cfa_rfi4/g1..g3` (respuestas_g*.json and png);
- the text grep `cfa_rfi4/set_text.txt`.

**New crops** (circled): `/tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_backcheck/`. The files are `a221_A11.png`, `s201_psl.png`, `a221_hoods.png`, `a603_cased.png`, `a601_cased.png` and `a602_cased.png`. The rev2 crops are still valid.

**Abbreviations:** MS = Material Summary, PT = Partition Takeoff, SC = Scope Checklist, PI = Pending Items.

## 1. CAMBIOS_rev4.md lines

| # | Item | rev3 | rev4 | Evidence (N/SHEET + crop; Excel) | Result |
|---|---|---|---|---|---|
| 1 | RFI-02 M3.5 spacing | open, 16" | RESOLVED 16" | A-202 schedule M3.5 "sistered to existing framing" + D.1 + S-101 note 4 "2x6 SYP @ 16" O.C." + D1/S-601 "existing 2x6 @ 16" O.C." (`g2/RFI02_evidence.png`); SC B48 | PASS |
| 2 | M3.5-01 kitchen board height | 10.5 | 14.667 | A-221 A.11: on the BOH / kitchen side, sheathing runs "from floor to roof deck" (`a221_A11.png`). S-201 prints +14'-8" T.O. joist at both ends of the line (`g1/r04_s201.png`, `s201_psl.png`). PT r9 H = 7.146 x 14.667 = 104.81. | PASS |
| 3 | M3.5-01 framing height | 10.667 | 14.667 | A-221 A.11 + A-202 C.2 (framing to the roof deck). MS r10 M3.5-01 = 7 x 14.667 = 102.67 (+28.0). | PASS |
| 4 | M3.5-01 top track | standard | 3" long-leg slotted | C1/S-801 (`s801_D1C1.png`). MS r6 = 7.15; r7 standard = M3.5-02 3.75 only. | PASS |
| 5 | MB-01 serving face | 3.5 | 7.667 | Serving sits inside the smoke loop on the BOH side (A-202 dash-dot line, `g1/a202_srv.png`), so A.11 floor to deck applies; board runs 14.667 - 7'-0" B.O. gyp (D3/A-624) = 7.667. 3.333 x 7.667 = 25.55. | PASS |
| 6 | MB-01 kitchen face | 10.5 | 14.667 | A.11 BOH. 3.333 x 14.667 = 48.89 (MS r32). | PASS |
| 7 | MB-01 framing height | 10.5 | 14.667 | A.11 + C.2. MS r11 = 4 x 14.667 = 58.67 (+16.67). | PASS |
| 8 | MB-01 top track | standard | slotted | C1/S-801. MS r8 = 3.33. | PASS |
| 9 | D1 braces at M3.5-01 / MB-01 | 12.25 LF | 0 | These walls now reach the truss, so C1/S-801 applies instead of D1 (`s801_D1C1.png`). MS r14 keeps only BRC-M3.5-02 = 4.71. | PASS |
| 10 | 54 mil bent plates | 7 | 2 | D1/S-801, one plate per brace at M3.5-02. MS r23 = 2. | PASS |
| 11 | **W6-01N-GB1 board height** | 10.417 | **14.25** | This is the north face of the W6 on the smoke line, facing the Dining north strip, which is the **public** side. A-221 A.11 reads "on public side, extend wall sheathing ... to 6" above finish ceiling" (`a221_A11.png`). PT J79 itself still reads "public side of smoke partition: sheathing to 6" above finish ceiling ... = 10.417 ft", yet H = 14.25. The board above the ceiling is not printed on the public face. | **FAIL**: -31.37 SF 1/2" regular (8.183 x (14.25 - 10.417)). Knock-on: joint compound -2.26 lb (143.49 to 141.23) and paper tape -11.61 LF (737.40 to 725.79). |
| 12 | W6-01S-SRV board height | 10.0 | 14.667 | Serving face of the same W6 (inside the loop, BOH), so A.11 floor to deck applies, and G.4 cement board runs to the deck where draftstopping is required. 7.9 x 14.667 = 115.87 (+36.87, MS r32). | PASS |
| 13 | RFI-06 walk-in G.11 | open | RESOLVED 10'-8" | A-202 G.11 + A-221 C.H. 10'-2" + KN2 closure panels (`g2/RFI06_evidence.png`). Value unchanged. | PASS |
| 14 | DEMO-04 | 12.333 / 226.51 | 12.25 / 224.98 | S-601 A4 "12'-3" (F.V.) B/existing PSL beam beyond" (`g1/r10_s601_A4.png`). 9.183 x 12.25 x 2 = 224.98. | PASS |
| 15 | DEMO-13 | 12.333 / 273.94 | 12.979 / 288.29 | S-601 A4 "12'-11 3/4" B/existing joists & T/new LVL" + "cut existing stud wall to sit on new beam". 11.106 x 12.979 x 2 = 288.29. | PASS |
| 16 | DEMO-08 | 12.333 / 22.61 | 12.167 / 22.30 | S-601 A3 "13'-6" field verify" (`g1/r10_s601_A3.png`) - 16" TJI = 12'-2" (DERIVED). 1.833 x 12.167 = 22.30. | PASS |
| 17-18 | DEMO-09 / -10 | 12.333 / 55.50 | 16.896 / 76.03 each | S-601 A4 "16'-10 3/4" (F.V.) T/exist top plate". 4.5 x 16.896 = 76.03. The opening height stays in RFI-10 (see section 3). | PASS |
| 19 | RFI-13 recess width | open | RESOLVED 24" | MH-102 "L = 24" for double pin and sleeve", H-2 / H-3 DOUBLE (`g2/RFI13_evidence.png`). Value unchanged. | PASS |
| 20 | Hatch shaft studs | 48.0 | 53.33 | A-230 legend "2'-6" x 3'-0" roof hatch" (`g1/r14_a230_legend.png`). S-201 +13'-6" T.O. joist - (A-221 C.H. 10'-2" - 24" per A1/A-604) = 5'-4". 10 studs (3'-0" side 4, 2'-6" side 3, corners shared) x 5.333 = 53.33 (MS r13). | PASS |
| 21 | Shaft runner + slotted top | 12 + 12 | 11 + 11 | 2 x (3.0 + 2.5) = 11.0 (MS r15 RH-SHAFT-T, r24). | PASS |
| 22 | Soffit hanger studs | 1.167 / 0.833 | 3.0 | S-201 +14'-8" - 24" TJS - C.H. 9'-8" = 3'-0" (DERIVED, `g1/r15_s201.png`). MS r13: SS-SRV-W 16 x 3 = 48 ... sum 213.0 + shaft 53.33 = 266.33. Observation: the S-201 trusses are tapered (24" / 16"), so the 24" depth used gives the shorter, lower-bound hanger. | PASS |
| 23-24 | XBR-SRV-W / -N | 32.05 / 13.2 | unchanged | 1:1 brace per C4/A-624 still fits in 3.0 ft (widths 2.83 / 2.33 ft): w x 1.414 = 4.006 / 3.30. | PASS |
| 25 | XBR-GT | 22.31 | 19.82 | GT width 3.944 ft is more than the 3.0 ft hanger, so the 1:1 brace is capped: sqrt(3.944² + 3.0²) = 4.955 x 4 = 19.82. | PASS |
| 26 | RFI-19 | open | RESOLVED, removed | A2/A-604 shows cement board and gyp in one plane on the studs, plus A-202 G.2 "between wall tile and studs" and A-050 KN10 (`g3/RFI-19_evidence.png`). 617.08 SF unchanged. | PASS |
| 27 | Draftstop patch | 16 SF | 32 SF | A-052 note 9; P-211: 4 x 6" beverage conduits at the kitchen / service wall (`g3/RFI-20_evidence.png`). 4 x 2 x 2 x 2 = 32. In MS r22 (PATCH-BEV 32). | PASS |
| 28-31 | RFI-07 / 09 / 11 / 12 sweeps | open | open + sweep | See section 3. | PASS |
| 32-34 | PS-RECESS split, BE-117 IDs | - | split / IDs | MS r10 PS-RECESS-S1 / S2 21.33 each; r19 T1 / T2 4 each; the verifier passes every annotation (section 5). | PASS |
| 35 | Pending Items: open RFIs only | 12 open | 6 open | PI A2-A7 = RFI-07, 09, 10, 11, 12, 20; resolved RFIs moved to SC B48-B60 "RESOLVED from drawings". | PASS |

Material Summary NET check:
- 1/2" regular +61.26 = W6-01N-GB1 31.37 + MB-01 serving 13.88 + patch 16.
- Cement board +80.53 = 29.78 + 13.89 + 36.87.
- Mesh tape 0.37 x 1880.8 = 695.90; setting compound 0.072 x 1880.8 = 135.42.
- Joint compound 0.072 x 1992.98 = 143.49 and paper tape 0.37 x 1992.98 = 737.40, where 1992.98 = 1512.90 + 332.06 + 148.02.
- All of these are consistent with the rev4 inputs. The paper tape and joint compound change if line 11 is fixed.

## 2. RFIs marked RESOLVED: is the printed or derived answer cited?

| RFI | Answer | Citation verified | Result |
|---|---|---|---|
| RFI-02 | 16" O.C. (DERIVED) | A-202 M3.5 + D.1, S-101 note 4, D1/S-601 (crop) | PASS |
| RFI-04 | deck +14'-8" (CONFIRMED) | S-201 +14'-8" x2, A-221 A.11, A-202 C.2 (crops). The application to the public face is wrong; that error is counted in line 11. | PASS |
| RFI-06 | 10'-8" AFF (DERIVED) | A-202 G.11 + A-221 C.H. 10'-2" / KN2 | PASS |
| RFI-10 (DEMO-04 / -13 part) | 12'-3" / 12'-11 3/4" (CONFIRMED) | S-601 A4 (crop) | PASS |
| RFI-13 | L = 24" (CONFIRMED) | MH-102 table + note (crop) | PASS |
| RFI-14 | 2'-6" x 3'-0" x 5'-4" (CONFIRMED + DERIVED) | A-230 legend (crop), S-201 +13'-6", A1/A-604, A-221 | PASS |
| RFI-15 | 3'-0" hanger (DERIVED) | S-201 +14'-8" / 24" TJS, A-221 9'-8", C4/A-624, C3/S-801 | PASS |
| RFI-19 | removed (CONFIRMED) | A2/A-604 + G.2 + KN10 (crop) | PASS |

## 3. The 6 open RFIs: sweep present, and truly not printed?

| RFI | Sweep in PI / RFI_PENDIENTES | Spot check (grep of set_text.txt + crops) | Result |
|---|---|---|---|
| RFI-07 play-bay ceiling framing | 19 sheets, 9 terms | "PT-41" appears only as finish tags (3 hits); "14'-6"" is only the C.H. and A-401 levels; no member is labeled. | PASS |
| RFI-09 bridging member | 15 sheets, 12 terms | "BRIDGING" hits: A2/S-241 "BRIDGING LOCATION / MID SPAN" (location only), S-902 C05400 3.4.E (wall studs), wood toe-nail. No joist bridging member is printed. | PASS |
| RFI-10 (partial) KN24 opening height | 29 sheets, 16 terms | A-602 D3 "stainless steel cased opening / open to beyond" has no dimension (`a602_cased.png`); A-601 A3 cased openings are doors with no dimension (`a601_cased.png`). The only "7'-0"" is the A-603 D2 drive-thru opening (`a603_cased.png`), which is not a KN24 east-wall opening. Observation: DEMO-09 / -10 are loaded to 16'-10 3/4" across a cased opening, which is very conservative. | PASS |
| RFI-11 half-wall height | 52 sheets, 31 terms | "HALF WALL" has 1 hit only (A-050 KN8, no height). | PASS |
| RFI-12 furr-down drop | 52 sheets | "FURR DOWN" hits: A-052 KN3 (no height) and "B.O. FURR DOWN" on new-work elevations only. | PASS |
| RFI-20 (partial) patch size | 52 sheets | "PATCH" hits: A-052 note 9 only for the draftstop; no size is printed. **But PI B7 still says "The current load is 2 chases at 2'-0" x 2'-0". Per P-211 the count should be 4"**, which contradicts the 4 chases / 32 SF loaded (line 27). | **FAIL** (text; 0 quantity) |

## 4. Format

| Check | Result | Evidence |
|---|---|---|
| Excel has exactly 6 sheets, no hidden sheet | PASS | Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist (all visible) |
| Project data present | PASS | Inputs A32 "PROJECT DATA", B33 project, B39 bid date, A51 mandatory sheets reviewed |
| README starts with "ESTA ES LA VERSIÓN FINAL PARA REVISAR" | PASS | `README_REVIEW.md` line 1 (RFI_PENDIENTES.md also starts with it) |

## 5. verificar_markups_excel.py re-run

Command: `python3 -I skill_v81cf11/take-off-metal-frame-drywall/tools/verificar_markups_excel.py <Markups_Bluebeam_rev4.pdf> <Takeoff_FINAL_rev4.xlsx> cfa_calc_rev4/etapas/4_canon/takeoff_canon.json`

Output: **rc = 0**, `{"annots": 121, "ok": 121, "fail": 0, "hojas_markups": {"A-050": 12, "A-052": 7, "A-202": 85, "A-221": 17}, "fallas": 0}`. Result: **PASS**. The report is saved as `cfa_backcheck/verif_rev4.md`.

## Summary

53 lines checked: **51 PASS, 2 FAIL**.

1. **W6-01N-GB1 (line 11):** board on the public (dining) face was taken to the deck. A-221 A.11 limits the public side to 6" above the finish ceiling. Fix: H 14.25 back to 10.417 ft. Delta: **-31.37 SF** 1/2" regular (1512.90 to 1481.53), joint compound -2.26 lb (143.49 to 141.23) and paper tape -11.61 LF (737.40 to 725.79).
2. **RFI-20 text (PI B7):** the sentence "current load is 2 chases ... should be 4" is out of date; 4 chases / 32 SF are loaded. Text only, no quantity change.

BACK-CHECK RESULT: FAIL - (1) W6-01N-GB1 public-side board height: -31.37 SF 1/2" gyp (-2.26 lb compound, -11.61 LF tape); (2) Pending Items RFI-20 stale "2 chases" sentence (text).

## Re-check of the rev4 fixes (regenerated rev4, 2026-11-03)

| # | Item | Before | Now | Evidence | Result |
|---|---|---|---|---|---|
| R1 | W6-01N-GB1 public (dining) face | H 14.25 / 116.61 SF | H 10.417 / 85.24 SF | A-221 A.11 "on public side ... 6" above finish ceiling" (`a221_A11.png`). PT r79 8.183 x 10.417 = 85.24; J79 is consistent with it. | PASS |
| R1a | 1/2" gyp regular (MS r22) | 1,512.90 | 1,481.53 | Breakdown includes W6-01N-GB1 85.24 (sum 1,481.54); 1,512.90 - 31.37 = 1,481.53 | PASS |
| R1b | Joint compound (MS r47) | 143.49 | 141.24 | Driver 1,481.53 + 332.06 + 148.02 = 1,961.61 SF; 0.072 x 1,961.61 = 141.24 (cell formula =Inputs!B23*1961.61) | PASS |
| R1c | Joint tape (MS r48) | 737.40 | 725.80 | 0.37 x 1,961.61 = 725.80 (cell formula =Inputs!B24*1961.61) | PASS |
| R2 | Pending Items RFI-20 text | "current load is 2 chases ... should be 4" | "Loaded: 4 chases (P-211, 4 x 6" dia beverage conduits) x 2'-0" x 2'-0" x 2 faces = 32 SF. The patch area per chase is still an RFI." | PI B7 / C7; matches MS r22 PATCH-BEV 32 | PASS |
| R3 | Bridging row and RFI-09 citation | C09111 3.2.C | A2/S-241 'BRIDGING LOCATION: MID SPAN' (printed) + S-902 C05400 3.4.E.2 by analogy | MS r18 N/SHEET A2/S-241, S-902; PI RFI-09 B3 / C3. No "3.2.C" left anywhere in the workbook or in RFI_PENDIENTES.md. | PASS |
| R4 | verificar_markups_excel.py on the regenerated rev4 PDF / Excel / canon | rc 0 | rc 0 | 121 annotations, 121 ok, 0 failures (`cfa_backcheck/verif_rev4b.md`) | PASS |
| R5 | Workbook sheets | 6 | 6 | Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist (all visible) | PASS |

Both rev4 failures and the bridging citation are now fixed. All of the re-check rows pass.

Observation (outside the requested scope, no quantity effect): the only remaining "C09111 3.2.C" is in Scope Checklist D57. It sits in the RFI-16 metal-alternative text ("+0.00 LF bracing C.R. channel (C09111 3.2.C @ 48\")"), not in the bridging row or RFI-09.

BACK-CHECK RESULT: PASS
