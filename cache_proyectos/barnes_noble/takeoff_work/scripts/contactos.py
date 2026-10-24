import sys, json, pymupdf as fitz, PIL.Image as I, PIL.ImageDraw as D
pdf, pno, js, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
d = fitz.open(pdf); p = d[pno-1]; R = json.load(open(js))
cells = []
for r in R:
    c = fitz.Rect(r['cx']-16, r['cy']-16, r['cx']+16, r['cy']+16)
    pix = p.get_pixmap(dpi=300, clip=c)
    im = I.frombytes('RGB', (pix.width, pix.height), pix.samples).resize((140, 140))
    cell = I.new('RGB', (150, 170), 'white'); cell.paste(im, (5, 25))
    D.Draw(cell).text((5, 5), f"id {r['id']}", fill=(255, 0, 0))
    cells.append(cell)
n = 8; rows = (len(cells)+n-1)//n
sheet = I.new('RGB', (150*n, 170*rows), 'white')
for i, c in enumerate(cells): sheet.paste(c, ((i % n)*150, (i//n)*170))
sheet.save(out)
