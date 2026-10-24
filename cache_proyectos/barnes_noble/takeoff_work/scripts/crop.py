import sys, pymupdf as fitz
# crop.py page x0 y0 x1 y1 (in 40dpi overview px) out [dpi]
pg=int(sys.argv[1]); x0,y0,x1,y1=map(float,sys.argv[2:6]); out=sys.argv[6]; dpi=int(sys.argv[7]) if len(sys.argv)>7 else 150
d=fitz.open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/bidset/bidset_SIN_MARKUPS.pdf')
f=72/40
d[pg-1].get_pixmap(dpi=dpi,clip=fitz.Rect(x0*f,y0*f,x1*f,y1*f)).save(out)
