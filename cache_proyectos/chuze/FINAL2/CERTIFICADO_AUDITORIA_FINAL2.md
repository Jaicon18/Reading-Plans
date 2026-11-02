# CERTIFICADO DE AUDITORÍA — FINAL2 (spec sweep + project data sheet, 2026-11-02)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL2.xlsx` (54,415 B), `Chuze_AustinBluffs_Markups_FINAL2.pdf` (220,484,040 B; 134 annotations, identical to FINAL), `imagenes_FINAL2/`, `CAMBIOS_FINAL2.md`. Sources: the bid set, the Project Manual (`plano/specs.pdf`, for spec citations) and the deliverables. Forbidden paths not opened.

## Result
| # | Check | FINAL2 |
|---|---|---|
| 1 | Tag sweep | PASS (walls identical to FINAL) |
| 2 | Re-measurement | PASS (Partition Takeoff 126 rows identical to FINAL) |
| 3 | Detail chain / spec | PASS (each new item checked in the Project Manual) |
| 4 | Scope sweep | PASS (the 4 uncited trade sheets reviewed, below; MEP not cited = not trade) |
| 5 | Arithmetic | PASS |
| 6 | Format | PASS (0 internal tokens; Pending Items = 3 OPEN spec RFIs with A / B / C) |
| 7 | Bluebeam | PASS (annotations identical to FINAL, which was already certified) |
| 8 | Files | PASS |

## (1) Diff FINAL → FINAL2
* **Partition Takeoff:** 0 differences.
* **Material Summary:** only the announced rows changed.
  * Bracing 5,390.39 → 6,301.09 LF (453 pcs = ROUNDUP(6,301.09 × 1.15 / 16)).
  * New rows: AR mesh tape 447.61 LF; foam sealer gasket 22.41 LF.
  * Corner bead split 441.22 = 379.02 + curved-edge 62.20.
  * Relabels with quantity unchanged: setting-type compound 4,707.99 lb; A1003 G60 on 600S162-33 432 LF, 600T250-54 22.41 + 22.41 LF and 16 ga deep-leg track 11 LF; "Type X MR" 5,483.88 SF; Armstrong grid.
* **Inputs:** data-sheet rows added. **Scope Checklist:** notes ALC-X48 to X52. **Pending Items:** RFI-S01 to S03.
* **+910.70 bracing, recomputed per wall.** The bracing breakdown lists 64 "top row" items. Each equals that wall's slip-track LF in the three slip-track rows (3-5/8" 397.30 + 6" 409.44 + 2-1/2" 103.96 = 910.70; 0 mismatches). A2-3D walls carry 2 rows (double stud).
  * Spec basis: 09 22 16 2.2.C.1, "Single Long-Leg Track System … with continuous bridging located within 12 inches of the top of studs" ✓.
  * The extra row is not double counted: at 22.83 ft the 48" rows stop at 20 ft, which is more than 12" below the top.
* **Other new rows, spec-checked:**
  * Sealer gasket: 05 40 00 2.x.E "Sealer Gaskets: closed-cell neoprene foam, 1/4" … width of bottom track" and 3.1.D "install at the underside of wall bottom track" ✓.
  * Mesh tape: 09 29 00 2.7.B.4 "Tile Backing Panels: as recommended by panel manufacturer" ✓.
  * Curved-edge cornerbead: 09 29 00 2.6.A.2.g ✓.

## (2) Project data sheet vs G001 (`img/FINAL2_chk_G001_project_data.png`)
Matches G001:
* Address "3630 Austin Bluffs Pkwy, Unit #C190, Colorado Springs, CO 80918" (the title blocks print "Unit # 190").
* III B, automatic sprinklered; 1 story; 30'-0"; occupancies A3, B, E, I-4, S1; separation "NOT REQUIRED PER 508.3".
* 37,952 SF actual and 37,949 SF square footage (both quoted); 662 occupants; 903.3.1.1.
* Codes (2023 Pikes Peak, 2021 IFC / IEBC Level 3 / IMC / IPC / IECC / IFGC, 2023 NEC, CRS Title 9).
* Architect DxU (15150 N. Hayden Rd., Christine Smith); tenant Chuze (1011 Camino del Rio South, San Diego).
✓ No discrepancy.

## (3) Trade sheets nobody cited
* **A000.B (p10) Interior Wall Verification Plan:** a GC survey form (verify dimensions 8 weeks before SOS). Vector check: every A000.B wall poche rectangle (91 matches, 0 unmatched) is also on A101, so it shows **no new wall** and no existing-wall condition, board or blocking note. **No quantity change.**
* **A002 (p12) Site Details:** ADA parking striping, wheel stops, sign post, pavement slopes. **No framing / gypsum content. No quantity change.**
* **A503.A (p62) Millwork Details:** studio custom cubby (72½"), recovery day-locker / shoe cubby, staff lounge millwork. Casework only ("WALL TYPE AND FINISHES AS SCHEDULED"); no new wall or board.
  * **Informative, metal blocking:** 6/A503.A prints the staff-lounge countertop at **10'-0"** and the uppers at 3 × 3'-3" = 9'-9". The A103 keys 51 / 52 runs are loaded at 8.75 ft × 2 rows each. If those are taken from this detail: **+4.5 LF of 6" × 16 ga track** (51: +1.25 × 2; 52: +1.0 × 2), 253.31 → 257.81 LF (+1.8 %, within tolerance; estimator's call). `img/FINAL2_A503A_6_staff_lounge_10ft_counter.png`.
* **A503.B (p63) Millwork Details:** Group X cabinets, kids club craft-area cabinets and front desk, base / upper cabinet sections. Casework only; blocking for these is A103 keys 33 / 34 / 36 (already handled). **No quantity change.**
* **MEP sheets not cited** (M601, M602, P120, P501, E000, E120, E402, E501, E603, E604, E605, E700): text sweep.
  * M602 duct / pipe sleeves = ducts EXCLUDED (R-ALC-03).
  * P120 "wall-mounted access panels lockable" = panel product note (trap-primer panels RFI closed, 0).
  * E501 TV / speaker backing "refer to architectural details" (= A103).
  * E000 "conceal conduit in nearest framing" = electrical.
  * M601 / E604 / E605: "STUD" hits are "STUDIO" in schedules.
  * **Confirmed: not trade** (ducts / fasteners excluded, MEP by others).

## (4) Format / gates
* Visible cells: 0 internal tokens (tools, canon, skill, spec_sweep, R-ALC-09, PT ids, status tokens, "default (no sheet)", USG).
* Pending Items holds RFI-S01 (stud gauge vs limiting height, L/240 option +2,371.6 LF), RFI-S02 (12 ga vs 0.16" hanger wire) and RFI-S03 (arc radius / flexible board), each with A / B / C and the current quantities loaded.
* **Information for RFI-S03:** the auditor's vector fit of the reception circle gives **R = 13.83 ft**. This can be used to resolve it against the dry-bend radius of 5/8" board.

## Registration and gates
See below.
Environment: BITACORA=/tmp/chuze/work/bitacora.jsonl, TAKEOFF_WORK=/tmp/chuze/work. The FINAL2 Excel sha256 is 4880b4ed2330…, unchanged before and after the runs.
* `bitacora.py backcheck BACKCHECK_FINAL2.md Takeoff_FINAL2.xlsx` → **OK back-check anotado (rc 0)**.
* `bitacora.py run reglas.py compuerta /tmp/chuze/work/etapas --excel Takeoff_FINAL2.xlsx` → **rc 0**: 838 rules, 0 failures, REGLAS OK (log bitacora_logs/reglas.py_20261102T210358.log).
* `bitacora.py compuerta takeoff.json registro.json Takeoff_FINAL2.xlsx` → **rc 0**: "BITACORA OK: 17 tools obligatorias vigentes + back-check".

## Verdict
**8 / 8 PASS. FINAL2 certified.** Two informative items for the estimator, neither a defect:
* 6/A503.A staff lounge 10'-0" counter: +4.5 LF of backing track if taken from the detail.
* RFI-S03 arc radius measured at 13.83 ft.
