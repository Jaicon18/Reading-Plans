"""burbujas/: une G1 + G2 (verificación a ojo de los dos subagentes) en burbujas_verificadas.json (formato
CE_DETALLES_CIRCULADOS: {<hoja>: [entradas], _destinos}), CADENA.md y callouts_no_aplican.json; cada destino con
detalle_existe se escribe también bajo su hoja destino. Imágenes: img_verif/ de cada grupo copiadas con prefijo."""
import json, os, shutil, glob
B = '/root/cr/work/burbujas'
out, dest, nap, cad = {"_nota": "U-137 / U-141: union of the eye verification G1 (T0.01, A0-A4, S, M, P, E) and G2 (A5-A9, A6, A7, A8, A9)", "_frame": "page pt, rotation 0"}, {}, {}, []
os.makedirs(f'{B}/img_verif', exist_ok=True)
for g in ('G1', 'G2'):
    d = json.load(open(f'{B}/{g}/burbujas_verificadas.json'))
    for f in glob.glob(f'{B}/{g}/img_verif/*.png'):
        shutil.copy2(f, f'{B}/img_verif/{g}_{os.path.basename(f)}')
    def fix(e):
        e = dict(e)
        if isinstance(e.get('img'), str) and e['img'].startswith('img_verif/'):
            e['img'] = 'img_verif/' + g + '_' + e['img'][len('img_verif/'):]
        return e
    for k, v in d.items():
        if k.startswith('_'):
            if k == '_destinos':
                for nt, x in v.items():
                    dest.setdefault(nt, fix(x))
            continue
        out.setdefault(k, []).extend(fix(e) for e in v)
    n = json.load(open(f'{B}/{g}/callouts_no_aplican.json'))
    for h, m in n.items():
        if not h.startswith('_'):
            nap.setdefault(h, {}).update(m)
    cad.append(open(f'{B}/{g}/CADENA.md').read())
for nt, x in dest.items():
    if x.get('detalle_existe') and nt.count('/') == 1:
        n_, h = nt.split('/')
        lst = out.setdefault(h, [])
        if not any(str(e.get('detalle_existe')) == n_ for e in lst):
            lst.append({"detalle_existe": n_, "x": x.get('x'), "y": x.get('y'), "x1": x.get('x1'), "y1": x.get('y1'), "img": x.get('img'), "title": x.get('title')})
out['_destinos'] = dest
json.dump(out, open(f'{B}/burbujas_verificadas.json', 'w'), indent=1, ensure_ascii=False)
json.dump(dict(nap, _nota="disposition of the bubbles not cited in a take-off row: {destination sheet: {detail: reason}}"), open(f'{B}/callouts_no_aplican.json', 'w'), indent=1, ensure_ascii=False)
open(f'{B}/CADENA.md', 'w').write('# CADENA de referencias (U-137 / U-141) - CR City Hotel, 148 sheets\n\n' + '\n\n---\n\n'.join(cad))
print(sum(len(v) for k, v in out.items() if not k.startswith('_')), 'entries;', len(dest), 'destinations;', sum(len(v) for v in nap.values()), 'no aplican')
