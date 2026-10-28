# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev13

rev13 = rev12 plus the estimator decisions of 2026-10-28 on the PVC trim / FRP targeted review (`../rev12_pvc_trim/RFI_PVC.md`).
- Rule R80e.30: only the two touched rows were verified.
- Wall LF does not change. The markups were regenerated for rev13 (see "Marked-up plans" below).
- Format: 6 sheets, no new sheets or columns. Waste: metal B5, non-metal B6.

## Changes rev12 → rev13 (Material Summary Net)
| Material | Unit | rev12 | rev13 | Δ | Δ % |
|---|---|---|---|---|---|
| PVC trim (edge / inside / outside corner molding, door edges + FRP division bars every 4') | LF | 530.54 | 887.62 | + 357.08 | + 67.3 % |
| FRP panels | SF | 1,967.38 | 2,001.38 | + 34.00 | + 1.7 % |

All other rows are unchanged.

## Detail (N/SHEET; "estimator decision 2026-10-28" is written in each row's "Where it comes from")
| Item | rev13 | Source |
|---|---|---|
| PVC — Cafe Work Room | 266.44 LF: bottom J-mold 81.22 + top edge 85.22 + inside corners 60.0 + stub outside corners 20.0 + door 3 edges 20.0 | 3/A-225, 1/A-225, 1/A-221, A-500 |
| PVC — Janitor | 84.86 LF: bottom J-mold 16.43 + top edge 19.43 + inside corners 32.0 + door 7 edges 17.0 | 9–12/A-200, A-500 |
| PVC — types 3 / 4, one face | 154.32 LF: bottom J-mold 122.32 + type 3 vertical edges 32.0. The 8 hourglass cap outside corners take the metal corner guard (A-001A), not PVC: − 60.0 | 3/A-410, 4/A-410, 4/A-225 |
| PVC — Cafe below the countertop | 19.0 LF bottom J-mold | 4/A-225, 1/A-225 |
| FRP division bars every 4' | 363.0 LF: Work Room 180 + Janitor 16 + type 3 32 + type 4 135 | A-001A (per manufacturer), 1/A-225, 9/A-200, 3/A-410, 4/A-410 |
| FRP — Cafe Work Room | 875.20 → 852.20 SF (finished perimeter 85.22 LF x 10.0) | 1/A-221 |
| FRP — Cafe below the countertop (C-E1-S) | + 57.0 SF (19.0 x 3.0) | 1/A-225, 4/A-225, 6/A-225 |

Pending Items: the new row **RFI-55** is CLOSED – estimator decision 2026-10-28, with its N/SHEET and the delta applied.

## Marked-up plans (rev13, 2026-10-28)
| File | Content |
|---|---|
| `Planos marcados/Barnes_Noble_ColoradoSprings_FINAL_markups_rev13.pdf` | Bluebeam markups: one PolyLine / Line per Excel row, with /Measure (sheet scale) and /Depth (height). Contents = TYPE · LF · H · SF · N/SHEET · Wall ID, identical to the Excel. Page labels A-101 / A-221 / LEGEND. The legend is titled "rev13 2026-10-28" |
| `Planos marcados/A-101_partitions_by_type_rev13.png`, `A-221_partitions_by_type_rev13.png` | Images per sheet, legend in schedule order |

- **Column wraps and soffit sides:** the 9 C25 column wraps (CW-01…CW-09, 72.0 LF, A-101) and the 5 soffit sides (SS-N, SS-E, SS-IN-N, SS-IN-E, SS-GG, 65.31 LF, A-221) now carry their own Subject, color and legend entry: "OTHER FRAMING - COLUMN WRAP" and "OTHER FRAMING - SOFFIT SIDE". Before, they were drawn under the generic "OTHER FRAMING".
- **Balance markup = Partition Takeoff, 100 %:**
  - all 17 partition types match, for a total of 569.81 LF; type I is 4.51 vs 4.516 because of rounding;
  - column wrap 72.00 = 72.00;
  - soffit side 65.31 = 65.31;
  - 77 quantity annotations = 707.12 LF;
  - every Excel Wall ID is present.
  The 17 existing-wall exclusion marks (RFI-01) are separate and carry no measure.
- **Excel:** the rebuilt file differs from the back-checked one only in the hidden `_reglas` seal; no visible cell changed (addendum in BACKCHECK_rev13.md).
- **rev9 files:** the rev9 copies in this rev13 folder were replaced (local only; nothing deleted in Drive).

## Error library
Independent back-check of the final Excel: **PASS WITH COMMENTS — LIBRARY 44 PASS · 0 FAIL · 3 N/A** (full library). See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev13.md`.
- Only R37 (FRP) and R58 (PVC) differ from rev12.
- The first pass had 1 FAIL, BE-47: RFI-13 and RFI-22 still showed the old figures. Both now end with "Revised by RFI-55".
- The 6/A-225 citation ("3'-0" AFF TO COUNTERTOP") is backed by `../rev12_pvc_trim/05_6-A-225_countertop_3-0_AFF.png`.

## Gates
- REGLAS OK (820 rules, 0 failures)
- ALCANCES OK (24 reviewed, 2 RFI)
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK (17 mandatory tools current + back-check)

Drive: not uploaded. Nothing sent to the client.
