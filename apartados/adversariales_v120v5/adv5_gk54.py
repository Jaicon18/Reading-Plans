import sys; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
band={"ori":"V","c0":1509.0,"c1":1512.8,"lo":1124.0,"hi":1163.8,"sheet":"Z9.11"}
red=[{"hoja":"Z9.11","tipo":"muro","id":"M-29","x":"1505.7","y":"1145.0","largo_ft":"4.0","estado":"ROJO"}]
W="X9-Z9-08"
def run(reason, extra=None, rows=red, excl=True):
    can={"walls":[{"id":W,"band":band}],"excluded_walls":[dict({"id":"EX","reason":reason},**(extra or {}))] if excl else []}
    return bool(CE.be_gk54_fallas(can,rows))
disp=lambda t: [dict(red[0],estado="DISPUESTO",disposicion=t)]
print("K0 control 'same wall as X9-Z9-08' -> FAIL:", run(f"same wall as {W}"))
for r in [f"covered by {W}", f"accounted for in {W}", f"merged with {W}", f"carried in {W}", f"taken off with {W}", f"other leaf of {W}", f"same wall {W} per 1/Z9.11", f"double leaf - {W}", f"furring side of {W} (one wall)"]:
    print(f"K1 reason {r!r} -> FAIL?", run(r))
# K2: no canon exclusion at all; reviewer disposes the red leaf as 'same wall' in COBERTURA_DISPOSICION (G4 without a canon exclusion)
for t in [f"NO ES NUESTRO: same wall as {W} (1/Z9.11)", f"NO ES MURO: part of {W} (1/Z9.11)", f"CUBIERTO: counted in {W} (1/Z9.11)"]:
    print(f"K2 no canon exclusion, DISPUESTO {t!r} -> FAIL?", run("", rows=disp(t), excl=False))
# K3: realistic gap_proof wording
for g in ['gap 0" (1/Z9.11)', "leaves touch, 0 in gap per 1/Z9.11", "0\" gap, 3-5/8\" studs back to back (1/Z9.11)", "no gap between leaves (1/Z9.11)"]:
    print(f"K3 gap_proof {g!r} accepted (no FAIL)?", not run(f"same wall as {W}", {"gap_proof": g}))
