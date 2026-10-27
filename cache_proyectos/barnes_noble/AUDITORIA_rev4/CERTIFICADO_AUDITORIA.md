# Certificado de auditoría final (paso 11) — Barnes & Noble, Colorado Springs — take-off rev4

- **Fecha:** 2026-10-27
- **Auditor:** sesión nueva e independiente. No leyó `takeoff_work/`, ni el canon, ni ningún take-off de terceros.
- **Fuentes usadas:** bid set (Drive id `1YxByMCw-3-SmrFo6PAv21eLc-rNTzB9C`, 69 páginas, md5 `c5a07249…f939`). Se renderizó sin `/Annots` porque el set trae markups ajenos.
- **Entregables auditados:** `FINAL_FOR_REVIEW_2026-10-24_rev4/` (Excel rev4, README, PARA_REVISAR) y `FINAL_FOR_REVIEW_2026-10-24_rev3/Planos marcados/` (markups PDF e imágenes `_v2`).
- **Decisiones del estimador:** `DECISIONES_ESTIMADOR.md` se usó solo para no marcarlas como error.
- **Detalle de cada diferencia:** `COMPARATIVA_AUDITORIA.xlsx` (24 renglones, en inglés). Los recortes circulados están en `img/`.
- **El Excel del take-off no se modificó.**

## Resultado por chequeo

| # | Chequeo | Resultado | Evidencia principal |
|---|---|---|---|
| 1 | Barrido de tags (A-101, A-221, A-200, A-412) | **FAIL** (menor) | `img/C1_A-101_tag_sweep.png`, `img/C1_A-221_tag_sweep.png`, `img/C1_A-221_I_SIM_tags_no_row.png` |
| 2 | Re-medición a ciegas por vectores | **PASS** | `img/C2_A-221_markups_L.png`, `_R.png`, `img/C2_A-101_BOH_markups.png`, `img/C2_A-101_type4_curved_walls.png` |
| 3 | Cadena de detalles | **PASS** | `img/C3_*.png` (2, 3, 4, 5/A-410 · A–I/A-221 · 2, 3/A-221) |
| 4 | Barrido de alcance en las 69 hojas | **FAIL** | `img/C4_*.png` |
| 5 | Aritmética | **FAIL** (trazabilidad) | COMPARATIVA, renglones 13–17 |
| 6 | Formato | **FAIL** (citas y comentarios) | COMPARATIVA, renglones 18–22 |
| 7 | Bluebeam | **PASS** | COMPARATIVA, renglón 23 |
| 8 | Drive | **PASS** | 63/63 archivos con el mismo tamaño |

**Diferencias registradas: 24.**
- 11 tienen delta de cantidad: 1 en el chequeo 1, 1 en el 2, 4 en el 4 y 5 en el 5.
- 13 son de texto o formato, u observaciones sobre decisiones del estimador.

## 1. Barrido de tags — FAIL (menor)

**Método.** Las burbujas en rombo se detectaron por vectores: 89 en A-101 y 27 en el plano de A-221. Cada una se leyó en una hoja de contacto y se ubicó sobre el plano junto con los markups.

**Lo que está bien:**
- Todos los tags 2, 3, 4 y 5 de 1/A-101 caen sobre un wall del Excel. En el janitor, el tag "2" tiene leaders a los dos lados: cubre W2-07 y W2-08.
- Los tags 1, 1A, 1B y 1C son perímetro existente. Están excluidos por decisión del estimador (RFI-01), así que no cuentan como falla.
- Todos los tags de 1/A-221 (H1, H2a, H2b, H3a, H3b, E1, E2, F, I, A, B, C, D) tienen su wall.
- Todos los walls del Excel tienen tag. Los segmentos sin tag (chase del drinking fountain, end posts type 3, legs type 4) están sumados a un wall con tag.
- No hay walls dibujados sin tag fuera del Excel. El vestibule 100 es storefront: su framing va en Material Summary según 1, 4 y 6/A-210.

**Falla.** Hay dos tags **"I SIM."** en 1/A-221 que apuntan a las caras de remate de C-H3a y C-H1-N (7 1/4") y no tienen renglón type I. El framing ya está contado. Falta el acabado:
- +1.21 LF de type I.
- +18.13 SF de 5/8" FRT plywood.
- +12.08 SF de GWB.

## 2. Re-medición a ciegas — PASS

**Escalas** (verificadas contra cotas impresas):
- A-101: 1/8" = 1'-0" (9 pt/ft).
- A-221: 1/2" = 1'-0" (36 pt/ft). Por ejemplo, C-H1-W = 12'-2" impreso.

**Resultado por wall:**
- Los 74 polylines terminan sobre una cara o línea de wall dibujada, a ≤ 1.5" en los dos extremos. Las únicas excepciones son los quiebres a 45° del counter A, las cuerdas curvas y los bordes de RCP de SS-IN.
- La cobertura de las líneas de cara confirma cada tramo; los huecos corresponden a doors dentro del wall (R77.10).
- Las cotas impresas coinciden: W2-02 = 5'-0", W2-05/08/09 = 12'-11", W2-07 = 7'-6" TYP., W3 = 12'-0" + 3'-8", W4 bar = 9'-0", y W2-01 suma 42'-0" + 2'-3" + 3'-0" + resto.
- En el muro sur de A-221, E2 + E1-S = 52.76 LF, igual a la extensión vectorial.

**Única diferencia (dentro de la tolerancia del 2 %).** En los walls curvos type 4 el Excel lleva 25.68 LF; el auditor mide 25.20 LF (R = 32'-9", cuerda 24.6 ft; 25'-1" impreso en una cara). Δ = −1.9 % por wall. Es decisión del estimador (RFI-18); queda como observación. Nota: las 6 cuerdas del markup se traslapan unos 0.8 pt cada una.

## 3. Cadena de detalles — PASS

| Type | Detalle | Lo confirmado |
|---|---|---|
| 2 | 2/A-410 | 3-5/8" @ 16" a deck, 5/8" GB cada lado |
| 5 | 5/A-410 | 6" @ 16" a deck |
| 3 | 3/A-410 | 3-5/8" @ 16", T.O. 8'-0" |
| 4 | 4/A-410 | 3-5/8" @ 16", T.O. 7'-6" |
| E1 / E2 | E/A-221 | 6" @ 16" a deck. E1 = 1/2" cement board; E2 = 5/8" FRT plywood |
| F | F/A-221 | 3-5/8" @ 16", FRT plywood en una cara |
| H1 / H2 | G/A-221 | H1 = 6", H2 = 3-5/8". H2b = FRT en los dos lados |
| H3 | H/A-221 | 6", GB del lado Grab & Go, plywood del lado Sales |
| I | I/A-221 | 6", FRT a T.O. WD-1 y GWB arriba |
| A, B, C | A, B, C/A-221 | 2'-8 1/2" a T.O. stud, cementitious board, 3/4" FRT del lado customer |
| D | D/A-221 | 1'-0" |
| Soffit | 2/A-221 | 3-5/8" @ 16" up to deck |

Los Layers del Excel coinciden con estos detalles.

**Cruces de cantidades:**
- **Cement board 851.4 SF** = E1 (697.0) + A, B, C, D (154.4).
- **3/4" FRT plywood 353.46 SF** = vestibule box 106.6 + posts 105.0 + menu boards 60.61 + backing 17.78 + counters A/B 63.47.

Las filas de material sin cita de hoja se reportan en el chequeo 6.

## 4. Barrido de alcance — FAIL

**Cobertura.** Se revisaron las 69 hojas:
- Hojas A: en imagen (índice y recortes).
- Hojas E, M y P, y addenda 1–3: por texto.
- Spec A-001A Div 05 / 06 / 08 / 09 y A-002 Responsibility Schedule.

**Diferencias con delta, que el plano resuelve:**
1. **Techos GWB de Men's y Women's.** A-410 Partition Notes, nota 2, pide "W.R. … for wall AND ceiling construction". Van ≈ 120.2 SF de Type X → Type X W.R.
2. **11/A-200.** "AREA OF 3/4" FIRE RESISTANT PLYWOOD BLOCKING (TYP)" en el janitor no está en la lista de blocking. Son ≈ 17.0 SF (cota superior).
3. **Soffit del Grab & Go, 3/A-221.** Está en RFI-20 como "not priced", pero el plano lo resuelve: 6'-2" HOLD × (deck − 7'-1"). Agrega ≈ 107.5 LF de 6" stud, 12.34 LF de track y 110.6 SF de cara.
4. **8/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP."** No está en el Excel. Serían hasta ≈ 230 LF si aplica.
5. **Additional head track, doors 3 y 11 (4'-0").** El Excel lleva 0 y cita una nota sin N/HOJA. El auditor no encontró esa nota en A-410 ni en A-500. Si existe, son ≈ 11.2 LF.

**Observaciones sobre decisiones del estimador** (sin FAIL propio):
- W.R. en los walls húmedos del Cafe (2/A-410, nota "*").
- Backing del water heater (P-201).
- Blocking de W-3 "BY GC/FIXTURE INSTALLER" (1, 7/A-414).
- FRP-1 en 104 y 107 (RFI-13).
- Wall tile del Corridor 110: no está en RFI-12.
- Sound batting excluido (A-002).

**Coinciden con el plano:** Type X (A-001A), Level 4 (A-001A), corner guards (RFI-29), access panels (RFI-30 y A-002), control joints (RFI-24), deflection track, vestibule GWB ceiling (A-121, key note 5) y bracing (A-410, nota 3 del schedule).

## 5. Aritmética — FAIL (trazabilidad)

**Recalculado exacto desde el Partition Takeoff:**
- Bottom / top track: 450.02 / 118.59 / 72.
- Bracing C.R.: 2,858.98 = Σ L × (ROUNDUP(H × 12 / 48) − 1).
- Slab pins: 640.61.
- Drywall screws, joint compound y tape: 16,599.8 SF × yields.
- Framing screws: 4 × 775.
- 3/4" FRT, cement board y el reparto de board: Type X + W.R. = board de walls − cement board.

**No reproducible (> 1 %):**
- **3-5/8" stud:** 10,778.08 LF contra 8,810.8 trazable. Faltan 1,967.3 LF sin desglose.
- **6" stud:** 2,900 contra 2,625. Faltan 275 LF.
- **5/8" FRT plywood:** de 2,709.63 SF solo 181.21 SF son trazables.

**Inconsistencias de texto:**
- ALC-07 / ALC-08 conservan cifras de rev2.
- La cross tee de RFI-15 (457.96 LF) difiere del registro de decisiones (443.19 LF).

## 6. Formato — FAIL (citas y comentarios)

**Lo que está bien:**
- 6 hojas visibles, en el orden de la plantilla. `_reglas` va oculta: es el sello de la plantilla.
- Partitions en el orden del schedule (2, 5, 3, 4, H1, H2a, H2b, H3a, H3b, E2, E1, F, I, A, B, D, C; 1A/1/1B/1C existentes).
- SUBTOTAL por type y GRAND TOTAL de 568.61 LF.
- Todo en inglés.

**Lo que falla:**
- En el Material Summary, 39 de 44 filas citan archivos internos (`familias_out.json`, `accesorios.py`) en vez de N/HOJA.
- En 19 filas, Board (SF) ≠ L × H × Layers (board por cara) y las alturas por cara no aparecen.
- Notas del Scope Checklist sin actualizar (ALC-06, ALC-12, ALC-13, ALC-15).
- El ID C-E1-P.1 está bajo TYPE I.

## 7. Bluebeam — PASS

- 74 PolyLineDimension (51 en A-101 y 23 en A-221), igual al número de walls del Excel (62 renglones, 74 elementos).
- Subject = type.
- Page Label A-101 / A-221 (`/PageLabels`).
- /Measure de la hoja: 1/8" = 1' y 1/2" = 1', con factor correcto.
- Depth = altura del renglón.
- Contents con TYPE · LF · H · SF · DETAIL · ID.
- La longitud geométrica de cada markup coincide con el LF de su Contents (±0.02).
- Observación: el PDF es el de rev3; el README de rev4 lo explica.

## 8. Drive — PASS

- En "JC HUNTER PROJECTS › Claude outputs › Barnes & Noble Colorado Springs › Barnes & Noble Colorado Springs - TAKE-OFF (2026-10-23)", las carpetas "FINAL FOR REVIEW rev4 (2026-10-24)" y "FINAL FOR REVIEW rev3 (2026-10-24) › Planos marcados" tienen 63 de 63 archivos con el mismo tamaño que el repo.
- Observación: `take-off-metal-frame-drywall_FINAL_v80g.zip` y `_v80h.zip` están sueltos en la raíz de la carpeta del proyecto.

## Resumen

El take-off rev4 está bien en geometría: todos los walls se re-midieron dentro del 2 %, y las cadenas de detalle, el formato de markups y la copia en Drive están correctos.

Los FAIL son de dos clases:
- **Alcance que el plano imprime y no se llevó:** W.R. en techos de restrooms, plywood del janitor (11/A-200) y soffit del Grab & Go (3/A-221). Más dos candidatos que dependen de una nota: fire-stop track y additional head track.
- **Trazabilidad del Excel:** studs y 5/8" FRT plywood sin desglose, y filas del Material Summary sin N/HOJA.

Ninguna diferencia se corrigió: el estimador decide en `COMPARATIVA_AUDITORIA.xlsx`.
