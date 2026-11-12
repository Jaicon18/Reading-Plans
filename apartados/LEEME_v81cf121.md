# v81cf121 PUBLICADA (orden de COORDINACIÓN 12-nov 22:11; publicada por su aviso de 22:35): arreglos ESTRUCTURALES de la verificación 5

Base: v81cf120 (vigente). Aplicar con `patch -p1` desde la carpeta que contiene `take-off-metal-frame-drywall/`:
- descomprimir el zip de v81cf120 en una carpeta X;
- `cd X` y `patch -p1 < v81cf121_desde_v81cf120.patch`.
Las rutas del parche empiezan con `v120/` y `v121/`. Las órdenes van en `apartados/ordenes_v121/` (verificar_version.py + test +
REGLAS_REGISTRO.json).

Informe: cache_proyectos/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION5.md (c7f3024). Adversariales: apartados/adversariales_v120v5/.
Cada caso adversarial quedó como test (abajo). Lo que no se pudo cerrar va en "Límites".

1. BE-CR40 (`chequeos_biblioteca.faltantes_auditoria`):
   - un hallazgo se cierra SOLO con `CERRADO: <ref> (<N/HOJA>)` (también `CLOSED:`); la ref tiene que existir en el canon con
     cantidad > 0 (`_cant_ref`: misc qty, ceilings area_sf, walls length_ft, trim / blocking lf). Una ref suelta en el texto no cierra.
     `CERRADO:` sin N/HOJA o con una ref sin cantidad = FAIL;
   - `RX_HOJA_FALTANTE` salta el renglón solo si NO hay palabra de cielo (ceiling / clg / gyp-N / soffit / cielo);
   - DOBLE_CIELO.csv resuelve un cuarto solo si `upper:` Y `lower:` citan cada uno una ref cargada (ref, ceilings[N] o [N]);
     'MISSING' / '(none)' / ref inexistente = no resuelve;
   - al resolver por cuarto, un soffit cargado no es el cielo del cuarto (y al revés);
   - 'not included', 'not in canon / take-off', 'omitted' son hallazgo.
   - Tests: `test_v121_be_cr40_cierre_explicito` (J0-J3b, L0-L3) y `test_v119_be_cr40_verificacion` actualizado.
2. BE-PM04 (`verificar_version.proyectos_abiertos_cache`):
   - el CSV cierra solo la MISMA rev de la última subida: rev de `CSV_BLUEBEAM_<rev>` = rev del SUBIDA_OK más nuevo (sufijo del
     nombre o carpeta `REVn_…`); SUBIDA_OK sin rev = no se puede emparejar = abierto;
   - SUBIDA_OK*.json recursivo (`_subidas_ok`, también en `_es_proyecto` y en U-185);
   - `Comparado:` por línea, antes de norm;
   - `csv_cuadra`: miles con coma, y toda forma 'K faltantes', 'faltantes en el CSV: K', 'K markups sin pareja', 'unmatched' != 0 = abierto.
   - Test: `adv5_v121` (R0-R5c). Real: abiertos = cr_city_hotel_castle_rock, grand_kia, xfinity_interquest (= PROYECTOS_ABIERTOS.json).
3. BE-PM06 (`compuerta_entrega.paso_de_celda`): la celda de paso acepta cualquier prefijo ('Paso 1', 'Step 1', 'Steps 2-3',
   '1. Inventario', '1 Inventario', '#5', '4a'); columna de paso por encabezado (Paso / Step / # / Etapa); una hora o una duración no
   es un paso. Test: `test_v121_estructurales` (M0-M4).
4. RETRO (`compuerta_entrega.inicio_rev_info`):
   - arranque = la primera marca con la etiqueta de la rev ('rev21'); si no, en el log PROPIO de la rev, la primera marca después de la
     última marca de otra rev (otra etiqueta revN), en orden del archivo (no la mínima);
   - log ACUMULADO del proyecto (carpeta madre) sin la etiqueta de la rev = no se puede fechar = FAIL (escribir 'inicio rev<N>');
   - año imposible (< año de la rev anterior) o marcas fuera de orden (atrás > 12 h, adelante > 60 días) = FAIL.
   - Test: `test_v121_estructurales` (P1, P1b, P3, P5 + control AMBER).
5. BE-GK54 ESTRUCTURAL (`compuerta_entrega.be_gk54_fallas`): para cada wall del canon con band, toda leaf paralela a <= 14 in (+ espesor)
   ROJA citada por una exclusión, DISPUESTA (cualquier texto / disposición, también NO ES NUESTRO) o una exclusión con band, exige
   gap_proof con N/HOJA + gap medido 0 (la medida MÁS CERCANA a la palabra 'gap'). No depende de sinónimos. Test:
   `test_v121_estructurales` (K1, K2, K3); `test_be_gk54` y `test_v120_adv4` H5 cambiados (una disposición de otro tipo ya no pasa).
6. U-193 (`compuerta_entrega.norm_agente`): ids solo alfanuméricos, sin prefijo subagente / subagent / agente / agent; la GUÍA
   documenta que la identidad es DECLARADA (CE_COBERTURA = FAIL sin 'identity … declared', entregas desde FECHA_V121). XF hacer_docs ya
   lo escribe (límite 6). Test: `test_v121_estructurales` (V1-V4) y `test_v119_cobertura`.
7. U-185 (`verificar_version.revisar_postmortem`): sin 'Fecha:' = fecha del commit que agregó el archivo en git (`fecha_git`); sin git =
   FALLA; `**Fecha:**` en negritas; columna 'estado' por encabezado (columnas extra después); sin 3er argumento usa la ruta por defecto
   (CACHE_DEFECTO) y corre siempre. Test: `adv5_v121` (E1, E2, E8, git, ruta por defecto).

Validación: suite 47/47; banco 0 familias distintas (8 proyectos, tools v81cf120 vs v81cf121); reglas.py 0 sin clasificar; 199 archivos;
test_verificar_version OK (selftest con las órdenes candidatas); XF PRUEBA_ABIERTOS v121 vs v120: 228/9/0 -> 228/9/0, 0 regresiones
(apartados/PRUEBA_ABIERTOS_v81cf121_XF.json).

Lo que cambia para los proyectos abiertos (GK / CR): hallazgos cerrados con una ref suelta tienen que reescribirse con
`CERRADO: <ref> (<N/HOJA>)`; un log acumulado necesita 'inicio rev<N>' en la marca de arranque; toda disposición de una leaf paralela a
<= 14 in de un wall cargado necesita gap_proof.

Límites (se documentan, no esconden un error de CANTIDAD):
- la identidad del subagente es declarada (V6: un autor que corre sus tools fuera de bitacora.py no queda registrado);
- un 'Fecha:' copiado de la verificación anterior empata y se desempata por nombre (E5);
- una etiqueta 'rev<N>' insertada a mano en medio del log con una fecha vieja: el orden de las marcas solo se revisa desde la etiqueta.

Agregado antes de publicar (COORDINACIÓN 22:15 / 22:30 / 22:35):
8. GK H-04: 'CERRADO: EXCLUDED - <motivo impreso> (<N/HOJA>)' cierra; una fila de DOBLE_CIELO.csv con EXCLUDED + N/HOJA resuelve el
   cuarto (cualquier fila, no solo 'double'); un hallazgo con N cuartos se resuelve cuarto por cuarto (un cuarto EXCLUDED no queda
   'cargado' por el SOF de otro elemento con el mismo número). Test: test_v121_excluded_y_brief.
9. CR: CB_FALTANTES_AUDITORIA ignora BRIEF*.md / LEEME* / README* y los renglones de definición; un hallazgo nombra un cuarto, un tag,
   una hoja o una ref concreta (`es_hallazgo_concreto`). Test: test_v121_excluded_y_brief; 'corridor ceiling missing' (sin cuarto) ya no es
   hallazgo (test_v119_be_cr40_verificacion actualizado).
10. BE-GK55 (de GK, commit 005540a) unido dentro de compuerta_entrega.py (`be_gk55_fallas`, CLI `compuerta_entrega.py be_gk55 <prev>
    <new> [CAMBIOS.txt]`) por el tope de 199 archivos. Test: test_be_gk55.
Zip: skills_archivo/take-off-metal-frame-drywall_v81cf121_estructurales-verificacion5_2026-11-12.zip (199 archivos, zip -D).
verificar_version de carpeta y zip: 0 reglas faltantes; 2 fallas esperadas (post-mortem 12b hasta la verificación 6; PRUEBA_ABIERTOS solo
con XF, GK y CR se agregan).
