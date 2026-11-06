"""Copia del PDF de markups sin firmas digitales (sello visible conservado) y con Page Label = hoja en todas las páginas."""
import sys, json, pikepdf
from pikepdf import Name, Dictionary, Array

src, dst, inv = sys.argv[1], sys.argv[2], sys.argv[3]
extra = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
sheets = {x['page']: x['sheet'] for x in json.load(open(inv))['sheets']}
sheets.update({int(k): v for k, v in extra.items()})

pdf = pikepdf.open(src)
def es_firma(a):
    ft = a.get('/FT') or (a.get('/Parent') or {}).get('/FT')
    return ft == Name.Sig
quitadas = 0
for page in pdf.pages:
    annots = page.obj.get('/Annots')
    if not annots: continue
    keep = Array()
    for a in annots:
        if es_firma(a):
            ap = a.get('/AP'); n = ap.get('/N') if ap else None
            if n is not None and isinstance(n, pikepdf.Stream):
                r = [float(v) for v in a.Rect]
                page.add_overlay(n, pikepdf.Rectangle(*r))
            quitadas += 1
        else:
            keep.append(a)
    page.obj.Annots = keep
af = pdf.Root.get('/AcroForm')
if af is not None:
    f = Array([x for x in af.get('/Fields', []) if not es_firma(x)])
    if len(f): af.Fields = f; 
    else: del pdf.Root['/AcroForm']
    if '/AcroForm' in pdf.Root and '/SigFlags' in pdf.Root.AcroForm: del pdf.Root.AcroForm['/SigFlags']
for k in ('/Perms',):
    if k in pdf.Root: del pdf.Root[k]
nums = Array()
for i in range(len(pdf.pages)):
    lab = sheets.get(i + 1) or ('LEGEND' if i == len(pdf.pages) - 1 else str(i + 1))
    nums.append(i); nums.append(Dictionary(P=pikepdf.String(lab)))
pdf.Root.PageLabels = Dictionary(Nums=nums)
pdf.save(dst)
print('firmas quitadas', quitadas)

# Uso: python3 -I quitar_firmas_labels.py <markups.pdf> <salida.pdf> <inventario.json> ['{"pagina":"HOJA",...}']
# Chequeo (U-151): la salida debe dar 0 campos /Sig, sin /SigFlags y Page Labels únicos = número de páginas.
