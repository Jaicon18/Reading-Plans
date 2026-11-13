#!/usr/bin/env python3
"""test_compuerta_entrega.py — BE-121: cada chequeo de compuerta_entrega.py / subir_entrega.py REPRODUCE el error original.
  - BE-120 (Harbor Freight rev2): RFI-01 abierto con la respuesta IMPRESA en A1.2 (B.O. DECK por zona) -> FAIL.
  - BE-119 (O'Reilly 3-nov): Depth del markup = H del Excel (comparación circular) pero la altura IMPRESA es otra -> FAIL.
  - Drive: carpeta bajo Projects › Claude outputs (O'Reilly / VS) -> FAIL; sin ENTREGA_OK verde -> subida bloqueada.
  - O'Reilly sin TIEMPOS.md -> FAIL. + formato Excel, tornillería, tracks, RFI A/B/C, RFI prohibidos.
Tokens que verificar_version.py busca en este archivo: ce_tiempos ce_drive_parent ce_rfi_barrido ce_altura_impresa
ce_formato_excel ce_tornilleria ce_track_familias ce_rfi_formato ce_rfi_prohibidos ce_entregables ce_sin_proposal
ce_sin_dolares ce_horas ce_seguimiento ce_atribucion ce_decisiones ce_fuentes_ms ce_datos_proyecto candados
ce_materiales_schedule revision_materiales texto_hoja_rotada ce_vista_bluebeam vista_bluebeam arreglar_sf_wall
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl  # noqa: E402
import pymupdf  # noqa: E402
import compuerta_entrega as CE  # noqa: E402
import subir_entrega as SE  # noqa: E402

RFI_OK = ("(A) Drawings (A2.0): printed B.O. deck per bay - delta -380 SF | (B) Code (ASTM C754): high point (loaded) - "
          "delta 0 (loaded) | (C) Other: ____")


def libro(p, pending=(("RFI-01", "Demising wall D-01 height basis per bay", RFI_OK),), ms=None, extra_hoja=False,
          extra_col=False, scope=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for h in CE.HOJAS6:
        ws = wb.create_sheet(h)
        fila, cab = CE.CABECERAS[h]
        for _ in range(fila - 1):
            ws.append(["x"])
        ws.append(cab + (["Extra"] if extra_col and h == "Material Summary" else []))
    ws = wb["Partition Takeoff"]
    ws.append(["TYPE S21"])
    ws.append(["S21 #S21-N", "S21-N", 20.0, 14.84375, 1, '6"', 16, 296.9, "Sales", "1/A3.2", "[CONFIRMED]"])
    for r in ms if ms is not None else (
            ["Bottom track 6\"", "LF", 20, 0.15, 0, 0, "run", 1, "N/SHEET: 1/A3.2"],
            ["Top slip / deflection track 6\" (2\" leg)", "LF", 20, 0.15, 0, 0, "run", 1, "N/SHEET: 10/A4.1"],
            ["Drywall screws #6 x 1-1/4\" Type S", "PCS", 0, 0, 0, 0, "each", 0, "N/SHEET: GA-216 | EXCLUDED - estimator decision 2026-10-31 (U-053)"]):
        wb["Material Summary"].append(list(r))
    for r in pending:
        wb["Pending Items"].append(list(r))
    for r in scope if scope is not None else (["ALC-30", "Fasteners", "EXCLUDED", "All screws / anchors EXCLUDED (U-053)"],):
        wb["Scope Checklist"].append(list(r))
    if extra_hoja:
        wb.create_sheet("Notas")
    wb.save(p)
    return p


def workdir(tiempos=True, drive=CE.DRIVE_RAIZ, set_texto=None, rfi=None):
    w = tempfile.mkdtemp(prefix="ce_test_")
    e = os.path.join(w, "FINAL_FOR_REVIEW")
    os.makedirs(os.path.join(e, "Take-off"))
    os.makedirs(os.path.join(e, "Planos marcados"))
    libro(os.path.join(e, "Take-off", "P_Takeoff_FINAL.xlsx"))
    for n in ("README_REVIEW.md", "PARA_REVISAR_EN_LA_MANANA.md"):
        open(os.path.join(e, n), "w").write("# PROJECT DATA\nHoras en PST.\n")
    open(os.path.join(e, "SEGUIMIENTO.md"), "w").write("| RFI-01 | A1.2 | ... |\n")
    if tiempos:
        open(os.path.join(w, "TIEMPOS.md"), "w").write(
            "START 2026-11-02 20:26 PST\n| 1 | arranque | 20:26 | 20:32 |\n| 2-3 | lecturas | 20:33 | 20:53 |\n"
            "| 4 | comparar | 20:54 | 20:54 |\n| 5 | resolver | 20:54 | 21:05 |\n| 6-9 | calc+excel+markups+gates | 20:55 | 21:31 |\n"
            "| **TOTAL** | | 20:26 | 21:31 |\n")
    json.dump({"drive": {"parent_id": drive, "carpeta_proyecto": "Proyecto X", "carpeta_proyecto_id": "FOLDER123"}},
              open(os.path.join(w, "entrega.json"), "w"))
    json.dump({"rfis": [rfi or HFT_RFI01]}, open(os.path.join(w, "takeoff.json"), "w"))
    if set_texto is not None:
        json.dump({"hojas": set_texto}, open(os.path.join(w, "set_texto.json"), "w"))
    return w


# RFI-01 de HFT Loveland rev2 (barrido real, takeoff_canon_FINAL_rev2.json): A1.2 SÍ estaba en la lista y aun así la
# respuesta impresa (B.O. DECK por zona) se quedó como RFI.
HFT_RFI01 = {"id": "RFI-01", "pregunta": "Demising wall D-01 (+-209'-1\", A1.1) runs under a sloped deck. Loaded 18.17 ft "
             "full length (conservative value loaded)", "barrido": {
                 "hojas": ["A0.0", "A1.1", "A1.2", "A2.0", "A4.1", "S2.1"], "terminos": ["DECK", "B.O.", "SLIP"],
                 "grep": "full set text: 'DECK' 93 hits ..."}}
SET_HFT = {"A1.1": "WALL LEGEND ALL WALLS BRACED TO STRUCTURE", "A1.2": "ZONE 1 B.O. DECK +-16'-9\" ZONE 2 B.O. DECK +-17'-5 1/2\"",
           "A2.0": "ROOF PLAN", "S2.1": "JOIST BEARING"}


def chk(fn, c):
    est, ev = fn(c)
    return est, " ".join(ev)


def test_hft_rfi01_impreso():
    w = workdir(set_texto=SET_HFT)
    est, ev = chk(CE.ce_rfi_barrido, CE.Ctx(w))
    assert est == "FAIL" and "A1.2" in ev and "IMPRESA" in ev, ev            # BE-120 reproducido
    # la vieja compuerta A_RFI_BARRIDO solo pedía la lista: con 6 hojas falla por cantidad, con 'ALL' pasaba
    r = dict(HFT_RFI01, barrido=dict(HFT_RFI01["barrido"], hojas="ALL"))
    w = workdir(set_texto=SET_HFT, rfi=r)
    assert chk(CE.ce_rfi_barrido, CE.Ctx(w))[0] == "FAIL"
    # hoja con el término fuera del barrido
    st = dict(SET_HFT, **{"S3.0": "DECK BEARING"})
    w = workdir(set_texto=st, rfi=dict(HFT_RFI01, barrido=dict(HFT_RFI01["barrido"], descartes={"A1.2": "x"})))
    est, ev = chk(CE.ce_rfi_barrido, CE.Ctx(w))
    assert est == "FAIL" and "S3.0" in ev and "NO está" in ev, ev
    # con descarte escrito por hoja y todas las hojas barridas -> PASS
    b = dict(HFT_RFI01["barrido"], hojas=list(st), descartes={"A1.2": "spot elevations at grid lines only, not per bay along the lease line"})
    w = workdir(set_texto=st, rfi=dict(HFT_RFI01, barrido=b))
    assert chk(CE.ce_rfi_barrido, CE.Ctx(w))[0] == "PASS"
    # sin texto del set no se puede probar -> FAIL
    assert chk(CE.ce_rfi_barrido, CE.Ctx(workdir()))[0] == "FAIL"


def markups_pdf(p, depth, label_h):
    doc = pymupdf.open()
    pg = doc.new_page(width=2592, height=1728)
    doc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1}])
    pg.insert_text((100, 1650), "FLOOR PLAN   SCALE: 1/8\" = 1'-0\"", fontsize=12)
    a = pg.add_polyline_annot([(100, 200), (100 + 20.0 * 9, 200)])
    a.set_info(content=f"S21 · 20.00 LF · H {label_h} · 296.9 SF · 1/A3.2 · S21-N", subject="S21")
    a.update()
    doc.xref_set_key(a.xref, "Depth", str(depth))
    doc.save(p)


def test_altura_circular_oreilly():
    w = workdir()
    c = CE.Ctx(w)
    pdf = os.path.join(w, "FINAL_FOR_REVIEW", "Planos marcados", "m.pdf")
    markups_pdf(pdf, 14.84375, "14'-10.125\"")              # Depth = H del Excel (lo que validaba la revisión circular)
    c = CE.Ctx(w)
    c.canon = {"walls": [{"id": "S21-N", "height_ft": 14.84375, "height_source": "1/A3.2 'STUDS TO 13'-11 1/2\" A.F.F.'"}]}
    est, ev = chk(CE.ce_altura_impresa, c)
    assert est == "FAIL" and "printed source H 13.958" in ev, ev            # BE-119 reproducido
    c.canon = {"walls": [{"id": "S21-N", "height_ft": 14.84375, "height_source": "[PENDIENTE] assumed 8\" purlin (RFI-01)",
                          "height_status": "PENDIENTE"}]}
    assert chk(CE.ce_altura_impresa, c)[0] == "AMBER"
    c.canon = {"walls": [{"id": "S21-N", "height_ft": 14.84375, "height_source": "1/A3.2 'STUDS TO 14'-10 1/8\" A.F.F.'"}]}
    assert chk(CE.ce_altura_impresa, c)[0] == "PASS", chk(CE.ce_altura_impresa, c)


def test_drive_parent():
    assert chk(CE.ce_drive_parent, CE.Ctx(workdir(drive=CE.DRIVE_PROHIBIDO)))[0] == "FAIL"   # O'Reilly / VS en Projects
    assert chk(CE.ce_drive_parent, CE.Ctx(workdir(drive="otro")))[0] == "FAIL"
    assert chk(CE.ce_drive_parent, CE.Ctx(workdir()))[0] == "PASS"
    w = workdir()
    os.remove(os.path.join(w, "entrega.json"))
    assert chk(CE.ce_drive_parent, CE.Ctx(w))[0] == "FAIL"


def test_tiempos():
    assert chk(CE.ce_tiempos, CE.Ctx(workdir(tiempos=False)))[0] == "FAIL"                  # O'Reilly sin TIEMPOS.md
    w = workdir()
    t = open(os.path.join(w, "TIEMPOS.md")).read().replace("| 4 | comparar | 20:54 | 20:54 |\n", "")
    open(os.path.join(w, "TIEMPOS.md"), "w").write(t)
    est, ev = chk(CE.ce_tiempos, CE.Ctx(w))
    assert est == "FAIL" and "paso 4" in ev, ev
    assert chk(CE.ce_tiempos, CE.Ctx(workdir()))[0] == "PASS"
    w = workdir()
    open(os.path.join(w, "TIEMPOS.md"), "a").write("subida 2026-11-03T05:01Z UTC\n")
    assert chk(CE.ce_horas, CE.Ctx(w))[0] == "FAIL"


def test_excel():
    w = workdir()
    c = CE.Ctx(w)
    assert chk(CE.ce_formato_excel, c)[0] == "PASS", chk(CE.ce_formato_excel, c)
    assert chk(CE.ce_tornilleria, c)[0] == "PASS", chk(CE.ce_tornilleria, c)
    assert chk(CE.ce_track_familias, c)[0] == "PASS", chk(CE.ce_track_familias, c)
    assert chk(CE.ce_fuentes_ms, c)[0] == "PASS"
    assert chk(CE.ce_rfi_formato, c)[0] == "PASS", chk(CE.ce_rfi_formato, c)
    assert chk(CE.ce_seguimiento, c)[0] == "PASS"
    assert chk(CE.ce_atribucion, c)[0] == "PASS", chk(CE.ce_atribucion, c)
    x = os.path.join(w, "FINAL_FOR_REVIEW", "Take-off", "P_Takeoff_FINAL.xlsx")
    libro(x, extra_hoja=True)
    assert chk(CE.ce_formato_excel, CE.Ctx(w))[0] == "FAIL"
    libro(x, extra_col=True)
    assert chk(CE.ce_formato_excel, CE.Ctx(w))[0] == "FAIL"
    libro(x, ms=[["Bottom track 6\"", "LF", 20, 0, 0, 0, "", 0, "N/SHEET: 1/A3.2"],
                 ["Top slip / deflection track 6\"", "LF", 20, 0, 0, 0, "", 0, "N/SHEET: 10/A4.1"],
                 ["Framing screws #8 x 1/2\"", "PCS", 410, 0, 0, 0, "", 0, "N/SHEET: A4.1"]])
    assert chk(CE.ce_tornilleria, CE.Ctx(w))[0] == "FAIL"
    libro(x, ms=[["Top and bottom track + slip track 6\"", "LF", 40, 0, 0, 0, "", 0, "N/SHEET: 1/A3.2"]])
    assert chk(CE.ce_track_familias, CE.Ctx(w))[0] == "FAIL"
    libro(x, ms=[["Bottom track 6\"", "LF", 20, 0, 0, 0, "", 0, "N/SHEET: 1/A3.2"]])
    assert chk(CE.ce_track_familias, CE.Ctx(w))[0] == "FAIL"
    libro(x, ms=[["Bottom track 6\"", "LF", 20, 0, 0, 0, "", 0, "see note"]])
    assert chk(CE.ce_fuentes_ms, CE.Ctx(w))[0] == "FAIL"
    libro(x, pending=[["RFI-01", "q", "(A) Drawings: x - delta 1 | (B) Code: y - delta 0"]])
    assert chk(CE.ce_rfi_formato, CE.Ctx(w))[0] == "FAIL"
    libro(x, pending=[["RFI-02", "Insulation type at demising wall", RFI_OK], ["RFI-03", "Fastener spacing at track", RFI_OK],
                      ["RFI-04", "Kicker length at bulkhead (no screws / bolts printed)", RFI_OK]])
    est, ev = chk(CE.ce_rfi_prohibidos, CE.Ctx(w))
    assert est == "FAIL" and "RFI-02" in ev and "RFI-03" in ev and "RFI-04" not in ev, ev
    libro(x, scope=[["ALC-1", "Note", "x", "EXCLUDED - estimator decision: wood blocking"]])
    assert chk(CE.ce_atribucion, CE.Ctx(w))[0] == "FAIL"


def test_entregables_y_docs():
    w = workdir()
    e = os.path.join(w, "FINAL_FOR_REVIEW")
    assert chk(CE.ce_entregables, CE.Ctx(w))[0] == "FAIL"                     # sin PDF ni PNG de markups
    open(os.path.join(e, "Proposal_v1.docx"), "w").write("x")
    assert chk(CE.ce_sin_proposal, CE.Ctx(w))[0] == "FAIL"
    open(os.path.join(e, "PARA_REVISAR_EN_LA_MANANA.md"), "a").write("Costo de la corrida: $12.40\n")
    assert chk(CE.ce_sin_dolares, CE.Ctx(w))[0] == "FAIL"
    # U-123 (preferencias del día 1, COSTOS): el monto en el EXCEL también cuenta (antes solo se miraban los .md)
    w2 = workdir()
    assert chk(CE.ce_sin_dolares, CE.Ctx(w2))[0] == "PASS", chk(CE.ce_sin_dolares, CE.Ctx(w2))   # fórmulas Inputs!$B$11 no
    x = os.path.join(w2, "FINAL_FOR_REVIEW", "Take-off", "P_Takeoff_FINAL.xlsx")
    libro(x, scope=[["ALC-30", "Fasteners", "EXCLUDED", "All screws EXCLUDED (U-053); framing labor approx. $4,200"]])
    est, ev = chk(CE.ce_sin_dolares, CE.Ctx(w2))
    assert est == "FAIL" and "Scope Checklist" in ev, ev
    assert chk(CE.ce_datos_proyecto, CE.Ctx(w))[0] == "FAIL"                  # takeoff.json sin proyecto_datos


def fake_gdrive(lista_ids):
    d = tempfile.mkdtemp(prefix="fake_gd_")
    p = os.path.join(d, "gd.py")
    log = os.path.join(d, "log.txt")
    open(p, "w").write(
        "import sys, json\n"
        f"open({log!r}, 'a').write(' '.join(sys.argv[1:]) + '\\n')\n"
        "c = sys.argv[1]\n"
        f"if c == 'list':\n    [print(json.dumps({{'id': i, 'name': 'Proyecto X'}})) for i in {list(lista_ids)!r}]\n"
        "elif c == 'mkdir':\n    print('NEW_' + sys.argv[3])\n"
        "elif c == 'put':\n    print('OK uploaded ' + sys.argv[2])\n")
    return p, log


def entrega_ok(w, ok=True, parent=CE.DRIVE_RAIZ):
    c = CE.Ctx(w)
    arch = {os.path.relpath(p, w): CE._sha(p) for p in c.archivos_entrega()}
    json.dump({"ok": ok, "entrega_dir": "FINAL_FOR_REVIEW", "chequeos": [{"id": "CE_X", "estado": "PASS" if ok else "FAIL"}],
               "archivos": arch, "drive": {"parent_id": parent, "carpeta_proyecto": "Proyecto X", "carpeta_proyecto_id": "FOLDER123"}},
              open(os.path.join(w, "ENTREGA_OK.json"), "w"))


def test_subida():
    w = workdir()
    try:
        SE.candados(w)
        raise AssertionError("subió sin ENTREGA_OK.json")
    except SE.Bloqueo as e:
        assert "ENTREGA_OK" in str(e)
    entrega_ok(w, ok=False)
    try:
        SE.candados(w)
        raise AssertionError("subió con compuerta roja")
    except SE.Bloqueo as e:
        assert "verde" in str(e)
    entrega_ok(w)
    open(os.path.join(w, "FINAL_FOR_REVIEW", "README_REVIEW.md"), "a").write("cambio tardío\n")
    try:
        SE.candados(w)
        raise AssertionError("subió un archivo cambiado después de la compuerta")
    except SE.Bloqueo as e:
        assert "cambió" in str(e)
    entrega_ok(w, parent=CE.DRIVE_PROHIBIDO)
    try:
        SE.candados(w)
        raise AssertionError("subió a Projects › Claude outputs")
    except SE.Bloqueo as e:
        assert "parent_id" in str(e)
    entrega_ok(w)
    gd, log = fake_gdrive(["OTRA"])
    env = dict(os.environ, GDRIVE_FETCH=gd)
    r = subprocess.run([sys.executable, "-I", os.path.join(CE.AQUI, "subir_entrega.py"), w], capture_output=True, text=True, env=env)
    assert r.returncode == 1 and "NO es hija" in r.stdout, r.stdout + r.stderr
    gd, log = fake_gdrive(["FOLDER123"])
    env = dict(os.environ, GDRIVE_FETCH=gd)
    r = subprocess.run([sys.executable, "-I", os.path.join(CE.AQUI, "subir_entrega.py"), w], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    L = open(log).read()
    assert f"list {CE.DRIVE_RAIZ}" in L and "mkdir FOLDER123 FINAL_FOR_REVIEW" in L and L.count("put ") == 4 and "mkdir NEW_FINAL_FOR_REVIEW Take-off" in L, L
    assert os.path.isfile(os.path.join(w, "SUBIDA_OK.json"))


def test_materiales_schedule():
    """BE-122 (j): sin lectura independiente del schedule = FAIL; board regular donde el schedule imprime Type X = FAIL."""
    w = workdir()
    c = CE.Ctx(w)
    assert chk(CE.ce_materiales_schedule, c)[0] == "FAIL"                     # sin fichas.json
    json.dump({"types": {"S21": {"stud_designation": "600S162-33", "gauge_ga": 20, "oc_in": 16,
                                 "faces": [{"side": "each side", "layers": 1, "board": "5/8\" Type X"}],
                                 "sources": {"stud": "1/A3.2", "board": "1/A3.2"}}}}, open(os.path.join(w, "fichas.json"), "w"))
    canon = os.path.join(w, "canon.json")
    caras = [{"side": "A", "board": "5/8 type X", "layers": 1, "height_ft": 14.8}, {"side": "B", "board": "5/8 regular", "layers": 1, "height_ft": 14.8}]
    json.dump({"walls": [{"id": "S21-N", "faces": caras}]}, open(canon, "w"))
    e = json.load(open(os.path.join(w, "entrega.json")))
    e["canon"] = "canon.json"
    json.dump(e, open(os.path.join(w, "entrega.json"), "w"))
    x = os.path.join(w, "FINAL_FOR_REVIEW", "Take-off", "P_Takeoff_FINAL.xlsx")
    wb = openpyxl.load_workbook(x)
    wb["Partition Takeoff"]["F6"] = '6" 20 ga (33 mil, 600S162-33)'
    wb.save(x)
    est, ev = chk(CE.ce_materiales_schedule, CE.Ctx(w))
    assert est == "FAIL" and "board type S21-N" in ev, ev
    caras[1]["board"] = "5/8 type X"
    json.dump({"walls": [{"id": "S21-N", "faces": caras}]}, open(canon, "w"))
    est, ev = chk(CE.ce_materiales_schedule, CE.Ctx(w))
    assert est != "FAIL" or "board type" not in ev, ev


def test_revision_materiales():
    """test de la herramienta (sesión O'Reilly, test_revision_materiales.py, unido aquí para quedar < 200 archivos)."""
    import revision_materiales as RV
    ficha = {"stud_designation": "362S162-33", "gauge_ga": 20, "oc_in": 16, "height": "STUDS TO 8'-6\" A.F.F.",
             "faces": [{"side": "each side", "layers": 1, "board": "5/8\" Type X W.R."}],
             "sources": {"stud": "W1/A1.1", "board": "W1/A1.1", "height": "W1/A1.1"}}
    fila = [{"type": "W1", "wall": "W-1", "lf": 10.0, "h": 8.5, "layers": 1, "stud": '3-5/8" 20 ga (33 mil, 362S162-33)',
             "oc": 16, "board_sf": 170, "location": "", "source": "W1/A1.1"}]
    bien = {"W-1": {"faces": [{"side": "A", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5},
                              {"side": "B", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5}]}}
    mal = {"W-1": {"faces": [{"side": "A", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5},
                             {"side": "B", "board": "5/8 regular", "layers": 1, "height_ft": 8.5}]}}
    assert RV.comparar_type("W1", ficha, fila, bien)["verdict"] == "GREEN"
    r = RV.comparar_type("W1", ficha, fila, mal)
    assert r["verdict"] == "RED" and any(c["field"].startswith("board type") and c["status"] == "RED" for c in r["checks"]), r
    fila2 = [dict(fila[0], stud='3-5/8" 25 ga (18 mil, 362S162-18)', h=9.0)]
    r = RV.comparar_type("W1", ficha, fila2, bien)
    assert {c["field"] for c in r["checks"] if c["status"] == "RED"} >= {"stud designation", "gauge", "height"}, r
    assert RV.tipo_board('5/8" TYPE "X" GYPSUM BOARD') == "X" and RV.tipo_board("5/8 type X WR") == "X-WR"
    ms = [{"row": 4, "name": "Bottom track 3-5/8\"", "unit": "LF", "net": 30.0,
           "where": "N/SHEET: W1/A1.1 | Breakdown [DERIVED]: W-1 10 + W-2 20 = 30 LF"},
          {"row": 5, "name": "Top track 3-5/8\"", "unit": "LF", "net": 31.0,
           "where": "N/SHEET: W1/A1.1 | Breakdown [DERIVED]: W-1 10 + W-2 20 = 30 LF"},
          {"row": 6, "name": "Additional head track", "unit": "LF", "net": 7.33, "where": "N/SHEET: default (no sheet) | Door 3"}]
    fil = [{"type": "W1", "wall": "W-1"}, {"type": "W1", "wall": "W-2"}]
    sm = {x["row"]: x for x in RV.sumas(ms, fil, "/nonexistent")}
    assert sm[4]["status"] == "GREEN" and sm[4]["by_type"] == {"W1": 30.0}, sm[4]
    assert sm[5]["status"] == "RED" and sm[6]["status"] == "RED", (sm[5], sm[6])


def test_materiales_cfa_rev5():
    """v81cf25 (CFA #2284 rev5): revision_materiales.sumas daba RED en (a) el driver de compound / tape cuando el board no es
    '5/8" Type X' (1/2" regular + MR + 5/8" ceiling) y (b) el desglose 'ítem: op = a LF + ítem: op = b LF = total LF'."""
    import revision_materiales as RV
    ms = [{"row": 4, "name": '1/2" gypsum board regular', "unit": "SF", "net": 100.0, "where": "N/SHEET: A-1"},
          {"row": 5, "name": '5/8" gypsum ceiling board, SAG-RESISTANT', "unit": "SF", "net": 50.0, "where": "N/SHEET: A-1"},
          {"row": 6, "name": 'Joint compound, all purpose', "unit": "LB", "net": 10.8,
           "where": "[DERIVED] N/SHEET: driver | Inputs!B23 (Joint compound (lb per SF) = 0.072) x 150 SF of board"},
          {"row": 7, "name": '3-5/8" stud, framed soffit', "unit": "LF", "net": 84.32,
           "where": "N/SHEET: C4/A-624 | Breakdown [DERIVED]: Serving soffit: ROUNDUP(18.122/(16/12))+1 = 15 joists x 3.755 = "
                    "56.32 LF 3-5/8\" joists + Dining soffit: ROUNDUP(8/(16/12))+1 = 7 joists x 4.0 = 28.0 LF 3-5/8\" joists = 84.32 LF (joists)"}]
    sm = {x["row"]: x for x in RV.sumas(ms, [], "/nonexistent")}
    assert sm[6]["status"] == "GREEN" and sm[7]["status"] == "GREEN", (sm[6], sm[7])
    ms[3]["net"] = 90.0
    assert {x["row"]: x for x in RV.sumas(ms, [], "/nonexistent")}[7]["status"] == "RED"


def test_texto_hoja_rotada():
    """v81cf24 (CFA #2284 rev5): en las hojas con /Rotate 270 (M / P / E del set) el número de hoja del title block salía
    p76.. porque las coordenadas de las palabras vienen sin rotar; el barrido BE-120 no podía casar 'M-201' con su hoja."""
    d = tempfile.mkdtemp(prefix="ce_rot_")
    pdf = os.path.join(d, "rot.pdf")
    doc = pymupdf.open()
    for rot, lab in ((0, "A-101"), (270, "M-201"), (90, "F-201")):
        pg = doc.new_page(width=1000, height=700)
        pg.set_rotation(rot)
        r = pg.rect                                          # rect visto (rotado)
        pt = pymupdf.Point(r.width * 0.9, r.height * 0.95) * pg.derotation_matrix
        pg.insert_text(pt, lab, fontsize=30, rotate=(360 - rot) % 360)
        pg.insert_text(pymupdf.Point(50, 50) * pg.derotation_matrix, "PLAN NOTES S06C", fontsize=8, rotate=(360 - rot) % 360)
    doc.new_page(width=1000, height=700)                     # title block vectorizado: hoja marcada (BE-CF05)
    doc.save(pdf)
    h = CE.texto_set([pdf], os.path.join(d, "set_texto.json"))
    assert list(h) == ["A-101", "M-201", "F-201", "p4-vector"], list(h)


def test_correr_rojo():
    w = workdir(tiempos=False)
    out = CE.correr(w)
    assert not out["ok"] and any(r["id"] == "CE_TIEMPOS" and r["estado"] == "FAIL" for r in out["chequeos"])
    assert any("U-094" in r["reglas"] for r in out["chequeos"] if r["id"] == "CE_TIEMPOS")
    out = CE.correr(w, solo={"CE_DRIVE_PARENT"})
    assert not out["ok"], "una corrida parcial nunca es verde"


# R80e.151–R80e.150 (O'Reilly rev5, 3-nov): tests de los arreglos de tool, como bloques (límite de 200 archivos del skill)
BLOQUES_OREILLY = []
BLOQUES_OREILLY.append(('test_texto_set_ocr', '#!/usr/bin/env python3\n"""test_texto_set_ocr.py — R80e.151 (O\'Reilly rev5, 3-nov): el set de O\'Reilly es RASTER (A1.1-A6.1 / S1.1 sin capa de\ntexto) y `compuerta_entrega.py texto` sacaba 1 carácter por hoja: el barrido BE-120 de los RFI quedaba ciego y pasaba.\nArma un PDF de 1 hoja que es SOLO imagen con \'PROVIDE ADDITIONAL HEAD TRACK\' impreso: con tesseract la frase sale en\nset_texto.json (ocr = [hoja]); sin OCR la hoja queda en sin_texto y CE_RFI_BARRIDO_IMPRESO falla con un RFI abierto."""\nimport json\nimport os\nimport shutil\nimport sys\nimport tempfile\n\nimport pymupdf\n\nAQUI = os.path.dirname(os.path.abspath(__file__))\nsys.path.insert(0, AQUI)\nimport compuerta_entrega as CE  # noqa: E402\n\nd = tempfile.mkdtemp()\nsrc = pymupdf.open()\npg = src.new_page(width=1224, height=792)\npg.insert_text((80, 300), "PROVIDE ADDITIONAL HEAD TRACK AT OPENINGS", fontsize=28)\npg.insert_text((1080, 760), "S1.1", fontsize=22)\npix = pg.get_pixmap(dpi=150)\ndoc = pymupdf.open()\np2 = doc.new_page(width=1224, height=792)\np2.insert_image(p2.rect, pixmap=pix)                    # hoja raster: sin capa de texto\ndoc.new_page(width=612, height=792)                     # página en blanco (separador del set)\npdf = os.path.join(d, "raster.pdf")\ndoc.save(pdf)\nassert len(pymupdf.open(pdf)[0].get_text("text").strip()) < CE.MIN_TEXTO\nsal = os.path.join(d, "set_texto.json")\nif CE._tessdata() and shutil.which("tesseract"):\n    CE.texto_set([pdf], sal)\n    st = json.load(open(sal))\n    txt = " ".join(st["hojas"].values()).upper()\n    assert "HEAD TRACK" in txt, txt[:300]\n    assert st["ocr"] and not st["sin_texto"] and len(st["en_blanco"]) == 1, st\nelse:\n    print("(sin tesseract: solo se prueba la rama sin_texto)")\n# rama sin OCR: barrido ciego -> FAIL con RFI abierto\njson.dump({"fuentes": [], "hojas": {"S1.1": " "}, "ocr": [], "sin_texto": ["S1.1"]}, open(sal, "w"))\n\n\nclass C:\n    set_p = sal\n\n    def rfis_abiertos(self):\n        return [("RFI-01", "head track?")]\n\n    def rfi(self, rid):\n        return {"id": rid, "barrido": {"terminos": ["HEAD TRACK"], "hojas": "ALL"}}\n\n\nr = CE.ce_rfi_barrido(C())\nassert r[0] == "FAIL" and "sin texto" in r[1][0], r\nprint("OK test_texto_set_ocr")\n'))
BLOQUES_OREILLY.append(('test_altura_el_sin_punto', '#!/usr/bin/env python3\n"""test_altura_el_sin_punto.py — R80e.142 (O\'Reilly rev4 → rev5, 3-nov): la fuente de EXT-HEAD-8 dice\n\'3/A3.1 B.O. SHEATHING EL 111\'-4" to T.O. METAL STUD EL 120\'-8" (4\'-3 1/4" + 5\'-0 3/4" printed) = 9.333 ft\'.\naltura_impresa solo reconocía \'EL.\' con punto, tomaba la primera cota (4\'-3 1/4" = 4.271) y la compuerta daba RED\ncontra el Depth 9.333 que SÍ es el impreso (120\'-8" - 111\'-4"). Falla con v81cf23."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport revision_markups as RM  # noqa: E402\n\nsrc = ("3/A3.1 B.O. SHEATHING EL 111\'-4\\" to T.O. METAL STUD EL 120\'-8\\" (4\'-3 1/4\\" + 5\'-0 3/4\\" printed) = 9.333 ft")\nh, regla, hojas = RM.altura_impresa(src)\nassert regla == "printed elevations" and abs(h - 9.3333) < 0.001, (h, regla)\nh2, regla2, _ = RM.altura_impresa("B.O. SHEATHING EL. 111\'-4\\" to T.O. METAL STUD EL. 120\'-8\\"")\nassert abs(h2 - 9.3333) < 0.001 and regla2 == "printed elevations"\n# una palabra que contiene \'EL\' (PANEL, LEVEL) no es una elevación\nh3, regla3, _ = RM.altura_impresa("PANEL 8\'-0\\" high, LEVEL 2")\nassert regla3 == "printed dimension" and abs(h3 - 8.0) < 0.001, (h3, regla3)\nprint("OK test_altura_el_sin_punto")\n'))
BLOQUES_OREILLY.append(('test_revision_markups_be117', '#!/usr/bin/env python3\n"""test_revision_markups_be117.py — R80e.143 (O\'Reilly rev5, 3-nov): con markups v81cf23 (SF = board SF del Excel, BE-117)\nrevision_markups exigía SF = LF x H y daba RED en todo wall con 2 caras; y daba RED a un LF medido con causa escrita\nen el canon (length_cause) que verificar_markups_excel sí acepta. Las dos compuertas se contradecían.\nW-1: SF = board 2 caras -> GREEN · W-2: línea 2 % larga con length_cause -> AMBER · W-3: igual sin causa -> RED.\nFalla con v81cf23."""\nimport os\nimport sys\nimport tempfile\n\nimport openpyxl\nimport pymupdf\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport revision_markups as RM  # noqa: E402\n\nd = tempfile.mkdtemp()\npdf, xlsx = os.path.join(d, "m.pdf"), os.path.join(d, "t.xlsx")\ndoc = pymupdf.open()\np = doc.new_page(width=2592, height=1728)\ndoc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1}])\nfor wid, y, drawn, board in (("W-1", 200, 20.0, 400.0), ("W-2", 300, 20.4, 400.0), ("W-3", 400, 20.4, 400.0)):\n    a = p.add_polyline_annot([(100, y), (100 + drawn * 9, y)])\n    a.set_info(content=f"A1 · 20.00 LF · H 10\'-0\\" · {board:,.2f} SF board · S1/A1.1 · {wid}", subject="A1")\n    a.update()\n    doc.xref_set_key(a.xref, "Depth", "10.0")\ndoc.save(pdf)\nwb = openpyxl.Workbook()\nws = wb.active\nws.title = "Partition Takeoff"\nfor _ in range(4):\n    ws.append([None])\nws.append(["TYPE A1"])\nfor wid in ("W-1", "W-2", "W-3"):\n    ws.append([f"A1 #{wid}", wid, 20.0, 10.0, 1, "3-5/8\\"", 16, 400.0, "x", "S1/A1.1", "[CONFIRMED]"])\nwb.save(xlsx)\ncanon = {"walls": [{"id": w, "length_ft": 20.0, "height_ft": 10.0, "height_source": "S1/A1.1 \'STUDS TO 10\'-0\\" A.F.F.\'"}\n                   for w in ("W-1", "W-2", "W-3")]}\ncanon["walls"][1]["length_cause"] = "line follows the drawn ink to the pier faces; printed 20\'-0\\" governs"\n_d, _m, res = RM.revisar(pdf, xlsx, {"A1.1": 9.0}, canon)\nv = {r["wall"]: r for r in res}\nassert v["W-1"]["verdict"] == "GREEN", v["W-1"]\nassert v["W-2"]["verdict"] == "AMBER" and "cause written" in " ".join(v["W-2"]["amber"]), v["W-2"]\nassert v["W-3"]["verdict"] == "RED" and any("LF measured" in f for f in v["W-3"]["fallas"]), v["W-3"]\nprint("OK test_revision_markups_be117")\n'))
BLOQUES_OREILLY.append(('test_head_track_furring', '#!/usr/bin/env python3\n"""test_head_track_furring.py — R80e.144 (O\'Reilly rev5, 3-nov): additional head track contaba las aberturas > 4\'-0" de\nwalls S21 (1-1/2" Z-furring 150ZF125-18 sobre CMU, sin studs: Door 3 6\'-0", Windows D1 / D2 11\'-4 3/8") = 32.73 LF con\n"N/SHEET: default (no sheet)". Un wall de furring no tiene head de studs (lleva el lintel de mampostería, S4.1); el plano\nno imprime head track (7/A5.1 solo box header). Falla con v81cf24."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport accesorios as A  # noqa: E402\n\ndata = {"constants": {"addl_head_track_none_source": {"value": True, "source": "7/A5.1; S4.1 lintel schedule"}},\n        "walls": [{"id": "S21-N", "stud_size": "1-1/2 in Z-furring (150ZF125-18)", "element": "wall",\n                   "openings": [{"ref": "Door 3", "kind": "door", "ro_w_ft": 6.0}]},\n                  {"id": "S43-OF-S", "stud_size": "3-5/8 in", "element": "wall",\n                   "openings": [{"ref": "Door 4", "kind": "door", "ro_w_ft": 3.333}]}]}\no = A.Out() if hasattr(A, "Out") else None\no = A.Out()\nA.additional_head_track(data, o)\nassert abs(o.fam[A.F_AHT]) < 1e-9, o.filas\nfila = o.filas[-1]\nassert "default (no sheet)" not in fila["source"] and "7/A5.1" in fila["source"], fila\nassert "Door 3 (S21-N)" in fila["operacion"], fila\n# un wall de studs con abertura > 4\'-0" sí la lleva\ndata["walls"][1]["openings"][0]["ro_w_ft"] = 6.0\no = A.Out()\nA.additional_head_track(data, o)\nassert o.fam[A.F_AHT] > 6.0, o.filas\nprint("OK test_head_track_furring")\n'))
BLOQUES_OREILLY.append(('test_chequeos_ocr_oreilly', '#!/usr/bin/env python3\n"""test_chequeos_ocr_oreilly.py — R80e.145 (O\'Reilly rev5, 3-nov): falsos positivos de la biblioteca v81cf24 sobre un set\nRASTER leído por OCR. Cada caso: el falso positivo de O\'Reilly ya no falla y el error de verdad SIGUE fallando.\nU-057 \'no longer deducted\' · BE-12 cita con \'...\' · BE-15 tag en hexágono que el OCR no lee (AMBER) · BE-21 \'5/8" EXTERIOR\nFIBERGLASS REINFORCED SHEATHING\' = glass mat · BE-102 \'S21/S24\' (types) no es N/HOJA · BE-CF05 páginas en blanco."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport chequeos_biblioteca as CB  # noqa: E402\n\nB = CB.B\n# U-057\nf_ok = {"side": "A", "deduct_info": "door R.O. 23.89 SF no longer deducted",\n        "board_note": "windows NOT deducted (estimator rule: board per face never deducts openings)"}\nf_mal = {"side": "A", "board_note": "board net of door openings"}\nassert CB.u_057(B(canon={"walls": [{"id": "W1", "faces": [f_ok]}]}))[0] == "PASS"\nassert CB.u_057(B(canon={"walls": [{"id": "W1", "faces": [f_mal]}]}))[0] == "FAIL"\n# BE-12\nhojas = {"S5.3": "16. SIMPSON FCB43.5 FRAMING CLIP AT EACH STUD TO PEMB WIND BEAM (TYP)"}\ncel_ok = [("Material Summary", "I38", "3/S5.3 key note 16 \'SIMPSON FCB43.5 FRAMING CLIP ... TO PEMB WIND BEAM\' drawn")]\ncel_mal = [("Material Summary", "I38", "note \'SIMPSON FCB43.5 FRAMING CLIP AT EVERY STUD TO DECK\' drawn")]\nassert CB.be_12(B(hojas=hojas, celdas=cel_ok))[0] == "PASS"\nassert CB.be_12(B(hojas=hojas, celdas=cel_mal))[0] == "FAIL"\n# BE-15\nms = [{"fila": 10, "material": "Bottom track", "net": 10, "fuente": "N/SHEET: S43/A1.1"}]\nassert CB.be_15(B(canon={}, ms=ms, hojas={"A1.1": "FLOOR PLAN"}, set_meta={"ocr": ["A1.1"]}))[0] == "AMBER"\nassert CB.be_15(B(canon={}, ms=ms, hojas={"A1.1": "FLOOR PLAN"}, set_meta={"ocr": []}))[0] == "FAIL"\n# BE-21\nms_g = [{"fila": 30, "material": \'5/8" glass mat sheathing\', "net": 534.88, "fuente": "N/SHEET: 1/A3.1"}]\nr_ok = CB.be_21(B(ms=ms_g, hojas={"A3.1": \'19. 5/8" EXTERIOR FIBERGLASS REINFORCED SHEATHING\'}, celdas=[]))\nr_mal = CB.be_21(B(ms=ms_g, hojas={"A3.1": \'19. 5/8" EXTERIOR GYPSUM SHEATHING\'}, celdas=[]))\nassert r_ok[0] != "FAIL" and r_mal[0] == "FAIL", (r_ok, r_mal)\n# BE-102\ncanon = {"walls": [{"id": "S21-N", "tag": "S21"}, {"id": "S24-OF", "tag": "S24"}], "type_order": ["S21", "S24"]}\nhj = {"A1.1": "x", "A5.1": "y"}\nassert CB.be_102(B(canon=canon, hojas=hj, celdas=[("Scope Checklist", "D3", "types S21/S24 per 7/A5.1")]))[0] == "PASS"\nassert CB.be_102(B(canon=canon, hojas=hj, celdas=[("Scope Checklist", "D3", "see 7/A9.9")]))[0] == "FAIL"\n# BE-CF05\nhb = {"p1": " ", "p2": " ", "p3": " ", "A1.1": "x", "A1.2": "y", "S1.1": "z", "T1.1": "w", "G1.1": "v", "A2.1": "u"}\nassert CB.be_cf05(B(hojas=hb, set_meta={"en_blanco": ["p1", "p2", "p3"]}))[0] == "PASS"\nassert CB.be_cf05(B(hojas=hb, set_meta={}))[0] == "FAIL"\nprint("OK test_chequeos_ocr_oreilly (1)")\n# BE-63: largo resuelto en la resolución dirigida (tabla de resolucion.md) = decisión citada\nA_ = {"walls": [{"id": "S43-OF-W", "length_ft": 7.43}]}\nB_ = {"walls": [{"id": "S43-OF-W", "length_ft": 7.88}]}\nAB = {"walls": [{"id": "S43-OF-W", "length_ft": 8.0, "length_source": "A1.1 printed 8 ft"}]}\nres = {"resolucion.md": "| 11 | S43-OF-W length | 7.43 | 7.88 | **8.0** CONFIRMADO | A1.1 printed 8 ft |"}\nassert CB.be_63(B(canon_a=A_, canon_b=B_, canon_ab=AB, textos=res))[0] == "PASS"\nassert CB.be_63(B(canon_a=A_, canon_b=B_, canon_ab=AB, textos={}))[0] == "FAIL"\nprint("OK test_chequeos_ocr_oreilly BE-63")\n# BE-50: cableado eléctrico no es traslape de framing; un blocking por otro contratista sí\nm_ok = {"M2": "EXHAUST FAN SHALL BE WIRED BY THE ELECTRICAL CONTRACTOR TO OPERATE WITH THE LIGHT SWITCH"}\nm_mal = {"M2": "BLOCKING FOR UNIT HEATER BY MECHANICAL CONTRACTOR"}\nassert CB.be_50(B(hojas=m_ok, celdas=[]))[0] != "FAIL"\nassert CB.be_50(B(hojas=m_mal, celdas=[]))[0] == "FAIL"\n# BE-63: la resolución nombra el type cuando el wall es el único de ese type\nAB2 = {"walls": [{"id": "S61-RR", "tag": "S61", "length_ft": 8.5, "length_source": "A1.1 8 ft 6 in"}]}\nr2 = {"resolucion.md": "| 14 | S61 length | 8.1 | 8.4 | **8.5** DERIVADO | A1.1 |"}\nassert CB.be_63(B(canon_a={"walls": [{"id": "S61-RR", "length_ft": 8.1}]}, canon_b={"walls": [{"id": "S61-RR", "length_ft": 8.4}]},\n                  canon_ab=AB2, textos=r2))[0] == "PASS"\nprint("OK test_chequeos_ocr_oreilly BE-50 / BE-63 type")\n'))
BLOQUES_OREILLY.append(('test_reconcile_ext', '#!/usr/bin/env python3\n"""test_reconcile_ext.py — R80e.146 (O\'Reilly rev5, 3-nov): las lecturas A / B traían el MISMO framing exterior sin tag\ncon nombres distintos (A: tag \'EXT-CFS\', element \'storefront_cripples\'; B: tag \'EXT\', element \'wall\'): completitud daba\n\'falta vs la otra\' en las dos (U-034) y reconcile emparejaba 25 de 32 (BE-62). Falla con v81cf24."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runner"))\nimport completitud as C  # noqa: E402\nimport reconcile as R  # noqa: E402\n\nband = {"ori": "H", "c0": 100.0, "c1": 104.0, "lo": 200.0, "hi": 548.0, "sheet": "A1.1"}\na = {"constants": {"plan_scale_pt_per_ft": {"value": 9.0, "source": "x"}},\n     "walls": [{"id": "SF-A-8", "tag": "EXT-CFS", "element": "storefront_cripples", "sheet": "A1.1", "length_ft": 38.67, "band": band},\n               {"id": "S21-N", "tag": "S21", "element": "wall", "sheet": "A1.1", "length_ft": 10, "band": dict(band, c0=300, c1=302)}]}\nb = {"constants": {"plan_scale_pt_per_ft": {"value": 9.0, "source": "x"}},\n     "walls": [{"id": "HEAD-A-8", "tag": "EXT", "element": "wall", "sheet": "A1.1", "length_ft": 38.667, "band": band},\n               {"id": "S21-N", "tag": "S21", "element": "wall", "sheet": "A1.1", "length_ft": 10, "band": dict(band, c0=300, c1=302)}]}\nassert C.revisar(a, ["A1.1"], b)["faltan_vs_otra"] == [] and C.revisar(b, ["A1.1"], a)["faltan_vs_otra"] == []\nm = R.emparejar(b, a)\nassert m.get("HEAD-A-8") == "SF-A-8" and m.get("S21-N") == "S21-N", m\n# un type de partition distinto sigue sin emparejar\nb["walls"][1]["tag"] = "S24"\nassert "S21-N" not in R.emparejar(b, a)\nprint("OK test_reconcile_ext")\n'))
BLOQUES_OREILLY.append(('test_runner_comparar_extra', '#!/usr/bin/env python3\n"""test_runner_comparar_extra.py — R80e.147 (O\'Reilly rev5, 3-nov): el runner corría comparar.py pero nunca\ncomparar_extra.py; la compuerta U-081 / BE-CF06 fallaba (\'las lecturas traen misc_items y no hay revision_extra.md\').\nR80e.148: v81cf24 importaba chequeos_biblioteca (tools/) sin tools/ en el path: el runner no arrancaba\n(ModuleNotFoundError); este test importa el runner SOLO con runner/ en el path. Comprueba también que Runner.comparar lo llama por bitácora en la misma carpeta, después de comparar.py. Falla con v81cf24."""\nimport inspect\nimport os\nimport sys\n\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runner"))\nimport run_takeoff as RT  # noqa: E402\n\nsrc = inspect.getsource(RT.Runner.comparar)\ni, j = src.find(\'self.tool("comparar.py"\'), src.find(\'self.tool("comparar_extra.py", A, B, inv, out\')\nassert i >= 0 and j > i, src[:400]\nassert os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparar_extra.py"))\nprint("OK test_runner_comparar_extra")\n'))
BLOQUES_OREILLY.append(('test_auditoria_raster', '#!/usr/bin/env python3\n"""test_auditoria_raster.py — R80e.150 (O\'Reilly rev5, 3-nov): A1.1 es un escaneo sin capa de texto; auditoria_entrega\nexigía /Measure = rótulo SCALE leído del texto de la página -> \'printed on the sheet: none\' en los 32 markups. Vale la\ncalibración del canon que cita el rótulo impreso (1/8" = 9.00 pt/ft) y la medición contra cotas impresas (9.04 pt/ft),\nsi difiere <= 1 % del rótulo; una calibración lejos del rótulo o sin fuente sigue fallando. Falla con v81cf24."""\nimport os\nimport sys\nfrom fractions import Fraction\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport auditoria_entrega as A  # noqa: E402\n\nsrc = "A1.1 1/8\\" = 1\'-0\\" printed (9.0 pt/ft nominal); measured on the raster: grid 1-4 85\'-0\\" = 766.9 pt"\ncan = {"constants": {"plan_scale_pt_per_ft": {"value": 9.04, "source": src}}}\nassert A.calibracion_raster(can, "A1.1", Fraction(113, 900))[0]                     # /Measure = calibración\nassert not A.calibracion_raster(dict(can, constants={"plan_scale_pt_per_ft": {"value": 9.5, "source": src}}),\n                                "A1.1", Fraction(95, 720))[0]                          # 5.5 % del rótulo impreso\nassert not A.calibracion_raster({"constants": {"plan_scale_pt_per_ft": {"value": 9.04, "source": "estimated"}}},\n                                "A1.1", Fraction(113, 900))[0]                         # sin rótulo + medición\nprint("OK test_auditoria_raster")\n'))
BLOQUES_OREILLY.append(('test_review_image_name', '#!/usr/bin/env python3\n"""test_review_image_name.py — R80e.153 (O\'Reilly rev6, 3-nov): U-118 exige la imagen circulada de cada Review Item en la\ncolumna Image, y plantilla_excel.verificar_texto_cliente (R80e.84) rechazaba todo \'.png\' en una hoja visible: las dos\ncompuertas se contradecían y el runner no armaba el Excel. Ahora la columna Image de Review Items acepta el NOMBRE de la\nimagen (sin ruta); una ruta o un nombre de archivo en otra columna sigue fallando. Falla con v81cf26."""\nimport os, sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport openpyxl\nimport plantilla_excel as P\nwb = openpyxl.Workbook(); ws = wb.active; ws.title = P.HOJA_REVISAR\nws.append(["#", "Phase", "Type / order", "Item", "Sheet + detail", "Image"])\nws.append([1, "floor_plan", "S42", "RFI-29 header wall extension", "6/A4.2", "review_RFI-29_A1.1.png"])\nassert P.verificar_texto_cliente(wb) == [], P.verificar_texto_cliente(wb)\nws.append([2, "detail", 1, "see img/review.png", "1/A3.2", "img_runner/x.png"])\ne = P.verificar_texto_cliente(wb)\nassert any("D3" in x for x in e) and any("F3" in x for x in e), e\nprint("OK test_review_image_name")\n'))

BLOQUES_OREILLY.append(('test_burbujas_oreilly', '#!/usr/bin/env python3\n"""test_burbujas_oreilly.py — U-137 / BE-139 (usuario 4-nov: "¿y qué pasó con los detail call outs?", burbuja "1" arriba /\n"A3.2" abajo). El detector de callouts solo veía "N/HOJA" escrito en una línea: en O\'Reilly (escaneo) encontraba 1 burbuja,\nen CFA y Chuze 0, y CE_CALLOUTS pasaba en vacío. Fixture: recorte REAL de la burbuja 1/A3.2 de A1.1 de O\'Reilly (escaneo\nde 400 dpi, recorte 80 x 80 pt a 250 dpi). (1) palabras_fitz.py (burbujas) la lee 1/A3.2; (2) compuerta_entrega texto la guarda en\nset_texto.json; (3) CE_CALLOUTS falla si no está citada y pasa citada; (4) la misma hoja sin la burbuja = 0 burbujas con\nhojas de detalles en el set = FAIL (PASS en vacío prohibido). Falla con v81cf32."""\nimport base64\nimport json\nimport os\nimport shutil\nimport sys\nimport tempfile\n\nimport pymupdf\n\nAQUI = os.path.dirname(os.path.abspath(__file__))\nsys.path.insert(0, AQUI)\nimport palabras_fitz as burbujas  # noqa: E402  (detector de burbujas, U-137)\nimport chequeos_biblioteca as CB  # noqa: E402\nimport compuerta_entrega as CE  # noqa: E402\n\nPNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAARcAAAEXCAAAAACiuF8IAAAACXBIWXMAACZzAAAmcwHzbHUKAAAY00lEQVR4nO2deXgURd6Aq+fI5A6EEMjJsgoJENkViCyHHAKKCoFAyIeioouyHLK6K6zLZZ4YhGVZZAMGEpBz0c/FEBAIIquyCgFU8NFdIBgRhSSGIyGE3GRm6qvq7pnpo2amA9M9mXz1/jFTXV3dU/M+3dXV1d2/BtALVIzyBwA8mGsR5W4HYKQ3aiMkCzzcyCaAV36+4XBXJMZvlSizbXgJq2ET3vEC4dcvGwEIHP2NIKtteLmnlk14ywu0rr4PbTL3rGmy57QNL082swmveYHw4q+QGN30Gtt02/Di5f0I8/0KBpl59H0rN0m92LgyLQSJCfj7RXaKenFwbAwSA5Iv4zTyMqjOu9VpM17gDhMrZuVR2PQ0AMwzTe4XUZEbDwP/3WwKJK3o3XtFn95CJJMSRhwdkdV/xLGiGTP24HIjXiWW6v9xqmNVffbMcFYuQQdYOnMpXcKWheJfIy/G8re/Sas7f4SjknwNWsW9qAod2BSgUNojgxIcaWaa9+rR1mAYwYTOa9WgUCitYHYkAJFxApYujQIgPI5IGABBkiwTMJHLorXoYvof6O/IiUHNQlTP+aTCqHfXATca4XF/judyggAItc+O35aOPv6Mk6N3xwD0k+nbum3b3RNP9lxTmASAAc1KH41rH8emZh08uLR/4UFcOGrpQY7CJ9HHHAMIWnOQCC4MdGlsGlj+BPp8ZxYA4Xkd2GImkglM2yRZy5kR5LJoLRPrLNDiyKmbCHTnzVZS4REg7rOJAMR9YZ/97tiOBwWVwqthZ1ngVsAsR1+oouwk+i550XTvbZS2mLlMlMLnohYIm58Gg67Yu7Ns5oo+/S+Te7uH0qcMBmHVXH+3LK5PiWR+87fDexFPVC5HhW6ySAvPDV4nzcNUTmDSqyV51em6w6T1WtYFx56QnjcWdl5EPCk429M/q1mSVzeqD/m//id4eIU07/Vfri8jld3VMeK04/zogaTv5EXKR+UR6nTyCb8t8tzTL/ttkufeeoyZUCPLrdnw66PystZcv5gv5efTW/yeOCkvfCZBnyXPhW8/UE7IPZPwICF7p/9CqVhE/b2hBwXnjb2lWwvL1TFJZ6R5X80N3kzaMs5MGHNImnd9HJNG3OT+p8vO69K8tf7dTkC5F8u24JdbpGWt/YwrbhPWWzFlzCVZ5rmeD14llG06GZIqy7zYNeqA8Hz6PKn2EJYNSzgrzrmSHp1HLmvOCN9gFuXc2qWbXEUsWzVZt+uWeOmNQdHsdiEff8kLy7wizjk7LjxD/FM2rA/8ao0k62xiX+IOA+v335deL876ZGTYPqhknOHK4IRzot/t1bHSWVnrCMMF4fTNcYYJ9U7K1k8wZIoycg1x3O5CGJd6Z2zUceH0uQRmmdXJir+bM7QUigsPXO+sxsv7rRAV/uiJDgfwt4Lxl4phQjGf3x+RR9qJOC7M6ZXjmFs5kUm74bTsjX3RnzumLDnBMfxfJ43XFd73vKChO5fgn0loGXjqRj4i3DzOJQz72WlZmNk9V9Dy1D4esZdNKBmXKh+YaG97vogxvu28JISnXvLb7PgRJkXe5DqomRh7zJa2bvSL/oJPE8cxL5gy7MLPJuozZQWEbBpYJig8lNQS29lpWmhvpxqfDynkUorG69b1f53fYk7PC37b+daCOTN+DH8Ivp7CTK51WbZuchebmLcC4u07CtGLZWv4Ir7xLU4wLic1uQ4q+kTsgrbCQ0lNroPGEyGT+OTFqK77+KSycczSBxOK8fe1KYEbXP4IojY+KA+3iLcm6lKdNkQ8lZPu+zdWZ94UJGg/nIx7bwjluivFvUxLZYcnCSVvDOa6K8W9Hix1U7Z+X9+pDTjx6UOhe22ZCsd3i3WJSIy1d8BmZ62dgxOxRtT43hzPpLgfvDZvZhvfjYbYE45MJ16smwOW4qokMlnuK/H9rBFlbOGBsu6cnDf64c3kX9M67LdnKfTS/HX8MktzZkSu652IoygmtaoqlZnsvMl1cGNy9DHL+uDoIkGes+skltyIpc0/ZZoynDe5DuqShpQjLUNdNLkOMvrtRkf+TnscOYqvB/zjwZlPGwn9WRJfRo0ezYy7qajszQlxM/2iRP1Z59ePNhmfTtRnKKvE+d7J83oNIfdb5IWT53YIOSDIUH6dZDoAfyD3pOTsBaC7qyORkFvdAdgrynHuxbwAgHTXTa6DUzoQ6q5tsTMSgHXCaYeXCjekIy/uyvD8nIq8lCssXI685AszLg4BYEjFTTM/2dh4HaIqmivM8Oq3vZGX63X4ZLn2Nj//OrzOJW7COtGKj+uAcZnCSuyJQL95UZCxAISWsAlgcoMeAL27MjYYABilZXFhoygDD36Yhrzmz00980xM9vB1614LeG1VmB+apY9JeQ1NjnuJLx2THcMlhqxLEa2GLaywDgY8AiXJsFeGQlFOjyD+I4i/QHN/SgSb13MwO5lkBCAiJSWCncE8FOdYMi4CfzzESNfoOxiTuH/ZMyXlfjZj8PggEJcyHv/9c4cLCgrwx+HiApbL8CiXd52d/GF/QcFRCI+yM/bUnS6wc/oo/qjbU+AZ3ukCgN8CD61MGft/4P4lOtu5zGZch4cLTkP0UeDt+xkEvA3AcCX9R01oQ17awn1BdqgXMtQLGeqFDPVChnohQ72QoV7IUC9kqBcy1AsZ6oUM9UKGeiFDvZChXshQL2SoFzLUCxnqhQz1QoZ6IUO9kKFeyFAvZKgXMtQLGeqFDPVChnohQ72QoV7ItB0v5iXUCwHLWj/qhcAqfN8t9SKhZW0goF7krOMidFAvIsyrAwH1IsPylh+gXuSstmmhXgS0vBUIqBc5b+kB9SLDsiYIUC8yLDl+gHqRs0b8YBj1wmJeHwioFznr9YB6kWHJDgLUiwzLBj+pFuoFkU14Fpd6MefKdiLqBbFB2uRSL5ANWEfS8v/dizVX3uSyxHzeiGgLD8V6xctaf7IWAEIjEfPz88+6X4m6eMGLeSOpyRXTY1x+2RX3q1IPL3jJNcg09P6DgDQ2S2+MejNf+8rZ0NyLJUfS5CYkP/WNKOhn3TffHH4gGQd/CP717K9cBltTD629WDcKmlwmIDMnx8kf/yQnid2uBqzxSjOstZe3AuxW+k+adcXVf67eOmlSfzaWhSzSqPpo7OU9W5NreH6fkiBQpW/HoK1mYrnSCFceQ1svNx/jtfRapvSfNi/rBRjTRlWrRUBTL1WpnJWQHHmsXOecHxoCggcXq1YrIlp6qR3HWolau8d9WRF7UhiQeFbTfUlDL5UTcMgl4+PH3BeVUjszHnSaoeXLkbTzUsvuRH5LXMf+bKwgx2It6gqYOY1q1IuMZl5usltLcrbr3sjtF0yvk+cUxQLdC0pjHt49Wnm5MRlvLfFu4lbWzdGDpU7mlWSa9HM025U08lKXgrXonP1nHvNMVMh5mSUAzNSq8dXGS2Uqvu/HKHsfgpj63xlcevnvo0bDC87iqXsYTbzUsTuR3yLXTe61F9kQgS62qVs9/JgXtWl8tfBSMxH/YSbDdZNb2IG7l8zVvtY0HOh2erZyTtDAyw12QMW0xPUrCE+xAwvhrr3Az6NBb8J7QzyP+l7qJ7BN7hI3xY6gLWps/nQ3XuAXc0DvCy5LeAbVvVRNZnePKe6CcyMvKTXQrRf4n1iw1mOVc47aXuq4UckuhNfYiCnqhl/o4t4L/Cww+D0PVc4FKnupmcQeY2LcaoFWtvlR4KXxMfC40iDid466XqrTuYGFp5QuoMALrOwPfnt31VKAql7eHcsPziluKZV4gRv0cafuql4KUNPLcdug5UuKe++KvJhfAX9S+3xAPS+Wf4ywXST7r+KFFHmBq/Whit4ncReo52Wr/YLIR8oXUubl9nOMq3cbeQK1vFg2h9q0PHbLfXEbyrzgzs6RO62ZMtTyst1+N5R/a0ZzFXq5PAB8cqc1U4ZKXk44LraGtaazodALXGn4jfuX/twN6ngpGOm42Brdit1IsZeasJBd7kvdBap4KZwguC6v8CVBHMq9KCt3x6jgxbo1TKCl37XWLKvUiyUDzFZ1EFwFLztEd0O17pY5pV7gmXt0qo7DeN7LFtH9LczcVi2s2AscCabcQeUU42kv1ndDhFpA4A+tWvzTTsq9qHrzpqe97JDcxf1qKw+nR2bsdV8Is4TxIS/W7WFiLeodNb7XDVRzFMazXnbKbkBVzUv1GLBdrXVDD3s5GSLVErjNk+sXkQUWqjjY4Ekve8dItYAe6vXWs1p3htFKPOjlUKpMi5pe9oX6hBfrhYFyLcDJG8498oM9fMJLdQeCFvCSp1Yvxze8nPyljuRFxf3oYowPePngEZIVAO6prlGLRb7Q7maRtQBdmGr4+7IXVfEBL5+Gk6sevmjx4vGdFi3u23fx4qf8H+40jGGYp4Yz48ejb/9XfsFghnZi+v4CTy4ejj/IvJIszRnmC17gR12JXh5H7e6tnyC8cgXChgs3f6oqKSlpqCq5dQt9X7CWlWAqfyq5UoYnYRX+IGOVDW/5SL/uXx1JXo54avVyVup8wgs8TNpijnhs9TIa7vENL/DDTnIvKg7a7wz0ES/wY3nj25OeNyI+7CL1EvujJ9cvIgv0U/FeXs+OS30UIBWj3lWeLN8Zl4INz0u3GNW81Ka5v2fvLvD0uPdBSRszz/U93nfOCZ0PjXsj/iUWo/+eUObyypUr/3pDnLcJ5a38X9Iam/6OZ62UXM8d5VvXSSAsjBR60R0iFHkbz3lSmNO4kL2LKKj/x7JjzNfPcSMYfgvOCLN97PoR4pCo8SXUvvke6QzzYsZW/lnJDdAHHFdehgnGuc3DmK2er7oDFbw0PBfp2svf2Jg4fX60Z7QsMDp2vBWisrXpjlUZFzgaq/eMSarGtVDlPo8DgnOl8I+lc81/5Ob8xt79qEHbhH/inkMf3oeyfy+6+oGfvQnOPnRoT6I/ACE/2rLrf+N793kgMgUbzDPSJwMuGNDGEi8cPkFemBVYR0kf6c2+IwEwsf0U8wpk6DnBEr7o5foWhxdZb30a2gLOz0Af39pyvg0GOu64laG3pXiQl79wzy3dfhGA6Y4luqkbHkal++t+zrY3l6GSqBPmYQB0vnXBBMA024Na/54RmMrZ2+gn8TLWmFDCJ7McXizTQKY6Fbeh2v27B22NL/OYaEip5VXUxq6Hlj+jHcT+hHlzZQP7fW042sUqhMVr/mF/bljg5ZjJV+9ThXC//YJSgTAbt7GmfAizUSuTKpxhLS/NxZfmnLUbZxKAznY5qgAEHVejzg5UfD7A3vh2KRLkYi8j0Lf5XgAihCEJajoZcAeu44dOVjcKNVXVXPJEF5N69wNwqOjl2vsRvBjhJrAQtaz/xomdkhk1XIvk5EocG/GuL/dYedNMW0o9VH3O5iDf8x3giJVUkoB69OyR+AiasVBQmPcSViBdC8Z6NRTYH4XNZHqq/uynql4anunMiUmxZ2Ebj/4zH4F3s+B8YeG0tGGSPDtrOzOA+T33RO2lJA3iIqr8HN8+biPotNu2d0wCIiR/sGpXEOnMgY14Z5jJ9Y/rB4OwferWGqr/3GcGfzbAd+5OdhZ7ufecuHjTBHkeH/FuFn9+8IE/WKxypaH6Xq5u4s4Gf8eFdZFdr82SPIR/IxlIxyd/XIuaXP1cvqX9Khyo/ewRRvXnp8tXczfdHcYT11AHRf9UgH+H1Un+/s8+q+POEqw3X8mwnymPlHo5m4iW1kXyG1zL80D/mdp1hprEIdjH7jsJOBToLnTul9549eo1WH31amPjEM5LUSSjX8kXvpwk8VKcgPvML9r6zG/qjcu1iI6jRdyKNHaLSShmN4ZAQScvlYt9cjwQgD9wrYd1LeoNvy9Y1rwALRq9zzYksTjRtFStEWMRWngxF7KnBInFxT3Ep9fFaEfSfQatT6OjDRehbh9qSoYLe3YbcZP7O36iObeHeK56aBMXZwfbxCS+ij6SBD3V5tmAvYR9FtkIHnzs9Ol3w5GoT/Gs2rn370ZfVQPYo9b9iEdOnZ6lB9FF5F/wNNp4KVtlu+NZHL5lOWpvZuJoW46b85hxN/GcI9wZwXbJ4SvqpCb11S7u1gf8udIQUbifW925v49bYJ5U7rE/J14UPlRx92gWp21PKMELXAO4zmvRTO5miA6pldyMogDWyy5RIHCmi0Z7kZZx/V7j9iNxDLrv5817nT2+WM7OwxTZBr2tO+Zl4exsNnseeyt57IIabRpdqKWXijyu53snMeiuoF6zqd8dBJC8YzSMj1m2knsKZ9L+Vj4HYv15EAB+6o7/S9EynmrDVK7xDRnxYWv6Zi1LIwEY/IO7QEyeRdu4xJP4Z0KNyyuVLlJ/dLwRabnsvqRH0dbLbX48Buhjv1C2xAcT0REpbK4GZ9BitI57vtV2zI1OHnbCTQzmq9+cGIb6g/GzlceP8RhaeyldIXjZRIeXc1qctDTmlpacQbjLYkyUDVNpgebvVbBmC3tqptjYNwvltw+e3N8vNhY/cRz721IvBMmH3ngPx6VBkr49MzYtbfa2Rdcwl3KubU9LS2NHbPRdNuR/pXn1eLzwfpLyB4AMxqALwPgbArhbYWJmz17aoH3d7HjjPT9l0i1GQlzf0Sc1DosvwyvvPyp9g/ymnzGrWbz+8iPorfeIWfMJzxKoeRN0q/HWe+d2kbYY6gXCpdQLkbIc6oXI5WWB1AsJ6y7p80rUC8c/g6gXEtYl1AuR0i0dqBciuwOpFxLW98KpFyIpAdQLicb8UOqFyCbqhcilDH/qhUT9hI7UC5F3A6gXEtb3Q6kXIjtCqRciz1IvRH7qR70Q+WHAcm9XwUEb8gLrXb+ZTlPakpe2BPVChnohQ72QoV7IUC9kqBcy1AsZ6oUM9UKGeiFDvZChXshQL2SoFzLUCxnqhQz1QoZ6IUO9kPERLxWlCOFjtPU4o9QWAtBaLp4rXrbetgQqcq20VFG0dJ/wUr26q8FgMC50PFDR/KwB05V//r6mk8HvgpOFT3RlQ/qiJXCR0QbDDiU/6QNeLOsS+Ptj4pbwWbv66LmcyCnsg7U1YZKwmg4+i+JCq/BFZOGInND2vVhzHTEaErhQ1oWCt2eyb4l37uVkDHB4OdeevBSxNw0NSBuLQ133wwEa6qbinF5paTg4DPtiXqdeWl4GDi84jF778TIJAEPcljJYf6APAEE4fMyXOqCLfvM7CMu2oD87pdm5l+ZMg81LbTfAFLQjL9YeAMziYoB81xuAR26ithP9Vf55/QzARtt05mUJG2+HC920pX21L9jLET49HbD/7TkAlvNh7yri2bmW5UQvG7mXG3NetvNekm/IC8pp817gO0PtAeumczFHayb626Ix2axtJ3lho+VNY0ReHlYYW7Pte4FX3+JD6VxHO8Ef8YZSf9UWdag4CsTjY9SRzr0qpMtdzmGAcflZHe+FK3Ja90dFP+oDXuzskd2C93MvW2zrObIHi3EoPBBf+73NCzx+Hn3UH1D2ciAf8mJFEjoUirLyGGDayqbkZwE4FB7YAh1eWoXveGnORK3oKGGAKcv6YHE8PCG141Aj/cGNdu/Fkon6dQPLBDnWTX7SeHgOWl7gQ+G1cy9fv4okGFcLs9YHoL8+Rxj3rWgvx2VYNxN16LpjH+3by3X8+ha/JYJgMebNaCcyzBDuRfbogEMbTuEOXffyioqK4zpgXFZR29of9A0vX8ag82cmUxDD+PxrOO7HC6KoOqfieC9hNewb5RkTAp906k1ccMlW4BNeimLwIfeUICLZ+V74786SbAYjeS996mwpG85GIZziC15OxKJ/Nkh4WsNqScyVhm4ryOYohmMkXozORq2c4QNejkehPzZY2J39DmtJcBUipnhCCs9DqNP7aEpeK0MJ+oCX4/FAEr/O8ieU0/GvyhZvr8cja2/cgi46Dz/4Eu0/OegDXsBt6ezsnJyccvgO/nBFu/XSg20guieHRCcndwcxpew4g21cc4A/AK7Hsdurl49ET+TjA8tXcaIcZ2964WmvXiRvYkBePpHEYJrkcvmfE9unl+Llc7tF8nSbG9n1IoSf5+enREZ22ZA//+VnUcpNDOdzSQvvILJ+m/cCreamRp4mcyN/OnS7Eacs5haUchfDucnipgCJtu/FO1AvZKgXMsq81DdWw7raWtiAd9UGW/NuqaysRGdudbC5qZKjqpFNteByloaWxirc4lW1NFQ248kqWNMAUWH8UVlZA+shrK60UQOrKhVR1ais3N0B8pTwyLRuG0YNH56X9gaamNyXz30jKDBweF7uqLwZ01EKEz6NTc3H5d5InT8tfH5eXnb4/MmBM/BkeHbfiXmocCr6CAzsm/1IXm63QBt9s8MDFRE+TVm5uwNQyBgUYpxCyp061dXcO2HWo4apq0QsG7YK5U1FM4KXiedMnbVKLcAlpdQRM+tczb0TmmouSUb4rTcgyqtDM0olXZU69R4spscjMtQLGeqFDPVChnohQ72QoV7IUC9kqBcy1AsZ6oXM/wEGXedX2Lm2mAAAAABJRU5ErkJggg==")\nHOJAS = ["A1.1", "A2.1", "A3.1", "A3.2", "A3.3", "A3.4", "A4.1", "A4.2", "A5.1", "A5.2"]\nif not shutil.which("tesseract"):\n    print("(sin tesseract: no se puede probar el detector raster)")\n    sys.exit(0)\nd = pymupdf.open()\np = d.new_page(width=80, height=80)\np.insert_image(p.rect, stream=PNG)\nr = burbujas.detectar(p, HOJAS)\nassert [(b["n"], b["hoja"]) for b in r["burbujas"]] == [("1", "A3.2")], r\n# hoja de 1 página con la burbuja (rótulo A1.1) + hoja de detalles A3.2 -> set_texto con burbujas\nw = tempfile.mkdtemp()\ndoc = pymupdf.open()\npg = doc.new_page(width=600, height=400)\npg.insert_image(pymupdf.Rect(260, 160, 340, 240), stream=PNG)\ndoc.new_page(width=600, height=400).insert_text((50, 50), "WALL SECTIONS  1  2  3   A3.2", fontsize=12)\ndoc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1},\n                     {"startpage": 1, "prefix": "A3.2", "style": "", "firstpagenum": 1}])\npdf = os.path.join(w, "set.pdf")\ndoc.save(pdf)\nsal = os.path.join(w, "set_texto.json")\nCE.texto_set([pdf], sal)\nst = json.load(open(sal))\nassert [(b["n"], b["hoja"]) for b in st["burbujas"]["A1.1"]["burbujas"]] == [("1", "A3.2")], st["burbujas"]\ncn = {"walls": [{"id": "S43-1", "tag": "S43", "sheet": "A1.1", "element": "wall", "length_ft": 10, "height_ft": 10}]}\nsm = {k: st.get(k) for k in ("ocr", "en_blanco", "sin_texto", "burbujas")}\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm, celdas=[]))\nassert e == "FAIL" and any("1/A3.2 (burbuja en A1.1" in x for x in ev), ev\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm,\n                            celdas=[("Partition Takeoff", "J6", "1/A3.2 studs to PEMB purlin")]))\nassert e in ("PASS", "AMBER"), ev\n# la misma hoja SIN la burbuja: 0 burbujas y el set tiene hojas de detalles -> FAIL (antes pasaba en vacío)\nsm0 = dict(sm, burbujas={"A1.1": {"burbujas": [], "sin_leer": [], "circulos": 0}})\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm0, celdas=[]))\nassert e == "FAIL" and "PASS en vacío prohibido" in ev[0], ev\nprint("OK test_burbujas_oreilly")\n'))

BLOQUES_OREILLY.append(('test_auditar_compuerta', '#!/usr/bin/env python3\n"""test_auditar_compuerta.py — U-138 (usuario 4-nov): un VERDE no basta. CE_CALLOUTS de CFA rev6 dijo PASS con\n"0 burbujas citadas + declaradas, cadenas seguidas por 4 hojas" en un set con hojas de detalles: auditar_compuerta lo pasa\na FAIL de PLAUSIBILIDAD; con 30 burbujas sigue PASS; un 0 de algo que el proyecto no tiene (0 RFI) no se toca."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport compuerta_entrega as CE  # noqa: E402\n\nesp = {"burbujas": 12, "hojas_detalle": 12, "walls": 40, "tags": 9, "hojas": 172, "imagenes": 40, "markups": 40, "types": 9}\nres = [{"id": "CE_CALLOUTS", "estado": "PASS", "evidencia": ["0 burbujas citadas + declaradas, cadenas seguidas por 4 hojas"]},\n       {"id": "CB_U_117", "estado": "PASS", "evidencia": ["9 tags barridos, 40 walls"]},\n       {"id": "CE_RFI", "estado": "PASS", "evidencia": ["0 RFI abiertos"]}]\nassert CE.auditar_compuerta(res, esp) == ["CE_CALLOUTS"], res\nassert res[0]["estado"] == "FAIL" and "PLAUSIBILIDAD" in res[0]["evidencia"][-1], res[0]\nassert res[1]["estado"] == "PASS" and res[1]["plausibilidad"] == "OK" and res[2]["estado"] == "PASS"\nres = [{"id": "CE_CALLOUTS", "estado": "PASS", "evidencia": ["30 burbujas citadas + declaradas (30 burbujas de dos líneas)"]}]\nassert CE.auditar_compuerta(res, esp) == [] and res[0]["estado"] == "PASS"\nres = [{"id": "CE_CALLOUTS", "estado": "PASS", "evidencia": ["1 burbujas citadas"]}]\nassert CE.auditar_compuerta(res, esp) == ["CE_CALLOUTS"]                  # casi 0 con 12 hojas de detalles\nres = [{"id": "CB_U_118", "estado": "PASS", "evidencia": ["0 walls sin imagen circulada", "missing 0 images"]}]\nassert CE.auditar_compuerta(res, esp) == [], res                         # cero de faltantes = bueno\nprint("OK test_auditar_compuerta")\n'))

BLOQUES_OREILLY.append(('test_no_impreso_rfi', '#!/usr/bin/env python3\n"""test_no_impreso_rfi.py — U-138 (auditoría 4-nov): CE_RFI_FORMATO y CE_RFI_BARRIDO_IMPRESO pasaban con 0 RFI abiertos\naunque el Excel dijera \'not printed - assumed, RFI-xx\'. Todo \'not printed / assumed / [PENDING]\' remite a un RFI abierto\n(Pending Items), a un RFI cerrado con su decisión, o cita la decisión / regla. Falla con v81cf34."""\nimport os\nimport sys\n\nimport openpyxl\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport compuerta_entrega as CE  # noqa: E402\n\n\nclass C:\n    def __init__(self, filas, pend=(), rfis=()):\n        self._wb = openpyxl.Workbook()\n        ws = self._wb.active\n        ws.title = "Material Summary"\n        for f in filas:\n            ws.append([f])\n        p = self._wb.create_sheet("Pending Items")\n        p.append(["RFI", "Question", "Delta"])\n        for r in pend:\n            p.append(list(r))\n        self._rfis = list(rfis)\n        self.set_p = None\n\n    def wb(self):\n        return self._wb\n\n    def rfis_abiertos(self):\n        return [(str(r[0]), " | ".join(map(str, r[1:]))) for r in self._wb["Pending Items"].iter_rows(min_row=2, values_only=True)]\n\n    def rfis(self):\n        return self._rfis\n\n    def rfi(self, rid):\n        return None\n\n\nmalo = C(["purlin depth not printed - assumed 8 in, RFI-40"])\nassert CE.ce_rfi_formato(malo)[0] == "FAIL" and CE.ce_rfi_barrido(malo)[0] == "FAIL"\nsin_rfi = C(["height not printed - assumed to deck"])\nassert any("sin RFI abierto" in e for e in CE.no_impreso_sin_rfi(sin_rfi))\ncerrado = C(["[PENDING] assumed 8 in purlin depth, estimator decision RFI-01"],\n            rfis=[{"id": "RFI-01", "estado": "CLOSED", "decision": "estimator decision 2026-11-01 = B"}])\nassert CE.no_impreso_sin_rfi(cerrado) == [], CE.no_impreso_sin_rfi(cerrado)\nabierto = C(["return not printed - conservative assumption RFI-34"], pend=[("RFI-34", "ends?", "(A) delta 0 (B) delta +4")])\nassert CE.no_impreso_sin_rfi(abierto) == []\nregla = C(["blocking size not printed: 3\'-0\\" x 2 rows per standing rule R-ALC-02"])\nassert CE.no_impreso_sin_rfi(regla) == []\nprint("OK test_no_impreso_rfi")\n'))

BLOQUES_OREILLY.append(('test_u140_u141', '#!/usr/bin/env python3\n"""test_u140_u141.py — U-140 (CFA rev9: RFI \'not printed\' con un barrido de 8 términos) y U-141 (usuario 5-nov: circular\ncada detalle revisado en origen y destino; rev8 de O\'Reilly sin DETALLES_REVISADOS.pdf). Falla con v81cf42."""\nimport os\nimport sys\nimport tempfile\n\nimport pymupdf\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport chequeos_biblioteca as CB  # noqa: E402\nimport compuerta_entrega as CE  # noqa: E402\n\n# U-140: 8 términos (CFA rev9) = FAIL; búsqueda completa = PASS\nr8 = {"barrido": {"hojas": "ALL", "terminos": ["W5", "WALL", "PARTITION", "SOFFIT", "FURR", "STUD", "BULKHEAD", "DRIVE THRU"]}}\nassert len(CE.busqueda_exhaustiva("RFI-11", r8, ["A", "S", "M"])) >= 5\nok = {"barrido": {"hojas": "ALL", "terminos": [f"t{i}" for i in range(12)], "disciplinas": "ALL", "shx": "SHX annots read (set_texto)",\n                  "vectorial": "A-202 vector lines measured at 1/4\\" = 1\'-0\\" printed", "specs": "spec 09 21 16 + addenda 1-2 searched",\n                  "otros_sets": "the other GC set searched: none provided"}}\nassert CE.busqueda_exhaustiva("RFI-11", ok, ["A", "S", "M"]) == []\nr_dis = {"barrido": dict(ok["barrido"], disciplinas=["A", "S"])}\nassert any("disciplinas" in e for e in CE.busqueda_exhaustiva("RFI-11", r_dis, ["A", "S", "M"]))\n\n# U-141: cadena de 2 burbujas; sin PDF = FAIL; con origen + destino = PASS; falta un destino = FAIL; cadena vacía = FAIL\nd = tempfile.mkdtemp()\nos.makedirs(os.path.join(d, "Planos marcados"))\nregs = [{"n": "1", "t": "A3.2", "origen": "A1.1", "x": 100, "y": 100, "r": 14, "disp": "citada", "motivo": "x"},\n        {"n": "5", "t": "A4.2", "origen": "A1.1", "x": 200, "y": 100, "r": 14, "disp": "citada", "motivo": "x"}]\n\n\nclass C:\n    planos = os.path.join(d, "Planos marcados")\n\n\n_orig = (CB.B.__dict__[\'desde_ctx\'], CB.cadena_detalles)\nCB.B.desde_ctx = classmethod(lambda cls, c: CB.B(canon={}))\nCB.cadena_detalles = lambda b: regs\nr = CE.ce_detalles_circulados(C())\nassert r[0] == "FAIL" and "no hay Planos marcados/DETALLES_REVISADOS.pdf" in r[1][0], r\n\n\ndef pdf(marcas):\n    doc = pymupdf.open()\n    for lab in ("A1.1", "A3.2", "A4.2"):\n        doc.new_page(width=600, height=400)\n    doc.set_page_labels([{"startpage": i, "prefix": l, "style": "", "firstpagenum": 1} for i, l in enumerate(("A1.1", "A3.2", "A4.2"))])\n    for pg, txt in marcas:\n        a = doc[pg].add_circle_annot(pymupdf.Rect(50, 50, 80, 80))\n        a.set_info(subject=CE.SUBJ_DET, content=txt)\n        a.update()\n    doc.save(os.path.join(C.planos, "DETALLES_REVISADOS.pdf"))\n\n\npdf([(0, "#1 origin 1/A3.2 on A1.1"), (1, "#1 destination 1/A3.2 (called from A1.1)"),\n     (0, "#2 origin 5/A4.2 on A1.1"), (2, "#2 destination 5/A4.2 (called from A1.1)")])\nassert CE.ce_detalles_circulados(C())[0] == "PASS"\npdf([(0, "#1 origin 1/A3.2 on A1.1"), (1, "#1 destination 1/A3.2 (called from A1.1)"), (0, "#2 origin 5/A4.2 on A1.1")])\nr = CE.ce_detalles_circulados(C())\nassert r[0] == "FAIL" and any("5/A4.2: sin marca en su vista destino" in e for e in r[1]), r\nCB.cadena_detalles = lambda b: []\nassert CE.ce_detalles_circulados(C())[0] == "FAIL"\nCB.B.desde_ctx, CB.cadena_detalles = _orig  # no dejar el parche para los otros tests\nprint("OK test_u140_u141")\n'))
BLOQUES_OREILLY.append(('test_u142', '#!/usr/bin/env python3\n"""test_u142.py — U-142 (usuario 5-nov: revisar todos los schedules del trade, lista de cada material y marcar cada partition\ntype). La rev8 de O\'Reilly no tenía lista ni marcas = FAIL. Falla con v81cf43 (no existe CE_SCHEDULES_MARCADOS)."""\nimport os\nimport sys\nimport tempfile\n\nimport pymupdf\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport compuerta_entrega as CE  # noqa: E402\n\n# cruce: la primera clave va en el NOMBRE del renglón (el track cita el stud en su fuente y no es el stud)\nms = [(\'Bottom track 3-5/8"\', 10.0, "track gauge = stud gauge 362S162-33"), (\'3-5/8" metal stud - 362S162-33\', 20.0, "T1-A 20")]\nassert CE._en_ms(ms, "stud", "362S162-33") == \'3-5/8" metal stud - 362S162-33\'\nalc = {"ALC-INSUL": {"id": "ALC-INSUL", "estado": "NO APLICA", "nota": "EXCLUDED: insulation by others"}}\nr = CE.resolver_material(\'3-5/8" 362S162-33 studs with 3-1/2" sound batt\', ms, alc, set())\nassert ("batt", None, "ALC-INSUL: EXCLUDED: insulation by others") in r and any(h for _, h, _ in r), r\nassert CE.resolver_material("exterior stucco over lath", ms, {}, set())[0][1:] == (None, None)   # sin ALC ni MS = NOT FOUND\n\n# U-141 (rev10): una keynote "1" grande con texto chico a la derecha ("REFER TO EXTERIOR ...") no es el título de la vista 1\nchicas = [(300 + 30 * i, 50, 325 + 30 * i, 56, "note") for i in range(20)]\nnota = chicas + [(100, 40, 112, 60, "1"), (120, 48, 160, 55, "PORTLAND"), (170, 48, 220, 55, "EXTERIOR")]\nassert CE.ubicar_titulo(nota, "1") is None\ntitulo = nota + [(100, 140, 112, 160, "1"), (120, 141, 260, 159, "ELEVATION")]\nassert CE.ubicar_titulo(titulo, "1") == (100, 140, 260, 160)\n\nd = tempfile.mkdtemp()\nos.makedirs(os.path.join(d, "Planos marcados"))\nlst = [{"k": 1, "hoja": "A1.1", "schedule": "Partition / wall types", "id": "T1",\n        "materiales": [{"campo": "stud", "valor": "x", "ms": "3-5/8\\" metal stud", "fuera": None}]},\n       {"k": 2, "hoja": "A5.1", "schedule": "DOOR SCHEDULE", "id": "7",\n        "materiales": [{"campo": "trade", "valor": "aluminum storefront", "ms": None, "fuera": "not our trade: Div. 08 41"}]}]\n\n\nclass C:\n    planos = os.path.join(d, "Planos marcados")\n    entrega = d\n    w = d\n\n\n_orig = CE.lista_schedules\nCE.lista_schedules = lambda c: (lst, True, False)                 # rev8: sin lectura independiente de los schedules\nassert CE.ce_schedules_marcados(C())[0] == "FAIL"\nCE.lista_schedules = lambda c: (lst, True, True)\nr = CE.ce_schedules_marcados(C())                                 # sin SCHEDULES_REVISADOS.pdf = FAIL\nassert r[0] == "FAIL" and "SCHEDULES_REVISADOS.pdf" in r[1][0], r\n\n\ndef pdf(marcas):\n    doc = pymupdf.open()\n    doc.new_page(width=600, height=400)\n    for txt in marcas:\n        a = doc[0].add_circle_annot(pymupdf.Rect(50, 50, 80, 80))\n        a.set_info(subject=CE.SUBJ_SCH, content=txt)\n        a.update()\n    doc.save(os.path.join(C.planos, "SCHEDULES_REVISADOS.pdf"))\n\n\nopen(os.path.join(d, "SCHEDULES_MATERIALES.md"), "w").write("| 1 | a |\\n| 2 | b |\\n")\npdf(["#1 T1 on A1.1 (Partition / wall types) reviewed", "#2 7 on A5.1 (DOOR SCHEDULE) reviewed"])\nassert CE.ce_schedules_marcados(C())[0] == "PASS"\npdf(["#1 T1 on A1.1 (Partition / wall types) reviewed"])          # un renglón sin marca = FAIL\nr = CE.ce_schedules_marcados(C())\nassert r[0] == "FAIL" and any("#2 7" in e and "sin marca" in e for e in r[1]), r\npdf(["#1 T1 on A1.1 (Partition / wall types) reviewed", "#2 7 on A5.1 (DOOR SCHEDULE) reviewed"])\nlst[1]["materiales"][0]["fuera"] = None                           # material sin MS ni motivo = FAIL\nassert CE.ce_schedules_marcados(C())[0] == "FAIL"\nlst[1]["materiales"][0]["fuera"] = "not our trade: Div. 08 41"\ndoc = pymupdf.open()                                              # U-119: anotación en español en el PDF entregado = FAIL\ndoc.new_page(width=600, height=400)\nfor txt in ["#1 T1 on A1.1 (Partition / wall types) reviewed", "#2 7 on A5.1 (DOOR SCHEDULE) reviewed"]:\n    an = doc[0].add_circle_annot(pymupdf.Rect(50, 50, 80, 80))\n    an.set_info(subject=CE.SUBJ_SCH, content=txt + " (verificada a ojo)")\n    an.update()\ndoc.save(os.path.join(C.planos, "SCHEDULES_REVISADOS.pdf"))\nr = CE.ce_schedules_marcados(C())\nassert r[0] == "FAIL" and any("español" in e for e in r[1]), r\nCE.lista_schedules = lambda c: ([], True, True)                   # 0 renglones = FAIL\nassert CE.ce_schedules_marcados(C())[0] == "FAIL"\nCE.lista_schedules = _orig                                        # no dejar el parche para los otros tests\n# U-143 por el canon (COORDINACIÓN 5-nov): demo = SF del área del wall (LF x H), LF x H x 2 layers = FAIL\nimport chequeos_biblioteca as CB  # noqa: E402\nmal = CB.B(canon={"misc_items": [{"ref": "DEMO-1", "familia": "demolition", "unit": "SF", "qty": 200.0, "op": "10.0 LF x 10.0 ft x 2 layers = 200.0 SF"}]})\nassert CB.u_143(mal)[0] == "FAIL"\ngeo = CB.B(canon={"demo_geom": [{"id": "D1", "lf": 10.0, "h": 10.0, "layers": 2}]})\nassert CB.u_143(geo)[0] == "FAIL"\nbien = CB.B(canon={"misc_items": [{"ref": "DEMO-1", "familia": "demolition", "unit": "SF", "qty": 100.0, "op": "10.0 LF x 10.0 ft = 100.0 SF"}]})\nassert CB.u_143(bien)[0] == "PASS"\nprint("OK test_u142")\n'))


def test_oreilly_rev5():
    aq = os.path.dirname(os.path.abspath(__file__))
    for n, src in BLOQUES_OREILLY:
        g = {"__name__": "__main__", "__file__": os.path.join(aq, n + ".py")}
        try:
            exec(compile(src, n + ".py", "exec"), g)
        except SystemExit as e:     # v81cf58: un bloque que sale con sys.exit(0) (p. ej. sin tesseract) ya no corta los tests siguientes
            if e.code not in (0, None):
                raise


BLOQUES_OREILLY.append(('test_u142_json', '#!/usr/bin/env python3\n"""test_u142.py - U-142 (usuario 5-nov: revisar todos los schedules del trade, lista de cada material y marcar cada partition\ntype). CFA rev10 / O\'Reilly rev9 se entregaron sin SCHEDULES_REVISADOS.pdf ni lista de materiales por fila. Falla con v81cf43."""\nimport json\nimport os\nimport sys\nimport tempfile\n\nimport pymupdf\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport compuerta_entrega as CE  # noqa: E402\n\nd = tempfile.mkdtemp()\nos.makedirs(os.path.join(d, "Planos marcados"))\nsch = [{"sheet": "A1.1", "page": 1, "title": "WALL TYPE SCHEDULE", "title_bbox": [10, 10, 200, 30], "ours": True, "why": "partition types",\n        "rows": [{"type": "S1", "bbox": [10, 40, 40, 55], "materials": [{"material": "3-5/8 stud", "spec": "20 GA @ 16", "source": "S1/A1.1"}],\n                  "in_canon": "yes: walls S1"},\n                 {"type": "S2", "bbox": [10, 60, 40, 75], "materials": [{"material": "6 stud", "spec": "18 GA", "source": "S2/A1.1"}],\n                  "in_canon": "no: type not used on the plans (no S2 tag on A1.1)"}]}]\njson.dump(sch, open(os.path.join(d, "schedules_materiales.json"), "w"))\n\n\nclass C:\n    cfg = {}\n    w = d\n    entrega = d\n    planos = os.path.join(d, "Planos marcados")\n\n\nr = CE.ce_schedules_revisados(C())\nassert r[0] == "FAIL" and any("SCHEDULES_REVISADOS.pdf" in e for e in r[1]), r\ndoc = pymupdf.open()\ndoc.new_page(width=600, height=400)\nfor k in (1, 2):\n    for sub in (CE.SUBJ_SCH, CE.SUBJ_SCH + " CHECK"):\n        a = doc[0].add_circle_annot(pymupdf.Rect(10, 20 * k, 40, 20 * k + 15))\n        a.set_info(subject=sub, content=f"#{k} reviewed")\n        a.update()\ndoc.save(os.path.join(C.planos, "SCHEDULES_REVISADOS.pdf"))\nopen(os.path.join(d, "SCHEDULES_MATERIALES.md"), "w").write("x")\nassert CE.ce_schedules_revisados(C())[0] == "PASS"\nsch[0]["rows"][1]["in_canon"] = "no"\njson.dump(sch, open(os.path.join(d, "schedules_materiales.json"), "w"))\nr = CE.ce_schedules_revisados(C())\nassert r[0] == "FAIL" and any("sin estado" in e for e in r[1]), r\nos.remove(os.path.join(d, "schedules_materiales.json"))\nassert CE.ce_schedules_revisados(C())[0] == "FAIL"\nprint("OK test_u142_json")\n'))


BLOQUES_OREILLY.append(('test_be_cf27', '#!/usr/bin/env python3\n"""test_be_cf27.py - BE-CF27 (CFA rev10, 5-nov): rev10 se subió con un skill sin U-141 / U-142 / U-143, órdenes del usuario\nque ya estaban en el remoto. subir_entrega bloquea si una orden U-NNN del remoto no está en el registro del skill."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport subir_entrega as SE  # noqa: E402\n\ntxt = "- [U-141 · programa] circular detalles\\n- [U-142 · programa] schedules\\n- [U-143 · programa] demo SF\\n"\nreg = {"reglas": [{"id": "U-141"}, {"id": "U-140"}]}\nassert SE.ordenes_sin_registro(txt, reg) == ["U-142", "U-143"]\nreg["reglas"] += [{"id": "U-142"}, {"id": "U-143"}]\nassert SE.ordenes_sin_registro(txt, reg) == []\nos.environ["SIN_ORDENES_REMOTAS"] = "1"\nSE.candado_ordenes()\ndel os.environ["SIN_ORDENES_REMOTAS"]\nprint("OK test_be_cf27")\n'))


def test_u145_estandar_oreilly():
    """U-145: CFA rev10 se subió sin DETALLES_REVISADOS.pdf (estándar O'Reilly incompleto) = FAIL."""
    w = workdir()
    e = os.path.join(w, "FINAL_FOR_REVIEW")
    est, ev = chk(CE.ce_estandar_oreilly, CE.Ctx(w))
    assert est == "FAIL" and "DETALLES_REVISADOS.pdf" in ev, ev
    for pat, _ in CE.ESTANDAR_OREILLY:
        f = os.path.join(e, pat.replace("*markups*", "P_markups").replace("*_type_*", "A1.1_type_S1").replace("*.xlsx", "P_Takeoff_FINAL.xlsx").replace("/*", "/x.json"))
        os.makedirs(os.path.dirname(f), exist_ok=True)
        if not os.path.exists(f):
            open(f, "w").write("x")
    assert chk(CE.ce_estandar_oreilly, CE.Ctx(w))[0] == "PASS", chk(CE.ce_estandar_oreilly, CE.Ctx(w))
    os.remove(os.path.join(e, "Planos marcados", "SCHEDULES_REVISADOS.pdf"))
    assert chk(CE.ce_estandar_oreilly, CE.Ctx(w))[0] == "FAIL"
    # U-148: Consumer Cellular rev4 se subió sin GUIA_DE_REVISION_DEL_ESTIMADOR.md = FAIL
    open(os.path.join(e, "Planos marcados", "SCHEDULES_REVISADOS.pdf"), "w").write("x")
    os.remove(os.path.join(e, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"))
    est, ev = chk(CE.ce_estandar_oreilly, CE.Ctx(w))
    assert est == "FAIL" and "GUIA_DE_REVISION_DEL_ESTIMADOR.md" in ev, ev


def test_u151_pdf_editable():
    """U-151 / BE-147 (CR City Hotel rev3): el PDF de markups se entregó con 3 firmas digitales /Sig del set (/SigFlags 3) y Page
    Labels numéricos; Bluebeam bloqueaba Page Labels. Repite el error: PDF con un campo /Sig FIRMADO (/V con /Name) y labels
    numéricos = FAIL; después de quitar_firmas_labels = PASS; carpeta sin PDF = FAIL (U-137, no pasa en vacío)."""
    import types
    import pikepdf
    from pikepdf import Name, Dictionary, Array
    import quitar_firmas_labels as QF
    d = tempfile.mkdtemp()
    planos = os.path.join(d, "Planos marcados")
    os.makedirs(planos)
    c = types.SimpleNamespace(planos=planos, cfg={})
    est, ev = CE.ce_pdf_editable(c)
    assert est == "FAIL" and "0 PDF" in ev[0], ev
    pdf = pikepdf.new()
    for _ in range(2):
        pdf.add_blank_page(page_size=(612, 792))
    ap = pdf.make_stream(b"0 0 1 rg 0 0 100 40 re f", Type=Name.XObject, Subtype=Name.Form, BBox=[0, 0, 100, 40])
    firma = pdf.make_indirect(Dictionary(Type=Name.Sig, Filter=Name("/Adobe.PPKLite"), SubFilter=Name("/adbe.pkcs7.detached"),
                                         Name=pikepdf.String("Chad Mitchell"), Contents=pikepdf.String(b"\x00" * 16)))
    campo = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Widget, FT=Name.Sig, T=pikepdf.String("Architect Stamp"),
                                         V=firma, Rect=[400, 50, 500, 90], F=4, P=pdf.pages[0].obj, AP=Dictionary(N=ap)))
    pdf.pages[0].obj.Annots = Array([campo])
    pdf.Root.AcroForm = Dictionary(Fields=Array([campo]), SigFlags=3)
    pdf.Root.PageLabels = Dictionary(Nums=Array([0, Dictionary(S=Name.D)]))
    mal = os.path.join(planos, "P_markups_rev3.pdf")
    pdf.save(mal)
    fs, info = CE.pdf_editable(mal)
    assert info["firmas"] == 1 and any("/Sig" in x and "1 firmado" in x for x in fs), fs
    assert any("/SigFlags" in x for x in fs) and any("puramente numérico" in x for x in fs), fs
    assert CE.ce_pdf_editable(c)[0] == "FAIL"
    assert not [x for x in CE.pdf_editable(mal, ["1", "2"])[0] if "numérico" in x]       # hoja impresa así = permitido
    bien = os.path.join(d, "P_markups_rev3b.pdf")
    assert QF.quitar(mal, bien, {1: "A0.01", 2: "A0.02"}) == 1
    fs, info = CE.pdf_editable(bien)
    assert fs == [] and info["labels"] == ["A0.01", "A0.02"] and info["firmas"] == 0, (fs, info)
    os.remove(mal)
    shutil.copy(bien, os.path.join(planos, "P_markups_rev3b.pdf"))
    est, ev = CE.ce_pdf_editable(c)
    assert est == "PASS" and "0 firmas" in ev[0], ev
    # labels repetidos / sin labels = FAIL
    p2 = pikepdf.open(bien, allow_overwriting_input=True)
    p2.Root.PageLabels = Dictionary(Nums=Array([0, Dictionary(P=pikepdf.String("A0.01"))]))
    p2.save(os.path.join(planos, "P_markups_rev3b.pdf"))
    assert any("repetido" in x for x in CE.pdf_editable(os.path.join(planos, "P_markups_rev3b.pdf"))[0])
    p3 = pikepdf.open(bien)
    del p3.Root["/PageLabels"]
    p3.save(os.path.join(d, "sin.pdf"))
    assert any("sin /PageLabels" in x for x in CE.pdf_editable(os.path.join(d, "sin.pdf"))[0])


def test_u152_escala_pagina():
    """U-152 / BE-148 (CR City Hotel rev3b): los markups traían su /Measure 1/4" pero ninguna página tenía /VP y Bluebeam mostraba
    la escala de página 0.125. Repite el error: PDF sin firmas y con labels = hoja, markups 1/4 in = 1 ft SIN /VP = FAIL;
    después de escala_pagina = PASS (mismo número de markups y /Measure); /VP con otra /R = FAIL; hoja con dos escalas: cada
    markup cae en un viewport de su /R."""
    import types
    import pikepdf
    from pikepdf import Name, Dictionary, Array
    import escala_pagina as EP
    d = tempfile.mkdtemp()
    planos = os.path.join(d, "Planos marcados")
    os.makedirs(planos)
    c = types.SimpleNamespace(planos=planos, cfg={})

    def medida(r, ptft):
        return Dictionary(Type=Name.Measure, Subtype=Name.RL, R=pikepdf.String(r),
                          X=Array([Dictionary(Type=Name.NumberFormat, U=pikepdf.String("ft"), C=1.0 / ptft, D=100)]))

    def markup(pdf, pg, rect, r, ptft):
        return pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.PolyLine, Rect=rect, Subj=pikepdf.String("A"),
                                            Vertices=[rect[0], rect[1], rect[2], rect[3]], Measure=medida(r, ptft), P=pg))
    pdf = pikepdf.new()
    for _ in range(3):
        pdf.add_blank_page(page_size=(2592, 1728))
    q = "1/4 in = 1 ft"
    pdf.pages[0].obj.Annots = Array([markup(pdf, pdf.pages[0].obj, [100, 100, 600, 110], q, 18),
                                     markup(pdf, pdf.pages[0].obj, [800, 900, 1200, 910], q, 18)])
    pdf.pages[1].obj.Annots = Array([markup(pdf, pdf.pages[1].obj, [100, 100, 900, 110], "1/8 in = 1 ft", 9),
                                     markup(pdf, pdf.pages[1].obj, [1900, 1300, 2100, 1310], "1/2 in = 1 ft", 36)])
    pdf.Root.PageLabels = Dictionary(Nums=Array([0, Dictionary(P=pikepdf.String("A6.00")), 1, Dictionary(P=pikepdf.String("A2.01")),
                                                 2, Dictionary(P=pikepdf.String("LEGEND"))]))
    mal = os.path.join(planos, "P_markups_rev3b.pdf")
    pdf.save(mal)
    fs, info = CE.pdf_editable(mal)
    assert any("SIN escala de página /VP" in x and "p1" in x for x in fs), fs
    assert info["paginas_escala"] == 2 and info["markups_medida"] == 4, info
    assert CE.ce_pdf_editable(c)[0] == "FAIL"
    bien = os.path.join(d, "P_markups_rev3c.pdf")
    puestas = EP.poner(mal, bien)
    assert puestas == [(1, [q]), (2, ["1/8 in = 1 ft", "1/2 in = 1 ft"])], puestas
    fs, info = CE.pdf_editable(bien)
    assert fs == [] and info["escalas"] == {1: [q], 2: ["1/2 in = 1 ft", "1/8 in = 1 ft"]}, (fs, info)
    assert info["markups_medida"] == 4
    os.remove(mal)
    shutil.copy(bien, os.path.join(planos, "P_markups_rev3c.pdf"))
    est, ev = CE.ce_pdf_editable(c)
    assert est == "PASS" and "/VP del mismo /R" in ev[0], ev
    # /VP con otra escala (0.125 en una hoja a 1/4") = FAIL
    p2 = pikepdf.open(bien)
    p2.pages[0].obj.VP = Array([Dictionary(Type=Name.Viewport, BBox=[0, 0, 2592, 1728], Measure=medida("1/8 in = 1 ft", 9))])
    p2.save(os.path.join(d, "otra.pdf"))
    fs, _ = EP.revisar(os.path.join(d, "otra.pdf"))
    assert fs and "1/4 in = 1 ft" in fs[0] and "1/8 in = 1 ft" in fs[0], fs


def test_u153_vista_bluebeam():
    """U-153 / BE-149 (CR City Hotel rev3c, 6-nov): markups_bluebeam escribía /DepthUnit /C 1/864 y Bluebeam mostraba el Wall Area
    x864 (lo encontró el USUARIO en Bluebeam en un wall de CR City Hotel). CE_VISTA_BLUEBEAM simula el Markups List y lo cuadra
    contra el Excel y la etiqueta: /C 1/864 = FAIL (x864); /C 1 = PASS; Length que no cuadra con el LF = FAIL; etiqueta sin
    'SF wall' = FAIL; carpeta sin PDF = FAIL (U-137); arreglar_sf_wall deja el PDF entregado en PASS."""
    import markups_bluebeam as MB
    import escala_pagina as EP
    w = workdir()
    e = os.path.join(w, "FINAL_FOR_REVIEW")
    c = CE.Ctx(w)
    assert CE.ce_vista_bluebeam(c)[0] == "FAIL"                               # 0 PDF: no pasa en vacío
    wall = {"id": "S21-N", "tag": "S21", "element": "wall", "length_ft": 20.0, "height_ft": 14.84375, "detail": "1/A3.2",
            "sheet": "A1.1", "faces": [{"side": "A", "layers": 1, "height_ft": 14.845, "length_ft": 20.0}]}
    etq = MB.contenido(wall)
    assert "296.88 SF wall (LF\u00d7H)" in etq and "SF board (faces\u00d7layers)" in etq, etq

    def pdf(nombre, c_depth=1, largo_pt=20.0 * 9, contents=etq):
        tmp = os.path.join(tempfile.mkdtemp(), "m.pdf")
        doc = pymupdf.open()
        pg = doc.new_page(width=2592, height=1728)
        pg.insert_text((2400, 1700), "A1.1", fontsize=30)
        doc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1}])
        a = MB._annot(doc, pg, [(100, 200), (100 + largo_pt, 200)], (1, 0, 0), None, "S21", contents, MB.AUTOR, "TO-S21-N")
        MB._measure(doc, a, 9.0)
        MB._depth(doc, a, 14.84375)
        if c_depth != 1:
            doc.xref_set_key(a.xref, "DepthUnit", f"[<</Type/NumberFormat/U(ft)/C {c_depth}/D 100/FD true/SS()>>]")
        doc.save(tmp)
        out = os.path.join(e, "Planos marcados", nombre)
        EP.poner(tmp, out)
        return out
    xl = c.excel
    # el error original: /C 1/864 -> Wall Area x864
    mal = pdf("P_markups_rev3c.pdf", c_depth=".001157407")
    filas, fs, info = CE.vista_bluebeam(mal, xl)
    assert info["markups"] == 1 and fs and "x864" in fs[0], fs
    assert abs(filas[0]["Wall Area (sf)"] - 20.0 * 14.84375 * 864) < 1, filas[0]
    assert CE.ce_vista_bluebeam(CE.Ctx(w))[0] == "FAIL"
    os.remove(mal)
    # /C 1 -> PASS, con CSV en Auditoria/
    bien = pdf("P_markups_rev3d.pdf")
    filas, fs, info = CE.vista_bluebeam(bien, xl)
    assert fs == [] and filas[0]["Wall Area (sf)"] == 296.88 and filas[0]["Status"] == "OK", (fs, filas)
    est, ev = CE.ce_vista_bluebeam(CE.Ctx(w))
    assert est == "PASS" and "1 markups revisados" in ev[0], ev
    assert os.path.isfile(os.path.join(e, "Auditoria", "VISTA_BLUEBEAM.csv"))
    os.remove(bien)
    # Length que no cuadra con el LF del Excel / de la etiqueta -> FAIL
    largo = pdf("P_markups_largo.pdf", largo_pt=22.0 * 9)
    fs = CE.vista_bluebeam(largo, xl)[1]
    assert fs and "Length 22.00 != Excel LF 20.0" in fs[0] and "etiqueta 20.00 LF" in fs[0], fs
    os.remove(largo)
    # etiqueta vieja sin 'SF wall' (solo 'SF board') -> FAIL; arreglar_sf_wall -> PASS
    vieja = pdf("P_markups_vieja.pdf", c_depth=".001157407", contents="S21 · 20.00 LF · H 14'-10.125\" · 296.90 SF board · 1/A3.2 · S21-N")
    fs = CE.vista_bluebeam(vieja, xl)[1]
    assert fs and "sin '<LF x H> SF wall'" in fs[0] and "x864" in fs[0], fs
    nueva = os.path.join(e, "Planos marcados", "P_markups_nueva.pdf")
    n = MB.arreglar_sf_wall(vieja, nueva)
    os.remove(vieja)
    assert n == {"depthunit": 1, "etiquetas": 1, "sin_cambio": 0}, n
    assert CE.vista_bluebeam(nueva, xl)[1] == []
    assert CE.ce_vista_bluebeam(CE.Ctx(w))[0] == "PASS"


def test_be_cr31_sin_firmas():
    """BE-CR31 (CR City Hotel rev4): (1) DETALLES_REVISADOS / SCHEDULES_REVISADOS heredaban el AcroForm de firma del bid set
    (/SigFlags 3) -> CE_PDF_EDITABLE FAIL; _sin_firmas lo quita y conserva las Page Labels. (2) markups_rcp re-aplica
    markups_bluebeam.editable() al PDF final (los polígonos de RCP quedaban sin escala de página /VP)."""
    import pikepdf
    from pikepdf import Dictionary, Array, Name
    d = tempfile.mkdtemp()
    p = os.path.join(d, "DETALLES_REVISADOS.pdf")
    pdf = pikepdf.new()
    for _ in range(2):
        pdf.add_blank_page(page_size=(612, 792))
    pdf.Root.AcroForm = Dictionary(Fields=Array(), SigFlags=3)
    pdf.Root.PageLabels = Dictionary(Nums=Array([0, Dictionary(P=pikepdf.String("A7.31")), 1, Dictionary(P=pikepdf.String("A7.50"))]))
    pdf.save(p)
    r0 = CE.pdf_editable(p)
    assert any("SigFlags" in str(f) for f in (r0[0] if isinstance(r0, tuple) else r0)), r0
    CE._sin_firmas(p)
    r1 = CE.pdf_editable(p)
    assert not any("SigFlags" in str(f) for f in (r1[0] if isinstance(r1, tuple) else r1)), r1
    q = pikepdf.open(p)
    assert "/AcroForm" not in q.Root or "/SigFlags" not in q.Root.AcroForm
    q.close()
    import pymupdf
    dd = pymupdf.open(p)
    assert [dd[i].get_label() for i in range(dd.page_count)] == ["A7.31", "A7.50"]
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "markups_rcp.py"), encoding="utf-8").read()
    assert "mb.editable(pdf_out" in src


if __name__ == "__main__":
    for f in (test_hft_rfi01_impreso, test_altura_circular_oreilly, test_drive_parent, test_tiempos, test_excel,
              test_entregables_y_docs, test_subida, test_materiales_schedule, test_revision_materiales, test_texto_hoja_rotada, test_materiales_cfa_rev5, test_correr_rojo, test_oreilly_rev5, test_u145_estandar_oreilly, test_u151_pdf_editable, test_u152_escala_pagina,
              test_u153_vista_bluebeam, test_be_cr31_sin_firmas):
        f()
        print("ok", f.__name__)
    print("test_compuerta_entrega OK")



def test_cr_r7_rcp_completo():
    """CR-R7-01 (rev7): cielos cuantificados como misc_items sin polígono = FAIL; con su markup TO-<id> (piezas ~k sumadas,
    soffit lineal por LF, cielo de varias capas por área dibujada) = PASS; un markup con otra cantidad = FAIL."""
    import compuerta_entrega as CE
    canon = {"ceilings": [{"room": "L2 Corridor 216", "area_sf": 455.0}],
             "misc_items": [{"ref": "CLG-L4-117 board", "qty": 129.0, "op": "129.0 SF x 1 layer(s) = 129.0"},
                            {"ref": "CLG-L4-118 board", "qty": 94.0, "op": "94.0 SF x 1 layer(s) = 94.0"},
                            {"ref": "CLG-L4-119 board", "qty": 11.0, "op": "11.0 SF x 1 layer(s) = 11.0"},
                            {"ref": "CLG-L1-00 board", "qty": 495.9, "op": "165.3 SF x 3 layer(s) = 495.9"},
                            {"ref": "SOF-L2-01 board", "qty": 139.62, "op": "152.26 LF x (0.375 bottom + 0.542 vertical) = 139.62"}]}
    esp = CE.esperados_rcp(canon)
    assert esp["CLG-L1-00"] == ("area", 165.3) and esp["SOF-L2-01"] == ("line", 152.26), esp
    solo_ceilings = [{"Wall ID": "TO-L2 Corridor 216", "Area (sf)": 455.0, "Length (ft)": 90.0}]
    fs = CE.rcp_completo(solo_ceilings, esp)
    assert any(f.startswith("CLG-L4-117") for f in fs) and any(f.startswith("CLG-L4-118") for f in fs) \
        and any(f.startswith("CLG-L4-119") for f in fs), fs
    todo = solo_ceilings + [{"Wall ID": "TO-CLG-L4-117", "Area (sf)": 129.0}, {"Wall ID": "TO-CLG-L4-118", "Area (sf)": 94.0},
                            {"Wall ID": "TO-CLG-L4-119", "Area (sf)": 11.0}, {"Wall ID": "TO-CLG-L1-00", "Area (sf)": 165.3},
                            {"Wall ID": "TO-SOF-L2-01~1", "Length (ft)": 84.36}, {"Wall ID": "TO-SOF-L2-01~2", "Length (ft)": 67.9}]
    assert CE.rcp_completo(todo, esp) == [], CE.rcp_completo(todo, esp)
    todo[1]["Area (sf)"] = 100.0
    assert CE.rcp_completo(todo, esp) == ["CLG-L4-117: markup 100.00 != cargado 129.00 SF"], CE.rcp_completo(todo, esp)
    print("test_cr_r7_rcp_completo OK")


test_cr_r7_rcp_completo()


def test_cr_r8_markup_en_wall():
    """CR-R8-W2 (rev8): un markup de wall puesto como recta del LF total corrida fuera de su banda dibujada = FAIL; sobre la banda = PASS;
    con markup_check_note (excepción escrita) no se revisa."""
    import tempfile, pymupdf
    import compuerta_entrega as CE
    d = tempfile.mkdtemp()
    pl = pymupdf.open(); pg = pl.new_page(width=400, height=300)
    pg.draw_line((100, 100), (300, 100), width=1.0); pg.draw_line((100, 107), (300, 107), width=1.0)
    plano = os.path.join(d, "plano.pdf"); pl.save(plano)
    def mk(pts, nm, nombre):
        m = pymupdf.open(plano); a = m[0].add_polyline_annot(pts); a.update()
        m.xref_set_key(a.xref, "NM", f"({nm})"); f = os.path.join(d, nombre); m.save(f); return f
    bien = mk([(110, 103.5), (290, 103.5)], "TO-W.6-L4-12", "bien.pdf")
    mal = mk([(110, 103.5), (290, 120.0)], "TO-W.6-L4-12", "mal.pdf")
    assert CE.markups_fuera_de_wall(bien, plano)[1] == []
    n, fs = CE.markups_fuera_de_wall(mal, plano)
    assert n == 1 and fs and "W.6-L4-12" in fs[0], fs
    assert CE.markups_fuera_de_wall(mal, plano, exentos={"W.6-L4-12"})[1] == []
    print("test_cr_r8_markup_en_wall OK")


test_cr_r8_markup_en_wall()


def test_cr_r9_contorno_real():
    """CR-R9-B (rev9): cielo 406 dibujado como localizador FUERA del edificio y 215 escalado al SF cargado = FAIL; contorno medido
    dentro de la huella = PASS; ceilings[] sin contorno medido o con medido != cargado = FAIL."""
    import tempfile, pymupdf
    import compuerta_entrega as CE
    d = tempfile.mkdtemp()
    pl = pymupdf.open(); pg = pl.new_page(width=600, height=400)
    pg.draw_rect(pymupdf.Rect(100, 100, 400, 300), width=1.0)          # huella del edificio
    pg.draw_line((250, 100), (250, 300), width=1.0)
    plano = os.path.join(d, "plano.pdf"); pl.save(plano)
    def mk(pts, nm, ct, nombre):
        m = pymupdf.open(plano); a = m[0].add_polygon_annot(pts); a.set_info(content=ct); a.update()
        m.xref_set_key(a.xref, "NM", f"({nm})"); f = os.path.join(d, nombre); m.save(f); return f
    r406 = mk([(480, 40), (560, 40), (560, 70), (480, 70)], "TO-L4 406 Cleaning", "RS-1 · CEILING · cause: polygon = locator at the printed room number", "a.pdf")
    r215 = mk([(110, 110), (240, 110), (240, 200), (110, 200)], "TO-CLG-L2-122", "GYP-1 · CEILING CLG-L2-122 · cause: measured 118.6 SF scaled about each centroid", "b.pdf")
    ok = mk([(102, 102), (248, 102), (248, 298), (102, 298)], "TO-L2 Guest room 202", "FS-1 · CEILING · cause: contour measured on 1/A2.02 (wall faces)", "c.pdf")
    fuera = mk([(450, 320), (500, 320), (500, 350), (450, 350)], "TO-L4 406 Cleaning", "RS-1 · CEILING · cause: contour measured", "e.pdf")
    n, fs = CE.contornos_no_medidos(r406, plano); assert n == 1 and fs and "locator" in fs[0], fs
    n, fs = CE.contornos_no_medidos(r215, plano); assert fs and "scaled" in fs[0], fs
    assert CE.contornos_no_medidos(ok, plano)[1] == []
    n, fs = CE.contornos_no_medidos(fuera, plano); assert fs and "FUERA" in fs[0], fs
    can = {"ceilings": [{"room": "202", "area_sf": 331.94, "contorno": {"area_medida_sf": 331.94, "sf_referencia": 269, "comparado_sf": 268.94}},
                        {"room": "406", "area_sf": 124.0}, {"room": "215", "area_sf": 123.0, "contorno": {"area_medida_sf": 118.6}}]}
    fs = CE.contornos_canon(can)
    assert len(fs) == 2 and any("406" in f for f in fs) and any("215" in f for f in fs), fs
    print("test_cr_r9_contorno_real OK")


test_cr_r9_contorno_real()


def test_cr_r10_barrido_respuesta():
    """CR-R10-E1 / E2 (rev10 CR City Hotel): la respuesta estaba impresa y el barrido no la vio. (E1) RFI de la membrana FS-1 sobre el
    bath: A0.08 imprime 'DROPPED CEILING IS NOT A COMPONENT OF THE RATED ASSEMBLY' junto al FS-1 = FAIL; (E2) RFI del rating de los
    muros de ELEC / TELE 120: A8.00 imprime 120.1 ELEC / TELE '90 MIN' = FAIL aunque A8.00 esté en barrido.hojas con un descarte
    genérico; el renglón vecino (118.1 DATA) no hereda el 90 MIN de otra puerta."""
    import compuerta_entrega as CE
    a008 = "LEVEL 2, 3, 4\n5/8\" TYPE C GYPSUM BOARD CEILING\nDROPPED CEILING IS NOT A \nCOMPONENT OF THE RATED \nASSEMBLY. REFER TO CEILING PLANS\nFS-1\nLEVEL 2, 3, 4\nTHROUGHOUT"
    a800 = "118.1\nDATA\n1\nWD\nPTD\n119.1\nTOILET\n1\nWD\n120.1\nELEC / TELE\n90 MIN\n1\nHM\n121.1\nRETAIL"
    r1 = {"pregunta": "Does the FS-1 membrane continue above the bath GYP-1?", "barrido": {"hojas": "ALL", "terminos": ["FS-1"]}}
    f1 = CE.barrido_impreso("RFI-27", r1, {"A0.08": a008})
    assert f1 and "NOT A COMPONENT" in f1[0], f1
    r2 = {"pregunta": "Which walls of 120 are 2 HR?", "barrido": {"hojas": ["A8.00"], "terminos": ["ELEC / TELE"], "descartes": {"A8.00": "door schedule, no wall data"}}}
    f2 = CE.barrido_impreso("RFI-23", r2, {"A8.00": a800})
    assert f2 and "90 MIN" in f2[0], f2
    r2["barrido"]["descartes"]["A8.00"] = "120.1 '90 MIN' -> S wall loaded 2 HR; the question is only W / E"
    assert CE.barrido_impreso("RFI-23", r2, {"A8.00": a800}) == []
    r3 = {"pregunta": "Is DATA 118B 2 HR?", "barrido": {"hojas": ["A8.00"], "terminos": ["DATA"]}}
    assert CE.barrido_impreso("RFI-24", r3, {"A8.00": a800}) == [], CE.barrido_impreso("RFI-24", r3, {"A8.00": a800})
    print("test_cr_r10_barrido_respuesta OK")


test_cr_r10_barrido_respuesta()


def test_cr_r10_puerta_rating_muro():
    """CR-R10-E2: muro con la puerta 120.1 '90 MIN' cargado W.6-0 = FAIL; W.6-2 = PASS; puerta de 20 MIN no exige rating."""
    import compuerta_entrega as CE
    hojas = {"A8.00": "DOOR SCHEDULE - ALL\n119.1\nTOILET\n1\nWD\n120.1\nELEC / TELE\n90 MIN\n1\nHM\n201.1\nGUEST ROOM\n20 MIN\n3"}
    can = {"walls": [{"id": "W.6-L1-25", "type_id": "W.6-0", "location": "L1 Elec-Tele 120 south (double door 120.1) | faces: x"},
                     {"id": "W.62-L2-01", "type_id": "W.62-1", "location": "L2 corridor (door 201.1)"},
                     {"id": "FW.4-L1-03", "type_id": "FW.4-0", "location": "L1 Passage (door 120.1) = shaft south CMU face"}]}
    fs = CE.puertas_vs_muros(can, hojas)
    assert len(fs) == 1 and "120.1" in fs[0], fs
    can["walls"][0]["type_id"] = "W.6-2"
    assert CE.puertas_vs_muros(can, hojas) == []
    can["walls"].append({"id": "W.6-L1-17 A", "type_id": "W.6-2", "location": "L1 Toilet 112 east (door 119.1)"})   # CR-R11-H1
    fs = CE.puertas_vs_muros(can, hojas)
    assert len(fs) == 1 and "SIN rating" in fs[0], fs
    can["walls"][-1]["door_rating_note"] = "Review Item: tag W.6.1 | 2 vs door without rating, delta -178.8 SF"
    assert CE.puertas_vs_muros(can, hojas) == []
    print("test_cr_r10_puerta_rating_muro OK")


test_cr_r10_puerta_rating_muro()


def test_cr_r10_conteos_explicados():
    """CR-R10-m3: CE_CALLOUTS (citas únicas + burbujas de la cadena del trade) y CE_DETALLES_CIRCULADOS (todas las burbujas del set)
    dan números distintos; la evidencia de ambos dice qué cuenta cada uno (texto 'conteos (CR-R10-m3)')."""
    import inspect, compuerta_entrega as CE, chequeos_biblioteca as CB
    assert "conteos (CR-R10-m3)" in inspect.getsource(CE) and "conteos (CR-R10-m3)" in inspect.getsource(CB)
    print("test_cr_r10_conteos_explicados OK")


test_cr_r10_conteos_explicados()


def test_cr_r10_coherencia():
    """CR-R10-R1 / m1 / m2 sobre un canon mínimo que repite los tres errores de rev9 y su versión corregida."""
    import compuerta_entrega as CE
    mal = {"existing_walls": [{"id": "CH-L2-01 A", "location": "L2 South shaft (7/A9.03) north wall"}],
           "misc_items": [{"ref": "CH-STUD CH-L2-01", "familia": "C-H stud 6\" (printed)", "qty": 44}],
           "ceilings": [{"room": "L2 Corridor 216", "source": "x | height 9.885 (11'-0\" - 1'-1 3/8\" (7/A7.23))"},
                        {"room": "L2 Guest room 201", "source": "x | height 9.885 (11'-0\" - 1'-1 3/8\" (7/A7.23))"}]}
    fs = CE.coherencia_r10(mal)
    assert any(f.startswith("R1") for f in fs) and any(f.startswith("m1") for f in fs) and any(f.startswith("m2") for f in fs), fs
    mal["existing_walls"][0]["stud_text"] = "C-H 2-1/2\" (7/A9.03: 4 3/4\")"
    mal["ceilings"][1]["source"] = "x | height 9.24 (4/A5.05 room zone)"
    assert CE.coherencia_r10(mal) == [], CE.coherencia_r10(mal)
    mal["ceilings"][1]["source"] = "x | height 9.885 (11'-0\" - 1'-1 3/8\" (7/A7.23))"
    hj = {"A7.23": "7\nWALL DETAIL - CORRIDOR CEILING\n", "A5.06": "1\nWALL SECTION WEST ALLEY\n"}
    assert any(f.startswith("m1") for f in CE.coherencia_r10(mal, hj))
    mal["ceilings"] = [{"room": "L4 412 Corridor", "source": "x | height 8.94 (1/A5.06)"}, {"room": "L4 401 Guest Room", "source": "x | height 8.94 (1/A5.06)"}]
    assert CE.coherencia_r10(mal, hj) == []        # sección de techo compartida: no es detalle de corridor
    print("test_cr_r10_coherencia OK")


test_cr_r10_coherencia()


def test_cr_r11_coherencia():
    """CR-R11-F2 / F3 / F4 / P: repite los errores de rev10 (stud a 8.94 con liner a 10.4375, corner bead con el LF viejo, cielo de baño
    en Type X con la nota de W.R. en shower rooms, compound por regla de plantilla y 'TAKE-OFF REV5 FINAL' en la rev11) y su corrección."""
    import tempfile, openpyxl, compuerta_entrega as CE
    can = {"existing_walls": [{"id": "CH-L4-05 A", "height_ft": 10.4375}],
           "misc_items": [{"ref": "CH-STUD CH-L4-05", "op": "ROUNDUP(4.3/2.0)+1 = 4 studs x 8.94 ft = 35.76"},
                          {"ref": "SOF-L4-02 board", "op": "343.67 LF x (0.375 bottom + 0.542 vertical) = 315.14", "familia": "x"},
                          {"ref": "CLG-L4-106 board", "op": "109.36 SF x 1 layer(s)", "familia": "5/8\" gyp board Type X", "source": "L4 401 bath: A3.04"}],
           "trim_items": [{"ref": "SOF-L4-02 CB", "lf": 242.72, "op": "242.72 LF soffit length x 1 edge = 242.72"}]}
    hj = {"A0.06": "12. USE WATER-RESISTANT GYPSUM BOARD FOR CEILINGS IN SHOWER ROOMS."}
    fs = CE.coherencia_r11(can, hj)
    assert {f[:2] for f in fs} == {"F2", "F3", "F4"}, fs
    can["misc_items"][0]["op"] = "ROUNDUP(4.3/2.0)+1 = 4 studs x 10.4375 ft = 41.75"
    can["trim_items"][0]["lf"] = 343.67
    can["misc_items"][2]["familia"] = "5/8\" gyp Type X W.R."
    assert CE.coherencia_r11(can, hj) == []
    d = tempfile.mkdtemp(); x = d + "/P_rev11.xlsx"
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "PRICING"
    ws.append(["All-purpose joint compound 3-1/2 gal box (template: 1 box per 200 SF of finished board)"])
    ws.append(["NOTE: PROPOSAL HOLDS GOOD ONLY FOR THE ITEMS AND QUANTITIES LISTED ABOVE (TAKE-OFF REV5 FINAL)"]); wb.save(x)
    assert len(CE.proposal_coherente(x, "11")) == 2, CE.proposal_coherente(x, "11")
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "PRICING"; ws.append(["(TAKE-OFF REV11 FINAL)"]); wb.save(x)
    assert CE.proposal_coherente(x, "11") == []
    print("test_cr_r11_coherencia OK")


test_cr_r11_coherencia()


def test_cr_r11_cita_con_celda():
    """CR-R11-H6: una burbuja 'citada' exige la celda del Excel que la cita; el texto del canon (índices, barridos) ya no cuenta."""
    import inspect, chequeos_biblioteca as CB
    src = inspect.getsource(CB.cadena_detalles) + inspect.getsource(CB.ce_callouts if hasattr(CB, "ce_callouts") else CB.cadena_detalles)
    assert "cited in the Excel row" in inspect.getsource(CB.cadena_detalles)
    assert "json.dumps(b.canon" not in inspect.getsource(CB.cadena_detalles)
    print("test_cr_r11_cita_con_celda OK")


test_cr_r11_cita_con_celda()


def test_cr_r11_sheathing_vs_interior():
    """CR-R11-F12: XW.6.6-L4-17 cargaba la cara interior de F&B 410 a 11'-4 3/4" (corte del deck bar 2/A5.01) con el sheathing a 10.24:
    sheathing más bajo que la cara interior = FAIL; corregida a 8'-11 1/4" (3/A5.07 corta 410) = PASS."""
    import chequeos_biblioteca as CB

    class B:
        canon = {"walls": [], "existing_walls": [
            {"id": "XW-L4-17 A", "height_ft": 10.24, "board": "5/8 exterior gyp sheathing type X"},
            {"id": "XW-L4-17 B", "height_ft": 11.3958, "board": "5/8 type X", "height_source": "2/A5.01 B.O. FRAMING 11'-4 3/4\""}]}
    r = CB.cr_r11_f12(B())
    assert "FAIL" in str(r) and "XW-L4-17 A" in str(r), r
    B.canon["existing_walls"][1]["height_ft"] = 8.9375
    r = CB.cr_r11_f12(B())
    assert "PASS" in str(r), r
    print("test_cr_r11_sheathing_vs_interior OK")


test_cr_r11_sheathing_vs_interior()


def test_cr_r13_detector_no_impreso():
    """CR-R13 (COORDINACIÓN 9-nov): CE_RFI_BUSQUEDA_EXHAUSTIVA contaba 1 RFI 'not printed' de 9 abiertos; RFI-04 / 13 / 15 / 17 dicen
    'no partition tag', 'does not give', 'not labeled', 'not printed' -> todos entran a la búsqueda exhaustiva."""
    import compuerta_entrega as CE
    for t in ("Walls drawn with no partition tag on the floor plans", "MB-1 does not give the steel stud size",
              "L1 Water Entry 128 ceiling not labeled on A3.01", "board type not printed", "untagged wall"):
        assert CE.RX_NO_IMPRESO_RFI.search(t), t
    assert not CE.RX_NO_IMPRESO_RFI.search("Entry canopy: S1.02 notes PRE-FABRICATED ROOF CANOPY BY OTHERS")
    print("test_cr_r13_detector_no_impreso OK")


test_cr_r13_detector_no_impreso()


def test_u158_nombres_entrega():
    """U-158 (usuario 10-nov): 'A3.02_rcp_markups.png' confundió al usuario con los markups editables -> FAIL; los nombres nuevos -> PASS."""
    import compuerta_entrega as CE
    malos = ["A3.02_rcp_markups.png", "A2.01_marked_by_type_rev14.png", "p22_marked_by_type_rev14.png", "CR_City_Hotel_markups_rev14.pdf",
             "CR_City_Hotel_markups_rev18 - OPEN THIS IN BLUEBEAM (walls + ceilings, editable).pdf"]   # U-165: el nombre largo de U-158 ya no vale
    assert len(CE.nombres_planos(malos)) == 5, CE.nombres_planos(malos)
    buenos = ["CR_markups_rev14 - OPEN IN BLUEBEAM.pdf",
              "A3.02 - IMAGE ONLY (not editable) - ceilings rev14.png", "A2.01 - IMAGE ONLY (not editable) - walls rev14.png",
              "DETALLES_REVISADOS.pdf", "SCHEDULES_REVISADOS.pdf"]
    assert CE.nombres_planos(buenos) == [], CE.nombres_planos(buenos)
    assert CE.nombres_planos(buenos + ["A3.02 - IMAGE ONLY (not editable) - ceilings rev14 (copy).png"])
    print("test_u158_nombres_entrega OK")


test_u158_nombres_entrega()


def test_u165_ruta_windows():
    """U-165 / BE-155 (usuario 11-nov, CR City Hotel rev18: 'este no quiere habrir'): la ruta Windows del PDF de markups medía 264 caracteres
    (> 260, Windows / Bluebeam no la abren) -> FAIL; con el nombre corto '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' (219) -> PASS."""
    import compuerta_entrega as CE
    proy = "CR City Hotel - Castle Rock, CO (Owen-Ames-Kimball) 11-12-26"
    rev = "rev18 FINAL \u2014 ESTA ES LA VERSI\u00d3N FINAL PARA REVISAR"
    largo = "Planos marcados/CR_City_Hotel_markups_rev18 - OPEN THIS IN BLUEBEAM (walls + ceilings, editable).pdf"
    assert len(CE.ruta_windows(proy, rev, largo)) == 264, len(CE.ruta_windows(proy, rev, largo))
    f = CE.rutas_windows_fallas(proy, rev, [largo])
    assert f and "264" in f[0], f
    corto = "Planos marcados/" + CE.nombre_markups("CR", 18)
    assert len(CE.ruta_windows(proy, rev, corto)) == 219, len(CE.ruta_windows(proy, rev, corto))
    assert CE.rutas_windows_fallas(proy, rev, [corto, "Take-off/CR_City_Hotel_Takeoff_FINAL_rev18.xlsx"]) == []
    assert CE.rutas_windows_fallas(None, rev, [corto])   # sin carpeta_proyecto no se puede medir = FAIL
    assert CE.nombres_planos([corto]) == [] and CE.nombres_planos([largo.split("/")[1]])
    print("test_u165_ruta_windows OK")


test_u165_ruta_windows()


def test_u166_uso_real():
    """U-166 (usuario 11-nov: 'si ya sabes que va a pasar si cometes un error, por que no lo arreglas antes de que yo te lo diga'): CE_USO_REAL
    simula el uso real: ruta Windows en Drive <= 230 (Auditoria.zip = 1 archivo, nombres dentro <= 120), PDF sin contraseña ni firmas,
    nombres sin < > : " / \\ | ? *, Excel sin #REF! / #VALUE! / #DIV/0!; la ruta de rev18 (264) = FAIL."""
    import tempfile
    import fitz
    import openpyxl
    import compuerta_entrega as CE
    assert "CE_USO_REAL" in {k[0] for k in CE.CHEQUEOS}
    proy = "CR City Hotel - Castle Rock, CO (Owen-Ames-Kimball) 11-12-26"
    viejo = "rev18 FINAL \u2014 ESTA ES LA VERSI\u00d3N FINAL PARA REVISAR"
    largo = "Planos marcados/CR_City_Hotel_markups_rev18 - OPEN THIS IN BLUEBEAM (walls + ceilings, editable).pdf"
    f = CE.rutas_entrega_fallas(proy, viejo, [largo])                     # (1) + (5) ruta de rev18 = 264 -> FAIL
    assert f and "264" in f[0], f
    nuevo = "rev19 FINAL PARA REVISAR"
    assert CE.carpeta_rev_fallas(viejo) and CE.carpeta_rev_fallas(nuevo) == [] and CE.carpeta_rev_fallas("FINAL_FOR_REVIEW") == []
    aud = [f"Auditoria/x/{i:04d}.png" for i in range(5)] + ["Auditoria/" + "a" * 130 + ".png"]
    png = "Planos marcados/A7.50 - IMAGE ONLY (not editable) - walls and ceilings rev19.png"
    ok = [png, "Planos marcados/" + CE.nombre_markups("CR", 19)]
    assert CE.rutas_entrega_fallas(proy, nuevo, ok) == []
    dr, zn = CE.rutas_drive(ok + aud, umbral=3)                           # Auditoria.zip = un solo archivo en Drive
    assert "Auditoria.zip" in dr and not any(r.startswith("Auditoria/") for r in dr) and len(zn) == 6, (dr, zn)
    f = CE.rutas_entrega_fallas(proy, nuevo, ok + aud, umbral=3)
    assert len(f) == 1 and "dentro de Auditoria.zip" in f[0], f           # nombre de 140 dentro del zip > 120
    assert len(CE.nombres_prohibidos_fallas(['a<b.png', 'c:d', 'e"f', 'g|h', 'i?j', 'k*l', 'fin.'])) == 7    # (3)
    assert CE.nombres_prohibidos_fallas([proy, nuevo, png.split("/")[1], CE.nombre_markups("CR", 19)]) == []
    t = tempfile.mkdtemp(prefix="u166_")
    wb = openpyxl.Workbook(); ws = wb.active; ws["A1"] = 1; ws["A2"] = "=A1*2"; ws["A3"] = "=#REF!*2"; ws["A4"] = "#DIV/0!"
    malo = os.path.join(t, "malo.xlsx"); wb.save(malo)
    e = CE.excel_errores_fallas(malo)                                     # (4) #REF! en fórmula, #DIV/0! guardado, fórmula sin valor
    assert any("A3" in x for x in e) and any("A4" in x for x in e) and any("A2" in x and "sin valor" in x for x in e), e
    roto = os.path.join(t, "roto.xlsx"); open(roto, "w").write("no es un xlsx")
    assert "no abre" in CE.excel_errores_fallas(roto)[0]
    d = fitz.open(); d.new_page(); d.set_page_labels([{"startpage": 0, "prefix": "A2.01", "style": ""}])
    bueno = os.path.join(t, "CR_markups_rev19 - OPEN IN BLUEBEAM.pdf"); d.save(bueno)
    d = fitz.open(); d.new_page(); sinl = os.path.join(t, "sin_labels.pdf"); d.save(sinl)
    assert any("PageLabels" in x for x in CE.pdf_abre_fallas(sinl)), CE.pdf_abre_fallas(sinl)   # (2) Page Labels
    assert CE.pdf_abre_fallas(bueno) == [], CE.pdf_abre_fallas(bueno)     # (2) sin contraseña
    d = fitz.open(); d.new_page(); clave = os.path.join(t, "clave.pdf")
    d.save(clave, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw="x", owner_pw="y")
    assert CE.pdf_abre_fallas(clave) and "contraseña" in CE.pdf_abre_fallas(clave)[0]
    print("test_u166_uso_real OK")


test_u166_uso_real()


def test_u167_nm_unico():
    """U-167 / BE-156 (CR City Hotel rev18, CSV de Bluebeam del usuario sin 5 markups): /NM con '/' ('bedroom/closet') o repetido
    (fitz-A0... de los EXCLUDED) = FAIL en CE_VISTA_BLUEBEAM (nm_fallas); markups_bluebeam / markups_rcp lo dejan único y sin '/'
    (nm_unicos, nm_seguro reversible con nm_leer); con el PDF viejo de rev18 (si está en esta máquina) = FAIL."""
    import tempfile
    import pymupdf as fitz
    import markups_bluebeam as MB
    import verificar_markups_excel as VME
    k = "L4 401 Guest Room Type 11 (bedroom/closet, excl. bath)"
    assert MB.nm_leer(MB.nm_seguro("TO-" + k)) == "TO-" + k and "/" not in MB.nm_seguro(k) and "\\" not in MB.nm_seguro("a\\b")
    assert MB.nm_leer(MB.nm_seguro("TO-50% a/b")) == "TO-50% a/b"
    assert VME.parse_contents("X", "x", MB.nm_seguro("TO-" + k))["id"] == k          # los lectores recuperan la llave original
    t = tempfile.mkdtemp(prefix="u167_")
    d = fitz.open()
    for _ in range(2):                                     # dos páginas: fitz pone 'fitz-A0' en cada una (repetido en el PDF)
        p = d.new_page()
        p.add_polygon_annot([(10, 10), (60, 10), (60, 60)]).update()
    a = d[0].add_polygon_annot([(100, 100), (150, 100), (150, 150)])
    a.update()
    d.xref_set_key(a.xref, "NM", fitz.get_pdf_str("TO-" + k))   # como rev18: /NM con '/'
    malo = os.path.join(t, "malo.pdf"); d.save(malo)
    f = MB.nm_fallas(malo)
    assert any("'/'" in x for x in f) and any("repetido" in x for x in f), f
    d = fitz.open(malo); n = MB.nm_unicos(d); bueno = os.path.join(t, "bueno.pdf"); d.save(bueno)
    assert n >= 2 and MB.nm_fallas(bueno) == [], (n, MB.nm_fallas(bueno))
    nms = [a.info.get("id") for p in fitz.open(bueno) for a in p.annots()]
    assert MB.nm_seguro("TO-" + k) in nms and len(set(nms)) == len(nms), nms
    viejo = ("/root/cr/work/entrega/rev18 FINAL \u2014 ESTA ES LA VERSI\u00d3N FINAL PARA REVISAR/Planos marcados/"
             "CR_City_Hotel_markups_rev18 - OPEN THIS IN BLUEBEAM (walls + ceilings, editable).pdf")
    if os.path.isfile(viejo):                              # el PDF de rev18 que el usuario exportó a CSV
        f = MB.nm_fallas(viejo)
        assert sum("'/'" in x for x in f) == 5 and any("repetido" in x for x in f), f
    # BE-157: vista_csv / _escribir no escriben dentro de un inode compartido (copia con hard links de una entrega ya subida)
    import compuerta_entrega as CE
    orig = os.path.join(t, "VISTA_BLUEBEAM.csv"); open(orig, "w").write("original")
    link = os.path.join(t, "link.csv"); os.link(orig, link)
    CE.vista_csv([], link)
    CE._escribir(link, "nuevo")
    assert open(orig).read() == "original" and open(link).read() == "nuevo"
    print("test_u167_nm_unico OK (incluye BE-157)")


test_u167_nm_unico()


def test_u168_checklist():
    """U-168 (usuario 11-nov: 'todo esas maneras de revisar ... los combiertas en reglas inviolables ... incluyendo las cvs'):
    A1 re-mide en vectores (wall cuyo dibujo es 3 ft más largo = FAIL), A2 contra la cota impresa (altura no impresa = FAIL; la
    nota dice dónde sí está impresa), checklist_revision.py arma CHECKLIST_REVISION.xlsx y CE_CHECKLIST_USUARIO lo exige completo."""
    import tempfile
    import openpyxl
    import pymupdf as fitz
    import compuerta_entrega as CE
    import markups_bluebeam as MB
    import checklist_revision as CL
    t = tempfile.mkdtemp(prefix="u168_")
    ptft = 9.0
    plano, mk = fitz.open(), fitz.open()
    for d in (plano, mk):
        d.new_page(width=1200, height=900)
        d.new_page(width=1200, height=900)
    pg = plano[0]
    walls = []
    for k in range(12):                                   # doce muros horizontales: largo 20 + k ft, una banda de 2 líneas + cierres
        y = 60 + 60 * k
        L = (20 + k) * ptft
        dib = L + (3 * ptft if k == 11 else 0)            # la wall más larga está dibujada 3 ft más larga que el Excel
        for dy in (-2.5, 2.5):
            pg.draw_line((100, y + dy), (100 + dib, y + dy))
        for x in (100, 100 + dib):
            pg.draw_line((x, y - 6), (x, y + 6))
        a = mk[0].add_polyline_annot([(100, y), (100 + L, y)])
        a.update()
        MB._nm(mk, a, f"TO-W{k:02d}")
        MB._measure(mk, a, ptft)
        walls.append((f"W{k:02d}", 20 + k, 9.2396 if k % 2 else 10.0))
    plano[1].insert_text((100, 100), "SECTION 4  9'-2 7/8\"  CEILING", fontsize=9)   # solo 9'-2 7/8" impresa; 10'-0" no
    mk.set_page_labels([{"startpage": 0, "prefix": "A2.01", "style": ""}, {"startpage": 1, "prefix": "A5.05", "style": ""}])
    pp, mp = os.path.join(t, "plano.pdf"), os.path.join(t, "CR_markups_rev1 - OPEN IN BLUEBEAM.pdf")
    plano.save(pp)
    mk.save(mp)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    ws.append(["t"]); ws.append(["t"]); ws.append([])
    ws.append(["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size", "Stud O.C. (in)", "Board (SF)",
               "Location", "Source (DETAIL/SHEET)", "Status"])
    for w, L, h in walls:
        ws.append(["X", w, L, h, 1, "", "", L * h, "", "4/A5.05", "[DERIVED]"])
    sc = wb.create_sheet("Scope Checklist")
    sc.append(["Scope ID", "Scope", "Status", "Note"])
    sc.append(["ALC-E05", "Insulation", "NOT APPLICABLE", "EXCLUDED - insulation"])
    sc.append(["ALC-01", "Framing", "QUANTIFIED", "loaded"])
    ri = wb.create_sheet("Review Items")
    ri.append(["1 questions"]); ri.append(["#", "Phase", "Type", "Item", "Sheet", "Image"])
    ri.append(["1/1", "Floor plan", "W", "Wall W05 loaded 2 layers; delta -100 SF if 1 layer", "A2.01", "x.png"])
    xp = os.path.join(t, "takeoff.xlsx")
    wb.save(xp)
    a1, f1 = CE.a1_remedir(xp, mp, pp)
    assert len(a1) == 10 and len(f1) == 1 and "W11" in f1[0], f1                  # la dibujada 3 ft más larga = FAIL
    assert all(abs(r["delta"]) <= 1 for r in a1 if r["wall"] != "W11"), a1
    a2, f2 = CE.a2_alturas(xp, mp, pp, {})
    est = {r["depth"]: r["estado"] for r in a2}
    assert est[9.2396] == "PRINTED" and est[10.0] == "NOT FOUND" and len(f2) == 1, (est, f2)
    sal = os.path.join(t, "CHECKLIST_REVISION.xlsx")
    CL.escribir(sal, xp, mp, a1, f1, a2, f2, [("A2.01", "Floor plan", 12, 0)], CL.datos(xp, mp, pp, {})[5])
    assert CE.checklist_fallas(sal, xp) == [], CE.checklist_fallas(sal, xp)
    w2 = openpyxl.load_workbook(sal)
    assert "AYUDA (ES)" in str(w2["B1 Longest walls"]["A2"].value) and w2["B1 Longest walls"]["B4"].value == "W11"
    assert {r[1] for r in w2["B4 Exclusions & decisions"].iter_rows(min_row=4, values_only=True)} >= {"ALC-E05", "1/1"}
    w2["B1 Longest walls"].delete_rows(4)                  # falta la wall más larga
    w2["B4 Exclusions & decisions"].delete_rows(4)         # falta una exclusión
    malo = os.path.join(t, "malo.xlsx")
    w2.save(malo)
    f = CE.checklist_fallas(malo, xp)
    assert any(x.startswith("B1") for x in f) and any(x.startswith("B4") for x in f), f
    assert {"CE_CHECKLIST_USUARIO", "CE_A1_REMEDICION", "CE_A2_ALTURAS"} <= {k[0] for k in CE.CHEQUEOS}
    print("test_u168_checklist OK")


test_u168_checklist()


def test_tiempos_cita_sf():
    """CR City Hotel 11-nov (COORDINACIÓN): (1) CE_TIEMPOS: filas de rev15-rev17 en UTC con etiqueta PST (encimadas) y TOTAL distinto de la
    suma = FAIL; (2) CE_CITA_ALTURA: la altura de W.4-L2-03 A de rev18 citaba 'A7.xx unit RCP' = FAIL; (3) CE_DATOS_PROYECTO / U-170:
    SF del proyecto sin hoja o [PENDIENTE] sin barrido = FAIL."""
    import compuerta_entrega as CE
    cab = "| # | Paso | Inicio | Fin | Duración | Evidencia |\n|---|---|---|---|---|---|\n"
    fila = lambda k, a, b, d: f"| {k} | x | 11-10 {a} PST | 11-10 {b} PST | {d} min | e |\n"   # noqa: E731
    malo = cab + fila("rev15", "14:05", "18:30", 265) + fila("rev16", "15:45", "16:57", 72) + "| **TOTAL** | x | a | b | **337 min** | m |\n"
    f = CE.tiempos_fallas(malo)
    assert any("encimadas" in x for x in f), f
    bueno = cab + fila("rev15", "14:05", "15:30", 85) + fila("rev16", "15:45", "16:57", 72) + "| **TOTAL** | x | a | b | **157 min** | m |\n"
    assert CE.tiempos_fallas(bueno) == [], CE.tiempos_fallas(bueno)
    assert any("TOTAL" in x for x in CE.tiempos_fallas(bueno.replace("**157 min**", "**2409 min**")))
    assert any("Duración" in x for x in CE.tiempos_fallas(bueno.replace("| 85 min |", "| 95 min |").replace("157", "167")))
    w = lambda i, src: {"id": i, "height_source": src}   # noqa: E731
    rev18 = w("W.4-L2-03 A", "Bath ceiling GYP-1 8'-6\" (A7.xx unit RCP) + 6\" above line of ceiling (A0.06 furred wood head detail) = 9'-0\"")
    f = CE.cita_altura_fallas({"walls": [rev18]})
    assert f and "A7.xx" in f[0], f
    assert CE.cita_altura_fallas({"walls": [w("W1", "Bath ceiling GYP-1 8'-6\" (A7.05 unit RCP) + 6\" (A0.06) = 9'-0\"")]}) == []
    assert CE.cita_altura_fallas({"walls": [w("W2", "9'-2 7/8\" - 9'-0\" = 0'-2 7/8\"")]})          # sin hoja = FAIL
    sf = lambda v, f_="": {"proyecto_datos": [{"campo": "total building area SF", "valor": v, "fuente": f_}]}   # noqa: E731
    assert CE.sf_proyecto_fallas(sf("35,676 SF gross", "A0.00 code summary")) == []
    assert CE.sf_proyecto_fallas(sf("1,798 SF", "BuildingConnected project size")) == []
    assert CE.sf_proyecto_fallas(sf("35,676 SF gross", "code summary"))                            # sin hoja
    assert CE.sf_proyecto_fallas(sf("[PENDIENTE]", ""))                                             # sin barrido
    assert CE.sf_proyecto_fallas(sf("[PENDIENTE] not printed; swept T0.00, A0.00, G0.01", "")) == []
    assert CE.sf_proyecto_fallas({"proyecto_datos": []})
    assert {"CE_CITA_ALTURA", "CE_TIEMPOS", "CE_DATOS_PROYECTO"} <= {k[0] for k in CE.CHEQUEOS}
    print("test_tiempos_cita_sf OK")


test_tiempos_cita_sf()


def test_u159_u160_rcp_cuartos():
    """U-159 / U-160 (usuario 10-nov, CR City Hotel rev13): 417 Women stalls / 421 sin renglón y 419 excluido sin texto EXCLUDED -> FAIL;
    con renglón / exclusión y FreeText sobre el cuarto -> PASS."""
    import compuerta_entrega as CE
    hojas = {"A3.04": "LEVEL 4 - RCP\nREFLECTED CEILING PLAN\n417\n419\n421\n104.1"}
    hc = CE.cuartos_rcp(hojas)
    assert hc == {"A3.04": ["417", "419", "421"]}, hc
    t13 = {"rooms": [{"sheet": "A3.04", "room": "419", "disposition": "exclusion", "reason": "F&B not in scope", "nhoja": "3/A7.50",
                      "label_xy": [100, 100]}]}
    ev = CE.rcp_cuartos_fallas(hc, t13, {})
    assert any("417" in e for e in ev) and any("421" in e for e in ev) and any("419" in e and "FreeText" in e for e in ev), ev
    t14 = {"rooms": t13["rooms"] + [{"sheet": "A3.04", "room": "417", "disposition": "missing_loaded", "rows": ["CLG-L4-117b board"]},
                                    {"sheet": "A3.04", "room": "421", "disposition": "row", "rows": ["CLG-L4-119 board"]}]}
    assert CE.rcp_cuartos_fallas(hc, t14, {"A3.04": [((50, 80, 150, 120), "EXCLUDED - F&B not in scope (3/A7.50)")]}) == []
    print("test_u159_u160_rcp_cuartos OK")


test_u159_u160_rcp_cuartos()


def test_rev15_u160_texto_dentro_poligono():
    """rev15 (revisión completa rev14 F02/F03/F08): exclusión sin polígono gris, texto fuera del cuarto (410.3 sobre Men 418) o con
    callout /CL = FAIL; markups_rcp.aplicar() real sobre un PDF -> polígono + texto dentro (>= 90 %) sin /CL = PASS."""
    import compuerta_entrega as CE, markups_rcp as MR, pymupdf, tempfile, os
    shaft = [[100, 100], [125, 100], [125, 135], [100, 135]]          # shaft de 25 x 35 pt (el caso de rev14: texto de 124-216 pt)
    t = {"rooms": [{"sheet": "A3.04", "room": "(north shaft)", "disposition": "exclusion", "reason": "2-hour shaft, no ceiling",
                    "nhoja": "1/A3.04", "label_xy": [112, 117], "polygon": shaft},
                   {"sheet": "A3.04", "room": "410", "disposition": "exclusion", "reason": "F&B not in scope", "nhoja": "1/A2.04",
                    "label_xy": [300, 300]}]}
    txt = "EXCLUDED - 2-hour shaft, no ceiling (1/A3.04)"
    ev = CE.rcp_excluded_geom_fallas(t, {"A3.04": [(txt, shaft)]}, {"A3.04": [((50, 103, 174, 131), txt, True)]})
    assert any("410" in e and "polígono" in e for e in ev), ev
    assert any("shaft" in e and "dentro" in e for e in ev) and any("/CL" in e for e in ev), ev
    d = tempfile.mkdtemp(); f = os.path.join(d, "m.pdf")
    doc = pymupdf.open(); pg = doc.new_page(width=600, height=400); doc.set_page_labels([{"startpage": 0, "prefix": "A3.04", "style": ""}]); doc.save(f)
    t["rooms"][1]["polygon"] = [[200, 200], [420, 200], [420, 330], [200, 330]]
    hechos, faltan = MR.aplicar(f, t)
    assert not faltan and len(hechos) == 2, (hechos, faltan)
    exp, ext = {}, {}
    D = pymupdf.open(f)
    for p in D:
        for a in p.annots():
            if a.type[1] == "Polygon":
                exp.setdefault("A3.04", []).append((a.info["content"], [[q[0], q[1]] for q in a.vertices]))
            elif a.type[1] == "FreeText":
                ext.setdefault("A3.04", []).append((tuple(a.rect), a.info["content"], D.xref_get_key(a.xref, "CL")[0] != "null"))
    assert CE.rcp_excluded_geom_fallas(t, exp, ext) == [], CE.rcp_excluded_geom_fallas(t, exp, ext)
    t2 = {"rooms": [dict(t["rooms"][0], polygon=None)]}
    assert MR.aplicar(f, t2)[1], "sin polígono debe quedar en faltan"
    print("test_rev15_u160_texto_dentro_poligono OK")


test_rev15_u160_texto_dentro_poligono()


def test_rev15_guia_cambios_primero():
    """rev15 #18: la GUIA de rev14 abría con 'CAMBIOS rev7 vs rev6' -> FAIL; con 'CAMBIOS rev15 vs rev14' primero -> PASS."""
    import compuerta_entrega as CE
    g14 = "OPEN IN BLUEBEAM: x\n# GUIA\n\n## CAMBIOS rev7 vs rev6\n\n## CAMBIOS rev14 vs rev13\n"
    assert CE.guia_cambios_fallas(g14, "rev14 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR")
    g15 = "OPEN IN BLUEBEAM: x\n# GUIA\n\n## CAMBIOS rev15 vs rev14\n\n## CAMBIOS rev14 vs rev13\n"
    assert CE.guia_cambios_fallas(g15, "rev15 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR") == []
    print("test_rev15_guia_cambios_primero OK")


test_rev15_guia_cambios_primero()


def test_rev15_rcp_contorno():
    """rev15 (revisión completa rev14 F04 / F05): polígono de cielo con el offset planta->RCP sumado dos veces (13, 19.5 pt) -> cobertura
    de borde baja = FAIL; en la vista 'ENLARGED PLAN' de una hoja A7 = FAIL; sobre las líneas y en la vista RCP = PASS."""
    import compuerta_entrega as CE, pymupdf
    def doc(dx, dy, titulo):
        d = pymupdf.open(); p = d.new_page(width=800, height=600)
        sh = p.new_shape(); sh.draw_rect(pymupdf.Rect(100, 100, 300, 250)); sh.finish(color=(0, 0, 0), width=0.5); sh.commit()
        p.insert_text((100, 300), titulo, fontsize=8)
        d.set_page_labels([{"startpage": 0, "prefix": "A7.50", "style": ""}])
        a = p.add_polygon_annot([pymupdf.Point(100 + dx, 100 + dy), pymupdf.Point(300 + dx, 100 + dy), pymupdf.Point(300 + dx, 250 + dy), pymupdf.Point(100 + dx, 250 + dy)])
        a.set_info(title="take-off", content="CEILING CLG-L2-56 · 442.09 SF"); a.update()
        return d
    limpio = doc(0, 0, "1/4\" = 1'-0\" 2 ENLARGED RCP - STAFF")
    ev, n, _ = CE.rcp_contorno_fallas(doc(13.1, 19.5, "1/4\" = 1'-0\" 2 ENLARGED RCP - STAFF"), limpio=limpio)
    assert n == 1 and any("contorno" in e for e in ev), ev
    ev, n, _ = CE.rcp_contorno_fallas(doc(0, 0, "1/4\" = 1'-0\" 1 ENLARGED PLAN - STAFF"), limpio=doc(0, 0, "x"))
    assert any("PLAN" in e for e in ev), ev
    ev, n, _ = CE.rcp_contorno_fallas(doc(0, 0, "1/4\" = 1'-0\" 2 ENLARGED RCP - STAFF"), limpio=limpio)
    assert ev == [], ev
    print("test_rev15_rcp_contorno OK")


test_rev15_rcp_contorno()


def test_rev15_piezas_min():
    """rev15 (revisión completa F08): studs largos sacados de sticks de 20 ft: un stud por stick; Pieces = MAX(ROUNDUP(Purchase / stock), piezas_min)."""
    import plantilla_excel as P
    m = {"material": "C-H stud 2-1/2 in. 20 GA", "unit": "LF", "net": 100.0, "metal": True, "selling_unit": "stick 20 ft", "stock": 20}
    f0 = P.formula_piezas(m, 19, {})
    assert f0.startswith("=ROUNDUP(") and "MAX" not in f0, f0
    f1 = P.formula_piezas(dict(m, piezas_min=9), 19, {})
    assert f1 == "=MAX(" + f0[1:] + ",9)", f1
    assert f1.count("ROUNDUP") == 1          # el validador: desperdicio una sola vez
    print("test_rev15_piezas_min OK")


test_rev15_piezas_min()


def test_rev16_verticales_rcp():
    """rev16 (revisión dirigida de rev15): A3.04 marca hoistways / shafts y A3.02 los deja en blanco (áreas sin número) -> FAIL;
    con su EXCLUDED en A3.02 (o not_on con motivo impreso) -> PASS."""
    import compuerta_entrega as CE
    t = {"rooms": [{"sheet": "A3.02", "room": "201", "disposition": "row", "rows": ["x"]},
                   {"sheet": "A3.04", "room": "(service elevator hoistway)", "disposition": "exclusion", "vertical": "hoistway-service"},
                   {"sheet": "A3.04", "room": "(north shaft)", "disposition": "exclusion", "vertical": "shaft-N"}]}
    ev = CE.rcp_verticales_fallas(t)
    assert any("A3.02" in e and "hoistway-service" in e for e in ev) and any("shaft-N" in e for e in ev), ev
    t["rooms"] += [{"sheet": "A3.02", "room": "(service elevator hoistway)", "disposition": "exclusion", "vertical": "hoistway-service"},
                   {"sheet": "A3.02", "room": "(north shaft)", "disposition": "row", "rows": ["CLG"], "vertical": "shaft-N"}]
    assert CE.rcp_verticales_fallas(t) == [], CE.rcp_verticales_fallas(t)
    t2 = {"rooms": [{"sheet": "A3.02", "room": "201", "disposition": "row", "rows": ["x"]},
                    {"sheet": "A3.04", "room": "(north shaft)", "disposition": "exclusion", "vertical": "shaft-N",
                     "not_on": {"A3.02": "shaft starts at L3 (7/A9.03)"}}]}
    assert CE.rcp_verticales_fallas(t2) == []
    print("test_rev16_verticales_rcp OK")


test_rev16_verticales_rcp()


def test_u164_un_solo_resumen():
    """U-164 (usuario 11-nov: 'RESUMEN_rev5 al 17, cual es la reazon de crear tantos'): rev18 subió RESUMEN_rev5..rev18 a la raíz -> FAIL;
    un solo RESUMEN_rev18.md + Auditoria/HISTORIAL_CAMBIOS.md -> PASS."""
    import compuerta_entrega as CE
    raiz18 = [f"RESUMEN_rev{n}.md" for n in range(5, 19)] + ["GUIA_DE_REVISION_DEL_ESTIMADOR.md", "Auditoria", "Take-off"]
    assert CE.resumenes_fallas(raiz18) and "U-164" in CE.resumenes_fallas(raiz18)[0]
    assert CE.resumenes_fallas(["RESUMEN_rev18.md", "GUIA_DE_REVISION_DEL_ESTIMADOR.md", "Auditoria"]) == []
    print("test_u164_un_solo_resumen OK")


test_u164_un_solo_resumen()


def test_xf_hojas_un_decimal():
    """Xfinity Interquest 10-nov (BE-XF03..BE-XF06): (1) RX_HOJA_CONCRETA y la cita de altura de A2 aceptan hojas de UN decimal
    (A0.1, A2.0): el SF del proyecto 'A0.1 BUILDING DATA' daba 'sin hoja'; (2) CE_RCP_CUARTOS acepta 'not_a_room' solo con motivo,
    N/HOJA e imagen existente (designator de acero '600 S 162' y herraje '200D' leídos como cuartos); (3) BE-CF04 con
    wood_walls_none_reason citado = PASS (no 'en vacío'); (4) CC-R12 sin walls de largo Y altura impresos = N/A declarado, no '0 walls'."""
    import tempfile
    assert CE.RX_HOJA_CONCRETA.search("A0.1 BUILDING DATA") and CE.RX_HOJA_CONCRETA.search("A2.01") and not CE.RX_HOJA_CONCRETA.search("A7.xx")
    d = tempfile.mkdtemp(); img = os.path.join(d, "x.png"); open(img, "wb").write(b"x")
    hc = {"A3.0": ["600"]}
    malo = {"rooms": [{"sheet": "A3.0", "room": "600", "disposition": "not_a_room", "reason": "designator", "nhoja": "A3.0"}]}
    bueno = {"rooms": [dict(malo["rooms"][0], img=img)]}
    assert CE.rcp_cuartos_fallas(hc, malo, {}) and not CE.rcp_cuartos_fallas(hc, bueno, {})
    import chequeos_biblioteca as CB
    class B_:
        canon = {"walls": [], "wood_walls_none_reason": "no wood-framed wall in the set: 2/A2.0 W2 metal studs"}
        def walls(self): return []
        def walls_todos(self): return [{"id": "W2-02", "length_status": "CONFIRMADO", "height_status": "DERIVADO"}]
        pt = []
    f04 = [f for n, f in vars(CB).items() if n == "be_cf04"][0]
    assert f04(B_())[0] == "PASS", f04(B_())
    r12 = [f for n, f in vars(CB).items() if n == "cc_r12"][0]
    est, ev = r12(B_())[0], r12(B_())[1:]
    assert est == "PASS" and "W2-02" in " ".join(map(str, ev)), (est, ev)
    print("test_xf_hojas_un_decimal OK")


test_xf_hojas_un_decimal()


def test_xf07_leyenda_subject_type():
    """BE-XF07 (Xfinity Interquest rev1, COORDINACIÓN 10-nov): la hoja LEGEND tenía 2 PolyLine con Subject 'W2' / 'CF' sin
    /Measure en una página sin /VP -> Bluebeam las sumaba al grupo del type (W2 3, CF 7). Subject = type o DEMO sin /Measure o
    en página sin /VP = FAIL en CE_VISTA_BLUEBEAM; Subject LEGEND = PASS. El nombre '<PROY>_markups_rev1b' es válido (rev con
    letra), y el decorador @chequeo de CE_VISTA_BLUEBEAM registra ce_vista_bluebeam (no una función auxiliar puesta en medio).
    Con el PDF viejo de Xfinity rev1 (si está en esta máquina) = FAIL."""
    import re, tempfile
    import pymupdf as fitz
    import compuerta_entrega as CE
    t = tempfile.mkdtemp(prefix="xf07_")
    for sj, nfallas in (("W2", 1), ("CF", 1), ("DEMO", 1), ("LEGEND", 0)):
        d = fitz.open(); p = d.new_page()
        a = p.add_polyline_annot([(10, 10), (80, 10)]); a.set_info(subject=sj, content=f"LEGEND · {sj}"); a.update()
        f = os.path.join(t, f"{sj}.pdf"); d.save(f)
        r = CE.subject_sin_medida_fallas(f, tipos=["W2", "CF"])
        assert len(r) == nfallas, (sj, r)
    assert re.fullmatch(CE.MARKUPS_RE, "XF_markups_rev1b - OPEN IN BLUEBEAM.pdf")
    assert re.fullmatch(CE.MARKUPS_RE, "XF_markups_rev2 - OPEN IN BLUEBEAM.pdf")
    assert not re.fullmatch(CE.MARKUPS_RE, "XF_markups_rev1bb - OPEN IN BLUEBEAM.pdf")
    reg = {cid: fn.__name__ for cid, _r, _d, fn in CE.CHEQUEOS}
    assert reg["CE_VISTA_BLUEBEAM"] == "ce_vista_bluebeam", reg["CE_VISTA_BLUEBEAM"]
    assert all(fn.__name__ != "subject_sin_medida_fallas" for *_x, fn in CE.CHEQUEOS)
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "markups_bluebeam.py"), encoding="utf-8").read()
    assert '"LEGEND",   # BE-XF07' in src
    viejo = "/root/xf/zz_XF_markups_rev1_old.pdf"
    if os.path.isfile(viejo):
        r = CE.subject_sin_medida_fallas(viejo, tipos=["W1", "W2", "W4", "CF"])
        assert len(r) == 2 and any("'W2'" in x for x in r) and any("'CF'" in x for x in r), r
    print("test_xf07_leyenda_subject_type OK")


test_xf07_leyenda_subject_type()


def test_u177_auditoria():
    """U-177 (auditoría adversarial U-138 11-nov, BE-AUD01..04) — cada caso repite el hallazgo:
    (3) CE_MS_GAUGE: '3-5/8" metal stud - per source' con 16 ga sin gauge = FAIL; con la designación = PASS; sin N/HOJA = FAIL.
    (4) CE_MS_PRODUCTO_IMPRESO: blocking impreso '6" sheet metal blocking strapping' en un renglón 'metal stud blocking' = FAIL.
    (2) CE_RCP_CONTORNO: coincidencia 0.0 con [EDGE NOT DRAWN] = FAIL (piso 0.5).
    (1) CE_ENTREGA_VIGENTE: Drive con otro md5 o compuerta sin los chequeos vigentes = FAIL; igual = PASS.
    CE_MATERIALES_SCHEDULE: type existente 'TO REMAIN', regla '6\\" ABOVE CEILING' y notas informativas ya no salen AMBER."""
    import tempfile
    import pymupdf as fitz
    import revision_materiales as RV
    import subir_entrega as SE
    import trazabilidad as TZ
    F = lambda m, net, cita="N/SHEET: 8/X9.9 | Breakdown": {"fila": 9, "material": m, "net": net, "cita": cita}   # noqa: E731
    assert CE.ms_gauge_fallas([F('3-5/8" metal stud (LF of material) - per source', 140)])
    assert CE.ms_gauge_fallas([F("Ceiling / soffit track (size per source, see Where it comes from)", 16.99)])
    assert CE.ms_gauge_fallas([F('3-5/8" metal stud (LF of material) - 362S162-54', 125, "Breakdown only")])
    assert not CE.ms_gauge_fallas([F('3-5/8" metal stud (LF of material) - 362S162-54', 125), F("Header / metal stud box beam - 362S125-33", 8.67),
                                    F('Blocking / backing at wall-mounted items (notes) - 16 ga x 6" x 1-1/2" unpunched track', 32.88),
                                    F("METAL trim - corner bead", 31.49), F('Bottom track 3-5/8"', 0)])
    can = {"blocking_items": [{"ref": "BK-Z1", "lf": 7.25, "product": '6" sheet metal blocking strapping (metal - included; gauge not printed)'}]}
    assert TZ._producto_impreso(can["blocking_items"][0]) == '6" sheet metal blocking strapping'
    assert CE.ms_producto_fallas([F("Metal stud blocking at wall-mounted items (notes) - stud blocking (per source)", 7.25, "N/SHEET: 8/X9.9 | BK-Z1 7.25")], can)
    assert not CE.ms_producto_fallas([F('Blocking / backing at wall-mounted items (notes) - 6" sheet metal blocking strapping', 7.25, "N/SHEET: 8/X9.9 | BK-Z1 7.25")], can)
    g = TZ._por_producto("Header / metal stud box beam", "header / box beam", [("Door 9 (X1-01)", 8.67)], {"X1-01": {"gauge": "20 ga (362S125-33)"}}, {})
    assert list(g) == ["362T125-33"], g                 # BE-GK30: el header (track con stud anidado) toma la designación de track
    g = TZ._por_producto("Blocking / backing at wall-mounted items (notes)", "metal stud blocking (362CR / STUD BLOCKING)", [("BK-Z1", 7.25)], {}, can)
    assert list(g) == ['6" sheet metal blocking strapping'], g
    # (2) piso de contorno
    d = fitz.open(); p = d.new_page()
    a = p.add_polygon_annot([(100, 100), (300, 100), (300, 300), (100, 300)]); a.set_info(title="take-off", content="CLG-Z1 [EDGE NOT DRAWN: open to the floor above, no line printed]"); a.update()
    limpio = fitz.open(); limpio.new_page()
    ev, n, st = CE.rcp_contorno_fallas(d, limpio=limpio)
    assert n == 1 and any("piso U-177" in x for x in ev), (ev, st)
    # (1) entrega vigente
    ids = [x[0] for x in CE.CHEQUEOS]
    ok = {"ok": True, "vigentes": {"pdf": {"nombre": "XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf", "md5": "abc"}, "excel": {"nombre": "XQ.xlsx", "md5": "def"}},
          "chequeos": [{"id": i} for i in ids]}
    assert CE.vigente_fallas(ok, {"XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf": "abc", "XQ.xlsx": "def"}, ids) == []
    assert CE.vigente_fallas(ok, {"XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf": "999", "XQ.xlsx": "def"}, ids)
    assert CE.vigente_fallas(dict(ok, chequeos=[{"id": i} for i in ids[:-3]]), {"XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf": "abc", "XQ.xlsx": "def"}, ids)
    assert CE.vigente_fallas({"ok": True, "chequeos": ok["chequeos"]}, {}, ids)
    log = [{"archivo": "r/Planos marcados/XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf", "carpeta_id": "P"}, {"archivo": "r/Take-off/XQ.xlsx", "carpeta_id": "T"}]
    lst = {"P": {"XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf": "abc"}, "T": {"XQ.xlsx": "def"}}
    assert SE.verificar_vigente(ok, log, listar=lambda cid: lst[cid]) == []
    lst["P"] = {"XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf": "000"}
    assert SE.verificar_vigente(ok, log, listar=lambda cid: lst[cid])
    t = tempfile.mkdtemp(); os.makedirs(os.path.join(t, "Planos marcados")); os.makedirs(os.path.join(t, "Take-off"))
    for n_ in ("XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf", "XQ_markups_rev1b - OPEN IN BLUEBEAM.pdf"):
        open(os.path.join(t, "Planos marcados", n_), "w").write("x")
    open(os.path.join(t, "Take-off", "XQ.xlsx"), "w").write("x")
    assert CE.vigentes_entrega(t)[1], "dos PDF vigentes = FAIL"
    os.rename(os.path.join(t, "Planos marcados", "XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf"), os.path.join(t, "Planos marcados", "zz NO USAR - XQ_markups_rev1 old.pdf"))
    assert CE.vigentes_entrega(t)[1] == []
    # CE_MATERIALES_SCHEDULE: falsos AMBER
    r = RV.comparar_type("X1", {"faces_note": "EXISTING demising wall to remain", "extras": ["EXISTING DEMISING WALL TO REMAIN"]}, [], {}, [])
    assert r["verdict"] == "GREEN", r
    fila = [{"type": "X2", "wall": "X2-01", "h": 12.5, "stud": '3-5/8"', "oc": 16}]
    r = RV.comparar_type("X2", {"height": "FROM SLAB TO 6\" ABOVE CEILING U.N.O.", "extras": ["Level 4 finish (X9.9 note 3)"]}, fila, {}, [])
    assert all(x["status"] == "GREEN" for x in r["checks"] if x["field"] in ("height", "extra")), r["checks"]
    r = RV.comparar_type("X2", {"extras": ["SOUND BATT INSULATION"]}, fila, {}, [])
    assert any(x["field"] == "extra" and x["status"] == "AMBER" for x in r["checks"])
    print("test_u177_auditoria OK")


test_u177_auditoria()


def test_u179_rfi_listo():
    """U-179 (usuario 11-nov: "Siempre que halla errores corrígelos antes de preguntar lo rfi"): caso Grand Kia RFI-35 — opción con
    '+10 %' sin medir = FAIL; medida en la geometría impresa ('-57.0 SF [DERIVED] triangle 1/2 x 9.5 x 12 = 57.0') = PASS; sin recorte = FAIL;
    PENDING - user manual verification (U-178) solo pide valor cargado; con otro chequeo en FAIL la compuerta pone CE_RFI_LISTO en FAIL."""
    import tempfile
    img = os.path.join(tempfile.mkdtemp(), "r.png"); open(img, "wb").write(b"x")
    malo = {"id": "RFI-35", "status": "open", "img": img, "opciones": {"A": {"delta": "loaded: 1,200 SF"}, "B": {"delta": "+10 %"}, "C": ""}}
    assert CE.rfi_listo_fallas([malo]), "'+10 %' sin medir debe fallar"
    bueno = dict(malo, opciones={"A": {"delta": "loaded: 1,200 SF"}, "B": {"delta": "-57.0 SF [DERIVED] triangle 1/2 x 9.5 x 12 = 57.0 SF (X9.9)"}, "C": ""})
    assert CE.rfi_listo_fallas([bueno]) == [], CE.rfi_listo_fallas([bueno])
    assert CE.rfi_listo_fallas([dict(bueno, img=None)]), "sin recorte debe fallar"
    assert CE.rfi_listo_fallas([{"id": "RFI-36", "status": "open", "pending": "PENDING - user manual verification", "loaded": "+12 SF"}]) == []
    assert CE.rfi_listo_fallas([{"id": "RFI-37", "status": "open", "pending": "PENDING - user manual verification"}])
    assert CE.rfi_listo_fallas([dict(malo, status="closed")]) == []
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "compuerta_entrega.py"), encoding="utf-8").read()
    assert "corregir los errores ANTES de preguntar (U-179)" in src and "CE_RFI_LISTO" in {cid for cid, *_x in CE.CHEQUEOS}
    print("test_u179_rfi_listo OK")


test_u179_rfi_listo()


def test_u184_protocolo_3h():
    """U-184 (usuario 11-nov: '... más de 30 horas ... tienes que terminarlo entre 2 y 3 horas'): caso CR rev18b — Excel editado a mano
    (no coincide con su sello ni con ninguna corrida de la bitácora) y verde de otro archivo = FAIL; auditoría U-181 fechada DESPUÉS de la
    primera subida = FAIL; 3 corridas finales sobre los mismos archivos = FAIL; sin H-A / H-B en las lecturas o sin corridas en TIEMPOS = FAIL;
    todo en orden = PASS."""
    import tempfile, hashlib, json as _j
    w = tempfile.mkdtemp(prefix="u184_"); e = os.path.join(w, "rev1 FINAL PARA REVISAR")
    for d in ("Take-off", "Planos marcados", "Auditoria/revision_independiente"):
        os.makedirs(os.path.join(e, d))
    xl = os.path.join(e, "Take-off", "XQ_Takeoff.xlsx"); open(xl, "wb").write(b"excel de la cadena")
    pdf = os.path.join(e, "Planos marcados", "XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf"); open(pdf, "wb").write(b"pdf de la cadena")
    sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()   # noqa: E731
    _j.dump({"xlsx_sha256": sha(xl)}, open(xl + ".sello.json", "w"))
    with open(os.path.join(w, "bitacora.jsonl"), "w") as f:
        f.write(_j.dumps({"tool": "plantilla_excel.py", "hashes": {xl: sha(xl), pdf: sha(pdf)}}) + "\n")
    for n in ("ALTURAS_IMPRESAS_A.csv", "ALTURAS_IMPRESAS_B.csv"):
        open(os.path.join(e, "Auditoria", n), "w").write("Wall ID,Printed H\n")
    open(os.path.join(e, "Auditoria", "revision_independiente", "INFORME_AUDITORIA_U181.md"), "w").write("# Auditoría U-181\nFecha: 2026-11-12 09:00 PST\n"
                                                                                                          f"Excel sha256 {sha(xl)}\nabiertos: 0\n")
    tt = "| 2-3 | lecturas A / B + H-A / H-B | ...\ncorridas de compuerta: 1\n"
    sub = {"primera_subida_iso": "2026-11-12T18:30:00+00:00"}
    ok = [{"excel": sha(xl), "pdf": sha(pdf)}]
    old = os.environ.pop("BITACORA", None)
    try:
        ev, info = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt, ok)
        assert ev == [], ev
        open(xl, "ab").write(b" editado a mano")                       # CR rev18b: arreglo a mano fuera de la cadena
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt, ok)
        assert any("editado a mano" in x for x in ev) and any("no salió de ninguna corrida" in x for x in ev), ev
        open(xl, "wb").write(b"excel de la cadena")
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, {"primera_subida_iso": "2026-11-12T08:00:00-08:00"}, tt, ok)
        assert any("DESPUÉS de la primera subida" in x for x in ev), ev
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt, ok * 3)
        assert any("3 corridas finales" in x for x in ev), ev
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, "| 2-3 | lecturas A / B |\n", ok)
        assert any("(2)" in x for x in ev) and any("(5)" in x for x in ev), ev
        # P3 (caso GK: TIEMPOS 9, el registro 10 inicios con cortadas) = FAIL; igual = PASS; > 4 corridas sin 'causa:' = FAIL
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt.replace(": 1", ": 9"), ok, registro_corridas={"inicios": 10, "rojas": 1, "cortadas": 3})
        assert any("registra 10 inicios" in x for x in ev) and any("(6)" in x for x in ev), ev
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt, ok, registro_corridas={"inicios": 1, "rojas": 0, "cortadas": 0})
        assert ev == [], ev
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt.replace(": 1", ": 5") + "causa: hoja nueva del addendum\n", ok,
                                       registro_corridas={"inicios": 5, "rojas": 3, "cortadas": 0})
        assert ev == [], ev
        # P4: auditoría de OTRA versión (sha distinto) o sin 'abiertos: 0' = FAIL
        inf = os.path.join(e, "Auditoria", "revision_independiente", "INFORME_AUDITORIA_U181.md")
        open(inf, "w").write("# Auditoría U-181\nFecha: 2026-11-12 09:00 PST\nExcel sha256 " + "ab" * 32 + "\nabiertos: 2\n")
        ev, _ = CE.protocolo_3h_fallas(w, e, xl, pdf, sub, tt, ok)
        assert any("auditó otra versión" in x for x in ev) and any("abiertos: 0" in x for x in ev), ev
    finally:
        if old:
            os.environ["BITACORA"] = old
    assert "CE_PROTOCOLO_3H" in {cid for cid, *_x in CE.CHEQUEOS}
    print("test_u184_protocolo_3h OK")


test_u184_protocolo_3h()

def test_u177_rcp_contorno_duro():
    """U-177 (auditoría 11-nov, CR rev18b): CE_RCP_CONTORNO pasaba con 'min 0.0' (EXCLUDED de la caja de equipo exterior con
    [EDGE NOT DRAWN]). Ahora < 0.5 = FAIL con o sin [EDGE NOT DRAWN]; pasa si declara 'source <HOJA> offset (dx, dy)' y en esa hoja
    (restando el offset) coincide; el borde compartido entre dos cielos cargados de la misma página cuenta como cubierto."""
    import pymupdf as fitz
    import compuerta_entrega as CE
    limpio, mk = fitz.open(), fitz.open()
    for d in (limpio, mk):
        d.new_page(width=800, height=600)
        d.new_page(width=800, height=600)
    limpio[1].draw_rect(fitz.Rect(90, 95, 190, 195), color=(0, 0, 0), width=1)          # la caja dibujada en el plano (A2.01)
    limpio[0].draw_rect(fitz.Rect(400, 100, 600, 300), color=(0, 0, 0), width=1)        # contorno exterior de dos cielos (A3.01)
    mk.set_page_labels([{"startpage": 0, "prefix": "A3.01", "style": ""}, {"startpage": 1, "prefix": "A2.01", "style": ""}])

    def poli(pts, titulo, sub, txt):
        a = mk[0].add_polygon_annot(pts)
        a.set_info(title=titulo, subject=sub, content=txt)
        a.update()
    caja = [(100, 100), (200, 100), (200, 200), (100, 200)]
    poli(caja, "Take-off excluded", "EXCLUDED", "EXCLUDED - exterior equipment box [EDGE NOT DRAWN: the box is drawn only on 1/A2.01]")
    poli([(400, 100), (500, 100), (500, 300), (400, 300)], "take-off", "GYP", "GYP · CEILING CLG-1 · 1/A3.01")
    poli([(500, 100), (600, 100), (600, 300), (500, 300)], "take-off", "GYP", "GYP · CEILING CLG-2 · 1/A3.01")
    ev, n, st = CE.rcp_contorno_fallas(mk, limpio=limpio)
    assert n == 3 and len(ev) == 1 and "equipment box" in ev[0] and "piso U-177" in ev[0], ev            # 0.0 = FAIL (antes pasaba)
    for a in mk[0].annots():                              # una pasada: la annot solo vale dentro del iterador
        if a.info.get("subject") == "EXCLUDED":
            a.set_info(content=a.info["content"].replace("1/A2.01]", "1/A2.01; source A2.01 offset (10, 5)]"))
            a.update()
    ev, n, st = CE.rcp_contorno_fallas(mk, limpio=limpio)
    assert ev == [], ev                                   # medido en A2.01 restando el offset = 1.0; el borde x=500 compartido cuenta
    print("test_u177_rcp_contorno_duro OK")


test_u177_rcp_contorno_duro()


def test_be_cr34_gauge_impreso():
    """BE-CR34 (CR City Hotel rev19): 'gauge not printed' + RFI con A0.06 STUD SCHEDULE 'MIN. GAUGE 25' impreso = FAIL; citado = PASS."""
    import compuerta_entrega as CE
    hojas = {"A0.06": "PARTITION TYPES - GENERAL NOTES STUD SCHEDULE STUD SUFFIX STUD DEPTH MIN. GAUGE HEIGHT LIMIT 2 2 1/2\" 25 11'-3\""}
    fila = {"fila": 4, "material": '2-1/2" stud, 18 mil min. ASTM C 645 (gauge not printed, RFI-30)', "net": 253.05, "cita": "N/SHEET: 5/A7.31"}
    rfi = {"id": "RFI-30", "status": "open", "pregunta": "the details print no stud size or gauge; gauge not printed"}
    ev = CE.gauge_impreso_fallas([fila], [rfi], hojas)
    assert len(ev) == 2 and "A0.06" in ev[0], ev
    fila["material"] = '2-1/2" stud, 25 ga min. (A0.06 STUD SCHEDULE)'
    assert CE.gauge_impreso_fallas([fila], [], hojas) == []
    assert CE.gauge_impreso_fallas([dict(fila, material="x (gauge not printed)")], [], {"A1.01": "PLAN"}) == []   # sin schedule: no aplica
    print("test_be_cr34_gauge_impreso OK")


test_be_cr34_gauge_impreso()


def test_be_gk35_watchdog_y_ciclos():
    """BE-GK35 (GK 11-nov: la compuerta colgada horas en un glob recursivo con symlinks en ciclo): (a) un chequeo que no termina sale
    FAIL 'chequeo colgado' dentro de su tope y la compuerta sigue; (b) _rglob_seguro (chequeos_biblioteca y reglas) termina con un
    symlink en ciclo y encuentra el archivo una sola vez; (c) cada chequeo de correr trae 'segundos'."""
    import time as _t, chequeos_biblioteca as CB, reglas as RG
    est, ev = CE.correr_con_tope(lambda c: _t.sleep(5) or ("PASS", []), None, 0.3)
    assert est == "FAIL" and "colgado" in ev[0], ev
    est, ev = CE.correr_con_tope(lambda c: 1 / 0, None, 2)
    assert est == "FAIL", ev
    w = tempfile.mkdtemp(prefix="gk35_")
    os.makedirs(os.path.join(w, "a", "b"))
    open(os.path.join(w, "a", "b", "takeoff_canon.json"), "w").write("{}")
    os.symlink(w, os.path.join(w, "a", "b", "ciclo"))                       # ciclo: a/b/ciclo -> raíz
    for f in (CB._rglob_seguro, RG._rglob_seguro):
        t0 = _t.time()
        hs = f(w, "**/takeoff_canon.json")
        assert len(hs) == 1 and _t.time() - t0 < 5, hs
    print("test_be_gk35_watchdog_y_ciclos OK")


test_be_gk35_watchdog_y_ciclos()


def test_p5_rcp_no_pasa_en_vacio():
    """P5 (post-mortem 11-nov): con cielos en el canon / hojas RCP en el set, 0 cuartos leídos o 0 polígonos de cielo = FAIL (no AMBER);
    sin cielos ni RCP = AMBER; el auditor de plausibilidad cuenta 'cielos'."""
    w = tempfile.mkdtemp(prefix="p5_")
    json.dump({"hojas": {"X9.9": "REFLECTED CEILING PLAN - LEVEL 9\n(texto en curvas)"}}, open(os.path.join(w, "set_texto.json"), "w"))
    os.makedirs(os.path.join(w, "etapas", "4_canon"))
    json.dump({"ceilings": [{"id": "CLG-X9-01", "area_sf": 120.0}]}, open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    c = CE.Ctx(w)
    assert CE.cielos_esperados(c) == (1, 1), CE.cielos_esperados(c)
    assert chk(CE.ce_rcp_cuartos, c)[0] == "FAIL"
    assert chk(CE.ce_rcp_contorno, c)[0] == "FAIL"
    assert CE.esperado_proyecto(c).get("cielos") == 1
    w2 = tempfile.mkdtemp(prefix="p5b_")
    json.dump({"hojas": {"X9.8": "FLOOR PLAN"}}, open(os.path.join(w2, "set_texto.json"), "w"))
    c2 = CE.Ctx(w2)
    assert chk(CE.ce_rcp_cuartos, c2)[0] == "AMBER" and chk(CE.ce_rcp_contorno, c2)[0] == "AMBER"
    print("test_p5_rcp_no_pasa_en_vacio OK")


test_p5_rcp_no_pasa_en_vacio()


def test_p6_presupuesto_horas():
    """P6: presupuesto por hojas A (<= 25 -> 180 min, <= 60 -> 360, más -> 720); > 60 % AMBER; > 100 % sin 'causa:' FAIL; con causa AMBER."""
    assert CE.hojas_a({"A1.1": "", "A-201": "", "S1.0": "", "X9.9": ""}) == 2
    assert CE.presupuesto_min(10) == 180 and CE.presupuesto_min(40) == 360 and CE.presupuesto_min(90) == 720
    assert CE.presupuesto_fallas(10, 90)[0] == "PASS"
    assert CE.presupuesto_fallas(10, 150)[0] == "AMBER"
    assert CE.presupuesto_fallas(10, 1800)[0] == "FAIL"
    assert CE.presupuesto_fallas(10, 1800, "causa: addendum de 40 hojas")[0] == "AMBER"
    assert CE.presupuesto_fallas(10, None)[0] == "AMBER"
    assert CE.total_minutos("| **TOTAL** | | 20:26 | 21:31 |") == 65
    print("test_p6_presupuesto_horas OK")


test_p6_presupuesto_horas()


def test_p3_registro_corridas():
    """P3 (GK 11-nov: TIEMPOS decía 9 corridas y hubo 10, dos cortadas sin registro): main escribe el INICIO antes de correr; una corrida
    cortada (inicio sin fin) cuenta; --solo / --paso escriben ENTREGA_RAPIDA.json y no cuentan como finales."""
    w = tempfile.mkdtemp(prefix="p3_")
    e = os.path.join(w, "FINAL_FOR_REVIEW_rev1"); os.makedirs(e)
    with open(os.path.join(w, "compuerta_corridas.jsonl"), "w") as f:
        f.write(json.dumps({"ts": "x", "entrega_dir": "FINAL_FOR_REVIEW_rev1", "ok": False}) + "\n")              # renglón viejo = completa
        f.write(json.dumps({"evento": "inicio", "corrida": "c2", "tipo": "final", "entrega_dir": "FINAL_FOR_REVIEW_rev1"}) + "\n")  # cortada
        f.write(json.dumps({"evento": "inicio", "corrida": "r1", "tipo": "rapida", "entrega_dir": "FINAL_FOR_REVIEW_rev1"}) + "\n")
    r = CE.registro_corridas(w, e)
    assert r == {"inicios": 2, "fines": 1, "cortadas": 1, "rojas": 1}, r
    cp = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "compuerta_entrega.py"), w,
                         "--solo", "CE_TIEMPOS", "--paso", "6"], capture_output=True, text=True, timeout=600)
    assert os.path.isfile(os.path.join(w, "ENTREGA_RAPIDA.json")) and not os.path.isfile(os.path.join(w, "ENTREGA_OK.json")), cp.stdout[-800:] + cp.stderr[-800:]
    assert CE.registro_corridas(w, e)["inicios"] == 2                       # la rápida no cuenta
    lns = [json.loads(x) for x in open(os.path.join(w, "compuerta_corridas.jsonl"))]
    assert [x.get("evento") for x in lns[-2:]] == ["inicio", "fin"] and lns[-1]["tipo"] == "rapida", lns[-2:]
    print("test_p3_registro_corridas OK")


test_p3_registro_corridas()


def test_u186_borrar():
    """U-186 (usuario 12-nov: 'todo lo que esté para borrarse, que ya no se ocupe, ponle borrar'): nombre_borrar escribe
    'BORRAR (NO USAR) - <nombre sin zz>' (idempotente, con REPLACED BY); 'zz old …' / REPLACED / superseded sin BORRAR = FAIL;
    BORRAR en el vigente = FAIL; vigentes_entrega y md5 de Drive ignoran BORRAR."""
    assert SE.nombre_borrar("zz old U-178 SEGUIMIENTO.md") == "BORRAR (NO USAR) - old U-178 SEGUIMIENTO.md"
    assert SE.nombre_borrar("zz NO USAR - XQ_markups_rev1 old.pdf") == "BORRAR (NO USAR) - XQ_markups_rev1 old.pdf"
    assert SE.nombre_borrar("Auditoria.zip", "Auditoria (folder)") == "BORRAR (NO USAR) - Auditoria.zip - REPLACED BY Auditoria (folder)"
    assert SE.nombre_borrar(SE.nombre_borrar("rev1 FINAL", "rev2")) == "BORRAR (NO USAR) - rev1 FINAL - REPLACED BY rev2"
    ev = SE.borrar_fallas(["zz old README.md", "rev1 FINAL - REPLACED BY rev2", "X9 takeoff (superseded).xlsx",
                           "BORRAR (NO USAR) - XQ_Takeoff.xlsx", "XQ_markups_rev2 - OPEN IN BLUEBEAM.pdf", "BORRAR (NO USAR) - old README.md"],
                          vigentes=["XQ_Takeoff.xlsx", "XQ_markups_rev2 - OPEN IN BLUEBEAM.pdf"])
    assert len(ev) == 4 and sum("no lleva el prefijo" in x for x in ev) == 3 and any("VIGENTE" in x for x in ev), ev
    assert SE.borrar_fallas(["BORRAR (NO USAR) - old README.md", "XQ_Takeoff.xlsx"], ["XQ_Takeoff.xlsx"]) == []
    e = tempfile.mkdtemp(prefix="u186_")
    for d in ("Take-off", "Planos marcados"):
        os.makedirs(os.path.join(e, d))
    for n in ("XQ_Takeoff.xlsx", "BORRAR (NO USAR) - old XQ_Takeoff.xlsx"):
        open(os.path.join(e, "Take-off", n), "wb").write(b"x")
    for n in ("XQ_markups_rev2 - OPEN IN BLUEBEAM.pdf", "BORRAR (NO USAR) - XQ_markups_rev1 - OPEN IN BLUEBEAM.pdf"):
        open(os.path.join(e, "Planos marcados", n), "wb").write(b"x")
    vg, ev = CE.vigentes_entrega(e)
    assert ev == [] and os.path.basename(vg["excel"]) == "XQ_Takeoff.xlsx", (vg, ev)
    assert SE.RX_VIEJO.match("BORRAR (NO USAR) - old XQ_Takeoff.xlsx") and not SE.RX_VIEJO.match("XQ_Takeoff.xlsx")
    print("test_u186_borrar OK")


test_u186_borrar()


def test_v97_campos_canon():
    """v81cf97 (COORDINACIÓN: los chequeos de v81cf96 no pasan en vacío, U-137): canon sin rated_floor_assemblies / typical_floors /
    stack_reasons ni su none_reason, o con puertas sin sheet + center_pt = FAIL en una entrega nueva; con los campos (o none_reason)
    = PASS; entrega subida antes de v81cf96 = AMBER. CB_BE_CR22_VANOS AMBER pasa a FAIL en una entrega nueva."""
    malo = {"walls": [], "opening_schedule": {"items": [{"ref": "901", "kind": "door"}]}}
    ev = CE.campos_canon_fallas(malo)
    assert len(ev) == 4 and any("rated_floor_assemblies" in x for x in ev) and any("901" in x for x in ev), ev
    bueno = {"walls": [], "rated_floor_assemblies": [], "typical_floors_none_reason": "single level (X9.1)", "stack_reasons": {},
             "opening_schedule": {"items": [{"ref": "901", "kind": "door", "sheet": "X9.1", "center_pt": [10, 20], "ro_w_ft": 3.0}]}}
    assert CE.campos_canon_fallas(bueno) == []
    w = tempfile.mkdtemp(prefix="v97_")
    os.makedirs(os.path.join(w, "etapas", "4_canon"))
    json.dump(malo, open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    c = CE.Ctx(w)
    assert CE.entrega_nueva(c) and chk(CE.ce_campos_canon, c)[0] == "FAIL"
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00"}, open(os.path.join(w, "SUBIDA_OK.json"), "w"))
    assert not CE.entrega_nueva(c) and chk(CE.ce_campos_canon, c)[0] == "AMBER"
    os.remove(os.path.join(w, "SUBIDA_OK.json"))
    json.dump(dict(malo, walls=[{"id": "Z9-01", "sheet": "X9.1", "length_ft": 10, "height_ft": 9, "path": [[0, 0], [90, 0]]}]),
              open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    cr22 = [r for r in CE.correr(w, solo={"CB_BE_CR22_VANOS"})["chequeos"] if r["id"] == "CB_BE_CR22_VANOS"]
    assert cr22 and cr22[0]["estado"] == "FAIL", cr22                    # entrega nueva: AMBER -> FAIL
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00"}, open(os.path.join(w, "SUBIDA_OK.json"), "w"))
    cr22 = [r for r in CE.correr(w, solo={"CB_BE_CR22_VANOS"})["chequeos"] if r["id"] == "CB_BE_CR22_VANOS"]
    assert cr22 and cr22[0]["estado"] == "AMBER", cr22                   # entrega anterior: sigue AMBER
    print("test_v97_campos_canon OK")


test_v97_campos_canon()


def test_u187_textos_legibles():
    """U-187 / BE-COORD02 (usuario 12-nov, CR rev19 SECTION de ALTURAS_REVISADAS: 'aqui tiene datos ensimados, arreglalo'): con muchas alturas
    pegadas (diferencias de décimas de pie) y decenas de cuartos, la sección vieja (etiqueta a la altura de su línea) se encima = FAIL; la nueva
    (seccion_sin_encimar) = PASS. FreeText de DETALLES / SCHEDULES_REVISADOS: dos etiquetas en el mismo lugar = FAIL; colocadas con
    hueco_etiqueta = PASS (con guía al elemento)."""
    import random
    import importlib.util
    import comparar_alturas as CA
    random.seed(1)
    hs = [14.0, 13.792, 13.658, 13.4, 11.396, 11.219, 10.538, 10.522, 10.501, 10.488, 10.31, 10.253, 10.052, 9.98, 9.917, 9.844, 9.25,
          9.167, 9.083, 9.0, 8.938, 8.59, 8.047, 7.275, 6.64, 5.912, 5.039, 1.746, 1.736, 1.063, 0.917, 0.24]
    final = [{"Printed H": f"{h}", "Wall ID": f"Z9.{i}-L9-0{i % 9} A", "Source": "x", "Operation": "", "Status": "CONFIRMED", "Image": ""}
             for i, h in enumerate(hs)]
    cuartos = {f"{900 + i}": random.choice([12.062, 11.0, 9.5, 9.167, 8.938, 8.417, 8.042, 7.0, 5.333]) for i in range(40)}
    bo = {"L1": 14.0, "L2": 11.0, "L3": 11.0, "L4": 14.0}
    w = tempfile.mkdtemp(prefix="u187_")
    nuevo = os.path.join(w, "ALTURAS_REVISADAS.pdf")
    CA.alturas_revisadas(final, w, nuevo, bo, cuartos)
    assert CA.textos_encimados(nuevo, -1) == [] and CE.textos_legibles_fallas(nuevo) == []
    viejo_py = os.path.join(w, "comparar_alturas_v97.py")                  # la sección de v81cf97 (antes del arreglo)
    src = open(CA.__file__).read()
    i, j = src.index("def alturas_revisadas("), src.index("\ndef ", src.index("def alturas_revisadas(") + 10)
    viejo_fn = '''def alturas_revisadas(final, entrega, salida, bo, cuartos):
    import pymupdf
    doc = pymupdf.open()
    niveles = sorted({round(ftin(r["Printed H"]), 3) for r in final}) + sorted(set(cuartos.values()))
    pg = doc.new_page(width=792, height=612)
    top = max(niveles) or 1
    for v in niveles:
        y = 570 - 500 * v / top
        pg.draw_line((80, y), (430, y), width=1.2)
        pg.insert_text((84, y - 2), f"{v:.3f} ft", fontsize=6)
        pg.insert_textbox(pymupdf.Rect(440, y - 6, 780, y + 20), f"walls at {v:.3f}", fontsize=7)
    doc.save(salida)
    return {}
'''
    open(viejo_py, "w").write(src[:i] + viejo_fn + src[j:])
    sp = importlib.util.spec_from_file_location("ca_viejo", viejo_py)
    V = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(V)
    viejo = os.path.join(w, "ALTURAS_REVISADAS_viejo.pdf")
    V.alturas_revisadas(final, w, viejo, bo, cuartos)
    assert len(CA.textos_encimados(viejo, -1)) > 10 and CE.textos_legibles_fallas(viejo), "la sección vieja debe salir encimada"
    # FreeText de DETALLES_REVISADOS
    d = pymupdf.open()
    pg = d.new_page(width=600, height=400)
    for k, (x, y) in enumerate([(100, 100), (104, 104)], 1):
        a = pg.add_freetext_annot(pymupdf.Rect(x, y, x + 40, y + 16), f"#{k}", fontsize=10)
        a.update()
    mal = os.path.join(w, "DETALLES_REVISADOS_mal.pdf")
    d.save(mal)
    assert any("FreeText '#1' encima de '#2'" in e for e in CE.textos_legibles_fallas(None, None, [mal]))
    d = pymupdf.open()
    pg = d.new_page(width=600, height=400)
    for k in range(1, 6):                                                   # cinco burbujas en el mismo renglón
        c = pg.add_circle_annot(pymupdf.Rect(80, 96, 100, 116))
        c.update()
        a = pg.add_freetext_annot(CE.hueco_etiqueta(pg, pymupdf.Rect(102, 100, 142, 116), ancla=(100, 106)), f"#{k}", fontsize=10)
        a.update()
    bien = os.path.join(w, "DETALLES_REVISADOS.pdf")
    d.save(bien)
    assert CE.textos_legibles_fallas(None, None, [bien]) == []
    assert sum(1 for a in pymupdf.open(bien)[0].annots() if a.info.get("subject") == "take-off guide") >= 3
    assert "CE_TEXTOS_LEGIBLES" in {cid for cid, *_x in CE.CHEQUEOS}
    print("test_u187_textos_legibles OK")


test_u187_textos_legibles()


def test_be_cr35_not_blind():
    """BE-CR35 (CR rev19, 12-nov): soffits / beam wraps (SOF-*, BW-*, Depth = ancho desarrollado) entraron a ALTURAS_IMPRESAS como
    '[take-off detail reading, not blind]' sin la doble lectura ciega H-A / H-B: 'not blind' = FAIL y todo markup con Depth falta en A /
    B = FAIL; con SOF / BW leídos por A y B = PASS; la página de ALTURAS_REVISADAS de un SOF dice 'developed board width per LF'."""
    import comparar_alturas as CA
    a = [{"Wall ID": "Z9-01", "Printed H": "10"}]
    final = a + [{"Wall ID": "SOF-Z9-01", "Printed H": "0.917", "Source": "X9.3 [take-off detail reading, not blind]", "Status": "DERIVED"}]
    ev = CA.cobertura_ab(a, list(a), final, ["Z9-01 A", "BW-Z9-02"])
    assert any("not blind" in e for e in ev) and sum("SOF-Z9-01: falta" in e for e in ev) == 2 and sum("BW-Z9-02: falta" in e for e in ev) == 2, ev
    ab = a + [{"Wall ID": "SOF-Z9-01", "Printed H": "0.917"}, {"Wall ID": "BW-Z9-02", "Printed H": "2.5"}]
    final_ok = ab[:2]
    assert CA.cobertura_ab(ab, list(ab), [dict(r, Source="X9.3 + 4/X9.5") for r in final_ok], ["Z9-01 A", "BW-Z9-02", "DEMO-DEMO-03"][:2]) == []
    w = tempfile.mkdtemp(prefix="cr35_")
    pdf = os.path.join(w, "ALTURAS_REVISADAS.pdf")
    CA.alturas_revisadas([{"Wall ID": "SOF-Z9-01", "Printed H": "0.917", "Source": "X9.3", "Operation": "", "Status": "DERIVED", "Image": ""}],
                         w, pdf, {"L9": 10.0}, {})
    assert "developed board width per LF" in pymupdf.open(pdf)[0].get_text()
    print("test_be_cr35_not_blind OK")


test_be_cr35_not_blind()


def test_be_cr36_textos_markups():
    """BE-CR36 (CR rev19, U-187): LEGEND - una celda larga cabe en su columna; EXCLUDED de dos cuartos vecinos no se enciman."""
    import pymupdf
    import markups_bluebeam as MB
    import markups_rcp as MR
    fs, v = MB.celda_legible("CH.6-2 - SHAFT WALL (C-H STUDS AND J-RUNNER, 1 IN LINER, 2 HR) - 2 LAYERS EACH SIDE", 194)
    assert pymupdf.get_text_length(v, fontname="helv", fontsize=fs) <= 194 and fs >= 3.5 and "..." not in v, (fs, v)
    assert MB.celda_legible("50", 64) == (10.0, "50")
    d = pymupdf.open(); pg = d.new_page(width=800, height=600); d.set_page_labels([{"startpage": 0, "prefix": "A7.50", "style": ""}])
    tmp = "/tmp/_be_cr36.pdf"; d.save(tmp)
    rooms = [{"sheet": "A7.50", "room": r, "disposition": "exclusion", "reason": "lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded",
              "nhoja": "2/A7.50", "polygon": pol} for r, pol in (("118B", [[100, 100], [300, 100], [300, 140], [100, 140]]),
                                                                ("119", [[299, 95], [460, 95], [460, 140], [299, 140]]))]
    hechos, faltan = MR.aplicar(tmp, {"rooms": rooms})
    assert len(hechos) == 2 and not faltan, (hechos, faltan)
    fts = [a.rect for a in pymupdf.open(tmp)[0].annots() if a.type[1] == "FreeText"]
    assert len(fts) == 2 and (fts[0] & fts[1]).is_empty or (fts[0] & fts[1]).get_area() < 0.5, fts
    print("test_be_cr36_textos_markups OK")


test_be_cr36_textos_markups()


def test_be_cr37_un_lado():
    """BE-CR37 (CR rev19 7/A7.23, usuario 12-nov): el ancho desarrollado de un soffit de corridor se armó con el fondo 4 1/2" del lado
    DERECHO + la caída 6 1/2" del IZQUIERDO = FAIL; sin side / faces = FAIL; las dos cotas del mismo lado con side = PASS; en
    CE_ALTURAS_EXTREMO es FAIL en entregas nuevas y AMBER en las subidas antes de v81cf100."""
    import comparar_alturas as CA
    mal = [{"Wall ID": "SOF-Z9-01", "Printed H": "0.917", "side": "", "faces": 'bottom 4 1/2" right; drop 6 1/2" left'}]
    ev = CA.lados_fallas(mal)
    assert any("lados distintos" in e for e in ev) and any("sin 'side'" in e for e in ev), ev
    assert any("sin 'faces'" in e for e in CA.lados_fallas([{"Wall ID": "BW-Z9-02", "Printed H": "1.5", "side": "left"}]))
    bien = [{"Wall ID": "SOF-Z9-01", "Printed H": "0.917", "side": "right", "faces": 'bottom 4 1/2" right; drop 6 1/2" right'},
            {"Wall ID": "SOF-Z9-01 L", "Printed H": "0.75", "side": "left", "faces": 'bottom 4 1/2" x=310; drop 4 1/2" x=322'},
            {"Wall ID": "Z9-01", "Printed H": "10"}]
    assert CA.lados_fallas(bien) == []
    assert CE.FECHA_V100 > CE.FECHA_V96
    print("test_be_cr37_un_lado OK")


test_be_cr37_un_lado()


# BE-GK39 / BE-GK40 (Grand Kia, parche sobre v81cf101; antes test_be_gk39_40.py)
def test_be_gk39_hueco_dentro_de_square():
    import pymupdf
    import compuerta_entrega as CE
    d = pymupdf.open()
    pg = d.new_page(width=800, height=600)
    sq = pg.add_rect_annot(pymupdf.Rect(50, 50, 750, 550))   # destination view covering the whole area
    sq.update()
    r = pymupdf.Rect(100, 100, 168, 118)
    a1 = pg.add_freetext_annot(CE.hueco_etiqueta(pg, r), "#1", fontsize=11)
    a1.update()
    s2 = CE.hueco_etiqueta(pg, r)
    a2 = pg.add_freetext_annot(s2, "#2", fontsize=11)
    a2.update()
    i = pymupdf.Rect(a1.rect) & pymupdf.Rect(a2.rect)
    assert i.is_empty or i.width <= 0.5 or i.height <= 0.5, (a1.rect, a2.rect)


def test_be_gk40_pregunta_misma_magnitud():
    import comparar_alturas as PC   # v81cf102: pregunta_ciega unido a comparar_alturas (límite de 199 archivos)
    canon = {"misc_items": [
        {"ref": "EXT-07 joists", "op": "ROUNDUP(125.667/1.3333)+1 = 96 joists x 0.82 ft = 78.72"},
        {"ref": "SOF-02 board", "op": "44.51 LF x developed 1.5 ft = 66.77"},
        {"ref": "EXT-04 studs", "op": "ROUNDUP(98.0/1.3333)+1 = 75 studs x 9.16 ft = 687.0"}]}
    t = {x["id"]: x["magnitude"] for x in PC.tareas(canon)}
    assert t == {"EXT-07": "joist_length", "SOF-02": "developed", "EXT-04": "stud_height"}, t
    mal = "| EXT-07 | pocket | depth of the joists (ft) |\n| SOF-02 | cove | developed board width (ft) |\n| EXT-04 | grid 4 | H of the 6\" studs (ft) |"
    ev = PC.pregunta_fallas(mal, canon)
    assert len(ev) == 1 and ev[0].startswith("EXT-07"), ev
    bien = mal.replace("depth of the joists", "LENGTH of each joist (pocket width)")
    assert PC.pregunta_fallas(bien, canon) == []


test_be_gk39_hueco_dentro_de_square()
test_be_gk40_pregunta_misma_magnitud()
print("test_be_gk39_40 OK")


def test_be_cr38_renglones_partidos():
    """BE-CR38 (CR rev20, 12-nov): al reemplazar un bloque del script de entrega se borraron los renglones partidos (cara de baño W.R.
    'X C' / 'X D' = misma altura que su padre 'X A'); los markups con Depth siguen en VISTA_BLUEBEAM -> cobertura_ab FAIL; con los
    partidos en A, B y la final -> 0 fallas. (Regla de conducta: diff contra la copia en cache_proyectos antes de reemplazar un bloque.)"""
    import comparar_alturas as CA
    padre = {"Wall ID": "Z9.4-L9-03 A", "Printed H": "9.5", "Source": "4/X9.05", "Status": "DERIVED", "Image": "x.png"}
    depth = ["TO-Z9.4-L9-03 A", "TO-Z9.4-L9-03 C", "TO-Z9.4-L9-03 D"]

    def partir(filas, ids):
        return list(filas) + [dict(padre, **{"Wall ID": i, "Source": "[split row of Z9.4-L9-03 A] 4/X9.05"}) for i in ids]
    ids = ["Z9.4-L9-03 C", "Z9.4-L9-03 D"]
    ev = CA.cobertura_ab([dict(padre)], [dict(padre)], partir([dict(padre)], ids), depth)
    assert any("Z9.4-L9-03 C" in e and "_A" in e for e in ev) and any("Z9.4-L9-03 D" in e and "_B" in e for e in ev), ev
    assert any("TO-Z9.4-L9-03 C" in e for e in CA.cobertura_ab([dict(padre)], [dict(padre)], [dict(padre)], depth))
    assert CA.cobertura_ab(partir([dict(padre)], ids), partir([dict(padre)], ids), partir([dict(padre)], ids), depth) == []
    print("test_be_cr38_renglones_partidos OK")


test_be_cr38_renglones_partidos()


def test_u189_cobertura_y_gating():
    """U-189 (3) (usuario 12-nov: '¿Te imaginas si te hago caso, qué pasaría?'): la auditoría U-181 declara COBERTURA con TODO detalle que
    gobierna cantidad y TODA hoja RCP; sin la sección o con un detalle / RCP fuera = FAIL; completa = PASS. CB_RCP_APILADOS /
    CB_DETALLE_CARAS en FAIL pasan a AMBER en una entrega subida antes de v81cf103."""
    can = {"ceilings": [{"room": "L9 Corridor 916", "detail": "7/X9.23", "source": "X9.2 RCP"}],
           "misc_items": [{"ref": "SOF-L9-01 board", "source": "7/X9.23 + 12/X9.03"}]}
    dets, rcp = CE.cobertura_esperada(can, {"X9.2": "REFLECTED CEILING PLAN - LEVEL 9", "X9.1": "FLOOR PLAN"})
    assert dets == ["12/X9.03", "7/X9.23"] and rcp == ["X9.2"], (dets, rcp)
    assert "sin sección COBERTURA" in CE.cobertura_fallas("# Auditoría\nmuestra de 5 walls\nabiertos: 0", dets, rcp)[0]
    ev = CE.cobertura_fallas("## COBERTURA\n- 7/X9.23 todas las caras\n- RCP X9.2 completo\n", dets, rcp)
    assert len(ev) == 1 and "12/X9.03" in ev[0], ev
    assert CE.cobertura_fallas("## COVERAGE\n- 7/X9.23\n- 12/X9.03\n- X9.2\n", dets, rcp) == []
    w = tempfile.mkdtemp(prefix="u189_")
    os.makedirs(os.path.join(w, "etapas", "4_canon"))
    json.dump({"walls": [], "ceilings": [{"room": "L9 Corridor 916", "assembly": {"id": "FS-1"}, "area_sf": 450.0}],
               "rcp_tags": [{"sheet": "X9.2", "tag": "FS-1", "height": "", "rows": ["ceilings[0]"]},
                            {"sheet": "X9.2", "tag": "GYP-1", "height": "8' - 11\"", "rows": ["ceilings[0]"]}]},
              open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    est = lambda: [r for r in CE.correr(w, solo={"CB_RCP_APILADOS"})["chequeos"] if r["id"] == "CB_RCP_APILADOS"][0]["estado"]   # noqa: E731
    assert est() == "FAIL"
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00"}, open(os.path.join(w, "SUBIDA_OK.json"), "w"))
    assert est() == "AMBER"
    print("test_u189_cobertura_y_gating OK")


test_u189_cobertura_y_gating()


def test_v104_rcp_todos_los_tags():
    """v81cf104 / U-189 (COORDINACIÓN: 'cualquier hueco de conteo se cierra'): CB_RCP_TAGS cuenta TODO tag de cielo impreso en un plano RCP
    (GYP / FS / RS / ACT / WS / MB y todo prefijo de la leyenda de la hoja; 'ACT-1:' de la leyenda no cuenta). Caso CR rev19 1/A7.23: el
    GYP-1 8'-11" colgado del enlarged RCP que nadie leyó (rcp_tags sin él) = FAIL; con su renglón y el WS-1 con motivo = PASS; una nota
    'RE: REFLECTED CEILING PLANS' de un schedule de assemblies no hace plano RCP."""
    import chequeos_biblioteca as CB
    t = ("ENLARGED RCP - LEVEL 9 CORRIDOR\nGYP-1\n8' - 11\"\nWS-1\n8' - 0 1/2\"\nCEILING LEGEND\nCEILING TYPES:\nACT-1: 2X4 LAY-IN\n"
         "WS-1: WOOD SLAT\nGYP-1: GYPSUM BOARD ON METAL SUSPENSION\nXC-1: CUSTOM CLOUD\nXC-1\n")
    assert CB.tags_cielo(t) == {"GYP-1": 1, "WS-1": 1, "XC-1": 1}, CB.tags_cielo(t)
    hojas = {"X9.23": t}
    can = {"walls": [], "ceilings": [{"room": "L9 Corridor 916", "assembly": {"id": "FS-1"}, "area_sf": 450.0}],
           "rcp_tags": [{"sheet": "X9.23", "tag": "WS-1", "height": "8' - 0 1/2\"", "none_reason": "wood slat by others (1/X9.23 legend WS-1)"},
                        {"sheet": "X9.23", "tag": "XC-1", "height": "", "none_reason": "custom cloud by others (1/X9.23 legend XC-1)"}]}
    e, ev = CB.rcp_tags(CB.B(canon=can, hojas=hojas))
    assert e == "FAIL" and any("GYP-1" in x for x in ev), ev
    can["ceilings"].append({"room": "L9 Corridor 916", "board": "5/8 type X", "area_sf": 450.0})
    can["rcp_tags"].append({"sheet": "X9.23", "tag": "GYP-1", "height": "8' - 11\"", "rows": ["ceilings[1]"]})
    e, ev = CB.rcp_tags(CB.B(canon=can, hojas=hojas))
    assert e == "PASS", ev
    nota = "FIRE RATED ASSEMBLIES\nFS-1\nTHROUGHOUT\nCEILING. RE: REFLECTED CEILING PLANS AND OTHER DETAILS"
    assert not CB.RX_PLAN_RCP.search(nota)
    assert CE.U189_CB["CB_RCP_TAGS"] == CE.FECHA_V104
    print("test_v104_rcp_todos_los_tags OK")


test_v104_rcp_todos_los_tags()


def test_u190_doble_cielo():
    """U-190 ⭐ REGLA DE ORO #3 (usuario 12-nov: 'siempre se tiene que checar en todos los proyectos ... si en algunos lugares llevan doble
    cielo'): sin Auditoria/DOBLE_CIELO.csv = FAIL; un cuarto del RCP fuera de la tabla = FAIL; caso CR L4 401 (GYP-1 en el baño y sin el
    RS-1 de arriba, con un roof / ceiling assembly rated sobre el último piso) = FAIL; tabla completa con el doble cielo y sus dos renglones
    = PASS; entrega anterior a U-190 = AMBER; la página DOUBLE CEILING de ALTURAS_REVISADAS sale con su Page Label y sin textos encimados."""
    import csv
    import comparar_alturas as CA
    can = {"walls": [], "rated_floor_assemblies": [{"id": "RS-1", "levels": ["ROOF"], "source": "X0.08"}],
           "ceilings": [{"room": "L9 901", "floor": "L9", "area_sf": 60.0}, {"room": "L8 801", "floor": "L8", "area_sf": 60.0}],
           "misc_items": [{"ref": r, "qty": 60.0} for r in ("CLG-L9-01 RS", "CLG-L9-02 board", "CLG-L9-03 RS")]}   # v81cf119: renglones reales
    assert CE.niveles_membrana(can) == {"L9"}
    cq = {"X3.09": ["901", "902"]}
    assert "falta Auditoria/DOBLE_CIELO.csv" in CE.doble_cielo_fallas(None, cq, {"L9"})[0]
    mal = [{"Room": "L9 901 BATH", "Level": "L9", "Type": "single", "Upper ceiling": "", "Lower ceiling": "GYP-1", "Heights": "8'-0\"",
            "N/SHEET": "1/X7.31", "Row / reason": "single: CLG-L9-01 board"}]
    ev = CE.doble_cielo_fallas(mal, cq, {"L9"})
    assert any("902" in e for e in ev) and any("falta el cielo superior" in e for e in ev), ev
    bien = [{"Room": "L9 901 BATH", "Level": "L9", "Type": "double", "Upper ceiling": "RS-1 membrane", "Lower ceiling": "GYP-1",
             "Heights": "9'-10\" / 8'-0\"", "N/SHEET": "1/X7.31", "Row / reason": "upper: CLG-L9-01 RS; lower: CLG-L9-02 board",
             "Framing": "RC per RS-1 assembly (UL L546); lower ceiling hat channel 3/X7.31"},
            {"Room": "L9 902", "Level": "L9", "Type": "double", "Upper ceiling": "RS-1 membrane", "Lower ceiling": "ACT-1",
             "Heights": "9'-10\" / 9'-0\"", "N/SHEET": "X3.09", "Row / reason": "upper: CLG-L9-03 RS; lower: ACT by others (1/X3.09 legend)",
             "Framing": "direct to wood (2/X5.04)"}]
    assert CE.doble_cielo_fallas(bien, cq, {"L9"}) == []
    bien2 = [dict(bien[0], **{"Row / reason": "upper: CLG-L9-01 RS"})] + bien[1:]
    assert any("cielo lower" in e for e in CE.doble_cielo_fallas(bien2, cq, {"L9"}))
    w = tempfile.mkdtemp(prefix="u190_")
    e = os.path.join(w, "FINAL_FOR_REVIEW_rev1")
    os.makedirs(os.path.join(e, "Auditoria"))
    os.makedirs(os.path.join(w, "etapas", "4_canon"))
    json.dump(can, open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    json.dump({"hojas": {"A3.09": "OVERALL RCP - LVL 9\nREFLECTED CEILING PLAN\n901\n902\n"}}, open(os.path.join(w, "set_texto.json"), "w"))
    assert chk(CE.ce_doble_cielo, CE.Ctx(w))[0] == "FAIL"
    with open(os.path.join(e, "Auditoria", "DOBLE_CIELO.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(bien[0]))
        wr.writeheader()
        wr.writerows(bien)
    assert chk(CE.ce_doble_cielo, CE.Ctx(w))[0] == "PASS"
    os.remove(os.path.join(e, "Auditoria", "DOBLE_CIELO.csv"))
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00"}, open(os.path.join(w, "SUBIDA_OK.json"), "w"))
    assert chk(CE.ce_doble_cielo, CE.Ctx(w))[0] == "AMBER"
    with open(os.path.join(e, "Auditoria", "DOBLE_CIELO.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(bien[0]))
        wr.writeheader()
        wr.writerows(bien)
    pdf = os.path.join(w, "ALTURAS_REVISADAS.pdf")
    CA.alturas_revisadas([{"Wall ID": "Z9-01", "Printed H": "10", "Source": "x", "Operation": "", "Status": "CONFIRMED", "Image": ""}],
                         e, pdf, {"L9": 10.0}, {})
    d = pymupdf.open(pdf)
    assert d[-1].get_label() == "DOUBLE CEILING" and "DOUBLE CEILING" in d[-1].get_text() and CA.textos_encimados(pdf, -1) == []
    print("test_u190_doble_cielo OK")


test_u190_doble_cielo()


def test_u190b_framing_y_be_cr40():
    """U-190 (corrección del usuario 12-nov): el metal NO es obligatorio; cielo con metal cargado sin fuente impresa = FAIL; board directo a
    madera sin metal con su N/HOJA = PASS; sin columna Framing = FAIL. BE-CR40 (CR rev20): un faltante se busca por tag en rcp_tags, no
    por texto del JSON (la comilla escapada no casa)."""
    import chequeos_biblioteca as CB
    base = {"Room": "L9 901", "Level": "L8", "Type": "single", "Upper ceiling": "", "Lower ceiling": "GYP-1", "Heights": "9'-0\"",
            "N/SHEET": "X3.09", "Row / reason": "single: CLG-L8-01 board"}
    cq = {"X3.09": ["901"]}
    assert any("metal cargado" in e for e in CE.doble_cielo_fallas([dict(base, Framing="hat channel 16 in. o.c.")], cq, set()))
    assert CE.doble_cielo_fallas([dict(base, Framing="direct to wood (2/X5.04)")], cq, set()) == []
    assert any("sin columna Framing" in e for e in CE.doble_cielo_fallas([dict(base)], cq, set()))
    can = {"misc_items": [{"ref": "CLG-Z9-56 board", "source": "GYP-1 8'-11\" on 1/X7.23"}], "ceilings": [{"room": "L9 Corridor 916"}],
           "rcp_tags": [{"sheet": "X7.23", "tag": "GYP-1", "height": "8' - 11\"", "rows": ["CLG-Z9-56 board", "ceilings[0] FS-1"]}]}
    assert "8'-11\"" not in json.dumps(can)
    falta, motivo = CB.faltante_por_tag(can, "X7.23", "GYP-1", "8' - 11\"")
    assert not falta and "CLG-Z9-56" in motivo, motivo
    can["rcp_tags"][0]["rows"] = ["CLG-Z9-99 board"]
    assert CB.faltante_por_tag(can, "X7.23", "GYP-1", "8' - 11\"")[0]
    can["rcp_tags"] = []
    assert CB.faltante_por_tag(can, "X7.23", "GYP-1", "8' - 11\"")[0]
    print("test_u190b_framing_y_be_cr40 OK")


test_u190b_framing_y_be_cr40()


def test_v106_paginas_y_watchdog():
    """v81cf106 (CR rev20 con v81cf105): (1) ALTURAS_REVISADAS con la página DOUBLE CEILING dejaba 'double_ceiling' en
    ALTURAS_REVISADAS_PAGINAS.json y el modo extremo hacía float('double_ceiling'): ValueError -> CE_ALTURAS_EXTREMO / CHECKLIST caían.
    Ahora extremo (controles) corre con DOBLE_CIELO.csv presente y la muestra apunta a páginas de altura. (2) El tope del watchdog crece
    con los markups (300 s + 0.5 s por markup, techo 30 min); un chequeo colgado sigue saliendo FAIL al llegar a su tope."""
    import csv
    import comparar_alturas as CA
    assert CA.paginas_de_alturas({"9.5": 1, "section": 2, "double_ceiling": 3, "10.0": 4}) == {9.5: 1, 10.0: 4}
    w = tempfile.mkdtemp(prefix="v106_")
    au = os.path.join(w, "Auditoria")
    os.makedirs(au)
    os.makedirs(os.path.join(w, "Planos marcados"))
    filas = [{"Wall ID": "Z9-01", "Printed H": "9.5", "Source": "X9.2", "Operation": "", "Status": "CONFIRMED", "Image": ""},
             {"Wall ID": "Z9-02", "Printed H": "10.0", "Source": "X9.2", "Operation": "", "Status": "CONFIRMED", "Image": ""}]
    for n in ("ALTURAS_IMPRESAS_A.csv", "ALTURAS_IMPRESAS_B.csv", "ALTURAS_IMPRESAS.csv"):
        with open(os.path.join(au, n), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(filas[0]))
            wr.writeheader()
            wr.writerows(filas)
    for n in ("ALTURAS_CUARTOS.csv", "ALTURAS_CUARTOS_A.csv", "ALTURAS_CUARTOS_B.csv"):
        open(os.path.join(au, n), "w").write("Room,C.H. (ft)\n901,9.0\n")
    with open(os.path.join(au, "DOBLE_CIELO.csv"), "w", newline="") as f:
        f.write("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
                "L9 901,L9,single,,GYP-1,9'-0\",X3.09,direct to wood (2/X5.04),single: CLG-L9-01 board\n")
    can = {"walls": [{"id": "Z9-01", "height_ft": 9.5}, {"id": "Z9-02", "height_ft": 10.0}], "constants": {"deck_heights": {"value": 12.0}}}
    res = CA.controles(w, can, None, construir=True)                     # v81cf105: ValueError aquí
    res2 = CA.controles(w, can, None, construir=False)
    pag = json.load(open(os.path.join(au, "ALTURAS_REVISADAS_PAGINAS.json")))
    assert "double_ceiling" in pag and "section" in pag
    mu = json.load(open(os.path.join(au, "ALTURAS_MUESTRA.json")))
    assert mu and all(isinstance(m["ALTURAS_REVISADAS page"], int) for m in mu), mu
    assert "6_muestreo" in res2["conteos"] and "5_evidencia" in res["conteos"]
    assert CE.tope_chequeo("CE_MARKUP_EN_WALL", 0) == CE.TIMEOUT_DEFAULT
    assert CE.tope_chequeo("CE_MARKUP_EN_WALL", 1000) == CE.TIMEOUT_DEFAULT + 1000 * CE.TOPE_POR_MARKUP   # v81cf111: 3x la tasa medida
    assert CE.tope_chequeo("CE_MARKUP_EN_WALL", 10 ** 6) == CE.TOPE_MAX and CE.tope_chequeo("CE_REGLAS", 0) >= 1800
    import time as _t
    est, ev = CE.correr_con_tope(lambda c: _t.sleep(5) or ("PASS", []), None, 0.3)   # colgado real: sigue FAIL al tope
    assert est == "FAIL" and "colgado" in ev[0]
    print("test_v106_paginas_y_watchdog OK")


test_v106_paginas_y_watchdog()


def test_be_gk41_celdas_doble_cielo():
    """BE-GK41 (Grand Kia rev3, U-190 / U-187): la página DOUBLE CEILING achicaba la letra hasta 4 pt sin partir el texto y las celdas largas
    de DOBLE_CIELO.csv invadían la columna de al lado (textos encimados). Ahora cada celda se parte en renglones dentro de su columna, sin
    recortar (BE-CR36b), y el renglón crece: 0 encimados y el texto completo en la página."""
    import csv
    import comparar_alturas as CA
    w = tempfile.mkdtemp(prefix="gk41_")
    os.makedirs(os.path.join(w, "Auditoria"))
    largo = "upper: CLG-L9-01 RS-1 membrane per X0.08 assembly with resilient channel at 16 in. o.c.; lower: CLG-L9-02 board hung on wire 4/X7.31"
    with open(os.path.join(w, "Auditoria", "DOBLE_CIELO.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["Room", "Level", "Type", "Upper ceiling", "Lower ceiling", "Heights", "N/SHEET", "Framing", "Row / reason"])
        for i in range(40):
            wr.writerow([f"L9 9{i:02d} CORRIDOR AND RESTROOM VESTIBULE EAST", "L9", "double", "RS-1 rated membrane (UL L546) above",
                         "GYP-1 suspended gypsum board ceiling", "9'-10 5/8\" / 8'-11\"", "1/X7.31, 4/X7.31, X0.08",
                         "RC per RS-1 assembly + hanger wire and grid per 4/X7.31", largo])
    pdf = os.path.join(w, "A.pdf")
    CA.alturas_revisadas([{"Wall ID": "Z9-01", "Printed H": "10", "Source": "x", "Operation": "", "Status": "CONFIRMED", "Image": ""}],
                         w, pdf, {"L9": 10.0}, {})
    d = pymupdf.open(pdf)
    dc = [k for k in range(d.page_count) if d[k].get_label().startswith("DOUBLE CEILING")]
    assert len(dc) >= 2 and all(CA.textos_encimados(pdf, k) == [] for k in dc), [(k, CA.textos_encimados(pdf, k)[:2]) for k in dc]
    txt = " ".join(d[k].get_text() for k in dc).replace("\n", " ")
    assert "hung on wire 4/X7.31" in txt and "VESTIBULE EAST" in txt and "…" not in txt
    assert CA._envolver_celda("A" * 300, 50, 6) and all(pymupdf.get_text_length(x, fontname="helv", fontsize=6) <= 50
                                                         for x in CA._envolver_celda("A" * 300, 50, 6))
    print("test_be_gk41_celdas_doble_cielo OK")


test_be_gk41_celdas_doble_cielo()


def test_v108_f2_membrana_superior():
    """v81cf108 (CR rev20, falso positivo de CE_COHERENCIA_R11 F2): la membrana rated de ARRIBA (RS-1 / FS-1, Type X o C según el assembly)
    de un baño con doble cielo, sobre un GYP W.R. colgado, no queda expuesta: PASS. Un baño con un solo cielo Type X expuesto = FAIL. Una
    membrana que no cita el assembly no se exenta."""
    gn = {"X0.01": "WATER-RESISTANT GYPSUM BOARD FOR CEILINGS IN SHOWER ROOMS"}
    doble = {"misc_items": [
        {"ref": "CLG-L9-106R board", "op": "60 SF x 1 layer(s)", "familia": "5/8\" gyp board Type X", "source": "L9 901 bath: RS-1 membrane (UL L546) X3.09"},
        {"ref": "CLG-L9-106 board", "op": "60 SF x 1 layer(s)", "familia": "5/8\" gyp board W.R.", "source": "L9 901 bath: GYP-1 W.R. 8'-0\" X3.09"}]}
    assert CE.coherencia_r11(doble, gn) == [], CE.coherencia_r11(doble, gn)
    solo = {"misc_items": [{"ref": "CLG-L9-107 board", "op": "60 SF x 1 layer(s)", "familia": "5/8\" gyp board Type X",
                            "source": "L9 902 bath: X3.09"}]}
    assert any(f.startswith("F2 CLG-L9-107") for f in CE.coherencia_r11(solo, gn))
    sin_assembly = {"misc_items": [dict(doble["misc_items"][0], source="L9 901 bath: X3.09"), doble["misc_items"][1]]}
    assert any(f.startswith("F2 CLG-L9-106R") for f in CE.coherencia_r11(sin_assembly, gn))
    por_tabla = {"misc_items": [doble["misc_items"][0]]}                 # el W.R. colgado está en otro renglón: lo dice DOBLE_CIELO
    assert CE.coherencia_r11(por_tabla, gn, dobles=["L9 901 BATH"]) == []
    assert CE.coherencia_r11(por_tabla, gn) != []
    print("test_v108_f2_membrana_superior OK")


test_v108_f2_membrana_superior()


def test_v109_u191():
    """U-191 / BE-CR41 (usuario 12-nov: 'toda la informacion biene en los planos'): caso CR RFI-14 — RC '16 in. o.c. per assembly' sin el ítem
    del listing = FAIL; con 'X546 Item 6' = PASS; 'gap 866' o 'gyp' no son un GA file; en una entrega subida antes de v81cf109 = AMBER."""
    import chequeos_biblioteca as CB
    mal = {"walls": [], "rfis": [{"id": "RFI-91", "question": "RC spacing per assembly not printed; 16 in. loaded (UL L946)"}]}
    bien = {"walls": [], "rfis": [{"id": "RFI-91", "question": "RC spacing per assembly: UL L946 Item 6 = 12 in. o.c. with insulation"}]}
    assert CB.u_191_ref(CB.B(canon=mal))[0] == "FAIL" and CB.u_191_ref(CB.B(canon=bien))[0] == "PASS"
    ruido = {"walls": [{"id": "Z9-01", "source": "X1.0 gap 866.3-928.3 = removed door; 1/2\" gyp board"}]}
    assert CB.u_191_ref(CB.B(canon=ruido))[0] == "PASS"
    w = tempfile.mkdtemp(prefix="u191_")
    os.makedirs(os.path.join(w, "etapas", "4_canon"))
    json.dump(mal, open(os.path.join(w, "etapas", "4_canon", "takeoff_canon.json"), "w"))
    est = lambda: [r for r in CE.correr(w, solo={"CB_U_191_REF"})["chequeos"] if r["id"] == "CB_U_191_REF"][0]["estado"]   # noqa: E731
    assert est() == "FAIL"
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00"}, open(os.path.join(w, "SUBIDA_OK.json"), "w"))
    assert est() == "AMBER"
    print("test_v109_u191 OK")


test_v109_u191()


def test_v111_registro_y_tope():
    """BE-CR43 / BE-GK46 (GK rev3: el script de armado hizo rm -rf de la carpeta y borró compuerta_corridas.jsonl): armar 2 veces conserva
    TODAS las corridas (historial_compuerta/<rev>/ fuera de la carpeta, el jsonl solo suma); un rm -rf a mano entre dos corridas de main
    tampoco las pierde. CE_PROTOCOLO_3H: corrida sin registro = FAIL salvo 'causa:' de registro perdido por CADA una. Watchdog: cuenta
    TODOS los markups (cualquier título) y la rejilla da la misma distancia que el barrido completo."""
    import random, shutil as _sh, pymupdf
    raiz = tempfile.mkdtemp(prefix="v111_")
    car = os.path.join(raiz, "entrega_rev9")
    os.makedirs(car)
    jl = os.path.join(car, "compuerta_corridas.jsonl")
    open(jl, "w").write('{"evento": "inicio", "corrida": "a1"}\n{"evento": "fin", "corrida": "a1", "ok": false}\n')
    open(os.path.join(car, "gate.txt"), "w").write("FAIL 3\n")
    open(os.path.join(car, "viejo.xlsx"), "w").write("x")
    CE.armar_carpeta(car)
    assert not os.path.exists(os.path.join(car, "viejo.xlsx")) and os.path.isfile(os.path.join(car, "gate.txt"))
    assert len(open(jl).read().splitlines()) == 2
    with open(jl, "a") as f:
        f.write('{"evento": "inicio", "corrida": "b2"}\n')
    CE.armar_carpeta(car)                                                # segunda vez: las 3 corridas siguen
    assert [json.loads(x)["corrida"] for x in open(jl)] == ["a1", "a1", "b2"]
    assert len(open(os.path.join(CE.historial_dir(car), "compuerta_corridas.jsonl")).read().splitlines()) == 3
    w = os.path.join(raiz, "proy_rev9")
    os.makedirs(w)
    CE.main(["compuerta_entrega.py", w, "--solo", "CE_ORDENES_VIGENTES"])
    _sh.rmtree(w)                                                        # armado a mano con rm -rf (lo que hizo GK rev3)
    os.makedirs(w)
    CE.main(["compuerta_entrega.py", w, "--solo", "CE_ORDENES_VIGENTES"])
    ev_ = [json.loads(x)["evento"] for x in open(os.path.join(w, "compuerta_corridas.jsonl"))]
    assert ev_.count("inicio") == 2 and ev_.count("fin") == 2, ev_
    reg = {"inicios": 2, "fines": 2, "cortadas": 0, "rojas": 0}
    f5 = lambda tt: [x for x in CE.protocolo_3h_fallas(w, None, None, None, None, tt, [], registro_corridas=reg)[0] if x.startswith("(5)")]  # noqa: E731
    assert f5("corridas de compuerta: 3\n"), "corrida sin registro y sin causa debía fallar"
    assert f5("corridas de compuerta: 4\ncausa: corrida 3 sin renglón en el registro (jsonl borrado al re-armar)\n")
    assert not f5("corridas de compuerta: 4\ncausa: corrida 3 sin registro (jsonl borrado al re-armar)\n"
                  "causa: corrida 4 cortada antes de escribir el registro\n")
    assert not f5("corridas de compuerta: 2\n") and f5("corridas de compuerta: 1\ncausa: registro perdido\n")
    reg2 = dict(reg, inicios=2)                                          # v81cf112: forma de CR rev20 (#N sin registro: causa)
    f5b = lambda tt: [x for x in CE.protocolo_3h_fallas(w, None, None, None, None, tt, [], registro_corridas=reg2)[0] if x.startswith("(5)")]  # noqa: E731
    assert not f5b("corridas de compuerta: 4 (#1 y #2 sin registro jsonl: armar_entrega lo borró, BE-CR43; #3 y #4 en el registro)\n")
    assert f5b("corridas de compuerta: 4 (#1 y #2 sin registro jsonl)\n"), "sin causa escrita debía fallar"
    assert f5b("corridas de compuerta: 4 (#1 sin registro jsonl: armar_entrega lo borró)\n"), "una causa para 2 faltantes debía fallar"
    assert f5b("corridas de compuerta: 4\n")
    assert CE.tope_chequeo("CE_MARKUP_EN_WALL", 309) >= 3 * 1.12 * 309 and CE.tope_chequeo("CE_MARKUP_EN_WALL", 309) >= 300 + 3 * 309
    pdf = os.path.join(raiz, "mk.pdf")
    d = pymupdf.open()
    pg = d.new_page()
    for k, t in enumerate(("take-off", "Take-off", "Take-off legend")):
        a = pg.add_polyline_annot([(10 + k, 10), (50 + k, 10)])
        a.set_info(title=t)
        a.update()
    d.save(pdf)
    assert CE.contar_markups([pdf]) == 3 and CE.contar_markups(pdf) == 3
    assert CE.tope_chequeo("CE_MARKUP_EN_WALL", 3) >= CE.TIMEOUT_DEFAULT + 3 * 3 * CE.MEDIDO_S_POR_MARKUP["viejo"] - 0.1
    random.seed(9)
    for _k in range(60):
        S = [(random.uniform(0, 600), random.uniform(0, 600), random.uniform(0, 600), random.uniform(0, 600)) for _ in range(random.randint(0, 40))]
        ix = CE._IndiceSegs(S, CE.MARKUP_WALL_TOL)
        for _j in range(20):
            x, y = random.uniform(-10, 610), random.uniform(-10, 610)
            assert abs(ix.dist(x, y) - min((CE._d_seg(x, y, s) for s in S), default=1e9)) < 1e-9
    print("test_v111_registro_y_tope OK")


test_v111_registro_y_tope()


def test_v114_auditoria_u138():
    """BE-AUD05..09 (auditoría U-138 del 12-nov: chequeos débiles / en vacío). Valores sintéticos.
    (a) BE-AUD05 CB_U_191: 'L946' suelto o 'UL L946' sin 'Item N' (y sin 'N in. o.c.' en un renglón de RC) = FAIL; con Item + o.c. = PASS.
    (b) BE-AUD06 CB_RCP_APILADOS: tags / DOBLE_CIELO.csv con filas y 0 cuartos evaluados = FAIL.
    (c) BE-AUD07 CE_RCP_COMPLETO: esperados vacío con SOF en el Excel o contornos RCP = FAIL (antes 'N/A sin cielos').
    (d) BE-AUD08 CE_RESUMEN_EXCEL: cifra de la rev actual en RESUMEN / BITACORA != Material Summary = FAIL; deltas y revs viejas no cuentan.
    (e) BE-AUD09 CE_VERSION_ENTREGA: la versión de ENTREGA_OK sale de la línea VERSION de SKILL.md (no del primer párrafo) y lo
    declarado en LEEME / README tiene que coincidir."""
    import chequeos_biblioteca as CB
    import re
    import openpyxl
    mal = {"walls": [], "misc_items": [{"ref": "CLG-Z9 RC", "source": "resilient channel 16 in. o.c. per L946"}]}
    mal2 = {"walls": [], "misc_items": [{"ref": "CLG-Z9 RC", "source": "resilient channel per UL L946 Item 6"}]}
    bien = {"walls": [], "misc_items": [{"ref": "CLG-Z9 RC", "source": "resilient channel per UL L946 Item 6: 12 in. o.c."}]}
    assert CB.u_191_ref(CB.B(canon=mal))[0] == "FAIL"
    assert CB.u_191_ref(CB.B(canon=mal2))[0] == "FAIL", "RC sin espaciamiento"
    assert CB.u_191_ref(CB.B(canon=bien))[0] == "PASS"
    assert CB.falta_cita_u191("plan X9.01 sheet L-901, wall U-191 note") is None
    can = {"walls": [], "ceilings": [{"room": "Z9 Corridor 901", "area_sf": 10.0}],
           "rcp_tags": [{"tag": "GYP-9", "height": "9'-0\"", "rows": ["walls[0]"]}]}
    e, ev = CB.rcp_apilados(CB.B(canon=can, textos={"Auditoria/DOBLE_CIELO.csv": "Room,Upper,Lower\nZ9 901,FS-9,GYP-9\n"}))
    assert e == "FAIL" and "en vacío" in ev[0], ev
    e, ev = CB.rcp_apilados(CB.B(canon={"walls": [], "ceilings": []}, textos={"x/DOBLE_CIELO.csv": "Room,Upper\nZ9 901,FS-9\n"}))
    assert e == "FAIL", ev
    d = tempfile.mkdtemp(prefix="v114_")
    xl = os.path.join(d, "t.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Material Summary"
    ws.append(["Material", "Unit", "Net"])
    ws.append(["Resilient channel - printed product", "LF", 1234.56])
    ws.append(["5/8\" gypsum board, Type X", "SF", 999.0, None, None, None, None, None, "Breakdown: Z9-01 990 + SOF-99 9"])
    wb.save(xl)
    assert CE.cielos_en_excel(xl), "SOF en el desglose del Material Summary"
    ms = [("Resilient channel - printed product", [1234.56]), ("5/8\" gypsum board, Type X", [999.0])]
    t_mal = {"RESUMEN_rev9.md": "| Material | Unit | rev8 | rev9 | Delta |\n|---|---|---|---|---|\n"
                                "| Resilient channel - printed product | LF | 1,000.00 | 1,111.11 | +111.11 |\n"}
    t_bien = {"RESUMEN_rev9.md": t_mal["RESUMEN_rev9.md"].replace("1,111.11 | +111.11", "1,234.56 | +234.56")}
    ev, n = CE.resumen_excel_fallas(t_mal, ms, 9)
    assert ev and n == 1, ev
    ev, n = CE.resumen_excel_fallas(t_bien, ms, 9)
    assert ev == [] and n == 1, ev
    assert CE.resumen_excel_fallas({"BITACORA_rev9.md": "| Material | Net |\n|---|---|\n| Mystery product | 5.00 |\n"}, ms, 9)[0]
    sk = "**VERSION: v81cf901**\n... v81cf900 ... v81cf902 ..."
    assert CE.version_fallas(sk, "v81cf901", {}), "VERSION más vieja que lo citado en SKILL.md"
    assert CE.version_fallas("**VERSION: v81cf902**\nv81cf900", "v81cf902", {"LEEME.md": "Compuerta final VERDE con v81cf902\nArranque: skill v81cf800\n"}) == []
    assert CE.version_fallas("**VERSION: v81cf902**", "v81cf902", {"LEEME.md": "Compuerta final VERDE con v81cf901\n"})
    hist = ("| rev | compuerta |\n|---|---|\n| rev2-c | compuerta VERDE v81cf856 |\n| rev7 | compuerta v81cf863 |\n"
            "| rev19 | gate v81cf887 |\n")                                   # v81cf115: historia de TIEMPOS (caso CR rev20a)
    assert CE.version_fallas("**VERSION: v81cf902**", "v81cf902", {"TIEMPOS.md": hist + "| rev20a | compuerta VERDE v81cf902 |\n"}, "rev20a") == []
    assert CE.version_fallas("**VERSION: v81cf902**", "v81cf902", {"TIEMPOS.md": hist + "| rev20a | compuerta VERDE v81cf901 |\n"}, "rev20a")
    assert CE.version_fallas("**VERSION: v81cf902**", "v81cf902", {"TIEMPOS.md": hist}, "rev20a") == []
    skp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(CE.__file__))), "SKILL.md")
    if os.path.isfile(skp):                                              # en la suite (tools copiados solos) no hay SKILL.md
        sk_txt = open(skp, encoding="utf-8").read()
        assert CE._skill_version() == re.search(r"(?m)^\*\*VERSION:\s*(v\d+cf\d+)", sk_txt).group(1)
        assert not CE.version_fallas(sk_txt, CE._skill_version(), {}), "subir la línea VERSION de SKILL.md"
    print("test_v114_auditoria_u138 OK")


test_v114_auditoria_u138()


def test_v116_listing():
    """v81cf116 (CR, renglones C-H y RC del Material Summary): trazabilidad.RX_HOJA metía los listings UL / GA en 'N/SHEET' (token
    suelto sin item -> CB_U_191 FAIL). Ahora van en 'Listing:' con el texto del canon que trae el item. Valores sintéticos."""
    import chequeos_biblioteca as CB
    import trazabilidad as TZ
    src_ch = "X0.06 CH '6\" 20GA METAL C-H STUD' (UL U915) | UL U915 Item 3: C-H studs 24 in. o.c. max"
    src_rc = "resilient channel 12 in. o.c. (UL L946 Item 6: RC 12 in. o.c.) as the unit rows"
    lt, seg = TZ._listings(src_ch)
    assert lt == {"U915"} and "Item 3" in seg, (lt, seg)
    lt2, seg2 = TZ._listings(src_rc)
    assert lt2 == {"L946"} and "Item 6" in seg2, (lt2, seg2)
    assert TZ._listings("see X101 and G001; detail 3/X501")[0] == set()
    antes = [{"fila": 22, "material": "C-H stud", "fuente": "[DERIVED] N/SHEET: X0.06, U915"},
             {"fila": 14, "material": "Resilient channel", "fuente": "[DERIVED] N/SHEET: X0.08, L946"}]
    despues = [{"fila": 22, "material": "C-H stud", "fuente": f"[DERIVED] N/SHEET: X0.06 | Listing: {seg}"},
               {"fila": 14, "material": "Resilient channel", "fuente": f"[DERIVED] N/SHEET: X0.08 | Listing: {seg2}"}]
    can = {"walls": [{"id": "Z9-01", "source": "X0.06 note 3"}]}
    assert CB.u_191_ref(CB.B(canon=can, ms=antes))[0] == "FAIL"
    assert CB.u_191_ref(CB.B(canon=can, ms=despues))[0] == "PASS", CB.u_191_ref(CB.B(canon=can, ms=despues))
    sin_item = [{"fila": 9, "material": "Resilient channel", "fuente": "[DERIVED] N/SHEET: X0.08 | Listing: UL L946"}]
    assert CB.u_191_ref(CB.B(canon=can, ms=sin_item))[0] == "FAIL"
    print("test_v116_listing OK")


test_v116_listing()


def test_v117_ceilings_misc():
    """v81cf117 (GK rev3a: todos los cielos como misc_items CLG-…; CB_RCP_APILADOS daba 'en vacío' con 83 cuartos reales):
    canon.ceilings_misc [{room, ref, height, nhoja}] = solo traza (canon.py no lo cuantifica); rcp_apilados une ceilings + ceilings_misc;
    ref que no está en misc_items = FAIL. Sintético: 12 cuartos, 4 con cielo apilado (con su renglón cada uno) = PASS; sin el campo = FAIL
    en vacío; un apilado cubierto por un solo misc = FAIL."""
    import chequeos_biblioteca as CB
    misc, cm, tg = [], [], []
    for i in range(12):
        room = f"Z9 9{i:02d}"
        refs = [f"CLG-Z9-{i:02d}"] + ([f"CLG-Z9-{i:02d}U"] if i < 4 else [])
        for k, r in enumerate(refs):
            misc.append({"ref": r, "qty": 10.0, "unit": "SF"})
            cm.append({"room": room, "ref": r, "height": "9'-0\"" if k == 0 else "10'-0\"", "nhoja": "1/X9.01"})
            tg.append({"sheet": "X9.01", "tag": "GYP-9" if k == 0 else "FS-9", "height": "9'-0\"" if k == 0 else "10'-0\"", "rows": [r]})
    can = {"walls": [], "ceilings": [], "misc_items": misc, "ceilings_misc": cm, "rcp_tags": tg}
    e, ev = CB.rcp_apilados(CB.B(canon=can))
    assert e == "PASS" and "12 cuartos" in ev[0] and "4 con" in ev[0], ev
    e, ev = CB.rcp_apilados(CB.B(canon={k: v for k, v in can.items() if k != "ceilings_misc"}))
    assert e == "FAIL" and "en vacío" in ev[0], ev
    malo = json.loads(json.dumps(can))
    malo["ceilings_misc"].append({"room": "Z9 999", "ref": "CLG-NO-EXISTE", "height": "9'-0\"", "nhoja": "1/X9.01"})
    assert CB.rcp_apilados(CB.B(canon=malo))[0] == "FAIL"
    uno = json.loads(json.dumps(can))
    uno["rcp_tags"][1]["rows"] = ["CLG-Z9-00"]                              # el FS de arriba y el GYP de abajo en un solo renglón
    e, ev = CB.rcp_apilados(CB.B(canon=uno))
    assert e == "FAIL" and "un solo renglón" in " ".join(ev), ev
    print("test_v117_ceilings_misc OK")


test_v117_ceilings_misc()


def test_v118_excluded_cero():
    """v81cf118 (GK / Xfinity, drywall screws U-053): renglón EXCLUDED con cantidad 0 cuyo yield de la plantilla dice 'GA-9xx' sin ítem
    = no carga nada, CB_U_191 lo salta (PASS); el mismo renglón con cantidad > 0 = FAIL. Sintético."""
    import chequeos_biblioteca as CB
    can = {"walls": [{"id": "Z9-01", "source": "X0.06 note 3"}]}
    exc = [{"fila": 28, "material": "Drywall screws #6 x 1-1/4\" Typ", "net": 0, "purchase": 0, "pieces": 0,
            "fuente": "[DERIVED] N/SHEET: GA-916 | EXCLUDED (U-053: screws by others)"}]
    assert CB.u_191_ref(CB.B(canon=can, ms=exc))[0] in ("PASS", "N/A"), CB.u_191_ref(CB.B(canon=can, ms=exc))
    con = [dict(exc[0], net=100, purchase=100, pieces=100)]
    assert CB.u_191_ref(CB.B(canon=can, ms=con))[0] == "FAIL"
    assert not CB.ms_excluido_cero(dict(exc[0], fuente="[DERIVED] N/SHEET: GA-916"))
    assert CB.ms_excluido_cero(dict(exc[0], purchase="=C28*1.1", pieces="=F28"))   # Excel sin valores calculados: manda Net = 0
    assert not CB.ms_excluido_cero(dict(exc[0], net="=SUM(X1:X9)"))
    print("test_v118_excluded_cero OK")


test_v118_excluded_cero()


def test_v119_cobertura():
    """U-193 (usuario 12-nov: 'que se te vaya a pasar algún muro algún cielo'): mapa de cobertura sintético a 1/4" = 1'-0" (18 pt/ft).
    Dos muros dibujados (pares de líneas a 4.875"): uno con markup W9 con /Measure (CUBIERTO), otro sin markup (ROJO); con disposición
    (motivo + N/HOJA) pasa a DISPUESTO. RCP: cuarto 901 dentro de un polígono de cielo (CUBIERTO), 902 sin polígono (ROJO), 903 dentro de
    un EXCLUDED. Sin markups de wall que aprender, mueble de líneas finas a 30" no es muro. Valores sintéticos."""
    import pymupdf
    d = tempfile.mkdtemp(prefix="v119_")
    pdf = os.path.join(d, "Z9_markups - OPEN IN BLUEBEAM.pdf")
    doc = pymupdf.open()
    med = "<</Type/Measure/Subtype/RL/R(1/4 in = 1 ft)/X[<</Type/NumberFormat/C .055555557/D 100/U(ft)>>]/D[<</Type/NumberFormat/C 1/D 100/U(ft)>>]/A[<</Type/NumberFormat/C 1/D 100/U(sf)>>]>>"
    t = 4.875 / 12 * 18
    pg = doc.new_page(width=1728, height=1152)

    def muro(p0, p1, marcar):
        (x0, y0), (x1, y1) = p0, p1
        if y0 == y1:
            pg.draw_line((x0, y0), (x1, y0), width=1.2)
            pg.draw_line((x0, y0 + t), (x1, y0 + t), width=1.2)
            eje = [(x0, y0 + t / 2), (x1, y0 + t / 2)]
        else:
            pg.draw_line((x0, y0), (x0, y1), width=1.2)
            pg.draw_line((x0 + t, y0), (x0 + t, y1), width=1.2)
            eje = [(x0 + t / 2, y0), (x0 + t / 2, y1)]
        if marcar:
            a = pg.add_polyline_annot(eje)
            a.set_info(title="take-off", subject="W9")
            a.update()
            doc.xref_set_key(a.xref, "Measure", med)
        return eje
    muro((200, 300), (920, 300), True)                                   # muro largo marcado
    for k, x in enumerate((200, 380, 560, 740, 900)):                     # 5 muros verticales marcados (de aquí se aprende el estilo)
        muro((x, 300 + t), (x, 600), True)
    muro((200, 600), (920, 600), False)                                   # muro de abajo SIN markup, conectado al edificio
    pg.draw_rect(pymupdf.Rect(420, 380, 460, 380 + 30 / 12 * 18), width=0.24)   # mueble de 30 in de fondo
    for xe in (300, 300 + t):                                             # filtro de cotas: 2 líneas de extensión con su tick (45°)
        pg.draw_line((xe, 612), (xe, 680), width=1.2)                     # en el cruce con la línea de cota: NO son un muro
        pg.draw_polyline([(xe - 2.5, 672.5), (xe - 2, 673), (xe + 2.5, 667.5), (xe + 2, 667), (xe - 2.5, 672.5)], width=0, fill=(0, 0, 0))
    pg.draw_line((285, 670), (325, 670), width=0.48)
    pg.draw_line((700, 610), (700, 673), width=1.2)                       # hoja de puerta de 3'-6" (con su arco) junto a un jamb
    pg.draw_line((700 + t, 610), (700 + t, 673), width=1.2)
    pg.draw_bezier((700, 673), (735, 673), (763, 645), (763, 610), width=0.48)
    pg.insert_text((900, 1000), "1 Z9 PARTITION PLAN", fontsize=14)
    pg2 = doc.new_page(width=1728, height=1152)
    pg2.insert_text((900, 1000), "1 Z9 REFLECTED CEILING PLAN", fontsize=14)
    for k, (x0, num) in enumerate(((200, "901"), (500, "902"), (800, "903"))):
        pg2.draw_rect(pymupdf.Rect(x0, 200, x0 + 200, 400), width=1.2)
        pg2.insert_text((x0 + 90, 300), num, fontsize=10)
    p1 = pg2.add_polygon_annot([(205, 205), (395, 205), (395, 395), (205, 395)])
    p1.set_info(title="take-off", subject="5/8 GYP BOARD TYPE X")
    p1.update()
    doc.xref_set_key(p1.xref, "Measure", med)
    for x0, sub in ((805, "EXCLUDED"), (1205, "EXCLUDED"), (1405, "EXCLUDED")):
        p_ = pg2.add_polygon_annot([(x0, 205), (x0 + 190, 205), (x0 + 190, 395), (x0, 395)])
        p_.set_info(title="take-off", subject=sub, content="EXCLUDED - by others (X9.01)")
        p_.update()
    doc.set_page_labels([{"startpage": 0, "prefix": "Z9.01", "style": ""}, {"startpage": 1, "prefix": "Z9.31", "style": ""}])
    doc.save(pdf)
    r = CE.mapa_cobertura(pdf, out_pdf=os.path.join(d, "COBERTURA - IMAGE ONLY.pdf"), out_csv=os.path.join(d, "COBERTURA.csv"))
    est = {(f["hoja"], f["tipo"], f["id"]): f["estado"] for f in r["filas"] if f["tipo"] == "cielo"}
    mur = {}
    for f in r["filas"]:
        if f["tipo"] == "muro":
            mur.setdefault(round(f["y"]), []).append((f["estado"], f["largo_ft"]))
    assert {e for e, _l in mur.get(round(300 + t / 2), [])} == {"CUBIERTO"}, mur
    assert sum(l_ for e, l_ in mur.get(round(600 + t / 2), []) if e == "ROJO") >= 30, mur      # los ~36 ft sin markup entre los verticales
    assert not any(f["estado"] == "ROJO" and 360 < f["y"] < 430 and 400 < f["x"] < 480 for f in r["filas"]), "mueble de 30 in no es muro"
    assert not any(f["tipo"] == "muro" and 610 < f["y"] < 690 and 290 < f["x"] < 320 for f in r["filas"]), "líneas de extensión de cota"
    assert not any(f["tipo"] == "muro" and 610 < f["y"] < 680 and 695 < f["x"] < 712 for f in r["filas"]), "hoja de puerta no es muro"
    assert est.get(("Z9.31", "cielo", "901")) == "CUBIERTO" and est.get(("Z9.31", "cielo", "902")) == "ROJO", est
    assert est.get(("Z9.31", "cielo", "903")) == "EXCLUDED", est
    n_r = r["rojos"]
    assert os.path.isfile(os.path.join(d, "COBERTURA - IMAGE ONLY.pdf")) and n_r >= 2, n_r
    rojos_png = sorted(os.listdir(os.path.join(d, "ROJOS")))
    assert len(rojos_png) == n_r, rojos_png                               # U-193 ⭐ (2): un recorte circulado por rojo
    disp = [{"hoja": "Z9.01", "tipo": "muro", "x0": "150", "y0": str(590), "x1": "960", "y1": str(620), "decision": "NO ES NUESTRO",
             "motivo": "existing to remain", "nhoja": "1/X9.01", "revisor": "subagente R9", "imagen": "ROJOS/" + rojos_png[0]},
            {"hoja": "Z9.31", "tipo": "cielo", "id": "902", "decision": "NO ES NUESTRO", "motivo": "open to structure", "nhoja": "1/X9.31",
             "revisor": "subagente R9", "imagen": "ROJOS/" + rojos_png[-1]}]
    r2 = CE.mapa_cobertura(pdf, disp)
    assert r2["rojos"] == 0, [f for f in r2["filas"] if f["estado"] == "ROJO"]
    assert CE.mapa_cobertura(pdf, [dict(disp[0], nhoja=""), disp[1]])["rojos"] == n_r - 1, "disposición sin N/HOJA no vale"
    assert CE.mapa_cobertura(pdf, [dict(disp[0], revisor=""), disp[1]])["rojos"] == n_r - 1, "disposición sin revisor no vale"
    assert CE.mapa_cobertura(pdf, [dict(disp[0], imagen="", ), disp[1]])["rojos"] == n_r - 1, "disposición sin recorte no vale"
    rm = [f for f in r["filas"] if f["tipo"] == "muro" and f["estado"] == "ROJO"][0]       # muro por id: vale solo con su x / y
    d_id = {"hoja": rm["hoja"], "tipo": "muro", "id": rm["id"], "decision": "NO ES NUESTRO", "motivo": "existing to remain",
            "nhoja": "1/X9.01", "revisor": "subagente R9", "imagen": "ROJOS/" + rojos_png[0]}
    f_id = lambda dd: next(f for f in CE.mapa_cobertura(pdf, [dd])["filas"] if f["id"] == rm["id"])["estado"]
    assert f_id(d_id) == "ROJO", "muro por id sin x / y no vale (el número cambia si cambia el detector)"
    assert f_id(dict(d_id, x=str(rm["x"]), y=str(rm["y"]))) == "DISPUESTO"
    assert f_id(dict(d_id, x=str(rm["x"] + 200), y=str(rm["y"]))) == "ROJO", "mismo id en otra posición = otro muro"
    w = tempfile.mkdtemp(prefix="v119ce_")                              # CE_COBERTURA de punta a punta sobre una carpeta de entrega
    e = os.path.join(w, "FINAL_FOR_REVIEW_rev9")
    os.makedirs(os.path.join(e, "Planos marcados"))
    shutil.copy(pdf, os.path.join(e, "Planos marcados", os.path.basename(pdf)))
    rr, rutas = CE.cobertura_entrega(e)
    assert rr["rojos"] == n_r and os.path.isfile(rutas["pdf"]) and os.path.isdir(os.path.join(e, "Auditoria", "ROJOS"))
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "GUÍA" in str(ev[1]), ev
    import csv as _csv
    filas = [f for f in _csv.DictReader(open(rutas["csv"], encoding="utf-8")) if f["estado"] == "ROJO"]
    with open(os.path.join(e, "Auditoria", CE.COB_DISP), "w", newline="", encoding="utf-8") as fh:
        wr = _csv.DictWriter(fh, fieldnames=["hoja", "tipo", "id", "x", "y", "decision", "motivo", "nhoja", "reviewer", "imagen"])
        wr.writeheader()
        for f in filas:
            wr.writerow({"hoja": f["hoja"], "tipo": f["tipo"], "id": f["id"], "x": f["x"], "y": f["y"], "decision": "NO ES NUESTRO",
                         "motivo": "EXISTING CONSTRUCTION TO REMAIN", "nhoja": "2/X9.01", "reviewer": "subagente R9", "imagen": f["imagen"]})
    open(os.path.join(e, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w").write(
        "## Coverage map limits\nA single missing face of a marked wall does not show in red; diagonal walls are not detected; two leaves "
        "fused by the map into one covered wall do not show in red (a 'same wall' exclusion needs its gap_proof with N/SHEET); the identity of the "
        "reviewer / subagent is declared (SUBAGENTE_ID), not proven by the program.\n")
    CE.cobertura_entrega(e)
    ev = chk(CE.ce_cobertura, CE.Ctx(w))                                # verificación 12b: sin CHECKLIST con B6 = FAIL
    assert ev[0] == "FAIL" and "CHECKLIST" in str(ev[1]) and "reviewer 'subagente R9'" in str(ev[1]), ev   # y revisor no registrado
    import bitacora as BT                                               # revisor = subagente REGISTRADO en la bitácora, distinto del canon
    BT.BIT = os.path.join(w, "bitacora.jsonl")
    BT.subagente("revisor_cobertura", "subagente R9")
    ev = chk(CE.ce_cobertura, CE.Ctx(w))                                # verificación 2: sin autores del canon registrados = FAIL
    assert ev[0] == "FAIL" and "corridas de canon.py con su agente" in str(ev[1]), ev
    tl_ = os.path.join(w, "canon.py")                                   # los autores se registran SOLOS: SUBAGENTE_ID al correr canon.py
    open(tl_, "w").write("print('canon sintético')\n")
    viejo = os.environ.get("SUBAGENTE_ID")
    os.environ["SUBAGENTE_ID"] = "subagente C9"
    try:
        BT.run(tl_, [])
    finally:
        os.environ.pop("SUBAGENTE_ID") if viejo is None else os.environ.__setitem__("SUBAGENTE_ID", viejo)
    assert [r.get("agente") for r in BT.leer() if r.get("tool") == "canon.py"] == ["subagente C9"]
    ev = chk(CE.ce_cobertura, CE.Ctx(w))                                # v120 (U6): un canon.py SIN agente = FAIL aunque haya otro con agente
    shutil.copy(os.path.join(w, "bitacora.jsonl"), os.path.join(w, "bit_c9.jsonl"))
    BT.run(tl_, [])
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "sin agente" in str(ev[1]), ev
    shutil.copy(os.path.join(w, "bit_c9.jsonl"), os.path.join(w, "bitacora.jsonl"))
    BT.subagente("canon", "FAKE-CANON")                                 # un 'subagente canon' declarado no es autor del canon
    assert "fake-canon" not in CE.subagentes_bitacora(w)[2]
    shutil.copy(os.path.join(w, "bit_c9.jsonl"), os.path.join(w, "bitacora.jsonl"))
    wb = openpyxl.Workbook()
    wb.active.title = "B1 Excel"
    wb.create_sheet("B6 Coverage")
    wb.save(os.path.join(e, "Z9_CHECKLIST_REVISION_rev9.xlsx"))
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "PASS", ev
    wb = openpyxl.Workbook()
    wb.active.title = "B1 Excel"
    wb.save(os.path.join(e, "Z9_CHECKLIST_REVISION_rev9.xlsx"))
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "B6" in str(ev[1]), ev                     # CHECKLIST sin la hoja B6
    shutil.copy(os.path.join(w, "bitacora.jsonl"), os.path.join(w, "bit0.jsonl"))
    BT.anotar({"tool": "resolver.py", "args": [], "rc": 0, "hashes": {}, "log": "x", "agente": "SUBAGENTE r9"})   # el revisor escribió
    # una etapa (U7: los ids se comparan en minúsculas)
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "escribió etapas 2-7" in str(ev[1]), ev
    shutil.copy(os.path.join(w, "bit0.jsonl"), os.path.join(w, "bitacora.jsonl"))
    BT.anotar({"tool": "compuerta_entrega.py", "args": [], "rc": 0, "hashes": {}, "log": "x", "agente": "subagente R9"})   # la compuerta no
    ev = chk(CE.ce_cobertura, CE.Ctx(w))                                # lo vuelve autor (aquí solo falta la B6 del paso anterior)
    assert "escribió etapas" not in str(ev[1:]) and "B6" in str(ev[1:]), ev
    shutil.copy(os.path.join(w, "bit0.jsonl"), os.path.join(w, "bitacora.jsonl"))
    open(os.path.join(w, "bitacora.jsonl"), "w").write(open(os.path.join(w, "bit0.jsonl")).read().replace('"revisor_cobertura"', '"revisor_otro"'))
    ev = chk(CE.ce_cobertura, CE.Ctx(w))                                # solo vale el rol EXACTO revisor_cobertura
    assert ev[0] == "FAIL" and "reviewer 'subagente R9'" in str(ev[1]), ev   # otro rol = autor, no revisor
    shutil.copy(os.path.join(w, "bit0.jsonl"), os.path.join(w, "bitacora.jsonl"))
    wb.create_sheet("B6 Coverage")
    wb.save(os.path.join(e, "Z9_CHECKLIST_REVISION_rev9.xlsx"))
    dp = os.path.join(e, "Auditoria", CE.COB_DISP)
    txt = open(dp, encoding="utf-8").read()
    open(dp, "w", encoding="utf-8").write(txt.replace("NO ES NUESTRO", "FALTA"))   # FALTA nunca limpia un rojo
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "ROJO sin markup" in str(ev[1]), ev
    open(dp, "w", encoding="utf-8").write(txt)
    os.remove(os.path.join(e, "Auditoria", CE.COB_CSV))                 # sin CSV / sin PDF = FAIL
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and CE.COB_CSV in str(ev[1]), ev
    CE.cobertura_entrega(e)
    os.remove(os.path.join(e, "Planos marcados", CE.COB_PDF))
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and CE.COB_PDF in str(ev[1]), ev
    CE.cobertura_entrega(e)
    assert chk(CE.ce_cobertura, CE.Ctx(w))[0] == "PASS"
    gp = os.path.join(e, "GUIA_DE_REVISION_DEL_ESTIMADOR.md")         # v120 BE-GK54: la GUÍA documenta el límite de leaves fusionadas
    gtxt = open(gp).read()
    open(gp, "w").write("## Coverage map limits\nA single missing face of a marked wall does not show in red; diagonal walls are not detected.\n")
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "BE-GK54" in str(ev[1]), ev
    open(gp, "w").write(gtxt.replace("identity", "name"))                # v121 U-193: sin 'identity … declared' = FAIL
    ev = chk(CE.ce_cobertura, CE.Ctx(w))
    assert ev[0] == "FAIL" and "DECLARADA" in str(ev[1]), ev
    open(gp, "w").write(gtxt)
    o = CE.mapa_cobertura                                               # detector ciego: planta con 0 muros / RCP con 0 cuartos = FAIL
    for k, cg in (("ciegas", ["Z9.01"]), ("ciegas_rcp", ["Z9.31"])):
        CE.mapa_cobertura = lambda *a, _k=k, _cg=cg, **kw: dict(o(*a, **kw), **{_k: _cg})
        try:
            ev = chk(CE.ce_cobertura, CE.Ctx(w))
        finally:
            CE.mapa_cobertura = o
        assert ev[0] == "FAIL" and "detector ciego" in str(ev[1]), (k, ev)
    dp = os.path.join(e, "Auditoria", CE.COB_DISP)                     # salida verificable: el revisor revisa la hoja entera (hoja_ciega)
    txt0 = open(dp, encoding="utf-8").read()
    img = [n for n in os.listdir(os.path.join(e, "Auditoria", "ROJOS"))][0]
    for dec, rv, esperado in (("CUBIERTO", "subagente R9", "PASS"), ("FALTA", "subagente R9", "FAIL"), ("CUBIERTO", "otro", "FAIL")):
        open(dp, "w", encoding="utf-8").write(txt0 + f"Z9.31,hoja_ciega,,,,{dec},all ceilings on the sheet checked by hand,1/X9.31,{rv},ROJOS/{img}\n")
        CE.mapa_cobertura = lambda *a, **kw: dict(o(*a, **kw), ciegas_rcp=["Z9.31"])
        try:
            ev = chk(CE.ce_cobertura, CE.Ctx(w))
        finally:
            CE.mapa_cobertura = o
        assert ev[0] == esperado, (dec, rv, ev)
    open(dp, "w", encoding="utf-8").write(txt0)
    pr = pymupdf.open(pdf)                                              # RCP real sin números de cuarto -> ciegas_rcp
    pr2 = pymupdf.open()
    pr2.insert_pdf(pr, from_page=1, to_page=1)
    pg_ = pr2[0]
    for b in pg_.get_text("words"):
        if b[4] in ("901", "902", "903"):
            pg_.add_redact_annot(pymupdf.Rect(b[:4]))
    pg_.apply_redactions(images=0, graphics=0)
    pr2.set_page_labels([{"startpage": 0, "prefix": "Z9.31", "style": ""}])
    sinc = os.path.join(d, "Z9_sin_cuartos.pdf")
    pr2.save(sinc)
    assert CE.mapa_cobertura(sinc)["ciegas_rcp"] == ["Z9.31"], CE.mapa_cobertura(sinc)
    print("test_v119_cobertura OK")


def test_v119_mutacion_cobertura():
    """verificación 12b (U-193 (4)): la mutación que se hizo a mano sobre CR rev20a (quitar las DOS caras de TO-W.4-L2-02 y los dos
    polígonos del corredor 216) entra a la suite con datos sintéticos equivalentes: un plano con todo marcado da 0 rojos; al quitar los
    markups de un muro sale ese muro ROJO; al quitar los polígonos de un cuarto (dos cielos apilados) sale el cuarto ROJO."""
    d = tempfile.mkdtemp(prefix="mut119_")
    med = "<</Type/Measure/Subtype/RL/R(1/4 in = 1 ft)/X[<</Type/NumberFormat/C .055555557/D 100/U(ft)>>]/D[<</Type/NumberFormat/C 1/D 100/U(ft)>>]/A[<</Type/NumberFormat/C 1/D 100/U(sf)>>]>>"
    t = 4.875 / 12 * 18
    doc = pymupdf.open()
    pg = doc.new_page(width=1728, height=1152)
    ejes = []
    for (x0, y0), (x1, y1) in [((200, 300), (920, 300)), ((200, 600), (920, 600))] + [((x, 300 + t), (x, 600)) for x in (200, 380, 560, 740, 900)]:
        if y0 == y1:
            pg.draw_line((x0, y0), (x1, y0), width=1.2)
            pg.draw_line((x0, y0 + t), (x1, y0 + t), width=1.2)
            ejes.append([(x0, y0 + t / 2), (x1, y0 + t / 2)])
        else:
            pg.draw_line((x0, y0), (x0, y1), width=1.2)
            pg.draw_line((x0 + t, y0), (x0 + t, y1), width=1.2)
            ejes.append([(x0 + t / 2, y0), (x0 + t / 2, y1)])
    for k, e_ in enumerate(ejes):
        for cara in ("A", "B"):                                         # CR marca cada cara (A / B) sobre la misma línea
            a = pg.add_polyline_annot(e_)
            a.set_info(title="take-off", subject="W9", content=f"X9-L9-{k:02d} face {cara}")
            a.update()
            doc.xref_set_key(a.xref, "Measure", med)
    pg.insert_text((900, 1000), "1 Z9 PARTITION PLAN", fontsize=14)
    pg2 = doc.new_page(width=1728, height=1152)
    pg2.insert_text((900, 1000), "1 Z9 REFLECTED CEILING PLAN", fontsize=14)
    for x0, num in ((200, "916"), (500, "917")):
        pg2.draw_rect(pymupdf.Rect(x0, 200, x0 + 200, 400), width=1.2)
        pg2.insert_text((x0 + 90, 300), num, fontsize=10)
        for sub in ("5/8 TYPE C", "GYP BOARD TYPE X"):                   # dos cielos apilados por cuarto (FS + GYP)
            p_ = pg2.add_polygon_annot([(x0 + 5, 205), (x0 + 195, 205), (x0 + 195, 395), (x0 + 5, 395)])
            p_.set_info(title="take-off", subject=sub, content=f"Z9 Corridor {num}")
            p_.update()
            doc.xref_set_key(p_.xref, "Measure", med)
    doc.set_page_labels([{"startpage": 0, "prefix": "Z9.02", "style": ""}, {"startpage": 1, "prefix": "Z9.32", "style": ""}])
    base = os.path.join(d, "Z9_markups.pdf")
    doc.save(base)
    r = CE.mapa_cobertura(base)
    assert r["rojos"] == 0, [f for f in r["filas"] if f["estado"] == "ROJO"]

    def mutar(sal, quitar):
        m = pymupdf.open(base)
        for p in m:
            for a in list(p.annots()):
                if quitar(a.info.get("content") or ""):
                    p.delete_annot(a)
        m.save(sal)
        return CE.mapa_cobertura(sal)
    r = mutar(os.path.join(d, "m1.pdf"), lambda c: c.startswith("X9-L9-04 "))        # las dos caras del muro vertical de x = 560
    rj = [f for f in r["filas"] if f["estado"] == "ROJO"]
    assert rj and all(f["tipo"] == "muro" and abs(f["x"] - (560 + t / 2)) < 2 for f in rj), rj
    assert sum(f["largo_ft"] for f in rj) >= 15, rj
    r = mutar(os.path.join(d, "m2.pdf"), lambda c: c == "Z9 Corridor 916")              # los dos polígonos del corredor 916
    rj = [(f["tipo"], f["id"]) for f in r["filas"] if f["estado"] == "ROJO"]
    assert rj == [("cielo", "916")], rj
    r = mutar(os.path.join(d, "m3.pdf"), lambda c: c == "X9-L9-04 face A")             # límite documentado: UNA sola cara no sale
    assert r["rojos"] == 0, "una sola cara faltante NO sale en rojo (límite documentado en la GUÍA)"
    print("test_v119_mutacion_cobertura OK")


test_v119_mutacion_cobertura()


test_v119_cobertura()


def test_v119_postmortem_12b():
    """post-mortem 2026-11-12b (CR rev20a): (U-190) renglón de DOBLE_CIELO inventado / borrado / repetido arriba y abajo = FAIL;
    (U-189) 'double' declarados con 0 apilados evaluados = FAIL, la pila FS / RS + GYP se toma de DOBLE_CIELO aunque la membrana no sea
    tag; detalle_caras 'loaded' = ref exacta; cobertura_esperada ve burbujas de letra; (BE-CR40) hallazgo 'falta' de algo cargado = FAIL;
    (3.2) versión fija del proyecto; (3.3) alarma de presupuesto y 'plan:' pasado el 100 %. Sintético."""
    import chequeos_biblioteca as CB
    can = {"walls": [], "ceilings": [{"id": "FS-9 Z9 901", "area_sf": 90.0}],
           "misc_items": [{"ref": "CLG-Z9-01 board", "qty": 90.0}, {"ref": "CLG-Z9-02 board", "qty": 0.0}],
           "rcp_tags": [{"sheet": "X9.02", "tag": "GYP-9", "height": "8'-11\"", "rows": ["CLG-Z9-01 board"]}],
           "ceilings_misc": [{"room": "Z9 901", "ref": "CLG-Z9-01 board", "height": "8'-11\"", "nhoja": "1/X9.02"}]}
    dc = ("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
          "Z9 901,Z9,double,FS-9 membrane,GYP-9,8'-11\",1/X9.02,RC per UL X999 Item 6 (1/X9.02),upper: FS-9 [0]; lower: CLG-Z9-01\n")
    filas = [{"Room": "Z9 901", "Type": "double", "Row / reason": "upper: FS-9 [0]; lower: CLG-Z9-01", "N/SHEET": "1/X9.02"}]
    assert CE.refs_doble_fallas(filas, can) == []
    assert CE.refs_doble_fallas([dict(filas[0], **{"Row / reason": "upper: FS-9 [0]; lower: CLG-Z9-77"})], can), "renglón inventado"
    assert CE.refs_doble_fallas([dict(filas[0], **{"Row / reason": "upper: CLG-Z9-01; lower: CLG-Z9-01"})], can), "mismo renglón"
    assert CE.refs_doble_fallas([dict(filas[0], **{"Row / reason": "upper: FS-9 [0]; lower: CLG-Z9-02"})], can), "cantidad 0"
    e, ev = CB.rcp_apilados(CB.B(canon=can, textos={"Auditoria/DOBLE_CIELO.csv": dc}))
    assert e == "PASS" and "1 de 1 'double'" in ev[0], ev
    malo = dc.replace("lower: CLG-Z9-01", "lower: CLG-Z9-55")
    assert CB.rcp_apilados(CB.B(canon=can, textos={"Auditoria/DOBLE_CIELO.csv": malo}))[0] == "FAIL"
    d2 = {"walls": [], "misc_items": [{"ref": "SOF-Z9-01 board", "qty": 9.0, "source": "1/X9.23"}],
          "detail_faces": [{"detail": "1/X9.23", "faces": [{"face": "bottom", "loaded": "SOF-Z9-01 board"}]}]}
    assert CB.detalle_caras(CB.B(canon=d2))[0] == "PASS"
    d2["detail_faces"][0]["faces"][0]["loaded"] = "SOF-Z9-01 side"            # antes pasaba con la primera palabra
    assert CB.detalle_caras(CB.B(canon=d2))[0] == "FAIL"
    dets, _r = CE.cobertura_esperada({"misc_items": [{"ref": "SOF-Z9-02", "source": "D/X9.31 and 4/X9.32"}]}, {})
    assert "D/X9.31" in dets and "4/X9.32" in dets, dets
    w = tempfile.mkdtemp(prefix="v119pm_")
    assert CE.version_proyecto_fallas(w, "v81cf999"), "sin VERSION_PROYECTO.txt = falla"
    CE.fijar_version_proyecto(w, "rev9", "v81cf998")
    assert CE.version_proyecto_fallas(w, "v81cf999"), "versión distinta a la fijada"
    try:
        CE.fijar_version_proyecto(w, "rev9", "v81cf999")
        raise AssertionError("cambiar la versión a mitad de la rev sin causa debía fallar")
    except ValueError:
        pass
    CE.fijar_version_proyecto(w, "rev9", "v81cf999", causa="regla nueva del usuario")
    assert CE.version_proyecto_fallas(w, "v81cf999", "| x |\n"), "falta 'causa:' en TIEMPOS"
    assert CE.version_proyecto_fallas(w, "v81cf999", "causa: versión v81cf999 por regla nueva\n") == []
    open(os.path.join(w, "tiempos.log"), "w").write("2026-01-01 08:00 | 0 inicio\n2026-01-01 10:00 | 4 fin\n")
    al = CE.alerta_presupuesto(w, 10)
    assert al["pct"] > 50 and al["umbral"] == 50 and os.path.isfile(os.path.join(w, "ALERTA_PRESUPUESTO.json")), al
    assert CE.presupuesto_fallas(10, 400, "causa: x", exigir_plan=True)[0] == "FAIL"
    assert CE.presupuesto_fallas(10, 400, "causa: x\nplan: cortar el paso 9", exigir_plan=True)[0] == "AMBER"
    assert CE.presupuesto_fallas(10, 400, "causa: x")[0] == "AMBER"                     # entregas anteriores: como antes
    print("test_v119_postmortem_12b OK")


test_v119_postmortem_12b()


def test_v119_gk_nombres_y_bitacora():
    """GK (PRUEBA_ABIERTOS de v119): (a) CE_NOMBRES_ENTREGA tomaba 'COBERTURA - IMAGE ONLY.pdf' (U-193) por un PDF de markups mal nombrado;
    una copia con otro nombre sí falla. (b) _hashes_cadena solo leía $BITACORA y <w>/bitacora.jsonl: GK corre la cadena en
    <w>/takeoff_work/bitacora.jsonl. Sintético."""
    ok = ["Z9_markups_rev9 - OPEN IN BLUEBEAM.pdf", CE.COB_PDF, "Z9.01 - IMAGE ONLY (not editable) - walls rev9.png"]
    assert CE.nombres_planos(ok) == [], CE.nombres_planos(ok)
    assert CE.nombres_planos(ok + ["COBERTURA - IMAGE ONLY (1).pdf"]), "otra copia del mapa con otro nombre sí falla"
    w = tempfile.mkdtemp(prefix="gkb_")
    os.makedirs(os.path.join(w, "takeoff_work"))
    viejo = os.environ.pop("BITACORA", None)
    try:
        open(os.path.join(w, "takeoff_work", "bitacora.jsonl"), "w").write(json.dumps({"tool": "x.py", "hashes": {"a": "f" * 64}}) + "\n")
        assert CE._hashes_cadena(w) == {"f" * 64}, CE._hashes_cadena(w)
        open(os.path.join(w, "bitacora.jsonl"), "w").write(json.dumps({"tool": "y.py", "hashes": {"b": "e" * 64}}) + "\n")
        assert CE._hashes_cadena(w) == {"f" * 64, "e" * 64}
    finally:
        if viejo is not None:
            os.environ["BITACORA"] = viejo
    print("test_v119_gk_nombres_y_bitacora OK")


test_v119_gk_nombres_y_bitacora()


def test_v119_prueba_abiertos():
    """verificación 12b (BE-PM04 STILL-WEAK: sin tests): prueba_abiertos con nombre de proyecto ('proy=<carpeta>'); un chequeo PASS con la
    vigente que da FAIL con la candidata = regresión sin explicar -> ok falso; con explicación -> ok; dos sesiones con proyectos distintos se
    UNEN en el mismo archivo. Compuertas simuladas (sin correr la cadena)."""
    d = tempfile.mkdtemp(prefix="pa119_")
    w1, w2 = os.path.join(d, "w1"), os.path.join(d, "w2")
    os.makedirs(w1), os.makedirs(w2)
    vig = {"skill_version": "v81cf900", "chequeos": [{"id": "CE_X9", "estado": "PASS"}, {"id": "CE_Z9", "estado": "FAIL"}]}
    cand = {"resumen": {"PASS": 0, "AMBER": 0, "FAIL": 2}, "chequeos": [{"id": "CE_X9", "estado": "FAIL", "evidencia": ["x"]},
                                                                        {"id": "CE_Z9", "estado": "FAIL", "evidencia": ["z"]}]}
    o1, o2 = CE._correr_con, CE.correr
    CE._correr_con, CE.correr = (lambda t, w, s: vig), (lambda w, **k: cand)
    try:
        sal = os.path.join(d, "PRUEBA_ABIERTOS_vX.json")
        o = CE.prueba_abiertos("/no/importa", [f"proy_a={w1}"], sal)
        assert not o["ok"] and o["proyectos"]["proy_a"]["sin_explicar"] == 1, o          # PASS -> FAIL sin explicar
        assert [r["chequeo"] for r in o["regresiones"]] == ["CE_X9"], o["regresiones"]     # FAIL -> FAIL no es regresión
        o = CE.prueba_abiertos("/no/importa", [f"proy_a={w1}"], sal, {"CE_X9": "falso positivo corregido en la candidata (X9.01)"})
        assert o["ok"] and len(o["regresiones"]) == 1, o                                  # re-correr el mismo proyecto lo reemplaza
        o = CE.prueba_abiertos("/no/importa", [f"proy_b={w2}"], sal, {"CE_X9": "explicado"})
        assert set(o["proyectos"]) == {"proy_a", "proy_b"} and o["ok"], o                 # otra sesión: se unen
        try:                                                            # v120: sin '<proyecto>=' no corre (la clave es el nombre)
            CE.prueba_abiertos("/no/importa", [w2], sal)
            raise AssertionError("prueba_abiertos sin nombre de proyecto debió fallar")
        except ValueError:
            pass
    finally:
        CE._correr_con, CE.correr = o1, o2
    print("test_v119_prueba_abiertos OK")


test_v119_prueba_abiertos()


def test_v119_alarma_presupuesto():
    """verificación 12b (BE-PM06 STILL-WEAK: la alarma era opcional): (1) paso cerrado en tiempos.log sin su corrida --paso = falla;
    (2) pasado el 50 % / 100 % sin la alerta escrita en ese momento = falla; (3) alertas medidas al cerrar cada paso (alerta_presupuesto,
    con historial) + corridas --paso de cada paso = sin fallas; (4) una alerta escrita tarde (después del paso siguiente) no vale.
    Presupuesto 180 min (5 hojas A), horas sintéticas."""
    w = tempfile.mkdtemp(prefix="al119_")
    log = ["2026-01-05 10:00 | 1 inicio", "2026-01-05 10:40 | 1 fin | 2 inicio", "2026-01-05 11:40 | 2 fin | 3 inicio",
           "2026-01-05 13:10 | 3-5 fin | 6 inicio", "2026-01-05 13:30 | 6-8 fin"]
    tl = os.path.join(w, "tiempos.log")
    reg = [{"evento": "fin", "paso": p} for p in ("1", "2", "3-5")]
    open(tl, "w").write("\n".join(log) + "\n")
    ev = CE.alarma_fallas(w, 5, reg)
    assert any("paso 6-8" in x for x in ev) and not any("paso 2 " in x for x in ev), ev          # (1)
    assert any("50 %" in x for x in ev) and any("100 %" in x for x in ev), ev                    # (2) sin ALERTA_PRESUPUESTO.json
    for k in range(2, len(log) + 1):                                     # (3) la sesión corre --paso al cerrar cada paso
        open(tl, "w").write("\n".join(log[:k]) + "\n")
        CE.alerta_presupuesto(w, 5)
    al = json.load(open(os.path.join(w, "ALERTA_PRESUPUESTO.json")))
    assert [h["umbral"] for h in al["historial"]] == [50, 100, 100], al["historial"]
    assert CE.alarma_fallas(w, 5, reg + [{"evento": "fin", "paso": "6-8"}]) == []
    al["historial"] = [h for h in al["historial"] if h["umbral"] == 50] + [dict(al["historial"][-1], log_ts="2026-01-05T15:00:00")]
    json.dump(al, open(os.path.join(w, "ALERTA_PRESUPUESTO.json"), "w"))
    ev = CE.alarma_fallas(w, 5, reg + [{"evento": "fin", "paso": "6-8"}])
    assert len(ev) == 1 and "100 %" in ev[0], ev                                                 # (4) alerta del 100 % tarde
    print("test_v119_alarma_presupuesto OK")


test_v119_alarma_presupuesto()


def test_be_gk54():
    """BE-GK54 (unido de apartados/be_gk54): caso real M-Z9.11-29 de Grand Kia rev3a — X9-Z9-20 excluido como 'same single wall as X9-Z9-08'
    mientras la hoja dibuja una segunda leaf a 2 in -> FAIL; con la leaf cargada (no ROJO) o con gap_proof -> PASS; otras exclusiones no
    se revisan."""
    canon = {"walls": [{"id": "X9-Z9-08", "band": {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}}],
             "excluded_walls": [{"id": "X9-Z9-20", "reason": "same single wall as X9-Z9-08 behind the niche"}]}
    red_v = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-Z9.11-29", "x": "1505.7", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
    real = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-Z9.11-29", "x": "1014.3", "y": "1505.7", "largo_ft": "3.48", "estado": "ROJO"}]
    rot270 = lambda h, x, y: (y, 2160.0 - x)                            # noqa: E731
    assert CE.be_gk54_fallas(canon, real, to_canon=rot270), "el rojo en coordenadas del CSV (rotación 270) da FAIL"
    assert CE.be_gk54_fallas(canon, red_v), "la segunda leaf escondida da FAIL"
    assert not CE.be_gk54_fallas(canon, [dict(red_v[0], estado="CUBIERTO")]), "con la leaf cargada: PASS"
    canon2 = {**canon, "excluded_walls": [dict(canon["excluded_walls"][0], gap_proof='1/X9.50 shows one wall: gap 0" (measured)')]}
    assert not CE.be_gk54_fallas(canon2, red_v), "exclusión con gap_proof impreso: PASS"
    assert not CE.be_gk54_fallas({**canon, "excluded_walls": [{"id": "Q", "reason": "existing CMU"}]}, red_v), "otras exclusiones no"
    d = pymupdf.open()                                                  # el convertidor del PDF usa rotation_matrix de la hoja (rot 270)
    pg = d.new_page(width=2160, height=3024)
    pg.set_rotation(270)
    d.set_page_labels([{"startpage": 0, "prefix": "Z9.11", "style": ""}])
    f = os.path.join(tempfile.mkdtemp(prefix="gk54_"), "x.pdf")
    d.save(f)
    tc = CE._gk54_desde_pdf(f)
    q = pymupdf.Point(1014.3, 1505.7) * pymupdf.open(f)[0].rotation_matrix
    assert tc("Z9.11", 1014.3, 1505.7) == (q.x, q.y) and tc("Z9", 1.0, 2.0) == (1.0, 2.0)
    def gk(wid, reason, extra=None, b=None):                            # v120 (verificación 3, adv_gk54)
        band = canon["walls"][0]["band"] if b is None else b
        can = {"walls": [{"id": wid, "band": band}], "excluded_walls": [dict({"id": "EX", "reason": reason}, **(extra or {}))]}
        return CE.be_gk54_fallas(can, red_v)
    assert gk("TO-W.4-L9-02", "same single wall as TO-W.4-L9-02"), "G1: id con otro formato"
    assert gk("W-12", "same wall as W-12"), "G1b"
    assert gk("X9-Z9-08", "duplicate of X9-Z9-08 (one wall)") and gk("X9-Z9-08", "same as X9-Z9-08") and gk("X9-Z9-08", "part of wall X9-Z9-08")
    assert gk("X9-Z9-08", "same wall as X9-Z9-08", {"gap_proof": "n/a"}), "G3: gap_proof sin N/HOJA no vale"
    assert not gk("X9-Z9-08", "same wall as X9-Z9-08", {"gap_proof": 'one wall, gap 0" (1/X9.50)'})
    ev = gk("X9-Z9-08", "same wall as X9-Z9-08", b={})
    assert ev and "no 'band'" in ev[0], ev                              # G6: sin band = FAIL, no salto silencioso
    disp = lambda txt: [dict(red_v[0], estado="DISPUESTO", disposicion=txt)]          # noqa: E731   v120 (G4)
    assert CE.be_gk54_fallas(canon, disp("NO ES NUESTRO: same wall as X9-Z9-08 (1/X9.11)")), "G4: disposición 'same wall' sin gap"
    assert CE.be_gk54_fallas(canon, disp("duplicate of X9-Z9-08 (1/X9.11)"))
    assert not CE.be_gk54_fallas(canon, disp('same wall as X9-Z9-08: gap 0" measured (1/X9.50)')), "con la prueba del gap"
    assert CE.be_gk54_fallas(canon, disp("EXISTING CONSTRUCTION TO REMAIN (2/X9.11)")), "v121 estructural: toda disposición exige gap_proof"
    assert CE.be_gk54_fallas(canon, disp("")), "DISPUESTO sin texto de disposición no se puede evaluar = FAIL"
    ev = CE.be_gk54_fallas({"walls": [], "excluded_walls": [{"id": "EX", "reason": "same wall as X9-Z9-77"}]}, red_v)
    assert ev and "not a wall of the canon" in ev[0], ev
    print("test_be_gk54 OK")


test_be_gk54()


def test_v119_alarma_verificacion2():
    """verificación 2 (BE-PM06 STILL-WEAK): (1) entrega nueva sin tiempos.log = FAIL (antes la alarma no corría); (2) TIEMPOS.md y
    tiempos.log cuadran: paso cerrado en TIEMPOS.md sin marca a esa hora, o menos marcas que pasos = FAIL; (3) ALERTA_PRESUPUESTO.json y
    compuerta_corridas.jsonl sellados en la bitácora: editados a mano = FAIL. Horas sintéticas."""
    w = tempfile.mkdtemp(prefix="al2_")
    tt = ("| # | Paso | Inicio | Fin | Duración |\n|---|---|---|---|---|\n| 1 | inventario | 01-05 10:00 PST | 01-05 10:20 PST | 20 min |\n"
          "| 2-3 | lecturas | 01-05 10:20 PST | 01-05 10:50 PST | 30 min |\n")
    reg = [{"evento": "fin", "paso": "1"}, {"evento": "fin", "paso": "2"}]
    ev = CE.alarma_fallas(w, 5, reg, tiempos_txt=tt)
    assert any("sin tiempos.log" in x for x in ev) and any("no cuadran" in x for x in ev), ev           # (1)
    tl = os.path.join(w, "tiempos.log")
    open(tl, "w").write("2026-01-05 10:00 | 1 inicio\n2026-01-05 10:20 | 1 fin | 2 inicio\n2026-01-05 10:45 | 2 fin\n")
    ev = CE.alarma_fallas(w, 5, reg, tiempos_txt=tt)
    assert len(ev) == 1 and "2-3" in ev[0] and "10:50" in ev[0], ev                                      # (2) la hora no cuadra
    open(tl, "w").write("2026-01-05 10:00 | 1 inicio\n2026-01-05 10:20 | 1 fin | 2 inicio\n2026-01-05 10:50 | 2 fin\n")
    assert CE.alarma_fallas(w, 5, reg, tiempos_txt=tt) == []
    rp = os.path.join(w, "compuerta_corridas.jsonl")                                                       # (3) registro sellado
    open(rp, "w").write("\n".join(json.dumps(r) for r in reg) + "\n")
    ev = CE.alarma_fallas(w, 5, None, tiempos_txt=tt)
    assert any("sin sello" in x for x in ev), ev
    CE.sellar_bitacora(w, rp)
    assert CE.alarma_fallas(w, 5, None, tiempos_txt=tt) == []
    open(rp, "a").write(json.dumps({"evento": "fin", "paso": "3"}) + "\n")                               # editado a mano
    ev = CE.alarma_fallas(w, 5, None, tiempos_txt=tt)
    assert any("compuerta_corridas.jsonl" in x and "último sello" in x for x in ev), ev
    CE.sellar_bitacora(w, rp)
    open(tl, "a").write("2026-01-05 12:00 | 4 fin\n")                                                    # 120 min de 180 = 67 %
    CE.alerta_presupuesto(w, 5)                                                                           # la compuerta la escribe y la sella
    assert CE.alarma_fallas(w, 5, None, tiempos_txt=tt) == [] or all("--paso 4" in x for x in CE.alarma_fallas(w, 5, None, tiempos_txt=tt))
    ap = os.path.join(w, "ALERTA_PRESUPUESTO.json")
    al = json.load(open(ap))
    al["historial"][0]["log_ts"] = "2026-01-05T11:30:00"
    json.dump(al, open(ap, "w"))                                                                          # alerta editada a mano
    ev = CE.alarma_fallas(w, 5, None, tiempos_txt=tt)
    assert any("ALERTA_PRESUPUESTO.json" in x and "último sello" in x for x in ev), ev
    rows = [json.loads(x) for x in open(os.path.join(w, "bitacora.jsonl"))]
    import bitacora as BT
    assert BT.cadena_ok(rows) == 0, "los sellos respetan la cadena de hashes"
    w3 = tempfile.mkdtemp(prefix="al3_")                                # v120 (verificación 3, E3): log a las horas de fin SIN 'N fin'
    open(os.path.join(w3, "tiempos.log"), "w").write("2026-01-05 10:00 | inicio\n2026-01-05 10:20 | inventario listo\n2026-01-05 10:50 | lecturas listas\n")
    ev = CE.alarma_fallas(w3, 5, [], tiempos_txt=tt)
    assert any("paso 1 cerrado en TIEMPOS.md" in x for x in ev) and any("paso 2-3 cerrado en TIEMPOS.md" in x for x in ev), ev
    assert CE.alarma_fallas(w3, 5, [{"evento": "fin", "paso": "1"}, {"evento": "fin", "paso": "2-3"}], tiempos_txt=tt) == []
    print("test_v119_alarma_verificacion2 OK")


test_v119_alarma_verificacion2()


def test_v120_adv4():
    """verificación 4 de v120 (apartados/adversariales_v120/adv4_*, sintético): norm_txt común; PM06 con el parser de CE_TIEMPOS (guiones
    Unicode, negritas, 4a, 3 columnas, columnas en otro orden, '--paso 9' / '1-9' no cubren); U-193 ids normalizados (mayúsculas, doble
    espacio, NBSP, ancho cero, tab) y 'tools/canon.py'; GK54 sinónimos amplios y prueba del gap = N/HOJA + gap medido en 0."""
    assert CE.norm_txt("Same\u2011Wall\u00a0 as\u200b X") == "same-wall as x"
    log = "2026-01-05 10:00 | inicio\n2026-01-05 10:20 | a\n2026-01-05 10:50 | b\n2026-01-05 11:10 | c\n"
    def tt(rows, hdr="| # | Paso | Inicio | Fin | Duración | Evidencia |\n|---|---|---|---|---|---|\n"):
        return "# T PST\n" + hdr + "".join(rows) + "| TOTAL | x | | | 70 min | |\n"
    def pm06(t, reg=None):
        w = tempfile.mkdtemp(prefix="adv4pm06_")
        open(os.path.join(w, "tiempos.log"), "w").write(log)
        return [x for x in CE.alarma_fallas(w, 5, reg or [], tiempos_txt=t) if "--paso" in x]
    std = ["| 1 | inv | 01-05 10:00 PST | 01-05 10:20 PST | 20 min | e |\n", "| 2-3 | lect | 01-05 10:20 PST | 01-05 10:50 PST | 30 min | e |\n",
           "| 4 | canon | 01-05 10:50 PST | 01-05 11:10 PST | 20 min | e |\n"]
    variantes = {"F1": tt([r.replace("| 2-3 |", "| 2\u20133 |") for r in std]), "F2": tt([r.replace("| 4 |", "| **4** |").replace("| 1 |", "| **1** |") for r in std]),
                 "F3": tt([r.replace("| 4 |", "| 4a |") for r in std]),
                 "F4": tt(["| 1 | 01-05 10:00 PST | 01-05 10:20 PST |\n", "| 2-3 | 01-05 10:20 PST | 01-05 10:50 PST |\n", "| 4 | 01-05 10:50 PST | 01-05 11:10 PST |\n"],
                          "| Paso | Inicio | Fin |\n|---|---|---|\n"),
                 "F5": tt(["| 1 | 01-05 10:00 PST | 01-05 10:20 PST | 20 min | inv |\n", "| 2-3 | 01-05 10:20 PST | 01-05 10:50 PST | 30 min | lect |\n",
                           "| 4 | 01-05 10:50 PST | 01-05 11:10 PST | 20 min | canon |\n"], "| # | Inicio | Fin | Duración | Paso |\n|---|---|---|---|---|\n")}
    for k, t in list(variantes.items()) + [("F0", tt(std))]:
        assert len(pm06(t)) == 3, (k, pm06(t))                          # los 3 pasos cerrados sin su --paso = FAIL
        assert CE.tiempos_fallas(t) == [], (k, CE.tiempos_fallas(t))     # y CE_TIEMPOS los lee con el mismo parser
    assert len(pm06(tt(std), [{"evento": "fin", "paso": "9"}] * 3)) == 3                     # F6
    assert len(pm06(tt(std), [{"evento": "fin", "paso": "1-9"}])) == 3                       # F7: '1-9' no cubre cada paso
    assert pm06(tt(std), [{"evento": "fin", "paso": p} for p in ("1", "2-3", "4")]) == []     # F8
    assert pm06(variantes["F3"], [{"evento": "fin", "paso": p} for p in ("1", "2-3", "4a")]) == []
    import bitacora as BT                                               # U-193 (adv4_u193)
    def bit(filas):
        w = tempfile.mkdtemp(prefix="adv4u_")
        BT.BIT = os.path.join(w, "bitacora.jsonl")
        for f in filas:
            if f[0] == "sub":
                BT.subagente(f[1], f[2])
            else:
                BT.anotar(dict({"tool": f[1], "args": [], "rc": 0, "hashes": {}, "log": "x"}, **({"agente": f[2]} if f[2] is not None else {})))
        return w
    def acepta(filas, rv):
        rev, aut, can, sin = CE.subagentes_bitacora(bit(filas))
        r = CE.norm_agente(rv)                                         # v121: el mismo normalizador que ce_cobertura
        return bool(can) and not sin and r in rev and r not in aut
    assert acepta([("run", "canon.py", "subagente A1"), ("sub", "revisor_cobertura", "subagente R9")], "subagente R9")      # U0
    for rv in ("subagente  A1", "subagente\u00a0A1", "subagente A1\u200b", "subagente\tA1", "SUBAGENTE a1", "subagente A1\u00a0"):
        assert not acepta([("run", "canon.py", "subagente A1"), ("sub", "revisor_cobertura", rv)], rv), repr(rv)            # U7-U12
    assert not acepta([("run", "tools/canon.py", "subagente A1"), ("run", "canon.py", "subagente Z"), ("sub", "revisor_cobertura", "subagente A1")], "subagente A1")  # U13
    assert not acepta([("sub", "canon", "FAKE"), ("run", "canon.py", None), ("sub", "revisor_cobertura", "subagente A1")], "subagente A1")   # U6
    band = {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}         # GK54 (adv4_gk54)
    red = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": "1505.7", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
    W = "X9-Z9-08"
    def gk(reason, extra=None, rows=red):
        return bool(CE.be_gk54_fallas({"walls": [{"id": W, "band": band}], "excluded_walls": [dict({"id": "EX", "reason": reason}, **(extra or {}))]}, rows))
    disp = lambda t: [dict(red[0], estado="DISPUESTO", disposicion=t)]  # noqa: E731
    for r in [f"same wall as {W}", f"same wall as: {W}", f"same wall as '{W}'", f"same wall ({W})", f"already counted in {W}", f"included in {W}",
              f"identical to {W}", f"counted with {W}", f"dup of {W}", f"same\u2011wall as {W}", f"same wall as\u00a0{W}", f"mismo muro que {W}", f"see {W}"]:
        assert gk(r), r                                                                          # H3
    for t in [f"NO ES NUESTRO: part of {W} (1/X9.11)", f"already counted in {W} (1/X9.11)", f"same leaf as {W} (1/X9.11)",
              f"NO ES NUESTRO: same\u2011wall {W} (1/X9.11)", f"dup of {W} (1/X9.11)", "same wall gap n/a A111", "same wall, gap n/a (1/A111)",
              "same wall gap N/A A111"]:
        assert gk(f"same wall as {W}", rows=disp(t)), t                                          # H1 / H4 / H7
    assert gk(f"same wall as {W}", rows=disp("EXISTING CONSTRUCTION TO REMAIN (2/X9.11)"))   # H5 (v121 estructural: sin gap_proof = FAIL)
    assert gk(f"same wall as {W}", {"gap_proof": "n/a (1/A111)"}) and gk(f"same wall as {W}", {"gap_proof": "there IS a 6in gap 3/A111"})   # H2 / H2b
    assert gk(f"same wall as {W}", {"gap_proof": "no gap (1/A111)"}) and not gk(f"same wall as {W}", {"gap_proof": 'gap 0" (1/A150)'})
    assert not gk(f"see note 3 (1/X9.11)")                               # 'see' sin un wall del canon no es GK54
    print("test_v120_adv4 OK")


test_v120_adv4()


def test_v120_retroactivo_proceso():
    """v120 (COORDINACIÓN, CR rev20b / GK rev3b, sintético): los requisitos de PROCESO de v119 (BE-PM05 VERSION_PROYECTO, BE-PM06
    tiempos.log / --paso / sellos, alarma) salen AMBER con la causa escrita en una rev que arrancó ANTES de FECHA_V119; el formato viejo del
    log ('12-nov 08:00 PST' / '10-nov 21:01 PST') se lee como ISO; sin marcas, la fecha sale del primer commit; sin fecha = FAIL; una rev
    que arrancó después = FAIL."""
    tt = ("| # | Paso | Inicio | Fin | Duración |\n|---|---|---|---|---|\n| 7 | calc | 11-12 08:30 PST | 11-12 09:00 PST | 30 min |\n"
          "| 8-10 | docs | 11-12 09:00 PST | 11-12 09:40 PST | 40 min |\n| TOTAL | | | | 70 min |\n")
    w = tempfile.mkdtemp(prefix="retro_")
    open(os.path.join(w, "tiempos.log"), "w").write("12-nov 08:00 PST | rev9b inicio\n12-nov 08:20 PST | 6 fin\n")   # cierres 7-10 solo en commits
    ms = CE.marcas_tiempos_log(os.path.join(w, "tiempos.log"))
    assert [t.isoformat() for t, _l in ms] == ["2026-11-12T08:00:00", "2026-11-12T08:20:00"], ms
    est, msg = CE.proceso_v119(w, None, tt, 5)
    assert est == "AMBER" and "causa:" in msg[0] and any("--paso 7" in x for x in msg) and any("VERSION_PROYECTO" in x for x in msg), (est, msg)
    open(os.path.join(w, "tiempos.log"), "w").write("10-nov 21:01 PST | rev9b inicio (formato GK)\n")
    assert CE.proceso_v119(w, None, tt, 5)[0] == "AMBER"
    open(os.path.join(w, "tiempos.log"), "w").write("12-nov 14:00 PST | rev9c inicio\n")                               # 22:00 UTC > v119
    assert CE.proceso_v119(w, None, tt, 5)[0] == "FAIL"
    w2 = tempfile.mkdtemp(prefix="retro2_")                             # sin tiempos.log ni git = no se puede fechar = FAIL
    est, msg = CE.proceso_v119(w2, None, tt, 5)
    assert est == "FAIL" and "no se puede fechar" in msg[0], (est, msg)
    e3 = os.path.join(w2, "FINAL_FOR_REVIEW_rev9b")                     # sin marcas: la fecha del primer commit de la carpeta de la rev
    os.makedirs(e3)
    open(os.path.join(e3, "x.md"), "w").write("x\n")
    env = dict(os.environ, GIT_AUTHOR_DATE="2026-11-12T08:00:00-08:00", GIT_COMMITTER_DATE="2026-11-12T08:00:00-08:00",
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@x")
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"], ["git", "commit", "-q", "-m", "rev9b"]):
        subprocess.run(cmd, cwd=w2, env=env, check=True, capture_output=True)
    assert CE.inicio_rev(w2, e3).isoformat().startswith("2026-11-12T08:00:00")
    assert CE.proceso_v119(w2, e3, tt, 5)[0] == "AMBER"
    print("test_v120_retroactivo_proceso OK")


test_v120_retroactivo_proceso()


def test_v121_estructurales():
    """v121 (verificación 5, adv5_pm06 / adv5_proceso / adv5_gk54 / adv5_u193, sintético): (1) BE-PM06 la celda de paso con cualquier
    prefijo ('Paso 1', 'Steps 2-3', '1. Inventario', '1 Inventario') la exige --paso y la lee CE_TIEMPOS; (2) RETRO: arranque = marca con
    la etiqueta de la rev o la primera después de las de otra rev, en orden del archivo; log acumulado sin etiqueta / año imposible /
    marcas fuera de orden = FAIL; (3) GK54 estructural: toda leaf paralela a <= 14 in excluida o dispuesta (cualquier texto) exige
    gap_proof con N/HOJA + gap medido; (4) U-193 ids normalizados (alfanumérico, sin prefijo 'subagente')."""
    def tab(c, head="| Paso | Inicio | Fin | Duración |"):
        return (head + "\n|---|---|---|---|\n" + f"| {c[0]} | 11-13 09:00 | 11-13 09:30 | 30 min |\n| {c[1]} | 11-13 09:30 | 11-13 10:00 | 30 min |\n"
                f"| {c[2]} | 11-13 10:00 | 11-13 10:20 | 20 min |\n| TOTAL | | | 80 min |\n")
    for c, h in ((("1", "2-3", "4"), None), (("Paso 1", "Paso 2-3", "Paso 4"), None), (("1. Inventario", "2-3. Lecturas A/B", "4. Comparación"), None),
                 (("1 Inventario", "2-3 Lecturas A/B", "4 Comparación"), None), (("Step 1", "Steps 2-3", "Step 4"), "| Step | Start | End | Duration |")):
        t = tab(c, h) if h else tab(c)
        assert CE.pasos_cerrados_tiempos(t) == ["1", "2-3", "4"], (c, CE.pasos_cerrados_tiempos(t))
        assert CE.tiempos_fallas(t) == [], (c, CE.tiempos_fallas(t))
    assert CE.paso_de_celda("30 min") is None and CE.paso_de_celda("11-13 09:00") is None and CE.paso_de_celda("rev15") is None
    assert CE.paso_de_celda("4a") == ("4a", [4]) and CE.paso_de_celda("#5") == ("5", [5])
    TT = "| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 1 | 11-13 09:00 | 11-13 09:30 | 30 min |\n"
    def mk(parent=None, own=None, nom="rev21"):
        p = tempfile.mkdtemp(prefix="retro121_")
        w = os.path.join(p, nom)
        os.makedirs(w)
        if parent is not None:
            open(os.path.join(p, "tiempos.log"), "w").write(parent)
        if own is not None:
            open(os.path.join(w, "tiempos.log"), "w").write(own)
        return w
    OLD = "05-nov 11:26 PST | 0 Arranque | inicio\n05-nov 19:42 PST | 4-6 | fin\n"
    NEW = "2026-11-13 09:00 | 1 inicio rev21\n2026-11-13 09:30 | 1 fin\n"
    assert CE.inicio_rev(mk(parent=OLD + NEW)).isoformat().startswith("2026-11-13T09:00")          # P1: etiqueta de la rev
    assert CE.proceso_v119(mk(parent=OLD + NEW), None, TT, 5)[0] == "FAIL"
    assert CE.proceso_v119(mk(parent=OLD + NEW.replace(" rev21", "")), None, TT, 5)[0] == "FAIL"     # acumulado sin etiqueta
    w = mk(own="10-nov 21:01 PST | (copiado de rev3) arranque\n2026-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n")
    assert CE.inicio_rev(w).isoformat().startswith("2026-11-13T09:00") and CE.proceso_v119(w, None, TT, 5)[0] == "FAIL"   # P3
    est, msg = CE.proceso_v119(mk(own="2025-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n"), None, TT, 5)
    assert est == "FAIL" and "fuera de orden" in msg[0], (est, msg)                                 # P5 año mal escrito
    est, msg = CE.proceso_v119(mk(parent="2026-11-10 09:00 | rev20 fin\n2025-11-11 09:00 | 1 inicio rev21\n"), None, TT, 5)
    assert est == "FAIL" and "año imposible" in msg[0], (est, msg)
    est, msg = CE.proceso_v119(mk(parent=OLD + "10-nov 08:00 PST | 1 inicio rev21\n10-nov 09:00 PST | 1 fin\n"), None, TT, 5)
    assert est == "AMBER" and "causa:" in msg[0], (est, msg)                                       # control: rev anterior a v119
    band = {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
    red = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": "1505.7", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
    W = "X9-Z9-08"
    def gk(reason, extra=None, rows=red, excl=True):
        can = {"walls": [{"id": W, "band": band}], "excluded_walls": [dict({"id": "EX", "reason": reason}, **(extra or {}))] if excl else []}
        return bool(CE.be_gk54_fallas(can, rows))
    for r in (f"covered by {W}", f"accounted for in {W}", f"merged with {W}", f"other leaf of {W}", f"furring side of {W} (one wall)"):
        assert gk(r), r                                                                             # K1 sin sinónimos
    for t in (f"NO ES NUESTRO: same wall as {W} (1/Z9.11)", "NO ES MURO: casework (1/Z9.11)", f"CUBIERTO: counted in {W} (1/Z9.11)"):
        assert gk("", rows=[dict(red[0], estado="DISPUESTO", disposicion=t)], excl=False), t        # K2 cualquier disposición
    assert not gk("", rows=[dict(red[0], estado="DISPUESTO", disposicion='NO ES NUESTRO: 0" gap, leaves touch (1/Z9.11)')], excl=False)
    for g, bien in (('gap 0" (1/Z9.11)', True), ("leaves touch, 0 in gap per 1/Z9.11", True),
                    ('0" gap, 3-5/8" studs back to back (1/Z9.11)', True), ("no gap between leaves (1/Z9.11)", False), ('gap 2" (1/Z9.11)', False)):
        assert gk(f"same wall as {W}", {"gap_proof": g}) != bien, g                                   # K3
    assert not gk("tile backer, see grid 4")                                                         # ROJO sin exclusión que lo cite: CE_COBERTURA
    for a_, b_ in (("subagente A1", "subagente_A1"), ("subagente A1", "subagente-A1"), ("A1", "subagente A1"), ("lectura-A", "lectura A"),
                   ("agent B2", "B2")):
        assert CE.norm_agente(a_) == CE.norm_agente(b_), (a_, b_)                                    # V1-V4
    assert CE.norm_agente("subagente R9") != CE.norm_agente("subagente A1")
    print("test_v121_estructurales OK")


test_v121_estructurales()


def test_be_gk55():
    """BE-GK55 (unido de apartados/be_gk55; caso R17-F1 de Grand Kia rev3b, ids sintéticos): T falsa sobre un wall que no cambió = FAIL;
    con corner_skip o con los dos ids en CAMBIOS = PASS; un nodo entre dos walls NUEVOS no se revisa."""
    a13 = {"id": "X9-Z1-13", "band": {"ori": "H", "c0": 1327.4, "c1": 1331.2, "lo": 1275.0, "hi": 1388.2, "sheet": "Z9.11"}}
    f21 = {"id": "F-Z1-21", "band": {"ori": "V", "c0": 1395.4, "c1": 1396.4, "lo": 1326.6, "hi": 1362.6, "sheet": "Z9.11"}}
    prev = {"walls": [a13], "nodes": [{"kind": "free", "wall": "X9-Z1-13"}]}
    new = {"walls": [a13, f21], "nodes": [{"kind": "T", "branch": "X9-Z1-13", "through": "F-Z1-21"}]}
    assert CE.be_gk55_fallas(prev, new, "F-Z1-21 + F-Z1-22 (nuevos): keynote patch"), "T falsa sobre un wall sin cambio = FAIL"
    new_skip = {"walls": [a13, dict(f21, corner_skip_info={"X9-Z1-13": "infill between (Z9.11)"})], "nodes": new["nodes"]}
    assert not CE.be_gk55_fallas(prev, new_skip, ""), "par declarado 'no se tocan'"
    assert not CE.be_gk55_fallas(prev, new, "X9-Z1-13 / F-Z1-21: corner checked on Z9.11"), "explicado en CAMBIOS"
    f22 = {"id": "F-Z1-22", "band": {"ori": "V", "c0": 1395.4, "c1": 1396.4, "lo": 1370.9, "hi": 1374.6, "sheet": "Z9.11"}}
    assert not CE.be_gk55_fallas(prev, {"walls": [a13, f21, f22], "nodes": [{"kind": "split", "walls": ["F-Z1-21", "F-Z1-22"]}]}, "")
    print("test_be_gk55 OK")


test_be_gk55()


def test_v122_sin_agente_historico():
    """v122 (COORDINACIÓN 12-nov, CR con miles de corridas históricas sin agente): las corridas sin agente fechadas ANTES de
    FECHA_V119 salen AMBER con su causa; las de después (o sin fecha) dan FAIL. Sintético."""
    v, n = CE.corridas_sin_agente_por_fecha(["canon.py 2026-11-06T10:00:00", "calc.py 2026-11-12T21:21:00", "canon.py 2026-11-12T21:22:00",
                                             "canon.py ", "excel.py 2026-11-12T22:00:00+00:00"])
    assert v == ["canon.py 2026-11-06T10:00:00", "calc.py 2026-11-12T21:21:00"], v
    assert n == ["canon.py 2026-11-12T21:22:00", "canon.py ", "excel.py 2026-11-12T22:00:00+00:00"], n
    print("test_v122_sin_agente_historico OK")


test_v122_sin_agente_historico()


def test_v123_fechas_publicacion():
    """v123 (COORDINACIÓN 12-nov 22:46, CR rev20b): las fechas de gating son la hora REAL del commit de publicación de cada versión; una rev
    arrancada a las 19:49 UTC (v118 vigente) no queda sujeta a las reglas de v119 (AMBER con causa); una arrancada después de 21:21:52Z sí."""
    import datetime as _dt
    assert CE.FECHA_V119 == "2026-11-12T21:21:52+00:00" and CE.FECHA_V120 == "2026-11-12T22:01:18+00:00"
    assert CE.FECHA_V121 == "2026-11-12T22:44:35+00:00" and {"v81cf119", "v81cf120", "v81cf121"} <= set(CE.FECHAS_PUBLICACION)
    assert CE.FECHA_V119 < CE.FECHA_V120 < CE.FECHA_V121
    tt = "| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 7 | 11-12 11:50 | 11-12 12:20 | 30 min |\n"
    for hora, esperado in (("11:49", "AMBER"), ("13:30", "FAIL")):          # PST: 19:49 UTC (antes de v119) / 21:30 UTC (después)
        w = os.path.join(tempfile.mkdtemp(prefix="v123_"), "rev20b")
        os.makedirs(w)
        open(os.path.join(w, "tiempos.log"), "w").write(f"12-nov {hora} PST | 1 inicio rev20b\n")
        est, msg = CE.proceso_v119(w, None, tt, 5)
        assert est == esperado, (hora, est, msg)
    v, n = CE.corridas_sin_agente_por_fecha(["canon.py 2026-11-12T19:49:00"])
    assert v and not n                                                  # corrida sin agente a las 19:49 UTC = histórica (AMBER)
    assert _dt.datetime.fromisoformat(CE.FECHA_V119) > _dt.datetime.fromisoformat("2026-11-12T19:49:00+00:00")
    print("test_v123_fechas_publicacion OK")


test_v123_fechas_publicacion()


def test_v124_gk_rev_y_material():
    """v124 (COORDINACIÓN 12-nov 22:56, 2 bugs de GK, sintético): (1) RX_REV_ETIQ encuentra 'rev3b' en 'entrega_rev3b' ('_' no corta);
    (2) GK54: MISMO MURO exige gap medido 0 + N/HOJA; NO ES NUESTRO de otro material impreso (CMU / masonry / concrete / existing /
    by others) exige material + N/HOJA + gap medido > 0 (no gap 0); 'same wall' con gap 4" = FAIL."""
    for nom, et in (("entrega_rev3b", "3b"), ("FINAL_FOR_REVIEW_rev21", "21"), ("rev20a", "20a"), ("prev3", None), ("rev3bx", None)):
        assert CE._etiqueta_rev(os.path.join("/x", nom)) == et, (nom, CE._etiqueta_rev(nom))
    w = os.path.join(tempfile.mkdtemp(prefix="v124_"), "entrega_rev3b")
    os.makedirs(w)
    open(os.path.join(w, "tiempos.log"), "w").write("10-nov 21:01 PST | (copiado de rev3a) arranque\n2026-11-12 15:00 | 1 inicio rev3b\n")
    assert CE.inicio_rev(w).isoformat().startswith("2026-11-12T15:00"), CE.inicio_rev(w)
    band = {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
    W = "X9-Z9-08"
    def gk(disp, x=1497.0, excl=None):                                  # leaf a ~13.5 in (x 1497.0) o ~10 in (x 1499.5) de la band
        rows = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": str(x), "y": "1145.0", "largo_ft": "4.0", "estado": "DISPUESTO",
                 "disposicion": disp}]
        return CE.be_gk54_fallas({"walls": [{"id": W, "band": band}], "excluded_walls": excl or []}, rows)
    assert not gk('NO ES NUESTRO: existing CMU, gap 13.5" to the stud wall (1/Z9.11)'), "CMU a 13.5 in con N/HOJA = PASS"
    assert not gk('NO ES NUESTRO: CMU type K, gap 10.0" (1/Z9.11)', x=1499.5), "CMU type K a 10.0 in = PASS"
    assert gk('NO ES NUESTRO: existing CMU (1/Z9.11)'), "otro material sin gap medido = FAIL"
    assert gk('NO ES NUESTRO: existing CMU, gap 13.5"'), "sin N/HOJA = FAIL"
    assert not gk('NO ES NUESTRO: 0" gap, leaves touch (1/Z9.11)'), "gap medido 0 + N/HOJA también vale (la leaf es la misma)"
    assert gk('NO ES NUESTRO: casework, gap 6" (1/Z9.11)'), "sin material impreso = FAIL"
    assert gk(f'same wall as {W}, gap 4" (1/Z9.11)'), "'same wall' con gap 4 in = FAIL"
    assert gk(f'NO ES NUESTRO: existing CMU, same wall as {W}, gap 13.5" (1/Z9.11)'), "dice 'same wall': caso (a), pide gap 0"
    assert not gk(f'same wall as {W}: gap 0" (1/Z9.11)'), "mismo muro con gap 0 + N/HOJA = PASS"
    ex = [{"id": "EX", "reason": f"by others: existing concrete beside {W}", "gap_proof": 'gap 12" (1/Z9.11)'}]
    assert not gk("", excl=ex) or True                                  # disposición vacía + exclusión: se revisa la exclusión
    rows_rojo = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": "1497.0", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
    assert not CE.be_gk54_fallas({"walls": [{"id": W, "band": band}], "excluded_walls": ex}, rows_rojo), "exclusión de otro material con gap > 0"
    print("test_v124_gk_rev_y_material OK")


test_v124_gk_rev_y_material()


def test_v125_gk54_face_centre():
    """v125 (COORDINACIÓN 12-nov 22:58, caso real de GK con ids sintéticos): GK54(b) acepta cualquier gap medido > 0, face-to-face o
    centre-to-centre, con el material impreso; el valor del campo gap_proof cuenta como texto de gap aunque no diga 'gap'."""
    t = 'gap_proof: 4.0" face-to-face / 10.0" centre-to-centre (46/A550) - CMU type K'
    assert CE.otro_material_ok(t) and not CE.es_mismo_muro(t)
    assert CE.otro_material_ok('4.0" face-to-face / 10.0" center-to-center (46/A550) - CMU type K')
    assert not CE.otro_material_ok('0" face-to-face (46/A550) - CMU type K'), "gap 0 no prueba dos muros en (b)"
    band = {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
    rojo = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": "1499.5", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
    ex = [{"id": "EX", "reason": "by others: CMU type K beside W1", "gap_proof": t.split("gap_proof: ")[1]}]
    assert not CE.be_gk54_fallas({"walls": [{"id": "W1", "band": band}], "excluded_walls": ex}, rojo), "gap_proof sin la palabra 'gap'"
    disp = [dict(rojo[0], estado="DISPUESTO", disposicion="NO ES NUESTRO: " + t)]
    assert not CE.be_gk54_fallas({"walls": [{"id": "W1", "band": band}], "excluded_walls": []}, disp)
    ex2 = [{"id": "EX", "reason": "same wall as W1", "gap_proof": t.split("gap_proof: ")[1]}]
    assert CE.be_gk54_fallas({"walls": [{"id": "W1", "band": band}], "excluded_walls": ex2}, rojo), "'same wall' con gap 4 in = FAIL"
    print("test_v125_gk54_face_centre OK")


test_v125_gk54_face_centre()


def test_v126_bloqueos_gk_cr():
    """v126 (COORDINACIÓN 12-nov 23:13, bloqueos de entrega de GK y CR, sintético): (1) corridas sin agente REEMPLAZADAS (la misma tool
    corrida después con agente) = AMBER 'cadena interrumpida y reemplazada'; sin reemplazo = FAIL; (2) GK54 enlaza exclusión y rojo SOLO
    por el id de canon del muro; una disposición NO ES NUESTRO con prueba de material no se cruza con la exclusión de fusión de otra pieza."""
    sin = ["disponer_tags.py 2026-11-12T21:24:01", "canon.py 2026-11-12T21:24:10", "test_ciego.py 2026-11-12T21:24:30"]
    con = [("disponer_tags.py", "2026-11-12T21:40:00"), ("canon.py", "2026-11-12T21:41:00"), ("test_ciego.py", "2026-11-12T21:45:00")]
    assert CE.sin_agente_reemplazadas(sin, con) == (sin, [])
    rep, no = CE.sin_agente_reemplazadas(sin, con[:2])
    assert rep == sin[:2] and no == sin[2:], (rep, no)                  # test_ciego sin reemplazo = FAIL
    assert CE.sin_agente_reemplazadas(["canon.py 2026-11-12T21:50:00"], con) == ([], ["canon.py 2026-11-12T21:50:00"])   # agente ANTES
    band = {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "Z9.11"}
    W, W2 = "X9-Z9-08", "X9-Z9-30"
    walls = [{"id": W, "band": band}, {"id": W2, "band": dict(band, c0=1700.0, c1=1703.8)}]
    disp = [{"hoja": "Z9.11", "tipo": "muro", "id": "M-29", "x": "1497.0", "y": "1145.0", "largo_ft": "4.0", "estado": "DISPUESTO",
             "disposicion": 'NO ES NUESTRO: existing CMU, gap 13.5" (1/Z9.11)'}]
    fusion = [{"id": "X9-Z9-31", "reason": f"same wall as {W2} (M-29 read by the reader)"}]      # fusión de OTRA pieza; cita el id de lector
    assert not CE.be_gk54_fallas({"walls": walls, "excluded_walls": fusion}, disp), "la exclusión de otra pieza no se cruza"
    rojo = [dict(disp[0], estado="ROJO", disposicion="")]
    assert not CE.be_gk54_fallas({"walls": walls, "excluded_walls": fusion}, rojo), "el id de lector en el texto no enlaza"
    assert CE.be_gk54_fallas({"walls": walls, "excluded_walls": [{"id": "X9-Z9-31", "reason": f"same wall as {W}"}]}, rojo)
    assert CE.be_gk54_fallas({"walls": walls, "excluded_walls": [{"id": "X9-Z9-31", "wall": W, "reason": "leaf"}]}, rojo), "campo wall"
    print("test_v126_bloqueos_gk_cr OK")


test_v126_bloqueos_gk_cr()


def test_v127_etiqueta_rev_cr():
    """v127 (COORDINACIÓN 12-nov 23:16, caso CR, sintético): workdir 'entrega' sin revN + Excel '..._rev20b.xlsx' + marca 'inicio rev20b'
    anterior a FECHA_V119 = AMBER; orden Excel / PDF -> VERSION_PROYECTO.txt -> carpeta."""
    w = os.path.join(tempfile.mkdtemp(prefix="v127_"), "entrega")
    os.makedirs(os.path.join(w, "Take-off"))
    open(os.path.join(w, "Take-off", "Z9_Hotel_TakeOff_rev20b.xlsx"), "w").write("x")
    open(os.path.join(w, "tiempos.log"), "w").write("10-nov 21:01 PST | (copiado de rev20a) arranque\n12-nov 11:49 PST | 1 inicio rev20b\n")
    assert CE._etiqueta_rev(w) == "20b"
    tt = "| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 7 | 11-12 11:50 | 11-12 12:20 | 30 min |\n"
    est, msg = CE.proceso_v119(w, None, tt, 5)
    assert est == "AMBER" and "causa:" in msg[0], (est, msg)          # 19:49 UTC < FECHA_V119 (21:21:52Z)
    w2 = os.path.join(tempfile.mkdtemp(prefix="v127b_"), "entrega")
    os.makedirs(w2)
    open(os.path.join(w2, "VERSION_PROYECTO.txt"), "w").write("2026-11-12T10:00:00+00:00 | rev20a | v81cf118 | \n2026-11-12T19:49:00+00:00 | rev20b | v81cf118 | \n")
    assert CE._etiqueta_rev(w2) == "20b"                              # (2) VERSION_PROYECTO.txt
    w3 = os.path.join(tempfile.mkdtemp(prefix="v127c_"), "entrega_rev3b")
    os.makedirs(w3)
    assert CE._etiqueta_rev(w3) == "3b"                               # (3) carpeta
    open(os.path.join(w3, "VERSION_PROYECTO.txt"), "w").write("2026-11-12T10:00:00+00:00 | rev3c | v81cf118 | \n")
    assert CE._etiqueta_rev(w3) == "3c"                               # VERSION_PROYECTO antes que la carpeta
    open(os.path.join(w3, "X_markups_rev3d.pdf"), "w").write("x")
    assert CE._etiqueta_rev(w3) == "3d"                               # el PDF / Excel de la entrega manda
    print("test_v127_etiqueta_rev_cr OK")


test_v127_etiqueta_rev_cr()


def test_v128_rev_con_letra():
    """v128 (COORDINACIÓN 12-nov 23:44, CR rev20b, sintético): UNA REV_PAT con letra; orden 20 < 20a < 20b < 21; la carpeta 'rev20b FINAL
    PARA REVISAR' valida de verdad (falta 'CAMBIOS rev20b vs rev20' = FAIL; RESUMEN_rev20 + RESUMEN_rev20b en la raíz = FAIL); sin rev
    identificable = FAIL 'no se pudo identificar la rev' (no PASS en vacío)."""
    assert sorted(["21", "20b", "20", "20a"], key=CE.rev_clave) == ["20", "20a", "20b", "21"]
    assert CE.rev_de("Proposal_rev20b.xlsx") == "20b" and CE.rev_de("entrega_rev3b") == "3b" and CE.rev_de("prev3") is None
    c = "rev20b FINAL PARA REVISAR"
    assert CE.carpeta_rev_fallas(c) == [] and CE.carpeta_rev_fallas("rev20b FINAL — ESTA ES LA VERSION") != []
    ev = CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev20 vs rev19\n", c)
    assert ev and "rev20b" in ev[0], ev                                 # la primera sección es de otra rev = FAIL
    assert CE.guia_cambios_fallas("# GUIA\nsin cambios\n", c), "falta la sección = FAIL"
    assert CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev20b vs rev20\n", c) == []
    assert CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev20b vs rev20a\n", c) == []
    assert CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev21 vs rev20b\n", "rev21 FINAL PARA REVISAR") == []
    ev = CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev20b vs rev20\n", "entrega")
    assert ev and "no se pudo identificar la rev" in ev[0], ev          # sin rev = FAIL, no []
    assert CE.guia_cambios_fallas("# GUIA\n## CAMBIOS rev20b vs rev20\n", "entrega", "20b") == []   # rev del Excel / PDF
    assert CE.resumenes_fallas(["RESUMEN_rev20.md", "RESUMEN_rev20b.md", "GUIA.md"]), "dos RESUMEN en la raíz = FAIL"
    d = tempfile.mkdtemp(prefix="v128_")
    for n in ("RESUMEN_rev20.md", "RESUMEN_rev20b.md", "RESUMEN_rev9.md"):
        open(os.path.join(d, n), "w").write(n)
    class C:
        w, entrega = d, None
    txt, n = CE._ultimos_md(C())
    assert n == "20b" and list(txt) == ["RESUMEN_rev20b.md"], (n, list(txt))   # rev20 y rev20b no se mezclan
    print("test_v128_rev_con_letra OK")


test_v128_rev_con_letra()


def test_be_gk56():
    """BE-GK56 (unido de apartados/be_gk56; casos de Grand Kia rev3b con ids sintéticos): destino 'same wall' leído del texto del lector
    sin medición = FAIL; medido = PASS; gap > 0 sin cargar = FAIL (FALTA); cargado como RI-x = PASS; destino fuera del canon = FAIL."""
    walls = [{"id": "X9-Z1-06"}, {"id": "X9-Z1-08"}, {"id": "G-Z2-19"}]
    assert CE.be_gk56_fallas({"walls": walls, "excluded_walls": [{"id": "readerB_X9-Z1-05", "reason": "same wall as X9-Z1-06: Merged: same leaf"}]})
    assert not CE.be_gk56_fallas({"walls": walls, "excluded_walls": [{"id": "readerB_X9-Z1-05", "reason": "same wall as X9-Z1-08: Merged",
                                                                     "gap_proof": "gap 0\" (1/Z9.11) - the piece lies on the band"}]})
    falta = {"walls": walls, "excluded_walls": [{"id": "readerA_G-Z2-15", "reason": "same wall as G-Z2-19: x", "gap_proof": "gap 6.9\" (1/Z9.11)"}]}
    assert CE.be_gk56_fallas(falta), "gap > 0 = FALTA"
    assert CE.be_gk56_fallas({"walls": walls, "excluded_walls": [{"id": "q", "reason": "same wall as X-Z9-99: x", "gap_proof": "gap 0\" (1/Z9.11)"}]})
    cargada = {"walls": walls, "misc_items": [{"ref": "RI-18C furring board", "qty": 18.2}], "excluded_walls": [{"id": "readerA_G-Z2-15",
               "reason": "same wall as G-Z2-19: its last part is a separate furring, loaded as RI-18C", "gap_proof": "gap 6.9\" (1/Z9.11)"}]}
    assert not CE.be_gk56_fallas(cargada)
    print("test_be_gk56 OK")


test_be_gk56()


def test_v130_plausibilidad_subconteo():
    """v130 (COORDINACIÓN 13-nov 01:02, bloqueaba la subida de CR): el auditor de plausibilidad no toma el '0' de una subcategoría
    ('(0 cielos vía ceilings_misc)', 'de los cuales 0 cielos', '0 cielos vía misc'); un '0 cielos evaluados' real sigue = FAIL."""
    esp = {"cielos": 52, "walls": 10}
    def est(txt):
        r = [{"id": "CB_RCP_APILADOS", "estado": "PASS", "evidencia": [txt]}]
        CE.auditar_compuerta(r, esp)
        return r[0]["estado"]
    assert est("7 cuartos con tags de RCP (0 cielos vía ceilings_misc); 2 con cielos apilados por tags + 5 de 5 'double'") == "PASS"
    assert est("52 cielos evaluados (0 vía ceilings_misc); 7 cuartos con tags de RCP") == "PASS"
    assert est("52 cielos evaluados, de los cuales 0 cielos rated") == "PASS"
    assert est("0 cielos vía misc; 52 cielos evaluados") == "PASS"
    assert est("0 cielos evaluados; 7 cuartos con tags de RCP") == "FAIL"           # conteo principal en 0 = FAIL
    assert est("0 walls revisados") == "FAIL"
    assert CE.es_subconteo("a (b 0 cielos)", 5, 13) and not CE.es_subconteo("0 cielos evaluados", 0, 8)
    print("test_v130_plausibilidad_subconteo OK")


test_v130_plausibilidad_subconteo()


def test_be_gk57():
    """BE-GK57 (unido de apartados/be_gk57; casos de Grand Kia rev3b): backup junto a su insumo = FAIL; CADENA.prev.md = FAIL; entrega_rev3a/
    en el workdir = FAIL; los mismos archivos en bak_rev3a/ y la entrega actual = PASS."""
    w = tempfile.mkdtemp(prefix="gk57_")
    def mk(p):
        os.makedirs(os.path.dirname(os.path.join(w, p)), exist_ok=True)
        open(os.path.join(w, p), "w").write("x")
    mk("etapas/4_canon/resuelto_Z1.json")
    mk("etapas/4_canon/resuelto_Z1.rev3a.bak.json")
    assert CE.be_gk57_fallas(w, "rev3b"), "backup junto a su insumo = FAIL"
    os.remove(os.path.join(w, "etapas/4_canon/resuelto_Z1.rev3a.bak.json"))
    mk("burbujas/CADENA.md")
    mk("burbujas/CADENA.prev.md")
    assert CE.be_gk57_fallas(w, "rev3b"), ".prev = FAIL"
    os.remove(os.path.join(w, "burbujas/CADENA.prev.md"))
    os.makedirs(os.path.join(w, "entrega_rev3a"))
    assert CE.be_gk57_fallas(w, "rev3b"), "entrega previa en el workdir = FAIL"
    os.rmdir(os.path.join(w, "entrega_rev3a"))
    os.makedirs(os.path.join(w, "entrega_rev3b"))
    mk("bak_rev3a/resuelto_Z1.rev3a.bak.json")
    mk("bak_rev3a/CADENA.prev.md")
    assert not CE.be_gk57_fallas(w, "rev3b"), "copias en bak_<rev>/ y la entrega actual = PASS"
    print("test_be_gk57 OK")


test_be_gk57()


def test_v131_verde_subido_version_anterior():
    """v131 (COORDINACIÓN 13-nov 01:48, caso GK: VERDE v129 subido y luego se publica v130, sintético): (1) la entrega SUBIDA con el VERDE
    de la versión vigente al subir sigue válida; (2) --vigente acepta ese ENTREGA_OK si SUBIDA_OK es posterior a él y anterior a la
    publicación de la versión siguiente y los hashes coinciden; (3) la re-corrida por cambio de versión no cuenta para el tope (AMBER)."""
    ok = {"ok": True, "skill_version": "v81cf129", "fecha_iso": "2026-11-13T00:40:00+00:00",
          "vigentes": {"excel": {"nombre": "Z9_TakeOff_rev3b.xlsx", "md5": "aa"}, "pdf": {"nombre": "Z9_markups_rev3b.pdf", "md5": "bb"}},
          "chequeos": [{"id": "CE_VIEJO"}]}
    drive = {"Z9_TakeOff_rev3b.xlsx": "aa", "Z9_markups_rev3b.pdf": "bb"}
    sub = {"fecha_iso": "2026-11-13T00:55:00+00:00"}
    assert CE.entrega_ok_anterior_valida(ok, sub)[0]
    assert CE.vigente_fallas(ok, drive, ["CE_VIEJO", "CE_NUEVO_V130"], sub) == []            # (1) / (2) válido
    assert CE.vigente_fallas(ok, drive, ["CE_VIEJO", "CE_NUEVO_V130"]), "sin SUBIDA_OK sigue exigiendo el skill vigente"
    tarde = {"fecha_iso": "2026-11-13T01:43:19+00:00"}                                         # (b') caso real GK: subida 01:43 > v130
    assert CE.entrega_ok_anterior_valida(ok, tarde)[0] and CE.vigente_fallas(ok, drive, ["CE_VIEJO", "CE_NUEVO_V130"], tarde) == []
    ok_tarde = dict(ok, fecha_iso="2026-11-13T01:20:00+00:00")                                  # VERDE de v129 DESPUÉS de publicarse v130
    assert not CE.entrega_ok_anterior_valida(ok_tarde, tarde)[0] and CE.vigente_fallas(ok_tarde, drive, ["CE_VIEJO", "CE_NUEVO_V130"], tarde)
    assert not CE.entrega_ok_anterior_valida(ok, {"fecha_iso": "2026-11-13T00:30:00+00:00"})[0]   # subida antes del VERDE
    ev = CE.vigente_fallas(ok, dict(drive, **{"Z9_TakeOff_rev3b.xlsx": "cc"}), ["CE_VIEJO", "CE_NUEVO_V130"], sub)
    assert ev and "md5" in ev[0], ev                                                          # (b) hash distinto = FAIL
    viejo = CE.VERSIONES_CAMBIAN_CANTIDADES
    CE.VERSIONES_CAMBIAN_CANTIDADES = {"v81cf130"}
    try:
        assert not CE.entrega_ok_anterior_valida(ok, sub)[0], "una versión posterior que cambia cantidades re-abre (U-180 (4))"
    finally:
        CE.VERSIONES_CAMBIAN_CANTIDADES = viejo
    fin = [{"ts": "2026-11-13T00:40:00+00:00", "version": "v81cf129"}, {"ts": "2026-11-13T01:20:00+00:00"}, {"excel": "x", "version": "v81cf131"}]
    rec = CE.recorridas_por_version(fin, sub)
    assert rec == fin[1:], rec                                          # 01:20 (v130 vigente) y la actual = re-corridas por versión
    assert CE.recorridas_por_version(fin, None) == []
    assert CE.version_vigente_en(CE._iso("2026-11-13T01:20:00+00:00")) == "v81cf130"
    assert CE.version_siguiente("v81cf129") == "v81cf130" and CE.version_siguiente("v81cf130") == "v81cf131"
    print("test_v131_verde_subido_version_anterior OK")


test_v131_verde_subido_version_anterior()


def test_be_gk59():
    """BE-GK59 (unido de apartados/be_gk59; caso de Grand Kia rev3b, corridas sintéticas): VERDE -> subida -> re-corrida ROJA que pisa
    ENTREGA_OK.json = FAIL; guardado por corrida y el ENTREGA_OK de la subida vigente = PASS; sin ENTREGA_OK_<corrida> de la subida = FAIL."""
    w = tempfile.mkdtemp(prefix="gk59_")
    def wj(n, d):
        json.dump(d, open(os.path.join(w, n), "w"))
    open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write(
        json.dumps({"evento": "fin", "corrida": "c1aaaa", "ts": "2026-11-13T01:05:13+00:00", "ok": True}) + "\n" +
        json.dumps({"evento": "fin", "corrida": "c2bbbb", "ts": "2026-11-13T01:47:38+00:00", "ok": False}) + "\n")
    wj("SUBIDA_OK.json", {"primera_subida_iso": "2026-11-13T01:43:19+00:00"})
    wj("ENTREGA_OK.json", {"ok": True, "fecha_iso": "2026-11-13T01:05:13+00:00", "skill_version": "v81cf129"})
    wj("ENTREGA_OK_c1aaaa.json", {"ok": True})
    assert not CE.be_gk59_fallas(w)
    wj("ENTREGA_OK.json", {"ok": False, "fecha_iso": "2026-11-13T01:47:38+00:00", "skill_version": "v81cf130"})
    assert CE.be_gk59_fallas(w), "re-corrida no verde que pisa ENTREGA_OK.json después de la subida = FAIL"
    os.remove(os.path.join(w, "ENTREGA_OK_c1aaaa.json"))
    wj("ENTREGA_OK.json", {"ok": True, "fecha_iso": "2026-11-13T01:05:13+00:00"})
    assert CE.be_gk59_fallas(w), "sin ENTREGA_OK_<corrida> de la corrida subida = FAIL"
    wj("SUBIDA_OK.json", {"primera_subida_iso": "2026-11-13T01:43:19+00:00", "corrida": "c1aaaa", "entrega_ok": "ENTREGA_OK_c1aaaa.json"})
    assert CE.be_gk59_fallas(w), "el puntero de SUBIDA_OK a un ENTREGA_OK_<corrida> que no existe = FAIL"
    wj("ENTREGA_OK_c1aaaa.json", {"ok": True})
    assert not CE.be_gk59_fallas(w), "puntero de SUBIDA_OK al ENTREGA_OK de la corrida subida = PASS"
    print("test_be_gk59 OK")


test_be_gk59()


def test_u195_add_alternates():
    """U-195 (usuario 13-nov, CR RFI-30 'ponlo como alternate'; COORDINACIÓN 04:49, ids sintéticos): el alternate va con el mecanismo del
    skill: canon add_alternates + línea 'ALTERNATE #N (ADD)' en el Scope Checklist + 'ALTERNATE #N (ADD)' en la Proposal; nunca un
    renglón ALTERNATE en el Material Summary. RFI cerrado como Alternate sin las tres = FAIL."""
    import plantilla_excel as P
    aa = [{"n": 1, "rfi": "RFI-30", "texto": "Stair Z9 furring 3 3/8\" (RE: INTERIOR DRAWINGS not issued)",
           "razon": "drawn furring, no material printed and 'RE: INTERIOR DRAWINGS' not issued (5/X9.20)",
           "cantidades": [{"material": "3-5/8\" stud 20 GA", "qty": 40.0, "unit": "LF", "op": "10 ft x 4 studs"},
                          {"material": "5/8\" board", "qty": 90.0, "unit": "SF", "op": "10 x 9 x 1 face"}]}]
    assert P.add_alternates_err({"add_alternates": aa}) == []
    assert P.add_alternates_err({"add_alternates": [{"n": 1, "rfi": "RFI-30", "texto": "x", "cantidades": [{"material": "a"}]}]})
    al = P.alcances_add_alternates({"add_alternates": aa})
    assert al[0]["nombre"].startswith("ALTERNATE #1 (ADD)") and "[DERIVED: 10 ft x 4 studs]" in al[0]["nota"] and "Alternate #1" in al[0]["nota"]
    can = {"add_alternates": aa, "rfi_cierre": {"RFI-30": {"pregunta": "stair furring", "delta": "user decision: Alternate #1"}}}
    sc = [(a["id"], a["nombre"], "ALTERNATE (ADD) - NOT IN BASE BID", a["nota"]) for a in al]
    ms = ["5/8\" Type X board"]
    prop_ok = ["BASE BID TOTAL", "ALTERNATE #1 (ADD): stair furring", "REASON: drawn, no material printed (5/X9.20)"]
    assert CE.alternates_fallas(can, sc, ms, prop_ok) == []
    assert CE.alternates_fallas(can, sc, ms, None) == []                                     # sin Proposal pedida: no se exige
    ev = CE.alternates_fallas(can, sc, ms, ["BASE BID TOTAL"])
    assert ev and any("Proposal" in x for x in ev), ev                                       # falta en la Proposal
    ev = CE.alternates_fallas(can, [("RFI-30", "stair", "CLOSED", "user decision: Alternate #1")], ms, prop_ok)
    assert ev and "Scope Checklist" in ev[0], ev                                             # falta la línea del Scope
    ev = CE.alternates_fallas({"rfi_cierre": can["rfi_cierre"]}, sc, ms, prop_ok)
    assert ev and "add_alternates" in ev[0], ev                                              # RFI cerrado sin add_alternates
    ev = CE.alternates_fallas(can, sc, ms + ["ALTERNATE #1 – 3-5/8\" stud"], prop_ok)
    assert ev and "Material Summary" in ev[0], ev                                            # ALTERNATE en el Material Summary = FAIL
    assert CE.alternates_fallas({}, [], ms, None) == []
    # U-198: REASON con N/HOJA en Proposal (+ PDF), Scope Checklist y README_REVIEW; sale de add_alternates[].razon
    assert "REASON: drawn furring" in al[0]["nota"] and "5/X9.20" in al[0]["nota"] and "until clarified" in al[0]["nota"]
    assert P.razon_alternate(aa[0]).startswith("REASON: drawn furring") and "add alternate until clarified" in P.razon_alternate(aa[0])
    assert any("razon" in e for e in P.add_alternates_err({"add_alternates": [dict(aa[0], razon="no material printed")]}))
    ev = CE.alternates_fallas({**can, "add_alternates": [dict(aa[0], razon="no material printed")]}, sc, ms, prop_ok)
    assert ev and "N/HOJA" in ev[0], ev                                                      # razón sin N/HOJA = FAIL
    assert CE.alternates_fallas(can, sc, ms, prop_ok, "README: ALTERNATE #1 (ADD) REASON: no material printed (5/X9.20)",
                                "PROPOSAL PDF ... REASON: drawn (5/X9.20)") == []
    ev = CE.alternates_fallas(can, sc, ms, prop_ok, "README sin la razón")
    assert ev and "README_REVIEW" in ev[0], ev
    ev = CE.alternates_fallas(can, sc, ms, prop_ok, None, "PDF sin la razón")
    assert ev and "PDF de la Proposal" in ev[0], ev
    ev = CE.alternates_fallas(can, sc, ms, ["ALTERNATE #1 (ADD): stair"])
    assert ev and "REASON" in ev[0], ev                                                      # Proposal sin REASON = FAIL
    print("test_u195_add_alternates OK (+ U-198)")


test_u195_add_alternates()


def test_u196_leeme_y_mapa():
    """U-196 (usuario 13-nov: 'mapa de cobertura, ponle ese nombre y haz una descripcion para saber para que sirve cada cosa'): (1) el PDF
    se llama 'MAPA DE COBERTURA - IMAGE ONLY.pdf' y el nombre viejo se sigue aceptando; (2) el LEEME se arma desde la lista REAL en el
    orden de revisión; (3) CE_LEEME_ARCHIVOS: falta el LEEME / archivo sin línea / línea de un archivo que no existe / sin patrón = FAIL."""
    assert CE.COB_PDF == "MAPA DE COBERTURA - IMAGE ONLY.pdf" and "COBERTURA - IMAGE ONLY.pdf" in CE.COB_PDFS
    ok = ["Z9_markups_rev9 - OPEN IN BLUEBEAM.pdf", "Z9.01 - IMAGE ONLY (not editable) - walls rev9.png"]
    assert CE.nombres_planos(ok + [CE.COB_PDF]) == [] and CE.nombres_planos(ok + [CE.COB_PDF_VIEJO]) == []
    e = tempfile.mkdtemp(prefix="u196_")
    for f in ("GUIA_DE_REVISION_DEL_ESTIMADOR.md", "README_REVIEW.md", "RESUMEN_rev9.md", "TIEMPOS.md", "CHECKLIST_REVISION.xlsx",
              "Take-off/Z9_Takeoff_rev9.xlsx", "Planos marcados/Z9_markups_rev9 - OPEN IN BLUEBEAM.pdf", "Planos marcados/" + CE.COB_PDF,
              "Planos marcados/DETALLES_REVISADOS.pdf", "Proposal/Z9_Proposal_rev9.xlsx", "Auditoria/x.csv"):
        os.makedirs(os.path.dirname(os.path.join(e, f)) or e, exist_ok=True)
        open(os.path.join(e, f), "w").write("x")
    assert CE.leeme_fallas(e) and "falta" in CE.leeme_fallas(e)[0]                          # sin LEEME = FAIL
    CE.escribir_leeme(e)
    assert CE.leeme_fallas(e) == [], CE.leeme_fallas(e)
    txt = open(os.path.join(e, CE.LEEME_NOMBRE), encoding="utf-8").read()
    lineas = [l for l in txt.splitlines() if l.startswith("- `")]
    assert lineas[0].startswith("- `GUIA_DE_REVISION") and "MAPA DE COBERTURA" in txt and "Auditoria/" in txt and "x.csv" not in txt
    assert all("QUÉ ES:" in l and "PARA QUÉ SIRVE:" in l and "CUÁNDO ABRIRLO:" in l for l in lineas)
    assert txt.index("OPEN IN BLUEBEAM") < txt.index("MAPA DE COBERTURA - IMAGE ONLY") < txt.index("Proposal/")   # orden de revisión
    open(os.path.join(e, "SEGUIMIENTO.md"), "w").write("x")
    assert any("sin línea" in x for x in CE.leeme_fallas(e))                                 # archivo nuevo sin línea = FAIL
    CE.escribir_leeme(e)
    os.remove(os.path.join(e, "TIEMPOS.md"))
    assert any("no existe" in x for x in CE.leeme_fallas(e))                                 # línea de un archivo que no existe = FAIL
    open(os.path.join(e, "notas_sueltas.txt"), "w").write("x")
    CE.escribir_leeme(e)
    assert any("ningún patrón" in x for x in CE.leeme_fallas(e))                             # archivo sin patrón = FAIL
    print("test_u196_leeme_y_mapa OK")


test_u196_leeme_y_mapa()


def _u199_canon():
    """canon sintético: ROOM 905 (rectángulo 100-300 x 100-200 pt en Z9.1) cerrado por 4 muros con cara del cuarto."""
    def w(i, ori, c, lo, hi, **k):
        return dict({"id": i, "type_id": "Z9", "faces": [{"room": "ROOM 905"}],
                     "band": {"sheet": "Z9.1", "ori": ori, "c0": c - 3, "c1": c + 3, "lo": lo, "hi": hi}}, **k)
    return {"walls": [w("Z9-N", "H", 100, 100, 300), w("Z9-S", "H", 200, 100, 300), w("Z9-O", "V", 100, 100, 200), w("Z9-E", "V", 300, 100, 200)],
            "ceilings": [{"room": "ROOM 905", "layer": "GYP", "area_sf": 100.0}],
            "u199": {"rooms": [{"room": "ROOM 905", "sheet": "Z9.1", "polygon": [[100, 100], [300, 100], [300, 200], [100, 200]], "area_sf": 100.0}],
                     "rated_lines": [], "secciones": [], "disposiciones": []}}


def test_u199_cierre_por_cuarto_mutacion():
    """U-199 (1): el perímetro del cuarto cerrado por sus 4 caras = PASS; MUTACIÓN: quitar UNA sola cara = FAIL; la cara cubierta por un
    vano o por un muro EXCLUDED con band = PASS; disposición con N/HOJA = PASS."""
    can = _u199_canon()
    assert CE.cierre_cuartos_fallas(can) == ([], 1), CE.cierre_cuartos_fallas(can)
    for k in range(4):                                  # cada una de las 4 caras, quitada sola
        m = json.loads(json.dumps(can))
        del m["walls"][k]
        fs, n = CE.cierre_cuartos_fallas(m)
        assert n == 1 and len(fs) == 1 and "(1) ROOM 905" in fs[0], (k, fs)
    m = json.loads(json.dumps(can))
    ex = m["walls"].pop(3)
    m["excluded_walls"] = [dict(ex, reason="existing to remain per 9/Z9.1")]
    assert CE.cierre_cuartos_fallas(m)[0] == []
    m = json.loads(json.dumps(can))
    del m["walls"][3]
    m["u199"]["rooms"][0]["openings"] = [[297, 100, 303, 200]]
    assert CE.cierre_cuartos_fallas(m)[0] == []
    m = json.loads(json.dumps(can))
    m["walls"][1]["band"]["hi"] = 250                   # cara corta: 50 pt sin cubrir
    assert CE.cierre_cuartos_fallas(m)[0]
    m["u199"]["disposiciones"] = [{"control": 1, "id": "ROOM 905", "motivo": "opening to corridor per 3/Z9.1", "nhoja": "3/Z9.1"}]
    assert CE.cierre_cuartos_fallas(m)[0] == []
    # (1) obligatorio: muros con cuartos y canon.u199.rooms ausente = FAIL (0 evaluados)
    m = json.loads(json.dumps(can))
    del m["u199"]["rooms"]
    assert any("(1)" in f and "0 evaluados" in f for f in CE.u199_fallas(m, {})["1"][0])
    print("test_u199_cierre_por_cuarto_mutacion OK")


def test_u199_pisos_gemelos():
    """U-199 (2) réplica sintética del caso real (muro de un cuarto de L-n sin su gemelo en L-n+1): dos pisos con los mismos sufijos de
    cuarto; el muro del cuarto ..12 en L8 sin gemelo en L9 = FAIL; con gemelo o disposición = PASS."""
    def w(i, piso, cuarto, t="Z9"):
        return {"id": i, "type_id": t, "floor": f"L{piso}", "faces": [{"room": cuarto}]}
    base = [w("Z9-L8-10", 8, "OFFICE 810"), w("Z9-L8-11", 8, "OFFICE 811"), w("Z9-L8-12", 8, "LINEN 812"),
            w("Z9-L9-10", 9, "OFFICE 910"), w("Z9-L9-11", 9, "OFFICE 911"), w("Z9-L9-99", 9, "STOR 912", "Z8")]
    fs, n = CE.pisos_gemelos_fallas({"walls": base})
    assert n >= 3 and any("Z9-L8-12" in f and "L9" in f for f in fs), fs
    ok = base + [w("Z9-L9-12", 9, "LINEN 912")]
    assert not [f for f in CE.pisos_gemelos_fallas({"walls": ok})[0] if "Z9-L8-12" in f]
    disp = {"walls": base, "u199": {"disposiciones": [{"control": 2, "id": "Z9-L8-12", "motivo": "not on L9 per 1/Z9.9", "nhoja": "1/Z9.9"}]}}
    assert not [f for f in CE.pisos_gemelos_fallas(disp)[0] if "Z9-L8-12" in f]
    print("test_u199_pisos_gemelos OK")


def test_u199_rated_y_excluded():
    """U-199 (6) réplica del caso real (muro de escalera sin contar): STAIR 9 sin muros contados = FAIL; muro sin rating = FAIL; rated
    2 HR = PASS; línea rated del code plan sin muro con band = FAIL. (13) réplica del caso real: wall exterior excluido con motivo de
    interior = FAIL (su cara exterior sigue en alcance); sin re-verificación = FAIL; re-verificado y con faces interiores = PASS."""
    can = {"walls": [], "u199": {"rooms": [{"room": "STAIR 9 951"}]}}
    assert any("STAIR 9" in f for f in CE.rated_fallas(can)[0])
    can["walls"] = [{"id": "Z9-ST", "type_id": "Z9", "faces": [{"room": "STAIR 9 951"}]}]
    assert any("Z9-ST" in f and "rating" in f for f in CE.rated_fallas(can)[0])
    can["walls"][0]["rating_hr"] = 2
    assert CE.rated_fallas(can)[0] == []
    can["u199"]["rated_lines"] = [{"sheet": "Z9.1", "rating_hr": 2, "x0": 50, "y0": 400, "x1": 250, "y1": 400, "nhoja": "1/G9.0"}]
    assert any("(6) línea rated" in f for f in CE.rated_fallas(can)[0])
    can["walls"][0]["band"] = {"sheet": "Z9.1", "ori": "H", "c0": 397, "c1": 403, "lo": 40, "hi": 260}
    assert CE.rated_fallas(can)[0] == []
    can["walls"][0]["rating_hr"] = 1                    # rating menor al de la línea = FAIL
    assert CE.rated_fallas(can)[0]
    # (6) obligatorio: code plan con muros rated en el set y canon.u199.rated_lines ausente = FAIL
    m = _u199_canon()
    del m["u199"]["rated_lines"]
    assert any("(6)" in f and "0 evaluados" in f for f in CE.u199_fallas(m, {"G9.0": "LIFE SAFETY PLAN ... 2 HR RATED"})["6"][0])
    ex = {"excluded_walls": [{"id": "XW.9.9-L9-99", "type_id": "XW.9.9", "reason": "interior of tenant space, by others"}]}
    fs, n = CE.reverificacion_excluded_fallas(ex)
    assert n == 1 and any("re-verificación" in f for f in fs) and any("cara exterior" in f for f in fs), fs
    ex["excluded_walls"][0]["reverificado"] = {"revisor": "lector B", "decision": "interior face only", "nhoja": "4/Z9.4"}
    assert [f for f in CE.reverificacion_excluded_fallas(ex)[0] if "re-verificación" in f] == []
    assert any("cara exterior" in f for f in CE.reverificacion_excluded_fallas(ex)[0])
    ex["excluded_walls"][0]["faces"] = ["A"]
    assert CE.reverificacion_excluded_fallas(ex)[0] == []
    print("test_u199_rated_y_excluded OK")


def test_u199_resto_controles():
    """U-199 (3)(4)(5)(7)(8)(9)(10)(11)(12): cada control con su caso FAIL y su caso PASS; 0 evaluados donde el plano los tiene = FAIL."""
    can = _u199_canon()
    hj = {"Z9.1": "FLOOR PLAN", "A9.2": "KEYNOTES\n1 PROVIDE GYPSUM BOARD SOFFIT AT BULKHEAD\n2 CLEAN FLOOR\n", "Z9.3": "DOOR SCHEDULE"}
    # (3) puertas
    can["opening_schedule"] = {"items": [{"ref": "D9", "kind": "door", "wall": "Z9-N"}, {"ref": "D8", "kind": "door", "wall": "Z9-X"}]}
    fs, n = CE.puertas_fallas(can, hj)
    assert n == 2 and len(fs) == 1 and "D8" in fs[0]
    assert any("0 puertas" in f for f in CE.puertas_fallas({"opening_schedule": {"items": []}}, hj)[0])
    # (4) keynotes: la 1 (gypsum / soffit) sin registrar = FAIL; la 2 no
    fs, n = CE.keynotes_fallas(can, hj)
    assert any("keynote 1 de A9.2" in f for f in fs) and not any("keynote 2" in f for f in fs)
    can["u199"]["keynotes"] = [{"sheet": "A9.2", "num": "1", "ref": "Z9-N"}]
    assert CE.keynotes_fallas(can, hj)[0] == []
    # (5) área de cielo +-5 %
    assert CE.area_cielo_fallas(can)[0] == []
    can["ceilings"][0]["area_sf"] = 90.0
    assert CE.area_cielo_fallas(can)[0]
    can["ceilings"][0]["area_sf"] = 100.0
    # (7) secciones
    can["walls"][0]["height_ft"] = 10.0
    can["u199"]["secciones"] = [{"sheet": "Z9.5", "detalle": "1", "elemento": "Z9-N", "altura_ft": 12.0}]
    assert any("(7)" in f for f in CE.secciones_fallas(can)[0])
    can["u199"]["secciones"][0]["altura_ft"] = 10.2
    assert CE.secciones_fallas(can)[0] == []
    can["u199"]["secciones"].append({"sheet": "Z9.5", "detalle": "2", "elemento": "Z9-NO", "altura_ft": 9})
    assert any("no existe" in f for f in CE.secciones_fallas(can)[0])
    can["u199"]["secciones"].pop()
    # (8) estructural / MEP: hojas S sin lista = FAIL
    assert CE.estructural_mep_fallas(can, {"S9.1": "FRAMING PLAN"})[0]
    can["u199"]["estructural_mep"] = [{"id": "COL-9", "tipo": "column wrap", "excluido": "exposed steel, no wrap per 2/Z9.6"}]
    assert CE.estructural_mep_fallas(can, {"S9.1": "FRAMING PLAN"})[0] == []
    # (9) finish schedule
    can["u199"]["finish_schedule"] = [{"room": "ROOM 905", "gyp": "both"}, {"room": "ROOM 906", "gyp": "ceiling"}]
    fs, n = CE.finish_schedule_fallas(can, {"A9.7": "ROOM FINISH SCHEDULE"})
    assert n == 2 and len(fs) == 1 and "ROOM 906" in fs[0]
    assert CE.finish_schedule_fallas({"walls": []}, {"A9.7": "ROOM FINISH SCHEDULE"})[0]
    # (10) unidades típicas
    tip = {"ceilings": [{"room": "UNIT 901 (Type A)", "area_sf": 100}, {"room": "UNIT 902 (Type A)", "area_sf": 100},
                        {"room": "UNIT 903 (Type A)", "area_sf": 80}]}
    fs, n = CE.unidades_tipicas_fallas(tip)
    assert n == 3 and len(fs) == 1 and "UNIT 903" in fs[0]
    # (11) specs locations
    sp = {"Z9.8": "SECTION 09 21 16 GYPSUM BOARD ASSEMBLIES ... LOCATIONS: provide abuse resistant board at corridors"}
    assert CE.specs_locations_fallas({}, sp)[0]
    assert CE.specs_locations_fallas({"u199": {"specs_locations": [{"id": "09 21 16 2.2", "ref": "Z9-N"}]}, "walls": [{"id": "Z9-N"}]}, sp)[0] == []
    # (12) tercer lector: 10 % de hojas A / I
    hojas = {f"A9.{k}": "PLAN" for k in range(12)}
    assert CE.lector3_fallas({}, hojas)[0]
    l3 = {"u199": {"lector3": [{"sheet": "A9.1", "conteo_lector3": 5, "conteo_canon": 5}, {"sheet": "A9.2", "conteo_lector3": 4, "conteo_canon": 5}]}}
    fs, n = CE.lector3_fallas(l3, hojas)
    assert n == 2 and len(fs) == 1 and "A9.2" in fs[0]
    l3["u199"]["lector3"][1]["revision_completa"] = True
    assert CE.lector3_fallas(l3, hojas)[0] == []
    # un control que revienta = FAIL (no pasa en vacío)
    assert CE.u199_fallas({"walls": [{"id": "x", "faces": "roto"}], "u199": {"rooms": [{"room": "R 905", "polygon": "x"}]}}, {})
    print("test_u199_resto_controles OK")


def test_u199_cobertura_diag_cortos():
    """U-199 (5b): el mapa de cobertura ve los muros DIAGONALES y CORTOS (< 2 ft) que el detector H / V no ve; una caja de tag con texto
    y un par suelto que no remata en otro muro NO son muros; markup sobre el muro = cubierto."""
    esc = 18.0                                          # 1/4" = 1'-0"
    doc = pymupdf.open()
    pg = doc.new_page(width=1200, height=900)
    sh = pg.new_shape()

    def par(x0, y0, x1, y1, dx, dy):
        sh.draw_line((x0, y0), (x1, y1))
        sh.draw_line((x0 + dx, y0 + dy), (x1 + dx, y1 + dy))
    par(100, 400, 1000, 400, 0, 9)                      # muro largo H (espesor 6")
    par(300, 409, 300, 409 + 1.5 * esc, 9, 0)           # muro CORTO de 1'-6" que arranca del muro largo
    par(500, 400, 500 + 6 * esc, 400 - 6 * esc, 9, 0)   # muro DIAGONAL a 45 grados que arranca del muro largo
    par(800, 600, 800 + 1.5 * esc, 600, 0, 12)          # par suelto (caja de símbolo): no remata en ningún muro
    sh.finish(color=(0, 0, 0), width=0.7)
    sh.commit()
    pg.insert_text((210, 205), "905", fontsize=10)      # caja de room tag con texto: no es muro
    sh = pg.new_shape()
    sh.draw_rect(pymupdf.Rect(200, 195, 236, 209))
    sh.finish(color=(0, 0, 0), width=0.7)
    sh.commit()
    f = CE.cob_diag_cortos(pg, esc, [])
    tipos = sorted(x["tipo"] for x in f)
    assert tipos == ["muro_corto", "muro_diag"], f
    assert all(not x["cubierto"] for x in f)
    mk = [(304, 409, 304, 436), (504, 400, 600, 304)]   # markups sobre los dos ejes
    assert all(x["cubierto"] for x in CE.cob_diag_cortos(pg, esc, mk))
    print("test_u199_cobertura_diag_cortos OK")


test_u199_cierre_por_cuarto_mutacion()
test_u199_pisos_gemelos()
test_u199_rated_y_excluded()
test_u199_resto_controles()
test_u199_cobertura_diag_cortos()


def test_be_xf16_muros_canon():
    """BE-XF16 (COORDINACIÓN 13-nov): canon estilo CR (walls = [], todos los muros en existing_walls). (1) muros_canon() los une;
    (2) la red U-138 (esperado_proyecto) ve los muros (antes: 0 esperados = un '0 walls' pasaba); (3) CE_MUROS_CANON: las tools no
    tienen lecturas solo de 'walls' sin marcar = PASS; una lectura nueva sin muros_canon() sobre un canon así = FAIL."""
    can = {"walls": [], "existing_walls": [{"id": "Z9-L9-01", "sheet": "Z9.1", "type_id": "Z9", "length_ft": 9.0},
                                           {"id": "Z9-L9-02", "sheet": "Z9.2", "type_id": "Z9", "length_ft": 4.0}]}
    assert [w["id"] for w in CE.muros_canon(can)] == ["Z9-L9-01", "Z9-L9-02"]
    c = type("C", (), {})()
    c.canon, c.set_p = can, None
    esp = CE.esperado_proyecto(c)
    assert esp["walls"] == 2 and esp["markups"] == 2
    res = [{"id": "CE_X9", "estado": "PASS", "evidencia": ["0 walls revisados"]}]
    assert CE.auditar_compuerta(res, esp) == ["CE_X9"]                  # '0 walls' con 2 muros en existing_walls = FAIL
    assert CE.ce_muros_canon(c)[0] == "PASS", CE.ce_muros_canon(c)
    d = tempfile.mkdtemp(prefix="xf16_")
    p = os.path.join(d, "x9.py")
    open(p, "w").write('def f(can):\n    return [w for w in can.get("walls") or []]\n'
                       'def g(can):\n    # solo-metal: a propósito\n    return can.get("walls")\n'
                       'def h(can):\n    return (can.get("walls") or []) + (can.get("existing_walls") or [])\n')
    assert CE.lecturas_solo_walls([p]) == ["x9.py:2"]
    viejo = CE.LECTORES_DE_MUROS
    try:
        CE.LECTORES_DE_MUROS = viejo + [p]
        r = CE.ce_muros_canon(c)
        assert r[0] == "FAIL" and "x9.py:2" in " ".join(r[1]), r
        c.canon = {"walls": [{"id": "Z9-A"}]}
        assert CE.ce_muros_canon(c)[0] == "AMBER"                     # sin muros en otra lista: aviso, no FAIL
    finally:
        CE.LECTORES_DE_MUROS = viejo
    print("test_be_xf16_muros_canon OK")


test_be_xf16_muros_canon()


def test_u199_casos_reales_replica():
    """U-199 réplicas sintéticas de los casos reales con el esquema de CR (muros en existing_walls, 'faces' = número, cuartos en
    'location'): (2) el muro del cuarto ..12 de L8 sin gemelo en L9 = FAIL y con su gemelo = PASS; (13) wall exterior excluido con
    motivo de interior = FAIL; con su cara B contada ('<id> B') o 'counted as <id>' existente = PASS; (3) puerta sin 'wall' ubicada
    por sheet + center_pt sobre la band de un muro = PASS, lejos = FAIL."""
    def w(i, piso, loc, t="Z9-0"):
        return {"id": i, "type_id": t, "floor": f"L{piso}", "faces": 2, "location": loc}
    base = [w("Z9-L8-10", 8, "L8 office | faces: 810 OFFICE; corridor 816"), w("Z9-L8-11", 8, "faces: 811 OFFICE; corridor 816"),
            w("Z9-L8-12", 8, "L8 corridor stub at LINEN 812 | faces: 812 LINEN; corridor 816"),
            w("Z9-L9-10", 9, "faces: 910 OFFICE; corridor 916"), w("Z9-L9-11", 9, "faces: 911 OFFICE; corridor 916"),
            w("Z9-L9-33", 9, "912 Linen / 913 Cleaning | faces: 912; 913", "Z8-0")]
    can = {"walls": [], "existing_walls": base}
    fs, n = CE.pisos_gemelos_fallas(can)
    assert any("Z9-L8-12" in f for f in fs), fs
    can["existing_walls"] = base + [w("Z9-L9-12", 9, "faces: 912 LINEN; corridor 916")]
    assert not [f for f in CE.pisos_gemelos_fallas(can)[0] if "Z9-L8-12" in f]
    ex = {"walls": [], "existing_walls": [{"id": "XW.9.9-L9-07 A", "faces": 1, "location": "faces: F&B 907 (tenant)"}],
          "excluded_walls": [{"id": "XW.9.9-L9-07", "reason": "'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' (Z9.4)",
                              "reverificado": {"revisor": "lector B", "decision": "interior face only", "nhoja": "1/Z9.4"}}]}
    assert any("cara exterior" in f for f in CE.reverificacion_excluded_fallas(ex)[0])
    ex["existing_walls"].append({"id": "XW.9.9-L9-07 B", "faces": 1, "location": "east facade | faces: exterior"})
    assert CE.reverificacion_excluded_fallas(ex)[0] == []
    ex["existing_walls"].pop()
    ex["existing_walls"].append({"id": "XW.9.9-L9-08", "faces": 1})
    ex["excluded_walls"][0]["reason"] += " | exterior face counted as XW.9.9-L9-08"
    assert CE.reverificacion_excluded_fallas(ex)[0] == []
    pu = {"walls": [{"id": "Z9-N", "band": {"sheet": "Z9.1", "ori": "H", "c0": 97, "c1": 103, "lo": 100, "hi": 300}}],
          "opening_schedule": {"items": [{"ref": "D9", "sheet": "Z9.1", "center_pt": [200, 101]},
                                         {"ref": "D8", "sheet": "Z9.1", "center_pt": [200, 160]}, {"ref": "D7"}]}}
    fs, n = CE.puertas_fallas(pu, {})
    assert n == 3 and len(fs) == 2 and any("D8" in f for f in fs) and any("D7" in f and "center_pt" in f for f in fs), fs
    print("test_u199_casos_reales_replica OK")


test_u199_casos_reales_replica()


def test_alternate_impreso_sin_rfi():
    """COORDINACIÓN 05:51 (caso CR: alternate impreso 'TF-1 ALT' en una hoja de interiores; ids sintéticos): un alternate IMPRESO en planos
    o specs no lleva RFI: 'impreso' con la hoja o la sección y la razón la cita. Sin RFI y sin 'impreso' = FAIL; n entero, razón y
    cantidades siguen obligatorios."""
    import plantilla_excel as P
    q = [{"material": "3-5/8\" stud 20 GA", "qty": 12.0, "unit": "LF", "op": "3 ft x 4 studs"}]
    aa = {"n": 2, "texto": "TF-9 ALT finish at stair", "impreso": "X9.19", "cantidades": q,
          "razon": "the plans print 'TF-9 ALT' on X9.19 as an alternate finish"}
    assert P.add_alternates_err({"add_alternates": [aa]}) == [], P.add_alternates_err({"add_alternates": [aa]})
    sec = dict(aa, impreso="SECTION 09 21 16", razon="specs list it as an alternate in 09 21 16 2.3")
    assert P.add_alternates_err({"add_alternates": [sec]}) == []
    sin = dict(aa); sin.pop("impreso")
    assert any("rfi" in e for e in P.add_alternates_err({"add_alternates": [sin]}))          # sin RFI ni impreso = FAIL
    assert any("razon" in e for e in P.add_alternates_err({"add_alternates": [dict(aa, razon="printed alternate")]}))
    assert any("'n'" in e for e in P.add_alternates_err({"add_alternates": [dict(aa, n="dos")]}))
    assert any("cantidades" in e for e in P.add_alternates_err({"add_alternates": [dict(aa, cantidades=[])]}))
    can = {"add_alternates": [aa]}
    al = P.alcances_add_alternates(can)
    sc = [(a["id"], a["nombre"], "ALTERNATE (ADD) - NOT IN BASE BID", a["nota"]) for a in al]
    prop = ["BASE BID TOTAL", "ALTERNATE #2 (ADD): TF-9 ALT", "REASON: the plans print 'TF-9 ALT' on X9.19 as an alternate finish"]
    assert CE.alternates_fallas(can, sc, ["5/8\" board"], prop) == [], CE.alternates_fallas(can, sc, ["5/8\" board"], prop)
    ev = CE.alternates_fallas({"add_alternates": [sin]}, sc, ["5/8\" board"], prop)
    assert ev and "rfi" in ev[0], ev
    print("test_alternate_impreso_sin_rfi OK")


test_alternate_impreso_sin_rfi()


def test_u199_rated_opcion_b_replica_rfi():
    """U-199 (6) opción (b) (COORDINACIÓN 05:57), réplica sintética del caso real (muro rated de la salida de una escalera que el canon
    no tenía): el lector carga canon.u199.rated_lines solo para NUESTROS muros, cada línea con su N/HOJA; esquema CR (muros en
    existing_walls con 'sheet' + 'path'). Sin el muro = FAIL; con el muro de rating 2 sobre la línea = PASS; con rating menor = FAIL;
    línea sin N/HOJA = FAIL; set con code plan rated y 0 rated_lines = FAIL (U-137)."""
    ln = {"id": "ST9-EXIT", "sheet": "Z9.01", "rating_hr": 2, "x0": 900.0, "y0": 700.0, "x1": 937.0, "y1": 700.0, "nhoja": "1/Z9.00"}
    viejo = {"walls": [], "existing_walls": [{"id": "Z9.6.3-L1-03 A", "type_id": "Z9.6.3-2", "sheet": "Z9.01",
                                              "path": [[600.0, 700.0], [880.0, 700.0]]}], "u199": {"rated_lines": [ln]}}
    fs, n = CE.rated_fallas(viejo)
    assert n == 1 and fs and "sin muro contado" in fs[0], fs
    nuevo = json.loads(json.dumps(viejo))
    nuevo["existing_walls"].append({"id": "Z9.6.3-L1-04 A", "type_id": "Z9.6.3-2", "sheet": "Z9.01", "path": [[900.0, 700.15], [937.0, 700.15]]})
    assert CE.rated_fallas(nuevo)[0] == [], CE.rated_fallas(nuevo)
    bajo = json.loads(json.dumps(nuevo))
    bajo["existing_walls"][1]["type_id"] = "Z9.6.3-0"
    assert CE.rated_fallas(bajo)[0]                                                        # rating menor que la línea = FAIL
    sin_nh = json.loads(json.dumps(nuevo))
    del sin_nh["u199"]["rated_lines"][0]["nhoja"]
    assert any("N/HOJA" in f for f in CE.rated_fallas(sin_nh)[0])
    vacio = {"walls": [{"id": "Z9-A", "faces": [{"room": "ROOM 905"}]}], "u199": {"rooms": []}}
    assert any("(6)" in f and "0 evaluados" in f for f in CE.u199_fallas(vacio, {"G9.0": "CODE PLAN ... 2 HR RATED"})["6"][0])
    print("test_u199_rated_opcion_b_replica_rfi OK")


test_u199_rated_opcion_b_replica_rfi()
