import json,glob,sys
sys.path.insert(0,'/tmp/chuze/scratch/CIERRE')
from T import T
W='/tmp/chuze/work/etapas/2_lectura/'
C=json.load(open('/tmp/chuze/work/etapas/3_revision/cierre_A101.json'))['walls']
def load(side):
    out=[]
    for f in sorted(glob.glob(W+side+'/Z*.json')):
        for w in json.load(open(f)).get('walls',[]): w['_f']=f.split('/')[-1]; out.append(w)
    return out
def proj(w):
    b=w['band']; s=b.get('sheet',w['sheet'])
    if s=='A101': return dict(ori=b['ori'],c0=b['c0'],c1=b['c1'],lo=b['lo'],hi=b['hi'])
    p,k,dx,dy=T[s]
    o=b['ori']
    if o=='H': return dict(ori='H',c0=k*b['c0']+dy,c1=k*b['c1']+dy,lo=k*b['lo']+dx,hi=k*b['hi']+dx)
    if o=='V': return dict(ori='V',c0=k*b['c0']+dx,c1=k*b['c1']+dx,lo=k*b['lo']+dy,hi=k*b['hi']+dy)
    if o=='BOX': return dict(ori='BOX',x0=k*b['c0']+dx,x1=k*b['c1']+dx,y0=k*b['lo']+dy,y1=k*b['hi']+dy)
def match(pb,c):
    cb=c['band']
    if pb['ori']=='BOX':
        # box vs closure H/V: rect overlap
        if cb['ori']=='H': cx0,cx1,cy0,cy1=cb['lo'],cb['hi'],cb['c0'],cb['c1']
        else: cx0,cx1,cy0,cy1=cb['c0'],cb['c1'],cb['lo'],cb['hi']
        ox=min(pb['x1'],cx1)-max(pb['x0'],cx0); oy=min(pb['y1'],cy1)-max(pb['y0'],cy0)
        return (max(ox,oy)/6.75) if ox>-2 and oy>-2 else 0
    if pb['ori']!=cb['ori']: return 0
    m1=(pb['c0']+pb['c1'])/2; m2=(cb['c0']+cb['c1'])/2
    if abs(m1-m2)>4: return 0
    ov=min(pb['hi'],cb['hi'])-max(pb['lo'],cb['lo'])
    return ov/6.75 if ov>0.5 else 0
if __name__=='__main__':
    for side in 'AB':
        for w in load(side):
            pb=proj(w)
            ms=[(c['id'],round(match(pb,c),2)) for c in C if match(pb,c)>0]
            pl=round(((pb['hi']-pb['lo']) if pb['ori'] in 'HV' else 0)/6.75,2)
            print(w['id'],w['tag'],w['length_ft'],'projLF',pl,ms)
