#!/usr/bin/env python3
"""glosario.py — v73: nombres de MATERIAL y del oficio (drywall / metal frame) en español -> inglés.

Por qué viaja en el paquete: hoja_indice.py, hoja_estado.py, hoja_detalles.py, traducir_materiales.py,
traducir_docs.py y verif_idioma.py lo importan, y el zip v72b no lo traía (ModuleNotFoundError en la prueba 21B).
Regla del usuario: todo término del trade va en INGLÉS (drywall, stud, track, header, sill, blocking, joint
compound…); nunca "tablaroca", "panel de yeso", "perfilería metálica", "poste metálico", "canal".

API:
  traducir(texto) -> texto con los términos del glosario en inglés (no toca bloques ``` ni `inline code`);
  faltas(texto)   -> lista ordenada de términos en español que quedan (sin código; vacía = OK).
"""
import re

import vocab_trade as _V

GLOSARIO = [
    (r"tabla\s*roca", "drywall"), (r"panel(?:es)? de yeso", "gypsum board"), (r"placas? de yeso", "gypsum board"),
    (r"paneles? de yeso", "gypsum board"), (r"yeso laminado", "gypsum board"),
    (r"perfiler[ií]a met[aá]lica", "metal framing"), (r"bastidor(?:es)? met[aá]lico(?:s)?", "metal framing"),
    (r"postes? met[aá]licos?", "steel stud"), (r"montantes?", "stud"), (r"canal(?:es)? de carga", "carrying channel"),
    (r"canal(?:es)? omega", "furring channel"), (r"canal(?:es)? listón", "furring channel"),
    (r"canal(?:es)?", "track"), (r"rieles?", "runner"), (r"viguetas?", "joist"),
    (r"tornillos? para (?:tabla\s*roca|drywall)", "drywall screw"), (r"tornillos? de framing", "framing screw"),
    (r"compuesto (?:para juntas|de juntas)", "joint compound"), (r"pasta (?:para juntas|de juntas)", "joint compound"),
    (r"cinta (?:de papel|para juntas)", "joint tape"), (r"esquineros?", "corner bead"),
    (r"encintado", "taping"), (r"dinteles?", "header"), (r"alf[eé]izar(?:es)?", "sill"), (r"antepechos?", "sill"),
    (r"refuerzos? de madera", "blocking"), (r"bloqueos?", "blocking"), (r"triplay", "plywood"),
    (r"contrachapado", "plywood"), (r"madera tratada (?:ignífuga|contra fuego)", "FRT wood"),
    (r"aislamiento(?: térmico| acústico)?", "insulation"), (r"sellador(?:es)? acústicos?", "acoustical sealant"),
    (r"alambre (?:colgante|de suspensi[oó]n)", "hanger wire"), (r"tirantes?", "bracing"),
    (r"panel(?:es)? de cemento", "cement board"), (r"tablero de cemento", "cement board"),
]
_RX = [(re.compile(r"(?<![\w-])" + a + r"(?![\w-])", re.I), b) for a, b in GLOSARIO]
_COD = re.compile(r"(```.*?```|`[^`\n]*`)", re.S)


def _trozos(t):
    """[(texto, es_codigo)] — el código citado no se traduce (es evidencia o nombre de campo)."""
    out, i = [], 0
    for m in _COD.finditer(t):
        if m.start() > i:
            out.append((t[i:m.start()], False))
        out.append((m.group(0), True))
        i = m.end()
    if i < len(t):
        out.append((t[i:], False))
    return out


def traducir(t):
    if not isinstance(t, str):
        return t
    res = []
    for x, cod in _trozos(t):
        if not cod:
            for rx, en in _RX:
                x = rx.sub(en, x)
        res.append(x)
    return "".join(res)


def faltas(t):
    s = _V.sin_codigo(t)
    return sorted({m.group(0).lower() for rx, _ in _RX for m in rx.finditer(s)})
