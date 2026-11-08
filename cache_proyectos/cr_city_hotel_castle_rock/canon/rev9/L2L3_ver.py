import sys, json, fitz
from PIL import Image, ImageDraw
W='/root/cr/work'
HS=list(json.load(open(f'{W}/set_texto.json'))['hojas'])
pdf=fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
def ver(sh, clip, fn, polys=(), baths=(), S=3, grid=20, labels=()):
    p=pdf[HS.index(sh)]; clip=fitz.Rect(*clip)
    pix=p.get_pixmap(matrix=fitz.Matrix(S,S),clip=clip)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    T=lambda x,y:((x-clip.x0)*S,(y-clip.y0)*S)
    if grid:
        import math
        x=math.ceil(clip.x0/grid)*grid
        while x<clip.x1:
            d.line([T(x,clip.y0),T(x,clip.y1)],fill=(0,200,0) if x%100 else (0,140,0),width=1); d.text(T(x+1,clip.y0+1),str(int(x)),fill=(0,120,0)); x+=grid
        y=math.ceil(clip.y0/grid)*grid
        while y<clip.y1:
            d.line([T(clip.x0,y),T(clip.x1,y)],fill=(0,200,0) if y%100 else (0,140,0),width=1); d.text(T(clip.x0+1,y+1),str(int(y)),fill=(0,120,0)); y+=grid
    for P in polys:
        Q=[T(*q) for q in P]; d.line(Q+[Q[0]],fill=(220,0,0),width=2)
    for P in baths:
        Q=[T(*q) for q in P]; d.line(Q+[Q[0]],fill=(0,90,255),width=2)
    for (x,y,t) in labels: d.text(T(x,y),t,fill=(220,0,0))
    im.save(fn)
if __name__=='__main__':
    sh=sys.argv[1]; cl=list(map(float,sys.argv[2:6])); fn=sys.argv[6]; S=float(sys.argv[7]) if len(sys.argv)>7 else 3
    g=float(sys.argv[8]) if len(sys.argv)>8 else 20
    ver(sh,cl,fn,S=S,grid=g)
