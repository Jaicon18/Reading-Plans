import sys; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, fitz
from matplotlib.path import Path
def snap(v,lo,hi,s,L,maxd,ov=0.5):
    c=[]
    for (q,a,b) in L:
        d=(q-v)*s
        if -0.3<=d<=maxd and min(b,hi)-max(a,lo)>=ov*(hi-lo): c.append((d,q))
    if not c: return None
    c=sorted(set(c)); cur=c[0]
    for x in c[1:]:
        if x[0]-cur[0]<=1.0: cur=x
        else: break
    return round(cur[1],2)
def ajustar(sh, P, maxd=6.0, fijos=()):
    """P: polígono ortogonal aproximado (ejes); cada borde se ajusta a la cara dibujada más hacia adentro dentro de maxd.
    fijos: índices de bordes que no se ajustan. Devuelve poly, log."""
    p=cc.pdf[cc.HS.index(sh)]
    xs=[q[0] for q in P]; ys=[q[1] for q in P]
    HL,VL=cc.lineas(p,fitz.Rect(min(xs)-15,min(ys)-15,max(xs)+15,max(ys)+15))
    pa=Path(P); n=len(P); E=[]; log=[]
    for i in range(n):
        a,b=P[i],P[(i+1)%n]
        if abs(a[1]-b[1])<1e-6:
            v=a[1]; lo,hi=sorted([a[0],b[0]]); xm=(lo+hi)/2
            s=1 if pa.contains_point((xm,v+1.0)) else -1
            r=None if i in fijos else snap(v,lo+2,hi-2,s,HL,maxd)
            E.append(('H',r if r is not None else v)); log.append(f"H y{v}->{r}")
        else:
            v=a[0]; lo,hi=sorted([a[1],b[1]]); ym=(lo+hi)/2
            s=1 if pa.contains_point((v+1.0,ym)) else -1
            r=None if i in fijos else snap(v,lo+2,hi-2,s,VL,maxd)
            E.append(('V',r if r is not None else v)); log.append(f"V x{v}->{r}")
    poly=[]
    for i in range(n):
        e1,e2=E[i-1],E[i]
        poly.append([e2[1],e1[1]] if e1[0]=='H' else [e1[1],e2[1]])
    return poly,log
