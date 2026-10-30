#!/usr/bin/env python3
"""cobertura.py — cobertura reducida del paso 12 (R80e.37): cada detalle / nota del trade con destino.

Entrada:
  lista.json = [{"sheet", "type", "text", "destination"?}] con los detalles / notas / spec lines del trade. En una corrida real la escribe
               el modelo (prompts/cobertura.md, ~1 USD) desde las hojas raster; en dry-run sale de la matriz del paso 12.
  canon (takeoff_canon.json) y takeoff.json finales.
Regla: con "destination" declarado, CUBIERTO si ese destino existe (ALC-xx / RFI-xx en el Excel, renglón del Material
       Summary / Partition Takeoff, o "n/a - <motivo>"); sin destino, CUBIERTO si alguna N/HOJA de su texto (o su hoja, si el texto no cita ninguna) aparece en el canon
       o en los textos del Excel (RFIs, cierres, Scope Checklist). Lo demás es HUECO y va a la resolución / al estimador.
Salida: cobertura.json + cobertura.md (en inglés). rc 0 siempre: la cobertura informa; no decide cantidades."""
import json
import re
import sys

NH = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}-?\d{2,3}[A-Z]?\b")
HOJA = re.compile(r"\b[A-Z]{1,2}-\d{3}[A-Z]?\b")


def corpus(canon, tk):
    txt = json.dumps(canon, ensure_ascii=False) + json.dumps(
        {k: tk.get(k) for k in ("rfis", "rfi_cierre", "alcances", "revisar", "inputs_notas")}, ensure_ascii=False)
    return set(NH.findall(txt)), set(HOJA.findall(txt))


def main(argv):
    lista, canon, tk, out = argv[1:5]
    items = json.load(open(lista))
    nh_ok, hoja_ok = corpus(json.load(open(canon)), json.load(open(tk)))
    res = []
    tkd = json.load(open(tk))
    alc = {a["id"] for a in tkd.get("alcances") or []}
    rfis = {r.get("id") for r in tkd.get("rfis") or []} | set((tkd.get("rfi_cierre") or {}).keys())
    for it in items:
        de = str(it.get("destination") or "")
        if de:                                             # destino declarado por la lectura: se verifica que exista
            ids_a = set(re.findall(r"\bALC-[A-Z]?\d+\b", de))
            ids_r = set(re.findall(r"\bRFI-[A-Z0-9-]+\b", de))
            malos = sorted((ids_a - alc) | {r for r in ids_r if r not in rfis and not any(x.startswith(r) for x in rfis)})
            # hoja / nota sin contenido del trade, CON motivo ("n/a" pelado = hueco: el motivo es obligatorio)
            na = re.match(r"(?i)\s*(n/?a\s*[-(:].{3,}|not div|no div|exclu|none needed|sheet reviewed)", de)
            if not malos and (ids_a or ids_r or na or re.search(r"Material Summary|Partition Takeoff|Inputs", de)):
                res.append(dict(it, status="COVERED (destination)", found=sorted(ids_a | ids_r) or [de[:60]]))
                continue
        refs = NH.findall(str(it.get("text") or ""))
        if refs:
            dest = [r for r in refs if r in nh_ok]
            st = "COVERED" if dest else "GAP"
        else:
            h = str(it.get("sheet") or "")
            dest = [h] if h in hoja_ok else []
            st = "COVERED (sheet)" if dest else "GAP"
        res.append(dict(it, status=st, found=dest))
    gaps = [r for r in res if r["status"] == "GAP"]
    s = {"items": len(res), "covered": len(res) - len(gaps), "gaps": len(gaps),
         "coverage_pct": round(100.0 * (len(res) - len(gaps)) / max(1, len(res)), 2)}
    json.dump({"summary": s, "items": res}, open(out + ".json", "w"), indent=1, ensure_ascii=False)
    with open(out + ".md", "w") as f:
        f.write(f"# Coverage (reduced step 12)\n\n{s['items']} items · {s['covered']} covered · {s['gaps']} gaps · {s['coverage_pct']} %\n\n")
        if gaps:
            f.write("| # | Sheet | Type | Text |\n|---|---|---|---|\n")
            for i, g in enumerate(gaps, 1):
                f.write(f"| {i} | {g.get('sheet')} | {g.get('type')} | {str(g.get('text'))[:160]} |\n")
    print(json.dumps(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
