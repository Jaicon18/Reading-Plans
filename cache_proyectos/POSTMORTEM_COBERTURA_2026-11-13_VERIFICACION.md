# VERIFICACION — POSTMORTEM 2026-11-13 (Xfinity rev1c -> rev1d)
Fecha: 2026-11-13 11:11 PT

Reviewer: Claude (Opus 5.5), independent reviewer. I did not do the take-off, rev1d, R_A3 or the post-mortem. I worked read-only: nothing in the
delivery, the scripts, the tools or the post-mortem was changed, and nothing was committed. Python was run with `python3 -I`.
Verified: `cache_proyectos/POSTMORTEM_COBERTURA_2026-11-13.md` (commit 638562f), against the audit `AUDITORIA_ADVERSARIAL_2026-11-13.md`,
the rev1d record `xfinity_interquest/rev1d_2026-11-13/` (commit a779336), the rev1c backup `/root/xf/work_rev1c_bak/`, the rev1d delivery
`/root/xf/work/entrega/rev1 FINAL PARA REVISAR/`, the tools at `/tmp/v1381/take-off-metal-frame-drywall/tools` (SKILL.md VERSION v81cf138a) and
`apartados/v81cf140_wip/detectores_xf/test_v140_detectores_xf.py`.
Scope: only E-1..E-4 and I-1..I-5 of the audit's Xfinity section, plus the post-mortem's C1.

## Table (verdicts)

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| XF13-E1 | 16 ga backing studs (8/A2.0) ADDED on top of the 20 ga studs of the same bays (double count 125 LF 362S125-33) | none (grep of tools/ for a stud-zone REPLACE / gauge-zone check: 0 hits) | none | CONFIRMED-OPEN - the error is real (rev1c MS 362S125-33 250.67 LF, 362S162-54 125 LF). It was fixed through the chain (resolver.py misc STUD20-GF-REPLACED -125 LF; rev1d MS 130.00 LF). No program check and no test guard it. |
| XF13-E2 | 7/A2.0 nested stud loaded as track (header 2 pieces as 362T125-33) | CE_MS_PRODUCTO_IMPRESO only checks the row name, and it PASSed on rev1c with the error present | none | CONFIRMED-OPEN - closer to MISSING than WEAK. The error is real (rev1c Header 362T125-33 8.67 LF = (3.0+1.333) x 2). It was fixed through the chain (pieces 1 + misc HDR-101-NESTED 4.33 LF; rev1d Header 4.33 LF). headers.py has one `piece` per header, not a per-piece product list, and no check would catch a repeat. |
| XF13-E3 | Proposal [RATE TO CONFIRM] in rows decided by U-192 (3)/(4) | compuerta_entrega.py u192_fallas (l.302), called by revisar_proposal (l.341) -> CE_PROPOSAL | test_chequeos_biblioteca.py test_u192_tasas_decididas (l.1170), PASS on v138a | OK - CONFIRMED-CLOSED. u192_fallas = 3 faults on the rev1c Proposal and 0 on rev1d; rev1d CE_PROPOSAL PASS. Correction to the post-mortem's wording: v81cf114 already contained U-192. The rev1c check DID detect the problem, but U-180 (4) "no se re-abre" turned it into AMBER. The rule did exist when rev1c's gate ran. |
| XF13-E4 | final gate with an old skill version before the bid (U-177 (1)) | CE_VERSION_ENTREGA + vigente_fallas / subir_entrega --vigente; prueba_abiertos (before publishing) | test_compuerta_entrega.py (l.1341-1388, 2206, 2707, 3304), PASS | CONFIRMED-OPEN (WEAK). The error is real: rev1c ENTREGA_OK skill_version v81cf114, CE_VERSION_ENTREGA PASS. The fix is real: rev1d ENTREGA_OK v81cf138 VERDE 230/12/0. No current check guards it. See note E-4. |
| XF13-I1 | CB_RCP_TAGS blind to DESCRIPTIVE tags and to an RCP title split by a newline | CB_RCP_TAGS (chequeos_biblioteca.py tags_cielo / RX_HOJA_RCP) | test_v140_detectores_xf.py: FAILS on v81cf138a (reproduces). It is WIP, not part of the tools suite. | CONFIRMED-OPEN - both sub-cases reproduce on v138a (PASS "N/A"). It is still blind in rev1d itself: rev1d ENTREGA_OK CB_RCP_TAGS = PASS "N/A: ninguna hoja de RCP con tags de cielo impresos" although canon.rcp_tags now has 6 entries. |
| XF13-I2 (NEW, missing from the post-mortem) | Audit I-2: CB_RCP_APILADOS passed in vacuum ("N/A: sin rcp_tags"), carried over from I-1 | CB_RCP_APILADOS (vacuum = FAIL since BE-AUD06) | test_compuerta_entrega.py l.2203-2222 / 2632-2651 (vacuum = FAIL), PASS | WEAK - in rev1d the check now sees the vacuum but only reports AMBER (U-180 (4)): "6 rcp_tags y 27 renglones de DOBLE_CIELO.csv, pero 0 cuartos evaluados". The descriptive tags / SOF-01 misc rows do not match any room. Quantity impact 0 (no double ceiling, R_A3), but the post-mortem has no row for it and it remains unevaluated. |
| XF13-I3 | Auditoria/DOBLE_CIELO.csv missing (U-190 REGLA DE ORO #3) | CE_DOBLE_CIELO (doble_cielo_fallas) | test_compuerta_entrega.py l.1933-1972 ("falta Auditoria/DOBLE_CIELO.csv" = FAIL), PASS | OK - CONFIRMED-CLOSED. rev1c: AMBER "falta Auditoria/DOBLE_CIELO.csv" (U-180 (4) only). rev1d: CSV present (armar_entrega.sh copies R_A3/DOBLE_CIELO.csv), CE_DOBLE_CIELO PASS. Caveat: the PASS relies on 3 "not a room" rows that work around I-5. |
| XF13-I4 | CB_BE_CF10 blind to an outline SPECIFICATIONS sheet without CSI numbers (A0.3) | CB_BE_CF10 (be_cf10) | test_v140_detectores_xf.py: FAILS on v138a (reproduces). It is WIP, not part of the tools suite. | CONFIRMED-OPEN - be_cf10 on the A0.3 text returns PASS "N/A: el set no trae specs del trade". rev1d ENTREGA_OK CB_BE_CF10 is still "N/A". The only cover is the manual R_A3/A0.3_SPECS_vs_MS.md (0 MISMATCH). |
| XF13-I5 | CE_DOBLE_CIELO cuartos_rcp reads designations ('162', '600') and hardware ('200D') as rooms | cuartos_rcp (compuerta_entrega.py l.3061, RX_CUARTO l.3058 `^\s*(\d{3}[A-Z]?)\s*$`) | none (test_u159_u160_rcp_cuartos l.1131 does not cover designations / hardware) | CONFIRMED-OPEN - reproduced: cuartos_rcp returns ['101','162','600'] and ['200D']. rev1d carries 3 workaround rows. Note: this is NOT the audit's I-5, which is the version item and is covered by XF13-E4. It is an R_A3 side-finding. The id overlaps. |
| XF13-C1 | plantilla_excel R80w.48 stopped the chain ('N/SHEET: default (no sheet)' on a listing-only row) | plantilla_excel.py verificar_excel (l.1509, R80w.48) | test_no_sheet_and_misc_product.py, PASS on v138a | OK - CONFIRMED-CLOSED. The lock worked. The fix is in the chain (resolver.py: fasteners_excluded source cites 3/A2.0, 4/A2.0, 8/A2.0). |

## Notes / evidence

**rev1c vs rev1d numbers.** The values come from the Material Summary of
`/root/xf/work_rev1c_bak/entrega/rev1 FINAL PARA REVISAR/Take-off/XF_Takeoff_FINAL_rev1.xlsx` and of the rev1d delivery Excel.
- 362S125-33: 250.67 LF ("W2-01 185.67 + W2-02 50 + SOF-01-STUDS 15", 21 sticks) -> 130.00 LF ("... + STUD20-GF-REPLACED -125 + ... + HDR-101-NESTED 4.33", 11 sticks).
  This matches the task's expected 250.67 -> 130.00. The audit's "≈125.67" is before E-2; 125.67 + 4.33 = 130.00.
- 362S162-54: 125 LF (STUD16-GF) in both. That matches the expected 125.
- Header 362T125-33: 8.67 LF "(3.0 + 1.333) x 2 pieces" -> 4.33 LF "x 1 pieces". The 4.33 LF nested stud sits in the 362S125-33 row. This matches E-2.
- All other rows checked (tracks 17.97, ceiling track 16.99, brace 95.46) are unchanged.

**Chain, not by hand.**
- `scripts/rev1c_a_rev1d.diff` changes resolver.py:
  - STUD20-GF-REPLACED (-125.0 LF);
  - header pieces 2 -> 1 + HDR-101-NESTED;
  - fasteners_excluded source;
  - canon.rcp_tags from R_A3/RCP_TAGS_A3.0.csv.
- It also changes formato.py (product map), armar_entrega.sh (copies DOBLE_CIELO.csv) and armar_proposal.py (corner bead labor folded into taping, tax label U-192 (4)).
- The record's resolver.py and formato.py are byte-identical to `/root/xf/work/scripts/`.
- The delivered Excel sha256 c9cda108… = `etapas/8_excel` chain output = ENTREGA_OK `vigentes.excel`. The bitácora ends with SELLO entries at 16:39 UTC.

**Tests run on v81cf138a.**
- `python3 -I test_v140_detectores_xf.py <tools>` -> rc 1, AssertionError at the first assert: CB_RCP_TAGS ('PASS', ['N/A: ninguna hoja de RCP con tags de cielo impresos']).
- The script stops at its first assert, so I ran each case separately in a scratch harness, without editing the test:
  - descriptive tags: PASS N/A (blind);
  - split title "REFLECTED\nCEILING PLAN" + GYP-1: PASS N/A (blind);
  - control, one-line title + GYP-1: FAIL (works);
  - A0.3 for be_cf10: PASS N/A (blind);
  - cuartos_rcp: {'A3.0': ['101','162','600'], 'A2.0': ['200D']}.
- test_chequeos_biblioteca.py rc 0; test_compuerta_entrega.py rc 0 (127 OK); test_no_sheet_and_misc_product.py rc 0.

**E-4 detail (why WEAK / open).**
- `ce_version_entrega` only compares SKILL.md VERSION with the docs of the delivery and with the running gate. So rev1c's v114 gate PASSed it by construction.
- `vigente_fallas` (l.4690) accepts an older green ENTREGA_OK through `entrega_ok_anterior_valida` (v131) when it was green with the version vigente at that moment. `VERSIONES_CAMBIAN_CANTIDADES` is the empty set (l.1753), so a newer vigente alone never re-opens a delivery.
- `prueba_abiertos` (l.5119; xfinity_interquest is in PROYECTOS_ABIERTOS.json) flags only PASS/AMBER -> FAIL regressions. An AMBER under both versions (CE_PROPOSAL) raises nothing.
- The post-mortem's "no alarm while a delivery is open" is therefore correct. It should also name prueba_abiertos as the partial guard that exists today.

**Gaps in the post-mortem.**
1. **Missing row: audit I-2 (CB_RCP_APILADOS in vacuum).** I added it above as XF13-I2. It is still AMBER "en vacío" in rev1d.
2. **Id overlap.** The post-mortem's XF13-I5 (cuartos_rcp) is not the audit's I-5. The audit's I-5 (version) is covered by XF13-E4. The post-mortem should say so.
3. **E-3 wording.** The rev1c gate (v114) did have U-192. The failure was the U-180 (4) retroactive AMBER, not a missing rule.
4. **Side-finding outside the strict E/I scope.**
   - rev1d CB_FALTANTES_AUDITORIA is AMBER. It says INFORME_R_A3.md declares a ceiling item that cannot be resolved against the canon (BE-CR40 wording).
   - The audit's RFI-06 observation is open: A0.1 note 3 "CEILINGS" patch allowance is not a Scope line. The rev1d LEEME does not mention it.
   - Neither item is in the E-1..E-4 / I-1..I-5 list, so I made no row for them.

**Summary.**
- 3 OK - CONFIRMED-CLOSED: E3, I3, C1.
- 6 CONFIRMED-OPEN: E1, E2, E4, I1, I4, I5.
- 1 new row, WEAK: I2.
- For all 9 rows the error happened in rev1c, and every fix in rev1d went through the chain scripts.
