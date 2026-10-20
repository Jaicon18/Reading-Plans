#!/usr/bin/env python3
"""test_reglas.py — v72b: UN TEST POR REGLA del catálogo (reglas_catalogo.py + reglas_clasificacion.py).

  (a) cada chequeo de reglas.py tiene un caso que VIOLA la regla (falla) y el proyecto sintético correcto
      (fixture_reglas.py) que pasa; una regla (a) pasa su test si TODOS sus chequeos lo pasan;
  (b) por cada regla: un caso de su trigger sin evidencia → falla; con su evidencia (N/HOJA + imagen que existe +
      valor) → pasa; con un valor que contradice la regla (prohibido / falta lo requerido) → falla;
  (c) la fusión / anulación no está vacía y no se apunta a sí misma.
Además: el catálogo completo está clasificado, el fixture da REGLAS OK, plantilla_excel.armar NO escribe el Excel
si la compuerta falla y el sello del libro se verifica.
Datos sintéticos (ningún proyecto real).  Correr: python3 test_reglas.py   (rc 0 = todo OK)
"""
import copy
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
os.environ.pop("BITACORA", None)
import fixture_reglas as FX  # noqa: E402
import reglas as R  # noqa: E402
import reglas_catalogo as RC  # noqa: E402
import reglas_clasificacion as CL  # noqa: E402

FALLOS = []
BASE = tempfile.mkdtemp(prefix="test_reglas_base_")
FX.crear(BASE)


def P(d, *x):
    return os.path.join(d, *x)


def leer(d):
    return json.load(open(P(d, "4_canon", "takeoff_canon.json")))


def guardar(d, c):
    json.dump(c, open(P(d, "4_canon", "takeoff_canon.json"), "w"))


def jw(p, o):
    json.dump(o, open(p, "w"))


def W(id_, **kw):
    w = {"id": id_, "tag": "X1", "element": "wall", "sheet": "Z1.01", "tag_ids": ["PT0001"], "stud_size": "3-5/8\"",
         "oc_in": 16, "rows": 1, "length_ft": 5.0, "length_source": "Z1.01 dimension", "length_status": "CONFIRMADO",
         "height_ft": 9.0, "height_source": "1/Z5.01", "height_status": "CONFIRMADO", "detail": "1/Z5.01",
         "band": {"ori": "H", "c0": 400, "c1": 406, "lo": 400, "hi": 490, "sheet": "Z1.01"}, "openings": [],
         "faces": [], "source": "Z1.01"}
    w.update(kw)
    return w


def OP(**kw):
    o = {"ref": "OP1", "kind": "window", "ro_w_ft": 3.0, "head_ft": 7.0, "head_source": "Z1.01", "sill_ft": 3.0,
         "sill_source": "Z1.01", "with_sill": True, "source": "Z1.01", "header_type": "track", "pieces": 1,
         "pieces_source": "1/Z5.01", "jamb_return": False, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "1/Z5.01"}
    o.update(kw)
    return o


def con_canon(fn):
    def m(d):
        c = leer(d)
        fn(c)
        guardar(d, c)
    return m


def con_op(**kw):
    def f(c):
        c["walls"][0]["openings"] = [OP(**kw)]
    return con_canon(f)


def agregar_wall(**kw):
    return con_canon(lambda c: c["walls"].append(W("WZ", **kw)))


def hook_fresco(f, mod):
    def h(ctx):
        R.recalcular(ctx)
        if ctx.fresco is None:
            ctx.fresco = {}
        ctx.fresco.setdefault(f, copy.deepcopy(ctx.salidas.get(f) or {}))
        if f == "familias_out.json":
            ctx.fresco[f].setdefault("familias", {})
        mod(ctx.fresco[f])
    return h


def _set_fam(k, v):
    return hook_fresco("familias_out.json", lambda o: o["familias"].__setitem__(k, v))


def m_vigencia(d):
    p = P(d, "out", "familias_out.json")
    o = json.load(open(p))
    o["familias"]["bottom track (todos)"] = 999.0
    jw(p, o)


def m_esquinas(c):
    b = lambda ori, c0, c1, lo, hi: {"sheet": "Z1.01", "ori": ori, "c0": c0, "c1": c1, "lo": lo, "hi": hi}
    c["walls"] += [W("H1", band=b("H", 600, 607, 600, 793), length_ft=193 / 18),
                   W("V1", band=b("V", 793, 800, 607, 900), length_ft=293 / 18)]


def m_pier(c):
    bx = {"ori": "BOX", "c0": 900, "c1": 940, "lo": 10, "hi": 40, "sheet": "Z1.01"}
    c["walls"] += [W("PX", tag="EXT", element="pier", tag_ids=[], location="exterior", band=dict(bx)),
                   W("PC", tag="C1", element="pier", band=dict(bx, c0=901, c1=939))]


def m_k_sin_hatch(c):
    c["walls"].append(W("K1", tag="X1K"))


def m_diag(c):
    c["walls"].append(W("D1", band={"ori": "D", "p0": [0, 0], "p1": [180, 0], "sheet": "Z1.01"}))


def m_vigas(d):
    jw(P(d, "out", "vigas_out.json"), {"walls_bajo_viga": [{"wall": "W1", "profile": "W14X30", "beam_axis_pt": 103}]})


def m_mep(c):
    c["mep_penetrations"] = [{"ref": "duct 8in", "wall": "W1", "dia_in": 8, "source": "M1.01"}]


def m_r73_2(c):
    c["walls"].append(W("K2", tag="X1K", hatch_extent={"value_ft": 5.0, "source": "Z1.01", "img": "img/evid.png"},
                        dim_scan={"found": [], "source": "cotas_banda.py"}))
    c["ballistic_jogs"] = [{"ref": "jog", "length_ft": 0.5, "height_ft": 9.0, "detail": "1/Z5.01", "faces_5_8": 1,
                            "source": "Z1.01"}]


def m_r73_5(d):
    c = leer(d)
    c["mep_penetrations"] = [{"ref": "duct 8", "wall": "W1", "width_in": 8, "xy": [450, 403], "method": "mep.cruces",
                              "kind": "duct", "source": "M1.01"}]
    guardar(d, c)
    p = P(d, "out", "familias_out.json")
    o = json.load(open(p))
    o["familias"]["stud reinforcement MEP"] = 5.0
    jw(p, o)


def m_side(c):
    c["walls"][0]["faces"][0]["side"] = "N"


def m_frp_jogs(c):
    c["tile_base"] = [{"room": "901", "perimeter_ft": 30.0, "perimeter_basis": "net",
                       "gross_ft": {"value": 30.0, "source": "Z6.01"}, "doors": [],
                       "inside_corners": {"value": 7, "vertices": 10, "outside_corners": 3, "source": "Z6.01"},
                       "source": "Z6.01"}]


def m_frp_net(c):
    c["tile_base"] = [{"room": "901", "perimeter_ft": 30.0, "perimeter_basis": "net",
                       "gross_ft": {"value": 36.0, "source": "Z6.01"}, "doors": [{"ref": "D1", "ro_w_ft": 3.0}],
                       "inside_corners": {"value": 4, "vertices": 4, "outside_corners": 0, "source": "Z6.01"},
                       "source": "Z6.01"}]


def m_atm(c):
    c["walls"][0]["openings"] = [OP(ref="ATM-1", kind="atm", atm_recess={"width_ft": 3.0, "width_status": "CRITERIO"})]


def m_excel(d):
    import plantilla_excel as PE
    import test_plantilla_v67 as TP
    fo = json.load(open(P(d, "out", "familias_out.json")))
    PE._escribir(PE.fusionar(TP.takeoff(), fo), P(d, "x.xlsx"), {"huella": {"version": "test"}})


def m_ciego(tmp):
    """SKILL con un valor de proyecto: A_CIEGO lo ve (se apunta reglas.AQUI a una copia)."""
    sk = P(tmp, "take-off-metal-frame-drywall")
    os.makedirs(P(tmp, "tools"))
    os.makedirs(sk)
    open(P(sk, "SKILL.md"), "w").write("Regla general.\nEl muro mide 1,234 LF en Broomfield.\n")  # [ciego-ok] caso malo sintético de A_CIEGO
    return P(tmp, "tools")


# chequeo -> (mutación de la carpeta, hook sobre el ctx, opciones)
MALOS = {
    "A_CANON": (lambda d: os.remove(P(d, "4_canon", "takeoff_canon.json")), None),
    "A_VIGENCIA": (m_vigencia, None),
    "A_ETAPAS": (lambda d: os.remove(P(d, "2_lectura", "canon_B.json")), None),
    "A_ESQUINAS": (con_canon(m_esquinas), None),
    "A_R71_1": (con_canon(lambda c: (c["constants"].pop("north_arrow"), c.__setitem__("facades", [{"id": "N"}]))), None),
    "A_R71_2": (con_canon(m_pier), None),
    "A_R71_3": (con_canon(lambda c: c.__setitem__("sealant_items", [{"ref": "door bulkhead sealant", "lf": 9}])), None),
    "A_R71_5": (con_canon(lambda c: c.__setitem__("tags_descartados", [{"id": "PT9", "motivo": "es de otra tarea",
                                                                         "imagen": "img/evid.png"}])), None),
    "A_R72_1": (con_canon(m_k_sin_hatch), None),
    "A_R72_2": (con_canon(m_diag), None),
    "A_R72_3": (con_canon(m_pier), None),
    "A_R72_4": (m_vigas, None),
    "A_R72_5": (con_canon(m_mep), None),
    "A_R72_6": (con_canon(m_side), None),
    "A_R72_10": (con_canon(m_frp_jogs), None),
    "A_R72_11": (con_canon(m_atm), None),
    "A_R73_1": (agregar_wall(tag="X1K", hatch_extent={"value_ft": 5.0, "source": "Z1.01", "img": "img/evid.png"}),
                None),
    "A_R73_2": (con_canon(m_r73_2), None),
    "A_R73_5": (m_r73_5, None),
    "A_R73_3": (con_canon(lambda c: c.__setitem__("plywood_strips", [{"ref": "p1", "lf": 4.0, "width_ft": 1.0,
                                                                       "material": "frt_3_4", "source": "Z1.01"}])), None),
    "A_R73_6": (con_canon(lambda c: c.pop("deflection_clips")), None),
    "A_R73_8": (con_canon(lambda c: c["walls"][0].update(length_op="1.5 + 2.25 + 1.0 = 5.0")), None),
    "A_R73_7": (con_canon(lambda c: (c.setdefault("partition_schedule", []).append(
        {"type": "X1", "thickness_in": 4.875, "source": "1/Z5.01"}), c["walls"].append(
        W("XU", tag_ids=[], default_type_source="Z1.01 note A", thickness_measured_in=8.5)))), None),
    "A_VIGAS_OUT": (lambda d: os.remove(P(d, "out", "vigas_out.json")), None),
    "A_ESTADO_DIM": (con_canon(lambda c: c["walls"][0].update(length_status="DERIVADO",
                                                              length_source="Z1.01 ~10 ft a ojo")), None),
    "A_FUENTES": (con_canon(lambda c: [c["walls"][0].pop(k) for k in ("length_source", "source")]), None),
    "A_DETALLE": (con_canon(lambda c: c["walls"][0].pop("detail")), None),
    "A_EJES": (agregar_wall(tag="EXT", tag_ids=[], location="exterior", facade="N, E"), None),
    "A_RFI_DELTA": (con_canon(lambda c: c.__setitem__("rfis", [{"id": "RFI-1", "pregunta": "x"}])), None),
    "A_TAG_IDS": (con_canon(lambda c: c["walls"][0].pop("tag_ids")), None),
    "A_DOOR_SILL": (con_op(ref="D1", kind="door", with_sill=True, sill_pieces=2), None),
    "A_DUCTOS": (con_op(ref="duct 12x12", kind="opening"), None),
    "A_HEADER_LF": (con_op(), _set_fam("header / box beam", 999.0)),
    "A_BOX4": (con_op(header_type="6\" BOX BEAM", pieces=2), None),
    "A_RUN_ENDS": (con_op(continuous_run=True), None),
    "A_STOREFRONT": (con_op(ref="SF1", kind="storefront"), None),
    "A_SILL": (None, hook_fresco("headers_in.json", lambda o: o.setdefault("openings", []).append(
        {"ref": "W9", "with_sill": True, "ro_w_ft": 6.0, "sill_pieces": 1}))),
    "A_TRACK_RUNS": (None, hook_fresco("corridas_out.json", lambda o: o["renglones"][0].update(bottom_lf=0.0))),
    "A_BALLISTIC": (agregar_wall(tag="X1K", hatch_extent={"value_ft": 5.0, "source": "Z1.01", "img": "img/evid.png"}),
                    None),
    "A_ANCHORS": (lambda d: jw(P(d, "out", "accesorios_out.json"), {"filas": [
        {"familia": "expansion anchors", "operacion": "bottom track exterior sobre losa 99.0 LF (3 walls) / 0.6667"}]}),
        None),
    "A_FRP": (con_canon(m_frp_net), None),
    "A_MR": (con_canon(lambda c: c["walls"][0]["faces"][0].update(board="5/8 MR")), None),
    "A_LAYERS_FACE": (con_canon(lambda c: c["walls"][0].update(layers=2)), None),
    "A_WRAP_FOS": (agregar_wall(tag="CW", element="column_wrap"), None),
    "A_CEILING_SYS": (con_canon(lambda c: c.__setitem__("ceilings", [{"room": "901", "system": "stud_joist",
                                                                      "source": "Z4.01"}])), None),
    "A_CANOPY": (con_canon(lambda c: c.__setitem__("runs", [{"id": "CS1", "element": "canopy_soffit"}])), None),
    "A_HANGER": (None, hook_fresco("familias_out.json", lambda o: (o["familias"].__setitem__("hanger wire", 5.0),
                                                                    o.__setitem__("hanger_pcs", [])))),
    "A_TRANSICION": (agregar_wall(element="ceiling_transition"), None),
    "A_FACADES": (con_canon(lambda c: c.__setitem__("facades", [{"id": "N", "source": "Z9.01"}])), None),
    "A_STOPS_BEAM": (con_canon(lambda c: c["walls"][0].update(stops_under_beam={"value": True})), None),
    "A_ACCESORIOS": (None, hook_fresco("familias_out.json", lambda o: o["estado_accesorios"].__setitem__(
        "slab pins", "PENDIENTE"))),
    "A_CLADDING": (None, hook_fresco("familias_out.json", lambda o: o["filas"].append(
        {"familia": "furring channel", "source": "7/Z9.31 hat channel at metal panel"}))),
    "A_BLOCKING": (con_canon(lambda c: c.__setitem__("blocking_items", [{"ref": "b1", "unit": "sf", "label": "X"}])),
                   None),
    "A_PLYWOOD": (con_canon(lambda c: c.__setitem__("plywood_strips", [{"ref": "p1", "material": "osb"}])), None),
    "A_CEMENT": (con_canon(m_frp_net), _set_fam("cement board", 0.0)),
    "A_DECK_BREAKS": (con_canon(lambda c: c.pop("deck_breaks_none_reason")), None),
    "A_JAMB_RETURN": (con_op(jamb_return=None), None),
    "A_MEP_SWEEP": (con_canon(lambda c: c["mep_sweep"]["registro"].update(matches=5)), None),
    "A_FO_MODULO": (con_op(ro_w_ft=1.0, pieces=2), None),
    "A_IDS": (agregar_wall(id="W1"), None),
    "A_DUPLICADOS": (con_canon(lambda c: c["walls"].append(dict(copy.deepcopy(c["walls"][0]), id="W1b"))), None),
    "A_PURLIN": (con_canon(lambda c: c["walls"][0].update(to_deck=True)), None),
    "A_BRACING": (None, hook_fresco("corridas_out.json", lambda o: o["renglones"].append(
        {"id": "Z", "orientation": "vertical", "height_ft": 13.0, "bracing_rows": 1}))),
    "A_PARAPET": (agregar_wall(tag="EXT-PARAPET", element="parapet", tag_ids=[]), None),
    "A_LEVEL5": (con_canon(lambda c: c.__setitem__("level5_items", [{"ref": "L5", "wall": "W1"}])), None),
    "A_DESCARTADOS": (con_canon(lambda c: c.__setitem__("tags_descartados", [{"id": "PT9", "motivo": ""}])), None),
    "A_BITACORA": (lambda d: os.remove(P(d, "bitacora.jsonl")), None),
    "A_ARCHIVOS": (lambda d: os.remove(P(d, "3_revision", "resolucion.md")), None),
    "A_EXCEL": (m_excel, None, "excel"),
    "A_AS_NEEDED": (con_op(header_type="BOX HEADER AS NEEDED", pieces=0, pieces_source=""), None),
    "A_BANDAS": (con_op(head_ft=None), None),
    "A_BITACORA_FINAL": (m_excel, None, "excel"),
    "A_CATALOGO": (None, None, "catalogo"),
    "A_CIEGO": (None, None, "ciego"),
}


def correr(ch):
    """-> (n fallas con la regla violada, n fallas en el fixture correcto)."""
    fn = R.CHEQUEOS[ch][0]
    spec = MALOS[ch]
    opc = spec[2] if len(spec) > 2 else None
    ok = len(fn(R.Ctx(BASE)))
    d = tempfile.mkdtemp(prefix="tr_")
    shutil.copytree(BASE, d, dirs_exist_ok=True)
    try:
        if spec[0]:
            spec[0](d)
        ctx = R.Ctx(d, P(d, "x.xlsx") if opc == "excel" else None)
        if spec[1]:
            spec[1](ctx)
        if opc == "catalogo":
            orig = R.catalogo_y_clasif
            cat, cls = orig()
            R.catalogo_y_clasif = lambda: (cat + [{"id": "S:nueva-regla", "titulo": "x", "texto": "x"}], cls)
            try:
                mal = len(fn(ctx))
            finally:
                R.catalogo_y_clasif = orig
        elif opc == "ciego":
            orig = R.AQUI
            R.AQUI = m_ciego(d)
            try:
                mal = len(fn(ctx))
            finally:
                R.AQUI = orig
        else:
            mal = len(fn(ctx))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return mal, ok


# ------------------------------------------------------------------------------------------- (b): casos por trigger
def caso_para(trigger, c, d):
    """Agrega al canon c un elemento del trigger SIN evidencia y devuelve el id del caso."""
    if trigger == "corrida":
        return "corrida"
    w = c["walls"]
    base = {"id": "WZ", "tag": "X1", "element": "wall", "sheet": "Z1.01", "tag_ids": ["PT0001"], "length_ft": 5.0,
            "length_status": "DERIVADO", "height_ft": 9.0, "openings": [], "faces": []}
    nuevos = {
        "walls": {}, "walls_medidos": {}, "walls_alto": {}, "walls_ext": {"tag": "EXT", "location": "exterior"},
        "walls_k": {"tag": "X1K"}, "walls_deck": {"to_deck": True}, "walls_2row": {"rows": 2},
        "walls_sin_tag": {"tag_ids": []}, "walls_cadena": {"length_source": "Z1.01 sum of the string 2'+3'"},
        "faces": {"faces": [{"board": "5/8 regular", "layers": 1}]},
        "soffits": {"element": "soffit_side"}, "cajas": {"element": "column_wrap", "sheathing_none_reason": "sintético (v76 R76.2)"}, "parapets": {"element": "parapet"},
        "otros_framing": {"element": "vestibule_head"}, "pendientes": {"length_status": "PENDIENTE"},
    }
    if trigger in nuevos:
        w.append(dict(base, **nuevos[trigger]))
        return "WZ.faces[0]" if trigger == "faces" else "WZ"
    if trigger in ("openings", "openings_ext", "openings_headed"):
        w[0]["openings"] = [{"ref": "OZ", "kind": "window", "location": "exterior"}]
        return "OZ"
    lst = {"ceilings": ("ceilings", {"id": "CZ", "room": "CZ"}, "CZ"),
           "facades": ("facades", {"id": "Z"}, "facade Z"),
           "blocking": ("blocking_items", {"ref": "BZ"}, "BZ"),
           "mep": ("mep_penetrations", {"ref": "MZ"}, "MZ"),
           "tile_base": ("tile_base", {"room": "TZ"}, "tile_base TZ"),
           "wet": ("wet_fixtures", {"ref": "FZ"}, "FZ"),
           "sealant": ("sealant_items", {"ref": "SZ"}, "SZ"),
           "trim": ("trim_items", {"ref": "TRZ"}, "TRZ"),
           "rfis": ("rfis", {"id": "RZ"}, "RZ"),
           "excluidos": ("exclusions", {"ref": "XZ"}, "XZ"),
           "vendor_ends": ("vendor_ends", {"id": "VZ"}, "VZ"),
           "recessed": ("recessed_sweep", {"tag": "RCZ"}, "RCZ")}
    if trigger in lst:
        k, o, cid = lst[trigger]
        c[k] = list(c.get(k) or []) + [o]
        return cid
    if trigger == "details":
        c["details"]["9/Z9.99"] = {}
        return "9/Z9.99"
    raise KeyError(trigger)


def test_b(rid, spec):
    d = tempfile.mkdtemp(prefix="trb_")
    shutil.copytree(BASE, d, dirs_exist_ok=True)
    try:
        c = leer(d)
        caso = caso_para(spec["trigger"], c, d)
        guardar(d, c)
        evp = P(d, "4_canon", "evidencias_reglas.json")
        ev = json.load(open(evp))
        ev["evidencias"] = [e for e in ev["evidencias"] if not (e["regla"] == rid and e.get("caso") == caso)]
        jw(evp, ev)
        sin = [x for x in R.revisar_b(R.Ctx(d), rid, spec) if x[0] == caso]
        bueno = {"regla": rid, "caso": caso, "source": "1/Z5.01", "img": "img/evid.png", "archivo": P(d, "registro.json"),
                 "valor": "verified on the synthetic plan: face to face, ticks simple, callout + arrow + grid + content"}
        ev["evidencias"].append(bueno)
        jw(evp, ev)
        con = [x for x in R.revisar_b(R.Ctx(d), rid, spec) if x[0] == caso]
        contra = []
        if spec.get("prohibido") and spec.get("cita") != "archivo":
            ev["evidencias"][-1] = dict(bueno, valor=bueno["valor"] + " — estimado a ojo ~10 ft")
            jw(evp, ev)
            contra = [x for x in R.revisar_b(R.Ctx(d), rid, spec) if x[0] == caso]
            contra = contra or [None] if False else contra
            if not contra:
                return f"{rid}: valor 'a ojo' no contradice ({spec['nombre']})"
        if not sin:
            return f"{rid}: caso {caso} sin evidencia NO falla ({spec['nombre']})"
        if con:
            return f"{rid}: caso {caso} con evidencia sigue fallando: {con}"
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return None


def main():
    cat = RC.extraer()
    cls = CL.clasificar(cat)
    sin = [r["id"] for r in cat if r["id"] not in cls]
    if sin:
        FALLOS.append(f"{len(sin)} regla(s) sin clasificar: {sin[:10]}")
    o = R.compuerta(BASE)
    if not o["ok"]:
        FALLOS.append(f"fixture correcto NO pasa: {o['fallas'][:5]}")
    # (a) un caso malo y el bueno por chequeo
    res_ch = {}
    usados = sorted({ch for c in cls.values() for ch in c.get("chequeos") or []})
    for ch in usados:
        if ch not in MALOS:
            res_ch[ch] = f"{ch}: sin caso malo en test_reglas"
            continue
        try:
            mal, ok = correr(ch)
            res_ch[ch] = None if (mal > 0 and ok == 0) else f"{ch}: malo {mal} fallas / bueno {ok} fallas"
        except Exception as e:                       # noqa: BLE001
            res_ch[ch] = f"{ch}: {type(e).__name__}: {e}"
    n_ok = {"a": 0, "b": 0, "c": 0}
    for r in cat:
        c = cls.get(r["id"])
        if not c:
            continue
        err = None
        if c["tipo"] in ("a", "b"):
            errs = [res_ch[ch] for ch in c.get("chequeos") or [] if res_ch.get(ch)]
            err = "; ".join(errs) if errs else None
        if c["tipo"] == "b" and not err:
            err = test_b(r["id"], c["spec"])
        if c["tipo"] == "c":
            f = str(c.get("fusion") or "")
            err = None if f.strip() and r["id"] not in f else f"{r['id']}: fusión vacía o circular"
        if err:
            FALLOS.append(f"{r['id']}: {err}")
        else:
            n_ok[c["tipo"]] += 1
    # armar no escribe sin compuerta OK
    import plantilla_excel as PE
    import test_plantilla_v67 as TP
    d = tempfile.mkdtemp(prefix="tr_armar_")
    shutil.copytree(BASE, d, dirs_exist_ok=True)
    fo = json.load(open(P(d, "out", "familias_out.json")))
    x = P(d, "final.xlsx")
    try:
        PE.armar(PE.fusionar(TP.takeoff(), fo), x, d)
        s = R.leer_sello(x)
        if not s or s.get("canon") != R.huella(R.Ctx(d))["canon"]:
            FALLOS.append(f"armar: sello ausente o distinto: {s}")
    except Exception as e:                           # noqa: BLE001
        FALLOS.append(f"armar con compuerta OK falló: {type(e).__name__}: {e}")
    con_canon(lambda c: c["walls"][0].update(openings=[OP(ref="D1", kind="door", with_sill=True, sill_pieces=2)]))(d)
    os.remove(x)
    try:
        PE.armar(PE.fusionar(TP.takeoff(), fo), x, d)
        FALLOS.append("armar escribió el Excel con una regla violada")
    except R.ReglasNoOK:
        if os.path.exists(x):
            FALLOS.append("armar dejó un Excel aunque la compuerta falló")
    try:
        PE.armar(PE.fusionar(TP.takeoff(), fo), x, None)
        FALLOS.append("armar sin carpeta de trabajo escribió el Excel")
    except R.ReglasNoOK:
        pass
    shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(BASE, ignore_errors=True)
    for f in FALLOS:
        print("FALLO:", f)
    print(f"test_reglas: reglas {len(cat)} · tests OK a {n_ok['a']} · b {n_ok['b']} · c {n_ok['c']} · "
          f"chequeos {len([v for v in res_ch.values() if v is None])}/{len(res_ch)} · fallos {len(FALLOS)}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
