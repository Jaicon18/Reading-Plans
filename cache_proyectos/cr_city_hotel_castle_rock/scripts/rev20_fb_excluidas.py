"""CR City Hotel rev20 (rev20b: polígono = la franja del muro entre sus dos caras dibujadas, y 408.8 / 418.9, CE_RCP_CONTORNO >= 60 %)\nCR City Hotel rev20 (COORDINACIÓN 12-nov, U-160): las caras F&B excluidas (non-rated, nota impresa 'INTERIOR OF FOOD AND BEVERAGE
SPACE IS NOT IN SCOPE OF THIS PERMIT') llevan markup EXCLUDED. Kitchen 100 (1/A7.45) y 419 (3/A7.50) ya tienen su polígono de cuarto;
faltaban las caras de W.6-L1-04 (lado Kitchen 100, norte del muro de arcos) y W.6-L1-32 (lado Bar 107, dentro de la L) en 1/A7.30.
Polígono = la zona del cuarto excluido pegada a la cara (coordenadas de A7.30 tal como se ve; muro medido en vectores: W.6-L1-04
y = 413.8, x 1110.2-1780.3; W.6-L1-32 x = 1938.1 y 373.6-413.8 + y = 413.8 x 1877.9-1938.1). Idempotente."""
import json

P = '/root/cr/work/etapas/4_canon/rev14/rcp_cuartos.json'
R = json.load(open(P))
R['rooms'] = [r for r in R.get('rooms') or [] if not r.get('rev20_fb')]
NOTA = "'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT'"
R['rooms'] += [
    {"sheet": "A7.30", "room": "100 (W.6-L1-04 N face)", "name": "KITCHEN 100", "disposition": "exclusion", "rows": [], "rev20_fb": True,
     "reason": "F&B (not in scope of this permit): Kitchen 100 face of W.6-L1-04, W.6-0 non-rated", "nhoja": "1/A7.30",
     "polygon": [[1110.0, 408.8], [1780.0, 408.8], [1780.0, 418.9], [1110.0, 418.9]], "label_xy": [1445, 414]},
    {"sheet": "A7.30", "room": "107 (W.6-L1-32 bar face)", "name": "BAR 107", "disposition": "exclusion", "rows": [], "rev20_fb": True,
     "reason": "F&B: Bar 107 face of W.6-L1-32", "nhoja": "1/A7.30",
     "polygon": [[1878.0, 408.8], [1933.0, 408.8], [1933.0, 374.0], [1943.2, 374.0], [1943.2, 418.9], [1878.0, 418.9]], "label_xy": [1905, 414]},
]
json.dump(R, open(P, 'w'), indent=1)
print("F&B caras EXCLUDED en A7.30: 2 (W.6-L1-04 Kitchen 100, W.6-L1-32 Bar 107)")
