# CAMBIOS tools v77c

- canon.py `_atm_wall` (U1, R77.11): el recess de ATM / equipo empotrado está en la wall que lo contiene; esa wall
  tiene que pasar por studs_nodos y corridas (su type lleva el metal); extra framing ATM = 0 (ya no suma la wall,
  ya no exige `to_deck`, ya no rechaza la wall exterior, ya no emite el RFI "counted once").
- accesorios.py (U1): `atm_recess_valido` acepta `extra_printed {source N/HOJA, text impreso, lf, op}` (RFI con
  delta, no suma); `extra_framing` de ATM a mano (kind atm_recess o ref ATM) = error; renglón "Extra framing - ATM
  recess (0: ...)".
- chequeos_v72.py R72.11 (U1): sin falla por wall exterior; extra_framing de ATM a mano = falla.
- canon.py `_sealant` (U8, R77.12): acoustical sealant EXCLUIDO (no calcula details[*].sealant ni sealant_items;
  aviso; `excluidas`); familia propia "sealant at base of gypsum (exterior)" (fuera de OBLIGATORIAS).
- familias.py (U8): familia "sealant at base of gypsum (exterior)" antes de "acoustical sealant".
- eval_takeoff.py (U8): modo "excluir" (sin renglón = EXCLUIDA OK; con renglón = MAL).
- alcances.py (U8): `EXCLUIDOS` (ALC-19 se cierra "EXCLUIDO: ..."; renglón de acoustical sealant en el Excel = falla).
- plantilla_excel.py: `acoustical_err` (U8, en validar y verificar), `EXCLUIDAS_SIEMPRE` (fusionar sobrescribe el
  alcance), `ordenar_revisar` / `revisar_err` / `verificar_v77c` (U9 / U10: fase, type, orden_plano, n/N, total
  anunciado, floor plan A-Z antes que los detalles); hoja Review Items con fila de total y columnas Phase / Type.
- reglas_clasificacion.py: R77.11–R77.16.
- Tests: test_v77.py (U1 reemplaza a D1), test_v77c.py (U7, U8 x3, U9/U10 x2, SKILL), test_v72.py, test_accesorios*.py,
  test_canon*.py, test_plantilla_v68.py actualizados.
