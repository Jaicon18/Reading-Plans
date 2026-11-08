import json, re, sys, fitz, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
W='/root/cr/work'
c=json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
HS=list(json.load(open(f'{W}/set_texto.json'))['hojas'])
pdf=fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
EXCL=set(sys.argv[2].split(',')) if len(sys.argv)>2 else {'W.4'}
sh=sys.argv[1]; Z=2
p=pdf[HS.index(sh)]
im=Image.new('L',(int(p.rect.width*Z),int(p.rect.height*Z)),255); d=ImageDraw.Draw(im)
for w in c['walls']+c['existing_walls']:
    if w.get('sheet')!=sh: continue
    t=w['id'].rsplit('-',2)[0]
    if t in EXCL: continue
    for P in (w.get('paths') or [w['path']]):
        d.line([(x*Z,y*Z) for x,y in P],fill=0,width=3*Z)
a=np.array(im)<128
G=int(sys.argv[3]) if len(sys.argv)>3 else 0
if G: a=ndimage.binary_closing(a,structure=np.ones((G*Z,G*Z)))
Image.fromarray((~a*255).astype('uint8')).save('/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/clg/rast.png')
free=~a; lab,n=ndimage.label(free)
fl={'A2.01':'L1','A2.02':'L2','A2.03':'L3','A2.04':'L4'}[sh]
for x in c['ceilings']:
    if x.get('floor')!=fl: continue
    m=re.search(r'\b([1-4]\d\d)\b',x['room'])
    if not m: print('NOID',x['room']); continue
    best=None
    for r in p.search_for(m.group(1)):
        cx,cy=int((r.x0+r.x1)/2*Z),int((r.y1+4)*Z)
        if cy>=a.shape[0] or not free[cy,cx]: continue
        reg=lab==lab[cy,cx]; sf=reg.sum()/(Z*Z)/81
        e=(sf-x['area_sf'])/x['area_sf']
        if best is None or abs(e)<abs(best[0]): best=(e,sf)
    print(f"{x['room'][:40]:40s} printed {x['area_sf']:8} flood {best[1] if best else None!s:>10.10} err {round(best[0]*100,1) if best else None}")
