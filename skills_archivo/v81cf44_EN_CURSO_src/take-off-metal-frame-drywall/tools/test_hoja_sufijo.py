#!/usr/bin/env python3
"""test_hoja_sufijo.py — R80w.12: una hoja con sufijo de letra (RCP / elevaciones "A421.A", "A000.B") es una HOJA válida
para reglas.py (HOJA / NHOJA) y para runner/evidencia.py (HOJA). Sintético: falla con reglas.py / evidencia.py v80v."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "runner"))
import reglas

ok_hoja = ["X421.A 10'-0\" ceiling tag", "elev 3/X426.A", "X000.B note", "X101", "X-101", "X2.10", "X421.AB"]
for t in ok_hoja:
    assert reglas.HOJA.search(t), f"HOJA no reconoce {t!r}"
assert reglas.NHOJA.search("3/X426.A"), "NHOJA no reconoce 3/X426.A"
assert reglas.NHOJA.search("D/X301"), "NHOJA protección"
# protecciones: un número suelto / keynote con dígitos tras el punto siguen como antes
assert not reglas.HOJA.search("421.5 pt"), "un número no es hoja"
assert reglas.HOJA.search("X421.5") is None or reglas.HOJA.search("X421.5").group(0) != "X421", "X421.5 no es X421"
try:
    import evidencia
    assert evidencia.HOJA.search("X421.A ceiling").group(1) == "X421.A", "evidencia.HOJA corta el sufijo .A"
    assert evidencia.HOJA.search("X-101 plan").group(1) == "X-101"
    assert evidencia.HOJA.search("X4.2 plan").group(1) == "X4.2"
except ImportError:          # el paquete de tools sin runner: solo reglas
    pass
print("test_hoja_sufijo OK")
