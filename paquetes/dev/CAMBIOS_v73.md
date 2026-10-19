# CAMBIOS v73 (2026-10-19) — la compuerta revisa consistencia con el plano

Arbitraje de una prueba ciega (v72b): la compuerta de reglas inviolables dio OK y dos familias salieron fuera de
rango con la regla escrita (ballistic / 3/8" y stud reinforcement MEP). Causa: los chequeos revisaban la FORMA del
dato (hay hatch medido, hay face customer, el cruce trae `method`) y no que fuera el del plano. v73 agrega chequeos de
consistencia y cierra los huecos de tools que reportó la prueba. Ningún valor de proyecto en el paquete.

## Compuerta (chequeos_v73.py; reglas.py los corre como A_R73_x)
- R73.1 type K: la cota impresa junto al tramo manda (`dim_scan` de la tool nueva `cotas_banda.py`).
- R73.2 contorno ballistic sin esquinas dobles (bands de walls K y jogs; paralelos del mismo contorno sin solape).
- R73.3 `plywood_strips[].uso` declarado (renglón de compra por uso).
- R73.5 stud reinforcement MEP = solo ductos de `mep.cruces` × rows; manual / pipe / fire damper a RFI con delta.
- R73.6 `deflection_clips` declarado (nota general o none_reason con hoja); familia nueva en accesorios.
- R73.7 segmento sin tag con espesor de otro type no entra al type por defecto de la nota general.
- R73.8 la operación escrita cuadra (`*_op` "aritmética = N" da N y N es el valor del campo).
- Reglas de lectura con evidencia (b): R73.10 cambio de type en el nodo, nunca en un jamb; R73.11 jamb return por
  borde; R73.13 corner bead en esquinas exteriores de boxes; R73.14 alto de backboards; R73.15 sealant / trim de una
  misma interfaz; R73.17 returns impresos dentro del contorno. Catálogo: 694 reglas (a 319 · b 205 · c 170), 74/74
  chequeos con caso malo y bueno.

## Excel con los renglones de la plantilla (R73.3)
- `plantilla_excel.fusionar`: renglón que cita su familia toma el nombre de la plantilla del estimador
  (`NOMBRES_PLANTILLA`); track por ELEMENTO (parapet; roof step / heads) y el resto por tamaño de stud
  (`track_by_element` de canon.py; sin partir por calibre); FRT plywood por material, espesor y uso; metal stud
  blocking por origen (edge del detalle / notas). Todo texto de tools al Excel en inglés (R73.9).

## Tools
- Nuevas: cotas_banda.py, chequeos_v73.py, planmark.py (contrato completo, con `sheet()`), glosario.py,
  vocab_trade.py, verif_respuesta.py, correr_suite.py.
- indice_set.py genérico (arma su cache con pymupdf; sin coordenadas de un set). registro.py `corregir`.
  particion.py: stub ≤ 6" solo se suma a un wall a ≤ 3 ft (R73.18). canon.py acepta `hatch_extent` / `dim_scan`;
  A_WRAP_FOS acepta `fos_chain` en forma dict.
- eval_takeoff.py: rango min == max manda; `_partition_types`; modo "consistencia" no califica; bloque OTHER no sobra.
- test_ciego_tools.py revisa también test_*.py y fixtures: P6 rooms 1xx, P7 ids de wall de planta, P8 cantidades de
  una lista externa de valores de examen (`--valores`, la lista NO viaja en el paquete). Tests limpiados a datos
  sintéticos (rooms 9xx, ids X / Y / Q, hojas Z).

## Arranque
- `python3 tools/correr_suite.py`: instala dependencias si faltan, ubica el skill ($TAKEOFF_SKILL), copia la
  estructura a una carpeta limpia y corre toda la suite. Una prueba corre SOLO con el zip, sin parches ni scripts.

## Verificación del paquete
- Suite completa desde el zip desempacado en carpeta limpia: todas OK (`correr_suite.py`).
- test_ciego_v69 sobre SKILL + referencias + docs de tools: 0 hallazgos. test_ciego_tools (con la lista externa del
  árbitro): 0 hallazgos.
