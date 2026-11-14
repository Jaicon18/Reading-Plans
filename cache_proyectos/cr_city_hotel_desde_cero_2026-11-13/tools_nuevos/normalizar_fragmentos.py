#!/usr/bin/env python3
"""normalizar_fragmentos.py (BE-CR0-02, CR desde cero 13-nov): varios lectores en paralelo escriben la MISMA constante
(plan_scale_by_sheet, plan_scale_pt_per_ft) o el MISMO detalle con textos de fuente distintos y `etapas.py unir` lo
rechaza como conflicto. Este programa copia los fragmentos a <out_dir> y mueve constants / details a un fragmento
00_comunes.json: valores IGUALES se unen (fuentes concatenadas); valores DISTINTOS = error (no se elige en silencio);
details con el mismo N/HOJA: notas unidas (cada lector citado). No cambia ningún número de walls / ceilings.
Uso: normalizar_fragmentos.py <dir_fragmentos> <out_dir>"""
import json, os, sys

def main(src, out):
    os.makedirs(out, exist_ok=True)
    comunes = {"constants": {}, "details": {}}
    errores = []
    pend = []
    for f in sorted(x for x in os.listdir(src) if x.endswith(".json")):
        d = json.load(open(os.path.join(src, f)))
        c = d.pop("constants", {}) or {}
        for k, v in c.items():
            if k == "plan_scale_by_sheet":
                tgt = comunes["constants"].setdefault(k, {})
                for sh, sv in v.items():
                    if sh not in tgt:
                        tgt[sh] = dict(sv) if isinstance(sv, dict) else {"value": sv, "source": f}
                    else:
                        a = tgt[sh]; vb = sv.get("value") if isinstance(sv, dict) else sv
                        if float(a["value"]) != float(vb):
                            errores.append(f"{k}.{sh}: {a['value']} vs {vb} ({f})")
                        elif isinstance(sv, dict) and sv.get("source") not in a["source"]:
                            a["source"] += " | " + str(sv.get("source"))
            elif k == "plan_scale_pt_per_ft":     # global = escala de las plantas generales; otra escala vale solo si
                pend.append((f, v, c.get("plan_scale_by_sheet") or {}))   # está declarada por hoja en plan_scale_by_sheet
            elif isinstance(v, dict) and "value" in v:
                if k not in comunes["constants"]:
                    comunes["constants"][k] = dict(v)
                elif comunes["constants"][k]["value"] != v["value"]:
                    errores.append(f"{k}: {comunes['constants'][k]['value']} vs {v['value']} ({f})")
                elif str(v.get("source")) not in str(comunes["constants"][k].get("source")):
                    comunes["constants"][k]["source"] = f"{comunes['constants'][k].get('source')} | {v.get('source')}"
            else:
                comunes["constants"].setdefault(k, v)
        for k, v in (d.pop("details", {}) or {}).items():
            if k not in comunes["details"]:
                comunes["details"][k] = dict(v, readers=[f])
            else:
                e = comunes["details"][k]
                e["readers"].append(f)
                if str(v.get("notes")) not in str(e.get("notes")):
                    e["notes"] = f"{e.get('notes')} || [{f}] {v.get('notes')}"
        json.dump(d, open(os.path.join(out, f), "w"), indent=1)
    psb = comunes["constants"].get("plan_scale_by_sheet") or {}
    gen = [(f, v) for f, v, _ in pend if any(sh.startswith("A2.") and float(psb[sh]["value"]) == float(v["value"]) for sh in psb)]
    if gen:
        comunes["constants"]["plan_scale_pt_per_ft"] = {"value": gen[0][1]["value"], "source": " | ".join(sorted({str(v.get("source")) for _, v in gen}))}
    for f, v, propio in pend:
        if float(v["value"]) != float(comunes["constants"].get("plan_scale_pt_per_ft", {}).get("value", v["value"])) and \
                not any(float((x.get("value") if isinstance(x, dict) else x)) == float(v["value"]) for x in propio.values()):
            errores.append(f"plan_scale_pt_per_ft {v['value']} ({f}) sin hoja en plan_scale_by_sheet")
    json.dump(comunes, open(os.path.join(out, "00_comunes.json"), "w"), indent=1)
    for e in errores:
        print("ERROR:", e)
    return 1 if errores else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
