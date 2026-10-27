# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev6

rev6 = rev5 + the W.R. / FRT plywood plan check requested by the estimator. Evidence (literal text, N/SHEET, circled crops): `../investigacion_WR_FRT/NOTA_WR_FRT.md` and images 01–11. Earlier revisions are unchanged. There is no geometry change: markups and images stay as in rev5 (`FINAL_FOR_REVIEW_2026-10-24_rev5/Planos marcados/`).

## Result by zone
| Zone | W.R. required? | Source | rev6 |
|---|---|---|---|
| Restroom GWB ceilings, Men's 108 / Women's 109 (122.30 SF) | YES | A-410 Partition Notes 2 "...FOR WALL AND CEILING CONSTRUCTION"; 1/A-121 GWB 9'-0"; A-510 painted gyp bd ceiling; A-001A Div 09 A.4 | kept |
| Restroom / janitor / drinking fountain walls (1,020.33 SF) | YES | A-410 notes 2 and 7, "*" note, 2/A-410 and 5/A-410 "WET SIDE(S) ONLY", A-001A A.4 | kept |
| Cafe Work Room 104 walls (570.36 SF) | NO | G/A-221 draws a single layer on the Work Room side: 5/8" FRT plywood (FRP-1 over it, A-510); there is no gypsum board on that face | Work Room GWB faces removed (C-H1-N B, C-H1-W B, C-H2a A); the FRT plywood stays |
| Grab & Go soffit 5/8" FRT plywood 110.49 SF | supported | 3/A-221 "5/8" PRESSURE TREATED FRT PLYWOOD SUBSTRATE" on the full face; GWB above T.O. WD-1 (RFI-34) | kept |
| Janitor 3/4" FRT plywood 17.0 SF | supported | 11/A-200 "AREA OF 3/4" FIRE RESISTANT PLYWOOD BLOCKING (TYP)", 8'-0" hold to the underside of the shelf; width RFI-33 | kept |

## Changes (rev5 → rev6)
| Material | rev5 | rev6 |
|---|---|---|
| 5/8" Type X W.R. | 1,713.00 SF | 1,142.63 SF |
| 5/8" FRT plywood | 2,838.21 SF | 1,886.46 SF |
| Drywall screws | 19,938.73 | 19,254.29 |
| Joint compound | 1,196.32 lb | 1,155.26 lb |
| Joint tape | 6,147.78 LF | 5,936.74 LF |

No change: 5/8" Type X 14,902.61 SF; 3/4" FRT plywood 370.46 SF; partitions 569.82 LF.

## RFIs
- **RFI-11:** rewritten. W.R. is confirmed in the wet rooms and on the restroom ceilings; there is none in the Cafe Work Room.
- **RFI-13:** FRP length now taken from the Work Room plywood faces (87.52 LF).
- **RFI-37 (resolved from the plan, CLOSED):** since rev0, the take-off carried 5/8" FRT plywood behind the GWB on the Sales / Cafe side of C-H1-N and C-H2a. Removed: −951.75 SF (C-H1-N A 647.50 + C-H2a B 304.25).
  - G/A-221: the Sales Floor side has one layer, "5/8" GYPSUM BOARD".
  - A-510 101: painted gyp bd.
  - 1/A-225 and 5/A-226A: the C-H2a Cafe face is PT-3 paint around door 3.
  - Evidence: images 12–14 in `../investigacion_WR_FRT/`.

## Gates
- REGLAS OK (810 rules, 0 failures)
- ALCANCES OK
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK
- Independent back-check: PASS WITH COMMENTS. The comments are resolved; see `takeoff_work/etapas/5_auditoria/BACKCHECK_rev6.md`.

Skill: new rule R80e.26 (count board layers per side in the section drawing before changing a face) in `take-off-metal-frame-drywall_FINAL_v80k.zip`. Merge it into v80l.

Drive: not uploaded.
