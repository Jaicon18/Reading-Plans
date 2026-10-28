VERDICT: FAIL
LIBRARY: 42 PASS · 2 FAIL · 3 N/A

# Back-check rev12 - Barnes & Noble Colorado Springs (2026-10-28)

File: `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev12.xlsx`, md5 3c64ba1a9525bc3fa4d4488204675d39 (verified). Scope per R80e.30: only the rows touched in rev12 plus the full error library (47 tests, BE-01..BE-57). Plans were not re-read.

## 1. RFI decisions (34/34 present in Pending Items, all start "CLOSED - estimator decision 2026-10-27:" with N/SHEET and delta)

| ID | Decision | Applied? | Evidence (Material Summary row / Scope) |
|---|---|---|---|
| RFI-ACC-slab-pins | B: 1 row @ 16" | YES | R63 777.43 -> 388.72 = 518.29 LF / B22 (1.333); types 3/4 LF excluded |
| RFI-ACC-stud-reinf-mep | A: 8 crossings + TG-1 x2 | YES | R54 0 -> 10 (X01-X08 + T01-T02); R59 duct sleeves 8; ALC-17 |
| RFI-03 | A: deck 25'-0" | YES | no change |
| RFI-05 | A: E1/E2 once | YES | no change |
| RFI-09 | B: 2-piece header every door | YES (text FAIL) | R53 83.32 LF, 9 doors; breakdown text cut at 519 chars (see B2) |
| RFI-13 | B: FRP-1 + PVC trim | YES | R37 875.20 + 155.44; R58 215.04 + 70.86 |
| RFI-21 | A: fascia +53.6 SF Type X | YES | R19 CLOUD-FASCIA-GWB 53.6 |
| RFI-22 | B: 1 face types 3/4 | YES | R50 +936.74 (309.44 + 627.30); R37 +936.74; R19 -936.74 (PT rows 19-44 layers 2 -> 1); R58 +244.64 |
| RFI-24 | A: control joints 250 LF | YES | R47 5 x 25 x 2 = 250 |
| RFI-28 | A: moment clips | YES | R42 162, R43 324, R44 324 |
| RFI-29 | Both: stainless 1 + metal 72 | YES | R46 1, R45 72 (= CONTEO.md 72) |
| RFI-30 | B: EXCLUDED with note | YES | ALC-17 note verbatim; R60 = 0 |
| RFI-31 | A: remove 10.67 LF | YES | rev11 row removed; inside R53 |
| RFI-32/33/35/38/39/40/42/45/46/47/48/52/53/54 | A: keep | YES | nets unchanged (10.67, 17.0, 264.21, 743.29/131.42, 16.0, 479.85, 90.0, 66.7, 6.52+122.32, FRT, 387, 14.96, 401.0, 180.99) |
| RFI-36 | A: EXCLUDED with note | YES | ALC-16 note verbatim |
| RFI-41 | A: joists 5'-0", 775 | YES | R41 775 |
| RFI-43 | A: E1 cement board 12'-0" | YES | R36 739.90 -> 434.28 (-305.62 = RFI43.md alt. B) |
| RFI-44 | AUTO: H3a WD-1 15'-0" | YES | R50 -40.8; R19 C-H3a +40.8 |
| RFI-49 | 0 cased openings | YES | 2x wood blocking row removed; ALC-16 note |
| RFI-50 | EXCLUDED BY GC | YES | R51 402.46 -> 370.46; ALC-10 note |
| RFI-51 | keep + 512 brace screws; 520 @ 8/A-210 | YES | R48 512 (128 x 2 x 2) |

Board chain: Type X 15,109.29 - 936.74 + 40.8 + 53.6 = 14,266.95 (breakdown 14,266.92, OK +/-0.1). FRT 5/8" 1,790.51 + 936.74 - 40.8 = 2,686.45. Type S 6,114.04 -> 5,103.23 = 1.2 x 4,252.69 (-842.34 SF; types 3/4 and H3a are 20 ga, so Type S is correct). Compound 1,105.89 and tape 5,683.03 = B23/B24 x 15,359.5 (Type X + W.R.). All 21 expected changes CONFIRMED.

## 2. Format
- Sheets 6 visible + hidden `_reglas`, same as rev11; columns unchanged (Inputs gains row 30 FRP panel = 40 SF; OK).
- Wood blocking R18: B6 waste, B26 = 16 ft kept. FRP R37 / B30. All Pieces formulas use Inputs stock cells.
- Waste: see B3.

## 3. Library

| Test | Result | Note |
|---|---|---|
| BE-01..BE-11, BE-13, BE-14, BE-15, BE-18 | PASS | rows untouched or changed only per estimator decision; no new plan reading |
| BE-12 | PASS | new quotes (3/A-410 HUS-EZ, A/A-410 #10-16, C22, A-001A) match RFI texts |
| BE-16 | PASS | moment clip accessories all carried |
| BE-17 | PASS | Type S moved with 20 ga faces |
| BE-19 | PASS | 16" per 8.F, estimator decision |
| BE-52, BE-53 | PASS | RFI-28 delta = clip + 2 HUS-EZ + 2 #10-16 |
| BE-56 | PASS | slab pins on 640.61 - 122.32 = 518.29 LF |
| BE-20..BE-25, BE-29 | PASS | tracks 450.02/118.59 unchanged; headers 83.32 with RFI-09 |
| BE-26, BE-27, BE-28 | N/A | no ballistic / ATM recess / canopy |
| BE-40 | **FAIL** | R53 "Where it comes from" truncated after "Door 3 (C-H2a): (4.0 + 2 x 0.667)": no door 3 result and no "= 83.32 LF" |
| BE-41 | **FAIL** | Pending Items C3 "rfi_mep_cruces/CRUCES.md", C32 "rfi29_corner_guards/CONTEO.md", C46 "rfi43_cement_board/", C52 "rfi49_cased_openings/" |
| BE-42, BE-43, BE-44, BE-45 | PASS | PT changes only layers (types 3/4) and E1 heights; lengths/heights for markups unchanged |
| BE-46..BE-51, BE-54, BE-55 | PASS | numbers/IDs in texts match; no plan-check codes |
| BE-57 | PASS | no non-metal row uses B5 (FRP, PVC, cement board, plywood, blocking = B6) |

## Blocking issues
- **B1 (BE-41)** Remove the internal folder/file names from Pending Items C3, C32, C46, C52 (replace with "count on M-102 / A-101", "count on A-001A / A-101", etc.).
- **B2 (BE-40)** Material Summary I53: complete the text: "...Door 3 (C-H2a): (4.0 + 2 x 0.667) x 1 x 2 pieces = 10.67 = 83.32 LF (9 doors)".
- **B3 (check 2, waste)** Rows touched in rev12 with Waste % = 0 instead of an Inputs cell: R46 stainless corner guard, R54 stud plates, R59 duct sleeves, R61 Type S screws, R63 slab pins -> `=Inputs!$B$5`; R65 joint compound, R66 tape -> `=Inputs!$B$6`. (R46 is inconsistent with its sibling R45, which uses B5.)

## Non-blocking comments
- Same 0 waste inherited from rev11 on untouched rows R52, R60, R62, R64, R68, R69, R70: fix together with B3 for consistency.
- R53 is a track header but is bought as 20 ft stud sticks (B10); rev11 used B11 (track 10 ft). B10's note does list "header", so it is acceptable; confirm.
- R59 name "Power-driven fasteners and duct sleeves - duct sleeves..." is a leftover; rename to "Duct sleeves at duct crossings (M-102)".
- Partition Takeoff A96-A109 show snake_case kinds ("column_wrap", "soffit_side"), and MS I49 shows "framed_soffit"; inherited, cosmetic.
- ALC-16 menu boards 60.61 / restroom 17.78 vs MS 60.6 / 17.77 (rounding, inherited).
