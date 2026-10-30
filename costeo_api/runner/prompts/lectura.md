LECTURA {lado} — take-off de metal frame y drywall (R80e.37). Lectura INDEPENDIENTE: no abras ni busques la otra lectura.

Tu único trabajo es LEER el plano y escribir el canon JSON. NO calcules materiales, studs, board ni accesorios: lo hacen canon.py, reglas.py y plantilla_excel.py después. Aplica TODAS las reglas del SKILL.md (cargado como system prompt), incluidas R80e.* y las reglas generales R80e.33 / R80e.34, como obligatorias.

Herramientas: tienes Read / Write / Glob / Grep y python3 (pymupdf está instalado) para renderizar recortes de las hojas raster y medir vectores. Las tools del skill están en el directorio del skill (no calcules materiales con ellas).

Entradas:
- Plano (PDF): {pdf}
- Inventario por script de hojas y tags (inventario_tags.py): {inventario}

COBERTURA OBLIGATORIA: lee TODAS las hojas del trade: plantas ({plan_sheets}), RCP (A-121), secciones y detalles de walls (A-410, A-221, A-210, A-200, A-412 / A-413 / A-414), elevaciones interiores (A-225, A-226A / B), especificaciones (A-001A) y A-500. Cada type del schedule de A-410 (y de A-221) tiene walls en el canon, o va en "types_none_reason" con su N/HOJA. Incluye column wraps (element "column_wrap") y soffit sides (element "soffit_side").

ESQUEMA EXACTO: usa solo las claves del esquema canon del SKILL.md (sin claves nuevas; una traza sin números lleva sufijo "_info"). Antes de responder, valida con `python3 validar_canon.py {out} tools` (está en tu directorio): debe imprimir "CANON OK". Si imprime CANON ERROR, corrige y vuelve a validar.

Escribe {out} con estos campos mínimos:
- walls[]: id, tag, element, sheet, page (1-based, página del PDF), band (H / V / D / BOX con coordenadas en pt de la página TAL COMO SE VE, es decir rotada, igual que pymupdf page.rect: H = {{ori, c0, c1 (y de las dos caras), lo, hi (x de los extremos)}}, V = {{ori, c0, c1 (x de las caras), lo, hi (y)}}, D = {{ori, p0, p1}}, BOX = {{ori, c0, c1 (x), lo, hi (y)}}), length_ft + length_source, height_ft + height_source, stud_size + stud_source, oc_in, gauge + gauge_source, detail (N/HOJA), top_track / bottom_track si difieren del type, anchorage si otro detalle ancla el track;
  - faces[]: side, room, board, layers, height_ft + height_source (length_ft si difiere);
  - openings[]: ref, kind, ro_w_ft, head_ft, source.
- nodes[] (kind L / T / free, walls / wall, source).
- ceilings[] (room, system, area_sf, board, height_ft, perimeter_ft, source).
- plywood_strips[], blocking_items[], trim_items[].
- misc_items[] (ref, familia, qty, unit, source, op): miembros y fasteners que imprime un detalle.
- constants: escala por hoja y spacing impresos.
- Razones "none" con N/HOJA: tile_base, frp (o bloque frp), edge_blocking, deck_breaks, accesorios_none[], deflection_clips.
- mep_sweep: barrido registrado.

Cada número lleva su fuente N/HOJA (CONFIRMADO / DERIVADO con su operación / PENDIENTE). Lo no impreso va como RFI con su delta, nunca como supuesto silencioso. Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual. No abras otros directorios, repositorios, take-offs anteriores ni resultados de otras corridas.
