# AUDIT CERTIFICATE - Step 11 (Independent Final Auditor)

**Project:** O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 - Metal Framing & Drywall (CSI Div. 05 / Div. 09)
**Bid set:** `bidset.pdf` (EV1 Current Conformed Set 11-20-2025, raster sheets, 68 pages)
**Deliverables audited:** `OReilly_Evans_CO1_Takeoff_pasada2.xlsx`, `OReilly_Evans_CO1_Markups_pasada2.pdf`, `markups.json`
**Audit date:** 2026-10-31. The auditor used only the files in `audit_p11/`. The Excel was **not** modified.
**Rule #0:** No dimension was scaled. Every figure below cites a printed dimension (N/SHEET), or the text says it is not printed. Evidence crops are in `audit_p11/img/` (19 files, circled). The auditor reopened every crop after writing it to check the circles.

**Estimator standing orders applied (not counted as errors):** all fasteners and anchors are excluded; MEP / electrical / civil / cabinets are excluded; board is not deducted at openings; FRT parapet nailers (Div. 06) are excluded; open RFIs carry a conservative assumption (Pending Items).

## RESULT: PASS 4 / 8 - FAIL: checks 2, 3, 5, 6

| # | Check | Result |
|---|---|---|
| 1 | Tag sweep | **PASS** |
| 2 | Re-measurement vs printed dimensions | **FAIL** |
| 3 | Detail chain (Material Summary -> N/SHEET) | **FAIL** |
| 4 | Scope sweep (A1.1-A6.1, S1.1-S5.3) | **PASS** (3 observations) |
| 5 | Arithmetic | **FAIL** |
| 6 | Format | **FAIL** |
| 7 | Bluebeam markups | **PASS** |
| 8 | Files | **PASS** |

---

## 1. Tag sweep - PASS
- A1.1 Interior Wall Types prints 6 types: S21, S24, S41, S42, S43, S61 (img `08`). All 6 are in the Partition Takeoff and in the markups.
- Every tag drawn on 1/A1.1 maps to a wall row and to a markup (img `18`):
  - S21: grids A, 1, 4 and C (both stretches).
  - S24: office 102 = S24-OF. R.R. 103/104 east side = S24-RR (2 tags, one line). R.R. 104 south side = S24-RRS.
  - S41: 4 tags, 2 box-outs (key note 5).
  - S42: grid B horizontal wall and the vertical wall.
  - S43: office 102 has 3 walls. R.R. has 1 west wall plus the line of 2 tags = S43-RR-S.
  - S61: wet wall.
- Walls drawn without a tag are also carried:
  - EXT-MS1 / EXT-MS2 metal stud piers at grid C (6'-0"/A1.1).
  - Storefront A head HEAD-A (38'-8" R.O./A5.2).
  - Vestibule heads VH-B1 / VH-B2 / VH-C (3/A3.1).
  - South cornice CORN-S (36'-0"/A1.1, 1/S5.3).
- Count: 32 walls = 32 markups = 30 Excel rows. The difference is because the S42 walls are merged into 2 rows (see check 6).

## 2. Re-measurement - FAIL
**Within 2% or exact against printed dimensions:**

S21 lengths (5 walls, 288.6 LF = 50% of the partition LF):
- Grid C chain 4'-0" + 6'-8" + 6'-0" + 18'-8" + 8'-0" + 12'-0" + 6'-0" + 22'-4" + 4'-0" on A1.1 (img `02`) gives S21-W1 = 9.156 and S21-W2 = 24.823. Both are exact.
- S21-N, S21-E and S21-S are within 0.42% of 30'-0" + 30'-0" + 25'-0"/A1.1.

S21 heights:
- They come from T.O. HIGH EAVE EL. 116'-4 3/4" and T.O. LOW EAVE EL. 114'-7 1/2" on 1/A3.2 and 2/A3.2 (img `07`), less the assumed 8" purlin (RFI-01, closed by the estimator).
- Results: 15.729 / 13.958 / 14.844 (average of the two eaves). These are consistent.

Other walls:
- **EXT-MS1/2:** 6'-0"/A1.1.
- **HEAD-A:** 38'-8"/A1.1 and 38'-8" (R.O.)/A5.2 (img `14a`).
- **D1 / D2:** 11'-4 3/8" (R.O.)/A5.2 (img `14b`).
- **S43-OF-W/E:** 8'-0"/A1.1.
- **S43-RR-W and S61-RR:** 8'-6"/A1.1.
- **S43-OF-S:** 11'-0"/A1.1 plus 2 x 4-1/4" = 11.708.
- **S43-RR-S:** 7'-10" + 6" + 7'-10"/A1.1 plus 4-1/4" = 16.521.
  - Both of these use the clear-room convention. The chain prints the S61 6" wall separately, which supports that convention (img `03`).
- **S41:** 2'-2"/A1.1 and 1'-8"/A1.1 (img `05`, `06`).
- **S42-01:** 1'-8" + 37'-0" = 38'-8"/A1.1.
- **S42-03:** 50'-4"/A1.1.
- **S42-04:** 8'-2"/A1.1.
- **Interior heights:** 8'-6" (S24 / S43 / S61), 12'-0" (S41) and 12'-0" in Parts Area A (S42), all from the A1.1 type legend (img `08`).
- **Board faces:**
  - 7/A4.2: 8'-6" + 6" joist gives the 9'-0" face.
  - 6/A4.2: 4'-8" + 6" gives the 5'-2" face, with B.O. FRAMING EL. 106'-10" (img `16`).
- **Not re-opened by the auditor:** the EXT-MS height of 20.667 ft (T.O. metal stud 120'-8", cited from 1/A3.1).

**Exceptions (> 2% or not printed):**
- **S42-02 = 25.455 LF:**
  - Only 18'-4"/A1.1 is printed, plus the S42-03 thickness.
  - The free end past the S42-03 corner (about 6.77 LF) has **no printed dimension** on A1.1 (img `04`). Its only reference is the witness line of the 16'-10 7/8"± vertical dimension.
  - The Excel marks the row [DERIVED] "(A1.1)" with no RFI or pending flag. Under Rule #0 this cannot be verified.
- **S24-OF:**
  - Take-off 11.708, auditor 11.000 (11'-0"/A1.1, clear). Delta +6.4%.
- **S24-RR:**
  - Take-off 16.823, auditor ≤ 16.167 (7'-10" + 6" + 7'-10"/A1.1). Delta ≥ +4.1%.
- **S24-RRS:**
  - Take-off 8.854, auditor 8.500 (8'-6"/A1.1). Delta +4.2%.
  - In all three S24 walls, the S24 runs through the adjoining walls' thickness.
  - Material impact is small: +1.7 LF and about +15 SF of board.

## 3. Detail chain - FAIL
**Sample (≥ 15 rows, including the largest quantities).** Each listed row was opened on the plans and its content confirmed:

| Row | Material | Confirmed by |
|---|---|---|
| 23 | 5/8" Type X | A1.1 types (img `08`); key 20/A3.2 (img `17`) |
| 24 | Type X W.R. | A1.1 note 3.B (img `09`); A1.2 R.R. 103/104 (img `15`) |
| 17 | 3-5/8" stud | 362S162-33 @ 24" O.C. in the A1.1 types |
| 16 | 6" stud | S61 600S162-33 (A1.1); keys 17/22 on S5.3 (img `10`) |
| 15 | 8" stud | key 18/S5.3 |
| 19 | C.R. bracing | note 2.F/A1.1 |
| 26 | Deep-leg deflection track | 3/S5.1 and 4/S5.1 (img `11`) |
| 27 | FCB43.5 clips | keys 16/23 on S5.3 |
| 21 | Glass mat sheathing | key 19/A3.2 |
| 28 / 29 / 36 | RC 7/8", 1/4" gypsum board, FRT plywood | 1/A5.2 (img `13`) |
| 30 | Diagonal flat strap | note 2.B/A1.1 |
| 35 | Control joints | note 3.A/A1.1 |
| 34 | Trim | note 3.C/A1.1 |
| 33 | Track brace | 5/S5.1 (img `12`) |
| 32 | W-4 panels | A1.2 (img `15`) |
| 22 | FRT blocking | note 2.A/A1.1 |
| 7 / 12 | 3-5/8" bottom and top track | 3/S5.1 (362T125-33) |

**Why this check fails:**
- Of the material rows, 44 / 51 say "N/SHEET: not applicable (see note)" in "Where it comes from". The chain cannot be opened from the Summary itself.
- Row 18 (ceiling perimeter track) cites **1/A-121 and 5/A-121**. Those sheets are not in this set (SHEET_MAP).
- Row 14 (Z-furring, 2,517.5 LF, the largest metal quantity) and row 20 (header / box beam, 56 LF) have **no breakdown and no detail**.

## 4. Scope sweep - PASS (with observations)
**Every required item is in the Scope Checklist and the Material Summary:**
- Blocking and backing: ALC-16, rows 22 and 36.
- Soffits: ALC-13.
- W.R.: row 24.
- Type X: row 23.
- Glass mat: row 21.
- FRT plywood: row 36.
- Headers: ALC-05, rows 20 and 37.
- Control joints: row 35.
- Corner bead / J molding: row 34.
- Deflection track: row 26.
- Bracing: rows 19 and 30.
- Clips: rows 25 and 27.
- Access panels: row 44, 0 with reason.
- Insulation: excluded under ALC-X28.
- Fasteners, MEP and FRT parapet nailers: excluded per the estimator's orders.

**Observations:**
- **(a) Rigid insulation.** The 1-1/2" foil-faced polyisocyanurate (min R-9) printed in S21 / S24 (img `08`) is not named in the exclusion. ALC-X28 says "batt" only.
- **(b) Acoustical sealant.** A1.1 note 4.B calls for sealant. The Excel excludes it as an "estimator standing order", which is not among the orders given to this audit. The estimator should confirm.
- **(c) Stucco.** Exterior portland cement stucco (1/A5.2) has no NOT-IN-SCOPE line.

## 5. Arithmetic - FAIL
**What ties:**
- Partition Takeoff board equals LF x H x faces on every single-face row. Multi-face rows tie to their printed face breakdowns (for example S21-S: 17 x 14.84 + 58.64 x 14.84 + 9.36 x 5.05 = 1,170).
- Subtotals and the grand total formulas: 576.32 LF and 7,755.65 SF.
- Every "Breakdown" sum equals its stated Net (32 rows checked by script).
- Tracks: 3-5/8" bottom = 219.19 = Σ LF of S24 + S41 + S42 + S43. Top = 219.19 − 46.84 deep-leg = 172.35.
- Stud counts: S24-OF 7 x 8.5. S42-01 is (ROUNDUP(38.667 / 2) + 1 + 1) x 14.505 = 319.11.
- Bracing rows: (ROUNDUP(H x 12 / 48) − 1) x L.
- Purchase and pieces formulas, for example Type X: 7,404.93 x 1.06 / 48 → 164.
- Compound: 0.072 x 8,126.14 = 585.08. Tape: 0.37 x 8,126.14 = 3,006.67.

**What fails:**
- **Z-furring row 14 cannot be reproduced.**
  - Auditor: S21 at 24" O.C. + 1 per wall x height = **2,235.0 LF**. Take-off: 2,517.5 LF. Delta +282.5 LF (+12.6%).
  - There is no breakdown. The excess may be S24 Z-furring, which is double counted because S21-E / S21-S already run behind S24.
- **Waste on compound and tape.** These rows carry 0% waste, but Inputs B6 says 6% on "EVERYTHING THAT IS NOT METAL". With B6: 620.18 lb (+35.1) and 3,187.07 LF (+180.4).
- **Resilient channel (row 28).** "Pieces" = LF (139). With 12 ft sticks it would be 12 pcs.

## 6. Format - FAIL
**What is right:**
- 6 visible sheets in the required order: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist. There is also a 7th, hidden sheet `_reglas`.
- Partitions follow the A1.1 schedule order (S21, S24, S41, S42, S43, S61, then EXT-8CFMF and EXT-6CFMF), with a subtotal per type.
- Trade terms are in English.

**What fails:**
- Spanish text remains in visible cells:
  - "RESPUESTAS_RFI_ESTIMADOR.md" appears 11 times (Pending Items, Material Summary, Scope Checklist).
  - Image paths "img_resolucion/", "img_ensamble/" and "img_revision/" (Review Items).
  - A raw Python dict `{'texto': ..., 'cita': ...}` in Pending Items C14.
  - The jargon "canon".
- S42-01+S42-02 and S42-03+S42-04 are merged into single rows with weighted heights (11.792 and 9.241), while the markups show 4 separate walls.
- The "Layers" column holds fractions (HEAD-A-8 = 0.79).

## 7. Bluebeam - PASS
- 32 PolyLine annotations on page 37 (Page Label "A1.1"), one per wall (img `18`).
- Each one carries /Subj = type, a /Measure (113/900 in = 1 ft, ft / sf), /Depth = height, and Contents of the form TYPE · LF · H · SF · DETAIL · id.
- The legend is on page 69 ("LEGEND", img `19`): 9 types, 32 walls, 673.74 LF. That equals the Excel partitions (576.32) plus other framing (97.42).

Reconciliation by type (markups.json):

| Type | Σ LF (markups) | Σ LF (Excel) | Σ geometric Length | Σ Wall Area (markups) | Σ L x H (Excel) |
|---|---|---|---|---|---|
| S21 | 288.625 | 288.625 | 288.54 (−0.03%) | 4,238.26 | 4,239.42 |
| S24 | 37.385 | 37.385 | 37.41 | 317.98 | 317.77 |
| S41 | 6.46 | 6.46 | 6.40 | 76.80 | 77.52 |
| S42 | 122.622 | 122.622 | 122.52 | 1,295.11 | 1,296.73 |
| S43 | 52.729 | 52.729 | 52.45 (−0.5%) | 445.83 | 448.20 |
| S61 | 8.5 | 8.5 | 8.52 | 72.42 | 72.25 |
| EXT-8CFMF | 12.0 | 12.0 | 11.96 | 247.18 | 248.00 |
| EXT-6CFMF | 48.0 | 48.0 | 48.02 | 534.54 | 534.89 |
| OTHER FRAMING | 97.418 | 97.418 | 97.31 | 806.49 | 807.84 |

Every type is within 0.6%.

## 8. Files - PASS

| File | Size (bytes) |
|---|---|
| OReilly_Evans_CO1_Takeoff_pasada2.xlsx | 36,899 (opens; 6 visible sheets + 1 hidden) |
| OReilly_Evans_CO1_Markups_pasada2.pdf | 57,866,352 (69 pages = 68 + legend) |
| markups.json | 7,304 |
| bidset.pdf | 58,017,594 (68 pages) |
| SHEET_MAP.md | 1,106 |

- Google Drive: **N/A - pending upload.**
- Note: the internal "pdf" / "bid_set" paths in markups.json point to other directories (provenance only).

Differences between the auditor and the take-off: see `COMPARATIVA_AUDITORIA.md` (16 items).
