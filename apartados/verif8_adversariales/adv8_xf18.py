# adv8_xf18: BE-XF18 elegir_pdf_markups — v137 (orden alfabético inverso) vs candidato. Sintético en /tmp/verif8/tmp.
import sys, os, json, tempfile, time, glob
sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif8/tmp"; os.makedirs(T, exist_ok=True)
def v137(e):
    return next((p for p in sorted(glob.glob(os.path.join(e, "Planos marcados", "*.pdf")), reverse=True)
                 if not os.path.basename(p).startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS", "ALTURAS_REVISADAS"))), None)
def caso(nombre, pdfs, xls=(), cfg=None, esperado=None):
    w = tempfile.mkdtemp(dir=T); pm = os.path.join(w, "Planos marcados"); os.makedirs(pm); os.makedirs(os.path.join(w, "Take-off"))
    t0 = time.time() - 1000
    for k, n in enumerate(pdfs):
        p = os.path.join(pm, n); open(p, "w").write("%PDF-1.4\n"); os.utime(p, (t0 + k, t0 + k))
    for k, n in enumerate(xls):
        p = os.path.join(w, "Take-off", n); open(p, "w").write("x"); os.utime(p, (t0 + 100 + k, t0 + 100 + k))
    if cfg is not None: json.dump(cfg, open(os.path.join(w, "entrega.json"), "w"))
    c = CE.Ctx(w); r = CE.ce_pdf_markups_elegido(c)
    a = os.path.basename(v137(w) or "-"); b = os.path.basename(c.markups or "-")
    tag = ""
    if esperado:
        tag = ("v137 OK" if a == esperado else "v137 MAL") + " / " + ("cand OK" if b == esperado and r[0] == "PASS" else ("cand FAIL-con-causa" if r[0] == "FAIL" else "cand MAL-EN-SILENCIO"))
    print(f"{nombre}\n   v137 lee: {a}\n   cand: {r[0]} lee: {b} {r[1][:1]}\n   -> {tag}")
caso("R1 un solo OPEN IN BLUEBEAM de la rev ANTERIOR + markups de la rev en curso sin sufijo; Excel rev20c",
     ["CR_markups_rev20b - OPEN IN BLUEBEAM.pdf", "CR_markups_rev20c.pdf"], ["CR_Takeoff_rev20c.xlsx"], esperado="CR_markups_rev20c.pdf")
caso("R2 un solo OPEN IN BLUEBEAM y es de la rev ANTERIOR (falta el de la rev en curso); Excel rev20c",
     ["CR_markups_rev20b - OPEN IN BLUEBEAM.pdf"], ["CR_Takeoff_rev20c.xlsx"], esperado="(ninguno: FAIL)")
caso("R3 dos OPEN IN BLUEBEAM (20b, 20c), Excel rev20c (control)",
     ["CR_markups_rev20b - OPEN IN BLUEBEAM.pdf", "CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"], ["CR_Takeoff_rev20c.xlsx"], esperado="CR_markups_rev20c - OPEN IN BLUEBEAM.pdf")
caso("R4 dos OPEN IN BLUEBEAM (20b, 20c), dos Excel: el más nuevo es el rev20b (re-guardado)",
     ["CR_markups_rev20b - OPEN IN BLUEBEAM.pdf", "CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"], ["CR_Takeoff_rev20c.xlsx", "CR_Takeoff_rev20b.xlsx"], esperado="CR_markups_rev20c - OPEN IN BLUEBEAM.pdf")
caso("R5 pre-U-165: markups + mapa con guion 'IMAGE-ONLY' (v137 elegía bien)",
     ["CR_MAPA - IMAGE-ONLY.pdf", "CR_markups_rev20c.pdf"], ["CR_Takeoff_rev20c.xlsx"], esperado="CR_markups_rev20c.pdf")
caso("R6 pre-U-165: markups + 'flattened' de la misma rev (v137 elegía el markups)",
     ["CR_markups_rev20c.pdf", "CR_markups_rev20c_flattened.pdf"], [], esperado="CR_markups_rev20c_flattened.pdf")
caso("R7 OPEN IN BLUEBEAM con 'rev20c' en minúsculas distinta: 'CR_markups_REV20C - open in bluebeam.pdf' + mapa",
     ["CR_markups_REV20C - open in bluebeam.pdf", "MAPA DE COBERTURA - IMAGE ONLY.pdf"], ["CR_Takeoff_rev20c.xlsx"], esperado="CR_markups_REV20C - open in bluebeam.pdf")
caso("R8 entrega.json 'markups' = el mapa IMAGE ONLY",
     ["MAPA DE COBERTURA - IMAGE ONLY.pdf", "CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"], [], cfg={"markups": "Planos marcados/MAPA DE COBERTURA - IMAGE ONLY.pdf"}, esperado="(ninguno: FAIL)")
caso("R9 solo el mapa IMAGE ONLY (sin markups)", ["MAPA DE COBERTURA - IMAGE ONLY.pdf"], [], esperado="(ninguno: FAIL)")
caso("R10 markups real cuyo nombre lleva 'COBERTURA' (p. ej. 'CR_markups_rev20c_COBERTURA-FIX - OPEN IN BLUEBEAM.pdf') + mapa",
     ["CR_markups_rev20c_COBERTURA-FIX - OPEN IN BLUEBEAM.pdf", "MAPA DE COBERTURA - IMAGE ONLY.pdf"], [], esperado="CR_markups_rev20c_COBERTURA-FIX - OPEN IN BLUEBEAM.pdf")
