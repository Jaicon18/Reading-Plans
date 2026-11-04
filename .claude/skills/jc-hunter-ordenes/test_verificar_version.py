#!/usr/bin/env python3
"""test_verificar_version.py — BE-121 / U-020 / U-027: verificar_version.py FALLA cuando una regla "programa" del registro
no tiene chequeo + test (revisar_registro), cuando el zip del skill no cumple (revisar_zip) y cuando la versión vigente del
INDICE.md no tiene zip (revisar_indice). Uso: python3 -I test_verificar_version.py  (o verificar_version.py --selftest)"""
import json
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verificar_version as V  # noqa: E402

U = "U-"   # ids armados en tiempo de corrida: el texto del test no debe parecer una regla acumulada (PAT)


def skill(reg, tools=None):
    d = tempfile.mkdtemp(prefix="vv_")
    s = os.path.join(d, "take-off-metal-frame-drywall")
    os.makedirs(os.path.join(s, "tools"))
    open(os.path.join(s, "SKILL.md"), "w").write("---\nname: take-off-metal-frame-drywall\ndescription: x\n---\n")
    json.dump({"reglas": reg}, open(os.path.join(s, "REGLAS_REGISTRO.json"), "w"))
    for n, t in (tools or {}).items():
        open(os.path.join(s, "tools", n), "w").write(t)
    return d


def ordenes(bes=("BE-Q1",), alc=("R-ALC-01",)):
    d = tempfile.mkdtemp(prefix="ord_")
    open(os.path.join(d, "BIBLIOTECA_ERRORES.md"), "w").write("\n".join(f"| {b} | x | y | z | w |" for b in bes))
    open(os.path.join(d, "REGLAS_ALCANCE.md"), "w").write("\n".join(f"## {a} — x" for a in alc))
    return d


OK = {"id": "BE-Q1", "categoria": "programa", "chequeos": ["take-off:tools/gate.py::ce_x"],
      "test": {"archivo": "take-off:tools/test_gate.py", "token": "ce_x"}}
ALC = {"id": "R-ALC-01", "categoria": "conducta"}
TOOLS = {"gate.py": "def ce_x(c):\n    return 1\n", "test_gate.py": "import gate\nassert gate.ce_x(0)\n"}


def revisar_registro():
    o = ordenes()
    assert V.revisar_registro(V.Fuente(skill([OK, ALC], TOOLS)), o) == []
    sin_test = dict(OK, test=None)
    assert any("sin test" in x for x in V.revisar_registro(V.Fuente(skill([sin_test, ALC], TOOLS)), o))
    sin_fn = dict(OK, chequeos=["take-off:tools/gate.py::ce_y"])
    assert any("no tiene ce_y" in x for x in V.revisar_registro(V.Fuente(skill([sin_fn, ALC], TOOLS)), o))
    sin_token = dict(TOOLS, **{"test_gate.py": "print(1)\n"})
    assert any("no cita" in x for x in V.revisar_registro(V.Fuente(skill([OK, ALC], sin_token)), o))
    h = {"id": U + "001", "categoria": "historico", "reemplazada_por": U + "999"}
    assert any("histórica" in x for x in V.revisar_registro(V.Fuente(skill([OK, ALC, h], TOOLS)), o))
    p = {"id": U + "002", "categoria": "programa-pendiente", "motivo": ""}
    assert any("sin motivo" in x for x in V.revisar_registro(V.Fuente(skill([OK, ALC, p], TOOLS)), o))
    assert any("BE-Q2" in x for x in V.revisar_registro(V.Fuente(skill([OK, ALC], TOOLS)), ordenes(bes=("BE-Q1", "BE-Q2"))))
    sk = skill([OK, ALC], TOOLS)
    os.remove(os.path.join(sk, "take-off-metal-frame-drywall", "REGLAS_REGISTRO.json"))
    assert V.revisar_registro(V.Fuente(sk), o)
    c = tempfile.mkdtemp()
    open(os.path.join(c, "REGLAS_USUARIO_CLAUDE.md"), "w").write(f"# x\n## REGLAS VIGENTES\n- [{U}003 · conducta] a\n- regla sin id\n")
    open(os.path.join(c, "REGLAS_HISTORICO.md"), "w").write(f"- [{U}001 · REEMPLAZADA por {U}003] b\n")
    f = V.revisar_registro(V.Fuente(skill([OK, ALC], TOOLS)), o, c)
    assert any(U + "003" in x for x in f) and any(U + "001" in x for x in f) and any("sin id" in x for x in f), f


def revisar_zip():
    d = skill([OK, ALC], TOOLS)
    z = os.path.join(d, "s.zip")
    with zipfile.ZipFile(z, "w") as zz:
        zz.writestr("take-off-metal-frame-drywall/SKILL.md", "---\nname: a\ndescription: b\n---\n")
        zz.writestr("take-off-metal-frame-drywall/tools/a.py", "x")
    assert V.revisar_zip(z) == []
    with zipfile.ZipFile(z, "w") as zz:
        zz.writestr("take-off-metal-frame-drywall/", "")
        zz.writestr("take-off-metal-frame-drywall/SKILL.md", "sin yaml")
        zz.writestr("take-off-metal-frame-drywall/tools/__pycache__/a.pyc", "x")
        zz.writestr("take-off-metal-frame-drywall/tools.orig_v1/a.py", "x")
        for i in range(200):
            zz.writestr(f"take-off-metal-frame-drywall/r/{i}.md", "x")
    f = " ".join(V.revisar_zip(z))
    for k in ("< 200", "directorio", "__pycache__", "tools.orig_", "YAML"):
        assert k in f, (k, f)


def revisar_indice():
    d = tempfile.mkdtemp()
    open(os.path.join(d, "INDICE.md"), "w").write("**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v9x = algo)**\n")
    assert V.revisar_indice(d)
    open(os.path.join(d, "take-off-metal-frame-drywall_v9x_P_2026-11-03.zip"), "w").write("x")
    assert V.revisar_indice(d) == []
    # BE-CF20: dos zips con el mismo número de versión = línea partida
    open(os.path.join(d, "take-off-metal-frame-drywall_v9x_Q_2026-11-03.zip"), "w").write("y")
    assert any("BE-CF20" in x for x in V.revisar_indice(d))


def revisar_skill():
    """BE-87 (choque de numeración R80e.49 trim / formato de RFI) y BE-VS-11 (A_NO_DIBUJADO sin clasificar nunca corría)."""
    d = skill([OK, ALC], dict(TOOLS, **{"reglas.py": '@chequeo("A_NO_DIBUJADO", "x")\ndef f(c):\n    return []\n',
                                        "reglas_clasificacion.py": 'X = {"R1": A("A_OTRA")}\n'}))
    s = os.path.join(d, "take-off-metal-frame-drywall", "SKILL.md")
    open(s, "a").write("### R80e.49 — Trim por programa\nx\n### R80e.49 — Formato de RFI A/B/C\ny\n")
    f = " ".join(V.revisar_skill(V.Fuente(d)))
    assert "BE-87" in f and "R80e.49" in f and "BE-VS-11" in f and "A_NO_DIBUJADO" in f, f
    open(s, "w").write("---\nname: t\ndescription: x\n---\n### R80e.49 — Trim por programa\n### R80e.50 — Formato de RFI\n")
    open(os.path.join(d, "take-off-metal-frame-drywall", "tools", "reglas_clasificacion.py"), "w").write('X = {"R1": A("A_NO_DIBUJADO")}\n')
    assert V.revisar_skill(V.Fuente(d)) == []


def revisar_banco():
    """U-043 / BE-94 (R80e.43 validado con una sola corrida): la versión vigente debe registrar el banco con 0 distintas."""
    d = tempfile.mkdtemp()
    p = os.path.join(d, "INDICE.md")
    open(p, "w").write("**03-nov: v9x = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v9w + arreglo. Probado con la corrida #4.\n")
    assert V.revisar_banco(d)
    open(p, "w").write("**03-nov: v9x = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v9w + arreglo. Banco #3 / #4 / #5 = 3 familias distintas.\n")
    assert V.revisar_banco(d)
    open(p, "w").write("**03-nov: v9x = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v9w. Banco B&N / VS / Chuze = 0 familias distintas.\n")
    assert V.revisar_banco(d) == []


def revisar_ordenes():
    import json, tempfile, datetime
    d = tempfile.mkdtemp(); c = os.path.join(d, "ORDENES_CRUDAS"); os.makedirs(c)
    viejo = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=30)).isoformat(timespec="seconds")
    open(os.path.join(c, "_entrantes.jsonl"), "w").write(json.dumps({"id": "abc", "ts_utc": viejo, "texto": "siempre 2 layers"}) + "\n")
    open(os.path.join(c, "MAPA_ORDENES.json"), "w").write("{}")
    assert V.revisar_ordenes(d), "orden sin clasificar debe fallar (U-136)"
    open(os.path.join(c, "MAPA_ORDENES.json"), "w").write(json.dumps({"abc": "U-127"}))
    assert not V.revisar_ordenes(d), "orden clasificada debe pasar"


def correr():
    for f in (revisar_registro, revisar_zip, revisar_indice, revisar_skill, revisar_banco, revisar_ordenes):
        f()
        print("ok", f.__name__)
    print("test_verificar_version OK")


if __name__ == "__main__":
    correr()
