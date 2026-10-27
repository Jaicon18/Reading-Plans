VERDICT: PASS WITH COMMENTS

# Back-check rev5 -> rev6: Barnes & Noble Colorado Springs (metal frame & drywall)
Date: 2026-10-27. Independent check. Sources: rev5/rev6 Excel (all 7 sheets diffed, values and formulas) and bidset_SIN_MARKUPS.pdf (crops rendered and read by eye).

## 1. Section G/A-221 (p.14, Section Wall Typ. H1/H2), read independently
- One board layer each side of the stud, outside the flange (the thin double line is the stud flange, not a board).
- Sales Floor side: 1 layer, stippled (gypsum). Leader "5/8" GYPSUM BOARD" points to it.
- Cafe Work Room side: 1 layer, cross-hatched (wood). Leader "5/8" FRT PLYWOOD" points to it.
- The note "H2a = 5/8" GWB, 5/8" FRT PLYWOOD / H2b = 5/8" FRT BOTH SIDES (CAFE WORK ROOM ONLY)" has two arrows: one to the Sales-side gypsum and one to the Work-Room-side plywood. So H2a = GWB on one face and plywood on the other, not both on each face.
- Other text: "H1 = 6" STUD, H2 = 3 5/8" STUD", "METAL STUDS @ 16" O.C.", "SEE SHEET A-225 FOR FINISH DETAILS", "NOTE: WALL TYPE H2 NO SOUND CONTROL INSULATION".
- Conclusion: the plan shows no gypsum board on the Work Room 104 face. Removing it is supported. RFI-37 (FRT plywood behind GWB on the Sales/Cafe faces) is justified, because G draws no plywood on that side.

## 2. Material Summary diff (only rows 20, 40, 44, 45 changed)
| Row | Item | rev5 | rev6 | Delta | Check |
|---|---|---|---|---|---|
| 20 | 5/8" Type X W.R. net SF | 1,713.00 | 1,142.63 | -570.37 | 29.98x10.5=314.79; 12.17x10.5=127.785 x2; sum 570.36 OK. Breakdown re-added = 1,142.63 OK |
| 20 | purchase / sheets (6%, 48 SF) | 1,815.78 / 38 | 1,211.19 / 26 | | 1,211.19/48=25.2 -> 26 OK |
| 40 | Drywall screws | 19,938.73 | 19,254.29 | -684.44 | 1.2 x (14,902.61+1,142.63=16,045.24) = 19,254.29 OK |
| 44 | Joint compound lb | 1,196.32 | 1,155.26 | -41.06 | 0.072 x 16,045.24 OK |
| 45 | Joint tape LF | 6,147.78 | 5,936.74 | -211.04 | 0.37 x 16,045.24 OK |
- Unchanged, as claimed: Type X 14,902.61; FRT plywood 5/8" 2,838.21 SF (Work Room strips kept); FRT plywood 3/4" 370.46 SF; studs, track, blocking.
- Minor: col J formulas use a rounded driver (=Inputs!B20*16045.2 -> 19,254.24), while col C holds 19,254.29. The 0.05 gap does not change the piece count. Same pattern as rev5.

## 3. Partition Takeoff rows
| Row | Wall | Faces E | Board H rev5 -> rev6 | Delta | Remaining face |
|---|---|---|---|---|---|
| 47 | C-H1-N | 2 -> 1 | 993.23 -> 678.44 | -314.79 | Sales 25.9x25=647.50 + Grab&Go 4.08x7.58=30.93 = 678.43 OK |
| 48 | C-H1-W | 2 -> 1 | 243.39 -> 115.61 | -127.78 | Manager 105 12.17x9.5=115.62 OK |
| 51 | C-H2a | 2 -> 1 | 432.03 -> 304.25 | -127.78 | Cafe 103 12.17x25=304.25 OK |
- Subtotals: H1 1,236.62 -> 794.05 (-442.57); H2a 432.03 -> 304.25; grand total H93 15,458.28 -> 14,887.93 (-570.35). All are live SUM formulas. C-H2b stays at 0 faces (FRT both sides), consistent with G.

## 4. Spot-checks
- A-410 Partition Notes box, note 2 (read on p.27): "PROVIDE WATER RESISTANT GYPSUM BOARD IN ALL BATHROOMS AND JANITOR'S CLOSET FOR WALL AND CEILING CONSTRUCTION." Matches the quote. It supports W.R. on the restroom and janitor walls and on the restroom GWB ceilings, and it does not name the Cafe Work Room.
- 3/A-221 Soffit Section Grab & Go: 6" metal studs @ 16" O.C., "5/8" PRESSURE TREATED FRT PLYWOOD SUBSTRATE" under WD-1, 5/8" GWB above T.O. WD-1 and at the soffit bottom. This supports the FRT plywood on the soffit.
- Not re-read this pass: A-121 GWB 9'-0" ceilings, A-510 room 104 FRP-1, 11/A-200 3/4" plywood. None of these changed in rev6.

## Comments (non-blocking)
1. Pending Items C16 now reads "Cafe Work Room 104 faces 0 LF x FRP height". This is wrong. FRP-1 is still applied in room 104 (over the FRT plywood, per A-510). Only the gypsum board was removed. Restore 54.32 LF (29.98+12.17+12.17).
2. Partition Takeoff I51 dropped the whole "Board by face" note, including the face that remains: "B Cafe 103 12.17 x 25 ft (5/8 type X)". Restore it.
3. Stale labels: Pending Items C30 and Scope Checklist D8 still say "Applied/Quantified (rev5)" but now show the rev6 W.R. figure (1,142.63).
4. RFI-37 amounts check out: 647.50 + 304.25 = 951.75 SF. G/A-221 supports raising it. A-225 finish details could still require the plywood, so leaving the quantity in pending the answer is acceptable.
5. The rev5 Pending Items B14 note (2026-10-24) had cited the A-410 "*" note "KITCHEN" for the Work Room W.R. That note applies to gypsum where gypsum exists, and G shows none on that face. The rev6 reasoning governs.

No other cell changed between rev5 and rev6, apart from the _reglas hash.

## Resolution of the comments (applied after this report, same rev6)
- RFI-13 FRP length: now from the Work Room FRT plywood faces = 87.52 LF (C-H1-N, C-H1-W, C-H2a, C-H2b x 2, C-E2) + Janitor 19.43 LF.
- "(rev5)" labels in RFI-27 / RFI-11 and Scope Checklist ALC-07 / ALC-08: now "(rev6)".
- C-H2a row: its only board face (Cafe 103, 12.17 x 25.0) equals L x H x Layers, so no per-face note is needed (rule R80e.24 writes it only when Board != L x H x Layers).
- Column J yield formulas vs column C: 0.05 rounding on the driver, no change in pieces to buy - accepted.
