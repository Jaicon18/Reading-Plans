# v81cf138 rev2 — FROZEN candidate (unpublished)

Order from COORDINACIÓN 13-nov 12:33: v138 rev2 = ONLY 3 fixes over v81cf137. BE-XF18 and the CE_COBERTURA_DIAG filters go
out, to v139, together with fixes (1) and (5) from verification 8 (saved in `apartados/v81cf139_wip/desde_verif8/`).

Patch: `v81cf138r2_desde_v81cf137.patch` (applies over the published v81cf137 zip).

| fix | what changes | verification 8 adversarial case as a test |
|---|---|---|
| CB_BE_CF04 | wood written any way ('2 X 6', DF stud, Douglas fir, SPF, timber) in stud_size / gauge / framing; evidence without '0 walls' (U-138) | test_v138_cf04_wood_board_only_plausible (VERDE in verif. 8, unchanged) |
| CB_BE_83 | numeric `faces` (crash in CR) -> one face with the wall's location; justification ONLY in the face's own clause (`sube_justificado_clausula`); a LIST of faces = exactly v137; walls WITHOUT `faces` / dict = not judged (like v137: the 2 BoA false positives go away) | test_v138_be83_faces_numero, test_v138r2_verif8_caras_lista_como_v137 (A1-A4, B2, B10), test_v138r2_caras_numero_clausula_propia |
| CE_PROTOCOLO_3H | `filas_tiempos` returns `linea`; start = the EARLIEST of log / VERSION_PROYECTO / git; a row is exempt (previous rev) only if it closes before the start AND tiempos.log has the mark of that close before the start; the exact row is removed, never by time coincidence; a log that can't be dated = FAIL like v137 | test_v138_protocolo_rev_posterior_solo_sus_pasos, test_v138r2_verif8_tiempos_desde_pruebas (Q1b, Q4), test_v138r2_protocolo_log_sin_fecha_como_v137 (Q2) |

Registry: BE-XF18 goes in as `programa-pendiente` with its reason (the program arrives in v139; CR uses entrega.json 'markups',
which v137 respects). verificar_version: faltan 0.

Verification 9 = adversarial ONLY on this diff, max 30 min.
