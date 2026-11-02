# Chuze Fitness Austin Bluffs, metal framing and drywall take-off: FINAL version (2026-11-02)

## What is in this folder
- **Chuze_AustinBluffs_Takeoff_FINAL.xlsx**: the delivered take-off. It has these sheets:
  - Inputs
  - Partition Takeoff (incl. the block EXISTING WALLS TO REMAIN - BOARD ONLY, 24 rows + SUBTOTAL)
  - Material Summary
  - Pending Items (empty)
  - Review Items
  - Scope Checklist (the 41 RFIs appear here as CLOSED rows)
  - Hidden `_reglas` seal sheet
- **Chuze_AustinBluffs_Markups_FINAL.pdf**: Bluebeam markups: 121 annotations = 97 walls / elements on the enlarged plans + 24 existing walls on AD101 (Subject "EXISTING - BOARD ONLY", 3/32" = 1'-0", Depth 22.83 ft).
- **imagenes_FINAL/**: stamped evidence images. `AD101_existing_walls_D007_D052.png` shows the existing walls that now get new board (straight runs, EX ids, legend).
- **CAMBIOS_FINAL.md**: what changed from rev3 to FINAL. It includes:
  - the full quantity comparison against rev3
  - each RFI with its decision and note
  - the four standing rules and how each changed the quantities
- **DECISIONES_ESTIMADOR_2026-11-02.md**: one row per RFI, 41 in total.
- **ENSAMBLE_CUADRE.md**: checks that each partition type's length in the source data matches the Excel. It also lists the Material Summary and the gate results.
- **PARA_REVISAR_EN_LA_MANANA.md**: what the estimator should look at first (in Spanish).
- **Earlier versions (rev0 to rev3)**: kept here for reference. Each has its own Excel, markups and CAMBIOS file.

## Totals (net quantities, before waste)
- Studs: 24,233.00 LF
- Bottom and top track: 2,209.54 LF. The top track is split into slip/deflection track where the wall reaches the deck and standard track where it stops below.
- Drywall and cement backer board: 66,598.52 SF. This includes 58,429.85 SF of 5/8" Type X.
- Metal stud blocking: 253.31 LF
- Fasteners: 0, all excluded.

## Decisions
- **All 41 RFIs are closed** (RFI-01 to RFI-37 plus 4 accessory RFIs). Each one uses the recommended option, which is the conservative assumption that was already loaded. The B.O. deck height is 22'-10".
  - 23 of them carry an internal note: "Recommend RFI to GC to confirm in field". Nothing has been sent to anyone.
- **Estimator standing rules applied:**
  - **All fasteners excluded.** Drywall screws, framing screws, TEK screws, cement board screws, slab pins and anchors are all 0. Clips, angles and other materials are still loaded.
  - **R-ALC-03: duct openings excluded.** Framed openings and stud reinforcement for ducts are by others, so 10 reinforcement plates and 6 duct sleeves were removed.
  - **R-ALC-02: accessory blocking.** Where an accessory's width is not printed, blocking is 3'-0" x 2 rows = 6 LF each. This adds 28.00 LF.
  - **Existing walls to remain.** Walls with the AD101 note "remove existing finish ... where required" (D0.07) get full new board on both faces. The existing demising wall noted "repair any damage" (D0.52) gets new board on the tenant face. Both use 5/8" Type X at the wall height of 22.83 ft: 24 straight runs (D0.07 555.66 LF, D0.52 113.96 LF), each a Partition Takeoff row and a markup. This adds 27,973.17 SF of board (EX-15 corrected to 38.98 LF after the audit).
- **Quantities against rev3:**
  - The Partition Takeoff rows of rev3 are identical; FINAL adds the existing-walls block (rule 4).
  - In the Material Summary, only the rows touched by the four rules changed. That is 11 rows, listed in CAMBIOS_FINAL.md §1.
- **Gates:** all pass except the back-check hash check. The back-check was registered on an earlier Excel and has not been re-registered; the auditor does that after a diff check.
