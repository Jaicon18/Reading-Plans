#!/usr/bin/env python3
"""etapas.py — control del flujo por etapas (v69): dónde quedó la corrida y compuerta antes del Excel.

Layout de la carpeta de etapas (cada etapa escribe en disco; una corrida cortada se reanuda en la primera etapa
que falte):

  <dir>/1_inventario/inventario.json   (+ inventario.md, recortes/)      ← inventario.py
  <dir>/2_lectura/canon_A.json                                           ← lectura A (subagentes)
  <dir>/2_lectura/canon_B.json                                           ← lectura B (subagentes, sin ver A)
  <dir>/3_revision/revision.json       (+ revision.md, img/)             ← comparar.py
  <dir>/4_canon/takeoff_canon.json     (canon conciliado)                ← estimador / revisión resuelta

También acepta los cinco archivos sueltos en <dir> (layout plano).

Uso:
  python3 etapas.py estado    <dir>   → qué etapa está hecha y cuál sigue (rc 0)
  python3 etapas.py compuerta <dir>   → rc 0 PASA / rc 1 FALLA, con cada motivo
  python3 etapas.py unir <carpeta_fragmentos> <canon_X.json>
                                      → une los fragmentos de una lectura (una hoja o grupo de tags por subagente):
                                        listas se concatenan; ids repetidos o constantes distintas = error (rc 1)

La compuerta FALLA si:
  - falta inventario.json, canon_A.json, canon_B.json o revision.json, o alguno no es JSON válido;
  - el inventario tiene recortes NO VERIFICADOS (aviso "PNG NO VERIFICADO" de inventario.py);
  - revision.json es más viejo que el inventario o que alguna lectura (revisión vencida: correr comparar.py otra vez);
  - la revisión no cubre exactamente los partition tags del inventario (fue hecha con otro inventario);
  - algún partition tag del inventario no tiene wall en la lectura A ni en la B y tampoco tiene alerta "tag sin wall".
Avisos (no fallan, se listan): walls sin `sheet` o sin `tag_ids`, tags ambiguos del inventario (no contados),
hojas no inventariables, ítems de revisión pendientes (difieren / solo A / solo B / alertas).
"""
import json
import os
import sys

ARCHIVOS = [
    ("inventario", "inventario.json", "1_inventario"),
    ("canon_A", "canon_A.json", "2_lectura"),
    ("canon_B", "canon_B.json", "2_lectura"),
    ("revision", "revision.json", "3_revision"),
    ("canon_final", "takeoff_canon.json", "4_canon"),
]
SIGUIENTE = {
    "inventario": "ETAPA 1: python3 inventario.py plano.pdf <dir>/1_inventario",
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

    tags = (inv.get("ocurrencias") or {}).get("partition_tag") or []
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
    n = {k: len(rev.get(k) or []) for k in ("difieren", "solo_A", "solo_B", "alertas")}
    if any(n.values()):
        avisos.append("revision.md pendiente para el estimador: " + " · ".join(f"{k} {v}" for k, v in n.items()))
    return fallas, avisos


def unir(carpeta):
    """Fragmentos *.json de una lectura -> un canon. Listas se concatenan; dicts se fusionan sin pisar un valor
    distinto; ids de walls repetidos = error. -> (canon, errores)."""
    out, errores, origen = {}, [], {}
    fs = sorted(f for f in os.listdir(carpeta) if f.endswith(".json"))
    if not fs:
        return None, [f"{carpeta}: sin fragmentos *.json"]
    for f in fs:
        with open(os.path.join(carpeta, f)) as fh:
            frag = json.load(fh)
        for k, v in frag.items():
            if isinstance(v, list):
                out.setdefault(k, []).extend(v)
            elif isinstance(v, dict):
                d = out.setdefault(k, {})
                for kk, vv in v.items():
                    if kk in d and d[kk] != vv:
                        errores.append(f"{k}.{kk}: {origen[(k, kk)]} y {f} traen valores distintos")
                    else:
                        d[kk] = vv
                        origen.setdefault((k, kk), f)
            elif k in out and out[k] != v:
                errores.append(f"{k}: {origen[(k, None)]} y {f} traen valores distintos")
            else:
                out[k] = v
                origen.setdefault((k, None), f)
    vistos = {}
    for w in out.get("walls") or []:
        if w.get("id") in vistos:
            errores.append(f"wall id {w.get('id')} repetido ({vistos[w.get('id')]} y otro fragmento)")
        vistos[w.get("id")] = w.get("sheet")
    out["fragmentos"] = fs
    return out, errores


def main(argv):
    if len(argv) == 4 and argv[1] == "unir":
        canon, errores = unir(argv[2])
        for x in errores:
            print("ERROR:", x)
        if errores:
            return 1
        with open(argv[3], "w") as f:
            json.dump(canon, f, indent=1, ensure_ascii=False)
        print(f"unidos {len(canon['fragmentos'])} fragmento(s), {len(canon.get('walls') or [])} wall(s) -> {argv[3]}")
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
