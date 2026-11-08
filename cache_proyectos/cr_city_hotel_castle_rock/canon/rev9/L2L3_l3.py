import sys, copy; sys.path.insert(0,'/root/cr/work/scripts'); sys.path.insert(0,'.')
import contorno_cielos as cc, fitz
from L2L3_poly import L2, area
p3=cc.pdf[cc.HS.index('A2.03')]
def resnap(P, tol=0.7, force={}):
    xs=[q[0] for q in P]; ys=[q[1] for q in P]
    H,V=cc.lineas(p3,fitz.Rect(min(xs)-10,min(ys)-10,max(xs)+10,max(ys)+10))
    n=len(P); new=[]; log=[]
    for i in range(n):
        a,b=P[i],P[(i+1)%n]
        if abs(a[1]-b[1])<0.01: t='H'; v,lo,hi=a[1],min(a[0],b[0]),max(a[0],b[0]); Ls=H
        else: t='V'; v,lo,hi=a[0],min(a[1],b[1]),max(a[1],b[1]); Ls=V
        if (t,v) in force: new.append((t,force[(t,v)])); log.append(f"{t}{v}->{force[(t,v)]} (manual)"); continue
        cov={}
        for (q,s,e) in Ls:
            if abs(q-v)<=tol: cov[round(q,2)]=cov.get(round(q,2),0)+max(0,min(e,hi)-max(s,lo))
        ok={q:c for q,c in cov.items() if c>=0.5*(hi-lo)}
        if v in ok or not ok: new.append((t,v)); 
        else:
            q=min(ok,key=lambda q:abs(q-v)); new.append((t,q)); log.append(f"{t}{v}->{q}")
        if not ok: log.append(f"{t}{v} SIN LINEA ({lo:.1f}-{hi:.1f})")
    Q=[]
    for i in range(n):
        e0,e1=new[i-1],new[i]
        x=e0[1] if e0[0]=='V' else e1[1]; y=e0[1] if e0[0]=='H' else e1[1]
        Q.append([x,y])
    return Q,log
FORCE={
 '201':{('V',1028.3):1032.6},
 '202':{('V',1028.0):1032.12,('H',536.0):537.0},
 '203':{('H',679.6):680.4,('V',1027.7):1028.28},
 '205':{('V',1003.9):1003.08},
 '209':{('H',1267.8):1276.56},
 '210':{('V',793.2):793.56},
 '212':{('V',567.0):565.56,('H',895.2):896.64},
}
L3={}
for k,v in L2.items():
    P,log=resnap(v['p'],force=FORCE.get(k,{}))
    b=None
    if v.get('b'): b,lb=resnap(v['b'],force=FORCE.get(k,{}))
    L3[str(int(k)+100)]=dict(v,p=P,b=b,log=log)
if __name__=='__main__':
    for k,v in L3.items():
        A=(area(v['p'])-(area(v['hole']) if v.get('hole') else 0))/81; B=area(v['b'])/81 if v.get('b') else 0
        print(k, round(A,2), round(B,2), round(A-B,2), v['log'])
