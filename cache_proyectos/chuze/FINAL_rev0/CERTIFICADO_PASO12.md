# CERTIFICADO PASO 12 — Matriz de cobertura total (plano → Excel) — Chuze Fitness Austin Bluffs rev0

Sesión independiente; solo planos (bidset_SIN_MARKUPS.pdf, 76 hojas del trade G/AD/A/S + specs 05 40 00, 09 22 16, 09 29 00, 09 51 23; la 09 21 16 no existe en el project manual) y entregables (Takeoff_rev0.xlsx, Markups_rev0.pdf). No se modificó ningún entregable.

**RESULTADO: BLOQUEADO** — cobertura 96.6 % (< 100 %), biblioteca con FAIL, 2 proporciones FAIL, cuadre Bluebeam nativo FAIL.

## (a) Cobertura

| Estado | Ítems |
|---|---|
| COVERED (renglón del Excel) | 281 |
| RFI (Pending Items) | 71 |
| EXCLUDED con motivo | 958 |
| **GAP (sin destino válido)** | **46** |
| Total | 1,356 |

Cobertura = 1,310 / 1,356 = **96.6 %** (exigido 100 %). Extracción: bloques de texto de las 76 hojas del trade (fitz), leyendas de keynotes partidas por código, notas generales partidas por número, títulos de detalle, tags por type y párrafos de spec (Partes 2-3); clasificación por reglas + revisión visual de A301, A502, A506, A602, A131, A435. Detalle ítem por ítem en MATRIZ_COBERTURA.xlsx › Matrix.

### Ítems sin destino (bloquean la entrega)

| Gap | Hoja / detalle | Qué falta | Estimado |
|---|---|---|---|
| GAP-01 | A010 GN 27; elevation GN 5 (A421.B-A437.A); A121 RCP GN 6; spec 09 29 00 2.6.A.2.f | No control-joint row. Scope Checklist ALC-18 says control joints are inside MS R26 "METAL trim" 193.90 LF, but that breakdown is only corner bead at soffit bottoms (BE-52). Precedent R80e.34 #8: ASTM C840 <= 30 ft, both faces, wall height. | ~330 LF of control joint (8 walls > 30 ft: A-A422-5, A-A426-6, A-A435-1, A-A422-1, A-A427-2, A-A427-3 (2 joints), A-A427-6, A-A429-3; joints x face height x faces); C-5 ceilings: 0 (no run > 30 ft) |
| GAP-02 | A103 Wall Backing Schedule keys 1, 8, 18, 33, 36, 40, 41, 45, 46 (CONT MTL TRACK 6 x 16 GA), keys 7, 9, 16, 30 (WOOD OR MTL STRAP); 12/13 A505.B "PROVIDE HORIZONTAL STUD" | RFI-13 says "LOADED: millwork run length per elevation" and RFI-28 "backing loaded at the wall top, 9.99 LF", but ALC-16 says 0 LF and the Material Summary has no backing row. Printed product left only as RFI (BE-105). | ~250-400 LF of 6" 16 ga track (9 tags, 1-3 rows each, run = millwork length on the cited elevation) + #10-16 screws; metal strap per tag (count) |
| GAP-03 | A301 type notes (all types); elevation GN 14 / 15; A503.C 10-12; spec 09 29 00 2.5 | RFI-06 says "LOADED: 5/8" cement backer board behind all tile" but ALC-20 says "not loaded as a separate row"; no backer row and no cement-board screws. Precedent R80e.34 #15: backer to highest tile + 6". | ~1,500 SF (range 1,200-1,900): 5'-0" wainscot on ~250 LF of locker / restroom / shower faces + full-height shower faces (A424 / A425) + Family Restroom T-24 wet wall, smoothie T-6/T-21, drinking fountain T-23 |
| GAP-04 | 2/A131 RTU curb cap (A131 leaders) | RFI-14 says "LOADED: 9 curb caps, size PENDING" but no Material Summary row exists (600S162-33, #10 TEK). | ~360 LF 600S162-33 (9 caps x ~40 LF, perimeter + cross members @ 12" on an assumed 4x6 ft curb) + ~1,000 #10 TEK; 0 if the landlord roofer carries it (RFI-14 alt.) |
| GAP-05 | 6, 7, 13, 15/A502 (called on A424.A, A425.A, A423.A, A422.A) | soffit_side rows load studs @ 24" + 2 ceiling tracks only; the box header drawn at the bottom of each headwall is not quantified, no RFI. | ~234 LF 6" 20 ga stud (2 pieces x 117.1 LF: A-A424.A-1 5.33, A-A425.A-2 5.0, A-A424.A-3 15.94, A-A423.A-1 77.5, A-A422.A-1 13.33) + up to 234 LF track if the ceiling-track row is not the header track |
| GAP-06 | 6/A502 (A424.A-1, A425.A-2) | No diagonal brace pieces; MS R16 carries only horizontal C.R. channel rows for these soffits. | ~6 braces x ~8-10 ft = ~50-60 LF 6" 20 ga stud |
| GAP-07 | B/A301 INTERIOR FURRING PARTITION TYPE B (B2E); spec 09 22 16 2.2.G / 3.2.F | B2E rows carry 2-1/2" studs and tracks only; no Z-furring row, no RFI (RFI-32 covers the 2" stud size only). BE-104: type with two systems must load both. | ~1,370 LF Z-furring (60 members @ 24" O.C. per spec 3.2.F x 22.83 ft on 103.96 LF of B2E) + ~690 PAF @ 24" |
| GAP-08 | F/A301 HEAD DETAIL (F) - type D6F (A-A429-6, A-A429-7) | Head F trim and board over the top of the D6F walls not in MS R26 / board breakdown. | ~45 LF metal edge trim (2 x 22.41 LF) + ~14 SF board over the wall top |
| GAP-09 | C/A301 HEAD DETAIL (C) (A3C, A6C, C3C walls stopping at ceiling); spec 05 40 00 3.5.G "stud kickers" | No kicker row and no RFI (RFI-21 only cites it as code backup). S sheets show no brace detail -> needs RFI with conservative load. | ~36 kickers / ~560 LF (stud or C.R. channel) on 9 head-C walls at ceiling: A-A421-15, A-A424-5, A-A424-6, A-A424-13, A-A424-14, A-A435-1, A-A421-13, A-A421-1, A-A421-2 (@ 48" O.C., 45 deg to deck 22.83 ft) |
| GAP-10 | Spec 09 29 00 3.1.C | Board faces finished to the deck in rooms open to structure have exposed top edges; no edge-trim (L-bead / J-bead) row, no exclusion, no RFI. (Sealant part = EXCLUDED.) | <= ~1,290 LF L-bead (sum of board faces running to deck, from "Board by face") |
| GAP-11 | A435 / A435.A, wall A-A435-1 (A3C) | Partition Takeoff stud height 10.5 ft for the whole wall (studs 355.98 LF) but board 5.91 x 22.83 ft on both faces of the Retail Storage segment -> board without framing above 10.5 ft. | ~75 LF 3-5/8" stud (6 studs x 12.33 ft) + ~24 LF bracing + head transition track |
| GAP-12 | A423 / A423.B keynote A2.163 "SEE DETAIL 13/A506"; 1/A506 ROOF HATCH - WALL | A506 has no detail 13 (orphan citation); 1/A506 draws the ladder wall framing. Nothing in the Excel: no row, no exclusion, no RFI. Steel ladder 3/A506 = misc. metals EXCLUDED. | ~11 LF 16 ga 4" deep-leg deflection track (hatch 2'-6" x 3'-0" perimeter) + ~5 LF 16 ga top runner; RFI on the citation |

Evidencia: 7_cobertura/img/GAP-*.png (recortes circulados).

## (b) Biblioteca de errores

PASS 31 · FAIL 17 · N/A 14 (BE-59..BE-98 = pruebas de proceso del runner, no verificables desde planos + entregables).

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
| BE-12 | FAIL | RFI-05 cites "spec 09 29 00 2.3.F" (article 2.3 has paragraphs A-E only); C-5 grid rows load USG DGLW26 / DGLW424 / DGCM27 / DGWM24 as a default while 09 51 23 prints Armstrong HD8906 / XL8945P / KAM151220E / DW90CAG / SB12P. |
| BE-13 | FAIL | E-sheet keynotes "PROVIDE 8' X 4' X 3/4" PLYWOOD BACKBOARD" (E111/E112, E401) have no row / exclusion / RFI in the Excel (wood -> should be listed EXCLUDED). |
| BE-14 | PASS | Sample of "not printed" claims verified (B.O. deck "VARIOUS"; stud gauge; S501 absent). |
| BE-15 | PASS | A502 members read with their function (soffit studs @ 24", horizontal bracing rows). |
| BE-16 | FAIL | Printed accessories without row/exclusion/RFI: A502 MTL STUD BOX HEADER, 6/A502 DIAGONAL BRACING @ 48", B/A301 Z-GIRT, F/A301 METAL EDGE, C/A301 WALL BRACING to structure, 1/A506 16 ga deep-leg track (GAP-05..09, -12). |
| BE-17 | PASS | 25/20 ga products separated; heavy-gauge screw rows = 0 with reason (600T250-54 uses printed #10 TEK). |
| BE-18 | FAIL | 12 GAP topics / 46 matrix items without valid destination (coverage 96.6 %). |
| BE-19 | PASS | Slab pins @ 16" = S200 printed spacing + RFI-ACC-slab-pins. |
| BE-52 | FAIL | ALC-18 says control joints are in MS R26 (breakdown = corner bead only); ALC-08 says impact board is "inside the board rows" (no breakdown line; RFI-25 says not loaded). |
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
| BE-40 | FAIL | Rows without N/SHEET or breakdown: MS R12 2-1/2" stud 2,009.04 LF ("default (no sheet)", no breakdown), R17/R27 hanger wire and R21-R24 grid cite "default (no sheet)" (should cite A121 C-5 / A502 / 09 51 23). |
| BE-41 | FAIL | Internal process tokens in Pending Items: "Stage 3 resolution R-29", "Stage 4 ... run mep.cruces", "Stage 5, E45", "Rule 0.F", "SKILL R55.6 / R59.9", "(E19 / E20)", "E12". |
| BE-42 | PASS | Order A2-3D, A3C, A6C, A6D, B2E, C3C, C3D, D3G, D6F, D6G, X6D = A301 schedule; subtotals = rows; grand total 1,006.721 LF. |
| BE-43 | PASS | 6 visible sheets + hidden _reglas signature. |
| BE-44 | FAIL | Content labels = Excel on all 12 subjects, but Bluebeam-native measurement fails: OTHER FRAMING - SOFFIT SIDE +117.9 % (RCP pages A421.A-A425.A calibrated "3/32 in = 1 ft" while the RCPs print 1/4"=1'-0"; A-A421.A-1 arc drawn as a 2-point chord); C3C +50.7 % (column / pier boxes drawn closed, 7.77 vs 4.77 LF). |
| BE-45 | FAIL | See Proportions: perimeter molding 2.0x (channel + angle) unexplained; A-A435-1 board above stud height. |
| BE-46 | FAIL | One row, two products: "Top / deflection track" (standard top track + 2" slip track, R80e.95); MS R26 "METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim". |
| BE-47 | FAIL | Text vs rows: RFI-13 / RFI-28 "loaded" vs ALC-16 0 LF; RFI-06 "loaded cement backer" vs ALC-20 not loaded; RFI-14 "loaded 9 curb caps" vs no row; ALC-18 control joints vs R26 breakdown; ALC-08 impact board vs RFI-25. |
| BE-48 | FAIL | Markups PDF metadata: keywords "markups_bluebeam; legend_page=107; bid_pages=106", creator "markups_bluebeam" (R80e.29 f: must be empty). |
| BE-49 | N/A | Dimension attribution belongs to step 11. |
| BE-50 | PASS | A/E/M/P overlaps carried as RFI (RFI-15 access panels, RFI-33 C-5 devices, RFI-ACC MEP). |
| BE-51 | PASS | Hanger wire by coil LF; grid pieces by stock length (Inputs B27-B29). |
| BE-54 | N/A | No S-12 / product split by face. |
| BE-55 | FAIL | Same tokens as BE-41 in client text (Pending Items). |
| BE-57 | PASS | Board / non-metal rows use Inputs B6 (6 %); no wood rows. |
| BE-58 | PASS | _reglas sheet: "reglas.py compuerta OK" signature present. |
| BE-59..BE-98 | N/A | Runner / canon / API process tests - not verifiable from plans + deliverables alone (step 12 scope). |
| BE-99 | N/A | Process (human take-off not used in this review). |
| BE-100 | PASS | Plans = bidset_SIN_MARKUPS.pdf. |
| BE-101 | N/A | Process. |
| BE-102 | PASS | Sheets cited in the Excel exist in the set (S001 / S501 quoted only as the plans' own missing references, RFI-18). |
| BE-103 | N/A | Vector sheets (text extractable). |
| BE-104 | FAIL | Type B (B2E) prints Z-GIRT + studs; only studs loaded (GAP-07). |
| BE-105 | FAIL | Printed products left only in RFI with 0 loaded: A103 6" 16 ga track (RFI-13), tile backer (RFI-06), 2/A131 600S162-33 curb cap (RFI-14); C-5 grid products replaced by USG defaults although 09 51 23 prints Armstrong. |
| BE-106 | PASS | Only "estimator standing rule" / labeled precedent (Inputs B26). |
| BE-107 | N/A | No fastener-exclusion order. |
| BE-108 | FAIL | Cases already decided by precedent left open: control joints (R80e.34 #8), MEP crossings counted visually (R80e.34 #2 vs RFI-ACC-stud-reinforcement-mep = 0), backer to finish + 6" (#15). |
| BE-110 | PASS | Board computed without deducting openings (A-A101-1 full). |
| BE-111 | N/A | No exterior-dimension board heights in this project. |
| BE-112 | FAIL | (1) control-joint 30 ft rule not applied (GAP-01). |

## (c) Proporciones

| Chequeo | Excel | Referencia | Ratio | Resultado | Comentario |
|---|---|---|---|---|---|
| Board SF vs Sum LF x height x layers (partitions + other framing) | 36,380.4 SF of walls (Partition Takeoff col H) + 1,024.0 SF ceilings = 37,404.4 SF (MS R18+R19+R20) | Sum L x D x E = 39,608.1 SF | 0.92 | PASS | Difference = per-face board heights ("Board by face": faces to ceiling + 6" vs stud to deck); no opening deduction found (A-A101-1 with door 141 = full L x H x 2). Exception: A-A435-1 board face 22.83 ft > stud height 10.5 ft = FAIL (GAP-11). |
| Board face height <= stud height (per wall) | 1 face of 105 exceeds | 0 expected | - | FAIL | A-A435-1 Retail Storage 126 segment (GAP-11). |
| Drywall screws per SF | 44,885 / 37,404.4 SF | 1.0-1.3 / SF (GA-216, 16" O.C.) | 1.20 | PASS | Inputs B20 = 1.2. |
| Joint compound lb per SF | 2,693.12 lb / 37,404.4 SF | 0.05-0.08 lb/SF (Level 4) | 0.072 | PASS | Inputs B23. |
| Joint tape LF per SF | 13,839.65 LF / 37,404.4 SF | 0.35-0.40 LF/SF | 0.37 | PASS | Inputs B24. |
| Bottom track vs partition LF | 1,104.77 LF | 1,006.72 LF partitions + 98.05 LF second stud row of A2-3D = 1,104.77 | 1.000 | PASS | A2-3D double row confirmed (A-A422-5 64.84 = 2 x 32.42). |
| Top track vs bottom track | 1,104.77 LF | = bottom track | 1.000 | PASS | Standard top track (heads C/F/G) and 2" slip track (heads D/E) share one row per size (BE-46 observation). |
| Studs vs field studs @ 16" O.C. (A2-3D) | 3,761.1 LF | (L/1.333 + 1) x rows x H = 3,494.7 | 1.08 | PASS | jambs, corners, intersections |
| Studs vs field studs (A3C) | 4,291.0 LF | 3,319.1 | 1.29 | PASS | many short walls / door jambs |
| Studs vs field studs (A6C / A6D) | 501.3 / 8,443.5 LF | 407.2 / 7,236.5 | 1.23 / 1.17 | PASS |  |
| Studs vs field studs (C3C / C3D / D3G / D6F / D6G / X6D) | 556.1 / 1,187.2 / 295.0 / 258.0 / 120.0 / 137.0 | 444.3 / 905.1 / 250.0 / 225.7 / 109.2 / 114.8 | 1.10-1.31 | PASS |  |
| Studs vs field studs (soffit sides @ 24") | 1,492.4 LF | 1,430.2 | 1.04 | PASS |  |
| 2-1/2" studs (B2E) | 2,009.04 LF | (L/1.333+1) x 22.83 = 1,894.2 | 1.06 | PASS | Ratio OK but MS R12 has no breakdown and cites "default (no sheet)" (BE-40 FAIL). |
| Slab pins per LF of bottom track | 828.6 / 1,104.77 | 0.75 / LF (@ 16", S200 schedule) | 0.75 | PASS | RFI-ACC-slab-pins. |
| Bracing C.R. channel rows | 5,372.66 LF | ROUNDUP(H x 12 / 48) - 1 rows x L (A-A421-6: 5 x 26.41 = 132.05) | 1.00 | PASS |  |
| Ceiling perimeter track vs soffit sides | 440.48 LF | 2 x soffit side LF (220.24) = 440.48 | 1.00 | PASS |  |
| C-5 hangers per SF | 187 / 1,024.0 SF | 1 per 16 SF field (4x4) + perimeter 8" rule | 0.18/SF | PASS | High, explained room by room in MS R27 (narrow strips 13-27 SF carry 6-10 hangers). |
| C-5 main tee / cross tee per SF | 523.35 / 969.80 LF per 1,024 SF | 0.25 / 0.75 LF per SF field | 0.51 / 0.95 | PASS | Explained by the per-area operation (narrow strips). |
| C-5 perimeter molding vs perimeter | 917.82 LF (channel 458.91 + angle 458.91) | 1 x perimeter = 458.91 LF (spec 09 51 23: one KAM knurled angle molding) | 2.00 | FAIL | Both channel and angle molding loaded on the full perimeter with no reason; spec prints Armstrong KAM151220E (single molding), HD8906, XL8945P, DW90CAG, SB12P; Excel loads USG DGCM27 + DGWM24, DGLW26, DGLW424. |
| Corner bead vs soffit bottoms | 193.9 LF | soffit bottom edges (A502) | 1.00 | PASS | but no control joints / head F edge / edge trim (GAP-01, -08, -10). |

## (d) Cuadre Bluebeam vs Excel por type

Etiquetas de contenido de los markups (LF / SF escritos en cada anotación): cuadran al 100 % con el Partition Takeoff en los 12 subjects (97 anotaciones, todos los Wall ID presentes, 0 faltantes / 0 sobrantes). Medición nativa de Bluebeam (largo del polyline × escala /Measure; Wall Area = Length × /Depth):

| Subject | Excel Σ Length | Bluebeam Σ Length | Δ % | Excel Σ Wall Area | Bluebeam Σ Wall Area | Δ % | Resultado |
|---|---|---|---|---|---|---|---|
| A2-3D | 98.05 | 98.08 | 0.04 | 2238.5 | 2239.3 | 0.03 | OK |
| A3C | 206.17 | 206.43 | 0.13 | 3933.5 | 3939.0 | 0.14 | OK |
| A6C | 23.83 | 23.85 | 0.08 | 465.3 | 465.7 | 0.09 | OK |
| A6D | 391.07 | 390.93 | -0.04 | 8878.3 | 8874.9 | -0.04 | OK |
| B2E | 103.96 | 103.93 | -0.02 | 2373.4 | 2372.8 | -0.02 | OK |
| C3C | 24.54 | 36.98 | 50.71 | 442.6 | 652.8 | 47.5 | FAIL |
| C3D | 44.86 | 44.91 | 0.1 | 1024.2 | 1025.2 | 0.1 | OK |
| D3G | 60.01 | 60.02 | 0.01 | 300.1 | 300.1 | -0.0 | OK |
| D6F | 22.41 | 22.44 | 0.13 | 268.9 | 269.3 | 0.14 | OK |
| D6G | 26.44 | 26.44 | -0.0 | 132.2 | 132.2 | -0.0 | OK |
| OTHER FRAMING - SOFFIT SIDE | 220.24 | 480.0 | 117.94 | 2582.0 | 5723.4 | 121.66 | FAIL |
| X6D | 5.37 | 5.37 | 0.04 | 122.7 | 122.7 | -0.03 | OK |

Causas: (1) las 11 anotaciones de soffit side en A421.A, A422.A, A423.A, A424.A, A425.A llevan escala "3/32 in = 1 ft" pero esos RCP imprimen 1/4"=1'-0" (factor 2.67); A-A421.A-1 (arco de 62.2 LF) está dibujado como cuerda de 2 puntos. (2) C3C A-A421-1/-2, A-A423-9, A-A426-2/-3: cajas dibujadas cerradas (7.77 LF) vs 4.77 LF cargados. Resto de types dentro de ±0.15 %. Metadata del PDF con keywords/creator "markups_bluebeam" (BE-48).

## Inconsistencias de texto a corregir junto con los GAP

- RFI-13 / RFI-28 dicen "LOADED" (backing) — ALC-16 y Material Summary = 0.
- RFI-06 dice "LOADED 5/8" cement backer" — ALC-20 "not loaded".
- RFI-14 dice "LOADED 9 curb caps" — no existe renglón.
- ALC-18 ubica control joints en MS R26 — el desglose es solo corner bead.
- ALC-08 "impact board inside the board rows" — RFI-25 "not loaded".
- Pending Items con tokens de proceso (Stage 3 R-29, Stage 4 mep.cruces, Stage 5 E45, Rule 0.F, SKILL R55.6/R59.9).
