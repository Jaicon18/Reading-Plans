"""BE-GK02 extended: OCR layer for every sheet whose text layer is only the title block (< 700 chars): S / M / P / E sheets."""
import json, sys, os, concurrent.futures as cf
sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
os.environ['OMP_THREAD_LIMIT'] = '1'
import palabras_fitz as PF, pymupdf
W = '/root/gk/work'
H = json.load(open(f'{W}/set_texto.json'))['hojas']; sm = json.load(open(f'{W}/sheetmap.json'))
pages = sorted(sm[k] - 1 for k, v in H.items() if len(str(v)) < 700 and k in sm and sm[k] > 48)
wd = f'{W}/ocr_extra'; os.makedirs(wd, exist_ok=True)
src = f'{W}/plans/GK_set_OCR.pdf'
with cf.ProcessPoolExecutor(4) as ex:
    list(ex.map(PF.ocr_pagina, [src] * len(pages), pages, [wd] * len(pages)))
d = pymupdf.open(src)
n = PF.capa_ocr(d, pages, wd)
d.save(f'{W}/plans/GK_set_OCR2.pdf', garbage=3, deflate=True)
print(len(pages), 'pages', n, 'words')
