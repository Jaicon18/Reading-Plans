#!/usr/bin/env python3
"""validar_canon.py — valida un canon con canon.py del skill (esquema + compuertas) en un directorio temporal.
Uso: python3 validar_canon.py <canon.json> [<tools_dir>]   -> imprime "CANON OK" (rc 0) o "CANON ERROR: ..." (rc 1).
Es el mismo canon.py que corre el runner después: si aquí falla, allá también."""
import os
import subprocess
import sys
import tempfile

canon = os.path.abspath(sys.argv[1])
tools = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
with tempfile.TemporaryDirectory() as d:
    p = subprocess.run([sys.executable, os.path.join(tools, "canon.py"), canon, d], capture_output=True, text=True)
    if p.returncode == 0:
        print("CANON OK")
        sys.exit(0)
    err = [l for l in (p.stdout + p.stderr).splitlines() if "ERROR" in l or "Error" in l] or (p.stdout + p.stderr).splitlines()[-3:]
    print("CANON ERROR: " + " | ".join(err)[-1500:])
    sys.exit(1)
