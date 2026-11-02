import json,sys
sys.path.insert(0,'/tmp/chuze/scratch/RES')
from proj import load,proj,match,C
A=load('A');B=load('B')
K=json.load(open('/tmp/chuze/work/etapas/4_canon/takeoff_canon.json'))['walls']
K=[w for w in K if w.get('element')!='soffit_side']
def m(ws):
    r={}
    for w in ws:
        pb=proj(w)
        for c in C:
            v=match(pb,c)
            if (pb['ori']=='BOX' and v>0 and c['type']=='C3C') or (pb['ori']!='BOX' and v>0.4 and (v>=0.3*c['length_ft'] or v>=0.9*min(c['length_ft'],(pb['hi']-pb['lo'])/6.75))):
                r.setdefault(c['id'],[]).append({'id':w['id'],'type':w['tag'],'length_ft':w['length_ft'],'overlap_ft':round(v,2)})
    return r
ma,mb,mk=m(A),m(B),m(K)
OV={ # manual status (resolucion items)
 'C-2':('DIFF','R-08'),'C-8':('DIFF','R-11'),'C-9':('DIFF','R-11'),'C-12':('OK','R-20'),'C-13':('OK','R-20'),
 'C-14':('DOUBLE_A+DOUBLE_B','R-01'),'C-15':('DOUBLE_A+DOUBLE_B','R-02'),'C-16':('DOUBLE_A+DOUBLE_B','R-02'),
 'C-17':('DOUBLE_A (C3C) / DIFF basis','R-06,R-07'),'C-18':('DOUBLE_A (C3C) / DIFF basis','R-06,R-07'),
 'C-29':('DIFF','R-10'),'C-33':('OK (<2%)','R-22'),'C-34':('DOUBLE_B / DIFF','R-03,R-09'),'C-37':('DOUBLE_A+DOUBLE_B','R-04'),
 'C-38':('DIFF basis (A=B 4.67 vs closure centerline)','R-07'),'C-39':('DIFF basis (A=B 4.67 vs closure centerline)','R-07'),
 'C-48':('DOUBLE_A+DOUBLE_B','R-05'),'C-51':('OK (return inside A-A424-10)','R-24'),'C-52':('OK','R-24'),
 'C-53':('OK (closure UNTYPED; A=B A6D)','R-23'),'C-54':('DIFF (B +0.49)','R-23'),'C-55':('OK (return inside A-A424-12)','R-23'),
 'C-56':('DIFF','R-14'),'C-57':('DIFF','R-14'),'C-58':('ONLY_B (A typed it inside A-A424-5) / closure UNTYPED','R-15'),
 'C-59':('OK (closure UNTYPED)','R-15'),'C-60':('ONLY_B / closure UNTYPED','R-15'),'C-61':('ONLY_B / closure UNTYPED','R-15'),
 'C-64':('ONLY_B','R-13'),'C-69':('ONLY_A (closure UNTYPED)','R-18'),'C-71':('DOUBLE_A+DOUBLE_B / type','R-17'),'C-72':('DOUBLE_A+DOUBLE_B / type','R-17'),
 'C-73':('DOUBLE_A+DOUBLE_B / type','R-17'),'C-74':('DOUBLE_A+DOUBLE_B / type','R-17'),'C-75':('OK (closure UNTYPED; A=B A3C)','RFI-22'),
 'C-76':('DOUBLE_A+DOUBLE_B','R-16'),'C-77':('DIFF basis','R-07'),'C-78':('DIFF type (closure UNTYPED)','R-19'),
 'C-82':('GAP','R-12'),'C-83':('GAP','R-12'),'C-84':('GAP','R-12'),'C-19':('OK','R-27'),'C-20':('OK','R-27'),'C-24':('OK','R-21'),
}
out=[]
for c in C:
    a=ma.get(c['id'],[]); b=mb.get(c['id'],[]); k=mk.get(c['id'],[])
    st,it=OV.get(c['id'],(None,None))
    if st is None:
        la=sum(x['overlap_ft'] for x in a if x['type']==c['type'] or c['type']=='UNTYPED'); lb=sum(x['overlap_ft'] for x in b if x['type']==c['type'] or c['type']=='UNTYPED')
        st='OK' if a and b else ('ONLY_A' if a else ('ONLY_B' if b else 'GAP'))
    out.append({'closure_id':c['id'],'closure_type':c['type'],'closure_lf':c['length_ft'],'room':c['room'],'closure_band_A101':c['band'],
                'A':a,'B':b,'canon':k,'status':st,'resolution_item':it})
summary={'closure_walls':len(C),'status_counts':{}}
for o in out: summary['status_counts'][o['status']]=summary['status_counts'].get(o['status'],0)+1
json.dump({'method':'A and B bands projected to A101 with the closure registration (scratch/CIERRE/T.py: A101 = k*sheet + (dx,dy)); match = same orientation, axis within 4 pt (A101), extent overlap; BOX by footprint overlap. overlap_ft = shared extent on A101 / 6.75. canon = reconciled 4_canon/takeoff_canon.json walls projected the same way.','summary':summary,'crosswalk':out},
          open('/tmp/chuze/work/etapas/3_revision/crosswalk.json','w'),indent=1)
print(json.dumps(summary,indent=0))
