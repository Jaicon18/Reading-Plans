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
    open(p, 'w', encoding='utf-8').write(s)
    print(f, 'RC row:', [l for l in s.splitlines() if l.startswith('| Resilient channel 1/2"')][:1])
