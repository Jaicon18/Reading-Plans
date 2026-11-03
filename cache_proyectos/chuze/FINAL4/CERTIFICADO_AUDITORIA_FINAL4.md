# CERTIFICADO DE AUDITORÍA — FINAL4 (last delivery, v81cf11 tools, 2026-11-03)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL4.xlsx` (56,493 B; 6 sheets; sha256 bc1fd68d4aad… = `.sello.json` xlsx_sha256), `Chuze_AustinBluffs_Markups_FINAL4.pdf` (220,509,917 B, 107 p., 134 annotations), `imagenes_FINAL4/` (19 PNG + summary), README_REVIEW.md, CAMBIOS_FINAL4.md. My own scripts only; the producer's BE-117 tool was not used. Forbidden paths not opened.

## Result
| # | Check | FINAL4 |
|---|---|---|
| 1 | Tag sweep | PASS (walls identical to FINAL3) |
| 2 | Re-measurement | PASS (Partition Takeoff 126 rows identical; Length vs LF ≤ 0.19 %) |
| 3 | Detail chain | PASS |
| 4 | Scope | PASS (0 open RFI; 44 CLOSED rows in the Scope Checklist) |
| 5 | Arithmetic | PASS (NET identical in all 44 families) |
| 6 | Format | PASS (6 visible sheets, no hidden sheet; seal in `.sello.json`; 0 internal tokens; 0 "default (no sheet)") |
| 7 | Bluebeam (BE-117, independent) | PASS |
| 8 | Files | PASS |

## (1) NET diff FINAL3 → FINAL4
* All 44 Material Summary families are equal in NET.
* Changes are labels and splits only:
  * ceiling / soffit track row name;
  * metal blocking split into backing 247.31 + stud blocking 6.00 = 253.31;
  * BOARD-ONLY block label.
* Purchase pieces changed only on AR mesh tape: 475 → 448, because a yield row carries no waste.
* Partition Takeoff: 0 differences in LF / H / layers / O.C. / board. Added SUBTOTAL OTHER FRAMING 220.24 LF / 1,692.40 SF ✓.

## (2) BE-117 re-run (own script, all 121 element annotations + 13 legend lines)
* **Fields vs Excel row:** each annotation's TYPE · LF · H · SF · DETAIL · Wall ID was parsed and matched to its Partition Takeoff row.
  * LF, H, Depth and board SF equal the row on all 121.
  * The 8 joined rows (`r` returns, A432-1+2) sum exactly to their row (e.g. 104.6 + 37.1 = 141.7 vs 141.68).
  * DETAIL matches the row source; A2-3D now reads "A2-3D/A301".
  * Every Excel row has at least one annotation.
* **Scale:** every element's /Measure R equals a printed scale of its sheet (3/32" A101 / AD101, 1/4" A421–A435 and the RCPs, 3/16" A432 / A434) ✓.
* **Length vs LF:** max deviation 0.19 % (limit 0.5 %) ✓. Includes the 49-point reception arc and the 3-side C3C boxes.
* **Legend per sheet:** all 19 marked sheets carry "TAKE-OFF LEGEND – <sheet> (partition schedule order)". Types appear in A301 order (A2-3D … X6D, then soffit side, then board only). Counts and LF equal the annotations on that sheet ✓.
* **PNG:** 19 marked sheets = 19 PNGs in imagenes_FINAL4 ✓.
* **Observation (non-blocking):** the board-only walls carry Subject / type "BOARD ONLY - NO FRAMING", while the Excel block header reads "BOARD ONLY - EXISTING OR WOOD-FRAMED WALLS (FRAMING NOT IN SCOPE)". Same group, same IDs / LF / SF / keynote; the wording could be unified.

## (3) Delivery items
* README_REVIEW.md first line: "ESTA ES LA VERSIÓN FINAL PARA REVISAR" ✓.
* Inputs carries the PROJECT DATA block (checked against G001 at FINAL2) ✓.
* Pending Items is empty (header only); 0 OPEN ✓.
* 6 sheets ✓.

## Registration and gates
See below.
Tools: /tmp/chuze/skill_v81cf11/take-off-metal-frame-drywall/tools. Environment: BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work. The Excel sha256 bc1fd68d4aad… is unchanged before and after the runs.
* `bitacora.py backcheck BACKCHECK_FINAL4.md Takeoff_FINAL4.xlsx` → OK back-check anotado, **rc 0**.
* `bitacora.py run reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_FINAL4.xlsx` → **rc 0**: 850 rules, 0 failures, REGLAS OK (log bitacora_logs/reglas.py_20261103T005709.log).
* `bitacora.py compuerta takeoff.json registro.json Takeoff_FINAL4.xlsx` → **rc 0**: BITACORA OK: 17 tools obligatorias vigentes + back-check.

## Verdict
**8 / 8 PASS. FINAL4 certified** as the final delivery. One non-blocking wording observation: the board-only Subject vs the block header.
