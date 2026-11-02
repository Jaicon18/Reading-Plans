import sys, pymupdf as fitz
# usage: crop.py page x0 y0 x1 y1 dpi out [rect x0,y0,x1,y1[,color]]...
doc=fitz.open('/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf')
p=int(sys.argv[1]); x0,y0,x1,y1=map(float,sys.argv[2:6]); dpi=int(sys.argv[6]); out=sys.argv[7]
d2=fitz.open(); d2.insert_pdf(doc,from_page=p-1,to_page=p-1); pg=d2[0]
cols={'r':(1,0,0),'b':(0,0,1),'g':(0,.6,0),'o':(1,.5,0),'m':(.8,0,.8)}
for spec in sys.argv[8:]:
    parts=spec.split(','); c=cols.get(parts[4] if len(parts)>4 else 'r')
    r=fitz.Rect(*map(float,parts[:4]))
    if len(parts)>5 and parts[5]=='e': pg.draw_oval(r,color=c,width=2)
    else: pg.draw_rect(r,color=c,width=1.5)
pg.get_pixmap(clip=fitz.Rect(x0,y0,x1,y1),dpi=dpi).save(out); print(out)
