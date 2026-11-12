# POSTMORTEM DE COBERTURA — tabla rehecha con skill v81cf96 (U-185)

Rehecha el 12-nov-2026 sobre `POSTMORTEM_COBERTURA_2026-11-11.md` (124 renglones: 79 OK · 29 WEAK · 16 MISSING). Cada renglón WEAK / MISSING
queda **OK** (chequeo de programa + test que repite el error, en v81cf96) o **conducta: motivo** (lo que no se puede leer desde un programa,
con la parte programable nombrada). `verificar_version.py::revisar_postmortem` (U-185) falla si queda un renglón sin una de las dos.

## Resumen: 110 OK · 14 conducta con motivo · 0 WEAK · 0 MISSING (124 renglones)

## 1. Tabla error / regla → chequeo → test → estado

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| BE-CR01 | inventario_tags ciego a types con punto (W.62) | inventario_tags.py (rc 1) | test_cf_pruebas::test_cr01_regex | OK |
| BE-CR02 | familias Type C / shaftliner / ext. sheathing / C-H faltaban | canon.py BOARD_FAM (ValueError) | test_cr02_familias | OK |
| BE-CR03 | ceiling sobre resilient channel sin sistema | canon._ceiling_rc | test_cr03_rc | OK |
| BE-CR04 | canon.py se caía con proyecto 100 % board-only | canon.py rama board-only | test_cf_pruebas::test_cr04_board_only (v96: corre canon.py con un canon solo-existing_walls: rc 0, Type X = L×H×caras, sin track) | OK |
| BE-CR05 | esquinas.py sin subcanons | esquinas.revisar | test_cr05_esquinas_board_only | OK |
| BE-CR06 | un solo Subject para todo wall board-only | markups_bluebeam.py (Subject por type board-only) | test_markups_excel 'BE-CR06' (v96) | OK |
| BE-CR07 | desglose Type C / exterior no cuadraba | trazabilidad.aplicar (v96: + familia 5/8" EXTERIOR gyp sheathing Type X, bug hallado por el test) | test_traza_hojas 'BE-CR07' + 'BE-CR07 5/8 exterior' (falla con el trazabilidad de v95) | OK |
| BE-CR08 | ALC-20 sin cement board; existing walls sin subtotal | plantilla_excel.py (SUBTOTAL <tid> BOARD ONLY) | test_markups_excel 'BE-CR08' (v96) | OK |
| BE-CR09 | escala leída cruzando salto de línea | verificar_markups_excel / auditoria_entrega RX_SCALE | test_cr09_escala_rotulo + test_be_cr09b | OK |
| BE-CR10 | chequeos ciegos a existing_walls | CB.B.walls_todos | test_r80f55_multinivel | OK |
| BE-CR11 | revision_markups no leía IDs con lado | revision_markups.leer_markups (ID con lado) | test_markups_excel 'BE-CR11' (v96) | OK |
| BE-CR12 | altura board-only sin fuente impresa / redondeada | CE_CITA_ALTURA + CE_ALTURA_IMPRESA + CE_ALTURAS_3LADOS / CE_ALTURAS_EXTREMO (U-175 / U-176) | test_tiempos_cita_sf, test_comparar_alturas | conducta: la lectura de la cota impresa de un wall board-only la hace el lector; el programa ya exige cita impresa y la triple comparación de alturas |
| BE-CR13 | comparar_extra con {value, source} | comparar_extra._num | test_be_cr13 | OK |
| BE-CR14 | lista_schedules no leía fichas.json | compuerta_entrega.lista_schedules (fichas.json hoja / pos / stud) | test_hoja_sufijo::test_be_cr14_fichas (v96) | OK |
| BE-CR15 | RFI de corner bead que el plano resuelve | CE_RFI_BARRIDO_IMPRESO (RFI con texto impreso que lo resuelve = FAIL) | test_compuerta_entrega (barrido impreso) | conducta: decidir que un corner bead está dibujado en el detalle es lectura gráfica del plano; el barrido de texto impreso ya cubre el caso escrito |
| BE-CR16 | cielo rated cargado por supuesto (schedule por LOCATION) | CB_RCP_TAGS + CE_RCP_CUARTOS (v96: FAIL en vacío) | test_u159_u160_rcp_cuartos, test_p5_rcp_no_pasa_en_vacio | conducta: el rating de un cielo por LOCATION del schedule se lee en el plano; el programa exige renglón o EXCLUDED por cuarto RCP |
| BE-CR17 | carpeta 'vacía' = dos carpetas distintas (Drive) | subir_entrega.py (destino hijo de Claude outputs) | test_chuze_r80f8_11 | conducta: listar Projects y Claude outputs en Drive antes de concluir que una carpeta está vacía es acción del agente fuera de la cadena |
| BE-CR18 | cadena_detalles no re-sembraba la cola | chequeos_biblioteca.cadena_detalles (re-sembrado de la cola) | test_hoja_sufijo::test_be_cr18_cr24_cadena (v96) | OK |
| BE-CR19 | GRAND TOTAL 0 / LF por cara en board-only | plantilla_excel.py (GRAND TOTAL único al final, LF de la primera cara) | test_markups_excel 'BE-CR19' (v96) | OK |
| BE-CR20 | membrana del piso N olvidada en cielo de N-1 | CB_BE_CR20 be_cr20_membrana (v96) | test_chequeos_biblioteca CASOS be_cr20_membrana | OK |
| BE-CR21 | excluir parte de un assembly rated | CB_U_184_EXCL (exclusión solo de caras no rated) | test_chequeos_biblioteca CASOS u_184_excl | conducta: si una cara pertenece al assembly rated se decide leyendo el UL del set; el programa ya rechaza la exclusión de una cara rated declarada |
| BE-CR22 | walls sobre vanos de puerta / walls fantasma | CB_BE_CR22 be_cr22_vanos (v96; AMBER si el opening_schedule no trae posición) | test_chequeos_biblioteca CASOS be_cr22_vanos | OK |
| BE-CR23 | destino de burbuja fuera del set | compuerta_entrega.ce_detalles_circulados (destino fuera del set) | test_hoja_sufijo::test_be_cr23_destino_fuera_del_set (v96) | OK |
| BE-CR24 | burbuja con cero a la izquierda | chequeos_biblioteca (burbuja con cero a la izquierda) | test_hoja_sufijo::test_be_cr18_cr24_cadena (v96) | OK |
| BE-CR25 | compuerta VERDE en vacío (walls=0) | CB.canon_no_vacio + en_vacio | test_be_cr25 | OK |
| BE-CR26 | paso escribía archivo que nadie leía | bitácora con hash de cada archivo (CE_PROTOCOLO_3H (3)) | test_u184_protocolo_3h | conducta: un archivo intermedio que nadie lee es diseño de la cadena del proyecto; el programa ya prueba que lo entregado salió de la cadena |
| BE-CR27 | cement board en caras enteras; shafts en un piso | CB_BE_CR27 be_cr27_stack (v96: FAIL con typical_floors declarados, AMBER inferidos) | test_chequeos_biblioteca CASOS be_cr27_stack + test_v96_sin_falsos_positivos_cr | OK |
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
| BE-GK15 | etiquetas de hoja OCR re-asignadas | capa OCR para hojas con texto en curvas (BE-GK02) | test_compuerta_entrega::test_texto_set_ocr | conducta: re-asignar etiquetas de hoja necesita el sheetmap verificado a ojo de cada set; no hay fuente impresa contra la cual compararlo |
| BE-GK16 | EXCLUDED en hojas rotadas | markups_rcp.aplicar | test_be_gk12_16 | OK |
| BE-GK17 | door entre dos bandas medidas | CE_MARKUP_EN_WALL / CE_CONTORNO_REAL | test_cr_r8_markup_en_wall | conducta: una puerta entre dos bandas medidas se resuelve leyendo la planta; el programa ya prueba que cada markup cae sobre el wall dibujado |
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
| BE-GK32 | glass mat sheathing ext. cargado como Dens Shield tile backer | CB_BE_GK32 be_gk32_sheathing_exterior (v96) | test_chequeos_biblioteca CASOS be_gk32_sheathing_exterior | OK |
| BE-GK33 | RFI cerrados con loaded/opciones viejos; '(open)', '[scale check]', texto cortado | CB_BE_GK33 be_gk33_textos_viejos (v96) | test_chequeos_biblioteca CASOS be_gk33_textos_viejos | OK |
| BE-GK33b | arreglo por ID dejó textos viejos en walls hermanos | CB_BE_GK33 be_gk33_textos_viejos (barrido global, no por ID) | test_chequeos_biblioteca CASOS be_gk33_textos_viejos | OK |
| BE-GK34 | 1/2" EXTERIOR sheathing fuera del desglose por caras | trazabilidad.aplicar (1/2" EXTERIOR en el desglose) | test_traza_hojas 'BE-GK34' (v96) | OK |
| BE-GK35 | compuerta colgada 43 min por symlinks en ciclo | _rglob_seguro (chequeos_biblioteca + reglas) + watchdog correr_con_tope (v96) | test_compuerta_entrega::test_be_gk35_watchdog_y_ciclos | OK |
| BE-GK36 | 1000S sin reconocer; track sin designación; Proposal rev1; GUIA sin CAMBIOS | compuerta_entrega.RX_GAUGE / ms_gauge_fallas (1000S162-43) | test_hoja_sufijo::test_be_gk36_gauge_1000s (v96) | OK |
| BE-GK37 | fila de 6" con track que el detalle no dibuja; clip faltante | CB_BE_GK37 be_gk37_fila_detalle (v96) | test_chequeos_biblioteca CASOS be_gk37_fila_detalle + test_v96_sin_falsos_positivos_cr | OK |
| BE-GK38 | capa_colores sin 'prev' rompía la bitácora | comparar_alturas._bitacora (bitacora.anotar con 'prev') | test_hoja_sufijo::test_be_gk38_bitacora_prev (v96) | OK |
| BE-XF01 | Download All de BC falla (S3 signature) | fuera del skill (descarga de BuildingConnected) | — | conducta: la descarga del bid set ocurre antes de que corra el skill; el skill verifica el set limpio que recibe (CE_COPIA_LIMPIA) |
| BE-XF02 | recorte con clip sin rotar | CB_U_118 (imagen circulada por wall) | test_chequeos_biblioteca CASOS u_118 | conducta: que el recorte salga rotado como la hoja se ve en la imagen; el programa ya exige la imagen circulada de cada wall |
| BE-XF03 | CE_RCP_CUARTOS leía designadores como cuartos | rcp_cuartos_fallas | test_xf_hojas_un_decimal | OK |
| BE-XF04 | BE-CF04 en vacío sin madera | CB be_cf04 | test_xf_hojas_un_decimal | OK |
| BE-XF05 | hojas de un decimal | RX_HOJA_CONCRETA / ce_a2 | test_xf_hojas_un_decimal | OK |
| BE-XF06 | CC-R12 sin walls de largo y altura impresos | CB cc_r12 | test_xf_hojas_un_decimal | OK |
| BE-XF07 | LEGEND con Subject de type | subject_sin_medida_fallas | test_xf07 | OK |
| BE-XF08 | skill con 208 archivos | verificar_version.revisar_zip / revisar_indice | test_verificar_version::zip_200_bexf08 | OK |
| BE-XF09 | CE_MATERIALES_SCHEDULE AMBER con todo impreso | revision_materiales.comparar_type | test_u177_auditoria | OK |
| BE-XF10 | sección nueva sin catálogo; PASS '0 walls' | CE_REGLAS (regla / sección sin clasificar = FAIL) + auditar_compuerta (PASS '0 …' plausibilidad U-138) | test_chequeos_biblioteca::test_be_cf08_catalogo + test_compuerta_entrega::test_auditar_compuerta | OK |
| BE-AUD01 | verde de otro archivo / skill viejo (CR rev18b) | CE_ENTREGA_VIGENTE + _skill_version + subir --vigente | test_u177_auditoria | OK |
| BE-AUD02 | polígono RCP con coincidencia 0.0 pasaba | CE_RCP_CONTORNO piso 0.5 + FAIL con 0 polígonos y cielos esperados (v96 P5) | test_u177_rcp_contorno_duro + test_p5_rcp_no_pasa_en_vacio | OK |
| BE-AUD03 | stud/track sin gauge (Xfinity r10) | CE_MS_GAUGE | test_u177_auditoria | OK |
| BE-AUD04 | producto distinto al impreso (Xfinity r15) | CE_MS_PRODUCTO_IMPRESO | test_u177_auditoria | OK |
| BE-COORD01 | CSV Bluebeam solo con ID: 'NO WALL ID' | comparar_alturas.id_nm | test_be_coord01_ids_csv_cr | OK |
| U-159 | todo cuarto RCP con renglón o EXCLUDED | CE_RCP_CUARTOS (v96 P5: 0 cuartos con hojas RCP / cielos = FAIL) | test_u159_u160_rcp_cuartos + test_p5_rcp_no_pasa_en_vacio | OK |
| U-160 | markup EXCLUDED dentro del cuarto | CE_RCP_CUARTOS + rcp_excluded_geom | test_u159_u160 / test_rev15_u160 | OK |
| U-161 | cuarto eléctrico: MAYOR rating; soffit en canopy = nuestro | CB_U_161 + CB_U_161_VALOR u_161_valor (v96: rating cargado < mayor impreso = FAIL) | test_chequeos_biblioteca CASOS u_161_valor | OK |
| U-162 | planos primero, luego código | CB_U_155 + CE_RFI_BARRIDO_IMPRESO | CASOS u_155 | OK |
| U-163 | solo gypsum + metal en assemblies | CB_U_163 | CASOS u_163 | OK |
| U-164 | un solo RESUMEN | resumenes_fallas | test_u164 | OK |
| U-165 | ruta Windows <= 230 | rutas_windows_fallas | test_u165 | OK |
| U-166 | simular uso real | CE_USO_REAL ((5) barrido de todos los proyectos es conducta) | test_u166 | OK |
| U-167 | /NM único sin '/' | nm_fallas | test_u167 | OK |
| U-168 | protocolo final A1-A5 + CHECKLIST | CE_A1_REMEDICION (re-mide vectores) / CE_A2 / CE_CHECKLIST | test_u168_checklist | OK |
| U-169 | una sola entrega; presupuesto de horas por tamaño | CE_TIEMPOS presupuesto_fallas (v96 P6) | test_compuerta_entrega::test_p6_presupuesto_horas | OK |
| U-170 | SF del proyecto con hoja | sf_proyecto_fallas | test_tiempos_cita_sf | OK |
| U-171 | no preguntar lo que ya sé | CE_GAUGE_IMPRESO + CE_RFI_BARRIDO_IMPRESO | test_be_cr34_gauge_impreso | conducta: 'no preguntar lo que ya sé' depende de lo que el agente ya resolvió en la conversación; lo impreso ya lo revisa el barrido |
| U-172 | regla de oro: buscar en planos, luego IBC | CB_U_155 + ce_rfi_busqueda | CASOS u_155 | OK |
| U-173 | al reanudar: seguir donde quedó + revisar addenda | — | — | conducta: al reanudar una sesión el agente lee ESTADO_PARA_RETOMAR y las addenda antes de cualquier programa; no hay archivo de la entrega que lo pruebe |
| U-174 | altura del edificio si no hay estructura impresa | CB_U_174 + CB_U_174_VALOR u_174_valor (v96: altura cargada = altura del edificio impresa) | test_chequeos_biblioteca CASOS u_174_valor | OK |
| U-175 | alturas a 3 lados | CE_ALTURAS_3LADOS | test_u175 | OK |
| U-176 | protocolo extremo de alturas | CE_ALTURAS_EXTREMO / comparar_alturas.controles | test_u176 | OK |
| U-177 | verde amarrado al hash; contorno; gauge; producto | CE_ENTREGA_VIGENTE / CE_RCP_CONTORNO / CE_MS_GAUGE / CE_MS_PRODUCTO | test_u177_* | OK |
| U-178 | decisiones GK = regla sin RFI | CB_U_178 + CB_U_178_LARGO u_178_largo (v96: inclinado / VARIES con su geometría) | test_chequeos_biblioteca CASOS u_178_largo + test_v96_sin_falsos_positivos_cr | OK |
| U-179 | corregir antes de preguntar RFI | CE_RFI_LISTO + correr() | test_u179_rfi_listo | OK |
| U-180 | presupuesto duro por ronda; 30 min sin reporte | watchdog correr_con_tope + registro_corridas (tope de corridas / rojas) + presupuesto P6 (v96) | test_be_gk35_watchdog_y_ciclos + test_p3_registro_corridas + test_p6_presupuesto_horas | OK |
| U-181 | 'terminado' solo con auditoría de fondo, 0 hallazgos | CE_PROTOCOLO_3H (1) (v96 P4: sha256 del vigente + 'abiertos: 0') | test_compuerta_entrega::test_u184_protocolo_3h | OK |
| U-182 | CSV de Bluebeam solo al final | — | — | conducta: el CSV de Bluebeam lo exporta el usuario en su Bluebeam al final; el skill no tiene ese archivo hasta que lo recibe |
| U-183 | reportar solo del proyecto urgente | — | — | conducta: de qué proyecto se le informa al usuario es una decisión de conversación de COORDINACIÓN |
| U-184 | protocolo bien a la primera 2-3 h | CE_PROTOCOLO_3H (v96: + inicios registrados, tope de corridas, auditoría con sha) + CB_U_184_ELEV (walls_todos) / EXCL | test_u184_protocolo_3h + test_p3_registro_corridas | OK |

## 2. Notas de la rehechura (v81cf96)
- 14 renglones quedan como **conducta con motivo**: lo que no se puede leer desde un programa (lectura gráfica del plano, acciones en Drive / BuildingConnected, decisiones de conversación). En cada uno se nombra la parte que SÍ revisa un programa.
- Bug real encontrado al escribir el test de BE-CR07: `trazabilidad.py` no desglosaba la familia `5/8" EXTERIOR gyp sheathing Type X` (cita 'default (no sheet)'). Arreglado; el test falla con el trazabilidad de v81cf95.
- Los chequeos nuevos se corrieron contra los 9 canons del banco y el canon cerrado de CR. Los falsos positivos que salieron (soffits en BE-GK37; 'sloped ceiling', 'NO SLOPE', pendiente de techo y 'VARIES - SEE PLAN' en U-178 (5); pisos típicos inferidos en BE-CR27) se corrigieron y quedan con su test (`test_v96_sin_falsos_positivos_cr`). Resultado: 0 FAIL nuevos en el banco.
- `CB_U_184_ELEV` sigue en FAIL sobre proyectos del banco anteriores a U-184 (CFA, Chuze, O'Reilly, CR): son entregas cerradas, no se re-abren (U-180 (4)).
- CR y GK no se re-abrieron. Xfinity con v81cf96 (corrida en seco, sin escribir): 225 PASS / 3 AMBER / 0 FAIL.
