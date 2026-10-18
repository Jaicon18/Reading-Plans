#!/usr/bin/env python3
"""etapas.py — control del flujo por etapas (v69): dónde quedó la corrida y compuerta antes del Excel.

Layout de la carpeta de etapas (cada etapa escribe en disco; una corrida cortada se reanuda en la primera etapa
que falte):

  <dir>/1_inventario/inventario.json   (+ inventario.md, recortes/)      ← inventario_tags.py
  <dir>/2_lectura/canon_A.json                                           ← lectura A (subagentes)
  <dir>/2_lectura/canon_B.json                                           ← lectura B (subagentes, sin ver A)
  <dir>/3_revision/revision.json       (+ revision.md, img/)             ← comparar.py
  <dir>/4_canon/takeoff_canon.json     (canon conciliado)                ← estimador / revisión resuelta

También acepta los cinco archivos sueltos en <dir> (layout plano).

Uso:
  python3 etapas.py estado    <dir>   → qué etapa está hecha y cuál sigue (rc 0)
  python3 etapas.py compuerta <dir>   → rc 0 PASA / rc 1 FALLA, con cada motivo
  python3 etapas.py unir <carpeta_fragmentos> <canon_X.json> [--inventario inventario.json]
                                      → une los fragmentos de una lectura (una hoja o grupo de tags por subagente):
                                        listas se concatenan; ids repetidos o constantes distintas = error (rc 1)

unir (v70) da ERROR (rc 1, sin crash) si:
  - una clave es lista en un fragmento y dict / escalar en otro ("<key>: list in X, dict in Y");
  - un escalar distinto entre fragmentos (nombra los dos). Excepción: texto tipo `notes` -> {fragmento: texto} + aviso;
  - band fuera de convención {ori, c0, c1 = caras (perpendicular), lo, hi = extensión}: |c1-c0| > 2 ft x escala en
    un partition (no ceilings / soffits), |hi-lo| vs length_ft x escala > 3 % y > 1 ft (salvo band_length_ok_reason),
    "banda traspuesta" (c0/c1 = extensión, lo/hi = caras). column_wrap / pier (caja) no se chequean;
  - `page` 0-based: el inventario (<carpeta>/../1_inventario/inventario.json, ../../ o --inventario) tiene la hoja
    del wall en la página N y el wall dice N-1;
  - hay lista de aberturas (opening_schedule / opening_list / openings, lista o {items}) y una ref de
    walls[].openings[] u openings_extra[] no está en ella (la tarea de openings escribe las refs primero, Etapa 2a).

La compuerta FALLA si:
  - falta inventario.json, canon_A.json, canon_B.json o revision.json, o alguno no es JSON válido;
  - el inventario tiene recortes NO VERIFICADOS (aviso "PNG NO VERIFICADO" de inventario_tags.py);
  - revision.json es más viejo que el inventario o que alguna lectura (revisión vencida: correr comparar.py otra vez);
  - la revisión no cubre exactamente los partition tags del inventario (fue hecha con otro inventario);
  - algún partition tag del inventario no tiene wall en la lectura A ni en la B y tampoco tiene alerta "tag sin wall";
  - v70: existe <dir>/4_canon/takeoff_canon.json y esquinas.revisar da fallas (R70.2 esquina sin dueño / doble,
    R70.3 hueco colineal sin gaps_ok) -> "esquinas: …".
Avisos (no fallan, se listan): walls sin `sheet` o sin `tag_ids`, tags ambiguos del inventario (no contados),
hojas no inventariables, ítems de revisión pendientes (difieren / solo A / solo B / alertas).
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

ARCHIVOS = [
    ("inventario", "inventario.json", "1_inventario"),
    ("canon_A", "canon_A.json", "2_lectura"),
    ("canon_B", "canon_B.json", "2_lectura"),
    ("revision", "revision.json", "3_revision"),
    ("canon_final", "takeoff_canon.json", "4_canon"),
]
SIGUIENTE = {
    "inventario": "ETAPA 1: python3 inventario_tags.py plano.pdf <dir>/1_inventario",
    "canon_A": "ETAPA 2A: lectura A por subagentes (una hoja o grupo de tags cada uno) -> <dir>/2_lectura/canon_A.json",
    "canon_B": "ETAPA 2B: lectura B independiente (no ve A) -> <dir>/2_lectura/canon_B.json",
    "revision": "ETAPA 3: python3 comparar.py <A> <B> <inventario> <dir>/3_revision --pdf plano.pdf",
    "canon_final": "ETAPA 3→4: resolver revision.md (plano con imagen o ítem del estimador) -> <dir>/4_canon/takeoff_canon.json",
}


def ruta(d, nombre, sub):
    for p in (os.path.join(d, sub, nombre), os.path.join(d, nombre)):
        if os.path.isfile(p):
            return p
    return None


def cargar(d):
    """{clave: (ruta, json|None, error|None)} para los archivos que existen."""
    out = {}
    for k, nombre, sub in ARCHIVOS:
        p = ruta(d, nombre, sub)
        if p is None:
            continue
        try:
            with open(p) as f:
                out[k] = (p, json.load(f), None)
        except (OSError, ValueError) as e:
            out[k] = (p, None, f"{type(e).__name__}: {e}")
    return out


def estado(d):
    a = cargar(d)
    lineas, sig = [], None
    for k, nombre, sub in ARCHIVOS:
        if k in a and a[k][2] is None:
            lineas.append(f"  [x] {k:12s} {a[k][0]}")
        else:
            lineas.append(f"  [ ] {k:12s} " + (f"JSON INVÁLIDO {a[k][0]}" if k in a else "falta"))
            sig = sig or SIGUIENTE[k]
    return lineas, sig or "todas las etapas en disco: correr etapas.py compuerta y después canon.py / Excel"


def compuerta(d):
    """-> (fallas, avisos)."""
    a = cargar(d)
    fallas, avisos = [], []
    for k, nombre, _ in ARCHIVOS[:4]:
        if k not in a:
            fallas.append(f"falta {nombre}")
        elif a[k][2]:
            fallas.append(f"{nombre} no es JSON válido ({a[k][2]})")
    if fallas:
        return fallas, avisos
    inv, ca, cb, rev = (a[k][1] for k in ("inventario", "canon_A", "canon_B", "revision"))

    fallas += [f"inventario: {x}" for x in inv.get("avisos") or [] if str(x).startswith("PNG NO VERIFICADO")]

    t_rev = os.path.getmtime(a["revision"][0])
    for k in ("inventario", "canon_A", "canon_B"):
        if os.path.getmtime(a[k][0]) > t_rev:
            fallas.append(f"revision.json es más viejo que {os.path.basename(a[k][0])}: revisión vencida, "
                          f"correr comparar.py otra vez")

    import comparar as C                       # v70: partition_tag + partition_candidato (PC####)
    tags = C.tags_inventario(inv)
    ids_inv = {o["id"] for o in tags}
    cob = {c.get("tag"): c for c in rev.get("cobertura_tags") or []}
    falt, sobr = sorted(ids_inv - set(cob)), sorted(set(cob) - ids_inv)
    if falt:
        fallas.append(f"{len(falt)} tag(s) del inventario no están en revision.json (revisión hecha con otro "
                      f"inventario): " + ", ".join(falt[:20]) + (" …" if len(falt) > 20 else ""))
    if sobr:
        fallas.append(f"{len(sobr)} tag(s) de revision.json no están en el inventario: " + ", ".join(sobr[:20])
                      + (" …" if len(sobr) > 20 else ""))
    alertados = {(x.get("tag") or {}).get("id") for x in rev.get("alertas") or [] if x.get("kind") == "tag sin wall"}
    for o in tags:
        c = cob.get(o["id"])
        if c is None:
            continue
        con_wall = bool((c.get("A") or {}).get("walls")) or bool((c.get("B") or {}).get("walls"))
        if not con_wall and o["id"] not in alertados:
            fallas.append(f"tag {o['id']} {o.get('type')} ({o.get('sheet')} p.{o.get('page')}) sin wall y sin alerta")

    for lado, c in (("A", ca), ("B", cb)):
        ws = c.get("walls") or []
        sin_sh = [w.get("id") for w in ws if not w.get("sheet")]
        sin_id = [w.get("id") for w in ws if not w.get("tag_ids")]
        if sin_sh:
            avisos.append(f"lectura {lado}: {len(sin_sh)} wall(s) sin `sheet`")
        if sin_id:
            avisos.append(f"lectura {lado}: {len(sin_id)} wall(s) sin `tag_ids` (cruce tag ↔ wall solo por posición)")
    amb = (inv.get("ocurrencias") or {}).get("partition_ambiguo") or []
    if amb:
        avisos.append(f"{len(amb)} tag(s) ambiguo(s) en el inventario (no contados): decide el estimador")
    for h in inv.get("no_inventariables") or []:
        avisos.append(f"hoja NO INVENTARIABLE POR SCRIPT p.{h.get('page')} {h.get('sheet') or ''}: {h.get('motivo')}")
    if "canon_final" in a:                      # v70: R70.2 / R70.3 sobre el canon conciliado (esquinas.py)
        if a["canon_final"][2]:
            fallas.append(f"takeoff_canon.json no es JSON válido ({a['canon_final'][2]})")
        else:
            import esquinas
            fallas += [f"esquinas: {x}" for x in esquinas.revisar(a["canon_final"][1])["fallas"]]
    n = {k: len(rev.get(k) or []) for k in ("difieren", "solo_A", "solo_B", "alertas")}
    if any(n.values()):
        avisos.append("revision.md pendiente para el estimador: " + " · ".join(f"{k} {v}" for k, v in n.items()))
    return fallas, avisos


TEXTO_KEYS = {"notes", "note", "notas", "nota", "comments", "comment", "observaciones", "notas_lectura"}
CARA_MAX_FT = 2.0          # |c1 - c0| de un wall (caras) <= 2 ft
LARGO_TOL_PCT = 0.03       # |hi - lo| vs length_ft x escala: falla si difiere > 3 % Y > 1 ft
LARGO_TOL_FT = 1.0
NO_CARAS = ("ceiling_transition", "ceiling_bulkhead", "soffit_side", "soffit_drop", "soffit_bottom", "canopy_soffit",
            "fascia_box", "ceiling_perimeter", "joist", "roof_step", "vestibule_head", "grille_head")
CAJAS = ("column_wrap", "pier")   # la banda es la caja y length_ft = suma de caras: sin chequeo de convención


def _es_texto(k):
    k = str(k).lower()
    return k in TEXTO_KEYS or k.endswith(("_note", "_notes", "_nota", "_notas"))


def _tipo(v):
    return "list" if isinstance(v, list) else "dict" if isinstance(v, dict) else type(v).__name__


def _fusion_escalar(cont, k, v, f, origen, okey, errores, avisos, ctx):
    """Escalar `v` del fragmento `f` en cont[k]. Texto tipo notes distinto -> {fragmento: texto} + aviso;
    otro escalar distinto -> ERROR con los dos fragmentos."""
    if k not in cont:
        cont[k] = v
        origen[okey] = f
        return
    prev = cont[k]
    if okey in origen.get("_por_fragmento", set()):
        if isinstance(v, str):
            prev[f] = v
            return
    if prev == v:
        return
    if (isinstance(prev, (list, dict)) or isinstance(v, (list, dict))) and _tipo(prev) != _tipo(v):
        errores.append(f"{ctx}: {_tipo(prev)} in {origen.get(okey)}, {_tipo(v)} in {f}")
        return
    if _es_texto(k) and isinstance(prev, str) and isinstance(v, str):
        cont[k] = {origen.get(okey): prev, f: v}
        origen.setdefault("_por_fragmento", set()).add(okey)
        avisos.append(f"{ctx}: texto distinto en {origen.get(okey)} y {f} -> unido como {{fragmento: texto}}")
        return
    errores.append(f"{ctx}: {origen.get(okey)} y {f} traen valores distintos ({prev!r} vs {v!r})")


def _escala(canon):
    v = ((canon.get("constants") or {}).get("plan_scale_pt_per_ft"))
    try:
        return float(v.get("value") if isinstance(v, dict) else v) if v is not None else 18.0
    except (TypeError, ValueError):
        return 18.0


def validar_bandas(canon):
    """v70: convención band = {ori, c0, c1 (caras, perpendicular), lo, hi (extensión)} en pt. -> errores."""
    esc = _escala(canon)
    err = []
    for w in canon.get("walls") or []:
        b = w.get("band")
        if not isinstance(b, dict) or b.get("ori") not in ("H", "V") or w.get("element") in CAJAS:
            continue
        try:
            c0, c1, lo, hi = (float(b[k]) for k in ("c0", "c1", "lo", "hi"))
        except (KeyError, TypeError, ValueError):
            err.append(f"wall {w.get('id')}: band sin c0/c1/lo/hi numéricos ({b})")
            continue
        cara, ext = abs(c1 - c0), abs(hi - lo)
        L = w.get("length_ft")
        Lpt = float(L) * esc if isinstance(L, (int, float)) else None
        es_part = w.get("element", "wall") not in NO_CARAS

        def largo_mal(x):
            return Lpt is not None and abs(x - Lpt) > LARGO_TOL_PCT * Lpt and abs(x - Lpt) > LARGO_TOL_FT * esc
        if Lpt is not None and largo_mal(ext) and not largo_mal(cara) and ext <= CARA_MAX_FT * esc:
            err.append(f"wall {w.get('id')}: banda traspuesta — c0/c1 ({c0}, {c1}) miden la extensión "
                       f"({round(cara / esc, 2)} ft ≈ length_ft {L}) y lo/hi ({lo}, {hi}) las caras; la convención es "
                       f"c0/c1 = caras (perpendicular al wall), lo/hi = extensión")
            continue
        if es_part and cara > CARA_MAX_FT * esc:
            err.append(f"wall {w.get('id')}: |c1 - c0| = {round(cara / esc, 2)} ft > {CARA_MAX_FT} ft — c0/c1 son las "
                       f"CARAS del wall (espesor), no la extensión")
        if largo_mal(ext) and not str(w.get("band_length_ok_reason") or "").strip():
            err.append(f"wall {w.get('id')}: |hi - lo| = {round(ext / esc, 2)} ft vs length_ft {L} (> 3 % y > 1 ft) — "
                       f"corregir la banda o declarar band_length_ok_reason (p. ej. length_source con cota impresa)")
    return err


def _inventario_de(carpeta, ruta_inv=None):
    cands = [ruta_inv] if ruta_inv else [os.path.join(carpeta, "..", "1_inventario", "inventario.json"),
                                         os.path.join(carpeta, "..", "..", "1_inventario", "inventario.json")]
    for p in cands:
        if p and os.path.isfile(p):
            with open(p) as f:
                return json.load(f), p
    return None, None


def _lista_openings(canon):
    """(clave, refs) de la lista de aberturas fijada antes de las tareas de walls, o (None, None)."""
    for k in ("opening_schedule", "opening_list", "openings"):
        v = canon.get(k)
        if isinstance(v, dict):
            v = v.get("items")
        if isinstance(v, list):
            refs = {str(x.get("ref")) if isinstance(x, dict) else str(x) for x in v}
            return k, refs - {"None"}
    return None, None


def validar_openings(canon):
    k, refs = _lista_openings(canon)
    if k is None:
        return []
    usadas = [(w.get("id"), str(o.get("ref"))) for w in canon.get("walls") or [] for o in w.get("openings") or []]
    usadas += [("openings_extra", str(o.get("ref"))) for o in canon.get("openings_extra") or []]
    malas = [f"{wid}: '{r}'" for wid, r in usadas if r not in refs]
    if not malas:
        return []
    return [f"openings: {len(malas)} ref(s) que no están en {k} — la tarea de openings escribe las refs primero "
            f"(Etapa 2a) y las tareas de walls usan ESAS refs: " + "; ".join(malas[:20]) + (" …" if len(malas) > 20 else "")]


def unir(carpeta, inventario=None, avisos=None):
    """Fragmentos *.json de una lectura -> un canon. Listas se concatenan; dicts se fusionan sin pisar un valor
    distinto; ids de walls repetidos = error. v70: tipo distinto entre fragmentos (lista / dict / escalar) = ERROR
    (no crash); notes distintas -> {fragmento: texto} + aviso; convención de band; page 1-based contra el
    inventario; refs de openings contra la lista de aberturas. -> (canon, errores)."""
    avisos = avisos if avisos is not None else []
    out, errores, origen = {}, [], {}
    fs = sorted(f for f in os.listdir(carpeta) if f.endswith(".json"))
    if not fs:
        return None, [f"{carpeta}: sin fragmentos *.json"]
    for f in fs:
        with open(os.path.join(carpeta, f)) as fh:
            frag = json.load(fh)
        for k, v in frag.items():
            if k in out and _tipo(out[k]) != _tipo(v) and (isinstance(v, (list, dict)) or
                                                           isinstance(out[k], list) or
                                                           (isinstance(out[k], dict) and
                                                            (k, None) not in origen.get("_por_fragmento", set()))):
                errores.append(f"{k}: {_tipo(out[k])} in {origen.get((k, None), '?')}, {_tipo(v)} in {f}")
                continue
            if isinstance(v, list):
                out.setdefault(k, []).extend(v)
                origen.setdefault((k, None), f)
            elif isinstance(v, dict):
                d = out.setdefault(k, {})
                origen.setdefault((k, None), f)
                for kk, vv in v.items():
                    _fusion_escalar(d, kk, vv, f, origen, (k, kk), errores, avisos, f"{k}.{kk}")
            else:
                _fusion_escalar(out, k, v, f, origen, (k, None), errores, avisos, k)
    vistos = {}
    for w in out.get("walls") or []:
        if w.get("id") in vistos:
            errores.append(f"wall id {w.get('id')} repetido ({vistos[w.get('id')]} y otro fragmento)")
        vistos[w.get("id")] = w.get("sheet")
    errores += validar_bandas(out)
    inv, p_inv = _inventario_de(carpeta, inventario)
    if inv is not None:
        import comparar as C
        errores += [f"{x} ({p_inv})" for x in C.paginas_0based(out, inv)]
    errores += validar_openings(out)
    out["fragmentos"] = fs
    return out, errores


def main(argv):
    if len(argv) >= 4 and argv[1] == "unir":
        a = list(argv)
        inv = None
        if "--inventario" in a:
            i = a.index("--inventario")
            inv = a[i + 1]
            del a[i:i + 2]
        if len(a) != 4:
            print(__doc__)
            return 2
        avisos = []
        canon, errores = unir(a[2], inv, avisos)
        for x in avisos:
            print("AVISO:", x)
        for x in errores:
            print("ERROR:", x)
        if errores:
            return 1
        with open(a[3], "w") as f:
            json.dump(canon, f, indent=1, ensure_ascii=False)
        print(f"unidos {len(canon['fragmentos'])} fragmento(s), {len(canon.get('walls') or [])} wall(s) -> {a[3]}")
        return 0
    if len(argv) != 3 or argv[1] not in ("estado", "compuerta"):
        print(__doc__)
        return 2
    d = argv[2]
    if argv[1] == "estado":
        lineas, sig = estado(d)
        print("\n".join(lineas))
        print("SIGUIENTE:", sig)
        return 0
    fallas, avisos = compuerta(d)
    for x in avisos:
        print("AVISO:", x)
    for x in fallas:
        print("FALLA:", x)
    print("COMPUERTA ETAPAS: " + ("PASA" if not fallas else f"FALLA ({len(fallas)})"))
    return 0 if not fallas else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
