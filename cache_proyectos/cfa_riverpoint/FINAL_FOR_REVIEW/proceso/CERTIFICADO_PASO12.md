# STEP 12 CERTIFICATE: Total Coverage Matrix (inverse review)

**Project:** Chick-fil-A #2284 River Point FSU Remodel, Sheridan, CO
**Deliverable reviewed:** `Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev1.xlsx` and `Planos marcados/CFA2284_RiverPoint_Markups_Bluebeam_rev1.pdf`
**Sources used:** the bid set (172 pages; the clean copy plus the SHX copy), the deliverables and BIBLIOTECA_ERRORES.md. No other take-off, canon, reading or resolution file was opened.
**Date:** 2026-11-02

## Verdict: DOES NOT PASS

The take-off still has 17 coverage gaps, 21 library FAILs and 3 proportion FAILs. The Bluebeam markups match the Excel.

## 1. Coverage (MATRIZ_COBERTURA.xlsx, sheet "Coverage Matrix")

| Set | Items | COVERED | EXCLUDED | RFI | N.A. | GAP | Coverage |
|---|---|---|---|---|---|---|---|
| Curated scope items (G, A, S, M/P/E, K, F, specs C05400 / C09111 / C09250 / C08306, S-902 C05000-C) | 220 | 90 | 78 | 23 | 12 | **17** | **92.3 %** |
| Raw sweep (every keyword block on the 172 sheets, classified by rule) | 1,834 | 588 | 1,205 | 0 | 41 | 0 | 100 % |
| All rows | 2,054 | | | | | 17 | 99.2 % |

The requirement is 100 % coverage, so it is **not met**. The 17 GAP rows reduce to the 13 unique plan and spec gaps G-01 to G-13 below. Two pairs of rows are the same item: C4/A-624 and C3/S-801 (cross brace), and A-202 C.4 and D1/S-801 (MB-01 bracing).

Limitation: the M, P and E plan sheets (pages 76-117) have no text that can be extracted, because the drawing text is vectorized. The SHX annotations exist only on pages 89 and 139-150. Those sheets were checked from their notes and specs (M-901, M-501, P-901, E-401, E-402, E-103, E-104, FP1.1), plus a visual check of E-203.

### Gaps (sheet "Gaps")

| # | N/SHEET | What is missing | Delta |
|---|---|---|---|
| G-01 | A-052 general note 9 | "PATCH EXISTING DRAFTSTOP WALL BETWEEN KITCHEN AND SERVICE AT NEW BEVERAGE CHASES": no row, no exclusion, no RFI | not quantifiable (allowance or RFI) |
| G-02 | C09250 2.2.A + 3.3.A (A-909) | Water-resistant gypsum backing board "at sinks, toilets, mop sinks" is not addressed. ALC-08 wrongly says no MR board is specified. | up to 148.02 SF of restroom gyp, 1/2" regular to 5/8" WR Type X |
| G-03 | C09250 2.1.E + 3.2.A.3 | Ceiling surfaces must be Ceiling Type (sag-resistant). Row 15 says "5/8" regular". | 332.06 SF, product change |
| G-04 | C09250 2.4.B.2 / 2.4.D.2 / 3.5.E | No joint treatment for 1,800.53 SF of cement board | ~ +666 LF AR mesh tape, ~ +130 lb setting compound |
| G-05 | D3/A-624 + C09250 3.4.B.2 | Exposed gyp edge at B.O. gyp 7'-0" (menu board) has no LC / J-bead | ~ +13.68 LF |
| G-06 | C4/A-624 + C3/S-801 | 3-5/8" cross brace @ 32" O.C. (362S162-33) at both soffits | ~ +70 LF 3-5/8" 33 mil |
| G-07 | C2 + D1/S-801, A-202 C.4 | MB-01 brace (362S162-33 @ 48", bent plate 54 mil, 33 mil continuous track) is carried as C.R. channel | ~ +8 LF 3-5/8", +2 plates, +3.33 LF track, −6.67 LF C.R. channel |
| G-08 | C2/S-801 | L1-1/2" x 1-1/2" x 33 mil continuous angle | +3.33 LF |
| G-09 | C2/S-801 | "33 MIL BLKG. T&B": only one row carried | +3.33 LF |
| G-10 | A1/A-604 | 3"x3"x1/4" clip angles @ 48" at the hatch shaft: not excluded and not in RFI-14 | ~4 pcs |
| G-11 | S-902 C05000-C 2.5.A.1 | Studs "min. base-metal thickness 0.0538 inch" against 33 mil carried, with no RFI | gauge of ~714 LF of studs and joists plus ~386 LF of track |
| G-12 | D3/A-624 | Menu-board wall prints "2X6 WD OR 6" METAL @ 16" O.C.", but RFI-17 says "printed nowhere" | if 6": 42 LF stud + 6.67 LF track, 3-5/8" to 6" |
| G-13 | K-001 equipment note 6 | Unistrut for suspended shelving and shrouds: exclusion not stated | n/a |
| G-14 | A-221 PT-41 / A2/S-241 | Play-bay gyp ceiling has no 6" rim track (the other 4 ceilings have it) | ~ +34 LF 6" track |
| G-15 | M2.1 / A1/A-605 | 28.33 LF of C.R. channel "bracing" on Z-furring, with no printed source | −28.33 LF |
| G-16 | MS row 8 | Labeled "1-1/2" Z" but 2" Z is printed | 96 LF, product change |
| G-17 | MS row 12 | 33 mil soffit track, 362T125-54 strongback and shaft track are in one row | split 26.51 LF |
| G-18 | MS row 16 | Breakdown is cut off after 3 of ~27 sources | traceability only |

G-14 to G-18 are Excel-integrity findings from (b) and (c), not plan coverage gaps.

## 2. Error library (sheet "Error Library"): 44 PASS · 21 FAIL · 20 N.A.

**FAIL (21):** BE-03, BE-12, BE-14, BE-15, BE-16, BE-18, BE-52, BE-53, BE-40, BE-45, BE-46, BE-55, BE-102, BE-105, BE-106, BE-VS-02, BE-VS-03, BE-VS-06, BE-VS-08, BE-VS-09, BE-CF07.

| Test | Finding |
|---|---|
| BE-03 / VS-02 | Wet-room backing board and ceiling-type board from C09250 are not applied (G-02, G-03) |
| BE-12 | Two citations do not support what the row says. MS row 13 and ALC-06 cite C09111 3.2.C, which covers suspension sway-bracing, not wall bracing. They also cite C2/S-801, which prints a diagonal stud brace, not C.R. channel. Separately, Inputs!C26 quotes "estimator decision 2026-10-27", a decision from another project. |
| BE-14 | Three "not printed / not specified" claims are contradicted: ALC-08 (no MR), RFI-17 (D3/A-624 and C2/S-801 do print the framing) and MS row 38 (C1/S-801 prints a 3" long-leg slotted track). |
| BE-15 / BE-105 / VS-06 | Printed products were replaced by defaults: Z 1-1/2" instead of 2"; C.R. channel instead of 362S162-33 brace; 5/8" regular instead of ceiling type; 33 mil instead of S-902 0.0538". |
| BE-16 / BE-53 | Printed accessories have no row and are missing from the RFI deltas: C2 angle, D1 bent plates, A1/A-604 clip angles, C4 cross brace. |
| BE-18 / VS-03 | The 17 coverage gaps above |
| BE-40 | MS row 16 breakdown is truncated |
| BE-45 | Proportion FAILs (section 3) |
| BE-46 / CF07 | MS row 12 mixes products; MS row 8 Z size is wrong |
| BE-52 | ALC-16 says "menu board 33 mil T&B", but row 18 has only one row |
| BE-55 | Client-facing text contains internal codes: R-ALC-xx, "resolver:", PT00xx and crop file names |
| BE-102 | "GA-216" and "3/CT-73B" are cited as N/SHEET but are not sheets |
| BE-106 | Precedent from another project, as above |
| VS-08 | No cross table of demolition against the new floor plan |
| VS-09 | Framing rows have no spec cross-check, which is how the S-902 and C09250 requirements were missed |

The N.A. tests are mostly runner and process tests (BE-59..98, 101, 108, 115, CF06) or conditions that do not exist here (ballistic, ATM, HOLD, SIM., rated assemblies, canopies). The library file was not edited; this step had no write order for it.

## 3. Proportions (sheet "Proportions"): 10 PASS · 3 FAIL

| Check | Result |
|---|---|
| Board vs Σ LF × H × faces: 3,716.25 SF in both the takeoff and MS | PASS (soffit bottoms ~100 SF appear only in the NET) |
| Studs per LF vs O.C. (M2.1 96, M3.5 117.34, MB-01 42, soffit sides 75.84, joists 304.5) | PASS |
| Track vs partitions (bottom = top = 14.23 LF; soffit track = 2 × 73.44) | PASS |
| **Rim track vs gyp ceilings: the play bay has none** | **FAIL** (~ +34 LF) |
| **Compound and tape vs board: driver 1,915.72 of 3,716.25 SF (51.5 %); cement board excluded without explanation** | **FAIL** |
| **Bracing vs walls: 28.33 LF C.R. channel on M2.1 Z-furring (not a stud system); MB-01 printed brace missing** | **FAIL** |
| Level 5 (731.2 SF), corner bead (73.44 LF), waste (15 % / 6 %), demo (2,646.57 SF) | PASS |

## 4. Bluebeam vs Excel (sheet "Bluebeam Cuadre"): PASS

The check covers 106 PolyLines with /Measure: 87 walls plus 19 demolition items. The legend page has 4 sample annotations, which were not counted.

| Type | Excel Σ L / Σ A | Markups Σ L / Σ A | Δ |
|---|---|---|---|
| M2.1 | 14.167 / 151.12 | 14.167 / 151.12 | 0.00 % |
| M3.5 (incl. MB-01) | 14.229 / 151.23 | 14.222 / 151.15 | −0.05 % |
| Soffit sides | 73.439 / 78.05 | 73.439 / 78.05 | 0.00 % |
| Board only | 950.940 / 2,887.16 | 950.933 / 2,887.06 | 0.00 % |
| Demo (SF) | 2,646.57 | 2,646.57 | 0.00 % |

The largest difference is 0.05 %, within the 0.5 % limit. Two observations:
- MB-01, which is 3-5/8", is filed under Subject "M3.5", which is 8".
- The DEMO annotation contents are in Spanish ("DERIVADO", "PENDIENTE").

## 5. To close Step 12

1. Add rows, RFIs or exclusions for G-01 to G-13. The most urgent are:
   - RFI for the S-902 0.0538" gauge (G-11)
   - RFI for the C09250 WR backing board (G-02), and change the ceiling-board product (G-03)
   - Cement board joint treatment (G-04)
   - Soffit cross braces (G-06)
   - MB-01 bracing per C2 and D1/S-801 (G-07 to G-09)
2. Fix G-14 to G-18: play-bay rim track, M2.1 bracing, row 8 label, row 12 split, row 16 breakdown.
3. Correct the wording errors:
   - ALC-08, RFI-17 and MS row 38
   - Citations in MS row 13 and ALC-06
   - Inputs!C26
   - The N/SHEET entries "GA-216" and "3/CT-73B"
   - Internal codes in the client text
4. Re-run Step 12.
