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
