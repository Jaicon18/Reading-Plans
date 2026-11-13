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

## rev3a (12-nov) — ENTREGADA (auditoría U-138 de COORDINACIÓN sobre rev3)
- Compuerta final con v81cf118: VERDE 231 PASS / 4 AMBER / 0 FAIL (12-nov 08:12 PST); skill_version v81cf118.
- Excel sha256 4db25b9d54c731dc3372334824e5dbb1eb92db6ae0de3c18408d600f8d1f723e; markups f98d253eb8298a0ef6ca0061450b61709c7f7a8a64af82176e51c44568970e31.
- Auditoría U-181: REVERIF15 (2 LOW: cita 1/A540 → 2/A540, C636 como hoja) → REVERIF16 open: 0.
- Sin cambio de cantidades vs rev3: clips "3" x 3" x 0'-3" x 20 ga" (64/S204 nota 6), "Hanger wire, 12 ga (No. 12 SWG)" (3/A540, 2/A540), RFI-18 loaded = Type X, canon.ceilings_misc (v81cf117) para CB_RCP_APILADOS, Auditoria/RCP_APILADOS.csv y revision_materiales (U-111).
- Subida: 2,626 archivos (Auditoria 2,598) a Claude outputs › Grand Kia Auto Dealership - Denver, CO (Brinkman) › rev3a FINAL PARA REVISAR; --vigente PASS; Drive = local, 0 duplicados. rev3 renombrada "BORRAR (NO USAR) - rev3 FINAL PARA REVISAR - REPLACED BY rev3a".
- Reglas de esta ronda: BE-GK50..BE-GK58 (BE-GK54..58 = rev3b, apartados/be_gk54..be_gk57).

## rev3b (12/13-nov) — ENTREGADA (mapa de cobertura U-193 + revisor independiente)
- FINAL = compuerta VERDE con v81cf129, 231 PASS / 6 AMBER / 0 FAIL (corrida 60914f5fc798, 12-nov 17:05 PST). Registro inmutable en compuerta_corridas_rev3b.jsonl.
  Subida con subir_entrega: CANDADOS OK, 2751 archivos, SUBIDA_OK_rev3b.json. --vigente PASS.
  rev3a renombrada en Drive: "BORRAR (NO USAR) - rev3a FINAL PARA REVISAR - REPLACED BY rev3b".
- Después COORDINACIÓN publicó v81cf130 y se re-corrió la compuerta. Salió ROJA por 3 corridas finales sobre los mismos archivos. COORDINACIÓN decidió la opción (a): v130 no reabre una entrega ya subida (U-180 (4)). Esa re-corrida sobrescribió el ENTREGA_OK local; se guarda como ENTREGA_OK_rev3b_v130_ROJA_post_subida.json. El VERDE de v129 es el de compuerta_corridas.
- Hashes entregados:
  - Excel 2ed813b35a09a01e4b3cf700bc12b658109104c0fae83496ef0de9d31f4ba0d6
  - PDF de markups 7eb81b221a1e90b55fe64c0957e26b063e5557ba3387d7154935c825e384e303
  - canon 1ab5af2c48061c89920ddd8da951399fb4e070ee793d432151ab96eab7801ff4
  - rfis 3f0e8d24d2f6f07e6099d6495414aac7e02075558603bb4792e42332547ad177
- REVERIF20 (auditor independiente): open 0. Revisor U-193 (a2b49d549b9d7d9a0): 45 renglones (40 NO ES NUESTRO, 4 NO ES MURO, 1 CUBIERTO), 0 FALTA abiertos.
- Elementos nuevos: A-Z1-20 (leaf A del nicho), F1-Z1-06 (end cap 18/A521), F-Z1-21/22 (patch kn 52), WR-05 + TRIM-057 (ventana D de Serv Mgr 128), RI-18C (box del roof drain kn 6 en Dealer 140). Delta completo en DELTA_rev3a_rev3b.md.
- Reglas de esta rev: BE-GK54..BE-GK58 (chequeos en apartados/be_gk54..be_gk57).
