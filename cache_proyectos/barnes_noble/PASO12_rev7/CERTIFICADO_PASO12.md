# CERTIFICADO PASO 12 — Matriz de cobertura total (segunda revisión independiente, 2.ª pasada)

**Proyecto:** Barnes & Noble – Colorado Springs (3173 Cinema Point)
**Entrega revisada:** rev7 (`FINAL_FOR_REVIEW_2026-10-24_rev7`: Excel rev7 + `Barnes_Noble_ColoradoSprings_FINAL_markups_rev7.pdf` + `README_REVIEW.md`)
**Fecha:** 2026-10-27 · **Skill:** take-off-metal-frame-drywall v80n (§0.F Paso 12, AUTONOMÍA TOTAL, R80e.26, R80e.27)

**Fuentes usadas:**
- El bid set (69 págs., Drive).
- Los entregables rev7.
- `DECISIONES_ESTIMADOR.md`, solo para separar decisiones de errores.
- `BIBLIOTECA_ERRORES.md`.
- La matriz rev6 (`PASO12_rev6/MATRIZ_COBERTURA.xlsx`), para no omitir ítems.

No se abrió `takeoff_work/` ni ningún take-off del estimador o de terceros. **No se editó el take-off.**

## Veredicto

**NO PASA.** Hay tres motivos:
1. La cobertura es **99.59 %**: quedan 2 GAP.
2. Hay **9 CORREGIR** confirmados en el plano (13 filas de la matriz).
3. La biblioteca tiene **10 pruebas en FAIL**.

Las proporciones y el cuadre Bluebeam están OK. Cada GAP trae su destino propuesto. Con los 9 CORREGIR y los 2 destinos aplicados, la entrega queda en 100 %.

## (a) Matriz de cobertura — `MATRIZ_COBERTURA.xlsx`

| Concepto | Cantidad |
|---|---|
| Ítems (471 de rev6 re-mapeados a las filas de rev7 + 13 nuevos de esta pasada) | **484** |
| COVERED | 235 |
| EXCLUDED (con motivo) | 162 |
| RFI | 72 |
| CORREGIR (filas; únicos = 9) | 13 |
| GAP | **2** |
| **Cobertura rev7** = (484 − 2) / 484 | **99.59 %** |

**Las 57 filas GAP / CORREGIR de rev6:** se verificaron una por una en el Excel rev7 y en el plano (hoja Coverage Matrix, columna "rev7 verification"). Todas tienen destino, salvo:
- **#147:** la parte del 1-5/8" está mal interpretada (C7-01).
- **#333:** el fastener es el de la nota típica y no el del detalle específico (C7-03).

**Destinos nuevos de rev7 confirmados en el plano en esta pasada (recortes en `img/` o en las teselas revisadas):**
- 6/A-226A: T.O. WD-1 = 2'-10" + 8'-2" + 4'-0" = 15'-0" (C-01).
- 22/A-201: cement board base 1'-2" (C-03).
- 3/A-410: bubble 3 = Top Track Detail (C-07).
- 2/A-221: cross bracing AS REQ'D y plywood a todo lo alto del soffit.
- H/A-221: H3b plywood UP TO 8'-0".
- 4/A-101: FRT header + base del FE cabinet.
- 5/A-410: clip angle 2"x2" 16 ga.
- 8.C / 8.D de A-410.
- 7/A-210: 3"x3"x16 ga clip angles.
- 2/E-103: 4'x8' FRT plywood BY GC.
- A-410 Metal Stud Schedule: 14 SJ 22'-0".
- 1/A-121: Grab & Go GWB 7'-1".
- 3/A-210: bandas B.O. ceiling 10'-6" a 11'-3 1/2" V.I.F.

**Re-barrido propio:** se leyeron por teselas a 110 dpi (≥ 200 dpi en los detalles citados):
- A-410, A-121, A-221, A-226A, A-101 (notas y key notes), A-002 (responsibility schedule) y A-210.
- Las hojas E/M/P y las narrativas, por texto.

**Ítems nuevos (filas N-01 … N-13):**
- **Nuevos de verdad:**
  - N-01 (GAP)
  - N-02 (CORREGIR)
  - N-03 (GAP)
  - N-04 … N-08 (EXCLUDED, E/M/P y A-002 sin fila en rev6)
  - N-13 (P.A.F. de 8/A-410)
- **Verificación:** N-09 (cota 46'-0").
- **Defectos de consistencia de los entregables:** N-10 … N-12.

### GAP (sin destino en rev7)

| Fila | Ítem (N/HOJA) | Destino propuesto |
|---|---|---|
| N-01 | 4/A-410 y 3/A-410 (types 4 y 3, partial height): "3 5/8" METAL STUDS @ 16" O.C. TO BOTTOM OF NESTED STUD BRACING." Es la misma frase que en F/A-221, que rev7 sí carga (6.52 LF + RFI-46) | Extender RFI-46 a los types 3 y 4. Delta: +122.32 LF de 3-5/8" stud [DERIVADO 38.68 + 83.64], un nested stud en el tope. Supuesto conservador documentado |
| N-03 | E-301 Sec. 265119: "This contractor shall provide and install all necessary support media for all lighting fixtures … All fixtures shall be firmly supported from beams or joists … Fixtures shall not be supported from roof deck." Rev7 carga 401.0 LF de wire adicional en luminarias (5/A-121) sin RFI de traslape | RFI (extender RFI-53). Si es del EC: −401.0 LF de hanger wire (29 hangers) |

## Lista de CORREGIR (valor correcto + evidencia)

| ID | Qué dice rev7 | Plano [CONFIRMADO] | Corrección | Imagen |
|---|---|---|---|---|
| C7-01 | Material Summary R13: 1-5/8" metal stud 131.42 LF, descrito como "compression post per brace group" citando 5/A-121 | 5/A-121 rotula "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C." sobre el tubo **horizontal**: es la alternativa del carrying member a 48". No hay poste dibujado. El miembro vertical en cada punto de brace es "16 GA. WIRE 12'-0" O.C. EACH WAY AND WITHIN 6'-0" OF EACH WALL" | R13: 131.42 → **0 LF**. Los mismos 131.42 LF [DERIVADO Σ grupos × drop] van como **16 ga wire** bajo RFI-38. Los splay wires (743.29 LF) no cambian | `A-121_5_1-5-8-metal-joist-framing-48OC-horizontal.png` |
| C7-02 | R49 slab pins: 640.61 pcs @ 12" (no impreso). RFI-ACC-slab-pins cita "24" (type K box)", que es de otro proyecto | 9/A-410: "0.177 DIA. HILTI POWDER ACTUATED FASTENER W/ 3/4" EMBEDMENT AT 24"". Nota 8.F: "0.145" DIA. HILTI X-DNI FASTENER … 2 ROWS AT 16" O.C." | R49 = **960.92 pcs X-DNI** [DERIVADO 640.61 × 2 / 1.3333], el impreso conservador (+320.31). RFI con la alternativa de 9/A-410: 320.31 pcs (−640.61). Quitar "type K box" | `A-410_9_floor-track-PAF-24in.png`, `A-410_note8_A-C-E-F_fasteners.png` |
| C7-03 | R28: X-EDNI 720 pcs (nota típica 8.C) en el deep leg / relief channel. Los P.A.F. de los cross members no están cargados | 8/A-410 Typ. Connection (perpendicular y parallel): relief channel "ANCHOR TO STEEL PLATE WITH #8 PAN HEAD SELF TAPPING SCREWS AT 24" O.C. AND 6" FROM ENDS"; "ATTACH TO TOP CORD OF EXIST'G STRUCTURE W/ #8 SCREWS"; cross member "(1) 3/16" 3/8" P.A.F. AT EACH END". El detalle específico manda sobre la nota típica | R28 → **#8 pan head self-tapping screws 291 pcs** [DERIVADO Σ ROUNDUP(L/2)+1 en las 32 corridas, 479.85 LF]. Fila nueva **P.A.F. 3/16" x 3/8": 282 pcs** [DERIVADO 705.0 / 5.0 = 141 × 2] (RFI-41). X-EDNI 720 queda solo como alternativa en RFI | `A-410_8_typ-connection-8-screws-24OC-PAF.png` |
| C7-04 | R48 framing screws: 3,124 = 4 × 781, un solo producto | Nota 8.A: 25/20 ga → #8-18 x 1/2", mín. 2 por conexión; 18/16 ga → #10-16 x 3/4", **mín. 3 por conexión**. Rev7 carga 14 ga SJ en el type 2, C-H2a, C-H2b y C-F | **#10-16 x 3/4": 1,740** [290 piezas = 7,257 LF / 25 ft, × 6] + **#8-18 x 1/2": 1,964** [491 × 4] = 3,704 (**+580**) | `A-410_note8_A-C-E-F_fasteners.png`, `A-410_stud-schedule-3-5-8-14ga-22ft.png` |
| C7-05 | R47 drywall screws: 19,442.26, un solo producto; N/SHEET "GA-216" (es un estándar, no una hoja) | Nota 8.E: #7 x 1-1/4" Hi-Low **Type S** a 25/20 ga; #6 x 1-1/4" **Type S-12** a 18/16 ga (aquí 14 ga) | **S-12: 13,372 pcs** [11,143.59 SF sobre walls de 14 ga × 1.2] + **Type S: 6,070 pcs** [5,058.29 SF × 1.2]. N/SHEET → A-410 8.E y A-001A Div 09 | `A-410_note8_A-C-E-F_fasteners.png` |
| C7-06 | R33 cement board 789.94 SF mezcla dos espesores | 22/A-201: "5/8" CEMENT BOARD". E/A-221: "E1-1/2" CEMENT BOARD". A, B, C, D/A-221: "1/2" CEMENTITOUS BOARD" | Dos renglones: **1/2": 739.90 SF** (C-E1-S 475.0 + C-E1-P.2 52.75 + C-E1-B 57.75 + counters 154.40) y **5/8": 50.04 SF**. En R30 (screws) agregar E/A-221 y A-D/A-221 al N/SHEET | `A-221_A-E_half-inch-cementitious-board.png`, `A-201_22_five-eighths-cement-board-base.png` |
| C7-07 | Pending RFI-23 (C52) y Scope ALC-16 (D100): "FRT blocking 585.27 LF" | R19 = 387.0 + 69.0 + 85.6 + 10.67 + 16.0 = **568.27 LF** | Corregir el texto en las dos celdas; sin cambio de cantidad | (celdas) |
| C7-08 | README_REVIEW rev7 cita ALC-X26, X27, X28, X29 y X30 | Scope Checklist: ALC-X40 (ACT), X41 (Unistrut / strut), X42 (caulk), X43 (seismic), X44 (remove & replace GWB). ALC-X30 = batt insulation | Reescribir los IDs del README | (README) |
| C7-09 | PDF de markups, página LEGEND: "Source: takeoff_canon.json" | Regla BE-41: no hay nombres internos en los entregables | "Source: take-off Excel rev7". El tool `markups_bluebeam.py` del skill escribe el basename y hay que cambiarlo | (pág. 70) |

**Verificado y descartado en esta pasada (no es error):** la cota "46'-0"" bajo la nube del Cafe Seating en 1/A-121 es el track **LWT-01**:
- La cadena cierra: 1'-5" + 46'-0" + 1'-5" = 48'-10" = 5'-0" + 38'-10" + 5'-0".
- "14'-0"" es el track del lado este.
- La nube mide 38'-10" × 14.77 ft, como en rev7.
- Queda como prueba nueva BE-49. Imagen: `A-121_1_46ft-is-LWT01-track-not-cloud.png`.

## (b) Biblioteca de errores — `cache_proyectos/BIBLIOTECA_ERRORES.md`

**Pruebas nuevas:**
- Por los errores de rev6: BE-14 (afirmaciones "not printed"), BE-15 (función del miembro dibujado), BE-16 (accesorios impresos sin fila), BE-17 (productos por gauge), BE-18 (ítems sin destino).
- Por los errores de rev7: BE-19 (espaciamiento impreso de fasteners), BE-46 (un espesor por renglón), BE-47 (textos e IDs vs renglones), BE-48 (nombres internos en markups), BE-49 (cota atribuida al elemento correcto), BE-50 (traslape A vs E/M/P sin RFI).

**Resultado rev7: 40 pruebas — 27 PASS · 10 FAIL · 3 N/A.**

| FAIL | Por qué |
|---|---|
| BE-12 | "type K box"; poste atribuido a 5/A-121; N/SHEET "GA-216" |
| BE-15 | C7-01 |
| BE-16 | C7-03 |
| BE-17 | C7-04, C7-05 |
| BE-18 | 2 GAP |
| BE-19 | C7-02, C7-03 |
| BE-46 | C7-06 |
| BE-47 | C7-07, C7-08 |
| BE-48 | C7-09 |
| BE-50 | N-03 |

**PASS destacados:**
- Fire-stop track (264.21 LF).
- W.R. en walls y ceilings de wet rooms.
- Capas por lado.
- Soffits por lado.
- I SIM.
- Cotas LF (19'-0" HOLD, 15'-0").
- Existing.
- Track = partitions − caras de remate.
- BE-40: los 51 renglones de Material Summary tienen N/SHEET y desglose u operación que reproduce el Net (Δ máx 0.06 SF).
- BE-41 (Excel), 6 hojas, orden y subtotales, cuadre Bluebeam.

## (c) Proporciones (hoja Proportions) — OK, con observaciones

| Proporción | Valor | Lectura |
|---|---|---|
| Board vs Σ LF × H × 2 | 0.66 (walls 0.62) | Explicado: caras a ceiling + 6" (RFI-19) y walls del Cafe con 0–1 cara de board |
| Conciliación Partition Takeoff vs Material Summary | Δ 0.06 SF | OK |
| Screws / SF | 1.20 | Igual al yield. Es mayor que el espaciamiento impreso en 8.E (≈ 0.75 walls / 1.1 ceilings): obs. O4 |
| Compound / SF | 0.072 | OK |
| Tape / SF | 0.37 | OK |
| Studs | 0.80 / LF a 25 ft | OK |
| Track = partitions − 1.206 | — | OK |
| Clip angles / crossings | 1.16 | OK |
| Plywood screws / SF | 1.063 | OK |
| Cement board screws / SF | 2.13 | OK |
| Hangers | 8.2 SF por hanger | OK |

Fuera de rango, y por eso cubierto por un CORREGIR:
- Slab pins: 1 / ft (C7-02).
- X-EDNI (C7-03).
- Framing screws por gauge (C7-04).

**Observaciones (hoja Observations, O1–O8):**
- **O1:** posible doble conteo de C-F (nested bracing + nested runner).
- **O2:** Inputs C12–C14 con "canon constants" y deck n/a.
- **O3:** banda frontal del vestibule de 1.63 SF (V.I.F.).
- **O4:** yield de screws vs 8.E.
- **O5:** grupos de brace de la nube.
- **O6:** los (4) Tek por clip angle de 5/A-410 no aparecen en ningún renglón de screws.
- **O7:** textos "(rev6)" y orden de RFI-51.
- **O8:** "PRESSURE TREATED" en 3/A-221.

## (d) Cuadre Bluebeam vs Excel (hoja Bluebeam vs Excel) — OK

- **Σ Length y Σ Wall Area (Length × Depth):** cuadran en los 18 types y en OTHER FRAMING.
  - Type I: Δ −0.006 LF / −0.15 SF, por redondeo.
  - OTHER FRAMING: Δ 0.003 LF / 0.05 SF.
- **Las 94 anotaciones:**
  - La geometría está dentro del 2 % del LF de cada una.
  - El Depth es igual a la altura del Excel.
  - El Page Label es A-101 / A-221 / LEGEND.
- **Existing:** los 17 walls (417.43 LF) están marcados "EXISTING – EXCLUDED".

## Pasos siguientes (sesión del take-off, regla de autonomía)

1. Aplicar C7-01 … C7-09.
2. Dar destino a N-01 y N-03: RFI con delta y supuesto conservador.
3. Revisar las observaciones O1–O8.
4. Actualizar el skill:
   - `markups_bluebeam.py`: no escribir nombres de archivos en la leyenda.
   - Familias de screws por gauge (8.A / 8.E).
   - Un renglón por espesor de cement board.
   - Regla "el detalle específico manda sobre la nota típica de fasteners".
5. Volver a correr el Paso 12 sobre la rev8.
