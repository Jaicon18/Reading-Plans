#!/usr/bin/env python3
"""test_excluidas_texto.py — R80w.20: el texto de exclusión que canon.py escribe (familias_out.excluidas -> Scope
Checklist) no trae nombres de archivo internos: plantilla_excel.TEXTO_INTERNO (R80e.84) lo rechazaba y el Excel
no pasaba verificar en NINGÚN proyecto. Sintético; falla con canon.py v80v."""
import os, re, sys
AQ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQ)
import plantilla_excel as P
src = open(os.path.join(AQ, "canon.py"), encoding="utf-8").read()
m = re.search(r'out\["excluidas"\]\s*=\s*\{(.+?)\}', src, re.S)
assert m, "no se encontró out['excluidas'] en canon.py"
for txt in re.findall(r'"([^"]+)"', m.group(1)):
    assert not P.TEXTO_INTERNO.search(txt), f"texto interno en excluidas: {P.TEXTO_INTERNO.search(txt).group(0)}"
print("test_excluidas_texto OK")
