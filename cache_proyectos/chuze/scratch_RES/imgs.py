import json,sys,pymupdf as fitz
sys.path.insert(0,'/tmp/chuze/scratch/RES'); sys.path.insert(0,'/tmp/chuze/scratch/CIERRE')
from proj import load,proj,C
from T import T
OUT='/tmp/chuze/work/etapas/3_revision/img_res/'
doc=fitz.open('/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf')
A={w['id']:w for w in load('A')}; B={w['id']:w for w in load('B')}
CC={c['id']:c for c in C}
canon={w['id']:w for w in json.load(open('/tmp/chuze/work/etapas/4_canon/takeoff_canon.json'))['walls']}
col={'A':(0,0,1),'B':(1,.5,0),'K':(0,.6,0),'R':(1,0,0)}
def rect_of(pb):
    if pb['ori']=='H': return fitz.Rect(pb['lo'],pb['c0'],pb['hi'],pb['c1'])
    if pb['ori']=='V': return fitz.Rect(pb['c0'],pb['lo'],pb['c1'],pb['hi'])
    return fitz.Rect(pb['x0'],pb['y0'],pb['x1'],pb['y1'])
def a101(item,cids,aids=(),bids=(),kids=(),pad=25,title=''):
    d=fitz.open(); d.insert_pdf(doc,from_page=13,to_page=13); pg=d[0]; U=None
    for i in aids: r=rect_of(proj(A[i])); pg.draw_rect(r+(-1,-1,1,1),color=col['A'],width=1.2); U=r if U is None else U|r
    for i in bids: r=rect_of(proj(B[i])); pg.draw_rect(r+(-2.5,-2.5,2.5,2.5),color=col['B'],width=1.0,dashes='[2] 0'); U=r if U is None else U|r
    for i in kids:
        w=canon[i]; b=w['band']; s=b['sheet']; p,k,dx,dy=T[s]
        pb=proj({'band':b,'sheet':s}); r=rect_of(pb); pg.draw_rect(r+(-4,-4,4,4),color=col['K'],width=1.0); U=r if U is None else U|r
    for i in cids:
        cb=CC[i]['band']; r=rect_of(dict(cb)); pg.draw_oval(r+(-7,-7,7,7),color=col['R'],width=1.5); U=r if U is None else U|r
    U=U+(-pad,-pad,pad,pad)
    pg.insert_text((U.x0+2,U.y0+8),f'{item} {title}  [red=A101 closure C-n, blue=A, orange=B, green=canon]',fontsize=5,color=(1,0,0))
    pg.get_pixmap(clip=U,dpi=300).save(OUT+item+'.png')
def sheet(item,page,clip,marks,title='',dpi=150):
    d=fitz.open(); d.insert_pdf(doc,from_page=page-1,to_page=page-1); pg=d[0]
    for r,cc,shape in marks:
        R=fitz.Rect(*r)
        if shape=='o': pg.draw_oval(R,color=col[cc],width=2)
        else: pg.draw_rect(R,color=col[cc],width=1.5)
    cl=fitz.Rect(*clip); pg.insert_text((cl.x0+3,cl.y0+10),f'{item} {title}',fontsize=8,color=(1,0,0))
    pg.get_pixmap(clip=cl,dpi=dpi).save(OUT+item+'.png')
a101('R-01',['C-14'],['A-A421-6','A-A429-8'],['B-A421-1','B-A429-9'],title='C-14 A6D counted on A421 and A429')
a101('R-02',['C-15','C-16'],['A-A421-7','A-A429-9','A-A421-8','A-A429-10'],['B-A421-2','B-A429-10'],pad=40,title='C-15/C-16 A6D stubs double')
a101('R-04',['C-37'],['A-A435-4','A-A426-4'],['B-A435-4','B-A426-5'],title='C-37 A6D on A435 and A426')
a101('R-05',['C-48'],['A-A423-5','A-A424-4'],['B-A423-5','B-A424-4'],title='C-48 A6D infill on A423 and A424')
a101('R-06',['C-17','C-18'],['A-A421-1','A-A421-2','A-A427-4','A-A427-5'],['B-A421-4','B-A421-5'],pad=30,title='C3C boxes on A421 and A427')
sheet('R-07',22,(1120,980,1480,1080),[((1173.4,1022.6,1227.4,1038.5),'K','r'),((1374,1022.6,1428,1038.5),'K','r'),((1165,1005,1236,1046),'R','o'),((1366,1005,1437,1046),'R','o')],title='C3C U boxes: S face 3-0 printed + legs; N face = A6D')
sheet('R-08',43,(450,1850,1750,2120),[((513.6,1892.6,1517.8,1903.4),'A','r'),((514,1895,1465,1901),'B','r'),((1260,1960,1340,2000),'R','o'),((80,1960,1340,2000),'R','o')],title='C-2 A6D: printed 44-9 (A427) + A421 8-1 1/2 + 3-0 + 5-0',dpi=110)
sheet('R-09',42,(1270,820,1840,1310),[((1420,1000,1580,1240),'R','o')],title='A426.A elev 3 ENTRY NORTH: wall continues above the 6-6 opening -> A3C runs through (A 21.00)',dpi=100)
a101('R-10',['C-29'],['A-A422-1'],['B-A422-1'],pad=20,title='C-29 A6D through window + door 122 (A=closure)')
sheet('R-11',48,(700,480,1480,900),[((790,640,920,820),'R','o')],title='5/A429.A: D6F continues above the 8-0 opening to EL+12-0 -> one wall 16-11',dpi=110)
sheet('R-12',52,(2480,1250,2700,1720),[((2585.5,1330.3,2591.0,1665.4),'K','r'),((2590.3,1330.3,2613.1,1335.1),'K','r'),((2590.3,1660.6,2613.8,1665.4),'K','r'),((2560,1310,2640,1690),'R','o')],title='D3G locker bank 2 (A432) - counted by nobody',dpi=140)
a101('R-13',['C-64'],[],['B-A423-9'],['A-A423-10'],title='B2E C-64 only in B')
sheet('R-14',33,(1640,1790,1810,1870),[((1692.5,1813.2,1781.8,1819.7),'K','r'),((1692.5,1819.7,1700.2,1851.4),'K','r'),((1680,1800,1795,1860),'R','o')],title='A424-5: H 4.96 + return to existing wall 1.76 = 6.72',dpi=250)
sheet('R-15',33,(1450,1860,1720,1925),[((1676.6,1875.4,1682.2,1912.8),'K','r'),((1682.2,1875.4,1692.5,1880.9),'K','r'),((1488.2,1875.4,1493.5,1912.8),'A','r'),((1665,1868,1700,1920),'R','o')],title='east lav wing L 2.65 (only B) - mirror of A-A424-13',dpi=250)
a101('R-16',['C-76'],['A-A423-6','A-A425-6'],['B-A423-7','B-A425-6'],title='C-76 Women Janitor east wall on A423 and A425')
sheet('R-17',30,(300,1520,420,1900),[((362,1743,374,1749),'R','r'),((362,1555,374,1560),'R','r'),((340,1730,395,1760),'R','o')],title='A423 tag C3D PT0130 on the vanity end cap (full cap drawn on A425)',dpi=170)
a101('R-18',['C-69'],['A-A101-1'],[],pad=30,title='door 141 wall: only A, untagged')
a101('R-19',['C-78'],['A-A434-1'],['B-A434-1'],pad=30,title='A2.25 infill: type not printed')
sheet('R-25',49,(560,1590,800,1650),[((590,1600,760,1640),'R','o')],title='only PRINTED deck value: EL.+22-10 on 6/A429.B; elsewhere B.O. DECK VARIOUS',dpi=200)
sheet('R-25b',40,(1000,970,1180,1010),[((1040,975,1170,1008),'R','o')],title='A425.C: B.O. DECK VARIOUS (22-10 / 22-5 hidden, not printed)',dpi=200)
a101('R-22',['C-33'],['A-A431-2'],['B-A431-2'],pad=20,title='C-33 C3D 4in gap inside the run')
a101('R-27',['C-19','C-20'],['A-A421-9','A-A421-10'],['B-A421-9','B-A421-10'],pad=25,title='check-in 3-0 gap: all readings split')
a101('R-03',['C-34'],['A-A435-1','A-A426-1'],['B-A435-1','B-A426-1','B-A426-2'],pad=20,title='C-34 A3C: B double counted 33.21 in B-A426-1')
a101('R-20',['C-12','C-13'],['A-A429-11'],['B-A429-12','B-A429-13'],pad=20,title='D6G with return')
a101('R-23',['C-54','C-55'],['A-A424-12'],['B-A424-9'],pad=25,title='ADA stall wall + return')
a101('R-24',['C-51','C-52'],['A-A424-10'],['B-A424-7'],pad=25,title='C3D furring + return')
a101('R-21',['C-24'],['A-A421-14'],['B-A421-15'],pad=20,title='PT0080 line counted once on A421')
a101('R-26',['C-45','C-46','C-47','C-62'],[],[],pad=40,title='wet rooms: MR behind fixtures only')
print('ok')
