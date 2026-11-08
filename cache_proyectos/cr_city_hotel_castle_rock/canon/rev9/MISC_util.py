import sys, json, fitz
from PIL import Image, ImageDraw
W='/root/cr/work'
HS=list(json.load(open(f'{W}/set_texto.json'))['hojas'])
pdf=fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
def page(sh): return pdf[HS.index(sh)]
def area(P): return abs(sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P))))/2
def img(sh, polys, fn, clip, S=3, lines=(), blue=(), txt=None):
    p=page(sh); clip=fitz.Rect(*clip)
    pix=p.get_pixmap(matrix=fitz.Matrix(S,S),clip=clip)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    T=lambda q:((q[0]-clip.x0)*S,(q[1]-clip.y0)*S)
    for P in polys:
        Q=[T(q) for q in P]; d.line(Q+[Q[0]],fill=(230,0,0),width=3)
    for P in blue:
        Q=[T(q) for q in P]; d.line(Q+[Q[0]],fill=(0,90,255),width=2)
    for a,b in lines: d.line([T(a),T(b)],fill=(230,0,0),width=4)
    if txt: d.text((10,10),txt,fill=(230,0,0))
    im.save(fn); print(fn, im.size)
def words(sh, R, pat=None):
    p=page(sh); out=[]
    for w in p.get_text('words'):
        if fitz.Rect(w[:4]).intersects(fitz.Rect(*R)) and (pat is None or pat.lower() in w[4].lower()): out.append((round(w[0],1),round(w[1],1),round(w[2],1),round(w[3],1),w[4]))
    return out
if __name__=='__main__':
    sh=sys.argv[1]; clip=list(map(float,sys.argv[2:6])); fn=sys.argv[6]; S=float(sys.argv[7]) if len(sys.argv)>7 else 3
    img(sh,[],fn,clip,S)
