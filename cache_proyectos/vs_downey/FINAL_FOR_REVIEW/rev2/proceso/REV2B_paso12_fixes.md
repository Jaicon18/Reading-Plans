# REV2B: content fixes to takeoff_canon_AB.json (VS #679 Downey)

Each fix was checked on the drawings before the canon was changed. I rendered crops with pymupdf from VS679_bidset_LIMPIO.pdf: A02.01 p13, A10.03 p27, A10.05 p28, A12.01 p31, A12.02 p32, A15.04 p40, S01.01 p43, S02.01 p44 and S03.01 p45.
Validation: `python3 validar_canon.py takeoff_canon_AB.json tools` prints **CANON OK**.
The deltas come from running canon.py before and after the change (familias_out.json).

## Family deltas (canon.py, before -> after)

| Family | Before | After | Delta |
|---|---|---|---|
| bracing C.R. channel | 1,739.06 LF | 982.50 LF | -756.56 |
| clip angle (incl. R/S03.01 bridging clips) | 1,359 EA | 1,519 EA | +160 (bridging clips 1,031 -> 1,191) |
| 3-5/8" stud | 14,854.78 LF | 14,895.08 LF | +40.30 (soffit members, see 4) |
| metal blocking, wall-mounted items | 1,543.30 LF | 1,566.55 LF | +23.25 (now 1,368.55 LF 6" 18 GA backing track + 198.0 LF 6" 18 GA backing plate) |
| ceiling / soffit track (no size) | 171.25 LF | 141.00 LF | -30.25 (now only the 1-5/8" valance track) |
| ceiling / soffit track 3-5/8" | 37.81 LF | 68.06 LF | +30.25 (SS1) |
| 5/8" gyp board Type X | 18,111.16 SF | 17,974.56 SF | -136.60 |
| joint compound / tape | 1,343.95 / 6,906.41 | 1,334.12 / 6,855.87 | -9.83 lb / -50.54 LF (driven by board) |
| deflection-clip RFI (RFI-ACC-deflection-clips) | 55 pcs RFI | none | pending item removed |

## 1. In-wall blocking product (BE-15a / BE-105)
- **Verified:** F/A12.01 BACKING - HEAVY DUTY prints '6" X 18 GA. BACKING TRACK LENGTH AS REQUIRED'. E/A12.01 BACKING - MEDIUM DUTY prints '6" X 18 GA. BACKING PLATE LENGTH AS REQUIRED'. S01.01 B.7 says 'TRACK BLOCKING ... SUCH AS F/A12.01 ... SHALL BE 18 GA (43 MIL) WITH 1 1/4" FLANGES'.
- **Change:** every blocking item now has its product from the detail its label calls, and keeps its LF. The label is prefixed with the product, and the new fields `product` / `product_source` hold the product and its source.
  - F/A12.01, 6" x 18 GA backing track with 1-1/4" flanges: **1,368.55 LF**. This covers:
    - the Garcy runs, the beauty cabinets, the lavatories, the AFR6 bench, the FR alcove, the break-room counter, the MGR desk and the go-back shelving;
    - lockers and communication boards, 39.0 LF. J/A14.02 note 3 says 'E OR F', so I carried the heavy-duty F track, which satisfies either detail;
    - fitting-room signage, 3.67 LF. No detail is called (A00.01, A06.01 keynote 9, P/A10.03), so it is carried as track blocking per S01.01 B.7.
  - E/A12.01, 6" x 18 GA backing plate: **198.0 LF**. This covers grab bars, restroom accessories, FR mirrors, FR hooks, break-room cabinetry, coat rack, shelving, keynote 41 mirror and paging buttons.
- **Delta:** 0 LF in total (product change only). The +23.25 LF in the table comes from fix 6.
- **TOOL PATCH NEEDED:** canon.py still puts every metal blocking item in `metal stud blocking (362CR / STUD BLOCKING)`. plantilla_excel.py then prints that as "Metal stud blocking at wall-mounted items (notes)" and buys it as 20 ft stud sticks, because the regex `stud blocking` maps to `stud_stock_ft`.
  - Patch: split `metal_blocking_by_origin["items"]` by `blocking_items[].product`, one row per product.
  - Row names: "6" x 18 GA backing track, 1-1/4" flanges (F/A12.01)" 1,368.55 LF and "6" x 18 GA backing plate (E/A12.01)" 198.0 LF.
  - Stock: track stock length, not stud sticks.

## 2. Bridging only where a face has no board (BE-15b)
- **Verified:** the R/S03.01 NOTE says 'BRIDGING IS NOT REQUIRED IF SHEATHING IS ATTACHED TO BOTH FACES OF THE STUD (SHEATHING INCLUDES ... GYPSUM BOARD ...). WHERE SHEATHING ONLY EXTENDS PARTIAL HEIGHT PROVIDE BRIDGING WHERE THERE IS NO SHEATHING'. The channel is '1 1/2" x 1/2" 16 GA C.R. CHANNEL - LOCATE AT 4'-0" O.C. MAX VERTICALLY'. S01.01 N note 2 says 'PROVIDE HORIZONTAL BRIDGING PER DETAIL R/S03.01'.
- **Supported field used:** per-wall `bracing_rows` + `bracing_rows_source`. corridas.py reads these per run (canon.py passes them through), and `constants.bracing_spacing_in` stays 48 (A/S03.01).
- **Rule applied to each wall:**
  - The unsheathed zone is the stud height minus the height to which **both** faces carry board. It is 0 on one-sided walls (furring, void, insulated, column wraps, piers).
  - Rows = ROUNDUP(zone / 4'-0") - 1. A zone of 4'-0" or less, between the board top and the top track, needs no row.
- **Result:** 40 walls drop to 0 rows because they have board on both faces with 4'-0" or less above it. These are W014, W020, W021, W028, W033-W037, W040, W042, W043, W045, W046, W048, W049, W067-W070, W073-W076, W082-W084, W089-W091, W094-W096, W101, W106, W107, W112-W115.
  - Each of these walls carries its own source text with the zone arithmetic.
  - Single-faced walls keep the full rows.
- **Clips:** the rows carried in the channel row are now the same rows used for the clips. The 2x2x16 GA channel clip is 'ATTACH AT EVERY STUD'.
  - The previous clip count (1,031) already used this zone rule. It left out the column wraps CW1-CW4 and the piers SP1/SP2, which do carry channel.
  - Recount: 1,191 EA (1,031 + CW 4 x 8 x 2 + SP 2 x 16 x 3).
- **Delta:** channel -756.56 LF (1,739.06 -> 982.50); clips +160 EA (1,031 -> 1,191).
- **Estimator decision:** CW1-CW4 (R/A10.01) and SP1/SP2 (A/S02.01) are one-faced, so the R/S03.01 rule applies. No detail draws bridging there. If they are excluded: -109.62 LF channel (CW 33.74 + SP 75.88) and -160 clips.
- **TOOL PATCH NEEDED (partial length):** `bracing_rows` is a whole number of rows times the full wall length.
  - Five walls have board on both faces along only part of their length: W032, W050, W072, W077, W099. The unsheathed run is a void or face with no board.
  - These carry full rows: 129.17 LF. Bridging only the unsheathed length would be 20.08 LF, which is -109.09 LF (channel 873.41 LF) with clips in proportion.
  - Patch: corridas.py should accept a per-wall `bracing_lf {value, source}`, or `bracing_length_ft {value, source}` per row, in place of rows x L.

## 3. Room 4 ceiling vs soffit zones (BE-VS-04)
- **Verified:** B/A10.03 ends the room ceiling at the valance face ('SEE CEILING PLAN' beyond the valance; the soffit box is closed by its own framing). The valance soffit zone is 70.5 LF x 1'-11 1/4" GYP TO GYP = 136.594 SF, carried as its own ceilings. The cashwrap backwrap soffit (F/A10.05, 30.91 SF) was already deducted from Room 4, and so were the CW closets (18.71).
- **Change:** ROOM 4 BEAUTY 3 `area_sf` goes from 1,131.858 to 995.264 SF, and `area_op` is rewritten with all three deductions.
- **Delta:** -136.60 SF 5/8" Type X board (plus compound and tape by yield).
- **TOOL PATCH NEEDED:** canon.py `usg_grid` computes tees, moldings and hangers from the `ns_ft x ew_ft` rectangle, not from `area_sf`, so the deduction does not reach grid or hangers. The same is true of the closets and the cashwrap soffit, which were already deducted from board only.
  - Pro rata for the valance zone is 11.56 % of the Room 4 grid:
    - main tee -44.70 LF
    - cross tee -73.48 LF
    - hangers -13 pcs x 6.167 = -80.17 LF wire
  - Patch: an optional `deduct_zones [{sf, source}]` on usg_grid ceilings that scales the grid and hangers by area.

## 4. Framed soffit bottoms as drawn (BE-20)
- **Verified:**
  - **B/A10.03:** the soffit bottom at 8'-4" B.O. SOFFIT is '5/8" GYP BD ON 3-5/8" MTL FRAMING AT 16" O.C.'. Members span from the wall to the valance, 1'-11 1/4" GYP TO GYP. A second level of '3 5/8" MTL FRAMING AT 16" O.C.' is drawn at the top of the box at the ceiling line. Both levels are screwed directly to the wall studs and to the 1-5/8" valance studs; no runner track is drawn at their ends. The valance face has a 1-5/8" track top and bottom.
  - **F/A10.05:** the same build at the cashwrap backwrap soffit: a '3 5/8" METAL STUD FRAMING' member at 9'-2" and a second member at the ceiling line. Both are screwed to the wall studs and the drop studs, with no runner track. The 3-5/8" drop studs have a track top and bottom. No O.C. is printed, so I carried 16" O.C., which is the stud spacing they fasten to (M/A02.01 'MTL STUDS @ 16" O.C.').
- **Change:**
  - The single 'BEAUTY CABINET VALANCE' framed_soffit (3 members x 70.5) is split into 6 framed_soffit ceilings, one per A02.01 run: N 18.875, S 18.875, T5 14.125, SW 9.375, NW 4.625, NE 4.625. Each ceiling has `span_ft` = run (members counted along the run) and `run_ft` = 1.9375 (member length), with its own VAL wall `soffit_of`.
  - CASHWRAP BACKWRAP SOFFIT: span 15.139 and run 2.042 (they were swapped before).
  - Two new 3-5/8" stud lines for the top-level members: valance 63 x 1.9375 = 122.06 LF and cashwrap 13 x 2.042 = 26.55 LF.
- **Delta:**
  - Soffit-bottom rows: B/A10.03 211.50 -> 122.06 LF (-89.44); F/A10.05 45.42 -> 26.55 LF (-18.87).
  - Top members: +148.61 LF.
  - Net 3-5/8" stud: +40.30 LF.
  - Track: no runner track at the member ends (none drawn). The soffit-face tracks stay as they were (see 7).

## 5. Top-track splice M/S01.01 (BE-16)
- **Verified:** M/S01.01 'TOP TRACK SPLICE - STRUCTURAL STUDS', 'METAL STUD x 1'-0" (GAGE TO MATCH GAGE OF TRACK)', centered between vertical studs. S01.01 B.1 defines structural studs as the storefront framing of S02.xx. S01.01 B.12 says 'SPLICES IN FRAMING COMPONENTS OTHER THAN BOTTOM WALL TRACK ARE NOT PERMITTED'.
- **Count:** the structural-stud top tracks are W114 4.861 ft, W115 4.778 ft, and the SP1/SP2 pier faces at 4.323 ft and 2.0 ft each (S02.01). Every one is shorter than a 10 ft track, so no splice occurs. The box-beam tracks are beam members that B.12 bars from splicing (continuous lengths, no splice piece). Non-structural partitions are outside M/S01.01.
- **Change:**
  - Removed 'top track splices per M/S01.01' from the 99 non-structural walls.
  - W114, W115, SP1 and SP2 now state why no splice applies.
  - `gap_closure_info` records the decision.
- **Delta:** 0 (BE-16 does not apply: no structural top track exceeds stock length).

## 6. Beauty-cabinet blocking B/A10.03 (BE-18, BE-12 second part)
- **Verified:** on A02.01, Room 4 has the beauty cabinets on 6 runs:
  - N and S 18'-10 1/2" OVERALL (A/A10.03 TYP);
  - NW and NE returns 4'-7 1/2" OVERALL. The NE return is on the TRANS #5 west face, north part;
  - SW 9'-4 1/2" OVERALL on the hallway wall;
  - TRANS #5 west face 14'-1 1/2" OVERALL, which is the A/A10.03 plan's 14'-1 1/2" HOLD.

  B/A10.03 prints '6" CONTINUOUS METAL BLOCKING BEHIND GYP BD, TYP AT THREE LOCATIONS. REFER TO F/A12.01' (C/L 0'-11", 4'-5", 7'-9"). K/A10.03 is VOID.
- **Change:**
  - Beauty item re-cited to B/A10.03 + A/A10.03 (K/A10.03 removed).
  - The two TRANS #5 west-face items carried as 4-row Garcy (56.5 + 18.5) are replaced by 3-row beauty runs (42.375 + 13.875).
  - Added the NW return (13.875) and the SW run (28.125).
- **Delta:** 3 x 70.5 = 211.5 LF required vs 188.25 carried, so **+23.25 LF** of 6" 18 GA backing track.

## 7. Ceiling / soffit perimeter track size (BE-14)
- **Verified:** N/A12.02 (drywall grid ceilings) uses 'ANGLE WALL MOLDING' at the perimeter, with no track; that molding is carried in the USG angle and channel molding rows. The track rows are the soffit faces:
  - B/A10.03: the valance face is '5/8" GYP BD ON 1-5/8" MTL FRAMING AT 16" O.C.', with a 1-5/8" track drawn top and bottom. That is 2 x 70.5 = 141.0 LF.
  - F/A10.05: the drop is '3 5/8" METAL STUD FRAMING', with a 3-5/8" track top and bottom (SS1). That is 2 x 15.125 = 30.25 LF.

  E/A12.02 and A/A12.02 are already carried as 3-5/8" track (9.81 LF).
- **Change:** new `family_splits` moves SS1 (30.25 LF, 20 GA S01.01 TABLE 1) to 'ceiling / soffit track 3-5/8"'. The VAL and SS1 `track_lines_source` now state the printed size. Nothing in the canon says "size not printed, RFI" any more.
- **Delta:** 3-5/8" ceiling/soffit track +30.25 LF; unsized ceiling track 171.25 -> 141.0 LF, all of it 1-5/8" valance track.
- **TOOL PATCH NEEDED:** plantilla_excel.py `NOMBRES_PLANTILLA["track de ceilings / soffits"]` hard-codes "Ceiling perimeter track at GWB ceilings (size not printed, RFI)". canon.py `F_SPLIT` has no 1-5/8" size.
  - Patch: add a family `ceiling / soffit track 1-5/8"`, named "Track 1-5/8" ({gauge}) at valance face, top and bottom", to `F_SPLIT`, NOMBRES_PLANTILLA and familias.py.
  - Then add this to the canon: `family_splits += {"from": "track de ceilings / soffits", "to": "ceiling / soffit track 1-5/8\"", "items": ["VAL-N","VAL-S","VAL-T5","VAL-SW","VAL-NW","VAL-NE"], "gauges": {each: "20 GA"}, "source": "B/A10.03 '5/8\" GYP BD ON 1-5/8\" MTL FRAMING AT 16\" O.C.', S01.01 STUDS AND TRACKS 1 5/8\" 20 GA"}`. That leaves the unsized family at 0.
  - Or simply rename the template row "Track 1-5/8" (20 GA) at beauty valance faces (B/A10.03)".

## 8. Deflection clips (BE-12 / BE-101)
- **Verified:** these sheets print no deflection clip:
  - S01.01 STRUCTURAL NOTES B.1-B.14 (B.8 only sends to L/S03.01 DEEP LEG DEFLECTION TRACK);
  - A15.04 092900 (B.1 'DEFLECTIONS: MAXIMUM L/240' is a stud deflection limit, not a clip);
  - M/A02.01 PARTITION SCHEDULE GENERAL NOTES 1-4;
  - L/S03.01, which draws the 18 GA vertical slotted slip-track with a 3/4" deflection gap and no clip.
- **Change:** `deflection_clips` = {none_reason, source "S01.01, A15.04, M/A02.01, L/S03.01"}. It previously held note_source + slip_track_source, which generated RFI-ACC-deflection-clips.
- **Delta:** the pending item is gone (it was a 55 pcs default, not a printed quantity). The deep-leg track stays at 45.05 LF.

## 9. Closed RFIs and internal wording (BE-47 / BE-55 / BE-102)
- **Closed-RFI citations outside `rfis[]`** are rewritten as "closed: <answer> (N/SHEET)":
  - RFI-01: bod_ft;
  - RFI-02: W001 height;
  - RFI-03: C/A12.01 notes;
  - RFI-04: storefront 1/2" MR faces W114, W115, SP1, SP2: "closed: 1/2" moisture resistant gyp bd under the storefront finish system, furnished and installed by G.C. (A/A08.05, A00.01)";
  - RFI-05: RFID foil-backed faces: "closed: regular foil-back 5/8" per spec (A15.04 092900 H.3)";
  - RFI-06: SS1 and VAL heights: "closed: continuous 3 5/8" 20 GA suspended stud on hanger wire @24" O.C. (S/S03.01)".

  RFI-08 had no citation in the canon outside its own record. Open RFIs (10, 11, 13, 15, 17, 22, 25, 26) are still cited where they apply.
- **Internal wording removed:**
  - "GAPn" prefixes on every misc and blocking ref (refs renamed, e.g. 'P-224 metal reveal at neutral piers + bulkhead', 'Metal FRP top + edge trim');
  - 'misc_items' / 'frp_info' / 'pvc_trim_items' in frp_none_reason;
  - 'blocking_items' in RFI-10;
  - 'misc_items' in opening_schedule;
  - 'reading A/B' and 'R80e.37' in 73 face notes, RFI options and default_type_rfi;
  - every `merged_from_info`;
  - 'U8', 'rule 7' and 'project rule 1' in the sealant and exclusion reasons;
  - 'corridas.py' in 8 top_track_info notes;
  - 'scripts/reg.py' in the MEP registration source;
  - 'SHEET_MAP.md' and file names in lectura_info;
  - '- LECTURA A' in the project name;
  - the orchestrator note in gap_closure_info, which is rewritten in plain English.

  A scan of every string in the canon now finds 0 hits for GAP#, schema keys, reading A/B, rule codes, file names or 'canon'.
- **NOT IN THE CANON, so the run must fix it when it writes the Excel.** The Scope Checklist notes are written by the run, not by the canon. Replacement texts:
  - ALC-05: "...H.M. door R.O. 3'-4": closed: A00.02 3'-0" door + frame ±2" each jamb, head 7'-0 1/2" (A/A10.08)."
  - ALC-08: "...is called for the wet rooms (A13.01, A13.02, A15.04 read)..." (drop 'in readings A and B').
  - ALC-09: "...carried in its own 1/2" moisture resistant gyp bd row; closed: furnished and installed by G.C. under the storefront finish system (A/A08.05, A00.01)."
  - ALC-12: "...ceiling perimeter = angle wall molding (N/A12.02); soffit face track 1-5/8" at valances (B/A10.03) and 3-5/8" at the backwrap drop (F/A10.05)."
  - ALC-13: "...suspended supports: closed: continuous 3 5/8" 20 GA suspended stud on hanger wire @24" O.C. (S/S03.01); storefront head framing open in RFI-17."
  - ALC-19: "EXCLUDED - estimator standing order: no acoustical sealant."
  - ALC-20: "...cement board 6" strip behind the B-13 porcelain cove base in the restrooms (A00.03)."
  - ALC-23 / ALC-24: "...foil-backed gypsum board; closed: regular foil-back 5/8" (A15.04 092900 H.3)."
  - ALC-29: "EXCLUDED - estimator standing order: insulation."
- **TOOL TEXT, so the tool must be patched:**
  - The tool generates the Pending Items row RFI-ACC-additional-head-track (accesorios.py / plantilla_excel.py) with the words "default (no sheet): skill standing criterion / precedent of a previous project". It needs plain wording, e.g. "not printed in this set; estimator's standing practice from a previous project".
  - The Material Summary R50-R61 fastener notes name another project ("same order O'Reilly 2026-10-31"), from plantilla_excel.py.

## Not changed (outside this brief)
- BE-40 (edge-blocking 71.1 LF row, R7/R11 'default (no sheet)').
- BE-46 product splits other than blocking.
- BE-51 (reveal trim pieces).
- BE-102 (truncated N/SHEET values written by the Excel builder).
- BE-44 (markups).
