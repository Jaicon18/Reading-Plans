import sys; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
band={"ori":"V","c0":1509.0,"c1":1512.8,"lo":1124.0,"hi":1163.8,"sheet":"Z9.11"}
red=[{"hoja":"Z9.11","tipo":"muro","id":"M-29","x":"1505.7","y":"1145.0","largo_ft":"4.0","estado":"ROJO"}]
def run(wid, reason, rows=red, extra=None, b=band):
    can={"walls":[{"id":wid,"band":b}],"excluded_walls":[dict({"id":"EX","reason":reason},**(extra or {}))]}
    return bool(CE.be_gk54_fallas(can,rows))
print("G0 control GK id:", run("X9-Z9-08","same single wall as X9-Z9-08"))
print("G1 id de otro proyecto 'TO-W.4-L2-02':", run("TO-W.4-L2-02","same single wall as TO-W.4-L2-02"))
print("G1b id 'W-12':", run("W-12","same wall as W-12"))
print("G2 sinónimo 'duplicate of X9-Z9-08':", run("X9-Z9-08","duplicate of X9-Z9-08 (one wall)"))
print("G2b 'same as X9-Z9-08':", run("X9-Z9-08","same as X9-Z9-08"))
print("G2c 'part of wall X9-Z9-08':", run("X9-Z9-08","part of wall X9-Z9-08"))
print("G3 gap_proof sin N/HOJA ('none'):", run("X9-Z9-08","same wall as X9-Z9-08",extra={"gap_proof":"n/a"}))
print("G4 rojo DISPUESTO (revisor lo dispuso NO ES NUESTRO):", run("X9-Z9-08","same wall as X9-Z9-08",rows=[dict(red[0],estado="DISPUESTO")]))
# G5 merged leaf: the coverage detector fused both leaves into the X band (CUBIERTO), no separate RED band
print("G5 leaves fusionadas por el detector (sin banda roja aparte):", run("X9-Z9-08","same wall as X9-Z9-08",rows=[dict(red[0],x="1511",estado="CUBIERTO")]))
print("G5b rojo dentro de la banda (|cross|<=0.5pt) (leaf fusionada parcialmente roja):", run("X9-Z9-08","same wall as X9-Z9-08",rows=[dict(red[0],x="1511.0")]))
print("G6 X sin 'band' en canon:", run("X9-Z9-08","same wall as X9-Z9-08",b={}))
