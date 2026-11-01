# CERTIFICADO DE AUDITORÍA — rev3 (Step 11 re-audit)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_rev3.xlsx` (54,712 B), `Chuze_AustinBluffs_Markups_rev3.pdf` (220,450,979 B), `imagenes_rev3/` (19 files), `CAMBIOS_rev3.md`. Forbidden paths not opened.

## Diff rev2 → rev3 (cell by cell, all visible sheets)
* **Material Summary:** only the top-track rows 8, 9, 10 and 12 changed (Net, waste, purchase, pieces, breakdown); row 13 changed only its N/SHEET citation.
* **Partition Takeoff:** 2 text cells (inventory id removed from the A-A422-5 location). LF, height, layers and board SF are identical in all 101 rows.
* **Pending Items:** 3 text cells (inventory ids removed).
* **Scope Checklist:** 2 text cells (ALC-04 split criterion, ALC-05 plain wording).
* **Markups:** the 109 annotations are identical to rev2 (subject, content, vertices).
* Every other check therefore carries over from rev2: 1, 2, 4, 5, 7 and 8 PASS.

## Result
| # | Check | rev2 | rev3 |
|---|---|---|---|
| 1 | Tag sweep | PASS | **PASS** (carried over; walls and markups identical) |
| 2 | Re-measurement | PASS | **PASS** (Partition Takeoff identical; auditor 1,228.35 vs 1,226.96 LF, +0.11 %) |
| 3 | Detail chain | FAIL | **PASS**: top track follows whether the studs reach the B.O. deck |
| 4 | Scope sweep | PASS | **PASS** (carried over) |
| 5 | Arithmetic | PASS | **PASS**. Track rows sum to their Net: 3-5/8" slip 397.30 + standard 134.38 = 531.68; 6" slip 409.44 + standard 37.28 + 600T250-54 22.41 = 469.13; 2-1/2" slip 103.96; total 1,104.77 = bottom track. Waste, purchase and pieces formulas recompute |
| 6 | Format | PASS | **PASS** (full visible-cell scan: 0 internal tokens) |
| 7 | Bluebeam | PASS | **PASS** (markups identical to rev2) |
| 8 | Files | PASS | **PASS** |

## Check 3 — verification of the top-track split
Each wall in the breakdowns was checked against its Partition Takeoff height.
* **Slip / deflection rows:** every wall has studs to the deck (22.83 ft). The single exception is the A-A435-1 Retail Storage 126 zone, 5.91 LF, which has run to the deck since rev1; the rest of that wall (27.30 LF, 10.5 ft) stays in the standard row ✓.
* **Standard rows:** no wall with studs to the deck remains (0 walls ≥ 22.8 ft).
* **Values match my rev2 correction:** 3-5/8" slip 240.96 + 150.43 + 5.91 = 397.30; standard 290.72 − 150.43 − 5.91 = 134.38; 6" slip 409.44, standard 37.28 ✓. This follows spec 09 22 16 Part 3 (slip-type head joints where framing reaches structure) and D/A301.
* **Observation (non-blocking):**
  * The standard 3-5/8" row cites "D/A301, B/A425.C, B/A434.A" and no longer cites C/A301 or G/A301 (the head details of the walls in that row).
  * The 2-1/2" slip row cites D/A301 rather than E/A301.
  * Recommend citing C/A301 + G/A301 on the standard rows and E/A301 on the B2E row. No quantity effect.

## Check 6 — format
I scanned every visible cell for R1-/R2-/R80, soffit_side, skill, canon, .py, familias, votes, grep, mep.cruces, "tools", plantilla, PT0###/PA0###, internal status tokens, A-A435-4, BE-/GAP- ids and "tramos". All absent. The rev2 residuals (PT0009, PT0130, PT0105, ALC-05) are cleaned. The hidden `_reglas` seal is kept by design.

## Standing observations (estimator's call, documented in the Excel)
* Gypsum behind cement backer not deducted (RFI-06, possible −1,209.77 SF).
* Grid main / cross tee use the bounding-box method (≈ +220 / +200 LF vs an area method).
* Hanger density: 187 PCS.
* Unconfirmed MEP crossings carried as an RFI range.

## Verdict
**8 / 8 PASS.** The back-check is registered on rev3 and the gates were run (results appended below).

## Registration and gates (env BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work)
* `bitacora.py backcheck BACKCHECK_rev3.md Takeoff_rev3.xlsx` → **OK back-check anotado (rc 0)**, 2026-11-01T11:47:56.
* `reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_rev3.xlsx` → **rc 0**: 838 rules, 0 failures, REGLAS OK.
  * The first direct run (outside the bitácora) also gave rc 0.
  * The bitácora only counts runs made through `bitacora.py run`, and its last logged reglas run (11:43:23, before the back-check existed) was rc 1. So the gate was re-run through `bitacora.py run`: rc 0 at 11:48:39.
* `bitacora.py compuerta takeoff.json registro.json Takeoff_rev3.xlsx` → **rc 0**: "BITACORA OK: 17 tools obligatorias vigentes + back-check".
* The rev3 Excel was not modified (sha256 unchanged by the audit).
