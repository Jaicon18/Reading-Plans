#!/usr/bin/env python3
"""verif_codigo.py — R80e.38 (CR City Hotel rev4, revisión de código del usuario 7-nov-2026): banderas de código sobre
CUALQUIER canon de take-off (existing_walls[] y/o walls[] con type_id 'FAM-n', floor, height_ft, height_source,
location 'xxx | faces: A; B', source / keynote). Solo LEE; no cambia cantidades.

  (a) ROOF_HEAD   row rated (n >= 1, no XW) del ÚLTIMO piso con altura a "underside of roof framing" / roof line y SIN
                  detalle de cabeza citado (head / sheathing / A0.10-like) -> ROJO. IBC 2018 §707.5 / §708.4: fire
                  barriers y fire partitions llegan a la cubierta (sheathing / deck) o a un ensamble rated encima.
  (b) XW_FSD      row XW con rating 0 cuya FSD (fsd_ft en el row, o --fsd {id: ft}) < 30 ft -> ROJO; sin FSD conocida ->
                  AMBER (dato por leer en la code plan). IBC 2018 Table 602.
  (c) ROOM_MIX    cuarto (número de 3 dígitos en las caras) con una pared interior >= 2 HR y otra en 0 -> ROJO
                  (un cuarto rated se cierra completo, IBC 2018 §707.4 / §509.4.1).
Uso:  python3 verif_codigo.py <takeoff_canon.json> [--fsd fsd.json] [--json salida.json]
      python3 verif_codigo.py --selftest
Sale 0 siempre que corra (es un reporte); imprime ROJO / AMBER por regla."""
import json, re, sys, collections

RX_RATING = re.compile(r"-(\d)$")
RX_ROOF = re.compile(r"(?i)underside of roof|roof framing|roof line|to roof|bottom of roof")
RX_HEAD = re.compile(r"(?i)head (detail|of wall)|underside of (roof )?sheathing|to (the )?sheathing|\bA0\.1\d\b|fire ?(barrier|partition) head")
RX_ROOM = re.compile(r"\b(\d{3}[A-Z]?)\b(?!\.\d)")   # 121.1 = puerta, no cuarto


def rating(t):
    m = RX_RATING.search(str(t or ""))
    return int(m.group(1)) if m else None


def filas(c):
    return [w for w in (c.get("existing_walls") or []) + (c.get("walls") or []) if isinstance(w, dict)]


def ultimo_piso(rows):
    pisos = sorted({str(w.get("floor")) for w in rows if w.get("floor")}, key=lambda f: (len(f), f))
    return pisos[-1] if pisos else None


def roof_head(c):
    rows = filas(c); top = ultimo_piso(rows); out = []
    for w in rows:
        r = rating(w.get("type_id"))
        if w.get("floor") != top or not r or str(w.get("type_id", "")).startswith("XW"):
            continue
        hs = f"{w.get('height_source') or ''} {w.get('source') or ''}"
        if RX_ROOF.search(hs) and not RX_HEAD.search(f"{w.get('head_detail') or ''} {w.get('keynote') or ''} {w.get('height_source') or ''}"):
            out.append({"id": w.get("id"), "type": w.get("type_id"), "floor": top, "h": w.get("height_ft"),
                        "why": "rated wall on the top floor stops at the roof framing line; no head detail cited (IBC 2018 §707.5 / §708.4)"})
    return out


def xw_fsd(c, fsd=None):
    fsd = fsd or {}; rojo, amber = [], []
    for w in filas(c):
        t = str(w.get("type_id", ""))
        if not t.startswith("XW") or rating(t) != 0:
            continue
        b = str(w.get("id", "")).split(" ")[0]
        d = w.get("fsd_ft", fsd.get(w.get("id"), fsd.get(b)))
        if d is None:
            amber.append({"id": w.get("id"), "type": t, "why": "XW rated 0: FSD of its facade not recorded (read it on the code plan, IBC 2018 Table 602)"})
        elif float(d) < 30:
            rojo.append({"id": w.get("id"), "type": t, "fsd_ft": d, "why": f"XW rated 0 with FSD {d} ft < 30 ft (IBC 2018 Table 602)"})
    return rojo, amber


def room_mix(c):
    cuartos = collections.defaultdict(list)
    for w in filas(c):
        t = str(w.get("type_id", ""))
        r = rating(t)
        if r is None or t.startswith(("XW", "CH", "FW", "FI", "XFW")):   # exteriores, shafts y furring no cierran el cuarto
            continue
        caras = str(w.get("location") or "").split("faces:")[-1]
        for m in set(RX_ROOM.findall(caras)):
            cuartos[(w.get("floor"), m)].append((w.get("id"), t, r))
    out = []
    for (fl, room), ws in sorted(cuartos.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        rs = {r for _, _, r in ws}
        if max(rs) >= 2 and 0 in rs:
            out.append({"floor": fl, "room": room, "walls": [f"{i} ({t})" for i, t, _ in ws],
                        "why": "room with one wall >= 2 HR and other walls rated 0: a rated room is enclosed on all sides (IBC 2018 §707.4 / §509.4.1)"})
    return out


def correr(c, fsd=None):
    a = roof_head(c); b_r, b_a = xw_fsd(c, fsd); m = room_mix(c)
    return {"ROOF_HEAD": {"ROJO": a}, "XW_FSD": {"ROJO": b_r, "AMBER": b_a}, "ROOM_MIX": {"ROJO": m}}


def selftest():
    W = lambda i, t, fl="L4", h=8.9375, hs="1/A5.06 printed 8'-11 1/4\" LEVEL 4 to underside of roof framing", loc="x | faces: 401; 402", **k: dict(
        {"id": i, "type_id": t, "floor": fl, "height_ft": h, "height_source": hs, "location": loc}, **k)
    c = {"existing_walls": [
        W("A1", "W.62-1"),                                                       # (a) rojo
        W("A2", "W.62-1", head_detail="2/A0.10 to underside of roof sheathing"),  # (a) con detalle: no
        W("A3", "W.62-1", fl="L3", hs="11'-0\" floor to floor"),                  # no es último piso
        W("A4", "W.4-0"),                                                         # rating 0: no
        W("X1", "XW.6.4-0", fl="L2", loc="x | faces: 219", fsd_ft=12.0),          # (b) rojo
        W("X2", "XW.6.4-0", fl="L2", loc="x | faces: 220"),                       # (b) amber
        W("X3", "XW.6.4-0", fl="L2", loc="x | faces: 221", fsd_ft=31.0),          # (b) ok
        W("E1", "W.6-2", fl="L1", hs="12'", loc="x | faces: 118B; 120"),          # (c) 120: 2 y 0 -> rojo
        W("E2", "W.6-0", fl="L1", hs="12'", loc="x | faces: 120; 115"),
        W("E3", "W.6-1", fl="L1", hs="12'", loc="x | faces: 130; 131"),           # 130/131 solo 1: no
        W("E4", "W.6-0", fl="L1", hs="12'", loc="x | faces: 130")]}
    r = correr(c)
    assert [x["id"] for x in r["ROOF_HEAD"]["ROJO"]] == ["A1"], r["ROOF_HEAD"]
    assert [x["id"] for x in r["XW_FSD"]["ROJO"]] == ["X1"] and [x["id"] for x in r["XW_FSD"]["AMBER"]] == ["X2"], r["XW_FSD"]
    assert [x["room"] for x in r["ROOM_MIX"]["ROJO"]] == ["120"], r["ROOM_MIX"]
    assert correr({"existing_walls": [W("Z", "XW.6.4-0", fl="L2", loc="| faces: 219")]}, {"Z": 10})["XW_FSD"]["ROJO"]
    print("verif_codigo selftest OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        selftest(); sys.exit(0)
    c = json.load(open(a[0]))
    fsd = json.load(open(a[a.index("--fsd") + 1])) if "--fsd" in a else None
    r = correr(c, fsd)
    for regla, d in r.items():
        for nivel, xs in d.items():
            print(f"{regla} {nivel}: {len(xs)}")
            for x in xs[:200]:
                print("   ", json.dumps(x, ensure_ascii=False)[:260])
    if "--json" in a:
        json.dump(r, open(a[a.index("--json") + 1], "w"), indent=1, ensure_ascii=False)
