import sys,os,tempfile,json; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE, bitacora as BT
w=tempfile.mkdtemp(); BT.BIT=os.path.join(w,"bitacora.jsonl")
BT.subagente("revisor_cobertura","subagente TAKEOFF-AUTHOR")   # el autor del canon se registra como revisor; canon nunca registrado
rev,canon=CE.subagentes_bitacora(w); rv="subagente TAKEOFF-AUTHOR"
print("solo revisor registrado -> rev",rev,"canon",canon,"; falla?", (rv not in rev or rv in canon))
w2=tempfile.mkdtemp(); BT.BIT=os.path.join(w2,"bitacora.jsonl"); BT.subagente("revisor_de_lo_que_sea","X1")
print("rol 'revisor_de_lo_que_sea' cuenta como revisor:", "X1" in CE.subagentes_bitacora(w2)[0])
# _cob_disp con FALTA
d={"hoja":"Z9.01","tipo":"muro","id":"M1","x":"10","y":"10","decision":"FALTA","motivo":"m","nhoja":"1/X9.01","reviewer":"R","imagen":"a.png"}
print("FALTA limpia rojo?", CE._cob_disp([d],"Z9.01","muro",10,10,"M1",18) is not None)
print("NO ES NUESTRO limpia?", CE._cob_disp([dict(d,decision="NO ES NUESTRO")],"Z9.01","muro",10,10,"M1",18) is not None)
print("decision vacia limpia?", CE._cob_disp([dict(d,decision="")],"Z9.01","muro",10,10,"M1",18) is not None)
print("nhoja sin N/ limpia?", CE._cob_disp([dict(d,decision="CUBIERTO",nhoja="X9.01")],"Z9.01","muro",10,10,"M1",18) is not None)
