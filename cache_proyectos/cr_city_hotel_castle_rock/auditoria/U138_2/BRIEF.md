# Auditoría adversarial U-138 #2 — CR City Hotel rev2 (415 Perry St, Castle Rock CO)

You are an independent auditor. You did NOT do this take-off. Your job is to find what is wrong, not to confirm it.
Read only; write ONLY inside `/root/cr/work/auditoria_U138_2/` (report `INFORME_AUDITORIA_U138_2.md`, images in `img/`, your scripts in `tools/`).
Never touch Bidding / Accept / Decline / messages; never read or print credentials.

## Inputs
- Bid set (clean): `/root/cr/work/plans/bidset_SIN_MARKUPS.pdf` (canon `page` is 1-based; PDF index = page - 1).
  Sheet list in `/root/cr/work/set_texto.json` (`hojas` keys in page order) with the text of each sheet.
  Floor plans 1/A2.01 (L1), 1/A2.02 (L2), 1/A2.03 (L3), 1/A2.04 (L4) at 1/8" = 1'-0" (9 pt/ft); enlarged plans A6.xx / A7.xx at 1/4" (18 pt/ft).
  Schedules A0.06 / A0.07 / A0.08; sections A5.xx; RCP A3.01–A3.04; unit plans / elevations A7.00–A7.17.
- Delivered Excel: `/root/cr/work/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev2.xlsx` (6 sheets).
- Canon: `/root/cr/work/etapas/4_canon/takeoff_canon.json` (`existing_walls` = board-only entries, one per face / board; wood framing is EXCLUDED — wood-framed building).
- Markups: `/root/cr/work/etapas/8_excel/CR_City_Hotel_markups_rev2.pdf`.
- Previous audit (#1) and its resolution: `/root/cr/work/auditoria_U138/` — do not repeat it; check whether its fixes hold.
- Independent schedule reading: `/root/cr/work/indep/fichas.json`.

## What to audit (random sample, PER FLOOR L1, L2, L3, L4 — never mix floors in one number)
1. **Walls**: at least 8 random walls per floor. Re-measure LF on the plan at the printed scale (vector lines), compare with the Excel row.
2. **Heights**: for each sampled wall, find the printed source of the height (section / detail, N/SHEET) and check the loaded height and its operation.
3. **BOTH SIDES**: for each sampled wall, does each face carry the board and layers the type prints (A0.06 / A0.07)? Wet areas
   (toilet / lavatory: water-resistant board per A2.0x general note 4; tile at showers: cement board per A0.06 GN 13 and the unit
   elevations A7.xx) — sample at least 3 guest baths per floor including faces on exterior and corridor walls.
4. **Bubbles / details**: for 6 sampled items, follow the bubble chain to its end and confirm the item cites the right N/SHEET.
5. **RFIs**: every open RFI — is it truly not resolved by the drawings? Every closed RFI — is the closure right?
6. **Material Summary**: recompute 4 rows (e.g. Type X, Type X W.R., cement board, Type C ceilings) from the canon entries
   and check the Excel figure; check waste and the GRAND TOTAL of the Partition Takeoff.

## Rules for every number
[CONFIRMADO] printed dimension citing the sheet · [DERIVADO] with its operation · [PENDIENTE] not dimensioned. Never scale by eye.
Every finding: severity (ALTA / MEDIA / BAJA), N/SHEET evidence, a circled image in `img/` (re-open it to verify), estimated delta, proposed action.
Report table first, then detail per finding, then the list of what you checked and found correct.
