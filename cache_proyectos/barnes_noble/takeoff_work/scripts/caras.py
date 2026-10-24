import json, sys, pymupdf as fitz
from collections import defaultdict
PDF='/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/bidset/bidset_SIN_MARKUPS.pdf'
wc=json.load(open('/home/user/Reading-Plans/cache_proyectos/barnes_noble/walls_coords.json'))['walls']
d=fitz.open(PDF)
segs={}
for pg in (6,15):
    p=d[pg-1]; M=p.rotation_matrix; L=[]
    for dr in p.get_drawings():
        w=dr.get('width') or 0
        for it in dr['items']:
            if it[0]=='l':
                a=fitz.Point(it[1])*M; b=fitz.Point(it[2])*M
                L.append((a.x,a.y,b.x,b.y,w))
            elif it[0]=='re':
                r=fitz.Rect(it[1])*M
                for (x0,y0,x1,y1) in ((r.x0,r.y0,r.x1,r.y0),(r.x0,r.y1,r.x1,r.y1),(r.x0,r.y0,r.x0,r.y1),(r.x1,r.y0,r.x1,r.y1)):
                    L.append((x0,y0,x1,y1,w))
    segs[pg]=L
out={}
for w in wc:
    pg=6 if w['sheet']=='A-101' else 15; esc=9 if pg==6 else 36
    s=w['points_pt'][0]
    if len(w['points_pt'])>1 or len(s)!=2: out[w['wall_id']]='multi'; continue
    (x0,y0),(x1,y1)=s
    if abs(y0-y1)<0.5: ori='H'; c=y0; lo,hi=sorted((x0,x1))
    elif abs(x0-x1)<0.5: ori='V'; c=x0; lo,hi=sorted((y0,y1))
    else: out[w['wall_id']]='diag'; continue
    offs=defaultdict(float)
    for (a,b,cc,dd,lw) in segs[pg]:
        if ori=='H' and abs(b-dd)<0.2:
            o=b-c; ov=min(hi,max(a,cc))-max(lo,min(a,cc))
        elif ori=='V' and abs(a-cc)<0.2:
            o=a-c; ov=min(hi,max(b,dd))-max(lo,min(b,dd))
        else: continue
        if abs(o)<=1.2*esc and ov>0: offs[(round(o,2),round(lw,2))]+=ov
    top=sorted(offs.items(),key=lambda kv:-kv[1])[:8]
    out[w['wall_id']]={'ori':ori,'c':c,'lo':lo,'hi':hi,'len':hi-lo,'offs':[(k[0],k[1],round(v,1)) for k,v in top]}
for k,v in out.items(): print(k,v if isinstance(v,str) else (v['ori'],round(v['c'],2),round(v['len'],1),v['offs']))
json.dump(out,open(sys.argv[1],'w'),indent=0)
