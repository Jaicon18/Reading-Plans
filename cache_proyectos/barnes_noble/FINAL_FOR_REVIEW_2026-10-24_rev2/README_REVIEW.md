# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev2

rev2 = rev1 + estimator decisions of 2026-10-25 (end of `DECISIONES_ESTIMADOR.md`). rev1 is unchanged in `FINAL_FOR_REVIEW_2026-10-24_rev1/`.
Markups did not change: the geometry and LF are the same, so use the rev1 PDF in `FINAL_FOR_REVIEW_2026-10-24_rev1/Planos marcados/`.

## Changes (rev1 → rev2)
| Item | rev1 | rev2 |
|---|---|---|
| 5/8" gyp board regular (GWB ceilings, 4/A-121, 5/A-121) | 981.38 SF | 0 (row removed) |
| 5/8" gyp board Type X | 14,557.36 SF | 15,538.74 SF (walls 14,557.36 + ceilings 981.38) |
| 3/4" FRT plywood, restroom backing (21/A-201) | 13.33 SF (12" high, assumed) | 17.77 SF (10 pcs x 16" bay x 16" high) |
| 3/4" FRT plywood total | 137.40 SF | 141.84 SF |
| FRT plywood (5/8" + 3/4") | 2,665.82 SF | 2,670.26 SF |

The backing comes out to 17.77 SF from 13.33 LF x 16/12. The decision's 17.78 uses 13.333, so the difference is 0.01 SF of rounding.
Partition LF did not change: **562.44 LF**.

## Text answers (in the Excel: Pending Items RFI-01 / RFI-23 / RFI-27, Scope Checklist)
- The break room kitchenette W.R. sits on the existing EXT-07, so it is INSIDE the patch & repair allowance.
- The patch & repair allowance amount stays BLANK (decided).
- The restroom backing height Review Item is closed and removed (11 Review Items).

## Gates
- `reglas.py`: OK. `alcances.py`: OK. `registro.py entregable`: OK. `etapas.py`: PASA.
- `bitacora.py compuerta`: BITACORA OK.
- Back-check rev2: PASS (`takeoff_work/etapas/5_auditoria/BACKCHECK_rev2.md`).
