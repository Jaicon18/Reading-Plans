# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev4

rev4 = rev3 + the estimator's answers to the last 3 open RFIs ("Open RFIs answered by estimator" in `DECISIONES_ESTIMADOR.md`). Earlier revisions are unchanged.

There is no geometry change, so markups and images stay as in rev3 (`FINAL_FOR_REVIEW_2026-10-24_rev3/Planos marcados/`, `_v2` images).

## Changes (rev3 → rev4)
| Item | rev3 | rev4 | Decision |
|---|---|---|---|
| North soffit face SS-N, 5/8" FRT plywood behind WD-1 | 45.54 SF (9'-0" to 11'-0") | 91.08 SF (11'-0" to 15'-0") | RFI-14: soffit 11'-0" (A-121 governs); WD-1 top 15'-0" as the east face (6/A-226A) |
| SS-N GWB height | 14 ft | 10 ft (15'-0" to deck) | RFI-14 |
| 5/8" Type X | 15,579.48 + 91.08 = 15,670.56 SF | 15,579.48 SF | RFI-14 |
| FRT plywood 5/8" | 2,664.09 SF | 2,709.63 SF | RFI-14 |
| FRT plywood 3/4" | 248.46 SF | 353.46 SF | RFI-16: vestibule posts 6 x 4 faces x 5" x 10.5 ft = 105.0 SF |
| C25 stud spacing | 16" | 16" (no change) | RFI-17 |
| Drywall screws / joint compound / joint tape | 20,029.07 / 1,201.74 / 6,175.63 | 19,919.77 / 1,195.19 / 6,141.93 | follow the board |

The partition total does not change: **568.61 LF**. RFI-14, RFI-16 and RFI-17 are CLOSED in Pending Items.

## Gates
- `reglas.py`: OK. `alcances.py`: OK. `registro.py entregable`: OK. `etapas.py`: PASA.
- `bitacora.py compuerta`: BITACORA OK.
- Back-check rev4: PASS (`takeoff_work/etapas/5_auditoria/BACKCHECK_rev4.md`).
