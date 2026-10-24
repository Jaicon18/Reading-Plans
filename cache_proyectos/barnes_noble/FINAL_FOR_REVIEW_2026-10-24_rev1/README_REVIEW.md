# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev1

rev1 applies the estimator decisions of 2026-10-24 (`cache_proyectos/barnes_noble/DECISIONES_ESTIMADOR.md`). rev0 is unchanged in `FINAL_FOR_REVIEW_2026-10-24/`.

## Files
| Folder | File |
|---|---|
| Take-off/ | `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev1.xlsx` (6 sheets, formulas recalculated) |
| Planos marcados/ | `Barnes_Noble_ColoradoSprings_FINAL_markups_rev1.pdf`: Bluebeam markups. The perimeter walls are marked Subject **"EXISTING - EXCLUDED"** (gray dashed, not counted). Also: images per sheet, the RFI-01 evidence crops, and `by_type/` |

## Decisions applied
1. **RFI-01: perimeter walls types 1 / 1A / 1B / 1C are EXISTING.**
   - Sources: 1/DM-101 legend + key note 3, A-101 legend, A-002.
   - Framing, track, bracing and 1B sheathing are EXCLUDED (Scope Checklist ALC-02 / ALC-09).
   - Interior face patch & repair = **ALLOWANCE, amount blank**.
   - RFI-02, RFI-07, RFI-10, RFI-25 and RFI-26 become N/A or are merged.
2. **RFI-23: FRT blocking by count.**
   - Blocking 552.27 LF:
     - 7/A-413 — 387.0 LF
     - 8A/A-413 — 69.0 LF
     - 3-4/A-412 — 85.6 LF
     - 6/A-412 — 10.67 LF
   - 3/4" FRT plywood:
     - menu boards 60.61 SF (4/A-226A);
     - restroom backing 13.33 SF (21/A-201; the 12" height is assumed and is a Review Item).
3. **RFI-11: W.R. on every face of Women's 109, Men's 108, Janitor 107 and the alcove corridor faces = 1,024.02 SF.**
   - This is new walls only. The EXT-07 faces and the kitchenette wall are existing.
4. **RFI-27: Type X on all new walls; W.R. faces are Type X W.R.** GWB ceilings stay regular (confirm).

## Partition LF by type (schedule order)
2 273.57 · 5 5.70 · 3 38.68 · 4 82.47 · H1 42.15 · H2a 12.17 · H2b 1.95 · H3a 4.08 · H3b 6.17 · E2 29.30 · E1 27.88 · F 3.26 · I 3.31 · A 20.27 · B 3.17 · D 5.14 · C 3.17 — **Total 562.44 LF** (rev0 979.87; −417.43 perimeter).
Other framing is unchanged: C25 surrounds 72 LF and soffit sides 59.14 LF.

## Materials changed (net, rev0 → rev1)
| Material | rev0 | rev1 |
|---|---|---|
| 3-5/8" stud (all) | 16,812.96 LF | 10,120.39 LF |
| 6" stud | 2,925.00 LF | 2,900.00 LF |
| 8" stud | 2,332.99 LF | 0 |
| Bottom track / top deflection track | 1,051.87 LF each | 634.44 LF each |
| Bracing C.R. channel | 5,230.74 LF | 2,827.81 LF |
| 1/2" exterior gyp sheathing | 2,469.22 SF | 0 |
| 5/8" gyp board regular | 16,562.77 SF | 981.38 SF (ceilings) |
| 5/8" gyp board Type X | 0 | 14,557.36 SF |
| 5/8" gyp Type X W.R. | 0 | 1,024.02 SF |
| FRT blocking | 0 | 552.27 LF |
| FRT plywood (5/8" + 3/4") | 2,591.90 SF | 2,665.82 SF (3/4": 63.48 → 137.40) |
| Additional head track | 19.0 LF | 0 (existing doors 12 / 13) |
| Slab pins | 1,051.87 | 634.44 |
| Framing screws | 4,556 | 3,080 |

## Gates
- `reglas.py`: OK. `alcances.py`: OK (24 rows, 2 RFI).
- `registro.py entregable`: OK. `etapas.py`: PASA.
- `bitacora.py compuerta`: BITACORA OK.
- closer: 61 walls sealed. Markups verified.
- Back-check rev1: PASS. See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev1.md`.
