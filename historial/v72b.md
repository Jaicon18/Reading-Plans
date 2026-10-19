# CAMBIOS v72b (2026-10-19) — REGLAS INVIOLABLES

Orden del estimador: "Las reglas están hechas para respetarse, conviértelas a inviolables." Antes, muchas reglas del
SKILL eran solo texto y una corrida las aplicaba y otra no. Desde v72b ninguna regla depende de que la corrida se
acuerde: `reglas.py compuerta` manda.

## Auditoría
- Catálogo automático (`tools/reglas_catalogo.py`): 668 reglas del SKILL.md y de referencias/ (§0 E1–E28, §1–§18,
  R70–R72, PT, D, A, todas las ⛔, REGLAS 44.x–60.x, viñetas de la referencia de método, adendas v26–v47,
  contratos de herramientas).
- Decisión regla por regla (`tools/reglas_clasificacion.py`): **a 301 · b 198 · c 169**.
  - (a) 67 chequeos automáticos sobre canon, salidas recalculadas con canon.py, bitácora y Excel.
  - (b) 35 specs de evidencia por caso: cita (HOJA / N/HOJA / archivo) + imagen que existe + valor; falla si falta o
    si el valor contradice la regla.
  - (c) fusionadas o anuladas (índice de errores, checklist ANTES DE ENTREGAR, copias de súper reglas, carpetas
    viejas anuladas por 49.1, 60.5 anulada por E2, tools que ya no viajan…); nada se borró.
- Tabla: `referencias/REGLAS_INVIOLABLES.md` (regla → tipo → chequeo → test), generada con `reglas.py tabla`.

## Inviolable
- `plantilla_excel.py armar` corre la compuerta EN PROCESO y no escribe el Excel si no da OK; exige el
  familias_out.json de la carpeta de trabajo; el libro sale sellado.
- `etapas.py compuerta` y `bitacora.py compuerta` (modo final, sello vigente) la corren. Sin flag de override.
- SKILL: bloque "⛔ REGLAS INVIOLABLES: ninguna regla se interpreta ni se omite; reglas.py compuerta manda." arriba
  del protocolo; Etapa 2 (evidencia b), §8 0e, §19.

## Tests
- `test_reglas.py`: un test por regla (668 OK; 67/67 chequeos con caso malo y bueno).
- Suite completa del zip desempacado en carpeta limpia: **45 de 45 rc 0** (python3 -I).
- `test_ciego_v69.py` sobre el skill: OK (25 archivos, 0 hallazgos). `test_ciego_tools.py`: OK (las tools sin
  valores de proyecto en comentarios / docstrings ni el nombre del proyecto en el código).

## Pruebas 20A / 20B (fuera del paquete)
Ver REPORTE_COMPUERTA_20A_20B.md en la carpeta de entrega: la compuerta da NO OK en las dos y nombra las reglas que
violaron (type K sin hatch medido, FRP sin jogs, MEP sin mep.cruces, column wraps sin fos_chain, partes de box sin
part_of, walls tipados sin tag_ids, aberturas sin las dos bandas, ATM sin alternativas, purlin sin declarar…).

Ver tools/CAMBIOS_tools_v72b.md para el detalle por tool y lo pendiente.
