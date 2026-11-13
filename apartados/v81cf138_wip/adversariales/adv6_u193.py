import sys, os, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE, bitacora as BT, time
T = "/tmp/v138wip/tmp"; os.makedirs(T, exist_ok=True)
def bit(rows):
    w = tempfile.mkdtemp(dir=T); BT.BIT = os.path.join(w, "bitacora.jsonl")
    for r in rows:
        if r[0] == "sub": BT.subagente(r[1], r[2])
        else:
            reg = {"tool": r[1], "args": r[3] if len(r) > 3 else [], "rc": r[4] if len(r) > 4 else 0, "hashes": {}, "log": "x",
                   "ts": r[5] if len(r) > 5 else "2026-11-13T10:00:00"}
            if r[2] is not None: reg["agente"] = r[2]
            BT.anotar(reg); time.sleep(1.1)
    return w
def judge(w, rv0):      # the U-193 part of ce_cobertura (lines 8163-8189), with one disposition row reviewed by rv0
    rev_ok, autores, canon_ids, sin = CE.subagentes_bitacora(w)
    ev, amber = [], []
    if not canon_ids: ev.append("sin autores del canon")
    viejas, nuevas = CE.corridas_sin_agente_por_fecha(sin)
    reemp, nuevas = CE.sin_agente_reemplazadas(nuevas, CE.corridas_con_agente(w))
    if reemp: amber.append("AMBER reemplazadas " + ", ".join(reemp))
    if nuevas: ev.append("sin agente " + ", ".join(nuevas))
    if viejas: amber.append("AMBER viejas " + ", ".join(viejas))
    rv = CE.norm_agente(rv0)
    if rv and (rv not in rev_ok or rv in autores): ev.append(f"reviewer {rv0} rechazado")
    return ("FAIL" if ev else "AMBER" if amber else "PASS"), ev + amber
C = {
 "V0 control distinct": ([("run", "canon.py", "subagente A1"), ("sub", "revisor_cobertura", "subagente R9")], "subagente R9"),
 "V1 'subagente A1' vs 'subagente_A1'": ([("run", "canon.py", "subagente A1"), ("sub", "revisor_cobertura", "subagente_A1")], "subagente_A1"),
 "V2 'subagente A1' vs 'subagente-A1'": ([("run", "canon.py", "subagente A1"), ("sub", "revisor_cobertura", "subagente-A1")], "subagente-A1"),
 "V3 SUBAGENTE_ID 'A1' vs 'subagente A1'": ([("run", "canon.py", "A1"), ("sub", "revisor_cobertura", "subagente A1")], "subagente A1"),
 "V4 'lectura-A' vs 'lectura A'": ([("run", "canon.py", "lectura-A"), ("sub", "revisor_cobertura", "lectura A")], "lectura A"),
 "V4b 'Subagent_A1' vs 'AGENT a1'": ([("run", "canon.py", "Subagent_A1"), ("sub", "revisor_cobertura", "AGENT a1")], "AGENT a1"),
 "V4c 'sub-agente A1' vs 'A1'": ([("run", "canon.py", "sub-agente A1"), ("sub", "revisor_cobertura", "A1")], "A1"),
 "V4d 'subagente #1' vs 'subagente 1'": ([("run", "canon.py", "subagente #1"), ("sub", "revisor_cobertura", "subagente 1")], "subagente 1"),
 "V4e 'revisor A1' (role word as prefix) vs 'A1'": ([("run", "canon.py", "A1"), ("sub", "revisor_cobertura", "revisor A1")], "revisor A1"),
 "V4f 'A1 (canon)' vs 'A1'": ([("run", "canon.py", "A1 (canon)"), ("sub", "revisor_cobertura", "A1")], "A1"),
 "V4g 'Ａ１' fullwidth vs 'A1'": ([("run", "canon.py", "Ａ１"), ("sub", "revisor_cobertura", "A1")], "A1"),
 # R9 (the reviewer) writes markups (stage 2-7) WITHOUT SUBAGENTE_ID after v119, later a trivial '--help' run of the same tool by A1
 "V7 reviewer's unattributed markups run 'replaced' by a trivial later run of the same tool (rc 2, --help)": (
     [("run", "canon.py", "A1", [], 0, "2026-11-13T09:00:00"), ("run", "markups_bluebeam.py", None, ["entrega"], 0, "2026-11-13T09:30:00"),
      ("run", "markups_bluebeam.py", "A1", ["--help"], 2, "2026-11-13T09:31:00"), ("sub", "revisor_cobertura", "R9")], "R9"),
 "V7-0 control same without the trivial run": (
     [("run", "canon.py", "A1", [], 0, "2026-11-13T09:00:00"), ("run", "markups_bluebeam.py", None, ["entrega"], 0, "2026-11-13T09:30:00"),
      ("sub", "revisor_cobertura", "R9")], "R9"),
}
for k, (rows, rv) in C.items():
    print(k, "->", judge(bit(rows), rv))
