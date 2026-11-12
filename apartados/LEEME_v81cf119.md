# v81cf119 APARTADA (NO publicada: versiones congeladas por orden de COORDINACIÓN, 12-nov)

Base: v81cf118. Aplicar: descomprimir v81cf118 en /tmp/v119 y
`patch -p1 -d /tmp/v119/take-off-metal-frame-drywall < v81cf119_desde_v81cf118.patch`.

## Contenido: la regla nueva del usuario (MAPA DE COBERTURA) + BE-GK53 unido

Texto del usuario (12-nov): "Una de las cosas que más me preocupan en cada proyecto es que se te vaya a pasar algún muro algún
cielo y no lo vayas a contar. ¿Hay alguna manera que podamos hacer para verificar esto de una manera rápida?"

- No hay archivo nuevo `tools/mapa_cobertura.py`: el skill está en el tope de 199 archivos. Todo va dentro de
  `tools/compuerta_entrega.py` (mapa_cobertura, cob_muros, cob_tipo_hoja, cob_estilos_muro, cob_region_edificio,
  cob_partir, ce_cobertura) y del subcomando `compuerta_entrega.py cobertura <carpeta de entrega>`.
- Muros: pares de líneas H / V paralelas a 2.5"-14" (escala /VP o /Measure de la hoja), traslape >= 2 ft, sin texto entre
  las dos líneas (tablas / notas), no una trama (líneas a la misma distancia antes y después), no una columna (caja <= 3 ft).
  Solo se cuentan los trazos con el ESTILO (color, grosor, relleno) de los muros que SÍ tienen markup en la hoja (>= 60 %
  de esos trazos bajo un markup). Si la hoja tiene pocos muros marcados, se usan los estilos del documento. La zona es el
  edificio: los trazos de muro conectados a los markups (rejilla de 2 ft) + 4 ft.
  - Cubierto = markup /Measure a <= max(0.5 ft, medio espesor + 2") del eje en >= 90 %.
  - Un muro parcialmente marcado sale con su parte ROJA aparte.
- Cielos: todo número de cuarto de un RCP dentro de un polígono de cielo con /Measure o de un EXCLUDED. Si el tag está
  afuera del cuarto, se sigue su línea guía hasta el extremo suelto.
- Clasificación de hojas:
  - planta: tiene markups de walls (Subject = type);
  - RCP: tiene polígonos de cielo / EXCLUDED;
  - plano de demolición (solo DEMO): ninguna de las dos;
  - hoja de arquitectura sin markups: se clasifica por el título de vista (FLOOR / PARTITION … PLAN, REFLECTED CEILING PLAN).
- Salida:
  - `Planos marcados/COBERTURA - IMAGE ONLY.pdf`: una página por hoja, gris claro; lo cubierto en verde tenue; lo ROJO
    grueso, circulado y numerado.
  - `Auditoria/COBERTURA.csv`.
- Disposición: `Auditoria/COBERTURA_DISPOSICION.csv` (hoja, tipo, id o x / y o zona x0, y0, x1, y1, motivo, nhoja).
  Sin N/HOJA no vale.
- CE_COBERTURA:
  - FAIL si hay un ROJO sin disposición;
  - FAIL si una planta con markups da 0 muros (detector ciego);
  - FAIL si falta el PDF / CSV;
  - FAIL si el CHECKLIST no tiene B6.
  - Entregas subidas antes de FECHA_V119 = AMBER.
- checklist_revision.py `--b6 Auditoria/COBERTURA.csv`: hoja B6 Coverage ("0 red").
- Test sintético: test_compuerta_entrega.test_v119_cobertura.
- SKILL.md: línea **VERSION: v81cf119** + párrafo de la regla.
- Registro: U-193 (programa).

## Para registrar AL PUBLICAR (no antes)

La regla y su texto van en ORDENES_DEL_USUARIO.md y en la BIBLIOTECA AL PUBLICAR. Si entraran antes, el candado BE-CF27
(órdenes U-NNN del remoto que el skill no tiene) bloquearía las compuertas de CR / GK con v118, como pasó con U-192.

## Pruebas del candidato

- Suite 47/47 (test_ciego y test_compuerta re-corridos después de reescribir dos docstrings).
- Banco 0 distintas en 8 proyectos (v118 vs v119).
- reglas.py 0 sin clasificar.
- 199 archivos.
- verificar_version OK.

## Corridas (salidas en apartados/cobertura_v119/)

| Proyecto | Tramos de muro | Muros ROJOS | Cuartos RCP | Cielos ROJOS | Tiempo |
|---|---|---|---|---|---|
| Xfinity rev1c | 21 | 16 | 5 | 0 | 3 s |
| GK rev3a | 131 | 40 | 32 | 7 | 44 s |
| CR rev20a (del Drive) | 838 | 437 | 69 | 19 | 193 s |

### Test de mutación (CR rev20a)

- Quité el muro TO-W.4-L2-02 de A2.02, las dos caras A y B: salió ROJO M-A2.02-25, de 12.99 ft.
- Quité los dos polígonos del corredor 216 de A3.02 (TO-L2 Corridor 216 '5/8 TYPE C' + TO-CLG-L2-56 GYP TYPE X): salió el
  cuarto 216 ROJO.
- Quitar solo UNA cara de un muro (CR marca A / B por cara) o solo UNO de dos cielos apilados NO sale ROJO: la otra cara /
  el otro cielo lo cubre. Eso lo revisan CB_RCP_APILADOS y el conteo de caras.


## Ampliación (post-mortem 2026-11-12b + U-193 inviolable con revisión de rojos)

- U-193 ⭐: `mapa_cobertura` deja un recorte circulado por rojo en Auditoria/ROJOS/<n>_<hoja>_<tipo>.png (columna 'imagen' del CSV); una
  disposición vale solo con decision / motivo / nhoja N/HOJA / revisor / imagen existente. Registro y SKILL.md con el texto de ORDENES
  (commit 79f518d).
- U-185 (verificar_version, en apartados/ordenes_v119/): cierre = fecha_iso de la última subida (todos los SUBIDA_OK*.json, hora completa);
  solo el post-mortem MÁS NUEVO cuenta; con hora anterior al cierre no vale. Con el 12b de hoy (7 WEAK) = FALLA; con el cierre propuesto
  (apartados/POSTMORTEM_COBERTURA_2026-11-12b_CIERRE_v81cf119.md) = OK.
- U-189 / BE-CR39: CB_RCP_APILADOS cuenta los 'double' de DOBLE_CIELO y evalúa su pila (FS / RS + GYP) contra el canon; 'double'
  declarados con 0 evaluados = FAIL; detalle_caras 'loaded' = ref exacta; cobertura_esperada con burbujas de letra (D/A301).
- U-190: CE_DOBLE_CIELO + refs_doble_fallas — cada renglón upper / lower existe en el canon (misc ref, su id base o FS-1 [k]) con
  cantidad > 0, o EXCLUDED con N/HOJA (del motivo o de la fila); mismo renglón arriba y abajo = FAIL. Sobre el DOBLE_CIELO real de CR
  rev20a (Auditoria.zip del Drive) contra el canon del cache: 2 renglones no encontrados (L2 217 'CLG-L2-217F', L3 317 'CLG-L3-317F');
  hay que confirmarlos con el canon de rev20a (el del cache puede ser de otra rev).
- BE-CR40: CB_FALTANTES_AUDITORIA (todo hallazgo 'falta / missing' de un cielo en la auditoría U-181 / U-138 se verifica con
  faltante_por_tag; algo cargado declarado faltante = FAIL; sin verificar = FAIL) + CLI `chequeos_biblioteca.py faltante`.
- BE-CR42 / BE-GK47 / BE-PM07: test_be_cr42_… se llama; verificar_version.tests_sin_llamar falla si un def test_ no se llama.
- BE-PM04 (NO GUARD 3.1): `compuerta_entrega.py prueba_abiertos <tools vigente> <salida> <workdirs…>`; verificar_version exige
  skills_archivo/PRUEBA_ABIERTOS_<vigente>.json con ok (desde v81cf119). Corrido sobre Xfinity rev1c (v118 -> v119): 227/8/0 -> 228/9/0,
  0 regresiones (apartados/PRUEBA_ABIERTOS_v81cf119_XF.json). CR rev20a y GK rev3a: sus carpetas de trabajo no están en esta sesión; lo
  corren sus sesiones (o COORDINACIÓN) con la misma orden antes de publicar.
- BE-PM05 (NO GUARD 3.2): VERSION_PROYECTO.txt (`compuerta_entrega.py version_proyecto <workdir> --rev revN [--causa …]`); en
  CE_PROTOCOLO_3H (entregas nuevas): sin archivo / otra versión / cambio sin causa = FAIL.
- BE-PM06 (NO GUARD 3.3): `--paso` escribe ALERTA_PRESUPUESTO.json al 50 % / 100 % (tiempos.log vs U-169); > 100 % exige 'causa:' y
  'plan:' (entregas nuevas).
- Gating: CB_RCP_APILADOS, CB_DETALLE_CARAS, CB_FALTANTES_AUDITORIA, CE_COBERTURA y los renglones de DOBLE_CIELO -> AMBER en entregas
  subidas antes de FECHA_V119.
- Pruebas: suite 47/47; banco 0 distintas en 8 proyectos; reglas.py 0 sin clasificar; 199 archivos; verificar_version (candidato, con el
  post-mortem 12b cerrado) OK; con el 12b de hoy = FALLA U-185 (como se pidió).

AL PUBLICAR: copiar apartados/ordenes_v119/*.py a .claude/skills/jc-hunter-ordenes/, el registro, el cierre del post-mortem (si COORDINACIÓN
lo confirma) y skills_archivo/PRUEBA_ABIERTOS_v81cf119.json con los 3 proyectos.
