import sys, json; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, fitz
sh=sys.argv[1]; P=json.loads(sys.argv[2]); W=float(sys.argv[3]) if len(sys.argv)>3 else 9
p=cc.pdf[cc.HS.index(sh)]
n=len(P)
for i in range(n):
    a,b=P[i],P[(i+1)%n]
    if abs(a[1]-b[1])<1e-6:
        v=a[1]; lo,hi=sorted([a[0],b[0]])
        HL,VL=cc.lineas(p,fitz.Rect(lo,v-W,hi,v+W))
        c=sorted(set((round(q,2),round(x0,1),round(x1,1)) for q,x0,x1 in HL if abs(q-v)<=W and min(x1,hi)-max(x0,lo)>=0.3*(hi-lo)))
        print(f"E{i} H y~{v} x[{lo},{hi}] :", c)
    else:
        v=a[0]; lo,hi=sorted([a[1],b[1]])
        HL,VL=cc.lineas(p,fitz.Rect(v-W,lo,v+W,hi))
        c=sorted(set((round(q,2),round(y0,1),round(y1,1)) for q,y0,y1 in VL if abs(q-v)<=W and min(y1,hi)-max(y0,lo)>=0.3*(hi-lo)))
        print(f"E{i} V x~{v} y[{lo},{hi}] :", c)
