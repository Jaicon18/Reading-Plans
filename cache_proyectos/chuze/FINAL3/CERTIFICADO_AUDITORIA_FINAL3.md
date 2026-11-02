# CERTIFICADO DE AUDITORÍA — FINAL3 (RFI-S01..S03 option A + R-ALC-11 sweep, 2026-11-02)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL3.xlsx` (56,680 B), `Chuze_AustinBluffs_Markups_FINAL3.pdf` (220,484,040 B; annotations identical to FINAL2), `CAMBIOS_FINAL3.md`. Spec ¶ checked in `plano/specs.pdf`. Forbidden paths not opened.

## Result
| # | Check | FINAL3 |
|---|---|---|
| 1 | Tag sweep | PASS |
| 2 | Re-measurement | PASS. Partition Takeoff LF / height / layers / board identical to FINAL2; only the stud size and O.C. text of the 16 + 3 walls changed |
| 3 | Detail chain / spec | PASS (clip-angle note corrected in the rebuild) |
| 4 | Scope sweep | PASS |
| 5 | Arithmetic | PASS |
| 6 | Format | PASS (fixed in the rebuild) |
| 7 | Bluebeam | PASS (identical to the certified FINAL2) |
| 8 | Files | PASS |

## Verified
* **Diff FINAL2 → FINAL3:**
  * Partition Takeoff: only columns F/G (stud size / O.C.) on A-A422-5, A-A426-5, A-A426-6, A-A422-2, A-A423-6, A-A424-1/-2/-3, A-A425-1 to -5, A-A426-1, A-A435-2/-3 (362S162-54 @ 12"), A-A421-15 (362S125-30) and A-A422-3/-4 (600S125-30).
  * Material Summary: gauge splits of track and stud (track totals unchanged: 3-5/8" bottom 180.02 + 20.13 + 331.53 = 531.68; 6" 430.57 + 16.15 = 446.72; top rows likewise); 3-5/8" stud 12,383.36; gasket 422.34; corner 332.52 + casing 46.5; jamb return 27.9.
  * Pending Items empty. RFI-S01 to S03 CLOSED "estimator decision 2026-11-02 (option A)", each with alternative + where-to-verify, in the Material Summary rows, Review Items and Scope Checklist ✓.
* **Studs at 12" o.c., recomputed:**
  * A-A426-6 (A2-3D, 38.31 LF): 2 × (ROUNDUP(38.31/1) + 1) = 80 pcs ✓ (FINAL2 60).
  * A-A424-1 (12.25 LF): 13 + 1 + 1 extra = 15 ✓.
  * A-A425-4 (1.489 LF): 3 ✓.
  * A-A422-5: 2 × 34 + 4 extras = 72 ✓.
  * The Σ of the per-wall deltas over the 16 walls = **1,788.27 LF** ✓.
  * Solid blocking @ 96" (05 40 00 3.5.F.1 "Install solid blocking at 96-inch centers" in the top bridging row ✓): Σ ROUNDUP(L/8) per row = 50 pcs × 1.0 ft = 50.0 LF ✓.
* **Gasket 422.34 LF:**
  * 22.41 (600T250-54) + **331.53** = bottom track of the 16 walls (A2-3D 2 rows × 32.42 / 27.32 / 38.31, plus the A3C walls) = the 362T125-54 bottom-track row 331.53 ✓.
  * + 68.40 isolation strip = 2 × 34.20 LF of C3D at the storefront (A-A422-6, A-A431-1, A-A431-2) ✓.
  * Spec: 05 40 00 2.x.E + 3.1.D ✓; 09 22 16 2.4.B "Isolation Strip at Exterior Walls" and 3.2.B "against exterior masonry or dissimilar metals at exterior walls" ✓ (conservative).
* **Headers = 0 ✓ (R-ALC-11 claims hold):**
  * 05 50 00 1.1 includes "Loose steel lintels" and "Structural-steel door frames" (2.17: lintels "for openings … in masonry walls and partitions").
  * 05 40 00 3.3.G "Install headers over wall openings" is under 3.3 LOAD-BEARING WALL INSTALLATION only; 3.5 (interior non-load-bearing) has no header.
  * 09 22 16 3.2.D.2 "install track section (for cripple studs) at head and secure to jamb studs; two studs at each jamb" (head track = bottom track not deducted; cripples and 4 jamb studs in the stud rows) ✓.
* **Jamb return 27.9 SF** with corner 46.5 + casing 46.5 (same 93 LF trim total as FINAL2) ✓. Observation: the factor 0.60 ft is the D6F thickness; the A426 opening is in an A3C wall (0.41 ft), so −4.6 SF is possible (negligible).

## Defects to fix (presentation only; no quantity changes)
1. **Clip angles: false spec statement.** Material Summary (clips row) and Scope Checklist (05 40 00 clip angles / solid blocking item) say "05 40 00 3.5.E.1 interior channel bridging has no clip angle (clip angles only in 3.3 load-bearing / 3.4 exterior); 3.5.G names no element or location".
   * The Project Manual 05 40 00 **3.5.G** (interior non-load-bearing) reads: "Install miscellaneous framing and connections, including stud kickers, web stiffeners, **clip angles**, continuous angles, anchors, and fasteners, to provide a complete and stable wall-framing system."
   * The 0 can stand, because no drawing gives a location or quantity: it is a "complete and stable system" allowance. The note must be corrected, e.g. "3.5.G lists clip angles generically (no location / quantity on the drawings) → 0, allowance to the estimator".
2. **Row 54 "Gypsum board jamb return at openings"** shows "N/SHEET: default (no sheet)". The sheets are in the text (3/A426.A, 5/A429.A, A3C/A301, D6F/A301, spec 09 29 00 3.1); move them into the N/SHEET. This was a FINAL defect that was fixed and has now regressed in a new row.
3. **(Recommended, non-blocking)** The "Foam sealer gasket" row mixes two products: 05 40 00 2.9.E neoprene 1/4" (353.94 LF) and 09 22 16 2.4.B isolation strip, felt or 1/8" vinyl foam (68.40 LF). Split it into two purchase lines.

## Rebuild (21:43) — fixes verified
Diff of every visible cell against the previous FINAL3, normalised for row shift: only 3 changes, no quantity moved (sha256 a81914f494b9…).
1. ALC-X53 and the Deflection clips row now read "Clip angles: listed generically in spec 05 40 00 3.5.G (…) no location or quantity on the drawings -> 0, allowance to the estimator" ✓.
2. Jamb return row: "N/SHEET: 3/A426.A, 5/A429.A, A3C/A301, D6F/A301" ✓. 0 "default (no sheet)" left in the workbook.
3. Gasket split into 353.94 LF sill sealer gasket (05 40 00 2.9.E) + 68.40 LF isolation strip (09 22 16 2.4.B) = 422.34 ✓.

## Back-check / gates (env BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work; Excel sha256 unchanged by the runs)
* `bitacora.py backcheck BACKCHECK_FINAL3.md Takeoff_FINAL3.xlsx` → OK back-check anotado, **rc 0**.
* `bitacora.py run reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_FINAL3.xlsx` → **rc 0** (838 rules, 0 failures, REGLAS OK; log bitacora_logs/reglas.py_20261102T214501.log).
* `bitacora.py compuerta takeoff.json registro.json Takeoff_FINAL3.xlsx` → **rc 0** (BITACORA OK: 17 tools obligatorias vigentes + back-check).

## Verdict
**8 / 8 PASS. FINAL3 certified.** Remaining observation (negligible): jamb-return depth of 0.60 ft at the A3C opening (−4.6 SF possible).
