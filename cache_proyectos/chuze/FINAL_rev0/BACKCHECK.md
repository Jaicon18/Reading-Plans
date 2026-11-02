# BACKCHECK — blind per-family back-check, Chuze Fitness Austin Bluffs, take-off rev0
Auditor: Step 11 independent auditor, 2026-11-01. Sources: plans `bidset_SIN_MARKUPS.pdf` + deliverables only.
Excel back-checked: `5_entrega/Chuze_AustinBluffs_Takeoff_rev0.xlsx` (sha256 2536ef0c6c7a…).

Method: LF per wall re-measured by vectors on the enlarged plans and again on A101 (see CERTIFICADO, check 2). Family quantities recomputed from the auditor LF with the plan rules: studs (ROUNDUP(LF/O.C.) + 1) × H × rows; track 2 × LF per family; bracing rows ROUNDUP(H×12/48) − 1; board LF × H × faces × layers; accessories from the notes and details.

| Family | Take-off | Auditor | Δ | Comment |
|---|---|---|---|---|
| Wall LF, partitions (11 types) | 1,006.72 LF | 1,008.16 LF | +0.14 % | Every type within ±0.81 %; 2 rows > 2 % by ≤ 0.10 LF |
| Soffit / headwall sides (OTHER FRAMING) | 220.24 LF | 220.19 LF | −0.02 % | Reception arc 62.05 vs 62.2 |
| Studs 3-5/8" | 10,090.37 LF | 8,848 LF (spacing only) | −12.3 % | Auditor excludes jambs / corners / intersections; ×1.14 is a normal allowance |
| Studs 6" (incl. soffits) | 10,952.22 LF | 9,949 LF (spacing only) | −9.2 % | Same reason |
| Studs 2-1/2" (B2E) | 2,009.04 LF | 1,941 LF | −3.4 % | Row has no breakdown / source (format) |
| Bottom track 3-5/8" / 6" / 600T250-54 / 2-1/2" | 531.68 / 446.72 / 22.41 / 103.96 LF | 531.68 / 446.71 / 22.41 / 103.96 LF | 0.00 % | 2 rows at A2-3D |
| Top / slip track (same families) | 1,104.77 LF | 1,104.76 LF | 0.00 % | 2" slip track heads D / E (A301) |
| Soffit / ceiling track | 440.48 LF | 440.38 LF | −0.02 % | 2 × soffit LF |
| Bracing 1-1/2" C.R. channel | 5,372.66 LF | 5,314.6 LF | −1.1 % | Partitions 4,874.1 + soffits 440.5 |
| Board, walls (all types) | 34,688.03 SF | 34,688 SF by detail heights; 36,764 SF upper bound at full height | 0 % / −5.6 % | Board on head C / E walls stops at ceiling + 6" (C, E/A301): the −5.6 % is explained |
| Board, C-5 GWB ceilings | 1,024.02 SF | reception 522.2 vs 518 SF (others not re-measured) | +0.8 % on the sample | |
| MR vs Type X split | MR 5,402.49 / X 30,526.94 / W.R. 1,475.02 SF | MR +81.4, X −81.4 | 81.4 SF | Men's Locker 128 soffit faces (A111 note 3) |
| Soffits (count / details) | 11 elements, 6/7/8/9/13/15/16 A502 | same | 0 | 9/A502 3-5/8" member not in the 3-5/8" stud row (< 10 LF) |
| Drywall grid main / cross tee | 523.35 / 969.80 LF | ≈ 300 / ≈ 770 LF (area method) | −43 % / −21 % | Take-off uses bounding box + 1 per area (explained); estimator's call |
| Channel + angle molding | 458.91 + 458.91 LF | 458.91 LF | −458.91 LF | Possible duplicate perimeter trim |
| Hangers (count / wire) | 187 PCS / 2,428.49 LF | ≈ 64–95 PCS at 4' × 4' / ≈ 1,000–1,250 LF | about −50 % | Hanger spacing not printed for C-5; estimator to confirm |
| Control joints (note 27) | 0 LF | 336.3 LF | +336.3 LF | MISSING |
| Corner bead / trim | 193.90 LF | ≈ 441 LF | ≈ +247 LF | C3C boxes + cased openings missing |
| Metal backing 6" 16 ga track (A103) | 0 LF | ≈ 300 LF (low confidence) | ≈ +300 LF | MISSING; RFI-13 / RFI-28 / ALC-16 contradict each other |
| RTU curb caps 600S162-33 (2/A131) | 0 (RFI-14 says loaded) | 9 caps, size n/q | n/q | Text inconsistency |
| Access panels | 1 + RFI-15 | 1 + RFI-15 | 0 | |
| Drywall screws / framing screws / pins | 44,885 / 4,916 / 828.6 | 44,885 / 4,916 / 828.6 | 0 | Yields recomputed exactly |
| Joint compound / tape | 2,693.12 lb / 13,839.65 LF | 2,693.1 / 13,839.6 | 0 | |
| Headers | 0 (steel by others, RFI-12) | 0 | 0 | 6/A602, 8/A602 "STEEL HEADER – REF: STRUCT." |

Verdict: wall measurements and core framing / board quantities are confirmed. Accessory scope is incomplete: control joints, corner bead, A103 metal backing. There is one likely duplicate (channel + angle molding), and the Bluebeam calibration of the RCP soffit markups is wrong. Details: CERTIFICADO_AUDITORIA.md and COMPARATIVA_AUDITORIA.md.
