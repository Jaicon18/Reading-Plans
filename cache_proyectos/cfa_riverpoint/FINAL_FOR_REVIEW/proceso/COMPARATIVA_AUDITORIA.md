# Audit Comparison - CFA #2284 River Point

Images are in this folder (`proceso/`). Δ is the auditor value minus the take-off value.

| # | Item | Take-off value | Auditor value | Delta | N/SHEET | Image | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | W6-04-KIT length (both faces, 1.5 ft) | 2.32 LF / 6.95 SF | 2.229 LF (printed 2'-2 3/4") / 6.69 SF | -0.091 LF (-4.1 %) / -0.26 SF | A-202 | w604.png | Use the printed dimension: 2.229 LF and 6.69 SF of cement board. |
| 2 | Z-furring description (Material Summary row 8) | 1-1/2" Z-furring channel | 2" metal Z channel | Size | M2.1 schedule A-202; A1/A-605 | chk3_A605_bracing.png | Rename the row to 2" Z channel. Quantity stays at 96 LF. |
| 3 | C.R. channel bracing on M2.1 / M3.5 / MB-01 | 56.79 LF (part of 107.66) | 0 LF (no detail shows it on furring or sistered studs) | -56.79 LF C.R. channel (-4 sticks of 16 ft after waste) | A1/A-605, A2/A-605, C2/S-801; C09111 3.2.C is suspension sway-bracing only | chk3_A605_bracing.png, s801_C2.png | Remove it, or keep it as an RFI. On MB-01, replace it with 362S162-33 kicker braces @ 48" per C2/S-801 (2 pcs; length per the brace schedule). |
| 4 | Soffit cross brace 3-5/8" @ 32" O.C. | 0 | about 14 pcs (serving soffit about 10, gathering table 4); about 42 LF at about 3 ft each | about +42 LF 3-5/8" stud (+15 % waste); final length per RFI-15 | C4/A-624; C1/S-801 (362S162-33 @ 32" O.C.) | c4_a624.png, s801_C1.png | Add a row and tie its length to RFI-15. |
| 5 | Ceiling board type (Material Summary row 15) | 5/8" gypsum board, regular | 5/8" Ceiling Type (sag-resistant) | Product | C09250 §2.1.E, §3.2.A.3 / A-909 | - | Relabel the row. 332.06 SF is unchanged. |
| 6 | Row 9 merged M3.5-01 + MB-01 | 10.479 LF, H 10.614, layers 1.32, 121.7 SF | 2 rows: 7.15 LF x 10.667 (8") and 3.33 LF x 10.667 (3-5/8", C.1/A-202) | MB-01 height +0.167 ft (+1.6 %); +0.6 LF stud | A-202 C.1; A2/A-605; C2/S-801 | chk2_M35_W8.png | Split into one row per wall. Show board by face. |
| 7 | 1/2" gyp traceability | 1,583.66 SF; I16 breakdown cut off after 3 items | 1,483.64 SF traceable + about 100 SF soffit bottoms (estimate 96-100) | 0 to -4 SF (not verifiable) | C4/A-624; A-221 | srv_soffit.png | Add soffit-bottom rows to the Partition Takeoff and restore the full I16 breakdown. |
| 8 | Workbook sheets | 7 (hidden `_reglas`, in Spanish) | 6 | +1 sheet | format rule | - | Delete `_reglas`. |
| 9 | OTHER FRAMING block subtotal | missing | SUBTOTAL row: 73.44 LF / 78.06 SF | - | Partition Takeoff rows 15-22 | - | Add the subtotal row. |
| 10 | RFI cross-reference, kitchen base height | "-> RFI-02" (rows 33-40) | RFI-03 (closed) | Label | A-050 KN16 / A.4/A-621 | - | Fix the reference. Also fix Review item 6/8 to say "A 8"". |
| 11 | Bluebeam Page Labels, demo pages | "6", "7" | A-050, A-052 | Label | A-050 p6, A-052 p7 | chk7_markups_A202.png | Set the page labels to the sheet numbers. |
| 12 | Bluebeam DEMO Contents | "DERIVADO" / "PENDIENTE" | English (DERIVED / PENDING) | Language | - | - | Translate. |
| 13 | Bluebeam SF, metal walls | M2.1 151.1, M3.5-01 76.2, M3.5-02 40.0 | Excel board SF 148.75, 75.03, 39.38 | +2.35, +1.17, +0.62 SF (markup vs Excel) | A1/A-605 G.4 (board to 4" above ceiling) | chk7_markups_A202.png | Make the markup SF equal the Excel board SF, or label it "framing SF". |
| 14 | Bluebeam MB-01 Subject | M3.5 | Untagged 3-5/8" infill (RFI-17) | Label | A-202 / A-050 KN1 | chk1_tags_A202.png | Change the Subject to "INFILL 3-5/8 (untagged)". |
| 15 | Items without markups | none | CLG x5 (332.06 SF), soffit bottoms (about 100 SF), Level 5 (731.2 SF), roof-hatch shaft, pin-and-sleeve recess | - | A-221, S-241, A1/A-604, A2/A-605 | - | Add area or count markups. |
| 16 | J-trim at play-area / dining cement board | 0 | Printed on A2/A-624 | Not quantified | A2/A-624 | - | RFI: confirm whether it is drywall trim scope. |
| 17 | Restroom existing-wall board removal (KN10) | 0 SF demo | 617 SF of new cement board loaded on existing walls | Possible demo of about 617 SF | A-050 KN10; A-611 | - | RFI: confirm whether the existing board is removed or the cement board goes over it. |
