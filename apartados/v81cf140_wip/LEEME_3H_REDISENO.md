# v140 — CE_PROTOCOLO_3H redesign (COORDINACIÓN 13-nov 15:31) — DO NOT START until COORDINACIÓN calls

v139 (strict 3H, 9897cf6) parked unpublished after verification 13 (W2 / X1 / G / Y). Do not infer evidence again.
Design: every TIEMPOS.md row and every tiempos.log mark carries an explicit rev label WRITTEN BY THE TOOL when it's created (not by hand);
CE_PROTOCOLO_3H judges only the rows / marks of the current rev. Old rows without a label = judged as in v137 (no exemption).
Material: apartados/v81cf139_final (patch + tests verif. 8-13), cache_proyectos/VERIFICACION8..13*.md, apartados/verif8..13_adversariales.
Also pending for v140: BE-XF18 + COBDIAG (apartados/v81cf139_wip/desde_verif8), post-mortem STILL-WEAK, BE-CR44 program check (0-byte log + no process at 5 min = ALARMA).

Also for v140 (verification 2 of v81cf138a, cache_proyectos/VERIFICACION_v81cf138a_subida_2.md, low severity): excepcion_usuario_fallas —
R1 README sections by Markdown parsing (indented / setext headings, comments, code blocks); R2 texto without padding (>= 30 visible
characters); R3 fecha with ASCII digits and a valid calendar date; R4 duplicate check ids in ENTREGA_OK = refuse.

BE-CR45 (CR rev20d, COORDINACIÓN 19:55 / 20:01; commit 77d8d06): the cement board / tile rule runs by program over the FINAL canon, after EVERY loaded face
(including later revs and FALTA); NON-rated type = cement board REPLACES the board and the band H - cement board height remains; rated type = layers stay and
the cement board goes on top; the cement board markup goes on the real shower face (line nearest to the shower pan box), same id / NM. Check CB_DUCHA_CBU =
the CR test (cache_proyectos/cr_city_hotel_castle_rock/scripts/tests/test_ducha_cbu.py + test_be_cr45.sh, fixtures rev20c -> 6 (a) + 6 (b) rc 1; rev20d -> 0) over
the delivery's canon, FAIL with the list.
