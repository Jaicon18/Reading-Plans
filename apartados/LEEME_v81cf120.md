# v81cf120 APARTADA (NO publicada; orden de COORDINACIÓN 12-nov 21:17): los 5 STILL-WEAK de la verificación 3 de v119

Base: v81cf119 (vigente). Aplicar con `patch -p1` desde la carpeta que contiene `take-off-metal-frame-drywall/`:
- descomprimir el zip de v81cf119 en una carpeta X;
- `cd X` y `patch -p1 < v81cf120_desde_v81cf119.patch`.
Las rutas del parche empiezan con `v119/` y `v120/`. Las ordenes van en `apartados/ordenes_v120/` (verificar_version.py + test).

Informe: cache_proyectos/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md (f6d46a0). Adversariales: apartados/adversariales_v119/.

1. U-185 (`verificar_version.revisar_postmortem`):
   - un renglón se cierra SOLO con el estado exacto `OK — CONFIRMED-CLOSED` (RX_PM_CERRADO, anclado al inicio): 'WEAK — NOT
     CONFIRMED-CLOSED' no cierra (C4);
   - un principal nuevo NO borra los abiertos de uno anterior: se arrastran hasta que una verificación los nombre cerrados (C1 / A2).
   - El arrastre empieza en el 12b (PM_ARRASTRE_DESDE), que es el primer post-mortem con verificación independiente. El 11-11 tiene WEAK
     que la re-revisión completa del 2026-11-12 (124 renglones) dejó en OK; si se arrastraran, se reabrirían de golpe. Está a decisión de
     COORDINACIÓN.
   - Test `postmortem_u185`: C4, C1 y el cierre por la verificación de un principal posterior.
   - adv_pm.py y adv_pm_real.py contra el cache real: todos los casos fallan.
2. BE-PM04:
   - `proyectos_abiertos_cache`: abierto si un SUBIDA_OK*.json (con o sin rev) o VERSION_PROYECTO.txt es más nuevo que el CSV N/N; el
     RESULTADO.md tiene que traer su fecha (sin fecha no se puede afirmar 'cerrado' = abierto) y ningún 'K faltantes' además de
     '0 faltantes' (P4b / P4c / P4d).
   - El detector corre SIEMPRE (sin el 3er argumento usa el cache_proyectos de al lado de skills_archivo; sin cache = FALLA, P8).
   - Se leen las regresiones de CADA proyecto: sin_explicar, cuenta vs renglones, FAIL candidata > vigente + regresiones (P3 / P3b).
   - version_candidata obligatoria (P5); un proyecto de la lista que no existe en cache_proyectos = FALLA (P6); sha_tools obligatorio
     (ya en v119).
   - prueba_abiertos exige `<proyecto>=<carpeta>`: la clave es el nombre.
   - Tests: `prueba_abiertos_be_pm04` y `test_v119_prueba_abiertos`.
   - Real: abiertos detectados = grand_kia, xfinity_interquest (CR cerrado por su CSV N/N con fecha 10:45 PT; está en la lista porque
     rev20b está en curso).
3. BE-PM06: las corridas `--paso` se exigen por cada paso cerrado en TIEMPOS.md (`pasos_cerrados_tiempos`), no por el texto 'N fin' del
   log (E3). Test: `test_v119_alarma_verificacion2`.
4. U-193 (`subagentes_bitacora` / CE_COBERTURA):
   - el autor sale SOLO de las corridas selladas de la bitácora;
   - toda corrida de las etapas 2-7 (no revisión, no arranque / inventario) sin `agente` = FAIL (U6: canon.py corrido sin agente);
   - el autor del canon sale solo de canon.py (un `subagente canon` declarado no cuenta);
   - ids en minúsculas (U7).
   - Test: `test_v119_cobertura`.
5. BE-GK54:
   - cualquier formato de id;
   - sinónimos 'same as' / 'same (single) wall as' / 'duplicate of' / 'part of (wall)';
   - gap_proof solo con N/HOJA (RX_NH_TRAZA);
   - wall sin band o que no existe en el canon = FAIL (no salto silencioso);
   - la GUÍA documenta que dos leaves fusionadas por el mapa no salen en rojo (CE_COBERTURA, entregas desde FECHA_V120).
   - Tests: `test_be_gk54` (G1, G1b, G2, G3, G6 y wall inexistente) y `test_v119_cobertura` (GUÍA).
   - adv_gk54: G1, G2 y G3 dan True; G6 da True; G4 (DISPUESTO) y G5 (fusionadas) no se detectan, y G5 queda como límite en la GUÍA.
   - Xfinity: `scripts/hacer_docs.py` ya agrega el punto (5) a 'Coverage map limits'.

Pruebas:
- suite 47/47;
- banco 0 distintas en 8 proyectos (tools v119 vs v120);
- reglas.py 0 sin clasificar;
- 199 archivos;
- selftest de verificar_version OK.
- verificar_version de v120 con el cache real: faltan 0 reglas; falla U-185 (los 7 renglones del 12b siguen abiertos hasta la
  verificación de v120) y falta PRUEBA_ABIERTOS_v81cf120.json en skills_archivo (va al publicar).
- PRUEBA_ABIERTOS de Xfinity con v120 contra v119: 228/9/0 -> 228/9/0, 0 regresiones (apartados/PRUEBA_ABIERTOS_v81cf120.json). GK y CR
  la corren al publicar v120.
- Parche probado: zip de v81cf119 + `patch -p1` = el candidato idéntico.

AL PUBLICAR:
- apartados/ordenes_v120/*.py van a .claude/skills/jc-hunter-ordenes/;
- REGLAS_REGISTRO.json (el del skill) va al registro de las órdenes;
- PRUEBA_ABIERTOS_v81cf120.json (con XF, GK y CR) va a skills_archivo/;
- INDICE.

## Ampliación (COORDINACIÓN 21:30)

- Arrastre de U-185 desde el 12b: APROBADO (el 11-11 quedó re-revisado completo el 12-nov).
- G4: be_gk54_fallas corre también sobre los rojos DISPUESTO. Da FAIL si la disposición dice 'same wall' / 'same as' / 'duplicate of' /
  'part of wall' / 'mismo muro' sin la prueba del gap (la palabra 'gap' + N/HOJA), o si el DISPUESTO no trae el texto de su disposición.
  Una disposición de otro tipo ('EXISTING CONSTRUCTION TO REMAIN') no es un caso GK54.
  - Test: test_be_gk54 con 5 casos nuevos.
  - adv_gk54 G4 = True.
- G5 (leaves fusionadas por el detector) queda como límite documentado en la GUÍA.
- Pruebas: test_compuerta_entrega + test_ciego re-corridos OK (el resto de la suite no cambió: 47/47); 199 archivos.
- PRUEBA_ABIERTOS de XF re-corrida con el sha nuevo: 0 regresiones.
- Parche re-generado y probado con -p1 sobre el zip de v119.

## Ampliación 2 (COORDINACIÓN 21:42): verificación 4 (d67651e), última ronda — normalización común y parsers compartidos

1. `norm_txt()`, UNA función con el mismo código en compuerta_entrega y en verificar_version:
   - NFKC;
   - todo guion Unicode a '-', y '--' a '-';
   - fuera el ancho cero;
   - espacios, NBSP y tabs colapsados;
   - minúsculas.
   La usan U-185 (estados e ids), U-193 (ids de agente y revisor), GK54 (razones, disposiciones, gap_proof) y el parser de TIEMPOS.md.
2. U-185:
   - el estado cierra solo con match COMPLETO de 'ok - confirmed-closed' después de norm_txt;
   - cada `_VERIFICACION` lleva 'Fecha: YYYY-MM-DD HH:MM PT|UTC' en su encabezado; sin ella, o más de 10 min en el futuro, = FALLA y esa
     verificación no cuenta;
   - un renglón cierra SOLO el id de su primera columna; `NG-N.M / id` cierra la causa N.M y ese id; texto suelto no cierra nada.
   - Ojo: las 4 verificaciones que ya existen no traen 'Fecha:', así que hoy verificar_version da 4 fallas más. La próxima verificación
     tiene que traer el campo.
   - Tests: `adv4_postmortem` (D1-D7) y `postmortem_u185`.
3. BE-PM04:
   - RESULTADO.md cierra solo con 'Comparado: <fecha con zona>' posterior a la última subida / VERSION_PROYECTO y con N > 0;
   - SUBIDA_OK con 'fecha_iso' o 'fecha'; sin fecha o sin zona = FALLA en verificar_version y el proyecto cuenta como abierto;
   - en PRUEBA_ABIERTOS cada proyecto trae los conteos de la vigente y de la candidata (> 0);
   - una carpeta de la lista que no es proyecto (sin SUBIDA_OK ni VERSION_PROYECTO.txt) = FALLA.
   - Tests: `adv4_prueba_abiertos` (Q1-Q6) y `prueba_abiertos_be_pm04`.
   - Real: CR cuenta como abierto (su RESULTADO.md no trae 'Comparado:'); ya está en la lista.
4. BE-PM06: `filas_tiempos` es EL parser de TIEMPOS.md.
   - Lo usan `_pasos_tiempos` y `tiempos_fallas` (CE_TIEMPOS), `pasos_cerrados_tiempos` (exigir --paso) y `tiempos_cuadran_fallas`.
   - Entiende: guiones Unicode, negritas, 4a, 3 columnas, columnas en cualquier orden según el encabezado, y filas sin número de paso
     ('rev15') para los encimados de CE_TIEMPOS.
   - '--paso 9' o '1-9' no cubren otros pasos.
   - Test: `test_v120_adv4` (F0-F8).
5. U-193:
   - ids con norm_txt (U7-U12: mayúsculas, doble espacio, NBSP, ancho cero, tab);
   - la tool se toma por su nombre base ('tools/canon.py' = canon.py, U13).
   - Test: `test_v120_adv4`.
6. GK54:
   - `gk54_mismo_muro`: lista amplia de sinónimos, la MISMA en la exclusión y en DISPUESTO (same wall/leaf (as, ':', comillas, paréntesis,
     'same-wall'), duplicate / dup of, part of, already counted in / with, counted with / in, included in, identical to, see <id> (solo si
     <id> es un wall del canon), mismo muro (que));
   - `gap_prueba_ok`: N/HOJA válido (regex de hoja) + el gap MEDIDO en 0 (p. ej. 'gap 0" (1/A150)'); 'n/a', 'none', 'no gap' o un gap > 0
     (H2b) = no vale.
   - Test: `test_v120_adv4` (H0-H7).
7. Todos los adv4_* están en la suite: test_compuerta_entrega::test_v120_adv4 y selftest de verificar_version (adv4_postmortem,
   adv4_prueba_abiertos).

Pruebas (Ampliación 2):
- suite 47/47; una corrida intermedia falló en test_tiempos_cita_sf (filas 'rev15' sin número de paso) y quedó arreglada en filas_tiempos;
- banco 0 distintas en 8 proyectos;
- reglas.py 0 sin clasificar;
- 199 archivos;
- selftest de verificar_version OK (incluye adv4_postmortem y adv4_prueba_abiertos);
- adversariales_v119 + adversariales_v120 corridos contra el candidato (adv4_pm con su copia mínima del cache).
- PRUEBA_ABIERTOS de XF re-corrida con las tools finales (sha 5c903a278cbd): 0 regresiones.
- Parche probado con -p1 sobre el zip de v119.

## Ampliación 3 (COORDINACIÓN 21:47 / 21:48 / 21:53): retroactivo de proceso (CR rev20b, GK rev3b) + CB_FALTANTES_AUDITORIA (GK)

(a) `proceso_v119` en CE_PROTOCOLO_3H:
- Los requisitos de PROCESO de v119 son BE-PM05 (VERSION_PROYECTO), BE-PM06 (tiempos.log ISO que cuadra con TIEMPOS, --paso por paso,
  sellos) y la alarma (ALERTA_PRESUPUESTO).
- En una rev que arrancó ANTES de FECHA_V119 salen AMBER, con la causa escrita.
- La fecha de arranque (`inicio_rev`) es la primera marca de tiempos.log o, si no hay, el primer commit que toca la carpeta de la rev.
- `marcas_tiempos_log` lee también el formato viejo ('05-nov 11:26 PST', '10-nov 21:01 PST') y lo convierte a ISO.
- Una rev que no se puede fechar = FAIL. Una rev que arrancó después de FECHA_V119 = FAIL, como antes.
- Test: `test_v120_retroactivo_proceso`, con los casos:
  - CR: log viejo y cierres 7-10 solo en commits = AMBER;
  - GK: formato '10-nov 21:01 PST' = AMBER;
  - rev posterior = FAIL;
  - sin fecha = FAIL;
  - fecha por el primer commit = AMBER.

(b) CB_FALTANTES_AUDITORIA (`faltantes_auditoria`):
- el cierre vale con CUALQUIER ref que exista cargada en el canon (`RX_REF_CANON` + `_ref_cargada`, que mira misc, ceilings, walls,
  existing_walls, trim, blocking y framed_soffits): EXT-, SOF-, CLG-, BW-, CW-…;
- una línea de hoja o dibujo faltante ('30/A520 (missing)') no es un cielo faltante y no se evalúa (`RX_HOJA_FALTANTE`);
- los cuartos que ya cubre Auditoria/DOBLE_CIELO.csv (renglón con upper y lower) se resuelven contra esa tabla (`cuartos_doble_cielo`).
- Test: `test_v119_be_cr40_verificacion`, con los casos GK #8 y H-04 con ids sintéticos y el cierre con EXT-.

Pruebas (Ampliación 3):
- suite 47/47. test_ciego marcó 'A520' y 'GK #8' en un comentario; quedaron sintéticos y se re-corrió OK;
- banco 0 distintas en 8 proyectos;
- reglas.py 0 sin clasificar;
- 199 archivos;
- selftest OK.
- PRUEBA_ABIERTOS de XF con las tools finales (sha cb4adc4a0566): 0 regresiones.
- Parche probado con -p1 sobre el zip de v119.
