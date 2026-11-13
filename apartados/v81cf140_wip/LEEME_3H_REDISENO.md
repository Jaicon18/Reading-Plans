# v140 — CE_PROTOCOLO_3H redesign (COORDINACIÓN 13-nov 15:31) — DO NOT START until COORDINACIÓN calls

v139 (strict 3H, 9897cf6) parked unpublished after verification 13 (W2 / X1 / G / Y). Do not infer evidence again.
Design: every TIEMPOS.md row and every tiempos.log mark carries an explicit rev label WRITTEN BY THE TOOL when it's created (not by hand);
CE_PROTOCOLO_3H judges only the rows / marks of the current rev. Old rows without a label = judged as in v137 (no exemption).
Material: apartados/v81cf139_final (patch + tests verif. 8-13), cache_proyectos/VERIFICACION8..13*.md, apartados/verif8..13_adversariales.
Also pending for v140: BE-XF18 + COBDIAG (apartados/v81cf139_wip/desde_verif8), post-mortem STILL-WEAK, BE-CR44 program check (0-byte log + no process at 5 min = ALARMA).

Also for v140 (verification 2 of v81cf138a, cache_proyectos/VERIFICACION_v81cf138a_subida_2.md, low severity): excepcion_usuario_fallas —
R1 README sections by Markdown parsing (indented / setext headings, comments, code blocks); R2 texto without padding (>= 30 visible
characters); R3 fecha with ASCII digits and a valid calendar date; R4 duplicate check ids in ENTREGA_OK = refuse.
