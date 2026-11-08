import sys, json; sys.path.insert(0,'/root/cr/work/scripts'); sys.path.insert(0,'.')
import contorno_cielos as cc, fitz
from L2L3_poly import L2
def chk(sh, polys, tol=0.7):
    p=cc.pdf[cc.HS.index(sh)]
    out={}
    for k,P in polys.items():
        xs=[q[0] for q in P]; ys=[q[1] for q in P]
        H,V=cc.lineas(p,fitz.Rect(min(xs)-10,min(ys)-10,max(xs)+10,max(ys)+10))
        bad=[]
        for i in range(len(P)):
            a,b=P[i],P[(i+1)%len(P)]
            if abs(a[1]-b[1])<0.01:
                v,lo,hi=a[1],min(a[0],b[0]),max(a[0],b[0]); Ls=H
            else:
                v,lo,hi=a[0],min(a[1],b[1]),max(a[1],b[1]); Ls=V
            cov=0; near=[]
            for (q,s,e) in Ls:
                if abs(q-v)<=tol: cov+=max(0,min(e,hi)-max(s,lo))
                elif abs(q-v)<=4 and min(e,hi)-max(s,lo)>0.5*(hi-lo): near.append(round(q,2))
            if cov<0.5*(hi-lo): bad.append(((round(a[0],2),round(a[1],2)),(round(b[0],2),round(b[1],2)),'cov%.0f%%'%(100*cov/max(hi-lo,1e-6)),sorted(set(near))))
        out[k]=bad
    return out
if __name__=='__main__':
    sh=sys.argv[1]
    r=chk(sh,{k:v['p'] for k,v in L2.items()})
    for k,b in r.items():
        print(k, len(b)); [print('   ',x) for x in b]
