# Parche para la línea principal (BE-115) — desde Chuze FINAL5, 2026-11-03 — NO es una versión archivada
Hecho sobre v81cf17 (vigente al momento). Unir como la próxima versión y correr el banco.
- R80f.13 `markups_rcp.py`: varias hojas RCP (cada ceiling con `sheet` e `id`), id del ceiling en el markup, leyenda y PNG por hoja (antes solo `constants.rcp_sheet`). Test `test_rcp_multihoja.py`.
- R80f.14 `verificar_markups_excel.buscar_pdf`: búsqueda de "*markup*" sin distinguir mayúsculas (tomaba el PDF viejo).
- R80f.15 `auditoria_entrega.py`: polígonos de ceiling validados contra el desglose del Material Summary y su área dibujada.
- R80f.16 `markups_rcp.py`: el polígono del ceiling tiene que seguir el hatch C-5; una parte sin hatch (≥ 1 SF) en el borde = rc 1 (errores Chuze: shower con esquina de fixtures, caja del storefront con panel de display). Test `test_rcp_hatch.py`.
- Regla: el GWB ceiling = SOLO el área con hatch, limitada por las caras; las áreas cargadas por extensión de trazos del hatch quedan cortas 1–5 % (Chuze FINAL4 → FINAL5).
- Pendiente de criterio del estimador: grid / hangers por caja envolvente del ceiling (caja oeste: 6.13 SF de soffit con la caja completa de 2.89 x 9.89 ft).
