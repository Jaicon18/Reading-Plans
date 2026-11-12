# Grand Kia Auto Dealership - Thornton (Denver), CO (Brinkman) - rev1

Cache del proyecto (scripts del pipeline y configuración) para retomarlo o reusarlo. Skill: v81cf88 (publicada 11-nov).

- scripts/: cadena.sh (etapas 4-9 por bitacora), armar_entrega.sh (carpeta rev1 FINAL + compuerta), build_canon.py,
  misc_gen.py, rcp_polys.py, alturas_final.py (U-175 / U-176), takeoff_json.py, schedules_pos.py / schedules_ms.py (U-142),
  sellar_y_marcar.py (closer + planmark), registro_marcar.py, backcheck_md.py, review_imgs.py, rfi_barrido.py, ocr_extra.py.
- config/: entrega.json (Drive, bidset, bidset_texto OCR), sheetmap.json, rfis_final.json, canon_patch.json (alturas),
  extra_markups.json (geometría verificada de board fuera del RCP), entrega_schedules_materiales.json, tiempos_pasos.json.
- Estado final (11-nov 07:32 PT): compuerta VERDE 206 PASS / 2 AMBER / 0 FAIL (ENTREGA_OK.json), subida con subir_entrega.py (SUBIDA_OK.json, 29 archivos) a Claude outputs › Grand Kia Auto Dealership - Denver, CO (Brinkman) › rev1 FINAL PARA REVISAR. 10.5 h, 0.25 h / 1,000 SF. RFIs abiertos: RFI-01, RFI-05, RFI-07, RFI-34, RFI-35.

## rev2 (11-nov, VIGENTE)
- Drive: Grand Kia Auto Dealership - Denver, CO (Brinkman) / rev2 FINAL PARA REVISAR (1jDg638Ip3vmp70gnRCu707wG8NMmCQOT); rev1 renombrada "zz rev1 FINAL - REPLACED BY rev2 (NO USAR)".
- Compuerta v81cf94 VERDE 213 / 3 / 0; Excel sha256 ca2844a0c0151a16ebc70a6cc6d927f55c172c94613df09ef5f63a3aa61e7e81; --vigente PASS; Drive = local 2,530 archivos (Auditoria 2,502), 0 duplicados.
- Auditoría independiente U-181: informe + 6 re-verificaciones, 0 abiertos (work/auditoria_U181, copia en Auditoria/auditoria_U181).
- Herramientas: v81cf94 + tools_post_v81cf94 (BE-GK36b trazabilidad, BE-GK38 comparar_alturas). Reglas BE-GK32..BE-GK38.

## rev3 (12-nov) — ENTREGADA
- Compuerta 4 con v81cf113: VERDE 229 PASS / 4 AMBER / 0 FAIL (12-nov 00:xx PST). Corridas en rev3: 4 (#1 ROJA v108 sin registro BE-GK46; #2 ROJA v111; #3 VERDE v112 bloqueada por U-192; #4 VERDE v113).
- Excel sha256 6be372555849353515e6917000252671fc4f745259b5ad693a54ee1ce4acae3b; markups 1317e0a71b57cff076e5f584b82971eb43d93bdd91f8590f57999eea75b8e1a7.
- Auditoría U-181 de cobertura: REVERIF7..REVERIF14, open: 0.
- Subida: 2,608 archivos (Auditoria 2,580) a Claude outputs › Grand Kia Auto Dealership - Denver, CO (Brinkman) › rev3 FINAL PARA REVISAR; --vigente PASS; Drive = local, 0 duplicados. rev2 renombrada "BORRAR (NO USAR) - rev2 FINAL PARA REVISAR - REPLACED BY rev3".
- RFIs abiertos: 0 (RFI-36 SOF-18 cerrado por precedente #6 con delta −91.00 / −81.22 SF).
- Deltas vs rev2: board +550.66 SF; 1/2" ext. sheathing +24.90 SF; 1000S162-43 −387.76 LF; 600S162-43 parapet −110.04; 600S162-43 −6.75; 362S162-33 +185.82; 362S162-43 −24.09; 250S162-33 +0.99; ceiling/soffit track +60.00 LF; hanger wire −16.00 LF; compound +39.65 LB; tape +203.74 LF.
- Reglas de esta ronda: BE-GK42..BE-GK49.
