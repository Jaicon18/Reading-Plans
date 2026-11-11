"""R-ALC-06 / BE-VS-08: demolition plans A108 / A109 vs the new plans A111 / A112 / A113, element by element, from the
demolition reading (2_lectura/A/DEMO.json 'cross_check_new_plan') + final height (U-176). Writes etapas/DEMO_CRUCE.md. Text only."""
import json
W = '/root/gk/work'
D = json.load(open(f'{W}/etapas/2_lectura/A/DEMO.json'))['demo_walls']
G = {g['id']: g for g in json.load(open(f'{W}/etapas/4_canon/demo_geom_out.json'))}
L = ["# DEMO_CRUCE - A108 / A109 demolition vs A111 / A112 / A113 new plans (element by element)", "",
     "Each existing wall to demolish (keynote on A108 / A109) was crossed with the new plan of the same area by the demolition reader; "
     "the height is the U-176 final table (two blind readings + directed resolution).", "",
     "| Demo element | Sheet | Keynote | LF | H (ft) | SF | Cross-check with the new plan |", "|---|---|---|---|---|---|---|"]
for d in D:
    g = G.get(d['id'], {})
    L.append(f"| {d['id']} | {d.get('sheet')} | {d.get('keynote')} | {g.get('lf', d.get('length_ft'))} | {g.get('h_ft')} | {g.get('sf')} | "
             f"{str(d.get('cross_check_new_plan') or 'no new wall on this line')[:220]} |")
open(f'{W}/etapas/DEMO_CRUCE.md', 'w').write("\n".join(L) + "\n")
print(len(D))
