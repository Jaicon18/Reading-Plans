#!/usr/bin/env python3
"""board_caras.py — board DETERMINISTA face por face, regla 60.2.

Por qué existe (arbitraje #10A/#10B, 16-oct-2026): con el mismo skill v59,
  - 5/8" regular: A <n> vs B <n> SF. A cargó G/G1 con "layers 2" = TOTAL (1 por face); 5/A12.01 dibuja
    2 layers POR FACE (9/A12.01 "2 LAYERS 5/8\" GYPSUM WALL BOARD"). -<n> SF.
  - ballistic / 3/8": A usó A1K <n> y <n> ft cuando A02.01 imprime <n>; B midió B2K hasta dentro del
    wall G (<n> vs <n> neto).
  - MR: A sumó la cara del extremo del chase; B tomó board a ceiling + 6" contra 53.3.
El campo ambiguo "layers" (¿total o por face?) desaparece: aquí solo existe layers POR FACE, y se valida
contra el detalle del tipo.

ENTRADA (JSON):
{
  "details": {"5/A12.01": {"layers_per_face": 2}, "3/A12.01": {"layers_per_face": 1},
              "4/A12.01": {"layers_per_face": 1, "k_panel": {"panel_to_ft": 8.0}}},
  "walls": [{
     "id": "W11", "tag": "A1K", "detail": "4/A12.01",
     "length_vector_ft": <n>,             # medido (cara a cara, 59.3)
     "length_printed_ft": <n>,          # cota impresa si existe -> MANDA (#0)
     "faces": [
        {"room": "Room A", "board": "5/8 regular", "layers": 1, "height_ft": <n>, "deduct_sf": 0},
        {"room": "Room B", "board": "5/8 regular", "layers": 1, "height_ft": <n>, "k_customer": true}
     ]}]
}
REGLAS:
  - largo = length_printed_ft si existe; si el vector difiere > 0.25 ft se anota DISCREPANCIA (no se
    promedia). Sin impresa: length_vector_ft.
  - layers de cada face == layers_per_face del detalle; si no, ValueError (se arregla el dato, no el total).
  - v68 (#16A RFI-28, 9/A12.01): face soffit_bottom usa details[d].soffit_bottom_layers {value, source} (el fondo
    del soffit puede llevar otra cantidad de capas que las caras).
  - "layers_total" o "layers" a nivel wall: ValueError (campo ambiguo prohibido).
  - SF de la face = largo x height x layers - deduct_sf (abertura NETA head - sill).
  - face k_customer (detalle con k_panel): ballistic = largo x min(panel_to, height);
    3/8" gyp = largo x max(0, height - panel_to).
SALIDA: SF por board type + ballistic + 3/8, y el detalle por face.

Uso:  python3 board_caras.py entrada.json [salida.json]
"""
import json
import sys

TOL_LARGO = 0.25


def calcular(data):
    det = data.get("details") or {}
    tot, filas, avisos = {}, [], []
    for w in data["walls"]:
        wid = w["id"]
        if "layers_total" in w or "layers" in w:
            raise ValueError(f"{wid}: campo 'layers' a nivel wall prohibido; usar layers por face")
        d = det.get(w.get("detail"))
        if d is None:
            raise ValueError(f"{wid}: detalle '{w.get('detail')}' no declarado en details")
        lp, lv = w.get("length_printed_ft"), w.get("length_vector_ft")
        if lp is None and lv is None:
            raise ValueError(f"{wid}: sin largo")
        L = float(lp if lp is not None else lv)
        if lp is not None and lv is not None and abs(float(lp) - float(lv)) > TOL_LARGO:
            avisos.append(f"{wid}: DISCREPANCIA impresa {lp} vs vector {lv} -> manda la impresa")
        faces = w.get("faces") or []
        if not faces:
            raise ValueError(f"{wid}: sin faces")
        # v66 (#15A CC-E1): una face que da a dos rooms con ceilings distintos se parte en tramos: cada tramo con
        # side (A|B), length_ft y length_source; los tramos de un side suman el largo del wall. Nada de alturas
        # ponderadas a mano.
        # v72 (R72.6, arbitraje #20): side "END" = cara de extremo / return de un box (p. ej. el return de un
        # furring): lleva length_ft + length_source, NO entra en Σ(side) = L y su board se suma al total.
        por_lado = {}
        for f in faces:
            if f.get("side") == "END":
                if f.get("length_ft") is None or not str(f.get("length_source") or "").strip():
                    raise ValueError(f"{wid} {f.get('room')}: face END exige length_ft y length_source")
                continue
            if f.get("length_ft") is not None:
                if f.get("side") not in ("A", "B") or not str(f.get("length_source") or "").strip():
                    raise ValueError(f"{wid} {f.get('room')}: face con length_ft exige side A|B y length_source")
                por_lado.setdefault(f["side"], []).append(float(f["length_ft"]))
        for lado, ls in por_lado.items():
            otras = [f for f in faces if f.get("side") == lado and f.get("length_ft") is None]
            if otras:
                raise ValueError(f"{wid} side {lado}: mezcla tramos con length_ft y faces sin largo")
            if abs(sum(ls) - L) > 0.05:
                raise ValueError(f"{wid} side {lado}: Σ tramos {round(sum(ls), 3)} != largo del wall {L}")
        for f in faces:
            Lf = float(f["length_ft"]) if f.get("length_ft") is not None else L
            lay = int(f["layers"])
            sbl = d.get("soffit_bottom_layers")
            if f.get("soffit_bottom") and isinstance(sbl, dict):     # v68: fondo de soffit con sus propias capas
                if not str(sbl.get("source") or "").strip() or lay != int(sbl["value"]):
                    raise ValueError(f"{wid} {f.get('room')}: fondo de soffit {lay} layer(s) != "
                                     f"{w['detail']}.soffit_bottom_layers {sbl.get('value')} (con source)")
            elif lay != int(d["layers_per_face"]):
                raise ValueError(f"{wid} {f.get('room')}: {lay} layer(s) por face pero {w['detail']} dibuja "
                                 f"{d['layers_per_face']}")
            H = float(f["height_ft"])
            sf = Lf * H * lay - float(f.get("deduct_sf", 0) or 0)
            if sf < -1e-6:
                raise ValueError(f"{wid} {f.get('room')}: SF negativo")
            b = f["board"]
            tot[b] = tot.get(b, 0.0) + sf
            op = f"{Lf} x {H} x {lay} - {f.get('deduct_sf', 0) or 0} = {round(sf, 2)}"
            if f.get("k_customer"):
                k = d.get("k_panel")
                if not k:
                    raise ValueError(f"{wid}: k_customer en un detalle sin k_panel")
                pt = float(k["panel_to_ft"])
                bal = Lf * min(pt, H)
                g38 = Lf * max(0.0, H - pt)
                tot["ballistic panel"] = tot.get("ballistic panel", 0.0) + bal
                tot["3/8 gyp"] = tot.get("3/8 gyp", 0.0) + g38
                op += f"; ballistic {Lf} x {min(pt, H)} = {round(bal, 2)}; 3/8 {Lf} x {round(max(0, H - pt), 3)} = {round(g38, 2)}"
            filas.append({"wall": wid, "room": f.get("room"), "board": b, "sf": round(sf, 2), "operacion": op})
    return {"totales_sf": {k: round(v, 2) for k, v in tot.items()}, "caras": filas, "avisos": avisos}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    out = calcular(json.load(open(argv[1])))
    s = json.dumps(out, indent=1)
    if len(argv) > 2:
        open(argv[2], "w").write(s)
    print(json.dumps(out["totales_sf"]))
    for a in out["avisos"]:
        print("AVISO", a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
