# CERTIFICADO DE AUDITORÍA — FINAL5 (rebuilt, 2026-11-03)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL5.xlsx` (56,554 B, 6 sheets, sha256 8fed54d1bb38…), `Chuze_AustinBluffs_Markups_FINAL5.pdf` (149 annotations = 121 elements + 15 RCP polygons + 13 legend). The first FINAL5 verdict is kept as `CERTIFICADO_AUDITORIA_FINAL5_rechazado.md`.

## Adjudication: CLG-A421A-05, north storefront west box
**The builder is right: 6.13 SF. My earlier 22.68 SF was wrong.**
* **Evidence:** 650 dpi render `img/FINAL5b_A421A_west_box_650dpi.png`.
  * The left box (A421.A pt x 1533.1–1647.8, y 996–1042.8) is a white panel with 6 stand-off bolt circles and a base rail/channel. It carries no C-5 stipple.
  * Stroke analysis: the 0.67-gray short strokes there (554) sit in only 15 of 60 grid cells, all at the 6 bolt circles and the base rail. They are bolt and rail drawing, not stipple.
  * In the real C-5 areas (east band, soffit band, 106 Smoothie Storage) the same stroke class fills the area uniformly at 7.6–14.2 per 100 pt².
  * My 4.9 per 100 pt² "sparse hatch" reading came from those bolt circles.
* **Drawing labels:** no legend / keynote / A502 note names the panel; the C-5 8'-6" tag belongs to the surrounding soffit.
* **The delivered polygon** = hatched soffit band y 1042.8 → 1048.1 + the hatched strips around the display box.
  * Every hatch stroke outside it sits in the bolt and rail clusters, except a ~0.16-ft hatched strip along the top edge (≈ 0.6 SF, negligible).
  * **6.13 SF accepted.**

## Result
| # | Check | FINAL5 |
|---|---|---|
| 1 | Tag sweep | PASS |
| 2 | Re-measurement | PASS (details below) |
| 3 | Detail chain | PASS |
| 4 | Scope | PASS (0 open RFI) |
| 5 | Arithmetic | PASS |
| 6 | Format | PASS (6 sheets; README first line "ESTA ES LA VERSIÓN FINAL PARA REVISAR") |
| 7 | Bluebeam | PASS (15 polygons at the printed 1/4" scale; area = Excel SF on all 15; legend + PNG per RCP sheet) |
| 8 | Files | PASS |

**Check 2, ceilings re-measured on the RCP vectors:**
* Reception: 504.8 by my own circle fit (R 13.83 ft) vs 505.14.
* 129 shower: 117.78 vs 117.79 (SE corner beyond the L-wall excluded ✓).
* Storefront east box: 13.70 ✓.
* Corridor triangle: 12.85 ✓.
* West box: 6.13 ✓.
* Total: 15 polygons = **1,005.28 SF** ✓.

**Check 5, diff FINAL4 → FINAL5:** the Partition Takeoff is identical; only ceiling-dependent rows changed.
* **Board and finishing:**
  * Type X 58,393.09 (= −36.76 = Type X ceilings 693.70 → 656.94) ✓.
  * W.R. 1,493.04 (+18.02 = 330.32 → 348.34) ✓.
  * Compound 4,706.64 and tape 24,186.90 (= 0.072 / 0.37 × −18.74 SF) ✓.
* **Grid and hangers:**
  * Main tee 548.43 / cross tee 968.46 = Σ per-ceiling operations ✓.
  * Hangers 2,497.64 LF / 192 ✓.
* **Moldings:**
  * KAM 455.36 + SC 61.31 = Σ perimeters 469.34 + 43.31 (both faces of the reception A6D wall, 2 × 21.66) + 4.01 (new west-box outline) ✓.
  * SC arc length by my own fit is 61.29 ✓.

**Observation (non-blocking, estimator's method):** grid and hangers are computed on each ceiling's bounding box. On the west box this keeps the 2.89 × 9.89 ft bbox (19.78 LF main + 26.01 LF cross + 8 hangers) for a 6.13 SF soffit.

## Registration and gates
Tools: /tmp/chuze/skill_v81cf16plus/take-off-metal-frame-drywall/tools (v81cf18). Environment: BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work. Excel sha256 unchanged by the runs.
* `bitacora.py backcheck BACKCHECK_FINAL5.md Takeoff_FINAL5.xlsx` → OK back-check anotado, **rc 0**.
* `bitacora.py run reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_FINAL5.xlsx` → **rc 0** (860 rules, 0 failures, REGLAS OK; log bitacora_logs/reglas.py_20261103T025135.log).
* `bitacora.py compuerta takeoff.json registro.json Takeoff_FINAL5.xlsx` → **rc 0** (BITACORA OK: 17 tools obligatorias vigentes + back-check).

## Verdict
**8 / 8 PASS. FINAL5 certified.**
