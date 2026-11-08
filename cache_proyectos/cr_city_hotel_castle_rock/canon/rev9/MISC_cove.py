import fitz, json, sys
pg=int(sys.argv[1]); R=fitz.Rect(*map(float,sys.argv[2:6])); gap=float(sys.argv[6]) if len(sys.argv)>6 else 3.36
p=fitz.open('/root/cr/work/plans/bidset_SIN_MARKUPS.pdf')[pg-1]
H=[];V=[]
for d in p.get_drawings():
  if abs((d.get('width') or 0)-0.24)>0.01: continue
  for it in d['items']:
    if it[0]!='l': continue
    a,b=it[1],it[2]
    if not (R.contains(a) and R.contains(b)): continue
    if abs(a.y-b.y)<0.05 and abs(a.x-b.x)>1: H.append((round(a.y,2),min(a.x,b.x),max(a.x,b.x)))
    if abs(a.x-b.x)<0.05 and abs(a.y-b.y)>1: V.append((round(a.x,2),min(a.y,b.y),max(a.y,b.y)))
def merge(L):
  from collections import defaultdict
  g=defaultdict(list)
  for k,lo,hi in L: g[k].append([lo,hi])
  out=[]
  for k,iv in g.items():
    iv.sort(); cur=iv[0][:]
    for lo,hi in iv[1:]:
      if lo<=cur[1]+0.6: cur[1]=max(cur[1],hi)
      else: out.append((k,cur[0],cur[1])); cur=[lo,hi]
    out.append((k,cur[0],cur[1]))
  return out
def pairs(L):
  L=merge(L); res=[]
  for k,lo,hi in L:
    for k2,lo2,hi2 in L:
      if abs(k2-k-gap)<0.12:
        a,b=max(lo,lo2),min(hi,hi2)
        if b-a>15: res.append((k,k2,round(a,2),round(b,2)))
  return res
ph=pairs(H); pv=pairs(V)
tot=0
for k,k2,a,b in ph: print('H',k,k2,a,b,round(b-a,2)); tot+=b-a
for k,k2,a,b in pv: print('V',k,k2,a,b,round(b-a,2)); tot+=b-a
print('total pt',round(tot,2),'LF@9',round(tot/9,2))
json.dump({'H':ph,'V':pv},open(sys.argv[7] if len(sys.argv)>7 else '/dev/null','w'))
