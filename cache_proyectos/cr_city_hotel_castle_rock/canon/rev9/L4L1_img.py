import sys, json; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc, fitz
from PIL import Image, ImageDraw
IMG='/root/cr/work/etapas/4_canon/img/rev9/'
def draw(sh, layers, fn, clip, S=2, page=None):
    p=cc.pdf[page-1] if page else cc.pdf[cc.HS.index(sh)]
    pix=p.get_pixmap(matrix=fitz.Matrix(S,S),clip=clip)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    for P,col,w,txt in layers:
        Q=[((x-clip.x0)*S,(y-clip.y0)*S) for x,y in P]
        d.line(Q+[Q[0]],fill=col,width=w)
        if txt:
            cx=sum(q[0] for q in Q)/len(Q); cy=sum(q[1] for q in Q)/len(Q)
            d.text((cx-40,cy+30),txt,fill=col)
    im.save(fn); print(fn, im.size)
d=json.load(open('L4L1_polys.json')); U=d['U']
A=lambda P: cc.area(P)/81
R=(220,0,0); B=(0,90,255); G=(0,150,0); O=(255,140,0)
lay=[]
for k,u in U.items():
    a=A(u['c']); b=A(u['b'])
    lay+= [(u['c'],R,3,f"{k} C={a:.1f} B={b:.1f} C-B={a-b:.1f} imp {u['imp']}"),(u['b'],B,2,None)]
lay+=[(d['chase405'],O,2,None),(d['c406'],R,3,f"406 {A(d['c406']):.1f} imp 124")]
draw('A2.04',lay,IMG+'L4L1_A204_unidades_401-406.png',fitz.Rect(520,335,1025,1090),S=2)
draw('A2.04',[(d['cor'],R,3,f"412 {A(d['cor']):.1f}"),(d['vrr'],R,3,f"vest {A(d['vrr']):.1f}"),(d['v410'],O,2,f"410/411 vest {A(d['v410']):.1f} (excl)")],IMG+'L4L1_A204_412_corridor.png',fitz.Rect(690,430,1500,1290),S=1.6)
draw('A2.04',[(d['st1'],R,3,f"STAIR1 {A(d['st1']):.2f}")],IMG+'L4L1_A204_lobby_stair.png',fitz.Rect(690,600,815,810),S=4)
draw('A2.04',[(d['st413'],R,3,f"413 {A(d['st413']):.2f}")],IMG+'L4L1_A204_SE_stair_413.png',fitz.Rect(1470,1170,1670,1290),S=4)
l=json.load(open('L4L1_l1polys.json'))
draw('A2.02',[(l['inn'],R,3,f"L2 plate inner {A(l['inn']):.1f}"),(l['out'],O,1,None),(l['st1'],B,3,None),(l['st2'],B,3,None),(l['hs'],G,3,None),(l['hl'],G,3,None)],IMG+'L4L1_A202_L1_FS1_placa.png',fitz.Rect(500,320,1800,1310),S=1.2)
dx,dy=13.7,18.66
T=lambda P:[(x+dx,y+dy) for x,y in P]
draw('A3.01',[(T(l['inn']),R,3,"L2 plate inner (A2.02 +13.7/+18.66)"),(T(l['st1']),B,3,None),(T(l['st2']),B,3,None),(T(l['hs']),G,3,None),(T(l['hl']),G,3,None)],IMG+'L4L1_A301_L1_FS1_placa.png',fitz.Rect(510,330,1810,1320),S=1.2)
# zooms de verificación de esquinas en A3.01
draw('A3.01',[(T(l['inn']),R,2,None),(T(l['st1']),B,2,None),(T(l['hs']),G,2,None)],IMG+'L4L1_A301_zoomNW.png',fitz.Rect(530,350,830,700),S=3)
draw('A3.01',[(T(l['inn']),R,2,None),(T(l['st2']),B,2,None)],IMG+'L4L1_A301_zoomSE.png',fitz.Rect(1480,1000,1800,1310),S=3)
