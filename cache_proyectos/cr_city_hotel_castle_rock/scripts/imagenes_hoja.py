"""7_imagenes: una PNG por hoja marcada (render del markups_con_rcp.pdf, walls + ceilings) + imagenes_hoja.json.
U-158 (usuario 10-nov: 'usa otro nombre ya que me confunden'): el nombre dice QUÉ ES: '<HOJA> - IMAGE ONLY (not editable) - walls|ceilings|walls
and ceilings revN.png', HOJA = Page Label impreso (nunca pNN). Una sola imagen por hoja (sin duplicados _rcp_markups)."""
import json, os, glob, fitz
W = '/root/cr/work/etapas'; REV = 'rev14'
d = fitz.open(f'{W}/6_markups/markups_con_rcp.pdf')
os.makedirs(f'{W}/7_imagenes', exist_ok=True)
for f in glob.glob(f'{W}/7_imagenes/*.png'):
    os.remove(f)
out = []
for i, p in enumerate(d):
    an = list(p.annots() or [])
    if not an:
        continue
    lab = (p.get_label() or '').strip()
    assert lab and not lab.lower().startswith('p') or lab.upper() == 'LEGEND', f'page {i + 1} sin Page Label impreso: {lab!r}'
    tit = {(a.info.get('title') or '') for a in an}
    muros = any(t == 'Take-off' or t == 'Take-off legend' for t in tit)
    cielos = any(t == 'take-off' for t in tit)
    kind = 'walls and ceilings' if muros and cielos else ('ceilings' if cielos else 'walls')
    fn = f"{lab} - IMAGE ONLY (not editable) - {kind} {REV}.png"
    p.get_pixmap(dpi=110, annots=True).save(f'{W}/7_imagenes/{fn}')
    assert os.path.getsize(f'{W}/7_imagenes/{fn}') > 0
    out.append({"sheet": lab, "page": i + 1, "annots": len(an), "kind": kind, "types": sorted({a.info.get('subject') for a in an}), "png": fn})
json.dump(out, open(f'{W}/7_imagenes/imagenes_hoja.json', 'w'), indent=1)
print(len(out), 'sheets')
