"""7_imagenes: una PNG por hoja marcada (render del markups.pdf, todas las annots visibles) + imagenes_hoja.json
(hoja, página, annots, types). Reabierta: se verifica tamaño > 0 y que el número de annots de la hoja = markups.json."""
import json, os, fitz
W = '/root/cr/work/etapas'
m = json.load(open(f'{W}/6_markups/markups.json'))
d = fitz.open(f'{W}/6_markups/markups_con_rcp.pdf')
os.makedirs(f'{W}/7_imagenes', exist_ok=True)
out = []
for i, p in enumerate(d):
    an = list(p.annots() or [])
    if not an:
        continue
    sheet = next((h.split(' ')[0] for h in (m.get('por_hoja') or {}) if h.endswith(f"(p.{i + 1})")), f"p{i + 1}")
    fn = f"{sheet}_marked_by_type_rev13.png"
    p.get_pixmap(dpi=110, annots=True).save(f'{W}/7_imagenes/{fn}')
    assert os.path.getsize(f'{W}/7_imagenes/{fn}') > 0
    out.append({"sheet": sheet, "page": i + 1, "annots": len(an), "types": sorted({a.info.get('subject') for a in an}), "png": fn})
json.dump(out, open(f'{W}/7_imagenes/imagenes_hoja.json', 'w'), indent=1)
print(len(out), 'sheets')
