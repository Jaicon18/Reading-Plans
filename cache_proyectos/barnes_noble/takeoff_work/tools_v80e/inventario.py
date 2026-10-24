#!/usr/bin/env python3
"""inventario.py v63 — INVENTARIO CERRADO de walls contra la planta. Obligatoria (bitacora.py).

Por qué existe (arbitraje #13, 16-oct-2026): con el mismo skill v62 y el mismo plano, #13A y #13B
sacaron <n> vs <n> LF de track, <n> vs <n> SF de MR y <n> vs <n> LF de 1-5/8". Todas las
diferencias vinieron de QUÉ walls existen y dónde empiezan/terminan, no de las fórmulas:
  - #13B corrió un wall <n> ft desde la cara de un jog exterior cuando el wall arranca
    en esa cara (cota impresa en la planta): +<n> ft x <n> rows.  -> solape PARALELO con otro wall.
  - #13A un stub de <n> ft entrando al wall que lo recibe (planta: <n>). -> solape en T más allá del
    espesor del wall que recibe.
  - #13B partió los exterior walls en "pieza baja" + "pieza alta" en la canopy beam (varias grid
    lines): +<n> LF de bottom y de top track con ids nuevos.     -> walls APILADOS en la misma huella.
  - #13B cargó MR (5/8" MR) al nicho del drinking fountain del corridor (+<n> SF): el detalle de MR pide
    "BEHIND TOILET AND LAVATORY" y los dos van en las faces del chase (enlarged plan).
  - #13B puso purlin en los door bulkheads (perpendiculares al flute, como los stubs que no la
    llevan) y en una 2.ª fila del roof step: +<n> LF.
  - #13B (bug propio): dos walls tomaron la altura del HI por un id viejo -> altura por zona.

Cada regla es determinista: el agente solo MIDE (banda en la planta, zona, fixture) y la tool decide.

ENTRADA: takeoff_canon.json con, además del esquema v62:
  constants.plan_scale_pt_per_ft {value, source}       (A02.01 1/4" = 1'-0" -> 18 pt/ft)
  constants.deck_flute_dir {value: "H"|"V", source}    (dirección del flute en el sistema de la planta)
  constants.deck_zones {zona: {stud_h_ft, source}}     (opcional; S2.20 B.O.D. − d por zona)
  constants.canopy_beam_split {value: false|true, source}  (OBLIGATORIA si algún wall declara canopy_beam)
                  v80 (R80.2): value true exige split_track_detail {source N/HOJA, text con TRACK} impreso en la viga
  walls[].band = {sheet, ori: "H"|"V", c0, c1, lo, hi}  (pt de la hoja como se ve; H: y entre c0-c1,
                  x entre lo-hi; V: x entre c0-c1, y entre lo-hi). Obligatoria en ELEMENTOS_BANDA.
  walls[].length_printed_ft (cota impresa: manda; la banda solo avisa DISCREPANCIA)
  walls[].adjacent_to + adjacent_source (dos rows de un chase / wall doble dibujados pegados)
  band.ori "BOX" solo para pier / column_wrap / chase (huella; no entra al chequeo de solapes)
  walls[].zone (si hay deck_zones) · walls[].canopy_beam {tos_ft, depth_ft, source} · walls[].split_of
  wet_fixtures = [{ref, kind, wall, room, source}]  (MR solo detrás de estos fixtures)
SALIDA: inventario_out.json {ok, walls, lf_por_tag, avisos, rfi}; ValueError con el motivo si algo falla.

Uso:  python3 inventario.py takeoff_canon.json [salida.json]
"""
import json
import math
import sys

ELEMENTOS_BANDA = ("wall", "pier", "storefront_cripples", "door_bulkhead", "column_wrap", "chase",
                   "vestibule_head", "grille_head", "grille_box")
PURLIN_ELEMS = ("wall", "door_bulkhead", "vestibule_head", "roof_step", "chase",
                "ceiling_transition", "ceiling_bulkhead")   # v66: track a deck de transiciones / bulkheads (10/A09.33)
MR_FIXTURES = ("water_closet", "lavatory", "urinal", "mop_sink", "shower")    # F/A08.01 + 53.x
TOL_FT = 0.15          # largo banda vs canon: TOL_FT más el 1 % del largo
JUNTA_FT = 0.10        # holgura de junta permitida más allá del espesor del wall que recibe
PARALELO_FT = 0.25     # dos walls paralelos a menos de esto y corriendo juntos = el mismo framing


def _const(data, k):
    c = (data.get("constants") or {}).get(k)
    if c is None:
        return None
    if not isinstance(c, dict) or "value" not in c or not str(c.get("source") or "").strip():
        raise ValueError(f"constants.{k} debe ser {{value, source}}")
    return c["value"]


def _rect(b):
    """(x0, y0, x1, y1) de la banda."""
    c0, c1, lo, hi = (float(b[k]) for k in ("c0", "c1", "lo", "hi"))
    if c1 <= c0 or hi <= lo:
        raise ValueError(f"banda {b}: c1 <= c0 o hi <= lo")
    return (lo, c0, hi, c1) if b["ori"] == "H" else (c0, lo, c1, hi)


def _bandas(data, scale, avisos):
    out = []
    for w in data.get("walls") or []:
        if w.get("element", "wall") not in ELEMENTOS_BANDA:
            continue
        b = w.get("band")
        if not isinstance(b, dict):
            raise ValueError(f"{w['id']}: falta band {{sheet, ori, c0, c1, lo, hi}} — el inventario se verifica "
                             f"contra la planta (v63, #13A/#13B: walls solapados o apilados)")
        if b.get("ori") not in ("H", "V", "BOX", "D") or not str(b.get("sheet") or "").strip():
            raise ValueError(f"{w['id']}: band.ori H|V|BOX|D y band.sheet obligatorios")
        if b["ori"] == "D":                             # 14B: wall diagonal (ni H ni V): eje p0-p1 en pt
            p0, p1 = b.get("p0"), b.get("p1")
            if not (isinstance(p0, list) and isinstance(p1, list) and len(p0) == 2 and len(p1) == 2):
                raise ValueError(f"{w['id']}: band D exige p0 [x,y] y p1 [x,y] (eje del wall en pt)")
            Ld = math.hypot(float(p1[0]) - float(p0[0]), float(p1[1]) - float(p0[1])) / scale
            L = float(w.get("length_printed_ft") or w["length_ft"])
            if abs(Ld - L) > TOL_FT + 0.01 * L:
                raise ValueError(f"{w['id']}: banda D {round(Ld, 3)} ft != length_ft {L} (plano marcado vs canon)")
            continue                                    # sin chequeo de solapes ortogonales (diagonal)
        if b["ori"] == "BOX":                           # pier / column wrap / nicho: huella, sin largo lineal
            if w.get("element", "wall") == "wall":
                raise ValueError(f"{w['id']}: un wall se marca H o V (BOX solo pier, column_wrap, chase)")
            continue
        L = float(w.get("length_printed_ft") or w["length_ft"])
        if abs(float(w["length_ft"]) - L) > 0.01:
            raise ValueError(f"{w['id']}: length_ft {w['length_ft']} != length_printed_ft {L} (la cota manda)")
        Lb = (float(b["hi"]) - float(b["lo"])) / scale
        if abs(Lb - L) > TOL_FT + 0.01 * L:
            if w.get("length_printed_ft"):
                avisos.append(f"DISCREPANCIA {w['id']}: dibujo {round(Lb, 3)} ft vs cota {L} (manda la cota)")
            else:
                raise ValueError(f"{w['id']}: banda {round(Lb, 3)} ft != length_ft {L} (plano marcado vs canon, #13B)")
        out.append((w, b, _rect(b)))
    return out


def _solapes(bandas, scale):
    junta = JUNTA_FT * scale
    par = PARALELO_FT * scale
    for i, (w1, b1, r1) in enumerate(bandas):
        for w2, b2, r2 in bandas[i + 1:]:
            if b1["sheet"] != b2["sheet"]:
                continue
            if w1.get("split_of") == w2["id"] or w2.get("split_of") == w1["id"] or \
                    (w1.get("split_of") and w1.get("split_of") == w2.get("split_of")):
                continue                                      # piezas de un split declarado (se ven abajo)
            ix0, iy0 = max(r1[0], r2[0]), max(r1[1], r2[1])
            ix1, iy1 = min(r1[2], r2[2]), min(r1[3], r2[3])
            if b1["ori"] == b2["ori"]:
                # paralelos: solape a lo largo (lo-hi) con las bandas tocándose o cruzándose de través
                gap = max(r1[1], r2[1]) - min(r1[3], r2[3]) if b1["ori"] == "H" else \
                    max(r1[0], r2[0]) - min(r1[2], r2[2])
                largo = (ix1 - ix0) if b1["ori"] == "H" else (iy1 - iy0)
                adj = w1.get("adjacent_to") == w2["id"] or w2.get("adjacent_to") == w1["id"]
                if adj and not str((w1 if w1.get("adjacent_to") else w2).get("adjacent_source") or "").strip():
                    raise ValueError(f"{w1['id']}/{w2['id']}: adjacent_to sin adjacent_source (detalle del tipo)")
                if not adj and gap <= par and largo > junta + 0.4 * scale:
                    raise ValueError(f"{w1['id']} y {w2['id']}: corren uno junto al otro {round(largo / scale, 2)} ft "
                                     f"(mismo framing contado dos veces: un wall sobre el jog de otro)")
                continue
            if ix1 <= ix0 or iy1 <= iy0:
                continue
            # perpendiculares: cada uno puede entrar al otro como máximo el espesor del otro + junta
            for (wa, ba, ra), (wb, bb, rb) in (((w1, b1, r1), (w2, b2, r2)), ((w2, b2, r2), (w1, b1, r1))):
                pen = (ix1 - ix0) if ba["ori"] == "H" else (iy1 - iy0)
                esp_b = (rb[2] - rb[0]) if bb["ori"] == "V" else (rb[3] - rb[1])
                if pen > esp_b + junta:
                    raise ValueError(f"{wa['id']} entra {round(pen / scale, 2)} ft en {wb['id']} (espesor "
                                     f"{round(esp_b / scale, 2)} ft): largo medido hasta dentro del otro wall "
                                     f"(#13A B2K/A1K-S2)")


def _apilados(data, bandas, scale):
    """Dos walls en la misma huella = split vertical. Solo con canopy_beam_split true y split_of."""
    split = _const(data, "canopy_beam_split")
    con_beam = [w for w in data.get("walls") or [] if w.get("canopy_beam")]
    if con_beam and split is None:
        raise ValueError("constants.canopy_beam_split {value, source} obligatoria: hay walls con canopy_beam "
                         "(decisión única del proyecto, no de cada agente — #13A continuo / #13B partido)")
    import criterios                     # v80 (R80.2): split solo con track IMPRESO en la viga; Σ filas = padre
    ok, motivo = criterios.split_valido((data.get("constants") or {}).get("canopy_beam_split"))
    if not ok:
        raise ValueError(motivo)
    errs = criterios.filas_dentro_del_padre(data.get("walls") or [], esc=float(scale or 18.0))
    if errs:
        raise ValueError("filas apiladas (split_of): " + "; ".join(errs[:6]) + " — R80.2: la suma de los tramos "
                         "split_of de un nivel es el wall padre")
    ids = {w["id"]: w for w in data.get("walls") or []}
    for w in data.get("walls") or []:
        p = w.get("split_of")
        if p is None:
            continue
        if not split:
            raise ValueError(f"{w['id']}: split_of {p} con canopy_beam_split false — el wall va CONTINUO "
                             f"(una pieza, un bottom y un top track)")
        if p not in ids:
            raise ValueError(f"{w['id']}: split_of {p} no existe")
    vistos = {}
    for w, b, r in bandas:
        if w.get("split_of"):
            continue
        k = (b["sheet"], b["ori"], round(r[0]), round(r[1]), round(r[2]), round(r[3]))
        if k in vistos:
            raise ValueError(f"{w['id']} y {vistos[k]}: misma huella sin split_of (wall duplicado o pieza alta "
                             f"suelta — #13B X-*u)")
        vistos[k] = w["id"]


def _zonas(data):
    zs = _const(data, "deck_zones")
    if zs is None:
        return
    for w in data.get("walls") or []:
        z = w.get("zone")
        if z is None:
            continue
        if z not in zs:
            raise ValueError(f"{w['id']}: zone {z} no está en constants.deck_zones")
        h = float(zs[z]["stud_h_ft"])
        if abs(float(w["height_ft"]) - h) > 0.05 and not str(w.get("height_source") or "").strip():
            raise ValueError(f"{w['id']}: height_ft {w['height_ft']} != zona {z} ({h}) sin height_source "
                             f"(#13B B2-2a/b tomaron la altura del HI por un id viejo)")


def _mr(data):
    fx = data.get("wet_fixtures")
    caras_mr = [(w, f) for w in data.get("walls") or [] for f in w.get("faces") or []
                if "MR" in str(f.get("board", "")).upper()]
    if not caras_mr:
        return
    if not fx:
        raise ValueError("hay faces 5/8 MR sin wet_fixtures: MR solo detrás de toilet / lavatory (nota de wet areas del set)")
    pedidas = set()
    for x in fx:
        if x.get("kind") not in MR_FIXTURES:
            raise ValueError(f"wet_fixture {x.get('ref')}: kind {x.get('kind')} no lleva MR "
                             f"({', '.join(MR_FIXTURES)}; un drinking fountain NO — #13B)")
        if not str(x.get("source") or "").strip():
            raise ValueError(f"wet_fixture {x.get('ref')}: falta source")
        pedidas.add((x["wall"], str(x["room"])))
    dadas = {(w["id"], str(f.get("room"))) for w, f in caras_mr}
    sobra, falta = dadas - pedidas, pedidas - dadas
    if sobra:
        raise ValueError(f"faces MR sin fixture detrás: {sorted(sobra)}")
    if falta:
        raise ValueError(f"fixtures sin face MR: {sorted(falta)}")


def _purlin(data, bandas):
    flute = _const(data, "deck_flute_dir")
    if flute is None:
        return
    if flute not in ("H", "V"):
        raise ValueError("deck_flute_dir.value H|V (en el sistema de la banda)")
    import criterios                     # v80 (R80.1): mismo criterio que canon._r79_purlin (tope a acero, filas)
    mal = []
    for w, b, r in bandas:
        if w.get("element", "wall") not in PURLIN_ELEMS:
            continue
        quiere = criterios.purlin_esperado(w, b["ori"], flute)
        if quiere is None:
            continue
        if bool(w.get("purlin")) != quiere:
            mal.append(f"{w['id']}({b['ori']}: purlin {'sí' if quiere else 'no'})")
    if mal:
        raise ValueError(f"purlin = top track a deck PARALELO al flute ({flute}); corregir: {mal} "
                         f"(#13B door bulkheads)")
    runs = {}
    for w in data.get("walls") or []:
        if w.get("element") == "roof_step" and w.get("purlin"):
            k = w.get("straight_run") or w.get("line") or w["id"]
            runs.setdefault(k, []).append(w["id"])
    por = {w["id"]: w for w in data.get("walls") or []}
    dob = {k: v for k, v in runs.items() if len(v) > 1 and
           not any(criterios.filas_purlin_ok(por[a], por[b]) for i, a in enumerate(v) for b in v[i + 1:])}
    if dob:
        raise ValueError(f"roof_step con purlin en más de una fila del mismo run: {dob} — una pieza (59.1)")


def _rfi_split(data):
    """Delta de partir en la canopy beam (para el RFI): track +2 L por familia; stud -studs x depth."""
    out = []
    for w in data.get("walls") or []:
        cb = w.get("canopy_beam")
        if not cb or w.get("split_of"):
            continue
        L = float(w["length_ft"])
        n = math.ceil(L * 12 / float(w.get("oc_in", 16)) - 1e-9) + 1
        out.append({"wall": w["id"], "bottom_track_lf": round(L, 2), "top_track_lf": round(L, 2),
                    "stud_lf": round(-n * float(cb["depth_ft"]), 2), "source": cb.get("source")})
    return out


def verificar(data):
    scale = _const(data, "plan_scale_pt_per_ft")
    if scale is None:
        raise ValueError("constants.plan_scale_pt_per_ft {value, source} obligatoria (v63): sin bandas no hay "
                         "inventario verificable contra la planta")
    scale = float(scale)
    av = []
    import criterios                                     # v80e: cada hoja con su escala
    bandas = []
    for _, sub in criterios.subcanons_por_hoja(data):
        esc_h = criterios.escala_global(sub, scale)
        bh = _bandas(sub, esc_h, av)
        _apilados(sub, bh, esc_h)
        _solapes(bh, esc_h)
        bandas += bh
    _zonas(data)
    _mr(data)
    _purlin(data, bandas)
    lf = {}
    for w in data.get("walls") or []:
        k = f"{w.get('element', 'wall')}:{w.get('tag')}"
        lf[k] = round(lf.get(k, 0.0) + float(w["length_ft"]) * int(w.get("rows", 1)), 2)
    # v74 (R74.1 / R74.5): el inventario avisa lo que la partición va a retipar o descontar, para que la lectura lo
    # corrija en el canon (el type del segmento y el box duplicado son de la lectura, no de la tool).
    try:
        import particion
        dups = particion.duplicados(data.get("walls") or [])
        ctx = particion.contexto([w for w in data.get("walls") or [] if w["id"] not in dups])
        av += [m for _, m in particion.retipar(ctx, scale).values()]
        av += [f"{k} sin tag con la huella del box {v} (con tag): mismo elemento leído dos veces (R74.5); declarar "
               f"part_of" for k, v in dups.items()]
    except ImportError:
        pass
    rfi = _rfi_split(data)
    if rfi and not _const(data, "canopy_beam_split"):
        tot = round(sum(r["bottom_track_lf"] for r in rfi), 2)
        av.append(f"RFI canopy beam en la cavidad (detalles de la banda / canopy): continuo (cargado). Si se parte: "
                  f"+{tot} LF bottom, +{tot} LF top, {round(sum(r['stud_lf'] for r in rfi), 2)} LF 6\" stud")
    return {"ok": True, "walls": len(data.get("walls") or []), "con_banda": len(bandas), "lf_por_tag": lf,
            "avisos": av, "rfi_split": rfi}


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    data = json.load(open(argv[1], encoding="utf-8"))
    try:
        out = verificar(data)
    except ValueError as e:
        print("INVENTARIO RECHAZADO:", e)
        return 1
    if len(argv) == 3:
        open(argv[2], "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
    for a in out["avisos"]:
        print("AVISO", a)
    print(f"INVENTARIO OK: {out['walls']} walls, {out['con_banda']} con banda en planta")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
