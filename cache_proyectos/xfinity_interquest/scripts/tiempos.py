"""TIEMPOS.md (hora de California, U-094 / U-045) de Xfinity Interquest desde /root/xf/tiempos.log + hora de fin (TZ=America/Los_Angeles).
Presupuesto U-169: 8 hojas A (< 10) = hasta 3 h activas. U-170: horas por cada 1,000 SF (TI 1,798 SF, A0.1)."""
import subprocess, datetime as dt
fin = subprocess.run(['date', '+%Y-%m-%d %H:%M'], env={'TZ': 'America/Los_Angeles'}, capture_output=True, text=True).stdout.strip()
F = lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M')
rows = [("0", "Arranque: órdenes U-001..U-166, skill v81cf77, verificar_version (0 faltantes); descarga BuildingConnected (2 archivos, solo lectura); Gmail (un solo GC); Drive Projects; copia limpia (SHX conservado)", "2026-11-10 20:02", "2026-11-10 20:20", "LEEME.md, bc/, Drive Projects"),
        ("1", "Inventario por script (inventario_tags.py) + texto del set con burbujas (compuerta_entrega texto)", "2026-11-10 20:20", "2026-11-10 20:22", "etapas/1_inventario, set_texto.json"),
        ("2-3", "Lecturas A y B independientes + lector independiente de schedules + verificación de burbujas (4 subagentes en paralelo); comparación A / B (comparar.py, comparar_extra.py)", "2026-11-10 20:22", "2026-11-10 20:40", "etapas/2_lectura, indep/, burbujas/, 3_revision/revision.md"),
        ("4-5", "Resolución A / B con imagen + re-barrido de RFI (U-156 / U-162) + canon al esquema de canon.py (formato.py, canon.py OK)", "2026-11-10 20:40", "2026-11-10 20:50", "3_revision/resolucion.md, 4_canon/out/familias_out.json (fin aprox.: lanzamiento del subagente de cálculo)"),
        ("6-8", "Cálculo + Excel fijo 6 hojas sellado + markups Bluebeam (walls, demo, RCP, EXCLUDED U-160) + imágenes (subagente, cadena.sh CHAIN-OK) + arreglo de markups de column wraps", "2026-11-10 20:50", "2026-11-10 21:15", "8_excel, tiempos.log 21:14 CHAIN-OK"),
        ("9", "Revisión independiente en paralelo (U-168 A1-A5, U-169) + docs + proposal + CHECKLIST + compuerta de entrega", "2026-11-10 21:15", fin, "ENTREGA_OK.json, revision_indep/")]
L = ["# Xfinity - Interquest, Colorado Springs, CO — registro de tiempos (hora de California, PST)", "",
     "Horas reales (tiempos.log, `TZ=America/Los_Angeles date`). Presupuesto U-169: 8 hojas A (< 10) = hasta 3 h activas. TI 1,798 SF (A0.1).", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
tot = 0
for r in rows:
    d = int((F(r[3]) - F(r[2])).total_seconds() // 60); tot += d
    L.append(f"| {r[0]} | {r[1]} | {r[2][5:]} PST | {r[3][5:]} PST | {d} min | {r[4]} |")
h = tot / 60
L.append(f"| **TOTAL** | **Arranque -> entrega verificada (sin la subida, paso 10)** | **11-10 20:02 PST** | **{fin[5:]} PST** | **{tot} min ({tot // 60} h {tot % 60:02d})** | {h / 1.798:.2f} h por cada 1,000 SF; presupuesto 3 h; referencia O'Reilly ~3 h, VS ~5.5 h, Consumer Cellular ~6 h, CR City Hotel 31 h |")
open('/root/xf/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
