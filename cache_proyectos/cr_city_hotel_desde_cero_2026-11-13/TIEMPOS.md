# TIEMPOS — CR City Hotel PRUEBA DESDE CERO 13-nov (hora de California, America/Los_Angeles, PST)

| Paso | Qué | Inicio | Fin | Duración |
|---|---|---|---|---|
| 0 | arranque (set_texto, OCR 17 hojas) | 2026-11-13 18:45 PST | 2026-11-13 18:51 PST | 5 min |
| 1 | inventario de tags | 2026-11-13 18:56 PST | 2026-11-13 19:04 PST | 7 min |
| 2-3 | lecturas A y B en paralelo + H-A / H-B (alturas A / B) + CORES A/B | 2026-11-13 19:05 PST | 2026-11-13 19:37 PST | 31 min |
| 4 | comparación A vs B | 2026-11-13 19:37 PST | 2026-11-13 19:40 PST | 3 min |
| 5 | resolución | 2026-11-13 19:40 PST | 2026-11-13 20:17 PST | 36 min |
| 6 | cálculo (canon.py, accesorios, trims) | 2026-11-13 20:17 PST | 2026-11-13 20:28 PST | 10 min |
| 7 | Excel | 2026-11-13 20:28 PST | 2026-11-13 20:40 PST | 12 min |
| 8 | markups Bluebeam walls + RCP (fin = markups_rcp 05:08:15 UTC en bitacora.jsonl) | 2026-11-13 20:40 PST | 2026-11-13 21:08 PST | 28 min |
| 9 | compuertas tempranas + arreglos + revisión independiente + compuerta final | 2026-11-13 21:08 PST | en curso | |
| TOTAL | pasos 0-9 (sin la subida, paso 10) | | | 132 min |

corridas de compuerta: 0

- Lecturas (paso 2-3): A-L1, A-L2, A-L3, A-L4, A-CEIL/DET, B-L1L2, B-L3L4, H-A y H-B (alturas A / B) en paralelo, + CORES_L2L4 A/B
- tool fixes (tiempo dentro del paso donde ocurrieron): BE-CR0-01 18:58–19:03 (P1), BE-CR0-02 (P2-3), BE-CR0-03 19:41 (P5), BE-CR0-04 20:37 (P7), BE-CR0-05 21:22 (P9), BE-CR0-06 21:50 (P9)
- reinicio de contenedor: ninguno. Compactación de contexto 21:3x–21:40 (sin pérdida de trabajo; tiempo incluido en el paso 9)

## Bitácora detallada
- INICIO: 2026-11-13 18:41:49 PST (primera acción)
- 18:5x bid set descargado (5 PDFs A/S/specs) read-only, md5 en bidset/MD5_BIDSET.txt
- PASO 0 (arranque) INICIO 18:45:22
- PASO 0 FIN 18:51:13 (arranque + set_texto OK; 17 hojas sin texto → OCR)
- PASO 1 (inventario) INICIO 18:56:35 (OCR 17 hojas terminado antes)
- PASO 1 FIN 19:04:02 (inventario rc 0; 17 types; ~395 tags; BE-CR0-01 arreglado: I/1 en verificar_png)
- PASO 2 (lectura A) + PASO 3 (lectura B) + H-A/H-B INICIO 19:05:53 — subagentes en paralelo: A-L1, A-L2, A-L3, A-L4, A-CEIL/DET, B-L1L2, B-L3L4, H-A, H-B
- tool fix BE-CR0-01 (inventario I/1): 18:58–19:03 dentro del Paso 1; enviado a Xfinity 19:07:46
- 19:23:20 hueco de cobertura detectado (cores escalera/elevador L2-L4 sin dueño) -> lecturas A/B CORES_L2L4 lanzadas
- PASOS 2-3 FIN 19:37:37 (11 lecturas: A 7 fragmentos, B 5 fragmentos, H-A, H-B; tool fix BE-CR0-02 normalizar_fragmentos)
- PASO 4 (comparación) INICIO 19:37:37
- PASO 4 FIN 19:40:38 (comparar.py: metal 4 coinciden/3 difieren/8 solo A/1 solo B, 589 alertas; comparar_extra board-only: 196 tags, 171 difieren)
- PASO 5 (resolución) INICIO 19:40:38 — 5 resolvedores (L1, L2, L3, L4, CORES) + back-check ciego de cielos; criterios en 3_revision/CRITERIOS_RESOLUCION.md
- tool fix BE-CR0-03 (chequeos_v71.ids_canon + existing_walls, R78.15 owner board-only): 19:41:39 dentro del Paso 5
- 19:41:58 Xfinity publicó BE-CR0-01 en v81cf138p (vigente, e43b2f2); esta corrida sigue con v81cf138o + los mismos arreglos locales (equivalentes)
- PASO 5 FIN 20:17:25 (5 resolvedores + back-check cielos + fix shaft N L4 + 59 ajustes de consistencia por programa; canon unido 1118 entradas board-only/shaft, 95 cielos)
- PASO 6 (cálculo) INICIO 20:17:25 — lectura de accesorios/trims (P8b) en paralelo con validación canon.py
- 20:25:03 cambio a skill VIGENTE v81cf138s (incluye BE-CR0-01/02/03); tools re-instaladas
- PASO 6 FIN 20:28:01 (canon.py rc 0, accesorios + trims; familias en etapas/4_canon/out)
- PASO 7 (Excel) INICIO 20:28:01
- inventario_tags via bitacora (re-corrida idéntica para registro) 20:33:15
- tool fix BE-CR0-04 (comparar.ambiguos + type_id de board-only): 20:37:38 Paso 7
- PASO 7 FIN (Excel armado, reglas.py OK) 20:40:14
- tool fix BE-CR0-05 (comparar_alturas lista larga): 21:22:22 Paso 9
- 21:40:07 reanudación tras compactación de contexto (Paso 9 cierre de compuerta)