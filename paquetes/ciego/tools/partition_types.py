#!/usr/bin/env python3
"""partition_types.py v67 — hoja Partition Takeoff: qué es "un wall", qué LF entra en cada type y cómo se llaman
los types que no son partition. Regla determinista (CONVENCION_PARTITION_TYPES.md).

Por qué existe (#15A/#15B, 17-oct-2026): el mismo plano dio types con distinto número de walls y distinto LF
porque cada agente partía los walls a su manera (por zona de altura, por room, por stub, por door bulkhead) y
nombraba los types no-partition a su manera (EXT / PARAPET / BULK / CANOPY / RS / TRANS / VH / CSR / BLKHD).

REGLA
 1. Type de cada elemento del canon:
      element wall, tag interior          -> el tag del plano (A1, A1K, B2, C1, G, G1 ...)
      element wall / pier exterior (EXT*) -> "EXT-<stud>CFMF"   (6" -> EXT-6CFMF)
      element parapet                     -> "EXT-PARAPET"
      element door_bulkhead               -> "BULKHEAD-<tag del wall que interrumpe>" (G -> BULKHEAD-G)
      element column_wrap                 -> su tag; tags de canopy normalizados a "CANOPY-COL"
      element pier con tag interior       -> su tag (pilastra tageada C1 = C1)
      todo lo demás (storefront_cripples, vestibule_head, grille_head, roof_step, fascia_box, canopy_soffit,
      ceiling_transition, ceiling_bulkhead, soffit_side) -> NO es partition type: sección OTHER FRAMING.
 v70 — CRITERIO E28 (decisión del estimador): la agrupación la hace particion.particion con
    particion.MODO_DEFAULT ("run"): un RUN CONTINUO del mismo type con quiebres o esquinas = UN wall (los tramos se
    encadenan extremo con extremo; una T no encadena; nunca entre hojas). Se conservan el tipado PT1 (EXT-6CFMF,
    EXT-PARAPET, BULKHEAD-<familia>, CANOPY-COL…), PT4 (door_bulkheads colineales de un frente = UN wall aunque
    los separen stubs) y PT5 (OTHER FRAMING). v70c (EJES): exteriores (EXT*, PARAPET, CFMF) NO encadenan esquinas:
    un wall por fachada / eje (particion.es_exterior). La regla 2-3 de abajo es la del modo "tramo" (`modo="tramo"`).
 2. Un wall = el tramo RECTO de un mismo type entre esquinas o extremos. Dos segmentos del canon del mismo type,
    colineales (centro de banda a <= 3") y contiguos (hueco <= 6") son UN wall: no se parte por zona de
    altura, por room del otro lado, por T que llega, ni por abertura. LF del wall = suma de sus largos.
 3. Jog / stub: segmento de largo <= jog_max_ft (default JOG_MAX_FT, del orden del espesor de la partición) que no
    es el único de su type: NO es wall ni entra en el LF del type; se lista aparte (su metal y board siguen en el
    canon). Office bulkheads: todos los door_bulkhead colineales de un frente = UN wall (run continuo del box
    beam, decisión #22), LF = suma de los bulkheads.
 4. Segmento sin banda (sin coordenadas) = su propio wall + aviso.

v67 (integración): cada fila trae lo que escribe plantilla_excel.py en la hoja Partition Takeoff (un renglón por
wall): ids unidos con "+", lf, height_ft ponderada por largo, stud_size, oc_in, rows, board_sf (de board_out
si se pasa), location (con "incl. jog <id> <lf>" del jog vecino, R3), source y status. other_framing trae lo
mismo por elemento. canon.py la llama: out["partition_types"].

v68 (arbitraje #16, mismo plano dio types distintos en dos pruebas):
 R6 EXT-PARAPET: un wall = un STRAIGHT RUN geométrico: mismo `ori` y mismo eje (`axis`, a <= 3") y contiguo.
    Un step / offset entre ejes = otro wall. Sin `ori` + `axis` (o `band`) el run no se puede verificar: se une por
    `line` como antes, pero la fila sale PENDIENTE y con aviso (una etiqueta de lado N/E/S/W junta ejes distintos).
 R7 door_bulkhead: BULKHEAD-<familia del tag interrumpido> (letras iniciales: G1 -> G, A1K -> A). El bulkhead
    sale de su propio detalle (el mismo en todos los frentes), no del pier vecino; un wall por frente colineal.
 R8 chase (element "chase"): un wall por cara con room (cada cara es su propia fila de studs y su propio tag).
 R9 column_wrap / pier con tag interior: LF = suma de las caras con board (largo de cara > 0, altura > 0, room
    que no sea EXTERIOR); sin `length_ft` en las caras = length_ft + aviso. Column wrap con `fos_chain`: la fuente
    debe citar FOS (E8); si no, PENDIENTE (una cota total de la caja o de los bollards no es la cara del stud).
 R10 Jog / return <= jog_max_ft que toca a un wall del mismo type: su LF SE SUMA a ese wall (es el mismo wall que
    dobla la esquina) y no cuenta como wall aparte. Ya no se descarta del LF del type.
 R11 Aviso (no cambia el LF) si el extremo de un wall entra en la banda de un wall perpendicular de otro type más
    que la mitad de su espesor: el wall termina en la CARA del que cruza, no en su eje (corregir en el canon).

v72 (arbitraje #20, R72.3): un pier / box partido en dos registros (parte exterior sin tag + registro con tag) es
    UN wall en la cuenta: la parte sin tag (`part_of` o solape BOX >= 50 % con un registro con tag) va a
    other_framing como element "pier_part" (su metal y board siguen en el canon). Antes la parte exterior sumaba un
    wall EXT por pier.

Uso:  python3 partition_types.py takeoff_canon.json [salida.json] [--board board_out.json]
"""
import json
import re
import sys
from collections import OrderedDict, Counter

OTHER = ("storefront_cripples", "vestibule_head", "grille_head", "roof_step", "fascia_box", "canopy_soffit",
         "ceiling_transition", "ceiling_bulkhead", "soffit_side")
JOG_MAX_FT = 1.0
TOL_LINE_FT = 0.25   # misma línea: centros de banda a <= 3"
TOL_GAP_FT = 0.5    # contiguos: hueco <= 6"


def _norm(tag):
    t = re.sub(r"\s+", "-", str(tag or "").strip().upper())
    return "CANOPY-COL" if t.replace("-", "") in ("CANOPYCOL", "CANOPYCOLUMN") else t


def _stud_in(w):
    m = re.match(r"\s*(\d+(?:-\d+/\d+)?)", str(w.get("stud_size") or ""))
    return m.group(1) if m else "?"


def _familia(tag):
    m = re.match(r"[A-Z]+", tag or "")
    return m.group(0) if m else tag


def tipo(w, tags_wall):
    el = w.get("element", "wall")
    tag = _norm(w.get("tag"))
    ext = tag.startswith("EXT") or w.get("location") == "exterior"
    if el in OTHER:
        return None
    if el == "parapet":
        return "EXT-PARAPET"
    if el in ("wall", "pier") and ext:
        return f"EXT-{_stud_in(w)}CFMF"
    if el == "door_bulkhead":
        if tag in tags_wall:
            return f"BULKHEAD-{_familia(tag)}"
        par = w.get("bulkhead_of")
        if par:
            return f"BULKHEAD-{_familia(_norm(par))}"
        # el type del wall interrumpido: mismo stud y rows (G/G1 double row 1-5/8") -> el más común
        same = [t for (s, r, t) in tags_wall.get("_sig", []) if s == _stud_in(w) and r == int(w.get("rows", 1))]
        return f"BULKHEAD-{_familia(Counter(same).most_common(1)[0][0])}" if same else "BULKHEAD"
    return tag


def _parapet_geo(w, esc=18.0):
    """(ori, eje en ft) del straight run del parapet, o None si el canon no lo da (R6). `axis` va en ft."""
    if w.get("ori") in ("H", "V") and w.get("axis") is not None:
        return w["ori"], float(w["axis"])
    b = w.get("band")
    if isinstance(b, dict) and b.get("ori") in ("H", "V"):
        return b["ori"], (float(b["c0"]) + float(b["c1"])) / 2.0 / esc
    return None


INTERIOR_NO = ("EXTERIOR", "EXT", "OUTSIDE")


def _lf(w, avisos=None):
    """LF del wall en la hoja (R9): column_wrap / pier interior = caras con board; el resto = length_ft."""
    if w.get("element") in ("column_wrap", "pier") and not _norm(w.get("tag")).startswith(("EXT", "CANOPY")):
        caras = [f for f in w.get("faces") or [] if float(f.get("height_ft") or 0) > 0
                 and str(f.get("room") or "").upper() not in INTERIOR_NO]
        if caras and all(f.get("length_ft") is not None for f in caras):
            return sum(float(f["length_ft"]) for f in caras)
        if avisos is not None:
            avisos.append(f"{w['id']} ({w.get('tag')}): caras sin length_ft; LF = length_ft (perímetro) - R9")
    return float(w["length_ft"])


def _pendiente(w):
    """Motivo PENDIENTE de un elemento (R6, R9) o None."""
    if w.get("element") == "parapet" and _parapet_geo(w) is None:
        return "parapet sin ori + axis (o band): el straight run no se puede verificar (R6)"
    fc = w.get("fos_chain")
    caras_lf = [f for f in w.get("faces") or [] if f.get("length_ft") is not None and float(f.get("height_ft") or 0) > 0]
    if w.get("element") == "column_wrap" and isinstance(fc, dict) and not caras_lf \
            and "FOS" not in str(fc.get("source") or "").upper():
        return "fos_chain sin cota FOS impresa: la cara del stud no sale de una cota total (R9, E8)"
    return None


def _expandir(walls):
    """R8: un chase = un wall por cara con room (ids <id>/<room>), sin unirse entre sí."""
    out = []
    for w in walls:
        caras = [f for f in w.get("faces") or [] if f.get("room")]
        if w.get("element") == "chase" and len(caras) > 1:
            for f in caras:
                v = dict(w, id=f"{w['id']}/{f['room']}", faces=[f], _padre=w["id"], _partes=len(caras), _no_unir=True)
                out.append(v)
        else:
            out.append(w)
    return out


def _linea(w, esc=18.0):
    if w.get("element") == "parapet" and w.get("line") is not None and w.get("from_ft") is not None:
        # v67 (R5): un wall de EXT-PARAPET = un run de E3; v68 (R6): la línea es geométrica (ori + eje)
        g = _parapet_geo(w, esc)
        if g is not None:
            return "G", g, float(w["from_ft"]), float(w["to_ft"])
        return "L", str(w["line"]), float(w["from_ft"]), float(w["to_ft"])
    b = w.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    return b["ori"], (float(b["c0"]) + float(b["c1"])) / 2.0, float(b["lo"]), float(b["hi"])


def _board_por_wall(board_out):
    out = {}
    for c in (board_out or {}).get("caras") or []:
        out[c.get("wall")] = out.get(c.get("wall"), 0.0) + float(c.get("sf") or 0)
    return out


def _loc(w):
    if w.get("location") and w.get("location") not in ("exterior", "interior"):
        return str(w["location"])
    rooms = [str(f.get("room")) for f in w.get("faces") or [] if f.get("room")]
    return " / ".join(dict.fromkeys(rooms)) if rooms else str(w.get("note") or w["id"])


def _bsf(w, bsf):
    if w.get("_padre"):
        return bsf.get(w["_padre"], 0.0) / w["_partes"]
    return bsf.get(w["id"], 0.0)


def _layers(sel, L):
    """v71 (arbitraje #19, propuesta P1 de la prueba): Layers = Σ(layers_face × largo_face) / LF del wall, 2 decimales
    (la convención del estimador: un wall de 2 caras con 1 layer = 2.00; una cara partida por room NO suma otra
    layer). Face sin `length_ft`: largo completo del wall, pero las faces sin largo del mismo `side` cuentan una vez
    (la de más layers). Face con height_ft 0 no cuenta."""
    if not L:
        return 0
    tot = 0.0
    for w in sel:
        lw = _lf(w)
        sin_largo = {}
        for k, f in enumerate(w.get("faces") or []):
            if f.get("height_ft") is not None and float(f.get("height_ft") or 0) <= 0:
                continue
            n = int(f.get("layers", 1) or 0)
            if f.get("length_ft") is not None:
                tot += n * float(f["length_ft"])
            elif f.get("side") is not None:
                sin_largo[f["side"]] = max(sin_largo.get(f["side"], 0), n)
            else:
                sin_largo[("_", k)] = n
        tot += sum(sin_largo.values()) * lw
    return round(tot / L, 2)


def _fila(ws, ids, bsf):
    por = {w["id"]: w for w in ws}
    sel = [por[i] for i in ids]
    L = sum(_lf(w) for w in sel)
    h = sum(_lf(w) * float(w.get("height_ft") or 0) for w in sel) / L if L else 0.0
    w0 = sel[0]
    pend = [m for m in (_pendiente(w) for w in sel) if m]
    st = "PENDIENTE" if pend else (
        "CONFIRMADO" if all(w.get("length_printed_ft") is not None for w in sel) else "DERIVADO")
    return {"ids": ids, "wall": "+".join(ids), "lf": round(L, 3), "height_ft": round(h, 3),
            "stud_size": str(w0.get("stud_size") or "-"), "oc_in": w0.get("oc_in", 16), "rows": int(w0.get("rows", 1)),
            "layers": _layers(sel, L),
            "board_sf": round(sum(_bsf(w, bsf) for w in sel), 2),
            "location": " + ".join(dict.fromkeys(_loc(w) for w in sel)),
            "source": "; ".join(dict.fromkeys(str(w.get("detail") or w.get("source") or "-") for w in sel)),
            "status": st, "pendiente": list(dict.fromkeys(pend))}


def _solapes(walls, tipos, esc):
    """R11: extremo de un wall dentro de la banda de un wall perpendicular de otro type, pasado de su cara."""
    av = []
    bw = [(w, w["band"]) for w in walls if isinstance(w.get("band"), dict) and w["band"].get("ori") in ("H", "V")]
    for a, ba in bw:
        ca = (float(ba["c0"]) + float(ba["c1"])) / 2.0
        for b, bb in bw:
            if b is a or bb["ori"] == ba["ori"] or tipos.get(a["id"]) == tipos.get(b["id"]):
                continue
            if not (float(bb["lo"]) - 1 <= ca <= float(bb["hi"]) + 1):
                continue
            c0, c1 = float(bb["c0"]), float(bb["c1"])
            esp = c1 - c0
            for fin, dentro in ((float(ba["lo"]), lambda x: c0 <= x < c1), (float(ba["hi"]), lambda x: c0 < x <= c1)):
                if not dentro(fin):
                    continue
                pen = (c1 - fin) if fin == float(ba["lo"]) else (fin - c0)
                if pen > esp / 2.0 + 1e-6:
                    av.append(f"{a['id']} ({tipos.get(a['id'])}) entra {round(pen / esc, 3)} ft en la banda de {b['id']} "
                              f"({tipos.get(b['id'])}): el wall termina en la CARA del que cruza (R11, corregir canon)")
    return av


def _banda_sintetica(w, esc):
    """Banda en pt para particion.py: la del wall, o (parapet con ori + axis + from/to en ft) una armada desde R6."""
    b = w.get("band")
    if isinstance(b, dict) and b.get("ori") in ("H", "V"):
        return dict(b)
    ln = _linea(w, esc)
    if ln is not None and ln[0] == "G":
        (ori, eje_ft), lo, hi = ln[1], ln[2], ln[3]
        return {"ori": ori, "c0": eje_ft * esc, "c1": eje_ft * esc, "lo": lo * esc, "hi": hi * esc}
    return None


def _jogs_r10(filas, jog_max_ft):
    """R10 (modo tramo): segmento <= jog_max_ft que no es el único de su type suma su LF al wall más cercano."""
    jogs = [f for f in filas if f["lf"] <= jog_max_ft + 1e-9]
    if len(jogs) == len(filas):
        return filas
    cuenta = [f for f in filas if f not in jogs]
    for j in jogs:
        def dist(i):
            d = 1e9
            for fl in cuenta[i]["bands"]:
                for jl in j["bands"]:
                    d = min(d, min(abs(fl["lo"] - jl["eje"]), abs(fl["hi"] - jl["eje"]), abs(fl["eje"] - jl["eje"])) +
                            min(abs(jl["lo"] - fl["eje"]), abs(jl["hi"] - fl["eje"]), abs(fl["lo"] - jl["hi"]),
                                abs(jl["lo"] - fl["hi"])))
            return d
        i = min(range(len(cuenta)), key=dist)
        cuenta[i]["ids"] = cuenta[i]["ids"] + j["ids"]
        cuenta[i]["lf"] += j["lf"]
        cuenta[i]["jog"] = cuenta[i]["jog"] + [{"ids": j["ids"], "lf": round(j["lf"], 3)}]
    return cuenta


def _agrupar(t, ws, esc, modo, jog_max_ft, tol_line_ft, tol_gap_ft, avisos):
    """v70 (E28): los walls de UN type se agrupan con particion.particion (modo = particion.MODO_DEFAULT, "run": un run
    continuo con quiebres / esquinas = un wall; una T no encadena). Sobre eso: parapets sin geometría (solo `line`)
    se unen por línea contigua (R6 viejo, PENDIENTE); chase por cara no se une (R8); PT4: door_bulkheads colineales
    de un frente = UN wall aunque los separen stubs. -> (filas [{ids, lf, jog?}], jogs)."""
    import particion
    sint, por_id = [], {w["id"]: w for w in ws}
    lineas_l = []                                   # parapets con solo `line` (sin geometría)
    for w in ws:
        ln = _linea(w, esc)
        if ln is not None and ln[0] == "L" and not w.get("_no_unir"):
            for g in lineas_l:
                gl = g["linea"]
                if gl[1] == ln[1] and ln[2] <= gl[3] + 0.1 and ln[3] >= gl[2] - 0.1:
                    g["ids"].append(w["id"])
                    g["linea"] = ("L", gl[1], min(gl[2], ln[2]), max(gl[3], ln[3]))
                    break
            else:
                lineas_l.append({"ids": [w["id"]], "linea": ln})
            continue
        b = None if w.get("_no_unir") else _banda_sintetica(w, esc)
        if b is None and not w.get("_no_unir"):
            avisos.append(f"{w['id']} ({t}) sin band: wall propio, no se puede unir con colineales")
        c = {"id": w["id"], "tag": "T", "element": "wall", "length_ft": _lf(w), "sheet": "_",
             "tag_ids": list(w.get("tag_ids") or []), "openings": w.get("openings") or []}   # v71: modo eje
        if particion.es_exterior(t) or all(particion.es_exterior(t, x) for x in ws):   # v70c (EJES) / v71
            c["exterior"] = True
        if b is not None:
            c["band"] = b
        sint.append(c)
    # en "tramo" los jogs se resuelven abajo con R10 (al vecino más cercano), no con la regla de extremos de particion
    r = particion.particion({"constants": {"plan_scale_pt_per_ft": {"value": esc}}, "walls": sint}, modo,
                            jog_max_ft=-1.0 if modo == "tramo" else jog_max_ft, tol_line_ft=tol_line_ft,
                            tol_gap_ft=tol_gap_ft)
    filas = [{"ids": list(f["ids"]), "lf": f["lf"], "bands": f.get("bands") or [], "jog": []}
             for f in (r["types"].get("T") or {}).get("filas") or []]
    if modo == "tramo":
        filas = _jogs_r10(filas, jog_max_ft)
    filas += [{"ids": g["ids"], "lf": sum(_lf(por_id[i]) for i in g["ids"]), "bands": [], "jog": []} for g in lineas_l]
    # PT4: door_bulkheads colineales (mismo ori y eje) = UN wall por frente
    def es_bh(f):
        return all(por_id[i].get("element") == "door_bulkhead" for i in f["ids"])
    bh = [f for f in filas if es_bh(f) and f["bands"]]
    if len(bh) > 1:
        tol = tol_line_ft * esc

        def colineal(a, b):
            return any(x["ori"] == y["ori"] and abs(x["eje"] - y["eje"]) <= tol for x in a["bands"] for y in b["bands"])
        grupos_bh = particion._raices(len(bh), lambda i, j: colineal(bh[i], bh[j]))
        unidas = []
        for comp in grupos_bh:
            fs = [bh[i] for i in comp]
            unidas.append({"ids": [x for f in fs for x in f["ids"]], "lf": sum(f["lf"] for f in fs),
                           "bands": [x for f in fs for x in f["bands"]], "jog": [x for f in fs for x in f["jog"]]})
        filas = [f for f in filas if f not in bh] + unidas
    orden = {w["id"]: k for k, w in enumerate(ws)}
    filas.sort(key=lambda f: min(orden[i] for i in f["ids"]))
    jogs = [j for f in filas for j in f["jog"]]
    return filas, jogs


def partition_types(canon, board_out=None, jog_max_ft=JOG_MAX_FT, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT,
                    modo=None):
    import particion
    modo = modo or particion.MODO_DEFAULT
    walls = canon.get("walls") or []
    esc = float(((canon.get("constants") or {}).get("plan_scale_pt_per_ft") or {}).get("value") or 18.0)
    tags_wall = {_norm(w.get("tag")) for w in walls if w.get("element", "wall") == "wall"}
    tags_wall = {t: 1 for t in tags_wall}
    tags_wall["_sig"] = [(_stud_in(w), int(w.get("rows", 1)), _norm(w.get("tag"))) for w in walls
                         if w.get("element", "wall") == "wall" and not _norm(w.get("tag")).startswith("EXT")]
    grupos = OrderedDict()
    otros, avisos = [], []
    bsf = _board_por_wall(board_out)
    walls = _expandir(walls)
    import chequeos_v72                             # v72 (R72.3): un box = un wall (el registro con tag)
    partes = chequeos_v72.partes_de_box(walls)
    tipos = {}
    for w in walls:
        t = tipo(w, tags_wall)
        tipos[w["id"]] = t
        if w["id"] in partes:
            otros.append(dict(_fila([w], [w["id"]], bsf), id=w["id"], element="pier_part", tag=w.get("tag"),
                              part_of=partes[w["id"]]))
            avisos.append(f"{w['id']} ({t}) parte sin tag del box {partes[w['id']]}: fuera de la cuenta de walls "
                          f"(R72.3); su material sigue en el canon")
            continue
        if t is None:
            otros.append(dict(_fila([w], [w["id"]], bsf), id=w["id"], element=w.get("element"), tag=w.get("tag")))
            continue
        grupos.setdefault(t, []).append(w)
    out = OrderedDict()
    for t, ws in grupos.items():
        for w in ws:
            m = _pendiente(w)
            if m:
                avisos.append(f"{w['id']} ({t}) PENDIENTE: {m}")
        filas, jogs = _agrupar(t, ws, esc, modo, jog_max_ft, tol_line_ft, tol_gap_ft, avisos)
        ricas = []
        for f in filas:
            r = _fila(ws, f["ids"], bsf)
            for j in f.get("jog", []):
                r["location"] += f" (incl. jog {'+'.join(j['ids'])} {round(j['lf'], 3)} LF)"
            ricas.append(r)
        st = "PENDIENTE" if any(r["status"] == "PENDIENTE" for r in ricas) else "OK"
        out[t] = {"walls": len(filas), "lf": round(sum(r["lf"] for r in ricas), 2),
                  "filas": ricas, "status": st, "jogs": jogs}
    avisos += _solapes(walls, tipos, esc)
    return {"types": out, "other_framing": otros, "avisos": avisos, "modo": modo,
            "regla": {"modo": modo, "jog_max_ft": jog_max_ft, "tol_line_ft": tol_line_ft, "tol_gap_ft": tol_gap_ft}}


def main(argv):
    argv = list(argv)
    bo = None
    if "--board" in argv:
        i = argv.index("--board")
        bo = json.load(open(argv[i + 1]))
        del argv[i:i + 2]
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    r = partition_types(json.load(open(argv[1])), bo)
    if len(argv) == 3:
        open(argv[2], "w").write(json.dumps(r, indent=1, ensure_ascii=False))
    for t, d in r["types"].items():
        j = f"  (incl. {len(d['jogs'])} jog/return: {sum(x['lf'] for x in d['jogs']):.2f} LF)" if d["jogs"] else ""
        p = "  PENDIENTE" if d.get("status") == "PENDIENTE" else ""
        print(f"{t:14s} {d['walls']:3d} walls {d['lf']:9.2f} LF{j}{p}")
    print(f"OTHER FRAMING (no partition type): {len(r['other_framing'])} elementos")
    for a in r["avisos"]:
        print("AVISO", a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
