import fitz, json, sys
p=fitz.open('/root/cr/work/plans/bidset_SIN_MARKUPS.pdf')[69]
segs=[]
for d in p.get_drawings():
  if abs((d.get('width') or 0)-0.48)>0.01: continue
  for it in d['items']:
    if it[0]=='l':
      a,b=it[1],it[2]
      if all(1540<q.x<2100 and 603<q.y<743 for q in (a,b)): segs.append(((round(a.x,2),round(a.y,2)),(round(b.x,2),round(b.y,2))))
# chain
from collections import defaultdict
adj=defaultdict(list)
for a,b in segs: adj[a].append(b); adj[b].append(a)
start=min(adj,key=lambda q:(q[0],q[1]))
ring=[start]; prev=None; cur=start
while True:
  nx=[q for q in adj[cur] if q!=prev]
  if not nx: break
  prev,cur=cur,nx[0]
  if cur==start: break
  ring.append(cur)
  if len(ring)>2000: break
A=abs(sum(ring[i][0]*ring[(i+1)%len(ring)][1]-ring[(i+1)%len(ring)][0]*ring[i][1] for i in range(len(ring))))/2
print(len(segs),len(ring),A, min(q[0] for q in ring),max(q[0] for q in ring),min(q[1] for q in ring),max(q[1] for q in ring))
json.dump(ring,open(sys.argv[1],'w'))
