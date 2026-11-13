import sys; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
W = "X9-Z9-08"
def band(c0=1509.0, c1=1512.8, ori="V"): return {"ori": ori, "c0": c0, "c1": c1, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
def leaf(x, est="DISPUESTO", disp=""): return [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": str(x), "y": "1145.0", "largo_ft": "4.0",
                                               "estado": est, "disposicion": disp}]
def run(rows, excl=None, b=None, escalas=None):
    can = {"walls": [{"id": W, "band": b or band()}], "excluded_walls": excl or []}
    return CE.be_gk54_fallas(can, rows, escalas=escalas)
mid = (1509.0 + 1512.8) / 2
# at 9 pt/ft: 1 in = 0.75 pt
d = lambda inch: mid - inch * 0.75
print("Q0 control: leaf 4 in from band, DISPUESTO 'CUBIERTO: same wall as X9-Z9-08 (1/Z9.11)' (no gap) -> FAIL?", bool(run(leaf(d(4), disp=f"CUBIERTO: same wall as {W} (1/Z9.11)"))))
print("Q0b control: same + 'gap 0\" (1/Z9.11)' -> accepted?", not run(leaf(d(4), disp=f"CUBIERTO: same wall as {W}, gap 0\" (1/Z9.11)")))
# Q1: geometry contradicts the declared gap: leaf centre 13 in from the band centre (band 5 in thick) -> >= 8 in real gap
print("Q1 leaf 13 in from band centre, 'same wall as X9-Z9-08, gap 0\" (1/Z9.11)' -> accepted? (program measured 13 in)",
      not run(leaf(d(13), disp=f"CUBIERTO: same wall as {W}, gap 0\" (1/Z9.11)")))
# Q2: sheet at 1/4" (18 pt/ft) but no scale for it in `escalas` -> default 9 pt/ft; a leaf 10 in away (15 pt) is out of the window
print("Q2 1/4\" sheet, escalas without the sheet, leaf 10 in (15 pt) DISPUESTO 'CUBIERTO: same wall as X9-Z9-08 (1/Z9.11)' -> FAIL?",
      bool(run(leaf(mid - 15.0, disp=f"CUBIERTO: same wall as {W} (1/Z9.11)"), escalas={"Z9.11": None})))
print("Q2-0 control same with escalas {'Z9.11': 18} -> FAIL?", bool(run(leaf(mid - 15.0, disp=f"CUBIERTO: same wall as {W} (1/Z9.11)"), escalas={"Z9.11": 18.0})))
# Q3: (b) another material: any printed-material word + N/HOJA + gap > 0 passes, even 'existing' for a metal leaf
print("Q3 'NO ES NUESTRO: existing, gap 4 in (1/Z9.11)' -> accepted?", not run(leaf(d(4), disp="NO ES NUESTRO: existing, gap 4 in (1/Z9.11)")))
# Q4: canon exclusion 'same wall as X' with NO gap_proof, leaf DISPUESTO with a (b) proof: exclusion never judged (v126)
print("Q4 canon excl 'same wall as X9-Z9-08' (no gap_proof, no band) + leaf DISPUESTO '(b) CMU gap 4 in (1/Z9.11)' -> FAIL?",
      bool(run(leaf(d(4), disp="NO ES NUESTRO: CMU, gap 4 in (1/Z9.11)"), excl=[{"id": "EX-1", "wall": W, "reason": f"same wall as {W}"}])))
