# Handoff a la nueva sesión de coordinación (2-nov-2026)

La sesión "⭐ REFERENCIA MAESTRA — Take-offs metal frame y drywall (NO BORRAR)" (session_01VMB6bPApabFaSdfrBk1gKK) queda como referencia histórica. NO archivar.

## Lo primero que debe leer la sesión nueva
1. cache_proyectos/REGLAS_USUARIO_CLAUDE.md (todas las reglas inviolables del usuario; copiar a ~/.claude/CLAUDE.md si no están).
2. cache_proyectos/SKILL_working.md (reglas del skill, R80e.*) y cache_proyectos/BIBLIOTECA_ERRORES.md.
3. skills_archivo/INDICE.md (mejor skill vigente).
4. cache_proyectos/USO_SEMANAL.md (calibración de uso: O'Reilly ~3 h/≈4 %, VS Downey ~5.5 h/≈6–7 %, Chuze ~8 h/≈13–14 % de la semana).

## Flujo obligatorio (R80e.120)
Una sesión nueva por proyecto con su nombre; permisos de red listos antes; lecturas A y B en paralelo en sesiones cortas; RFI en bloque con botones (4 por ventana, total/quedan); trades que no hacemos y tornillería EXCLUDED sin RFI.

## Estado de proyectos al 2-nov
| Proyecto | Estado | Sesión |
|---|---|---|
| Victoria's Secret #679 Downey | rev4 FINAL, 0 RFI. Bid 2-nov 1 PM PT | session_01BLzQaE4gnPbfm7CcnQxKKv |
| Chuze Fitness Austin Bluffs (Hilbers; también NNI) | cerrando FINAL (RFI contestados con la opción recomendada por orden del usuario 2-nov). Bid 4-nov 11 AM PT | session_01BLzQaFgUrmojCWAXA96ohf (entra a BuildingConnected) |
| O'Reilly Evans #1 | pasada 1 rev4 + pasada 2 FINAL; usuario compara contra su take-off humano (NUNCA abrirlo) | p1 session_01BLzQaGqFUvXc5j4BtA8MyA · p2 session_01BLzQaG8vLjwc8gVgTxQDQd |
| Barnes & Noble Colorado Springs | rev13 final | — |
| Bank of America Broomfield | final | — |
| Port of Subs Littleton | no hecho (bid 2025 vencido); sesión archivada | — |
| Runner API B&N | en pausa (≈$12 de $60 usados de la autorización automática) | session_01UQBQT8jCVU6KW8QmKhZS83 |

## Tareas programadas que hoy disparan en la sesión maestra
- "Vigilar addenda de bids activos" (trig_01DkBP6g1aEDWyYgSeS9woxt, cada 3 h, se apaga después del 4-nov 11 AM PT).
- "Pedir captura de usage diaria" (trig_016DoCE37PzoaKt1PuELQoxk, 7:51 AM Denver).
Al arrancar la sesión nueva: recrearlas apuntando a la sesión nueva (create_trigger) y desactivar las viejas (update_trigger enabled=false).

## Entorno
env_01KvJ1Y5fQ1msxzgKu7dToYG ("pruebas unicamente"): TAKEOFF_API_KEY, gdrive_sa_json (NUNCA leer), BC_EMAIL/BC_PASSWORD (solo para login de BuildingConnected, nunca imprimir). Allowed domains: elite-constructionplans.com, buildingconnected.com, app.buildingconnected.com, accounts.autodesk.com, autodesk.com, panteratools, myfbm. Sesiones nuevas: source_url del repo + source_revision claude/gifted-pasteur-x2sfzs.

## CHECKLIST AHORRO DE TOKENS (usuario 2-nov: "no olvides aplicar las reglas para ahorrar tokens") — obligatorio en todo proyecto
1. Una sesión por proyecto; lecturas A y B, auditor, cobertura, subidas = SUBAGENTES en paralelo (su salida no infla el contexto principal) (R80e.120/121).
2. Permisos de red y bid set limpio ANTES de lanzar (nada de arranques fallidos).
3. Caché primero: cache_proyectos/<proyecto>/ y scratchpad; nunca volver a bajar, leer ni recalcular lo ya verificado.
4. Lectura A y B una vez cada una; cada diferencia A/B = UNA revisión dirigida con recorte; si sigue la duda = Review Item, no otra lectura completa.
5. Correcciones: verificar SOLO los ítems cambiados; nunca relanzar revisiones completas.
6. Los PROGRAMAS calculan (inventario_tags, comparar, canon, reglas, plantilla); el modelo solo lee.
7. Sin RFI para tornillería, trades que no hacemos, ductos, cielos existentes sin tipo: EXCLUDED directo.
8. RFI en bloque (4 por ventana) y se procesan todos juntos una sola vez.
9. Mensajes y reportes cortos; check-ins espaciados (25–60 min), sin sondeos repetidos; leer otras sesiones con filtros (kinds) y nunca volcar transcripciones completas.
10. Medir tiempo y % semanal por proyecto vs O'Reilly ~3 h/≈4 %, VS ~5.5 h/≈6–7 %, Chuze ~8–9 h/≈13–14 %.

## ESTADO AL TRASPASO (3-nov ~8:30 PM PST) — COORDINACIÓN toma TODO desde aquí
- Skill de órdenes: .claude/skills/jc-hunter-ordenes (carga sola; hook SessionStart corre verificar_version). Skill de take-off VIGENTE: el que marca skills_archivo/INDICE.md (hoy v81cf18). Una sola línea (BE-115).
- Entregas: SOLO Shared drives › JC HUNTER PROJECTS › Claude outputs (id 1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc). La carpeta Projects › Claude outputs (1rUgu9…) es vieja: el usuario la va a renombrar "_ARCHIVO VIEJO - NO USAR"; no usarla.
- El usuario revisa en orden hacia adelante: O'Reilly (pasada2 FINAL, revisándolo) → Victoria's Secret (rev17 FINAL) → Chuze (rev FINAL5) → Chick-fil-A #2284 (rev4; 6 RFI para presentar con botones A/B/C cuando llegue). Lo que está revisando no se toca; lo entregado = 100 % terminado (BE-117).
- EN CURSO: Harbor Freight Tools - Loveland, CO (Marco Contractors) 11-03-26, session_01BLzQaEFLFLD6jyuTm7dNV1; bid 3-nov 10:00 AM PST (11 AM MST); meta entrega verificada antes de 2:00 AM PST. Check-in de avance cada hora (BE-118) — COORDINACIÓN debe armarlo (send_later 60 min) hasta la entrega y reportar al usuario con ruta.
- Siguiente candidato (due más cercano): Chagee - Santa Anita Mall, Arcadia, CA (Americo Builders), bid 3-nov EOD — el usuario no lo ha aprobado aún.
- Pendientes del usuario: renombrar carpeta vieja; autorizar push en sesión CFA (commit local BE-CF18) y respaldo en sesión O'Reilly (o dejarlos).
- Reglas nuevas de hoy: R-ALC-05..12, BE-114..118, BE-CF16, una sola carpeta, solo versión más reciente, otros GC en Gmail, monitoreo inviolable (todas en CLAUDE.md / REGLAS_USUARIO_CLAUDE.md / ORDENES_DEL_USUARIO.md).
