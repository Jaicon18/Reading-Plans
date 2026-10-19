# -*- coding: utf-8 -*-
"""verif_caras.py -- COMPUERTA: los rooms que nombra la ubicacion son los de las faces.

ORIGEN (8-oct-2026, verificando los walls A1 #2, #3, #4 y #7). Cuatro walls seguidos con el
mismo patron: la `ubicacion` nombraba dos rooms y las `caras` nombraban otros.

  A1 #2 y #3  ubicacion "MW01 niche / Calling Cubes 122"  ->  faces Calling Cubes 122 y
              **Corridor 111**. El corridor no llega al nicho: queda al oeste del wall
              vertical de x=1224-1228. La height no cambiaba (los dos bands a <n>), pero el
              nombre si, y el nombre es lo que lee quien compra y quien instala.
  A1 #7       las DOS faces decian "Break Room 118". La ESTE da a CASH WINDOW 116, cuyo
              ceiling es ACT-4 a 9'-0" -> board a 9.50, no 9.00. **+0.87 SF** que faltaban.
  A1 #4       el caso contrario: las dos faces decian "Corridor 111" y la ubicacion decia
              "entry from Central Zone". Ahi las faces TENIAN razon -- se comprobo que la
              reticula del ceiling cruza el wall sin interrupcion -- y fiarse de la ubicacion
              habria subido una face a 12.00 ft y metido +15 SF que no existen.

> **Ninguno de los dos lados manda por si solo: cuando la ubicacion y las faces no coinciden,
> hay que ir al plano.** Lo que esta compuerta hace es IMPEDIR que la discrepancia pase
> inadvertida, no decidir quien tiene razon.

COMO SE EVITA QUE SEA RUIDO (que es como una compuerta se acaba apagando): solo se compara
cuando la `ubicacion` tiene la forma limpia `<room A> / <room B>`. Se descarta en cuanto el
texto trae coordenadas (`y 1120.68/1128.48`), parentesis, o una barra dentro de una sigla
(`T/STUD`): ahi la barra no separa rooms. Las discrepancias ya EXPLICADAS se declaran una por
una con su motivo, nunca se aflojan en silencio.
"""
import os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG

# Discrepancias REALES ya verificadas contra el plano, con su motivo escrito.
DECLARADAS = {
    'A1 #6': ('La ubicacion dice "Break Room 118 / Future FCAM" y la face se llama Cash '
              'Window 116: el area FUTURE FCAM esta DENTRO del room Cash Window 116, y asi lo '
              'dice la propia operacion de la height. Comprobado en A04.01.'),
    'G #47': ('La ubicacion dice "teller line" y la face "Teller line": es el mismo room, '
              'escrito con mayuscula distinta.'),
}


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
