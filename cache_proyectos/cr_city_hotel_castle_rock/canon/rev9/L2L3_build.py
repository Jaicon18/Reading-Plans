import sys, json, re; sys.path.insert(0,'.'); sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, fitz
from PIL import Image, ImageDraw, ImageFont
from L2L3_poly import L2, area
from L2L3_l3 import L3
IMG='/root/cr/work/etapas/4_canon/img/rev9/'
c=cc.c
rooms={}
for x in c['ceilings']:
    if x.get('floor') in ('L2','L3'):
        n=re.search(r'\b([23]\d\d)\b',x['room']).group(1)
        m=re.search(r'printed[^"]*"(?:\d+ / )?(\d+) SF"',x['source']) or re.search(r'"(?:\d+ / )?(\d+) SF"',x['source'])
        rooms[n]=dict(room=x['room'],cargado=x['area_sf'],impreso=float(m.group(1)) if m else None)
# L3: lobby 317 = lobby + vestibulo (310/311); 318 sin vestibulo
v318=L3['318']['p']
vest=[[709.92,1075.32],[755.28,1075.32],[755.28,1098.48],[799.08,1098.48],[799.08,1138.2],[709.92,1138.2]]
L3['318']=dict(L3['318'],p=[q for q in v318 if q[0]>=799.0],m=L3['318']['m'].replace(" + vestíbulo de 210 709.92-799.2 x 1075.32/1098.48-1138.2 (shaft 755.28-799.2 fuera)"," (el vestíbulo de 310/311 va en lobby 317)"))
L3['317']=dict(L3['317'],p=None,polys=[[[709.92,1007.64],[799.08,1007.64],[799.08,1069.68],[709.92,1069.68]],vest],
   m="lobby 709.92-799.08 x 1007.64-1069.68 (abierto al corridor en 799.08) + vestíbulo de entrada a 310/311 709.92-799.08 x 1075.32-1138.2 menos shaft 755.28-799.08 x 1075.32-1098.48; el impreso 132 parece incluir el muro 1069.68-1075.32 entre ambos")
L3['316']['m']=L2['216']['m'].replace('A3.02 999.0 - 19.5','A3.03, mismo layout que L2')
out={}; rows=[]
def mk(fl,k,v,sh):
    r=rooms[k]; polys=v.get('polys') or [v['p']]
    A=sum(area(P) for P in polys)/81-(area(v['hole'])/81 if v.get('hole') else 0)
    B=area(v['b'])/81 if v.get('b') else 0.0
    S=r['impreso']; C=r['cargado']
    if S:
        ei=(A-S)/S; ee=(A-B-S)/S if B else None
        if ee is not None and abs(ee)<=0.02: cq,er='impreso excl. bath',ee
        elif abs(ei)<=0.02: cq,er='impreso incl. bath' if B else 'impreso',ei
        else: cq,er='NO CUADRA', (ee if ee is not None and abs(ee)<abs(ei) else ei)
    else:
        ei=(A-C)/C; cq,er=('cargado' if abs(ei)<=0.02 else 'NO CUADRA'),ei
    d={"sheet":sh}
    if v.get('polys'): d["polygons"]=[[[round(x,2),round(y,2)] for x,y in P] for P in polys]
    else: d["polygon"]=[[round(x,2),round(y,2)] for x,y in v['p']]
    if v.get('hole'): d["hueco_restado"]=v['hole']
    d.update({"area_sf":round(A,2),"bath":[[round(x,2),round(y,2)] for x,y in v['b']] if v.get('b') else None,"bath_sf":round(B,2),
      "contorno_menos_bath_sf":round(A-B,2),"sf_cargado":C,"sf_impreso":S,"cuadra_con":cq,"err_pct":round(100*er,2),
      "metodo":"caras [DERIVADO] área = shoelace(pt²)/81: "+v['m']+(("; ajustes A2.03: "+", ".join(v['log'])) if v.get('log') else ""),
      "nhoja":"1/"+sh,"img":IMG+f"L2L3_{fl}_{'W' if (k[1:] in ('10','11','12','13','14','15','16','17','21') ) else 'E'}.png","nota":""})
    out[r['room']]=d; return d
for k,v in L2.items(): mk('L2',k,v,'A2.02')
for k,v in L3.items(): mk('L3',k,v,'A2.03')
# corridors/lobbies: imagen propia
for k in ('L2 Corridor 216','L2 Corridor 218','L2 Lobby 217','L3 Corridor 316','L3 Corridor 318','L3 Lobby 317','L2 Elec 221','L2 Linen 222','L2 Cleaning 223','L3 ELEC 321','L3 322 Linen','L3 323 Cleaning','L2 Cleaning 215','L3 315 Cleaning'):
    out[k]['img']=IMG+('L2L3_L2_circ.png' if k.startswith('L2') else 'L2L3_L3_circ.png')
json.dump(out,open('/root/cr/work/etapas/4_canon/rev9/contornos_L2L3.json','w'),indent=1,ensure_ascii=False)
# imágenes
F=ImageFont.load_default()
def img(sh,fn,clip,keys,S=2.2):
    p=cc.pdf[cc.HS.index(sh)]; clip=fitz.Rect(*clip)
    pix=p.get_pixmap(matrix=fitz.Matrix(S,S),clip=clip); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    T=lambda x,y:((x-clip.x0)*S,(y-clip.y0)*S)
    for k in keys:
        v=out[k]
        for P in (v.get('polygons') or [v['polygon']]):
            Q=[T(*q) for q in P]; d.line(Q+[Q[0]],fill=(220,0,0),width=3)
        if v.get('hueco_restado'):
            Q=[T(*q) for q in v['hueco_restado']]; d.line(Q+[Q[0]],fill=(220,0,0),width=2)
        if v.get('bath'):
            Q=[T(*q) for q in v['bath']]; d.line(Q+[Q[0]],fill=(0,90,255),width=2)
        P=(v.get('polygons') or [v['polygon']])[0]; cx=sum(q[0] for q in P)/len(P); cy=sum(q[1] for q in P)/len(P)
        n=re.search(r'\b([23]\d\d)\b',k).group(1)
        t=f"{n}: {v['area_sf']} / -bath {v['contorno_menos_bath_sf']} | imp {v['sf_impreso']} carg {v['sf_cargado']}"
        x,y=T(cx,cy); d.rectangle([x-5,y+28,x+6.2*len(t),y+42],fill=(255,255,220)); d.text((x,y+30),t,fill=(200,0,0),font=F)
    im.save(fn)
for fl,sh in (('L2','A2.02'),('L3','A2.03')):
    ks=[k for k in out if out[k]['sheet']==sh]
    units=lambda s:[k for k in ks if re.search(r'room (\d+)',k) and re.search(r'room (\d+)',k).group(1)[1:] in s]
    img(sh,IMG+f'L2L3_{fl}_W.png',(525,340,1075,1285),units(('01','02','03','04','05','10','11','12','13','14')),S=2.0)
    img(sh,IMG+f'L2L3_{fl}_E.png',(1055,990,1775,1290),units(('06','07','08','09')),S=2.2)
    img(sh,IMG+f'L2L3_{fl}_circ.png',(700,340,1600,1285),[k for k in ks if not re.search(r'room',k)],S=2.0)
for k,v in out.items():
    print(f"{k:28s} {v['area_sf']:8} {v['bath_sf']:7} {v['contorno_menos_bath_sf']:8} carg {v['sf_cargado']:7} imp {v['sf_impreso']!s:6} {v['cuadra_con']:20s} {v['err_pct']}")
