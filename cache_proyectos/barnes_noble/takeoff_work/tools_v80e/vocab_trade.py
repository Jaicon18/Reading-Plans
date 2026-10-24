#!/usr/bin/env python3
"""vocab_trade.py — v73: vocabulario del trade en PROSA (chat, documentos, literales de generadores).

Lista distinta de glosario.py a propósito (adenda v40): glosario revisa el DATO (nombres de material); aquí van
palabras de prosa que en inglés son wall, door, length, line item, dimension… Varias son claves del cierre, por
eso no entran al glosario. La normalización del código vive en UN lugar (adenda v42): `sin_codigo` quita bloques
cercados ``` y `inline code`; `faltas()` la aplica de oficio.
"""
import re

VOCAB = [
    (r"muros?", "wall(s)"), (r"puertas?", "door(s)"), (r"ventanas?", "window(s)"), (r"largos?", "length"),
    (r"partidas?", "line item(s)"), (r"cotas?", "dimension(s)"), (r"abatibles?", "swing"), (r"bisagras?", "hinge(s)"),
    (r"alturas?", "height"), (r"espesor(?:es)?", "thickness"), (r"plafones?", "ceiling(s)"), (r"cielos? rasos?", "ceiling(s)"),
    (r"losas?", "slab"), (r"vigas?", "beam(s)"), (r"columnas?", "column(s)"), (r"fachadas?", "facade(s)"),
    (r"aberturas?", "opening(s)"), (r"vanos?", "opening(s)"), (r"esquinas?", "corner(s)"), (r"desperdicio", "waste"),
]
_RX = [(re.compile(r"(?<![\w-])" + a + r"(?![\w-])", re.I), b) for a, b in VOCAB]
_FENCE = re.compile(r"```.*?```", re.S)
_INLINE = re.compile(r"`[^`\n]*`")


def sin_codigo(t):
    """Texto sin bloques ``` ni `inline code` (lo citado como código no se revisa como prosa)."""
    return _INLINE.sub(" ", _FENCE.sub(" ", str(t or "")))


def lineas_sin_codigo(t):
    """[(n_linea, texto sin código)] — misma normalización, por renglón (los bloques cercados quedan vacíos)."""
    limpio = _FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), str(t or ""))
    return [(i + 1, _INLINE.sub(" ", ln)) for i, ln in enumerate(limpio.split("\n"))]


def faltas(t):
    """[(término en español, inglés)] en la prosa de `t` (sin código)."""
    s = sin_codigo(t)
    out = []
    for rx, en in _RX:
        for m in rx.finditer(s):
            out.append((m.group(0), en))
    return out


def traducir(t):
    """Prosa con el vocabulario del trade en inglés; el código citado (``` / `inline`) no se toca."""
    if not isinstance(t, str):
        return t
    partes = re.split(r"(```.*?```|`[^`\n]*`)", t, flags=re.S)
    for i in range(0, len(partes), 2):
        for rx, en in _RX:
            partes[i] = rx.sub(en.replace("(s)", ""), partes[i])
    return "".join(partes)
