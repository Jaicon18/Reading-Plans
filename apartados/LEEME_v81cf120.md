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
