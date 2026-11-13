import sys,pymupdf,importlib.util,collections
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); sys.path.insert(0,p.rsplit('/',1)[0]); s.loader.exec_module(m); sys.path.pop(0); return m
C=load(sys.argv[1],'c8')
orig=C._cob_divisor_tag; reg_=[]
cur={}
def wrap(f,pal,esc,todas=()):
    r=orig(f,pal,esc,todas)
    if r:
        rama='2lados' if orig(f,pal,esc,()) else 'encerrada'
        reg_.append((cur['lab'],f['x'],f['y'],rama,round(f['d']/esc*12,1),f['largo_ft'],f['cubierto']))
    return r
C._cob_divisor_tag=wrap
doc=pymupdf.open('/tmp/claude-0/crmk/CR_mk.pdf')
for pg in doc:
    es,_=C.cob_tipo_hoja(doc,pg); esc=C.cob_escala(doc,pg) if es else None
    if not esc: continue
    cur['lab']=pg.get_label()
    segs,exc,clg=C._cob_markups(doc,pg); e=C.cob_estilos_muro(pg.get_drawings(),segs,esc) or C.cob_estilos_pares(pg.get_drawings(),esc)
    reg=C._cob_region(pg,segs,exc,clg,esc)
    C.cob_diag_cortos(pg,esc,segs,reg,estilos=e)
nc=[r for r in reg_ if not r[6]]
print('divisor_tag no cubiertos:',len(nc), collections.Counter(r[3] for r in nc))
for r in sorted(nc,key=lambda r:(r[3],r[4])): print(r)
