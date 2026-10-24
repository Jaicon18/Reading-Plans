"""Cierra los 24 renglones ALC-xx del registro y escribe etapas/alcances_estado.json (corrida B&N)."""
import json, subprocess, sys, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = sys.argv[1]
V, R = "verificado", "pendiente_rfi"
A = [
 ("ALC-01", V, "QUANTIFIED", "Partition types 1A,1,1B,1C,2,5,3,4,H1,H2a,H2b,H3a,H3b,E2,E1,F,I,A,B,D,C per schedule A-410 (1A/A-410..5/A-410) and A-221 Cafe types; plan A-101, A-221; 3-5/8\", 6\", 8\" stud families in Material Summary"),
 ("ALC-02", V, "QUANTIFIED", "Exterior wall lining types 1, 1A, 1B, 1C (1/A-410, 1A/A-410, 1B/A-410, 1C/A-410) on A-101 quantified as framing; existing building shell, no new exterior CFMF structure; E-301 (p44) note is electrical conduit only"),
 ("ALC-03", V, "NO APLICA", "NO APLICA: no parapet framing in scope - partition schedule A-410 and sections A-400A, A-400B show no parapet type; M-301 (p50) mention is a mechanical roof-edge note"),
 ("ALC-04", V, "QUANTIFIED", "Bottom track and top / deflection track = partition LF per type (A-101, A-221; 2/A-410, 3/A-410); M-302 (p51) mention is plumbing expansion fittings"),
 ("ALC-05", R, "RFI", "RFI-09 door headers: no header schedule in the set and 1/A-500 shows no header; jambs carried as studs; sill track not called (A-500 door schedule)"),
 ("ALC-06", V, "QUANTIFIED", "Bracing C.R. channel @ 4'-0\" O.C. per A-410 partition note 4 and 2/A-410, 3/A-410, 4/A-410; diagonal bracing type 2 > 22' per note 3/A-410 (RFI-04)"),
 ("ALC-07", V, "QUANTIFIED", "5/8\" gyp bd per type and face (A-410 schedule, A-101, A-221); types 1/1A/1B/1C gyp bd EXCLUDED - by future tenant (RFI-01)"),
 ("ALC-08", R, "RFI", "RFI-11 W.R. gyp bd in wet rooms (A-410 partition note 7, 2/A-410) - extent not defined; not carried"),
 ("ALC-09", V, "NO APLICA", "NO APLICA: no exterior gyp / glass mat sheathing in partition types A-410; M-301 (p50) 'plastic sheathing' is temporary protection, not wall sheathing"),
 ("ALC-10", V, "QUANTIFIED", "FRT plywood 5/8\" substrate types I, 3, 4 (I/A-221, 3/A-410, 4/A-410) and 3/4\" FRT plywood boards E-103 (p37 4'x8' FRT PLYWOOD) in Material Summary"),
 ("ALC-11", V, "QUANTIFIED", "Suspended GWB ceilings and soffits per A-121 RCP (5/A-121, 4/A-121) and A-221 / 2/A-221; in 5/8\" gyp bd family"),
 ("ALC-12", V, "QUANTIFIED", "Furring channel @ 24\", carrying channel @ 48\", hanger wire 103 pcs, ceiling track per 5/A-121 on A-121; direction assumed E-W (RFI-15); M-100 (p46), M-101 (p47), M-102 (p48) hangers are MEP"),
 ("ALC-13", V, "QUANTIFIED", "Framed soffit 2/A-221, Grab & Go header 3/A-221 (RFI-20), soffit sides on A-121; E-102 (p36) bulkhead is signage (by others)"),
 ("ALC-14", V, "NO APLICA", "NO APLICA: E-102 (p36) 'MOUNT WITHIN CANOPY BULKHEAD' is an electrical sign note at the existing canopy; no canopy framing on A-101, A-121, A-210"),
 ("ALC-15", V, "QUANTIFIED", "Column wraps C25 x 9 on A-101 (stud spacing assumed 16\", RFI-17) carried under OTHER FRAMING"),
 ("ALC-16", R, "RFI", "RFI-23 backing / blocking: P-201 (p60) water heater metal stud backing and steel blocking; accessory blocking not drawn on A-sheets; not quantified"),
 ("ALC-17", V, "NO APLICA", "NO APLICA: no framed MEP opening or access panel drawn in GWB walls or ceilings (A-121 ceiling key notes, M-102, P-101A reviewed); access panels furnished by MEP trades per E-201 (p40) and M-100 (p46) notes"),
 ("ALC-18", V, "QUANTIFIED", "Metal trim (corner bead, casing / L-bead) per A-410 and A-121 details; M-100 (p46) CJ is a legend abbreviation"),
 ("ALC-19", V, "EXCLUDED", None),
 ("ALC-20", V, "QUANTIFIED", "Cement board at wet walls (A-510 tile finishes, RFI-12); FRP-1 extent RFI-13 / RFI-22 not carried"),
 ("ALC-21", V, "NO APLICA", "NO APLICA: no shaft wall / area separation wall in partition schedule A-410 or plan A-101"),
 ("ALC-22", V, "NO APLICA", "NO APLICA: all partition types are Non-Rated per A-410 titles (2/A-410, 3/A-410, 4/A-410, 5/A-410); E-201 (p40), E-202 (p42), E-301 (p44), M-100 (p46) mentions are generic penetration notes"),
 ("ALC-23", V, "NO APLICA", "NO APLICA: no ballistic, lead-lined or abuse panels in A-410 schedule or A-510 finish schedule"),
 ("ALC-24", V, "NO APLICA", "NO APLICA: no finish level specified in A-510 finish schedule / notes (paint PT-1..PT-8 only); Level 4 assumed by default for joint compound and tape - see Review Items"),
]
sys.path.insert(0, T)
import alcances
excl = alcances.EXCLUIDOS["ALC-19"][1]
est = []
for aid, st, lab, nota in A:
    nota = nota or excl
    subprocess.run([sys.executable, T + "/registro.py", "marcar", K + "/registro.json", aid, st, nota], check=True)
    est.append({"id": aid, "estado": lab, "nota": nota})
json.dump(est, open(K + "/etapas/alcances_estado.json", "w"), ensure_ascii=False, indent=1)
print("OK", len(est))
