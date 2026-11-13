# adv7_xf18: BE-XF18 elegir_pdf_markups / CE_PDF_MARKUPS_ELEGIDO (v138). Sintético en /tmp/verif7/tmp.
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
def caso(pdfs, cfg=None):
    w = tempfile.mkdtemp(dir=T); pm = os.path.join(w, "Planos marcados"); os.makedirs(pm)
    for n in pdfs: open(os.path.join(pm, n), "w").write("%PDF-1.4\n")
    if cfg is not None: json.dump(cfg, open(os.path.join(w, "entrega.json"), "w"))
    c = CE.Ctx(w); r = CE.ce_pdf_markups_elegido(c)
    return r[0], os.path.basename(c.markups or "-"), os.path.exists(c.markups or "")
print("X0 control (mapa + OPEN IN BLUEBEAM) ->", caso(["MAPA DE COBERTURA - IMAGE ONLY.pdf", "CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"]))
print("X1 entrega.json 'markups' apunta a un archivo que NO existe ->", caso(["CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"], {"markups": "Planos marcados/CR_markups_rev20b.pdf"}))
print("X2 entrega.json 'markups' apunta al PDF de la rev ANTERIOR (existe) ->", caso(["CR_markups_rev20b.pdf", "CR_markups_rev20c - OPEN IN BLUEBEAM.pdf"], {"markups": "Planos marcados/CR_markups_rev20b.pdf"}))
print("X3 OPEN IN BLUEBEAM viejo (rev20b) + markups actual sin sufijo (rev20c) ->", caso(["CR_markups_rev20b - OPEN IN BLUEBEAM.pdf", "CR_markups_rev20c.pdf"]))
print("X4 mapa con nombre 'MAPA - IMAGE-ONLY.pdf' (guion) como único otro PDF + markups ->", caso(["CR_MAPA - IMAGE-ONLY.pdf", "CR_markups_rev20c.pdf"]))
print("X5 mapa 'Coverage map - image only.pdf' (inglés) + markups sin sufijo ->", caso(["Coverage map.pdf", "CR_markups_rev20c.pdf"]))
