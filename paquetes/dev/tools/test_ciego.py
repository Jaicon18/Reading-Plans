"""test_ciego.py — E24 (protocolo ciego). Falla si el SKILL, referencias/ o una tool entregable contiene un valor
BOA de la referencia (cantidad, cota, R.O. o conteo). La lista vive en tests_arbitraje/valores_referencia.json y
NUNCA se entrega a pruebas.

Uso:  python3 -I test_ciego.py <zip|carpeta|archivo> [...]  [--valores valores_referencia.json]
      python3 -I test_ciego.py --selftest
Exit 0 = ciego; 1 = fuga (lista archivo:línea:valor).

v67: la tool viaja en tools/ (selftest con números inventados). Sin valores_referencia.json (prueba: la lista
NUNCA se entrega) corre el MODO PRUEBA: falla si la ruta trae material de arbitraje (tests_arbitraje/,
valores_referencia.json, ARBITRAJE_*.md, VERIFICACION_*.md, DECISIONES_*.md); con la lista, el chequeo completo.
bitacora.py compuerta exige su corrida con rc=0.
"""
import json, os, re, sys, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTO = ('.md', '.py', '.txt', '.json', '.csv', '.sh')
EXCLUIR = {'valores_referencia.json', 'generar_valores.py', 'test_ciego.py'}
ARBITRAJE = re.compile(r'(^|/)(tests_arbitraje/|valores_referencia\.json$|ARBITRAJE_[^/]*\.md$|VERIFICACION_[^/]*\.md$|'
                       r'DECISIONES_[^/]*\.md$)')


def material_arbitraje(rutas):
    """Modo prueba: nombres de archivo que solo existen en el material de arbitraje."""
    out = []
    for r in rutas:
        if zipfile.is_zipfile(r):
            nombres = zipfile.ZipFile(r).namelist()
        elif os.path.isdir(r):
            nombres = [os.path.relpath(os.path.join(dp, f), r).replace(os.sep, '/') + ('/' if f in dn else '')
                       for dp, dn, fn in os.walk(r) for f in fn + dn]
        else:
            nombres = [os.path.basename(r)]
        out += [f"{r}!{n}" for n in nombres if ARBITRAJE.search(n)]
    return out


def patrones(vals):
    pats = []
    for v in vals['decimales']:
        ent, dec = v.split('.')
        con_coma = f"{int(ent):,}" if len(ent) > 3 else ent
        alts = {re.escape(ent + '.' + dec), re.escape(con_coma + '.' + dec)}
        pats.append((v, re.compile(r'(?<![\w.,/])(?:' + '|'.join(alts) + r')(?!\d)')))
    for f in vals['ft_in']:
        pats.append((f, re.compile(r'(?<![\d\'-])' + re.escape(f).replace('"', '(?:"|”|in)'))))
    for rx in vals['regex']:
        pats.append((rx, re.compile(rx, re.I)))
    return pats


def archivos(ruta):
    if zipfile.is_zipfile(ruta):
        with zipfile.ZipFile(ruta) as z:
            for n in z.namelist():
                if n.endswith(TEXTO) and os.path.basename(n) not in EXCLUIR and '/tests_arbitraje/' not in '/' + n:
                    yield ruta + '!' + n, z.read(n).decode('utf-8', 'replace')
    elif os.path.isdir(ruta):
        for dp, dn, fn in os.walk(ruta):
            dn[:] = [d for d in dn if d not in ('tests_arbitraje', '__pycache__')]
            for f in sorted(fn):
                if f.endswith(TEXTO) and f not in EXCLUIR:
                    p = os.path.join(dp, f)
                    yield p, open(p, encoding='utf-8', errors='replace').read()
    else:
        yield ruta, open(ruta, encoding='utf-8', errors='replace').read()


def fugas(rutas, vals):
    pats, out = patrones(vals), []
    for r in rutas:
        for nombre, txt in archivos(r):
            for i, linea in enumerate(txt.splitlines(), 1):
                for v, p in pats:
                    if p.search(linea):
                        out.append((nombre, i, v, linea.strip()[:140]))
    return out


def selftest():
    vals = {'decimales': ['123.47', '8765.21', '7.777'], 'ft_in': ["21'-3 1/4\""], 'regex': [r'\bZZ9\s*=\s*7\b']}
    import tempfile
    d = tempfile.mkdtemp()
    malo = os.path.join(d, 'malo.md'); bueno = os.path.join(d, 'bueno.md')
    open(malo, 'w').write('parapet X 123.47\nstud 8,765.21\nrun 21\'-3 1/4"\nZZ9 = 7\nlargo 7.777\n')
    open(bueno, 'w').write('parapet bay por bay (11/S5.10)\n1123.475 no es fuga\n0.75 x L\n27.777\n')
    f = fugas([malo], vals); assert len(f) == 5, f
    assert fugas([bueno], vals) == [], fugas([bueno], vals)
    z = os.path.join(d, 'x.zip')
    with zipfile.ZipFile(z, 'w') as zz:
        zz.writestr('skill/SKILL.md', 'ok\n'); zz.writestr('skill/tests_arbitraje/x.md', '123.47')
    assert fugas([z], vals) == []
    assert material_arbitraje([z]) == [z + '!skill/tests_arbitraje/x.md']
    open(os.path.join(d, 'ARBITRAJE_9.md'), 'w').write('x')
    assert len(material_arbitraje([d])) == 1 and material_arbitraje([bueno]) == []
    print('test_ciego selftest: 5 tests OK')


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--selftest' in a:
        selftest(); sys.exit(0)
    vp = os.path.join(AQUI, 'valores_referencia.json')
    if '--valores' in a:
        i = a.index('--valores'); vp = a[i + 1]; del a[i:i + 2]
    if not os.path.exists(vp):
        m = material_arbitraje(a)
        for x in m:
            print(f'FUGA material de arbitraje: {x}')
        print(f'test_ciego MODO PRUEBA (sin lista de examen): {len(m)} archivo(s) de arbitraje en {len(a)} ruta(s)'
              + (' -> FALLA' if m else ' -> OK'))
        sys.exit(1 if m else 0)
    vals = json.load(open(vp))
    f = fugas(a, vals)
    for n, i, v, l in f:
        print(f'FUGA {n}:{i}: [{v}] {l}')
    print(f'test_ciego: {len(f)} fuga(s) en {len(a)} ruta(s)' + (' -> FALLA' if f else ' -> OK (ciego)'))
    sys.exit(1 if f else 0)
