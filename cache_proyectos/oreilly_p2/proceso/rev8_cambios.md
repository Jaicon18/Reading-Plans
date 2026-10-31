# Rev8 changes: O'Reilly Auto Parts, Evans CO, pass 2 (element 4: track and RC)

Backups:
- `takeoff_canon_AB_rev7.json` is the canon before rev8.
- `overlay_OReilly_p2_rev7.json` is the overlay before rev8, including the G-flow group.
- The older file with the same name was kept as `overlay_OReilly_p2_rev7_preGflow.json`.

Edited files:
- `takeoff_canon_AB.json` (the reading):
  - `bottom_track` / `top_track` / `track_source` / `top_track_info` of every wall
  - misc DLT-S42-FULL split into DLT-S42-01 and DLT-S42-04
  - `deflection_clips.slip_track_source`
  - new RFI-20, RFI-21 and RFI-22
- `overlay_OReilly_p2.json`:
  - new group **G-rev8**, which upserts ZF-RUNNER-S21 = 577.25 LF
  - G25 text updated
- `canon_ov.json`, regenerated with `overlay.aplicar_canon`. Applying it twice gives the same result.

Checks:
- `validar_canon.py` reports CANON OK on both files.
- `tools/canon.py canon_ov.json /tmp/rev8_out` exits rc 0 with `partition_types.avisos = []`.

Rule #0 applies: nothing was scaled. Every LF below is a printed wall length x 1. Each crop in `img_rev8/` was rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, circled, then reopened and checked.

## Verified notes
- **A1.1 Interior Wall & Ceiling Notes 2.C** reads: "WHERE WALL FRAMING EXTENDS TO BOTTOM OF ROOF DECK OR STRUCTURE, PROVIDE DEFLECTION CHANNELS AT TOP TRACK FOR 1 1/2" MINIMUM DEFLECTION." Image: `img_rev8/rev8_p1_A1.1_note_2C_deflection.png`.
- **S1.1 7.E** reads: "WALL STUDS SHALL SEAT SQUARELY WITHIN METAL TRACK OF SAME SIZE GAUGE". The track gauge = stud gauge is therefore **printed**. The 1-1/4" flange (T125) is derived from 3/S5.1 and 4/S5.1, which print 362T125-33. This is the same as the skill rule "calibre que el plano no nombra": stud 362S162-33 -> track 362T125-33.
- **S1.1 7.B** reads: "SLIP TRACK ASSEMBLIES ... SSMA TECHNICAL NOTE #1". Image: `img_rev8/rev8_p3_S1.1_7B_7E_track_same_gauge.png`.

## 1-3. Wall -> top reaches structure? -> track family -> product / gauge -> LF -> N/SHEET -> image
LF = length x 1 (rows 1). Standard bottom and top go to `bottom track (todos)` / `top / deflection track (todos)` through corridas.py. Deflection walls go to misc `deep-leg slotted deflection track (printed)`.

| Wall | Top reaches structure? | Family (top) | Product / gauge, bottom / top | LF bottom / top | N/SHEET | Image |
|---|---|---|---|---|---|---|
| S42-01 | **Yes**, PEMB purlin, 1-1/2" CLR. | **[DEFLECTION]** misc DLT-S42-01 | 362T125-33 (printed) / 3"x14ga deep-leg slotted, 3-5/8" web (derived), 68 mil | 38.67 / 38.67 (misc) | 4/S5.1; A1.1 2.C | rev8_p1_S5.1_3_4_deep_leg_and_362T125-33.png |
| S42-04 | **Yes**, PEMB purlin | **[DEFLECTION]** misc DLT-S42-04 | 362T125-33 (printed) / 3"x14ga deep-leg slotted | 8.17 / 8.17 (misc) | 3/S5.1; A1.1 2.C | same |
| S42-02 | Hung from the purlins: fixed screwed connection to 600S200-54, bottom free | [STANDARD] | 362T125-33 / 362T125-33 (top **not drawn**: conservative assumption carried per S1.1 7.E, RFI-22; 2.C on hung framing: RFI-20) | 25.45 / 25.45 | 1/S5.1; 6/A4.2 k11; S1.1 7.E | rev8_p1_S5.1_1_2_header_walls_hung_fixed.png |
| S42-03 | Hung from the purlins: L4x4 clip + CONT 6" each side, fixed | [STANDARD] | 362T125-33 / 362T125-33 (top not drawn, RFI-22; RFI-20) | 50.33 / 50.33 | 2/S5.1; S1.1 7.E | same |
| VH-C / VH-B1 / VH-B2 | Hung: key 8 "ATTACHED TO" the PEMB framing, bottom free over the storefront head | [STANDARD] | 600T125-43 (18 ga = key 8 600S162-43) / 600T125-43 (RFI-20) | 8.75 + 5.67 + 5.67 = 20.08 / 20.08 | 3/A3.1 key 8; 3/A5.2 | rev8_p1_A3.1_3_VH_key8_attached_to_PEMB.png |
| EXT-MS1-8 / EXT-MS2-8 | No: T.O. METAL STUD 120'-8" under FRT nailer, free top above the roof (T.O. HIGH EAVE 116'-4 3/4") | [STANDARD] | 800T125-54 / 800T125-54 | 6.0 + 6.0 / 12.0 | 1/A3.1 key 11; 7/A3.2; 3/S5.3 key 18 | rev8_p1_A3.1_1_2_EXT-MS_HEAD-A_top_above_roof.png |
| EXT-MS1-6 / EXT-MS2-6 | No (same) | [STANDARD] | 600T125-54 / 600T125-54 | 12.0 / 12.0 | 1/A3.1; 3/S5.3 key 17 | same |
| HEAD-A-8 / HEAD-A-6 | No (same, 2/A3.1) | [STANDARD] | 800T125-54 and 600T125-54 | 38.67 each / 38.67 each | 2/A3.1 key 11; 3/S5.3 | same |
| CORN-S | No: top of the cornice under the FRT nailer, bottom on masonry | [STANDARD] | 600T125-43 (key 22 18 ga min.) | 36.0 / 36.0 | 1/S5.3 keys 4 / 22; 6/A3.4 | (rev6/rev7 S5.3 crops) |
| S24-OF / -RR / -RRS | No: 8'-6" under the hard-lid joists (own framing) | [STANDARD] | 362T125-33 | 37.38 / 37.38 | 7/A4.2 key 5; A1.1 | img_rev6/rev6_p2_A4.2_key5_joists.png |
| S43-OF-W / -E / -S, S43-RR-W / -S | No (8'-6" hard lid) | [STANDARD] | 362T125-33 | 52.73 / 52.73 | 7/A4.2; A1.1 | same |
| S61-RR | No (8'-6" hard lid) | [STANDARD] | 600T125-33 | 8.5 / 8.5 | S61/A1.1; 7/A4.2 | img_rev6/rev6_p2_A1.1_types_S41_S42_S43_S61.png |
| S41-B1V / B1H / B2H / B2V | No: 12'-0" free-standing | [STANDARD] cap | 362T125-33 | 6.46 / 6.46 | S41/A1.1; note 2.B | same |
| S21-N/E/S/W1/W2 | Z-furring on CMU, stops under the purlin (RFI-01); not a stud wall spanning to structure | [STANDARD] runner, misc ZF-RUNNER-S21 | 1-1/2" runner, 18 mil | 288.625 / 288.625 (misc, 577.25) | S21/A1.1; RFI-16 = B | img_rev6/rev6_p2_A1.1_types_S21_S24.png |

Family totals (canon_ov, /tmp/rev8_out):

| Family | rev7 | rev8 | Change |
|---|---|---|---|
| `bottom track (todos)` | 385.11 | 385.11 | unchanged |
| `top / deflection track (todos)`, the standard top | 385.11 | **338.28** | -46.83, S42-01 / -04 removed |
| `deep-leg slotted deflection track (printed)` | 46.83 | 46.84 | DLT-S42-01 38.67 + DLT-S42-04 8.17 |

## 2. Double count: tool behaviour and fix
**Cause** (`tools/corridas.py`, `calcular`, the two lines `b = bool(r.get("bottom_track", True))` / `t = bool(r.get("top_track", True))`):
- Any truthy `top_track`, including a descriptive string, counts L x rows in `top / deflection track (todos)`.
- `canon.py` (`generar`, runs dict) passes `top_track` / `track_source` through unchanged.
- In rev7, S42-01 / -04 carried a string top_track, so they were counted in the generic top (46.83 LF) **and** in DLT-S42-FULL (46.83 LF).

**Fix, with existing keys only:**
- On S42-01 / S42-04, `top_track: false` plus `track_source` "4/S5.1 ..." / "3/S5.1 ..." (R80e.23, declared absence). The E10 / A_TRACK_RUNS gate accepts this.
- The deflection track is counted once, in misc DLT-S42-01 / DLT-S42-04 (length x 1, with source and op).

**Limitation, so the order is not met literally:**
- A `top_track` that starts with "[DEFLECTION] " is a truthy string, so corridas.py would count it in the generic family again.
- The "[DEFLECTION] ..." tag and product therefore sit at the start of `top_track_info` on S42-01 / -04.
- The same applies to S21: `top_track` / `bottom_track` must stay `false` because the runner is a misc item. Its "[STANDARD] ..." tag is in `top_track_info`.
- Every other wall has the prefix at the start of `top_track`.
- Putting the tag literally in `top_track` while also excluding the wall would need a change in corridas.py, for example reading `top_track` strings that start with "[DEFLECTION]" as false. Not done, as instructed.

`deflection_clips.slip_track_source` now points to DLT-S42-01 / -04. The 0 + RFI from accesorios stays: there are no `to_deck` walls.

## 4. Doors, runner, additional head track
- **Doors (E10):** bottom track is never deducted at doors. `corridas` reports doors_ro 10.0 LF as an RFI delta only.
- **ZF-RUNNER-S21:** 564.58 -> **577.25 LF** = 2 x 288.625. The "- bottom at doors 3 / 2 / 7 (12.667)" deduction is removed (E10, in overlay G-rev8). The runner LF is the wall length, top and bottom, and does not depend on the Z-furring height (top under the purlin, RFI-01).
- **Additional head track 32.73 LF:** Door 3 7.33 + D1 12.70 + D2 12.70, skill criterion "precedent of a previous project".
  - This set does not print it. A5.1 head details 1 / 3 / 5 (CMU + bond beam / masonry lintel, Z-furring + FRT 2x4 blocking anchored to masonry) and 7 (600S162-33 box header) draw no head track.
  - All three openings are in S21 Z-furring on CMU, with header steel_by_others.
  - The criterion stays carried. New **RFI-21**: (A) 32.73 carried | (B) 0, delta -32.73 LF. Image: rev8_p4_A5.1_head_details_no_addl_head_track.png.

## 5. RC (087F125-33)
RC-EXT-MS **120.51 LF, unchanged and verified.**

**@ 24" O.C. horizontal is printed:** A3.1 / A3.2 / A3.4 key 33.

**Where tag 33 appears:** 1/A3.1 (pier, interior face below the ceiling), 2/A3.1 (head face) and 7/A3.2 (pier plan section). It does not appear on 3/A3.1 (vestibule heads), the A3.2 sections 1-4, the A3.4 sections, A4.2 (the key list has no RC) or any ceiling, so there is no RC elsewhere.

**Rows:**
- Piers at 12.0 (RFI-16 = A): ROUNDUP(12/2) + 1 = 7 rows.
- EXT-MS1: 7 x 6.0 = 42.0.
- EXT-MS2: 7 x 3.08 = 21.56 in Parts A, plus 9 x 2.92 = 26.28 in Parts B (15.729 under the purlin).
- Head: 1 row x 30.667 = 30.67 (11'-4" -> 12'-0").

Image: rev8_p5_A3.1_key33_RC_piers_head.png.

## New RFIs (canon `rfis`)
| RFI | Topic | Carried | Delta |
|---|---|---|---|
| RFI-20 (A plans / B code) | A1.1 2.C deflection on hung framing (S42-02 / -03, VH) | A: standard track (fixed connection printed) | B: standard top -95.87 LF / deep-leg +95.87 LF (75.79 at 3-5/8" + 20.08 at 6") |
| RFI-21 | Additional head track, not printed | A: 32.73 LF (skill criterion) | B: -32.73 LF |
| RFI-22 | Top track of S42-02 / -03, not drawn on 1/S5.1 or 2/S5.1 | A: 75.79 LF 362T125-33 (S1.1 7.E, conservative) | B: -75.79 LF |
