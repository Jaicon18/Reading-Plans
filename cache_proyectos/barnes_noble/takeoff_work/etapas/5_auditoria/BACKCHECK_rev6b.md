VERDICT: PASS WITH COMMENTS

# Back-check rev6b: RFI-37, 5/8" FRT plywood removed from the Sales face of C-H1-N and the Cafe face of C-H2a

Scope: Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev6.xlsx compared with rev5. I read the bid set directly (bidset_SIN_MARKUPS.pdf, rendered crops).

## 1. Drawings: are the Sales / Cafe faces plywood?
- Section G/A-221 (p.14): the SALES FLOOR side shows one layer with the gypsum stipple ("5/8" GYPSUM BOARD"). The CAFE WORK ROOM side shows one layer with the plywood cross-hatch. The "5/8" FRT PLYWOOD" leader crosses the wall to the Work Room face. Note: "H2a = 5/8" GWB, 5/8" FRT PLYWOOD" has two leaders, one to each face, so it means GWB on one side and plywood on the other. It does not mean two layers on the Sales/Cafe side. "H2b = 5/8" FRT BOTH SIDES (CAFE WORK ROOM ONLY)" applies only to the stub wall. CONFIRMED.
- A-510 (p.32), room 101 Sales Area: walls = PAINTED GYP. BD. only, with remark "PAINT WALLS PT-2". CONFIRMED.
- 1/A-225 (p.19): the Cafe face of C-H2a is tagged PT-3 / B-2 BASE. A WD-1 leader points only to the short return at the south end of the wall. CONFIRMED.
- 5/A-226A (p.20): PT-3 around door 3, with PT-1 above. WD-1 is a narrow edge strip left of the door, between TL-4 and PT-3, which matches the type I return C-I-P.1 (already carried as C-I-P.1-A-FRT 15.0 SF). The full-height WD-1 field on the right is the type I / E2 face, not C-H2a. CONFIRMED.
- Conclusion: neither face carries plywood. The removal is correct.

## 2. Arithmetic
- C-H1-N Sales face: 25.90 x 25.0 = 647.50. C-H2a Cafe face: 12.17 x 25.0 = 304.25. Total 951.75. OK.
- Material Summary C29: 2,838.21 - 951.75 = 1,886.46. OK (rev6 = 1,886.46). Waste 6% = 113.19, purchase 1,999.65, 42 sheets (was 63). OK.
- Board total = Type X 14,902.61 (unchanged) + Type X W.R. 1,142.63 = 16,045.24 SF.
  - Screws: 1.2 x 16,045.24 = 19,254.29. OK.
  - Compound: 0.072 x 16,045.24 = 1,155.26. OK.
  - Tape: 0.37 x 16,045.24 = 5,936.74. OK.
  - The plywood is not part of the board driver, so these rows are unaffected by RFI-37, as they should be.
- Partition Takeoff: C-H1-N board 993.23 -> 678.44 (647.50 + 30.94 Grab & Go), and C-H2a 432.03 -> 304.25. The removed amounts are the W.R. faces from the earlier rev6 change. The GWB on the Sales / Cafe faces is unchanged. OK.

## 3. Material Summary I29 breakdown
- C-H1-N-A-FRT and C-H2a-B-FRT are gone. 16 items remain, including C-H1-N-B 314.79 and C-H2a-A 127.78 on the Work Room faces.
- The items sum to 1,886.43, and the text states "= 1,886.43". Net is 1,886.46.
- The 0.03 SF difference comes from rounding the items and was already there before this change (rev5: text 2,838.18 vs Net 2,838.21). Not material.

## 4. Pending Items RFI-37 (row 40)
- B40: CLOSED - resolved from the plan (rev6). It cites G/A-221, A-510 101, 1/A-225, 5/A-226A and C-I-P.1, which matches what I read.
- C40: "-951.75 SF ... 647.50 + 304.25 ... GWB on those faces unchanged". Correct.
- The evidence images 12-14 exist in investigacion_WR_FRT/.
- Scope Checklist D11 updated to 1,886.46 SF. OK.

## Comments (non-blocking)
1. Partition Takeoff I51 (C-H2a): the "Board by face" text was dropped completely. The board SF of 304.25 is still there, but it no longer says which face it is on. Restore "Board by face: B Cafe 103 12.17 x 25 ft (5/8 type X)".
2. I29 text total (1,886.43) and Net (1,886.46) differ by 0.03 SF from rounding. Consider matching the text total to Net or adding a rounding note.
3. C29 is a hardcoded value, not a formula, so it will not update if the breakdown changes. Same as before.

## Resolution of the comments (same rev6)
- Partition Takeoff C-H2a: the row now carries "Board by face" whenever the canon has a faces note (trazabilidad.py, R80e.24 extended), so it states the remaining face B Cafe 103 12.17 x 25 ft and why the Work Room side has no gypsum.
- 0.03 SF breakdown gap: rounding of the strip items (each to 0.01), inside the 0.05 tolerance - accepted.
- Material Summary Net values are typed by the template (the Net comes from the canon family); the breakdown text is the audit trail - by design.
