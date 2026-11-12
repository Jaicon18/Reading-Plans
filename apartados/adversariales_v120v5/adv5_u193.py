import sys,os,tempfile,json,subprocess; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE, bitacora as BT
T=os.environ.get("ADVTMP")
def bit(rows):
    w=tempfile.mkdtemp(dir=T); BT.BIT=os.path.join(w,"bitacora.jsonl")
    for r in rows:
        if r[0]=="sub": BT.subagente(r[1],r[2])
        else: BT.anotar({"tool":r[1],"args":[],"rc":0,"hashes":{},"log":"x", **({"agente":r[2]} if r[2] is not None else {})})
    return w
def judge(w, rv):   # same logic as ce_cobertura lines 6650-6664
    rev,aut,can,sin=CE.subagentes_bitacora(w); r=CE.norm_txt(rv)
    return bool(can) and not sin and r in rev and r not in aut
C={
 "V0 control distinct": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente R9")],"subagente R9"),
 "V1 author 'subagente A1', reviewer 'subagente_A1' (underscore)": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente_A1")],"subagente_A1"),
 "V2 author 'subagente A1', reviewer 'subagente-A1' (hyphen)": ([("run","canon.py","subagente A1"),("sub","revisor_cobertura","subagente-A1")],"subagente-A1"),
 "V3 author SUBAGENTE_ID 'A1', reviewer 'subagente A1' (prefix)": ([("run","canon.py","A1"),("sub","revisor_cobertura","subagente A1")],"subagente A1"),
 "V4 author 'lectura-A', reviewer 'lectura A'": ([("run","canon.py","lectura-A"),("sub","revisor_cobertura","lectura A")],"lectura A"),
 "V5 role typo 'revisor-cobertura'": ([("run","canon.py","A1"),("sub","revisor-cobertura","R9")],"R9"),
 "V6 author's markups run only via plain python (no bitácora row) and same agent reviews": ([("run","canon.py","A1"),("sub","revisor_cobertura","M7")],"M7"),
}
for k,(rows,rv) in C.items(): print(k,"-> reviewer accepted?",judge(bit(rows),rv))
