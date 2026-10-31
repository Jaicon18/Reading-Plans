# AUDIT COMPARISON - Take-off vs Independent Auditor (Step 11)

O'Reilly Auto Parts, 23rd Ave., Evans, CO #1. No dimension was scaled. Images are in `audit_p11/img/`. The Excel was not modified.

| # | Item | Take-off | Auditor | Delta | N/SHEET | Image | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | S24-OF length | 11.708 LF | 11.000 LF (clear office width) | +0.708 LF (+6.4%); about +6 SF board | 11'-0"/A1.1 | 03 | Stop S24 between the S43 walls, or document the corner run-through convention. |
| 2 | S24-RR length | 16.823 LF | ≤ 16.167 LF | ≥ +0.656 LF (+4.1%) | 7'-10" + 6" + 7'-10"/A1.1 | 03 | Same as item 1. |
| 3 | S24-RRS length | 8.854 LF | 8.500 LF | +0.354 LF (+4.2%) | 8'-6"/A1.1 | 03 | Same as item 1. |
| 4 | S42-02 free end past the S42-03 corner | 25.455 LF total (≈ 6.77 LF past the corner, [DERIVED]) | 18.333 + 0.354 verifiable; the free end is **not printed** | ≈ 6.77 LF unverifiable | 18'-4"/A1.1; no horizontal dimension (witness of 16'-10 7/8"±/A1.1 only) | 04 | Flag the item [PENDING] and add an RFI for the free-end location (Rule #0). |
| 5 | 1-1/2" Z-furring (MS row 14) | 2,517.5 LF | 2,235.0 LF (S21: (ROUNDUP(L / 2) + 1) x H per wall) | +282.5 LF (+12.6%) | S21/A1.1 types (150ZF125-18 @ 24" O.C.); heights from 116'-4 3/4" and 114'-7 1/2"/A3.2 | 08, 07 | Add a breakdown. Remove any S24 Z-furring already covered by S21-E / S21-S. |
| 6 | Joint compound waste | 585.08 lb (0% waste) | 620.18 lb (6% per Inputs B6) | +35.1 lb | Inputs B6 (rule) | - | Apply B6, or state that the yield already includes waste. |
| 7 | Joint tape waste | 3,006.67 LF (0%) | 3,187.07 LF (6%) | +180.4 LF | Inputs B6 | - | Same as item 6. |
| 8 | Resilient channel purchase unit (row 28) | 139 "pieces" (= LF) | 12 pcs of 12 ft (ROUNDUP(138.59 / 12)) | Unit error | 1/A5.2 (7/8" RC) | 13 | Use the stick length from Inputs (B17). |
| 9 | Flat strap stock (row 30) | "C.R. channel 16 ft" | 3" x 16 ga flat strap (coil / LF) | Unit mismatch | Note 2.B/A1.1 | 09 | Change the selling unit. |
| 10 | Ceiling perimeter track source (row 18) | "1/A-121, 5/A-121" | Sheet not in set; GWB ceilings are at 7/A4.2 (6" joists, B.O. framing 108'-6") and 3/A3.1 | Wrong N/SHEET | 7/A4.2 | 16 | Fix the citation. |
| 11 | Header / box beam (row 20) | 56 LF, no breakdown or N/SHEET | Not verifiable | - | - | - | Add a breakdown and its detail (7/A5.1 per ALC-05). |
| 12 | Rigid polyiso insulation in S21 / S24 | Not mentioned (ALC-X28 covers "batt" only) | Printed: 1-1/2" foil-faced polyisocyanurate (min R-9) | Scope note | S21, S24/A1.1 types | 08 | Add an explicit EXCLUDED / IN SCOPE line. |
| 13 | Acoustical sealant | Excluded ("standing order") | A1.1 note 4.B prints it; this exclusion is not among the orders given to the audit | Scope note | Note 4.B/A1.1 | 09 | The estimator should confirm the exclusion. |
| 14 | Exterior stucco / lath | Not addressed in the Scope Checklist | Printed: exterior portland cement (stucco) | Scope note | 1/A5.2 | 13 | Add a NOT IN SCOPE line. |
| 15 | Language / format | Spanish text in visible cells: RESPUESTAS_RFI_ESTIMADOR.md x11; img_resolucion / img_ensamble / img_revision; raw dict `{'texto','cita'}` in Pending C14; "canon" | Everything in English | Format | - | - | Clean the text; render Pending C14 as plain text. |
| 16 | S42 rows merged | 2 rows (S42-01+02, S42-03+04) with weighted heights | 4 walls (markups show 4) | Format | 5/A4.2, 6/A4.2 | 18 | One row per wall, matching the markups. |
