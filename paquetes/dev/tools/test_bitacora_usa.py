#!/usr/bin/env python3
"""Test v61 de bitacora.usa() (arbitraje #11): 'import json; import closer' no se veía y la compuerta
decía que closer/planmark no se usaron. Correr: python3 test_bitacora_usa.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bitacora as B  # noqa: E402

CASOS = {
    "import json\nfrom closer import emit\n": ["closer"],
    "x = 1; import closer\n": ["closer"],
    "import json; import planmark\n": ["planmark"],
    "import os, closer as c\n": ["closer"],
    "from py import planmark\n": ["planmark"],
    "from . import (os, closer)\n": ["closer"],
    "m = __import__('closer')\n": ["closer"],
    "import importlib; importlib.import_module(\"planmark\")\n": ["planmark"],
    "import closerx\nprint('closer')\n": [],          # dato malo: nombre parecido / texto suelto
    "# x = 1; import closer\ns = 'from closer import emit'\n": [],   # v66: comentario / string no es import
}


def test_usa():
    for src, want in CASOS.items():
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(src)
        got = B.usa(f.name)
        os.unlink(f.name)
        assert got == want, (src, got, want)


def test_v66_bitacora_no_se_usa_a_si_misma():
    """#15A: `bitacora.py run bitacora.py compuerta` anotaba usa=closer (texto de su propio docstring/regex) y la
    compuerta se rechazaba a sí misma."""
    assert B.usa(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bitacora.py")) == []


if __name__ == "__main__":
    test_usa()
    test_v66_bitacora_no_se_usa_a_si_misma()
    print("OK test_usa (%d casos) + test_v66_bitacora_no_se_usa_a_si_misma" % len(CASOS))
