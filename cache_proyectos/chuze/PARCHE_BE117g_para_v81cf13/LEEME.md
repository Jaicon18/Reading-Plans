# Parche para la línea principal (BE-115) — desde Chuze FINAL4, 2026-11-03

**No es una versión archivada.** Para unir en la próxima versión vigente (v81cf13) sobre v81cf12.

## 1. BE-117g — `verificar_markups_excel.py` (compuerta A_MARKUPS_EXCEL) no entendía renglones unidos "A+B"
- Error: con la v81cf12, Chuze FINAL4 daba 16 FAIL / 24 fallas: cada pieza de un renglón "A-A424-5+A-A424-5r" (PT2: wall + return) se buscaba sola, caía al desglose del Material Summary ("TYPE != Bottom track...") y el renglón quedaba "sin anotación"; además las piezas contaban como "Wall ID duplicado".
- Solución: `leer_excel` arma `union` {pieza -> renglón "A+B"}; cada pieza se valida contra su renglón (TYPE, H) y LF / SF se suman y cuadran contra el renglón (±0.5 %); las piezas no cuentan como duplicado.
- Resultado: Chuze FINAL4 121/121 OK, 0 fallas, rc 0 (`VERIF_v81cf12g_FINAL4.md`; antes `VERIF_v81cf12_FINAL4.md`). `test_markups_excel.py` original sigue OK; prueba nueva `test_markups_excel_union.py`.
- Falta al unir: correr el banco (B&N / VS / O'Reilly / CFA) con el parche.

## 2. Arreglos hechos en la corrida Chuze sobre v81cf10 (carpeta `arreglos_rama_chuze/`, R80f.7–R80f.10 de esa corrida — los ids R80f.7 ya existen en la línea principal con otro contenido: renumerar al unir)
- `markups_bluebeam.py`: leyenda por hoja marcada en el orden del schedule (`leyendas_por_hoja`); run con diferencia < TOL_PT dibujado con el LF impreso (Length = LF); DETAIL de types con guion (A2-3D/A301, no 3D/A301); resumen de markups más reciente del canon. (SF = board SF ya está en v81cf12 como BE-117b.)
- `plantilla_excel.py` verificar: exención de idioma del valor citado en el bloque "PROJECT DATA" (nombre propio "Camino del Rio").
- `auditoria_entrega.py`: auditoría de entrega BE-117 completa (además de markups: 6 hojas, orden del schedule, SUBTOTAL por bloque, PROJECT DATA arriba de Inputs / README / PARA_REVISAR, 0 RFI, un PNG por hoja marcada) — se solapa con verificar_markups_excel; unir lo que falte.
- Pruebas: `test_v81cf11.py` (4 tests de esa corrida en un archivo).
