#!/usr/bin/env python3
"""particion.py — regla de partición de walls como PARÁMETRO (no fija). Toma los walls de un takeoff_canon.json y
los reporta como "walls" según el modo pedido.

Por qué existe: dos lecturas del mismo plano daban walls por type distintos porque cada una partía a su manera
(una contaba cada tramo, otra el run completo con sus quiebres). La regla vive en UNA constante y las dos lecturas
se parten con la misma.

v70 — DECISIÓN TOMADA (criterio del estimador): MODO_DEFAULT = "run". Un run continuo del mismo partition type con
quiebres o esquinas = un wall. "tramo" queda como opción (--modo tramo) para comparar o para un set que lo pida.
v70 — door_bulkhead se tipa BULKHEAD-<familia> (familia = letras iniciales del tag, convención de
partition_types.py R7: G1 -> G, G -> G, A1K -> A; sin tag usa `bulkhead_of`): el bulkhead nunca se une con sus
walls G / G1. La unión de "tramo" es por componentes conexas (union-find): el resultado no depende del orden de
los walls en el canon.
v70c — REGLA DE EJES (estimador: "nunca juntar dos ejes o fachadas en un número"): en modo "run" los walls
EXTERIORES (type que empieza con EXT, o contiene PARAPET o CFMF, o wall con location "exterior" / exterior true)
NO encadenan esquinas: se cortan en cada cambio de dirección, un wall por fachada / eje. Los interiores siguen igual.

v71 — MODO "eje" (DEFAULT). Arbitraje #19: con "run" faltaban walls en todos los types interiores. Comparando wall
por wall el canon contra la lista de walls del estimador, el estimador corta así (regla general, verificable):
  1. Un wall = una LÍNEA RECTA (eje) de un type: los segmentos colineales y contiguos del mismo type se unen (pieza
     partida por un wall que los cruza en T, por un beam o por un grid = mismo wall). La door / R.O. va DENTRO del
     wall (R70.3); un hueco colineal solo se cruza si un R.O. de esos walls cae en él (aviso). Un hueco vacío
     (alcove, pasillo) o con otro type (door_bulkhead, storefront) corta.
  2. Una ESQUINA (L), un JOG (eje desplazado) o una T entre dos líneas CON TAG = dos walls (cada tag marca su
     wall; dos tags sobre la misma línea = un wall).
  3. Un segmento SIN tag (return, jog, cierre) se suma al wall con tag que toca por el extremo (el más largo si
     toca dos). Un grupo conexo SIN ningún tag (p. ej. un alcove en U sin tag) = un wall: es el caso del criterio
     del estimador ("run continuo con quiebres = un wall").
     Sin tag_ids en todo el type: anclas = tramos > jog_max_ft; return / jog <= jog_max_ft se suma al que toca.
  4. Exteriores / parapets / CFMF: un wall por eje / fachada (regla 1), nunca se encadenan esquinas.
  5. Box cerrado (pier, column wrap; sin band H|V) = un wall.
  6. (v72, R72.7) Un grupo suelto SIN tag de largo total <= STUB_MAX_FT (6") no es wall: es el stub de un jamb o el
     remate de un frente cortado por otro type; su LF se suma al wall con tag más cercano del mismo type.
  Si un type no trae `tag_ids` en ningún segmento, se corta en cada esquina (regla 1) y se avisa.

v74 — ESTUDIO DE PARTICIÓN (arbitraje wall por wall contra la lista del estimador, dos canons). Reglas genéricas
nuevas del modo "eje" (sin números de ningún proyecto; cada una con su test sintético en test_particion_v74.py):
  R74.1 TYPE POR ESPESOR EN LA LÍNEA. Un segmento SIN tag (tipado por la nota general) cuyo espesor de band no es el
        de su type (|Δ| > ESPESOR_TOL_IN contra la mediana de los walls CON tag de ese type en la hoja) toma el type
        de los walls CON tag de la misma LÍNEA (colineales y encadenados sin hueco vacío, de cualquier type) que sí
        tienen su espesor. Es el return / remate de un office front: es del frente, no del type por defecto.
  R74.2 STUB APARTE. Un grupo suelto SIN tag de largo <= STUB_MAX_FT que NO toca por el extremo a un wall CON tag de
        su type no es wall de la lista ni suma LF al type: va a `stubs` (su metal y su board siguen en el canon).
        Reemplaza a R72.7 / R73.18 (sumarlo al wall con tag más cercano): la lista del estimador mide ese wall de
        cara a cara sin el stub. Un stub que SÍ toca por el extremo a un wall con tag es su return (regla 3).
  R74.3 NICHO / ALCOVE. Un grupo SIN tag (más de un tramo) cuyos dos extremos libres caen sobre dos tramos
        COLINEALES de una misma línea de OTRO type, cerrando el hueco entre ellos, es un nicho de esa línea (alcove
        de drinking fountain, recess de equipo): no es wall de la lista; va a `anexos` con su LF (material en el
        canon). Un grupo sin tag que no abre en otra línea sigue siendo UN wall (regla 3).
  R74.4 FRENTE DE BULKHEADS. door_bulkheads colineales (type BULKHEAD-*) cuyos huecos están cubiertos por tramos
        colineales de otros types (los returns del frente) o son cortos (<= GAP_ABERTURA_MAX_FT: stub / jamb) = UN
        wall por frente (PT4 de partition_types, ahora también aquí: comparar.py y partition_types dan lo mismo).
        Un hueco largo y vacío separa dos frentes.
  R74.5 DUPLICADO DE BOX. Un box / pier SIN tag con la misma huella (solape >= 50 %) que un registro CON tag es el
        mismo elemento leído dos veces (R72.3): no cuenta; va a `duplicados`. El tag del plano manda.
  R74.6 NOMBRE EXTERIOR. wall / pier exterior con stud conocido -> EXT-<stud>CFMF; parapet -> EXT-PARAPET; canopy
        column -> CANOPY-COL (los nombres de partition_types.py R1): dos lecturas que escriben "EXT" y "EXT-6CFMF"
        ya no salen como dos types.

MODOS
  "eje"    (default v71) reglas 1-5 de arriba.
  "tramo"  un wall por cada tramo RECTO de un type: segmentos colineales (ejes a <= tol_line_ft) y contiguos
           (hueco <= tol_gap_ft) se unen; un quiebre / esquina empieza otro wall. Jog / return <= jog_max_ft que
           toca un wall del mismo type se suma a ese wall (no es wall propio).
  "run"    un wall por RUN CONTINUO del mismo type aunque tenga quiebres: los tramos rectos se encadenan cuando el
           extremo de uno toca el extremo del otro (esquina L, jog, step). Una T (extremo contra el COSTADO del
           otro) NO encadena: el que llega termina en la cara del que sigue.
           Excepción (v70c): exteriores / parapets / CFMF se cortan en cada cambio de dirección (un wall por eje).
Nunca se une entre hojas distintas ni entre types distintos (BULKHEAD-G es otro type que G). Segmento sin `band` = wall propio + aviso.

Geometría del canon (la misma de partition_types.py): band = {ori: H|V, c0, c1 (caras, perpendicular), lo, hi
(extensión)} en pt de la hoja; escala constants.plan_scale_pt_per_ft.value (default 18). Hoja del wall: `sheet`
(o `plan_sheet`); si falta, el primer sheet number que aparezca en `source`.

Uso:  python3 particion.py takeoff_canon.json [--modo eje|run|tramo] [salida.json]
"""
import json
import math
import re
import sys
from collections import OrderedDict

MODO_DEFAULT = "eje"       # v71: arbitraje #19 (línea recta por tag; sin tag se suma; grupo sin tag = run)
MODOS = ("tramo", "run", "eje")
GAP_ABERTURA_MAX_FT = 7.0  # v71: hueco colineal máximo que se cruza, y solo con un R.O. del wall dentro (R70.3)
JOG_MAX_FT = 1.0
STUB_MAX_FT = 0.5         # v72 (R72.7): grupo suelto sin tag <= 6" = stub, se suma al wall con tag que toca
TOL_LINE_FT = 0.25        # colineales: ejes a <= 3"
ESPESOR_TOL_IN = 0.5      # v74 (R74.1): mismo espesor de band = a <= 1/2" (la mitad de la diferencia entre dos types de stud vecinos)
TOL_GAP_FT = 0.5          # contiguos / extremos que se tocan: hueco <= 6" (más el espesor del wall)
ESCALA_DEFAULT = 18.0
NO_PARTITION = ("storefront_cripples", "vestibule_head", "grille_head", "roof_step", "fascia_box", "canopy_soffit",
                "ceiling_transition", "ceiling_bulkhead", "soffit_side", "soffit_drop", "soffit_bottom", "joist",
                "ceiling_perimeter")
SHEET_IN_SRC = re.compile(r"(?:^|[\s/;(,])([A-Z]{1,3}-?\d{1,3}(?:\.\d{1,3}[A-Z]?))\b")


def norm_type(tag):
    return re.sub(r"\s+", "-", str(tag or "").strip().upper())


def familia(tag):
    """Familia del tag = letras iniciales (misma convención que partition_types._familia, R7): G1 -> G, A1K -> A."""
    m = re.match(r"[A-Z]+", tag or "")
    return m.group(0) if m else tag


def _stud(w):
    m = re.match(r"\s*(\d+(?:-\d+/\d+)?)", str(w.get("stud_size") or ""))
    return m.group(1) if m else None


def tipo(w):
    """Type de partición del segmento. door_bulkhead -> BULKHEAD-<familia del tag (o de bulkhead_of)>.
    v74 (R74.6): nombres de partition_types R1 (EXT-<stud>CFMF, EXT-PARAPET, CANOPY-COL)."""
    t = norm_type(w.get("tag"))
    el = w.get("element")
    if el == "door_bulkhead":
        base = t or norm_type(w.get("bulkhead_of"))
        return f"BULKHEAD-{familia(base)}" if base else "BULKHEAD"
    if el == "parapet":
        return "EXT-PARAPET"
    if t.replace("-", "") in ("CANOPYCOL", "CANOPYCOLUMN"):
        return "CANOPY-COL"
    if el in ("wall", "pier") and (t.startswith("EXT") or str(w.get("location") or "").lower() == "exterior") \
            and "PARAPET" not in t and _stud(w):
        return f"EXT-{_stud(w)}CFMF"
    return t


def es_exterior(t, w=None):
    """v70c: ¿type / wall exterior? (EXT*, *PARAPET*, *CFMF*, o location "exterior" / exterior true en el canon)."""
    t = norm_type(t)
    if t.startswith("EXT") or "PARAPET" in t or "CFMF" in t:
        return True
    return bool(w) and (str(w.get("location") or "").lower() == "exterior" or w.get("exterior") is True)


def hoja(w):
    for k in ("sheet", "plan_sheet"):
        if w.get(k):
            return str(w[k]), w.get("page")
    m = SHEET_IN_SRC.search(" " + str(w.get("source") or ""))
    return (m.group(1) if m else "?"), w.get("page")


def escala(canon):
    v = ((canon.get("constants") or {}).get("plan_scale_pt_per_ft") or {})
    return float(v.get("value") or ESCALA_DEFAULT) if isinstance(v, dict) else float(v or ESCALA_DEFAULT)


def geo(w):
    """(ori, eje, lo, hi, espesor) en pt o None."""
    b = w.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    c0, c1 = float(b["c0"]), float(b["c1"])
    lo, hi = sorted((float(b["lo"]), float(b["hi"])))
    return b["ori"], (c0 + c1) / 2.0, lo, hi, abs(c1 - c0)


def extremos(g):
    ori, eje, lo, hi, _ = g
    return [(lo, eje), (hi, eje)] if ori == "H" else [(eje, lo), (eje, hi)]


def _raices(n, une):
    """Union-find: componentes conexas de n nodos con la relación une(i, j). -> lista de listas de índices (orden
    estable: por el menor índice de cada componente)."""
    padre = list(range(n))

    def raiz(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            if raiz(i) != raiz(j) and une(i, j):
                padre[raiz(i)] = raiz(j)
    comp = OrderedDict()
    for i in range(n):
        comp.setdefault(raiz(i), []).append(i)
    return list(comp.values())


def _tramos(ws, esc, tol_line_ft, tol_gap_ft):
    """Une colineales y contiguos del mismo type y hoja en tramos rectos. v70: componentes conexas (la unión voraz
    contra el primer tramo que tocaba NO era transitiva y dependía del orden de los walls)."""
    gs = [geo(w) for w in ws]

    def une(i, j):
        a, b = gs[i], gs[j]
        if a is None or b is None or a[0] != b[0] or abs(a[1] - b[1]) > tol_line_ft * esc:
            return False
        return a[2] <= b[3] + tol_gap_ft * esc and a[3] >= b[2] - tol_gap_ft * esc
    tramos = []
    for comp in _raices(len(ws), une):
        comp = sorted(comp, key=lambda i: (gs[i][2] if gs[i] else 0.0, str(ws[i]["id"])))
        g = [gs[i] for i in comp if gs[i] is not None]
        tg = None
        if g:
            ejes = sorted(x[1] for x in g)
            tg = (g[0][0], ejes[len(ejes) // 2], min(x[2] for x in g), max(x[3] for x in g), max(x[4] for x in g))
        tramos.append({"ids": [ws[i]["id"] for i in comp], "lf": sum(float(ws[i]["length_ft"]) for i in comp),
                       "geo": tg})
    return tramos


def _tags(w):
    return [str(x) for x in (w.get("tag_ids") or []) if x]


def _tramos_eje(ws, esc, tol_line_ft, tol_gap_ft, avisos_gap):
    """Regla 1 (v71): colineales del mismo type unidos si se tocan (hueco <= tol_gap). Un hueco mayor solo se cruza
    si un R.O. de uno de los dos walls (`openings[].xy_pt`) cae dentro (la door es parte del wall, R70.3). Un hueco
    vacío (alcove, pasillo, otro type, bulkhead, storefront) corta."""
    gs = [geo(w) for w in ws]

    def une(i, j):
        a, b = gs[i], gs[j]
        if a is None or b is None or a[0] != b[0] or abs(a[1] - b[1]) > tol_line_ft * esc:
            return False
        if a[2] <= b[3] + tol_gap_ft * esc and a[3] >= b[2] - tol_gap_ft * esc:
            return True
        g0, g1 = (a[3], b[2]) if a[3] < b[2] else (b[3], a[2])
        if g1 - g0 > GAP_ABERTURA_MAX_FT * esc:
            return False
        for k in (i, j):                          # R70.3: un R.O. de estos walls cae en el hueco -> mismo wall
            for o in ws[k].get("openings") or []:
                xy = o.get("xy_pt") if isinstance(o, dict) else None
                if isinstance(xy, (list, tuple)) and len(xy) == 2:
                    pos = float(xy[0] if a[0] == "H" else xy[1])
                    if g0 - 1.0 <= pos <= g1 + 1.0:
                        avisos_gap.append(f"{ws[i]['id']} / {ws[j]['id']}: hueco con el R.O. {o.get('ref')} dentro "
                                          f"-> mismo wall (R70.3: el R.O. va DENTRO del wall en el canon)")
                        return True
        return False
    tramos = []
    for comp in _raices(len(ws), une):
        comp = sorted(comp, key=lambda i: (gs[i][2] if gs[i] else 0.0, str(ws[i]["id"])))
        g = [gs[i] for i in comp if gs[i] is not None]
        tg = None
        if g:
            ejes = sorted(x[1] for x in g)
            tg = (g[0][0], ejes[len(ejes) // 2], min(x[2] for x in g), max(x[3] for x in g), max(x[4] for x in g))
        tramos.append({"ids": [ws[i]["id"] for i in comp], "lf": sum(float(ws[i]["length_ft"]) for i in comp),
                       "geo": tg, "tags": sorted({t for i in comp for t in _tags(ws[i])})})
    return tramos


def _walls_eje(tramos, esc, tol_gap_ft, exterior, t, sh, avisos, jog_max_ft=JOG_MAX_FT, ctx=None, aparte=None,
               tipo_ctx=None, sheet_ctx=None):
    """Reglas 2-5 (v71) sobre los tramos rectos de un type / hoja. v74: R74.2 (stub aparte) y R74.3 (nicho); lo que
    no es wall de la lista va a `aparte` = {"stubs": [...], "anexos": [...]} con su LF."""
    aparte = {"stubs": [], "anexos": []} if aparte is None else aparte

    def fila(parts, sin_tag=None):
        d = {"ids": [x for p in parts for x in p["ids"]], "lf": sum(p["lf"] for p in parts), "tramos": len(parts),
             "geos": [p["geo"] for p in parts], "tags": sorted({x for p in parts for x in p["tags"]})}
        if sin_tag:
            d["sin_tag_sumado"] = sin_tag
        return d
    if exterior:
        return [fila([p]) for p in tramos]
    if any(p["tags"] for p in tramos):
        con = [k for k, p in enumerate(tramos) if p["tags"]]
    else:                                         # sin tag_ids: ancla = tramo > jog_max (return / jog se suma)
        con = [k for k, p in enumerate(tramos) if p["lf"] > jog_max_ft + 1e-9] or list(range(len(tramos)))
        if len(tramos) > 1:
            avisos.append(f"{t} ({sh}): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), "
                          f"returns / jogs <= {jog_max_ft} ft se suman al tramo que tocan")
    sin = [k for k in range(len(tramos)) if k not in con]
    dest = {k: [k] for k in con}
    sueltos = []
    for comp in _raices(len(sin), lambda i, j: _tocan(tramos[sin[i]], tramos[sin[j]], esc, tol_gap_ft)):
        ks = [sin[i] for i in comp]
        toca = [c for c in con if any(_tocan(tramos[k], tramos[c], esc, tol_gap_ft) for k in ks)]
        if toca:
            c = max(toca, key=lambda c: (tramos[c]["lf"], -c))
            dest[c] += ks
        else:
            sueltos.append(ks)
    # v74 (R74.2, reemplaza R72.7 / R73.18): un grupo suelto SIN tag <= STUB_MAX_FT que no toca por el extremo a un
    # wall con tag de su type (si lo tocara, ya es su return arriba) no es wall de la lista ni suma LF al type: la lista
    # del estimador mide cada wall de cara a cara sin el stub. Va a `stubs`; su metal y board siguen en el canon.
    # v74 (R74.3): un grupo suelto SIN tag que cierra el hueco entre dos tramos colineales de una línea de OTRO type es
    # un nicho de esa línea (alcove): va a `anexos`.
    quedan = []
    for ks in sueltos:
        ids = [x for k in ks for x in tramos[k]["ids"]]
        lf = round(sum(tramos[k]["lf"] for k in ks), 3)
        if con and lf <= STUB_MAX_FT + 1e-9:
            aparte["stubs"].append({"ids": ids, "lf": lf, "regla": "R74.2"})
            avisos.append(f"{'+'.join(ids)} ({t}, {sh}) stub sin tag <= {STUB_MAX_FT} ft que no toca un wall con tag de "
                          f"su type: no es wall de la lista ni suma LF (R74.2); su material sigue en el canon")
            continue
        ni = nicho([tramos[k]["geo"] for k in ks], tipo_ctx or t, sheet_ctx or sh, ctx, esc,
                   tol_gap_ft=tol_gap_ft) if ctx else None
        if ni:
            aparte["anexos"].append({"ids": ids, "lf": lf, "regla": "R74.3", "abre_en": [ni[0], ni[1]],
                                     "type_linea": ni[2]})
            avisos.append(f"{'+'.join(ids)} ({t}, {sh}) grupo sin tag que cierra el hueco entre {ni[0]} y {ni[1]} "
                          f"({ni[2]}): nicho / alcove de esa línea, no es wall de la lista (R74.3)")
            continue
        quedan.append(ks)
    sueltos = quedan
    out = []
    for c in con:
        extra = [x for k in dest[c][1:] for x in tramos[k]["ids"]]
        out.append(fila([tramos[k] for k in dest[c]], extra or None))
    for ks in sueltos:
        out.append(fila([tramos[k] for k in ks]))
    return out

# ------------------------------------------------------------------ v74: contexto entre types (R74.1 / R74.3 / R74.4)
def _espesor_in(g, esc):
    return g[4] / esc * 12.0


def _colineal(a, b, esc, tol_line_ft):
    return a is not None and b is not None and a[0] == b[0] and abs(a[1] - b[1]) <= tol_line_ft * esc


def _contiguo(a, b, esc, tol_gap_ft):
    return a[2] <= b[3] + tol_gap_ft * esc and a[3] >= b[2] - tol_gap_ft * esc


def _lineas(ctx, esc, tol_line_ft, tol_gap_ft):
    """Líneas físicas de la hoja: segmentos con band H|V de CUALQUIER type, colineales y encadenados sin hueco
    vacío (hueco <= tol_gap). -> {id: n de línea}."""
    idx = [k for k, c in enumerate(ctx) if c["geo"] is not None]
    comp = _raices(len(idx), lambda i, j: ctx[idx[i]]["sheet"] == ctx[idx[j]]["sheet"]
                   and _colineal(ctx[idx[i]]["geo"], ctx[idx[j]]["geo"], esc, tol_line_ft)
                   and _contiguo(ctx[idx[i]]["geo"], ctx[idx[j]]["geo"], esc, tol_gap_ft))
    return {ctx[idx[i]]["id"]: n for n, cs in enumerate(comp) for i in cs}


def retipar(ctx, esc, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT, tol_in=ESPESOR_TOL_IN):
    """R74.1: {id: (type nuevo, motivo)} para segmentos SIN tag cuyo espesor es el de los walls con tag de su línea y
    no el de su type. Solo element wall con band H|V; el type por defecto necesita walls con tag en la hoja para
    tener un espesor de referencia (si no, no se toca)."""
    linea = _lineas(ctx, esc, tol_line_ft, tol_gap_ft)
    ref = {}
    for c in ctx:
        if c["tags"] and c["geo"] is not None and c["element"] == "wall":
            ref.setdefault((c["type"], c["sheet"]), []).append(_espesor_in(c["geo"], esc))
    med = {k: sorted(v)[len(v) // 2] for k, v in ref.items()}
    out = {}
    for c in ctx:
        if c["tags"] or c["geo"] is None or c["element"] != "wall" or c["id"] not in linea:
            continue
        e = _espesor_in(c["geo"], esc)
        propio = med.get((c["type"], c["sheet"]))
        if propio is None or abs(e - propio) <= tol_in:
            continue
        cand = sorted({o["type"] for o in ctx if o is not c and o["tags"] and o["element"] == "wall"
                       and o["geo"] is not None and linea.get(o["id"]) == linea[c["id"]]
                       and abs(_espesor_in(o["geo"], esc) - e) <= tol_in and o["type"] != c["type"]})
        if len(cand) == 1:
            out[c["id"]] = (cand[0], f"{c['id']} sin tag mide {round(e, 2)} in y su type {c['type']} {round(propio, 2)} "
                                     f"in: toma el type {cand[0]} de los walls con tag de su línea (R74.1)")
    return out


def _extremos_libres(geos, esc, tol_gap_ft):
    """Extremos de un grupo de tramos que no tocan a otro tramo del mismo grupo."""
    libres = []
    for k, g in enumerate(geos):
        for p in extremos(g):
            lim = g[4] + tol_gap_ft * esc
            if not any(o is not g and (math.dist(p, q) <= lim or _sobre(p, o, lim)) for o in geos for q in extremos(o)):
                libres.append(p)
    return libres


def _sobre(p, g, lim):
    """¿El punto p cae sobre la band g (dentro de su largo y a <= lim de su eje)?"""
    ori, eje, lo, hi, esp = g
    a, b = (p[0], p[1]) if ori == "H" else (p[1], p[0])
    return lo - lim <= a <= hi + lim and abs(b - eje) <= esp / 2.0 + lim


def nicho(geos, tipo_grupo, sheet, ctx, esc, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT):
    """R74.3: si los dos extremos libres del grupo caen sobre dos tramos colineales DISTINTOS de una misma línea de
    otro type (el grupo cierra el hueco entre ellos) -> (id_a, id_b, type de la línea); si no, None."""
    geos = [g for g in geos if g is not None]
    if len(geos) < 2:
        return None
    libres = _extremos_libres(geos, esc, tol_gap_ft)
    if len(libres) != 2:
        return None
    lim = tol_gap_ft * esc

    def toca(p):
        return [o for o in ctx if o["geo"] is not None and o["sheet"] == sheet and o["type"] != tipo_grupo
                and _sobre(p, o["geo"], lim)]
    for a in toca(libres[0]):
        for b in toca(libres[1]):
            if a is not b and a["type"] == b["type"] and _colineal(a["geo"], b["geo"], esc, tol_line_ft):
                return a["id"], b["id"], a["type"]
    return None


def _frente_bulkheads(walls, ctx, t, sh, esc, tol_line_ft, tol_gap_ft):
    """R74.4: walls BULKHEAD-* colineales cuyo hueco lo cubren tramos colineales de otros types (returns del frente)
    = UN wall por frente."""
    if len(walls) < 2:
        return walls
    otros = [c["geo"] for c in ctx if c["geo"] is not None and c["sheet"] == sh and c["type"] != t]

    def cubierto(a, b):
        """¿El hueco entre a y b (colineales) está cubierto por tramos colineales de otros types?"""
        g0, g1 = (a[3], b[2]) if a[3] < b[2] else (b[3], a[2])
        if g1 <= g0 + GAP_ABERTURA_MAX_FT * esc:    # hueco corto (stub / jamb entre bulkheads): mismo frente (PT4)
            return True
        tramos = sorted((o[2], o[3]) for o in otros if _colineal(o, a, esc, tol_line_ft) and o[3] >= g0 - 1
                        and o[2] <= g1 + 1)
        x = g0
        for lo, hi in tramos:
            if lo > x + tol_gap_ft * esc:
                return False
            x = max(x, hi)
        return x >= g1 - tol_gap_ft * esc

    def une(i, j):
        for a in walls[i]["geos"]:
            for b in walls[j]["geos"]:
                if a is not None and b is not None and _colineal(a, b, esc, tol_line_ft) and cubierto(a, b):
                    return True
        return False
    out = []
    for comp in _raices(len(walls), une):
        ps = [walls[i] for i in comp]
        d = {"ids": [x for p in ps for x in p["ids"]], "lf": sum(p["lf"] for p in ps),
             "tramos": sum(p.get("tramos", 1) for p in ps), "geos": [g for p in ps for g in p["geos"]],
             "tags": sorted({x for p in ps for x in p.get("tags") or []})}
        if len(ps) > 1:
            d["frente"] = "R74.4"
        out.append(d)
    return out


def _tocan(a, b, esc, tol_gap_ft):
    """¿Algún extremo de a toca algún extremo de b? (esquina L / jog / step; no T)."""
    if a["geo"] is None or b["geo"] is None:
        return False
    lim = max(a["geo"][4], b["geo"][4]) + tol_gap_ft * esc
    return any(math.dist(p, q) <= lim for p in extremos(a["geo"]) for q in extremos(b["geo"]))


def contexto(walls, tipos=None):
    """v74: todos los segmentos de partición (con su type) para las reglas entre types (R74.1 / R74.3 / R74.4).
    `tipos` = {id: type} si el llamador ya los tiene (partition_types); si no, tipo(w)."""
    ctx = []
    for w in walls:
        if w.get("element") in NO_PARTITION:
            continue
        ctx.append({"id": w["id"], "type": (tipos or {}).get(w["id"]) or tipo(w), "sheet": hoja(w)[0],
                    "element": w.get("element") or "wall", "tags": _tags(w), "geo": geo(w)})
    return ctx


def duplicados(walls):
    """R74.5 (= R72.3): {id sin tag: id con tag} de boxes / piers con la misma huella (solape >= 50 %)."""
    try:
        import chequeos_v72
    except ImportError:
        return {}
    return chequeos_v72.partes_de_box([w for w in walls if w.get("element") not in NO_PARTITION])


def particion(canon, modo=MODO_DEFAULT, jog_max_ft=JOG_MAX_FT, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT,
              ctx=None, tipo_ctx=None):
    """v80e: con constants.plan_scale_by_sheet (hojas de escala distinta) se parte cada hoja con SU escala y se
    unen los resultados (nunca se une entre hojas, así que es exacto)."""
    import criterios
    if ctx is None and criterios.multi_escala(canon):
        res = None
        for sh, sub in criterios.subcanons_por_hoja(canon):
            r = _particion_hoja(sub, modo, jog_max_ft, tol_line_ft, tol_gap_ft)
            if res is None:
                res = r
                res["escalas_por_hoja"] = {str(sh): r["escala_pt_por_ft"]}
                res["escala_pt_por_ft"] = criterios.escala_global(canon)
                continue
            res["escalas_por_hoja"][str(sh)] = r["escala_pt_por_ft"]
            for t, d in r["types"].items():
                if t not in res["types"]:
                    res["types"][t] = d
                    continue
                e = res["types"][t]
                e["filas"] += d["filas"]
                e["walls"] += d["walls"]
                e["lf"] = round(e["lf"] + d["lf"], 3)
                for k in ("stubs", "anexos"):
                    if d.get(k):
                        e[k] = (e.get(k) or []) + d[k]
            res["other_framing"] += r["other_framing"]
            res["avisos"] += r["avisos"]
            res["retipados"].update(r["retipados"])
            res["duplicados"].update(r["duplicados"])
        return res
    return _particion_hoja(canon, modo, jog_max_ft, tol_line_ft, tol_gap_ft, ctx, tipo_ctx)


def _particion_hoja(canon, modo=MODO_DEFAULT, jog_max_ft=JOG_MAX_FT, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT,
                    ctx=None, tipo_ctx=None):
    """`ctx` / `tipo_ctx` (v74): contexto externo de todos los types (partition_types agrupa un type a la vez con
    walls sintéticos; `tipo_ctx` es el type real de ese grupo). Sin ctx, el modo "eje" lo arma del canon."""
    if modo not in MODOS:
        raise ValueError(f"modo '{modo}' no existe: {MODOS}")
    esc = escala(canon)
    grupos = OrderedDict()
    otros, avisos = [], []
    walls_c = canon.get("walls") or []
    retip, dups = {}, {}
    externo = ctx is not None
    ctx = list(ctx or [])
    if modo == "eje" and not externo:             # v74: reglas entre types (R74.1 / R74.3 / R74.4 / R74.5)
        dups = duplicados(walls_c)
        ctx = contexto([w for w in walls_c if w["id"] not in dups])
        retip = retipar(ctx, esc, tol_line_ft, tol_gap_ft)
        for c in ctx:
            if c["id"] in retip:
                c["type"] = retip[c["id"]][0]
        avisos += [m for _, m in retip.values()]
        avisos += [f"{k} sin tag con la huella del box {v} (con tag): el mismo elemento leído dos veces, no cuenta "
                   f"(R74.5 / R72.3)" for k, v in dups.items()]
    aparte = OrderedDict()
    for w in walls_c:
        if w.get("element") in NO_PARTITION:
            otros.append(w["id"])
            continue
        if w["id"] in dups:
            continue
        t = retip[w["id"]][0] if w["id"] in retip else tipo(w)
        sh, pg = hoja(w)
        if geo(w) is None:
            ori = (w.get("band") or {}).get("ori") if isinstance(w.get("band"), dict) else None
            avisos.append(f"{w['id']} ({t}, {sh}) sin band" + (f" H|V (ori {ori})" if ori else "")
                          + ": wall propio, no se puede unir")
        grupos.setdefault((t, sh, pg), []).append(w)
    out = OrderedDict()
    for (t, sh, pg), ws in grupos.items():
        if modo == "eje":
            ext = es_exterior(t) or all(es_exterior(t, w) for w in ws)   # un pier exterior no vuelve exterior al type
            tramos = _tramos_eje(ws, esc, tol_line_ft, tol_gap_ft, avisos)
            ap = aparte.setdefault(t, {"stubs": [], "anexos": []})
            tr, shr = (tipo_ctx or t, "_") if externo else (t, sh)       # type / hoja con que se busca en ctx
            walls = _walls_eje(tramos, esc, tol_gap_ft, ext, t, sh, avisos, jog_max_ft,
                               ctx=[dict(c, sheet=shr if externo else c["sheet"]) for c in ctx] if ctx else None,
                               aparte=ap, tipo_ctx=tr, sheet_ctx=shr)
            if tr.startswith("BULKHEAD"):
                walls = _frente_bulkheads(walls, ctx, tr, shr, esc, tol_line_ft, tol_gap_ft)
        else:
            tramos = _tramos(ws, esc, tol_line_ft, tol_gap_ft)
        if modo == "eje":
            pass                                  # walls ya armados arriba (reglas 1-5)
        elif modo == "run" and any(es_exterior(t, w) for w in ws):
            # v70c (EJES): exterior = un wall por tramo recto (fachada / eje); el cambio de dirección corta
            walls = [{"ids": list(x["ids"]), "lf": x["lf"], "tramos": 1, "geos": [x["geo"]]} for x in tramos]
        elif modo == "run":
            # componentes conexas por extremos que se tocan
            walls = []
            for comp in _raices(len(tramos), lambda i, j: _tocan(tramos[i], tramos[j], esc, tol_gap_ft)):
                parts = [tramos[i] for i in comp]
                walls.append({"ids": [x for p in parts for x in p["ids"]], "lf": sum(p["lf"] for p in parts),
                              "tramos": len(parts), "geos": [p["geo"] for p in parts]})
        else:                                     # "tramo"
            jogs = [x for x in tramos if x["lf"] <= jog_max_ft + 1e-9]
            if len(jogs) == len(tramos):
                jogs = []
            walls = [{"ids": list(x["ids"]), "lf": x["lf"], "tramos": 1, "geos": [x["geo"]]}
                     for x in tramos if x not in jogs]
            for j in jogs:                        # el jog suma al wall del mismo type que toca
                toca = [k for k, x in enumerate(tramos) if x not in jogs and _tocan(j, x, esc, tol_gap_ft)]
                if toca:
                    dst = walls[[x for x in tramos if x not in jogs].index(tramos[toca[0]])]
                    dst["ids"] += j["ids"]
                    dst["lf"] += j["lf"]
                    dst.setdefault("jogs", []).append({"ids": j["ids"], "lf": round(j["lf"], 3)})
                else:
                    walls.append({"ids": list(j["ids"]), "lf": j["lf"], "tramos": 1, "geos": [j["geo"]]})
                    avisos.append(f"{'+'.join(j['ids'])} ({t}, {sh}) jog <= {jog_max_ft} ft que no toca a otro "
                                  f"wall del mismo type: queda como wall propio")
        for w in walls:
            w["wall"] = "+".join(w["ids"])
            w["lf"] = round(w["lf"], 3)
            w["sheet"], w["page"] = sh, pg
            gs = [g for g in w.pop("geos") if g is not None]
            if gs:
                xs, ys = [], []
                for g in gs:
                    for p in extremos(g):
                        xs.append(p[0])
                        ys.append(p[1])
                e = max(g[4] for g in gs) / 2.0
                w["bbox_pt"] = [round(min(xs) - e, 2), round(min(ys) - e, 2), round(max(xs) + e, 2),
                                round(max(ys) + e, 2)]
                w["bands"] = [{"ori": g[0], "eje": round(g[1], 2), "lo": round(g[2], 2), "hi": round(g[3], 2),
                               "espesor": round(g[4], 2)} for g in gs]
            else:
                w["bbox_pt"] = None
                w["bands"] = []
        d = out.setdefault(t, {"walls": 0, "lf": 0.0, "filas": []})
        d["filas"] += walls
        d["walls"] += len(walls)
        d["lf"] = round(d["lf"] + sum(w["lf"] for w in walls), 3)
    for t, ap in aparte.items():
        if t in out and (ap["stubs"] or ap["anexos"]):
            out[t]["stubs"], out[t]["anexos"] = ap["stubs"], ap["anexos"]
    return {"modo": modo, "types": out, "other_framing": otros, "avisos": avisos, "escala_pt_por_ft": esc,
            "retipados": {k: v[0] for k, v in retip.items()}, "duplicados": dups,
            "regla": {"jog_max_ft": jog_max_ft, "tol_line_ft": tol_line_ft, "tol_gap_ft": tol_gap_ft}}


def main(argv):
    a = list(argv[1:])
    modo = MODO_DEFAULT
    if "--modo" in a:
        i = a.index("--modo")
        modo = a[i + 1]
        del a[i:i + 2]
    if len(a) not in (1, 2):
        print(__doc__)
        return 2
    r = particion(json.load(open(a[0])), modo)
    if len(a) == 2:
        with open(a[1], "w") as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
    print(f"modo = {r['modo']}")
    for t, d in r["types"].items():
        print(f"{t:14s} {d['walls']:3d} walls {d['lf']:9.2f} LF")
    for x in r["avisos"]:
        print("AVISO:", x)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
