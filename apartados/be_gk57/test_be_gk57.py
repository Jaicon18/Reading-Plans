"""Test BE-GK57 with the real cases (Grand Kia rev3b): resuelto_Z1.rev3a.bak.json in etapas/4_canon -> FAIL; CADENA.prev.md -> FAIL;
entrega_rev3a/ in the work dir -> FAIL; the same files under bak_rev3a/ and entregas_previas/ -> PASS."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import be_gk57 as G
w = tempfile.mkdtemp()
def mk(p):
    os.makedirs(os.path.dirname(os.path.join(w, p)), exist_ok=True); open(os.path.join(w, p), "w").write("x")
mk("etapas/4_canon/resuelto_Z1.json"); mk("etapas/4_canon/resuelto_Z1.rev3a.bak.json")
assert G.fallas(w, "rev3b"), "backup next to its input must FAIL"
os.remove(os.path.join(w, "etapas/4_canon/resuelto_Z1.rev3a.bak.json")); mk("burbujas/CADENA.md"); mk("burbujas/CADENA.prev.md")
assert G.fallas(w, "rev3b"), ".prev copy must FAIL"
os.remove(os.path.join(w, "burbujas/CADENA.prev.md")); os.makedirs(os.path.join(w, "entrega_rev3a"))
assert G.fallas(w, "rev3b"), "previous delivery in the work dir must FAIL"
os.rmdir(os.path.join(w, "entrega_rev3a")); os.makedirs(os.path.join(w, "entrega_rev3b")); mk("bak_rev3a/resuelto_Z1.rev3a.bak.json"); mk("bak_rev3a/CADENA.prev.md")
assert not G.fallas(w, "rev3b"), "copies under bak_<rev>/ and the current delivery pass"
print("test_be_gk57 OK")
