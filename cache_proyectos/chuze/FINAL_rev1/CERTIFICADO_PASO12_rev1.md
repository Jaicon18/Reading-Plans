# CERTIFICADO PASO 12 rev1 — Matriz de cobertura total — Chuze Fitness Austin Bluffs

Sesión independiente; planos (bidset_SIN_MARKUPS.pdf + specs) vs entregables Takeoff_rev1.xlsx / Markups_rev1.pdf; lectura permitida de CAMBIOS_rev1.md y DECISIONES_ORQUESTADOR.md. No se modificó ningún entregable. Cada cierre se verificó en el desglose del renglón (no en el texto del changelog).

**Cobertura: 1356/1356 = 100.0 %** (COVERED 323, RFI 71, EXCLUDED 962, GAP 0).

**Resultado: cobertura OK; quedan 4 FAIL de biblioteca (BE-44 marginal, BE-46, BE-55, BE-108) → no certificable hasta corregirlos.**

## Re-chequeo de los 46 ítems sin destino (12 gaps rev0)

| Gap | Destino rev1 | Cantidad rev1 | Estado |
|---|---|---|---|
| GAP-01 | MS R32 control joint | 363.93 LF | CERRADO |
| GAP-02 | MS R28 metal stud blocking + RFI-13/28 | 225.31 LF | CERRADO |
| GAP-03 | MS R31 cement backer + R25 screws + RFI-06 | 1,209.77 SF + 1,451.72 pcs | CERRADO |
| GAP-04 | MS R14 600S162-33 + R26 #10 TEK + RFI-14 | 432 LF + 972 pcs | CERRADO |
| GAP-05 | MS R13 box-header studs + R16 track | 234.2 LF + 117.1 LF | CERRADO |
| GAP-06 | MS R13 diagonal braces + RFI-35 | 16.96 LF | CERRADO |
| GAP-07 | EXCLUDED standing rule SKILL section 7 + RFI-34, ALC-X45 | 0 (delta ~1,370 LF in RFI-34) | EXCLUDED (regla) |
| GAP-08 | MS R30 metal edge + R20 cap | 44.82 LF + 11.13 SF | CERRADO |
| GAP-09 | MS R15/R13 kickers + RFI-36 | 424.23 LF | CERRADO |
| GAP-10 | MS R30 L-bead edge trim | 1,290.95 LF | CERRADO |
| GAP-11 | MS R15 studs to deck + R17 bracing | 73.98 LF + 17.73 LF | CERRADO |
| GAP-12 | MS R27 deep-leg track + R16 runners + RFI-37 | 11 LF + 10 LF | CERRADO |

Verificaciones propias: A103 — los tags 30, 36, 40, 46 solo aparecen en el schedule (sin tag en planta), los cargados (8, 18, 33, 41, 45, 48, 50, 51, 52 + straps 7, 9, 16) están en el desglose R28; corner bead 441.22 = 193.9 + 154.32 (cajas C3C) + 93 (cased); edge trim 1,335.77 = 1,290.95 + 44.82; track de ceilings 567.58 = 440.48 + 117.1 + 10. Observación (no gap): las cajas C3C A-A421-1/-2 (head C a 10.5 ft) no llevan kickers — furring sobre columna existente; conviene decirlo en RFI-36.

## Biblioteca de errores (rev1)

| Test | Resultado | Evidencia |
|---|---|---|
| BE-01 | PASS | Fire-stop / deflection head of X6D ("CONT. C SHAPED TRACK, DO NOT FASTEN TO STUD", X/A301) inside MS R9 6" top track breakdown (A-A424-7 5.37 LF); no "FIRE STOP AT CEILING LINE TYP." note in this set. |
| BE-02 | PASS | W.R. breakdown (MS R20) includes the C-5 ceilings of 105, 109, 129, 128 entry, women's corridor. |
| BE-03 | PASS | Wet-room faces (locker / restroom / janitor / laundry) in MR (MS R18) per A111 note 3; RFI-30/32. |
| BE-04 | PASS | No face without gypsum in MR / W.R. |
| BE-05 | PASS | X6D 4 layers (2/side as drawn, RFI-07); A2-3D 1 layer/side; soffit faces per "Board by face". |
| BE-06 | PASS | Soffit sides per detail with per-face board (A421.A-A425.A) + bottoms in C-5 ceilings. |
| BE-07 | N/A | No "SIM." partition tags in A101 / A421-A437. |
| BE-08 | N/A | Printed-dimension re-measure belongs to step 11; not re-run here (Bluebeam geometry = labels within 0.25 LF except 6 annotations, see cuadre). |
| BE-09 | PASS | Only infills of existing openings (A6D/A3C infill rows); existing walls excluded; RFI-23/26. |
| BE-10 | N/A | No "HOLD" dimension on trade sheets. |
| BE-11 | PASS | A1.11/A1.13 FRT plywood areas = wood EXCLUDED (ALC-10), board below 24" AFF not counted. |
| BE-12 | PASS | RFI-05 now cites 09 29 00 2.3.A / 2.3.E (exist); C-5 grid rows carry the spec Armstrong products (HD8906, XL8945P, KAM151220E). |
| BE-13 | PASS | E111 / E112 / E401 plywood backboards = EXCLUDED wood in Scope Checklist ALC-X44. |
| BE-14 | PASS | Sample of "not printed" claims verified (B.O. deck "VARIOUS"; stud gauge; S501 absent). |
| BE-15 | PASS | A502 members read with their function (soffit studs @ 24", horizontal bracing rows). |
| BE-16 | PASS | Box header (R13/R16), 6/A502 diagonal bracing (R13 + RFI-35), head F metal edge (R30), head C kickers (R15/R13 + RFI-36), 1/A506 deep-leg + runner (R27/R16 + RFI-37) loaded; Z-girt EXCLUDED by standing rule + RFI-34. Observation: C3C column boxes A-A421-1/-2 (head C at 10.5 ft) carry no kickers (furring on existing columns, laterally supported) - not stated in RFI-36. |
| BE-17 | PASS | 25/20 ga products separated; heavy-gauge screw rows = 0 with reason (600T250-54 uses printed #10 TEK). |
| BE-18 | PASS | 0 items without destination (coverage 100 %). |
| BE-19 | PASS | Slab pins @ 16" = S200 printed spacing + RFI-ACC-slab-pins. |
| BE-52 | PASS | ALC-18 points to its own control-joint row; ALC-08 no longer claims impact board (RFI-25). |
| BE-53 | PASS | RFI-12, RFI-14 deltas list the printed pieces. |
| BE-56 | PASS | One anchorage family; S200 and A301 shot pins coincide (@ 16"). |
| BE-20 | PASS | Soffit sides: studs + 2 tracks (MS R15 = 2 x LF). |
| BE-21 | PASS | DensArmor / W.R. only where A301 / elevation notes print it (RFI-30). |
| BE-22 | PASS | Jamb return 0 with citation + RFI-ACC-gypsum-board-jamb-return. |
| BE-23 | PASS | No acoustical sealant row (ALC-19). |
| BE-24 | PASS | Top = bottom track, separate rows (1,104.77 LF each). |
| BE-25 | PASS | C-5 = A121 / 09 51 23 drywall grid (RFI-08); no invented furring system. |
| BE-26 | N/A | No ballistic type. |
| BE-27 | N/A | No ATM / recess. |
| BE-28 | N/A | No canopy / new parapet (ALC-03/14). |
| BE-29 | PASS | Headers 0 + RFI-12 (steel header REF: STRUCT.). |
| BE-40 | PASS | Every Material Summary row cites a sheet; 2-1/2" stud row has its per-wall breakdown (B2E/A301); grid / hanger rows cite 5/A121. Accessory yield rows cite GA-216 / their driver rows (unchanged, acceptable). |
| BE-41 | PASS | No file names / tool names in the visible sheets (only the hidden _reglas signature). |
| BE-42 | PASS | Order A2-3D, A3C, A6C, A6D, B2E, C3C, C3D, D3G, D6F, D6G, X6D = A301 schedule; subtotals = rows; grand total 1,006.721 LF. |
| BE-43 | PASS | 6 visible sheets + hidden _reglas signature. |
| BE-44 | FAIL | Native Bluebeam measure now within tolerance on 11 of 12 subjects (soffit sides 220.23 vs 220.24 LF, RCP pages calibrated 1/4"); C3C 24.36 vs 24.54 LF (-0.73 %) and wall area -0.90 % > 0.5 %: A-A426-2 drawn 4.59 LF and A-A426-3 4.57 LF vs 4.67 LF labeled/loaded. Content labels = Excel 100 %. |
| BE-45 | PASS | All proportions in range or explained (see Proportions rev1). |
| BE-46 | FAIL | "Top / deflection track" rows still combine standard top track (heads C/F/G) and 2" slip track (heads D/E) in one row per size (R80e.95). Trim now split into corner-bead row (R29) and edge-trim row (R30). |
| BE-47 | PASS | RFI-06 / 13 / 14 / 28, ALC-08 / 16 / 18 / 20 texts match their rows (1,209.77 SF; 225.31 LF; 432 LF + 972; 9.99 LF; 363.93 LF). |
| BE-48 | PASS | Markups rev1 metadata: keywords and creator empty. |
| BE-49 | N/A | Dimension attribution belongs to step 11. |
| BE-50 | PASS | A/E/M/P overlaps carried as RFI (RFI-15 access panels, RFI-33 C-5 devices, RFI-ACC MEP). |
| BE-51 | PASS | Hanger wire by coil LF; grid pieces by stock length (Inputs B27-B29). |
| BE-54 | N/A | No S-12 / product split by face. |
| BE-55 | FAIL | Stage / rule / tool tokens removed, but Material Summary breakdowns now carry internal revision element codes "R1-BH", "R1-DB", "R1-KC", "R1-GS", "R1-BK", "R1-CB", "R1-ET", "R1-HF", "R1-TB", "R1-CJ", "R1-CC", "R1-HT" (client text; rename to plain descriptions). |
| BE-57 | PASS | Board / non-metal rows use Inputs B6 (6 %); no wood rows. |
| BE-58 | PASS | _reglas sheet: "reglas.py compuerta OK" signature present. |
| BE-59..BE-98 | N/A | Runner / canon / API process tests - not verifiable from plans + deliverables alone (step 12 scope). |
| BE-99 | N/A | Process (human take-off not used in this review). |
| BE-100 | PASS | Plans = bidset_SIN_MARKUPS.pdf. |
| BE-101 | N/A | Process. |
| BE-102 | PASS | Sheets cited in the Excel exist in the set (S001 / S501 quoted only as the plans' own missing references, RFI-18). |
| BE-103 | N/A | Vector sheets (text extractable). |
| BE-104 | PASS | B2E Z-girt EXCLUDED by standing rule (SKILL section 7 cladding / Z-girt) with RFI-34 and ALC-X45 (orchestrator decision). |
| BE-105 | PASS | Printed products now loaded (A103 metal track, cement backer, 600S162-33 curb cap, Armstrong grid); Z-girt excluded by standing rule, not by RFI alone. |
| BE-106 | PASS | Only "estimator standing rule" / labeled precedent (Inputs B26). |
| BE-107 | N/A | No fastener-exclusion order. |
| BE-108 | FAIL | Control joints and backer now follow precedent; MEP crossings still 0 (RFI-ACC-stud-reinforcement-mep: "the per-wall crossing count is not done") although precedent R80e.34 #2 says count visually: 1 plate per 16" of duct width + 1 sleeve per full-height wall crossing. |
| BE-110 | PASS | Board computed without deducting openings (A-A101-1 full). |
| BE-111 | N/A | No exterior-dimension board heights in this project. |
| BE-112 | PASS | Control-joint 30 ft rule applied (R32, 363.93 LF). |

## Proporciones (rev1)

| Chequeo | Excel | Referencia | Ratio | Resultado | Comentario |
|---|---|---|---|---|---|
| Board SF vs Sum LF x height x layers | 37,415.6 SF (MR 5,483.88 + Type X 30,456.68 + W.R. 1,475.02) | walls 36,391.6 + ceilings 1,024.0 | - | PASS | Same per-face basis as rev0 + 11.13 SF head-F cap; no opening deduction. |
| Board face height <= framing height | A-A435-1 Retail Storage segment now framed to deck (R15 R1-GS 73.98 LF, R17 17.73 LF) | 0 faces above framing | - | PASS | rev0 FAIL closed. |
| Drywall screws per SF | 44,898.70 / 37,415.6 | 1.0-1.3 | 1.20 | PASS |  |
| Cement board screws per SF | 1,451.72 / 1,209.77 | 1.0-1.5 (8" O.C. field) | 1.20 | PASS |  |
| Joint compound lb/SF | 2,693.92 / 37,415.6 | 0.05-0.08 | 0.072 | PASS |  |
| Joint tape LF/SF | 13,843.76 / 37,415.6 | 0.35-0.40 | 0.37 | PASS |  |
| Bottom = top track vs partition LF | 1,104.77 / 1,104.77 | 1,006.72 + 98.05 (A2-3D 2nd row) | 1.000 | PASS |  |
| Studs per type (field @ 16" / 24") | unchanged partitions + listed elements (box header 234.2, kickers 424.23, curb caps 432, Retail Storage 73.98, braces 16.96) | rev0 ratios 1.04-1.31 | 1.04-1.31 | PASS | elements itemized in R13 / R14 / R15 breakdowns |
| Control joints | 363.93 LF | independent estimate ~330 LF walls + soffit runs > 30 ft (A-A421.A-1 arc, A-A423.A-1) | 1.10 | PASS |  |
| C-5 perimeter molding vs perimeter | 458.91 LF (KAM151220E only) | 1 x perimeter 458.91 | 1.00 | PASS | rev0 FAIL (channel + angle) closed. |
| C-5 mains / cross tees per SF | 523.35 / 969.80 per 1,024 SF | 0.25 / 0.75 field | 0.51 / 0.95 | PASS | narrow strips (per-area operation) |
| C-5 hangers per SF | 187 / 1,024 | 1/16 SF field + perimeter | 0.18 | PASS | explained room by room |
| Ceiling / soffit track | 567.58 LF | 440.48 (2 x soffit sides) + 117.1 box-header track + 10 hatch runners | 1.00 | PASS |  |
| Corner bead | 441.22 LF | 193.9 soffit bottoms + C3C boxes 154.32 + cased openings 93 | 1.00 | PASS |  |
| Edge trim / metal edge | 1,335.77 LF | 1,290.95 faces to deck + 44.82 head F | 1.00 | PASS |  |
| Kickers head C | 424.23 LF | independent ~560 LF incl. C3C boxes A-A421-1/-2 and full rise on A-A435-1 | 0.76 | PASS | explained by RFI-36 basis (walls that stop at ceiling; column boxes braced by the column) - observation only |
| Slab pins per LF | 828.6 / 1,104.77 | 0.75 | 0.75 | PASS |  |

## Cuadre Bluebeam nativo vs Excel (rev1)

| Subject | Excel Σ L | BB Σ L | Δ % | Excel Σ Área | BB Σ Área | Δ % | Resultado |
|---|---|---|---|---|---|---|---|
| A2-3D | 98.05 | 98.08 | 0.04 | 2238.5 | 2239.3 | 0.04 | OK |
| A3C | 206.17 | 206.43 | 0.12 | 3933.5 | 3939.0 | 0.14 | OK |
| A6C | 23.83 | 23.85 | 0.08 | 465.3 | 465.7 | 0.09 | OK |
| A6D | 391.07 | 390.93 | -0.04 | 8878.3 | 8874.9 | -0.04 | OK |
| B2E | 103.96 | 103.93 | -0.02 | 2373.4 | 2372.8 | -0.02 | OK |
| C3C | 24.54 | 24.36 | -0.73 | 442.6 | 438.6 | -0.9 | FAIL |
| C3D | 44.86 | 44.91 | 0.1 | 1024.2 | 1025.2 | 0.1 | OK |
| D3G | 60.01 | 60.02 | 0.01 | 300.1 | 300.1 | 0.01 | OK |
| D6F | 22.41 | 22.44 | 0.13 | 268.9 | 269.3 | 0.13 | OK |
| D6G | 26.44 | 26.44 | -0.0 | 132.2 | 132.2 | -0.0 | OK |
| OTHER FRAMING - SOFFIT SIDE | 220.24 | 220.23 | -0.0 | 2582.0 | 2582.0 | -0.0 | OK |
| X6D | 5.37 | 5.37 | 0.0 | 122.7 | 122.7 | 0.0 | OK |

Etiquetas de contenido = Excel 100 % (97 anotaciones, 0 Wall ID faltantes / sobrantes). RCP A421.A–A425.A calibradas 1/4"; arco A-A421.A-1 dibujado (220.23 vs 220.24 LF). Único FAIL: C3C −0.73 % (A-A426-2 / -3 dibujadas 4.59 / 4.57 LF vs 4.67 LF). Metadata del PDF limpia.

## Pendiente para certificar

1. BE-44: redibujar A-A426-2 y A-A426-3 a 4.67 LF.
2. BE-46: separar top track estándar (heads C/F/G) del 2" slip track (heads D/E) por tamaño.
3. BE-55: reemplazar los códigos "R1-xx" de los desgloses por descripciones.
4. BE-108: contar a ojo los cruces MEP en walls full height (precedente R80e.34 #2) en lugar de 0 + RFI.
