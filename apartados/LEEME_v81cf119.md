# v81cf119 APARTADA (NO publicada: versiones congeladas por orden de COORDINACIÓN, 12-nov)

Base: v81cf118. Aplicar: con `patch -p1` desde la carpeta que contiene `take-off-metal-frame-drywall/` (descomprimir v81cf118 en una
carpeta X, `cd X` y `patch -p1 < v81cf119_desde_v81cf118.patch`; las rutas del parche empiezan con `v118/` y `v119/`).

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


## Ampliación 2 (COORDINACIÓN 19:44 / 19:49)

- Recortes: Auditoria/ROJOS/<id>.png (muro: M-<hoja>-<n>.png; cielo: C-<hoja>-<cuarto>.png), a escala, circulados y con el número; la
  disposición acepta la columna 'reviewer' (o 'revisor'). CE_COBERTURA: rojo sin recorte = FAIL; renglón de disposición sin reviewer o
  sin imagen = FAIL. (El script de GK, scripts/recortes_rojos.py, no está en el repo; la tool ya hace lo mismo.)
- LÍMITES DOCUMENTADOS (aquí, en SKILL.md y exigidos en la GUÍA del estimador por CE_COBERTURA): (1) una sola cara faltante de un muro
  que sí tiene markup en la otra cara NO sale en rojo (CR marca A / B por cara sobre la misma línea); (2) los muros en diagonal NO se
  detectan (solo pares H / V); (3) dos cielos apilados donde falta uno los revisa CB_RCP_APILADOS, no el mapa.
- Xfinity rev1c: los 16 rojos de A2.0 los revisa un revisor independiente (subagente) sobre sus recortes -> COBERTURA_DISPOSICION.csv
  en /root/xf/work/cobertura_v119/ (listo para rev1d cuando se publique v119; la entrega no cambia antes).

- Xfinity rev1c, revisión de rojos por el revisor independiente (subagente que no hizo el take-off): 16 / 16 NO ES NUESTRO.
  - 4 W1 / W4 existentes (2/A2.0).
  - 6 pilastras existentes del storefront y 2 tramos de storefront existente (key note 11, 1/A2.0).
  - 4 NO son muros: líneas de extensión de cotas y la línea de una hoja de puerta, que el detector tomó como muros. Son falsos
    rojos = 25 % en esta hoja, lejos del <= 2 % pedido; queda anotado como límite para afinar (filtrar líneas de cota).
  - Con apartados/cobertura_v119/XF_COBERTURA_DISPOSICION.csv el mapa da 0 rojos abiertos (16 DISPUESTO).
  - Para rev1d (cuando se publique v119): la disposición y la sección 'Coverage map limits' de la GUÍA ya están preparadas
    (scripts/hacer_docs.py).


## Ampliación 3 (COORDINACIÓN 20:06): filtro de cotas, extensión y hojas de puerta

- `cob_marcas_cota` + `_cob_es_cota` (dentro de compuerta_entrega.py): no se forma un par de muro con una línea que tenga un tick de cota
  a 45° (una línea sola o un paralelogramo relleno delgado, 2.5 pt-0.75 ft) con su centro EN el cruce H / V (<= 0.4 pt, COB_TICK_TOL_PT)
  a <= 0.6 ft de su extremo, ni con la hoja de una puerta (un extremo toca el arco y el otro extremo es el centro del arco).
- Lo que se probó y se descartó (cada uno borraba muros reales cubiertos): cualquier relleno chico como tick (XF perdió 15.6 LF
  cubiertos; GK 283 LF); flechas como marca de cota (GK A111: la flecha de la línea guía de una burbuja cae en la esquina de un muro;
  GK perdió 117.6 LF cubiertos); tolerancia 0.8 pt (un pedazo de trama en una esquina de GK A113 quitaba un rojo que es muro).
  Las cotas con FLECHA quedan como límite documentado (SKILL.md y GUÍA 'Coverage map limits' punto 4).
- Disposición de muros: el id M-<hoja>-<n> es un número de secuencia que cambia si cambia el detector (este filtro renumeró XF). Desde
  ahora una disposición de muro por id vale solo con su x / y (a <= 2 ft); por id solo = no vale. Cielos siguen por número de cuarto.
  La disposición de Xfinity se re-mapeó por posición (columna id_anterior): 12 renglones, 0 rojos abiertos; los 4 renglones de los
  falsos (M-A2.0-4, -14, -17, -18 de antes) se quitaron porque el filtro ya no los saca.
- Test: test_v119_cobertura agrega 2 líneas de extensión con tick y una hoja de puerta de 3'-6" con su arco (las dos partes fallan con
  el candidato anterior y pasan con el filtro) y el caso muro-por-id sin x / y.

### Falsos rojos por proyecto (falso = lo marcado NO es un muro; revisores independientes con recortes ctx + zoom)

| Proyecto | Rojos de muro antes | Falsos antes | Rojos después | Falsos después | Quitados por el filtro | Cubiertos perdidos |
|---|---|---|---|---|---|---|
| Xfinity rev1c | 16 | 4 (25 %), todos cota / extensión / hoja | 12 | 0 (0 %) | 4 (los 4 falsos) | 0 muros reales (se fue 1 par cota + cara, 4.0 LF, imagen revisada) |
| GK rev3a | 40 | 3 (7.5 %, IC95 2.6-19.9 %) + 1 dudoso | 40 | igual: 7.5 % | 0 | 0 |
| CR rev20a | 437 | muestra 120: 9 (7.5 %, IC95 4.0-13.6 %) + 5 dudosos | 437 | igual: 7.5 % | 0 | 0 |

- GK y CR NO tienen falsos de cota / extensión / puerta en lo revisado: sus falsos son de otro tipo:
  - GK: escalera existente (borde / stringer / huellas, 3);
  - CR: equipo en el trash area (3 lados de un cuadro), vidrio de storefront (2), ventana (1), borde de losa / curb exterior (2), una
    puerta en el vano (1); dudosos: el "U" de 12" en la fachada sur repetido en cada nivel (parapet / marco, 5).
- Meta <= 2 %: se cumple en Xfinity; NO en GK ni CR (7.5 %). Para bajarlos haría falta otro filtro (equipo / escalera / storefront:
  líneas finas sin relleno ni trama), que no está en esta orden.

Archivos: cobertura_v119/revision_falsos/ (res_GK.json, res_CR1.json, res_CR2.json, cr_muestra.txt semilla 119, crops_revision.py).

- Siguiente mejora (COORDINACIÓN 20:33: NO meterla todavía): filtro de falsos de otro tipo (equipo / escalera / vidrio de storefront /
  curb: líneas finas sin relleno ni trama) para bajar GK y CR de 7.5 % a <= 2 %. Por ahora el revisor independiente los limpia.


## Ampliación 4 (COORDINACIÓN 20:10 / 20:25 / 20:33): los 5 STILL-WEAK de la verificación (a2babc8) + GK (a) (b), cada uno con test

1. U-185 (`apartados/ordenes_v119/verificar_version.py`):
   - solo cuenta `POSTMORTEM_COBERTURA_<fecha>[letra].md`;
   - sin la tabla principal = FALLA (antes pasaba en vacío);
   - los acompañantes del mismo post-mortem se leen y manda el más estricto: un `_CIERRE` o una copia nunca relajan lo que deja abierto
     el principal; de las `_VERIFICACION*` cuenta la MÁS NUEVA (hora del encabezado), así una verificación nueva limpia puede cerrar;
   - la tabla de causas (`# | causa | candado | estado`) con `NO GUARD` = abierto.
   - Test: `postmortem_u185`, ampliado con 5 casos nuevos.
   - Sobre el cache real da hoy: 12b + 12b_VERIFICACION = 10 WEAK / 3 NO GUARD abiertos. Es lo esperado: cerrar exige un post-mortem
     principal nuevo, o el 12b corregido, más una verificación limpia.
2. BE-CR40 (`chequeos_biblioteca.faltantes_auditoria` + `resolver_faltante`):
   - lee todo `.md` de `Auditoria/`;
   - el texto `faltante_por_tag:` no es prueba: la compuerta llama a la función;
   - sin tag, resuelve por número de cuarto contra ceilings / misc del canon;
   - tag ambiguo o sin tag ni cuarto = FAIL (antes N/A);
   - un hallazgo cerrado cita la ref que lo cargó (CLG- / SOF- / BW-), y esa ref tiene que existir en el canon.
   - Test: `test_v119_be_cr40_verificacion`.
   - Sobre la Auditoria real de CR rev20a contra el canon del cache: FAIL en 3 renglones.
     - Dos refs de cierre (SOF-L2-01P, CLG-L4-106R) no están en el canon del cache (es anterior a rev20).
     - El narrativo de U-138 "falta del cielo de 412" no cita su cierre.
     - CR rev20a ya está subido: este chequeo da AMBER para entregas anteriores a FECHA_V119.
3. BE-PM04 (`prueba_abiertos` + `verificar_version.revisar_prueba_abiertos`):
   - workdirs `<proyecto>=<carpeta>`;
   - las corridas de cada sesión se UNEN en el mismo `PRUEBA_ABIERTOS_vN.json`;
   - verificar_version exige, para la versión del CANDIDATO (línea `VERSION:` de su SKILL.md, no la del INDICE), todos los proyectos de
     `skills_archivo/PROYECTOS_ABIERTOS.json` con 0 regresiones sin explicar.
   - Tests: `prueba_abiertos_be_pm04` (verificar) y `test_v119_prueba_abiertos` (compuerta).
   - Propuesta de lista: `apartados/PROYECTOS_ABIERTOS_propuesta.json` (XF, GK, CR).
4. BE-PM06 (`alarma_fallas` en CE_PROTOCOLO_3H, entregas nuevas):
   - todo paso 1-9 cerrado en `tiempos.log` (`| N fin`) tiene su corrida `--paso N` en `compuerta_corridas.jsonl`;
   - el cruce del 50 % / 100 % tiene su alerta en `ALERTA_PRESUPUESTO.json` (historial con la hora del log), escrita a más tardar al
     cerrar el paso siguiente al cruce.
   - Test: `test_v119_alarma_presupuesto`, con 4 casos, uno de ellos la alerta escrita tarde.
5. U-193:
   - `_cob_disp` lee `decision`: FALTA nunca limpia un rojo; solo NO ES NUESTRO / NO ES MURO / CUBIERTO.
   - El revisor se registra con `bitacora.py subagente <rol> <id>`, en la cadena de hashes. CE_COBERTURA exige que el `reviewer` sea un
     id registrado como `revisor_cobertura` y distinto de los del canon.
   - Sin CHECKLIST con B6 = FAIL (antes, sin CHECKLIST no se revisaba).
   - RCP con 0 cuartos = detector ciego.
   - Tests nuevos de `ce_cobertura`: sin B6, B6 faltante, revisor no registrado o igual al del canon, FALTA, sin CSV, sin PDF, detector
     ciego de planta y de RCP.
   - Mutación sintética en la suite (`test_v119_mutacion_cobertura`, equivalente a la de CR):
     - sin las dos caras de un muro = ROJO;
     - sin los dos cielos apilados de un cuarto = ROJO;
     - sin una sola cara = no sale (límite documentado).
   - HALLAZGO con datos reales: "RCP con 0 cuartos" dispara en CR A3.01 / A7.30 / A7.31 y GK A220. En esas hojas los números de cuarto
     no están como texto, o están fuera del edificio. Para que la compuerta tenga una salida VERIFICABLE, hay un renglón `tipo=hoja_ciega`
     en COBERTURA_DISPOSICION.csv con:
     - decision CUBIERTO;
     - motivo;
     - nhoja N/HOJA;
     - reviewer registrado;
     - imagen.
     El revisor independiente revisó a mano todos los cielos de esa hoja. Con FALTA o con un revisor no registrado sigue en FAIL.
   - Para rev1d de Xfinity: registrar al revisor con `bitacora.py subagente revisor_cobertura <id>` y poner ese id en la columna reviewer.
6. GK (a), BE-PM08: `nombres_planos` exceptúa `COBERTURA - IMAGE ONLY.pdf`; una copia con otro nombre sigue fallando.
7. GK (b), BE-PM09: `_bitacoras` lee `$BITACORA`, `<w>/bitacora.jsonl` y `<w>/takeoff_work/bitacora.jsonl`.
   - Test de 6 y 7: `test_v119_gk_nombres_y_bitacora`.
   - Los ids BE-PM08 / 09 son nuevos porque GK ya usó BE-GK54 en su candidato aparte.

AL PUBLICAR, además:
- `apartados/ordenes_v119/BIBLIOTECA_agregar_al_publicar.md` va a `BIBLIOTECA_ERRORES.md`;
- la lista de proyectos abiertos, confirmada, va a `skills_archivo/PROYECTOS_ABIERTOS.json`;
- un solo `PRUEBA_ABIERTOS_v81cf119.json` con los 3 proyectos. GK y CR re-corren con el candidato final:
  `compuerta_entrega.py prueba_abiertos <tools v118> <salida> grand_kia=<workdir>`.

Pruebas del candidato (Ampliación 4):
- suite 47/47;
- banco 0 distintas en 8 proyectos;
- reglas.py 0 sin clasificar (borré REGLAS_FALLAS.md y reglas_out.json, que esa corrida deja en la carpeta);
- 199 archivos;
- selftest de verificar_version 13/13 OK;
- verificar_version del candidato:
  - con el CIERRE propuesto (tabla de causas 3.1-3.3 con su candado) y PRUEBA_ABIERTOS con la lista completa = OK;
  - con el cache real = FALLA U-185 (12b + 12b_VERIFICACION abiertos, como se pidió) + PRUEBA ABIERTOS (falta la lista).
- PRUEBA_ABIERTOS de Xfinity con el candidato final: 227/8/0 -> 228/9/0, 0 regresiones (apartados/PRUEBA_ABIERTOS_v81cf119.json, que es el
  archivo único al que GK y CR agregan su proyecto).

COORDINACIÓN 20:47: lista PROYECTOS_ABIERTOS confirmada (xfinity_interquest, grand_kia, cr_city_hotel_castle_rock; va a skills_archivo/ al publicar) y salida hoja_ciega aceptada. Verificación independiente final lanzada; no se publica sin su aviso.


## Ampliación 5 (COORDINACIÓN 20:54): verificación 2 (75f98d5) — 4 STILL-WEAK + BE-GK54, cada uno con su test adversarial

1. U-185 (`apartados/ordenes_v119/verificar_version.py`):
   - se leen TODAS las `_VERIFICACION*` en orden de hora;
   - un renglón abierto (en el principal, en un `_CIERRE` o en cualquier verificación) solo se cierra cuando una verificación MÁS NUEVA
     lo nombra explícitamente CONFIRMED-CLOSED; si la nueva lo omite, o dice solo 'OK', sigue abierto;
   - una `_VERIFICACION` sin tabla = FALLA;
   - la causa N de la tabla de causas se cierra con el renglón `NG-N` de la verificación.
   - Test: `postmortem_u185`, con los casos A3b (verificación nueva sin tabla), A4 (renglón omitido), 'OK' sin CONFIRMED-CLOSED y
     NG-3.1.
   - Sobre el cache real queda abierto exactamente lo de la verificación 2: U-185, NG-3.1 / BE-PM04, NG-3.3 / BE-PM06, U-193 y las
     causas 3.1 / 3.3.
2. BE-PM04:
   - `PROYECTOS_ABIERTOS.json` vacío = FALLA;
   - `proyectos_abiertos_cache`: un proyecto con `SUBIDA_OK*` desde U-157 y sin `CSV_BLUEBEAM_<rev subida>/RESULTADO.md` con
     N CSV / N PDF / N emparejados y 0 faltantes tiene que estar en la lista. Hoy son grand_kia y xfinity_interquest; CR está cerrado
     por CSV N/N y Consumer Cellular es de antes de U-157;
   - cada proyecto del PRUEBA guarda el `sha_tools` (sha256 del árbol `tools/`), que tiene que ser el del candidato. La compuerta y
     verificar_version dan el mismo sha.
   - Test: `prueba_abiertos_be_pm04` con los casos B1 (lista vacía), B2 (otro build) y el cache sintético.
   - Consecuencia: XF re-corre con el candidato final (abajo); GK y CR también.
3. BE-PM06 (CE_PROTOCOLO_3H, entregas nuevas):
   - sin `tiempos.log` = FAIL;
   - TIEMPOS.md y `tiempos.log` cuadran: una marca a la hora (y MM-DD) de cada paso 1-9 cerrado, y no menos marcas que pasos;
   - `ALERTA_PRESUPUESTO.json` y `compuerta_corridas.jsonl` los sella la compuerta en la cadena de hashes de la bitácora (renglón
     SELLO), cada vez que los escribe; si el sha actual no es el del último sello = FAIL.
   - Test: `test_v119_alarma_verificacion2`, que incluye ediciones a mano de los dos archivos y comprueba que la cadena de hashes sigue
     íntegra.
4. U-193:
   - `bitacora.py run` anota `agente` = `$SUBAGENTE_ID`, así que los autores del canon quedan registrados SOLOS;
   - CE_COBERTURA:
     - sin autores del canon registrados = FAIL;
     - solo el rol EXACTO `revisor_cobertura` cuenta como revisor (otro rol = autor);
     - el revisor no puede haber corrido ninguna tool de la cadena (etapas 2-7). Correr la compuerta o el checklist no lo vuelve autor.
   - Test: `test_v119_cobertura`.
5. BE-GK54, unido dentro de `compuerta_entrega.py` porque el tope es de 199 archivos:
   - `be_gk54_fallas` + `_gk54_desde_pdf` (la conversión con `rotation_matrix`, como el CLI de GK), con la escala de cada hoja del mapa;
   - CE_COBERTURA la llama;
   - test `test_be_gk54` con el caso real M-A111-29;
   - registro BE-GK54 en el candidato.
6. Patch: la instrucción de arriba dice exactamente `-p1` desde la carpeta que contiene `take-off-metal-frame-drywall/`.

Pruebas del candidato (Ampliación 5):
- suite 47/47. test_ciego rechazó los ids reales de GK en test_be_gk54; ahora usa valores sintéticos equivalentes y se re-corrió OK;
- banco 0 distintas en 8 proyectos;
- reglas.py 0 sin clasificar;
- 199 archivos;
- selftest de verificar_version OK.
- verificar_version:
  - (a) con el cache y el archivo reales: faltan 0 reglas (BE-GK54 ya está), U-185 abierto (lo de la verificación 2) y sin
    PROYECTOS_ABIERTOS.json — lo esperado;
  - (b) con la lista completa y el post-mortem cerrado: FALLA solo porque faltan GK y CR en la PRUEBA_ABIERTOS;
  - (c) con GK y CR simulados con el mismo sha = OK.
- PRUEBA_ABIERTOS de XF con el candidato FINAL: 227/8/0 -> 228/9/0, 0 regresiones, sha_tools igual al del candidato
  (apartados/PRUEBA_ABIERTOS_v81cf119.json).
- GK y CR: re-correr con ESTE candidato (el sha cambió) y agregarse a ese mismo archivo.
- Parche probado con la instrucción exacta (-p1 desde la carpeta que contiene take-off-metal-frame-drywall/): da el candidato idéntico.
