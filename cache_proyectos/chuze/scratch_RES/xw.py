import json,sys
sys.path.insert(0,'.')
from proj import load,proj,match,C
A=load('A');B=load('B')
def m(ws):
    r={}
    for w in ws:
        pb=proj(w)
        for c in C:
            v=match(pb,c)
            if v>0.4 or (pb['ori']=='BOX' and v>0): r.setdefault(c['id'],[]).append((w['id'],w['tag'],w['length_ft'],round(v,2)))
    return r
ma,mb=m(A),m(B)
for c in C:
    print(c['id'],c['type'],c['length_ft'],'| A:',ma.get(c['id']),'| B:',mb.get(c['id']))
