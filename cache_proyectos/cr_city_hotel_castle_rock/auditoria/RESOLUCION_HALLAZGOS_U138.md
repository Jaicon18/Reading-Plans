# Resolución de los hallazgos de la auditoría adversarial U-138 — CR City Hotel rev1

Informe del auditor: `INFORME_AUDITORIA_U138.md` (auditor independiente, no hizo el take-off). Cada hallazgo se verificó en el plano antes de aplicarlo.

| # | Sev. | Hallazgo | Verificación | Acción aplicada |
|---|---|---|---|---|
| 1 | ALTA | Falta FS-1 bajo el piso de Level 2 (cielo de L1) | A0.08 FS-1 "LEVEL 2, 3, 4 THROUGHOUT / 1 HOUR / L546" [CONFIRMADO] | Ceiling "L1 FS-1 membrane": 8,587 (A0.01) − 354.5 (franja muros ext.) − 2 × 151.85 (escaleras) = 7,928.8 SF Type C + RC [DERIVADO]; hoistways no descontados (conservador) |
| 2 | ALTA | Retail 124 cargado como GYP-1 2,373 SF | A3.01 GYP-1 solo en franja 11'-0"; A2.01 nota tenant | GYP-1 del retail EXCLUDED (tenant); vigas de acero envueltas (nota A0.08 FS-1) 154.2 LF medidas en A3.01 → BW-L1-RETAIL Type C + RC; alto de lados = RFI-20 |
| 3 | ALTA | Falta cielo de campo del corridor 412 (L4) | A2.04 "1350 SF CORRIDOR 412" [CONFIRMADO] | Ceiling RS-1 1,350 SF |
| 4 | ALTA | Corner bead | A8.02 solo dibuja el lado exterior (sin casing interior) | Esquinas contra XW fuera; + perímetro de window returns (1,142 LF) + canto de soffits |
| 5 | MEDIA | Franja L3 bajo terrazas = RS-6 | A0.08 RS-6 "2 LAYERS, 5/8" TYPE 'X'" [CONFIRMADO] | RS6-L3: 427.4 SF × 2 layers Type X; restado de FS-1 de 301-304 |
| 6 | MEDIA | MB-1 en 104 / 116 | MB-1 nombra solo GENERATOR ROOM | MB-1 se mantiene en los 3 cuartos GYP-2 (conservador); alternativa con delta en RFI-13 |
| 7 | MEDIA | Walls sobre vanos de puerta | W.4-L3-44 y W.4-L4-22 verificados a ojo | Fuera (excluded_walls); vanos_puertas.py: 57 puertas dentro de tramos anotadas, NO descontadas (conservador) |
| 8 | MEDIA | F&B NOT IN SCOPE inconsistente con RFI-05 | Nota en A2.04 / A5.07 / A7.45 / A7.50 / A7.55 [CONFIRMADO] | Caras no rated hacia F&B EXCLUDED (1,818.9 SF); rated se quedan |
| 9 | MEDIA | GRAND TOTAL 0 / LF por cara | Excel | plantilla_excel (BE-CR19): LF físico una vez por wall; GRAND TOTAL al final |
| 10 | BAJA | W.4-L4-21/22 en hoja equivocada | coordenadas de 3/A7.50 | W.4-L4-21 → A7.50 1.07 ft; W.4-L4-22 = vano (fuera) |
| 11 | BAJA | Mezzanine 219 supuesto silencioso | A3.02 sin cielo | Board siguiendo la pendiente 536.7 SF sobre RC; en RFI-15 con delta |
| 12 | BAJA | Waste 0 % en compound / tape | regla BE-CF17 (yield incluye waste) | Sin cambio; explicado en README |
| 13 | BAJA | RFI-15 "hat channel" | canon RC | Texto corregido a resilient channel |
| 14 | BAJA | W.6-L1-31 cota 9'-1 1/2" vs 8.82 | −14.7 SF | Menor, sin acción (subcarga mínima, anotada) |
| 15 | BAJA | ALC-15 excluía beam wraps | nota A0.08 FS-1 | ALC-15 corregido; wraps cargados (hallazgo 2) |

Reglas nuevas para todos los proyectos: BE-CR18 … BE-CR22 (BIBLIOTECA_ERRORES), R80f.55 punto 4 (membrana del piso de arriba en el cielo de abajo).
