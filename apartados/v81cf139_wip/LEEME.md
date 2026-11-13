# v81cf139 WIP (base): lo que sale de v138 por orden de COORDINACIÓN (09:50)

`base_desde_v81cf137.patch` es el árbol ancho que armé como v138 antes del cambio de plan:
- los 7 STILL-WEAK de la verificación 6 (BE-CR40 / glob, BE-PM04, BE-PM06, U-193, BE-GK54, v120-RETRO, v120-FALT);
- los 5 arreglos que sí entran en v138 angosta.

`ordenes/` trae verificar_version (BE-PM04 bloqueante) y su test.

La verificación 7 (cache_proyectos/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION7.md, adversariales en apartados/verif7_adversariales/) encontró en este árbol una regresión (filas de tabla en falta_cielo_misma_frase), el glob de hallazgos, GK54 Q2-Q4, el rol escrito detrás en U-193, el retroactivo con fuente copiada, CERRADO: con ítems que no son cielo y csv_cuadra con 'unpaired'. Todo eso va a v139, después de que CR cierre, con su propia verificación completa.
