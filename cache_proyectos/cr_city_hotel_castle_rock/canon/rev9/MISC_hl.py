import sys, fitz
# lista lineas H/V largas (>=ml) dentro de R; agrupa duplicados por coordenada redondeada a 0.5
pg=int(sys.argv[1]); R=fitz.Rect(*map(float,sys.argv[2:6])); ml=float(sys.argv[6])
p=fitz.open('/root/cr/work/plans/bidset_SIN_MARKUPS.pdf')[pg-1]
H={};V={}
for d in p.get_drawings():
  for it in d['items']:
    segs=[]
    if it[0]=='l': segs=[(it[1],it[2])]
    elif it[0]=='re':
      r=it[1]; segs=[(fitz.Point(r.x0,r.y0),fitz.Point(r.x1,r.y0)),(fitz.Point(r.x0,r.y1),fitz.Point(r.x1,r.y1)),(fitz.Point(r.x0,r.y0),fitz.Point(r.x0,r.y1)),(fitz.Point(r.x1,r.y0),fitz.Point(r.x1,r.y1))]
    for a,b in segs:
      if abs(a.y-b.y)<0.3 and abs(a.x-b.x)>=ml and R.y0<=a.y<=R.y1 and max(a.x,b.x)>R.x0 and min(a.x,b.x)<R.x1:
        k=round(a.y,2); lo,hi=min(a.x,b.x),max(a.x,b.x); o=H.get(k); H[k]=(min(lo,o[0]),max(hi,o[1])) if o else (lo,hi)
      if abs(a.x-b.x)<0.3 and abs(a.y-b.y)>=ml and R.x0<=a.x<=R.x1 and max(a.y,b.y)>R.y0 and min(a.y,b.y)<R.y1:
        k=round(a.x,2); lo,hi=min(a.y,b.y),max(a.y,b.y); o=V.get(k); V[k]=(min(lo,o[0]),max(hi,o[1])) if o else (lo,hi)
print('H',' '.join(f'{k}[{v[0]:.0f}-{v[1]:.0f}]' for k,v in sorted(H.items())))
print('V',' '.join(f'{k}[{v[0]:.0f}-{v[1]:.0f}]' for k,v in sorted(V.items())))
