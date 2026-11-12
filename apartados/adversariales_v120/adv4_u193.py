import sys,os,tempfile,json; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE, bitacora as BT
T=os.environ.get("ADVTMP")
def bit(rows):
    w=tempfile.mkdtemp(dir=T); BT.BIT=os.path.join(w,"bitacora.jsonl")
    for r in rows:
        if r[0]=="sub": BT.subagente(r[1],r[2])
        else: BT.anotar({"tool":r[1],"args":[],"rc":0,"hashes":{},"log":"x", **({"agente":r[2]} if r[2] is not None else {})})
    return w
def judge(w, rv):
    rev,aut,can,sin=CE.subagentes_bitacora(w); r=rv.strip().lower()
    ok = bool(can) and not sin and r in rev and r not in aut
    return ok, dict(rev=rev,aut=aut,can=can,sin=sin)
cases={
 "U0 control distinct reviewer": ([("run","canon.py","subagente A1"),("run","plantilla_excel.py","subagente A1"),("sub","revisor_cobertura","subagente R9")],"subagente R9"),
 "U6 re-run canon w/o agent + fake canon sub": ([("sub","canon","FAKE"),("run","canon.py",None),("sub","revisor_cobertura","subagente A1")],"subagente A1"),
 "U7 case-only diff": ([("run","canon.py","author-1"),("sub","revisor_cobertura","AUTHOR-1")],"AUTHOR-1"),
 "U8 internal double space": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente  A1")],"subagente  A1"),
 "U9 NBSP inside id": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente A1")],"subagente A1"),
 "U10 zero-width space": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente A1​")],"subagente A1​"),
 "U11 tab inside": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente\tA1")],"subagente\tA1"),
 "U12 author agent with trailing NBSP only": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente A1 ")],"subagente A1 "),
 "U13 author runs canon via path 'tools/canon.py'": ([("run","tools/canon.py","subagente A1"),("run","canon.py","subagente Z"),("sub","revisor_cobertura","subagente A1")],"subagente A1"),
}
for k,(rows,rv) in cases.items():
    ok,d=judge(bit(rows),rv); print(k,"-> reviewer accepted (PASS)?",ok, {x:sorted(v) if isinstance(v,set) else v for x,v in d.items()})
