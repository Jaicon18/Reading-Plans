# adv7_u193: U-193 contra v81cf138 (misma lógica de ce_cobertura que adv6_u193, con los renglones de v138). Sintético en /tmp/verif7/tmp.
import sys, os, tempfile, time; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE, bitacora as BT
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
def bit(rows):
    w = tempfile.mkdtemp(dir=T); BT.BIT = os.path.join(w, "bitacora.jsonl")
    for r in rows:
        if r[0] == "sub": BT.subagente(r[1], r[2])
        else:
            reg = {"tool": r[1], "args": r[3] if len(r) > 3 else [], "rc": r[4] if len(r) > 4 else 0, "hashes": r[6] if len(r) > 6 else {},
                   "log": "x", "ts": r[5] if len(r) > 5 else "2026-11-13T10:00:00"}
            if r[2] is not None: reg["agente"] = r[2]
            BT.anotar(reg); time.sleep(1.05)
    return w
def judge(w, rv0):      # parte U-193 de ce_cobertura en v138 (sin_agente_reemplazadas con corridas_sin_agente_filas)
    rev_ok, autores, canon_ids, sin = CE.subagentes_bitacora(w)
    ev, amber = [], []
    if not canon_ids: ev.append("sin autores del canon")
    viejas, nuevas = CE.corridas_sin_agente_por_fecha(sin)
    reemp, nuevas = CE.sin_agente_reemplazadas(nuevas, CE.corridas_con_agente(w), CE.corridas_sin_agente_filas(w))
    if reemp: amber.append("AMBER reemplazadas " + ", ".join(reemp))
    if nuevas: ev.append("sin agente " + ", ".join(nuevas))
    if viejas: amber.append("AMBER viejas " + ", ".join(viejas))
    rv = CE.norm_agente(rv0)
    if rv and (rv not in rev_ok or rv in autores): ev.append(f"reviewer {rv0} rechazado")
    return ("FAIL" if ev else "AMBER" if amber else "PASS"), [x[:70] for x in ev + amber]
base = lambda a: [("run", "canon.py", a, [], 0, "2026-11-13T09:00:00")]
for rv in ("A1 revisor", "A1-reviewer", "A1_rev", "A01", "A1 bis", "a.1", "A1 (revisor)", "agente A1 revisor"):
    print("Y1 autor 'A1' / revisor", repr(rv), "->", judge(bit(base("A1") + [("sub", "revisor_cobertura", rv)]), rv))
H = {"/w/canon.json": "aaa"}
print("Y2 control: R9 corre markups sin agente; A1 lo rehace con mismos args/hashes rc 0 ->",
      judge(bit(base("A1") + [("run", "markups_bluebeam.py", None, ["/w/canon.json"], 0, "2026-11-13T09:30:00", H),
                              ("run", "markups_bluebeam.py", "A1", ["/w/canon.json"], 0, "2026-11-13T09:31:00", H),
                              ("sub", "revisor_cobertura", "R9")]), "R9"))
print("Y3 A1 rehace con mismos args pero hashes distintos ->",
      judge(bit(base("A1") + [("run", "markups_bluebeam.py", None, ["/w/canon.json"], 0, "2026-11-13T09:30:00", H),
                              ("run", "markups_bluebeam.py", "A1", ["/w/canon.json"], 0, "2026-11-13T09:31:00", {"/w/canon.json": "bbb"}),
                              ("sub", "revisor_cobertura", "R9")]), "R9"))
print("Y4 args con espacios / './' (mismo archivo) ->",
      judge(bit(base("A1") + [("run", "markups_bluebeam.py", None, ["./entrega"], 0, "2026-11-13T09:30:00"),
                              ("run", "markups_bluebeam.py", "A1", ["entrega", "--dry-run"], 0, "2026-11-13T09:31:00"),
                              ("sub", "revisor_cobertura", "R9")]), "R9"))
