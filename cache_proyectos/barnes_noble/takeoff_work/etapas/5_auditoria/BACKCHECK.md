# BACK-CHECK - Barnes & Noble, Colorado Springs (metal frame / drywall take-off)

Date: 2026-10-24. Independent back-check of
`etapas/8_excel/Barnes_Noble_ColoradoSprings_Takeoff_FINAL.xlsx` against the clean bid set
(`bidset_SIN_MARKUPS.pdf`). Read-only: no input file was modified.
Evidence crops: `etapas/5_auditoria/backcheck_img/`. Scratch scripts: `scratchpad/backcheck/`.

## 1. Method

1. **Blind re-quantification first.** I did not open the Partition Takeoff until the blind numbers below were fixed.
   Sources: A-101 (p6, 1/8" = 1'-0", 9 pt/ft), A-221 (p15, 1/2" = 1'-0", 36 pt/ft), A-410 (p28), A-400A/B (p26/27).
   Sheets are vectorized, so I read printed dimensions from rendered crops and measured lengths from the vector
   geometry: dimension-tick positions (`ticks.py`) and the gray (0.8) new-wall fill polygons (`fills.py`), using
   `Point * page.rotation_matrix` for rotation 270.
2. **Closure checks.** Grid string and north wall string summed and compared with the overall dimension and the vector.
   Cafe workroom string closed against its overall dimension.
3. **Cross-sheet check.** Cafe walls measured on both A-101 (9 pt/ft) and A-221 (36 pt/ft). Heights taken from the A-400A/B
   level marks and the A-410 / A-221 details.
4. **Three-way comparison**: blind result, Excel and plan evidence. Any difference over 2 % is flagged with its delta.
5. **Arithmetic / format**: subtotals and grand total recomputed; Material Summary formulas checked
   (net x waste = waste, net + waste = purchase); board SF = LF x height x faces checked on sample walls;
   RFI deltas checked; Spanish-text and "PENDING" scan.

Status legend: **CONFIRMED** = printed on the sheet. **DERIVED** = computed (the operation is shown).
**PENDING** = not printed / not resolvable from the set.

## 2. Blind numbers (before reading the Excel)

| Item | Blind value | Status / source |
|---|---|---|
| Grid string A-H | 5" + 11'-8" + 27'-0" + 5 x 30'-0" + 5" = **189'-6"**, which equals the printed 189'-6" LEASE DIM | CONFIRMED, closes (A-101 top) |
| North facade, interior face to interior face | 15'-7"+5"+2'-5"+12'-0"+3'-8"+9'-0"+3'-8"+12'-0"+3'-8"+18'-0"+3'-8"+18'-0"+3'-8"+18'-0"+1'-10"+5"+48'-4" = **174'-4" (174.33 LF)** | DERIVED, sum of 17 printed segments. Vector tick-to-tick = 174'-5.6"; after the 0.7" tick-line thickness, the difference is under 1" (closes) |
| North 1A / 1 split | Exterior label west of the adjacent-tenant line (x = 800.4 to 806.4 pt). 1A from 355.8 to 803.4 pt = **49.7 LF**, type 1 from 803.4 to 1925.7 pt = **124.7 LF** | DERIVED, vector measure. The split point is not dimensioned: PENDING (RFI) |
| Type 2 total (A-101), gross through doors | Storage 112: 4.99 + 44.29 + 1.91 + door 3.00 = 54.19 · W of Stock/Corridor x=498: 49.05+8.56+8.57+8.05+11.63 + door 11 gap 6.00 = 91.86 · BOH north wall: 2.73 + door 4 gap 3.00 + 51.45 = 57.18 · Corridor E 7.51 · Restroom/Janitor north run with chase jog, doors 9/8/7: about 25.0 to 25.8 · Men's/Janitor 7.51 · Janitor/Break with door 5: 12.92 · Break/Manager with door 6: 9.42 + 3.50 = 12.92 → **about 269.1 to 269.9 LF** | DERIVED (vector fill extents + door gaps), tags "2" at A-101 |
| Type 5 | 7"-thick plumbing wall between Women's and Men's restrooms: **5.69 LF** | DERIVED (vector) |
| Type 3 (Cafe Seating) | 2 runs x 12'-0" (clear between 5" posts) + 4 posts x 3'-8" = 24.00 + 14.67 = **38.67 LF** (or 40.33 LF counting the 5" post widths in the run). Height **8'-0" AFF** | CONFIRMED dimensions on A-101; height CONFIRMED 3/A-410 |
| C25 column surrounds | 9 columns counted (row 1: 5 at x = 587/857/1127/1398/1667 pt; row 2: 4 at 587/1127/1398/1667 pt). 9 x 4 sides x 2'-0" = **72 LF**, "24"x24" GWB surround over 3-5/8" metal framing from slab to **8'-0" AFF**" | Count DERIVED; size and height CONFIRMED (key note C25, A-101) |
| Cafe type H1 | North: 29.98 LF (west outside face to the Grab & Go "I SIM" end; the finished-face portion 190.7 to 1216.3 pt = 28.49 ft equals the printed 28'-5 7/8"). West: 12.17 LF = printed 12'-2". **Total 42.15 LF**, 6" stud (G/A-221 "H1 = 6" STUD") | DERIVED + CONFIRMED. Cross-sheet: A-101 gives 29.99 / 12.17 (same) |
| Workroom closure | 2'-2 1/8" + 4 7/8" (H2b stub = 3-5/8" + 2 x 5/8") + 25'-10 7/8" = 28'-5 7/8" | CONFIRMED, closes |
| Heights | B.O. deck 25'-0" (1/A-400A, 1/A-400B) · 25'-7" (2/A-400A) · 24'-0" (2/A-400B), all V.I.F. B.O. joist 23'-0" / 23'-7" / 22'-0". Type 2: to underside of deck (2/A-410). Type 3: 8'-0" AFF. Type 4: 7'-6" AFF. C25: 8'-0" AFF. Cafe H1/H2: the section breaks at the top | CONFIRMED (levels). Cafe heights PENDING |
| Studs (A-410) | Types 2/3/4: 3-5/8" @ 16" O.C. · Type 5: 6" @ 16" · H1 6", H2 3-5/8" (G/A-221) · 3-5/8" schedule maximum at 16" O.C. = 22'-0" (14 ga SJ) | CONFIRMED |

## 3. Three-way comparison (blind / Excel / evidence)

| Item | Blind | Excel | Delta (Excel - blind) | % | Evidence | Result |
|---|---|---|---|---|---|---|
| North facade 1A + 1 (EXT-01 + EXT-02) | 174.33 | 16.33 + 159.35 = 175.68 | +1.35 | +0.8 % | A-101 north string | OK |
| North type **1A** only | 49.7 | 16.33 | **-33.4** | **-67 %** | A-101: "EXTERIOR" north of x < 800 pt; "ADJACENT TENANT" from x > 800 pt | FLAG (already RFI-02, 33.54 LF) |
| North type **1** only | 124.7 | 159.35 | **+34.7** | **+28 %** | same | FLAG (RFI-02) |
| Type 2 total | 269.1 to 269.9 | 273.57 | +3.7 to +4.5 | +1.4 to +1.7 % | A-101 | OK |
| W2-01+02 Storage | 54.19 | 53.76 | -0.43 | -0.8 % | A-101 | OK |
| W2-03 + W2-04 | 149.04 | 151.00 | +1.96 | +1.3 % | A-101 | OK |
| W2-05 Corridor E | 7.51 | 7.92 | +0.41 | +5.5 % | A-101 | minor (start point at the restroom front line) |
| W2-06 Restroom north run | 25.0 to 25.8 | 27.54 | +1.7 to +2.5 | +7 to +10 % | A-101 | FLAG minor: Excel runs outside extents (555.8 to 763.6 pt) + full-depth jogs, which overlaps the T-junctions with W2-05/07/08 |
| W2-07 / W2-08 / W2-09 | 7.51 / 12.92 / 12.92 | 7.51 / 12.92 / 12.92 | 0 | 0 % | A-101 | OK |
| Type 5 | 5.69 | 5.70 | +0.01 | 0 % | A-101, 5/A-410 (6") | OK |
| Type 3 | 38.67 | 38.68 | +0.01 | 0 % | A-101, 3/A-410 | OK. Height 8 ft OK, 3-5/8" @ 16" OK |
| C25 column surrounds | 9 x 8 LF = 72 LF, 8'-0" | 9 x 8 LF, 8 ft, 3-5/8" @ 16" | 0 | 0 % | key note C25 | OK (spacing not printed: RFI-17) |
| H1 | 42.15 | 29.98 + 12.17 = 42.15 | 0 | 0 % | 1/A-221, G/A-221 | OK. 6" stud OK. Height 25 ft loaded, not printed (RFI-06) |
| H3a / H3b | 4.08 / 6.17 | 4.08 / 6.17 | 0 | 0 % | 1/A-221 | OK |
| Type 2 height | deck 24'-0" (W) to 25'-7" (E), 25'-0" at 1/A-400A/B | 25.0 ft all type 2 | W2-03 near the west facade could be about 24'-0" to 24'-3" (-0.8 to -1.0 ft, about -3 to -4 %) | | A-400A/B | covered by RFI-03 (683.46 LF per ft) |
| Type 2 stud size | 3-5/8" @ 16" max 22'-0" | 3-5/8" @ 16" at 25 ft | over the schedule limit | | A-410 schedule | covered by RFI-04 / RFI-07 |

## 4. Arithmetic checks

- **Partition Takeoff subtotals**: every SUBTOTAL row is a live `=SUM()` and equals the sum of its rows. Grand total
  979.87 LF / 17,852.41 SF = the sum of the subtotals. LF by stud size: 3-5/8" 761.54, 6" 118.59, 8" 99.74. Each equals
  the Material Summary bottom/top track net for that size. **OK.**
- **Material Summary**: on every row, Waste = Net x Waste % and Purchase = Net + Waste (= Net x (1 + w)). No errors.
  Waste % links to Inputs (15 % metal, 6 % non-metal). Screws, mud and tape yields re-compute
  (1.2 x 16,562.77 = 19,875.3; 0.072 x 16,562.77 = 1,192.5; 0.37 x 16,562.77 = 6,128.2). **OK.**
- **Board SF = LF x height x faces** (5 walls):
  W2-01+02 53.76 x 25 x 2 = 2,688 ✓ · W3-02 12 x 8 x 2 = 192 ✓ · W4-28 12.68 x 7.5 x 2 = 190.2 ✓ ·
  EXT-04 (1B sheathing, 1 face) 13.2 x 24 x 1 = 316.8 ✓ · W2-04 56.76 x (25 + 9.5) = 1,958.2 ✓ (one face full
  height, the ceiling side at ceiling + 6", the RFI-19 rule). The board SF cells are hard-coded values, not formulas.
- **Sheet counts (FINDING)**: 5/8" gyp board, 1/2" exterior sheathing and cement board use `=ROUNDUP(F/32,0)`
  (a hard-coded 4x8 sheet). Inputs B7/B8/B9 say 4 x 12 = 48 SF and that "every sheet count re-rounds", but those
  rows ignore Inputs. The FRT plywood rows do use Inputs!B9.

## 5. Pending Items / language / status

- All 32 Pending Items have a "Delta of each alternative" entry. Most give a number (LF, SF or pcs). Weak deltas:
  **RFI-25** (C5 demising patch) gives only an allowance basis, with no figure. **RFI-ACC-stud-reinforcement-mep** gives a
  per-duct rule only. **RFI-12 / RFI-13** give partial figures ("about 76 SF", "~81 LF x 10'-0"").
- RFI-02 delta spot-check: blind 1A shift = 49.7 - 16.33 = 33.4 LF, against 33.54 LF in the RFI. ✓
- Spanish text: none found (accents, ¿¡ and a Spanish keyword list, all sheets). The only exception is the hidden `_reglas`
  sheet, which holds just a hash. "PENDING" in Partition Takeoff: none. Every row is [DERIVED] with a DETAIL/SHEET source.

## 6. Findings ranked by severity

1. **MEDIUM - North facade 1A / 1 split (A-101).** Excel puts the change at W2-03 (1A = 16.33 LF). The plan labels
   the facade "EXTERIOR" up to the adjacent-tenant line at x = 800.4 pt, which gives 1A = 49.7 LF and type 1 = 124.7 LF.
   Delta: 33.4 LF moves from 1 to 1A (-67 % / +28 % on those rows). The framing is the same (3-5/8"), so there is no
   material cost change while the gyp board stays "by future tenant". This matters if RFI-01 brings the exterior
   board into scope. Already disclosed as RFI-02. Recommendation: take the tenant edge as the default.
2. **MEDIUM - Board / sheathing / cement-board sheet count hard-coded to 32 SF** (Material Summary rows 20, 21, 23),
   which contradicts the Inputs 4x12 (48 SF) parameter. At 4x12 the 5/8" board would be 366 sheets instead of 549, and
   the sheathing 55 instead of 82. The SF quantity is correct; the purchase-unit count does not follow Inputs.
3. **LOW - Type 2 height on the west side.** Everything is carried at 25'-0". 2/A-400B shows the deck at 24'-0" at the
   west, so W2-03 (94.24 LF) may be about 0.8 to 1 ft high (about 75 to 95 SF per face). Covered by RFI-03.
4. **LOW - W2-06 restroom run +1.7 to +2.5 LF (+7 to +10 %)** and **W2-05 +0.41 LF (+5.5 %)**. These come from corner
   overlaps at T-junctions (outside extents plus full-depth jogs). Impact on the type 2 total is below 1 %.
5. **INFO - Weak RFI deltas**: RFI-25 has no figure; RFI-ACC-stud-reinforcement-mep gives a per-unit rule only.
6. **INFO - Already disclosed, consistent with the plans**: 3-5/8" studs at 25 ft exceed the 22'-0" schedule limit
   (RFI-04/07). Cafe heights are not printed (RFI-06). C25 stud spacing is not printed (RFI-17).

## 7. Verdict

**PASS WITH COMMENTS.** Every blind re-quantification requested is within 2 % of the Excel on the type totals:
north facade 1A + 1 (+0.8 %), type 2 (+1.4 to 1.7 %), type 3 (0 %), C25 x 9 (0 %), H1 (0 %), type 5 (0 %). Dimension
strings close and the A-101 / A-221 cross-sheet check matches. Heights and stud sizes agree with A-400A/B, A-410 and
G/A-221, or are disclosed as RFIs. The arithmetic is sound. No Spanish text and no PENDING quantities were found.
Before issue: (1) decide the north 1A / 1 split (RFI-02); (2) link the board / sheathing / cement-board sheet counts
to Inputs!B9 (or relabel Inputs to 4x8).

---
## Addendum (main session, after the back-check) — disposition of findings
- **Finding 2 (sheet counts ignore Inputs) — FIXED.** The board / sheathing / cement board rows came through the plantilla_excel R80.4 fallback with a hard 4x8 sheet. They now use `4x12 ft sheet (Inputs)` and `ROUNDUP(F/Inputs!$B$9,0)`. After recalculation: 5/8" gyp bd 366 sheets, 1/2" exterior sheathing 55, cement board 19 — the same values this back-check computed at 4x12. Only the selling-unit column changed; no SF or LF moved.
- **Finding 1 (north 1A / 1 split)** — left as carried; already RFI-02 (33.54 LF) and Review Item 2. Added to the estimator questions. Framing cost is the same (both 3-5/8").
- **Finding 3 (type 2 height at the west, 24'-0")** — covered by RFI-03 (deck V.I.F., 24'-0" to 25'-7").
- **Finding 4 (T-junction overlaps W2-06 / W2-05)** — under 1% of the type 2 total; W2-05 is Review Item 4. Listed for the estimator.
- **Finding 5 (weak RFI deltas)** — RFI-25 is an allowance by nature (extent not measurable); kept, flagged in PARA_REVISAR.
