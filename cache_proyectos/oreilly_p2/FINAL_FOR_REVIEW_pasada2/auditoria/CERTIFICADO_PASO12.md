# STEP 12 CERTIFICATE - Total coverage matrix (reverse review, plans -> Excel)

**Project:** O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 (EV1 Current Conformed Set 11-20-2025)
**Excel audited:** OReilly_Evans_CO1_Takeoff_pasada2.xlsx (not modified)
**Inputs used:** bidset.pdf (raster, read at 150-250 dpi, no scaling), SHEET_MAP.md, markups.json, BIBLIOTECA_ERRORES.md
**Matrix:** audit_p12/MATRIZ_COBERTURA.xlsx (sheets: Coverage Matrix, Summary, Error Library, Proportions, Markups Reconciliation). Image crops are in audit_p12/img/.

Standing estimator orders were applied as valid destinations, not as gaps: fasteners/anchors excluded; MEP/electrical/civil/cabinets excluded; board not deducted at openings; Div. 06 FRT parapet nailers excluded; open RFIs carried with a conservative assumption.

## Verdict: DOES NOT PASS

The 10 gaps, the 14 library failures, the proportion failure and the reconciliation failure all block delivery.

## 1. Coverage

Sheets swept: G1.1, S1.1, S4.1, S5.1, S5.2, S5.3, A1.1, A1.2, A2.1, A3.1, A3.2, A3.3, A3.4, A4.1, A4.2, A5.1, A5.2, A6.1.

| Status | Items |
|---|---|
| COVERED (Excel row) | 150 |
| EXCLUDED with reason (other trade / estimator order) | 63 |
| RFI (Pending Items) | 3 |
| **GAP (no destination)** | **10** |
| **Coverage** | **216 / 226 = 95.6 %** |

### Gaps (no row, no exclusion, no RFI)

1. **A1.1 note 3.A (second clause):** "Install control joints where framing or furring changes direction." The MS R35 breakdown only covers masonry CJ locations, the 30 ft rule and the vee joints.
2. **A1.2 GN D:** suspended ceiling seismic bracing per 9/A4.2. Nothing in the Excel mentions "seismic".
3. **A4.2 9/A4.2:** the suspended ceiling seismic bracing detail itself (SDC A/B, ASTM C636). Same item as #2, seen from the detail.
4. **A4.2 KN 12:** 1x4 paint-grade wood trim attached to the metal studs with Tech 12 screws @ 24" (top of the 7/A4.2 hard lid). No row, no exclusion and no RFI.
5. **A4.1 KN 11:** "Wood trim, paint". Same item as #4.
6. **A4.1 KN 8:** "Provide trim and edge molding around perimeter" of the W-4 sanitary panels. MS R32 carries only the panel SF, and R42 (PVC trim) = 0 with the reason "No FRP".
7. **A5.2 GN H:** security shutters, "provide additional support framing system as required". No destination.
8. **3/A5.2 (with 3/A3.1):** "6" cold form metal framing with diagonal bracing, refer to structural drawings" at the vestibule head. The VH-* rows carry studs, track and C.R. bridging only. The diagonal brace drawn in 3/A3.1 has no row and no RFI.
9. **11/A5.2:** window D head prints "5/8" fire treated plywood sheathing". The Excel carries glass mat on CORN-S (MS R21) and sends it to "RFI-05", but RFI-05 does not exist in Pending Items, so the destination is broken.
10. **1/A3.1 (pier interior board height):** MS R28, R29 and R35 carry "RFI-16 option A" (12.0 ft vs 16.396 ft), but RFI-16 does not exist in Pending Items, so the destination is broken.

Observations (not counted as gaps):
- Insulation (polyiso R-9, rigid R-10, batt R-19, sound batt) is excluded through ALC-X28 "estimator criterion: no insulation". That criterion is not one of the standing orders and needs a written source (BE-106).
- C-1 ACT is excluded as "by the ceiling installer" (ALC-12). That is not an estimator order. Confirm it in the clarifications.
- A5.2 GN I (storm panels) does not apply because G1.1 gives Vult = 108 mph, which is under 120 mph. The Excel does not state this.

## 2. Error library (BIBLIOTECA_ERRORES.md)

**PASS 33 / FAIL 14 / N/A 14** (61 lines; BE-59..BE-98 are grouped as one N/A line because the runner logs are not in the package).

| Test | Result | Evidence (short) |
|---|---|---|
| BE-12 | FAIL | MS R18 cites "1/A-121, 5/A-121", a sheet that is not in this set. RFI-ACC-deflection-clips cites a general note that does not exist, plus "R73.6". |
| BE-16 | FAIL | The 3/A5.2 + 3/A3.1 vestibule diagonal bracing has no row. |
| BE-18 | FAIL | 10 gaps. |
| BE-40 | FAIL | R14 Z-furring (2,517.5 LF) and R20 header (56 LF) have no breakdown. Rows read "N/SHEET: not applicable" instead of citing a sheet. |
| BE-41 | FAIL | "RESPUESTAS_RFI_ESTIMADOR.md" and img_*/…png paths appear in visible sheets (MS, Pending Items, Review Items, Scope Checklist). |
| BE-44 | FAIL | Drawn Length vs Excel LF: S41 -0.93 %, S43 -0.53 % (limit 0.5 %). |
| BE-45 | FAIL | Z-furring is +12.6 % over the computed value with no explanation. |
| BE-46 | FAIL | Several products share one row: R34 (corner bead + casing + J + DRMF + JDM), R25 (L4x4 + 2x2 clip), R16 (600S162 + 600S200), R5/R10 (mixed track gauges). |
| BE-47 | FAIL | RFI-05 and RFI-16 are cited but missing. RFI-11 says option A is carried while R17/R27 carry option B (98 LF of ties, 24 FCB clips). RFI-ACC-additional-head-track gives a 40 LF delta vs 32.73 LF in R37. |
| BE-51 | FAIL | R28 resilient channel is in LF but sold by "piece", and Pieces = ROUNDUP(LF). |
| BE-55 | FAIL | Internal codes appear in client text: "rev9 verified", "rev4 re-check", "rev8", "rev7", "R73.6", "pass 2 / resolution A vs B", "the other pass". |
| BE-101 | FAIL | Pending Items text contradicts the carried rows (RFI-11, RFI-25). |
| BE-102 | FAIL | A-121 is cited and is not in SHEET_MAP. |
| BE-106 | FAIL | "estimator criterion" has no written source in Inputs C23 and ALC-X28. Pending C16 cites a decision "of the other pass". |

**PASS (33):** BE-02, 03, 04, 05, 06, 08, 10, 11, 14, 15, 20, 21, 22, 23, 24, 25, 28, 29, 42, 43, 49, 52, 53, 54, 57, 58, 100, 103, 104, 105, 107, 110, 111.

**N/A (14 lines):** BE-01, 07, 09, 13, 17, 19, 26, 27, 48 (markups PDF not supplied), 50, 56, 59..98 (one line), 99, 108.

The evidence for every test is in MATRIZ_COBERTURA.xlsx, sheet "Error Library".

## 3. Proportions: FAIL

| Check | Result |
|---|---|
| Board on walls 7,789.50 SF = MS R23 walls 7,198.07 + R24 walls 591.43; every wall = sum of its faces (L x face height), no opening deductions | OK |
| Studs per LF vs O.C.: (ceil(L x 12 / OC) + 1) x H. Ratios 1.00-2.00, with the excess explained by doubled jambs (8/A5.1) and end studs on short walls | OK |
| **Z-furring S21 @ 24": 2,517.5 LF in the Excel vs 2,235.0 LF computed (+12.6 %), no breakdown** | **FAIL** |
| Track vs partition LF: 3-5/8" 219.19, 6" 56.5, 8" 12 (bottom = top + deep-leg 46.84) | OK |
| Z runner = 2 x 288.625 LF | OK |
| Joint compound = 0.072 x 8,126.14 SF; tape = 0.37 x 8,126.14 SF | OK |
| Bracing = (ceil(H x 12 / 48) - 1) x L per wall | OK |

## 4. Markups reconciliation (markups.json vs Excel, by type): FAIL

| Type | Sum Length (markups) | Excel LF | dLF | Sum Wall Area | Excel L x H | dArea |
|---|---|---|---|---|---|---|
| EXT-6CFMF | 48.02 | 48.000 | +0.04 % | 534.54 | 534.89 | -0.07 % |
| EXT-8CFMF | 11.96 | 12.000 | -0.33 % | 247.18 | 248.00 | -0.33 % |
| OTHER FRAMING | 97.31 | 97.418 | -0.11 % | 806.49 | 807.84 | -0.17 % |
| S21 | 288.54 | 288.625 | -0.03 % | 4,238.26 | 4,239.42 | -0.03 % |
| S24 | 37.41 | 37.385 | +0.07 % | 317.98 | 317.77 | +0.07 % |
| **S41** | 6.40 | 6.460 | **-0.93 %** | 76.80 | 77.52 | **-0.93 %** |
| S42 | 122.52 | 122.622 | -0.08 % | 1,295.11 | 1,296.73 | -0.12 % |
| **S43** | 52.45 | 52.729 | **-0.53 %** | 445.83 | 448.20 | **-0.53 %** |
| S61 | 8.52 | 8.500 | +0.24 % | 72.42 | 72.25 | +0.24 % |

The "LF takeoff" data field in markups.json matches the Excel exactly. The drawn geometry of S41 and S43 is outside the 0.5 % tolerance. There are 32 annotations for 32 walls, with 0 without geometry.
