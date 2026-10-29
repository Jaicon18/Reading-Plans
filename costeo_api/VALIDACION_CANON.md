# Validación sin API: canon final de B&N → tools v80s → Excel, contra rev13

Regla R80e.30. No se gastó API ni se tocaron entregables o Drive.

## Cómo se corrió
- Copia en un directorio temporal de `cache_proyectos/barnes_noble/takeoff_work/` (canon `etapas/4_canon/takeoff_canon.json` + `fo_in.json`, `alcance_in.json`, `takeoff.json`, `registro.json`, `escaneo.json`). Las carpetas de evidencia se enlazaron con la misma ruta relativa.
- Cadena, solo con tools del skill v80s:
  1. `canon.py`, que corre por dentro studs, board, corridas y accesorios.
  2. `inventario.py`, `vigas_sobre_walls.py`, `framed_openings.py`, `alcance_filtro.py` y `markups_bluebeam.py`.
  3. `plantilla_excel.py armar`, que corre la compuerta `reglas.py` por dentro.
- No se corrieron los scripts del proyecto (`build_A.py`, `excel_json.py`): el canon y el `takeoff.json` se usaron tal como están.

## (1) ¿Reproduce rev13 al 100 %? **SÍ**
| Hoja | Filas rev13 / validación | Celdas distintas |
|---|---|---|
| Inputs | 30 / 30 | 0 |
| Partition Takeoff | 109 / 109 | 0 |
| Material Summary | 70 / 70 (67 renglones con Net) | **0** |
| Pending Items | 58 / 58 | 0 |
| Review Items | 2 / 2 | 0 |
| Scope Checklist | 31 / 31 | 0 |

Renglones distintos: **ninguno**. La hoja oculta `_reglas` (sello) no se comparó.

Dos hallazgos de la corrida:
1. **Compuerta de reglas: 115 fallas en el primer intento.**
   - 113 eran del entorno: imágenes de evidencia con ruta relativa `../../AUDITORIA_rev4/...` y `../../PASO12_rev6/...` que en el directorio temporal no existían.
   - Para una corrida en otro lugar, el runner debe copiar las carpetas de evidencia con su ruta relativa (o el canon debe usar rutas resolubles).
2. **Defecto real del skill v80s: la regla R80e.36 no tenía clasificación** en `reglas_clasificacion.py` (2 fallas). Corregido en la copia de trabajo del skill y re-empaquetado `take-off-metal-frame-drywall_FINAL_v80s.zip`.

## (2) Decisiones del estimador que NO salen del canon + tools
**Ninguna existe solo como edición manual del Excel.** La edición a mano de rev11 (waste no metal del blocking de madera, sticks de 16 ft) se migró en rev12. Todo sale hoy del canon, del `takeoff.json` o de los defaults de las tools.

Pero no todo está en el canon como dato. Hay tres lugares:

| Dónde vive hoy | Decisiones | Qué hace falta para una corrida automática desde una lectura nueva |
|---|---|---|
| **Canon (dato)**, escrito por el script del proyecto `build_A.py` (bloques REV1–REV13) | E1 cement board a 12'-0" (caras); H3a WD-1 15'-0" (strip + cara); FRT + FRP una cara types 3/4 (strips + misc); FRP-1 Workroom / Janitor / bajo countertop; moment clips, HUS-EZ, #10-16; corner guards 72 + 1; control joint 250; #8 en brace ends 512; #8 de 8/A-410; Teks 5/A-410, 7/A-210, 8/A-210; fascia GWB; slab pins 1 hilera (`constants.slab_pin_spacing_ft`); header de 2 piezas (`addl_head_track_min_ro_ft` = 0, `addl_head_track_pieces` = 2); conteo MEP (`mep_estimator_count`); PVC (`pvc_trim_items`); exclusiones (strip server, blocking cased opening); `anchorage other` types 3/4; `board_base_sf_by_wall`; `family_splits`; `frp_none_reason`; `acc_nombres` | El modelo de lectura NO produce estos campos solo. Hay que pasarle las decisiones como **reglas generales** (R80e.33 / R80e.34 / R80e.35) para que las escriba en el canon, o un "overlay de decisiones" (JSON por proyecto) que el runner fusione al canon antes de `canon.py` |
| **`takeoff.json` (texto)**, escrito por el script del proyecto `excel_json.py` | Pending Items "CLOSED - estimator decision" (`rfi_cierre`), textos de los RFI con sus deltas, notas del Scope Checklist (exclusiones RFI-30, 36, 50), `inputs_notas` | Lo mismo: overlay de decisiones → `rfi_cierre` / `alcances` |
| **Defaults de las tools (v80r / v80s)**: aplican a TODO proyecto | Blocking de madera = waste no metal (B6); 2x lumber 16 ft (Inputs B26); panel FRP 40 SF (B30); main tee 12 / cross tee 4 / molding 12; yields sin waste; piezas ≤ 20 sin waste | Confirmar con el estimador que son defaults generales. Si alguno es solo de B&N, pasarlo al Inputs del proyecto |

## (3) Campos mínimos del canon que debe producir el modelo en la lectura
Los números los calculan las tools; el modelo solo produce:

- **walls[]**: `id`, `tag`, `element` (wall / column_wrap / soffit_side / …), `sheet`, `page`, `band` (geometría: H / V / D / BOX con coordenadas), `length_ft` + `length_source`, `height_ft` + `height_source`, `stud_size` + `stud_source`, `oc_in`, `gauge` + `gauge_source`, `detail` (N/HOJA), `top_track` / `bottom_track` cuando difieren del type, `anchorage` cuando otro detalle ancla el track.
  - `faces[]`: `side`, `room`, `board`, `layers`, `height_ft` + `height_source`, `length_ft` si difiere.
  - `openings[]`: `ref`, `kind`, `ro_w_ft`, `head_ft`, `source`.
- **nodes[]**: `id`, `kind` (L / T / free), `walls` o `wall`, `source`.
- **ceilings[]**: `room`, `system`, `area_sf`, `board`, `height_ft`, `source` / `detail`, `perimeter_ft`.
- **plywood_strips[]**: `ref`, `wall`, `lf`, `width_ft`, `material`, `uso`, `source`.
- **blocking_items[]**: `ref`, `lf`, `material`, `source`.
- **trim_items[]**: `ref`, `kind`, `lf` o `qty`, `source`.
- **misc_items[]**: `ref`, `familia` (de FAMS), `qty`, `unit`, `source`, `op` (operación DERIVADA). Son los miembros y fasteners que imprime un detalle.
- **constants**: `plan_scale_pt_per_ft` (+ por hoja), spacing de furring / carrying / hangers / bracing, `slab_pin_spacing_ft`, `drywall_screws_per_sf`.
- **Razones "none" con N/HOJA:** `tile_base_none_reason`, `frp_none_reason` (o bloque `frp`), `edge_blocking_none_reason`, `deck_breaks_none_reason`, `accesorios_none[]`, `deflection_clips`.
- **Barrido MEP o conteo:** `mep_sweep` registrado o `mep_estimator_count`.
- **Opcionales de presentación:** `family_splits`, `acc_nombres`, `markup_label`, `details`, `opening_schedule`.

Conclusión: la cadena determinista está sana; el canon de rev13 reproduce el Excel exacto. Para el runner por API, el trabajo pendiente es:
1. Que la lectura escriba los campos de arriba con el skill completo.
2. Que las decisiones del estimador entren como overlay o regla al canon antes de `canon.py`, nunca editando el Excel.
