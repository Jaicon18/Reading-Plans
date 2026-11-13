import pymupdf,numpy as np,json
from PIL import Image,ImageFilter
d=pymupdf.open('/tmp/claude-0/crset/CR_arch.pdf')
K=12.0; CLIP=pymupdf.Rect(0,520,1300,1560); IY,IX=33*4,48*4; zA=K/6.75
p=d[3]; pix=p.get_pixmap(matrix=pymupdf.Matrix(zA,zA),clip=CLIP,colorspace=pymupdf.csGRAY)
A=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width)
im=Image.fromarray(((A<70)*255).astype(np.uint8))
op=im.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
m=np.array(op)>0
for w in p.get_text('words'):
    r=pymupdf.Rect(w[:4])&CLIP
    if r.is_empty: continue
    x0,y0,x1,y1=[int((v-o)*zA) for v,o in zip(r,(CLIP.x0,CLIP.y0,CLIP.x0,CLIP.y0))]
    m[max(0,y0-3):y1+3,max(0,x0-3):x1+3]=False
ys,xs=np.nonzero(m); sel=(ys%4==0)&(xs%4==0)
pts=[((x+IX)/(K/9.0),(y+IY)/(K/9.0)) for y,x in zip(ys[sel],xs[sel])]
json.dump(pts,open('/tmp/claude-0/crset/rated_pts_A201.json','w')); print(len(pts))
Image.fromarray((m*255).astype(np.uint8)).resize((m.shape[1]//4,m.shape[0]//4)).save('/tmp/claude-0/crset/rated_mask.png')
