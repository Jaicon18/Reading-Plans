"""v81cf119 (CB_FALTANTES_AUDITORIA, BE-CR40): todo hallazgo de cielo faltante de un informe de auditoría ya corregido cita la ref del canon
que lo cargó (cierre). Anota (no borra) el informe U-138 #1. Idempotente."""
p = '/root/cr/work/auditoria_U138/INFORME_AUDITORIA_U138.md'
s = open(p, encoding='utf-8').read()
a = "y la falta del cielo de 412 (hallazgo 3)."
b = ("y la falta del cielo de 412 (hallazgo 3). Cierre del hallazgo 3: cargado después en el canon como ceilings[51] 'L4 412 Corridor (field ceiling)', "
     "RS-1, rev10-rev20. CERRADO: ceilings[51] (1/A3.04).")
import re
s = re.sub(r" Cierre del hallazgo 3:.*?(?= El barrido)", "", s)
if True:
    assert s.count(a) == 1
    s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
print("cierre_hallazgos: OK")
