#!/usr/bin/env python3
"""Test v68 de arranque.asegurar_deps (arbitraje #16B: el arranque no instalaba pikepdf / pymupdf)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arranque as A  # noqa: E402


class R:
    def __init__(self, rc):
        self.returncode = rc


def main():
    ok = 0
    instalado, cmds = set(), []

    def imp(m):
        if m not in instalado:
            raise ImportError(m)

    def run(cmd, **kw):                         # pip normal falla; con --break-system-packages instala
        cmds.append(cmd)
        if "--break-system-packages" in cmd:
            instalado.add({"pymupdf": "fitz"}.get(cmd[5], cmd[5]))
            return R(0)
        return R(1)
    assert A.asegurar_deps(run=run, imp=imp) == [], cmds; ok += 1
    pk = [c[5] for c in cmds]
    assert {"pikepdf", "pymupdf", "pdfplumber"} <= set(pk), pk; ok += 1
    assert all(c[1:5] == ["-m", "pip", "install", "--quiet"] for c in cmds), cmds; ok += 1
    assert A.asegurar_deps(run=lambda c, **k: R(1), imp=lambda m: (_ for _ in ()).throw(ImportError(m))) == \
        ["pikepdf", "pymupdf", "pdfplumber"]; ok += 1                    # no se puede instalar -> se dice
    n = []
    assert A.asegurar_deps(run=lambda c, **k: n.append(c), imp=lambda m: None) == [] and not n; ok += 1
    assert ("fitz", "pymupdf") in A.DEPS and ("pikepdf", "pikepdf") in A.DEPS; ok += 1
    print(f"test_arranque_v68: {ok} checks OK")


if __name__ == "__main__":
    main()
