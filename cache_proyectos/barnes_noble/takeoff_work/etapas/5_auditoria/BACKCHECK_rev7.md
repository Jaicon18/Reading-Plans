VERDICT: PASS WITH COMMENTS

# Back-check rev7: Barnes & Noble Colorado Springs, metal frame & drywall
Date: 2026-10-27. Compared `..._FINAL_rev7.xlsx` against `..._FINAL_rev6.xlsx`, PASO12_rev6 (certificate + MATRIZ_COBERTURA, 57 GAP/CORREGIR rows) and BIBLIOTECA_ERRORES.
Bid set re-read: A-410 (page 27). Bubble 3 is the "Top Track Detail" and the type 2 head bubble points to 3/A-410. I also checked the evidence crops for 6/A-226A (15'-0") and 1/A-221 (19'-0" HOLD).
Every quantity change matches its source. All 57 matrix rows have a destination. The comments below are text and traceability defects with no effect on the Net, except C3 and C6, which are small undercounts.

## 1. CORREGIR C-01..C-09
| ID | Status | Evidence in rev7 |
|---|---|---|
| C-01 | OK | RFI-34 CLOSED at T.O. WD-1 15'-0". SS-GG Type X 61.67 SF (6.167 x 10) in MS R20 and in Partition Takeoff R109. FRT plywood stays at 110.49 |
| C-02 | PARTIAL | RFI-13 text and delta corrected (875.20 + 155.44 = 1,030.64 SF). **MS R44 (PVC trim) still says "no FRP height / extent printed for partitions"**. The certificate listed this row (rev6 R37) |
| C-03 | OK | RFI-12 cites 22/A-201. +50.04 SF cement board (RESTROOM-BASE-CEMENT) and -50.04 SF W.R. (RESTROOM-BASE-WR-DEDUCT). Plausible: about 49.5 LF of new restroom faces x 1.167, less doors 8 and 9; the certificate's upper bound was 68.4 |
| C-04 | OK | C-E1-S cement board 19 x 25 = 475.0 SF (-111.5) in MS R33 and Partition Takeoff R68. The FIRESTOP C-E1-S line also uses 19 |
| C-05 | PARTIAL | ALC-24 is QUANTIFIED and quotes A-001A Div 09 A.8. **Inputs!C23 still reads "level 4 (estimator criterion)"**; the fix asked for "level 4 per A-001A Div 09 A.8" |
| C-06 | OK | No "6/A-210" remains. Rows R10, R12 and R14 cite 8/A-210 and 7/A-210 |
| C-07 | OK, with text defects | No "8/A-410" remains where the top track is meant. The 8/A-410 citations left are all cross members / Typ. Connection (R11, R12, RFI-41, ALC-04). The global replace damaged the change history: **RFI-04 says "Citation corrected ... (rev0-rev2 said 3/A-410)"** and **RFI-35 says "citation corrected from 3/A-410"**; both should say 8/A-410. RFI-04 also drops a word from the quote: the plan prints "...TO STRUCTURE **ABOVE** (TYP.)" |
| C-08 | OK | MS R40 and RFI-ACC-stud-reinforcement-mep mark the delta "skill default, not printed: 6/A-410 and 7/A-410 are pipe firestopping only". Quantity stays 0. N/SHEET still lists 6/ and 7/A-410 (acceptable as "checked") |
| C-09 | OK | Door 4 label moved to W2-04 and removed from W2-05. Board and stud LF unchanged, as the matrix said |

## 2. Matrix destinations (57 GAP/CORREGIR rows)
**No row is left without a destination.** Mapping by matrix #:
- #7, #51 Unistrut / strut channel: ALC-X27 EXCLUDED with reason.
- #20: ALC-24 (see C-05).
- #48, #148, #149, #432 ACT: ALC-X26 EXCLUDED, by the ACT contractor (A-002).
- #53 seismic bracing: ALC-X29 plus RFI-38.
- #54, #74, #110, #115 FE cabinets: RFI-39 plus BLK-FE-CABINETS 16 LF.
- #61 base caulk: ALC-X28 EXCLUDED as a sealant.
- #143 tie wire: ALC-12 note ("consumable ... no separate row").
- #145 fixture hangers: HANGERS-FIXTURES 401 LF (see C3).
- #147 splay wires: RFI-38 plus 743.29 LF of splay wire and 131.42 LF of 1-5/8" posts.
- #154 Grab & Go ceiling: 25.16 SF, plus track, furring, carrying channel and hangers.
- #170, #283: RFI-13. #191: RFI-12 plus rows. #199, #200: VEST-GWB-BANDS 14.96 SF (13.33 + 1.63).
- #203: C-06. #204: CLIP-ANGLES-7-A210 4 plus RFI-51. #225: C-04. #226: RFI-45. #230: E2 at 10.5 ft plus RFI-43 (E1).
- #232: RFI-46 plus 6.52 LF. #237: RFI-44. #238: H3b +104.89 SF. #246: SS-N/SS-E plywood to deck (+328.9 SF). #247: RFI-42 plus 90 LF.
- #260: RFI-13 (substrate conflict). #262, #266: RFI-47. #279: C-01. #297: RFI-03.
- #315: ALC-02 exclusion plus RFI-01 text (see C10).
- #317-#320, #344 gauge: gauge on every Partition Takeoff row, and MS split by gauge. #318: RFI-04 extended, DIAG-BRACES-CAFE 44 LF, Cafe walls at 14 ga.
- #333: X-EDNI row. #334: plywood screws row. #349: clip angles row. #352: nested runner plus RFI-40. #355: C-07.
- #357: RFI-41 plus 705 LF of cross members. #361: C-08. #372: RFI-01 plus ALC-X30. #373: RFI-48.
- #387: C-09. #400: RFI-49 plus 17 LF wood blocking. #421: CORNER-BEAD-SOFFITS 65.31 LF. #445, #454: RFI-50 plus SERVER-ROOM-BACKBOARD 32 SF.

## 3. Material Summary Net diff, rev6 to rev7 (every change reconciles)
| Row | rev6 -> rev7 | Delta check |
|---|---|---|
| 6" stud | 3,007.5 -> 3,162.5 | +155 cross members (6") |
| 3-5/8" stud | 10,788.75 -> 11,479.27 | +44 Cafe braces + 550 cross members + 90 soffit cross bracing + 6.52 nested = 690.52 OK |
| 1-5/8" stud (new) | 131.42 | Groups x drop: 16 + 16 + 13.5 + 16 + 4 x 13 + 17.917 = 131.42 OK |
| Ceiling track / furring / carrying | +20.49 / +24.66 / +12.24 | Grab & Go ceiling OK |
| Hanger wire | 1,438 -> 2,689.79 | +107.5 G&G (6 x 17.917) + 401 fixtures + 743.29 splay = 1,251.79 OK. Splay recomputes to 131.42 x 4 x 1.414 = 743.42 (0.13 rounding) |
| Hanger count | 103 -> 109 | +6 G&G |
| FRT 2x blocking | 552.27 -> 568.27 | +16 FE cabinets (4 x 4.0) OK |
| 5/8" Type X | 14,902.61 -> 15,109.29 | +61.67 SS-GG + 25.16 G&G ceiling (4.08 x 6.167) + 14.96 vestibule bands + 104.89 H3b (6.17 x 17) = 206.68 OK |
| Type X W.R. | 1,142.63 -> 1,092.59 | -50.04 restroom base OK |
| Cement board | 851.4 -> 789.94 | -111.5 (C-E1-S at 19'-0") + 50.04 = -61.46 OK |
| FRT 5/8" | 1,886.46 -> 1,790.51 | E2 29.3 x 10.5 = 307.65 (-424.85); SS-N 22.77 x 14 = 318.78 and SS-E 10.12 x 14 = 141.68 (+328.9); total -95.95 OK |
| FRT 3/4" | 370.46 -> 402.46 | +32 server room backboard (4x8) |
| Metal trim | 891.72 -> 957.03 | +65.31 soffit corner bead OK |
| Clip angles (new) | 2,522 | 5/A-410 bracing rows x studs, which I re-derived independently as 2,518, plus 4 (7/A-210) OK |
| X-EDNI (new) | 720 | 479.85 x 2 / 1.333 = 719.8 -> 720 OK |
| Plywood screws (new) | 2,331 | 2,192.97 SF x 34/32 = 2,330.03 -> 2,331 OK |
| Cement board screws (new) | 1,686 | 789.94 x 32/15 = 1,685.2 -> 1,686 OK |
| Nested runner (new) | 479.85 | The 32-term list sums to 479.847 OK |
| Wood blocking, not FRT (new) | 17 | One cased opening (RFI-49) |
| Drywall screws / compound / tape | updated | 1.2, 0.072 and 0.37 x 16,201.9 SF (Type X + W.R.) OK |

## 4. Error library re-run
- **BE-08: PASS.** C-01, C-02 and C-04 values match the print. Residual stale text: see C-02 above.
- **BE-12: PASS with comments.** The C-06, C-07 and C-08 citations are fixed. The new quotes (3/A-410 runner and fire-stop notes, 5/A-410 clip, notes 8.C and 8.D, 5/A-121 post, 22/A-201, 2/E-103, A-413, 5/A-225, 10/A-225, F/H/2/A-221, A-410 "BY FUTURE TENANT") match the plan or the matrix crops. Exceptions: RFI-04 drops "ABOVE", and note 8.D is printed "FILED" (quoted as "FIELD").
- **BE-13: PASS.** 2/E-103 goes to the MS FRT 3/4" row (32 SF) with RFI-50 (delta -32 SF if electrical). E-301 is cross-referenced.
- **BE-40: PASS.** All 51 rows carry N/SHEET plus a breakdown or operation that reproduces the Net within 0.1. R34 (soffit joists, 13 x 4.716 = 61.31) and the FIRESTOP per-wall lines (sum 264.21) are now present. Defect: **the R27 operation text is cut off mid-list at "CW-05"**; the 2,518 still reproduces.
- **BE-41: PASS.** No file or folder names appear in any visible sheet. AUDITORIA_rev4 and ri07_rcp/ are gone; reglas.py appears only in the hidden _reglas sheet. Cosmetic: process labels "Paso 12 (rev7)", "images 12-14" (RFI-37), "canon constants" (Inputs) and "PT0037" (W4-31). Removing ri07_rcp/ also cut RFI-06 C9 short: "Applied (faces already at these heights in rev2;."

## 5. Gauges in Partition Takeoff vs the A-410 Metal Stud Schedule: PASS
Every row carries a gauge.
- Type 2, H2a, H2b and F are 3-5/8" 14 ga SJ. The schedule maximum is 22'-0", below the 25'-0" height; the exceedance is handled by the RFI-04 decision and the 3/A-410 diagonal bracing.
- Type 5 and the 6" Cafe walls are 6" 20 ga SJ, within the 26'-8" limit.
- Types 3/4, counters, column wraps and soffit sides are 3-5/8" 20 ga, with a maximum height of 14 ft against the 17'-11" limit.
- SS-GG is 6" 20 ga SJ at 17.9 ft.
- The minimum-20-ga note is respected.
- MS track gauge matches the studs: 14 ga 295.95 LF and 20 ga 154.07 LF. The 14 ga split totals 7,257 = 6,656 + 601.

## Comments (fix in rev8; none changes the Net except C3 and C6)
- C1. Text-only fixes:
  - Inputs!C23 (C-05).
  - MS R44 FRP wording (C-02).
  - RFI-04 and RFI-35 history ("said 8/A-410"); RFI-04 quote ("ABOVE").
  - RFI-06 C9 cut-off sentence.
  - The cut-off R27 operation text.
- C2. Stale narratives:
  - RFI-11: the components sum to 1,142.63, not 1,092.59.
  - RFI-27: the components sum to 15,094.33, not 15,109.29.
  - ALC-11: 981.38 is not equal to 884.24 + 122.30.
  - ALC-12 says "103 pcs"; the row now has 109.
  - ALC-16 and RFI-23 say "585.27 LF"; MS has 568.27.
- C3. The 401 LF of fixture hangers equals restrooms 8 x 16 + cloud 21 x 13. The D4 fixtures in the Cafe GWB bands (about 20 by the matrix) are neither counted nor sent to an RFI. The hanger count row (109 PCS) leaves out the 29 fixture hangers and the 36 splay wires.
- C4. Framing screws still use 781 stud pieces. rev7 adds about 181 pieces (141 cross members, 11 braces, about 18 soffit braces, 2 nested, 9 posts), so the row is about 724 screws short.
- C5. Mixed rows:
  - The clip angle row combines 2x2 clips (5/A-410) and 3x3 clips (7/A-210).
  - The cement board row combines 1/2" (E1) and 5/8" (22/A-201).
  - Cement board screws assume 3x5 boards, while the sheet count uses 4x12.
- C6. Note 8.F on A-410 reads "STEEL STUDS OR TRACKS TO CONCRETE: 0.145" HILTI X-DNI ... 2 ROWS AT 16" O.C.". RFI-ACC-slab-pins models a single row at 16" (-160 pcs). Two rows at 16" would be about 961 pcs (+321 against the 640.61 carried). Add this alternative to the RFI.
- C7. Rows with no gauge stated:
  - Elements marked "gauge in their operation" give none: cross members 705 LF, soffit cross bracing 90 LF, vestibule posts 126 LF, nested bracing 6.52 LF.
  - The 8" stud row says "(all gauges)".
  - Partition Takeoff writes "20 ga" without ST/SJ; both are within the schedule limits.
- C8. Scope Checklist has the ID ALC-X30 twice. C-E1-S shows a fractional Layers value of 0.81.
- C9. VEST-GWB-BANDS is carried on V.I.F. heights with no RFI. The matrix suggested a V.I.F. note.
- C10. Matrix #315 ("BY FUTURE TENANT"): rev7 excludes it inside RFI-01. The certificate asked for the upper-bound delta (about 10,436 SF Type X). Add it to RFI-01 or ALC-02.

## Resolution of the comments (applied in the same rev7)
- C-05: Inputs!C23 note now cites A-001A Div 09 A.8 "LEVEL 4 FINISH" (template accepts a project note per input).
- C-02: the FRP / PVC trim row reason now gives the printed heights (10'-0" A-226B, 96" A-131 / 8'-0" A-200).
- C-07 text: RFI-04 and RFI-35 rewritten (citation history explicit; quote "TO STRUCTURE ABOVE (TYP.)").
- BE-40: the clip-angle row prints the full rows x studs operation (no truncation).
- BE-41: RFI-06 note restored without the folder name.
- Undercounts: Cafe-band fixture hangers -> RFI-53; framing screws of detail members (+724) and A-410 note 8.F pins (+321) -> stated in RFI-51 with delta.
- Narratives: RFI-11, RFI-27, ALC-11, ALC-12, ALC-16 / RFI-23 rewritten with the rev7 totals; cross members state 20 ga; Scope Checklist IDs unique (ALC-X40..X44).
- rev8 items done now: RFI-01 carries the 10,436 SF upper bound for the "BY FUTURE TENANT" board; vestibule bands V.I.F. -> RFI-52.
- Mixed-size rows (2x2 / 3x3 clips; 1/2" / 5/8" cement board) kept as one row by template family, each size listed in its breakdown.
