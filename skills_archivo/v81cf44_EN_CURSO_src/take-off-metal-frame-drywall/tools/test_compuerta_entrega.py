#!/usr/bin/env python3
"""test_compuerta_entrega.py — BE-121: cada chequeo de compuerta_entrega.py / subir_entrega.py REPRODUCE el error original.
  - BE-120 (Harbor Freight rev2): RFI-01 abierto con la respuesta IMPRESA en A1.2 (B.O. DECK por zona) -> FAIL.
  - BE-119 (O'Reilly 3-nov): Depth del markup = H del Excel (comparación circular) pero la altura IMPRESA es otra -> FAIL.
  - Drive: carpeta bajo Projects › Claude outputs (O'Reilly / VS) -> FAIL; sin ENTREGA_OK verde -> subida bloqueada.
  - O'Reilly sin TIEMPOS.md -> FAIL. + formato Excel, tornillería, tracks, RFI A/B/C, RFI prohibidos.
Tokens que verificar_version.py busca en este archivo: ce_tiempos ce_drive_parent ce_rfi_barrido ce_altura_impresa
ce_formato_excel ce_tornilleria ce_track_familias ce_rfi_formato ce_rfi_prohibidos ce_entregables ce_sin_proposal
ce_sin_dolares ce_horas ce_seguimiento ce_atribucion ce_decisiones ce_fuentes_ms ce_datos_proyecto candados
ce_materiales_schedule revision_materiales texto_hoja_rotada
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


def test_oreilly_rev5():
    aq = os.path.dirname(os.path.abspath(__file__))
    for n, src in BLOQUES_OREILLY:
        g = {"__name__": "__main__", "__file__": os.path.join(aq, n + ".py")}
        exec(compile(src, n + ".py", "exec"), g)


BLOQUES_OREILLY.append(('test_u142', '#!/usr/bin/env python3\n"""test_u142.py - U-142 (usuario 5-nov: revisar todos los schedules del trade, lista de cada material y marcar cada partition\ntype). CFA rev10 / O\'Reilly rev9 se entregaron sin SCHEDULES_REVISADOS.pdf ni lista de materiales por fila. Falla con v81cf43."""\nimport json\nimport os\nimport sys\nimport tempfile\n\nimport pymupdf\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport compuerta_entrega as CE  # noqa: E402\n\nd = tempfile.mkdtemp()\nos.makedirs(os.path.join(d, "Planos marcados"))\nsch = [{"sheet": "A1.1", "page": 1, "title": "WALL TYPE SCHEDULE", "title_bbox": [10, 10, 200, 30], "ours": True, "why": "partition types",\n        "rows": [{"type": "S1", "bbox": [10, 40, 40, 55], "materials": [{"material": "3-5/8 stud", "spec": "20 GA @ 16", "source": "S1/A1.1"}],\n                  "in_canon": "yes: walls S1"},\n                 {"type": "S2", "bbox": [10, 60, 40, 75], "materials": [{"material": "6 stud", "spec": "18 GA", "source": "S2/A1.1"}],\n                  "in_canon": "no: type not used on the plans (no S2 tag on A1.1)"}]}]\njson.dump(sch, open(os.path.join(d, "schedules_materiales.json"), "w"))\n\n\nclass C:\n    cfg = {}\n    w = d\n    entrega = d\n    planos = os.path.join(d, "Planos marcados")\n\n\nr = CE.ce_schedules_revisados(C())\nassert r[0] == "FAIL" and any("SCHEDULES_REVISADOS.pdf" in e for e in r[1]), r\ndoc = pymupdf.open()\ndoc.new_page(width=600, height=400)\nfor k in (1, 2):\n    for sub in (CE.SUBJ_SCH, CE.SUBJ_SCH + " CHECK"):\n        a = doc[0].add_circle_annot(pymupdf.Rect(10, 20 * k, 40, 20 * k + 15))\n        a.set_info(subject=sub, content=f"#{k} reviewed")\n        a.update()\ndoc.save(os.path.join(C.planos, "SCHEDULES_REVISADOS.pdf"))\nopen(os.path.join(d, "SCHEDULES_MATERIALES.md"), "w").write("x")\nassert CE.ce_schedules_revisados(C())[0] == "PASS"\nsch[0]["rows"][1]["in_canon"] = "no"\njson.dump(sch, open(os.path.join(d, "schedules_materiales.json"), "w"))\nr = CE.ce_schedules_revisados(C())\nassert r[0] == "FAIL" and any("sin estado" in e for e in r[1]), r\nos.remove(os.path.join(d, "schedules_materiales.json"))\nassert CE.ce_schedules_revisados(C())[0] == "FAIL"\nprint("OK test_u142")\n'))


BLOQUES_OREILLY.append(('test_be_cf27', '#!/usr/bin/env python3\n"""test_be_cf27.py - BE-CF27 (CFA rev10, 5-nov): rev10 se subió con un skill sin U-141 / U-142 / U-143, órdenes del usuario\nque ya estaban en el remoto. subir_entrega bloquea si una orden U-NNN del remoto no está en el registro del skill."""\nimport os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport subir_entrega as SE  # noqa: E402\n\ntxt = "- [U-141 · programa] circular detalles\\n- [U-142 · programa] schedules\\n- [U-143 · programa] demo SF\\n"\nreg = {"reglas": [{"id": "U-141"}, {"id": "U-140"}]}\nassert SE.ordenes_sin_registro(txt, reg) == ["U-142", "U-143"]\nreg["reglas"] += [{"id": "U-142"}, {"id": "U-143"}]\nassert SE.ordenes_sin_registro(txt, reg) == []\nos.environ["SIN_ORDENES_REMOTAS"] = "1"\nSE.candado_ordenes()\ndel os.environ["SIN_ORDENES_REMOTAS"]\nprint("OK test_be_cf27")\n'))


if __name__ == "__main__":
    for f in (test_hft_rfi01_impreso, test_altura_circular_oreilly, test_drive_parent, test_tiempos, test_excel,
              test_entregables_y_docs, test_subida, test_materiales_schedule, test_revision_materiales, test_texto_hoja_rotada, test_materiales_cfa_rev5, test_correr_rojo, test_oreilly_rev5):
        f()
        print("ok", f.__name__)
    print("test_compuerta_entrega OK")
