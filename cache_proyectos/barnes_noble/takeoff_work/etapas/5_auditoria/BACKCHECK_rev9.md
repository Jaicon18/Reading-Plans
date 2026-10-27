VERDICT: PASS WITH COMMENTS
LIBRARY: 43 PASS · 0 FAIL · 3 N/A

# Back-check rev9: B&N Colorado Springs

File: `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev9.xlsx`, final rebuild **md5 48be3bb54c7ec4e318bfd42578663b85**. Earlier runs: 47acc0a9..., then b8a99e84... (that rebuild changed only the RFI-41 delta). The 48be3bb5 rebuild changes only RFI-51: BE-47 and BE-52 were re-tested on it. Material Summary nets and pieces are identical to b8a99e84, the changed-cell set vs rev8 is the same, and the internal-name scan still gives 0 hits. Read with openpyxl data_only=True. Diffed against rev8. Per R80e.30 the review was targeted: changed cells plus the circled crops 8/A-410, A/A-410, 3-4/A-410, 3/A-410, 5/A-410, 8/A-210 and 5/A-121.

## Test table

| ID | Result | Evidence |
|---|---|---|
| BE-01 | PASS | Fire-stop track is in its own rows by size: 3-5/8" 157.81 (MS R37) + 6" 106.40 (MS R38) = 264.21 = RFI-35 |
| BE-02 | PASS | Unchanged from rev8. W.R. 1,092.59 SF includes the restroom GWB ceilings (MS R20) |
| BE-03 | PASS | Unchanged (MS R20 breakdown) |
| BE-04 | PASS | Unchanged |
| BE-05 | PASS | Unchanged (Partition Takeoff has no diff) |
| BE-06 | PASS | SS-N / SS-E / SS-IN / SS-GG track is now in R37 / R38 |
| BE-07 | PASS | Unchanged |
| BE-08 | PASS | Unchanged |
| BE-09 | PASS | RFI-01 unchanged in substance |
| BE-10 | PASS | Unchanged |
| BE-11 | PASS | Unchanged |
| BE-12 | PASS | New quotes checked against the crops: 3/A-410 and 4/A-410 "3 5/8" X 20GA TRACK W/ (2)-1/4"ø X 1 5/8" HILTI KWIK HUSEZ ... MOMENT CLIP"; A/A-410 "(1) #10-16 SCREW @ EACH FLANGE"; the three 8/A-410 #8 callouts all match |
| BE-13 | PASS | Unchanged (RFI-50) |
| BE-14 | PASS | RFI-54 "prints no track size": 5/A-121 crop shows no perimeter track size |
| BE-15 | PASS | The 8/A-410 members are described as drawn: cross member to track, top chord, perpendicular crossing. See comment N1 |
| BE-16 | PASS | 8/A-410 #8 screws now have their own row (MS R40, 775). A/A-410 #10-16 is in the RFI-28 delta |
| BE-17 | PASS | Type S / S-12 and #8 / #10-16 are separate rows by gauge (R54, R55, R62, R63) |
| BE-18 | PASS | No new item lacks a destination |
| BE-19 | PASS | Slab pins use the printed note 8.F; the 9/A-410 PAF @ 24" alternative is in the RFI |
| BE-52 | PASS (re-test 48be3bb5) | RFI-51 now reads "5/A-410 bracing clips are in the Tek screw row; diagonal brace end screws (3/A-410) are not printed and not carried (if 2 per end: + 512 #8)". The clips are in the MS R28 breakdown. The other coverage claim (8/A-410 #8 in their own row) matches R40 |
| BE-53 | PASS | RFI-28 lists clips + 324 HUS-EZ + 324 #10-16. RFI-41 now states the alternative reading 380 (+98). See comment N4 |
| BE-56 | PASS | Slab pins = (640.61 − 122.32) / 0.6667 = 777.43. The 122.32 LF matches type 3 (38.68) + type 4 (83.64) bottom track |
| BE-20 | PASS | Unchanged |
| BE-21 | PASS | Unchanged |
| BE-22 | PASS | R50 = 0 citing 1/A-500 |
| BE-23 | PASS | No acoustical sealant row |
| BE-24 | PASS | Bottom = top: 450.02 / 118.59 / 72.00, separate rows |
| BE-25 | PASS | Unchanged |
| BE-26 | N/A | No ballistic type |
| BE-27 | N/A | No recess (R48 = 0) |
| BE-28 | N/A | No new canopy / parapet |
| BE-29 | PASS | RFI-09 unchanged |
| BE-40 | PASS | Every MS row has N/SHEET plus a breakdown or operation that reproduces Net within ±0.1. Checked: R13 180.99, R37 281.09, R38 144.06, R39 12.67, R40 775, R55 4×485 (673+108−296), R62 296, R63 1.2×11,106.85 |
| BE-41 | PASS | Regex for .json / .py / work folders / PASO / AUDITORIA: 0 hits |
| BE-42 | PASS | Partition Takeoff identical to rev8 |
| BE-43 | PASS | 6 visible sheets + hidden _reglas |
| BE-44 | PASS | Partition LF / heights unchanged from rev8 (markups not re-run) |
| BE-45 | PASS | Track split 281.09 + 144.06 + 12.67 + 180.99 = 618.81 (old row). Screws 6,114.04 + 13,328.22 = 19,442.26 (unchanged total) |
| BE-46 | PASS | One product per track row. 8/A-210 crop: column = 3-5/8"×16 ga track (R37), beam = 6"×16 ga track (R38), ledger 8" (R39) |
| BE-47 | PASS (re-test 48be3bb5) | RFI-51 now reads "= - 518.29 pcs (518.29 LF of interior bottom track on slab)", which matches RFI row 2 and MS R56. All RFI / ALC IDs cited exist (0 undefined) |
| BE-48 | PASS | Markups PDF not changed in rev9 |
| BE-49 | PASS | No new dimension applied |
| BE-50 | PASS | Unchanged |
| BE-51 | PASS | 2x 8 ft (82 / 3), main tee 12 ft (19), cross tee 4 ft (132), molding 12 ft (11 / 11), wire as coil LF. See comment N3 |
| BE-54 | PASS | 36.74 SF of cement base taken off the S-12 basis (11,143.59 → 11,106.85) and moved to Type S (5,095.03). The two bases sum to 16,201.9 SF board total |
| BE-55 | PASS | No C7-/C8-/C-0x/N-xx codes or "plan check" text left. See comment N2 |

## Blocking issues

None. The two rev9 FAILs (BE-47, BE-52) were corrected in the rebuild md5 48be3bb5.

## Non-blocking comments

- **N1 (C8-03, 775).** I accept 775 as a correct and slightly conservative reading of the three callouts.
  - **Top chord:** 141 × 2 = 282. This follows the leader to the joist chord.
  - **"(2) #8 SCREW AT EACH STUD":** read as 2 per cross member = 282. The leaders end at the two screws at the cross member / track connection. 3/A-410 also says "DO NOT SECURE METAL STUDS OR GWB TO DEEP LEG TRACK", which contradicts the plan-check reading of 2 × 213 wall studs (426).
  - **Possible over-counts, for RFI-41:**
    - "ATTACH TO TRACK W/ #8 @ 24" O.C." (141) may describe the same cross-member screws, which would make it −141.
    - The end P.A.F. (282) and the top-chord #8 may be alternatives at the same end.
- **N2.** Removing "Plan check" left orphan tags and broken punctuation in client text:
  - "decided).(rev7):" in Pending B4; also B6, B7, B15, B16 ("Not carried(rev7)"), B37, B49 and B55. The C56 "(rev8):" tag is gone; the sentence after it now starts lowercase ("... per 8.A. relief channel").
  - RFI-35 B38 has an unclosed "(rev5-rev6 cited 8/A-410 ...".
  - MS R27 has a stray ")" after "RFI-51"; MS R29 needs a separator before "the 1-5/8"".
  - Fix: delete "(revN):" and restore spacing / parentheses.
- **N3.** The new stock lengths are hard-coded in the formulas (`/8`, `/12`, `/4`), not Inputs cells. The sheet header says "Every stock length ... is an Inputs cell", so add Inputs rows for them. R45 hanger count has an empty Selling unit.
- **N4.** RFI-41's alternative 380 pcs uses about 217 LF of parallel walls (479.85 − 262.46). The certificate's 426 uses about 282 LF. One of the two LF figures should be reconciled.
- **N5.** R37 VEST-POSTS-TRACK = 5 LF, but 8/A-210 draws the 3-5/8"×16 ga track as two sides of each nested column box, the same as the beam (25.33 = 2 × 12.67). If the column track also runs full length, it should be 6 × 2 × 10.5 = 126 LF (+121 LF). This value was inherited from rev8; confirm.
- **N6.** A/A-410 "W/ SCREWS TO STUD AS REQ'D BY DESIGN" (clip to stud) has no count. Mention it in RFI-28.
- **N7.** Ceiling perimeter track 180.99 may overlap DGWM24 angle molding. This is already flagged in RFI-54.
