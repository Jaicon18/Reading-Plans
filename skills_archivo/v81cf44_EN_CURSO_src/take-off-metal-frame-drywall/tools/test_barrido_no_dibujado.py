#!/usr/bin/env python3
"""test_barrido_no_dibujado.py — R80f.3 / R-ALC-11 / BE-116: falla con el dato malo (sintético)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglas as R
malo = {"materials": [{"material": "Lateral bracing struts (gyp ceiling)", "unit": "LF", "net": 0,
                       "source": "EXCLUDED - not shown on RCP"}]}
assert R.barrido_no_dibujado_fallas(malo), "debía fallar sin barrido"
medio = dict(malo, barrido_no_dibujado=[{"item": "lateral bracing struts", "specs": "", "schedule": "none", "estructural": "none"}])
assert R.barrido_no_dibujado_fallas(medio), "debía fallar con specs vacío"
bueno = dict(malo, barrido_no_dibujado=[{"item": "lateral bracing struts", "specs": "none (swept sheets A-90x)",
                                          "schedule": "none", "estructural": "found S-801 C3 -> loaded elsewhere"}])
assert not R.barrido_no_dibujado_fallas(bueno), R.barrido_no_dibujado_fallas(bueno)
otro = {"materials": [{"material": "3-5/8\" stud", "unit": "LF", "net": 0, "source": "not shown"}]}
assert not R.barrido_no_dibujado_fallas(otro)
print("test_barrido_no_dibujado OK")
