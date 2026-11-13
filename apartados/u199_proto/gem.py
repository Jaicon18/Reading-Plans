import json,re,sys,collections
sys.path.insert(0,'/tmp/v135/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE
RXN=re.compile(r"(?<![\w.'/-])(\d{3,4})[A-Z]?(?![\w'\"/-])")
STOP={"L1","L2","L3","L4","L5","FACES","WALL","WALLS","SIDE","NORTH","SOUTH","EAST","WEST","AND","AT","OF","THE","BETWEEN","DOOR","STUB","SEE","NOTE","INSIDE","FACE","END"}
def cuartos(w):
    txt=str(w.get('location') or '')
    m=re.search(r'(?i)faces?:(.*)$',txt); txt=m.group(1) if m else txt
    out=set()
    for ch in re.split(r'[;|,]',txt):
        nums=RXN.findall(ch)
        words=[x.upper() for x in re.findall(r"[A-Za-z][A-Za-z&]{2,}",ch) if x.upper() not in STOP]
        for n in nums:
            out.add(n[-2:])
    return out
def gem(can):
    por={}
    for w in CE.muros_canon(can):
        p=CE._piso(w)
        if p is None: continue
        cs=frozenset(cuartos(w))
        if not cs: continue
        por.setdefault(p,[]).append((str(w.get('type_id') or '').split('-')[0],cs,w['id']))
    rooms={p:set().union(*[c for _,c,_ in ws]) for p,ws in por.items()}
    nom={}
    for w in CE.muros_canon(can):
        p=CE._piso(w)
        if p is None: continue
        for ch in re.split(r'[;|,/]',str(w.get('location') or '')):
            ws_=[x.upper()[:5] for x in re.findall(r"[A-Za-z][A-Za-z&]{2,}",ch) if x.upper() not in STOP]
            for n in RXN.findall(ch):
                if ws_: nom.setdefault(p,set()).add((n[-2:],ws_[0]))
    ev=[];n=0
    ps=sorted(por)
    for i,a in enumerate(ps):
        for b in ps[i+1:]:
            ra,rb=rooms[a],rooms[b]
            na,nb=nom.get(a,set()),nom.get(b,set())
            com=len(na&nb)/max(1,min(len(na),len(nb)))
            if com<0.6: continue
            for x,y in((a,b),(b,a)):
                for t,cs,wid in por[x]:
                    if not cs<=rooms[y]: continue
                    n+=1
                    if any(t2==t and (cs<=c2 or c2<=cs) for t2,c2,_ in por[y]): continue
                    ev.append((x,y,wid,t,sorted(cs)))
    return ev,n,{(a,b):round(len(nom.get(a,set())&nom.get(b,set()))/max(1,min(len(nom.get(a,set())),len(nom.get(b,set())))),2) for i,a in enumerate(ps) for b in ps[i+1:]}
for p in sys.argv[1:]:
    can=json.load(open(p)); ev,n,cm=gem(can)
    print(p.split('/')[-1],'eval',n,'hall',len(ev),cm)
    for e in ev[:40]: print('  ',e)
    print('  UNTYPED-L2-12 hallado:',any(e[2]=='UNTYPED-L2-12' for e in ev))
