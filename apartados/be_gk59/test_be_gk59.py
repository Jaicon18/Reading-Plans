"""Test BE-GK59 with the real case (Grand Kia rev3b): VERDE 60914f5fc798 01:05 -> upload 01:43 -> re-run 7819a4ce749e 01:47 ROJA
overwrote ENTREGA_OK.json = FAIL; with guardar() per run and the uploaded run's ENTREGA_OK kept = PASS."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import be_gk59 as G
w = tempfile.mkdtemp()
def wj(n, d): json.dump(d, open(os.path.join(w, n), "w"))
open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write(
    json.dumps({"evento": "fin", "corrida": "60914f5fc798", "ts": "2026-11-13T01:05:13+00:00", "ok": True}) + "\n" +
    json.dumps({"evento": "fin", "corrida": "7819a4ce749e", "ts": "2026-11-13T01:47:38+00:00", "ok": False}) + "\n")
wj("SUBIDA_OK.json", {"primera_subida_iso": "2026-11-13T01:43:19+00:00"})
wj("ENTREGA_OK.json", {"ok": True, "fecha_iso": "2026-11-13T01:05:13+00:00", "skill_version": "v81cf129"})
G.guardar(w, "60914f5fc798")
assert not G.fallas(w), "uploaded run's ENTREGA_OK kept and current = PASS"
wj("ENTREGA_OK.json", {"ok": False, "fecha_iso": "2026-11-13T01:47:38+00:00", "skill_version": "v81cf130"})
assert G.fallas(w), "a re-run after the upload that overwrites ENTREGA_OK.json = FAIL"
os.remove(os.path.join(w, "ENTREGA_OK_60914f5fc798.json")); wj("ENTREGA_OK.json", {"ok": True, "fecha_iso": "2026-11-13T01:05:13+00:00"})
assert G.fallas(w), "without ENTREGA_OK_<corrida>.json of the uploaded run = FAIL"
print("test_be_gk59 OK")
