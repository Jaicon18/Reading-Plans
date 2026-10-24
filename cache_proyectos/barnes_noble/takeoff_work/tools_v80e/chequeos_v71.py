#!/usr/bin/env python3
"""chequeos_v71.py — compuerta v71 sobre el canon conciliado (arbitraje #19). Genérico: ningún valor de proyecto.

  R71.1  Fachadas: si el canon trae `facades`, `constants.north_arrow` = {value: up|down|left|right, source (N/HOJA o
         HOJA de planta), img} es obligatorio. La letra de la fachada sale de la FLECHA NORTE de la planta; el título de
         una elevación nunca la define (si el título contradice la flecha: RFI, la flecha manda).
  R71.2  Pier / box con dos sistemas se carga UNA vez por parte: dos registros de walls con huella BOX que se solapan
         (>= 50 % del menor) = el mismo box contado dos veces (p. ej. un registro "exterior" y otro interior con
         `parts`). Falla salvo `same_box_ok: "<motivo + N/HOJA>"` en uno de los dos.
  R71.3  Accesorios de door bulkhead (sealant / trim / blocking cuyo `ref` dice bulkhead) van sobre el ANCHO de los
         vanos (Σ length_ft de los door_bulkhead), nunca sobre el run del box beam: LF del ítem > Σ bulkheads = falla.
  R71.5  Un tag nunca se descarta "por ser de otra tarea / lectura": `tags_descartados[].motivo` con ese motivo =
         falla (se mide o se descarta con motivo de PLANO). v78 (R78.15): pasa solo si nombra su `owner`.
  R78.15 Dueño obligatorio: todo tag descartado (`tags_descartados[]`) o grupo / segmento sin tag
         (`walls[].untagged_reason`) cuyo motivo lo remite a otra tarea / otro elemento ("otra tarea", "counted in",
         "adds to", "es <elemento>"...) declara `owner` (id de un wall / run / ceiling / ítem del canon, tag_id de un
         wall, o tarea del canon que lo cuantifica; `part_of` vale como owner de un wall). Sin owner, o con un owner
         que no existe en el canon = falla: el grupo queda sin dueño y nadie lo cuantifica.

Uso:  python3 chequeos_v71.py takeoff_canon.json      rc 0 = sin fallas; rc 1 = fallas (se listan).
"""
import json
import re
import sys

FLECHAS = ("up", "down", "left", "right")
OTRA_TAREA = re.compile(r"other task|otra tarea|otra lectura|another (task|reading)|de la tarea [A-Z]", re.I)
HOJA = re.compile(r"[A-Z]{1,3}-?(?:\d{1,3}\.\d{1,3}|\d{3}[A-Z]?(?![\w.]))")


def _box(w):
    b = w.get("band")
    if not isinstance(b, dict) or str(b.get("ori")).upper() != "BOX":
        return None
    try:
        x0, x1 = sorted((float(b["c0"]), float(b["c1"])))
        y0, y1 = sorted((float(b["lo"]), float(b["hi"])))
    except (KeyError, TypeError, ValueError):
        return None
    return x0, y0, x1, y1


def _solape(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    menor = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return (ix * iy) / menor if menor > 0 else 0.0


def r71_1(canon):
    if not canon.get("facades"):
        return []
    na = (canon.get("constants") or {}).get("north_arrow")
    if not isinstance(na, dict):
        return ["R71.1 hay facades y falta constants.north_arrow {value, source, img}: la fachada sale de la flecha "
                "norte de la planta, no del título de la elevación"]
    f = []
    if na.get("value") not in FLECHAS:
        f.append(f"R71.1 north_arrow.value '{na.get('value')}' no es {FLECHAS}")
    if not HOJA.search(str(na.get("source") or "")):
        f.append("R71.1 north_arrow.source sin hoja (N/HOJA o HOJA de la planta)")
    if not na.get("img"):
        f.append("R71.1 north_arrow sin img (evidencia visual de la flecha)")
    return f


def r71_2(canon):
    ws = [(w, _box(w)) for w in canon.get("walls") or []]
    ws = [(w, b) for w, b in ws if b is not None]
    f = []
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            (a, ba), (b, bb) = ws[i], ws[j]
            if a.get("same_box_ok") or b.get("same_box_ok"):
                continue
            if (a.get("sheet") or "") != (b.get("sheet") or ""):
                continue
            s = _solape(ba, bb)
            if s >= 0.5:
                f.append(f"R71.2 {a['id']} ({a.get('tag')}) y {b['id']} ({b.get('tag')}) son el mismo box "
                         f"(solape {round(s * 100)} %): cada parte del pier se carga UNA vez (parts del registro "
                         f"interior o registro exterior, nunca los dos)")
    return f


def r71_3(canon):
    bh = sum(float(w.get("length_ft") or 0) for w in canon.get("walls") or [] if w.get("element") == "door_bulkhead")
    f = []
    for k in ("sealant_items", "trim_items", "blocking_items"):
        for it in canon.get(k) or []:
            ref = str(it.get("ref") or "")
            if "bulkhead" not in ref.lower() or it.get("bulkhead_run_ok"):
                continue
            lf = float(it.get("lf") or it.get("length_ft") or 0)
            if bh and lf > bh + 0.01:
                f.append(f"R71.3 {k} '{ref[:60]}' LF {round(lf, 2)} > Σ door_bulkhead {round(bh, 2)}: el accesorio "
                         f"del bulkhead va sobre el ancho de los vanos, no sobre el run del box beam")
            elif not bh:
                f.append(f"R71.3 {k} '{ref[:60]}' habla de bulkhead y el canon no trae door_bulkhead")
    return f


def r71_5(canon):
    return [f"R71.5 tag {t.get('id')} descartado por otra tarea / lectura sin owner: medir, descartar con motivo de "
            f"plano o nombrar el owner que lo cuantifica (R78.15)"
            for t in canon.get("tags_descartados") or [] if isinstance(t, dict)
            and OTRA_TAREA.search(str(t.get("motivo") or "")) and not _owners(t.get("owner"))]


# v78 (R78.15): elementos del canon que un motivo puede nombrar como dueño ("es roof_step", "is a fascia_box")
ELEMENTOS = ("roof_step", "ceiling_transition", "soffit_side", "soffit_drop", "soffit_bottom", "ceiling_bulkhead",
             "vestibule_head", "grille_head", "grille_box", "fascia_box", "canopy_soffit", "column_wrap", "pier",
             "chase", "door_bulkhead", "storefront_cripples", "parapet", "framed_soffit", "kicker", "bulkhead")
REMITE = re.compile(OTRA_TAREA.pattern + r"|\b(counted|quantified|included|carried)\s+(in|by|as|with|under)\b"
                    r"|\b(contad|cuantificad|incluid)[oa]s?\s+(en|por|como|con)\b|\bbelongs to\b|"
                    r"\bpertenece a\b|\badds to\b|\bse suma a(l)?\b|\bowned by\b|\blo cuantifica\b|"
                    r"\b(es|is|=)\s+(un |una |a |an |the |el |la )?(" + "|".join(ELEMENTOS) + r")\b", re.I)


def _owners(o):
    if isinstance(o, str):
        o = [o]
    return [str(x).strip() for x in o or [] if str(x).strip()] if isinstance(o, list) else []


def ids_canon(canon):
    """Ids a los que un owner puede apuntar: walls / runs / parapets / facades / canopies (id), ceilings y tile_base
    (room / id), ítems (ref), tag_ids de los walls y las tareas del canon (task / tareas)."""
    ids = set()
    for k in ("walls", "runs", "parapets", "facades", "canopies", "ceilings", "openings_extra", "blocking_items",
              "plywood_strips", "trim_items", "sealant_items", "level5_items", "access_panels", "wet_fixtures",
              "tile_base", "kickers", "kicker_runs"):
        for x in canon.get(k) or []:
            if not isinstance(x, dict):
                continue
            for c in ("id", "ref", "room"):
                if str(x.get(c) or "").strip():
                    ids.add(str(x[c]).strip())
            ids.update(str(t).strip() for t in x.get("tag_ids") or [] if str(t).strip())
            for o in x.get("openings") or []:
                if isinstance(o, dict) and str(o.get("ref") or "").strip():
                    ids.add(str(o["ref"]).strip())
    for k in ("task", "tasks", "tareas"):
        v = canon.get(k)
        if isinstance(v, dict):
            for t in v:
                ids.update({str(t), re.sub(r"\.json$", "", str(t))})
        elif isinstance(v, list):
            ids.update(str(t.get("id") if isinstance(t, dict) else t) for t in v)
    return ids


def r78_15(canon):
    ids = ids_canon(canon)
    f = []

    def chk(qué, yo, motivo, owner):
        ow = _owners(owner)
        if not ow:
            f.append(f"R78.15 {qué} {yo} se remite a otra tarea / elemento ('{str(motivo)[:70]}') sin owner: nombrar "
                     f"el id del canon que lo cuantifica")
            return
        malos = [o for o in ow if o not in ids or o == yo]
        if malos:
            f.append(f"R78.15 {qué} {yo}: owner {malos} no existe en el canon (o es él mismo): el grupo queda sin "
                     f"dueño")

    for t in canon.get("tags_descartados") or []:
        if not isinstance(t, dict):
            continue
        m = str(t.get("motivo") or "")
        if REMITE.search(m) and not (OTRA_TAREA.search(m) and not _owners(t.get("owner"))):   # ese ya es R71.5
            chk("tag descartado", t.get("id"), m, t.get("owner"))
    for w in canon.get("walls") or []:
        if not isinstance(w, dict) or [x for x in (w.get("tag_ids") or []) if x]:
            continue
        m = str(w.get("untagged_reason") or "")
        if m and REMITE.search(m):
            chk("grupo sin tag", w.get("id"), m, w.get("owner") or w.get("part_of"))
    return f


def revisar(canon):
    fallas = r71_1(canon) + r71_2(canon) + r71_3(canon) + r71_5(canon) + r78_15(canon)
    return {"fallas": fallas, "avisos": []}


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    r = revisar(json.load(open(argv[1])))
    for x in r["fallas"]:
        print("FALLA", x)
    print("OK" if not r["fallas"] else f"{len(r['fallas'])} falla(s)")
    return 1 if r["fallas"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
