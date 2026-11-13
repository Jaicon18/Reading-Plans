import sys; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB, test_chequeos_biblioteca as T
fn = CB.faltantes_auditoria; B = T.B
# canon: corridor 901 ceiling LOADED (ceilings[0]) and GYP-9 tag row -> any "missing" finding about it must FAIL
can = {"walls": [{"id": "X9-901-01", "length_ft": 20.0}], "ceilings": [{"room": "Z9 Corridor 901", "area_sf": 50.0}],
       "misc_items": [{"ref": "EXT-Z9-2 board", "qty": 30.0}],
       "rcp_tags": [{"sheet": "X9.01", "tag": "GYP-9", "height": "8'-11\"", "rows": ["ceilings[0]"]}]}
A = "Auditoria/AUDITORIA_U181_rev9.md"
def run(ln, c=can, k=A, x=None):
    return fn(B(canon=c, textos=dict({k: "| 1 | " + ln + " | OPEN |"}, **(x or {}))))
print("S0 control 'corridor 901 ceiling missing' ->", run("corridor 901 ceiling missing")[0])
for ln in ("corridor 901 ceiling not found in take-off",
           "corridor 901 ceiling not taken off",
           "corridor 901 ceiling not counted",
           "corridor 901 ceiling absent from estimate",
           "corridor 901: ceiling GYP-9 is not in the Excel",
           "no se cargó el cielo del corredor 901",
           "corredor 901 sin cielo en el take-off",
           "corridor 901 ceiling was left out",
           "corridor 901 ceiling NOT LOADED",
           "corridor 901 ceiling - MISSING",
           "corridor 901 ceilng missing",            # typo de 'ceiling'
           "X9.01 GYP-9 not loaded in corridor 901",
           ):
    print("S1", repr(ln), "->", run(ln))
# room ids that RX_CUARTO_H does not see
can3 = {"walls": [], "ceilings": [{"room": "Corridor C-12", "area_sf": 50.0}, {"room": "Room B12", "area_sf": 40.0}], "rcp_tags": []}
for ln in ("Corridor C-12 ceiling missing", "Room B12 ceiling missing", "room 12 ceiling missing"):
    print("S2", repr(ln), "->", run(ln, can3))
# findings outside the files the check reads
for k in ("Auditoria/HALLAZGOS_rev9.md", "COORDINACION/hallazgos_rev9.md", "REVIEW_rev9.md", "Auditoria/hallazgos.csv",
          "Auditoria/AUDITORIA_U181_rev9.xlsx.txt", "BITACORA.md", "RESUMEN_rev9.md"):
    print("S3", k, "->", run("corridor 901 ceiling missing", k=k))
# explicit closure with an UNRELATED loaded ref (exterior wall line) silences a TRULY missing ceiling (room 216 not in canon)
print("S4 'corridor 216 ceiling missing | CERRADO: EXT-Z9-2 (1/X9.31)' (ceiling truly missing, closed with an exterior wall item) ->",
      run("corridor 216 ceiling missing | CERRADO: EXT-Z9-2 (1/X9.31)"))
# S5: DOBLE_CIELO row whose upper / lower cite loaded refs UNRELATED to the room (exterior wall item) resolves room 901,
#     so the false 'missing' of the LOADED ceiling of 901 is no longer reported
dc = ("Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason\n"
      "Z9 901 Corridor,Z9,double,RS-9,GYP-9,8'-11\",7/X9.23,x,upper: EXT-Z9-2; lower: EXT-Z9-2\n")
print("S5 DOBLE_CIELO 'upper: EXT-Z9-2; lower: EXT-Z9-2' + finding 'corridor 901 ceiling missing' (901 LOADED) ->",
      run("corridor 901 ceiling missing", x={"Auditoria/DOBLE_CIELO.csv": dc}))
for ln in ("Cuarto 901: falta el techo de tablaroca", "Room 901 hard lid missing", "Room 901 bulkhead missing (7/X9.23)",
           "Room 901 drywall lid not loaded"):
    print("S6", repr(ln), "->", run(ln))
