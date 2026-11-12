import sys; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
band={"ori":"V","c0":1509.0,"c1":1512.8,"lo":1124.0,"hi":1163.8,"sheet":"Z9.11"}
red=[{"hoja":"Z9.11","tipo":"muro","id":"M-29","x":"1505.7","y":"1145.0","largo_ft":"4.0","estado":"ROJO"}]
W="X9-Z9-08"
def run(reason, extra=None, rows=red, wid=W):
    can={"walls":[{"id":wid,"band":band}],"excluded_walls":[dict({"id":"EX","reason":reason},**(extra or {}))]}
    return bool(CE.be_gk54_fallas(can,rows))
disp=lambda t: [dict(red[0],estado="DISPUESTO",disposicion=t)]
print("H0 control 'same wall as X9-Z9-08' -> FAIL:", run(f"same wall as {W}"))
print("H1 DISPUESTO 'same wall gap n/a A111' -> FAIL?", run(f"same wall as {W}", rows=disp("same wall gap n/a A111")))
print("H1b DISPUESTO 'same wall, gap n/a (1/A111)' -> FAIL?", run(f"same wall as {W}", rows=disp("same wall, gap n/a (1/A111)")))
print("H2 gap_proof 'n/a (1/A111)' in canon -> FAIL?", run(f"same wall as {W}", {"gap_proof":"n/a (1/A111)"}))
print("H2b gap_proof 'gap exists, 3/A111' (proof says the opposite) -> FAIL?", run(f"same wall as {W}", {"gap_proof":"there IS a 6in gap 3/A111"}))
for r in [f"same wall as: {W}", f"same wall as '{W}'", f"same wall ({W})", f"already counted in {W}", f"included in {W}", f"identical to {W}", f"counted with {W}", f"dup of {W}", f"same‑wall as {W}", f"same wall as {W}", f"mismo muro que {W}", f"see {W}"]:
    print(f"H3 reason {r!r} -> FAIL?", run(r))
for t in [f"NO ES NUESTRO: part of {W} (1/X9.11)", f"already counted in {W} (1/X9.11)", f"same leaf as {W} (1/X9.11)", f"NO ES NUESTRO: same‑wall {W} (1/X9.11)", f"dup of {W} (1/X9.11)"]:
    print(f"H4 DISPUESTO {t!r} -> FAIL?", run(f"same wall as {W}", rows=disp(t)))
print("H5 DISPUESTO 'EXISTING CONSTRUCTION TO REMAIN (2/X9.11)' (other disposition) -> FAIL?", run(f"same wall as {W}", rows=disp("EXISTING CONSTRUCTION TO REMAIN (2/X9.11)")))
print("H6 RX_NH_TRAZA on 'n/a A111':", bool(CE.RX_NH_TRAZA.search("same wall gap n/a A111")), "| on 'N/A A111':", bool(CE.RX_NH_TRAZA.search("same wall gap N/A A111")))
print("H7 DISPUESTO 'same wall gap N/A A111' -> FAIL?", run(f"same wall as {W}", rows=disp("same wall gap N/A A111")))
