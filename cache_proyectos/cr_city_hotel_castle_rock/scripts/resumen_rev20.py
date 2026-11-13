"""rev20a (auditoría U-138 12-nov, hallazgo 2): RESUMEN_rev20.md y BITACORA_rev20.md NO llevan una tabla de deltas escrita a mano: la
sección '## Delta del Material Summary' se regenera SIEMPRE desde etapas/DELTA_rev19_rev20.md (delta_rev.py, que lee el Material Summary
del Excel final), y se agregan los renglones de cambio de RC (UL L546) y de citas U-191. Idempotente."""
import re

W = '/root/cr/work'
D = open(f'{W}/etapas/DELTA_rev19_rev20.md', encoding='utf-8').read()
tabla = "\n".join(l for l in D.splitlines() if l.startswith('|'))
SEC = ("## Delta del Material Summary (NET) rev19 -> rev20\n\n"
       "Regenerated from the final Excel Material Summary (etapas/DELTA_rev19_rev20.md, delta_rev.py); never typed by hand.\n\n" + tabla + "\n")
EXTRA = [
    ("| Resilient channel FS-1 (ceilings[] + RC-FS1-ENDJ-L1/L2/L3 + 24 closet rows) |",
     "| Resilient channel FS-1 (ceilings[] + RC-FS1-ENDJ-L1/L2/L3 + 24 closet rows) | 16 in o.c. (RFI-14) | 12 in o.c. + 2 channels 6 in apart at each board "
     "end joint (+7,070.95 LF [DERIVED] = 7,526.67 total delta - 455.72 delta before UL L546) | UL L546 Item 6 (insulation draped over the membrane; A0.08 FS-1 'BATT INSULATION TO FILL ENTIRE "
     "FRAMING CAVITY' / 'SPACING PER ASSEMBLY TO ACHIEVE FULL CAVITY INSULATION'); RS-1 stays 16 in o.c. (no UL #, spec 09 22 16 3.1.A) |"),
]
for f in ('RESUMEN_rev20.md', 'BITACORA_rev20.md'):
    p = f'{W}/{f}'
    s = open(p, encoding='utf-8').read()
    s = re.sub(r"## Delta del Material Summary \(NET\) rev19 -> rev20\n.*?(?=\n## )", SEC, s, count=1, flags=re.S)
    for marca, fila in EXTRA:
        if marca not in s:
            s = re.sub(r"(\| Vigas de borde norte BW-L1-NORTH[^\n]*\n)", lambda m: m.group(1) + fila + "\n", s, count=1)
    if "rev20a" not in s:
        s = s.replace("\n## Entrega", "\n## rev20a (auditoría U-138, 12-nov)\n\n- Delta table above regenerated from the Excel (was typed before UL L546: RC "
                      "20,054.03 / +455.72; the Excel says 27,124.98 / +7,526.67).\n- Material Summary RC row cites UL L546 Item 6 (U-191).\n"
                      "- AUDITORIA_U181_rev20: independent RC review added.\n- No quantity changes vs rev20; markups PDF unchanged.\n\n## Entrega", 1)
    s = re.sub(r"\n## rev20b .*?(?=\n## Entrega)", "", s, count=1, flags=re.S)   # siempre se regenera
    open(p, 'w', encoding='utf-8').write(s)
    print(f, 'RC row:', [l for l in s.splitlines() if l.startswith('| Resilient channel 1/2"')][:1])

# rev20b (COORDINACIÓN 12-nov 23:25, opción b): entrega NUEVA con su nombre. RESUMEN_rev20b.md / BITACORA_rev20b.md: delta rev20 -> rev20b
# regenerado SIEMPRE desde etapas/DELTA_rev20_rev20b.md (Excel rev20b contra el Excel rev20 entregado, archivo_rev20); nunca a mano.
D2 = open(f'{W}/etapas/DELTA_rev20_rev20b.md', encoding='utf-8').read()
T2 = "\n".join(l for l in D2.splitlines() if l.startswith('|'))
R20 = open(f'{W}/RESUMEN_rev20.md', encoding='utf-8').read()
sec = lambda t, h: (re.search(r"\n## " + h + r".*?(?=\n## |\Z)", t, re.S) or [""])[0]
CAMBIOS = (
    "\n## rev20b (U-193 coverage map: 457 reds reviewed by 3 independent reviewers, Auditoria/COBERTURA_DISPOSICION.csv, 0 open)\n\n"
    "- Loaded (missing walls found): UNTYPED-L3-12 (W.4 stub west of LINEN 322, 2.40 LF x 2 faces, L3 twin of UNTYPED-L2-12); "
    "XW.6.6-L4-16 B (exterior sheathing face of the F&B 410 NW corner, 5.03 LF; only the F&B interior face is excluded); "
    "FW.2-L2-15 / FW.2-L3-15 / FW.2-L3-14 (SE stair CMU north face: corridor 218 / 318 parts 12.06 LF + 309 foyer / closet 6.59 LF; FW.2-L2-14 extended to the 209.1 door).\n"
    "- XW.6.3-L1-01 S: pier west face to the lobby strip, 3.23 LF x 11.0, +35.53 SF (outside the RFI-05 Retail 124 boundary).\n"
    "- Loaded conservative (type / material not printed; U-172 / U-191 sweep without answer) with RFI A / B / C and delta: RFI-30 lobby "
    "stair 127 lining LIN-127-L1..L4 (2,325.5 SF 5/8\" Type X, one face; INTERIOR DRAWINGS referenced but not issued in the bid set); "
    "RFI-31 Stair 2 exit passage wall XW.6.3-L1-04 A / B (4.11 LF).\n"
    "- Addendum reviewed (BuildingConnected 12-nov): Geotech / Irrigation / Landscape / Site Demo Plans - no quantity impact.\n")
for f, tit in (('RESUMEN_rev20b.md', 'RESUMEN'), ('BITACORA_rev20b.md', 'BITACORA')):
    t = (f"# {tit} rev20b FINAL — CR City Hotel (Castle Rock, CO)\n\n"
         "rev20b is a NEW delivery that replaces rev20 (rev20a): different quantities (coverage review U-193).\n\n"
         "## Delta del Material Summary (NET) rev20 -> rev20b\n\n"
         "Regenerated from the final Excel Material Summary (etapas/DELTA_rev20_rev20b.md, delta_rev.py: rev20b Excel vs the delivered rev20 "
         "Excel); never typed by hand.\n\n" + T2 + "\n" + CAMBIOS + sec(R20, "Entrega") + sec(R20, "Errores") + "\n")
    open(f'{W}/{f}', 'w', encoding='utf-8').write(t)
    print(f, 'filas delta:', T2.count('\n') - 1)

# rev20c (decisión del usuario 13-nov sobre RFI-30 -> ALTERNATE #1): RESUMEN_rev20c.md / BITACORA_rev20c.md, delta rev20b -> rev20c
# regenerado del Excel (etapas/DELTA_rev20b_rev20c.md: Excel rev20c contra el Excel rev20b entregado, archivo_rev20b); nunca a mano.
D3 = open(f'{W}/etapas/DELTA_rev20b_rev20c.md', encoding='utf-8').read()
T3 = "\n".join(l for l in D3.splitlines() if l.startswith('|'))
_C = __import__('json').load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
_A = next((a for a in _C.get('add_alternates') or [] if a.get('id') == 'ALTERNATE #1'), None)
ALT = ("\n## ALTERNATE #1 (ADD) - NOT in the base (user decision 13-nov on RFI-30: 'ponlo como alternate')\n\n"
       + (_A['texto'] + ". REASON: " + str(_A.get('razon', '')).rstrip('.') + "; excluded from the base bid and priced as an add alternate until clarified" + "\n\nIts quantities [DERIVED] are NOT in the Material Summary (the "
          "Material Summary is the base bid): they are on the Scope Checklist line ALTERNATE #1 and in the Proposal ALTERNATE #1 PRICING block, each with its operation." if _A else "(missing)") + "\n")
for f, tit in (('RESUMEN_rev20c.md', 'RESUMEN'), ('BITACORA_rev20c.md', 'BITACORA')):
    t = (f"# {tit} rev20c FINAL — CR City Hotel (Castle Rock, CO)\n\n"
         "rev20c is a NEW delivery that replaces rev20b: the user answered RFI-30 ('ponlo como alternate'). The stair 127 lining leaves the base bid "
         "and is priced apart as ALTERNATE #1 (ADD). RFI-31 resolved from the printed rating + finish (A0.01 2 HR RATED EXTERIOR WALL, 1/A4.01 wood siding, A0.07 XW.6.3 | 2): XW.6.3-L1-04 A / B at 4.33 LF [DERIVED 39.0 / 9]; Review Item with the delta if the exterior face carries no exterior gypsum (-121.24 SF).\n\n"
         "## Delta del Material Summary (NET) rev20b -> rev20c\n\n"
         "Regenerated from the final Excel Material Summary (etapas/DELTA_rev20b_rev20c.md, delta_rev.py: rev20c Excel vs the delivered rev20b "
         "Excel); never typed by hand.\n\n" + T3 + "\n" + ALT + sec(R20, "Entrega") + sec(R20, "Errores") + "\n")
    open(f'{W}/{f}', 'w', encoding='utf-8').write(t)
    print(f, 'filas delta:', T3.count('\n') - 1)
