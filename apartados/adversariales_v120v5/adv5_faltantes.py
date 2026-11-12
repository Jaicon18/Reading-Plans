import sys; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB, test_chequeos_biblioteca as T
fn=CB.faltantes_auditoria; B=T.B
# canon: corridor 216 has NO ceiling loaded; a soffit SOF-Z9-216 and wall X9-216-01 / EXT-Z9-2 are loaded (other elements)
can={"walls":[{"id":"X9-216-01"}],"ceilings":[{"room":"Z9 Lobby 101","area_sf":80.0}],
     "misc_items":[{"ref":"SOF-Z9-216 board","qty":40.0},{"ref":"EXT-Z9-2 board","qty":30.0}],
     "rcp_tags":[{"sheet":"X9.01","tag":"GYP-9","height":"8'-11\"","rows":[]}]}
A="Auditoria/AUDITORIA_U181_rev9.md"
def run(ln, extra=None): return fn(B(canon=can, textos=dict({A:"| 1 | "+ln+" |"}, **(extra or {}))))
print("J0 control 'corridor 216 ceiling missing' -> PASS (true missing, counted):", run("corridor 216 ceiling missing"))
# J1: finding mentions a DIFFERENT loaded element as context (soffit loaded, ceiling missing)
print("J1 'Corridor 216: soffit SOF-Z9-216 loaded but GYP-9 8\\'-11\" ceiling missing' (loaded ref is context) ->", run("Corridor 216: soffit SOF-Z9-216 loaded but X9.01 GYP-9 8'-11\" ceiling missing | OPEN"))
print("J1b 'corridor 216 ceiling missing along wall X9-216-01' ->", run("corridor 216 ceiling missing along wall X9-216-01 | OPEN"))
# J2: realistic phrasing with a detail reference 'not in canon' / 'not included'
print("J2 'Corridor 216 GYP-9 8\\'-11\" missing per 7/X9.23 (not in canon)' ->", run("Corridor 216 GYP-9 8'-11\" missing per 7/X9.23 (not in canon) | OPEN"))
print("J2b 'Room 216 ceiling band 7/X9.23 not included in take-off' ->", run("Room 216 ceiling band 7/X9.23 not included in take-off | OPEN"))
# J3: DOBLE_CIELO.csv row that itself records the lower ceiling as MISSING
dc=("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
    "Z9 216 Corridor,Z9,double,RS-9,GYP-9,8'-11\",7/X9.23,x,upper: RS-9 [0]; lower: GYP-9 MISSING (H-04)\n")
print("J3 DOBLE_CIELO row 'lower: GYP-9 MISSING' resolves finding 'lower ceiling missing in room 216'? ->", run("lower ceiling missing in room 216 (H-04) | OPEN", {"Auditoria/DOBLE_CIELO.csv": dc}))
dc2=dc.replace("lower: GYP-9 MISSING (H-04)","lower: CLG-Z9-216 (row does not exist)")
print("J3b DOBLE_CIELO lower ref that does not exist in canon ->", run("lower ceiling missing in room 216 | OPEN", {"Auditoria/DOBLE_CIELO.csv": dc2}))
print("---- BE-CR40 direction: ceiling IS loaded, finding declares it missing (must FAIL)")
can2={"walls":[{"id":"X9-901-01"}],"ceilings":[{"room":"Z9 Corridor 901","area_sf":50.0}],
      "rcp_tags":[{"sheet":"X9.01","tag":"GYP-9","height":"8'-11\"","rows":["ceilings[0]"]}]}
def run2(ln, extra=None): return fn(B(canon=can2, textos=dict({A:"| 1 | "+ln+" | OPEN |"}, **(extra or {}))))
print("L0 control 'X9.01 GYP-9 8\\'-11\" missing in corridor 901' ->", run2("X9.01 GYP-9 8'-11\" missing in corridor 901")[0])
print("L1 same + context wall 'along wall X9-901-01' ->", run2("X9.01 GYP-9 8'-11\" missing in corridor 901 along wall X9-901-01")[0])
print("L2 same + 'per 7/X9.23 (not in canon)' ->", run2("X9.01 GYP-9 8'-11\" missing in corridor 901 per 7/X9.23 (not in canon)"))
print("L2b 'corridor 901 ceiling 7/X9.23 not included in take-off' ->", run2("corridor 901 ceiling per 7/X9.23 not included in take-off"))
dc=("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
    "Z9 901 Corridor,Z9,double,RS-9,GYP-9,8'-11\",7/X9.23,x,upper: RS-9 (none); lower: GYP-9 ceilings[0]\n")
print("L3 room 901 in DOBLE_CIELO, finding 'corridor 901 lower ceiling missing' ->", run2("corridor 901 lower ceiling missing", {"Auditoria/DOBLE_CIELO.csv": dc}))
