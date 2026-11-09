"""rev13 (auditoría diaria U-138 de COORDINACIÓN sobre rev12, 9-nov), verificada en el plano:
E1 (U-058): cara EXTERIOR con la altura de la línea del board INTERIOR.
  - Mezzanine 219 (2/A5.04, 27 pt/ft): el sheathing exterior (líneas x 609.24 / 610.68 / 612.12) sube hasta y 1006.2 y baja a 1185.48
    -> (1185.48 - 1006.2) / 27 = 6.64 ft; la línea interior x 627.4 para en 1026.1 (5.915). Gable este: 6.64 + 2.733 / 2 = 8.0065.
  - Pilares del retail en grid 7 (L1, cara courtyard): el sheathing exterior pasa la zona del piso (rebanada por piso = piso a piso
    14'-0", LEVEL 1 6197.75' / LEVEL 2 6211.75'), como XW.6.3-L1-03 A; 12'-0" B.O. DECK de 5/A5.04 es la cara interior.
RS (A0.08 / A2.05): disposición real de cada roof assembly (antes 'not tagged on any plan', falso)."""
import json, re
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP)); IDX = {w['id']: w for w in c['walls'] + c['existing_walls']}
EAVE = ("DERIVED: 2/A5.04 (27 pt/ft) exterior sheathing line x=610.68 from the mezzanine floor 1185.48 to the top of the sheathing "
        "under the roof edge 1006.2: (1185.48-1006.2)/27 = 6.64 ft; the interior board line x=627.4 stops lower, at 1026.1")
GABLE = ("DERIVED: 2/A5.04 exterior sheathing at the eave 6.64 ft (line x=610.68, (1185.48-1006.2)/27) + half the rise of the sloped roof line "
         "(1026.1-952.3)/27 = 2.733 ft -> gable average 6.64 + 2.733/2 = 8.0065 ft (equivalent rectangle)")
L1F = ("LEVEL 2 6211.75' - LEVEL 1 6197.75' = 14'-0\" printed on A5.08 / A4.04: exterior gyp sheathing passes the floor zone "
       "(per-floor slice = floor to floor, as XW.6.3-L1-03 A); the 12'-0\" B.O. DECK of 5/A5.04 is the interior face")
CAMBIOS = {'XW.6.4-L2-01 A': (6.64, EAVE), 'XW.6.3-L2-12 A': (6.64, EAVE), 'XW.6.4-L2-02 A': (8.0065, GABLE),
           'XW.6.4-L1-01 A': (14.0, L1F), 'XW.6.4-L1-02 A': (14.0, L1F), 'XW.6.4-L1-05 A': (14.0, L1F)}
dsf = 0.0
for i, (h, src) in CAMBIOS.items():
    w = IDX[i]
    if abs(float(w['height_ft']) - h) < 0.001:
        continue
    d = float(w['length_ft']) * (h - float(w['height_ft'])) * int(w.get('faces') or 1) * int(w.get('layers') or 1)
    dsf += d
    print('E1', i, w['height_ft'], '->', h, round(d, 2))
    w['height_ft'] = h; w['height_status'] = 'DERIVADO'; w['height_source'] = src; w['height_note'] = src
    w['source'] = re.sub(r"\| height: [^|]*", "", str(w['source'])) + f" | height: {src}"
    w['height_img'] = '/root/cr/work/etapas/4_canon/img/rev13/E1_2A504_sheathing.png' if h < 10 else w.get('height_img')
print('E1 total', round(dsf, 2), 'SF exterior sheathing')
RS = {
 'RS-1': "LOADED: A2.05 tags RS-1 x3 (L4 roof over the guest rooms / corridor 412); A0.08 RS-1 ceiling 'RE: REFLECTED CEILING PLANS' -> ceilings[] 'RS-1' rows of L4 (A3.04)",
 'RS-2': "A2.05 tags RS-2 x3 (sloped roofs); A0.08 RS-2 has no board of its own: 'CEILING. RE: REFLECTED CEILING PLANS' -> the ceiling rows of the rooms below (A3.0x RCP)",
 'RS-3': "A2.05 tags RS-3 x2 (steep roof); A0.08 RS-3 = roof sheathing on wood framing, no gypsum in the assembly",
 'RS-4': "A2.05 tags RS-4 x1 (Deck Bar 411 roof / brow); A0.08 RS-4 'CEILING ASSEMBLY - TBD'; A7.55 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' -> no ceiling row (future TI)",
 'RS-5': "A2.05 tags RS-5 x2 (low roofs on metal deck); A0.08 RS-5 = membrane roofing / tapered insulation / METAL DECK, no gypsum in the assembly (the rooms below carry their RCP ceiling rows)",
 'RS-6': "LOADED: A2.05 tags RS-6 x2 (L4 terrace 420 / 421 over L3 301-304 and the covered deck east of 411 over L3 309); A0.08 RS-6 '2 LAYERS, 5/8\" TYPE 'X' GYP BOARD' -> rows 'RS6-L3 board' and 'RS6-L3-309 board' (RS-6)",
 'RS-7': "A2.05 tags RS-7 x1; A0.08 RS-7 = steel roof tile / spray foam / batt, no gypsum in the assembly",
 'FS-1': "LOADED: A0.08 FS-1 (5/8\" Type C on resilient channel, UL L546) -> ceilings[] 'FS-1' rows of L1-L3 and the L1 FS-1 membrane",
 'FS-1 (L2 alley)': "LOADED with FS-1 (same A0.08 assembly)",
 'MB-1': "LOADED: A0.08 MB-1 2-HR membrane at L1 Generator 103 / Elec 104 / Elevator Controls 116 (RFI-13)"}
tnr = c.setdefault('types_none_reason', {})
for k, v in RS.items():
    if k in tnr or k.startswith('RS-'):
        tnr[k] = v
json.dump(c, open(CP, 'w'), indent=1)
