# BITACORA rev20c FINAL — CR City Hotel (Castle Rock, CO)

rev20c is a NEW delivery that replaces rev20b: the user answered RFI-30 ('ponlo como alternate'). The stair 127 lining leaves the base bid and is priced apart as ALTERNATE #1 (ADD). RFI-31 resolved from the printed rating + finish (A0.01 2 HR RATED EXTERIOR WALL, 1/A4.01 wood siding, A0.07 XW.6.3 | 2): XW.6.3-L1-04 A / B at 4.33 LF [DERIVED 39.0 / 9]; Review Item with the delta if the exterior face carries no exterior gypsum (-121.24 SF).

## Delta del Material Summary (NET) rev20b -> rev20c

Regenerated from the final Excel Material Summary (etapas/DELTA_rev20b_rev20c.md, delta_rev.py: rev20c Excel vs the delivered rev20b Excel); never typed by hand.

| Material | Unit | rev20b | rev20c | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 92,750.35 | 92,103.69 | -646.66 |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 28,498.16 | 28,711.62 | +213.46 |
| Resilient channel 1/2" deep (09 22 16 2.2.E.4), spacing per the UL assembly (A0.08 FS-1 / RS-1) | LF | 27,124.98 | 27,179.23 | +54.25 |
| 5/8" exterior gypsum sheathing, Type X | SF | 18,349.58 | 18,512.59 | +163.01 |
| Joint compound, all purpose | LB | 8,917.74 | 8,886.55 | -31.19 |
| Joint tape, paper | LF | 53,064.71 | 52,904.42 | -160.29 |

## ALTERNATE #1 (ADD) - NOT in the base (user decision 13-nov on RFI-30: 'ponlo como alternate')

Stair 1 (Room 127) interior lining, Levels 1-4: 2-1/2" metal stud furring @ 16" o.c. + top / bottom track + 5/8" Type X gypsum board, one face, Level 4 finish. REASON: the drawings show a 3-3/8" layer on all four sides of the CMU stair enclosure (7-10/A6.01, 11/A6.01) but do not specify its material, and the referenced Interior Drawings ('RE: INTERIOR DRAWINGS') were not included in the bid set. Excluded from the base bid and priced as an add alternate until clarified; excluded from the base bid and priced as an add alternate until clarified

Its quantities [DERIVED] are NOT in the Material Summary (the Material Summary is the base bid): they are on the Scope Checklist line ALTERNATE #1 and in the Proposal ALTERNATE #1 PRICING block, each with its operation.

## Entrega
- ALTURAS_IMPRESAS_A / _B / final: 1068 markups con Depth en las dos lecturas ciegas (0 'not blind'); 24 renglones de ancho desarrollado con side / faces (lados_fallas 0).
- Auditoria/DOBLE_CIELO.csv: 64 cuartos de 5 hojas RCP (todos), páginas DOUBLE CEILING en ALTURAS_REVISADAS.
- detail_faces: 19 detalles cara por cara. rcp_tags: + 17 ACT / WS con motivo N/HOJA. Caras F&B de W.6-L1-04 / W.6-L1-32 con markup EXCLUDED (1/A7.30).
- Auditoría U-181 independiente (cambios + COBERTURA de 57 detalles y 25 hojas RCP + lecturas ciegas de cada renglón nuevo): Auditoria/AUDITORIA_U181_rev20.md, abiertos: 0.

## Errores míos registrados (con regla y test)
- BE-CR38: al reemplazar un bloque de alturas_entrega se perdieron los 12 renglones partidos de DW.4 (test BE-CR38).
- BE-CR40: reporté un faltante (GYP-1 8'-11" de corredores) buscando texto en el JSON; estaba cargado (test BE-CR40).
- Las dos lecturas ciegas del smoke curtain omitieron la cara del shaft: la auditoría U-181 la encontró (pregunta ciega: pedir TODAS las caras).

