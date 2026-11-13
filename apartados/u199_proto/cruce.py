import json,math,sys
pts=json.load(open('/tmp/claude-0/crset/rated_pts_A201.json'))
def segs(can,sheet='A2.01'):
    out=[]
    for k in ('walls','existing_walls','excluded_walls'):
        for w in can.get(k) or []:
            if w.get('sheet')!=sheet: continue
            ps=w.get('paths') or ([w['path']] if w.get('path') else [])
            for p in ps:
                for a,b in zip(p,p[1:]): out.append((a[0],a[1],b[0],b[1],w['id']))
    return out
def dseg(px,py,s):
    x0,y0,x1,y1=s[:4];dx,dy=x1-x0,y1-y0;L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x0)*dx+(py-y0)*dy)/L));return math.hypot(px-x0-t*dx,py-y0-t*dy)
for f in sys.argv[1:]:
    can=json.load(open(f)); S=segs(can); tol=1.5*9
    sin=[(x,y) for x,y in pts if not any(dseg(x,y,s)<=tol for s in S)]
    # cluster on 2ft grid
    cl={}
    for x,y in sin: cl.setdefault((int(x//36),int(y//36)),[]).append((x,y))
    big=[(k,len(v)) for k,v in cl.items() if len(v)>=4]
    print(f.split('/')[-1],'segs',len(S),'rated pts',len(pts),'sin muro',len(sin),'clusters',len(big))
    json.dump(sin,open(f'/tmp/claude-0/crset/sin_{f.split("/")[-1]}','w'))
