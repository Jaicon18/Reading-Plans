import sys,random; sys.path.insert(0,'.')
import comparar_alturas as C, pymupdf
random.seed(1)
# caso CR: muchas alturas pegadas (10.2-10.6, 8.9-9.2) + 30 cuartos de C.H.
grupos=[14.0,13.792,13.658,13.4,11.396,11.219,10.538,10.522,10.501,10.488,10.31,10.253,10.052,9.98,9.917,9.844,9.25,9.167,9.083,9.0,8.938,8.59,8.047,7.275,6.64,5.912,5.039,1.746,1.736,1.063,0.917,0.24]
final=[{"Printed H":f"{h}","Wall ID":f"XW.6.{i}-L1-0{i%9} A","Source":"x","Operation":"","Status":"CONFIRMED","Image":""} for i,h in enumerate(grupos)]
cuartos={f"{100+i}":random.choice([12.062,11.0,9.5,9.167,8.938,8.417,8.042,7.0,5.333]) for i in range(40)}
bo={"L1":14.0,"L2":11.0,"L3":11.0,"L4":14.0}
C.alturas_revisadas(final,".","out.pdf",bo,cuartos)
m=C.textos_encimados("out.pdf",-1)
print("encimados:",len(m)); print(m[:5])
d=pymupdf.open("out.pdf"); print("pag sec alto",d[-1].rect.height)
d[-1].get_pixmap(dpi=110).save("sec.png")
# el chequeo debe detectar la version vieja
import importlib.util
sp=importlib.util.spec_from_file_location("old","../v97/take-off-metal-frame-drywall/tools/comparar_alturas.py"); old=importlib.util.module_from_spec(sp); sp.loader.exec_module(old)
old.alturas_revisadas(final,".","old.pdf",bo,cuartos)
print("version vieja encimados:",len(C.textos_encimados("old.pdf",-1)))
