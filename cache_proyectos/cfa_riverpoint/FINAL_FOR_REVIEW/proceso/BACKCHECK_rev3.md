# Back-check of rev3 - CFA #2284 River Point, Sheridan, CO

Date: 2026-11-02. Scope: only the 6 defects found in BACKCHECK_rev2.md and the 15 failed rows they cover. The rest of rev2 passed and was not checked again.

Sources:
- the bid set `cfa_work/plano/bidset_CLEAN_SIN_MARKUPS.pdf`
- `Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev3.xlsx`
- `Planos marcados/*_rev3.*`
- `proceso/CAMBIOS_rev3.md`

Drawing evidence is the rev2 back-check crops, which are still valid because the bid set did not change: `/tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_backcheck/`. The new crop is `png221_rev3.png`.

MS = Material Summary; PT = Partition Takeoff; SC = Scope Checklist.

| # | Issue (rev2 failed rows) | rev2 | rev3 | Evidence | Result |
|---|---|---|---|---|---|
| 1 | J trim A2/A-624 (line 14; B audit-4 obs) | 59.69 LF (play-room perimeter), 7 sticks | 30.79 LF (dining face, EX-DIN-03), 4 sticks | A2/A-624 shows the "J" trim on top of the 1/2" cement board on the dining (tile) face (`a624_A2.png`, `a624_A1.png`). PT r31 EX-DIN-03 = 30.79 LF equals MS r30 J-PLAY 30.79, which cites A2/A-624, A1/A-624 and A-202. Purchase = ROUNDUP(30.79 x 1.15 / 10) = 4. | PASS |
| 2 | Setting-type compound at cement board (line 26c; G-04) | note only, not bought | own row: 129.62 lb, waste 0, ROUNDUP pieces | MS r26 "Setting-type joint compound at cement board joints". 0.072 x 1800.27 = 129.62 lb. Cites C09250 2.4.D.2 / 3.5.E (A-909, `spec_C09250_2x.png`, `spec_C09250_35E.png`). | PASS |
| 3 | Mesh tape waste (line 26b; G-04) | 6 %, purchase 706.07 LF | 0 %, purchase 666.10 LF | MS r25 D-col = 0. This matches Inputs C23 / C24 ("Yields carry no waste") and the paper tape row r47. Net 0.37 x 1800.27 = 666.10. | PASS |
| 4a | Ceiling board label (line 11; audit 3c / G-03) | "5/8" gypsum board, regular" | "5/8" gypsum ceiling board, SAG-RESISTANT (ceiling type)", 332.06 SF | MS r19 A-col. Note cites C09250 2.1.E + 3.2.A.3 (`spec_C09250_2x.png`, `spec_C09250_3x.png`). DEMO_CRUCE and the Bluebeam GYP CEILING contents agree. | PASS |
| 4b | Z channel label (audit 3a / G-16) | "1-1/2" Z-furring channel" | "2" Z-furring channel (LF of material)", 96 LF | MS r8 A-col. A1/A-605 prints 2" metal "Z" channel (`a605_A1A2.png`). PT r6 F-col also reads 2". | PASS |
| 5a | Hidden `_reglas` sheet (line 32; audit 6; C) | 7 sheets | 6 sheets | Sheet list: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist. All 6 are visible; no hidden sheet. A scan of every cell finds no "compuerta", "reglas", "DERIVADO" or "PENDIENTE". | PASS |
| 5b | OTHER FRAMING subtotal (line 31; audit 6; C) | none | PT r26 "SUBTOTAL OTHER FRAMING" =SUM(C18:C25) / =SUM(H18:H25) | Evaluates to 73.439 LF / 78.06 SF, which equals the audit target (73.44 / 78.06). | PASS |
| 6a | SC ALC-04 stale text (BE-14) | "3-5/8" MB-01; no deflection track printed" | 6" MB-01 (D3/A-624); D1 braces; C1/S-801 3" long-leg slotted track in its own row; strongback own row | SC D5. Matches MS r5 / r7 / r10 / r15 / r23 and `a624_D3.png`, `s801_D1C1.png`. | PASS |
| 6b | MR rows citing §2.1.B (BE-14) | "§2.1.B (1/2 in standard interior)" | "§2.2.A (water-resistant gypsum backing board)" | PT J51 EX-RRM-01-GB and J55 EX-RRW-01-GB. The remaining §2.1.B citations are all on 1/2" regular rows, which is correct. | PASS |
| 6c | Spec reference on MS rows (line 23) | missing on r17 / r22 / r27 | present on every MS row | Every row 4-51 carries a spec cite: r17 C09111 3.2.C, r22 C09111 2.3, r28 corner bead C09250 2.3. Observation: the r17 cite "C09111 3.2.C bracing of ceiling systems" is weak. That clause reads "Sway-brace suspension systems" (p45), and these ceilings are framed joists, not suspended (SC ALC-12). C09111 3.2.C is also the citation RFI-09 already gives for this row. No quantity effect. | PASS (with observation) |

**Bluebeam / images:** these were not among the defects. They are unchanged from rev2:
- The rev3 PDF has the same 126 annotations, the page labels A-050 / A-052 / A-202 / A-221 and no Spanish text.
- The rev3 A-221 PNG now draws the 5 gyp ceilings, 2 soffit bottoms, Level 5 and the hatch shaft with their take-off labels (`png221_rev3.png`).

**Result:** all 6 issues pass. All 10 lines above pass, and they cover the 15 rows that failed in rev2. The workbook has exactly the 6 fixed sheets.

BACK-CHECK RESULT: PASS
