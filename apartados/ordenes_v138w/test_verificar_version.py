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

AQUI_T = os.path.dirname(os.path.abspath(__file__))
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


def indice_encabezado():
    """BE-146 (6-nov): v81cf55..v81cf57 publicadas y el encabezado de INDICE.md seguía en 'hoy v81cf54'."""
    d = tempfile.mkdtemp()
    cab = "**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf54 = v81cf52 + proposal)**\n\n"
    lin = "".join(f"**06-nov: {v} = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = x\n\n" for v in ("v81cf54", "v81cf55", "v81cf56", "v81cf57"))
    open(os.path.join(d, "INDICE.md"), "w").write(cab + lin)
    for v in ("v81cf54", "v81cf57"):
        open(os.path.join(d, f"take-off-metal-frame-drywall_{v}_P_2026-11-06.zip"), "w").write(v)
    r = V.revisar_indice_encabezado(d)
    assert r and "BE-146" in r[0] and "v81cf54" in r[0] and "v81cf57" in r[0], r
    assert any("BE-146" in x for x in V.revisar_indice(d)), "revisar_indice (main) debe correr el chequeo del encabezado"
    open(os.path.join(d, "INDICE.md"), "w").write(cab.replace("hoy v81cf54", "hoy v81cf57") + lin)
    assert V.revisar_indice_encabezado(d) == [] and V.revisar_indice(d) == []


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


def hook_solo_usuario():
    """BE-143: el hook U-136 guardó 32 avisos automáticos (task-notification, agent-message) como órdenes."""
    import importlib.util
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    spec = importlib.util.spec_from_file_location("ro", os.path.join(raiz, "hooks", "registrar_orden.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for auto in ("<task-notification> <task-id>x</task-id>", "<agent-message from=\"a\"> [Subagent hand-back]",
                 "<cross-session-message from-session=\"s\">", "[SYSTEM NOTIFICATION - NOT USER INPUT] x",
                 "<system-reminder>x</system-reminder>",
                 "This session's worker process was restarted. If your previous turn was already complete, take no action and wait for the "
                 "next event. Otherwise, continue from where you left off.",                          # v132: id 3b88645a6b4d
                 "This session is being continued from a previous conversation that ran out of context."):
        assert not m.es_del_usuario(auto), auto
    assert m.es_del_usuario("the worker process was restarted? revisa la subida"), "una frase del usuario que lo menciona sí se guarda"
    assert not m.es_del_usuario("mi password es x")
    assert m.es_del_usuario("si el type dice BOTH SIDES van las dos caras")


def versiones_unicas():
    """BE-144: v81cf43 armada por dos sesiones."""
    d = tempfile.mkdtemp()
    for n, x in (("take-off-metal-frame-drywall_v81cf43_A_2026-11-05.zip", "a"), ("take-off-metal-frame-drywall_v81cf43_B_2026-11-05.zip", "b")):
        open(os.path.join(d, n), "w").write(x)
    open(os.path.join(d, "take-off-metal-frame-drywall_v81cf42_X_2026-11-05.zip"), "w").write("same")
    open(os.path.join(d, "take-off-metal-frame-drywall_v81cf42_FINAL-P_2026-11-05.zip"), "w").write("same")
    assert V.revisar_versiones_unicas(d), "número repetido debe fallar"
    os.remove(os.path.join(d, "take-off-metal-frame-drywall_v81cf43_B_2026-11-05.zip"))
    assert V.revisar_versiones_unicas(d) == []


def zip_200_bexf08():
    """BE-XF08 (Xfinity 11-nov): v81cf86 se publicó con 208 archivos porque verificar_version se corrió sobre la CARPETA (el límite
    solo se contaba en un .zip). Carpeta con 200 archivos = FAIL; 199 = OK; zip vigente de INDICE con 200 archivos = FAIL."""
    d = tempfile.mkdtemp()
    sk = os.path.join(d, "take-off-metal-frame-drywall")
    os.makedirs(os.path.join(sk, "tools"))
    open(os.path.join(sk, "SKILL.md"), "w").write("---\nname: a\ndescription: b\n---\n")
    for i in range(198):
        open(os.path.join(sk, "tools", f"t{i}.py"), "w").write("x")
    assert V.revisar_zip(d) == [], V.revisar_zip(d)                 # 199 archivos
    open(os.path.join(sk, "tools", "t198.py"), "w").write("x")
    assert any("BE-XF08" in x for x in V.revisar_zip(d)), "200 archivos en la carpeta debe fallar"
    a = tempfile.mkdtemp()
    open(os.path.join(a, "INDICE.md"), "w").write("**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v9y = algo)**\n")
    with zipfile.ZipFile(os.path.join(a, "take-off-metal-frame-drywall_v9y_P_2026-11-11.zip"), "w") as z:
        z.writestr("take-off-metal-frame-drywall/SKILL.md", "---\nname: a\ndescription: b\n---\n")
        for i in range(199):
            z.writestr(f"take-off-metal-frame-drywall/tools/t{i}.py", "x")
    assert any("BE-XF08" in x for x in V.revisar_indice(a)), "zip vigente con 200 archivos debe fallar"


def postmortem_u185():
    """U-185 + post-mortem 2026-11-12b: último proyecto cerrado sin post-mortem = falta; cierre = fecha_iso de la ÚLTIMA subida (todos los
    SUBIDA_OK*.json, hora completa); solo cuenta el post-mortem MÁS NUEVO: uno limpio más viejo no tapa uno nuevo con WEAK; uno con hora
    anterior al cierre no vale; 'conducta' sin motivo sigue abierto. Datos sintéticos."""
    c = tempfile.mkdtemp(prefix="pm_")
    os.makedirs(os.path.join(c, "proy_x"))
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00", "fecha_iso": "2026-11-11T16:25:00+00:00"},
              open(os.path.join(c, "proy_x", "SUBIDA_OK_rev19.json"), "w"))
    json.dump({"primera_subida_iso": "2026-11-11T16:25:00+00:00", "fecha_iso": "2026-11-12T22:10:00+00:00"},
              open(os.path.join(c, "proy_x", "SUBIDA_OK.json"), "w"))
    assert any("sin cache_proyectos/POSTMORTEM" in x for x in V.revisar_postmortem(c)), V.revisar_postmortem(c)
    cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
    limpio = cab + "| BE-Q1 | x | ce_x | test_x | OK |\n| BE-Q2 | y | conducta | — | conducta: no se puede leer desde un programa |\n"
    open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12.md"), "w").write("# PM 2026-11-12 14:00 PT\n" + limpio)
    r = V.revisar_postmortem(c)
    assert r and "anterior al cierre" in r[0], r                       # cierre 22:10 UTC = 14:10 PT: el de las 14:00 PT no vale
    open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12.md"), "w").write("# PM 2026-11-12 15:00 PT\n" + limpio)
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)
    open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b.md"), "w").write(
        "# PM b 2026-11-12 16:00 PT\n" + cab + "| BE-Q2 | y | conducta | — | conducta |\n" + "".join(f"| BE-W{k} | z | n | — | WEAK |\n" for k in range(7)))
    r = V.revisar_postmortem(c)
    assert r and "7 WEAK" in r[0] and "BE-Q2" in r[0] and "12b" in r[0], r   # el caso de hoy: el limpio más viejo NO lo tapa
    pb = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b.md")         # verificación 12b: (1) principal sin tabla = falla, no pasa en vacío
    open(pb, "w").write("# PM b 2026-11-12 16:00 PT\nsin tabla\n")
    r = V.revisar_postmortem(c)
    assert r and "sin la tabla principal" in r[0], r
    open(pb, "w").write("# PM b 2026-11-12 16:00 PT\n" + limpio)
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)
    pv = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md")   # (2) verificación con WEAK = abierto
    open(pv, "w").write("# VERIF\nFecha: 2026-11-01 17:00 PT\n" + cab + "| BE-Q1 | x | ce_x | test_x | WEAK — STILL-WEAK |\n"
                        "| BE-Q9 | x | ce_x | test_x | WEAK — STILL-WEAK |\n")
    r = V.revisar_postmortem(c)
    assert r and "BE-Q1" in r[0] and "2 WEAK" in r[0] and "_VERIFICACION" in r[0], r
    pv3 = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md")     # verificación 2 (A3b): una nueva SIN tabla = falla y
    open(pv3, "w").write("# VERIF 3\nFecha: 2026-11-01 19:00 PT\nsin tabla, todo bien\n")   # no borra los WEAK de la anterior
    r = V.revisar_postmortem(c)
    assert any("sin la tabla" in x for x in r) and any("BE-Q1" in x and "BE-Q9" in x for x in r), r
    open(pv3, "w").write("# VERIF 3\nFecha: 2026-11-01 19:00 PT\n" + cab + "| BE-Q1 | x | ce_x | test_x | OK — CONFIRMED-CLOSED |\n")
    r = V.revisar_postmortem(c)                                          # (A4) la nueva cierra Q1 y OMITE Q9: Q9 sigue abierto
    assert r and "BE-Q9" in r[0] and "BE-Q1" not in r[0] and "1 WEAK" in r[0], r
    open(pv3, "w").write("# VERIF 3\nFecha: 2026-11-01 19:00 PT\n" + cab + "| BE-Q1 | x | ce_x | test_x | OK |\n| BE-Q9 | x | x | x | OK — CONFIRMED-CLOSED |\n")
    r = V.revisar_postmortem(c)                                          # 'OK' sin CONFIRMED-CLOSED no cierra
    assert r and "BE-Q1" in r[0] and "BE-Q9" not in r[0], r
    open(pv3, "w").write("# VERIF 3\nFecha: 2026-11-01 19:00 PT\n" + cab + "| BE-Q1 | x | ce_x | test_x | OK — CONFIRMED-CLOSED |\n"
                         "| BE-Q9 | x | x | x | OK — CONFIRMED-CLOSED |\n")
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)       # una verificación más nueva que cierra todo explícitamente
    pc = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b_CIERRE.md")              # un _CIERRE nunca relaja: abierto en él = abierto
    open(pc, "w").write("# CIERRE 2026-11-12 18:30 PT\n" + cab + "| BE-Q3 | x | ce_x | — | WEAK |\n")
    r = V.revisar_postmortem(c)
    assert r and "BE-Q3" in r[0], r
    os.remove(pc)
    os.remove(pv3)
    os.remove(pv)
    causas = "\n| # | causa | candado | estado |\n|---|---|---|---|\n| 3.1 | x | — | **NO GUARD** |\n| 3.2 | y | ce_y | candado OK |\n"
    open(pb, "w").write("# PM b 2026-11-12 16:00 PT\n" + limpio + causas)            # (3) tabla de causas con NO GUARD = abierto
    r = V.revisar_postmortem(c)
    assert r and "1 NO GUARD" in r[0] and "causa 3.1" in r[0] and "3.2" not in r[0], r
    open(pv, "w").write("# VERIF\nFecha: 2026-11-01 17:00 PT\n" + cab + "| NG-3.1 / BE-Q4 | x | x | x | OK — CONFIRMED-CLOSED |\n")
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)       # la verificación cierra la causa 3.1 por su id NG-3.1
    os.remove(pv)
    pvx = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md")      # v120 (verificación 3, C4): el cierre es el estado EXACTO
    open(pb, "w").write("# PM b 2026-11-12 16:00 PT\n" + cab + "| BE-Q5 | y | z | — | WEAK |\n")
    open(pvx, "w").write("# VERIF\nFecha: 2026-11-01 17:00 PT\n" + cab + "| BE-Q5 | y | z | — | WEAK — NOT CONFIRMED-CLOSED |\n")
    r = V.revisar_postmortem(c)
    assert r and "BE-Q5" in r[0], r
    open(pvx, "w").write("# VERIF\nFecha: 2026-11-01 17:00 PT\n" + cab + "| BE-Q5 | y | z | — | OK — CONFIRMED-CLOSED |\n")
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)
    os.remove(pvx)
    pcc = os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c.md")        # (C1 / A2) un principal nuevo con 1 renglón OK NO borra los del 12b
    open(pcc, "w").write("# PM c 2026-11-12 18:00 PT\n" + cab + "| BE-Q6 | y | z | — | OK |\n")
    r = V.revisar_postmortem(c)
    assert r and "BE-Q5" in r[0] and "12c" in r[0], r
    open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c_VERIFICACION.md"), "w").write(
        "# VERIF c\nFecha: 2026-11-01 19:00 PT\n" + cab + "| BE-Q5 | y | z | — | OK — CONFIRMED-CLOSED |\n")   # una verificación posterior lo cierra
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)
    os.remove(pcc)
    os.remove(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c_VERIFICACION.md"))
    open(pb, "w").write("# PM b 2026-11-12 16:00 PT\n" + limpio + causas)
    open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c_COPIA.md"), "w").write("# copia 2026-11-12 23:00 PT\n")   # no es principal
    r = V.revisar_postmortem(c)
    assert r and "12b.md" in r[0], r


def tests_llamados():
    """BE-CR42 / BE-GK47: un 'def test_…' que nadie llama = falta (correr_suite ejecuta el archivo como script)."""
    d = tempfile.mkdtemp(prefix="tl_")
    os.makedirs(os.path.join(d, "tools"))
    open(os.path.join(d, "SKILL.md"), "w").write("x")
    open(os.path.join(d, "tools", "test_x.py"), "w").write("def test_a():\n    pass\n\n\ndef test_b():\n    pass\n\n\ntest_a()\n")
    assert V.tests_sin_llamar(V.Fuente(d)) == ["test_x.py::test_b"], V.tests_sin_llamar(V.Fuente(d))
    open(os.path.join(d, "tools", "test_x.py"), "a").write("for f in (test_b,):\n    f()\n")
    assert V.tests_sin_llamar(V.Fuente(d)) == []


def prueba_abiertos_be_pm04():
    """verificación 12b (BE-PM04 STILL-WEAK): desde v81cf119 la versión del CANDIDATO necesita PRUEBA_ABIERTOS_<v>.json con TODOS los
    proyectos de PROYECTOS_ABIERTOS.json y 0 regresiones sin explicar; uno solo de tres no alcanza. Datos sintéticos."""
    a = tempfile.mkdtemp(prefix="pa_")
    c0 = tempfile.mkdtemp(prefix="pac0_")                               # cache con los proyectos de la lista (v120: el detector corre siempre)
    for nom in ("proy_a", "proy_b", "proy_c"):
        os.makedirs(os.path.join(c0, nom))
        open(os.path.join(c0, nom, "VERSION_PROYECTO.txt"), "w").write("2026-11-01T10:00:00+00:00 | rev1 | v81cf901 | \n")
    d = tempfile.mkdtemp(prefix="pac_")
    open(os.path.join(d, "SKILL.md"), "w").write("x\n**VERSION: v81cf901**\n")
    f = V.Fuente(d)
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "PROYECTOS_ABIERTOS" in r[0], r
    json.dump({"proyectos": ["proy_a", "proy_b", "proy_c"]}, open(os.path.join(a, "PROYECTOS_ABIERTOS.json"), "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "no tiene" in r[0], r
    pa = os.path.join(a, "PRUEBA_ABIERTOS_v81cf901.json")
    uno = {"version_candidata": "v81cf901", "ok": True, "regresiones": [], "proyectos": {"proy_a": {"regresiones": 0, "sha_tools": V.sha_tools(f), "vigente": {"PASS": 5}, "candidata": {"PASS": 5}}}}
    json.dump(uno, open(pa, "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "proy_b" in r[0] and "proy_c" in r[0], r                  # el caso de la verificación: un proyecto solo pasaba
    tres = dict(uno, proyectos={k: {"regresiones": 0, "sha_tools": V.sha_tools(f), "vigente": {"PASS": 5}, "candidata": {"PASS": 5}} for k in ("proy_a", "proy_b", "proy_c")})
    json.dump(tres, open(pa, "w"))
    assert V.revisar_prueba_abiertos(a, f, cache=c0) == [], V.revisar_prueba_abiertos(a, f, cache=c0)
    json.dump(dict(tres, ok=False, regresiones=[{"proyecto": "proy_b", "chequeo": "CE_X9", "explicacion": ""}]), open(pa, "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "proy_b:CE_X9" in str(r), r
    sha = V.sha_tools(f)                                                 # verificación 2 (B2): el PRUEBA está atado al sha de las tools
    json.dump(dict(tres, proyectos={k: {"regresiones": 0, "sha_tools": "viejo", "vigente": {"PASS": 5}, "candidata": {"PASS": 5}} for k in ("proy_a", "proy_b", "proy_c")}), open(pa, "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "otras tools" in r[0], r
    json.dump(dict(tres, proyectos={k: {"regresiones": 0, "sha_tools": sha, "vigente": {"PASS": 5}, "candidata": {"PASS": 5}} for k in ("proy_a", "proy_b", "proy_c")}), open(pa, "w"))
    assert V.revisar_prueba_abiertos(a, f, cache=c0) == [], V.revisar_prueba_abiertos(a, f, cache=c0)
    os.makedirs(os.path.join(d, "tools"), exist_ok=True)
    open(os.path.join(d, "tools", "x.py"), "w").write("y = 1\n")         # cambiar una tool cambia el sha
    assert V.revisar_prueba_abiertos(a, V.Fuente(d), cache=c0), "un build distinto del mismo v81cf901 no vale"
    os.remove(os.path.join(d, "tools", "x.py"))
    json.dump({"proyectos": []}, open(os.path.join(a, "PROYECTOS_ABIERTOS.json"), "w"))   # (B1) lista vacía = falla
    json.dump(dict(tres, proyectos={}), open(pa, "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c0)
    assert r and "VACÍA" in r[0], r
    c = tempfile.mkdtemp(prefix="pac_cache_")                            # proyectos con entrega vigente sin CSV N/N que faltan en la lista
    for nom, fecha, csv_ok in (("proy_a", "2026-11-12T10:00:00+00:00", False), ("proy_d", "2026-11-12T11:00:00+00:00", False),
                               ("proy_e", "2026-11-12T12:00:00+00:00", True), ("proy_viejo", "2026-11-05T10:00:00+00:00", False)):
        os.makedirs(os.path.join(c, nom))
        json.dump({"fecha_iso": fecha}, open(os.path.join(c, nom, "SUBIDA_OK_rev2.json"), "w"))
        if csv_ok:
            os.makedirs(os.path.join(c, nom, "CSV_BLUEBEAM_rev2"))
            open(os.path.join(c, nom, "CSV_BLUEBEAM_rev2", "RESULTADO.md"), "w").write("Comparado: 2026-11-12 13:00 UTC\n- comparar: 10 CSV / 10 PDF / 10 emparejados; 0 faltantes")
    assert V.proyectos_abiertos_cache(c) == ["proy_a", "proy_d"], V.proyectos_abiertos_cache(c)   # proy_e: CSV N/N con Comparado: posterior
    json.dump({"proyectos": ["proy_a", "proy_b", "proy_c"]}, open(os.path.join(a, "PROYECTOS_ABIERTOS.json"), "w"))
    json.dump(dict(tres, proyectos={k: {"regresiones": 0, "sha_tools": sha, "vigente": {"PASS": 5}, "candidata": {"PASS": 5}} for k in ("proy_a", "proy_b", "proy_c")}), open(pa, "w"))
    r = V.revisar_prueba_abiertos(a, f, cache=c)
    assert r and "proy_d" in str(r) and "proy_viejo" not in str(r), r
    # v120 (verificación 3): P4b SUBIDA_OK.json sin rev más nuevo que el CSV, P4c VERSION_PROYECTO más nuevo, P4d '3 faltantes' = abiertos
    c2 = tempfile.mkdtemp(prefix="pac2_")
    csv_ = "- Comparado: 2026-11-11 12:00 UTC\n- comparar: 10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"
    def proy(nom, extra):
        os.makedirs(os.path.join(c2, nom, "CSV_BLUEBEAM_rev1"))
        json.dump({"fecha_iso": "2026-11-11T10:00:00+00:00"}, open(os.path.join(c2, nom, "SUBIDA_OK_rev1.json"), "w"))
        open(os.path.join(c2, nom, "CSV_BLUEBEAM_rev1", "RESULTADO.md"), "w").write(extra.pop("_csv", csv_))
        for f, v in extra.items():
            open(os.path.join(c2, nom, f), "w").write(json.dumps(v) if isinstance(v, dict) else v)
    proy("cerrado", {})
    proy("p4b", {"SUBIDA_OK.json": {"fecha_iso": "2026-11-12T10:00:00+00:00"}})
    proy("p4c", {"VERSION_PROYECTO.txt": "2026-11-12T10:00:00+00:00 | rev2 | v81cf901 | \n"})
    proy("p4d", {"_csv": csv_ + "- 3 faltantes en el PDF\n"})
    proy("sin_fecha", {"_csv": "- 10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"})
    assert V.proyectos_abiertos_cache(c2) == ["p4b", "p4c", "p4d", "sin_fecha"], V.proyectos_abiertos_cache(c2)
    a3 = tempfile.mkdtemp(prefix="pa3_")                                # P3 / P3b / P5 / P6 / P8 sobre la versión del candidato
    for nom in ("proy_a",):
        os.makedirs(os.path.join(c2, nom), exist_ok=True)
        open(os.path.join(c2, nom, "VERSION_PROYECTO.txt"), "w").write("2026-11-01T10:00:00+00:00 | rev1 | v81cf901 | \n")
    json.dump({"proyectos": ["proy_a", "p4b", "p4c", "p4d", "sin_fecha"]}, open(os.path.join(a3, "PROYECTOS_ABIERTOS.json"), "w"))
    bien = {k: {"sha_tools": sha, "regresiones": 0, "vigente": {"FAIL": 1}, "candidata": {"FAIL": 1}} for k in ("proy_a", "p4b", "p4c", "p4d", "sin_fecha")}
    pa3 = os.path.join(a3, "PRUEBA_ABIERTOS_v81cf901.json")
    def prueba(proyectos, **top):
        json.dump(dict({"version_candidata": "v81cf901", "ok": True, "regresiones": [], "proyectos": proyectos}, **top), open(pa3, "w"))
        return V.revisar_prueba_abiertos(a3, f, cache=c2)
    assert prueba(bien) == [], prueba(bien)
    assert any("proy_a" in x for x in prueba(dict(bien, proy_a=dict(bien["proy_a"], regresiones=5, sin_explicar=5))))   # P3
    assert any("proy_a" in x for x in prueba(dict(bien, proy_a=dict(bien["proy_a"], candidata={"FAIL": 12}))))           # P3b
    assert any("versión None" in x for x in prueba(bien, version_candidata=None))                                       # P5
    json.dump({"proyectos": ["proy_a", "p4b", "p4c", "p4d", "sin_fecha", "zz_fake"]}, open(os.path.join(a3, "PROYECTOS_ABIERTOS.json"), "w"))
    assert any("zz_fake" in x for x in prueba(dict(bien, zz_fake=bien["proy_a"])))                                      # P6
    json.dump({"proyectos": ["proy_a"]}, open(os.path.join(a3, "PROYECTOS_ABIERTOS.json"), "w"))
    assert any("cache_proyectos" in x for x in V.revisar_prueba_abiertos(a3, f))                                        # P8: sin cache
    open(os.path.join(d, "SKILL.md"), "w").write("x\n**VERSION: v81cf118**\n")       # versiones anteriores a v81cf119: no se exige
    assert V.revisar_prueba_abiertos(a, V.Fuente(d), cache=c0) == []


def adv4_postmortem():
    """verificación 4 (adv4_pm, sintético): norm_txt común + 'Fecha:' explícita + cierre solo por la PRIMERA columna con match COMPLETO.
    D1 guiones Unicode en el estado = cierra (es el mismo estado); D2 'OK — CONFIRMED-CLOSED-NOT …' no cierra; D3 un id renombrado (U185)
    no cierra U-185; D4 verificación sin 'Fecha:' = falla; D5 'Fecha:' en el futuro = falla; D6 'junk NG-3.1 NG-3.3' no cierra causas;
    D7 control."""
    cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
    ids = ["BE-Q1", "NG-3.1 / BE-Q4"]
    def base():
        c = tempfile.mkdtemp(prefix="adv4_")
        os.makedirs(os.path.join(c, "proy_x"))
        json.dump({"fecha_iso": "2026-11-01T10:00:00+00:00"}, open(os.path.join(c, "proy_x", "SUBIDA_OK.json"), "w"))
        open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b.md"), "w").write(
            "# PM b 2026-11-01 16:00 PT\n" + cab + "| BE-Q1 | x | x | x | WEAK |\n\n| # | causa | candado | estado |\n|---|---|---|---|\n| 3.1 | x | - | NO GUARD |\n")
        return c
    def ver(c, nombre, fecha, est, filas=ids):
        open(os.path.join(c, nombre), "w").write(f"# V\n\n{fecha}\n\n" + cab + "".join(f"| {i} | x | x | x | {est} |\n" for i in filas))
    for dash in ["\u2012", "\u2015", "\u2212", "\u2E3A", "--", "\u2014"]:
        c = base()
        ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "Fecha: 2026-11-02 09:00 PT", f"OK {dash} CONFIRMED\u2010CLOSED")
        assert V.revisar_postmortem(c) == [], (dash, V.revisar_postmortem(c))                 # D1 / D7
    c = base()
    ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "Fecha: 2026-11-02 09:00 PT", "OK — CONFIRMED-CLOSED-NOT, WEAK — STILL-WEAK")
    assert V.revisar_postmortem(c), "D2"
    c = base()
    ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "Fecha: 2026-11-02 09:00 PT", "OK — CONFIRMED-CLOSED", ["BEQ1", "NG-3.1 / BE-Q4"])
    r = V.revisar_postmortem(c)
    assert r and "BE-Q1" in r[-1] and "causa 3.1" not in r[-1], r                              # D3: id renombrado no cierra
    c = base()
    ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "2026-11-02 09:00 PT", "OK — CONFIRMED-CLOSED")
    r = V.revisar_postmortem(c)
    assert any("sin el campo 'Fecha:" in x for x in r) and any("BE-Q1" in x for x in r), r   # D4: sin 'Fecha:' = falla y no cierra
    c = base()
    ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "Fecha: 2099-01-01 00:00 PT", "OK — CONFIRMED-CLOSED")
    r = V.revisar_postmortem(c)
    assert any("en el futuro" in x for x in r) and any("BE-Q1" in x for x in r), r            # D5
    c = base()
    ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md", "Fecha: 2026-11-02 09:00 PT", "OK — CONFIRMED-CLOSED", ["junk NG-3.1 NG-3.3", "BE-Q1"])
    r = V.revisar_postmortem(c)
    assert r and "causa 3.1" in r[-1] and "BE-Q1" not in r[-1], r                              # D6
    assert V.norm_txt("BE\u2011GK54\u00a0 ok\u200b") == "be-gk54 ok"


def adv4_prueba_abiertos():
    """verificación 4 (adv4_pm04, sintético): 'Comparado:' explícito; N = 0 no cierra; fecha en 'fecha_iso' o 'fecha', sin fecha o sin zona
    = abierto + falla; PRUEBA con los conteos vigente Y candidata > 0; una carpeta que no es proyecto en la lista = falla."""
    def cache_con(files, nombre="proj", c=None):
        c = c or tempfile.mkdtemp(prefix="adv4pa_")
        d = os.path.join(c, nombre)
        os.makedirs(d, exist_ok=True)
        for n, v in files.items():
            p = os.path.join(d, n)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write(json.dumps(v) if isinstance(v, dict) else v)
        return c
    csv = "Comparado: 2026-11-12 12:00 PT\n- 10 CSV / 10 PDF / 10 emparejados; 0 faltantes en cada lado.\n"
    sub = lambda t: {"fecha_iso": t}                                    # noqa: E731
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T10:00:00+00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md": csv})) == []
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T10:00:00+00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md": csv,
                                                 "SUBIDA_OK_rev2.json": {"fecha": "2026-11-12T23:00:00+00:00"}})) == ["proj"]   # Q1
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T10:00:00+00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md":
                                                 "Comparado: 2026-11-12 12:00 PT\n0 CSV / 0 PDF / 0 emparejados; 0 faltantes\n"})) == ["proj"]  # Q2
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T20:00:00+00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md":
                                                 "Bid due 2026-11-20 14:00\nComparado: 2026-11-12 09:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"})) == ["proj"]  # Q3
    e = []
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T20:00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md": csv}), e) == ["proj"] and e  # Q4
    e = []
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK.json": {"x": 1}}), e) == ["proj"] and "sin fecha" in e[0], e
    assert V.proyectos_abiertos_cache(cache_con({"SUBIDA_OK_rev1.json": sub("2026-11-12T10:00:00+00:00"), "CSV_BLUEBEAM_rev1/RESULTADO.md":
                                                 "2026-11-12 12:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"})) == ["proj"]   # sin 'Comparado:'
    d = tempfile.mkdtemp(prefix="adv4pad_")
    open(os.path.join(d, "SKILL.md"), "w").write("x\n**VERSION: v81cf901**\n")
    f = V.Fuente(d)
    sha = V.sha_tools(f)
    a = tempfile.mkdtemp(prefix="adv4paa_")
    c = cache_con({"SUBIDA_OK.json": sub("2026-11-12T10:00:00+00:00")}, nombre="xf")
    json.dump({"proyectos": ["xf"]}, open(os.path.join(a, "PROYECTOS_ABIERTOS.json"), "w"))
    def pr(p):
        json.dump({"version_candidata": "v81cf901", "ok": True, "regresiones": [], "proyectos": p}, open(os.path.join(a, "PRUEBA_ABIERTOS_v81cf901.json"), "w"))
        return V.revisar_prueba_abiertos(a, f, cache=c)
    assert any("conteos" in x for x in pr({"xf": {"sha_tools": sha}}))                                         # Q5
    assert any("conteos" in x for x in pr({"xf": {"sha_tools": sha, "vigente": {"PASS": 0}, "candidata": {"PASS": 0}}}))   # Q5b
    assert pr({"xf": {"sha_tools": sha, "vigente": {"PASS": 9}, "candidata": {"PASS": 9}}}) == []
    os.makedirs(os.path.join(c, "herramientas"))
    json.dump({"proyectos": ["xf", "herramientas"]}, open(os.path.join(a, "PROYECTOS_ABIERTOS.json"), "w"))
    assert any("no son proyectos" in x for x in pr({"xf": {"sha_tools": sha, "vigente": {"PASS": 9}, "candidata": {"PASS": 9}},
                                                    "herramientas": {"sha_tools": sha, "vigente": {"PASS": 9}, "candidata": {"PASS": 9}}}))  # Q6


def adv5_v121():
    """v121 (verificación 5, adv5_pm / adv5_pm04, sintético): U-185 'Fecha:' en negritas, columna 'estado' por encabezado (columna extra
    después), sin 'Fecha:' = fecha del commit en git (sin git = falla), sin 3er argumento = ruta por defecto (corre siempre); BE-PM04 el
    CSV cierra solo la MISMA rev de la última subida, SUBIDA_OK recursivo, 'Comparado:' en la primera línea, miles con coma y formas
    'faltantes en el CSV: 3' / '3 markups sin pareja'."""
    import subprocess
    cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
    def base():
        c = tempfile.mkdtemp(prefix="adv5_")
        os.makedirs(os.path.join(c, "proy_x"))
        json.dump({"fecha_iso": "2026-11-01T10:00:00+00:00"}, open(os.path.join(c, "proy_x", "SUBIDA_OK.json"), "w"))
        open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b.md"), "w").write("# PM b 2026-11-01 16:00 PT\n" + cab + "| BE-Q1 | x | x | x | WEAK |\n")
        return c
    vn = "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md"
    c = base()
    open(os.path.join(c, vn), "w").write("# V\n\n**Fecha:** 2026-11-02 09:00 PT\n\n" + cab + "| BE-Q1 | x | x | x | **OK — CONFIRMED-CLOSED** |\n")
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)                                   # E1 / E2
    c = base()
    open(os.path.join(c, vn), "w").write("# V\n\nFecha: 2026-11-02 09:00 PT\n\n| id | error | chequeo | test | estado | notas |\n|---|---|---|---|---|---|\n"
                                        "| BE-Q1 | x | x | x | OK — CONFIRMED-CLOSED | n |\n")
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)                                   # E8 columna extra
    c = base()
    open(os.path.join(c, vn), "w").write("# V\n\n" + cab + "| BE-Q1 | x | x | x | OK — CONFIRMED-CLOSED |\n")
    r = V.revisar_postmortem(c)
    assert any("ni commit en git" in x for x in r), r                                              # sin Fecha y sin git = falla
    g = dict(os.environ, GIT_AUTHOR_DATE="2026-11-02T09:00:00-08:00", GIT_COMMITTER_DATE="2026-11-02T09:00:00-08:00",
             GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "init", "-q", c], check=True)
    subprocess.run(["git", "-C", c, "add", "-A"], check=True)
    subprocess.run(["git", "-C", c, "commit", "-q", "-m", "v"], check=True, env=g)
    assert V.revisar_postmortem(c) == [], V.revisar_postmortem(c)                                   # fecha del commit en git
    viejo = V.CACHE_DEFECTO
    V.CACHE_DEFECTO = os.path.join(c, "no_existe")
    try:
        assert V.revisar_postmortem(None), "sin 3er argumento: corre con la ruta por defecto (aquí no existe = falla)"
    finally:
        V.CACHE_DEFECTO = viejo
    assert V.CACHE_DEFECTO.endswith("cache_proyectos")
    def cache_con(files, sub_dir=""):
        c = tempfile.mkdtemp(prefix="adv5pa_")
        for n, v in files.items():
            p = os.path.join(c, "proj", n)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write(json.dumps(v) if isinstance(v, dict) else v)
        return c
    ok = lambda t: "# R\nComparado: " + t + "\n- 1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en cada lado.\n"   # noqa: E731
    s20 = {"SUBIDA_OK_rev20.json": {"fecha_iso": "2026-11-12T18:00:00+00:00"}}
    assert V.proyectos_abiertos_cache(cache_con(dict(s20, **{"CSV_BLUEBEAM_rev20/RESULTADO.md": ok("2026-11-12 12:00 PT")}))) == []   # R0
    s19 = dict(s20, **{"SUBIDA_OK_rev19.json": {"fecha_iso": "2026-11-11T18:00:00+00:00"}})
    assert V.proyectos_abiertos_cache(cache_con(dict(s19, **{"CSV_BLUEBEAM_rev19/RESULTADO.md": ok("2026-11-12 12:00 PT")}))) == ["proj"]   # R1
    c = cache_con({"REV3_FINAL/SUBIDA_OK.json": {"fecha_iso": "2026-11-12T18:00:00+00:00"}})
    assert V.proyectos_abiertos_cache(c) == ["proj"] and V._es_proyecto(os.path.join(c, "proj"))                    # R2 recursivo
    c = cache_con({"REV3_FINAL/SUBIDA_OK.json": {"fecha_iso": "2026-11-12T18:00:00+00:00"}, "CSV_BLUEBEAM_rev3/RESULTADO.md": ok("2026-11-12 12:00 PT")})
    assert V.proyectos_abiertos_cache(c) == [], V.proyectos_abiertos_cache(c)                      # rev de la carpeta = rev del CSV
    for malo in ("Comparado: 2026-11-12 12:00 PT\n1,351 CSV / 1,351 PDF / 1,350 emparejados; 0 faltantes\n",
                 "Comparado: 2026-11-12 12:00 PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en el PDF; faltantes en el CSV: 3\n",
                 "Comparado: 2026-11-12 12:00 PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en el PDF; 3 markups sin pareja en el CSV\n"):
        assert V.proyectos_abiertos_cache(cache_con(dict(s20, **{"CSV_BLUEBEAM_rev20/RESULTADO.md": malo}))) == ["proj"], malo   # R3 / R5
    assert V.proyectos_abiertos_cache(cache_con(dict(s20, **{"CSV_BLUEBEAM_rev20/RESULTADO.md":
                                                             "Comparado: 2026-11-12 12:00 PT\n1,351 CSV / 1,351 PDF / 1,351 emparejados; 0 faltantes\n"}))) == []

def fechas_be_xf17():
    """BE-XF17: FECHAS_PUBLICACION a más de 60 s del commit 'Publica vX' = falta; dentro de 60 s = ok; versión sin commit = falta salvo la
    candidata (se publica con este commit)."""
    import subprocess
    d = tempfile.mkdtemp(prefix="xf17_")
    run = lambda *a, **k: subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True, check=True, **k)
    run("init", "-q")
    run("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "Publica v81cf901 (VIGENTE): prueba",
        env=dict(os.environ, GIT_COMMITTER_DATE="2026-01-01T10:00:00+00:00", GIT_AUTHOR_DATE="2026-01-01T10:00:00+00:00"))
    sk = os.path.join(d, "sk")
    os.makedirs(os.path.join(sk, "tools"))

    def poner(fechas, ver="v81cf902"):
        open(os.path.join(sk, "SKILL.md"), "w").write(f"**VERSION: {ver}**\n")
        open(os.path.join(sk, "tools", "compuerta_entrega.py"), "w").write(
            'FECHA_X = "2026-01-01T10:00:30+00:00"\nFECHAS_PUBLICACION = {' + ", ".join(f'"{k}": {v}' for k, v in fechas.items()) + "}\n")
    poner({"v81cf901": "FECHA_X"})
    assert V.revisar_fechas(V.Fuente(sk), d) == []                                  # 30 s: ok (constante resuelta)
    poner({"v81cf901": '"2026-01-01T10:02:05+00:00"'})
    assert V.revisar_fechas(V.Fuente(sk), d) and "125 s" in V.revisar_fechas(V.Fuente(sk), d)[0]   # fijada antes / lejos = falta
    poner({"v81cf901": '"2026-01-01T10:00:00+00:00"', "v81cf903": '"2026-01-01T11:00:00+00:00"'})
    assert any("v81cf903" in x for x in V.revisar_fechas(V.Fuente(sk), d))         # versión sin commit = falta
    poner({"v81cf901": '"2026-01-01T10:00:00+00:00"', "v81cf902": '"2026-01-01T11:00:00+00:00"'})
    assert V.revisar_fechas(V.Fuente(sk), d) == []                                  # la candidata todavía no tiene commit


def version_skill_be_xf19():
    """BE-XF19: verificar_version corre compuerta_entrega.version_fallas DEL CANDIDATO sobre su SKILL.md; el texto de v81cf138b ('VERSION: v81cf138b'
    + 'Chequeo CB_DUCHA_CBU en v81cf140') = falta (bloquea); el de v81cf138c ('la próxima versión del skill (la 140)') = 0; sin poder correrla = falta."""
    import tempfile
    mod = ("import re\nRX_VER = re.compile(r'\\bv(\\d+)cf(\\d+)([a-z]?)\\b')\n"
           "def _k(v):\n    m = RX_VER.search(str(v or ''))\n    return (int(m.group(1)), int(m.group(2)), m.group(3)) if m else (0, 0, '')\n"
           "def version_fallas(t, version, docs, rev_actual=None):\n    vs = [x.group(0) for x in RX_VER.finditer(t or '')]\n"
           "    return [f'SKILL.md: la línea VERSION dice {version} y el mismo SKILL.md cita {max(vs, key=_k)}: subir la línea VERSION'] "
           "if version and vs and _k(max(vs, key=_k)) > _k(version) else []\n")

    def cand(txt, con_mod=True):
        d = tempfile.mkdtemp(prefix="vv_xf19_")
        sk = os.path.join(d, "take-off-metal-frame-drywall")
        os.makedirs(os.path.join(sk, "tools"))
        open(os.path.join(sk, "SKILL.md"), "w").write(txt)
        open(os.path.join(sk, "tools", "compuerta_entrega.py"), "w").write(mod if con_mod else "raise ImportError('x')\n")
        return d
    malo = "**VERSION: v81cf138b**\n- BE-CR45: Chequeo CB_DUCHA_CBU en v81cf140.\n"
    bueno = "**VERSION: v81cf138c**\n- BE-CR45: Chequeo CB_DUCHA_CBU en la próxima versión del skill (la 140).\n"
    ev = V.revisar_version_skill(cand(malo))
    assert ev and "v81cf140" in ev[0] and "BE-XF19" in ev[0], ev
    assert V.revisar_version_skill(cand(bueno)) == []
    assert V.revisar_version_skill(cand(bueno, con_mod=False))                  # no se puede correr = falta
    print("version_skill_be_xf19 OK")


def pendientes_u202():
    """U-202: programa-pendiente > 4 h = falta; sin 'pendiente_desde' = falta; 3 h = 0; 'programa' / 'conducta' no cuentan."""
    import datetime as _dt
    import tempfile
    d = tempfile.mkdtemp(prefix="u202_")
    open(os.path.join(d, "SKILL.md"), "w").write("x")
    ahora = _dt.datetime(2026, 11, 13, 22, 30, tzinfo=_dt.timezone.utc)
    def corre(reglas):
        json.dump({"reglas": reglas}, open(os.path.join(d, "REGLAS_REGISTRO.json"), "w"))
        return V.revisar_pendientes_u202(V.Fuente(d), ahora)
    assert corre([{"id": "BE-XF18", "categoria": "programa-pendiente", "motivo": "m", "pendiente_desde": "2026-11-13T12:33:00+00:00"}])
    assert corre([{"id": "U-202", "categoria": "programa-pendiente", "motivo": "m", "pendiente_desde": "2026-11-13T22:01:18+00:00"}]) == []
    assert corre([{"id": "U-9", "categoria": "programa-pendiente", "motivo": "m"}]), "sin pendiente_desde = falta"
    assert corre([{"id": "U-9", "categoria": "programa-pendiente", "motivo": "m", "pendiente_desde": "2026-11-13 12:00"}]), "sin zona = falta"
    assert corre([{"id": "U-8", "categoria": "conducta"}, {"id": "BE-1", "categoria": "programa"}]) == []
    print("pendientes_u202 OK")


def bandeja_be_coord03():
    """BE-COORD03: (1) el hook registrar_orden publica la línea en la rama de la bandeja desde OTRA rama (repo bare local) y no guarda avisos
    automáticos; (2) verificar_version falla si la última orden registrada (posterior al corte) es > 24 h más nueva que el último mensaje real
    del usuario en la bandeja; con un mensaje reciente = 0."""
    import subprocess as sp
    import tempfile
    d = tempfile.mkdtemp(prefix="coord03_")
    run = lambda *a, cwd=d, inp=None, env=None: sp.run(list(a), cwd=cwd, input=inp, capture_output=True, text=True, env=env)   # noqa: E731
    run("git", "init", "-q", "--bare", "bare")
    w = os.path.join(d, "work")
    run("git", "clone", "-q", os.path.join(d, "bare"), w)
    g = lambda *a: run("git", "-c", "user.name=t", "-c", "user.email=t@t", *a, cwd=w)   # noqa: E731
    g("checkout", "-q", "-b", "claude/gifted-pasteur-x2sfzs")
    os.makedirs(os.path.join(w, "cache_proyectos", "ORDENES_CRUDAS"))
    os.makedirs(os.path.join(w, ".claude", "skills", "jc-hunter-ordenes"))
    os.makedirs(os.path.join(w, ".claude", "hooks"))
    hook = os.path.join(os.path.dirname(os.path.dirname(V.AQUI)), "hooks", "registrar_orden.py")
    import shutil
    shutil.copy(hook, os.path.join(w, ".claude", "hooks", "registrar_orden.py"))
    open(os.path.join(w, "cache_proyectos", "ORDENES_CRUDAS", "_entrantes.jsonl"), "w").write(
        json.dumps({"id": "a1", "ts_utc": "2026-11-11T21:39:00+00:00", "session": "c", "texto": "orden vieja"}) + "\n" +
        json.dumps({"id": "a2", "ts_utc": "2026-11-13T00:55:21+00:00", "session": "c", "texto": "This session's worker process was restarted."}) + "\n")
    open(os.path.join(w, ".claude", "skills", "jc-hunter-ordenes", "ORDENES_DEL_USUARIO.md"), "w").write("- [U-1] x\n")
    g("add", "-A")
    env = dict(os.environ, GIT_COMMITTER_DATE="2026-11-15T10:00:00+00:00", GIT_AUTHOR_DATE="2026-11-15T10:00:00+00:00")
    run("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "U-205", cwd=w, env=env)
    g("push", "-q", "origin", "claude/gifted-pasteur-x2sfzs")
    f = V.revisar_bandeja_u136(w)
    assert f and "BE-COORD03" in f[0], f                 # el error original: el aviso de reinicio no cuenta, el último real es del 11-nov
    g("checkout", "-q", "-b", "rama-coordinacion")       # (1) el hook publica desde OTRA rama
    envh = dict(os.environ, U136_ORIGIN=os.path.join(d, "bare"), U136_CACHE=os.path.join(d, "cache"), U136_PENDIENTES=os.path.join(d, "pend"),
                CLAUDE_PROJECT_DIR=w)
    r = run(sys.executable, "-I", hook, inp=json.dumps({"prompt": "orden nueva del usuario", "session_id": "s"}), env=envh)
    assert "publicado en la bandeja" in r.stdout, r.stdout + r.stderr
    run(sys.executable, "-I", hook, inp=json.dumps({"prompt": "<cross-session-message from='x'>hola", "session_id": "s"}), env=envh)
    remoto = run("git", "show", "claude/gifted-pasteur-x2sfzs:cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl", cwd=os.path.join(d, "bare")).stdout
    assert "orden nueva del usuario" in remoto and "cross-session" not in remoto, remoto
    g("checkout", "-q", "claude/gifted-pasteur-x2sfzs")
    g("pull", "-q", "origin", "claude/gifted-pasteur-x2sfzs")
    lineas = [json.loads(x) for x in open(os.path.join(w, "cache_proyectos", "ORDENES_CRUDAS", "_entrantes.jsonl")) if x.strip()]
    lineas[-1]["ts_utc"] = "2026-11-15T09:00:00+00:00"   # el mensaje que originó la orden U-205
    open(os.path.join(w, "cache_proyectos", "ORDENES_CRUDAS", "_entrantes.jsonl"), "w").write("".join(json.dumps(x) + "\n" for x in lineas))
    assert V.revisar_bandeja_u136(w) == [], V.revisar_bandeja_u136(w)
    print("bandeja_be_coord03 OK")


def correr():
    for f in (revisar_registro, revisar_zip, revisar_indice, revisar_skill, revisar_banco, revisar_ordenes, hook_solo_usuario, versiones_unicas, indice_encabezado, zip_200_bexf08, postmortem_u185, tests_llamados, prueba_abiertos_be_pm04, adv4_postmortem, adv4_prueba_abiertos, adv5_v121, fechas_be_xf17, version_skill_be_xf19, pendientes_u202, bandeja_be_coord03):
        f()
        print("ok", f.__name__)
    print("test_verificar_version OK")


if __name__ == "__main__":
    correr()
