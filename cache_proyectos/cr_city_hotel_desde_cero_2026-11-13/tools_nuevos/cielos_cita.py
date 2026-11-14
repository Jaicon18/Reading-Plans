#!/usr/bin/env python3
"""CE_MARKUPS_EXCEL (BE-117) en cielos: el DETAIL del markup = N/HOJA del cielo, y esa cita está en el renglón del Excel. Cada cielo sin
'detail' toma la vista RCP donde se midió (1/<hoja>); el 'detail' se antepone a 'source' si no aparece (la fuente del ítem lo cita).
Uso: cielos_cita.py <canon.json>"""
import json, sys
p = sys.argv[1]; c = json.load(open(p, encoding="utf-8")); n = 0
for x in c.get("ceilings") or []:
    if not str(x.get("detail") or "").strip() and x.get("sheet"):
        x["detail"] = f"1/{x['sheet']}"; n += 1
    d = str(x.get("detail") or "")
    if d and d not in str(x.get("source") or ""):
        x["source"] = f"{d} | {x.get('source') or ''}"
json.dump(c, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("cielos con detail nuevo:", n)
