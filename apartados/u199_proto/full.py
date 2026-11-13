import pymupdf,numpy as np,json,math,sys,collections
d=pymupdf.open('/tmp/claude-0/crset/CR_arch.pdf'); K=3.0; KEY=16; EK=9.0
lab2i={}
for i,p in enumerate(d):
    import re
    t=p.get_text(); m=re.findall(r'\b(A\d\.\d{2})\b',t)
    if m: lab2i.setdefault(m[-1],i)
def ras(i,zoom,clip=None):
    p=d[i]; pix=p.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),clip=clip,colorspace=pymupdf.csGRAY)
    return (np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width)<128).astype(np.float32)
B=ras(KEY,K/EK)
def corr(a,b):
    H=a.shape[0]+b.shape[0]; W=a.shape[1]+b.shape[1]
    c=np.fft.irfft2(np.fft.rfft2(b-b.mean(),(H,W))*np.conj(np.fft.rfft2(a-a.mean(),(H,W))),(H,W))
    iy,ix=np.unravel_index(np.argmax(c),c.shape); v=c.max()/np.sqrt(((a-a.mean())**2).sum()*((b-b.mean())**2).sum())
    if iy>H-a.shape[0]: iy-=H
    if ix>W-a.shape[1]: ix-=W
    return v,iy,ix
can=json.load(open(sys.argv[1])); floor=sys.argv[2] if len(sys.argv)>2 else 'L1'
ws=[w for k in ('walls','existing_walls','excluded_walls') for w in can.get(k) or [] if w.get('floor')==floor]
por=collections.defaultdict(list)
for w in ws:
    for p in (w.get('paths') or ([w['path']] if w.get('path') else [])): por[w.get('sheet')].append((w['id'],p))
T={}
for sh,lst in por.items():
    if sh not in lab2i: print('sin hoja',sh); continue
    i=lab2i[sh]
    if i==KEY: T[sh]=(1.0,0,0,None); continue
    xs=[x for _,p in lst for x,_ in p]; ys=[y for _,p in lst for _,y in p]
    clip=pymupdf.Rect(min(xs)-150,min(ys)-150,max(xs)+150,max(ys)+150)&d[i].rect
    best=None
    for e in (12,13.5,18,24,36,48):
        v,iy,ix=corr(ras(i,K/e,clip),B)
        if best is None or v>best[0]: best=(v,e,iy,ix)
    T[sh]=(best[1],best[2],best[3],clip); print(sh,i,'escala',best[1],'corr',round(best[0],3))
def to_key(sh,x,y):
    e,iy,ix,clip=T[sh]
    if clip is None: return x,y
    return ((x-clip.x0)*K/e+ix)/(K/EK),((y-clip.y0)*K/e+iy)/(K/EK)
S=[]
for sh,lst in por.items():
    if sh not in T: continue
    for wid,p in lst:
        q=[to_key(sh,x,y) for x,y in p]
        for a,b in zip(q,q[1:]): S.append((a[0],a[1],b[0],b[1],wid))
json.dump(S,open('/tmp/claude-0/crset/segs_key_'+sys.argv[1].split('/')[-1],'w'))
pts=json.load(open('/tmp/claude-0/crset/rated_pts_A201.json'))
def dseg(px,py,s):
    x0,y0,x1,y1=s[:4];dx,dy=x1-x0,y1-y0;L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x0)*dx+(py-y0)*dy)/L));return math.hypot(px-x0-t*dx,py-y0-t*dy)
tol=1.5*EK
sin=[(x,y) for x,y in pts if not any(dseg(x,y,s)<=tol for s in S)]
print('segs',len(S),'rated',len(pts),'sin muro',len(sin))
near=[(x,y) for x,y in sin if 1640<=x<=1700 and 1270<=y<=1300]
print('cerca de XW.6.3-L1-04 (1653-1690,1286):',len(near))
json.dump(sin,open('/tmp/claude-0/crset/sin_'+sys.argv[1].split('/')[-1],'w'))
