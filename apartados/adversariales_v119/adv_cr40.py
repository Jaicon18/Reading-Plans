import sys; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB
B=CB.Bundle if hasattr(CB,'Bundle') else None
import test_chequeos_biblioteca as T
fn=CB.faltantes_auditoria; Bb=T.B
can = {"walls": [], "ceilings": [{"room": "Z9 Corridor 901", "area_sf": 50.0}],
       "rcp_tags": [{"sheet": "X9.01", "tag": "GYP-9", "height": "8'-11\"", "rows": ["ceilings[0]"]}]}
for ln in ["X9.01 GYP-9 8'-11\" missing in corridor 901 — faltante_por_tag: CARGADO",
           "GYP-9 missing (faltante_por_tag: CARGADO)",
           "corridor 901 ceiling missing — closed by CLG-Z9-901",
           "Room 901 soffit not loaded"]:
    print(repr(ln), fn(Bb(canon=can, textos={"Auditoria/x_rev.md": ln})))
print("non-auditoria path:", fn(Bb(canon=can, textos={"resolucion.md": "GYP-9 missing"})))
