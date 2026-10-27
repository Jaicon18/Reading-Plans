# BACKCHECK rev3 -> rev4 (independent, openpyxl data_only)

Method: cell-by-cell diff of all 7 sheets (same sheet list), then arithmetic re-check of changed rows.

## Changed cells (complete list)
- Partition Takeoff r103 (SS-N soffit side): Board 318.78 -> 227.7 SF (22.77 LF x 10 ft x 1 layer = 227.70). OK, -91.08.
- Material Summary r19 Type X 5/8": 15,670.56 -> 15,579.48 (-91.08). OK.
- r29 FRT 5/8": 2,664.09 -> 2,709.63 (+45.54 = 91.08 - 45.54). OK.
- r30 FRT 3/4": 248.46 -> 353.46 (+105.00). OK.
- r40 screws 20,029.07 -> 19,919.77; r44 compound 1,201.74 -> 1,195.19; r45 tape 6,175.63 -> 6,141.93 (accessories follow board SF 16,599.8; formulas 1.2 / 0.072 / 0.37 re-computed: 19,919.76 / 1,195.19 / 6,141.93). OK (0.01 rounding on screws already present in rev3).
- Pending Items r17 (RFI-14), r19 (RFI-16), r20 (RFI-17): CLOSED, text in English; r30 note updated to 15,579.48.
- _reglas r2: integrity hash/metadata only.
No other quantity cell differs. Partition LF unchanged.

## Arithmetic on changed rows (net x waste% = waste; net + waste = purchase; pieces = ceil(purchase/48))
- Type X: 15,579.48 x 0.06 = 934.7688; purchase 16,514.2488; 344.05 -> 345. OK
- FRT 5/8: 162.5778; 2,872.2078; 59.84 -> 60. OK
- FRT 3/4: 21.2076; 374.6676; 7.81 -> 8. OK
- Accessories: waste 0, purchase = net, pieces = ceil. OK

## Other checks
- No Spanish text found in any cell (accent/keyword regex scan, all sheets). Internal "accesorios.py", "_reglas" names only.
- Note: the source rows for the FRT 5/8 (+45.54) and 3/4 (+105.0) totals are not visible as changes in Partition Takeoff (only r103 changed); they are fed through Material Summary from canon/familias data. Totals tie to the decisions, but line-level traceability of those two adds is not on the Partition sheet.

## Verdict
PASS. Only the intended changes (RFI-14, RFI-16) and board-driven accessory shifts occurred; RFI-17 has no quantity change; RFI-14/16/17 marked CLOSED.
