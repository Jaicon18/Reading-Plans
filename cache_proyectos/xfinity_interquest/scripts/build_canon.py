import json, copy, math
W='/tmp/claude-0/-home-user-reading-plans/8286ed83-02db-5490-a21c-6cf4b9d790c9/scratchpad/hf'
A=json.load(open(W+'/etapas/2_lectura/takeoff_canon_A.json'))
B=json.load(open(W+'/etapas/2_lectura/takeoff_canon_B.json'))
c=copy.deepcopy(A)
IMG='etapas/3_revision/img/'
FUENTES=["A0.0","A0.2","A0.3 (raster)","A0.4 (raster)","D1.0","A1.1","A1.2","A1.3","A1.3A","A2.0","A3.0","A3.1","A4.0","A4.1","A4.2","A4.3","A5.0","A5.1","A5.2","A5.3","S1.0","S2.0","S2.1","S3.0","S4.0","S4.1","M1.0-M1.3","P1.0-P1.1","FP1.0","E1.0-E4.x","EMS-1..4 (SHX annots)",
 "stage-3 text sweep all 50 pages incl. SHX annots: KICKER, B.O. DECK, B.O. JOIST, EXISTING GYP/PARTITION/STUD, LAYER, 16'-5, T.O. STEEL, FORK, HEADER"]
# ---------- 1. door / window heads printed 2/A5.1 + 5/A5.1 ----------
for w in c['walls']:
    for o in w.get('openings') or []:
        if o['ref']=='D08':
            o['header']='steel_by_others'
            o['header_source']="existing H.M. door 08 in EXISTING MASONRY wall (A1.1 keynotes 317/318): head is the existing masonry lintel, not metal framing; type E hat channel only returns at the jamb (E/A4.1)"
            o.pop('header_rfi',None); continue
        o.pop('header_rfi',None)
        o['header']='metal'
        if o['kind']=='window':
            o['source']='A1.1 keynote 306 (4.0 W x 3.0 H one-way glass, sill 3.33 ft, head 6.33 ft)'
            o['header_type']="HEAD TRACK - 5/A5.1 TYP. INTERIOR WINDOW HEAD DETAIL 'MTL. STUD TO MATCH WALL CONSTRUCTION'"
            o['header_type_source']='5/A5.1'
            o['with_sill']=True
            o['with_sill_source']='5/A5.1 (interior window, sill @ 40" A.F.F. A1.1 keynote 306)'
        else:
            o['header_type']="HEAD TRACK - 2/A5.1 TYP. INTERIOR DOOR HEAD DETAIL 'STEELSTUD TO MATCH WALL CONSTRUCTION'"
            o['header_type_source']='2/A5.1'
        o['pieces']=1; o['pieces_source']=o['header_type_source']+' draws ONE track (web down) at the head [crop '+IMG+'R08_A5.1_int_door_head.png]'
        o['piece']='track matching wall stud ('+w['stud_size']+')'
        o['header_source']=o['header_type_source']+' (printed; closes A RFI-02 / B RFI-08)'
# ---------- 2. vestibule bulkhead walls VH ----------
for w in c['walls']:
    if w['id'].startswith('VH'):
        if w['id'] in ('VH-02','VH-03'):
            w['length_ft']=8.92
            w['length_source']="A5.2 printed 4 1/2\" + 8'-0 1/2\" + 6\" = 8'-11\" (storefront side run; bulkhead centered on storefront, 1/A5.3) [CONFIRMED, stage-3 review: printed dim governs over A vector 8.59]"
            w['length_printed_ft']=8.92; w['length_printed_source']="A5.2 8'-11\" (4 1/2\" + 8'-0 1/2\" + 6\")"
        w['height_ft']=7.67
        w['height_source']="1/A5.3 studs from top of 6\" stud box header (2/A5.3) over storefront head +-10'-0\" V.I.F. (A5.2) to line of structure; vestibule B.O. DECK @ +-18'-2\" A.F.F. (A2.0 callout at vestibule) [CONFIRMED]: 18.17 - 10.0 - 0.5 = 7.67 ft [DERIVED] [crop "+IMG+"R06_A5.3_vest_bulkhead.png]"
        w['faces'][0]['height_ft']=8.17
        w['faces'][0]['height_source']="1/A5.3 sales face from storefront head +-10'-0\" to structure +-18'-2\" (A2.0 vestibule callout): 18.17 - 10.0 = 8.17 ft [DERIVED]"
# ---------- 3. receiving enclosure walls (from B, heights / openings resolved) ----------
for w in B['walls']:
    if not w['id'].startswith('RE'): continue
    r=copy.deepcopy(w)
    for k in ('type','top_track_kind','top_track_kind_source'): r.pop(k,None)
    if r['id']=='RE-1':
        r['height_ft']=16.0
        r['height_source']="1/A4.3 'B.O. DECK VARIES - 16'-0\" @ LP' + 4/A4.3 'T.O. STEEL L.P. @16'-0\" A.F.F.'; RE-1 is the low side (S2.1 roof plan 'SLOPE 1/4\" PER FT DOWN' toward RE-1) [CONFIRMED]; stud vs box-beam bearing -> RFI-03 [crop "+IMG+"R05_A4.3_encl_section1.png]"
        r['openings']=[{"ref":"RE-OP1","kind":"door","ro_w_ft":6.0,"head_ft":10.0,"source":"S2.1 roof plan opening in west enclosure wall (vector 108.7 pt / 18.31 pt/ft (1/4\" scale, verified 19'-8\" = 360 pt) = 5.94 -> 6.0 ft DERIVED) + A4.3 head 10'-0\" A.F.F. (A4.3 'B.O. OPENING @ 14'-0\" A.F.F. (10'-0\" A.F.F. @ FORK LIFT ACCESS OPENING)': lower head loaded = more cripples, conservative, RFI-03)",
            "header":"metal","header_type":"H-2 built-up cold-formed header (2) 600S162-54 + (2) 600T150-54","header_type_source":"S2.1 TYPICAL COLD FORMED HEADER SCHEDULE + S2.1 roof plan mark H-2 at this opening","pieces":4,"pieces_source":"S2.1 header schedule H-2 MEMBERS (2) 600S162-54 + (2) 600T150-54 [crop "+IMG+"R04_S2.1_header_boxbeam_sched.png, "+IMG+"R03_S2.1_receiving_encl.png]","piece":"600S162-54 / 600T150-54","header_source":"S2.1 (printed; closes B RFI-05)","jamb_return":False,"jamb_return_source":"2/A4.3 RECEIVING ENCLOSURE JAMB DETAIL (no gypsum board at the enclosure)","substrate_none_reason":"enclosure opening: FRT exterior grade plywood at interior side is Div. 06 EXCLUDED and metal wall panels / trim by others (A4.3 3/A4.3); no gypsum substrate"}]
    else:
        r['height_ft']=16.42
        r['height_source']="1/A4.3 'B.O. DECK @ +-16'-5\" A.F.F. - HP' (high side; roof slopes 1/4\"/ft down toward RE-1, S2.1) [CONFIRMED]; standing order: sloped structure -> high point loaded (conservative) + RFI-03 [crop "+IMG+"R05_A4.3_encl_section1.png]"
    if r['id']=='RE-3':
        r['openings']=[{"ref":"RE-OP3","kind":"door","ro_w_ft":10.0,"head_ft":10.0,"source":"S2.1 roof plan opening in east enclosure wall (vector 181.8 pt / 18.31 pt/ft = 9.93 -> 10.0 ft DERIVED) + A4.3 head 10'-0\" A.F.F. loaded (A4.3, conservative, RFI-03)",
            "header":"metal","header_type":"H-1 built-up cold-formed header (3) 600S162-54 + (2) 600T150-54","header_type_source":"S2.1 TYPICAL COLD FORMED HEADER SCHEDULE + S2.1 roof plan mark H-1 at this opening","pieces":5,"pieces_source":"S2.1 header schedule H-1 MEMBERS (3) 600S162-54 + (2) 600T150-54 [crop "+IMG+"R04_S2.1_header_boxbeam_sched.png]","piece":"600S162-54 / 600T150-54","header_source":"S2.1 (printed; closes B RFI-05)","jamb_return":False,"jamb_return_source":"2/A4.3 RECEIVING ENCLOSURE JAMB DETAIL (no gypsum board at the enclosure)","substrate_none_reason":"enclosure opening: FRT exterior grade plywood at interior side is Div. 06 EXCLUDED and metal wall panels / trim by others (A4.3 3/A4.3); no gypsum substrate"}]
    r['scope_info']="Cold-formed metal framing Div. 05 40 = our scope (standing order); members printed on S2.1 / S4.1"
    r.pop('openings_info',None)
    c['walls'].append(r)
# ---------- misc_items ----------
keep={'CJ-01','CJ-02','CB-01','FRP-01','FRP-02','SHELF-B'}
misc=[m for m in A['misc_items'] if m['ref'] in keep]
for m in misc:
    if m['ref'].startswith('FRP'):
        m['source']+=" -- FRP carried per A1.3 finish schedule (G.C. scope)"
bmap={m['ref']:m for m in B['misc_items']}
for ref in ('SHELF-joists','SHELF-track','RE-BB1'):
    m=copy.deepcopy(bmap[ref]); misc.append(m)
bmap_bb=misc[-1]; bmap_bb['source']+=" [crop "+IMG+"R03_S2.1_receiving_encl.png: 4 BB-1 lines spanning RE-1 to RE-3]"
L=[13.79,8.92,8.92]
n=sum(math.ceil(x/4)+1 for x in L)
misc += [
 {"ref":"KCK-01","familia":"3-5/8\" stud (todos los gauges)","qty":round(n*6.0,1),"unit":"LF","pcs":n,
  "source":"1/A5.3 '3-5/8\" X 18 GA. STEEL STUD KICKER @ 4'-0\" O.C.' + 'KICKER ANGLE MUST BE BETWEEN 30-45 deg'; length not printed -> RFI-04 [crop "+IMG+"R06_A5.3_vest_bulkhead.png]",
  "op":f"kickers SUM(ROUNDUP(L/4)+1) for VH 13.79 / 8.92 / 8.92 = 5+4+4 = {n} x 6.0 ft (conservative: 7.67 ft stud braced at mid-height to deck at 45 deg = 3.83/sin45 = 5.4 ft -> 6.0 loaded, RFI-04) = {round(n*6.0,1)} LF"},
 {"ref":"BXH-01","familia":"header / box beam","qty":round(sum(L)*4,2),"unit":"LF","pcs":4,
  "source":"2/A5.3 '6\" X 18GA. STEEL STUD BOX HEADER' (box = 2 C + 2 track) under vestibule bulkhead 1/A5.3; runs A1.1 13'-9 1/2\" + A5.2 8'-11\" x 2",
  "op":f"(13.79 + 8.92 + 8.92) = {round(sum(L),2)} LF x 4 pcs = {round(sum(L)*4,2)} LF"},
 {"ref":"BXH-02","familia":"header / box beam","qty":round(12.042*4,2),"unit":"LF","pcs":4,
  "source":"8/A5.3 BOX HEADER DETAIL 'BRAKE METAL SECTION OVER 6\" 16 GA. METAL BOX-HEADER' + 9/A5.3 BOX HEADER ATTACHMENT DETAIL (T162-54 track clip to jamb, header spans jamb to jamb) at new bi-parting door opening +-12'-0 1/2\" W (D1.0 219, A5.2) [crop "+IMG+"R07_A5.3_box_header_attach.png]",
  "op":"12.042 ft (opening, jamb to jamb per 9/A5.3, no bearing extension) x 4 pcs = 48.17 LF (6\" 16 GA)"},
 {"ref":"BXH-02-CLIP","familia":"header / box beam","qty":2.17,"unit":"LF","pcs":4,
  "source":"9/A5.3 'T162-54 TRACK SCREWED TO HEADER ... TRACK WEB TO JAMB' (one clip each end, 2 flanges)",
  "op":"2 ends x 2 pcs x 6 1/2\" (box header depth, 8/A5.3) = 2 x 2 x 0.542 = 2.17 LF T162-54"},
 {"ref":"RE-JAMB","familia":"6\" stud (todos los gauges)","qty":round(2*16.0+2*16.42,1),"unit":"LF","pcs":4,
  "source":"S2.1 header schedule JAMB STUDS column: (1) 600S162-54 + (1) 600T150-54 per jamb; the 600S jamb stud is generated by the opening logic of the wall; this row carries the 600T150-54 closure track per jamb (S4.1 TYPICAL JAMB STUD DETAIL 'FULL HEIGHT CLOSURE TRACK FOR JAMB')",
  "op":"RE-OP1 2 jambs x 16.0 ft + RE-OP3 2 jambs x 16.42 ft = 64.8 LF 600T150-54"},
]
# ---------- demolition ----------
H2='A1.2 CLEARANCE HEIGHTS CHART SALES B.O. STRUCTURE high point +-16\'-9" A.F.F. (standing order R-ALC-07: demolished partition with no printed height -> printed B.O. structure of its bay) [DERIVED]'
H1='A1.2 CLEARANCE HEIGHTS CHART SALES REPLENISHMENT B.O. STRUCTURE high point +-15\'-9 1/2" A.F.F. (standing order R-ALC-07) [DERIVED]'
demo=[
 ("DEMO-01","west bay partition (Sales Replenishment), from 4'-0\" past lease line (211) to west wall",[[509.7,807.4],[509.7,1338.1]],78.62,15.79,H1,2,"207 + 211","A","vector D1.0 dashed double line x 507.8/511.6 runs 807.4 (lease line 834.4 - 4'-0\" x 6.75) to west wall 1338.1 = 530.7/6.75 = 78.62 [crop "+IMG+"R12_D1.0_DEMO01_end.png]"),
 ("DEMO-02","east block N-S office wall, crosses lease line (211)",[[1714.7,807.4],[1714.7,1020.7]],31.60,16.75,H2,2,"207 + 211","A/B merged","vector x 1713/1716 dashed double line 806.0-1020.7; 211 limits it to 4'-0\" past lease line (807.4): 213.3/6.75 = 31.60"),
 ("DEMO-03","east block E-W wall north of lease line inside 211 4'-0\" zone",[[1715.6,817.3],[1815.8,817.3]],14.84,16.75,H2,2,"207 + 211","A=B","vector y 816/819 1715.6-1815.8 = 14.84"),
 ("DEMO-04","east block E-W wall with door 208",[[1715.6,902.6],[1782.0,902.6]],9.84,16.75,H2,2,"207 / 208","A","vector y 897/903 dashes 1715.6-1782.0 = 9.84 (B's run to 1816 not drawn) [crop "+IMG+"R10_D1.0_east_block_RR.png]"),
 ("DEMO-05","restroom block north wall",[[1659.2,1048.6],[1816.8,1048.6]],23.35,16.75,H2,2,"207 (201 tile area)","B","vector y 1047/1050 dashes 1659.2-1816.8 = 23.35 (A stopped at 1751)"),
 ("DEMO-06","restroom block south wall",[[1619.1,1159.1],[1816.8,1159.1]],29.58,16.75,H2,2,"207","printed","D1.0 printed +-29'-7\" (block overall) = 29.58 [CONFIRMED]; vector 1619.1-1816.8 = 29.29"),
 ("DEMO-07","restroom block west wall",[[1617.3,1009.6],[1617.3,1169.2]],23.64,16.75,H2,2,"207","B","vector x 1615/1619 dashes 1009.6-1169.2 = 23.64 (A's run to 1266 is not drawn)"),
 ("DEMO-08","restroom block interior N-S wall between toilet rooms",[[1699.5,1049.6],[1699.5,1157.9]],16.04,16.75,H2,2,"207","B only","vector x 1698/1701 dashes 1049.6-1157.9 = 16.04"),
 ("DEMO-09","existing riser-room west wall (rebuilt as D-02)",[[1775.2,1049.6],[1775.2,1157.9]],16.04,16.75,H2,2,"207 / 200","A=B","vector x 1774/1777 1049.6-1157.9 = 16.04"),
 ("DEMO-10","restroom block corridor stub N-S",[[1661.0,1018.0],[1661.0,1049.6]],4.68,16.75,H2,2,"207","B only","vector x 1659 dashes 1018-1049.6 = 4.68"),
 ("DEMO-11","restroom block corridor wall E-W (east part)",[[1713.0,1019.5],[1776.6,1019.5]],9.42,16.75,H2,2,"207","B only","vector y 1018/1021 1713.0-1776.6 = 9.42"),
 ("DEMO-12","restroom block corridor wall E-W (west part)",[[1619.1,1019.5],[1662.0,1019.5]],6.36,16.75,H2,2,"207","B only","vector y 1018/1021 1619.1-1662.0 = 6.36"),
 ("DEMO-13","gyp bd furring on south masonry (adjacent-tenant side), printed +-6'-1\"",[[1845.7,793.6],[1845.7,834.9]],6.08,16.75,H2,1,"209","A=B","D1.0 printed +-6'-1\" = 6.08 [CONFIRMED]; 1 face (furring on masonry)"),
 ("DEMO-14","gyp bd furring on west masonry wall (209 leader), drawn dashed extent",[[532.6,1335.2],[1587.2,1335.2]],156.24,16.75,H2,1,"209","resolved","vector D1.0 dashed line y 1335.2 (78 dashes) x 532.6-1587.2 = 1054.6/6.75 = 156.24 [DERIVED] - drawn extent closes B RFI-03; whole run lies east of the DEMO-01 partition = Sales bay [crop "+IMG+"R09_D1.0_209_west_wall.png, "+IMG+"R11_D1.0_west_wall_209_extent.png]"),
]
geom=[]
for (i,grp,poly,lf,h,hs,lay,kn,orig,lop) in demo:
    sf=round(lf*h*lay,1)
    misc.append({"ref":i,"familia":"demolition - gypsum board and metal framing","qty":sf,"unit":"SF",
      "source":f"D1.0 keynote {kn} (+ Demo Legend dashed = existing construction to be removed); length {lop}; height {hs}",
      "op":f"{lf} LF x {h} ft x {lay} face-layer(s) = {sf} SF"})
    geom.append({"id":i,"group":grp,"page":4,"sheet":"D1.0","polyline":poly,"lf":lf,"h_ft":h,
      "h_status":"DERIVED (standing order R-ALC-07: B.O. structure of bay)","h_source":hs,"layers":lay,
      "layers_info":"2 faces x 1 layer (wall removed completely, 207); construction not shown -> RFI-02" if lay==2 else "1 face (furring over masonry, 209)",
      "sf":sf,"keynote":kn,"op":f"{lf} x {h} x {lay} = {sf}","resolution_source":orig})
c['misc_items']=misc
# misc_info: drop RECV-ENCL pending
c['misc_info']=[m for m in A['misc_info'] if m['ref']!='RECV-ENCL']
c['misc_info'].append({"ref":"TOOL-LIMIT-HAT","familia":"tool limit note","qty":0,"unit":"LF","source":"E/A4.1","op":"Type E 1-1/2\" metal hat channel @ 24\" O.C. is loaded in the Z-furring family (no hat-channel family): label must read 1-1/2\" hat channel (calc stage to fix in the tool)"})
# ---------- RFIs ----------
def rfi(i,q,A_,B_,loaded,extra=[]):
    return {"id":i,"question":q,"fuentes_revisadas":FUENTES+extra,"loaded":loaded,"options":{"A":A_,"B":B_,"C":""}}
c['rfis']=[
 rfi("RFI-01","Demising wall D-01 (+-209'-1\", A1.1) runs under a sloped deck/joists: A2.0 B.O. DECK callouts +-16'-11\" (north), +-17'-5 1/2\", +-17'-3 1/2\", +-18'-0 1/2\", +-18'-3\" (south) and A1.2 B.O. DECK / JOIST / BEAM spots. Studs/Type X board loaded at the high point 18'-3\" - 1\" slip = 18.17 ft full length. Confirm height basis per bay.",
   {"texto":"Use printed B.O. deck per bay along the lease line (A2.0 / A1.2 callouts)","source":"A2.0 / A1.2","delta":"approx -0.9 ft avg x 209 LF x 2 faces = approx -380 SF 5/8 Type X; studs approx -0.9 ft each (157 studs) = approx -140 LF 6\""},
   {"texto":"High point full length (loaded)","cita":"ASTM C754 / GA-216 framing to structure; AISI S220 deflection track","delta":"0 (loaded)"},"LOADED 18.17 ft full length (high point, conservative)",["A1.2 / A2.0 B.O. DECK callouts (both readers)"]),
 rfi("RFI-02","Existing partitions to be removed (D1.0 207 / 211) and furring (209): construction (stud size, layers) is not printed. Heights closed by standing order (B.O. structure of the bay, A1.2). Loaded 1 layer each face (207, wall removed completely) and 1 face at furring (209).",
   {"texto":"1 layer each face of partitions, 1 face at furring (loaded)","source":"D1.0 207 / 209 + Demo Legend","delta":"0 (loaded)"},
   {"texto":"2 layers per face if field shows rated partitions","cita":"field verification per D1.0 general demolition note 1 / keynote 204","delta":"+8,693 SF on 2-face partitions (DEMO-01..12)"},"LOADED 1 layer per face",["D1.0 Demo Legend, keynotes 200-253, general demolition notes 1-20"]),
 rfi("RFI-03","Receiving enclosure 600S162-54 studs: 1/A4.3 'B.O. DECK VARIES - 16'-0\" @ LP', 'B.O. DECK @ +-16'-5\" - HP', '4/A4.3 T.O. STEEL L.P. @16'-0\"'; stud top vs BB-1 box-beam bearing and opening head heights (14'-0\" vs 10'-0\" @ fork lift opening) are not assigned per opening. Loaded RE-1 16.0 ft (LP), RE-2 / RE-3 16.42 ft (HP), heads 10'-0\" both openings.",
   {"texto":"Studs to T.O. steel L.P. 16'-0\" on all three walls","source":"4/A4.3","delta":"-0.42 ft x approx 31 studs RE-2/RE-3 = approx -13 LF 600S162-54"},
   {"texto":"High point / lower heads as loaded","cita":"AISI S240 (wall studs to structure)","delta":"0 (loaded)"},"LOADED RE-1 16.0 / RE-2 16.42 / RE-3 16.42 ft; heads 10'-0\"",["1/A4.3, 3/A4.3, 4/A4.3, S2.1 roof plan, S4.1"]),
 rfi("RFI-04","Vestibule bulkhead kickers 3-5/8\" x 18 GA @ 4'-0\" O.C. (1/A5.3): kicker length not printed (only 'angle 30-45 deg'). Loaded 6'-0\" each.",
   {"texto":"Length from section geometry: brace at mid-height of 7.67 ft stud at 45 deg = 5.4 ft","source":"1/A5.3","delta":f"-0.6 ft x {n} = -{round(0.6*n,1)} LF"},
   {"texto":"6'-0\" per kicker (loaded, conservative)","cita":"AISI S240 / ASTM C754 bracing","delta":"0 (loaded)"},"LOADED 6.0 ft each",["1/A5.3, 3/A5.3, A5.2, A2.0"]),
]
c['accesorios_rfi']=A.get('accesorios_rfi')
c['accesorios_none']=[x for x in c['accesorios_none'] if x['familia']!='additional head track']
c['nodes']+= [dict(n,id='NRE'+n['id'][1:]) for n in B['nodes'] if 'RE-' in json.dumps(n)]
c['opening_schedule']['items']+= [{'ref':'RE-OP1'},{'ref':'RE-OP3'}]
c['opening_schedule']['sources'].append('S2.1')
c.setdefault('constants',{})
c['constants']['plan_scale_by_sheet']['S2.1']={'value':18.0,'source':"S2.1 ENLARGED RECEIVING ENCLOSURE plans SCALE 1/4\" = 1'-0\" = 18 pt/ft; verified printed 19'-8\" (O.F. stud) = 360 pt drawn"}
c['constants']['resolution_info']={"value":"stage-3 resolution of readings A and B","source":"etapas/3_revision/resolucion.md"}
json.dump(c,open(W+'/etapas/4_canon/takeoff_canon.json','w'),indent=1)
json.dump(geom,open(W+'/etapas/4_canon/demo_geom.json','w'),indent=1)
print('demo SF',round(sum(g['sf'] for g in geom),1),'kickers',n)
