# RESUMEN rev20 FINAL — CR City Hotel (Castle Rock, CO)

rev20 FINAL reemplaza a rev19. Origen: el usuario revisó ALTURAS_REVISADAS (12-nov, "aqui tiene datos ensimados, arreglalo") y preguntó por las alturas tipo soffit, el cielo del corredor, el doble cielo y las doble layer. COORDINACIÓN: doble lectura ciega U-176 de todo renglón con Depth (BE-CR35), textos legibles (U-187 / BE-CR36), side / faces (BE-CR37), cobertura completa de detalles y RCP (U-189), REGLA DE ORO #3 doble cielo (U-190). Skill vigente v81cf105.

## Delta del Material Summary (NET) rev19 -> rev20

Regenerated from the final Excel Material Summary (etapas/DELTA_rev19_rev20.md, delta_rev.py); never typed by hand.

| Material | Unit | rev19 | rev20 | Delta |
|---|---|---|---|---|
| 2-1/2" stud, 25 ga min. - soffit cripples (soffit framing not drawn: A0.06 partition STUD SCHEDULE 2 1/2" min. gauge 25 applied) | LF | 253.05 | 215.76 | -37.29 |
| Hanger wire 0.162 in dia. (8 ga), ASTM A 641 Class 1, soft temper (09 22 16 2.2.C) | LF | 507.54 | 528.12 | +20.58 |
| 5/8" gypsum board, Type X | SF | 87,140.05 | 89,916.12 | +2,776.07 |
| USG drywall suspension main tee DGLW26 | LF | 1,632.86 | 1,736.75 | +103.89 |
| USG drywall suspension cross tee DGLW424 | LF | 4,898.69 | 5,210.45 | +311.76 |
| USG angle molding DGWM24 | LF | 2,839.59 | 3,094.03 | +254.44 |
| Resilient channel 1/2" deep (09 22 16 2.2.E.4), spacing per the UL assembly (A0.08 FS-1 / RS-1) | LF | 19,598.31 | 27,124.98 | +7,526.67 |
| 5/8" gypsum board, Type C (ceiling) | SF | 21,644.66 | 22,169.62 | +524.96 |
| Joint compound, all purpose | LB | 8,476.00 | 8,713.68 | +237.68 |
| Joint tape, paper | LF | 50,794.66 | 52,016.04 | +1,221.38 |

## Cambios de cantidad (todos por la cadena: rev20_soffits, rev20_campo, rev20_detalle_caras, rev20_fb_excluidas)

| Renglón | rev19 | rev20 | Fuente |
|---|---|---|---|
| Banda del corredor SOF-L2-01 / L2-02 / L3-316 / L3-318 / L4-02 | 0.917 ft/LF | 1.9375 ft/LF (+1,025.06 SF) | 7/A7.23 impreso 6 1/2" + 4 1/2" + 4 1/2" + 7 3/4" por lado |
| Cara de la caja derecha en el plenum SOF-*P (nuevo) | - | 0.9688 ft x LF banda / 2 (+486.09 SF) | 7/A7.23 9 1/2" + 2 1/8" (H-A 0.917 / H-B 0.97) |
| Smoke curtain SOF-*-SC* | 5.039 | 5.04 (rev20 corrigió a 3.06 y la auditoría U-181 encontró la 5a cara) | 12/A9.03 medido |
| Coffers SOF-L1-01 | 1.063 | 1.25 (+55.33 SF); cripples -37.29 LF | 5/A7.31 impreso 10 3/4" |
| Beam wraps retail BW-L1-RETAIL | 389.49 SF | 379.14 SF | S1.02 + AISC viga por viga |
| RS-1 sobre los baños de L4 CLG-L4-106R..114R (nuevo) | - | +484.63 SF Type X + 363.48 LF RC | doble cielo (A0.08 RS-1) |
| Cara inferior del mezzanine 219 CLG-L1-219U (nuevo) | - | +467.38 SF Type C | 2/A5.04 'GYP BD APPLIED TO B.O. WOOD JOIST'; A0.03 1 HR, A0.08 FS-1 |
| Campo GYP-1 lobby 217 / 317 + vestíbulo + tramo de corredor CLG-L2-217F / L3-317F (nuevo) | - | +202.7 SF c/u + suspensión | 1/A7.23, 2/A7.23 |
| Lazo de banda del vestíbulo SOF-*-217V / 317V (nuevo) | - | 27.35 LF x 1.9375 c/u | 1/A7.23 + 7/A7.23 (H-A / H-B) |
| Caja de borde del WS-1 SOF-*-217B / 317B (nuevo) | - | 38.16 LF x 2.2083 c/u | 5/A7.23, 6/A7.23 (H-A 1.29 / H-B 2.21) |
| Pasaje L1 CLG-L1-129P (nuevo) | - | +35.85 SF Type X | 5/A5.04 'CEILING APPLIED TO UNDERSIDE OF DECK' |
| Vigas de borde norte BW-L1-NORTH (nuevo) | - | +67.95 SF Type C + 92.24 LF RC | A0.08 FS-1 wrap; S1.02 W24X68 + W24X55; 4/S3.08 |
| Resilient channel FS-1 (ceilings[] + RC-FS1-ENDJ-L1/L2/L3 + 24 closet rows) | 16 in o.c. (RFI-14) | 12 in o.c. + 2 channels 6 in apart at each board end joint (+7,070.95 LF [DERIVED] = 7,526.67 total delta - 455.72 delta before UL L546) | UL L546 Item 6 (insulation draped over the membrane; A0.08 FS-1 'BATT INSULATION TO FILL ENTIRE FRAMING CAVITY' / 'SPACING PER ASSEMBLY TO ACHIEVE FULL CAVITY INSULATION'); RS-1 stays 16 in o.c. (no UL #, spec 09 22 16 3.1.A) |

## Review Items nuevos (deducciones / alternativas con su delta)
- Diffuser box del corredor: -28.44 SF. Cara del plenum: -486.09 SF si no se construye. Coffers: cara medida +11.83 SF; posible doble conteo del fondo -104.77 SF.
- Beam wraps retail build-up 2 3/4": +83.6 SF. Caras F&B de 5 walls W.6-0 (nota impresa, non-rated): +940.06 SF si son nuestras.
- Lobby L1: A3.01 GYP-1 vs 1/A7.31 WS-1: -590.81 SF + suspensión si manda WS-1.

## rev20a (auditoría U-138, 12-nov)

- Delta table above regenerated from the Excel (was typed before UL L546: RC 20,054.03 / +455.72; the Excel says 27,124.98 / +7,526.67).
- Material Summary RC row cites UL L546 Item 6 (U-191).
- AUDITORIA_U181_rev20: independent RC review added.
- No quantity changes vs rev20; markups PDF unchanged.

## Entrega
- ALTURAS_IMPRESAS_A / _B / final: 1068 markups con Depth en las dos lecturas ciegas (0 'not blind'); 24 renglones de ancho desarrollado con side / faces (lados_fallas 0).
- Auditoria/DOBLE_CIELO.csv: 64 cuartos de 5 hojas RCP (todos), páginas DOUBLE CEILING en ALTURAS_REVISADAS.
- detail_faces: 19 detalles cara por cara. rcp_tags: + 17 ACT / WS con motivo N/HOJA. Caras F&B de W.6-L1-04 / W.6-L1-32 con markup EXCLUDED (1/A7.30).
- Auditoría U-181 independiente (cambios + COBERTURA de 57 detalles y 25 hojas RCP + lecturas ciegas de cada renglón nuevo): Auditoria/AUDITORIA_U181_rev20.md, abiertos: 0.

## Errores míos registrados (con regla y test)
- BE-CR38: al reemplazar un bloque de alturas_entrega se perdieron los 12 renglones partidos de DW.4 (test BE-CR38).
- BE-CR40: reporté un faltante (GYP-1 8'-11" de corredores) buscando texto en el JSON; estaba cargado (test BE-CR40).
- Las dos lecturas ciegas del smoke curtain omitieron la cara del shaft: la auditoría U-181 la encontró (pregunta ciega: pedir TODAS las caras).
