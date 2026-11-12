# POSTMORTEM DE COBERTURA — skill v81cf95 (CR City Hotel, Grand Kia, Xfinity Interquest)

Auditoría independiente, solo lectura, 12-nov-2026. Código leído en `v95/take-off-metal-frame-drywall/tools/` (compuerta_entrega.py, chequeos_biblioteca.py, subir_entrega.py, comparar_alturas.py, trazabilidad.py y tests), REGLAS_REGISTRO.json (v81cf95, 565 entradas), BIBLIOTECA_ERRORES.md, REGLAS_USUARIO_CLAUDE.md, y los TIEMPOS.md de los tres proyectos. Suite del skill: 47/47 OK (suite95.log). Todas las referencias chequeo/test del registro para estos ids existen en disco (script `chk_reg.py`); la clasificación de abajo viene de leer el código, no de los nombres.

**Criterio.** OK = hay chequeo de programa Y test que repite el error, y el chequeo revisa el fondo. WEAK = el arreglo existe pero no tiene test (registro "programa-pendiente"), o el chequeo puede pasar en vacío / sale solo en AMBER, o solo detecta la *forma* (un RFI abierto) y no el valor cargado. MISSING = solo hay regla de conducta o script del proyecto, sin chequeo en el skill.

## Resumen: 79 OK · 29 WEAK · 16 MISSING (124 renglones)

## 1. Tabla error / regla → chequeo → test → estado

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| BE-CR01 | inventario_tags ciego a types con punto (W.62) | inventario_tags.py (rc 1) | test_cf_pruebas::test_cr01_regex | OK |
| BE-CR02 | familias Type C / shaftliner / ext. sheathing / C-H faltaban | canon.py BOARD_FAM (ValueError) | test_cr02_familias | OK |
| BE-CR03 | ceiling sobre resilient channel sin sistema | canon._ceiling_rc | test_cr03_rc | OK |
| BE-CR04 | canon.py se caía con proyecto 100 % board-only | canon.py rama board-only | test_cr04_board_only (solo busca un texto en el fuente) | WEAK |
| BE-CR05 | esquinas.py sin subcanons | esquinas.revisar | test_cr05_esquinas_board_only | OK |
| BE-CR06 | un solo Subject para todo wall board-only | markups_bluebeam.py (código) | ninguno (programa-pendiente) | WEAK |
| BE-CR07 | desglose Type C / exterior no cuadraba | trazabilidad.py (código) | ninguno | WEAK |
| BE-CR08 | ALC-20 sin cement board; existing walls sin subtotal | plantilla_excel.py (código) | ninguno | WEAK |
| BE-CR09 | escala leída cruzando salto de línea | verificar_markups_excel / auditoria_entrega RX_SCALE | test_cr09_escala_rotulo + test_be_cr09b | OK |
| BE-CR10 | chequeos ciegos a existing_walls | CB.B.walls_todos | test_r80f55_multinivel | OK |
| BE-CR11 | revision_markups no leía IDs con lado | revision_markups.py (código) | ninguno | WEAK |
| BE-CR12 | altura board-only sin fuente impresa / redondeada | CE_CITA_ALTURA + CE_ALTURA_IMPRESA (indirecto) | test_tiempos_cita_sf (indirecto) | WEAK |
| BE-CR13 | comparar_extra con {value, source} | comparar_extra._num | test_be_cr13 | OK |
| BE-CR14 | lista_schedules no leía fichas.json | compuerta_entrega (código) | ninguno dedicado | WEAK |
| BE-CR15 | RFI de corner bead que el plano resuelve | CE_RFI_BARRIDO_IMPRESO (genérico); esquinas_cb.py es script del proyecto | ninguno | WEAK |
| BE-CR16 | cielo rated cargado por supuesto (schedule por LOCATION) | CB_RCP_TAGS / barrido genérico | ninguno | WEAK |
| BE-CR17 | carpeta 'vacía' = dos carpetas distintas (Drive) | conducta | — | MISSING |
| BE-CR18 | cadena_detalles no re-sembraba la cola | chequeos_biblioteca (código) | ninguno | WEAK |
| BE-CR19 | GRAND TOTAL 0 / LF por cara en board-only | plantilla_excel.py (código) | ninguno | WEAK |
| BE-CR20 | membrana del piso N olvidada en cielo de N-1 | conducta | — | MISSING |
| BE-CR21 | excluir parte de un assembly rated | CB_U_184_EXCL (regex del motivo) | u_184_excl | WEAK |
| BE-CR22 | walls sobre vanos de puerta / walls fantasma | vanos_puertas.py solo en el proyecto | — | MISSING |
| BE-CR23 | destino de burbuja fuera del set | CE_DETALLES_CIRCULADOS (código) | ninguno | WEAK |
| BE-CR24 | burbuja con cero a la izquierda | chequeos_biblioteca lstrip (código) | ninguno | WEAK |
| BE-CR25 | compuerta VERDE en vacío (walls=0) | CB.canon_no_vacio + en_vacio | test_be_cr25 | OK |
| BE-CR26 | paso escribía archivo que nadie leía | bitácora/hash (indirecto); assert solo en script del proyecto | — | WEAK |
| BE-CR27 | cement board en caras enteras; shafts en un piso | conducta (banos_cbu.py / shafts_l3l4.py del proyecto) | — | MISSING |
| BE-CR28 | subida cortada por tiempo; Excel al final | subir_entrega.empaquetar_auditoria + CE_SUBIDA_PAQUETE | test_be_cr28 | OK |
| BE-CR29 | chequeos en vacío restantes | CB be_cf04 / both_sides / en_vacio | test_be_cr29 | OK |
| BE-CR30 | tags GYP del RCP sin renglón | CB_RCP_TAGS | CASOS['rcp_tags'] | OK |
| BE-CR31 | PDF sin /VP en RCP y con /SigFlags | _sin_firmas + markups_rcp.escribir | test_be_cr31_sin_firmas | OK |
| BE-CR32 | parser tomaba la comprobación vectorial | revision_markups.altura_impresa | test_be_cr32 | OK |
| BE-CR33 | comparar_alturas: hojas con punto/guion | comparar_alturas.reglas_fisicas / cruce_cuartos | test_be_cr33_* | OK |
| BE-CR34 | 'gauge not printed' con STUD SCHEDULE impreso | CE_GAUGE_IMPRESO | test_be_cr34_gauge_impreso | OK |
| BE-150 | cuartos de RCP sin renglón | CE_RCP_CUARTOS | test_u159_u160_rcp_cuartos | OK |
| BE-151 | (CR rev15) barrido | CB_CR_R15_BARRIDO | CASOS cr_r15_barrido | OK |
| BE-152 | EXCLUDED / contorno RCP | rcp_excluded_geom_fallas / rcp_contorno_fallas | test_rev15_rcp_contorno | OK |
| BE-153 | verticales / RI / T509 / madera | rcp_verticales_fallas + cr_r16_* | CASOS cr_r16_* | OK |
| BE-154 | supuesto conservador en silencio | CB_CR_R17_SILENCIO | CASOS cr_r17_silencio | OK |
| BE-155 | ruta Windows > 260 | rutas_windows_fallas (CE_NOMBRES_ENTREGA) | test_u165_ruta_windows | OK |
| BE-156 | /NM con '/' y duplicados | nm_fallas + CE_VISTA_BLUEBEAM | test_u167_nm_unico | OK |
| BE-157 | simulación con hard links reescribió el original | _escribir / vista_csv (os.replace) | test_u167_nm_unico | OK |
| BE-158 | TIEMPOS con UTC etiquetado PST, encimado | tiempos_fallas (CE_TIEMPOS) | test_tiempos_cita_sf | OK |
| BE-159 | altura citando hoja comodín | cita_altura_fallas (CE_CITA_ALTURA) | test_tiempos_cita_sf | OK |
| BE-GK01 | deps faltantes con hook 'OK' | arranque.asegurar_deps | test_be_gk01_deps | OK |
| BE-GK02 | texto en curvas (0 caracteres) | palabras_fitz.hojas_sin_texto / capa_ocr | test_be_gk02 | OK |
| BE-GK03 | inventario con capa OCR | inventario_tags.ocr_normalizar | test_be_gk03 | OK |
| BE-GK04 | Dens Shield sin familia | canon.F_DENS | test_be_gk04_gk06 | OK |
| BE-GK05 | double_row_types fijo | canon._v65_checks | test_be_gk05_10 | OK |
| BE-GK06 | 10" stud sin familia | canon.F_10 | test_be_gk04_gk06 | OK |
| BE-GK07 | OCR no confirmado = fatal | inventario_tags.inventario | test_be_gk05_10 | OK |
| BE-GK08 | misc_items con ref duplicado | canon (ValueError) | test_be_gk05_10 | OK |
| BE-GK09 | hanger wire sin hoja del detalle | trazabilidad.aplicar | test_be_gk05_10 | OK |
| BE-GK10 | edge blocking sin hoja | trazabilidad.aplicar | test_be_gk05_10 | OK |
| BE-GK11 | B.O. por wall en deck con pendiente | comparar_alturas.reglas_fisicas | test_be_gk11 | OK |
| BE-GK12 | height_diff_reason vs B.O. | comparar_alturas.reglas_fisicas | test_be_gk12_16 | OK |
| BE-GK13 | slip track genérico | trazabilidad._por_producto | test_be_gk12_16 | OK |
| BE-GK14 | hojas sin punto | RX_HOJA_CONCRETA | test_be_gk12_16 | OK |
| BE-GK15 | etiquetas de hoja OCR re-asignadas | conducta (scripts del proyecto) | — | MISSING |
| BE-GK16 | EXCLUDED en hojas rotadas | markups_rcp.aplicar | test_be_gk12_16 | OK |
| BE-GK17 | door entre dos bandas medidas | conducta (scripts del proyecto) | — | MISSING |
| BE-GK18 | soffit en lazo cerrado = 0 LF | markups_rcp.largo_polilinea | test_be_gk18 | OK |
| BE-GK19 | closer descontaba mal el stud de nodo | closer._fallos | test_be_gk19 | OK |
| BE-GK20 | capa OCR en un proceso cortada | palabras_fitz.capa_ocr_paralelo | test_be_gk20 | OK |
| BE-GK21 | gauge_ga con texto tumbaba la compuerta | revision_materiales.comparar_type | test_be_gk21 | OK |
| BE-GK22 | DensShield en ALC-08/20 | alcances.ALCANCES | test_be_gk22_26 | OK |
| BE-GK23 | double sill track 'default' | headers.SILL_RULE_DEFAULT | test_be_gk22_26 | OK |
| BE-GK24 | conflicto declarado wall < C.H. | comparar_alturas.cruce_cuartos | test_be_gk22_26 | OK |
| BE-GK25 | CE_A2 hojas sin punto / OCR | a2_alturas | test_be_gk22_26 | OK |
| BE-GK26 | resolución 'reader B is other wall' | CB u_017 | test_be_gk22_26 | OK |
| BE-GK27 | PASS con '0 walls' | CB be_cf04 | test_be_gk22_26 | OK |
| BE-GK28 | CE_ALTURA_IMPRESA tomaba paso intermedio | revision_markups.altura_impresa | test_be_gk22_26 | OK |
| BE-GK29 | access panels cierran ALC-17 | alcances.compuerta | test_be_gk22_26 | OK |
| BE-GK30 | designación en renglones de framing | trazabilidad._por_producto | test_be_gk22_26 | OK |
| BE-GK31 | Auditoria/ desempacada (--auditoria-carpeta) | subir_entrega.subir | test_be_gk22_26 | OK |
| BE-GK32 | glass mat sheathing ext. cargado como Dens Shield tile backer | ninguno | — | MISSING |
| BE-GK33 | RFI cerrados con loaded/opciones viejos; '(open)', '[scale check]', texto cortado | ninguno | — | MISSING |
| BE-GK33b | arreglo por ID dejó textos viejos en walls hermanos | ninguno | — | MISSING |
| BE-GK34 | 1/2" EXTERIOR sheathing fuera del desglose por caras | trazabilidad.py (código) | ninguno (programa-pendiente) | WEAK |
| BE-GK35 | compuerta colgada 43 min por symlinks en ciclo | compuerta_entrega._walk_seguro/_rglob; NO en chequeos_biblioteca.desde_ctx ni reglas.py | ninguno | WEAK |
| BE-GK36 | 1000S sin reconocer; track sin designación; Proposal rev1; GUIA sin CAMBIOS | RX_GAUGE (código), revisar_proposal, guia CAMBIOS (rev15) | ninguno para 1000S | WEAK |
| BE-GK37 | fila de 6" con track que el detalle no dibuja; clip faltante | ninguno | — | MISSING |
| BE-GK38 | capa_colores sin 'prev' rompía la bitácora | comparar_alturas (bitacora.anotar) | ninguno | WEAK |
| BE-XF01 | Download All de BC falla (S3 signature) | conducta; bc_descargar.js fuera del skill | — | MISSING |
| BE-XF02 | recorte con clip sin rotar | CB_U_118 (genérico) | — | WEAK |
| BE-XF03 | CE_RCP_CUARTOS leía designadores como cuartos | rcp_cuartos_fallas | test_xf_hojas_un_decimal | OK |
| BE-XF04 | BE-CF04 en vacío sin madera | CB be_cf04 | test_xf_hojas_un_decimal | OK |
| BE-XF05 | hojas de un decimal | RX_HOJA_CONCRETA / ce_a2 | test_xf_hojas_un_decimal | OK |
| BE-XF06 | CC-R12 sin walls de largo y altura impresos | CB cc_r12 | test_xf_hojas_un_decimal | OK |
| BE-XF07 | LEGEND con Subject de type | subject_sin_medida_fallas | test_xf07 | OK |
| BE-XF08 | skill con 208 archivos | verificar_version.revisar_zip / revisar_indice | test_verificar_version::zip_200_bexf08 | OK |
| BE-XF09 | CE_MATERIALES_SCHEDULE AMBER con todo impreso | revision_materiales.comparar_type | test_u177_auditoria | OK |
| BE-XF10 | sección nueva sin catálogo; PASS '0 walls' | CE_REGLAS (regla sin clasificar) + U-138 | ninguno | WEAK |
| BE-AUD01 | verde de otro archivo / skill viejo (CR rev18b) | CE_ENTREGA_VIGENTE + _skill_version + subir --vigente | test_u177_auditoria | OK |
| BE-AUD02 | polígono RCP con coincidencia 0.0 pasaba | CE_RCP_CONTORNO (piso 0.5); AMBER si 0 polígonos | test_u177_rcp_contorno_duro | WEAK |
| BE-AUD03 | stud/track sin gauge (Xfinity r10) | CE_MS_GAUGE | test_u177_auditoria | OK |
| BE-AUD04 | producto distinto al impreso (Xfinity r15) | CE_MS_PRODUCTO_IMPRESO | test_u177_auditoria | OK |
| BE-COORD01 | CSV Bluebeam solo con ID: 'NO WALL ID' | comparar_alturas.id_nm | test_be_coord01_ids_csv_cr | OK |
| U-159 | todo cuarto RCP con renglón o EXCLUDED | CE_RCP_CUARTOS (AMBER si 0 números de cuarto detectados) | test_u159_u160 | WEAK |
| U-160 | markup EXCLUDED dentro del cuarto | CE_RCP_CUARTOS + rcp_excluded_geom | test_u159_u160 / test_rev15_u160 | OK |
| U-161 | cuarto eléctrico: MAYOR rating; soffit en canopy = nuestro | CB_U_161 (solo detecta RFI abierto; no verifica lo cargado) | CASOS u_161 | WEAK |
| U-162 | planos primero, luego código | CB_U_155 + CE_RFI_BARRIDO_IMPRESO | CASOS u_155 | OK |
| U-163 | solo gypsum + metal en assemblies | CB_U_163 | CASOS u_163 | OK |
| U-164 | un solo RESUMEN | resumenes_fallas | test_u164 | OK |
| U-165 | ruta Windows <= 230 | rutas_windows_fallas | test_u165 | OK |
| U-166 | simular uso real | CE_USO_REAL ((5) barrido de todos los proyectos es conducta) | test_u166 | OK |
| U-167 | /NM único sin '/' | nm_fallas | test_u167 | OK |
| U-168 | protocolo final A1-A5 + CHECKLIST | CE_A1_REMEDICION (re-mide vectores) / CE_A2 / CE_CHECKLIST | test_u168_checklist | OK |
| U-169 | una sola entrega; presupuesto de horas por tamaño | ninguno (CE_TIEMPOS no compara horas vs presupuesto) | — | MISSING |
| U-170 | SF del proyecto con hoja | sf_proyecto_fallas | test_tiempos_cita_sf | OK |
| U-171 | no preguntar lo que ya sé | conducta; solo la parte 'gauge' en CE_GAUGE_IMPRESO | test_be_cr34 | WEAK |
| U-172 | regla de oro: buscar en planos, luego IBC | CB_U_155 + ce_rfi_busqueda | CASOS u_155 | OK |
| U-173 | al reanudar: seguir donde quedó + revisar addenda | ninguno | — | MISSING |
| U-174 | altura del edificio si no hay estructura impresa | CB_U_174 (solo detecta RFI abierto; no verifica la altura cargada) | CASOS u_174 | WEAK |
| U-175 | alturas a 3 lados | CE_ALTURAS_3LADOS | test_u175 | OK |
| U-176 | protocolo extremo de alturas | CE_ALTURAS_EXTREMO / comparar_alturas.controles | test_u176 | OK |
| U-177 | verde amarrado al hash; contorno; gauge; producto | CE_ENTREGA_VIGENTE / CE_RCP_CONTORNO / CE_MS_GAUGE / CE_MS_PRODUCTO | test_u177_* | OK |
| U-178 | decisiones GK = regla sin RFI | CB_U_178 (solo RFI abierto; (5) largo inclinado no se verifica) | CASOS u_178 | WEAK |
| U-179 | corregir antes de preguntar RFI | CE_RFI_LISTO + correr() | test_u179_rfi_listo | OK |
| U-180 | presupuesto duro por ronda; 30 min sin reporte | ninguno (sin watchdog ni tope por ronda) | — | MISSING |
| U-181 | 'terminado' solo con auditoría de fondo, 0 hallazgos | CE_PROTOCOLO_3H (1) solo exige un informe fechado; no hash ni '0 abiertos' | test_u184_protocolo_3h | WEAK |
| U-182 | CSV de Bluebeam solo al final | ninguno | — | MISSING |
| U-183 | reportar solo del proyecto urgente | conducta (no programable) | — | MISSING |
| U-184 | protocolo bien a la primera 2-3 h | CE_PROTOCOLO_3H + CB_U_184_ELEV/EXCL (ver huecos) | test_u184_protocolo_3h | WEAK |

Nota de registro: BE-AUD01..04 y BE-GK33b NO tienen entrada propia en REGLAS_REGISTRO.json (van dentro de U-177 / BE-GK33). BE-GK32..36 y BE-GK38 están como "programa-pendiente" aunque GK34/35/36/38 ya tienen código en v81cf95.

## 2. Hallazgos verificados en el código (lo más grave primero)

1. **BE-GK35 se cerró solo a medias: el cuelgue por symlinks puede volver en la corrida COMPLETA.** `compuerta_entrega._walk_seguro/_rglob` ya no entran en ciclos (probado: 0.0 s). Pero `chequeos_biblioteca.B.desde_ctx` (las funciones `ult()` y el bucle de `textos`, líneas 131 y 161) y `reglas.py:175` siguen usando `glob.glob(..., recursive=True)`. En Python 3.13 eso sigue los symlinks de directorios. Lo reproduje con dos symlinks `takeoff_work` hacia el work dir: `glob.glob('**/x.json')` no termina en 15 s, y `_rglob` termina en 0.0 s. GK solo se salvó porque escondió el symlink (`.takeoff_work_rev1`; glob salta los nombres que empiezan con punto). No hay test.
2. **CB_U_184_ELEV (la regla del east eave de CR) pasa en vacío justo en CR.** Lee `b.canon.get("walls")`, no `b.walls_todos()`. Con un proyecto wood-framed (todo en `existing_walls`) devuelve `PASS '0 walls revisados'`. Lo probé con un wall cuya altura sale de una elevación (`3/A4.01`) y no tiene comprobación en planta. `en_vacio` no lo atrapa, y U-138 tampoco (los walls esperados se calculan con `canon.walls` = 0).
3. **Corridas de compuerta (U-184 (2)(7)):**
   - (b) TIEMPOS: `protocolo_3h_fallas` solo exige que exista el texto `corridas de compuerta: N`. **Nunca compara N con `compuerta_corridas.jsonl`**. El propio `test_u184_protocolo_3h` escribe `corridas de compuerta: 1` con 3 corridas registradas y pasa. Además, `main()` escribe el renglón del jsonl solo cuando `correr()` TERMINA. Una corrida colgada o cortada (la 1 y la 2 de GK) nunca queda registrada, así que el conteo automático también habría dado 8 y no 10. **SIN GUARDA.**
   - (c) `>2` corridas finales = FAIL para proyectos con primera subida posterior a `FECHA_U184` (o sin subir todavía): **sí**. Pero "final" quiere decir "mismo sha de Excel y de PDF". Las 10 corridas de GK fueron sobre archivos distintos (una cadena nueva en cada ronda), así que el chequeo (4) habría dado PASS. El total por rev y las corridas ROJAS solo salen como `info`. **WEAK.**
   - Tampoco hay "modo rápido por paso" (U-184 (2)): `correr(..., solo=)` existe, pero `main()` no lo expone (no hay `--solo` ni `--paso`).
4. **(d) No hay guarda de cuelgue ni de tiempo en la compuerta.** No hay `signal.alarm`, watchdog, timeout por chequeo ni tiempo por chequeo en ENTREGA_OK.json. El único timeout es el subprocess de reglas.py en CE_REGLAS (1800 s). Un chequeo colgado bloquea la corrida sin límite y sin decir cuál fue. **SIN GUARDA** (solo el arreglo parcial de ciclos).
5. **(a) subir_entrega.py no parte la subida en tramos ni la retoma sola.** Sube archivo por archivo en serie, con un `subprocess` de `gdrive_fetch put` por archivo (~13 archivos/min en GK). No tiene tope de tiempo ni checkpoint, y `SUBIDA_OK.json` se escribe solo al final. Si se vuelve a correr a mano, sí retoma (R80f.42: mismo nombre + mismo tamaño = ya subido). Pero nada la relanza antes del límite de 2 h de la tarea en segundo plano. Además, BE-GK31 (`--auditoria-carpeta`, Auditoria/ desempacada) **revirtió la mitigación de BE-CR28**: GK rev2 subió 2,502 archivos sueltos, el tramo 1 se cortó a los 121 min y el tramo 2 tuvo que retomarse. **WEAK** (retoma manual), **SIN GUARDA** para los tramos de menos de 2 h y para la retoma automática.
6. **U-169 / U-180 (presupuesto de horas) no tiene programa.** La regla dice que "CE_TIEMPOS reporta horas vs presupuesto", pero `ce_tiempos`/`tiempos_fallas` solo validan el formato (filas encimadas, Duración, TOTAL). No leen hojas A ni SF, no calculan el presupuesto (3/6/12 h) y no avisan al pasar 60 % o 100 %.
7. **U-181 "terminado" sin auditoría de fondo:** CE_PROTOCOLO_3H (1) acepta CUALQUIER archivo de Auditoria/ cuyo nombre coincida con `RX_AUDITORIA_U181` y que tenga una fecha anterior a la primera subida. No exige el hash de la entrega auditada (U-177) ni "0 hallazgos abiertos". Un informe con 36 hallazgos pasa igual.
8. **U-161 / U-174 / U-178 solo revisan la forma.** Dan FAIL si hay un RFI abierto sobre el tema, pero no comprueban que el valor cargado sea el de la regla: el rating MAYOR, la altura del edificio de A0.1, el gauge SFIA, C.H.+6", el largo inclinado real (U-178 (5)). Si no hay RFI, pasan aunque el número esté mal.
9. **Vacíos en AMBER:** CE_RCP_CONTORNO da AMBER "sin PDF de markups" / "sin polígonos de cielo". CE_RCP_CUARTOS da AMBER "ninguna hoja RCP con números de cuarto" (es el caso de un set con texto en curvas sin capa OCR, como GK). Ninguno trae un conteo que el auditor U-138 pueda marcar, así que la entrega sale VERDE.
10. **Tests débiles o faltantes:** test_cr04 solo busca un texto dentro del código fuente. BE-CR06/07/08/11/14/18/19/23/24 y BE-GK34/35/36(1000S)/38 tienen el arreglo en el código y ninguna prueba de regresión. Un cambio futuro los puede reabrir sin que la suite lo vea.

## 3. Causas de horas perdidas y su guarda

| # | causa (evidencia) | horas | guarda existente | estado |
|---|---|---|---|---|
| 1 | CR: 19 revisiones; auditorías U-138 y revisiones del usuario DESPUÉS de cada entrega (rev2-rev19, TIEMPOS CR) | ~31 h de 36.8 | CE_PROTOCOLO_3H (1) auditoría fechada antes de la 1.ª subida | WEAK: no exige 0 hallazgos ni el hash auditado; nada limita ni cuenta las revN |
| 2 | Reglas nuevas aplicadas a entregas ya hechas (CR rev14-rev19, GK R2.11 skill v81cf92→v81cf94) | CR ~12 h; GK ~40 min | U-180 (4) / FECHA_U184 = AMBER para entregas viejas | WEAK: solo en CE_PROTOCOLO_3H; `candado_ordenes` (BE-CF27) corre recién en subir_entrega, así que el skill viejo se descubre al final |
| 3 | Reruns de compuerta: GK 10 en rev2 (3 rojas, 2 cortadas, 1 colgada); CR rev19 9 | GK ~2.5 h | CE_PROTOCOLO_3H (4) | WEAK: solo cuenta las corridas con el mismo hash; las cortadas/colgadas no se registran; sin modo rápido por paso |
| 4 | Cuelgue de 43 min en `compuerta_entrega.py detalles` (BE-GK35) | 0.8 h | _walk_seguro / _rglob | WEAK: chequeos_biblioteca.desde_ctx y reglas.py siguen con glob recursivo; sin watchdog; sin test |
| 5 | Subidas cortadas por el límite de 2 h: CR rev2 2,093 archivos 172 min; GK rev2 2,502 archivos 121 min + tramo 2 | CR ~3 h; GK ~2.2 h | BE-CR28 Auditoria.zip; retoma por nombre+tamaño | WEAK: BE-GK31 desempaca Auditoria/ y anula BE-CR28; sin tramos de menos de 2 h, sin retoma automática, sin `put` en lote; SIN GUARDA del tamaño de Auditoria/ |
| 6 | Alturas corregidas tarde: GK 6b (84 min) DESPUÉS del canon; CR rev19 (329 min) alturas U-175/176 al final | GK 1.4 h; CR 5.5 h | CE_PROTOCOLO_3H (2) pide H-A/H-B en la fila de lecturas de TIEMPOS | WEAK: solo busca el texto 'lectura… H-A… H-B' en TIEMPOS, no la hora de los CSV contra la hora del canon |
| 7 | Rondas de re-verificación de la auditoría U-181 (GK 6 rondas, R2.3-R2.12), arreglos por ID (BE-GK33b) | ~2.5 h | ninguna | SIN GUARDA: no hay barrido global de textos viejos ('(open)', '[scale check]', texto cortado) ni chequeo de loaded/opciones de RFI cerrados |
| 8 | Arreglos a mano fuera de la cadena (CR rev18b) | — | CE_PROTOCOLO_3H (3) sello + bitácora; CE_ENTREGA_VIGENTE | OK |
| 9 | Revisión independiente después del armado (GK 6c 131 min, en serie) | 2.2 h | U-184 (1) conducta | SIN GUARDA de programa (nada verifica que corra en paralelo con 7-8) |
| 10 | Paso 7-10 de GK = 240 min (Excel + markups + compuerta + subida en una fila) | 4 h | ninguna | SIN GUARDA: TIEMPOS no separa compuerta y subida ni da el tiempo por chequeo |
| 11 | Ninguna alarma de presupuesto (CR 36.8 h vs 12; GK 18.3 h vs 12) | — | U-169 / U-180 conducta | SIN GUARDA |
| 12 | Conteo de corridas mal escrito a mano (GK: 9 vs 10) | — | — | SIN GUARDA (ver hallazgo 3) |

## 4. Arreglos propuestos (archivo + función)

**Tiempo / proceso**
- `chequeos_biblioteca.py::B.desde_ctx` (`ult` y el bucle de `textos`) y `reglas.py` (búsqueda `hits = glob.glob(... "**" ...)`): reemplazar por `compuerta_entrega._rglob` (o una copia `_rglob` en un módulo común `rutas_seguras.py`). Test nuevo `test_be_gk35_ciclos`: dos symlinks en ciclo, `CB.B.desde_ctx` y `reglas` terminan en menos de 5 s.
- `compuerta_entrega.py::correr`: watchdog por chequeo (`signal.alarm` o hilo con timeout, por ejemplo 300 s, y FAIL "chequeo colgado: <id>"), más `segundos` por chequeo en ENTREGA_OK.json. Test con un chequeo falso que duerme.
- `compuerta_entrega.py::main`: escribir en `compuerta_corridas.jsonl` un renglón `{"evento":"inicio"}` ANTES de `correr()` y otro de `fin` después. `corridas_compuerta` cuenta los inicios (cortadas y colgadas incluidas).
- `compuerta_entrega.py::protocolo_3h_fallas`: (5) N de TIEMPOS != número de inicios en el jsonl de la rev = FAIL. (4) total de corridas de la rev > 4, o ROJAS > 2, = FAIL "reportar causa", además del criterio por hash. Exponer `--solo CE_x,CB_y` / `--paso N` en `main()` (modo rápido U-184 (2)). Ampliar `test_u184_protocolo_3h` con el caso GK (TIEMPOS 9, jsonl 10 = FAIL).
- `compuerta_entrega.py::protocolo_3h_fallas` (1): el informe U-181 debe nombrar el sha256 del Excel/PDF auditado (= el vigente o el de la corrida anterior de la cadena) y la línea `abiertos: 0`; si no, FAIL.
- `compuerta_entrega.py::ce_tiempos`: presupuesto U-169 por hojas A (set_texto) → 3/6/12 h. TOTAL > 100 % = FAIL salvo línea "causa: …" (y AMBER > 60 %). Test con CR (2208 min vs 720).
- `subir_entrega.py::subir`: tope `--max-min 100` que deja `SUBIDA_PARCIAL.json` (lista de lo subido) y sale con rc 3. Un wrapper `subir_entrega.py --continuar` relanza hasta terminar, cada tramo de menos de 2 h. Subir en paralelo (pool de 4–8) o con `gdrive_fetch put` en lote. Con > UMBRAL archivos, `--auditoria-carpeta` sube el zip PRIMERO y desempaca después (lo vigente nunca queda a medias). Test: GDRIVE_FETCH falso que tarda, el corte y la retoma no duplican.
- `subir_entrega.py::candado_ordenes` → llamarlo también al inicio de `compuerta_entrega.correr` (AMBER "skill sin U-xxx del remoto") para que el cambio de skill se vea antes de la ronda y no en la subida (GK R2.11).
- `compuerta_entrega.py::protocolo_3h_fallas` (2): comparar el mtime/`ts` de `ALTURAS_IMPRESAS_A/B.csv` contra la primera entrada de canon.py en `bitacora.jsonl`. Si las alturas ciegas son posteriores al canon = FAIL (GK 6b, CR rev19).

**Fondo**
- `chequeos_biblioteca.py::u_184_elev`: usar `b.walls_todos()` (walls + existing_walls). Test con el wall del east eave de CR rev19 en existing_walls.
- `chequeos_biblioteca.py` nuevo `be_gk33_textos_viejos`: barrido de TODO string del canon / rfis / celdas del Excel con `RX = r"\(open\)|\[scale check\]|\[TBD\]|…$"` y un RFI `status != open` cuyo `loaded`/`opciones` tenga "+x %" / "≈" o un delta distinto al de Review Items = FAIL. Test con GK rev2 (RFI-35 "+10 %", RFI-07 (open), A-Z3-03 [scale check]).
- `chequeos_biblioteca.py` nuevo `be_gk32_sheathing_exterior`: una cara `side/location` exterior / EIFS / sheathing cargada con familia tile backer (Dens Shield) = FAIL, y el keynote citado tiene que aparecer en el texto de su hoja con la misma palabra (glass mat). Test con C-Z3-01/02.
- `chequeos_biblioteca.py` nuevo `be_gk37_fila_detalle`: misc/track de una fila de studs cuya fuente cita un detalle donde set_texto no tiene 'TRACK' / 'RUNNER' = FAIL. Toda conexión citada como motivo ('clip', 'angle') con qty 0 = FAIL.
- `chequeos_biblioteca.py` nuevo `be_cr20_membrana`: floor/ceiling assembly listado "LEVEL N" en el canon sin renglón de membrana en los cielos de N-1 = FAIL. Y `be_cr27_stack`: SF por familia de pisos típicos con |Δ| > 10 % sin motivo = AMBER→FAIL.
- `chequeos_biblioteca.py::u_161 / u_174 / u_178`: además del RFI, verificar el valor. U-174: walls "to structure" sin altura de estructura impresa con height ≠ altura del edificio del code analysis = FAIL. U-178 (5): wall con 'VARIES'/'sloped' en la fuente sin `length_op` de geometría inclinada = FAIL. U-161: cuarto ELEC/IT con dos ratings en set_texto y el menor cargado = FAIL.
- `compuerta_entrega.py::ce_rcp_contorno` y `ce_rcp_cuartos`: si el canon tiene ceilings > 0 (o set_texto tiene hojas RCP / A3.xx) y hay 0 polígonos / 0 números de cuarto = FAIL (U-137), no AMBER. Agregar `ceilings` a `esperado_proyecto`.
- Tests de regresión para lo que ya tiene código: BE-CR06 (Subject por type board-only), CR07 (desglose Type C), CR08 (SUBTOTAL BOARD ONLY), CR11 (`'CH-L2-01 A'` en revision_markups), CR14 (fichas.json hoja/pos/stud), CR18 (re-sembrado de la cola), CR19 (GRAND TOTAL con board-only), CR23 (destino fuera del set), CR24 ('08/A9.05' = '8/A9.05'), GK34 (1/2" EXTERIOR en el desglose), GK36 (`RX_GAUGE` con 1000S162-43 y track EXT sin designación), GK38 (`capa_colores` usa bitacora.anotar con 'prev'). Rehacer test_cr04 para que corra canon.py con un canon solo-existing_walls.
- REGLAS_REGISTRO.json: agregar BE-AUD01..04 y BE-GK33b, y pasar BE-GK34/35/36/38 a "programa" con su test cuando exista.

## 5. Lo que NO se comprobó
- No corrí la compuerta completa sobre las entregas reales (solo lectura del código y pruebas sintéticas con datos de un solo caso: ciclo de symlinks, u_184_elev).
- Los CASOS de test_chequeos_biblioteca de BE-151..154 / U-161 / U-163 / U-174 / U-178 se dan por buenos según el registro; no leí cada caso.
- CR06–CR24 "pendientes": confirmé que el arreglo está en el código (grep de la marca BE-CRxx), pero no su comportamiento.
