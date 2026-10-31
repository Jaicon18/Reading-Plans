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
