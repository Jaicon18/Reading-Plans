"""BE-149 / U-153: /DepthUnit con /C 1/864 hacía que Bluebeam multiplicara el Wall Area x864.
Pone /C 1 (Depth guardado en ft) en todo markup con /Depth. Uso: in.pdf out.pdf"""
import sys, pikepdf
pdf = pikepdf.open(sys.argv[1]); n = 0
for page in pdf.pages:
    for a in page.obj.get('/Annots', []):
        du = a.get('/DepthUnit')
        if du is None: continue
        for nf in du:
            nf.C = 1
        n += 1
pdf.save(sys.argv[2]); print('markups corregidos', n)
