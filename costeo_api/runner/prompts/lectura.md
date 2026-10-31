LECTURA {lado} — take-off de metal frame y drywall (R80e.37). Lectura INDEPENDIENTE: no abras ni busques la otra lectura.

Tu único trabajo es LEER el plano y escribir el canon JSON. NO calcules materiales, studs, board ni accesorios: lo hacen canon.py, reglas.py y plantilla_excel.py después. Aplica TODAS las reglas del SKILL.md (cargado como system prompt), incluidas R80e.* y las reglas generales R80e.33 / R80e.34, como obligatorias.

Herramientas: tienes Read / Write / Glob / Grep y python3 (pymupdf está instalado) para renderizar recortes de las hojas raster y medir vectores. Las tools del skill están en el directorio del skill (no calcules materiales con ellas).

Entradas:
- Plano (PDF): {pdf}
- Inventario por script de hojas y tags (inventario_tags.py): {inventario}

COBERTURA OBLIGATORIA: lee TODAS las hojas del trade: plantas ({plan_sheets}), RCP (A-121), secciones y detalles de walls (A-410, A-221, A-210, A-200, A-412 / A-413 / A-414), elevaciones interiores (A-225, A-226A / B), ELEVACIONES Y SECCIONES DEL EDIFICIO (A-300, A-400A / A-400B: B.O. DECK impreso = altura de los walls a deck; nunca un placeholder si alguna hoja lo imprime), especificaciones (A-001A) y A-500. Cada type del schedule de A-410 (y de A-221) tiene walls en el canon, o va en "types_none_reason" con su N/HOJA. Incluye column wraps (element "column_wrap") y soffit sides (element "soffit_side").

ESCALA: constants.plan_scale_pt_per_ft {{value, source}} de la planta y band.sheet en cada band son obligatorios (sin ellos canon.py no cruza la band contra length_ft). Cada band medida debe dar el length_ft del wall; si la cota impresa y la band no cuadran, es un RFI, no un número.

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
- mep_sweep: barrido registrado; mep_sweep.sheets INCLUYE las hojas M-* y P-* del set (pipes y ductos que cruzan walls). Si no cruzan walls, igual se listan con su conteo explícito (0 cruces + motivo).

CAMPOS QUE EXIGE reglas.py (sin ellos no hay Excel):
- cada wall: detail y detail_source (N/HOJA del detalle del type); top_track = condición del top track con su N/HOJA y el gap (o to_deck_source); length_basis = base del LF declarada ("face to face" o "centerline / axis"); length_source y height_source con la cadena (cota impresa con su hoja, o B.O.D. de la zona del RCP + sección).
- wall sin tag de type: default_type_source (nota del set que fija el type por defecto) o part_of (wall con tag del que es return) o untagged_reason.
- details{{}}: una entrada por N/HOJA abierto ("2/A-410": {{source: "2/A-410", layers_per_face, layers_source, title, notes, sealant o sealant_none_reason + sealant_source}}).
- column wraps / cajas (element "column_wrap"): fos_chain {{value: [eslabones ft], source}} con TODOS los eslabones impresos (o fos_chain_faces por face si la caja es parcial) y thickness_measured_in.
- ESQUINAS Y HUECOS (R70.2 / R70.3): cada esquina L / T con UN solo dueño que cubre el cuadrado (ni doble ni sin dueño); un hueco colineal entre dos tramos es una door (su R.O. dentro del run) o va en gaps_ok con su motivo.
- diagonales (band D): band.faces_top y band.faces_bottom [[x, y], [x, y]] medidas en vector (el largo es el promedio de las dos caras).
- segmento sin tag con type por nota general: thickness_measured_in; part_of solo con un id que exista en tu canon.
- accesorios_rfi[] / rfis[]: fuentes_revisadas (designación, otra fila, regla estándar, detalle).
- R80e.50: cada RFI con opciones {{A: {{texto, source (N/HOJA), delta}}, B: {{texto, cita (código del trade), delta}}, C: ""}}, en ese orden; si el plano no responde o no hay código aplicable, la opción lo dice.
- SOFFIT SIDES (element "soffit_side", 2/A-221 y la planta A-221): TODOS los bordes del soffit (los de la línea exterior y los del escalón interior), cada uno con soffit_of, drop_line, faces (lados con board, layers y height_ft por la sección) y su height con la cadena de la sección.
- ALTURA POR CARA: la face sube hasta el ceiling del cuarto que mira (+6" si la partition note lo dice); a deck solo si el cuarto es open to structure o el detalle dice full height. El B.O. DECK es la altura del STUD, no de toda face.
- UN WALL, UNA VEZ: un wall que aparece en la planta general y en una planta ampliada (enlarged plan) se cuenta UNA sola vez, en la ampliada con su tag; la planta general no repite tramos dentro del área de la ampliada.
- NO generes imágenes: la evidencia visual (recortes con la band marcada) y los estados los genera el programa desde tus coordenadas. Tus bands deben caer sobre la línea dibujada.

Cada número lleva su fuente N/HOJA (CONFIRMADO / DERIVADO con su operación / PENDIENTE). Lo no impreso va como RFI con su delta, nunca como supuesto silencioso. Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual. No abras otros directorios, repositorios, take-offs anteriores ni resultados de otras corridas.
