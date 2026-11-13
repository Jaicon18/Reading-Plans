import sys; sys.path.insert(0, "/tmp/v138r3/take-off-metal-frame-drywall/tools")
import tempfile; tempfile.tempdir = "/tmp/verif10/tmp"
import test_compuerta_entrega as T
T.test_v138_protocolo_rev_posterior_solo_sus_pasos()
for n in dir(T):
    if n.startswith("test_v138_protocolo") and n != "test_v138_protocolo_rev_posterior_solo_sus_pasos":
        getattr(T, n)(); print(n, "OK")
