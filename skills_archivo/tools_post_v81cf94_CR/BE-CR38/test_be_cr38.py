"""BE-CR38 (CR City Hotel rev20, 12-nov): al reemplazar un bloque de alturas_entrega.py se borró el bloque que agrega los renglones
partidos (cara de baño W.R. de los DW.4: 'DW.4-L3-03 C' / 'D' = misma altura que su padre ' A'). Los markups con Depth siguen en
VISTA_BLUEBEAM ('TO-DW.4-L3-03 C') y faltan en ALTURAS_IMPRESAS_A / _B -> cobertura_ab DEBE dar FAIL. Con el bloque restaurado
(los partidos copian la lectura ciega del padre en A, en B y en la final) -> 0 fallas.
Correr: python3 -m pytest test_be_cr38.py  (con tools/ del skill en sys.path)."""
import os
import sys

sys.path.insert(0, os.environ.get("SKILL_TOOLS", "/root/skill/take-off-metal-frame-drywall/tools"))
import comparar_alturas as CA  # noqa: E402

PADRE = {"Wall ID": "DW.4-L3-03 A", "Printed H": "9.2396", "Source": "4/A5.05 11'-0\" - 1'-9 1/8\"", "Status": "DERIVED", "Image": "x.png"}
DEPTH = ["TO-DW.4-L3-03 A", "TO-DW.4-L3-03 C", "TO-DW.4-L3-03 D"]


def partir(filas, ids):
    por = {r["Wall ID"]: r for r in filas}
    out = list(filas)
    for i in ids:
        r = dict(por["DW.4-L3-03 A"]); r["Wall ID"] = i
        r["Source"] = "[split row of DW.4-L3-03 A (bath face W.R., A0.06 GN 11), same height as its parent] " + r["Source"]
        out.append(r)
    return out


def test_be_cr38_bloque_borrado_falla():
    a, b = [dict(PADRE)], [dict(PADRE)]
    final = partir([dict(PADRE)], ["DW.4-L3-03 C", "DW.4-L3-03 D"])     # rev19: los partidos solo en la final
    ev = CA.cobertura_ab(a, b, final, DEPTH)
    assert any("DW.4-L3-03 C" in e and "ALTURAS_IMPRESAS_A" in e for e in ev)
    assert any("DW.4-L3-03 D" in e and "ALTURAS_IMPRESAS_B" in e for e in ev)
    ev2 = CA.cobertura_ab(a, b, [dict(PADRE)], DEPTH)                   # rev20 antes del arreglo: bloque borrado
    assert any("TO-DW.4-L3-03 C" in e for e in ev2)


def test_be_cr38_partidos_en_a_b_y_final_pasan():
    ids = ["DW.4-L3-03 C", "DW.4-L3-03 D"]
    a, b, final = partir([dict(PADRE)], ids), partir([dict(PADRE)], ids), partir([dict(PADRE)], ids)
    assert CA.cobertura_ab(a, b, final, DEPTH) == []
