"""U-190 ⭐ REGLA DE ORO #3 (v81cf105): Auditoria/DOBLE_CIELO.csv - TODO cuarto de cada RCP (cuartos_rcp del set) con Type single / double,
Upper ceiling (membrana rated FS-1 / RS-1 del canon), Lower ceiling (GYP colgado = renglón CLG; ACT / WS = otro oficio), Heights, N/SHEET,
Framing (metal SOLO con fuente impresa: RC del assembly FS-1 / RS-1 A0.08; suspensión de la leyenda GYP-1 'GYPSUM BOARD ON METAL
SUSPENSION SYSTEM' 1/A3.0x; o 'direct to wood') y Row / reason ('upper: …; lower: …').
El cielo de abajo de cada cuarto sale de los renglones CLG del canon (número de cuarto en la fuente) y, si no hay, del tag de cielo impreso
más cercano a la etiqueta del cuarto en su hoja RCP (A3.0x / A7.xx). Uso: doble_cielo.py <carpeta_entrega>"""
import csv
import json
import os
import re
import sys

import pymupdf as fitz

sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE  # noqa: E402

W = '/root/cr/work'
E = sys.argv[1]
C = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
H = json.load(open(f'{W}/set_texto.json'))['hojas']
PG = {x['sheet']: x['page'] - 1 for x in json.load(open(f'{W}/etapas/1_inventario/paginas_hojas.json'))['sheets']}
doc = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
cq = CE.cuartos_rcp(H)
RQ = json.load(open(f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'))
RCP_NIVEL = {'L1': '1/A3.01', 'L2': '1/A3.02', 'L3': '1/A3.03', 'L4': '1/A3.04'}
LEY = "GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING'"


def nivel(n):
    return f"L{n[0]}"


def ft(h):
    try:
        h = float(h)
    except (TypeError, ValueError):
        return ""
    i = int(h); r = round((h - i) * 12 * 8) / 8
    return f"{i}'-{r:g}\""


# membranas rated (ceilings[]) por cuarto
memb = {}
for i, c in enumerate(C['ceilings']):
    for n in re.findall(r"\b(\d{3}[A-Z]?)\b", str(c['room'])):
        memb.setdefault(n, (i, c))
L1M = next((i, c) for i, c in enumerate(C['ceilings']) if str(c['room']).startswith('L1 FS-1 membrane'))
# cielos colgados = renglones CLG ' board' (no RC: el RC es la membrana; R = RS-1 sobre el baño de L4)
colg, extra_up = {}, {}
for m in C['misc_items']:
    r = str(m['ref'])
    if not (r.startswith('CLG-') and r.endswith(' board')):
        continue
    head = str(m.get('source') or '').split(':')[0]
    nums = re.findall(r"\b(\d{3}[A-Z]?)\b", head)
    alt = re.search(r"height (\d+\.\d+)|GYP-\d (\d+' ?- ?\d+(?: \d/\d)?\")", str(m.get('source')))
    for n in nums:
        if r.split('-')[1][:2] != nivel(n):           # el renglón es de otro piso (CLG-L1-219U = cielo de L1 bajo el piso del mezzanine 219)
            continue
        if re.search(r"RS-1 board on resilient channel", str(m.get('source'))):   # 219: el renglón CLG ES la membrana RS-1 (sobre RC)
            extra_up.setdefault(n, []).append(r + " = RS-1 membrane on RC (RFI-15)")
            continue
        if r.split(' ')[0].endswith('R'):
            extra_up.setdefault(n, []).append(r)
        else:
            colg.setdefault(n, []).append((r, head, m))


def tag_cercano(hoja, n):
    if hoja not in PG:
        return None
    p = doc[PG[hoja]]
    ws = p.get_text('words')
    lab = [w for w in ws if w[4] == n]
    tags = [w for w in ws if re.match(r"^(ACT|WS|GYP)-\d$", w[4])]
    best = None
    for l in lab:
        for t in tags:
            d = ((l[0] - t[0]) ** 2 + (l[1] - t[1]) ** 2) ** .5
            if d < 260 and (best is None or d < best[0]):
                alt = " ".join(x[4] for x in ws if 0 < x[1] - t[1] < 14 and abs(x[0] - t[0]) < 30)
                best = (d, t[4], alt)
    return best


filas, vistos = [], set()
for h, rooms in sorted(cq.items()):
    for n in rooms:
        if n in vistos:
            continue
        vistos.add(n)
        lv = nivel(n)
        up_i, up_c = memb.get(n) or ((L1M if lv == 'L1' else (None, None)))
        up = f"{(up_c.get('assembly') or {}).get('id')} membrane" if up_c else ""
        if not up_c and any('RS-1 membrane' in x for x in extra_up.get(n, [])):
            up = "RS-1 membrane (sloped, on RC)"
        up_row = f"ceilings[{up_i}] {(up_c.get('assembly') or {}).get('id')}" if up_c else ""
        if n in extra_up:
            _rs = [x for x in extra_up[n] if 'RS-1 membrane' not in x]
            _m = [x for x in extra_up[n] if 'RS-1 membrane' in x]
            if _rs:
                up_row += " + " + " / ".join(_rs) + " (RS-1 over the bath)"
            if _m and not up_row:
                up_row = " / ".join(_m)
        low_rows = colg.get(n) or []
        low, low_row, alts, fr_low = "", "", [], ""
        if low_rows:
            low = "GYP (hung)"
            low_row = " / ".join(r for r, _h, _m in low_rows)
            fr_low = f"lower: metal suspension per the {LEY} ({RCP_NIVEL[lv]})"
        else:
            x_ = next((x for x in RQ.get('rooms') or [] if x.get('disposition') == 'exclusion' and str(x.get('room')).split(' ')[0] == n
                       and re.search(r"ACT|WS-1|Food & Beverage", str(x.get('reason')))), None)
            if x_:
                t_ = re.search(r"(ACT-\d|WS-1)", str(x_.get('reason')))
                low = t_.group(1) if t_ else ("ACT-3 (F&B, tenant)" if n == '100' else "F&B by tenant")
                low_row = f"{low} by others ({str(x_.get('reason'))[:70]}; {x_.get('sheet')} rcp_cuartos)"
                fr_low = "lower: by others"
        if up_c:
            alts.append(ft(up_c.get('height_ft')))
        tipo = "double" if (up and low) else "single"
        asm = (up_c.get('assembly') or {}).get('id') if up_c else None
        fr_up = (f"upper: RC per {asm} assembly (A0.08, UL L546)" if asm == 'FS-1' else f"upper: channel per {asm} assembly (A0.08)") if asm else ""
        if not asm and up.startswith('RS-1'):
            fr_up = "upper: RC per RS-1 assembly (A0.08, RFI-15)"
        if not up_c:
            if n in ('410', '411', '419'):
                up, up_row = "", "F&B interior by tenant ('INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT', 1/A2.04 / 3/A7.50)"
                fr_up = "none (tenant) - 1/A2.04"
            elif lv == 'L4':
                up_row = "roof assembly RS-2 / RS-3 without board (A0.08 / A2.05, ALC-25): the hung GYP-1 is the only ceiling"
                fr_up = "upper: none (no board in the roof assembly, A0.08)"
        if tipo == "single" and not low and up_c and not fr_low:
            fr_low = ""
        row = f"upper: {up_row or 'none'}; lower: {low_row or 'none'}" if tipo == "double" else (f"single: {up_row or low_row or 'none'}" + (f"; lower: {low_row}" if (low_row and up_row) else ""))
        filas.append({"Room": f"{lv} {n} {'' if lv == 'L1' else str((up_c or {}).get('room') or '').replace(lv, '').strip()[:40]}".strip(), "Level": lv, "Type": tipo,
                      "Upper ceiling": up, "Lower ceiling": low, "Heights": " / ".join(a for a in alts if a),
                      "N/SHEET": f"{RCP_NIVEL[lv]} / {h}", "Framing": "; ".join(x for x in (fr_up, fr_low) if x) or f"direct to wood ({RCP_NIVEL[lv]})",
                      "Row / reason": row})
# U-187 (CE_TEXTOS_LEGIBLES): la página DOUBLE CEILING pone cada celda en una columna fija (Framing 120 pt, Row 130 pt, letra mínima 4 pt):
# textos cortos sin perder la fuente (N/HOJA / assembly) ni el renglón
def _corto(t, n):
    t = re.sub(r"\b((?:CLG|SOF|BW)-[\w-]+) board\b", r"\1", t)
    for a, b in ((r"RC per FS-1 assembly \(A0\.08, UL L546\)", "RC FS-1 (A0.08)"), (r"channel per RS-1 assembly \(A0\.08\)", "chan. RS-1 (A0.08)"),
                 (r"metal suspension per the GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' \((1/A3\.0\d)\)", r"GYP-1 grid (\1)"),
                 (r"RC per RS-1 assembly \(A0\.08, RFI-15\)", "RC RS-1 (A0.08)"), (r" \(RS-1 over the bath\)", ""),
                 (r"by others \(.*?rcp_cuartos\)", "by others"), (r"ceilings\[(\d+)\] (FS-1|RS-1)", r"\2 [\1]"),
                 (r"upper: none \(no board in the roof assembly, A0\.08\)", "upper: none (A0.08 RS-2/3)"),
                 (r"roof assembly RS-2 / RS-3 without board \(A0\.08 / A2\.05, ALC-25\): the hung GYP-1 is the only ceiling", "roof RS-2/3 no board (A0.08)"),
                 (r"F&B interior by tenant \('INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT', 1/A2\.04 / 3/A7\.50\)", "F&B by tenant (1/A2.04)"),
                 (r" = RS-1 membrane on RC \(RFI-15\)", " RS-1 on RC"), (r"none \(tenant\) - 1/A2\.04", "none, tenant (1/A2.04)")):
        t = re.sub(a, b, t)
    return t if len(t) <= n else t[:n - 3] + "..."


for f_ in filas:
    f_["Framing"] = _corto(f_["Framing"], 58)
    f_["Row / reason"] = _corto(f_["Row / reason"], 64)
    f_["Room"] = f_["Room"][:24]
os.makedirs(os.path.join(E, 'Auditoria'), exist_ok=True)
with open(os.path.join(E, 'Auditoria', 'DOBLE_CIELO.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0]))
    w.writeheader(); w.writerows(filas)
print(f"DOBLE_CIELO: {len(filas)} cuartos, {sum(1 for x in filas if x['Type'] == 'double')} double")
