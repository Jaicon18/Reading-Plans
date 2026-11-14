#!/usr/bin/env python3
"""Reescribe la tabla de TIEMPOS.md (encabezado) conservando la bitácora debajo. Uso: tiempos_tabla.py [fin_paso9 HH:MM:SS] [corridas_finales]"""
import sys, datetime as dt, re
P = "/root/cr0/TIEMPOS.md"
D = "2026-11-13"
F = [("0", "arranque (set_texto, OCR 17 hojas)", "18:45:22", "18:51:13"),
     ("1", "inventario de tags", "18:56:35", "19:04:02"),
     ("2-3", "lecturas A y B en paralelo + H-A / H-B (alturas A / B) + CORES A/B", "19:05:53", "19:37:37"),
     ("4", "comparación A vs B", "19:37:37", "19:40:38"),
     ("5", "resolución", "19:40:38", "20:17:25"),
     ("6", "cálculo (canon.py, accesorios, trims)", "20:17:25", "20:28:01"),
     ("7", "Excel", "20:28:01", "20:40:14"),
     ("8", "markups Bluebeam walls + RCP (fin = markups_rcp 05:08:15 UTC en bitacora.jsonl)", "20:40:14", "21:08:15"),
     ("9", "compuertas tempranas + arreglos + revisión independiente + compuerta final", "21:08:15", None)]
fin9 = sys.argv[1] if len(sys.argv) > 1 else None
corr = sys.argv[2] if len(sys.argv) > 2 else "0"
def t(h, d=D):
    x = dt.datetime.fromisoformat(f"{d} {h}")
    return x if x.hour >= 12 else x + dt.timedelta(days=1)       # todo pasa en la tarde del 13 y madrugada del 14
rows, tot = [], 0
for p, desc, a, b in F:
    if p == "9":
        b = fin9
    if b:
        ta, tb = t(a), t(b); m = int((tb - ta).total_seconds() // 60); tot += m
        rows.append(f"| {p} | {desc} | {ta:%Y-%m-%d %H:%M} PST | {tb:%Y-%m-%d %H:%M} PST | {m} min |")
    else:
        rows.append(f"| {p} | {desc} | {t(a):%Y-%m-%d %H:%M} PST | en curso | |")
head = ["# TIEMPOS — CR City Hotel PRUEBA DESDE CERO 13-nov (hora de California, America/Los_Angeles, PST)", "",
        "| Paso | Qué | Inicio | Fin | Duración |", "|---|---|---|---|---|", *rows,
        f"| TOTAL | pasos 0-9 (sin la subida, paso 10) | | | {tot} min |", "",
        f"corridas de compuerta: {corr}", "",
        "- Lecturas (paso 2-3): A-L1, A-L2, A-L3, A-L4, A-CEIL/DET, B-L1L2, B-L3L4, H-A y H-B (alturas A / B) en paralelo, + CORES_L2L4 A/B",
        "- tool fixes (tiempo dentro del paso donde ocurrieron): BE-CR0-01 18:58–19:03 (P1), BE-CR0-02 (P2-3), BE-CR0-03 19:41 (P5), BE-CR0-04 20:37 (P7), BE-CR0-05 21:22 (P9), BE-CR0-06 21:50 (P9)",
        "- reinicio de contenedor: ninguno. Compactación de contexto 21:3x–21:40 (sin pérdida de trabajo; tiempo incluido en el paso 9)", "",
        "## Bitácora detallada", ""]
txt = open(P).read()
cuerpo = txt.split("## Bitácora detallada", 1)[1].lstrip("\n") if "## Bitácora detallada" in txt else "\n".join(txt.splitlines()[1:])
open(P, "w").write("\n".join(head) + cuerpo)
print("\n".join(head[:16]))
