"""BE-CR0-02: dos lectores con la misma escala y textos de fuente distintos -> unir fallaba; normalizar une. Valores distintos = error."""
import json, os, subprocess, sys, tempfile
AQ = os.path.dirname(os.path.abspath(__file__))
def run(frags):
    d = tempfile.mkdtemp(); o = tempfile.mkdtemp()
    for n, f in frags.items(): json.dump(f, open(os.path.join(d, n), "w"))
    p = subprocess.run([sys.executable, os.path.join(AQ, "normalizar_fragmentos.py"), d, o], capture_output=True, text=True)
    return p.returncode, (json.load(open(os.path.join(o, "00_comunes.json"))) if os.path.exists(os.path.join(o, "00_comunes.json")) else None)
def test_iguales_se_unen():
    rc, c = run({"a.json": {"constants": {"plan_scale_by_sheet": {"A2.01": {"value": 9.0, "source": "x"}}, "plan_scale_pt_per_ft": {"value": 9.0, "source": "x"}}},
                 "b.json": {"constants": {"plan_scale_by_sheet": {"A2.01": {"value": 9.0, "source": "y"}, "A6.00": {"value": 18.0, "source": "z"}}, "plan_scale_pt_per_ft": {"value": 18.0, "source": "z"}}}})
    assert rc == 0 and c["constants"]["plan_scale_by_sheet"]["A2.01"]["source"] == "x | y" and c["constants"]["plan_scale_pt_per_ft"]["value"] == 9.0
def test_distintos_fallan():
    rc, _ = run({"a.json": {"constants": {"plan_scale_by_sheet": {"A2.01": {"value": 9.0, "source": "x"}}}},
                 "b.json": {"constants": {"plan_scale_by_sheet": {"A2.01": {"value": 18.0, "source": "y"}}}}})
    assert rc == 1
if __name__ == "__main__":
    test_iguales_se_unen(); test_distintos_fallan(); print("OK")
