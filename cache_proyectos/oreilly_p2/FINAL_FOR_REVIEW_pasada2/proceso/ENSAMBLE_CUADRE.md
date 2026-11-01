# ENSAMBLE — cuadre Excel (run4) vs ELEMENTO_1..6 aprobados (O'Reilly Evans CO #1, pasada 2)

Excel: `run4/takeoff_work/etapas/8_excel/Takeoff_runner.xlsx` (= `ENTREGA/OReilly_Evans_CO1_Takeoff_pasada2.xlsx`). Todo NET, sin waste.
Resultado: **1 diferencia** (renglón nuevo impreso, track brace en empalme de strut, 6.0 LF, RFI-28). El resto cuadra exacto; abajo, dos diferencias de presentación que no cambian ningún total.

## ELEMENTO 1 — Partitions (Partition Takeoff)
| Type | Excel LF | E1 LF | Excel Board SF | E1 Board SF | Cuadra |
|---|---|---|---|---|---|
| S21 (5 walls) | 288.625 | 288.62 | 3,891.05 | 3,891.05 | sí |
| S24 (3) | 37.385 | 37.38 | 317.77 | 317.77 | sí |
| S41 (4) | 6.46 | 6.46 | 77.52 | 77.52 | sí |
| S42 (2 filas: 01+02, 03+04) | 122.622 | 122.62 | 2,267.16 (1,368.50 + 898.66) | 2,267.16 | sí |
| S43 (5) | 52.729 | 52.73 | 902.76 | 922.76 → 902.76 (nota de E2) | sí (*) |
| S61 (1) | 8.5 | 8.5 | 144.50 | 144.50 | sí |
| EXT-8CFMF (MS1-8 / MS2-8) | 12.0 | 12.0 | 154.89 | 154.89 | sí |
| EXT-6CFMF (MS1-6 / MS2-6 / CORN-S) | 48.0 | 48.0 | 0 | 0 | sí |
| OTHER: HEAD-A-8 / HEAD-A-6 | 38.667 c/u | 38.667 c/u | 20.45 / 0 | 20.45 / 0 | sí |
| OTHER: VH-C / VH-B1 / VH-B2 | 8.75 / 5.667 / 5.667 | igual | 5.84 / 3.78 / 3.78 (= 13.40) | 13.40 | sí |
(*) E2 ya lo dice: los 20.0 SF de la cara break de S43-RR-W sobre el W.R. del janitor salen en el ítem GWB-S43-RR-W-ABOVE-WR; el total de board no cambia.
Alturas por wall (14.844 / 13.958 / 15.729 / 8.5 / 12.0 / 11.792 pond. / 9.241 pond. / 20.667 / 7.969 / 9.333 / 4.286) = E1.

## ELEMENTO 2 — Board por tipo (Material Summary)
| Renglón | Excel | E2 | Cuadra |
|---|---|---|---|
| 5/8" gypsum board, Type X | 7,404.93 SF | 7,404.93 | sí |
| 5/8" gypsum board, Type X W.R. | 721.21 SF | 721.21 | sí |
| 5/8" glass mat sheathing | 534.88 SF | 534.88 | sí |
| FRT plywood substrate (5/8 in.) | 407.63 SF | 407.63 | sí |
| 1/4" gypsum board - printed | 187.16 SF | 187.16 | sí |
| Sanitary wall panel system W-4 | 555.34 SF | 555.34 | sí |
| Level 5 finish | 6,432.72 SF | 6,432.72 | sí |
| Gypsum board jamb return at openings | 11.78 SF | 11.78 | sí |

## ELEMENTO 3 — Studs por tamaño / gauge
| Renglón | Excel | E3 (rev2) | Cuadra |
|---|---|---|---|
| 1-1/2" Z-furring channel 150ZF125-18 (25 ga) | 2,517.50 LF | 2,517.50 | sí |
| 8" stud 800S162-54 (16 ga) | 537.32 LF | 537.32 | sí |
| 6" metal stud (600S162-54 714.20 + 600S200-54 225.67 + 50.33 CONT kicker + 600S162-43 291.70 + 600S162-33 68.00) | 1,349.90 LF | 1,349.90 | sí |
| 3-5/8" metal stud 362S162-33 / -43 (walls + kickers + struts + ties 140.0 + 98.0 + dobles CJ 46.02) | 2,149.54 LF | 2,149.54 | sí |
El desglose por gauge va en "Where it comes from" de cada renglón (trazabilidad.py).

## ELEMENTO 4 — Track (estándar vs deflexión separados) + RC
| Renglón | Excel | E4 | Cuadra |
|---|---|---|---|
| Track estándar bottom (8" 12.0 + 6" 56.5 + other framing 77.34 + 3-5/8" 219.19 + heads 20.09) | 385.12 LF | 385.11 | sí (redondeo por renglón) |
| Track estándar top (12.0 + 56.5 + 77.34 + 172.35 + 20.09) | 338.28 LF | 338.28 | sí |
| Total estándar | 723.40 | 723.40 | sí |
| Deep-leg slotted deflection track (S42-01 38.67 + S42-04 8.17) | 46.84 LF | 46.84 | sí |
| Z-furring runner track 1-1/2" | 577.25 LF | 577.25 | sí |
| Ceiling perimeter track at GWB ceilings | 72.00 LF | 72.00 | sí |
| Additional head track | 32.73 LF | 32.73 | sí |
| Header / metal stud box beam 600S162-33 | 56.00 LF | 56.00 | sí |
| Resilient channel - printed | 120.51 LF | 120.51 | sí |
Presentación: el Excel agrupa el track estándar por TAMAÑO del renglón de la plantilla (8" / 6" / 3-5/8" / other framing / heads) y E4 por PRODUCTO (362T125-33 391.54 = 3-5/8" bottom 219.19 + top 172.35, exacto; 600T125-33 / -43 / -54 y 800T125-54 quedan repartidos entre 6", 8", "other framing" (HEAD-A) y "heads" (VH)). El gauge por wall va en "Where it comes from". Totales iguales; deflexión nunca mezclada con estándar.

## ELEMENTO 5 — Bracing, blocking, strap, clips
| Renglón | Excel | E5 | Cuadra |
|---|---|---|---|
| Bracing 1-1/2" C.R. channel @ 48" | 807.52 LF | 807.52 | sí |
| Blocking FRT / 2X FRT wood | 499.16 LF | 499.16 | sí |
| Diagonal flat strap bracing - printed | 96.91 LF | 96.91 | sí |
| Clip angles and framing clips (2x2x14ga 14 + L4x4 12) | 26 PCS | 14 + 12 = 26 | sí |
| Framing clips per stud - printed (FCB43.5 84 + 60 + 24) | 168 PCS | 168 | sí |
| Deflection clips | 0 | 0 | sí |

## ELEMENTO 6 — Trim, control joints, compound / tape
| Renglón | Excel | E6 | Cuadra |
|---|---|---|---|
| METAL trim (corner bead, casing, J, reveal) | 1,117.32 LF | 1,117.32 | sí |
| Control joint, gypsum board walls | 242.78 LF | 242.78 | sí |
| Joint compound | 585.08 LB | 585.08 | sí |
| Joint tape | 3,006.67 LF | 3,006.67 | sí |

## La diferencia
| # | Renglón | Excel | ELEMENTO | Motivo / evidencia |
|---|---|---|---|---|
| 1 | Track brace at strut splice - printed product | 6.0 LF 362T162-33 | no está en E4 ni E5 | Hueco real hallado en la cobertura: 5/S5.1 imprime "2'-0" LONG 3-5/8"x20ga TRACK BRACE AT STRUT SPLICE (362T162-33)" (recorte `proj/takeoff_work/etapas/4_canon/img/img_ensamble/s51_5_track_brace.png`). Lo impreso se carga (R80e.76). Empalmes no ubicados en el plano: 1 por stick de 20 ft del lateral strut continuo (S42-02 1, S42-03 2) = 3 x 2'-0" = 6.0 LF → RFI-28 (B: 1 por wall, -2.0 LF). El elemento estaba incompleto en ese punto; los totales aprobados no cambian (renglón propio). |

## Otros puntos para el revisor (sin cambio de cantidad)
- Pending Items trae además 3 RFIs automáticos de accesorios.py (RFI-ACC additional head track en el storefront A con delta 40 LF; jamb return width; deflection clips, delta 0). Son de la tool, no del canon.
- A4.2 key 12 ("1x4 wood trim paint grade pine") va en la cobertura como n/a Div. 06. Si el revisor lo ubica en las esquinas de los box-outs S41 (4/A4.2), revisar CB-S41-BOXES 24.0 LF de E6.
- S42-02: su continuación de 6.715 ft sigue saliendo de una medida vectorial en pt de A1.1 (aprobada en E1 / RFI-14 cerrado A); no la cambié.
- Cambios de evidencia en el canon y el overlay (sin cantidades): `lect_resolucion/ensamble_cambios.md` (10 renglones). Tools: `skill/take-off-metal-frame-drywall/tools/CAMBIOS_tools_v80v.md` (R80e.79-82).

---

# rev2 — run7 (post-auditoría pasos 11 / 12) vs ELEMENTO_1..6

Excel: `run7/takeoff_work/etapas/8_excel/Takeoff_runner.xlsx` (= `ENTREGA/OReilly_Evans_CO1_Takeoff_pasada2.xlsx`). Partition Takeoff sin cambios contra rev1: los 9 types y OTHER FRAMING dan el mismo LF y board, y S43 sigue en 902.76. Ahora cada renglón lleva un solo producto (BE-46), así que los renglones se compararon contra la suma de sus productos.

## Igual a los ELEMENTO (sin cambio)
| Elemento / renglón | Excel run7 | ELEMENTO | Cuadra |
|---|---|---|---|
| E2: 5/8" X / X W.R. / glass mat / FRT / 1/4" / W-4 / Level 5 / jamb return | 7,404.93 / 721.21 / 534.88 / 407.63 / 187.16 / 555.34 / 6,432.72 / 11.78 | igual | sí |
| E3: Z-furring 150ZF125-18 | 2,517.50 (desglose por wall: S21-N 807.77 + S21-E 642.07 + S21-S 753.08 + S21-W1 94.37 + S21-W2 220.21) | 2,517.50 | sí |
| E3: 8" 800S162-54 | 537.32 | 537.32 | sí |
| E3: 3-5/8" = 362S162-33 1,911.54 + 362S162-43 238.0 (ties 140 + 98) | 2,149.54 | 2,149.54 | sí |
| E4: track estándar bottom / top (8" 12 / 6" 12 + 36 + 8.5 / other framing 38.67 + 38.67 / 3-5/8" 219.19 bottom, 172.35 top / heads 20.09) | 385.12 / 338.28 = 723.40 | 723.40 | sí |
| E4: deep-leg 46.84; ZF runner 577.25; ceiling track 72.0; additional head track 32.73; header 56.0 (desglose (3.333 + 1.333) x 4 x 3); RC 120.51 | igual | igual | sí |
| E5: bracing 807.52; blocking 499.16; strap 96.91; clips 2x2x14ga 14 + L4x4 12 = 26; FCB43.5 168 | igual | igual | sí |
| E6: metal trim = corner bead 465.65 + Fry JDM-625 41.3 + Fry DRMF-625-75 41.3 + casing (J) bead 194.25 + J molding 374.82 | 1,117.32 | 1,117.32 | sí |
| E6: compound 585.08 lb / tape 3,006.67 LF (0 % waste: regla del skill, yields sin waste) | igual | igual | sí |

## Diferencias (5)
| # | Renglón | Excel run7 | ELEMENTO | Motivo / evidencia |
|---|---|---|---|---|
| 1 | Track brace at strut splice (362T162-33) | 6.0 LF | — | Viene de rev1: impreso en 5/S5.1; el número de empalmes va a RFI-28 |
| 2 | Control joint | 312.49 LF | 242.78 (E6) | +69.71 LF CJ-DIR-CHANGE. A1.1 3.A (2.ª cláusula) pide juntas "where framing or furring changes direction": 4 esquinas del Z-furring S21 (2 x 15.729 + 2 x 13.958) + esquina del header S42 (2 caras x 5.167). RFI-30. Hueco 1 del paso 12: E6 estaba incompleto. |
| 3 | 6" stud (600S162-43) | 340.72 LF; total 6" 1,372.04 | 6" 1,349.90 (E3) | +22.14 LF VH-DIAG-BRACE. 3/A5.2 + 3/A3.1 imprimen el diagonal bracing del vestibule head: 3 x SQRT(5.375² + 5.0625²) = 7.38 ft, con cotas impresas. RFI-32 para spacing / miembro. Hueco 8 del paso 12. |
| 4 | W-4 panel trim and edge molding | 234.0 LF (renglón nuevo) | — (E2 solo trae el panel) | A4.1 key 8 "provide trim and edge molding around perimeter". Se carga con el panel (RFI-07 cerrado A): 2 x (32.667 + 32.667 + 34.0 + 17.667). RFI-31. Hueco 6 del paso 12. |
| 5 | Producto dentro de la familia 6" | 600S162-54 = 687.32 / 600S162-43 = 340.72 | E3 pone los 176.88 LF de joists en 600S162-54 | No es diferencia de total: E3 había clasificado mal los joists. Los del vestíbulo (CJ-VEST-100A, 26.88 LF) son 600S162-43 (3/A3.1 key 8, canon); los de office y R.R. (150.0) sí son 600S162-54 (7/A4.2 key 5). |

Sin cambio de cantidad, solo documentado: S24-OF / RR / RRS (dueño de esquina, R70.2 / R78.35); S42-02 (6.715 sigue cargado como supuesto conservador con RFI-29); S42 en dos renglones (convención de partition_types); Layers 0.79 de HEAD-A-8; markups S41 / S43 ahora a 0.00 % (bands ajustados al LF contado). Exclusiones nuevas con fuente (ALC-INSUL, ALC-STUCCO, ALC-ACT, ALC-SHUTTERS, ALC-WOODTRIM con RFI-33, ALC-STORM) sin cantidad.

---

# final — run10 (respuestas del estimador 2026-11-01) vs ELEMENTO_1..6

Delta por renglón contra run7 y su explicación: `TOTALES_FINALES.md` (23 renglones cambian). Resumen de lo que difiere de los ELEMENTO aprobados:
| Elemento | Renglón | ELEMENTO | Final | Diferencia / respuesta |
|---|---|---|---|---|
| E1 | S42 (S42-01+02) LF | 64.122 | 64.606 | RFI-29: extensión de S42-02 7.2 ft (antes 6.715 sin cota) [PENDIENTE] + RFI al GC |
| E2 | 5/8" Type X | 7,404.93 | 7,421.40 | RFI-15 B +8.84 (cara 5.34 + underside 3.50); RFI-29 +7.63 |
| E2 | 1/4" | 187.16 | 195.58 | RFI-15 B +8.42 |
| E2 | Level 5 | 6,432.72 | 6,440.16 | RFI-29 +7.44 |
| E3 | 362S162-43 (ties) | 238.0 | 140.0 | RFI-11 A: sin ties en los piers |
| E3 | 362S162-33 | 1,911.54 | 1,912.02 | RFI-29: lateral strut +0.48 |
| E3 | 6" (600S162-43) | 340.72 (rev2) | 340.72 | sin cambio (RFI-32 A) |
| E4 | track estándar top 3-5/8" | 172.35 | 96.57 | RFI-20 B: el top de S42-02 / S42-03 pasa a deep-leg |
| E4 | top heads (VH) 20.09 | 20.09 | 0 | RFI-20 B: pasa a deep-leg 6" web |
| E4 | deep-leg | 46.84 | 123.11 (3-5/8") + 20.09 (6") | RFI-20 B; renglón separado por web |
| E4 | bottom 3-5/8" | 219.19 | 219.68 | RFI-29 +0.49 |
| E4 | RC | 120.51 | 128.51 | RFI-15 B +8.0 |
| E5 | bracing | 807.52 | 808.01 | RFI-29 +0.49 |
| E5 | blocking FRT | 499.16 | 600.79 | RFI-25 B +100.67; RFI-29 nailers +0.96 |
| E5 | clips 2x2 / L4x4 | 14 / 12 | 22 / 19 | RFI-26 B |
| E5 | FCB43.5 | 168 | 144 | RFI-11 A −24 |
| E6 | corner bead | 465.65 | 474.62 | RFI-15 B +8.0; RFI-29 +0.97 |
| E6 | J molding | 374.82 | 375.79 | RFI-29 +0.97 |
| E6 | control joint | 242.78 | 340.24 | RFI-27 B −101.25 (S21 a 30 ft); rev2 +69.71 reemplazado por RFI-30 B +129.0 en las esquinas de partition. Las 4 esquinas de S21 y la del header S42 (69.71) siguen cargadas porque la respuesta B agrega las de partition sobre la opción A |
| E6 | compound / tape | 585.08 / 3,006.67 | 586.27 / 3,012.77 | siguen el board |
| — | W-4 trim | — | 100.67 | RFI-31 B |
| — | track brace | — | 6.0 | RFI-28 A |
Compuertas run10: reglas.py solo back-check; registro entregable OK; alcances compuerta OK; cobertura 254/254; markups por type dentro de 0.33 %; compuerta de texto de cliente sin hallazgos.
