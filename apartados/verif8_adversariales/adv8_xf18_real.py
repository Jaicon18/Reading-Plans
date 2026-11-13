# adv8_xf18_real: PDF de markups que elige v137 (orden alfabético inverso) vs el candidato (elegir_pdf_markups) en carpetas reales
import sys, os, glob
sys.path.insert(0, "/tmp/verif8/take-off-metal-frame-drywall/tools"); import compuerta_entrega as CE
def v137(e):
    return next((p for p in sorted(glob.glob(os.path.join(e, "Planos marcados", "*.pdf")), reverse=True)
                 if not os.path.basename(p).startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS", "ALTURAS_REVISADAS"))), None)
for pm in sys.argv[1:]:
    e = os.path.dirname(pm.rstrip("/"))
    a = v137(e); b, causa = CE.elegir_pdf_markups(e)
    print(("IGUAL " if a == b else "DISTINTO ") + e, "\n   v137:", a and os.path.basename(a), "\n   cand:", b and os.path.basename(b), causa or "")
