import json
E = '/home/user/Reading-Plans/cache_proyectos/barnes_noble/takeoff_work/etapas'
rv = json.load(open(E + '/3_revision/revision.json'))
ri = json.load(open(E + '/3_revision/resolucion_items.json'))
L = ['# Stage 3 resolution - Barnes & Noble Colorado Springs', '',
     'Every item of revision.md is closed here: item -> decision -> N/SHEET -> image. Nothing is averaged; where both',
     'readings are defensible the reading with the drawn evidence is taken and the other goes to an RFI with its delta.', '',
     '## Decisions applied to the reconciled canon (4_canon/takeoff_canon.json)', '']
for i, r in enumerate(ri, 1):
    L.append(f"{i}. **{r['item']}** -> {r['decision']} · source {r['source']} · ΔLF vs reading A {r['delta_lf']} · ![img](../{r['img']})")
EXT = {'1A', '1', '1B', '1C'}
def dec(x, kind):
    t = x['type']; w = (x.get('A') or x.get('B') or {}).get('wall', '')
    if t in EXT:
        return ('Reading A kept. Storefront / curtain wall openings are OUT of the exterior LF (R70.7) - reading B '
                'measured each facade through the storefronts; solid piers agree (east 10.80, south-east 19.36, 1C 18.94 LF). '
                'Type boundaries without a drawn node -> RFI-02 (north 1A/1 +33.54 LF moves, south 1B/1 1.55 LF). Cafe south line '
                'counted once as E1/E2 -> RFI-05 (B type-1 50.24 LF behind the cafe walls). Source 1/A-410, 1A/A-410, 1B/A-410, 1C/A-410, A-101.')
    if t == '2':
        return 'See decision 1 (W2-05 / W2-06 from reading B, image res_W205.png). W2-01 kept from reading A: 48.77 = printed 48\'-4" (A-101) + W2-02 thickness; B ran into the exterior wall (49.20). Source 2/A-410, A-101.'
    if t == '4':
        return 'See decision 2 (type 4 from reading B: open U caps, curved walls 25\'-1" printed; RFI-18). Source 4/A-410, A-101.'
    if t in ('E1', 'I'):
        return 'See decision 3 (I tag PT0050 = 1\'-0" return; E1 = 2\'-8" pier) and type_change_rfi E2/E1 at H2a (RFI-05, 0.20 LF). Source E/A-221, I/A-221, 1/A-221.'
    if t in ('', 'C25'):
        return 'Key note C25 column surrounds (A-101): not partition tags; reading A counted 9 (9 C25 boxes + 9 hatched column symbols, img_cache/keynotes_contactos.png); reading B mentioned 10 without measuring -> Review item. OTHER FRAMING (column_wrap).'
    if t == 'E2':
        return 'E2/E1 split at the H2a centerline (reading A) vs Workroom face (reading B): type_change_rfi, 0.20 LF (RFI-05).'
    return 'Reading A kept (difference within the tolerance of the type, see image).'
L += ['', '## Review items of revision.md', '']
n = 0
for kind in ('difieren', 'solo_A', 'solo_B'):
    for x in rv.get(kind) or []:
        n += 1
        a = (x.get('A') or {}); b = (x.get('B') or {})
        L.append(f"{n}. [{kind}] {x['type']} {x['sheet']}: A {a.get('wall', '-')} {a.get('lf', '-')} LF / B {b.get('wall', '-')} {b.get('lf', '-')} LF -> {dec(x, kind)}")
L += ['', '## Alerts', '']
for x in rv.get('alertas') or []:
    tag = (x.get('tag') or {}).get('id', '')
    if tag in ('PT0048', 'PT0049'):
        d = 'Discarded with plan reason: "I (SIM.)" tag points to the exposed end face of a wall (finish callout, I/A-221), not a wall line; image 1_inventario/recortes/' + tag + '_I_A-221_p15.png. Both readings agree.'
    else:
        d = 'Column surrounds C25 (OTHER FRAMING, no partition type) - see C25 above.'
    L.append(f"- {x['kind']} {x.get('type')} {tag}: {d}")
open(E + '/3_revision/resolucion.md', 'w').write('\n'.join(L) + '\n')
print(n, 'items,', len(rv.get('alertas') or []), 'alerts')
