#!/usr/bin/env python3
"""canon.py v63 — UN takeoff canónico de GEOMETRÍA -> todas las familias, sin juicio fuera de medir el plano.

[v78 R78.12] Las N/HOJA citadas en comentarios / docstrings son EJEMPLOS del set donde se halló cada regla, no
fuentes: la fuente de cada fila sale del canon (constants.*_source o el source del dato) o es "default (no sheet)".

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
  - v77c (U8): acoustical sealant EXCLUIDO en todos los proyectos (sin renglón ni cálculo; exclusión en
    Clarifications); solo sealant_base_exterior (sealant at base of gypsum, exterior) se cuantifica, familia propia.
  - door entre dos walls (jamb_wall + head_ft): cripples FLOOR(R.O./oc) x (H − head) + bottom/top track R.O.
    (#14A, ADV1-3).
  - level 5 (level5_items, SF) y batt insulation EXCLUDED siempre (criterio del usuario: "no insulation").

v65b (DECISIONES DEL USUARIO #18-#22, 17-oct-2026) — header / sill son REGLAS, no parámetros:
  - header_params se rechaza (v65 lo pasaba a headers.py con default = v64).
  - #19 abertura con "OR STEEL" (or_steel: true u "OR STEEL" en header_type) y header steel_by_others = error.
  - #20 box = 4 piezas, door <ref> double (#21), #18 sill double > 4'-0", #22 office front CONT. BOX BEAM un run por
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
import chequeos_v75  # noqa: E402   v75: R75.5 / R75.6 / R75.7 (arbitraje #23)
import chequeos_v76  # noqa: E402   v76: R76.1-R76.5 (arbitraje #24)
import chequeos_v77  # noqa: E402   v77: R77.4 (decisiones del usuario D3 / D4); v77b: R77.10 (largo a través de doors)

EPS = 1e-6
DEFAULT_SIN_HOJA = "default (no sheet)"           # v78 (R78.12): default de oficio, nunca una N/HOJA fija
F_PAR = "6\" parapet stud"
F_36 = "3-5/8\" stud (todos los gauges)"
F_TRIM = "metal trim (corner bead, casing, shadow molding)"
F_GYP = "5/8\" gyp board regular (walls + ceilings)"
# v80f (R80e.20): 8" joist (ceiling box) y USG drywall suspension grid (main tee / cross tee / moldings)
F_J8 = "8\" joist"
# v80n (R80e.27): accesorios impresos en los detalles (clips, fasteners de detalle, nested runner)
F_NEW27 = ["clip angle (bracing / nested connections)", "#8 pan head screws, relief channel to structure", "P.A.F. at cross members", "5/8\" cement board", "plywood screws (Teks/3)", "cement board screws", "nested inner runner (deflection head)"]
F_MT, F_CT = "USG drywall main tee (DGLW26)", "USG drywall cross tee (DGLW424)"
F_CM, F_AM = "USG channel molding (DGCM27)", "USG angle molding (DGWM24)"
USG_GRID = "usg_grid"
SUSP = ("furring", "stud_joist")                 # sistemas suspendidos: carrying + hangers + perimeter track
JOIST_ONLY = ("canopy_joist", "framed_soffit")   # joists 3-5/8" sin carrying ni hangers
TRIM_KINDS = {"corner_bead", "casing_bead", "shadow_molding", "edge_trim", "j_bead"}
NO_NODOS = ("ceiling_transition", "column_wrap", "grille_head")  # v65 + v67: grille 2-1/2" -> accesorios.py
F_FRP = "FRP"
F_SEAL = "sealant at base of gypsum (exterior)"   # v77c U8: el acoustical sealant está EXCLUIDO
F_SEAL_AC = "acoustical sealant"
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
POLY = [""]                                        # v76: espesor impreso del polyiso del nailbase (constants)
# v73 (arbitraje #21, R73.3): renglón de compra por USO con el nombre de la plantilla del estimador (un renglón por
# material, espesor y uso). `plywood_strips[].uso` lo declara; sin él se infiere del texto (pier / column / canopy).
PLY_USO_NOMBRE = {
    "nailbase": "Exterior sheathing {th} FRT plywood bonded to {poly} polyiso",   # v76: nombre de la plantilla
    "canopy_soffit": "{th} FRT plywood sheathing (canopy and soffits)",
    "column_wrap": "{th} FRT plywood at canopy column wraps",
    "pier": "{th} FRT plywood at storefront piers",
    "substrate": "FRT plywood substrate ({tin} in.)",
}
PLY_USOS = tuple(PLY_USO_NOMBRE)
PLY_TH = {"nailbase_5_8_polyiso": "5/8", "frt_5_8_ext": "5/8", "frt_5_8": "5/8", "frt_3_4": "3/4"}
PLY_USO = {}                                       # nombre de plantilla -> SF
BLK_ORIGEN = {}                                    # v73: metal blocking por origen (edge del detalle / notas)
BLK_MADERA = {}                                    # v76: blocking de madera no FRT (renglón propio)
STUD_ELEM = {}                                     # v76: {familia: {renglón: LF}} (framed soffit en su renglón)
SEAL = {}                                          # exterior -> LF (v77c U8: acoustical EXCLUIDO)
EXCL_SEAL_AC = ("EXCLUDED in all projects (estimator standing order): no acoustical sealant row and no "
                "quantity; listed in Clarifications as an exclusion")
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
    if uso == "nailbase" and not POLY[0]:
        raise ValueError("constants.nailbase_polyiso_in {value: '<espesor impreso>\"', source N/HOJA} obligatoria con "
                         "nailbase (renglón 'Exterior sheathing ... bonded to <espesor> polyiso'; v76)")
    n = PLY_USO_NOMBRE[uso].format(th=th + '"', tin=th, poly=POLY[0])
    PLY_USO[n] = PLY_USO.get(n, 0.0) + sf


def _polyiso(data):
    """v76 (arbitraje #24): el renglón del nailbase lleva el espesor IMPRESO del polyiso (nombre de la plantilla del
    estimador): constants.nailbase_polyiso_in {value: '<n>"', source N/HOJA} obligatoria si hay nailbase."""
    c = (data.get("constants") or {}).get("nailbase_polyiso_in")
    if c is None:
        return ""                                      # _ply falla si después hay nailbase
    v = str(c.get("value") or "").strip() if isinstance(c, dict) else ""
    if not v or not chequeos_v76.NHOJA.search(str(c.get("source") or "")):
        raise ValueError("constants.nailbase_polyiso_in {value, source N/HOJA} (v76)")
    v = re.sub(r"^(\d+)\s+(\d+/\d+)", r"\1-\2", v)            # 2 1/2" -> 2-1/2"
    return v if v.endswith('"') else v + '"'


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
    # v75 (R75.1, arbitraje #23): el nombre de un renglón de track nunca lleva "ceiling" ni "soffit": el calificador y el
    # estimador lo leerían como track de ceilings (en dos pruebas ciegas el renglón de heads caía en esa familia y bottom / top quedaba baja)
    "heads": ("Bottom track - roof step and heads (vestibule / bulkhead)",
              "Top track - roof step and heads (vestibule / bulkhead)"),
    "size": ("Bottom track {sz}", "Top / deflection track {sz}"),
    # v75 (R75.2): un ELEMENTO (no wall) que no es fila de la Partition Takeoff (cripples, grille head, partes de pier
    # sin type...) va por elemento, no al renglón por tamaño: el renglón {sz} = walls (con tag o sin tag: alcove, stub)
    # + elementos que sí son fila de un type (column wrap, bulkhead, pier de un type)
    "elemento": ("Bottom track - other framing (not a partition type, see source)",
                 "Top / deflection track - other framing (not a partition type, see source)"),
    "otro": ("Bottom track - other (openings between walls, see source)",
             "Top / deflection track - other (openings between walls, see source)"),
}
TRACK_FAM = {"bottom": "bottom track (todos)", "top": "top / deflection track (todos)"}


def ids_partition_takeoff(pt):
    """v75 (R75.2): ids de los walls que son FILA de la Partition Takeoff (types de partition_types.py)."""
    out = set()
    for x in ((pt or {}).get("types") or {}).values():
        for f in x.get("filas") or []:
            out.update(str(i) for i in (f.get("ids") or []))
            if f.get("wall") is not None:
                out.add(str(f["wall"]))
    return out


def verificar_track_nombres(tbe):
    """v75 (R75.1) compuerta: cada renglón de track_by_element cae en SU familia (bottom / top) con familias.py."""
    import familias
    malos = [(k, n, familias.familia(n, "lf")) for k, d in tbe.items() for n in d
             if familias.familia(n, "lf") != TRACK_FAM[k]]
    if malos:
        raise ValueError("R75.1: renglón de track fuera de su familia (nombre con ceiling / soffit u otro): "
                         + "; ".join(f"{k} '{n}' -> {f}" for k, n, f in malos))
    return True


def track_by_element(data, co, fam, pt=None):
    """{"bottom": {renglón: LF}, "top": {renglón: LF}}: la familia de track repartida por ELEMENTO (parapet, roof step /
    heads) y, para el resto, por TAMAÑO de stud del wall (R71.8 + R73.3). Σ renglones = familia (el resto que corridas
    no explica, p. ej. track sobre openings entre walls, va a 'other'). Nombres = plantilla del estimador.
    v75 (R75.2): con `pt` (partition_types), un elemento (no wall) que no es fila de la Partition Takeoff va al renglón
    'other framing' por elemento; walls y elementos de un type siguen en su renglón por tamaño."""
    en_pt = ids_partition_takeoff(pt) if pt else None
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
        elif en_pt is not None and el not in (None, "wall") and wid not in en_pt:
            nb, nt = TRACK_NOMBRES["elemento"]      # R75.2: elemento (no wall) que no es fila de la Partition Takeoff
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
    verificar_track_nombres(out)
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
    sin = sch.get("sources_none") or {}                  # v80e: set sin hojas S* (lo dice el índice) -> motivo
    if not any(re.match(r"^(\w+/)?S-?\d", h) for h in hojas) and not str(sin.get("S") or "").strip():
        raise ValueError("opening_schedule.sources sin plan estructural (S*): barrer lintels HSS / steel headers "
                         "(o sources_none.S con el motivo citado del índice del set)")
    if not any(re.match(r"^(\w+/)?M-?\d", h) for h in hojas):
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
        if ("ns_ft" not in c or "ew_ft" not in c) and c.get("system") not in SUSP and "span_ft" in c:
            return float(c["span_ft"]), float(c["run_ft"])     # v77: joists (soffit) con su span propio
        if "ns_ft" not in c or "ew_ft" not in c:
            raise ValueError(f"{c.get('room')}: con carrying_direction declarar ns_ft y ew_ft (no span/run: "
                             f"la orientación es del proyecto, no de cada room — #12A room <ref> cruzado)")
        ns, ew = float(c["ns_ft"]), float(c["ew_ft"])
        return (ns, ew) if d == "N-S" else (ew, ns)
    if c.get("system") in SUSP:
        # v77: sin dirección del proyecto cada corrida tomaba el lado largo por room y el carrying channel variaba
        # entre corridas. La dirección es UNA para el proyecto: impresa (source) o RFI con delta.
        raise ValueError(f"{c.get('room')}: ceiling {c.get('system')} sin constants.carrying_direction {{value N-S | "
                         f"E-W, source N/HOJA o rfi con el delta de la otra dirección}} (R77.7)")
    return float(c["span_ft"]), float(c["run_ft"])


def generar(data):
    walls = data.get("walls") or []
    runs_extra = data.get("runs") or []
    _solapes([dict(w, id=w["id"], **({"line": "PAR:" + str(w["line"])} if _es_parapet(w) and w.get("line") is not None
                                    else {})) for w in walls] + [dict(r, id=r["id"]) for r in runs_extra])
    for r in runs_extra:
        if r.get("element") in ("parapet", "column_wrap", "pier") or _es_parapet(r):
            # v68: sus studs solo se cuentan desde walls (E3 / wraps); en runs se perdían sin aviso (como una transición TR-nnn de una prueba)
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
                     **({k: w[k] for k in ("track_lines", "track_lines_source", "wall_line_ft", "bracing_rows", "bottom_track", "top_track", "track_source",
                                           "bracing_rows_source") if k in w})})   # v80k (R80e.23): bracing_rows pasa a corridas
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
            if hdr == "not_called":                       # v80e (R71.10): ningún schedule / detalle llama header
                if not str(o.get("header_source") or "").strip() or not str(o.get("header_rfi") or "").strip():
                    raise ValueError(f"{w['id']} {o['ref']}: header not_called exige header_source (N/HOJA de lo "
                                     f"revisado) y header_rfi (RFI con el delta) — R71.10")
                avisos.append(f"{o['ref']}: header NOT CALLED by any schedule / detail ({o['header_source']}) -> "
                              f"0 LF + RFI: {o['header_rfi']}")
                continue
            if hdr != "metal":
                raise ValueError(f"{o['ref']}: header debe ser metal | steel_by_others | not_called")
            ops.append({"ref": o["ref"], "wall": w["id"], "kind": o.get("kind", "door"),
                        "location": o.get("location", ""), "ro_w_ft": o["ro_w_ft"], "qty": 1,
                        "with_sill": bool(o.get("with_sill")), "source": o.get("source", src),
                        **{k: o[k] for k in ("header_type", "header_type_source", "beams", "beams_source",
                                             "structure_source", "structure", "pieces", "pieces_source",
                                             "piece", "sill_pieces", "sill_pieces_source", "continuous_run",
                                             "or_steel", "run_ends", "run_ends_source", "front_line",
                                             "with_sill_source") if k in o}})
    bordes = chequeos_v76.bordes_transicion(data, SUSP)      # v76 (R76.6): R73.16 hecha compuerta
    for c in data.get("ceilings") or []:
        if c.get("system") in SUSP:
            if c.get("perimeter_ft") is None:
                raise ValueError(f"{c['room']}: ceiling {c['system']} sin perimeter_ft (ceiling_perimeter track, "
                                 f"#12B -<n>)")
            chequeos_v76.r76_6_perimetro(c)
            resta = bordes.get(str(c["room"]), 0.0)
            runs.append({"id": "CP:" + str(c["room"]), "element": "ceiling_perimeter", "orientation": "horizontal",
                         "length_ft": round(float(c["perimeter_ft"]) - resta, 4), "source": _src(c, c["room"])
                         + (f" (perímetro {c['perimeter_ft']} - transiciones {round(resta, 3)}, R76.6)" if resta else "")})
    for r in runs_extra:
        rr = dict(r)
        for k in ("line", "from_ft", "to_ft"):
            rr.pop(k, None)
        runs.append(rr)
    _bsp = (data.get("constants") or {}).get("bracing_spacing_in")
    corr_in = {"bracing": {"spacing_in": _c(data, "bracing_spacing_in", 48.0),
                           # v78 (R78.12): sin constants.bracing_spacing_in = default de oficio marcado, sin N/HOJA
                           "source": _bsp.get("source") if isinstance(_bsp, dict) else DEFAULT_SIN_HOJA,
                           "default_de_oficio": not isinstance(_bsp, dict)},
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
                         f"(decisiones usuario #19, #20) — no steel_by_others")


def _v65_checks(data):
    """Reglas deterministas del arbitraje #14 (17-oct-2026) que no necesitan totales."""
    if data.get("header_params") is not None:
        raise ValueError("header_params ya no existe (v65b): sill double > 4'-0\", window metal box, box = 4 piezas, "
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
                             f"T/STUD - B/STUD del detalle de la fascia; v65, #14A −<n> LF)")
    cj = [c for c in data.get("ceilings") or [] if c.get("system") == "canopy_joist"]
    if cj and not str(data.get("fascia_none_reason") or "").strip():
        if not any(w.get("element") == "fascia_box" for w in walls):
            raise ValueError("canopy_joist sin fascia_box en walls — la fascia (T/STUD - B/STUD de su detalle) lleva studs "
                             "3-5/8\" y track; o fascia_none_reason (v65, #14A −<n> LF)")
    # BOX HEADER AS NEEDED -> framing_wall (vestibule_head)
    for o in data.get("openings_extra") or []:
        if "AS NEEDED" in str(o.get("header_type") or "").upper():
            fw = o.get("framing_wall")
            if fw not in por_id or por_id[fw].get("element") != "vestibule_head":
                raise ValueError(f"{o['ref']}: 'BOX HEADER AS NEEDED' sin framing_wall (vestibule_head) — el detalle rotula "
                                 f"'METAL STUD FRAMING & BOX HEADER AS NEEDED': los studs sobre el storefront se "
                                 f"cuentan (v65, #14B −<n> LF)")
    # framed_soffit -> drop_lines
    for c in data.get("ceilings") or []:
        if c.get("system") != "framed_soffit":
            continue
        dl = c.get("drop_lines")
        if not isinstance(dl, dict) or not str(dl.get("source") or "").strip():
            raise ValueError(f"{c['room']}: framed_soffit sin drop_lines {{value, source}} (líneas de drop studs que "
                             f"= bordes del soffit que en el RCP dan a un ceiling, no a una partición; el detalle del soffit dibuja STL STUD "
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
                             f"del detalle) -> abut: el stud de la junta está en el stub (arb11, #14A)")
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


# v79 (R79.3): un detalle es de TODO lo que corta, no solo de la hoja que lo burbujea. Un ceiling suspendido sin detail
# no puede despachar con un motivo que CITA detalles (N/HOJA) que lo cortan o que lo nombran en su título (sección de
# un enlarged plan / elevación, "CEILING DETAIL @ <elemento>"): esa es su fuente y su sistema. Si el lector de verdad
# los descarta, details_checked [{ref N/HOJA, cuts_this: false, why}] por cada uno. Un elemento que su ubicación nombra
# SOFFIT no se carga como ceiling suspendido sin un detalle que dibuje la suspensión.
RX_NHOJA_DET = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d{1,2}(?:\.\d{1,2})?\b")
RX_SOFFIT = re.compile(r"\bsoffit\b", re.I)


def _r79_ceiling_detalle(c):
    rid = c.get("id") or c.get("room")
    dc = c.get("details_checked") or []
    if not isinstance(dc, list) or not all(isinstance(x, dict) and RX_NHOJA_DET.search(str(x.get("ref") or "")) and
                                           isinstance(x.get("cuts_this"), bool) and str(x.get("why") or "").strip()
                                           for x in dc):
        raise ValueError(f"{rid}: details_checked = lista de {{ref N/HOJA, cuts_this (bool), why}} (R79.3)")
    corta = [x["ref"] for x in dc if x["cuts_this"]]
    if corta:
        raise ValueError(f"{rid}: details_checked dice que {', '.join(corta)} corta este ceiling: ese detalle ES su fuente "
                         f"(detail = N/HOJA y system del detalle), no detail_none_reason (R79.3)")
    revisados = {str(x["ref"]).strip().upper() for x in dc}
    citados = {m.group(0).upper() for m in RX_NHOJA_DET.finditer(str(c.get("detail_none_reason") or ""))}
    sin = sorted(citados - revisados)
    if sin:
        raise ValueError(f"{rid}: detail_none_reason cita {', '.join(sin)} y el ceiling queda suspendido sin detail. "
                         f"R79.3: un detalle que corta este ceiling desde CUALQUIER hoja (sección burbujeada en un "
                         f"enlarged plan / elevación) o que lo nombra en su título ES su fuente; declarar detail = N/HOJA "
                         f"con su system, o details_checked [{{ref, cuts_this: false, why}}] por cada uno")
    if RX_SOFFIT.search(f"{c.get('location') or ''} {c.get('name') or ''}") and \
            not str(c.get("soffit_suspended_source") or "").strip():
        raise ValueError(f"{rid}: la ubicación lo nombra SOFFIT y va como ceiling suspendido sin detail. R79.3: un soffit "
                         f"lleva el detalle que lo arma (framed_soffit con su N/HOJA), o soffit_suspended_source = "
                         f"N/HOJA del detalle que dibuja hangers / carrying en ese soffit")


# v79 (R79.4): purlin (track a deck a través de los flutes) solo en un top track que APOYA EN EL DECK. Un top track que
# el detalle fija a acero estructural (slip clip a viga, T/STEEL) no lleva purlin salvo que un detalle lo imprima
# (purlin_detail {source N/HOJA, text con PURLIN}). Filas apiladas de una misma línea en planta (misma banda) llevan
# purlin a lo más en una, salvo purlin_rows_reason.
RX_A_ACERO = re.compile(r"\bSTEEL\b|\bSLIP CLIP\b|\bBEAMS?\b|T/STEEL", re.I)


def _r79_purlin(data):
    import criterios                                # v80 (R80.1): el mismo criterio que inventario._purlin
    con = [w for w in data.get("walls") or [] if w.get("purlin")]
    for w in con:
        impreso = criterios.purlin_impreso(w)
        if criterios.purlin_detail_mal(w):
            raise ValueError(f"{w['id']}: purlin_detail {{source N/HOJA, text literal con PURLIN}} (R79.4)")
        if criterios.tope_a_acero(w) and not impreso:
            raise ValueError(f"{w['id']}: purlin true y el tope se fija a acero estructural ({w.get('to_deck_source')}). "
                             f"R79.4: purlin solo donde el top track apoya en el deck; con acero, purlin false salvo "
                             f"purlin_detail impreso")
    grupos = {}
    for w in con:
        b = w.get("band") or {}
        if not b:
            continue
        k = (str(b.get("sheet")), str(b.get("ori")), round(float(b.get("c0", 0)), 1), round(float(b.get("c1", 0)), 1))
        grupos.setdefault(k, []).append(w)
    for k, ws in grupos.items():
        for i, a in enumerate(ws):
            for bw in ws[i + 1:]:
                ba, bb = a["band"], bw["band"]
                lo = max(min(ba["lo"], ba["hi"]), min(bb["lo"], bb["hi"]))
                hi = min(max(ba["lo"], ba["hi"]), max(bb["lo"], bb["hi"]))
                if hi - lo > 1.0 and not criterios.filas_purlin_ok(a, bw):
                    raise ValueError(f"{a['id']} y {bw['id']}: filas apiladas de la misma línea en planta con purlin las "
                                     f"dos (R79.4: el purlin va en la fila cuyo top track apoya en el deck; la otra "
                                     f"purlin false, o purlin_rows_reason)")


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
                             f"un CSR soffit de detalle propio como furring con hangers)")
        cs = (det.get(d) or {}).get("ceiling_system") if d else None
        if cs and cs != c.get("system"):
            raise ValueError(f"{c['room']}: system {c.get('system')} != details['{d}'].ceiling_system {cs}")
        if c.get("system") in SUSP and not d:
            _r79_ceiling_detalle(c)
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
            # v78 (R78.10): un elemento que arranca SOBRE otro (cripples sobre lintel / box, vestibule head sobre el
            # box) declara su arranque en base_ft {value, source}: altura = B.O.D. - d - base. Sin base_ft = piso.
            base = 0.0
            if sb.get("base_ft") is not None:
                base = float(_num_src(sb["base_ft"], f"{w['id']}.stops_under_beam.base_ft"))
                if base < 0:
                    raise ValueError(f"{w['id']}: stops_under_beam.base_ft {base} < 0")
            hb = float(_num_src(bod, f"{w['id']}.stops_under_beam.bod_ft")) - d_ft - base
            if abs(float(w["height_ft"]) - hb) > 0.02:
                tb = f" - base {round(base, 3)}" if base else ""
                raise ValueError(f"{w['id']}: height_ft {w['height_ft']} != B.O.D. {bod['value']} - d {round(d_ft, 3)}"
                                 f"{tb} = {round(hb, 3)} (E26; si el elemento arranca sobre un lintel / box declarar "
                                 f"stops_under_beam.base_ft {{value, source}}, R78.10)")


BOARD_ELEMS = ("roof_step", "ceiling_transition", "soffit_side", "ceiling_bulkhead", "vestibule_head", "grille_head")
# Claves que canon.py y las tools que reciben los walls (inventario, partition_types, accesorios, studs_nodos,
# board_caras, corridas, headers, particion / comparar / etapas v69) leen de un wall, + campos de traza de etapas.
WALL_KEYS = frozenset("""
id tag element jamb_strips location room sheet plan_sheet page band line from_ft to_ft axis ori straight_run split_of front
facade chase length_ft length_source length_status length_printed_ft length_printed_source length_vector_ft
length_basis length_op height_ft height_source height_status height_op height_avg_ft zones zones_source zone
to_deck to_deck_source stops_under_beam canopy_beam break_reason stud_size stud_source stud_size_source
stud_size_status gauge gauge_source stud_gauge oc_in oc_source rows rows_source purlin purlin_source purlin_note
detail detail_source faces faces_ft faces_ft_source faces_note faces_none_reason fos_chain fos_chain_faces parts kickers
vertical_studs edges drop_line soffit_of openings track_lines track_lines_source wall_line_ft bulkhead_of
bottom_track_lf head_build exterior in_cavity in_cavity_source source source_chain status notes note tag_ids
tags_descartados band_length_ok_reason img evidence_png type_source type_status default_type_source adjacent_to
adjacent_source wet_fixtures k_customer studs_drawn hatch_extent dim_scan sheathing edge_of
beam_override part_of same_box_ok opening_ref type_change_rfi anchorage orientation sheets_searched
thickness_measured_in default_type_rfi sheathing_bottom_ft owner purlin_detail bracing_rows bracing_rows_source bottom_track top_track track_source
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


def _r78_espesor(walls):
    """v78 (R78.11): un solo campo de espesor medido entre faces: `thickness_measured_in` (número, in). Lo leen
    chequeos_v73 (R73.7) y la spec G_THICK; `thickness_measured_info` queda como alias de traza y no puede
    contradecirlo."""
    for w in walls:
        if "thickness_measured_in" not in w:
            continue
        v = w["thickness_measured_in"]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"{w.get('id')}: thickness_measured_in '{v}' debe ser un número (in) medido entre las "
                             f"dos faces, no texto (R78.11)")
        al = w.get("thickness_measured_info")
        if isinstance(al, (int, float)) and not isinstance(al, bool) and abs(float(al) - float(v)) > 0.01:
            raise ValueError(f"{w.get('id')}: thickness_measured_in {v} != thickness_measured_info {al} — un solo "
                             f"espesor medido (R78.11)")


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
    _r78_espesor(walls)
    import chequeos_v71                             # v78 (R78.15): grupo sin tag / tag remitido -> owner del canon
    sin_dueno = chequeos_v71.r71_5(data) + chequeos_v71.r78_15(data)
    if sin_dueno:
        raise ValueError(f"{len(sin_dueno)} grupo(s) / tag(s) sin dueño: " + "; ".join(sin_dueno))
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
    detalle típico local (p. ej. un fixture con joists) no cambia el sistema del campo. v79 (R79.3): o la sección que
    lo CORTA burbujeada en otra hoja: {detail, cuts_this: true, cut_on: hojas de la burbuja, source}."""
    for c in data.get("ceilings") or []:
        sysm = c.get("system")
        import criterios
        if not criterios.sistema_pide_callout(sysm):
            continue
        sc = c.get("system_callout")
        # v79 (R79.3): vale también la sección / detalle que CORTA este ceiling burbujeado en OTRA hoja (enlarged plan,
        # elevación): cuts_this true + cut_on (las hojas donde está la burbuja). Un detalle es de todo lo que corta.
        # v80 (R80.1): el criterio vive en criterios.py y lo comparte reglas.py A_CEILING_SYS (nunca dos versiones).
        import criterios
        ok = criterios.system_callout_ok(sc)[0]
        susp = RX_SUSP.search(f"{c.get('source', '')} {c.get('legend', '')}")
        if not ok:
            raise ValueError(f"{c.get('room')}: ceiling {sysm}" + (" con source / legend SUSPENDED" if susp else "")
                             + " sin system_callout {detail, on_plan: true, source} — R70.1: a typical local detail "
                               "does not change the field system; declare system_callout (bubble on THIS ceiling, or "
                               "R79.3 cuts_this: true + cut_on: the sheet(s) whose section bubble cuts it) "
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
        if inter > EPS and all(f.get("length_ft") is not None for f in w.get("faces") or [] if f.get("board")):
            continue          # v76 (R76.5): partition_types toma el LF del type de las caras interiores con board
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
        raise ValueError("frp.top_ft {value, source N/HOJA} (cota 'TO TOP OF FRP' del detalle / elevación)")
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
    """v77c (decisión del usuario U8, R77.12): ACOUSTICAL SEALANT EXCLUIDO EN TODOS LOS PROYECTOS: sin renglón ni
    cálculo; va en Clarifications / Scope Checklist como exclusión (out["excluidas"]). details[*].sealant y
    sealant_items de un canon viejo no se calculan (aviso con lo que se dejó fuera). Solo se cuantifica el
    sealant_base_exterior ("sealant at base of gypsum", exterior), que NO es acoustical: familia propia."""
    det = data.get("details") or {}
    viejos = sorted(d for d, x in det.items() if isinstance(x, dict) and isinstance(x.get("sealant"), dict) and
                    int(x["sealant"].get("bottom_faces") or 0) + int(x["sealant"].get("top_faces") or 0) > 0)
    if viejos or data.get("sealant_items"):
        SEAL["_ignorado"] = (f"acoustical sealant EXCLUDED (U8): not computed from details {viejos} "
                             f"{'+ sealant_items' if data.get('sealant_items') else ''}".strip())
    be = data.get("sealant_base_exterior")
    if be:
        src = _src(be, "sealant_base_exterior")
        if re.search(r"acoustic", f"{be.get('label', '')} {src}", re.I) and not re.search(r"not acoustic",
                                                                                           f"{be.get('label', '')} {src}", re.I):
            raise ValueError("sealant_base_exterior rotulado acoustical: el acoustical sealant está EXCLUIDO (U8)")
        fam[F_SEAL] += float(be["lf"])
        SEAL["exterior"] = SEAL.get("exterior", 0.0) + float(be["lf"])
        filas.append({"familia": F_SEAL, "ref": "sealant at base of gypsum (exterior)", "source": src,
                      "operacion": f"{be['lf']} LF (not acoustical)"})


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



def _atm_wall(data, fam, filas, st, co):
    """[R77.11 RETIRADA en v80 ("ATM = 0"); manda R78.36 / R80.3] El framing de un recess de ATM / equipo empotrado está en la wall que
    lo contiene: su partition type lleva todo su metal (studs_nodos + corridas) y el renglón "extra framing ATM" = 0;
    no se agrega renglón, ni sistered, ni furring, salvo lo que un detalle impreso pida explícitamente
    (v78 W1, R78.36: atm_recess.extra_printed {source N/HOJA, text literal, lf, op} SE SUMA a extra framing ATM en
    accesorios.py; la wall no cambia: nada se resta ni se mueve). Vale igual en una partición interior (walk-up) o en
    una wall exterior (drive-up). Compuerta: la wall del ATM pasa por studs_nodos y corridas (si no, el metal del
    recess no está en ningún type); la fórmula vieja = error (accesorios.atm_recess_valido)."""
    data["_atm_wall"] = []
    st_w = {str(x.get("id")): x for x in (st or {}).get("walls") or []}
    co_w = {str(r.get("id")): r for r in (co or {}).get("renglones") or []}
    for w in data.get("walls") or []:
        for o in w.get("openings") or []:
            if not o.get("atm_recess"):
                continue
            accesorios.atm_recess_valido(o, f"{w['id']} {o['ref']}")
            wid = str(w["id"])
            if _es_parapet(w) or _no_nodos(w) or wid not in st_w or ("W:" + wid) not in co_w:
                raise ValueError(f"{wid} {o['ref']}: atm_recess en un elemento sin studs_nodos / corridas (U1 v77c: el "
                                 f"framing del recess está en la wall que lo contiene; esa wall tiene que estar en "
                                 f"su type con studs y bottom / top track)")
            slf = float(st_w[wid].get("lf") or 0.0)
            cw = co_w["W:" + wid]
            if slf <= EPS or float(cw.get("bottom_lf") or 0.0) <= EPS or float(cw.get("top_lf") or 0.0) <= EPS:
                raise ValueError(f"{wid}: wall del ATM sin studs o sin bottom / top track en su type (U1 v77c)")
            op = (f"ATM recess {o['ref']} in wall {wid} (type {w.get('type', '?')}): its framing is in that wall "
                  f"(studs {round(slf, 2)} LF + bottom / top track in its type); extra framing = 0 (U1)")
            data["_atm_wall"].append({"ref": o["ref"], "wall": wid, "lf": 0.0, "op": op})


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
            raise ValueError(f"{w['id']}: ceiling_transition sin kickers (detalle de la transición) — sus studs son kickers + "
                             f"vertical_studs, no pasa por studs_nodos (v65)")
        if not k:
            continue
        if w.get("element") != "ceiling_transition":
            raise ValueError(f"{w['id']}: kickers solo en ceiling_transition")
        src = _src(k, f"{w['id']}.kickers")
        vs = w.get("vertical_studs")                  # decisión usuario #7: studs verticales (dashed) a estructura
        if not isinstance(vs, dict):
            raise ValueError(f"{w['id']}: ceiling_transition con kickers sin vertical_studs {{oc_in, height_ft, "
                             f"source}} — los studs verticales a estructura se cuentan además del kicker "
                             f"(decisión usuario #7)")
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
            fcf = w.get("fos_chain_faces")            # v76: caja parcial = una cadena (o medida en vector) POR cara
            if fcf is not None:
                if fc is not None:
                    raise ValueError(f"{w['id']}: fos_chain y fos_chain_faces a la vez (una u otra; v76)")
                if not isinstance(fcf, list) or len(fcf) != len(fs):
                    raise ValueError(f"{w['id']}: fos_chain_faces debe tener una entrada por face de faces_ft ({len(fs)})")
                for i_, (f_, e_) in enumerate(zip(fs, fcf)):
                    if not isinstance(e_, dict) or not str(e_.get("source") or "").strip():
                        raise ValueError(f"{w['id']}.fos_chain_faces[{i_}]: {{value: [eslabones] | measured_op, source}}")
                    if e_.get("value") is not None:
                        cad = sum(float(x) for x in e_["value"])
                        if abs(cad - f_) > 0.02:
                            raise ValueError(f"{w['id']}.fos_chain_faces[{i_}]: face {f_} != Σ cadena {round(cad, 3)} "
                                             f"({e_['source']}; v76)")
                    elif not str(e_.get("measured_op") or "").strip():
                        raise ValueError(f"{w['id']}.fos_chain_faces[{i_}]: sin cadena impresa -> measured_op (vector) "
                                         f"+ source (v76)")
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
                             f"esquina lleva stud en las dos faces), no como wall recto (v65)")
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
        if sysm not in SUSP + JOIST_ONLY + (USG_GRID,):
            raise ValueError(f"{c['room']}: system {' | '.join(SUSP + JOIST_ONLY + (USG_GRID,))}")
        if sysm == USG_GRID:   # v80f (R80e.20): USG drywall suspension grid (detalle del RCP), sin furring/carrying
            dr = c.get("hanger_drop_ft")
            if not isinstance(dr, dict) or "value" not in dr or not str(dr.get("source") or "").strip():
                raise ValueError(f"{c['room']}: usg_grid sin hanger_drop_ft {{value, source}}")
            for k_ in ("main_oc_in", "cross_oc_in"):
                v_ = c.get(k_)
                if not isinstance(v_, dict) or "value" not in v_ or not str(v_.get("source") or "").strip():
                    raise ValueError(f"{c['room']}: usg_grid sin {k_} {{value, source}} (impreso o estándar USG con nota)")
            if c.get("perimeter_ft") is None:
                raise ValueError(f"{c['room']}: usg_grid sin perimeter_ft (moldings)")
            ns_, ew_ = float(c["ns_ft"]), float(c["ew_ft"])
            lng, sht = max(ns_, ew_), min(ns_, ew_)
            m_oc, x_oc = float(c["main_oc_in"]["value"]) / 12.0, float(c["cross_oc_in"]["value"]) / 12.0
            n_m = int(math.ceil(sht / m_oc - EPS)) + 1
            n_x = int(math.ceil(lng / x_oc - EPS)) + 1
            n_hm = int(math.ceil(lng / h_oc - EPS)) + 1
            per, area, drop = float(c["perimeter_ft"]), float(c["area_sf"]), float(dr["value"])
            fam[F_MT] += n_m * lng
            fam[F_CT] += n_x * sht
            fam[F_CM] += per
            fam[F_AM] += per
            hang = n_m * n_hm
            fam["hanger wire"] += hang * drop
            HANGERS.append({"room": c["room"], "pcs": hang, "altura_ft": drop, "altura_source": dr["source"],
                            "lf": round(hang * drop, 2)})
            fam[BOARD_FAM.get(c.get("board") or "5/8 regular", F_GYP)] += area
            filas.append({"familia": "ceilings", "room": c["room"], "source": src,
                          "operacion": f"usg_grid: main tee ROUNDUP({round(sht, 3)}/{round(m_oc, 3)})+1 = {n_m} x "
                                       f"{round(lng, 3)} = {round(n_m * lng, 2)}; cross tee ROUNDUP({round(lng, 3)}/"
                                       f"{round(x_oc, 3)})+1 = {n_x} x {round(sht, 3)} = {round(n_x * sht, 2)}; "
                                       f"channel + angle molding {per} each; hangers {n_m} x {n_hm} = {hang} x drop "
                                       f"{drop} = {round(hang * drop, 2)} LF; board {area} SF"})
            continue
        if "soffit" in str(c["room"]).lower() and sysm in SUSP:
            raise ValueError(f"{c['room']}: un soffit es framed (su detalle dibuja studs) -> framed_soffit o "
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
                fam[BOARD_FAM.get(c.get("board") or "5/8 regular", F_GYP)] += area   # v80f R80e.19: board del ceiling
                bd = f"board {area} SF"
                det_ = str((c.get("system_callout") or {}).get("detail") or c.get("detail") or "").strip()
                nom_ = f"3-5/8\" stud, framed soffit {det_} (LF)".replace("  ", " ")   # v76: renglón propio
                STUD_ELEM.setdefault(F_36, {})
                STUD_ELEM[F_36][nom_] = STUD_ELEM[F_36].get(nom_, 0.0) + joist
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
        fam[BOARD_FAM.get(c.get("board") or "5/8 regular", F_GYP)] += area   # v80f R80e.19: board del ceiling
        filas.append({"familia": "ceilings", "room": c["room"], "source": src,
                      "operacion": f"{op}; carrying ROUNDUP(({round(run, 3)}-1)/{round(c_oc, 3)})+1 = {n_c} x "
                                   f"{round(lc, 3)} = {round(carry, 2)}{' (polígono: cuerda media área/ancho)' if poligono else ''}; "
                                   f"hangers {n_c} x (ROUNDUP(({round(lc, 3)}-1)/{round(h_oc, 3)})+1 = {n_h}) = {hang} x "
                                   f"drop {drop} ({dr['source']}) = {round(hang * drop, 2)} LF; board {area} SF"})


def _trim_lf(t):
    """v78 (R78.2): en trim_items `lf` es el TOTAL del renglón y `qty` es solo informativo (conteo de piezas /
    esquinas). Antes se sumaba lf x qty y un lector que escribía lf total + qty conteo inflaba el trim qty veces.
    Por pieza: `lf_each` + `qty` (entero >= 1) -> total = lf_each x qty; si vienen lf y lf_each deben cuadrar
    (lf == lf_each x qty, tol 0.01) o ValueError. Sin lf ni lf_each = ValueError."""
    ref = t.get("ref", "trim")
    if t.get("lf_each") is not None:
        q = t.get("qty")
        if q is None or isinstance(q, bool) or float(q) != int(float(q)) or int(float(q)) < 1:
            raise ValueError(f"{ref}: lf_each exige qty entero >= 1 (total = lf_each x qty)")
        q = int(float(q))
        tot = float(t["lf_each"]) * q
        if t.get("lf") is not None and abs(float(t["lf"]) - tot) > 0.01:
            raise ValueError(f"{ref}: lf {t['lf']} != lf_each {t['lf_each']} x qty {q} = {round(tot, 3)} "
                             f"(lf es el TOTAL; R78.2)")
        return tot, f"{t['lf_each']} x {q} = {round(tot, 2)}"
    if t.get("lf") is None:
        raise ValueError(f"{ref}: trim sin lf (total) ni lf_each + qty")
    tot = float(t["lf"])
    q = f" (qty {t['qty']} informativo)" if t.get("qty") not in (None, 1) else ""
    return tot, f"{t['lf']} LF total{q} = {round(tot, 2)}"


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
        lf, op = _trim_lf(t)                             # v78 R78.2: lf = TOTAL; qty informativo
        fam[F_TRIM] += lf
        filas.append({"familia": F_TRIM, "ref": t["ref"], "kind": t["kind"], "source": src,
                      "operacion": op})
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
                             f"— glass mat detrás de la canopy (detalle de la banda 'GLASS-MAT'; banda sin glass mat = canopies[].band.sheathing none con source N/HOJA + img, R78.13)")


def _fascia_sheathing(data, fam, filas):
    for s_ in data.get("plywood_strips") or []:
        if "fascia" in str(s_.get("ref", "")).lower():
            raise ValueError(f"plywood_strip '{s_['ref']}': el sheathing de fascia_box lo genera canon.py (v63)")
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        if w.get("element") != "fascia_box":
            continue
        hs = str(w.get("height_source") or "").strip()
        if not hs:
            raise ValueError(f"{w['id']}: fascia_box sin height_source (T/STUD - B/STUD de la fascia, detalle del "
                             f"fascia box)")
        sf = float(w["length_ft"]) * float(w["height_ft"])
        _ply(fam, "frt_5_8_ext", sf, "canopy_soffit")
        filas.append({"familia": "FRT plywood (SF)", "ref": w["id"], "source": hs, "material": "frt_5_8_ext",
                      "operacion": f"fascia_box sheathing {w['length_ft']} x {w['height_ft']} = {round(sf, 2)} SF "
                                   f"(5/8\" ext. grade FRT plywood, {hs})"})
        # v78 (R78.14): plywood del FONDO del fascia box (el detalle lo dibuja bajo los studs): L x sheathing_bottom_ft
        # al MISMO material del sheathing de la fascia; {value, source N/HOJA, op} obligatorio.
        sb = w.get("sheathing_bottom_ft")
        if sb is not None:
            if not isinstance(sb, dict) or not RX_NHOJA.search(str(sb.get("source") or "")) or \
                    not str(sb.get("op") or "").strip() or isinstance(sb.get("value"), bool) or \
                    not isinstance(sb.get("value"), (int, float)) or float(sb["value"]) <= 0:
                raise ValueError(f"{w['id']}: sheathing_bottom_ft debe ser {{value > 0, source N/HOJA, op}} (fondo "
                                 f"del fascia box medido en su detalle, R78.14)")
            sfb = float(w["length_ft"]) * float(sb["value"])
            _ply(fam, "frt_5_8_ext", sfb, "canopy_soffit")
            filas.append({"familia": "FRT plywood (SF)", "ref": f"{w['id']} bottom", "source": sb["source"],
                          "material": "frt_5_8_ext",
                          "operacion": f"fascia_box bottom {w['length_ft']} x {sb['value']} = {round(sfb, 2)} SF "
                                       f"({sb['op']})"})


def _column_wrap_sheathing(data, fam, filas):
    """v76 (R76.2): sheathing de column wrap / pier sin board = Σ faces_ft x alto (lo declara walls[].sheathing)."""
    for w, mat, sf, op in chequeos_v76.sheathing_column_wraps(data):
        _ply(fam, mat, sf, "column_wrap")
        filas.append({"familia": F_PLY, "ref": w["id"], "source": w["sheathing"]["source"], "material": mat,
                      "operacion": f"column_wrap sheathing {op} (R76.2)"})


def _opening_substrate(data, fam, filas):
    """v76 (R76.4): strip de substrate en head / jambs (/ sill) de aberturas exteriores con label de plywood.
    Bordes: storefront = R.O. + jambs contra wall x head (en un pier el plywood es otra decisión); ventana / door /
    ATM = R.O. + 2 x (head - sill) + R.O. si substrate.sill true. SF = bordes x opening_substrate_width_ft."""
    ops = [op for op in chequeos_v76.aberturas_ext(data, accesorios.es_exterior)
           if isinstance(op.get("substrate"), dict) and chequeos_v76.RX_PLY.search(str(op["substrate"]["label"]))]
    if not ops:
        return
    wd = data["constants"]["opening_substrate_width_ft"]
    for op in ops:
        sb = op["substrate"]
        mat = sb.get("material")
        if mat not in PLY_NAMES:
            raise ValueError(f"{op.get('ref')}: substrate.material {mat!r} fuera de {sorted(PLY_NAMES)} (R76.4)")
        ro = float(op["ro_w_ft"])
        if str(op.get("kind")) == "storefront":
            nj = accesorios._wall_jambs(op) if op.get("jambs") is not None else 0
            e = ro + nj * float(op["head_ft"])
            op_t = f"R.O. {ro} + {nj} jamb(s) contra wall x {op['head_ft']}"
        else:
            hj = float(op["head_ft"]) - float(op.get("sill_ft", 0) or 0)
            e = ro + 2 * hj + (ro if sb.get("sill") else 0.0)
            op_t = f"R.O. {ro} + 2 x {round(hj, 4)}" + (f" + sill {ro}" if sb.get("sill") else "")
        sf = e * float(wd["value"])
        _ply(fam, mat, sf, "substrate")
        filas.append({"familia": F_PLY, "ref": f"{op.get('ref')} substrate", "source": sb["source"], "material": mat,
                      "operacion": f"opening substrate ({op_t}) = {round(e, 3)} LF x {wd['value']} = {round(sf, 2)} SF "
                                   f"(R76.4)"})


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


def _banda_sin_sheathing(data, c):
    """v78 (R78.13): la banda de canopy lleva glass mat salvo que el detalle de ESA banda no lo rotule:
    `canopies[].band.sheathing: "none"` (o `band.sheathing: "none"` para todas) con {source N/HOJA, img}. Sin fuente
    N/HOJA o sin img = error; cualquier otro valor de sheathing distinto de "none" no se acepta aquí."""
    for b, ctx in ((c.get("band"), f"canopy {c.get('id')}.band"), (data.get("band"), "band")):
        if not isinstance(b, dict) or "sheathing" not in b:
            continue
        sh = str(b.get("sheathing") or "").strip().lower()
        if sh != "none":
            raise ValueError(f"{ctx}.sheathing '{b.get('sheathing')}': solo se declara \"none\" (banda sin glass mat "
                             f"porque el detalle no lo rotula); el glass mat de la banda es el default (R78.13)")
        if not RX_NHOJA.search(str(b.get("source") or "")) or not str(b.get("img") or "").strip():
            raise ValueError(f"{ctx}.sheathing none sin {{source N/HOJA, img}}: el detalle de la banda que NO rotula "
                             f"sheathing es obligatorio (R78.13)")
        return True
    return False


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
                             "mat va en la cara del stud, altura = T/STUD - B/STUD del detalle de la banda, "
                             "no T/CANOPY - B/CANOPY de la elevación (v65)")
        band_h = float(ts["value"]) - float(bs["value"])
        bh = bd.get("height_ft")
        if isinstance(bh, dict) and abs(float(bh["value"]) - band_h) > 0.01:
            raise ValueError(f"band.height_ft {bh['value']} != T/STUD - B/STUD {round(band_h, 3)}")
    band_por_fac = {k: 0.0 for k in fac}
    band_gm_fac = {k: 0.0 for k in fac}                # v78 (R78.13): banda que SÍ lleva glass mat
    for c in can:
        if c.get("facade") not in fac:
            raise ValueError(f"canopy {c.get('id')}: facade '{c.get('facade')}' no declarada")
        _src(c, f"canopy {c.get('id')}")
        band_por_fac[c["facade"]] += float(c["band_lf"])
        if not _banda_sin_sheathing(data, c):
            band_gm_fac[c["facade"]] += float(c["band_lf"])
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
        band_gm = band_gm_fac[k] * band_h               # v78 (R78.13): banda sheathing "none" no carga glass mat
        nail = float(f["solid_lf"]) * float(f["height_nailbase_ft"]) - float(f.get("openings_sf", 0)) - band
        fam["5/8\" glass mat sheathing"] += base + band_gm
        _ply(fam, "nailbase_5_8_polyiso", nail, "nailbase")
        sin = f" (banda sin sheathing {round(band - band_gm, 2)} SF: no carga glass mat)" if band - band_gm > EPS else ""
        filas.append({"familia": "exterior", "facade": k, "source": src,
                      "operacion": f"glass mat base {round(base, 2)} + banda {band_gm_fac[k]} x {band_h} = "
                                   f"{round(band_gm, 2)}{sin}; nailbase {f['solid_lf']} x {f['height_nailbase_ft']} - "
                                   f"{f.get('openings_sf', 0)} - banda {round(band, 2)} = {round(nail, 2)}"})


def _plies_blocking(p):
    """v78 R78.32 (arbitraje): plies del FRT blocking del parapet = número de capas que DIBUJA el detalle del remate
    (capas rayadas). Obligatorio como {value, source N/HOJA}; un int suelto o la falta del campo (antes default 0) =
    error, porque el número sale del detalle y no de la costumbre."""
    pb = p.get("plies_blocking")
    if not isinstance(pb, dict) or "value" not in pb or isinstance(pb.get("value"), bool) \
            or not isinstance(pb.get("value"), (int, float)) or float(pb["value"]) != int(pb["value"]) \
            or int(pb["value"]) < 0:
        raise ValueError(f"{p.get('id')}: plies_blocking {{value, source N/HOJA}} obligatorio: value = número entero de "
                         f"plies que DIBUJA el detalle del remate (capas rayadas), no un int suelto ni un default "
                         f"(R78.32)")
    if not chequeos_v76.NHOJA.search(str(pb.get("source") or "")):
        raise ValueError(f"{p.get('id')}: plies_blocking.source debe citar el detalle N/HOJA que dibuja las capas "
                         f"(R78.32)")
    return int(pb["value"])


TOL_PARAPET_LF = 0.05                                  # ft, decisión del usuario W2


def _parapet_lf_base(data, p):
    """v78 (decisión del usuario W2, R78.37): el parapet sigue el largo de la wall exterior de su fachada (mismo eje),
    salvo que un detalle diga otra cosa. Cada parapets[] declara base_walls [ids de walls] (las walls exteriores sobre
    las que corre; facade opcional, se cruza con la facade de cada wall). lf debe ser sum(length_ft) de esas walls
    (tolerancia TOL_PARAPET_LF); si difiere, lf_override {value (= lf), source N/HOJA, motivo} con el detalle que lo dice.
    Devuelve la operación escrita."""
    pid = p.get("id")
    bw = p.get("base_walls")
    if isinstance(bw, str):
        bw = [bw]
    if not isinstance(bw, list) or not bw:
        raise ValueError(f"{pid}: parapet sin base_walls [ids de las walls exteriores de su fachada, mismo eje] (W2 "
                         f"v78: el parapet sigue el largo de la wall exterior que remata)")
    ws = {str(w.get("id")): w for w in data.get("walls") or []}
    tot, partes = 0.0, []
    for i in bw:
        w = ws.get(str(i))
        if w is None:
            raise ValueError(f"{pid}: base_walls '{i}' no existe en walls (W2)")
        if _es_parapet(w):
            raise ValueError(f"{pid}: base_walls '{i}' es el propio parapet; va la wall exterior que remata (W2)")
        fp, fw = p.get("facade"), w.get("facade")
        if fp is not None and fw is not None and str(fp) != str(fw):
            raise ValueError(f"{pid}: base_walls '{i}' es de la facade '{fw}', el parapet de '{fp}' (W2: misma "
                             f"fachada / mismo eje)")
        tot += float(w["length_ft"])
        partes.append(f"{i} {w['length_ft']}")
    lf = float(p["lf"])
    op = f"lf parapet = base_walls {' + '.join(partes)} = {round(tot, 4)}"
    if abs(lf - tot) <= TOL_PARAPET_LF:
        return op
    ov = p.get("lf_override")
    if not isinstance(ov, dict) or not isinstance(ov.get("value"), (int, float)) \
            or not chequeos_v76.NHOJA.search(str(ov.get("source") or "")) or not str(ov.get("motivo") or "").strip():
        raise ValueError(f"{pid}: lf {lf} != largo de sus base_walls {round(tot, 4)} (W2 v78: el parapet sigue el largo "
                         f"de la wall exterior de su fachada) sin lf_override {{value, source N/HOJA, motivo}}")
    if abs(float(ov["value"]) - lf) > 0.01:
        raise ValueError(f"{pid}: lf_override.value {ov['value']} != lf {lf} (W2)")
    return f"{op}; lf_override {lf} ({ov['source']}: {ov['motivo']})"


def _board_base(w, f):
    """v78 R78.33 (ii): base de la pieza de board de una face sobre el piso. face.board_base_ft manda; en un
    door_bulkhead (o una face medida desde el piso con abertura debajo) la pieza arranca en el head de la abertura
    (wall.head_ft o el head_ft más alto de sus openings). None = la pieza arranca en el piso."""
    if f.get("board_base_ft") is not None:
        return float(f["board_base_ft"])
    if w.get("element") == "door_bulkhead":
        hs = [w.get("head_ft")] + [o.get("head_ft") for o in w.get("openings") or [] if isinstance(o, dict)]
        hs = [float(h) for h in hs if isinstance(h, (int, float))]
        return max(hs) if hs else None
    return None


def _r80_11_edge(data):
    """v80 (R80.11): el edge blocking no se omite en silencio: constants.sheet_len_ft {value, source} o
    edge_blocking_none_reason que cite el detalle de blocking revisado (N/HOJA) y por qué no aplica. Sin ninguno la
    familia salía 0 sin aviso (una corrida perdió todo el blocking de borde)."""
    if (data.get("constants") or {}).get("sheet_len_ft") is None and \
            not RX_NHOJA.search(str(data.get("edge_blocking_none_reason") or "")):
        raise ValueError("constants.sheet_len_ft {value, source} (stud blocking en el borde del gypboard, R78.33) o "
                         "edge_blocking_none_reason con el N/HOJA del detalle de blocking revisado y por qué no aplica "
                         "(R80.11: sin ninguno el blocking de borde salía 0 en silencio)")


def _edge_blocking_wall(w, L_hoja):
    """v78 R78.33 stud blocking en el borde del gypboard (sheet_len_ft): (i) LF = largo de la(s) face(s) cuya PIEZA de
    board es más alta que la hoja (face.length_ft si la face es parcial; si no, el largo del wall), por stud row: con
    1 row cuenta el lado más largo (un blocking sirve a las dos faces), con N rows los N lados más largos; (ii) altura
    de la pieza = height_ft - base (board_base_ft o el head de la abertura en un door_bulkhead). Un door_bulkhead con
    face > hoja medida desde el piso sin base declarada = error."""
    L = float(w.get("length_ft") or 0.0)
    por_lado, ops = {}, []
    for f in w.get("faces") or []:
        h = float(f["height_ft"])
        b = _board_base(w, f)
        if b is None and w.get("element") == "door_bulkhead" and h > L_hoja + EPS:
            raise ValueError(f"{w.get('id')}: door_bulkhead con face {h} ft > hoja {L_hoja} ft sin board_base_ft ni "
                             f"head_ft: la pieza de board arranca en el head de la abertura (R78.33)")
        pieza = h - (b or 0.0)
        if pieza <= L_hoja + EPS:
            continue
        lf = float(f["length_ft"]) if f.get("length_ft") is not None else L
        lado = str(f.get("side") or "A").upper()
        por_lado[lado] = por_lado.get(lado, 0.0) + lf
        ops.append(f"{lado} {round(lf, 2)} (pieza {round(pieza, 2)})")
    if not por_lado:
        return 0.0, ""
    vals = sorted((min(v, L) if k != "END" and L > EPS else v for k, v in por_lado.items()), reverse=True)
    rows = max(1, int(w.get("rows", 1) or 1))
    lf = sum(vals[:rows])
    return lf, f"[{', '.join(ops)}] x {min(rows, len(vals))} row(s) = {round(lf, 2)}"


def _parapets_blocking(data, fam, filas, avisos):
    bay = _c(data, "stud_bay_in", 14.375)
    for p in data.get("parapets") or []:
        src = _src(p, p["id"])
        lf_op = _parapet_lf_base(data, p)                # v78 W2 (R78.37): lf = largo de su(s) wall(s) de base
        sh = float(p["lf"]) * float(p["roofside_h_ft"])
        nply = _plies_blocking(p)                        # v78 R78.32: {value, source N/HOJA} obligatorio
        bl = float(p["lf"]) * nply
        fam["5/8\" EXTERIOR gyp sheathing"] += sh
        fam["FRT blocking"] += bl
        filas.append({"familia": "parapet", "id": p["id"], "source": src,
                      "operacion": f"{lf_op}; ext gyp {p['lf']} x {p['roofside_h_ft']} = {round(sh, 2)}; FRT "
                                   f"blocking {p['lf']} x {nply} plies = {round(bl, 2)}"})
    sl = data.get("constants", {}).get("sheet_len_ft")
    if sl is not None:
        L_hoja = _c(data, "sheet_len_ft")
        edge, ops = 0.0, []
        for w in data.get("walls") or []:
            lf_w, op_w = _edge_blocking_wall(w, L_hoja)   # v78 R78.33: por pieza de board y por face
            if lf_w > EPS:
                edge += lf_w
                ops.append(f"{w.get('id')} {op_w}")
        fam["metal stud blocking (362CR / STUD BLOCKING)"] += edge
        BLK_ORIGEN["edge"] = BLK_ORIGEN.get("edge", 0.0) + edge
        filas.append({"familia": "blocking edge", "source": sl["source"],
                      "operacion": f"sum por stud row del largo de las faces cuya pieza de board > {L_hoja} ft = "
                                   f"{round(edge, 2)} (R78.33: {'; '.join(ops[:40]) or 'ninguna'})"})
    for it in data.get("blocking_items") or []:
        src = _src(it, it["ref"])
        mat = it.get("material")
        lab = str(it.get("label") or "")
        if mat == "metal" and it.get("width_in") is not None and float(it["width_in"]) <= bay + EPS and not lab:
            avisos.append(f"{it['ref']}: {it['width_in']}\" <= stud bay {bay}\" sin rótulo -> sin blocking "
                          f"(anclaje a stud)")
            continue
        if mat not in ("metal", "FRT", "wood"):
            raise ValueError(f"{it['ref']}: blocking material metal | FRT | wood (v76: wood = 2X / WOOD sin rótulo FRT)")
        if mat == "FRT" and not RX_MADERA.search(lab):
            raise ValueError(f"{it['ref']}: FRT blocking solo donde el detalle lo rotula (label FRT / FRTW / 2X / WOOD / "
                             f"PLYWOOD) — 'PROVIDE BLOCKING' a secas = metal (58.6, v68)")
        # v76 (arbitraje #24): madera rotulada 2X / WOOD SIN FRT en el rótulo = material wood (su renglón), salvo
        # frt_basis {source N/HOJA} (la nota que hace FRT toda la madera). Nunca se escribe "FRT" en otro campo para
        # que pase un chequeo (regla inviolable 0.R76).
        if mat == "FRT" and not RX_FRT_LABEL.search(lab) and re.search(r"\b2X\b|\bWOOD\b", lab, re.I):
            fb = it.get("frt_basis")
            if not isinstance(fb, dict) or not chequeos_v76.NHOJA.search(str(fb.get("source") or "")):
                raise ValueError(f"{it['ref']}: rótulo '{lab}' sin FRT -> material wood (renglón propio) o frt_basis "
                                 f"{{source N/HOJA}} con la nota que hace FRT toda la madera (v76)")
        if mat == "wood" and (RX_FRT_LABEL.search(lab) or not re.search(r"\b2X\b|\bWOOD\b", lab, re.I)):
            raise ValueError(f"{it['ref']}: material wood = rótulo 2X / WOOD sin FRT (rótulo '{lab}')")
        k = "FRT blocking" if mat in ("FRT", "wood") else "metal stud blocking (362CR / STUD BLOCKING)"
        fam[k] += float(it["lf"])
        if mat == "wood":
            BLK_MADERA["wood"] = BLK_MADERA.get("wood", 0.0) + float(it["lf"])
        if mat == "metal":
            BLK_ORIGEN["items"] = BLK_ORIGEN.get("items", 0.0) + float(it["lf"])
        filas.append({"familia": k, "ref": it["ref"], "source": src, "operacion": f"{it['lf']} LF"})
    for it in data.get("misc_items") or []:   # v80f (R80e.20): miembros dibujados en un detalle (braces, box beam, joists)
        src = _src(it, it["ref"])
        if it.get("familia") not in FAMS:
            raise ValueError(f"{it['ref']}: misc_items.familia debe ser una de FAMS (vino {it.get('familia')!r})")
        if not str(it.get("op") or "").strip():
            raise ValueError(f"{it['ref']}: misc_items sin op (operación DERIVADA)")
        fam[it["familia"]] += float(it["qty"])
        filas.append({"familia": it["familia"], "ref": it["ref"], "source": src, "operacion": it["op"]})
    for s in data.get("plywood_strips") or []:
        src = _src(s, s["ref"])
        mat = _strip_material(s)
        sf = float(s["lf"]) * float(s["width_ft"])
        _ply(fam, mat, sf, _uso_strip(s))
        filas.append({"familia": "FRT plywood (SF)", "ref": s["ref"], "source": src, "material": mat,
                      "operacion": f"strip {s['lf']} x {s['width_ft']} = {round(sf, 2)} SF (no es blocking ni sill)"})


FAMS = ["2-1/2\" stud", "8\" stud (todos los gauges)", "6\" stud (todos los gauges)", F_36, "1-5/8\" stud", F_PAR,
        "bottom track (todos)", "top / deflection track (todos)", "track de ceilings / soffits",
        "bracing C.R. channel", "purlin (track to deck)", "header / box beam", "sill track",
        "furring channel", "carrying channel", "hanger wire", F_GYP,
        "5/8\" gyp MOISTURE RESISTANT", "ballistic panel", "3/8\" gyp board", "5/8\" glass mat sheathing",
        "5/8\" EXTERIOR gyp sheathing", "1/2\" EXTERIOR gyp sheathing", "FRT plywood (SF)", "FRT blocking",
        "5/8\" gyp board Type X", "5/8\" gyp Type X W.R.",   # v80f R80e.18
        F_J8, F_MT, F_CT, F_CM, F_AM,   # v80f R80e.20: 8" joist, USG drywall grid
        *F_NEW27,   # v80n R80e.27
        "metal stud blocking (362CR / STUD BLOCKING)", F_TRIM, "cement board", F_FRP, F_SEAL, F_L5]
# familias que DEBEN salir de canon.py con número (PROTOCOLO_v62 §6); framed openings MEP sale de
# framed_openings.py y se agrega con --fo
# v80e: 8" stud y 1/2" exterior gyp sheathing son familias opcionales (solo si el set las dibuja)
OBLIGATORIAS = [f for f in FAMS if f not in ("2-1/2\" stud", "8\" stud (todos los gauges)",
                                             "1/2\" EXTERIOR gyp sheathing", F_L5, F_SEAL,
                                             "5/8\" gyp board Type X", "5/8\" gyp Type X W.R.",
                                             F_J8, F_MT, F_CT, F_CM, F_AM, *F_NEW27)]   # v77c U8: sealant exterior opcional
STUD_FAM = (("parapet", F_PAR), ("2-1/2\"", "2-1/2\" stud"), ("6\"", "6\" stud (todos los gauges)"),
            ("3-5/8\"", F_36), ("1-5/8\"", "1-5/8\" stud"),
            ("8\"", "8\" stud (todos los gauges)"))  # v80e: 8" exterior stud, AL FINAL ('8"' está dentro de '3-5/8"')
BOARD_FAM = {"5/8 regular": F_GYP, "5/8 MR": "5/8\" gyp MOISTURE RESISTANT",
             "ballistic panel": "ballistic panel", "3/8 gyp": "3/8\" gyp board",
             # v80e: caras con cement board (detalle de wall / counter) y sheathing exterior de 1/2" en un wall
             "1/2 cement board": "cement board", "1/2 exterior gyp sheathing": "1/2\" EXTERIOR gyp sheathing",
             # v80f (R80e.18): Type X y Type X W.R. cuando el set / el estimador los pide
             "5/8 type X": "5/8\" gyp board Type X", "5/8 type X WR": "5/8\" gyp Type X W.R."}


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
    _r79_purlin(data)
    PLY.clear()
    PLY_USO.clear()
    BLK_ORIGEN.clear()
    STUD_ELEM.clear()
    BLK_MADERA.clear()
    POLY[0] = _polyiso(data)
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
    _atm_wall(data, fam, filas, st, co)                  # el ATM está en su wall; lo impreso se cuenta (R80.3)
    _jambs_extra(data, fam, filas)
    _kickers(data, fam, filas)
    _column_wraps(data, fam, filas)
    _ceilings(data, fam, filas)
    _exterior(data, fam, filas)
    _r80_11_edge(data)                                   # v80: edge blocking declarado o descartado con N/HOJA
    _parapets_blocking(data, fam, filas, avisos)
    _trim(data, fam, filas)
    _fascia_sheathing(data, fam, filas)
    chequeos_v76.verificar(data, accesorios.es_exterior)   # v76: R76.1-R76.5 (después de las compuertas previas)
    chequeos_v77.verificar(data)                        # v77: R77.4 strips de pier (D3 / D4); v77b: R77.10
    _column_wrap_sheathing(data, fam, filas)            # v76 R76.2
    _opening_substrate(data, fam, filas)                # v76 R76.4
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
    # v73 (R73.3): contexto para los nombres de la plantilla y metal blocking por origen (edge vs notas)
    out["metal_blocking_by_origin"] = {k: round(v, 2) for k, v in BLK_ORIGEN.items() if v > EPS}
    # v76: renglones de stud por elemento (framed soffit) dentro de su familia; plantilla_excel los separa
    out["wood_blocking_lf"] = round(BLK_MADERA.get("wood", 0.0), 2)   # v76: dentro de "FRT blocking", renglón aparte
    out["stud_by_element"] = {f: {n: round(v, 2) for n, v in d.items() if v > EPS} for f, d in STUD_ELEM.items()}
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
    out["excluidas"] = {"batt insulation": "EXCLUDED (criterio del estimador: no insulation)",
                        F_SEAL_AC: EXCL_SEAL_AC}
    if SEAL.get("_ignorado"):
        out["avisos"].append(SEAL["_ignorado"])
    out["partition_types"] = partition_types.partition_types(data, bo)
    chequeos_v75.verificar_r75_5(data)                    # v75: cambio de type colineal en un nodo (R73.10)
    chequeos_v75.verificar_v75(data, out["partition_types"])   # v75: alcove sin esquina; returns desde la cara exterior
    # v75 (R75.2): después de partition_types (el renglón por tamaño = walls de la Partition Takeoff)
    out["track_by_element"] = track_by_element(data, co, fam, out["partition_types"])
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
