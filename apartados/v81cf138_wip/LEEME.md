# v81cf138 WIP: arreglos de los 7 STILL-WEAK de la verificación 6 (post-mortem 12b)

Estado: preparado, NO publicado. Vigente: v81cf137. Se publica cuando COORDINACIÓN avise, después de que CR cierre rev20c.

## Contenido

- `v81cf138_desde_v81cf137.patch`: parche completo del skill.
- `ordenes/`: verificar_version.py, test_verificar_version.py y REGLAS_REGISTRO.json candidatos.
- `adversariales/`: los adv6_* de la verificación 6, con su salida antes (`before/`) y después (`after/`).
- `PRUEBA_ABIERTOS_v81cf138_XF.json`.

## Qué cambia (un test por caso)

| renglón | arreglo | test |
|---|---|---|
| NG-3.1 / BE-PM04 (prioridad) | PRUEBA_ABIERTOS sin un proyecto abierto = "BLOQUEA LA PUBLICACIÓN" (main sale con 1 y dice NO PUBLICAR); un proyecto en curso sin SUBIDA_OK cuenta como abierto (canon o TIEMPOS / log / VERSION_PROYECTO con fecha); csv_cuadra con no emparejados / duplicados / huérfanos / diferencias > 0 = no cerrado; VERSION_PROYECTO en subcarpetas | adv6_pm04 (test_verificar_version) |
| BE-CR40 / v120-FALT | lista abierta de faltante (en / es) y de cielo (techo, plafón, hard lid, bulkhead); cuartos C-12 / B12 / room 12; hallazgos en COORDINACION / REVIEW / HALLAZGO / RESUMEN / BITACORA / FINDINGS (solo la rev actual); CERRADO: y DOBLE_CIELO solo con ref DEL cuarto; faltante y cielo en la misma frase ('above ceiling' es altura) | test_v138_faltantes_listas_abiertas, test_v138_faltante_misma_frase |
| NG-3.3 / BE-PM06 | plazo por las marcas "\| N fin" y por TIEMPOS.md; sin ninguna, cada marca del log cierra | test_v138_alarma_plazo_tiempos |
| U-193 | una corrida solo reemplaza a la sin agente con rc 0, resultado, mismos args y hashes, sin --help | test_v138_reemplazo_corrida_sin_agente |
| BE-GK54 | gap_proof 'gap 0' con distancia medida > 2 in = FAIL | test_v138_gk54_gap_medido |
| v120-RETRO | el AMBER retroactivo exige inicio independiente (VERSION_PROYECTO / bitácora / git) anterior a v119 y a <= 24 h del log | test_v138_retro_fuente_independiente |

## BE-XF18 (COORDINACIÓN 08:12)

`Ctx` elegía el PDF de markups por orden alfabético inverso. Desde v133, 'MAPA DE COBERTURA - IMAGE ONLY.pdf' ordena antes que '<PROY>_markups…' cuando el prefijo del proyecto es menor que M (CR, GK); la compuerta leía el mapa (0 annots) y daba FAIL falsos. Ahora `elegir_pdf_markups` toma entrega.json 'markups' o el único '… - OPEN IN BLUEBEAM.pdf' (U-165); nunca 'IMAGE ONLY' / COBERTURA; sin candidato o con más de uno = FAIL con la causa (CE_PDF_MARKUPS_ELEGIDO). Test test_be_xf18_pdf_markups_por_nombre.
Entregas revisadas (ENTREGA_OK archivos): GK rev2 / rev3 / rev3a / rev3b y XF rev1c leyeron su PDF OPEN IN BLUEBEAM. En GK rev3b el mapa todavía se llamaba 'COBERTURA - IMAGE ONLY.pdf', que ordena antes que 'GK_…', así que la regla vieja acertó. El error aparece solo con el nombre de v133 ('MAPA…').

## Pedidos de CR rev20c con v137 (COORDINACIÓN 08:25)

1. CB_BE_83 'int object is not iterable': runner/completitud.caras_sobre_ceiling ahora lee existing_walls (BE-XF16), y en CR 'faces' es un número. Un muro así cuenta como UNA cara (altura del muro, cuarto del location). Justificaciones agregadas: 'underside of roof / floor / structure', 'extend to …', 'floor to floor', 'stair enclosure'; la cara exterior no se compara con el cielo del cuarto. CR rev20b: 86 → 0. Test test_v138_be83_faces_numero.
2. CB_BE_CF04 en set wood-framed: su PASS decía 'cero walls de madera con framing' en cifras; desde v134 la red U-138 espera 943 muros en CR y lo volvía FAIL. Redacción sin conteo. Test test_v138_cf04_wood_board_only_plausible.
3. CE_PROTOCOLO_3H AMBER (v134) → FAIL (v137): el código es idéntico entre v134 y v137. Pedí a CR la evidencia de las dos corridas, VERSION_PROYECTO.txt y tiempos.log. PENDIENTE.
4. CE_COBERTURA_DIAG 555 en CR: pedí a CR las familias de falsos con ejemplos (o el PDF de markups de rev20c). PENDIENTE.

## Lo que NO cierra (para la verificación 7)

- BE-GK54 Q2: una hoja sin escala en `escalas` usa 9 pt/ft por omisión; una leaf de una hoja a 1/4" se sale de la ventana.
- BE-GK54 Q3: 'existing' se acepta como otro material aunque la leaf sea de metal.
- BE-GK54 Q4: una exclusión 'same wall' sin gap_proof con la leaf dispuesta como caso (b) no se juzga.
- BE-GK54 K3: 'no gap between leaves' sigue rechazado (es ruidoso, no silencioso).
- Ambigüedades conservadoras: 'room 12' contra 'C-12' se resuelve como cargado (FAIL de más); 'techo' puede ser roof en español.
- NG-3.1: falta el candado automático en el commit de publicación. Hasta que exista, quien publica tiene que abortar si verificar_version sale con 1 por PRUEBA ABIERTOS.

## Validación

suite 47/47 · banco 0 distintas (8) · XF PRUEBA_ABIERTOS 0 regresiones (231 / 12 / 0, con BE-XF18) · reglas 0 sin clasificar · 199 archivos. La primera corrida dio un falso positivo nuevo en XF (CB_FALTANTES_AUDITORIA leía 'not quantified' + 'above ceiling' de una fila del Scope); quedó corregido con la regla de "misma frase".
No dice CONFIRMED-CLOSED en ningún lado: eso lo decide la verificación independiente 7.
