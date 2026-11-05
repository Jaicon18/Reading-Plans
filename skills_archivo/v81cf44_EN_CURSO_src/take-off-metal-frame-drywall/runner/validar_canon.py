#!/usr/bin/env python3
"""validar_canon.py — valida un canon con canon.py del skill (esquema + compuertas) en un directorio temporal.
Uso: python3 validar_canon.py <canon.json> [<tools_dir>]   -> imprime "CANON OK" (rc 0) o "CANON ERROR: ..." (rc 1).
Es el mismo canon.py (+ inventario.py) que corre el runner después: si aquí falla, allá también.
Sin constants.plan_scale_pt_per_ft canon.py salta el cruce band vs length_ft (#13B): por eso es obligatoria aquí."""
import json
import os
import subprocess
import sys
import tempfile

canon = os.path.abspath(sys.argv[1])
tools = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
c = json.load(open(canon))
if not (c.get("constants") or {}).get("plan_scale_pt_per_ft"):
    print("CANON ERROR: constants.plan_scale_pt_per_ft {value, source} obligatoria (inventario.py; sin ella canon.py no "
          "cruza band vs length_ft)")
    sys.exit(1)
sin = [w.get("id") for w in c.get("walls") or [] if isinstance(w.get("band"), dict) and not w["band"].get("sheet")]
if sin:
    print(f"CANON ERROR: band.sheet obligatorio en cada band: {sin[:10]}")
    sys.exit(1)
with tempfile.TemporaryDirectory() as d:
    p = subprocess.run([sys.executable, os.path.join(tools, "canon.py"), canon, d], capture_output=True, text=True)
    if p.returncode == 0:
        p = subprocess.run([sys.executable, os.path.join(tools, "inventario.py"), canon, os.path.join(d, "inv.json")],
                           capture_output=True, text=True)
    if p.returncode == 0:
        print("CANON OK")
        sys.exit(0)
    err = [l for l in (p.stdout + p.stderr).splitlines() if "ERROR" in l or "Error" in l] or (p.stdout + p.stderr).splitlines()[-3:]
    print("CANON ERROR: " + " | ".join(err)[-1500:])
    sys.exit(1)
