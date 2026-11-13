# adv7_gk54: BE-GK54 contra v81cf138 (misma geometría que adv6_gk54: band 5 in a 9 pt/ft). Sintético.
import sys; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
W = "X9-Z9-08"
def band(c0=1509.0, c1=1512.8, ori="V"): return {"ori": ori, "c0": c0, "c1": c1, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
def leaf(x, est="DISPUESTO", disp="", **kw):
    r = {"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": str(x), "y": "1145.0", "largo_ft": "4.0", "estado": est, "disposicion": disp}
    r.update(kw); return [r]
def run(rows, excl=None, b=None, escalas=None):
    can = {"walls": [{"id": W, "band": b or band()}], "excluded_walls": excl or []}
    return CE.be_gk54_fallas(can, rows, escalas=escalas)
mid = (1509.0 + 1512.8) / 2
d = lambda inch: mid - inch * 0.75
print("G0 control Q1 (13 in, 'gap 0\"') -> FAIL?", bool(run(leaf(d(13), disp=f"CUBIERTO: same wall as {W}, gap 0\" (1/Z9.11)"))))
for pr in ("gap 0", "no gap", "flush", "touching", "abutting", "tight to", "gap 1/2\"", "gap 1\"", "gap 0'-0\"", "gap: none", "sin gap", "gap = 0 in"):
    r = run(leaf(d(13), disp=f"CUBIERTO: same wall as {W}, {pr} (1/Z9.11)"))
    print("G1 leaf a 13 in, prueba", repr(pr), "-> FAIL?", bool(r))
print("G2 leaf a 13 in con espesor_in=20 en la fila del mapa, 'gap 0\"' -> FAIL?",
      bool(run(leaf(d(13), disp=f"CUBIERTO: same wall as {W}, gap 0\" (1/Z9.11)", espesor_in="20"))))
print("G3 leaf a 13 in, disp (b) 'NO ES NUESTRO: existing (1/Z9.11)' sin gap -> FAIL?", bool(run(leaf(d(13), disp="NO ES NUESTRO: existing (1/Z9.11)"))))
print("G4 leaf a 4 in (gap real ~1.5 in), disp (b) 'NO ES NUESTRO: existing, gap 4 in (1/Z9.11)' (Q3) -> FAIL?",
      bool(run(leaf(d(4), disp="NO ES NUESTRO: existing, gap 4 in (1/Z9.11)"))))
print("G5 Q2 repetido: 1/4\" sin escala, leaf 10 in -> FAIL?", bool(run(leaf(mid - 15.0, disp=f"CUBIERTO: same wall as {W} (1/Z9.11)"), escalas={"Z9.11": None})))
print("G6 Q2 sin argumento escalas (None) -> FAIL?", bool(run(leaf(mid - 15.0, disp=f"CUBIERTO: same wall as {W} (1/Z9.11)"))))
print("G7 Q4 repetido -> FAIL?", bool(run(leaf(d(4), disp="NO ES NUESTRO: CMU, gap 4 in (1/Z9.11)"), excl=[{"id": "EX-1", "wall": W, "reason": f"same wall as {W}"}])))
