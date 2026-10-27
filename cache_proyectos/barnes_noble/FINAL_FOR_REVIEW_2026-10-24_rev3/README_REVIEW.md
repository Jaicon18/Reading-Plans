# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev3

rev3 = rev2 + the 11 closed Review Items ("Review Items (rev2 → rev3)" in `DECISIONES_ESTIMADOR.md`), resolved from the drawings. rev1 and rev2 are unchanged.

## Files
- `Take-off/Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev3.xlsx`
- `Planos marcados/Barnes_Noble_ColoradoSprings_FINAL_markups_rev3.pdf`: markups redone because W2-05 and the type 4 geometry changed. Depth = wall height; perimeter walls are "EXISTING - EXCLUDED".
- `Planos marcados/`: images per sheet, the RI evidence crops (ri07 to ri11), and `by_type/`.

## Changes (rev2 → rev3)
| Item | rev2 | rev3 | Source |
|---|---|---|---|
| Partition total | 562.44 LF | **568.61 LF** | |
| Type 2 (W2-05 printed 12'-11") | 273.57 | 278.57 | A-101 (RI 1) |
| Type 4 (curved walls 25.68 each) | 82.47 | 83.64 | 4/A-410, RFI-18 (RI 2) |
| 3-5/8" stud | 10,120.39 LF | 10,831.39 LF | braces 468 (117 x 4, 8/A-410, RI 6) + vestibule posts 126 + W2-05 |
| 8" stud | 0 | 25.33 LF | vestibule box beam 6/A-210 (RI 11) |
| 8" joist (new) | 0 | 88.0 LF | 4/A-210 (RI 11) |
| Bottom / top track | 634.44 each | 640.61 each | W2-05 |
| Bracing C.R. channel | 2,827.81 | 2,858.98 | W2-05 |
| Ceiling / soffit track | 385.99 | 321.78 | cloud −107.21; vestibule +43.0 |
| Furring channel | 493.02 | 182.79 | cloud −310.23 (RI 10) |
| Carrying channel | 341.09 | 146.92 | cloud −194.17 (RI 10) |
| USG main tee DGLW26 | 0 | 194.16 LF | 4/A-121 (RI 10) |
| USG cross tee DGLW424 | 0 | 457.96 LF (124 pcs) | 4/A-121 (RI 10) |
| USG channel molding DGCM27 / angle molding DGWM24 | 0 | 107.21 LF each | 4/A-121 (RI 10) |
| 5/8" Type X | 15,538.74 SF | 15,670.56 SF | vestibule +105.5; W2-05; type I and SS-E GWB above WD-1 |
| 5/8" Type X W.R. | 1,024.02 SF | 1,020.33 SF | W2-05 Women's face 7.51 LF |
| FRT plywood 5/8" | 2,528.42 SF | 2,664.09 SF | type I 49.65 (6/A-226A) + SS-E 40.48 + SS-N 45.54 (RI 8, RI 9) |
| FRT plywood 3/4" | 141.84 SF | 248.46 SF | vestibule 106.6 (4/A-210) |

## Still open
- **RFI-14:** the top of the north "BN CAFE" sign-panel WD-1 is not printed (carried as GWB), and the soffit height is 9'-0" on 1/A-226A vs 11'-0" on A-121.
- **RFI-16:** vestibule post sheathing "AS REQUIRED" (5/A-210).
- **RFI-17:** C25 stud spacing.
- Review Items: none open.

## Notes
- **Citation corrected:** the diagonal bracing is on 8/A-410 Top Track Detail, not 3/A-410.
- **Cloud spacing:** the main tees at 48" and cross tees at 16" are USG standard spacing, not printed (24" alternative = 88 pcs).

## Gates
- `reglas.py`: OK. `alcances.py`: OK. `registro.py entregable`: OK. `etapas.py`: PASA.
- `bitacora.py compuerta`: BITACORA OK.
- Back-check rev3: PASS (`takeoff_work/etapas/5_auditoria/BACKCHECK_rev3.md`).
