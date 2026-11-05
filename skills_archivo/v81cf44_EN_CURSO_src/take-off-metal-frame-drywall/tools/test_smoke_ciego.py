#!/usr/bin/env python3
"""test_smoke_ciego.py — v73d: smoke test del paquete CIEGO. Las tools importan y corren sobre un canon 100 %
inventado (coordenadas, rooms, largos y tags inventados; ningún dato de un set real). No trae fixtures."""
import importlib
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
os.environ.setdefault("TAKEOFF_WORK", tempfile.mkdtemp(prefix="smoke_"))
F = []
RETIRADAS = {"excel", "hojas_por_tipo", "auditor", "hoja_detalle_img", "localizar", "cruzar_mep"}          # retiradas en v66 (E24): levantan ImportError a propósito


def ok(n, c, info=""):
    print(("OK   " if c else "FALLA"), n, info)
    c or F.append(n)


# 1) todas las tools importan
malos = []
for f in sorted(os.listdir(AQUI)):
    if f.endswith(".py") and not f.startswith("test_") and f[:-3] not in RETIRADAS:
        try:
            importlib.import_module(f[:-3])
        except ImportError as e:
            if "RETIRADA" not in str(e):                     # stub retirado en v66 (E24): esperado
                malos.append(f"{f}: {type(e).__name__}: {e}")
        except Exception as e:                               # noqa: BLE001
            malos.append(f"{f}: {type(e).__name__}: {e}")
ok("todas las tools importan", not malos, "; ".join(malos[:5]))

# 2) canon inventado: un wall K con cota, un ducto de mep.cruces, un segmento sin tag con otro espesor
import chequeos_v73 as C  # noqa: E402
import accesorios as A  # noqa: E402
import canon  # noqa: E402
import particion  # noqa: E402
canon_x = {
    "walls": [
        {"id": "XK-1", "tag": "QK", "element": "wall", "tag_ids": ["T1"], "length_ft": 5.0, "length_status": "CONFIRMADO",
         "band": {"ori": "H", "c0": 300, "c1": 306, "lo": 500, "hi": 590, "sheet": "Q1.01"},
         "dim_scan": {"found": [{"text": "5' - 0\"", "value_ft": 5.0}], "source": "cotas_banda.py"}},
        {"id": "XU-1", "tag": "Q1", "tag_ids": [], "default_type_source": "Q1.01 note", "thickness_measured_in": 4.9,
         "length_ft": 2.0, "length_op": "1.25 + 0.75 = 2.0"},
        {"id": "XW-1", "tag": "Q1", "rows": 2, "length_ft": 9.0}],
    "partition_schedule": [{"type": "Q1", "thickness_in": 4.875}],
    "mep_sweep": {"sheets": ["P9.01", "M9.01"], "source": "mep.registro", "registro": {
        "dx_pt": 0, "dy_pt": 0, "matches": 40, "source": "mep.registro"}},
    "mep_penetrations": [{"ref": "duct a", "wall": "XW-1", "width_in": 10, "xy": [1, 2], "method": "mep.cruces",
                          "kind": "duct", "source": "M9.01"}],
    "deflection_clips": {"none_reason": "notas barridas sin clips", "source": "Q0.01"},
    "plywood_strips": [{"ref": "s1", "uso": "substrate"}],
}
r = C.revisar(canon_x, {"familias": {"stud reinforcement MEP": 2.0}})
ok("chequeos_v73 sobre el canon inventado: 0 fallas", r["fallas"] == [], r["fallas"][:3])
o = A.Out()
A.stud_reinforcement(canon_x, None, o)
ok("accesorios: plates de un ducto en wall de 2 rows = 2", o.fam[A.F_REINF] == 2)
t = canon.track_by_element({"walls": [{"id": "XW-1", "stud_size": "3-5/8\""}]},
                           {"renglones": [{"id": "W:XW-1", "element": "wall", "bottom_lf": 9.0, "top_lf": 9.0}]},
                           {"bottom track (todos)": 9.0, "top / deflection track (todos)": 9.0})
ok("canon.track_by_element", t["bottom"] == {'Bottom track 3-5/8"': 9.0}, t)
pw = particion.particion({"constants": {"plan_scale_pt_per_ft": {"value": 18, "source": "Q1.01"}}, "walls": [
    {"id": "P1", "tag": "Q1", "element": "wall", "sheet": "Q1.01", "length_ft": 5.0, "tag_ids": ["T2"],
     "band": {"ori": "H", "c0": 0, "c1": 8, "lo": 0, "hi": 90}}]}, "eje")
ok("particion corre", pw["types"]["Q1"]["walls"] == 1)

# 3) PDF inventado: cotas_banda y planmark
import pymupdf as fitz  # noqa: E402
import cotas_banda as CB  # noqa: E402
import planmark as PM  # noqa: E402
d = tempfile.mkdtemp(prefix="smk_")
pdf = os.path.join(d, "x.pdf")
doc = fitz.open()
pg = doc.new_page(width=500, height=400)
pg.draw_line(fitz.Point(50, 100), fitz.Point(450, 100), width=2)
pg.draw_line(fitz.Point(50, 108), fitz.Point(450, 108), width=2)
pg.insert_text((230, 90), "22' - 2\"", fontsize=8)
doc.save(pdf)
f = CB.dim_scan(pdf, 1, {"ori": "H", "c0": 100, "c1": 108, "lo": 50, "hi": 450})["found"]
ok("cotas_banda encuentra la cota inventada", [x["value_ft"] for x in f] == [round(22 + 2 / 12, 4)], f)
os.environ["PLANMARK_CACHE"] = os.path.join(d, "c")
h = PM.Hoja(pdf, 1, 72)
ok("planmark verifica la banda inventada", h.verify([{"id": "Z", "band": {"ori": "H", "c0": 100, "c1": 108, "lo": 50,
                                                                         "hi": 450}, "lf": 22.2}]))

# 4) registro, glosario, calificador
import registro as R  # noqa: E402
import glosario as G  # noqa: E402
import eval_takeoff as E  # noqa: E402
p = os.path.join(d, "reg.json")
R.crear(p, [{"id": "X-1", "tipo": "otro", "ubicacion": "inventada", "fuente": "Q0.01"}])
R.marcar(p, "X-1", "verificado", "Q0.01")
ok("registro corregir", R.corregir(p, "X-1", "verificado", "NO APLICA: Q0.01")["corregido"] == 1)
ok("glosario", G.faltas("tablaroca") == ["tablaroca"] and G.traducir("canal") == "track")
ok("calificador min == max", E.grade_rango(5.0, 5.0, 5.05, 0.02, 0.1)[0].startswith("IGUAL"))
print("test_smoke_ciego:", "OK" if not F else f"{len(F)} falla(s)")
sys.exit(1 if F else 0)
