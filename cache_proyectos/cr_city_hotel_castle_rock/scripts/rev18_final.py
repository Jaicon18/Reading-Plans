"""rev18 FINAL (respuestas del usuario 11-nov, U-161 / U-162 / U-163): todo RFI cerrado.
RFI-04 / RFI-24 'A: 2 HR (cargado)' -> DA-6 / DA-2 dejan de ser deduct alternates (decisión del usuario, nota de ambas hojas);
RFI-21 'A: Nuestro (cargado)'; RFI-17 (U-162): 1/A3.01 no marca cielo en 128 y el código no lo pide -> fuera CLG-L1-10, EXCLUDED en 128;
RFI-13 / RFI-29 (U-163): solo gypsum board + metal framing (MB-1 como está); fireproofing / steel support platform EXCLUDED."""
import json
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP)); LOG = []
dec = [d for d in c.get('deduct_alternates') or [] if d.get('id') in ('DA-2', 'DA-6')]
if dec:
    c['deduct_alternates'] = [d for d in c['deduct_alternates'] if d.get('id') not in ('DA-2', 'DA-6')]
    for d in dec:
        d['decision'] = f"user decision 11-nov ({d['rfi']} 'A: 2 HR (cargado)', U-161): 2 HR loaded; the 1 HR reading of the sheet is not an alternate"
    c['decisiones_usuario_da'] = dec
    LOG.append("DA-2 / DA-6 -> user decision 11-nov (2 HR loaded), no longer deduct alternates")
fuera = [m for m in c['misc_items'] if m['ref'].startswith('CLG-L1-10 ')]
if fuera:
    c['misc_items'] = [m for m in c['misc_items'] if m not in fuera]
    LOG.append("CLG-L1-10 (WATER ENTRY 128) removed: " + ", ".join(f"{m['ref'].split(' ', 1)[1]} -{m['qty']}" for m in fuera))
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'; T = json.load(open(TP))
if not any(r['sheet'] == 'A3.01' and r['room'] == '128' for r in T['rooms']):
    P = json.load(open(f'{W}/etapas/4_canon/rev9/contornos_MISC.json'))['CLG-L1-10']
    P = (P.get('polygons_final') or [P['polygon']])[0]; dx, dy = json.load(open(f'{W}/etapas/6_markups/offset_plan_rcp.json'))['L1']
    P = [[round(q[0] + dx, 2), round(q[1] + dy, 2)] for q in P]
    rs = "no ceiling printed on 1/A3.01; not required by IBC 2018 Section 913.2.1 exc. 1 (user decision 11-nov, RFI-17)"
    T['rooms'].append({"sheet": "A3.01", "room": "128", "name": "WATER ENTRY", "disposition": "exclusion", "rows": [], "nhoja": "1/A3.01",
                       "reason": rs, "reason_short": rs, "polygon": P, "area_sf": 188.01,
                       "label_xy": [round(sum(q[0] for q in P) / len(P), 1), round(sum(q[1] for q in P) / len(P), 1)]})
    json.dump(T, open(TP, 'w'), indent=1)
    LOG.append("A3.01 128: EXCLUDED (no ceiling printed; IBC 2018 913.2.1 exc. 1)")
c['rev18_cambios'] = LOG
json.dump(c, open(CP, 'w'), indent=1)
print("\n".join(LOG))
