# ESTADO PARA RETOMAR — CR City Hotel (5-nov ~8:30 PM PT)
- Trabajo local: /root/cr/work (plans/bidset_SIN_MARKUPS.pdf, etapas/, scripts/, entrega/). Skill de trabajo: /root/skill/take-off-metal-frame-drywall (= v81cf54 + BE-CR01..09; copias en tools_v81cf53/).
- Si el contenedor se pierde: rehacer /root/cr/work desde este caché (scripts/, lecturas/, revision/, canon/, indep/, burbujas/) + bajar el bid set de Drive Projects (id 13n-O-vE8iizFbY5DXzNCLzVX9B30-ob4) y la copia limpia (quitar anotaciones 'Architect Stamp').
- Cadena: `bash scripts/cadena.sh [desde]` (pasos 4-8, CHAIN-OK al 5-nov 20:28: Excel + markups 819/819). Entrega: `bash scripts/armar_entrega.sh` (detalles, schedules, banco, compuerta).
- Compuerta de entrega 1.ª corrida: PASS 119 / AMBER 16 / FAIL 36 -> trabajando las FAIL.
- Pendiente: FAILs de compuerta, auditoría adversarial U-138 (subagente), Proposal U-150, subir_entrega.py, publicar skill v81cf55 (registro de BE-CR01..09 + suite + banco + verificar_version), informe final a COORDINACIÓN.
- Drive: Projects › CR City Hotel… (bid set) ; Claude outputs (raíz) › CR City Hotel - Castle Rock, CO (Owen-Ames-Kimball) 11-12-26 (id 1UVry3iaGhJrahxk8DE-Q150WvRAE38h3), vacía.

## PAUSA 98 % uso semanal (6-nov ~20:50 PT) — orden COORDINACIÓN
Paso exacto: Paso 10 / compuerta de entrega, corrigiendo FAIL. Hecho desde 20312d1:
- BE-CR09b auditoria_entrega RX_SCALE (test OK); BE-CR10 chequeos_biblioteca walls_todos (BE-61, BE-VS-15, BE-90 wood); BE-CR11 revision_markups id con lado ('CH-L2-01 A').
- rfis.py: cerrados con fuentes_revisadas (E23); takeoff_json: structural steel EXCLUDED (KICKER/CLIP ANGLE/L3x3), J RUNNER CHANNEL; build_canon: detail 1/A3.0x en GYP misc; canon_AB: constants.plan_scale.
- armar_entrega.sh ya NO re-une burbujas (backup burbujas/FINAL_backup).
- NUEVO scripts/esquinas_cb.py (corner bead por programa, cierra RFI-19): L1 356 / L2 589 / L3 574 / L4 573 LF; falta integrarlo en finalizar_canon (reemplaza CB-CORR-L2/L3) y verificar imágenes img/cb.
Siguiente: integrar corner bead → bash scripts/cadena.sh 2 → armar_entrega.sh → iterar FAIL (lista en gate_old) → OCR set_texto_ocr.json (corría en background) → auditoría U-138 → Proposal U-150 → subir_entrega → skill v81cf55.
- Al retomar también (msg COORDINACIÓN 04:07Z, anterior a la pausa): pasar los 19 RFI uno por uno por el filtro U-140 / R-ALC-10 / U-083 / R80e.34 / U-146 / U-147 / U-143 / U-061; solo quedan abiertos los no impresos en ningún lado, con barrido completo (referencia: Consumer Cellular 8→2). Ya cerrados: RFI-07/11/12/14/16; RFI-19 se cierra con esquinas_cb.py.


## ESTADO 6-nov ~10:00 PM PT (sesión reanudada, "continua hasta que se terminen los creditos")
- Compuerta: de 36 FAIL a 13 (última corrida completa); después: alturas 0 RED, español 0, schedules REVISADOS PASS, RFI barrido OK, reglas.py solo falta BACK-CHECK.
- RFI: abiertos 04, 09, 13 (solo stud size MB-1), 15, 17. Cerrados por impreso/regla: 01,02,03,05,06,07,08,10,11,12,14,16,18,19.
- Cambios de cantidad: corner bead por programa (esquinas_cb.py); retail non-rated faces EXCLUDED (-532.5 SF, RFI-05); GYP-2 = A0.08 MB-1 (3 layers + liner + C-H + J) (+401 SF Type X, +401 SF liner, +253 LF C-H, +83 LF J).
- Proposal U-150 hecha (/root/cr/work/Proposal, script /root/cr/work/proposal/build.sh) -> REARMAR al final (cantidades cambiaron con MB-1).
- En curso: subagente burbujas (CE_DETALLES_CIRCULADOS / CE_CALLOUTS), subagente auditoría U-138 (-> /root/cr/work/auditoria_U138/INFORME_AUDITORIA_U138.md -> bitacora.py backcheck <informe> <excel>).
- Bitácora rehecha en orden (bitacora.jsonl nueva; la vieja = bitacora_corrida1_archivada.jsonl); registro.json recreado (viejo archivado).
- Siguiente: integrar burbujas + citas en canon -> cadena.sh 2 -> armar_entrega.sh -> FAIL restantes -> backcheck -> proposal build -> subir_entrega -> skill v81cf55 (+ sección multinivel R80f) -> reporte.
- 6-nov ~10:15 PM PT: Drive del proyecto llenado (estaba vacío, BE-CR17): '2026 Permit Drawings (bid set)' 11 PDF + copia limpia 148p; '2025 Drawings (superseded)' 5 PDF. Auditoría U-138 recibida: 4 ALTA (FS-1 en cielo L1, Retail 124 GYP-1, corridor 412 L4, corner bead) + 5 MEDIA -> en verificación.
- 6-nov 12:25 AM PT: ENTREGADA. Drive › JC HUNTER PROJECTS › Claude outputs › CR City Hotel - Castle Rock, CO (Owen-Ames-Kimball) 11-12-26 › rev1 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR (id 1ohr8whOoMPthHRechOtkUYTW-7-qBqVH): 558 archivos verificados por listado (raíz 6, Take-off 2, Proposal 2, Planos marcados 27, Auditoria 521). Para borrar a mano: 24 'DUPLICADO - borrar - *' en Planos marcados; carpeta 'NO USAR - subida cortada...'; '2026 Permit Drawings (bid set)' y '2025 Drawings (superseded)' duplicados en Claude outputs (el bid set real está en Projects).

## rev2 (6-nov, orden COORDINACIÓN 10:12Z: rev1 pasó la compuerta EN VACÍO)
- BE-CR25 en curso (v81cf56): walls() sintetiza board-only de existing_walls (caras por cuarto, capas sumadas en la misma cara; liner/exterior por clase);
  canon_no_vacio (0 walls + PT>0 = FAIL); en_vacio() convierte N/A 'sin walls/sin canon' en FAIL (correr + wrapper de compuerta_entrega); test_be_cr25 en test_cf_pruebas.
- BOTH SIDES: 48 -> 10 -> faces_none_reason con N/HOJA verificada (1/A7.45 nota F&B en Kitchen 100; 1/A2.01 retail; 1/A2.04, 3/A7.50; 1/A2.03 shaft box RFI-09, DW.4 cavity).
- U-140: alturas L4 stair 5/A6.02 y 11/A6.01: la cota L4 -> underside roof sheathing NO está impresa (imágenes imagenes/alturas) -> AMBER legítimo.
- Salidas renombradas a rev2 (cadena.sh, armar_entrega.sh, hacer_docs, cobertura, imagenes_hoja, proposal). rev1 archivado en /root/cr/work/archivo_rev1.
- Pendiente: cadena rev2 -> armar_entrega -> compuerta -> auditoría U-138 #2 (subagente) -> subir rev2 -> aviso REPLACED BY rev2 en rev1 -> listar Drive -> informe COORDINACIÓN.
