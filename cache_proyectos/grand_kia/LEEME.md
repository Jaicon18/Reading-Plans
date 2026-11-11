# Grand Kia Auto Dealership - Thornton (Denver), CO (Brinkman) - rev1

Cache del proyecto (scripts del pipeline y configuración) para retomarlo o reusarlo. Skill: v81cf88 (publicada 11-nov).

- scripts/: cadena.sh (etapas 4-9 por bitacora), armar_entrega.sh (carpeta rev1 FINAL + compuerta), build_canon.py,
  misc_gen.py, rcp_polys.py, alturas_final.py (U-175 / U-176), takeoff_json.py, schedules_pos.py / schedules_ms.py (U-142),
  sellar_y_marcar.py (closer + planmark), registro_marcar.py, backcheck_md.py, review_imgs.py, rfi_barrido.py, ocr_extra.py.
- config/: entrega.json (Drive, bidset, bidset_texto OCR), sheetmap.json, rfis_final.json, canon_patch.json (alturas),
  extra_markups.json (geometría verificada de board fuera del RCP), entrega_schedules_materiales.json, tiempos_pasos.json.
- Estado al guardar: compuerta en curso (ver ENTREGA_OK / SUBIDA_OK cuando se agreguen).
