"""Pone la escala de PÁGINA (/VP viewport con /Measure) en cada página que tiene markups con /Measure,
copiando la misma medida de sus markups. Así Bluebeam muestra la escala correcta de la hoja (U-152 / BE-148)."""
import sys, collections, pikepdf
from pikepdf import Name, Dictionary, Array
src, dst = sys.argv[1], sys.argv[2]
pdf = pikepdf.open(src)
puestas = []
for i, page in enumerate(pdf.pages):
    meds = collections.Counter(); ejemplo = {}
    for a in page.obj.get('/Annots', []):
        m = a.get('/Measure')
        if m is None: continue
        k = str(m.get('/R')); meds[k] += 1; ejemplo.setdefault(k, m)
    if not meds: continue
    if len(meds) > 1: print('AVISO pagina', i + 1, 'con varias escalas', dict(meds))
    r, _ = meds.most_common(1)[0]
    mb = [float(x) for x in page.obj.MediaBox]
    vp = Dictionary(Type=Name.Viewport, BBox=Array(mb), Name=pikepdf.String(r),
                    Measure=pdf.copy_foreign(ejemplo[r]) if False else ejemplo[r])
    page.obj.VP = Array([vp])
    puestas.append((i + 1, r))
pdf.save(dst)
print('paginas con escala', len(puestas)); print(puestas)
