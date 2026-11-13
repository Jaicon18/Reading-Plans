# adv7_falt: BE-CR40 / v120-FALT contra v81cf138 (verificación 7). Sintético; escribe solo en /tmp/verif7/tmp.
import sys, os, json, tempfile, shutil; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB, compuerta_entrega as CE
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
fn = CB.faltantes_auditoria; B = CB.B
can = {"walls": [{"id": "X9-901-01", "length_ft": 20.0}], "ceilings": [{"room": "Z9 Corridor 901", "area_sf": 50.0}],
       "misc_items": [{"ref": "EXT-Z9-2 board", "qty": 30.0}, {"ref": "BLK-216", "qty": 4.0, "location": "Corridor 216 blocking at grab bars"},
                      {"ref": "BLK-901", "qty": 4.0, "location": "Corridor 901 blocking"}],
       "trim_items": [{"id": "CB-216", "qty": 12.0, "room": "Corridor 216", "desc": "corner bead"}],
       "rcp_tags": [{"sheet": "X9.01", "tag": "GYP-9", "height": "8'-11\"", "rows": ["ceilings[0]"]}]}
A = "Auditoria/AUDITORIA_U181_rev9.md"
def run(raw, c=can, k=A, x=None):
    return fn(B(canon=c, textos=dict({k: raw}, **(x or {}))))
def show(tag, raw, **kw):
    r = run(raw, **kw); print(tag, repr(raw)[:90], "->", r[0], "|", (r[1][0] if len(r) > 1 and r[1] else "")[:110] if isinstance(r, tuple) else r)
print("== A: celdas de tabla separadas (faltante y cielo en celdas distintas), cuarto 901 CARGADO -> debe FAIL")
show("A0 control", "| 1 | corridor 901 ceiling missing | OPEN |")
show("A1", "| 1 | corridor 901 ceiling | MISSING | OPEN |")
show("A2", "| # | Item | Status |\n|---|---|---|\n| 1 | Corridor 901 ceiling | NOT LOADED |")
show("A3", "| 1 | Room 901 | ceiling | missing |")
show("A4", "corridor 901 ceiling; status: missing")
show("A5", "1\tcorridor 901 ceiling\tMISSING")
show("A6", "- Corridor 901 ceiling. Not loaded in the take-off.")
show("A7", "| 1 | 901 | Corridor | CLG | FALTA |")
print("== B: otras formas de 'falta' (cuarto 901 CARGADO) -> debe FAIL")
for ln in ("corridor 901 ceiling isn't loaded", "corridor 901 ceiling wasn't counted", "corridor 901 ceiling never added to the take-off",
           "corridor 901 ceiling not in the take off", "corridor 901 ceiling forgotten", "se olvidó el cielo del corredor 901",
           "corridor 901 ceiling needs to be added", "cielo del corredor 901 pendiente de cargar", "no hay cielo en el corredor 901",
           "corridor 901 ceiling: 0 SF in the Excel", "corridor 901 ceiling not yet taken off", "corridor 901 ceiling - TBD, not in TO"):
    show("B", "| 1 | " + ln + " | OPEN |")
print("== D: CERRADO con una ref del MISMO cuarto que NO es cielo (cuarto 216 FALTA de verdad) -> debe FAIL")
show("D0 control (muro exterior)", "| 1 | corridor 216 ceiling missing | CERRADO: EXT-Z9-2 (1/X9.31) | OPEN |")
show("D1 blocking misc", "| 1 | corridor 216 ceiling missing | CERRADO: BLK-216 (1/X9.31) | OPEN |")
show("D2 corner bead trim", "| 1 | corridor 216 ceiling missing | CERRADO: CB-216 (1/X9.31) | OPEN |")
dc = ("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
      "Z9 901 Corridor,Z9,double,RS-9,GYP-9,8'-11\",7/X9.23,x,upper: BLK-901; lower: BLK-901\n")
show("E1 DOBLE_CIELO upper/lower = blocking del 901 + hallazgo falso '901 missing'", "| 1 | corridor 901 ceiling missing | OPEN |",
     x={"Auditoria/DOBLE_CIELO.csv": dc})
print("== C: descubrimiento real de archivos (Ctx -> B.desde_ctx), cuarto 901 CARGADO, hallazgo falso -> debe FAIL")
def ctx_case(rel, entrega_name="entrega_rev9", extra=None):
    w = tempfile.mkdtemp(dir=T); os.makedirs(os.path.join(w, "4_canon"))
    json.dump(can, open(os.path.join(w, "4_canon", "canon.json"), "w"))
    for r2, txt in dict({rel: "| 1 | corridor 901 ceiling missing | OPEN |\n"}, **(extra or {})).items():
        p = os.path.join(w, r2); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(txt)
    try:
        c = CE.Ctx(w); b = B.desde_ctx(c)
        b.canon = can
        found = sorted(set(list((b.textos or {}).keys()) + list((getattr(b, "textos_hallazgos", {}) or {}).keys())))
        r = fn(b); return r[0], found
    except Exception as e:
        return "ERR " + repr(e)[:120], []
for rel in ("COORDINACION/hallazgos_rev9.md", "REVIEW_rev9.md", "review_rev9.md", "Review_rev9.md", "hallazgos_rev9.md",
            "Coordinacion/hallazgos.md", "COORDINACIÓN/hallazgos.md", "coordinacion/hallazgos.md", "NOTAS_COORDINACION_rev9.md",
            "QA_rev9.md", "PENDIENTES_rev9.md", "INFORME_COORDINACION_rev9.md", "COORDINACION/hallazgos_rev9.xlsx.txt"):
    print("C", rel, "->", ctx_case(rel))
print("C-rev", "REVIEW_rev9.md + RESUMEN_rev10_plan.md ->", ctx_case("REVIEW_rev9.md", extra={"RESUMEN_rev10_plan.md": "plan\n"}))
