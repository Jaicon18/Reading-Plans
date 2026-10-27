# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev10

rev10 = rev9 with the 3 form fixes from the targeted rev9 check (`../PASO12_rev9_dirigida/VERIFICACION.md`).
- No quantity changes: every Material Summary Net and every "Pieces to buy" is the same as rev9.
- Rule R80e.30: only the changed items and tests BE-46, BE-47 and BE-51 were re-run.
- The markups PDF and the images are the rev9 ones (`Planos marcados/`, copied unchanged).

## Files
| Folder | File |
|---|---|
| Take-off/ | `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev10.xlsx` (6 sheets, formulas recalculated) |
| Planos marcados/ | rev9 markups PDF and images (no geometry change) |

## Changes rev9 → rev10 (form only)
| Item | rev9 | rev10 |
|---|---|---|
| C8-04 — MS A37 | Track 3-5/8" 281.09 LF, no gauge | Name carries the gauge: 14 ga 157.81 + 16 ga 5.00 + 20 ga 118.28 LF (track gauge = stud gauge, A-410 schedule note 2; 8/A-210 "3 5/8"x16 GA") |
| C8-04 — MS A38 | Track 6" 144.06 LF, no gauge | 16 ga 25.33 + 20 ga 118.73 LF (8/A-210 "6"x16 GA TOP & BOTTOM TRACK") |
| C8-04 — MS A39 | 8" ledger 12.67 LF | "gauge not printed, RFI-54". RFI-54 adds the ledger: 4/A-210 prints "8" LEDGER" with no gauge; no LF change |
| C8-05 — MS H18, H22–H25, H42 | Stock length typed in the formula (/8, /12, /4, /12) | Formulas point to the new Inputs cells B26 (2x lumber 8 ft), B27 (main tee 12 ft), B28 (cross tee 4 ft), B29 (molding 12 ft). Pieces unchanged |
| C8-08 — MS I55 | "partition walls 673" as one number | Per-wall list of the 485 light pieces: 377 on the 25/20 ga walls + 108 on the column wraps (CW-01…CW-09) |
| Optional | — | I56 cites "A-410 note 8.F (9/A-410 = alternate)"; G45 selling unit "each"; Pending Items B49 "estimator decision 2026-10-26" |

## Error library (BE-46, BE-47, BE-51)
Targeted back-check of the rev10 Excel: **PASS WITH COMMENTS — 3 PASS · 0 FAIL · 0 N/A** (BE-46, BE-47, BE-51). Nets and pieces match rev9 exactly; the internal-name scan is clean. See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev10.md`. The full library run on rev9 stays valid (43 PASS · 0 FAIL · 3 N/A), because no quantity changed.

Open non-blocking comments (for estimator review):
- Rows A37 and A38 hold more than one gauge in one row; the buyer splits them by the figures in the name.
- Revision history tags "(revN):" remain in some Pending Items notes.
- The nested-column track is 5 LF; it may be up to 126 LF (inherited).

## Gates
- REGLAS OK (815 rules, 0 failures)
- ALCANCES OK (24 reviewed, 2 RFI)
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK (17 mandatory tools current + back-check)

Skill **v80q**: rule R80e.32 (gauge per split row, stock lengths in Inputs, per-wall piece list, yield citation), in `take-off-metal-frame-drywall_FINAL_v80q.zip` at the repo root.

Drive: not uploaded. Nothing sent to the client.
