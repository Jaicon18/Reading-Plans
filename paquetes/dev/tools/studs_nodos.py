#!/usr/bin/env python3
"""studs_nodos.py — conteo DETERMINISTA de studs por NODO (esquina / T / extremo), regla 60.1.

Por qué existe (arbitraje #10A/#10B, 16-oct-2026): con el mismo skill v59 las dos corridas contaron
distinto los studs de extremo. A puso +2 por row en cada punta de los G largos; B +2 por row también;
la referencia v4 cuenta cada junta UNA vez ("1 per T end, 0.5 per corner end"). 6" stud, 1-5/8" stud y
3-5/8" stud salían inestables por eso. Aquí el agente ya no decide: declara los NODOS y la herramienta
cuenta.

ENTRADA (JSON):
{
  "walls": [{
      "id": "W36", "tag": "G", "stud_size": "1-5/8\"",
      "length_ft": <n>,            # neto cara a cara (59.3)
      "oc_in": 16,                    # O.C. del tipo / schedule
      "rows": 2,                      # 2 = doble row (G/G1/bulkhead)
      "height_ft": <n>,            # stud completo; lado alto si hay pendiente (53.2)
      "zones": [{"from_ft": 0, "to_ft": 6, "oc_in": 12}],   # opcional: S1.11 n.5, 6 ft de BUILDING CORNER
      "openings": [{"ref": "door <ref>", "ro_w_ft": 3.333, "head_ft": 7.0, "sill_ft": 0.0}]
  }],
  "nodes": [
      {"id": "N1", "kind": "T", "branch": "W36", "through": "W57"},   # +1 al branch (x rows del branch)
      {"id": "N2", "kind": "L", "walls": ["W43", "W36"]},             # +1 al PRIMER wall (x sus rows)
      {"id": "N3", "kind": "X", "walls": ["W1", "W2"]},               # +2 al primero
      {"id": "N4", "kind": "free", "wall": "W42"},                    # extremo libre: 0 (ya está en el +1)
      {"id": "N5", "kind": "vendor_end", "wall": "W42"},              # office front 10/A12.01: +1 TOTAL (no x rows)
      {"id": "N6", "kind": "split", "walls": ["X1-1a", "X1-1b"],      # v61: UN wall continuo partido en 2 registros
       "why": "cambio de altura en un grid"},                         #   (grid, altura): -1 x rows al segundo
      {"id": "N7", "kind": "abut", "wall": "W36", "into": "W43",       # v61: extremo contra un wall cuyo stud de
       "source": "10/A12.01"}                                          #   cierre YA está contado: 0
  ]
}
Cada wall tiene DOS extremos; cada extremo aparece en exactamente un nodo. Si no, ValueError.

FÓRMULA (53.2 + 60.1):
  posiciones de campo  = 1 + sum(ROUNDUP(largo_zona / oc_zona))  (zonas que cubren 0..largo sin hueco)
  dentro de cada R.O.  = FLOOR(ro_w / oc)  -> se quitan del campo y vuelven como cripples de largo real
  jambs                = 4 por abertura (king + jack en cada jamb), altura completa
  nodos                = L +1 · T +1 al branch · X +2 · free 0 · vendor_end +1 total
                         split -1 x rows al 2.º wall (el stud del corte ya está en el campo del 1.º; v61)
                         abut 0 (extremo que muere contra un stud ya contado en otro wall; exige source; v61)
  studs completos      = (campo - dentro_RO + jambs + nodos_por_row) x rows + vendor_end
  LF                   = completos x height_ft + cripples x (height_ft - head) + cripples x sill
SALIDA: por wall {pcs_full, cripples, lf, operacion} y total por stud_size.

Cambio v61 (arbitraje #11, 16-oct-2026): #11B partió walls continuos (ids <ref>a / <ref>b) y declaró los dos
extremos del corte como 'free' -> el stud del corte salía dos veces. #11A/#11B declararon la punta de los G
largos contra el stub del office front como T (+1 por row) cuando 10/A12.01 ya pone el stud de cierre en el
stub -> +2 por G largo (+<n> LF de 1-5/8"). Nuevos nodos 'split' y 'abut'.

Uso:  python3 studs_nodos.py entrada.json [salida.json]
"""
import json
import math
import sys

EPS = 1e-6


def _roundup(x):
    return int(math.ceil(x - EPS)) if x > EPS else 0


def _zonas(w):
    L = float(w["length_ft"])
    oc = float(w["oc_in"])
    zs = sorted(w.get("zones") or [], key=lambda z: z["from_ft"])
    out, pos = [], 0.0
    for z in zs:
        a, b = float(z["from_ft"]), float(z["to_ft"])
        if a < pos - EPS or b > L + EPS or b <= a:
            raise ValueError(f"{w['id']}: zona {a}-{b} solapada o fuera del largo {L}")
        if a > pos + EPS:
            out.append((a - pos, oc))
        out.append((b - a, float(z["oc_in"])))
        pos = b
    if L > pos + EPS:
        out.append((L - pos, oc))
    return out


def contar(data):
    walls = {w["id"]: w for w in data["walls"]}
    if len(walls) != len(data["walls"]):
        raise ValueError("id de wall repetido")
    ends = {wid: 0 for wid in walls}
    extra_row = {wid: 0 for wid in walls}     # se multiplica por rows
    extra_tot = {wid: 0 for wid in walls}     # no se multiplica
    nota = {wid: [] for wid in walls}

    def use(wid, nid):
        if wid not in walls:
            raise ValueError(f"nodo {nid}: wall {wid} no existe")
        ends[wid] += 1

    for n in data.get("nodes", []):
        k, nid = n["kind"], n["id"]
        if k == "L":
            ws = n["walls"]
            if len(ws) != 2:
                raise ValueError(f"nodo {nid}: L necesita 2 walls")
            for wid in ws:
                use(wid, nid)
            extra_row[ws[0]] += 1
            nota[ws[0]].append(f"L {nid} +1")
        elif k == "T":
            use(n["branch"], nid)
            if n["through"] not in walls:
                raise ValueError(f"nodo {nid}: through {n['through']} no existe")
            extra_row[n["branch"]] += 1
            nota[n["branch"]].append(f"T {nid} +1")
        elif k == "X":
            ws = n["walls"]
            for wid in ws:
                use(wid, nid)
            extra_row[ws[0]] += 2
            nota[ws[0]].append(f"X {nid} +2")
        elif k == "free":
            use(n["wall"], nid)
        elif k == "split":
            ws = n.get("walls") or []
            if len(ws) != 2:
                raise ValueError(f"nodo {nid}: split necesita 2 walls")
            for wid in ws:
                use(wid, nid)
            a, b = walls[ws[0]], walls[ws[1]]
            for campo_ in ("stud_size", "oc_in", "rows"):
                if a.get(campo_, 1) != b.get(campo_, 1):
                    raise ValueError(f"nodo {nid}: split entre walls con {campo_} distinto ({a.get(campo_)} vs "
                                     f"{b.get(campo_)}): no es el mismo wall partido; declarar L/T")
            extra_row[ws[1]] -= 1
            nota[ws[1]].append(f"split {nid} -1 (stud del corte ya contado en {ws[0]})")
        elif k == "abut":
            use(n["wall"], nid)
            if n.get("into") not in walls:
                raise ValueError(f"nodo {nid}: abut necesita 'into' = wall existente que ya lleva el stud")
            if not str(n.get("source") or "").strip():
                raise ValueError(f"nodo {nid}: abut exige source (detalle que muestra el stud de cierre)")
            nota[n["wall"]].append(f"abut {nid} 0 (stud en {n['into']}, {n['source']})")
        elif k == "vendor_end":
            use(n["wall"], nid)
            extra_tot[n["wall"]] += 1
            nota[n["wall"]].append(f"vendor_end {nid} +1 total (10/A12.01)")
        else:
            raise ValueError(f"nodo {nid}: kind '{k}' desconocido (L, T, X, free, vendor_end, split, abut)")

    malos = {w: e for w, e in ends.items() if e != 2}
    if malos:
        raise ValueError(f"cada wall necesita exactamente 2 extremos en nodos; mal: {malos}")

    res, tot = [], {}
    for wid, w in walls.items():
        H = float(w["height_ft"])
        rows = int(w.get("rows", 1))
        if rows < 1:
            raise ValueError(f"{wid}: rows < 1")
        oc_ft = float(w["oc_in"]) / 12.0
        zon = _zonas(w)
        campo = 1 + sum(_roundup(l / (oc / 12.0)) for l, oc in zon)
        dentro, jambs, crip_lf_row, crip_n = 0, 0, 0.0, 0
        for o in w.get("openings") or []:
            ro = float(o["ro_w_ft"])
            if ro >= float(w["length_ft"]) - EPS:
                raise ValueError(f"{wid}: abertura {o.get('ref')} más ancha que el wall")
            n_in = int(math.floor(ro / oc_ft + EPS))
            dentro += n_in
            jambs += 4
            head, sill = float(o["head_ft"]), float(o.get("sill_ft", 0) or 0)
            if head > H + EPS:
                raise ValueError(f"{wid}: head {head} > altura {H}")
            crip_lf_row += n_in * ((H - head) + sill)
            crip_n += n_in * ((1 if H - head > EPS else 0) + (1 if sill > EPS else 0))
        por_row = campo - dentro + jambs + extra_row[wid]
        full = por_row * rows + extra_tot[wid]
        lf = full * H + crip_lf_row * rows
        op = (f"campo 1+sum ROUNDUP(zona/oc) {[(round(l, 3), oc) for l, oc in zon]} = {campo}"
              f" - {dentro} dentro de R.O. + {jambs} jambs + nodos {extra_row[wid]}/row = {por_row} x {rows} row(s)"
              f" + {extra_tot[wid]} total = {full} full x {H} + cripples {round(crip_lf_row * rows, 2)} LF"
              f" = {round(lf, 2)} LF [{'; '.join(nota[wid]) or 'sin extras de nodo'}]")
        res.append({"id": wid, "tag": w.get("tag"), "stud_size": w.get("stud_size"), "pcs_full": full,
                    "cripples": crip_n * rows, "lf": round(lf, 2), "operacion": op})
        k = w.get("stud_size") or "?"
        tot[k] = round(tot.get(k, 0.0) + lf, 2)
    return {"walls": res, "total_lf_por_stud": tot}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    data = json.load(open(argv[1]))
    out = contar(data)
    s = json.dumps(out, indent=1)
    if len(argv) > 2:
        open(argv[2], "w").write(s)
    print(json.dumps(out["total_lf_por_stud"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
