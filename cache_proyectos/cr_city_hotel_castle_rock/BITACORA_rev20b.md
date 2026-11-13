# BITACORA rev20b FINAL — CR City Hotel (Castle Rock, CO)

rev20b is a NEW delivery that replaces rev20 (rev20a): different quantities (coverage review U-193).

## Delta del Material Summary (NET) rev20 -> rev20b

Regenerated from the final Excel Material Summary (etapas/DELTA_rev20_rev20b.md, delta_rev.py: rev20b Excel vs the delivered rev20 Excel); never typed by hand.

| Material | Unit | rev20 | rev20b | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 89,916.12 | 92,750.35 | +2,834.23 |
| 5/8" exterior gypsum sheathing, Type X | SF | 18,184.98 | 18,349.58 | +164.60 |
| Joint compound, all purpose | LB | 8,713.68 | 8,917.74 | +204.06 |
| Joint tape, paper | LF | 52,016.04 | 53,064.71 | +1,048.67 |

## rev20b (U-193 coverage map: 457 reds reviewed by 3 independent reviewers, Auditoria/COBERTURA_DISPOSICION.csv, 0 open)

- Loaded (missing walls found): UNTYPED-L3-12 (W.4 stub west of LINEN 322, 2.40 LF x 2 faces, L3 twin of UNTYPED-L2-12); XW.6.6-L4-16 B (exterior sheathing face of the F&B 410 NW corner, 5.03 LF; only the F&B interior face is excluded); FW.2-L2-15 / FW.2-L3-15 / FW.2-L3-14 (SE stair CMU north face: corridor 218 / 318 parts 12.06 LF + 309 foyer / closet 6.59 LF; FW.2-L2-14 extended to the 209.1 door).
- XW.6.3-L1-01 S: pier west face to the lobby strip, 3.23 LF x 11.0, +35.53 SF (outside the RFI-05 Retail 124 boundary).
- Loaded conservative (type / material not printed; U-172 / U-191 sweep without answer) with RFI A / B / C and delta: RFI-30 lobby stair 127 lining LIN-127-L1..L4 (2,325.5 SF 5/8" Type X, one face; INTERIOR DRAWINGS referenced but not issued in the bid set); RFI-31 Stair 2 exit passage wall XW.6.3-L1-04 A / B (4.11 LF).
- Addendum reviewed (BuildingConnected 12-nov): Geotech / Irrigation / Landscape / Site Demo Plans - no quantity impact.

## Entrega
- ALTURAS_IMPRESAS_A / _B / final: 1068 markups con Depth en las dos lecturas ciegas (0 'not blind'); 24 renglones de ancho desarrollado con side / faces (lados_fallas 0).
- Auditoria/DOBLE_CIELO.csv: 64 cuartos de 5 hojas RCP (todos), páginas DOUBLE CEILING en ALTURAS_REVISADAS.
- detail_faces: 19 detalles cara por cara. rcp_tags: + 17 ACT / WS con motivo N/HOJA. Caras F&B de W.6-L1-04 / W.6-L1-32 con markup EXCLUDED (1/A7.30).
- Auditoría U-181 independiente (cambios + COBERTURA de 57 detalles y 25 hojas RCP + lecturas ciegas de cada renglón nuevo): Auditoria/AUDITORIA_U181_rev20.md, abiertos: 0.

## Errores míos registrados (con regla y test)
- BE-CR38: al reemplazar un bloque de alturas_entrega se perdieron los 12 renglones partidos de DW.4 (test BE-CR38).
- BE-CR40: reporté un faltante (GYP-1 8'-11" de corredores) buscando texto en el JSON; estaba cargado (test BE-CR40).
- Las dos lecturas ciegas del smoke curtain omitieron la cara del shaft: la auditoría U-181 la encontró (pregunta ciega: pedir TODAS las caras).

