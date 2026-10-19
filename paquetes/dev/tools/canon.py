#!/usr/bin/env python3
"""canon.py v63 — UN takeoff canónico de GEOMETRÍA -> todas las familias, sin juicio fuera de medir el plano.

Por qué existe (arbitraje #11, 16-oct-2026): con studs_nodos.py y board_caras.py obligatorias, las familias
calculadas por tool salieron IGUALES entre #11A y #11B; todas las inestables se armaron a mano. Aquí el agente
declara UNA vez lo que mide y canon.py genera las entradas de studs_nodos / board_caras / corridas / headers,
las corre y suma las familias con los NOMBRES del calificador.

v62 (arbitraje #12, 16-oct-2026) — lo que #12A y #12B tuvieron que dejar PENDING o agregar por fuera:
  - 6" parapet stud POR BAY entre HSS posts (59.4, 11/S5.10 "ONE STUD EA. SIDE OF EA. POST", posts @5'-0" max
    6/S5.10): walls element parapet NO pasan por studs_nodos (#12A <n> / #12B <n> contaban @16" continuo).
  - hanger wire en LF (= hangers x drop deck -> ceiling; convención ref v4). Sin drop -> ValueError.
  - metal trim (corner bead, casing bead, shadow molding) con número: trim_items + jamb returns + transiciones.
  - ceilings: canopy_joist (#12A) y framed_soffit (CSR 10/A09.33) = joists sin carrying ni hangers; un soffit
    no puede ser furring ni stud_joist (#12A CSR como furring +<n>; #12B CSR con carrying +<n>).
  - ceilings: orientación fija del proyecto (constants.carrying_direction + ns_ft/ew_ft) y polígono por cuerda
    media (área / ancho) (#12B room <ref> como rectángulo +<n> carrying).
  - ceiling_perimeter track generado desde ceilings[].perimeter_ft (#12B no lo declaró: -<n>).
  - track_lines por wall con su source (#12B), kickers 7/A09.33 en ceiling_transition, purlin una pieza en
    doble row (59.1, corridas v62), bottom track con descuento de doors solo con fuente (corridas v62).
  - storefront dentro de un wall G/G1 -> ValueError (office fronts = stubs vendor_end + door_bulkhead, 59.7).
  - opening_schedule: lista CERRADA de aberturas barridas (door schedule, ventanas, storefronts, ATMs, grille,
    vestibule box headers, ductos de M-plan) — cada una debe quedar declarada UNA vez (metal, steel_by_others
    con fuente o fits_module). Header salió MAL 5 veces por omisiones silenciosas.

v63 (arbitraje #13, 16-oct-2026) — la VARIANZA entre dos agentes con el mismo skill (#13A <n> / #13B <n> LF
de track; MR <n> / <n>; 1-5/8" <n> / <n>) salió del inventario de walls, no de las fórmulas:
  - inventario.verificar() corre aquí si hay constants.plan_scale_pt_per_ft (y bitacora.py exige inventario.py):
    bandas en planta, solapes, walls apilados, MR por fixture, purlin por flute, altura por zona.
  - glass mat: todo canopy_soffit / fascia_box declara su `facade`, y esa facade DEBE llevar has_canopy y banda
    (#13A dejó sin banda la fachada oeste: 15/A09.27 dibuja la misma línea que 7/A09.26 rotula GLASS-MAT).
  - fascia_box genera su sheathing (5/8" ext. grade FRT plywood, 7/A09.26) = L x H con height_source; un
    plywood_strip de fascia a mano = error (#13A <n> de banda / #13B <n>, los dos a mano).
  - canopy_soffit: track_lines = constants.canopy_soffit_track_lines (una sola vez para el proyecto; #13A 1 / #13B 2).
  - cement board (tile cove base CT, 58.7) con tool: bloque tile_base o tile_base_none_reason (#13A FALTA).
  - jamb_wall (#13A door <ref>) y joist_dir de canopy_joist (#13B) integrados.

v64 (decisiones del usuario/estimador, 2026-10-16 — mandan sobre ref v4, rangos y arbitrajes):
  - header por PIEZAS (#1, #2): header_schedule (con pieces por fila) y sill_rule pasan a headers.py; las
    aberturas pasan pieces / pieces_source / piece / structure / sill_pieces. Salida extra: header_por_pieza.
  - ductos / fire dampers (#12): kind duct | fire_damper -> NOT_FRAMED en headers.py (0 header, 0 sill).
  - storefront con HSS (#16): structure HSS | steel + structure_source -> 0 metal stud header.
  - hanger wire (#4): se entrega en PCS con la altura de cada hanger por room (hanger_pcs); el LF de la familia
    "hanger wire" es renglón DERIVADO = suma PCS x altura.
  - kickers 7/A09.33 (#7): exigen vertical_studs {oc_in, height_ft, bod_ft, ceiling_ft, source} (los studs dashed
    a estructura; v68: height_ft = bod_ft - ceiling_ft, nunca el escalón entre ceilings).
  - room <ref> (#14): system stud_joist exige joist_source (detalle que dibuje joists); un ceiling suspended
    del RCP sin ese detalle es furring.
  - canopy soffit (#13): constants.canopy_soffit_track_lines = 2 (track en los dos extremos de los joists).
  - bottom track en doors (#10): sin descuento (corridas.py rechaza bottom_track_deduct_doors true).

v65 (arbitraje #14A/#14B, 17-oct-2026) — lo que todavía variaba o faltaba entre dos agentes con v64:
  - ceiling_transition NO pasa por studs_nodos (sus studs son kickers + vertical_studs): #14A <n> ft de alto
    contaba los verticales DOS veces (+<n>); #14B height_ft <n> inventado (+<n>). height_ft del elemento =
    vertical_studs.height_ft (bracing, track). Kicker sin largo impreso = vertical_studs.height_ft / sin(angle)
    (45 deg dibujado, 53.3): #14A <n> / #14B <n> a mano.
  - column_wrap NO pasa por studs_nodos: studs = Σ (ROUNDUP(face / oc) + 1) por face (faces_ft) o studs_drawn
    {value, source}; 5/A09.25 4 faces x <n> = <n> studs (A y B <n> = −<n> LF).
  - roof_step: constants.roof_step_rows_drawn {value, source} = cantidad de walls roof_step (4/A02.02 dibuja <n>
    filas; #14A <n> = −<n> LF).
  - canopy_joist exige fascia_box en cada facade de canopy (o fascia_none_reason): #14A sin fascia (−<n> LF).
  - "BOX HEADER AS NEEDED" (openings_extra) exige framing_wall = vestibule_head existente (#14B sin vestibule
    heads: −<n> LF 3-5/8", −<n> bracing).
  - framed_soffit exige drop_lines {value, source} = walls soffit_side / ceiling_bulkhead con soffit_of = room
    (10/A09.33: 1 drop line, el otro borde es la partición; #14B 2 lados +<n>).
  - nodo T entre dos walls G/G1 (10/A12.01) = error -> abut (arb11; #14A +<n> LF 1-5/8").
  - ballistic: constants.ballistic_contour_ft {value, source} = Σ largo de faces con k_panel (E5).
  - glass mat: band.t_stud_ft y band.b_stud_ft {value, source}; altura = T/STUD − B/STUD (7/A09.26 <n>;
    #14A <n> de la elevación T/CANOPY − B/CANOPY = +<n> SF).
  - FRP (familia obligatoria): bloque frp {top_ft, rooms (tile_base), mop_sink} o frp_none_reason (#14B FALTA).
  - acoustical sealant (familia obligatoria): details[*].sealant {bottom_faces, top_faces, source} por cada
    detail con faces, menos R.O. de doors en las corridas de abajo (55.5) + sealant_items + sealant_base_exterior.
  - door entre dos walls (jamb_wall + head_ft): cripples FLOOR(R.O./oc) x (H − head) + bottom/top track R.O.
    (#14A, ADV1-3).
  - level 5 (level5_items, SF) y batt insulation EXCLUDED siempre (criterio del usuario: "no insulation").

v65b (DECISIONES DEL USUARIO #18-#22, 17-oct-2026) — header / sill son REGLAS, no parámetros:
  - header_params se rechaza (v65 lo pasaba a headers.py con default = v64).
  - #19 abertura con "OR STEEL" (or_steel: true u "OR STEEL" en header_type) y header steel_by_others = error.
  - #20 box = 4 piezas, #21 door <ref> double, #18 sill double > 4'-0", #22 office front CONT. BOX BEAM un run por
    frente (continuous_run + wall): los valida headers.py; canon pasa continuous_run / or_steel.

v66 (arbitraje #15A/#15B, 17-oct-2026) — reglas deterministas nuevas (cada una con test en test_canon_v66.py):
  - parapet: walls element parapet exigen line + from_ft/to_ft y length_basis "stud_cl" (eje del stud, no cara
    exterior). Los tramos CONTIGUOS de una misma línea forman UN straight run aunque cambie la altura (los posts
    siguen sobre la viga): bays = ROUNDUP(L_run / post) sobre el run completo, altura ponderada (E3).
  - ballistic_jogs [{ref, length_ft, height_ft, detail, faces_5_8, source}]: jogs / retornos del contorno
    ballistic (E5) SIN crear walls (sin studs fantasma); suman ballistic + 3/8" + 5/8" de la face customer y
    entran en ballistic_contour_ft.
  - column_wrap / pier con parts [{stud_size, studs_drawn {value, source}}]: un detalle que dibuja dos sistemas
    (ej. L interior 3-5/8" METAL FRAMING + L exterior 6" CFMF) carga cada parte en su familia.
  - nailbase a T/STUD del parapet (E25): una facade con walls parapet declara parapet_t_stud_ft {value, source} y
    nailbase_top_ft {value, source}; nailbase_top < T/STUD del parapet sin plywood_strip parapet_face_of = error.
  - canopy_soffit: track = línea de fascia (length_ft) + línea de wall (wall_line_ft {value, source}) medidas por
    separado (corridas.py v66); L x 2 = error.
  - purlin también en ceiling_transition / ceiling_bulkhead con track a deck paralelo al flute (inventario.py).

v67 (accesorios y partition types, 17-oct-2026):
  - accesorios.py corre DENTRO de calcular(): las 15 familias de accesorios / extras salen en familias_out.json
    con estado y fuente (accesorios_out.json aparte); una familia PENDIENTE bloquea plantilla_excel.py armar.
  - partition_types.py corre dentro de calcular(): out["partition_types"] = types de la hoja Partition Takeoff.
  - grille_head NO pasa por studs_nodos (NO_NODOS): su 2-1/2" sale de accesorios.grille_head() desde head_build.
  - Level 5: constants.level5_tags {value, source} obligatorio con level5_items; base descontada en accesorios.
  - E3 (decisión usuario #3): cinco studs por bay como mínimo en TODO bay (dos en posts + tres intermedios), aunque el
    bay mida menos que el spacing de posts; bays más largos suman intermedios @ O.C.
  - column_wrap con fos_chain {value: [eslabones ft], source}: cada face = Σ de la cadena FOS impresa completa.
  - filas de studs con "pcs" explícito (framing screws = 4 x piezas del conteo actual).
  - insulation EXCLUDED en out["excluidas"].

v70 (paquete v70, pruebas #18A / #18B):
  - canopy_soffit en `walls` -> ValueError: doble cuenta de los canopy joists (van en `runs` / ceilings canopy_joist).
  - roof_step, ceiling_transition, soffit_side, ceiling_bulkhead, vestibule_head, grille_head: su detalle dibuja
    board -> `faces` (no vacío) o `faces_none_reason` obligatorio (antes faces [] contaba cero SF en silencio).
  - claves de un wall fuera del esquema (WALL_KEYS): con números (número, o dict / lista con números) ->
    ValueError que nombra la clave y el campo del esquema (plywood -> plywood_strips, blocking -> blocking_items…);
    sin números -> aviso. Sufijos de traza aceptados: _info, _note(s), _check, _source, _status, _img, _reason,
    _basis, _desc, _op (datos que la tool no lee y lo dice el nombre).
  - canopy_joist / framed_soffit: la operación imprime el RUN que cuenta joists:
    "ROUNDUP(<run_ft>/<oc_ft>)+1 = <n> joists x <joist_len_ft> = <LF>" (antes imprimía el largo del joist).
  - constants.deck_breaks.value[] con `sheet`: el quiebre solo se compara con bandas de ESA hoja.

ENTRADA: takeoff_canon.json (esquema en PROTOCOLO_v67.md §4).
SALIDA: familias_out.json {familias: {nombre: valor}, filas: [...], avisos: [...]} + las entradas generadas.

Uso:  python3 canon.py takeoff_canon.json salida_dir/ [--fo fo_in.json]
"""
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import board_caras  # noqa: E402
import corridas  # noqa: E402
import headers  # noqa: E402
import studs_nodos  # noqa: E402
import inventario  # noqa: E402
import accesorios  # noqa: E402   v67: familias de accesorios / extras
import partition_types  # noqa: E402   v67: types de la hoja Partition Takeoff

EPS = 1e-6
F_PAR = "6\" parapet stud"
F_36 = "3-5/8\" stud (todos los gauges)"
F_TRIM = "metal trim (corner bead, casing, shadow molding)"
F_GYP = "5/8\" gyp board regular (walls + ceilings)"
SUSP = ("furring", "stud_joist")                 # sistemas suspendidos: carrying + hangers + perimeter track
JOIST_ONLY = ("canopy_joist", "framed_soffit")   # joists 3-5/8" sin carrying ni hangers
TRIM_KINDS = {"corner_bead", "casing_bead", "shadow_molding", "edge_trim", "j_bead"}
NO_NODOS = ("ceiling_transition", "column_wrap", "grille_head")  # v65 + v67: grille 2-1/2" -> accesorios.py
F_FRP = "FRP"
F_SEAL = "acoustical sealant"
F_L5 = "Level 5 finish"
GG = ("G", "G1")                                   # double row 10/A12.01: junta G-G = abut
# v68: FRT plywood por material / espesor (un renglón de compra por material; la familia del calificador suma todo)
PLY_NAMES = {
    "nailbase_5_8_polyiso": "5/8\" FRT plywood bonded to 2-1/2\" polyiso (exterior sheathing / nailbase)",
    "frt_5_8_ext": "5/8\" exterior grade FRT plywood (canopy soffits, fascia, column wraps)",
    "frt_5_8": "5/8\" FRT plywood",
    "frt_3_4": "3/4\" FRT plywood",
}
PLY = {}                                           # material -> SF (se llena en calcular)
# v73 (arbitraje #21, R73.3): renglón de compra por USO con el nombre de la plantilla del estimador (un renglón por
# material, espesor y uso). `plywood_strips[].uso` lo declara; sin él se infiere del texto (pier / column / canopy).
PLY_USO_NOMBRE = {
    "nailbase": "Exterior sheathing {th} FRT plywood bonded to polyiso (nailbase)",
    "canopy_soffit": "{th} FRT plywood sheathing (canopy and soffits)",
    "column_wrap": "{th} FRT plywood at canopy column wraps",
    "pier": "{th} FRT plywood at storefront piers",
    "substrate": "FRT plywood substrate ({tin} in.)",
}
PLY_USOS = tuple(PLY_USO_NOMBRE)
PLY_TH = {"nailbase_5_8_polyiso": "5/8", "frt_5_8_ext": "5/8", "frt_5_8": "5/8", "frt_3_4": "3/4"}
PLY_USO = {}                                       # nombre de plantilla -> SF
BLK_ORIGEN = {}                                    # v73: metal blocking por origen (edge del detalle / notas)
SEAL = {}                                          # acoustical / exterior -> LF
F_PLY = "FRT plywood (SF)"
RX_MADERA = re.compile(r"\bFRTW?\b|F\.R\.T\.|FIRE[ -]?(TREATED|RETARDANT)|\b2X\b|\bWOOD\b|PLYWOOD", re.I)
RX_FRT_LABEL = re.compile(r"\bFRTW?\b|F\.R\.T\.|FIRE[ -]?(TREATED|RETARDANT)", re.I)


def _ply(fam, mat, sf, uso="substrate"):
    if mat not in PLY_NAMES:
        raise ValueError(f"FRT plywood material '{mat}' fuera de {sorted(PLY_NAMES)} (v68: un renglón por material)")
    if uso not in PLY_USOS:
        raise ValueError(f"FRT plywood uso '{uso}' fuera de {list(PLY_USOS)} (v73)")
    fam[F_PLY] += sf
    PLY[mat] = PLY.get(mat, 0.0) + sf
    th = PLY_TH[mat]
    n = PLY_USO_NOMBRE[uso].format(th=th + '"', tin=th)
    PLY_USO[n] = PLY_USO.get(n, 0.0) + sf


def _uso_strip(s):
    u = s.get("uso")
    if u:
        return u
    t = " ".join(str(s.get(k) or "") for k in ("ref", "element", "source", "location", "material", "label"))
    if re.search(r"polyiso|nailbase|bonded", t, re.I):
        return "nailbase"
    if re.search(r"\bcolumn", t, re.I):
        return "column_wrap"
    if re.search(r"\bpiers?\b", t, re.I):
        return "pier"
    if re.search(r"canopy|fascia|soffit", t, re.I):
        return "canopy_soffit"
    return "substrate"


TRACK_PARAPET = ("parapet",)
TRACK_HEADS = ("roof_step", "vestibule_head", "fascia_box", "ceiling_bulkhead", "soffit_side")
TRACK_NOMBRES = {   # v73 (R73.3): renglones de track de la plantilla del estimador
    "parapet": ("Parapet bottom track", "Parapet top track"),
    "heads": ("Bottom track - roof step and heads (vestibule / soffit)",
              "Top track - roof step and heads (vestibule / soffit)"),
    "size": ("Bottom track {sz}", "Top / deflection track {sz}"),
    "otro": ("Bottom track - other (openings between walls, see source)",
             "Top / deflection track - other (openings between walls, see source)"),
}


def track_by_element(data, co, fam):
    """{"bottom": {renglón: LF}, "top": {renglón: LF}}: la familia de track repartida por ELEMENTO (parapet, roof step /
    heads) y, para el resto, por TAMAÑO de stud del wall (R71.8 + R73.3). Σ renglones = familia (el resto que corridas
    no explica, p. ej. track sobre openings entre walls, va a 'other'). Nombres = plantilla del estimador."""
    tam = {}
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        m = re.search(r'(\d+-\d+/\d+"|\d+(?:\.\d+)?")', str(w.get("stud_size") or ""))
        if m:
            tam[str(w.get("id"))] = m.group(1)
    out = {"bottom": {}, "top": {}}
    for r in co.get("renglones") or []:
        el = r.get("element")
        wid = str(r.get("id") or "").split(":", 1)[-1]
        if el in TRACK_PARAPET:
            nb, nt = TRACK_NOMBRES["parapet"]
        elif el in TRACK_HEADS:
            nb, nt = TRACK_NOMBRES["heads"]
        else:
            sz = tam.get(wid) or r.get("stud_size")
            nb, nt = (x.format(sz=sz) for x in TRACK_NOMBRES["size"]) if sz else TRACK_NOMBRES["otro"]
        for k, n, v in (("bottom", nb, r.get("bottom_lf")), ("top", nt, r.get("top_lf"))):
            if v:
                out[k][n] = out[k].get(n, 0.0) + float(v)
    for k, f, no in (("bottom", "bottom track (todos)", TRACK_NOMBRES["otro"][0]),
                     ("top", "top / deflection track (todos)", TRACK_NOMBRES["otro"][1])):
        resto = float(fam.get(f, 0.0)) - sum(out[k].values())
        if resto > 0.01:
            out[k][no] = out[k].get(no, 0.0) + resto
        out[k] = {n: round(v, 2) for n, v in out[k].items() if v > EPS}
    return out


def _no_nodos(w):
    """v68: pier con parts tampoco pasa por studs_nodos (sus studs salen de parts, como column_wrap)."""
    return w.get("element") in NO_NODOS or (w.get("element") == "pier" and bool(w.get("parts")))


def _c(data, k, dflt=None):
    c = (data.get("constants") or {}).get(k)
    if c is None:
        if dflt is None:
            raise ValueError(f"constants.{k} ausente")
        return dflt
    if not isinstance(c, dict) or "value" not in c or not str(c.get("source") or "").strip():
        raise ValueError(f"constants.{k} debe ser {{value, source}}")
    return c["value"] if isinstance(c["value"], str) else float(c["value"])


def _src(o, ctx, k="source"):
    s = str(o.get(k) or "").strip()
    if not s:
        raise ValueError(f"{ctx}: falta {k} (N/HOJA)")
    return s


def _solapes(items):
    por_linea = {}
    for it in items:
        if it.get("line") is None:
            continue
        a, b = float(it["from_ft"]), float(it["to_ft"])
        if b <= a:
            raise ValueError(f"{it['id']}: to_ft <= from_ft")
        por_linea.setdefault(it["line"], []).append((a, b, it["id"]))
    for ln, xs in por_linea.items():
        xs.sort()
        for (a1, b1, i1), (a2, b2, i2) in zip(xs, xs[1:]):
            if a2 < b1 - 0.01:
                raise ValueError(f"line {ln}: {i1} [{a1}-{b1}] y {i2} [{a2}-{b2}] se solapan "
                                 f"{round(b1 - a2, 3)} ft (mismo framing contado dos veces)")


def _es_parapet(w):
    return w.get("element") == "parapet"


def _cerrar_aberturas(data, declaradas):
    """opening_schedule: cada abertura barrida debe declararse UNA vez (metal / steel_by_others / fits)."""
    sch = data.get("opening_schedule")
    if sch is None:
        if declaradas:
            raise ValueError("opening_schedule ausente: lista cerrada de aberturas barridas (door schedule, "
                             "windows, storefronts, ATMs, grille, box headers, ductos M-plan) — v62")
        return []
    hojas = [str(h) for h in sch.get("sources") or []]
    if not any(re.match(r"^(\w+/)?S\d", h) for h in hojas):
        raise ValueError("opening_schedule.sources sin plan estructural (S*): barrer lintels HSS / steel headers")
    if not any(re.match(r"^(\w+/)?M\d", h) for h in hojas):
        raise ValueError("opening_schedule.sources sin M-plan: barrer ductos / fire dampers en walls (58.4)")
    pedidas = [str(i["ref"]) for i in sch.get("items") or []]
    if len(set(pedidas)) != len(pedidas):
        raise ValueError("opening_schedule.items con ref repetido")
    vistos = {}
    for r in declaradas:
        vistos[r] = vistos.get(r, 0) + 1
    for i in sch.get("none") or []:                      # barridas que no llevan header (con motivo)
        if not str(i.get("why") or "").strip():
            raise ValueError(f"opening_schedule.none {i.get('ref')}: falta why")
        vistos[str(i["ref"])] = vistos.get(str(i["ref"]), 0) + 1
    falta = [r for r in pedidas if vistos.get(r, 0) == 0]
    dobles = [r for r in pedidas if vistos.get(r, 0) > 1]
    if falta:
        raise ValueError(f"opening_schedule: {len(falta)} abertura(s) barrida(s) sin declarar: {falta}")
    if dobles:
        raise ValueError(f"opening_schedule: declaradas más de una vez: {dobles}")
    fuera = sorted(set(declaradas) - set(pedidas))
    if fuera:
        raise ValueError(f"aberturas declaradas que no están en opening_schedule.items: {fuera}")
    return hojas


def _ceil_dims(data, c):
    """(span, run) en la orientación del proyecto. span = largo del carrying channel."""
    dirc = (data.get("constants") or {}).get("carrying_direction")
    if dirc is not None:
        d = str(_c(data, "carrying_direction")).upper().replace("–", "-")
        if d not in ("N-S", "E-W"):
            raise ValueError("constants.carrying_direction debe ser N-S | E-W")
        if "ns_ft" not in c or "ew_ft" not in c:
            raise ValueError(f"{c.get('room')}: con carrying_direction declarar ns_ft y ew_ft (no span/run: "
                             f"la orientación es del proyecto, no de cada room — #12A room <ref> cruzado)")
        ns, ew = float(c["ns_ft"]), float(c["ew_ft"])
        return (ns, ew) if d == "N-S" else (ew, ns)
    return float(c["span_ft"]), float(c["run_ft"])


def generar(data):
    walls = data.get("walls") or []
    runs_extra = data.get("runs") or []
    _solapes([dict(w, id=w["id"], **({"line": "PAR:" + str(w["line"])} if _es_parapet(w) and w.get("line") is not None
                                    else {})) for w in walls] + [dict(r, id=r["id"]) for r in runs_extra])
    for r in runs_extra:
        if r.get("element") in ("parapet", "column_wrap", "pier") or _es_parapet(r):
            # v68: sus studs solo se cuentan desde walls (E3 / wraps); en runs se perdían sin aviso (como TR-104 #16B)
            raise ValueError(f"{r['id']}: element {r.get('element')} va en walls, no en runs (sus studs salen de "
                             f"walls; v68)")
        if r.get("element") == "ceiling_perimeter":
            raise ValueError(f"{r['id']}: ceiling_perimeter lo genera canon.py desde ceilings[].perimeter_ft (v62)")
    par_ids = {w["id"] for w in walls if _es_parapet(w) or _no_nodos(w)}
    nodes = []
    for n in data.get("nodes") or []:
        ws = set(n.get("walls") or []) | ({n["wall"]} if n.get("wall") else set())
        if ws and ws <= par_ids:
            continue                                     # parapet: se cuenta por bay, sin nodos
        if n.get("kind") == "abut" and n.get("into") in par_ids and n.get("wall") not in par_ids:
            nodes.append({"id": n.get("id"), "kind": "free", "wall": n["wall"]})   # v65: abut (0) contra column_wrap
            continue
        if ws & par_ids:
            raise ValueError(f"nodo {n.get('id')}: mezcla parapet y wall — el parapet se cuenta por bay (59.4)")
        nodes.append(n)
    studs_in = {"walls": [], "nodes": nodes}
    board_in = {"details": data.get("details") or {}, "walls": []}
    runs, ops, avisos, declaradas = [], [], [], []
    for w in walls:
        src = _src(w, w["id"])
        tag = str(w.get("tag") or "").upper()
        for o in w.get("openings") or []:
            if tag in ("G", "G1") and o.get("kind") == "storefront":
                raise ValueError(f"{w['id']} {o['ref']}: storefront dentro de un wall {tag} — office front = stubs "
                                 f"con nodo vendor_end + door_bulkhead (59.7, #12B)")
        if not _es_parapet(w) and not _no_nodos(w):
            sw = {k: w[k] for k in ("id", "tag", "stud_size", "length_ft", "oc_in", "rows", "height_ft", "zones")
                  if k in w}
            sw["openings"] = [{"ref": o["ref"], "ro_w_ft": o["ro_w_ft"], "head_ft": o["head_ft"],
                               "sill_ft": o.get("sill_ft", 0)} for o in w.get("openings") or []]
            studs_in["walls"].append(sw)
        if w.get("faces"):
            board_in["walls"].append({"id": w["id"], "tag": w.get("tag"), "detail": w["detail"],
                                      "length_vector_ft": w["length_ft"],
                                      **({"length_printed_ft": w["length_printed_ft"]}
                                         if w.get("length_printed_ft") is not None else {}),
                                      "faces": w["faces"]})
        runs.append({"id": "W:" + w["id"], "element": w.get("element", "wall"), "orientation": "vertical",
                     "length_ft": w["length_ft"], "height_ft": w["height_ft"], "rows": w.get("rows", 1),
                     "openings": [{"ro_w_ft": o["ro_w_ft"], "sill_ft": o.get("sill_ft", 0), "head_ft": o["head_ft"],
                                   "kind": o.get("kind", "door")} for o in w.get("openings") or []],
                     "purlin": bool(w.get("purlin")), "source": src,
                     **({k: w[k] for k in ("track_lines", "track_lines_source", "wall_line_ft") if k in w})})
        for o in w.get("openings") or []:
            declaradas.append(str(o["ref"]))
            hdr = o.get("header", "metal")
            _v65b_or_steel(o, hdr)
            if hdr == "steel_by_others":
                if not str(o.get("header_source") or "").strip():
                    raise ValueError(f"{w['id']} {o['ref']}: header steel_by_others sin header_source "
                                     f"(si el detalle dice 'box beam OR steel' -> metal + RFI, 53.3)")
                avisos.append(f"{o['ref']}: header steel by others ({o['header_source']}) — fuera de header LF")
                continue
            if hdr != "metal":
                raise ValueError(f"{o['ref']}: header debe ser metal | steel_by_others")
            ops.append({"ref": o["ref"], "wall": w["id"], "kind": o.get("kind", "door"),
                        "location": o.get("location", ""), "ro_w_ft": o["ro_w_ft"], "qty": 1,
                        "with_sill": bool(o.get("with_sill")), "source": o.get("source", src),
                        **{k: o[k] for k in ("header_type", "header_type_source", "beams", "beams_source",
                                             "structure_source", "structure", "pieces", "pieces_source",
                                             "piece", "sill_pieces", "sill_pieces_source", "continuous_run",
                                             "or_steel", "run_ends", "run_ends_source") if k in o}})
    for c in data.get("ceilings") or []:
        if c.get("system") in SUSP:
            if c.get("perimeter_ft") is None:
                raise ValueError(f"{c['room']}: ceiling {c['system']} sin perimeter_ft (ceiling_perimeter track, "
                                 f"#12B -<n>)")
            runs.append({"id": "CP:" + str(c["room"]), "element": "ceiling_perimeter", "orientation": "horizontal",
                         "length_ft": float(c["perimeter_ft"]), "source": _src(c, c["room"])})
    for r in runs_extra:
        rr = dict(r)
        for k in ("line", "from_ft", "to_ft"):
            rr.pop(k, None)
        runs.append(rr)
    corr_in = {"bracing": {"spacing_in": _c(data, "bracing_spacing_in", 48.0),
                           "source": (data.get("constants") or {}).get("bracing_spacing_in", {}).get("source",
                                                                                                   "F/1/S5.20")},
               "section_details": data.get("section_details") or [],
               "ceiling_details": data.get("ceiling_details") or [],
               "runs": runs}
    if data.get("bottom_track_deduct_doors") is not None:
        corr_in["bottom_track_deduct_doors"] = data["bottom_track_deduct_doors"]
    hdr_in = {"openings": ops} if ops else None
    for extra in data.get("openings_extra") or []:          # aberturas fuera de walls (grille, vestibule)
        declaradas.append(str(extra["ref"]))
        _v65b_or_steel(extra, extra.get("header", "metal"))
        if extra.get("header") == "steel_by_others":
            if not str(extra.get("header_source") or "").strip():
                raise ValueError(f"{extra['ref']}: header steel_by_others sin header_source")
            avisos.append(f"{extra['ref']}: header steel by others ({extra['header_source']}) — fuera de header LF")
            continue
        hdr_in = hdr_in or {"openings": []}
        hdr_in["openings"].append({k: v for k, v in extra.items() if k not in ("header", "header_source",
                                                                                 "jamb_return", "jamb_return_source",
                                                                                 "head_ft", "sill_ft", "jamb_wall",
                                                                                 "jamb_wall_source")})
    if hdr_in:
        for k in ("header_schedule", "sill_rule", "stud_bay_in", "stud_bay_source"):
            if data.get(k) is not None:
                hdr_in[k] = data[k]
    _cerrar_aberturas(data, declaradas)
    return studs_in, board_in, corr_in, hdr_in, avisos


def _v65b_or_steel(o, hdr):
    """Decisión usuario #19: 'METAL STUD BOX BEAM OR STEEL FRAMING AS REQUIRED' = metal stud box beam."""
    if hdr == "steel_by_others" and (o.get("or_steel") or "OR STEEL" in str(o.get("header_type") or "").upper()):
        raise ValueError(f"{o.get('ref')}: 'BOX BEAM OR STEEL FRAMING AS REQUIRED' = METAL STUD BOX BEAM, 4 piezas "
                         f"(decisiones usuario #19, #20; 11/A09.27) — no steel_by_others")


def _v65_checks(data):
    """Reglas deterministas del arbitraje #14 (17-oct-2026) que no necesitan totales."""
    if data.get("header_params") is not None:
        raise ValueError("header_params ya no existe (v65b): sill double > 4'-0\", GL-2 metal box, box = 4 piezas, "
                         "door double y office front continuo son reglas (decisiones usuario #18-#22)")
    walls = data.get("walls") or []
    por_id = {w["id"]: w for w in walls}
    tags = {w["id"]: str(w.get("tag") or "").upper() for w in walls}
    # roof step: filas dibujadas en el detalle (4/A02.02: 3)
    rs = [w for w in walls if w.get("element") == "roof_step"]
    if rs:
        n = _c(data, "roof_step_rows_drawn", -1)
        if n == -1:
            raise ValueError("constants.roof_step_rows_drawn {value, source} obligatoria con roof_step (filas de "
                             "studs que dibuja el detalle)")
        if len(rs) != int(n):
            raise ValueError(f"roof_step: {len(rs)} walls declarados != roof_step_rows_drawn {int(n)} (una pieza por "
                             f"fila dibujada en el detalle, cada una con su altura)")
    # canopy_joist -> fascia_box en cada facade de canopy
    for r in data.get("runs") or []:
        if r.get("element") == "fascia_box":
            raise ValueError(f"{r['id']}: fascia_box en runs no cuenta studs — va en walls (3-5/8\" studs @16\" "
                             f"T/STUD - B/STUD, 7/A09.26; v65, #14A −<n> LF)")
    cj = [c for c in data.get("ceilings") or [] if c.get("system") == "canopy_joist"]
    if cj and not str(data.get("fascia_none_reason") or "").strip():
        if not any(w.get("element") == "fascia_box" for w in walls):
            raise ValueError("canopy_joist sin fascia_box en walls — la fascia (T/STUD - B/STUD, 7/A09.26) lleva studs "
                             "3-5/8\" y track; o fascia_none_reason (v65, #14A −<n> LF)")
    # BOX HEADER AS NEEDED -> framing_wall (vestibule_head)
    for o in data.get("openings_extra") or []:
        if "AS NEEDED" in str(o.get("header_type") or "").upper():
            fw = o.get("framing_wall")
            if fw not in por_id or por_id[fw].get("element") != "vestibule_head":
                raise ValueError(f"{o['ref']}: 'BOX HEADER AS NEEDED' sin framing_wall (vestibule_head) — 4-7/A12.10 "
                                 f"'METAL STUD FRAMING & BOX HEADER AS NEEDED': los studs sobre el storefront se "
                                 f"cuentan (v65, #14B −<n> LF)")
    # framed_soffit -> drop_lines
    for c in data.get("ceilings") or []:
        if c.get("system") != "framed_soffit":
            continue
        dl = c.get("drop_lines")
        if not isinstance(dl, dict) or not str(dl.get("source") or "").strip():
            raise ValueError(f"{c['room']}: framed_soffit sin drop_lines {{value, source}} (líneas de drop studs que "
                             f"= bordes del soffit que en el RCP dan a un ceiling, no a una partición; 10/A09.33 dibuja STL STUD "
                             f"donde el soffit encuentra el scheduled ceiling — v66)")
        ds = [w for w in walls if w.get("soffit_of") == c["room"]
              and w.get("element") in ("soffit_side", "ceiling_bulkhead", "soffit_drop")]
        lineas = {w.get("drop_line", w["id"]) for w in ds}
        if len(lineas) != int(dl["value"]):
            raise ValueError(f"{c['room']}: {len(lineas)} drop line(s) declaradas (soffit_of) != drop_lines "
                             f"{int(dl['value'])} (#14B 2 lados = +<n> LF; tramos de una línea comparten drop_line)")
    # T entre dos G/G1 -> abut
    for n in data.get("nodes") or []:
        if n.get("kind") == "T" and tags.get(n.get("branch")) in GG and tags.get(n.get("through")) in GG:
            raise ValueError(f"nodo {n.get('id')}: T entre {n.get('branch')} y {n.get('through')} (G/G1, double row "
                             f"10/A12.01) -> abut: el stud de la junta está en el stub (arb11, #14A)")
    # ballistic: contorno medido UNA vez
    det = data.get("details") or {}
    kl = 0.0
    hay = False
    for w in walls:
        for f in w.get("faces") or []:
            if f.get("k_customer"):
                hay = True
                kl += float(f["length_ft"]) if f.get("length_ft") is not None else \
                    float(w.get("length_printed_ft") or w["length_ft"])
    for j in data.get("ballistic_jogs") or []:              # v66: jogs del contorno sin wall propio (E5)
        hay = True
        kl += float(j["length_ft"])
    if hay:
        bc = _c(data, "ballistic_contour_ft", -1)
        if bc == -1:
            raise ValueError("constants.ballistic_contour_ft {value, source} obligatoria con ballistic (E5: contorno "
                             "completo con jogs, medido una vez: Σ faces customer + ballistic_jogs)")
        if abs(kl - float(bc)) > 0.05:
            raise ValueError(f"ballistic: Σ largo de faces k_customer {round(kl, 3)} != ballistic_contour_ft {bc} "
                             f"(#14A <n> con el A1K SW <n>; #14B <n> con <n> en vez de la cota impresa)")
    del det
    if data.get("level5_items") and "level5_tags" not in (data.get("constants") or {}):
        raise ValueError("constants.level5_tags {value, source} obligatorio con level5_items (v67): tags del "
                         "finish schedule con 'LEVEL 5' + key notes del finish plan")
    # batt insulation: EXCLUDED siempre (criterio del usuario)
    for k in ("insulation", "insulation_items", "batt_insulation"):
        if data.get(k):
            raise ValueError(f"'{k}': batt insulation EXCLUDED siempre (criterio del usuario 'no insulation')")


def _strip_material(s):
    """v68 (#16A/#16B, RFI-27): cada plywood_strip declara material (espesor / producto); el texto de ref y label no
    puede contradecirlo; lo rotulado BLOCKING va en blocking_items (LF), nunca como strip (SF)."""
    mat = s.get("material")
    txt = f"{s.get('ref', '')} {s.get('label', '')}"
    if "BLOCKING" in txt.upper():
        raise ValueError(f"plywood_strip '{s.get('ref')}': rotulado BLOCKING -> blocking_items en LF (#16B CSR soffit "
                         f"FRTW blocking cargado como SF)")
    if mat not in PLY_NAMES:
        raise ValueError(f"plywood_strip '{s.get('ref')}': material obligatorio, uno de {sorted(PLY_NAMES)} (v68; #16B "
                         f"strip sin espesor)")
    if '3/4"' in txt and mat != "frt_3_4":
        raise ValueError(f"plywood_strip '{s.get('ref')}': el texto dice 3/4\" y material = {mat}")
    if '5/8"' in txt and mat == "frt_3_4":
        raise ValueError(f"plywood_strip '{s.get('ref')}': el texto dice 5/8\" y material = frt_3_4")
    if "POLYISO" in txt.upper() and mat != "nailbase_5_8_polyiso":
        raise ValueError(f"plywood_strip '{s.get('ref')}': bonded to polyiso = nailbase_5_8_polyiso")
    return mat


def _num_src(o, ctx):
    if not isinstance(o, dict) or "value" not in o or not str(o.get("source") or "").strip():
        raise ValueError(f"{ctx}: {{value, source}} obligatorio")
    return o["value"]


AISC_D_IN = None


def _v68_checks(data):
    """Reglas deterministas del arbitraje #16 (17-oct-2026): lo que varió entre #16A y #16B con el mismo plano."""
    walls = data.get("walls") or []
    # 1. 5/8" MR solo detrás del fixture (A08.01 F 'BEHIND TOILET AND LAVATORY'): wet_fixtures con back_source
    wf = data.get("wet_fixtures") or []
    for x in wf:
        if not str(x.get("back_source") or "").strip():
            raise ValueError(f"wet_fixture '{x.get('ref')}': back_source obligatorio (N/HOJA que muestra el respaldo / "
                             f"carrier del fixture contra ESE wall; la pared lateral de grab bars no es 'behind'; #16B "
                             f"puso los WC en el exterior wall)")
    con_fix = {(str(x.get("wall")), str(x.get("room"))) for x in wf}
    for w in walls:
        for f in w.get("faces") or []:
            if f.get("board") == "5/8 MR" and (str(w["id"]), str(f.get("room"))) not in con_fix:
                raise ValueError(f"{w['id']} {f.get('room')}: 5/8 MR sin wet_fixture (wall, room) con back_source — MR "
                                 f"solo detrás del fixture (v68, #16B)")
    # 1b. ballistic (E5): jogs declarados (lista o motivo) y largo de cada face customer con su fuente
    kw = [w for w in walls if any(f.get("k_customer") for f in w.get("faces") or [])]
    if kw:
        if "ballistic_jogs" not in data and not str(data.get("ballistic_jogs_none_reason") or "").strip():
            raise ValueError("ballistic: ballistic_jogs [...] o ballistic_jogs_none_reason obligatorio (v68: #16A y #16B "
                             "sin el jog del contorno; la decisión del estimador lo sigue)")
        for w in kw:
            if w.get("length_printed_ft") is None and not str(w.get("length_source") or "").strip():
                raise ValueError(f"{w['id']}: face customer (ballistic) sin length_printed_ft ni length_source (cota "
                                 f"impresa o vector con coordenadas; #16B largo vector contra la cota impresa)")
    # 2. parapets: plies de FRT blocking contados en el detalle
    for p_ in data.get("parapets") or []:
        pb = p_.get("plies_blocking")
        if not isinstance(pb, dict):
            raise ValueError(f"{p_.get('id')}: plies_blocking {{value, source}} obligatorio (capas de plywood que DIBUJA "
                             f"el detalle del remate; #16A y #16B distinto con el mismo detalle)")
        _num_src(pb, f"{p_.get('id')}.plies_blocking")
    # 3. blocking_items: rótulo literal (o motivo) en todos; rótulo FRT -> material FRT
    for it in data.get("blocking_items") or []:
        lab = str(it.get("label") or "")
        if not lab.strip() and not str(it.get("no_label_reason") or "").strip():
            raise ValueError(f"{it.get('ref')}: blocking sin label (texto literal del detalle / sheet note) ni "
                             f"no_label_reason (v68: #16B items 'metal' sin rótulo donde la sheet note dice FRT)")
        if RX_FRT_LABEL.search(lab) and it.get("material") != "FRT":
            raise ValueError(f"{it.get('ref')}: el rótulo '{lab}' dice FRT y material = {it.get('material')}")
    # 4. ceilings suspendidos: detalle del RCP o motivo; details[d].ceiling_system manda
    det = data.get("details") or {}
    for c in data.get("ceilings") or []:
        d = c.get("detail")
        if c.get("system") in SUSP and not d and not str(c.get("detail_none_reason") or "").strip():
            raise ValueError(f"{c['room']}: ceiling suspendido sin detail (N/HOJA) ni detail_none_reason (v68: #16B "
                             f"116 CSR soffit 10/A09.33 como furring con hangers)")
        cs = (det.get(d) or {}).get("ceiling_system") if d else None
        if cs and cs != c.get("system"):
            raise ValueError(f"{c['room']}: system {c.get('system')} != details['{d}'].ceiling_system {cs}")
    # 5. quiebres de deck: ningún wall cruza un quiebre sin partirse
    cb = (data.get("constants") or {}).get("deck_breaks")
    if cb is None and not str(data.get("deck_breaks_none_reason") or "").strip():
        raise ValueError("constants.deck_breaks {value: [{ori_walls: H|V, coord_pt, sheet}], source} o deck_breaks_none_reason "
                         "obligatorio (v68: #16A y #16B, un wall cada uno, cruzan un grid con una sola altura)")
    for br in (cb or {}).get("value") or []:
        _src(cb, "constants.deck_breaks")
        for w in walls:
            b = w.get("band") or {}
            if b.get("ori") != br["ori_walls"]:
                continue
            # v70 (#18A): coord_pt es de UNA hoja; un wall con banda en otra hoja (p. ej. roof plan) no se compara
            if br.get("sheet") and _hoja_wall(w) and str(_hoja_wall(w)) != str(br["sheet"]):
                continue
            lo, hi = sorted((float(b["lo"]), float(b["hi"])))
            if lo + 1.0 < float(br["coord_pt"]) < hi - 1.0 and not str(w.get("break_reason") or "").strip():
                raise ValueError(f"{w['id']}: cruza el quiebre de deck en {br['coord_pt']} pt ({cb['source']}) — partir "
                                 f"en dos walls con su altura, o break_reason (altura que no depende del deck)")
    # 6. stops_under_beam: perfil único y peralte AISC; altura = B.O.D. - d
    import vigas_sobre_walls as V
    for w in walls:
        sb = w.get("stops_under_beam")
        if not isinstance(sb, dict) or sb.get("value") is False:
            continue
        prof = str(sb.get("profile") or "").upper().replace(" ", "")
        if prof not in V.AISC_D_IN and not str(sb.get("d_source") or "").strip():
            raise ValueError(f"{w['id']}: stops_under_beam.profile '{sb.get('profile')}' no es una marca única de "
                             f"{sorted(V.AISC_D_IN)} ni trae d_source (#16A 'W12 / W14x22' con un solo peralte)")
        d_ft = V.AISC_D_IN[prof] / 12.0 if prof in V.AISC_D_IN else float(sb["depth_ft"])
        if sb.get("depth_ft") is not None and abs(float(sb["depth_ft"]) - d_ft) > 0.01:
            raise ValueError(f"{w['id']}: depth_ft {sb['depth_ft']} != d AISC {prof} {round(d_ft, 3)}")
        bod = sb.get("bod_ft")
        if bod is not None:
            hb = float(_num_src(bod, f"{w['id']}.stops_under_beam.bod_ft")) - d_ft
            if abs(float(w["height_ft"]) - hb) > 0.02:
                raise ValueError(f"{w['id']}: height_ft {w['height_ft']} != B.O.D. {bod['value']} - d {round(d_ft, 3)} "
                                 f"= {round(hb, 3)} (E26)")


BOARD_ELEMS = ("roof_step", "ceiling_transition", "soffit_side", "ceiling_bulkhead", "vestibule_head", "grille_head")
# Claves que canon.py y las tools que reciben los walls (inventario, partition_types, accesorios, studs_nodos,
# board_caras, corridas, headers, particion / comparar / etapas v69) leen de un wall, + campos de traza de etapas.
WALL_KEYS = frozenset("""
id tag element location room sheet plan_sheet page band line from_ft to_ft axis ori straight_run split_of front
facade chase length_ft length_source length_status length_printed_ft length_printed_source length_vector_ft
length_basis length_op height_ft height_source height_status height_op height_avg_ft zones zones_source zone
to_deck to_deck_source stops_under_beam canopy_beam break_reason stud_size stud_source stud_size_source
stud_size_status gauge gauge_source stud_gauge oc_in oc_source rows rows_source purlin purlin_source purlin_note
detail detail_source faces faces_ft faces_ft_source faces_note faces_none_reason fos_chain parts kickers
vertical_studs edges drop_line soffit_of openings track_lines track_lines_source wall_line_ft bulkhead_of
bottom_track_lf head_build exterior in_cavity in_cavity_source source source_chain status notes note tag_ids
tags_descartados band_length_ok_reason img evidence_png type_source type_status default_type_source adjacent_to
adjacent_source wet_fixtures k_customer studs_drawn hatch_extent dim_scan
""".split())
TRAZA_SUFIJOS = ("_info", "_note", "_notes", "_check", "_source", "_status", "_img", "_reason", "_basis", "_desc",
                 "_op")
SUGERIR = {"plywood": "plywood_strips", "frt": "plywood_strips", "sheathing": "plywood_strips / facades",
           "blocking": "blocking_items", "backing": "blocking_items", "board": "faces", "gyp": "faces",
           "faces": "faces", "trim": "trim_items", "bead": "trim_items", "sealant": "sealant_items", "frp": "frp",
           "tile": "tile_base", "level5": "level5_items", "insulation": "(EXCLUDED: no insulation)",
           "kicker": "kickers", "stud": "parts / vertical_studs / height_ft", "header": "openings[].header_type",
           "height": "height_ft (+ height_source) o zones", "length": "length_ft / length_printed_ft",
           "deck": "constants.deck_breaks + break_reason", "depth": "detail (details[d]) o *_info",
           "opening": "openings[] / openings_extra"}


def _con_numeros(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, dict):
        return any(_con_numeros(x) for x in v.values())
    if isinstance(v, list):
        return any(_con_numeros(x) for x in v)
    return False


def _sugerencia(k):
    for clave, campo in SUGERIR.items():
        if clave in k.lower():
            return campo
    return "un campo del esquema (PROTOCOLO §4) o sufijo _info si es solo traza"


def _v70_checks(data, avisos):
    """Reglas v70 (#18A / #18B): canopy_soffit fuera de walls, faces de los elementos con board, claves fuera de
    esquema. Corre ANTES que todo lo demás para que el mensaje sea el de la regla."""
    walls = data.get("walls") or []
    for w in walls:
        if w.get("element") == "canopy_soffit":
            raise ValueError(f"{w['id']}: canopy_soffit en walls cuenta dos veces los canopy joists (ya salen del "
                             f"ceiling canopy_joist) — va en runs (track) / ceilings, nunca en walls (v70, #18B)")
    for w in walls:
        if w.get("element") in BOARD_ELEMS and not w.get("faces") and \
                not str(w.get("faces_none_reason") or "").strip():
            raise ValueError(f"{w['id']}: {w['element']} sin faces — its detail draws board: declare faces or "
                             f"faces_none_reason (v70, #18B roof_step / ceiling_transition con faces [] = 0 SF)")
    _r70_1(data, avisos)
    _r70_6(walls)
    _r70_7(walls)
    malos = []
    for w in walls:
        for k, v in w.items():
            if k in WALL_KEYS or k.endswith(TRAZA_SUFIJOS):
                continue
            if _con_numeros(v):
                malos.append(f"{w.get('id')}.{k} -> {_sugerencia(k)}")
            else:
                avisos.append(f"{w.get('id')}: clave '{k}' fuera del esquema (sin números): canon.py no la lee")
    if malos:
        raise ValueError(f"{len(malos)} clave(s) de walls fuera del esquema CON números (canon.py las ignoraría en "
                         f"silencio; #18B: walls[].plywood ignorado) — mover al campo del esquema o renombrar "
                         f"con sufijo _info si es solo traza: " + "; ".join(malos))


RX_NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,3}-?\d")
RX_SUSP = re.compile(r"\bSUSPEND", re.I)
RX_CARA_EXT = re.compile(r"EXTERIOR|NO\s+GYP|OUTSIDE", re.I)


def _r70_1(data, avisos):
    """R70.1 (v70): el sistema de un ceiling es el del campo (RCP / leyenda). Todo ceiling que no es furring declara
    system_callout {detail N/HOJA, on_plan: true, source}: el bubble de ESE detalle dibujado sobre ESTE ceiling. Un
    detalle típico local (p. ej. un fixture con joists) no cambia el sistema del campo."""
    for c in data.get("ceilings") or []:
        sysm = c.get("system")
        if sysm == "furring":
            continue
        sc = c.get("system_callout")
        ok = isinstance(sc, dict) and RX_NHOJA.search(str(sc.get("detail") or "")) and sc.get("on_plan") is True \
            and str(sc.get("source") or "").strip()
        susp = RX_SUSP.search(f"{c.get('source', '')} {c.get('legend', '')}")
        if not ok:
            raise ValueError(f"{c.get('room')}: ceiling {sysm}" + (" con source / legend SUSPENDED" if susp else "")
                             + " sin system_callout {detail, on_plan: true, source} — R70.1: a typical local detail "
                               "does not change the field system; declare system_callout (bubble on THIS ceiling) "
                               "or use furring + RFI")
        if susp:
            avisos.append(f"{c.get('room')}: ceiling {sysm} con leyenda SUSPENDED y system_callout "
                          f"{sc['detail']} ({sc['source']}): revisar que el bubble esté sobre este ceiling (R70.1)")


def _r70_6(walls):
    """R70.6 (v70): pier / column_wrap con parts y tag interior: el LF del type = caras del sistema INTERIOR (las que
    llevan board hacia un room), no el perímetro completo de la caja (que incluye la parte exterior)."""
    for w in walls:
        if w.get("element") not in ("pier", "column_wrap") or not w.get("parts"):
            continue
        tag = str(w.get("tag") or "").upper().replace(" ", "")
        if tag.startswith(("EXT", "CANOPY")) or str(w.get("type_lf_basis") or "").strip():
            continue
        pf = [p_.get("faces_ft") for p_ in w["parts"]]
        if all(isinstance(x, list) and x for x in pf):
            perim = sum(float(v) for x in pf for v in x)
        else:
            fs = w.get("faces") or []
            if not fs or any(f.get("length_ft") is None for f in fs):
                continue
            perim = sum(float(f["length_ft"]) for f in fs)
        inter = sum(float(f.get("length_ft") or 0) for f in w.get("faces") or []
                    if f.get("board") and float(f.get("height_ft") or 0) > 0
                    and not RX_CARA_EXT.search(str(f.get("room") or "")))
        L = float(w["length_ft"])
        if abs(L - perim) <= 0.02 and inter < perim - 0.02:
            raise ValueError(f"{w['id']}: {w['element']} {w.get('tag')} con parts: length_ft {L} = perímetro completo de "
                             f"la caja {round(perim, 3)} (incluye la parte exterior) — R70.6: el LF del type interior = "
                             f"caras de la parte interior ({round(inter, 3)}) o declarar type_lf_basis")


def _r70_7(walls):
    """R70.7 (v70): un storefront / curtain wall desde el piso (sill 0 o sin sill) no es parte del wall: su vano sale
    del LF del type EXT y el framing sobre el head va como storefront_cripples."""
    for w in walls:
        if str(w.get("storefront_in_lf_reason") or "").strip() or str(w.get("tag") or "").upper() in GG:
            continue                                   # G / G1: la regla 59.7 de generar() da el mensaje propio
        for o in w.get("openings") or []:
            k = str(o.get("kind") or o.get("class") or "").lower()
            if k in ("storefront", "curtain_wall") and float(o.get("sill_ft") or 0) <= 0.01:
                raise ValueError(f"{w['id']} {o.get('ref')}: R70.7: storefront span goes out of the EXT type LF; model "
                                 f"framing above head as storefront_cripples (o storefront_in_lf_reason)")


def _hoja_wall(w):
    b = w.get("band") or {}
    return b.get("sheet") or w.get("sheet") or w.get("plan_sheet")


def _frp(data, fam, filas):
    """v65: FRP = perímetro neto de tile_base de cada room x top_ft + mop sink (59.10: TODAS las doors del cuarto,
    también las de cuartos vecinos que abren hacia él)."""
    fr = data.get("frp")
    if fr is None:
        if not str(data.get("frp_none_reason") or "").strip():
            raise ValueError("frp {top_ft {value, source}, rooms [...], mop_sink} o frp_none_reason obligatorio "
                             "(v65: #14B sin FRP)")
        return
    top = fr.get("top_ft")
    if not isinstance(top, dict) or not str(top.get("source") or "").strip():
        raise ValueError("frp.top_ft {value, source} (A-D/A08.01 '5'-0\" TO TOP OF FRP')")
    tb = {str(t["room"]): t for t in data.get("tile_base") or []}
    for r in fr.get("rooms") or []:
        if str(r) not in tb:
            raise ValueError(f"frp room {r}: sin tile_base (el FRP usa el MISMO perímetro neto, 59.10)")
        t = tb[str(r)]
        if "doors" not in t:
            raise ValueError(f"tile_base {r}: con FRP declarar doors [{{ref, ro_w_ft}}] (59.10: todas, incl. las de "
                             f"cuartos vecinos que abren hacia él; #14A sin door <ref>)")
        net, op_n = _perim_neto(t)
        sf = net * float(top["value"])
        fam[F_FRP] += sf
        filas.append({"familia": F_FRP, "room": r, "source": top["source"],
                      "operacion": f"{op_n} x {top['value']} = {round(sf, 2)} SF"})
    ms = fr.get("mop_sink")
    if ms:
        _src(ms, "frp.mop_sink")
        sf = int(ms["sides"]) * float(ms["width_ft"]) * float(ms["height_ft"])
        fam[F_FRP] += sf
        filas.append({"familia": F_FRP, "ref": "mop sink", "source": ms["source"],
                      "operacion": f"{ms['sides']} x {ms['width_ft']} x {ms['height_ft']} = {round(sf, 2)} SF"})


def _sealant(data, fam, filas):
    """v65: acoustical sealant por detalle (59.12): cada detail con faces declara sealant {bottom_faces, top_faces,
    source}; LF = L x (bottom + top) - Σ R.O. de doors x bottom_faces (55.5). Beads de un detalle de bulkhead /
    head van en sealant_items (no se propagan al tipo). La familia del calificador suma también
    sealant_base_exterior (sealant at base of gypsum, exterior)."""
    det = data.get("details") or {}
    usados = sorted({w.get("detail") for w in data.get("walls") or [] if w.get("faces")})
    if not usados:
        return
    for d in usados:
        sp = (det.get(d) or {}).get("sealant")
        if not isinstance(sp, dict) or not str(sp.get("source") or "").strip():
            raise ValueError(f"details['{d}'].sealant {{bottom_faces, top_faces, source}} obligatorio (0 con source "
                             f"si el detalle no dibuja bead; v65, #14B sin sealant)")
    for w in data.get("walls") or []:
        if not w.get("faces") or w.get("element") == "door_bulkhead":
            continue                                   # bulkhead del office front: sus beads (8, 9/A12.01) van en sealant_items
        sp = det[w["detail"]]["sealant"]
        b, t = int(sp["bottom_faces"]), int(sp["top_faces"])
        if b + t == 0:
            continue
        L = float(w.get("length_printed_ft") or w["length_ft"])
        doors = sum(float(o["ro_w_ft"]) for o in w.get("openings") or [] if o.get("kind", "door") == "door")
        lf = L * (b + t) - doors * b
        fam[F_SEAL] += lf
        SEAL["acoustical"] = SEAL.get("acoustical", 0.0) + lf
        filas.append({"familia": F_SEAL, "wall": w["id"], "source": sp["source"],
                      "operacion": f"{L} x ({b} bottom + {t} top) - doors {round(doors, 3)} x {b} = {round(lf, 2)}"})
    for it in data.get("sealant_items") or []:
        src = _src(it, it.get("ref", "sealant"))
        lf = float(it["lf"]) * int(it.get("faces", 1))
        fam[F_SEAL] += lf
        SEAL["acoustical"] = SEAL.get("acoustical", 0.0) + lf
        filas.append({"familia": F_SEAL, "ref": it["ref"], "source": src,
                      "operacion": f"{it['lf']} x {it.get('faces', 1)} face(s) = {round(lf, 2)}"})
    be = data.get("sealant_base_exterior")
    if be:
        src = _src(be, "sealant_base_exterior")
        fam[F_SEAL] += float(be["lf"])
        SEAL["exterior"] = SEAL.get("exterior", 0.0) + float(be["lf"])
        filas.append({"familia": F_SEAL, "ref": "sealant at base of gypsum (exterior)", "source": src,
                      "operacion": f"{be['lf']} LF (no acústico; la familia del calificador lo suma)"})


def _level5(data, fam, filas):
    for it in data.get("level5_items") or []:
        src = _src(it, it.get("ref", "level 5"))
        sf = float(it["sf"]) if "sf" in it else float(it["l_ft"]) * float(it["h_ft"])
        fam[F_L5] += sf
        filas.append({"familia": F_L5, "ref": it["ref"], "source": src, "operacion": f"{round(sf, 2)} SF"})


def _parapet_runs(par):
    """v66 (#15A/#15B): un straight run = tramos CONTIGUOS de la misma línea (line + from_ft/to_ft), aunque cambie
    la altura del parapet: los posts (6/S5.10) siguen sobre la viga. #15A partió la misma línea en dos runs en el
    cambio de altura y perdió bays; #15B midió a la cara exterior. Se exige length_basis "stud_cl"."""
    por_linea = {}
    for w in par:
        for k in ("line", "from_ft", "to_ft"):
            if w.get(k) is None:
                raise ValueError(f"{w['id']}: parapet sin {k} — el straight run sale de la línea (tramos contiguos de "
                                 f"una línea = un run aunque cambie la altura; v66)")
        if str(w.get("length_basis") or "") != "stud_cl":
            raise ValueError(f"{w['id']}: parapet sin length_basis 'stud_cl' — el largo se mide en el eje del stud "
                             f"(cara exterior menos el offset del detalle del parapet), no en la cara exterior (v66)")
        if abs((float(w["to_ft"]) - float(w["from_ft"])) - float(w["length_ft"])) > 0.05:
            raise ValueError(f"{w['id']}: to_ft - from_ft != length_ft")
        por_linea.setdefault(str(w["line"]), []).append(w)
    grupos = []
    for ln, ws in por_linea.items():
        ws = sorted(ws, key=lambda w: float(w["from_ft"]))
        actual = [ws[0]]
        for w in ws[1:]:
            if float(w["from_ft"]) - float(actual[-1]["to_ft"]) <= 0.1:
                actual.append(w)
            else:
                grupos.append((ln, actual))
                actual = [w]
        grupos.append((ln, actual))
    return grupos


def _parapet_studs(data, fam, filas):
    """59.4 / E3: por straight run, bays = ROUNDUP(L / post); studs por bay = MAX(5, 2 (uno a cada lado del post) +
    ROUNDUP((bay - 0.6) / oc) - 1 intermedios) en runs de 2+ bays; run de UN bay (stub entre posts) = la fórmula sin
    mínimo (v68, cálculo aprobado de la decisión usuario #3; constants.parapet_studs_per_bay_min lo cambia con source); LF = studs x altura ponderada por
    LF del run. v66: run por línea."""
    par = [w for w in data.get("walls") or [] if _es_parapet(w)]
    if not par:
        return
    post = _c(data, "parapet_post_spacing_ft")
    spb_min = _c(data, "parapet_studs_per_bay_min", 5.0)
    for w in par:
        if "zones" in w:
            raise ValueError(f"{w['id']}: parapet sin zones (se cuenta por bay entre posts, 59.4)")
    for ln, ws in _parapet_runs(par):
        g = f"line {ln} [{ws[0]['from_ft']}-{ws[-1]['to_ft']}]"
        L = sum(float(w["length_ft"]) for w in ws)
        h = sum(float(w["length_ft"]) * float(w["height_ft"]) for w in ws) / L
        oc = float(ws[0].get("oc_in", 16)) / 12.0
        nb = max(1, int(math.ceil(L / post - EPS)))
        bay = L / nb
        spb_f = 2 + max(0, int(math.ceil((bay - 0.6) / oc - EPS)) - 1)
        # v68 (E3 exacta, cálculo aprobado 16-oct): el mínimo de 5 vale en los bays que salen de dividir un run por
        # los posts (nb >= 2); un run de UN solo bay (L <= spacing de posts: stub entre posts) usa la fórmula.
        spb = max(int(spb_min), spb_f) if nb >= 2 else spb_f
        lf = nb * spb * h
        fam[F_PAR] += lf
        filas.append({"familia": F_PAR, "run": g, "walls": [w["id"] for w in ws], "pcs": nb * spb,
                      "source": "; ".join(sorted({_src(w, w["id"]) for w in ws})),
                      "operacion": f"L {round(L, 3)} -> ROUNDUP(L/{post}) = {nb} bays de {round(bay, 3)}; "
                                   f"{spb} studs/bay ({'MAX(' + str(int(spb_min)) + ', ' if nb >= 2 else '(1 bay: '}2 + ROUNDUP(({round(bay, 3)}-0.6)/{round(oc, 3)})-1)) = "
                                   f"{nb * spb} x H ponderada {round(h, 4)} = {round(lf, 2)}"})


def _jambs_extra(data, fam, filas):
    """#13A: una abertura que muere ENTRE dos walls (openings_extra) no tiene wall propio en studs_nodos y sus 4 jamb
    studs se perdían en silencio. Con "jamb_wall" (+ "jamb_wall_source") se cargan los 4 jambs (king +
    jack por lado, 53.2) a ESE wall, altura completa x rows, en la familia de su stud.
    v65 (#14A ADV1-3): con head_ft también los cripples sobre el head (FLOOR(R.O./oc) x (H - head) x rows) y el
    bottom + top track sobre el R.O. (el track de los dos walls termina en las jambs; bottom continuo, E10)."""
    walls = {w["id"]: w for w in data.get("walls") or []}
    for o in data.get("openings_extra") or []:
        jw = o.get("jamb_wall")
        if not jw:
            continue
        if jw not in walls:
            raise ValueError(f"{o['ref']}: jamb_wall {jw} no existe")
        _src(o, o["ref"], "jamb_wall_source")
        w = walls[jw]
        if _es_parapet(w):
            raise ValueError(f"{o['ref']}: jamb_wall no puede ser parapet")
        k = next((f for key, f in STUD_FAM if key in str(w["stud_size"]).lower()), None)
        if k is None or k == F_PAR:
            raise ValueError(f"{o['ref']}: stud_size '{w['stud_size']}' sin familia para jambs")
        rows = int(w.get("rows", 1))
        lf = 4 * float(w["height_ft"]) * rows
        fam[k] += lf
        filas.append({"familia": k, "ref": o["ref"], "wall": jw, "source": o["jamb_wall_source"], "pcs": 4 * rows,
                      "operacion": f"4 jambs x {w['height_ft']} x {rows} row(s) = {round(lf, 2)} LF "
                                   f"(abertura entre walls, cargada a {jw})"})
        if o.get("head_ft") is None:
            if str(o.get("kind", "door")) == "door":
                raise ValueError(f"{o['ref']}: door entre walls (jamb_wall) sin head_ft — faltan cripples y track "
                                 f"sobre el R.O. (v65, #14A ADV1-3)")
            continue
        oc = float(w.get("oc_in", 16)) / 12.0
        ro = float(o["ro_w_ft"])
        nc = int(math.floor(ro / oc + EPS))
        clf = nc * max(0.0, float(w["height_ft"]) - float(o["head_ft"])) * rows
        fam[k] += clf
        fam["bottom track (todos)"] += ro * rows
        fam["top / deflection track (todos)"] += ro * rows
        filas.append({"familia": k, "ref": o["ref"] + " cripples+track", "wall": jw, "source": o["jamb_wall_source"],
                      "pcs": nc * rows,
                      "operacion": f"cripples FLOOR({ro}/{round(oc, 3)}) = {nc} x ({w['height_ft']} - {o['head_ft']}) x "
                                   f"{rows} = {round(clf, 2)} LF; bottom + top track {ro} x {rows} c/u (E10)"})


def _kickers(data, fam, filas):
    # v68 (#16B: la transición en `runs` no contaba kickers ni vertical studs: −<n> LF de 3-5/8"): walls Y runs
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        k = w.get("kickers")
        if w.get("element") == "ceiling_transition" and not k:
            raise ValueError(f"{w['id']}: ceiling_transition sin kickers (7/A09.33) — sus studs son kickers + "
                             f"vertical_studs, no pasa por studs_nodos (v65)")
        if not k:
            continue
        if w.get("element") != "ceiling_transition":
            raise ValueError(f"{w['id']}: kickers solo en ceiling_transition (7/A09.33)")
        src = _src(k, f"{w['id']}.kickers")
        vs = w.get("vertical_studs")                  # decisión usuario #7: studs verticales (dashed) a estructura
        if not isinstance(vs, dict):
            raise ValueError(f"{w['id']}: ceiling_transition con kickers sin vertical_studs {{oc_in, height_ft, "
                             f"source}} — los studs verticales a estructura se cuentan además del kicker "
                             f"(decisión usuario #7, 7/A09.33)")
        # v68 (#16A <n> = <n> bordes contra ACT; #16B <n> sumó el borde contra wall): edges [{edge, against,
        # length_ft, source}] obligatorio; solo cuentan los bordes contra otro ceiling; length_ft = su suma.
        eds = w.get("edges")
        if not isinstance(eds, list) or not eds:
            raise ValueError(f"{w['id']}: ceiling_transition sin edges [{{edge, against, length_ft, source}}] "
                             f"(bordes del RCP; solo contra otro ceiling; v68)")
        tot_e = 0.0
        for e in eds:
            _src(e, f"{w['id']}.edges {e.get('edge')}")
            ag = str(e.get("against") or "").lower()
            if ag not in ("act", "gyp", "ceiling", "open"):
                raise ValueError(f"{w['id']}.edges {e.get('edge')}: against '{ag}' — un borde contra wall / "
                                 f"storefront / soffit no es transición (v68)")
            tot_e += float(e["length_ft"])
        if abs(tot_e - float(w["length_ft"])) > 0.05:
            raise ValueError(f"{w['id']}: length_ft {w['length_ft']} != Σ edges contra ceiling {round(tot_e, 3)} (v68)")
        fs = {str(c.get("room")) for c in data.get("ceilings") or [] if c.get("system") == "framed_soffit"}
        if w.get("room") is not None and str(w.get("room")) in fs:
            raise ValueError(f"{w['id']}: transición en el room {w['room']} de un framed_soffit — sus bordes ya son "
                             f"drop_lines (doble conteo; v68)")
        vh = float(vs["height_ft"])
        # v68 (#16A <n> vs #16B <n> en la misma transición): el vertical stud va A ESTRUCTURA = B.O.D. del lugar menos
        # el ceiling de gyp (decisión #7); el escalón entre los dos ceilings no es su alto. bod_ft y ceiling_ft
        # {value, source} obligatorios y height_ft = bod - ceiling.
        bd, cl = vs.get("bod_ft"), vs.get("ceiling_ft")
        if not (isinstance(bd, dict) and isinstance(cl, dict)):
            raise ValueError(f"{w['id']}: vertical_studs sin bod_ft / ceiling_ft {{value, source}} — el stud va a "
                             f"estructura: alto = B.O.D. - ceiling (decisión #7, v68)")
        _src(bd, f"{w['id']}.vertical_studs.bod_ft")
        _src(cl, f"{w['id']}.vertical_studs.ceiling_ft")
        if abs(float(bd["value"]) - float(cl["value"]) - vh) > 0.02:
            raise ValueError(f"{w['id']}: vertical_studs.height_ft {vh} != B.O.D. {bd['value']} - ceiling "
                             f"{cl['value']} (a estructura, no el escalón entre ceilings; v68)")
        if abs(float(w["height_ft"]) - vh) > 0.01:     # v65: #14B height_ft <n> inventado
            raise ValueError(f"{w['id']}: height_ft {w['height_ft']} != vertical_studs.height_ft {vh} — el elemento "
                             f"mide B.O.D. - ceiling (bracing y track salen de aquí; v65, #14B <n>)")
        if k.get("length_ft") is not None and not str(k.get("length_printed_source") or "").strip():
            raise ValueError(f"{w['id']}: kickers.length_ft a mano sin length_printed_source — sin largo impreso el "
                             f"largo = vertical_studs.height_ft / sin(angle_deg) (v65, 53.3)")
        if k.get("length_ft") is not None:
            kl = float(k["length_ft"])
            kop = f"{kl} ({k['length_printed_source']})"
        else:
            ang = float(k.get("angle_deg", 45))
            kl = vh / math.sin(math.radians(ang))
            kop = f"{vh}/sin({ang:g}) = {round(kl, 3)} (53.3, largo no impreso)"
        oc = float(k["oc_in"]) / 12.0
        n = int(math.ceil(float(w["length_ft"]) / oc - EPS)) + 1
        lf = n * kl
        fam[F_36] += lf
        filas.append({"familia": "kickers", "wall": w["id"], "source": src,
                      "operacion": f"ROUNDUP({w['length_ft']}/{round(oc, 3)})+1 = {n} kickers x {kop} = "
                                   f"{round(lf, 2)} LF 3-5/8\""})
        vsrc = _src(vs, f"{w['id']}.vertical_studs")
        voc = float(vs["oc_in"]) / 12.0
        nv = int(math.ceil(float(w["length_ft"]) / voc - EPS)) + 1
        vlf = nv * vh
        fam[F_36] += vlf
        filas.append({"familia": "vertical studs @ transition", "wall": w["id"], "source": vsrc, "pcs": nv,
                      "operacion": f"ROUNDUP({w['length_ft']}/{round(voc, 3)})+1 = {nv} studs x {vh} = "
                                   f"{round(vlf, 2)} LF 3-5/8\" (decisión usuario #7; sin studs_nodos, v65)"})


def _column_wraps(data, fam, filas):
    """v65: column_wrap = studs por face (cada face lleva sus studs de esquina): Σ (ROUNDUP(face/oc) + 1), o los
    studs_drawn {value, source} que dibuja el detalle. 5/A09.25: 4 faces x <n> -> <n> studs (A y B <n>)."""
    for w in data.get("walls") or []:
        if w.get("element") != "column_wrap" and not (w.get("element") == "pier" and w.get("parts")):
            continue                                  # v68: pier con parts = mismo trato que column_wrap (#16A)
        k = next((f for key, f in STUD_FAM if key in str(w.get("stud_size", "")).lower()), None)
        if (k is None or k == F_PAR) and not w.get("parts"):
            raise ValueError(f"{w['id']}: column_wrap stud_size '{w.get('stud_size')}' sin familia")
        oc = float(w.get("oc_in", 16)) / 12.0
        sd = w.get("studs_drawn")
        if w.get("parts"):                            # v66: detalle con dos sistemas (ej. L 3-5/8" + L 6" CFMF)
            if sd is not None or w.get("faces_ft"):
                raise ValueError(f"{w['id']}: parts excluye studs_drawn / faces_ft (cada parte trae los suyos)")
            for i, pt in enumerate(w["parts"]):
                kp = next((f for key, f in STUD_FAM if key in str(pt.get("stud_size", "")).lower()), None)
                psd = pt.get("studs_drawn")
                if kp is None or kp == F_PAR:
                    raise ValueError(f"{w['id']}.parts[{i}]: stud_size '{pt.get('stud_size')}' sin familia")
                if not isinstance(psd, dict) or not str(psd.get("source") or "").strip():
                    raise ValueError(f"{w['id']}.parts[{i}]: studs_drawn {{value, source}} (studs que dibuja el "
                                     f"detalle para esa parte)")
                n = int(psd["value"])
                hp = float(pt.get("height_ft", w["height_ft"]))
                lf = n * hp * int(w.get("rows", 1))
                fam[kp] += lf
                filas.append({"familia": kp, "ref": f"{w['id']}.{pt['stud_size']}", "source": psd["source"],
                              "pcs": n * int(w.get("rows", 1)),
                              "operacion": f"{w['element']} parte {pt['stud_size']}: {n} studs dibujados x {hp} x "
                                           f"{w.get('rows', 1)} = {round(lf, 2)} LF (v66 parts)"})
            continue
        if sd is not None:
            if not isinstance(sd, dict) or not str(sd.get("source") or "").strip():
                raise ValueError(f"{w['id']}: studs_drawn {{value, source}}")
            n = int(sd["value"])
            op = f"{n} studs dibujados ({sd['source']})"
        elif w.get("faces_ft"):
            fs = [float(x) for x in w["faces_ft"]]
            fc = w.get("fos_chain")                   # v67: face = cadena FOS impresa COMPLETA (todos los eslabones)
            if fc is not None:
                if not isinstance(fc, dict) or not str(fc.get("source") or "").strip():
                    raise ValueError(f"{w['id']}: fos_chain {{value: [eslabones ft], source}}")
                cad = sum(float(x) for x in fc["value"])
                malas = [f_ for f_ in fs if abs(f_ - cad) > 0.02]
                if malas:
                    raise ValueError(f"{w['id']}: faces_ft {malas} != Σ fos_chain {round(cad, 3)} ({fc['source']}): "
                                     f"la face es la cadena FOS impresa completa, no su primer eslabón (v67)")
            if abs(sum(fs) - float(w["length_ft"])) > 0.05:
                raise ValueError(f"{w['id']}: Σ faces_ft {round(sum(fs), 3)} != length_ft {w['length_ft']}")
            n = sum(int(math.ceil(f_ / oc - EPS)) + 1 for f_ in fs)
            op = f"Σ (ROUNDUP(face/{round(oc, 3)})+1) por face {fs} = {n} studs"
        else:
            raise ValueError(f"{w['id']}: column_wrap sin faces_ft ni studs_drawn — los studs van por face (cada "
                             f"esquina lleva stud en las dos faces), no como wall recto (v65; 5/A09.25 8 por wrap)")
        lf = n * float(w["height_ft"]) * int(w.get("rows", 1))
        fam[k] += lf
        filas.append({"familia": k, "ref": w["id"], "source": _src(w, w["id"]), "pcs": n * int(w.get("rows", 1)),
                      "operacion": f"column_wrap {op} x {w['height_ft']} x {w.get('rows', 1)} = {round(lf, 2)} LF"})


HANGERS = []


def _ballistic_jogs(data, fam, filas):
    """v66 (E5, #15A): jog / retorno del contorno ballistic sin wall propio. #15A los modeló como walls A1K de
    <n> ft (studs y dos faces de 5/8" fantasma). Cada jog: ballistic L x min(panel_to, H), 3/8" L x (H - panel_to)
    y 5/8" L x H x faces_5_8 (la face que el detalle cubre; 0 si ya está en la face del wall vecino)."""
    det = data.get("details") or {}
    for j in data.get("ballistic_jogs") or []:
        ref = j.get("ref", "jog")
        src = _src(j, f"ballistic_jogs {ref}")
        d = det.get(j.get("detail"))
        if not d or not d.get("k_panel"):
            raise ValueError(f"ballistic_jogs {ref}: detail con k_panel (panel_to_ft) obligatorio")
        if j.get("faces_5_8") not in (0, 1, 2):
            raise ValueError(f"ballistic_jogs {ref}: faces_5_8 0|1|2 obligatorio (cuántas faces de 5/8\" agrega el jog)")
        L, H = float(j["length_ft"]), float(j["height_ft"])
        pt = float(d["k_panel"]["panel_to_ft"])
        bal, g38 = L * min(pt, H), L * max(0.0, H - pt)
        g58 = L * H * int(j["faces_5_8"]) * int(d.get("layers_per_face", 1))
        fam["ballistic panel"] += bal
        fam["3/8\" gyp board"] += g38
        fam[F_GYP] += g58
        filas.append({"familia": "ballistic jog", "ref": ref, "source": src,
                      "operacion": f"ballistic {L} x {min(pt, H)} = {round(bal, 2)}; 3/8 {L} x {round(max(0, H - pt), 3)}"
                                   f" = {round(g38, 2)}; 5/8 {L} x {H} x {j['faces_5_8']} = {round(g58, 2)} (sin studs, v66)"})


def _num_txt(x, ok):
    """Número corto que reproduce el resultado (ok(valor) True); si redondear lo cambia, más decimales."""
    for nd in (3, 4, 6):
        if ok(round(x, nd)):
            return f"{round(x, nd):g}"
    return repr(x)


def _op_joists(run, oc_ft, n, largo, lf):
    """v70 (#18A): "ROUNDUP(<run_ft>/<oc_ft>)+1 = <n> joists x <joist_len_ft> = <LF>" con el RUN (no el largo del
    joist) y números que, evaluados, dan n."""
    oc_in = oc_ft * 12.0
    if abs(round(oc_ft, 3) - oc_ft) < 1e-9:
        oc_txt, ocv = f"{round(oc_ft, 3):g}", round(oc_ft, 3)
    else:
        oc_txt, ocv = f"({oc_in:g}/12)", oc_in / 12.0
    run_txt = _num_txt(run, lambda r: math.ceil(r / ocv) + 1 == n)
    return f"ROUNDUP({run_txt}/{oc_txt})+1 = {n} joists x {round(largo, 3)} = {round(lf, 2)}"


def _ceilings(data, fam, filas):
    HANGERS.clear()
    cs = data.get("ceilings") or []
    if not cs:
        return
    f_oc = _c(data, "furring_oc_in", 16.0) / 12.0
    c_oc = _c(data, "carrying_oc_in", 48.0) / 12.0
    h_oc = _c(data, "hanger_oc_in", 48.0) / 12.0
    for c in cs:
        src = _src(c, c["room"])
        sysm = c.get("system")
        if sysm not in SUSP + JOIST_ONLY:
            raise ValueError(f"{c['room']}: system {' | '.join(SUSP + JOIST_ONLY)}")
        if "soffit" in str(c["room"]).lower() and sysm in SUSP:
            raise ValueError(f"{c['room']}: un soffit es framed (10/A09.33, 7/A09.26) -> framed_soffit o "
                             f"canopy_joist, sin furring/carrying/hangers (#12A furring, #12B carrying)")
        if sysm == "stud_joist" and not str(c.get("joist_source") or "").strip():
            raise ValueError(f"{c['room']}: stud_joist sin joist_source — un ceiling suspended (hangers + carrying) "
                             f"del RCP es furring salvo que un detalle dibuje joists (decisión usuario #14)")
        span, run = _ceil_dims(data, c)               # span: largo del carrying; run: atravesado por el carrying
        area = float(c["area_sf"])
        poligono = area < span * run * 0.98
        lc = area / run if poligono else span         # cuerda media del carrying (polígono)
        lf_ = area / span if poligono else run        # cuerda media del furring / joist
        n_f = int(math.ceil(span / f_oc - EPS)) + 1
        cuenta = span                                 # v70: dimensión que cuenta joists (el RUN), para la operación
        jd = c.get("joist_dir")
        if jd is not None:                            # 13B: joists perpendiculares al muro (canopy N/S)
            if sysm not in JOIST_ONLY:
                raise ValueError(f"{c['room']}: joist_dir solo en {JOIST_ONLY}")
            if not isinstance(jd, dict) or str(jd.get("value", "")).upper() not in ("N-S", "E-W") \
                    or not str(jd.get("source") or "").strip():
                raise ValueError(f"{c['room']}: joist_dir {{value: N-S|E-W, source}}")
            ns_, ew_ = float(c["ns_ft"]), float(c["ew_ft"])
            cnt, lf_ = (ew_, ns_) if str(jd["value"]).upper() == "N-S" else (ns_, ew_)
            if poligono:
                lf_ = area / cnt
            n_f = int(math.ceil(cnt / f_oc - EPS)) + 1
            cuenta = cnt
        if sysm in JOIST_ONLY:
            joist = n_f * lf_
            fam[F_36] += joist
            if sysm == "canopy_joist":                 # #12A: soffit exterior, sheathing ext grade FRT plywood
                _ply(fam, "frt_5_8_ext", area, "canopy_soffit")
                bd = f"5/8\" exterior grade FRT plywood {area} SF"
            else:
                fam[F_GYP] += area
                bd = f"board {area} SF"
            filas.append({"familia": "ceilings", "room": c["room"], "source": src,
                          "operacion": f"{sysm}: {_op_joists(cuenta, f_oc, n_f, lf_, joist)} LF 3-5/8\" joists; "
                                       f"sin carrying ni hangers; {bd}"})
            continue
        dr = c.get("hanger_drop_ft")
        if not isinstance(dr, dict) or "value" not in dr or not str(dr.get("source") or "").strip():
            raise ValueError(f"{c['room']}: hanger_drop_ft {{value, source}} obligatorio (B.O.D. - ceiling height; "
                             f"hanger wire en PCS con la altura de cada hanger, decisión usuario #4)")
        drop = float(dr["value"])
        n_c = int(math.ceil((run - 1.0) / c_oc - EPS)) + 1
        carry = n_c * lc
        n_h = int(math.ceil((lc - 1.0) / h_oc - EPS)) + 1
        hang = n_c * n_h
        fam["carrying channel"] += carry
        fam["hanger wire"] += hang * drop             # renglón DERIVADO: PCS x altura (decisión usuario #4)
        HANGERS.append({"room": c["room"], "pcs": hang, "altura_ft": drop, "altura_source": dr["source"],
                        "lf": round(hang * drop, 2)})
        if sysm == "furring":
            furr = n_f * lf_
            fam["furring channel"] += furr
            op = f"furring ROUNDUP({round(span, 3)}/{round(f_oc, 3)})+1 = {n_f} x {round(lf_, 3)} = {round(furr, 2)}"
        else:
            joist = n_f * lf_
            fam[F_36] += joist
            op = f"3-5/8\" ceiling joists ({src}) {n_f} x {round(lf_, 3)} = {round(joist, 2)} (no furring)"
        fam[F_GYP] += area
        filas.append({"familia": "ceilings", "room": c["room"], "source": src,
                      "operacion": f"{op}; carrying ROUNDUP(({round(run, 3)}-1)/{round(c_oc, 3)})+1 = {n_c} x "
                                   f"{round(lc, 3)} = {round(carry, 2)}{' (polígono: cuerda media área/ancho)' if poligono else ''}; "
                                   f"hangers {n_c} x (ROUNDUP(({round(lc, 3)}-1)/{round(h_oc, 3)})+1 = {n_h}) = {hang} x "
                                   f"drop {drop} ({dr['source']}) = {round(hang * drop, 2)} LF; board {area} SF"})


def _trim(data, fam, filas):
    """metal trim con número (nunca PENDING): trim_items + jamb returns (53.1: corner bead + casing bead por
    borde) + ceiling transitions (7/A09.33: transition_trim_per_lf por LF)."""
    if "trim_items" not in data:
        raise ValueError("trim_items ausente: metal trim (corner bead, casing, shadow molding) debe salir de "
                         "canon.py con número (v62); lista vacía solo con trim_none_reason")
    if not data["trim_items"] and not str(data.get("trim_none_reason") or "").strip():
        raise ValueError("trim_items vacío sin trim_none_reason")
    for t in data["trim_items"]:
        src = _src(t, t.get("ref", "trim"))
        if t.get("kind") not in TRIM_KINDS:
            raise ValueError(f"{t.get('ref')}: kind de trim {sorted(TRIM_KINDS)}")
        lf = float(t["lf"]) * int(t.get("qty", 1))
        fam[F_TRIM] += lf
        filas.append({"familia": F_TRIM, "ref": t["ref"], "kind": t["kind"], "source": src,
                      "operacion": f"{t['lf']} x {t.get('qty', 1)} = {round(lf, 2)}"})
    jr = 0.0
    det = []
    for w in data.get("walls") or []:
        for o in w.get("openings") or []:
            if o.get("jamb_return"):
                _src(o, o["ref"], "jamb_return_source")
                e = accesorios._edge(o)                  # v67: mismos bordes que gypsum board jamb return
                jr += e
                det.append(f"{o['ref']} {round(e, 2)}")
    for o in data.get("openings_extra") or []:
        if o.get("jamb_return"):
            _src(o, o["ref"], "jamb_return_source")
            e = accesorios._edge(o)                      # v67: mismos bordes que gypsum board jamb return
            jr += e
            det.append(f"{o['ref']} {round(e, 2)}")
    if jr > EPS:
        fam[F_TRIM] += 2 * jr
        filas.append({"familia": F_TRIM, "ref": "jamb returns", "source": "53.1",
                      "operacion": f"bordes {round(jr, 2)} LF x 2 (corner bead + casing bead) = {round(2 * jr, 2)} "
                                   f"[{'; '.join(det)}]"})
    tr = [w for w in data.get("walls") or [] if w.get("element") == "ceiling_transition"] + \
         [r for r in data.get("runs") or [] if r.get("element") == "ceiling_transition"]
    if tr:
        k = _c(data, "transition_trim_per_lf")
        L = sum(float(x["length_ft"]) for x in tr)
        fam[F_TRIM] += k * L
        filas.append({"familia": F_TRIM, "ref": "ceiling transitions",
                      "source": data["constants"]["transition_trim_per_lf"]["source"],
                      "operacion": f"{round(L, 2)} LF x {k} (corner bead + shadow molding) = {round(k * L, 2)}"})


CANOPY_ELEMS = ("canopy_soffit", "fascia_box")


def _canopy_facades(data, fac, can):
    """v63: cada canopy_soffit / fascia_box dice a qué facade pertenece; esa facade lleva banda de glass mat."""
    elems = [w for w in (data.get("walls") or []) + (data.get("runs") or []) if w.get("element") in CANOPY_ELEMS]
    con_banda = {c.get("facade") for c in can}
    cs = [e for e in elems if e["element"] == "canopy_soffit"]
    if cs:                                         # #13A 1 línea / #13B 2 (default): +<n> LF entre agentes
        n = _c(data, "canopy_soffit_track_lines", -1)
        if n == -1:
            raise ValueError("constants.canopy_soffit_track_lines {value 2, source} obligatoria si hay canopy_soffit "
                             "(decisión usuario #13: track en los dos extremos de los joists)")
        if int(n) != 2:
            raise ValueError(f"constants.canopy_soffit_track_lines {int(n)}: el canopy soffit lleva track en LOS DOS "
                             f"extremos de los joists (fascia y wall) -> 2 (decisión usuario #13)")
        for e in cs:
            if int(e.get("track_lines", 2)) != int(n):
                raise ValueError(f"{e['id']}: track_lines {e.get('track_lines', 2)} != "
                                 f"constants.canopy_soffit_track_lines {int(n)}")
    for e in elems:
        f = e.get("facade")
        if f is None:
            raise ValueError(f"{e['id']}: {e['element']} sin facade (v63: la banda de glass mat sale de aquí, "
                             f"#13A fachada oeste sin banda)")
        if f not in fac:
            raise ValueError(f"{e['id']}: facade '{f}' no declarada en facades")
        if not fac[f].get("has_canopy") or f not in con_banda:
            raise ValueError(f"facade {f}: tiene {e['element']} {e['id']} pero has_canopy false o sin canopies[] "
                             f"— glass mat detrás de la canopy (3/, 7/A09.26 'GLASS-MAT'; 15/A09.27 misma línea)")


def _fascia_sheathing(data, fam, filas):
    for s_ in data.get("plywood_strips") or []:
        if "fascia" in str(s_.get("ref", "")).lower():
            raise ValueError(f"plywood_strip '{s_['ref']}': el sheathing de fascia_box lo genera canon.py (v63)")
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        if w.get("element") != "fascia_box":
            continue
        hs = str(w.get("height_source") or "").strip()
        if not hs:
            raise ValueError(f"{w['id']}: fascia_box sin height_source (T/STUD - B/STUD de la fascia, 7/A09.26)")
        sf = float(w["length_ft"]) * float(w["height_ft"])
        _ply(fam, "frt_5_8_ext", sf, "canopy_soffit")
        filas.append({"familia": "FRT plywood (SF)", "ref": w["id"], "source": hs, "material": "frt_5_8_ext",
                      "operacion": f"fascia_box sheathing {w['length_ft']} x {w['height_ft']} = {round(sf, 2)} SF "
                                   f"(5/8\" ext. grade FRT plywood, 7/A09.26)"})


def _perim_neto(t):
    """v68 (#16A 'neto' sin una door; #16B 'bruto' sin descontar): perimeter_basis gross|net obligatorio;
    con gross se descuentan TODAS las doors declaradas (59.10)."""
    bas = t.get("perimeter_basis")
    if bas not in ("gross", "net"):
        raise ValueError(f"tile_base {t.get('room')}: perimeter_basis gross|net obligatorio (v68)")
    p_ = float(t["perimeter_ft"])
    dd = sum(float(d["ro_w_ft"]) for d in t.get("doors") or [])
    if bas == "net":
        # v68 (#16A declaró "net" el bruto impreso): net exige gross_ft {value, source} y net = gross - doors
        g = t.get("gross_ft")
        if not isinstance(g, dict) or not str(g.get("source") or "").strip():
            raise ValueError(f"tile_base {t.get('room')}: perimeter_basis net sin gross_ft {{value, source}} (v68)")
        if abs(float(g["value"]) - dd - p_) > 0.05:
            raise ValueError(f"tile_base {t.get('room')}: net {p_} != gross {g['value']} - doors {round(dd, 3)} (v68)")
        return p_, f"{p_} (net = {g['value']} - doors {round(dd, 3)})"
    return p_ - dd, f"({p_} - doors {round(dd, 3)})"


def _tile_base(data, fam, filas):
    tb = data.get("tile_base")
    if tb is None:
        if not str(data.get("tile_base_none_reason") or "").strip():
            raise ValueError("tile_base [{room, perimeter_ft, height_ft {value, source}, source}] o "
                             "tile_base_none_reason obligatorio (cement board 58.7; #13A FALTA)")
        return
    for t in tb:
        src = _src(t, f"tile_base {t.get('room')}")
        h = t.get("height_ft")
        if not isinstance(h, dict) or not str(h.get("source") or "").strip():
            raise ValueError(f"tile_base {t.get('room')}: height_ft {{value, source}} (CT cove base)")
        net, op_n = _perim_neto(t)
        sf = net * float(h["value"])
        fam["cement board"] += sf
        filas.append({"familia": "cement board", "room": t["room"], "source": src,
                      "operacion": f"{op_n} x {h['value']} = {round(sf, 2)} SF ({h['source']})"})


def _exterior(data, fam, filas):
    fac = {f["id"]: f for f in data.get("facades") or []}
    can = data.get("canopies") or []
    _canopy_facades(data, fac, can)
    if not fac and not can:
        return
    band_h = 0.0
    if can:
        bd = data.get("band") or {}
        ts, bs = bd.get("t_stud_ft"), bd.get("b_stud_ft")
        if not all(isinstance(x, dict) and str(x.get("source") or "").strip() for x in (ts, bs)):
            raise ValueError("band.t_stud_ft y band.b_stud_ft {value, source} obligatorios si hay canopies: el glass "
                             "mat va en la cara del stud, altura = T/STUD - B/STUD del detalle de la banda (7/A09.26), "
                             "no T/CANOPY - B/CANOPY de la elevación (v65)")
        band_h = float(ts["value"]) - float(bs["value"])
        bh = bd.get("height_ft")
        if isinstance(bh, dict) and abs(float(bh["value"]) - band_h) > 0.01:
            raise ValueError(f"band.height_ft {bh['value']} != T/STUD - B/STUD {round(band_h, 3)}")
    band_por_fac = {k: 0.0 for k in fac}
    for c in can:
        if c.get("facade") not in fac:
            raise ValueError(f"canopy {c.get('id')}: facade '{c.get('facade')}' no declarada")
        _src(c, f"canopy {c.get('id')}")
        band_por_fac[c["facade"]] += float(c["band_lf"])
    par_fac = {}
    for w in data.get("walls") or []:
        if _es_parapet(w) and fac:
            if w.get("facade") not in fac:
                raise ValueError(f"{w['id']}: parapet sin facade declarada (E25: la nailbase de esa facade sube a "
                                 f"T/STUD del parapet)")
            par_fac.setdefault(w["facade"], []).append(w["id"])
    caras_par = {s_.get("parapet_face_of") for s_ in data.get("plywood_strips") or []}
    for k, ids in par_fac.items():
        f = fac[k]
        if k in caras_par:
            continue
        pt, nt = f.get("parapet_t_stud_ft"), f.get("nailbase_top_ft")
        if not all(isinstance(x, dict) and str(x.get("source") or "").strip() for x in (pt, nt)):
            raise ValueError(f"facade {k}: tiene parapet ({ids}) — declarar parapet_t_stud_ft y nailbase_top_ft "
                             f"{{value, source}} (E25: cada capa del sheathing se sigue en la sección hasta su remate) "
                             f"o un plywood_strip parapet_face_of '{k}'")
        nb_ = f.get("nailbase_bottom_ft")
        if not isinstance(nb_, dict) or not str(nb_.get("source") or "").strip():
            raise ValueError(f"facade {k}: nailbase_bottom_ft {{value, source}} (T/BASE del detalle de base) obligatorio "
                             f"con nailbase_top_ft")
        if abs(float(f["height_nailbase_ft"]) - (float(nt["value"]) - float(nb_["value"]))) > 0.02:
            raise ValueError(f"facade {k}: height_nailbase_ft {f['height_nailbase_ft']} != nailbase_top_ft - "
                             f"nailbase_bottom_ft {round(float(nt['value']) - float(nb_['value']), 3)}")
        if float(nt["value"]) < float(pt["value"]) - 0.02:
            raise ValueError(f"facade {k}: nailbase_top_ft {nt['value']} < T/STUD del parapet {pt['value']} — la "
                             f"nailbase sigue en la cara exterior del parapet hasta el coping (E25, #15B)")
    for k, f in fac.items():
        src = _src(f, f"facade {k}")
        if f.get("has_canopy") and band_por_fac[k] <= EPS:
            raise ValueError(f"facade {k}: has_canopy pero ninguna canopy le declara banda (59.2)")
        base = float(f["base_strip_lf"]) * float(f.get("base_h_ft", 0.5))
        band = band_por_fac[k] * band_h
        nail = float(f["solid_lf"]) * float(f["height_nailbase_ft"]) - float(f.get("openings_sf", 0)) - band
        fam["5/8\" glass mat sheathing"] += base + band
        _ply(fam, "nailbase_5_8_polyiso", nail, "nailbase")
        filas.append({"familia": "exterior", "facade": k, "source": src,
                      "operacion": f"glass mat base {round(base, 2)} + banda {band_por_fac[k]} x {band_h} = "
                                   f"{round(band, 2)}; nailbase {f['solid_lf']} x {f['height_nailbase_ft']} - "
                                   f"{f.get('openings_sf', 0)} - banda {round(band, 2)} = {round(nail, 2)}"})


def _parapets_blocking(data, fam, filas, avisos):
    bay = _c(data, "stud_bay_in", 14.375)
    for p in data.get("parapets") or []:
        src = _src(p, p["id"])
        sh = float(p["lf"]) * float(p["roofside_h_ft"])
        pb = p.get("plies_blocking", 0)
        nply = int(pb["value"]) if isinstance(pb, dict) else int(pb)
        bl = float(p["lf"]) * nply
        fam["5/8\" EXTERIOR gyp sheathing"] += sh
        fam["FRT blocking"] += bl
        filas.append({"familia": "parapet", "id": p["id"], "source": src,
                      "operacion": f"ext gyp {p['lf']} x {p['roofside_h_ft']} = {round(sh, 2)}; FRT blocking "
                                   f"{p['lf']} x {nply} plies = {round(bl, 2)}"})
    sl = data.get("constants", {}).get("sheet_len_ft")
    if sl is not None:
        L_hoja = _c(data, "sheet_len_ft")
        edge = 0.0
        for w in data.get("walls") or []:
            hi = [f for f in w.get("faces") or [] if float(f["height_ft"]) > L_hoja + EPS]
            if hi:
                rows = int(w.get("rows", 1))
                n = min(len(hi), rows) if rows > 1 else 1
                edge += float(w["length_ft"]) * n
        fam["metal stud blocking (362CR / STUD BLOCKING)"] += edge
        BLK_ORIGEN["edge"] = BLK_ORIGEN.get("edge", 0.0) + edge
        filas.append({"familia": "blocking edge", "source": sl["source"],
                      "operacion": f"sum L x stud rows con face > {L_hoja} ft = {round(edge, 2)} (por stud row, "
                                   f"no por face)"})
    for it in data.get("blocking_items") or []:
        src = _src(it, it["ref"])
        mat = it.get("material")
        lab = str(it.get("label") or "")
        if mat == "metal" and it.get("width_in") is not None and float(it["width_in"]) <= bay + EPS and not lab:
            avisos.append(f"{it['ref']}: {it['width_in']}\" <= stud bay {bay}\" sin rótulo -> sin blocking "
                          f"(anclaje a stud)")
            continue
        if mat == "FRT" and not RX_MADERA.search(lab):
            raise ValueError(f"{it['ref']}: FRT blocking solo donde el detalle lo rotula (label FRT / FRTW / 2X / WOOD / "
                             f"PLYWOOD) — 'PROVIDE BLOCKING' a secas = metal (58.6, v68)")
        k = "FRT blocking" if mat == "FRT" else "metal stud blocking (362CR / STUD BLOCKING)"
        fam[k] += float(it["lf"])
        if mat != "FRT":
            BLK_ORIGEN["items"] = BLK_ORIGEN.get("items", 0.0) + float(it["lf"])
        filas.append({"familia": k, "ref": it["ref"], "source": src, "operacion": f"{it['lf']} LF"})
    for s in data.get("plywood_strips") or []:
        src = _src(s, s["ref"])
        mat = _strip_material(s)
        sf = float(s["lf"]) * float(s["width_ft"])
        _ply(fam, mat, sf, _uso_strip(s))
        filas.append({"familia": "FRT plywood (SF)", "ref": s["ref"], "source": src, "material": mat,
                      "operacion": f"strip {s['lf']} x {s['width_ft']} = {round(sf, 2)} SF (no es blocking ni sill)"})


FAMS = ["2-1/2\" stud", "6\" stud (todos los gauges)", F_36, "1-5/8\" stud", F_PAR,
        "bottom track (todos)", "top / deflection track (todos)", "track de ceilings / soffits",
        "bracing C.R. channel", "purlin (track to deck)", "header / box beam", "sill track",
        "furring channel", "carrying channel", "hanger wire", F_GYP,
        "5/8\" gyp MOISTURE RESISTANT", "ballistic panel", "3/8\" gyp board", "5/8\" glass mat sheathing",
        "5/8\" EXTERIOR gyp sheathing", "FRT plywood (SF)", "FRT blocking",
        "metal stud blocking (362CR / STUD BLOCKING)", F_TRIM, "cement board", F_FRP, F_SEAL, F_L5]
# familias que DEBEN salir de canon.py con número (PROTOCOLO_v62 §6); framed openings MEP sale de
# framed_openings.py y se agrega con --fo
OBLIGATORIAS = [f for f in FAMS if f not in ("2-1/2\" stud", F_L5)]
STUD_FAM = (("parapet", F_PAR), ("2-1/2\"", "2-1/2\" stud"), ("6\"", "6\" stud (todos los gauges)"),
            ("3-5/8\"", F_36), ("1-5/8\"", "1-5/8\" stud"))
BOARD_FAM = {"5/8 regular": F_GYP, "5/8 MR": "5/8\" gyp MOISTURE RESISTANT",
             "ballistic panel": "ballistic panel", "3/8 gyp": "3/8\" gyp board"}


def _fo(data, fo):
    """fo_in de framed_openings (access panels, penetraciones en walls): argumento, dict en el canon o ruta."""
    if fo is not None:
        return fo
    x = data.get("framed_openings_in")
    if isinstance(x, str):
        return json.load(open(x))
    return x


def _materiales(fam, hp):
    """v68: renglones de COMPRA por material (nombre del Excel en inglés, unidad, NET). La familia del calificador
    sigue sumando todo; plantilla_excel arma un renglón por material con su unidad de compra."""
    out = []
    for k, nom in PLY_NAMES.items():
        if PLY.get(k, 0.0) > EPS:
            out.append({"material": nom, "family": F_PLY, "key": k, "unit": "SF", "net": round(PLY[k], 2)})
    tot = sum(PLY.values())
    if abs(tot - fam[F_PLY]) > 0.05:
        raise ValueError(f"FRT plywood: Σ por material {round(tot, 2)} != familia {round(fam[F_PLY], 2)}")
    if SEAL.get("acoustical", 0.0) > EPS:
        out.append({"material": "Acoustical sealant", "family": F_SEAL, "key": "acoustical", "unit": "LF",
                    "net": round(SEAL["acoustical"], 2)})
    if SEAL.get("exterior", 0.0) > EPS:
        out.append({"material": "Sealant at base of gypsum (exterior, not acoustical)", "family": F_SEAL,
                    "key": "exterior", "unit": "LF", "net": round(SEAL["exterior"], 2)})
    if hp["total_pcs"]:
        out.append({"material": "Hanger wire 12 ga", "family": "hanger wire", "key": "hanger_wire", "unit": "LF",
                    "net": hp["lf_derivado"], "pcs": hp["total_pcs"],
                    "operation": "LF = Σ PCS x hanger height per room (user decision #4)"})
    return out


def calcular(data, outdir=None, fo=None):
    av70 = []
    _v70_checks(data, av70)
    inv = None
    if (data.get("constants") or {}).get("plan_scale_pt_per_ft") is not None:
        inv = inventario.verificar(data)              # v63: inventario cerrado contra la planta
    _v65_checks(data)
    _v68_checks(data)
    PLY.clear()
    PLY_USO.clear()
    BLK_ORIGEN.clear()
    SEAL.clear()
    studs_in, board_in, corr_in, hdr_in, avisos = generar(data)
    avisos += av70
    for r in (data.get("walls") or []) + (data.get("runs") or []):    # v67: E13 sin L x 2 encubierto
        wl = r.get("wall_line_ft")
        if r.get("element") == "canopy_soffit" and isinstance(wl, dict) and \
                abs(float(wl.get("value", 0)) - float(r["length_ft"])) < 0.01:
            avisos.append(f"{r['id']}: canopy_soffit wall_line_ft = length_ft ({wl.get('source')}): en esquinas la "
                          f"línea del wall no mide lo mismo que la fascia; medirla por separado (E13) o RFI")
    if inv:
        avisos += inv["avisos"]
    else:
        avisos.append("SIN INVENTARIO: falta constants.plan_scale_pt_per_ft + walls[].band (v63, inventario.py)")
    fam = {k: 0.0 for k in FAMS}
    filas = []
    st = studs_nodos.contar(studs_in) if studs_in["walls"] else {"total_lf_por_stud": {}}
    for size, lf in st["total_lf_por_stud"].items():
        k = next((f for key, f in STUD_FAM if key in size.lower()), None)
        if k is None:
            raise ValueError(f"stud_size '{size}' sin familia")
        if k == F_PAR:
            raise ValueError(f"stud_size '{size}' parapet fuera de element parapet (se cuenta por bay, 59.4)")
        fam[k] += lf
    _parapet_studs(data, fam, filas)
    bo = board_caras.calcular(board_in) if board_in["walls"] else {"totales_sf": {}, "avisos": []}
    for b, sf in bo["totales_sf"].items():
        if b not in BOARD_FAM:
            raise ValueError(f"board '{b}' sin familia (usar {sorted(BOARD_FAM)})")
        fam[BOARD_FAM[b]] += sf
    avisos += bo.get("avisos", [])
    _ballistic_jogs(data, fam, filas)
    co = corridas.calcular(corr_in)
    for k, v in co["totales_lf"].items():
        fam[k] += v
    for r in (co.get("rfi"), co.get("rfi_doors")):
        if r:
            avisos.append(r)
    hpp = {}
    if hdr_in:
        he = headers.calcular(hdr_in)
        hpp = he.get("por_pieza", {})
        fam["header / box beam"] += he["totales_lf"]["header"]
        fam["sill track"] += he["totales_lf"]["sill track"]
        avisos += he.get("avisos", [])
    _jambs_extra(data, fam, filas)
    _kickers(data, fam, filas)
    _column_wraps(data, fam, filas)
    _ceilings(data, fam, filas)
    _exterior(data, fam, filas)
    _parapets_blocking(data, fam, filas, avisos)
    _trim(data, fam, filas)
    _fascia_sheathing(data, fam, filas)
    _tile_base(data, fam, filas)
    _frp(data, fam, filas)
    _sealant(data, fam, filas)
    # v67: Level 5 lo da accesorios.level5() (base descontada, level5_tags); _level5 queda por compatibilidad
    avisos.append("batt insulation: EXCLUDED (criterio del usuario 'no insulation')")
    out = {"familias": {k: round(v, 2) for k, v in fam.items()}, "filas": filas, "avisos": avisos,
           "obligatorias": OBLIGATORIAS, "header_por_pieza": hpp,
           "hanger_pcs": {"total_pcs": sum(h["pcs"] for h in HANGERS), "por_room": list(HANGERS),
                          "lf_derivado": round(sum(h["pcs"] * h["altura_ft"] for h in HANGERS), 2)}}
    out["materiales"] = _materiales(fam, out["hanger_pcs"])
    # v68 (contrato con plantilla_excel): FRT plywood por material y sealant exterior aparte del acoustical
    # v73 (R73.3): por material, espesor Y uso, con el nombre de renglón de la plantilla del estimador
    out["frt_plywood_by_material"] = {k: round(v, 2) for k, v in PLY_USO.items() if v > EPS}
    out["track_by_element"] = track_by_element(data, co, fam)
    # v73 (R73.3): contexto para los nombres de la plantilla y metal blocking por origen (edge vs notas)
    out["metal_blocking_by_origin"] = {k: round(v, 2) for k, v in BLK_ORIGEN.items() if v > EPS}
    th = ""
    for d_ in (data.get("details") or {}).values():
        if isinstance(d_, dict) and isinstance(d_.get("k_panel"), dict):
            m_ = re.search(r'(\d+/\d+)"', str(d_["k_panel"].get("panel") or ""))
            th = th or (m_.group(1) + '"' if m_ else "")
    sp = (data.get("constants") or {}).get("bracing_spacing_in")
    sp = sp.get("value") if isinstance(sp, dict) else sp
    out["nombres_contexto"] = {"ballistic_th": th, "bracing_oc_in": sp}
    out["sealant_exterior_lf"] = round(SEAL.get("exterior", 0.0), 2)
    # v67: accesorios y extras (ACCESORIOS_REGLAS) + partition types (CONVENCION_PARTITION_TYPES)
    acc = accesorios.calcular(out, data, st, _fo(data, fo))
    out["familias"].update(acc["familias"])              # Level 5 v67 sustituye al de _level5; grille aparte
    out["filas"] += acc["filas"]
    out["avisos"] += acc["avisos"]
    out["accesorios"] = {"familias": acc["familias"], "estado": acc["estado"], "unidades": acc["unidades"],
                         "waste": acc["waste"], "nombres_excel": acc["nombres_excel"]}
    out["rfis_accesorios"] = acc["rfis"]
    out["estado_accesorios"] = acc["estado"]
    out["obligatorias"] = OBLIGATORIAS + [f for f in accesorios.FAMS if f not in OBLIGATORIAS]
    out["excluidas"] = {"batt insulation": "EXCLUDED (criterio del estimador: no insulation)"}
    out["partition_types"] = partition_types.partition_types(data, bo)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        for n, d in (("studs_in.json", studs_in), ("board_in.json", board_in), ("corridas_in.json", corr_in),
                     ("headers_in.json", hdr_in), ("studs_out.json", st), ("board_out.json", bo),
                     ("corridas_out.json", co), ("familias_out.json", out), ("accesorios_out.json", acc)):
            if d is not None:
                open(os.path.join(outdir, n), "w").write(json.dumps(d, indent=1, ensure_ascii=False))
    return out


def main(argv):
    argv = list(argv)
    fo = None
    if "--fo" in argv:
        i = argv.index("--fo")
        fo = json.load(open(argv[i + 1]))
        del argv[i:i + 2]
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])), argv[2], fo)
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR canon.py: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out["familias"], indent=1, ensure_ascii=False))
    for a in out["avisos"]:
        print("AVISO", a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
