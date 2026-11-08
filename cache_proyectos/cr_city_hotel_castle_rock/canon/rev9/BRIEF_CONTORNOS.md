# Brief rev9 — contorno REAL de cielos (CR City Hotel)  — leer completo

## Objetivo
Cada cielo cuantificado necesita su polígono MEDIDO EN VECTORES del PDF (caras interiores de los walls), no bbox / localizador /
caja de walls / polígono escalado. El área del polígono es una medición [DERIVADO] y se compara con el SF cargado.

## Datos
- PDF: /root/cr/work/plans/bidset_SIN_MARKUPS.pdf (página = índice de la hoja en list(json.load(open('/root/cr/work/set_texto.json'))['hojas']) + 1;
  A2.01=17, A2.02=18, A2.03=19, A2.04=20, A3.01=22 ... A3.04=25). Unidades PDF: pt. Escala de plantas A2/A3 1/8" = 9 pt/ft -> SF = pt²/81.
  Ampliadas: ver canon constants.plan_scale_by_sheet (A6.0x 18 pt/ft -> /324; A7.xx 1/4" = 18 pt/ft).
- Canon: /root/cr/work/etapas/4_canon/takeoff_canon.json (SOLO LECTURA: no lo escribas). ceilings[] (room, area_sf, source),
  misc_items[] (ref, familia, qty, op, source), walls[] + existing_walls[] (id, sheet, path / paths = ejes en coords de la hoja, location).
- Polígonos actuales: /root/cr/work/etapas/6_markups/rcp_polys.json (para ver dónde está cada cosa; causa = cómo se hizo).
- Offsets planta->RCP (A2.0x -> A3.0x, pt): /root/cr/work/etapas/6_markups/offset_plan_rcp.json (L1 13.7/8.7, L2 13.1/19.5, L3 13.3/18.7, L4 13.2/18.7).
- Herramienta: /root/cr/work/scripts/contorno_cielos.py (importable): medir(hoja, [{"num","sf"}], G=14) = flood sobre los walls del canon
  (sin W.4) desde la etiqueta del cuarto + ajuste de cada borde a la cara interior dibujada; lineas(page, fitz.Rect) = líneas H/V del PDF;
  imagen(hoja, resultados, png, clip). Para listar caras: python3 -I -W ignore /tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/clg/lineas.py <pag> x0 y0 x1 y1 [minlen].
  Ejecuta python siempre con -I -W ignore. Scripts tuyos en /root/cr/work/etapas/4_canon/rev9/ (nombre con tu grupo).

## Hallazgo ya medido (aplica a tu trabajo)
El SF impreso de las unidades en A2.0x NO es consistente: en 201-206 / 208 excluye el bath (contorno - caja exterior del bath ≈ impreso, 202:
333.27 - 64.33 = 268.94 vs 269), en 207 / 212 / 213 lo incluye (212: 389.55 vs 390). Por eso:
- L2 / L3 FS-1 (membrana rated continua sobre el bath, decisión ya documentada): el cielo = CONTORNO COMPLETO de la unidad (caras interiores de
  demising / corridor / exterior; restar solo chases / shafts que interrumpen el cielo). Reporta también contorno - bath y con cuál definición
  cuadra el impreso (±2 %).
- L4 RS-1 'excl. bath' (el bath lleva GYP-1 8'-6"): cielo = contorno - caja del bath (polígono con hueco como keyhole: un solo anillo).
- Si una medición no cuadra con nada (>2 % de impreso y de impreso+bath), NO la fuerces: repórtala con imagen y causa.

## Reglas
- Cada número: [CONFIRMADO] cota impresa citando hoja · [DERIVADO] con su operación · [PENDIENTE]. Nunca a ojo: coordenadas de líneas vectoriales.
- Polígono ortogonal en coords de la hoja donde lo mides (normalmente A2.0x, o la ampliada A6/A7 si el cielo se midió ahí); indica la hoja.
- Evidencia: PNG por cuarto o por grupo con el polígono en rojo sobre el plano (y el bath en azul) en /root/cr/work/etapas/4_canon/img/rev9/<grupo>_*.png.
  ÁBRELA y verifica que el contorno siga las caras antes de entregar.
- No toques ningún archivo fuera de tu salida; no subas nada; no git.

## Salida (un JSON por grupo): /root/cr/work/etapas/4_canon/rev9/contornos_<grupo>.json
{"<clave exacta: ceilings[].room o misc id>": {"sheet": "A2.03", "polygon": [[x,y],...]  (o "polygons": [[...],[...]] si son piezas,
  o "lines": [[[x,y],[x,y]],...] para soffits lineales), "area_sf": n, "bath": [[x,y]x4] | null, "bath_sf": n, "contorno_menos_bath_sf": n,
  "sf_cargado": n, "sf_impreso": n|null, "cuadra_con": "impreso excl. bath" | "impreso incl. bath" | "cargado" | "NO CUADRA",
  "err_pct": n, "metodo": "caras: N y=.. (DW.4 face) / S .. / W .. / E ..; chase restado ..", "nhoja": "1/A2.03", "img": "/root/.../x.png",
  "nota": "..."}}
Responde al final con una tabla corta: clave | área medida | cargado | impreso | cuadra_con | err %, y la lista de lo que NO cuadra con su causa.
