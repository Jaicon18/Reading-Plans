import sys, json, re
sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc
c=cc.c
out={}
for fl,sh in (('L2','A2.02'),('L3','A2.03')):
    its=[]
    for x in c['ceilings']:
        if x.get('floor')!=fl: continue
        m=re.search(r'\b([1-4]\d\d)\b',x['room'])
        mm=re.search(r'(\d+) SF"? ?\)?',x['source'])
        mm=re.search(r'printed[^"]*"(?:\d+ / )?(\d+) SF"',x['source']) or re.search(r'"(?:\d+ / )?(\d+) SF"',x['source'])
        its.append({"num":m.group(1),"sf":float(mm.group(1)) if mm else float(x['area_sf']),"room":x['room'],"cargado":x['area_sf']})
    res=cc.medir(sh,its)
    for r in res: out[r['room']]=r; print(r['num'],r['sf'],r.get('area_sf'),r.get('bath_sf'),r.get('estado'),r.get('n_bordes'))
    p=cc.pdf[cc.HS.index(sh)]; print(sh,p.rect)
    cc.imagen(sh,[r for r in res if r.get('polygon')],f'/root/cr/work/etapas/4_canon/img/rev9/L2L3_auto_{fl}.png')
json.dump(out,open('/root/cr/work/etapas/4_canon/rev9/L2L3_auto.json','w'),indent=1)
