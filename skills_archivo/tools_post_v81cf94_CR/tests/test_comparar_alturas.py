"""U-175 (usuario 11-nov, Xfinity Interquest rev1): comparación de ALTURAS a tres lados (Depth de Bluebeam / Height del Excel /
ALTURAS_IMPRESAS.csv de una lectura independiente). Con las alturas impresas correctas = 0 fallas (20/20 OK); con W2-02 cambiada
a 9'-6" = FAIL; fila sin Source / Image o DERIVED sin Operation = FAIL; 0 markups comparados = FAIL. Y la compuerta CE_ALTURAS_3LADOS
y la línea del CHECKLIST B2 existen."""
import csv, io, os, sys, tempfile, contextlib
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comparar_alturas as CA


def _datos():
    """BE-XF08 (v81cf87): los datos de prueba (Xfinity rev1: xlsx + csv) viven en el repo, cache_proyectos/herramientas/tests/,
    no en el zip del skill (límite de Upload skill < 200 archivos). $TAKEOFF_REPO o la ruta del repo; sin ellos el caso se salta con aviso."""
    for raiz in (os.environ.get("TAKEOFF_REPO"), "/home/user/Reading-Plans", os.path.join(AQUI, "..", "..")):
        d = os.path.join(raiz or "", "cache_proyectos", "herramientas", "tests")
        if raiz and os.path.isfile(os.path.join(d, "xf_takeoff_rev1.xlsx")):
            return d
    return None


D = _datos()
V, X = (os.path.join(D, "xf_vista_bluebeam.csv"), os.path.join(D, "xf_takeoff_rev1.xlsx")) if D else (None, None)


def corre(alt):
    t = tempfile.mkdtemp(prefix="u175_"); out = os.path.join(t, "c.csv"); buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = CA.main([V, X, alt, out])
    return rc, buf.getvalue(), out


def test_u175_comparar_alturas():
    import compuerta_entrega as CE
    assert "CE_ALTURAS_3LADOS" in {cid for cid, *_x in CE.CHEQUEOS}
    assert "Three-way height check (U-175)" in open(os.path.join(AQUI, "checklist_revision.py"), encoding="utf-8").read()
    if not D:
        print("AVISO test_u175_comparar_alturas: datos de prueba no encontrados (cache_proyectos/herramientas/tests); caso con datos saltado")
        return
    rc, txt, out = corre(os.path.join(D, "xf_alturas_ok.csv"))
    assert rc == 0 and "20/20 markups OK" in txt, txt
    assert all(r["Result"] == "OK" for r in csv.DictReader(open(out, encoding="utf-8-sig")))
    rc, txt, _ = corre(os.path.join(D, "xf_alturas_mal.csv"))
    assert rc == 1 and "MISMATCH" in txt, txt
    t = tempfile.mkdtemp(prefix="u175b_")
    filas = list(csv.DictReader(open(os.path.join(D, "xf_alturas_ok.csv"), encoding="utf-8-sig")))
    filas[0]["Image"] = ""; filas[1]["Status"] = "DERIVED"; filas[1]["Operation"] = ""
    p = os.path.join(t, "malo.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
    rc, txt, _ = corre(p)
    assert rc == 1 and "without value / Source / Image" in txt and "DERIVED without Operation" in txt, txt
    vacio = os.path.join(t, "vista_vacia.csv"); open(vacio, "w").write(open(V, encoding="utf-8-sig").readline())
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = CA.main([vacio, X, os.path.join(D, "xf_alturas_ok.csv"), os.path.join(t, "v.csv")])
    assert rc == 1 and "0 markups" in buf.getvalue()
    print("test_u175_comparar_alturas OK")


# --- U-176 (antes test_alturas_extremo.py, unido en v81cf87) ---
# U-176 REGLA DE ORO #2 (usuario 11-nov): los 6 controles de comparar_alturas.py extremo. Obligatorios: un wall de 12'-6" en un cuarto de
# C.H. 13'-0" = FAIL y un wall más alto que el deck = FAIL. Además: 'above ceiling' que no toma el MAYOR C.H., 'to deck' sin slip track,
# board más alto que el wall, cierre dimensional que no cuadra, diferencia A / B sin resolver, muestreo sin una altura = FAIL;
# los casos correctos = PASS; la compuerta CE_ALTURAS_EXTREMO existe y el CHECKLIST lleva la muestra.
import comparar_alturas as AE   # U-176 (antes alturas_extremo.py)


def W(i, h, rooms, regla="above_ceiling", ext=0.5, board=None, top="standard", tipo="X1"):
    return {"id": i, "tipo": tipo, "h": h, "regla": regla, "ext": ext, "rooms": rooms, "board": board or [("A", h)], "top": top, "motivo": None}


def test_u176_alturas_extremo():
    # (3) reglas físicas — los dos obligatorios
    n, f = AE.reglas_fisicas([W("X1-01", 12.5, ["901"], regla="fixed")], {"901": 13.0}, 20.0)
    assert any("< C.H. 13.000" in x for x in f), f                                   # 12'-6" en cuarto de 13'-0"
    n, f = AE.reglas_fisicas([W("X1-02", 15.0, ["901"], regla="fixed")], {"901": 9.0}, 14.0)
    assert any("> B.O. estructura" in x for x in f), f                               # más alto que el deck
    n, f = AE.reglas_fisicas([W("X1-03", 10.5, ["901", "902"])], {"901": 10.0, "902": 12.0}, 20.0)
    assert any("MAYOR C.H." in x for x in f), f                                      # 6" sobre el cielo BAJO = mal
    n, f = AE.reglas_fisicas([W("X1-04", 14.0, ["901"], regla="to_deck", ext=0)], {"901": 9.0}, 14.0)
    assert any("slip" in x for x in f), f
    n, f = AE.reglas_fisicas([W("X1-05", 12.5, ["901"], board=[("A", 13.0)])], {"901": 12.0}, 20.0)
    assert any("board de la cara" in x for x in f), f
    n, f = AE.reglas_fisicas([W("X1-06", 12.5, ["901", "902"]), W("X1-07", 14.0, ["903"], regla="to_deck", ext=0, top="slip track")],
                             {"901": 12.0, "902": 10.0, "903": 9.0}, 14.0, [{"id": "Z-01", "h": 14.0}])
    assert n == 3 and f == [], f
    n, f = AE.reglas_fisicas([], {}, 14.0, [{"id": "Z-02", "h": 26.0}])
    assert f, "demolición más alta que la estructura"
    # (4) cruce por cuarto
    n, f, _ = AE.cruce_cuartos([W("X1-08", 12.5, ["901"]), W("X1-09", 10.5, ["901"])], {"901": 12.0})
    assert any("por debajo del cielo" in x for x in f) and any("alturas distintas" in x for x in f), f
    n, f, filas = AE.cruce_cuartos([W("X1-10", 12.5, ["901"]), W("X1-11", 12.5, ["901", "902"])], {"901": 12.0, "902": 10.0})
    assert n == 2 and f == [] and len(filas) == 3, f
    # (2) cierre dimensional
    assert AE.cierre("12'-0\" (A9.9 ceiling) + 0'-6\" (type legend) = 12.5", 12.5)[0]
    assert AE.cierre("North (room 901) (10'-0\" + 0'-6\") - 8'-6\" = 2.000; Underside (scaled) 7.32 pt / 18 pt/ft = 0.407; Total 2.000 + 0.407 = 2.407", 2.407)[0]
    assert AE.cierre("structure height not printed (rule U-174): 26 FT = 26.0", 26.0)[0]
    assert not AE.cierre("12'-0\" + 0'-6\" = 12.75", 12.75)[0]                         # suma que no cuadra
    assert not AE.cierre("12'-0\" + 0'-6\" = 12.5", 13.0)[0]                           # termina en otra altura
    assert not AE.cierre("", 12.5)[0]
    # (1) doble lectura
    a = [{"Wall ID": "X1-01", "Printed H": "12.5"}, {"Wall ID": "X1-02", "Printed H": "10.5"}]
    b = [{"Wall ID": "X1-01", "Printed H": "12'-6\""}, {"Wall ID": "X1-02", "Printed H": "12.5"}]
    filas, f = AE.comparar_ab(a, b)
    assert len(f) == 1 and "X1-02" in f[0], f
    filas, f = AE.comparar_ab(a, b, {"X1-02": {"Resolution": "A9.9 tag read on directed crop: 10'-0\" + 6\"", "Image": "x.png"}})
    assert f == [] and [r["Result"] for r in filas] == ["MATCH", "RESOLVED"]
    # (6) muestreo
    fin = [{"Wall ID": f"X1-{k:02d}", "Printed H": h} for k, h in enumerate(["12.5"] * 6 + ["9.5", "26"], 1)]
    m = AE.muestra(fin, {12.5: 1, 9.5: 2, 26.0: 3})
    assert len(m) >= 5 and {x["H (ft)"] for x in m} == {12.5, 9.5, 26.0} and AE.muestra_fallas(m, fin) == []
    assert AE.muestra_fallas(m[:2], fin)
    import compuerta_entrega as CE
    assert "CE_ALTURAS_EXTREMO" in {cid for cid, *_x in CE.CHEQUEOS}
    assert "Random sample (U-176)" in open(os.path.join(AQUI, "checklist_revision.py"), encoding="utf-8").read()
    print("test_u176_alturas_extremo OK")


if __name__ == "__main__":
    test_u175_comparar_alturas()
    test_u176_alturas_extremo()


def test_alturas_multinivel_cr():
    """v81cf90 (CR City Hotel rev19, 4 niveles, walls de madera board-only en existing_walls): comparar_alturas extremo lee
    existing_walls, las salas desde 'location ... | faces: 208 living; corridor 216', el B.O. por nivel (deck_heights dict) y no
    pide slip track a un wall de madera 'to roof'; un wall más alto que el floor-to-floor de su nivel = FAIL."""
    import comparar_alturas as CA
    can = {"constants": {"deck_heights": {"value": {"L2": "11'-0\"", "L4": "14'-0\""}}},
           "existing_walls": [
               {"id": "W.4-L2-41 A", "type_id": "W.4-0", "floor": "L2", "height_ft": "9.2396", "location": "L2 Bath 208 north wall | faces: 208 living",
                "decision": "R80f.1 / U-139: wood-framed wall - gypsum board is our scope, wood framing EXCLUDED", "height_source": "4/A5.05"},
               {"id": "W.4-L4-01 A", "type_id": "W.4-0", "floor": "L4", "height_ft": "8.9375", "location": "L4 room 401 | faces: 401 room",
                "decision": "wood-framed wall (board only)", "height_source": "1/A5.06 to the underside of roof sheathing"},
               {"id": "W.4-L2-99", "type_id": "W.4-0", "floor": "L2", "height_ft": "11.5", "location": "L2 | faces: 209 room",
                "decision": "board only", "height_source": "x"}]}
    ws = CA.walls_de_canon(can)
    assert len(ws) == 3 and ws[0]["rooms"] == ["208"] and ws[1]["regla"] == "to_deck" and ws[1]["madera"], ws
    bo = {k: CA.ftin(v) for k, v in can["constants"]["deck_heights"]["value"].items()}
    n, f = CA.reglas_fisicas(ws, {"208": 8.5, "401": 8.0}, bo)
    assert n == 3 and len(f) == 1 and "W.4-L2-99" in f[0] and "B.O." in f[0], f      # 11.5 > 11'-0" del nivel; sin pedir slip a madera
    n, f = CA.reglas_fisicas(ws, {"208": 9.5}, bo)
    assert any("W.4-L2-41 A" in x and "C.H." in x for x in f), f                        # wall por debajo del cielo de su cuarto
    ok, det = CA.cierre("14'-0\" - 1 1/2\" - 1/4\" - 3/4\" = 13'-9 1/2\"", 13.7917)     # pulgada en fracción sola (CR rev19)
    assert ok, det
    assert not CA.cierre("14'-0\" - 1/4\" = 13'-9 1/2\"", 13.7917)[0]
    print("test_alturas_multinivel_cr OK")


test_alturas_multinivel_cr()


def test_be_cr33_motivo_hoja_con_punto():
    """BE-CR33 (CR City Hotel rev19): height_diff_reason citing 'A7.05' / '4/A5.05' (dotted sheets) explains a partial row below the room C.H."""
    import comparar_alturas as CA
    w = {"id": "W.4-L2-03 A", "h": 9.0, "regla": "fixed", "ext": 0.0, "rooms": ["213"], "board": [], "top": "", "floor": "L2", "madera": True,
         "motivo": "material split of the face (A7.05 bath 'GYP-1 8'-6\"' + 6\"; continues per 4/A5.05)"}
    n, f = CA.reglas_fisicas([w], {"213": 9.24}, {"L2": 11.0})
    assert not f, f
    w["motivo"] = "material split of the face (no sheet)"
    n, f = CA.reglas_fisicas([w], {"213": 9.24}, {"L2": 11.0})
    assert f and "C.H." in f[0], f


def test_be_cr33_cruce_tipo_explicado():
    """BE-CR33 (b): same type with two heights in one room: explained rows (motivo with N/HOJA) do not count; two unexplained heights still FAIL."""
    import comparar_alturas as CA
    mk = lambda i, h, mot=None: {"id": i, "tipo": "W.4-0", "h": h, "rooms": ["213"], "motivo": mot}   # noqa: E731
    n, f, _ = CA.cruce_cuartos([mk("A", 9.24), mk("B", 9.24), mk("C", 9.24 + 0.5, "S1.05 zone over the wall (2/A0.10)")], {"213": 9.24})
    assert not f, f
    n, f, _ = CA.cruce_cuartos([mk("A", 9.24), mk("B", 9.74)], {"213": 9.24})
    assert any("alturas distintas" in x for x in f), f
    n, f, _ = CA.cruce_cuartos([mk("A", 9.24), mk("B", 9.74, "no sheet")], {"213": 9.24})
    assert any("alturas distintas" in x for x in f), f


if __name__ == "__main__":
    test_be_cr33_motivo_hoja_con_punto()
    test_be_cr33_cruce_tipo_explicado()
    print("test_be_cr33 OK")
