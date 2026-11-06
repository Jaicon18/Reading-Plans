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
