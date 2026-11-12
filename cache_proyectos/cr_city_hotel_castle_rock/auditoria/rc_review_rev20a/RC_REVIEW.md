# U-181 Independent review: Resilient channel 1/2" (RC), CR City Hotel rev20

Under review: `CR_City_Hotel_Takeoff_FINAL_rev20.xlsx`, sheet "Material Summary", row 14, C14 = **27,124.98 LF** net [CONFIRMED, cell value]. In rev19 the same cell was 19,598.31 LF [CONFIRMED], so the change is +7,526.67 LF [DERIVED].
Reviewer: U-181 (independent; read-only on /root/cr/work and /root/skill).

## Verdict: **OK with notes** (no LF delta on the governing reading)

My independent rebuild comes to **27,124.96 LF** [DERIVED]. The take-off has 27,124.98 LF, so the difference is **-0.02 LF** [DERIVED], which is rounding of the items. FS-1 spacing (12 in) and the end-joint requirement are confirmed. There are no double counts beyond a few LF, and waste is applied once. The notes below are open items and sensitivities. None of them is a quantity error in the current reading of the documents.

## 1. Governing documents

| Point | Source (verified) | Result |
|---|---|---|
| FS-1 scope | A0.08 (PDF p.12): "FS-1 LEVEL 2, 3, 4 THROUGHOUT 1 HOUR (1/2 HR REQD.) L546" and "FS-1 LEVEL 2 ABOVE PARKING AT ALLEY ... L546" [CONFIRMED] | Membrane under L2, L3 and L4 floors = L1, L2 and L3 ceilings |
| FS-1 RC | A0.08 FS-1: "RESILIENT CHANNELS, SPACING PER ASSEMBLY TO ACHIEVE FULL CAVITY INSULATION", "NON-COMBUSTIBLE FIBERGLASS BATT INSULATION TO FILL ENTIRE FRAMING CAVITY", "5/8" TYPE C GYPSUM BOARD CEILING" [CONFIRMED] | RC spacing is the one UL L546 allows for full-cavity batts |
| Truss depth | S1.02 (p.90) general notes: 18" pre-engineered open-web wood trusses; TOS 13'-8" [CONFIRMED] | Full cavity is well over 3-1/2 in. of batt |
| UL L546 Item 5 | "When the resilient channels (Item 6) ... are spaced 16 in. OC, the insulation shall be a max of 3-1/2 in. thick ... When ... spaced a max of 12 in. OC ... there is no limit in the overall thickness of insulation ... or draped over" [CONFIRMED, L546.pdf] | Full-cavity batt requires a spacing of **12 in. OC or less** |
| UL L546 Item 6 | "spaced 16 in. OC ... When insulation (Items 5, 5A, 5B) is draped over the resilient channel/gypsum board ceiling membrane, the spacing shall be reduced to 12 in. OC ... Two channels, spaced 6 in OC, oriented opposite each gypsum board end joint ... Additional channels shall extend 6 in beyond each side edge of board." [CONFIRMED] | **FS-1 = 12 in. OC [CONFIRMED by Items 5 and 6]**. **End-joint channel pairs are required [CONFIRMED]** |
| UL L546 Item 7 | Board "48 in. wide ... long dimension perpendicular to resilient channels ... End joints secured to both resilient channels" [CONFIRMED] | Basis for the end-joint geometry |
| FS-1 beam wrap | A0.08 note: "GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES" [CONFIRMED]; A3.01 "ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS" [CONFIRMED in text layer p.22] | BW rows are in scope |
| RS-1 | A0.08 RS-1 "ROOF RE: A2.05", RATING blank, UL # blank. Ceiling callout reads "CEILING. RE: REFLECTED CEILING PLANS AND OTHER DETAILS ..." with a channel drawn under the framing but **not labelled as resilient channel** [CONFIRMED, crop a008_rs1.png] | No UL, so no end-joint pairs. Spacing is not printed |
| Spec | 09 22 16 2.2.E.4 "Resilient Furring Channels: 1/2-inch deep" [CONFIRMED]; 3.1.A "Installation Standard: ASTM C 754, except comply with framing sizes and spacing indicated" [CONFIRMED] | RS-1 at 16 in. OC is an assumption ([PENDING], see note N1) |

## 2. Independent recompute (net LF, before waste)

Area sources: the canon `ceilings[]` (52 rows; area_sf equals the shoelace area of each contour polygon divided by 81 for all 52 rows, checked) and the misc rows I re-derived from their printed dimensions. LF = SF x 12 / spacing(in).

| # | Component | Basis (my operation) | Mine (LF) | Take-off (LF) | Diff | Citation |
|---|---|---|---|---|---|---|
| a1 | FS-1 L1 plate (membrane under L2 floor) | 7,711.49 SF x 12/12 | 7,711.49 [DERIVED] | 7,711.49 | 0 | A0.08 FS-1; UL L546 It.5/6; A3.01 |
| a2 | FS-1 L2 ceilings (21 rooms) | 7,003.05 SF x 12/12 | 7,003.05 [DERIVED] | 7,003.05 | 0 | A3.02, 1/A2.02 |
| a3 | FS-1 L3 ceilings (21 rooms) | 6,371.71 SF x 12/12 | 6,371.71 [DERIVED] | 6,371.71 | 0 | A3.03, 1/A2.03 |
| a4 | FS-1 closet boxes L2 (14) + L3 (10) | (103.33 + 65.59) SF x 12/12 | 168.92 [DERIVED] | 168.92 | 0 | A3.02 / A3.03 |
| b1 | RS-1 L4 ceilings (10 rows) | 3,424.60 SF x 12/16 | 2,568.45 [DERIVED] | 2,568.45 | 0 | A0.08 RS-1; A3.04 |
| b2 | RS-1 L4 strips/closets (405C, 403C, 404C, 412A/B/C, 401D, 402D) | 114.14 SF x 0.75 | 85.61 [DERIVED] | 85.61 | 0 | 1/A3.04 |
| b3 | RS-1 L4 membrane above dropped bath GYP-1 (106R to 114R), new in rev20 | 484.63 SF x 0.75 | 363.47 [DERIVED] | 363.48 | -0.01 | 1/A3.04, A2.04 |
| b4 | Mech mezzanine 219, sloped roof (CLG-L2-64) | 536.72 SF x 0.75 | 402.54 [DERIVED] | 402.55 | -0.01 | 1/A4.04, 1/A2.02 |
| c | FS-1 end-joint extra channel | 7,711.49/12 + 7,003.05/12 + 6,371.71/12 = 642.62 + 583.59 + 530.98 | 1,757.19 [DERIVED] | 1,757.19 | 0 | UL L546 Item 6 |
| d1 | Beam wrap, retail 124 | 154.23 LF x 3 lines + 68.80 LF x 2 lines (LF re-added: 22.35+22.32+22.35+20.29+19.49+31.67+15.76; 32.58+19.37+16.85) | 600.29 [DERIVED] | 600.29 | 0 | A0.08 note; A3.01; S1.02 |
| d2 | Beam wrap, grid 1 north (new in rev20) | 46.12 LF (29.06+17.06) x 2 lines | 92.24 [DERIVED] | 92.24 | 0 | 4/S3.08; S1.02 |
| | **Total net** | | **27,124.96 [DERIVED]** | **27,124.98 [CONFIRMED C14]** | **-0.02** | |

Material Summary row 14 [CONFIRMED formulas]:
- D14 = `Inputs!B5`, which is 0.15 ("ALL METAL").
- E14 = C14 x D14.
- F14 = C14 + E14, so 27,124.98 x 1.15 = **31,193.73 LF purchase** [DERIVED].
- H14 = ROUNDUP(F14 / `Inputs!B17`), with B17 = 12 ft. 31,193.73 / 12 = 2,599.48, which rounds up to **2,600 pcs** [DERIVED].

The canon rows hold only net quantities (none of them contains a waste factor), so **waste is applied once**. There is no rounding on the net.

### Rev19 to rev20 bridge (+7,526.67 LF)

| Driver | Operation | LF |
|---|---|---|
| FS-1 spacing 16 to 12 in. OC | (21,086.25 + 168.92) SF x (1 - 0.75) | +5,313.79 [DERIVED] |
| End-joint channels L1/L2/L3 | item c | +1,757.19 [DERIVED] |
| L4 bath RS-1 membrane rows | item b3 | +363.47 [DERIVED] |
| BW-L1-NORTH | item d2 | +92.24 [DERIVED] |
| **Sum** | | **+7,526.69 [DERIVED]** (vs +7,526.67; rounding) |

As a cross-check, I rebuilt rev19 at FS-1 = 16 in. without b3, c or d2 and got 19,598.26 LF [DERIVED], against 19,598.31 in the rev19 sheet [CONFIRMED].

## 3. Spot-checks of canon areas against the RCP (wall-face vectors)

Method: I took each polygon's bounding faces (A2.0x plan coordinates) plus the stated plan-to-RCP offset (L2 [13.1, 19.5] pt; L3/L4 [13.3/13.2, 18.7] pt) and matched them to the drawn wall-face lines on the RCP sheet with pymupdf get_drawings. The scale is 9 pt/ft (1/8"=1'-0"). "Match" means the face is within 0.5 pt (0.06 ft).

| Level / sheet | Ceiling | Polygon faces + offset (pt) | RCP wall faces found (pt) | Result |
|---|---|---|---|---|
| L1 / A3.01 | FS-1 plate | W 550.08, N 372.34, S 1289.74, E 1771.44 | W 550.44/550.80, N 372.60, S 1290.00, E 1770.00 | W/N/S match (<=0.7 pt). E is 1.4 pt (0.16 ft) off because the L2 wing overhangs L1 (noted in canon) |
| L1 | FS-1 plate, gross check | 7,711.49 net vs A0.01 "LEVEL 2 8,587 SQ FT TOTAL GROSS" [CONFIRMED p.4] | | Plausible (gross minus wall band, stairs, hoistways) |
| L2 / A3.02 | 202 (333.24 SF) | x 871.82 to 1075.22; y 530.5 to 667.4 | 871.68 / 1075.20; 530.76 / 667.68 | Match; bbox 22.6 x 15.2 ft, closet notch carried in 202C |
| L2 / A3.02 | 203 (333.48 SF) | x 871.82 to 1075.22; y 674.3 to 811.3 | 871.68 / 1075.20; 674.16 / 811.56 | Match |
| L2 / A3.02 | 205 (564.17 SF) | x 871.7 to 1072.46; y 962.1 to 1225.5 | 871.68 / 1072.32; 961.92 / 1225.80 | Match |
| L3 / A3.03 | 302 (251.24 SF) | x 872.0 (W); y 529.66 to 666.58 | 871.68; 529.44 / 666.84 | Match. E edge clipped at RS-6 terrace, x 1007.35 plan |
| L3 / A3.03 | 305 (563.92 SF) | x 871.8 to 1072.56; y 961.3 to 1224.7 | 871.56 / 1072.68; 961.08 / 1224.96 | Match; printed 468 SF excl. bath (A2.03) |
| L3 / A3.03 | 310 (383.84 SF) | x 550.08 to 806.76; y 1162.18 to 1289.74 | 549.84 / 807.00; 1162.44 / 1290.00 | Match |
| L4 / A3.04 | 403 (512.92 SF) | x 553.08 to 806.4; y 812.98 to 1088.98 | 553.20 / 806.52; 813.12 / 1089.12 | Match |
| L4 / A3.04 | 404 (313.34 SF) | x 553.08 to 716.88; y 592.06 to 806.02 | 553.20 / 717.00; 592.20 / 806.28 | Match |
| L4 / A3.04 | 406 Cleaning (119.74 SF) | x 759.12 to 865.92; y 375.34 to 474.58 | 759.24 / 866.04; 375.12 / 474.72 | Match |

Limit: I checked the outer faces of each ceiling, not every interior notch. All 52 canon areas equal their own polygon areas (shoelace / 81).

Overlap check (shapely): the closet "C" boxes (A3.0x coordinates) and bath "R" boxes (A2.04 coordinates) do not overlap their room polygons in the coordinate system each row states. Two R boxes, read in RCP coordinates, touch neighbours: 106R by 14.2 SF into 402, and 110R by 5.6 SF into the corridor. That is at most about 15 LF and negligible.

## 4. End-joint method check (item c)

The take-off uses LF = SF / 12 (one extra channel per end-joint line of 12-ft boards). My independent estimate works room by room:
- Each 4-ft board row has ceil(L/12) - 1 end joints.
- Each joint adds one channel of 4 ft + 2 x 6 in = 5 ft (Item 6 "extend 6 in beyond each side edge").
- I computed both board orientations from the polygon bbox, scaled to the net area.

This gives 1,590 to 1,845 LF [DERIVED], depending on orientation; the per-level figures are in the script output. The take-off's 1,757.19 LF falls inside that range, so the method and magnitude are **OK**. It slightly undercounts the 6-in extensions on the L1 plate (756 to 781 LF vs 642.62) and overcounts small rooms on L2/L3 (431 to 557 vs 583.59 L2; 403 to 506 vs 530.98 L3). These offset each other.

## 5. Notes (no change to C14 on the governing reading)

- **N1 [PENDING], RS-1 spacing and channel type.** A0.08 RS-1 has no rating and no UL #. Its ceiling callout defers to the RCP and does not name resilient channel; the drawn profile is a channel. 09 22 16 3.1.A defers to ASTM C 754 "spacing indicated", and none is indicated. The 16 in. OC is therefore an estimator assumption, carried since rev19 (the canon cites RFI-14 / RFI-CR-RS1).
  - Sensitivity: the RS-1 family (b1 to b4) covers 4,560.09 SF (3,424.60 + 114.14 + 484.63 + 536.72) and gives 3,420.07 LF at 16 in. At 24 in. OC it would be 2,280.05 LF, a difference of **-1,140.02 LF** [DERIVED]. If the designer intends hat channel, those LF move to another row.
  - The b3 bath rows (+363.47 LF) also depend on the RS-1 membrane being continuous above the dropped bath GYP-1 at an unrated roof. That is a reasonable reading but not printed.
- **N2, beam-wrap bottom line vs field.** The L1 plate SF includes the beam footprints, so the "bottom" line of each wrap (269.15 LF of beams) partly duplicates field channel across about a 0.59-ft flange. The overlap is at most about 160 LF [DERIVED: 269.15 x 0.59]. This is conservative, defensible as wrap framing, and within tolerance.
- **N3, beam-wrap drops.** The retail side drops are carried as 1 line per face; the drop is not printed (RFI-20 in canon). From AISC d, the side faces are 5 to 12 in, so 1 line per face at 12 in. OC is adequate. W18 beams elsewhere (S1.02) project about 1 to 2 in below the trusses. The canon (rev9 MISC) resolves the lobby with a lowered rated plane at 12'-0 3/4" (7/A7.31 "W18X71 DEEPEST BEAM IN LOBBY"). I did not re-check every W18 for exposure ([PENDING], likely nil).
- **N4, net excludes splice laps and perimeter extra lines.** These cover the Item 6 4-in overlap at splices (about +2.8% on 12-ft sticks) and +1 channel per bay edge. They are covered by the 15% metal waste in D14, so no change is needed.
- **N5, description cell.** Row 14 col I lists the L4 rows at x 0.75 (e.g. 412 Corridor 818.26 = 1,091.02 x 0.75), consistent with the table above.

## Files

- Overlays: `ov_A3.0x.png` and `crop_A3.0x.png` in `/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/rc_review/`. The polygons are drawn in A2 coordinates, without the offset.
- RS-1 detail crop: `/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/rc_review/a008_rs1.png`
- Wall-face extraction script: `/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/rc_review/seg.py`
- UL text dump: `/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/rc_review/L546.txt`
