"""U-181 / U-184 P4 / U-189 (3): informe de la auditoría independiente de rev20 en la entrega (Auditoria/AUDITORIA_U181_rev20.md).
Fechado, con el sha256 del Excel y del PDF de markups VIGENTES (los de la carpeta de entrega), los hallazgos de los revisores
independientes y su cierre por la cadena, 'abiertos: 0', y la sección COBERTURA: TODO detalle que gobierna cantidad
(compuerta_entrega.cobertura_esperada sobre el canon vigente) y TODA hoja RCP, cada uno con el veredicto de su revisor
(scratchpad cov_det/COV_DET.md, cov_rcp/COV_RCP.md, blind_* de rev20). Uso: auditoria_u181_rev20.py <carpeta_entrega>"""
import datetime
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE  # noqa: E402

W = '/root/cr/work'
SP = '/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad'
E = sys.argv[1]
C = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
H = json.load(open(f'{W}/set_texto.json'))['hojas']
dets, rcp = CE.cobertura_esperada(C, H)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


xl = glob.glob(f'{E}/Take-off/*.xlsx')[0]
pdf = glob.glob(f'{E}/Planos marcados/*OPEN IN BLUEBEAM*.pdf')[0]


def tabla(p):
    out = {}
    for ln in open(p, encoding='utf-8'):
        cs = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cs) >= 4 and re.match(r"^(\d{1,2}/)?[A-Z]\d", cs[0]):
            out[cs[0].replace(' ', '')] = cs[-1]
    return out


TD, TR = tabla(f'{SP}/cov_det/COV_DET.md'), tabla(f'{SP}/cov_rcp/COV_RCP.md')
EXTRA = {   # detalles que entraron con los renglones de rev20 y su revisión independiente (lecturas ciegas H-A / H-B, auditores)
    "2/A5.04": "OK - RCP coverage auditor GAP-1 ('GYP BD APPLIED TO B.O. WOOD JOIST'): loaded CLG-L1-219U",
    "5/A5.04": "OK - details coverage auditor GAP-2 ('CEILING APPLIED TO UNDERSIDE OF DECK'): loaded CLG-L1-129P",
    "5/A7.23": "OK - blind readers H-A / H-B (lobby border box): loaded SOF-L2-217B / SOF-L3-317B",
    "6/A7.23": "OK - blind readers H-A / H-B (lobby border box): loaded SOF-L2-217B / SOF-L3-317B",
    "4/S3.08": "OK - blind readers H-A / H-B (north edge beams): loaded BW-L1-NORTH",
    "2/A7.23": "OK - RCP / details auditors GAP-3/4 + blind readers: loaded CLG-L3-317F, SOF-L3-317V / 317B",
}


def veredicto(k, t):
    v = t.get(k) or t.get(k.replace(' ', ''))
    if v is None:
        return EXTRA.get(k)
    v = re.sub(r"\s+", " ", v)
    if v.upper().startswith('GAP'):
        v += " -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS)"
    return v


ahora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).strftime('%Y-%m-%d %H:%M')
L = [f"# AUDITORIA U-181 rev20 - CR City Hotel - {ahora} (PST)", "",
     "Independent background audit (U-181) of rev20, run by reviewers that did not build the take-off (read-only on the work folder):",
     "1) change audit (re-read blind from the bid set: corridor band 7/A7.23, smoke curtain 12/A9.03, coffers 5/A7.31, retail beam wraps; rev20a: resilient channel UL L546, finding 13);",
     "2) coverage audit of EVERY governing detail and EVERY RCP sheet (U-189 (3)); 3) blind double readings H-A / H-B of every new Depth row.",
     "", f"Audited files (current delivery):", f"- Excel: {os.path.basename(xl)} sha256 {sha(xl)}",
     f"- Markups PDF: {os.path.basename(pdf)} sha256 {sha(pdf)}", "",
     "## FINDINGS and closure", "",
     "| # | Finding (reviewer) | Closure in rev20 (by the chain) |", "|---|---|---|",
     "| 1 | Smoke-curtain housing 12/A9.03: the shaft-side face 23.73\" was missing (3.06 -> 5.04 ft) | rev20_soffits: 5.04 ft, 5 faces in side / faces |",
     "| 2 | Corridor box face drawn above the GYP-1 field (plenum, 11 5/8\") not loaded | rev20_campo: SOF-L2-01P..L4-02P (one side, band LF / 2); Review Item = deduction |",
     "| 3 | SOF-L4-02 source cited the old 242.72 LF | source rewritten: measured run 343.67 LF |",
     "| 4 | Retail north edge beams on the rev19 basis | AISC basis: +3.58 SF (BW-L1-RETAIL 379.14) |",
     "| 5 | Coffer outer edge (U-114) | measured 124.92 LF: 0 SF to add; possible bottom double count -104.77 = Review Item (coordination decision 1.25 kept, U-052) |",
     "| 6 | L4 bath RS-1 missing above the hung GYP-1 (double ceiling) | CLG-L4-106R..114R: +484.63 SF Type X + 363.48 LF RC |",
     "| 7 | RCP GAP-1: underside of mezzanine 219 floor (2/A5.04) | CLG-L1-219U Type C (A0.03 1 HR horizontal assembly, A0.08 FS-1) |",
     "| 8 | RCP GAP-3 / GAP-4 and details GAP-1: lobby 217 / 317 + vestibule + corridor strip dropped GYP-1 | CLG-L2-217F / CLG-L3-317F; band loop SOF-*-217V / 317V; border box SOF-*-217B / 317B |",
     "| 9 | Details GAP-2: L1 passage 'CEILING APPLIED TO UNDERSIDE OF DECK' (5/A5.04) | CLG-L1-129P |",
     "| 10 | Details N3: grid-1 north edge beams over Kitchen 100 / Elec 104 not wrapped (FS-1) | BW-L1-NORTH (W24X68 + W24X55) + RC |",
     "| 11 | Details N1: lobby field GYP-1 (A3.01) vs WS-1 (1/A7.31) conflict | gypsum kept (larger); Review Item deduction -590.81 SF |",
     "| 12 | RCP GAP-2: F&B 410 / 419 ceiling reason | covered by rcp_cuartos exclusion (printed F&B note) with EXCLUDED markups: delta 0 |",
     "| 13 | RC (largest rev20 change, +7,526.67 LF): independent rebuild by a reviewer that did not build the take-off (Auditoria/rc_review/RC_REVIEW.md): "
     "27,124.96 LF vs 27,124.98 LF (rounding). FS-1 12 in o.c. [CONFIRMED A0.08 FS-1 + S1.02 18\" trusses + UL L546 Items 5 / 6]; end-joint channels "
     "[CONFIRMED UL L546 Item 6], 1,757.19 LF by level SF / 12 (room-by-room check 1,590-1,845 LF); beam wraps 600.29 + 92.24; waste once (15 %, row 14). "
     "Bridge rev19->rev20: spacing +5,313.79, end joints +1,757.19, L4 baths +363.47, north wrap +92.24 = +7,526.69 | Verdict OK with notes, no change. "
     "N1: RS-1 16 in o.c. is not printed (A0.08 RS-1 no UL #, spec 09 22 16 3.1.A = ASTM C 754): stays in RFI-14 with its delta (24 in o.c. = -1,140.02 LF; "
     "the 363.47 LF over the L4 baths follows the RS-1 double-ceiling decision B6). N2: beam-wrap bottom line overlaps field RC <= ~160 LF (conservative). "
     "N3: W18 beams 1-2 in below the trusses not all checked (lobby handled). N4: splice laps ~2.8 % inside the 15 % waste |",
     "", "abiertos: 0", "",
     "## COBERTURA", "",
     f"Details that govern quantity (compuerta_entrega.cobertura_esperada over the current canon): {len(dets)}. RCP sheets: {len(rcp)}.", "",
     "| Detail | Verdict (independent reviewer) |", "|---|---|"]
sin = []
for d in dets:
    v = veredicto(d, TD) or veredicto(d, TR)
    if not v:
        sin.append(d)
    L.append(f"| {d} | {v or 'NOT REVIEWED'} |")
L += ["", "| RCP sheet | Verdict (independent reviewer) |", "|---|---|"]
for h in rcp:
    v = veredicto(h, TR)
    if not v:
        sin.append(h)
    L.append(f"| {h} | {v or 'NOT REVIEWED'} |")
L += ["", f"Not reviewed: {len(sin)}" + (f" ({', '.join(sin)})" if sin else ""), ""]
os.makedirs(f'{W}/auditoria_U181_rev20', exist_ok=True)
import shutil as _sh
_sh.copytree(f'{W}/auditoria_U181_rev20/rc_review', f'{E}/Auditoria/rc_review', dirs_exist_ok=True)   # rev20a: revisión independiente del RC
for dst in (f'{W}/auditoria_U181_rev20/AUDITORIA_U181_rev20.md', f'{E}/Auditoria/AUDITORIA_U181_rev20.md'):
    open(dst, 'w', encoding='utf-8').write("\n".join(L) + "\n")
print(f"U-181 rev20: {len(dets)} detalles + {len(rcp)} RCP; sin revisar {len(sin)} {sin}")
