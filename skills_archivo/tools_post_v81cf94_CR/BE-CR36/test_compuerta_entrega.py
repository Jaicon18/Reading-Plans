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

BLOQUES_OREILLY.append(('test_burbujas_oreilly', '#!/usr/bin/env python3\n"""test_burbujas_oreilly.py — U-137 / BE-139 (usuario 4-nov: "¿y qué pasó con los detail call outs?", burbuja "1" arriba /\n"A3.2" abajo). El detector de callouts solo veía "N/HOJA" escrito en una línea: en O\'Reilly (escaneo) encontraba 1 burbuja,\nen CFA y Chuze 0, y CE_CALLOUTS pasaba en vacío. Fixture: recorte REAL de la burbuja 1/A3.2 de A1.1 de O\'Reilly (escaneo\nde 400 dpi, recorte 80 x 80 pt a 250 dpi). (1) palabras_fitz.py (burbujas) la lee 1/A3.2; (2) compuerta_entrega texto la guarda en\nset_texto.json; (3) CE_CALLOUTS falla si no está citada y pasa citada; (4) la misma hoja sin la burbuja = 0 burbujas con\nhojas de detalles en el set = FAIL (PASS en vacío prohibido). Falla con v81cf32."""\nimport base64\nimport json\nimport os\nimport shutil\nimport sys\nimport tempfile\n\nimport pymupdf\n\nAQUI = os.path.dirname(os.path.abspath(__file__))\nsys.path.insert(0, AQUI)\nimport palabras_fitz as burbujas  # noqa: E402  (detector de burbujas, U-137)\nimport chequeos_biblioteca as CB  # noqa: E402\nimport compuerta_entrega as CE  # noqa: E402\n\nPNG = base64.b64decode("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")\nHOJAS = ["A1.1", "A2.1", "A3.1", "A3.2", "A3.3", "A3.4", "A4.1", "A4.2", "A5.1", "A5.2"]\nif not shutil.which("tesseract"):\n    print("(sin tesseract: no se puede probar el detector raster)")\n    sys.exit(0)\nd = pymupdf.open()\np = d.new_page(width=80, height=80)\np.insert_image(p.rect, stream=PNG)\nr = burbujas.detectar(p, HOJAS)\nassert [(b["n"], b["hoja"]) for b in r["burbujas"]] == [("1", "A3.2")], r\n# hoja de 1 página con la burbuja (rótulo A1.1) + hoja de detalles A3.2 -> set_texto con burbujas\nw = tempfile.mkdtemp()\ndoc = pymupdf.open()\npg = doc.new_page(width=600, height=400)\npg.insert_image(pymupdf.Rect(260, 160, 340, 240), stream=PNG)\ndoc.new_page(width=600, height=400).insert_text((50, 50), "WALL SECTIONS  1  2  3   A3.2", fontsize=12)\ndoc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1},\n                     {"startpage": 1, "prefix": "A3.2", "style": "", "firstpagenum": 1}])\npdf = os.path.join(w, "set.pdf")\ndoc.save(pdf)\nsal = os.path.join(w, "set_texto.json")\nCE.texto_set([pdf], sal)\nst = json.load(open(sal))\nassert [(b["n"], b["hoja"]) for b in st["burbujas"]["A1.1"]["burbujas"]] == [("1", "A3.2")], st["burbujas"]\ncn = {"walls": [{"id": "S43-1", "tag": "S43", "sheet": "A1.1", "element": "wall", "length_ft": 10, "height_ft": 10}]}\nsm = {k: st.get(k) for k in ("ocr", "en_blanco", "sin_texto", "burbujas")}\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm, celdas=[]))\nassert e == "FAIL" and any("1/A3.2 (burbuja en A1.1" in x for x in ev), ev\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm,\n                            celdas=[("Partition Takeoff", "J6", "1/A3.2 studs to PEMB purlin")]))\nassert e in ("PASS", "AMBER"), ev\n# la misma hoja SIN la burbuja: 0 burbujas y el set tiene hojas de detalles -> FAIL (antes pasaba en vacío)\nsm0 = dict(sm, burbujas={"A1.1": {"burbujas": [], "sin_leer": [], "circulos": 0}})\ne, ev = CB.ce_callouts(CB.B(hojas=st["hojas"], canon=cn, set_meta=sm0, celdas=[]))\nassert e == "FAIL" and "PASS en vacío prohibido" in ev[0], ev\nprint("OK test_burbujas_oreilly")\n'))

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


def test_be_cr36_textos_markups():
    """BE-CR36 (CR rev19, U-187): LEGEND - una celda larga cabe en su columna; EXCLUDED de dos cuartos vecinos no se enciman."""
    import pymupdf
    import markups_bluebeam as MB
    import markups_rcp as MR
    fs, v = MB.celda_legible("CH.6-2 - SHAFT WALL (C-H STUDS AND J-RUNNER, 1 IN LINER, 2 HR) - 2 LAYERS EACH SIDE", 194)
    assert pymupdf.get_text_length(v, fontname="helv", fontsize=fs) <= 194 and fs >= 5.5, (fs, v)
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
