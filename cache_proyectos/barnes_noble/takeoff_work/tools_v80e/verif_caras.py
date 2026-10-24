# -*- coding: utf-8 -*-
"""verif_caras.py -- COMPUERTA: los rooms que nombra la ubicacion son los de las faces.

ORIGEN (8-oct-2026, verificando walls de un mismo type). Varios walls seguidos con el
mismo patron: la `ubicacion` nombraba dos rooms y las `caras` nombraban otros.

  caso 1      la ubicacion nombraba un nicho y un room; las faces, ese room y un corridor
              que no llega al nicho (queda del otro lado de un wall vecino). La height no
              cambiaba, pero el nombre si, y el nombre es lo que lee quien compra y quien
              instala.
  caso 2      las DOS faces decian el mismo room. Una da a otro room, con otro ceiling ->
              otra altura de board: faltaban <n> SF.
  caso 3      el caso contrario: las faces TENIAN razon y la ubicacion no -- se comprobo que
              la reticula del ceiling cruza el wall sin interrupcion -- y fiarse de la
              ubicacion habria subido una face y metido +<n> SF que no existen.

> **Ninguno de los dos lados manda por si solo: cuando la ubicacion y las faces no coinciden,
> hay que ir al plano.** Lo que esta compuerta hace es IMPEDIR que la discrepancia pase
> inadvertida, no decidir quien tiene razon.

COMO SE EVITA QUE SEA RUIDO (que es como una compuerta se acaba apagando): solo se compara
cuando la `ubicacion` tiene la forma limpia `<room A> / <room B>`. Se descarta en cuanto el
texto trae coordenadas (`y <c0>/<c1>`), parentesis, o una barra dentro de una sigla
(`T/STUD`): ahi la barra no separa rooms. Las discrepancias ya EXPLICADAS se declaran una por
una con su motivo, nunca se aflojan en silencio.
"""
import os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG

# Discrepancias REALES ya verificadas contra el plano, con su motivo escrito. Son DEL
# PROYECTO: se leen de $TAKEOFF_WORK/caras_declaradas.json = {"<tag> #<n>": "<motivo>"}.
def _declaradas():
    import json
    p = os.path.join(os.environ.get('TAKEOFF_WORK', os.getcwd()), 'caras_declaradas.json')
    try:
        return dict(json.load(open(p, encoding='utf-8')))
    except (OSError, ValueError, TypeError):
        return {}


DECLARADAS = _declaradas()


def _norm(t):
    t = unicodedata.normalize('NFKD', (t or '')).encode('ascii', 'ignore').decode()
    t = re.sub(r'\s*\(face \d+\)\s*$', '', t, flags=re.I)
    return re.sub(r"[^a-z0-9 ]", '', t.lower()).strip()


# La ubicacion solo se lee cuando la barra de verdad separa dos rooms.
SUCIA = re.compile(r'\d\s*/|/\s*\d|\(|\)|/[A-Z]{2,}')


def rooms_de(ub):
    cab = re.split(r'\s+[-–—]\s+', ub or '')[0]
    if '/' not in cab or SUCIA.search(cab):
        return []
    rs = [p.strip() for p in cab.split('/') if p.strip()]
    return rs if len(rs) == 2 else []


def verificar():
    """[(etiqueta, ubicacion, faces, rooms que ninguna face nombra)]."""
    out = []
    for tipo, ws in RG.cargar().items():
        for w in ws:
            et = '%s #%s' % (w.get('tag') or tipo.split()[0], w.get('muro'))
            if et in DECLARADAS:
                continue
            rs = rooms_de(w.get('ubicacion') or '')
            if not rs:
                continue
            caras = [(c.get('cuarto') or '') for c in (w.get('caras') or [])]
            base = {_norm(c) for c in caras}
            falta = [r for r in rs
                     if not any(_norm(r) and (_norm(r) in b or b in _norm(r)) for b in base)]
            if falta:
                out.append((et, w.get('ubicacion'), caras, falta))
    return out


if __name__ == '__main__':
    mal = verificar()
    if not mal:
        print('OK: cada face nombra uno de los rooms que nombra su ubicacion')
        sys.exit(0)
    print('*** LA UBICACION Y LAS FACES NO COINCIDEN (%d):' % len(mal))
    for et, ub, caras, falta in mal:
        print('    %-12s %s' % (et, (ub or '')[:70]))
        print('          faces: %s' % caras)
        print('          ningun face nombra: %s' % falta)
    print('\n    Ir al PLANO: ninguno de los dos lados manda por si solo. Verificar el room de '
          'cada face por la banda de ceiling, corregir el que este mal, y si la discrepancia '
          'es real y explicada, declararla en verif_caras.DECLARADAS con su motivo.')
    sys.exit(1)
