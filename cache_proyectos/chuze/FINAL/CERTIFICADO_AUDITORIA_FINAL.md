# CERTIFICADO DE AUDITORÍA — FINAL (Step 11 re-audit of the rebuilt FINAL, 2026-11-02)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL.xlsx` (49,710 B), `Chuze_AustinBluffs_Markups_FINAL.pdf` (220,484,040 B, 107 p., 134 annotations = 121 wall / element markups + 13 legend lines), `imagenes_FINAL/` (20 files), `CAMBIOS_FINAL.md`. The previous verdict is kept as `CERTIFICADO_AUDITORIA_FINAL_rechazado.md`. Forbidden paths not opened.

## Result
| # | Check | FINAL |
|---|---|---|
| 1 | Tag sweep | **PASS** (partition walls identical to rev3; the 19 D0.07 plan tags + the 1 D0.52 plan tag are all covered by EX runs) |
| 2 | Re-measurement | **PASS**. The 101 partition rows are identical to rev3. Existing-wall runs spot re-measured on AD101 vectors (table below) |
| 3 | Detail chain | **PASS** (D0.07 / D0.52 wording on AD101; EX-20 stops at the D0.50 concrete wall) |
| 4 | Scope sweep | **PASS** (4 estimator rules applied as decided; 41 RFIs CLOSED) |
| 5 | Arithmetic | **PASS** |
| 6 | Format | **PASS** (citations restored, 0 tokens; 1 minor observation) |
| 7 | Bluebeam | **PASS** (24 AD101 markups, Σ 669.61 LF = Excel 669.62) |
| 8 | Files | **PASS** |

## Check 2 — existing-wall runs (AD101 at 3/32", 6.75 pt/ft, wall line extents)
| Run | Excel / markup LF | Auditor LF | Δ | Note |
|---|---|---|---|---|
| EX-15 | 38.98 | 38.98 (y1585 1207.2 → 1282.6 + jog 5.41 + y1622 1282.6 → 1433.8) | 0 | Now starts at the D0.35 demolished partitions ✓ |
| EX-07A | 32.89 | 32.90 (y1622.4, 486.2 → 708.2) | 0 | |
| EX-07B | 6.25 | 6.25 (x598.8, 1539.4 → 1581.6) | 0 | Locker-end wall per the D0.07 leader; small, estimator's reading |
| EX-09A | 41.07 | 41.07 (x575.3, 1625.3 → 1902.5 inner face of the demising wall) | 0 | |
| EX-16 | 41.04 | 41.21 (x1196.4, 1625.5 → 1903.7) | +0.4 % | |
| EX-17 / EX-18 | 16.53 / 16.53 | 16.53 / 16.53 (1790.9 → 1902.5) | 0 | Stop at the demising wall ✓ |
| EX-19 | 27.60 | 27.63 (y1829.5 1320.5 → 1433.8 + x1433.8 1829.5 → 1902.5) | +0.1 % | Stops at the demising wall ✓ |
| EX-20 (D0.52) | 113.96 | 114.06 (328.6 / 327.8 → 1097.8 at the D0.50 change) | +0.1 % | Tenant face only |
* No markup vertex lies below y 1902.5 (the inner face of the demising wall), so nothing is drawn in N.I.C. ✓
* SF = LF × 22.83 × faces recomputed on all 24 rows ✓. Example: EX-01 77.33 × 22.83 × 2 = 3,530.89; EX-20 113.96 × 22.83 × 1 = 2,601.71.

## Check 5 — traceability and arithmetic
* **Partition Takeoff:** new block "TYPE EXISTING WALLS TO REMAIN - BOARD ONLY (NOT A PARTITION, NO FRAMING)" with 24 rows. Each row carries the AD101 keynote text, faces and Type X. SUBTOTAL 669.62 LF / 27,973.17 SF. The partition grand total (1,006.721 LF / 34,688.03 SF) is unchanged and correctly excludes the block.
* **Material Summary Type X:** 58,429.85 = rev3 30,456.68 + 27,973.17 ✓. The breakdown lists the 24 EX ids and sums exactly to 58,429.85 ✓.
* **Yields:** board total 65,388.75 SF (X 58,429.85 + MR 5,483.88 + W.R. 1,475.02). Joint compound 0.072 × 65,388.75 = 4,707.99 ✓; tape 0.37 × 65,388.75 = 24,193.84 ✓.
* **Blocking:** 253.31 = 225.31 + 13 accessory tags × 2 LF + 10/A505.B 2 LF ✓ (R-ALC-02).
* **Fasteners and duct reinforcement:** all 0 with the EXCLUDED note ✓.
* **Track and stud families:** unchanged from rev3 ✓.

## Check 6 — format
* The 7 fastener rows cite sheets again: GA-216 / A301, A301, B/S200, C/S200, M110 / M120 / S200. 0 "default (no sheet)" ✓.
* Full scan of the visible cells: 0 internal tokens ✓.
* Pending Items holds the header only; 41 CLOSED RFI rows carry the decision text ✓. Hidden `_reglas` seal kept.
* **Minor observation (non-blocking):** the Type X row's N/SHEET lists the A301 / A502 / A121 sources but not "D0.07/AD101, D0.52/AD101", although 27,973.17 SF come from AD101. The breakdown items (EX ids) trace to the Partition Takeoff rows, which do cite AD101. Recommend adding AD101 to that N/SHEET.

## Check 7 — Bluebeam
* AD101 (page 6, Page Label "AD101") carries 24 PolyLines, one per EX run. Each has Subject "EXISTING - BOARD ONLY", Measure "3/32 in = 1 ft", Depth 22.83 and NM TO-EX-xx. Contents LF matches the Bluebeam Length on all 24 (Σ 669.61 vs 669.62).
* All polylines are open: EX-15 has 4 vertices, EX-03 and EX-19 have 3, the rest 2. `img/FINAL2_chk7_AD101_markups_EX15_EX19.png`, `img/FINAL2_chk7_AD101_markups_EX06_EX12_EX20.png`.
* The other 97 element markups are unchanged from rev3. Totals: 121 element markups + 13 legend lines.
* **Evidence image** `imagenes_FINAL/AD101_existing_walls_D007_D052.png` was redrawn: open straight runs inside the building, labels with id + LF, D0.07 red / D0.52 blue legend, no closing diagonals, nothing in N.I.C. ✓

## Registration and gates
See the end of this file.
Environment: BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work. The FINAL Excel sha256 is c27e3e7630ae…, unchanged before and after the runs.
* `bitacora.py backcheck BACKCHECK_FINAL.md Takeoff_FINAL.xlsx` → **OK back-check anotado (rc 0)**.
* `bitacora.py run reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_FINAL.xlsx` → **rc 0**: 838 rules, 0 failures, REGLAS OK (log bitacora_logs/reglas.py_20261102T193225.log).
* `bitacora.py compuerta takeoff.json registro.json Takeoff_FINAL.xlsx` → **rc 0**: "BITACORA OK: 17 tools obligatorias vigentes + back-check".

## Verdict
**8 / 8 PASS.** FINAL is certified. One non-blocking observation: add D0.07/AD101 and D0.52/AD101 to the N/SHEET of the Type X row.
