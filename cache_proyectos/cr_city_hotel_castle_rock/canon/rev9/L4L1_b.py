import sys; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, json
for G in (14,20,28):
  r=cc.medir('A2.04',[{"num":"412","sf":1350,"punto":[825,705]},{"num":"406","sf":124,"punto":[800,400]}],G=G)
  for x in r: print(G,{k:v for k,v in x.items() if k not in('polygon',)})
  if G==14: cc.imagen('A2.04',[x for x in r if x.get('polygon')],'/root/cr/work/etapas/4_canon/img/rev9/L4L1_412_auto.png')
