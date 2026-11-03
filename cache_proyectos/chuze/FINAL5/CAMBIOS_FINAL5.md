# CAMBIOS FINAL5 - Chuze Fitness Austin Bluffs (FINAL4 -> FINAL5, 2026-11-03)

Orchestrator decision #0: drawn geometry wins over hatch-stroke extents. The 15 GWB ceilings / soffit bottoms (C-5) are measured on the RCP outlines to the room faces at each sheet's printed scale (1/4" = 18 pt/ft) and marked on their RCP sheets. Built with v81cf18 (= v81cf17 + R80f.13-R80f.15, prepared in /tmp/chuze/skill_v81cf16plus/). FINAL4 kept untouched. Walls, partitions and every other quantity unchanged (Partition Takeoff 0 differences).

## 1. Ceilings - FINAL4 loaded vs FINAL5 measured

| Id | Sheet | Ceiling | FINAL4 SF | FINAL5 SF | Delta | Outline |
|---|---|---|---|---|---|---|
| CLG-A421A-01 | A421.A | 102 CHECK-IN + 104 SMOOTHIE (reception circular GWB ceiling) | 518.00 | 505.14 | -12.86 | FINAL5 (decision #0, drawn geometry): arc r = 249.0 pt / 18 = 13.83 ft (fit of the A421.A arc vectors), chord at the wall face y 1701.6 (22.11 ft), se |
| CLG-A421A-02 | A421.A | 106 SMOOTHIE STORAGE | 73.75 | 76.49 | +2.74 | FINAL5 (decision #0, drawn geometry): room outline to the wall faces (RCP region) on A421.A at 18 pt/ft = 7.68 x 9.96 ft outline, polygon area 76.49 S |
| CLG-A421A-03 | A421.A | 105 FAMILY RESTROOM | 56.25 | 58.98 | +2.73 | FINAL5 (decision #0, drawn geometry): room outline to the wall faces (RCP region) on A421.A at 18 pt/ft = 7.68 x 7.68 ft outline, polygon area 58.98 S |
| CLG-A421A-04 | A421.A | Smoothie storage west strip (9/A502 soffit) | 13.75 | 13.31 | -0.44 | FINAL5 (decision #0, drawn geometry): strip outline to the faces (RCP region) on A421.A at 18 pt/ft = 7.68 x 1.73 ft outline, polygon area 13.31 SF, p |
| CLG-A421A-05 | A421.A | North storefront soffit west box (8'-6") | 27.40 | 6.13 | -21.27 | FINAL5 (decision #0, drawn geometry): hatched area only: soffit band y 1042.8-1048.1 + the hatched strips around the white display box 1654.6-1708.1 x |
| CLG-A421A-06 | A421.A | North storefront soffit east box (8'-6") | 20.00 | 13.70 | -6.30 | FINAL5 (decision #0, drawn geometry): soffit band drawn: storefront box bottom line y 1032.0 to the soffit edge y 1048.1, x 1722.0-1997.8 (not the lar |
| CLG-A421A-07 | A421.A | North storefront header strip (10'-0") | 12.90 | 13.07 | +0.17 | FINAL5 (decision #0, drawn geometry): strip outline (RCP region) on A421.A at 18 pt/ft = 0.84 x 15.56 ft outline, polygon area 13.07 SF, perimeter 32. |
| CLG-A422A-01 | A422.A | 109 KID'S CLUB RESTROOM | 67.20 | 67.78 | +0.58 | FINAL5 (decision #0, drawn geometry): room outline to the wall faces (RCP region) on A422.A at 18 pt/ft = 7.4 x 9.16 ft outline, polygon area 67.78 SF |
| CLG-A423A-01 | A423.A | 124 VIP north box at grid 4 (16/A502) | 22.50 | 23.65 | +1.15 | FINAL5 (decision #0, drawn geometry): box outline (RCP region) on A423.A at 18 pt/ft = 2.56 x 9.24 ft outline, polygon area 23.65 SF, perimeter 23.6 f |
| CLG-A424A-01 | A424.A | 128 MEN'S LOCKER ENTRY soffit (6/A502) | 10.67 | 10.67 | +0.00 | FINAL5 (decision #0, drawn geometry): soffit outline (RCP region) on A424.A at 18 pt/ft = 2.0 x 5.33 ft outline, polygon area 10.67 SF, perimeter 14.6 |
| CLG-A424A-02 | A424.A | 129 MEN'S SHOWER | 108.10 | 117.79 | +9.69 | FINAL5 (decision #0, drawn geometry): hatched area only: room outline minus the SE corner beyond the L-shaped wall (x 1980-2012.4, y 1659.2-1719.8, fi |
| CLG-A424A-03 | A424.A | 128 MEN'S LOCKER headwall bottom strip at shower (7/A502) | 20.10 | 22.12 | +2.02 | FINAL5 (decision #0, drawn geometry): strip outline (RCP region) on A424.A at 18 pt/ft = 1.92 x 11.52 ft outline, polygon area 22.12 SF, perimeter 26. |
| CLG-A425A-01 | A425.A | WOMEN'S CORRIDOR new portion (east of 135 WOMEN'S LOCKER) | 55.80 | 58.15 | +2.35 | FINAL5 (decision #0, drawn geometry): corridor outline to the faces (RCP region) on A425.A at 18 pt/ft = 5.01 x 11.6 ft outline, polygon area 58.15 SF |
| CLG-A425A-02 | A425.A | WOMEN'S CORRIDOR east end triangle at 6/A502 | 12.20 | 12.85 | +0.65 | FINAL5 (decision #0, drawn geometry): triangle drawn on the soffit edge: diagonal from (2006.6, 953.3) to (2106.0, 869.5), legs to the faces on A425.A |
| CLG-A426-01 | A426 | 121 STUDIO ENTRY door soffit | 5.40 | 5.45 | +0.05 | FINAL5 (decision #0, drawn geometry): soffit outline (RCP region) on A426 at 18 pt/ft = 0.84 x 6.49 ft outline, polygon area 5.45 SF, perimeter 14.67  |
| **Total** | | 15 GWB ceilings / soffit bottoms (C-5) | **1,024.02** | **1,005.28** | **-18.74** | |

Rule (audit FINAL5): the GWB ceiling = the HATCHED area only, bounded by the faces; every polygon is checked against the C-5 hatch strokes by markups_rcp.py (R80f.16, 0 parts without hatch). Storefront east box = the hatched soffit band (15.32 x 0.89 ft). Storefront west box = hatched area only: the white display box 1654.6-1708.1 x 996-1032 AND the left box 1533.1-1647.8 x 996-1042.8 carry no C-5 hatch (only fixture circles; the audit counted those circle strokes as hatch and expected 22.68) -> 6.13 SF. Women's corridor triangle = diagonal on the soffit edge, legs to the faces. 129 Men's shower: SE corner beyond the L-shaped wall (x 1980-2012.4, y 1659.2-1719.8, no hatch) excluded, hatched 1'-7" stall box kept -> 117.79 SF. Reception: drawn arc r = 13.83 ft cut at the wall face, minus the interior wall -> 505.14 SF; its angle-molding perimeter now includes both faces of that interior wall (2 x 21.66 ft measured on the A421.A vectors).

## 2. Family deltas (recomputed by the tools from area / perimeter / ns / ew of each ceiling)

| Material Summary row | FINAL4 | FINAL5 | Delta |
|---|---|---|---|
| Hanger wire | 2,428.49 LF / 2793 | 2,497.64 LF / 2873 | +69.15 |
| 5/8" gypsum board, Type X | 58,429.85 SF / 1291 | 58,393.09 SF / 1290 | -36.76 |
| 5/8" gypsum board, Type X W.R. (water resistant) | 1,475.02 SF / 33 | 1,493.04 SF / 33 | +18.02 |
| Armstrong HD8906 drywall grid main tee (heavy-duty main runner, spec 09 51 23) | 523.35 LF / 51 | 548.43 LF / 53 | +25.08 |
| Armstrong XL8945P drywall grid cross tee (spec 09 51 23) | 969.80 LF / 279 | 968.46 LF / 279 | -1.34 |
| Armstrong KAM151220E knurled angle molding at the C-5 perimeter (spec 09 51 23) | 396.71 LF / 39 | 455.36 LF / 44 | +58.65 |
| Armstrong SC151220EQ curved perimeter molding at the reception circle (spec 09 51 23) | 62.20 LF / 6 | 61.31 LF / 6 | -0.89 |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | 187.00 PCS / 187 | 192.00 PCS / 192 | +5.00 |
| Joint compound - setting-type taping and sandable topping (09 29 00 2.7.C) | 4,707.99 LB / 4708 | 4,706.64 LB / 4707 | -1.35 |
| Joint tape, paper | 24,193.84 LF / 24194 | 24,186.90 LF / 24187 | -6.94 |

Ceiling / soffit track, corner bead / trim: unchanged (they follow the soffit-side walls). Grid / hangers use the bounding dimensions of each ceiling (unchanged by the two corrections).

## 3. Markups

Chuze_AustinBluffs_Markups_FINAL5.pdf = 121 wall / element markups (as FINAL4) + 15 RCP polygons (A421.A 7, A422.A 1, A423.A 1, A424.A 3, A425.A 2, A426 1): Subject = board of the Excel row, Contents '<board> · GWB CEILING C-5 · CEILING <room> · <SF> SF · CLG <height> · <detail> · <id>', /Measure at the printed 1/4" scale, Page Label = sheet, legend per sheet; imagenes_FINAL5/ has one PNG per marked sheet incl. the 6 RCP sheets (<sheet>_rcp_markups.png).

## 4. Gates

verificar_markups_excel (v81cf18): 136 annotations, 136 OK, 0 failures, RCP sheets counted. markups_rcp hatch check (R80f.16): 0 parts without hatch. BE-117 auditoria_entrega: 0 failures. reglas.py (860 rules): only the back-check (S:§1:2fab33, the auditor registers it); plantilla validar / armar / verificar, markups verificar, markups_rcp, registro, alcances, etapas: rc 0; bitacora: back-check only.

## 5. Tool changes (v81cf18, not pushed)

R80f.13 markups_rcp.py: several RCP sheets (ceilings[].sheet), ID = ceilings[].id, ceiling tag in Contents, bracing clusters only when the set has them, legend per sheet, PNG per sheet. R80f.14 verificar_markups_excel.buscar_pdf: 'Markups' with a capital M next to the Excel. R80f.15 auditoria_entrega.py: area annots squared against the 'ID SF' breakdown and their drawn area. R80f.16 markups_rcp.py: polygon must follow the hatch (part without hatch touching the boundary = rc 1; small interior hole = opening). Tests test_rcp_multihoja.py, test_rcp_hatch.py (fail with v81cf17); suite 52/52; test_ciego_tools OK; verificar_version.py 0 missing (474).
