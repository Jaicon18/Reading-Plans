import sys; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, json
its=[{"num":n,"sf":s} for n,s in [("401",443),("402",556),("403",521),("404",317),("405",427),("406",124),("412",1350)]]
r=cc.medir('A2.04',its)
for x in r:
  print({k:v for k,v in x.items() if k!='polygon'}, len(x.get('polygon') or []))
json.dump(r,open('/root/cr/work/etapas/4_canon/rev9/L4L1_a.json','w'))
cc.imagen('A2.04',[x for x in r if x.get('polygon')],'/root/cr/work/etapas/4_canon/img/rev9/L4L1_A204_auto.png')
