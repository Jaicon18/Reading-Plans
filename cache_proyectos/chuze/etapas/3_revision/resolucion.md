# Stage 3 resolution — Chuze Fitness Austin Bluffs (metal frame / drywall)

Inputs: reading A (Z1-Z6 + general), reading B (Z1-Z6), A101 closure (84 walls, 997.24 LF).
Method: A and B bands projected to A101 with the closure registration (scratch/CIERRE/T.py).
Crosswalk C-n <-> A <-> B <-> canon: `crosswalk.json`. Items: `resolucion_items.json`.
Canon: `../4_canon/takeoff_canon.json` (reading A + general.json + fixes). Validator: **CANON OK**.
Rule applied everywhere: printed dimension wins; ONE WALL ONCE (tag on two enlarged sheets -> lower sheet);
an opening is inside the run when the wall continues above it (door, storefront, cased opening with wall over it);
a gap cuts only when nothing continues above (R-27). Never averaged.

## Totals per type (LF)

| Type | Canon | Closure | A | B | Main reasons canon vs closure |
|---|---|---|---|---|---|
| A2-3D | 98.05 | 98.06 | 98.05 | 97.95 | - |
| A3C | 206.17 | 191.41 | 220.46 | 245.50 | +15.58 closure-UNTYPED typed A3C (C-58..61, C-75, C-76); -0.55 T at C-34 |
| A6C | 23.83 | 23.97 | 23.83 | 23.75 | - |
| A6D | 391.08 | 379.46 | 432.80 | 421.76 | +11.77 closure-UNTYPED typed A6D (C-53, C-69, C-78); C-2 60.88 vs 61.16 |
| B2E | 103.96 | 104.45 | 99.32 | 104.00 | - |
| C3C | 24.54 | 20.72 | 41.86 | 21.30 | board-face basis (PT7) vs closure centerline |
| C3D | 44.86 | 40.29 | 40.56 | 42.63 | +5.32 vanity caps C-71..74 (closure UNTYPED, tag C3D) |
| D3G | 60.01 | 59.91 | 31.76 | 31.76 | gap filled (bank 2) |
| D6F | 22.41 | 14.41 | 22.41 | 14.47 | +8.00 opening inside the run (R-11) |
| D6G | 26.44 | 26.53 | 26.47 | 26.45 | - |
| X6D | 5.37 | 5.36 | 5.37 | 5.37 | - |
| UNTYPED | 0 | 32.67 | - | - | all typed (A / B readings, RFI-20/22/24) |
| **Total** | **1006.72** | **997.24** | 1046.05 | 1034.94 | |

A6D excess explained: A +53.34 = double counts C-14/C-15/C-16/C-37/C-48 (+49.91) + closure-untyped walls
typed A6D (C-53, C-69: +8.63) + C-2 short (-5.38) + rounding; B +42.30 = doubles (+49.97) + C-53 / C-78 (+6.56)
- C-2 short (-8.28) - C-29 short (-6.35) + rounding. Canon removes the doubles and runs C-2 / C-29 fully.

## Items (item -> decision -> N/SHEET -> image -> LF delta vs A)

- R-01 C-14 A6D double (A421 + A429, A and B) -> A421 owns, A-A429-8 removed -> A421/A429 -> img_res/R-01.png -> -26.43
- R-02 C-15/C-16 A6D stubs double -> A421 owns, A-A429-9/-10 removed -> img_res/R-02.png -> -5.90
- R-03 C-34 A3C: B counted 33.21 twice -> A kept (printed 33'-2 1/2" = A) -> img_res/R-03.png -> 0 (B -41.34)
- R-04 C-37 A6D double (A435 + A426) -> A426 owns, printed 12'-5 1/2" (A435) -> img_res/R-04.png -> -12.53
- R-05 C-48 A6D infill double (A423 + A424) -> A423 owns -> img_res/R-05.png -> -5.12
- R-06 C-17/C-18 C3C double (A421 + A427, A only) -> A421 owns -> img_res/R-06.png -> -9.10
- R-07 C3C basis -> faces with board (PT7); A421 U 4.77 each (N face = A6D) -> img_res/R-07.png -> -8.22
- R-08 C-2 A6D extent -> printed chain 60'-10 1/2" through storefronts F/H to C-15 -> img_res/R-08.png -> +5.10
- R-09 C-34 Studio Entry 6'-6" opening -> wall above (3/A426.A) -> A 21.00 kept -> img_res/R-09.png -> 0
- R-10 C-29 A6D through door 122 -> A 56.44 kept (= closure) -> img_res/R-10.png -> 0 (B +6.36)
- R-11 C-8/C-9 D6F 8'-0" opening -> wall continues above (5/A429.A), printed 16'-11" -> A kept -> img_res/R-11.png -> 0 (B +8.00)
- R-12 C-82..84 D3G bank 2 GAP -> added on A432, 28.25 LF, T.O. 60" -> img_res/R-12.png -> +28.25
- R-13 C-64 B2E only B -> ported 4.64 with A fields -> img_res/R-13.png -> +4.64
- R-14 C-56/57 A3C A-A424-5 13.16 -> 6.72 (gray fills; B) -> img_res/R-14.png -> -6.44
- R-15 C-60/61 east lav wing only B -> added 2.65 -> img_res/R-15.png -> +2.65
- R-16 C-76 Women's Janitor east wall double -> A423 owns -> img_res/R-16.png -> -5.13
- R-17 C-71..74 vanity caps double + type -> tag C3D PT0130 wins, 2 x 2.68 -> img_res/R-17.png -> -1.34 (A3C -5.36, C3D +4.02)
- R-18 C-69 door 141 wall only A -> kept A6D, RFI-20 -> img_res/R-18.png -> 0
- R-19 C-78 A2.25 infill type -> A6D, RFI-24 -> img_res/R-19.png -> 0
- R-20 D6G + return -> split 19.87 + 6.57 -> img_res/R-20.png -> -0.03
- R-21 C-24 PT0080 line -> A421 15.85 -> img_res/R-21.png -> 0
- R-22 C-33 C3D 4" gap in run -> 17.21 -> img_res/R-22.png -> +0.33
- R-23 C-53..55 shower stall walls -> A kept, split 3.40 + 1.24 -> img_res/R-23.png -> 0
- R-24 C-51/52 C3D furring -> printed 3'-8 1/2" + 1.59 -> img_res/R-24.png -> -0.05
- R-25 deck -> printed only on 6/A429.B; A425 walls CONFIRMED -> PENDING (hidden text) -> img_res/R-25.png, R-25b.png -> 0 LF (height)
- R-26 MR board -> canon gate: MR behind fixtures only (13 faces), rest type X, RFI-32 -> img_res/R-26.png -> 0 LF (~3,990 SF type X)
- R-27 C-19/20 check-in 3'-0" gap -> split kept (nothing above) -> img_res/R-27.png -> 0
- R-28 head C criterion -> ceiling + 6", deck where face open (A rule kept), RFI-21 -> 0
- R-29 headers -> steel header "REF STRUCT" = by others (A602 6/8/1); A426 opening not called, RFI-12/29 -> 0 LF wall
- R-30 B2E 2" stud -> 2-1/2" loaded, RFI-32 -> 0
- R-31 board name -> 5/8" type X everywhere (spec 09 29 00), RFI-05 -> 0

Sum of LF deltas vs reading A: -39.32 LF (1046.05 -> 1006.72).

## Readers' doubts (dudas_lectores.md) -> decision

| Doubt | Decision |
|---|---|
| B-Z6 1 / A-Z1 7 / B-Z5 header / B-Z1 6: D3G bank 2 | R-12 added on A432 |
| B-Z6 2 PT0012/PT0044 A3C/A6C overlap | A6C (A421 reads A6C, drawn 6") - A-A421-13 kept |
| B-Z6 3 / B-Z4 7 / A-Z4: B2E Group X north existing? | loaded new B2E 34.29 (A101 tag + gray fill + AD101 note 5), RFI-23 |
| B-Z1 1 D3G 3 walls vs 1 | 3 rows kept (ΔLF 0); partition_types joins returns |
| B-Z1 2 storefront-line band 21.17 | not a separate wall: it is C-2 (A427 owner), R-08 |
| B-Z1 3 A435 stub 5.76" | excluded; printed 33'-2 1/2" = A 33.21 (R-03) |
| B-Z1 4 / A-Z2 4 PT0080 15.90 vs 8.94 | A421 owns full 15.85 (R-21) |
| B-Z1 5 / B-Z4 6 / B-Z2 6 C3C basis | R-07 faces with board |
| B-Z1 7 PT0069/0070 3'-1 1/2" open passage | split kept (R-27) |
| B-Z3 1 / A-Z3 D7 untagged 3-5/8" type | A3C (R-15), RFI-22 |
| B-Z3 2 shower west wall 10.71 vs 10.83 | 10.71 kept (A = B vector); B's 10.83 is a printed chain minus an existing piece (derived, not a direct printed wall dimension); Δ 0.12 < 2 % |
| B-Z3 3 short returns face | inner face, corner owned by the tagged leg (return_basis declared) |
| B-Z3 4 A425-2 infill 1.60 | inside A-A425-2 (ΔLF 0) |
| B-Z3 5 X6D + A3C two bands | two walls (two bands, closure C-62/C-63) |
| B-Z3 6 A424-4 5.12 vs 5'-2" | wall owned by A423 (A-A423-5 5.17 = printed 5'-2") - R-05 |
| B-Z4 double count A426/A435 | R-03 |
| B-Z4 2 / A-Z4 3 / B-Z2 2 / A-Z2 2 Studio Entry east 6.35 | inside A-A422-1 56.44 (R-10) |
| B-Z4 3 B-A427-2 extent | R-08 printed chain 60.88 |
| B-Z4 4 B-A427-3 36.57 vs 36.36 | 36.57 (A = B), to existing face |
| B-Z4 5 B-A431-2 17.21 vs 16.88 | 17.21 (R-22) |
| B-Z5 1 / A-Z5 6 curved Lift Lab wall | not loaded, RFI-25 |
| B-Z5 2 / A-Z5 5 A2.25 infill | A6D 3.16 @ 7'-0", RFI-24 (R-19) |
| B-Z5 3 / A-Z5 4 D6F opening | R-11 one wall 16.92, head 7'-0" ALIGN (RFI-29) |
| B-Z5 4 D6G return type | D6G (touches D6G, R-20) |
| B-Z5 5 Sauna north 15.05 vs 15.00 | 15.05 printed chain (A = B) |
| B-Z5 6 head of door 113 | inside C-2 run: storefront H (R-08) |
| B-Z5 7 / A-Z6 door 141 wall | R-18 |
| A-Z4 1 / A-Z3 D1 / A-Z5 1 / A-Z1 4 / A-Z2 1 deck | R-25, RFI-01 |
| A-Z4 2 / A-Z3 D2 / A-Z1 3,5 / A-Z2 5 head C | R-28, RFI-21 |
| A-Z4 4 / B-Z2 3,4 C3D A422/A431 | A422 6.93 + A431 10.06 (no double, closure C-32 17.64) |
| A-Z4 6 / RFI-02 B2E head E vs H | E loaded (board ceiling + 6"), RFI-02 |
| A-Z4 7 / A-Z3 D11 gauge / O.C. | 16" O.C., gauge PENDING, RFI-04 / RFI-18 |
| B-Z2 doubles A423/A424 infill, janitor east | R-05, R-16 |
| B-Z2 5 / A-Z2 9 A423-8 C3D L | R-17 |
| B-Z2 7 A422-3 type A6C | A6C (A101 tag PT0045) |
| B-Z2 8 A423-9 B2E owner | A423 (R-13) |
| A-Z3 D3 X6D faces | both faces 2 layers type X (detail), RFI-07 / RFI-30 |
| A-Z3 D4 janitors / laundry MR | R-26, RFI-30 / RFI-32 |
| A-Z3 D5 A425-3 22'-10" vs 21'-10" | 22'-10" PENDING (R-25) |
| A-Z3 D6 / D13 A425 face heights | kept as read (8'-0" / 10'-1"), RFI-21 |
| A-Z3 D8/D9 parts / corners | ΔLF ≤ 0.29, kept |
| A-Z3 D10 A103 tag 19 not in schedule | blocking_pending_info, RFI-13 |
| A-Z3 D12 / A-Z5 opening heads, R.O. | RFI-29 |
| A-Z5 2 / RFI-03 D6F/D6G 6" vs 3-5/8" | 6" loaded, RFI-03 |
| A-Z5 3 sauna board | DensArmor Plus full height (5/8 type X WR), RFI-30 |
| A-Z5 7 existing walls re-furring | not loaded, RFI-26 |
| A-Z6 1-3 | R-18, RFI-01, RFI-04 |
| A-Z6 4 tags only on A101 | PT0105/0109/0045 counted once (A427-6, A423-10, A422-3); PT0137/0138 -> R-12 |
| A-Z2 7 cinema headwall 15/A502 | in general.json (soffit_side A-A422.A-1) |
| A-Z2 8 header door 134 | existing opening, opening_schedule.none, RFI-29 |
| A-Z2 6 A423-3 N face board | no board (furring C), faces_none_info |
| A-Z2 10 pier A423-9 board 11'-6" | kept PENDING (AP-1) |
| A-Z1 2 Family RR ceiling 12'-1" vs 9'-0" | 12'-1" (RCP), RFI-27 |
| A-Z1 6 A421-10 no poche, tag A6D | A6D (tag) |
| A-Z1 8 A103 key 8 track 5'-5" on 5'-0" wall | RFI-28 |
| A-Z1 9 tile backer product | RFI-06 |
| A-Z1 existing D0.07 finish removal | RFI-26 |
| A-GEN RFIs 01-19 | merged in rfis_etapa3.json |

## Canon changes made only to satisfy canon.py gates (no LF change)

- returns split into their own rows with `part_of` + `return_basis` (band = one straight segment).
- `nodes[]` generated from canon bands (L / T / free), same sheet only.
- `opening_schedule` (A601 28 marks + glazing frames + cased openings), headers per R-29.
- `wet_fixtures[]` (13) and MR -> type X elsewhere (R-26); board names normalized.
- wood blocking moved to `blocking_excluded_info` (standing order); metal backing without lengths to
  `blocking_pending_info` (RFI-13) - canon `blocking_items` is empty.
- unboarded furring faces moved to `faces_none_info` ("a lining has no face on the side it lines").
- `frp_none_reason`, `system_callout.on_plan` (C-5 tag printed on each ceiling), `detail` = TYPE key.

RFIs: 32 (rfis_etapa3.json: RFI-01..19 from A-GEN, RFI-01 updated; RFI-20..32 new).
