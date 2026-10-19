#!/usr/bin/env python3
"""test_glosario.py — v73: glosario.py y vocab_trade.py (datos sintéticos)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glosario as G  # noqa: E402
import vocab_trade as V  # noqa: E402

F = []


def ok(n, c):
    print(("OK   " if c else "FALLA"), n)
    c or F.append(n)


ok("traduce tablaroca / postes metálicos / canal", G.traducir("tablaroca sobre postes metálicos y canal") ==
   "drywall sobre steel stud y track")
ok("no toca inline code", G.traducir("ver `canal` y canal") == "ver `canal` y track")
ok("no toca bloque cercado", "```\ncanal\n```" in G.traducir("```\ncanal\n```\ncanal"))
ok("faltas encuentra panel de yeso", G.faltas("dos capas de panel de yeso") == ["panel de yeso"])
ok("faltas vacía en inglés", G.faltas("two layers of 5/8\" gypsum board on 3-5/8\" studs") == [])
ok("faltas ignora código", G.faltas("campo `canal` del cierre") == [])
ok("vocab_trade: muro en prosa", [t for t, _ in V.faltas("el muro norte")] == ["muro"])
ok("vocab_trade: `muro` como código no cuenta", V.faltas("la clave `muro` del cierre") == [])
ok("lineas_sin_codigo conserva renglones", [n for n, _ in V.lineas_sin_codigo("a\n```\nb\n```\nc")] == [1, 2, 3, 4, 5])
print("test_glosario:", "OK" if not F else f"{len(F)} fallo(s)")
sys.exit(1 if F else 0)
