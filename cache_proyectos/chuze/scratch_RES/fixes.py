# validator-driven fixes
for w in c['walls']:
    if w['id']=='A-A422-3':
        w['untagged_reason']='No tag on A422 for this 6" wall between Storage 110 and Restroom 109; type from the A101 tag A6C PT0045 (tag inside restroom 109 on A101; that A101 tag is listed in tags_descartados as shown on enlarged plan A422) - this wall quantifies it'
for w in c['walls']:
    for k in ('segments_pt','corner_bead_edges','height_zones'):
        if k in w: w[k+'_info']=w.pop(k)
import copy as _cp
_W={w['id']:w for w in c['walls']}
def _split(mid,main_len,main_band,ret_id,ret_len,ret_band,ret_lens=None,op=None):
    m=_W[mid]; r=_cp.deepcopy(m)
    m['length_ft']=main_len; m['band'].update(main_band)
    r.update(id=ret_id,tag_ids=[],part_of=mid,length_ft=ret_len,band=dict(ret_band,sheet=m['band']['sheet']),openings=[],
             untagged_reason='untagged return of '+mid+' (joins the tagged wall it touches, E28 / PT3: partition_types adds it to that wall); split in STAGE 3 so each straight segment carries its own band')
    for k in ('storefront_in_lf_reason','img_res','band_length_ok_reason','default_type_rfi'): r.pop(k,None)
    m.pop('band_length_ok_reason',None)
    if ret_lens is not None:
        mf=[f for f in m['faces'] if f.get('length_ft') is None or round(f['length_ft'],2) not in ret_lens]
        rf=[f for f in r['faces'] if f.get('length_ft') is None or round(f['length_ft'],2) in ret_lens]
        for f in rf:
            if f.get('length_ft') is not None: f['length_ft']=ret_len
        m['faces']=mf or m['faces']; r['faces']=rf or r['faces']
    r['length_op']=op or f'return segment {ret_len} ft (vector, band)'
    m['length_op']=m.get('length_op','')+f' | STAGE 3 split: this row = main leg {main_len} ft; return = {ret_id} {ret_len} ft'
    c['walls'].insert(c['walls'].index(m)+1,r); _W[ret_id]=r
_split('A-A423-7',2.07,{},'A-A423-7r',0.61,{'ori':'V','c0':1941.1,'c1':1946.4,'lo':1819.0,'hi':1830.0},op='gray fill A425 x1941.1-1946.4 y1819.0->1830.0 = 11.0 pt / 18 = 0.61 ft')
_split('A-A423-8',2.07,{},'A-A423-8r',0.61,{'ori':'V','c0':1941.1,'c1':1946.4,'lo':1614.0,'hi':1625.0},op='gray fill A425 x1941.1-1946.4 y1614.0->1625.0 = 11.0 pt / 18 = 0.61 ft')
_split('A-A424-5',4.96,{'lo':1692.5},'A-A424-5r',1.76,{'ori':'V','c0':1692.5,'c1':1700.2,'lo':1819.7,'hi':1851.4},ret_lens=[1.76],op='gray fill A424 x1692.5-1700.2 from inner face y1819.7 to end at existing wall y1851.4 = 31.7 pt / 18 = 1.76 ft')
_split('A-A424-10',3.71,{'lo':2032.1},'A-A424-10r',1.59,{'ori':'V','c0':2032.1,'c1':2037.6,'lo':1525.2,'hi':1553.8},ret_lens=[1.64],op='gray fill A424 x2032.1-2037.6 y1525.2->1553.8 = 28.6 pt / 18 = 1.59 ft (from the H leg face; H leg printed 3\'-8 1/2" owns the corner)')
_W['A-A424-10']['length_status']='CONFIRMED'; _W['A-A424-10']['length_source']='A424 printed 3\'-8 1/2"'
_split('A-A424-12',3.40,{},'A-A424-12r',1.24,{'ori':'H','c0':1650.5,'c1':1659.6,'lo':2076.5,'hi':2098.8},ret_lens=[1.24],op='gray fill A424 x2076.5->2098.8 (existing E wall face) y1650.5-1659.6 = 22.3 pt / 18 = 1.24 ft')
_split('A-A424-13',2.08,{'ori':'V','c0':1488.2,'c1':1493.5,'lo':1875.4,'hi':1912.8},'A-A424-13r',0.58,{'ori':'H','c0':1875.4,'c1':1880.9,'lo':1477.7,'hi':1488.2},ret_lens=[0.58],op='gray fill A424 x1477.7->1488.2 y1875.4-1880.9 = 10.5 pt / 18 = 0.58 ft')
_split('A-A424-14',2.08,{},'A-A424-14r',0.57,{'ori':'H','c0':1875.4,'c1':1880.9,'lo':1682.2,'hi':1692.5},ret_lens=[0.57],op='gray fill A424 x1682.2->1692.5 y1875.4-1880.9 = 10.3 pt / 18 = 0.57 ft')
_split('A-A429-11',19.87,{},'A-A429-11r',6.57,{'ori':'V','c0':1178.4,'c1':1187.28,'lo':1583.28,'hi':1701.6},op='vector A429 y1583.28 (free N end) -> 1701.6 (N face of D6G PT0147) = 118.32 pt / 18 = 6.57 ft (= B-A429-13)')
w=_W['A-A431-2']; w['length_ft']=17.21; w['length_status']='DERIVED'
w['length_op']='end to end 1557.6 -> 1867.4 = 309.8 pt / 18 = 17.21 ft; the 4" gap at the existing mullion pier (1681.4-1687.4) is <= 6" and stays inside the run (PT2 contiguous <= 6"; same criterion as the A101 closure C-33 and reading B)'
w['notes']=(w.get('notes') or '')+' [STAGE 3 R-22: 16.88 -> 17.21, small gap inside the run]'
for i in ('A-A426-2','A-A426-3'):
    _W[i]['element']='pier'
# face clean-up of split walls
m,r=_W['A-A424-14'],_W['A-A424-14r']
m['faces']=[dict(f,length_ft=2.08) for f in m['faces'] if round(f.get('length_ft') or 0,2)==2.08]
r['faces']=[dict(f,length_ft=0.57) for f in r['faces'] if round(f.get('length_ft') or 0,3)==0.583]
m,r=_W['A-A424-5'],_W['A-A424-5r']
ef=[f for f in m['faces'] if 'E face of V' in f.get('room','')]
m['faces']=[f for f in m['faces'] if 'E face of V' not in f.get('room','')]
for f in m['faces']: f['length_ft']=4.96; f['length_source']='H leg 1692.5->1781.8 (gray fill)'
r['faces']=[f for f in r['faces'] if 'W face of V' in f.get('room','')]+[dict(f,length_ft=1.76,length_source='vector y1819.7->1851.4') for f in ef]
# MR only behind fixtures (R55.6 / R59.9 / D1, inventario._mr); other wet-room faces -> type X + RFI-32
WF=[('WC-105','water_closet','A-A421-13','Family Restroom 105 (east) - wet room','A421: toilet tank against this wall (west wall of Family Restroom 105)'),
    ('LAV-105','lavatory','A-A421-13','Family Restroom 105 (east) - wet room','A421: lavatory (A2.11) on this wall'),
    ('WC-109','water_closet','A-A421-15',"Kid's Club Restroom 109 (south) - wet room",'A422: toilet tank against the north wall of Restroom 109 (A2.71)'),
    ('LAV-109','lavatory','A-A421-15',"Kid's Club Restroom 109 (south) - wet room",'A422: lavatory (A2.11) on the north wall of Restroom 109'),
    ('MS-131a','mop_sink','A-A424-2',"Men's Janitor 131",'A424: mop sink in the SE corner of Men\'s Janitor 131 (A2.18) against the east wall'),
    ('MS-131b','mop_sink','A-A424-3',"Men's Janitor 131",'A424: mop sink in the SE corner of Men\'s Janitor 131 (A2.18) against the south wall'),
    ('MS-138','mop_sink','A-A423-6',"Women's Janitor 138",'A425: mop sink (A2.18) in the NE corner of Women\'s Janitor 138 against the east wall'),
    ('UR-130','urinal','A-A424-6',"Men's Restroom 130 urinal area",'A424: urinal (A2.59) on this wet wall'),
    ('SH-129a','shower','A-A424-11',"Men's Shower 129 standard stall",'A424: shower stall partition (A2.134 / A3.11)'),
    ('SH-129b','shower','A-A424-11',"Men's Shower 129 ADA stall",'A424: ADA shower stall side wall'),
    ('SH-129c','shower','A-A424-12',"Men's Shower 129 ADA stall (W face of V)",'A424: ADA shower stall east wall'),
    ('SH-129d','shower','A-A424-12r',"Men's Shower 129 (N face of return)",'A424: ADA shower stall return'),
    ('SH-129e','shower','A-A424-9',"dry vanity alcove + Men's Shower 129",'A424: west wall of the first shower stall')]
c['wet_fixtures']=[{'ref':a,'kind':k,'wall':w,'room':rm,'source':s,'back_source':s+' - fixture bears on this face (STAGE 3)'} for a,k,w,rm,s in WF]
keep={(w,rm) for _,_,w,rm,_ in WF}
conv=[]
for w in c['walls']:
    for f in w.get('faces') or []:
        if 'MR' in str(f.get('board','')).upper() and (w['id'],str(f.get('room'))) not in keep:
            L=f.get('length_ft') or w['length_ft']; H=f.get('height_ft') or 0
            conv.append((w['id'],f.get('room'),round(L*H,1)))
            f['board']='5/8" type X'; f['board_source']='spec 09 29 00 2.2 Type X; STAGE 3 R-26: MR only on faces where a toilet / lavatory / urinal / mop sink / shower bears (SKILL R55.6 / R59.9); A111 note 3 MR at all locker / restroom faces -> RFI-32'
c['_mr_conv_info']=conv
c['mr_conversion_info']=c.pop('_mr_conv_info')
bk=[];pend=[];excl=[]
for i,b in enumerate(c.get('blocking_items') or []):
    b.setdefault('ref',f"blocking-{i+1} {str(b.get('wall') or b.get('label') or '')[:40]}")
    mat=str(b.get('material') or '')
    if 'wood' in mat.lower() or 'EXCLUDED' in mat.upper(): excl.append(b); continue
    try: lf=float(b.get('lf'))
    except (TypeError,ValueError): lf=None
    if mat=='metal' and lf is not None: b['lf']=lf; bk.append(b)
    else: pend.append(b)
c['blocking_items']=bk
c['blocking_excluded_info']=excl
c['blocking_pending_info']=pend
for w in c['walls']:
    if not str(w.get('source') or '').strip():
        w['source']='; '.join(x for x in (str(w.get('length_source') or w.get('sheet') or ''), str(w.get('detail_source') or '')) if x)
_decl=[str(o['ref']) for w in c['walls'] for o in (w.get('openings') or [])]
_why={'101A':'existing exterior lobby storefront door (A601 MATCH EXISTING, existing frame) - not in a new wall',
 '101B':'existing exterior lobby storefront door (A601 MATCH EXISTING, existing frame) - not in a new wall',
 '102':'lobby gate OS6 by manufacturer (A601 MFG) - no wall opening / header',
 '103':'check-in gate by manufacturer (A601 MFG) - no wall opening / header',
 '104':'smoothie gate by manufacturer (A601 MFG) - no wall opening / header',
 '107':'AD1 door inside interior storefront C (declared as opening C of A-A421-16)',
 '107A':"kid's check-in gate by manufacturer (A601 MFG) - no wall opening / header",
 '107B':"Kid's Club AD1 aluminum door in an aluminum (ALF) glazing frame - frame/head by storefront trade; no stud wall opening found in the reconciled runs",
 '113':'AD1 door inside interior storefront H (declared as opening H (door 113) of A-A427-3)',
 '124':'VIP room OS6 by manufacturer (A601 MFG) - no wall opening / header',
 '133':'door in the existing Maintenance Fitness wall (A425 EXISTING; frame in existing opening) - no new header',
 '134':'door in the existing Electrical Room wall (A423; A-A423-4 infill beside it) - existing opening, no new header loaded (RFI-29)',
 '152':'door in the existing north wall of Laundry 152 (A425 EXISTING) - no new header'}
_marks=['101A','101B','102','103','104','105','106','107','107A','107B','109','110','113','115','119','122','123','124','125','126','127','131','132','133','134','138','141','152']
_none=[{'ref':m,'why':_why.get(m,'see A601')} for m in _marks if m not in _decl]
c['opening_schedule']={'sources':['A601','A602','A101','S200','S300','M110','M401','M402'],
  'items':[{'ref':r} for r in sorted(set(_decl))]+[{'ref':x['ref']} for x in _none],
  'none':_none,
  'source':'A601 DOOR SCHEDULE (28 marks) + A601 GLAZING AND FRAME TYPES + cased openings on A426 / A429; S200 / S300 swept for lintels (none at these openings; A602 "STEEL HEADER - REF STRUCT" = RFI-12); M110 / M401 / M402 swept for ducts (mep_sweep)'}
# ---- nodes (2 ends per wall) generated from the canon bands, same sheet only
def _rect(b):
    if b['ori']=='H': return (b['lo'],b['c0'],b['hi'],b['c1'])
    return (b['c0'],b['lo'],b['c1'],b['hi'])
def _endseg(b,which):
    v=b['lo'] if which=='lo' else b['hi']
    return (v,b['c0'],v,b['c1']) if b['ori']=='H' else (b['c0'],v,b['c1'],v)
def _hit(seg,r,t=4.0):
    x0,y0,x1,y1=seg; return not (x1<r[0]-t or x0>r[2]+t or y1<r[1]-t or y0>r[3]+t)
cand=[w for w in c['walls'] if isinstance(w.get('band'),dict) and w['band'].get('ori') in ('H','V') and w.get('element','wall') not in ('column_wrap',)]
ids_all=[w['id'] for w in c['walls'] if w.get('element','wall') not in ('column_wrap',)]
used={}; nodes=[]; k=0
def _use(i): used[i]=used.get(i,0)+1
ends=[(w,e) for w in cand for e in ('lo','hi')]
# L corners: end of A touches end zone of perpendicular B (both ends free so far)
for w,e in ends:
    if used.get((w['id'],e)): continue
    b=w['band']; seg=_endseg(b,e)
    for o in cand:
        if o is w or o['band']['sheet']!=b['sheet'] or o['band']['ori']==b['ori']: continue
        ob=o['band']
        for oe in ('lo','hi'):
            if used.get((o['id'],oe)): continue
            r=_rect(ob); th=abs(b['c1']-b['c0'])+4
            # o's end must lie near w's band
            oseg=_endseg(ob,oe)
            if _hit(seg,r) and _hit(oseg,_rect(b),t=th):
                k+=1; nodes.append({'id':f'N{k}','kind':'L','walls':[w['id'],o['id']],'source':f"STAGE 3 node from canon bands ({b['sheet']}): corner {w['id']}.{e} / {o['id']}.{oe}"})
                used[(w['id'],e)]=1; used[(o['id'],oe)]=1; break
        if used.get((w['id'],e)): break
# T: end of A touches the side of B
for w,e in ends:
    if used.get((w['id'],e)): continue
    b=w['band']; seg=_endseg(b,e)
    for o in cand:
        if o is w or o['band']['sheet']!=b['sheet'] or o['band']['ori']==b['ori']: continue
        if _hit(seg,_rect(o['band'])):
            k+=1; nodes.append({'id':f'N{k}','kind':'T','branch':w['id'],'through':o['id'],'source':f"STAGE 3 node from canon bands ({b['sheet']}): {w['id']}.{e} dies into the side of {o['id']}"})
            used[(w['id'],e)]=1; break
# remaining ends free
for i in ids_all:
    for e in ('lo','hi'):
        if not used.get((i,e)):
            k+=1; nodes.append({'id':f'N{k}','kind':'free','wall':i,'source':'STAGE 3: free end / end against existing construction or a wall on another sheet (no stud added, R60.1)'})
c['nodes']=nodes
w=_W['A-A101-1']; w['height_ft']=22.83; w['height_status']='PENDING'
w['height_source']='head D assumed (type not printed, RFI-20) -> stud to B.O. deck; deck not printed (A121 note 4 assumed, A437 VARIOUS) -> 22\'-10" loaded [PENDING, RFI-01]'
for f in w['faces']: f['height_ft']=22.83; f['height_source']+=' [22\'-10" loaded, RFI-01]'
for w in c['walls']:
    if str(w.get('stud_size')).strip()=='2"':
        w['stud_size']='2-1/2"'
        w['stud_source']='A301 TYPE B schedule prints STUD SIZE 2"; 2" is not a standard SSMA stud depth (162 / 250 / 362 ...) and the take-off families have no 2" stud -> loaded 2-1/2" (next standard depth, conservative) [PENDING, RFI-32]'
for w in c['walls']:
    if w.get('element')=='soffit_side': continue
    key=f"TYPE {w['tag']}/A301"
    if key in c['details'] and w.get('detail')!=key:
        w['detail_info']=w.get('detail'); w['detail']=key; w['detail_source']='A301'
for i in ('A-A421-1','A-A421-2'):
    w=_W[i]
    w['faces']=[dict(f,side='A',length_ft=(3.0 if f['side']=='B' else 0.885)) for f in w['faces']]
    w['faces_ft']=[3.0,0.885,0.885]; w['fos_chain']['value']=[3.0,0.885,0.885]
# per-side tramos must sum to the wall length (board_caras): absorb end/corner zones in the last tramo
def _fixsides(w):
    L=w['length_ft']; pl={}
    for f in w.get('faces',[]):
        if f.get('side') in ('A','B') and f.get('length_ft') is not None: pl.setdefault(f['side'],[]).append(f)
    for s,fs in pl.items():
        d=round(L-sum(f['length_ft'] for f in fs),3)
        if abs(d)>0.05:
            big=max(fs,key=lambda f:f['length_ft']); big['length_ft']=round(big['length_ft']+d,3)
            big['length_source']=str(big.get('length_source',''))+f' (STAGE 3: {d:+.2f} ft end / corner zone added so the side sums to the wall length {L})'
w=_W['A-A423-9']
for f in w['faces']:
    f['room']=f['room']+f" ({f['side']} face)"; f['side']='A'
w=_W['A-A424-5']
w['faces']=[f for f in w['faces'] if 'face of H' in f.get('room','')]
for i in ('A-A426-2','A-A426-3'):
    w=_W[i]; fa=[f for f in w['faces'] if f['side']=='A'][0]; fe=[f for f in w['faces'] if f['side']=='END'][0]; fb=[f for f in w['faces'] if f['side']=='B'][0]
    fa['length_ft']=3.0; fa['length_source']='A426 printed 3\'-0"'
    e1=dict(fe,side='A',length_ft=0.835,length_source='A426 printed 10" leg',room='Box side 10" (west)'); e2=dict(e1,room='Box side 10" (east)')
    fb['length_ft']=4.67; fb['length_source']='inside of the U against the A3C wall (no board)'
    w['faces']=[fa,e1,e2,fb]
for w in c['walls']: _fixsides(w)
for w in c['walls']:
    z=[f for f in w.get('faces',[]) if int(f.get('layers') or 0)==0]
    if z:
        w['faces']=[f for f in w['faces'] if int(f.get('layers') or 0)!=0]
        w['faces_none_info']=[{'side':f.get('side'),'room':f.get('room'),'board_none_reason':f.get('board_none_reason')} for f in z]
        _fixsides(w)
for f in _W['A-A424-7']['faces']:
    if int(f.get('layers') or 0)==1:
        f['layers']=2; f['layers_source']='TYPE X6D/A301 detail draws 2 layers each side (UL U465; RFI-07)'
for w in c['walls']:
    for f in w.get('faces',[]):
        if f.get('length_ft') is not None and not str(f.get('length_source') or '').strip():
            f['length_source']=f"{w.get('band',{}).get('sheet',w.get('sheet'))} vector (room extent given in the face room text)"
for w in c['walls']:
    for f in w.get('faces',[]):
        if f.get('side')=='END' and f.get('length_ft') is None:
            t=float(w.get('thickness_measured_in') or 6)/12
            f['length_ft']=round(t,2); f['length_source']=f"free-end face = wall thickness {w.get('thickness_measured_in')} in measured on {w['band']['sheet']} (vector)"
_W['A-A429-11']['faces']=[f for f in _W['A-A429-11']['faces'] if not (f.get('side')=='END' and 'stub north' in f.get('room',''))] or _W['A-A429-11']['faces']
for f in _W['A-A429-11']['faces']:
    if f.get('side')=='END': f['room']='RECOVERY 113 (west free end)'
for f in _W['A-A429-11r']['faces']:
    if f.get('side')=='END': f['room']='RECOVERY 113 (stub north free end)'
_BM={'5/8" type X':'5/8 type X','5/8" gyp bd':'5/8 type X','5/8" MR':'5/8 MR','DensArmor Plus':'5/8 type X WR'}
for w in c['walls']:
    for f in w.get('faces',[]):
        b=f.get('board')
        if b in _BM:
            if b!='5/8" type X': f['board_product_info']=b+(' -> spec 09 29 00 2.2 lists only 5/8" Type X interior board: loaded type X everywhere (one criterion; RFI-05)' if b=='5/8" gyp bd' else (' (A301 type note: DensArmor Plus 5/8" at pool / spa rooms full height)' if 'Dens' in b else ''))
            f['board']=_BM[b]
for w in c['walls']:
    if w.get('element')=='soffit_side':
        for k in ('top_track','bottom_track'):
            if k in w: w[k+'_info']=w.pop(k)
import re as _re
_RXS=_re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")
def _clean_src(t):
    toks=[]
    for tok in _re.findall(r"[A-Za-z0-9./\-]+",str(t)):
        tok=tok.strip('.')
        if _RXS.match(tok) and _re.search(r'[A-Z]\d{3}|[A-Z]\d{1,3}\.',tok) and tok not in toks: toks.append(tok)
    return ', '.join(toks)
for w in c['walls']:
    for o in w.get('openings') or []:
        s=o.get('source')
        cs=_clean_src(s)
        if cs and cs!=s:
            o['source_info']=s; o['source']=cs
for w in c['walls']:
    for o in w.get('openings') or []:
        r=str(o['ref'])
        if r.startswith('OPNG-A426'):
            o['header']='not_called'; o['header_source']='A426, A426.A, A602'; o['header_rfi']='RFI-29 (cased opening head not detailed; metal stud header would add (6.5 + 1.33) x pieces LF)'
        elif r.startswith('A429-RZ'):
            o['header']='steel_by_others'; o['header_source']='A/S200 (HSS 6x6 posts / frame at the 8\'-0" opening = structural steel, EXCLUDED; E16)'
        elif o.get('kind')=='storefront':
            o['header']='steel_by_others'; o['header_source']='8/A602 "STEEL HEADER FRAMING - REF: STRUCT." at interior storefront heads (structural steel EXCLUDED; not shown on S100-S300) - RFI-12'
        else:
            o['header']='steel_by_others'; o['header_source']=('1/A602' if r=='115' else '6/A602')+' "STEEL HEADER @ HEAD LOCATIONS - REF: STRUCT." (structural steel EXCLUDED; not shown on S100-S300) - RFI-12'
for i in ('A-A421-1','A-A421-2'):
    w=_W[i]; w.pop('fos_chain',None)
    w['fos_chain_faces']=[{'value':[3.0],'source':'A421 printed 3\'-0" (box face)'},
        {'measured_op':'(1038.5 - 1022.6) / 18 = 0.88 ft (A6D S face to box S face)','source':'A421 vector'},
        {'measured_op':'(1038.5 - 1022.6) / 18 = 0.88 ft','source':'A421 vector'}]
for w in c['walls']:
    for o in w.get('openings') or []:
        if o.get('kind')=='storefront':
            o['substrate_none_reason']='interior storefront: 8/A602 HEAD/JAMB @ INT. STOREFRONT shows "2x6 BLOCKING" (wood, EXCLUDED Div. 06) and 5/8" gyp bd to the frame; no plywood substrate strip'
            o['location']='interior'
for i in ('A-A423-9','A-A426-2','A-A426-3','A-A421-1','A-A421-2'):
    _W[i]['jamb_strips_none_reason']='no storefront jamb strip detailed at this furring box: C/A301 furring type C only (no FRT plywood jamb label on A421 / A423 / A426 / 8/A602 - wood would be EXCLUDED anyway)'
_fr=c.pop('frp',None)
if isinstance(_fr,dict) and _fr.get('none_reason'):
    c['frp_none_reason']=_fr['none_reason']+' ('+_fr.get('source','')+')'
for w in c['walls']:
    for o in w.get('openings') or []:
        if o.get('kind')=='storefront':
            o['jamb_return']=False; o['jamb_return_source']='8/A602 HEAD/JAMB DETAIL @ INT. STOREFRONT: gyp bd stops at the aluminum frame (sealant), no gypsum return drawn (0.F jamb return rule)'
for w in c['walls']:
    if w.get('part_of'):
        w['return_basis']={'value':'inner_face','source':f"{w['band']['sheet']} vector: the tagged leg {w['part_of']} owns the corner (R70.2 one owner); return measured from its inner face so the corner is not counted twice"}
