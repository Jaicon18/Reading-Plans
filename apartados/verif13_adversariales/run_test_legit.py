import sys; sys.path.insert(0, "/tmp/v139p/take-off-metal-frame-drywall/tools")
import tempfile, os; os.makedirs("/tmp/verif13/tmp/tests", exist_ok=True); tempfile.tempdir = "/tmp/verif13/tmp/tests"
import test_compuerta_entrega as T
for n in sorted(dir(T)):
    if n.startswith(("test_v138_protocolo", "test_v138r2_protocolo", "test_v139_protocolo")):
        try: getattr(T, n)(); print(n, "OK")
        except Exception as e: print(n, "FALLA", type(e).__name__, e)
