# POST-MORTEM U-185 — Xfinity Interquest rev1c -> rev1d (2026-11-13 19:10 UTC)

Fecha: 2026-11-13 11:10 PT
Proyecto: Xfinity Interquest (bid 13-nov). Close for U-185 = rev1d upload (SUBIDA_OK 2026-11-13T16:45 UTC). For the user, Xfinity is NOT
finished until its Bluebeam CSV comes back N/N (U-182, COORDINACIÓN 18:28).
Origin: independent adversarial audit `cache_proyectos/AUDITORIA_ADVERSARIAL_2026-11-13.md` (commit 3ed5006) over rev1c (gate v81cf114).
Fixes: rev1d (`cache_proyectos/xfinity_interquest/rev1d_2026-11-13/`, commit a779336), gate v81cf138 VERDE 230 / 12 / 0, upload 331 + --vigente PASS.
Scope (COORDINACIÓN 18:28): ONLY the new BE / U of Xfinity rev1c -> rev1d (E-1..E-4, detectors CB_RCP_TAGS / CB_BE_CF10).

## What happened (short)
1. E-1: 8/A2.0 prints the backing-zone studs AS 16 ga; the canon ADDED 10 x 12.5 = 125 LF of 362S162-54 and KEPT the same 10 positions in
   the 20 ga W2 row (its own note had the delta "-125 LF if replaced" and no RFI / decision). Over-count of 125 LF of 362S125-33.
2. E-2: 7/A2.0 head = 1 track + 1 NESTED STUD; both pieces were loaded as 362T125-33 track (8.67 LF) - the product of the 2nd piece is a stud.
3. E-3: the Proposal kept [RATE TO CONFIRM] on corner bead / L bead labor and on tax, decided by the user in U-192 (3)/(4) on 12-nov.
4. E-4: the delivery's gate ran with v81cf114 while the vigente was v81cf138 (U-177 (1)); with v114 the U-192 / U-190 checks were AMBER
   "no se re-abre" (U-180 (4)) and nobody re-ran the vigente gate before the bid.
5. I-1 / I-4: CB_RCP_TAGS and CB_BE_CF10 passed in vacuum (N/A) on a set that HAS 5 ceiling tags (A3.0) and a spec sheet (A0.3).
6. I-3: Auditoria/DOBLE_CIELO.csv missing (REGLA DE ORO #3) - AMBER retro in rev1c.

## Table (U-185)

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| XF13-E1 | 16 ga backing studs (8/A2.0) ADDED on top of the 20 ga studs of the same bays instead of REPLACING them (double count 125 LF) | none: no program check compares a printed stud gauge zone (backing detail) against the wall stud row of the same bays | none | MISSING - v140: check 'stud zone replaces wall studs' (a misc stud row with a different gauge in the bays of a wall needs a REPLACE deduction or a written decision with N/HOJA) |
| XF13-E2 | 7/A2.0 nested stud loaded as track (product of each header piece = printed, U-177 (4)) | CE_MS_PRODUCTO_IMPRESO / CB U-177 only look at the row name, not at each printed piece of a head detail | none | WEAK - v140: headers with a 'pieces' list [{product printed, N/HOJA}] and a check that the track / stud split matches the detail text |
| XF13-E3 | Proposal [RATE TO CONFIRM] in rows decided by U-192 (3)/(4) | CE_PROPOSAL / revisar_proposal (U-192: (2)(3)(4) in [RATE TO CONFIRM] = FAIL, since v81cf113) | test of revisar_proposal (U-192) in the suite | OK - the program existed; rev1c's gate ran with v81cf114 before it applied (U-180 (4)); rev1d with v81cf138 = CE_PROPOSAL PASS, revisar_proposal 0 faltas |
| XF13-E4 | final gate with an old skill version before the bid (U-177 (1)) | CE_VERSION_ENTREGA + subir_entrega --vigente | existing tests (U-177) | WEAK - the lock exists but only fires when someone re-runs the gate / --vigente; no alarm when a NEW vigente is published while a delivery is open (v140: CE / verificar_version alarm 'entrega abierta con gate de una versión anterior a la vigente') |
| XF13-I1 | CB_RCP_TAGS blind to DESCRIPTIVE tags ("2x4 ACT 12'-0\" AFF", "GYP. BD. 8'-6\" AFF") and to an RCP title split by a newline | CB_RCP_TAGS (tags_cielo / RX_HOJA_RCP) | apartados/v81cf140_wip/detectores_xf/test_v140_detectores_xf.py (FAILS with v81cf138a = reproduces) | MISSING - fix in v140; rev1d carries the 6 tag assignments in canon.rcp_tags from the independent review R_A3 |
| XF13-I3 | Auditoria/DOBLE_CIELO.csv missing (U-190 REGLA DE ORO #3) | CE_DOBLE_CIELO | existing U-190 tests | OK - rev1d has the CSV (independent review R_A3), CE_DOBLE_CIELO PASS |
| XF13-I4 | CB_BE_CF10 blind to an outline SPECIFICATIONS sheet without CSI numbers (A0.3) | CB_BE_CF10 | test_v140_detectores_xf.py | MISSING - fix in v140; rev1d: A0.3 vs Material Summary by hand in R_A3 (0 MISMATCH) |
| XF13-I5 | CE_DOBLE_CIELO cuartos_rcp reads stud designations ('162', '600') and hardware ('200D') as rooms | CE_DOBLE_CIELO (cuartos_rcp) | none | WEAK - v140: filter designations / hardware out of the room list (rev1d: 3 'not a room' rows) |
| XF13-C1 | v81cf138 plantilla_excel R80w.48 stopped the chain: a row citing only a listing (GA-216 moved to 'Listing:' in v81cf116) = 'N/SHEET: default (no sheet)' | plantilla_excel verificar (R80w.48) | existing | OK - the lock worked (it stopped the chain); rev1d: fasteners_excluded cites 3/A2.0, 4/A2.0, 8/A2.0 |

## Causes (no guard)

| # | causa | candado | estado |
|---|---|---|---|
| 1 | A conservative choice ("keep the 20 ga, delta in the note") was left without RFI / decision although the plan prints the answer (U-116 / U-052) | XF13-E1 check (v140) | NO GUARD hasta v140 |
| 2 | Detectors that return N/A on an unexpected text format pass in vacuum (U-137) | XF13-I1 / XF13-I4 fixes + 'RCP sheet with AFF heights and 0 tags = AMBER' (v140) | NO GUARD hasta v140 |
