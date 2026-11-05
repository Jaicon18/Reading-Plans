# Independent schedule reader - CR City Hotel (notes)

Reader: independent subagent. I did not see the take-off or the Excel. Date: 2026-11-05. Source: bidset_SIN_MARKUPS.pdf. Crops are in /root/cr/work/indep/img/.

## What was read
- **A0.06 (p10):** 27 interior type rows: W x5, FW x4, DW x2, FI x2, SFRM x1, C x4, CM x5, CH x4. Also the 6-row stud schedule plus its 5 notes, the legend and the 25 general notes (GN), copied word for word.
- **A0.07 (p11):** 11 exterior rows (XI/XW/X), plus the legend's finish-material codes.
- **A0.08 (p12):** 11 horizontal rows: RS-1..7, MB-1, FS-1 (two rows), and SFRM at the beam.
- **A7.19:** this is **p63**, a vector-only page with no text, so I read it from the image. It has two key schedules with 17 room rows and 20 public rows.
- **A8.00 (p78):** 129 door rows. Ratings: 20 MIN x50, 90 MIN x16, 45 MIN x2, 180 MIN x1, none x60. Also read: frame types 1/2/2A/3/4 and the door notes.
- **A0.09 (p13):** 13 details. **A0.10 (p14):** 4 details. **A0.11 (p15):** annular-space and penetration details, plus the penetration schedule.

## Key findings for metal framing and drywall
- **Almost no metal framing in the assemblies.** All interior W/FW/DW/FI types are wood. All exterior XW types are FRT 2x6 wood. Metal appears only in:
  - CH shaft walls: 20 GA C-H stud, J runner, 1" shaftliner.
  - MB-1 generator-room membrane: steel studs, C-channel, J-track, 1" liner on top, 3 layers of 5/8" below.
  - FS-1 resilient channels.
  Even so, GN4, GN6, GN7, GN8 and GN22 are written for metal studs.
- **Layers by rating:**
  - The W and CH detail notes say "1 layer for 1HR / 2 for 2HR / 3 for 3HR". W and DW are drawn on each side.
  - W.62-1 has 2 layers each side at 1 HR.
  - DW.4-1 has 1 layer each side.
  - FW and FI have one face only.
  - Exterior 2HR types have 2 layers of Type X on the interior. XW.6.3-2 and 6.4-2 have 2 layers of exterior Type X gyp. XW.6.6-2 has 1. XW.6.6-1 has 1 on each side.
- **Ceilings:**
  - FS-1 is 1 layer of 5/8" Type C on resilient channel.
  - RS-6 is 2 layers of 5/8" Type X.
  - RS-1 and RS-2 ceilings are "per RCP". RS-4 is "TBD".
- **Finish level:** A7.19 gives TF-1 (2-coat plaster, tadelakt) for "walls and ceilings" in both rooms and public spaces. The alternate is vinyl wallcovering. BOH is painted (P-1 walls eggshell, P-2 ceilings flat).
  - Spec 09 29 00 3.6.E.4 calls for Level 4 under plaster or wall covering and in BOH. 3.6.E.5 limits Level 5 to public areas *without* wall covering or plaster.
  - So, per A7.19, **no area clearly gets Level 5**. A7.19 has no room-by-room list, no ceiling heights and no ceiling-material column (not printed).

## Conflicts between plans and specs
1. **Deflection track leg depth.** GN7 asks for a minimum 3" deep-leg track with 1" deflection. Spec 09 22 16 2.3.B.1–2 gives a 2" deep flange for the long-leg/double runner.
2. **Ceiling board.**
   - FS-1 uses 5/8" Type C. 09 29 00 2.3 lists only Type X, a 1/2" ceiling board and MR Type X, with no Type C.
   - 09 29 00 also has no exterior sheathing gypsum and no shaftliner (the liner is in 09 21 16.23 2.3 as 1" Type X liner).
3. **Studs for wood partitions.** The stud schedule gives a 25 ga minimum, but every interior partition is wood. Spec 06 10 00 3.3.A.2 says interior studs are 2x4 at 16" o.c. Yet W types print 2x6.
4. **CH stud sizes.** CH.2-1 (2 1/2") and CH.4-1 (4") are on the sheet, but the stud schedule lists only a 6" C-H stud (20 ga, 28'). Height limits for the 2 1/2" and 4" are not printed. 09 21 16.23 2.6.B.2 gives a minimum 0.0329" (about 20 ga), which agrees.
5. **UL numbers on exterior types.** XW.6.3-2, XW.6.4-2 and XW.6.6-2 have table UL V337, but the drawings are labeled "ASSEMBLY U301". XW.6.2-2 prints rating "-" while carrying UL V337 and a "2" suffix.
6. **SFRM.** A0.06 cites X790 and A0.08 cites N743.
7. **Board at non-rated walls.** GN10 calls for plain 5/8" board at non-rated walls, but the wood detail says "Type X typ.".
8. **Water-resistant and tile backing board.** GN11 and GN12 call for water-resistant board, which matches 09 29 00 2.3.C (MR Type X). GN13 calls for cementitious backer units (CBU) at tile or stone, which matches 2.4. 09 29 00 3.6.E.2 puts Level 2 on tile substrates.
9. **DW rating.** The DW table says walls shown as 1/2 HR on the code plan are to be built as 1 HR.

## Unreadable or not printed
- No type IDs are printed for the SFRM rows.
- Not printed:
  - stud-schedule height for the 8" stud
  - MB-1 stud size, gauge and spacing
  - type of the outer 5/8" board on XW.6.2-0
  - stud o.c. in the W and CH blocks
- FI.6-0 has a "6" width in its ID but is drawn with 2x4 furring.
- CM.4-0 prints 3 5/8" as "8" NOM.", which looks wrong.
- Every type ID is printed with a space ("W.6 1"). I normalized them to "W.6-1".
