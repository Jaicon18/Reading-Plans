import json, copy
W='/tmp/chuze/work/etapas/2_lectura/'
OUT='/tmp/chuze/work/etapas/4_canon/takeoff_canon.json'
frag={f:json.load(open(W+'A/'+f+'.json')) for f in ['Z1','Z2','Z3','Z4','Z5','Z6']}
gen=json.load(open(W+'A/general.json'))
B={w['id']:w for f in ['Z1','Z2','Z3','Z4','Z5','Z6'] for w in json.load(open(W+'B/'+f+'.json')).get('walls',[])}
walls=[]; desc=[]; blocking=[]; notes=[]
for f,d in frag.items():
    for w in d['walls']: w['_frag']=f; walls.append(w)
    desc+=d.get('tags_descartados',[])
    blocking+=d.get('blocking_items',[]) or []
    ni=d.get('notes_info')
    if isinstance(ni,list): notes+=[f'{f}: '+str(x) for x in ni]
    elif ni: notes.append(f'{f}: '+json.dumps(ni) if not isinstance(ni,str) else f'{f}: '+ni)
Wd={w['id']:w for w in walls}
RES='3_revision/resolucion.md'
def rm(i,tags_motivo,item):
    w=Wd.pop(i); walls.remove(w)
    for t in w.get('tag_ids',[]):
        desc.append({'id':t,'motivo':tags_motivo,'imagen':f'../3_revision/img_res/{item}.png'})
def setdesc(t,motivo,item):
    for x in desc:
        if x['id']==t: x['motivo']=motivo; x['imagen']=f'../3_revision/img_res/{item}.png'
def stamp(w,item,txt):
    w['notes']=(w.get('notes') or '')+f' [STAGE 3 {item}: {txt} - {RES}]'
    w['img_res']=f'../3_revision/img_res/{item}.png'

# ---- double counts (ONE WALL ONCE: tagged on two enlarged sheets -> lower sheet owns)
rm('A-A429-8','same wall as A421 (counted there as A-A421-6, C-14) - STAGE 3 R-01 double count removed','R-01')
rm('A-A429-9','same wall as A421 (counted there as A-A421-7, C-15) - STAGE 3 R-02','R-02')
rm('A-A429-10','same wall as A421 (counted there as A-A421-8, C-16) - STAGE 3 R-03','R-03')
setdesc('PT0103','same wall as A421 (A-A421-7, C-15; A429 copy removed in STAGE 3 R-02)','R-02')
rm('A-A435-4','same wall as A426 (counted there as A-A426-4, C-37) - STAGE 3 R-04','R-04')
rm('A-A424-4','same wall as A423 (counted there as A-A423-5, C-48) - STAGE 3 R-05','R-05')
rm('A-A427-4','same wall as A421 (C3C box counted there as A-A421-1, C-17) - STAGE 3 R-06','R-06')
rm('A-A427-5','same wall as A421 (C3C box counted there as A-A421-2, C-18) - STAGE 3 R-06','R-06')
for t,b in (('PT0122','A-A421-2'),('PT0123','A-A421-2'),('PT0125','A-A421-2'),('PT0124','A-A421-1')):
    setdesc(t,f'same wall as A421 (C3C box counted there as {b}; A427 copy removed in STAGE 3 R-06)','R-06')
rm('A-A425-6','','R-16')   # untagged duplicate of A-A423-6
rm('A-A425-7','','R-17'); rm('A-A425-8','','R-17')

# ---- R-04 C-37 printed length
w=Wd['A-A426-4']; w['length_ft']=12.46; w['length_status']='CONFIRMED'; w['length_source']='A435'
w['length_op']='printed 7\'-1" + 5\'-4 1/2" = 12\'-5 1/2" = 12.46 ft (A435 left string ticks y1714.3-1939.0, same wall; from N face of A3C line, A6D owns the T); A426 vector 12.53'
w['band']['lo']=round(1225.9-12.46*18,2)
w['tag_ids']=['PT0089','PT0104'] if False else ['PT0089']
stamp(w,'R-04','printed dimension 12\'-5 1/2" (A435) wins; A435 copy A-A435-4 removed')

# ---- R-07 C3C U boxes at storefront line (north face owned by A6D C-2)
for i in ('A-A421-1','A-A421-2'):
    w=Wd[i]; w['length_ft']=4.77; w['length_status']='DERIVED'
    w['length_op']='U furring at existing column under the A6D line (A427 draws A6D poche over the column, C3C U below): S face printed 3\'-0" (A421 top string) + 2 legs (1038.5-1022.6)/18 = 0.88 each = 3.00 + 0.88 + 0.88 = 4.76 ~ 4.77 ft; N face belongs to A6D A-A427-3 (one owner, R70.2)'
    w['faces_ft']=[3.0,0.88,0.88]
    w['fos_chain']={'value':[3.0,0.88,0.88],'source':'A421: 3\'-0" printed (S face); legs DERIVED vector A421 (A6D S face y1022.6 to box S face y1038.5)'}
    w['band']['lo']=1022.6
    w['faces']=[{'side':'B','room':'Reception corridor under 10\'-0" C-5 GYP soffit (south face)','board':'5/8" type X','layers':1,'height_ft':10.0,'height_source':'A421.A \'10\'-0" AFF C-5\'; board to ceiling per C/A301','length_ft':3.0,'length_source':'printed 3\'-0" A421'},
                {'side':'END','room':'Corridor (west end)','board':'5/8" type X','layers':1,'height_ft':10.0,'height_source':'A421.A 10\'-0" C-5','length_ft':0.88,'length_source':'DERIVED A421 vectors'},
                {'side':'END','room':'Corridor (east end)','board':'5/8" type X','layers':1,'height_ft':10.0,'height_source':'A421.A 10\'-0" C-5','length_ft':0.88,'length_source':'DERIVED A421 vectors'}]
    w['height_ft']=10.5; w['height_status']='PENDING'
    w['height_source']='head C (C/A301): stud stops above the ceiling of the faces it serves = 10\'-0" C-5 soffit (A421.A) + 6" extension drawn, not dimensioned [PENDING, RFI-21]; N side is the A6D wall (to deck)'
    w['element']='column_wrap'
    stamp(w,'R-07','C3C basis = faces that carry board (PT7), outer face; north face owned by A6D C-2')

# ---- R-08 C-2 A6D through interior storefronts F/H to C-15 (R70.3 / R77.10)
w=Wd['A-A427-3']; w['length_ft']=60.88; w['length_status']='CONFIRMED'; w['length_source']='A427 + A421'
w['length_op']='printed chain: A427 44\'-9" (W face of Group X W wall to storefront F jamb = E face of C3C box 1) + A421 top string 8\'-1 1/2" (storefront F incl. door 119) + 3\'-0" (box 2) + 5\'-0" (storefront H incl. door 113, to W face of A6D stub A-A421-7) = 60\'-10 1/2" = 60.875 ft; vector A101 1212.48-1625.28 = 61.16'
w['band']['hi']=round(513.6+60.88*18,1)
w['location']='Group X 119 / Recovery 113 south line (to Turf 144 / circulation), incl. interior storefronts F (door 119) and H (door 113) and the column boxes'
w['openings'].append({'ref':'H (door 113)','kind':'storefront','ro_w_ft':5.0,'head_ft':10.0,'source':'A421 printed 5\'-0" (top string); A601 glazing frame types 10\'-0" high (type H head not separately dimensioned - PENDING); door 113 AD1 3\'-0" x 7\'-0" ALF (A601)'})
w['storefront_in_lf_reason']='Interior aluminum storefront set INSIDE the A6D stud wall line (A602 8 HEAD/JAMB DETAIL @ INT. STOREFRONT: metal stud framing + 5/8" gyp bd above the frame); wall continues above the frame to deck (A421.B elev 2 LOBBY/RETAIL NORTH) - run through per R70.3 / R77.10; header/cripples from openings[]'
stamp(w,'R-08','length = printed chain 60\'-10 1/2"; storefronts F/H inside the run')
for i in ('A-A421-16','A-A422-1','A-A426-5'):
    Wd[i]['storefront_in_lf_reason']='Interior aluminum storefront / sidelight + AD1 door set INSIDE the stud wall line between two segments of the same wall (A602 8 HEAD/JAMB DETAIL @ INT. STOREFRONT: metal stud framing + 5/8" gyp bd above the frame); run through per R70.3 / R77.10 (A, B and the A101 closure agree)'

# ---- R-14 A424-5 return ends at existing wall; R-15 east lav wing
w=Wd['A-A424-5']; w['length_ft']=6.72; w['length_status']='DERIVED'
w['length_op']='gray fills A424: H 1692.5->1781.8 = 89.3 pt = 4.96 (printed 4\'-6" = gray 1700.2-1781.8) + untagged V return from inner face y1819.7 to its end at the existing wall y1851.4 = 31.7 pt = 1.76; total 4.96 + 1.76 = 6.72 ft (east lav wing L is a separate group: A-A424-14)'
w['faces']=[f for f in w['faces'] if 'niche' not in f.get('room','')]
for f in w['faces']:
    if f.get('length_ft') and f['length_ft']>3.0 and f['length_ft']<4: f['length_ft']=1.76; f['length_source']='vector y1819.7->1851.4'
stamp(w,'R-14','6.72 per gray fills (B reading); A ran the return to y1921 and absorbed the east lav wing')
n=copy.deepcopy(Wd['A-A424-13']); n['id']='A-A424-14'; n['tag_ids']=[]
n['location']="Men's Locker Room 128 - trough sink niche east side (wing wall L)"
n['length_ft']=2.65; n['length_op']='gray fills A424: V x1676.6-1682.2 y1875.4->1912.8 = 37.4 pt = 2.078 (printed 2\'-1") + H x1682.2->1692.5 = 10.3 pt = 0.572; 2.078 + 0.572 = 2.65 ft'
n['band']={'ori':'V','c0':1676.6,'c1':1682.2,'lo':1875.4,'hi':1912.8,'sheet':'A424'}
n['untagged_reason']='untagged new wall group (gray poche) at east side of trough sink niche, mirror of A-A424-13; thickness 5.6 pt = 3-5/8" stud -> A3C (type of untagged 3-5/8" interior partitions, RFI-22); ported from reading B (B-A424-14)'
n['img']='../3_revision/img_res/R-15.png'
for f in n['faces']:
    f['room']=f['room'].replace('N face of stub','S/W face of wing').replace('E face of','W face of')
stamp(n,'R-15','ONLY_B wall confirmed on plan, ported with reader-A fields')
walls.append(n); Wd[n['id']]=n

# ---- R-17 alcove end caps: tag PT0130 C3D (A423), full L drawn on A425
for i,(c0,c1,lo,hi) in (('A-A423-7',(1812.24,1819.66,1941.1,1978.3)),('A-A423-8',(1624.0,1632.0,1941.1,1978.3))):
    w=Wd[i]; w['length_ft']=2.68; w['length_status']='DERIVED'; w['length_source']='A425'
    w['sheet']='A425'; w['page']=37
    w['band']={'ori':'H','c0':c0,'c1':c1,'lo':lo,'hi':hi,'sheet':'A425'}
    w['length_op']='full end cap drawn on A425 (A423 shows only its east 0.67 ft): H x1941.1->1978.3 = 37.2 pt = 2.07 + return 11.0 pt = 0.61 (gray fills A425); 2.07 + 0.61 = 2.68 ft'
    w['band_length_ok_reason']='band = H leg 2.07 ft; length adds the 0.61 ft untagged return (E28 return joins the tagged cap)'
    stamp(w,'R-17','type C3D from printed tag PT0130 (A423, owner by tag); length from A425 where fully drawn; A425 copies typed A3C removed')

# ---- R-19 A2.25 infill type
w=Wd['A-A434-1']; w['tag']='A6D'
w['default_type_rfi']={'alternativas':['A6D (6" stud, both readings: thickness of the existing wall)','A3C (3-5/8")'],'source':'A434 / A101 keynote A2.25 (no type printed) - RFI-24'}
w['detail']="INTERIOR PARTITION TYPE 'A' A301 (A6D assumed for keynote A2.25 infill; type not printed)"; w['detail_source']='A301'
w['stud_size']='6"'
stamp(w,'R-19','typed A6D (B reading, A stud 6") instead of non-schedule tag A2.25-INFILL; RFI-24')

# ---- R-18 door 141 wall
stamp(Wd['A-A101-1'],'R-18','only reading A; confirmed new (rev 8 cloud, gray poche, door 141 A601); type not printed -> A6D, RFI-20')
Wd['A-A101-1']['default_type_rfi']={'alternativas':['A6D (poche 6", loaded)','A6C (head C)','A3C'],'source':'A101 (no tag) - RFI-20'}

# ---- R-12 D3G bank 2 (A432)
base=Wd['A-A421-3']; ret=Wd['A-A421-4']
d1=copy.deepcopy(base); d1.update(id='A-A432-1',sheet='A432',page=52,tag_ids=['PT0137'],
   location='Circulation 120 / Cardio 146 - locker bank 2 low wall (back, west face)',
   length_ft=24.82,length_status='DERIVED',length_source='A432',
   length_op='SCALE A432 3/16"=1\'-0" = 13.5 pt/ft (constants). West face x2585.5, outer extent y1330.3->1665.4 = 335.1 pt / 13.5 = 24.82 ft (owns both corners, same method as bank 1 A-A421-3)',
   band={'ori':'V','c0':2585.5,'c1':2591.0,'lo':1330.3,'hi':1665.4,'sheet':'A432'},thickness_measured_in=4.89,
   height_source='T.O. WALL 60" ABOVE FFE (A101 notes at D3G tags PT0137 / PT0138) = 5.0 ft; head G',
   img='../3_revision/img_res/R-12.png')
for f in d1['faces']: f['height_source']='T.O. WALL 60" ABOVE FFE (A101 notes at PT0137/PT0138) = 5.0 ft; head G'
d1['faces'][0]['room']='Circulation 120 (west)'; d1['faces'][1]['room']='Lockers A2.54 zone (east)'
d1['notes']='Partial height (type D tube steel support = EXCLUDED structural steel). Wall cap 7/A501 on top (RFI-17). Lockers A2.54 inside the U.'
stamp(d1,'R-12','gap filled: counted by nobody (A-Z1 / B-Z1 / B-Z5 / B-Z6 hand-offs); A432 is the only sheet that draws it fully')
d2=copy.deepcopy(ret); d2.update(id='A-A432-2',sheet='A432',page=52,tag_ids=[],location='Locker bank 2 - north end return',
   length_ft=1.69,length_op='(2613.1 - 2590.3) / 13.5 = 1.69 (from inner face of A-A432-1)',
   band={'ori':'H','c0':2590.3,'c1':2591.0+0.0,'lo':2590.3,'hi':2613.1,'sheet':'A432'},
   part_of='A-A432-1',untagged_reason='untagged return of locker bank 2 (joins the tagged back wall, E28)',img='../3_revision/img_res/R-12.png')
d2['band']={'ori':'H','c0':1330.3,'c1':1335.1,'lo':2590.3,'hi':2613.1,'sheet':'A432'}
d3=copy.deepcopy(ret); d3.update(id='A-A432-3',sheet='A432',page=52,tag_ids=['PT0138'],location='Locker bank 2 - south end return',
   length_ft=1.74,length_op='(2613.8 - 2590.3) / 13.5 = 1.74 (from inner face of A-A432-1)',
   band={'ori':'H','c0':1660.6,'c1':1665.4,'lo':2590.3,'hi':2613.8,'sheet':'A432'},img='../3_revision/img_res/R-12.png')
for d in (d2,d3):
    d['height_source']=d1['height_source']; d['band_length_ok_reason']='short return; band = vector extent'
    for f in d['faces']: f['height_source']=d1['height_source']
    stamp(d,'R-12','gap filled (bank 2 return)')
d3.pop('part_of',None); d3.pop('untagged_reason',None)
for d in (d1,d2,d3): walls.append(d); Wd[d['id']]=d
desc=[x for x in desc if x['id'] not in ('PT0137','PT0138')]

# ---- R-13 B2E C-64 (only B)
b=B['B-A423-9']; n=copy.deepcopy(Wd['A-A427-6'])
n.update(id='A-A423-10',sheet='A423',page=30,tag_ids=[],location=b['location'],demo_source=b['demo_source'],
   length_ft=4.64,length_status='DERIVED',length_source='A423',length_op=b['length_op'],band=b['band'],
   thickness_measured_in=b['thickness_measured_in'],untagged_reason=b['untagged_reason'],img='../3_revision/img_res/R-13.png')
n['faces']=[{'side':'A','room':'VIP Room 124','board':'5/8" gyp bd','layers':1,'height_ft':14.5,'height_source':'A423.A C-12 ACT 14\'-0" AFF (VIP Room 124) + E/A301 board 6" above ceiling (printed 6") = 14\'-6" [DERIVED]'},
            {'side':'B','room':'Existing exterior wall side','board':'none','layers':0,'height_ft':0,'height_source':'furring','board_none_reason':'type B furring against existing exterior construction - no board on wall side (B/A301)'}]
n['notes']='Ported from reading B (B-A423-9). B2E Z-girt / rigid insulation EXCLUDED.'
stamp(n,'R-13','ONLY_B wall confirmed on plan (gray 2" furring on A423, A101 tag PT0109), ported with reader-A fields')
walls.append(n); Wd[n['id']]=n

# ---- R-25 deck: hidden text is not a printed dimension
for w in walls:
    src=w.get('height_source','')
    if w.get('height_status')=='CONFIRMED' and 'A425.C' in src and (w.get('height_ft') or 0)>15:
        w['height_ft']=22.83 if w['height_ft']<22.83 else w['height_ft']; w['height_status']='PENDING'
        w['height_source']=src+' | STAGE 3 R-25: the 22\'-10" / 22\'-5" on A425.C sits under the printed \'B.O. DECK VARIOUS\' (hidden, not printed) -> PENDING, RFI-01 (22\'-10" loaded)'
        for f in w['faces']:
            if (f.get('height_ft') or 0)>15: f['height_ft']=22.83; f['height_source']=(f.get('height_source') or '')+' [PENDING RFI-01]'
for f in Wd['A-A425-3']['faces']:
    if 21<(f.get('height_ft') or 0)<22.8: f['height_ft']=22.83; f['height_source']+=' | STAGE 3 R-25: hidden 21\'-10" not printed -> 22\'-10" RFI-01'

for w in walls: w.pop('_frag',None)
# ---- assemble
c={}
c['constants']=json.load(open(W+'comun/constants.json'))['constants']
for k,v in gen.items():
    if k=='walls': continue
    c[k]=v
c['walls']=walls+gen.get('walls',[])
c['tags_descartados']=desc
c['blocking_items']=(gen.get('blocking_items') or [])+blocking
c['notes_info']=notes+['STAGE 3 reconciliation: see ../3_revision/resolucion.md and resolucion_items.json (A/B readings + A101 closure)']
c['rfis']=json.load(open('/tmp/chuze/work/etapas/3_revision/rfis_etapa3.json'))['rfis']
for x in c.get('ceilings',[]):
    sc=x.get('system_callout')
    if isinstance(sc,dict) and not sc.get('on_plan') and not sc.get('cuts_this'):
        sc['detail']='C-5/A121 '+sc['detail']
        sc['on_plan']=True
        sc['source']=sc['source']+' (STAGE 3: the C-5 finish tag is printed on this ceiling in the RCP; system from the A121 RCP finish schedule)'
exec(open('/tmp/chuze/scratch/RES/fixes.py').read())
json.dump(c,open(OUT,'w'),indent=1)
import collections
lf=collections.defaultdict(float)
for w in walls: lf[w['tag']]+=w['length_ft']
print({k:round(v,2) for k,v in sorted(lf.items())}, round(sum(lf.values()),2), len(walls))
