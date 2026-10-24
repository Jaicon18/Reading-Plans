# AUDIT_COMPLETENESS — Barnes & Noble, Colorado Springs (bid set 250918)

Adversarial completeness check of the metal framing (Div 05) and gypsum board (Div 09) take-off against `bidset_SIN_MARKUPS.pdf` (69 pp).
Baseline compared: `4_canon/takeoff_canon.json` and `4_canon/out/*.json` (familias_out, board_out, studs_out, accesorios_out).
Evidence crops (red circle = cited text) are in `5_auditoria/img/`. Status: CONFIRMED = printed; DERIVED = operation shown; PENDING = not measurable from the set.

Two facts about the baseline drive several findings:
- `familias_out.json` has **0.0** for `1/2" EXTERIOR gyp sheathing`, `5/8" gyp MOISTURE RESISTANT`, `FRT blocking`, `expansion anchors` and `access panel`. Every board face is `5/8 regular`.
- `trim_items` holds 3 corner-bead items only: type 3 tops, type 4 tops, and the W2-06 recess.

---

## 1. CONFIRMED FINDINGS (missing or wrong scope)

### F-01 1/2" exterior gypsum sheathing on type 1B was never quantified (wrong vs. stated coverage)
- **Source:** 1B/A-410, "1/2" EXTERIOR GYP SHEATHING" (with weather barrier, 1" air gap and 4" stone veneer). A-001A Div 09 A.3: "EXTERIOR APPLICATIONS: PROVIDE A GLASS MAT GYPSUM SUBSTRATE FOR USE AS SHEATHING."
- **Problem:** The take-off says 1B carries sheathing, but `familias_out` has "1/2" EXTERIOR gyp sheathing": 0.0 and "5/8" glass mat sheathing": 0.0.
- **Quantity (DERIVED):** 1B walls EXT-04, 05, 06, 09, 10, 11, 12, 17, 18 = 99.7 LF, and Σ length x height = **2,469 SF gross**, one face. Deduct the door 12 opening (10'-0" wide, head not printed). Product type is also an RFI: the detail says 1/2" exterior gyp, the spec says glass mat.
- **Ownership:** ours, if the 1B framing stays in our scope. See A-01.
- **Evidence:** `img/F_1B_ext_sheathing_A410.png`

### F-02 Water-resistant board in wet rooms is loaded as regular board
- **Source:**
  - A-410 note under the details: "* PROVIDE 5/8" WATER RESISTANT GYP. BD AT JANITOR'S CLOSET, DRINKING FOUNTAIN, KITCHEN AND ALL TOILET LOCATIONS."
  - A-410 partition note 7: "G.C. TO INSTALL GREENBOARD (OR EQUAL MOLD-RESISTANT GYP. BD) ON ALL TOILET ROOM, JANITORS CLOSET, OR SIMILAR TYPE OF WETROOM AREAS."
  - 2/A-410 and 5/A-410: "RESTROOM/CAFE WALLS ONLY: PROVIDE W.R. GYPSUM BOARD ON WET SIDE(S) ONLY TO B.O. GYP CEILING."
  - A-101 general note 8: wet areas and walls behind plumbing fixtures to be "MOISTURE RESISTANT DRYWALL OR CEMENT BOAR[D]".
  - A-201 21/26: "W.R. GYPSUM BOARD PARTITION".
- **Problem:** Every Men's 108, Women's 109 and Janitor 107 face is `5/8 regular`, and `5/8" gyp MOISTURE RESISTANT` = 0. The canon parks this as RFI-11, but the requirement is printed in three places, so it is not an open question.
- **Quantity (DERIVED from canon faces):** move **1,326 SF** from regular to W.R.: Men's 284.4 + Women's 248.8 + Janitor 793.0. Add the drinking-fountain alcove faces (W2-06.2/.3/.4, corridor side, 9.5 ft) and the break-room kitchenette wall behind the sink (6/A-412); both are PENDING small areas. Note 8 also covers the restroom walls behind the fixtures on EXT-07, but those faces are currently excluded (see A-01).
- **Ownership:** ours.
- **Evidence:** `img/F_WR_board_note_A410.png`, `img/F_WR_note7_A410.png`, `img/F_gen_note8_moisture_A101.png`

### F-03 Board type: the specification default is 5/8" Type X, not regular
- **Source:**
  - A-001A Div 09 A.2: "GYPSUM DRYWALL: U.S. GYPSUM 5/8" THICK FIRE CODE SHEETROCK (TYPE "X") PANELS OF STANDARD QUALITY OR EQUAL OR AS OTHERWISE SPECIFIED IN THE DRAWINGS."
  - 4/A-121: "5/8" USG ECOSMART FIRECODE X (UL TYPE ULIX) PANELS".
  - 5/A-121: "5/8" TYPE 'X' G.W.B."
- **Problem:** No sheet "specifies otherwise" (A-410 details just say "5/8" GYPSUM BOARD"), but the canon prices everything as `5/8 regular`.
- **Quantity (DERIVED):** **16,563 SF** (15,581 SF walls + 981 SF ceilings, from `board_out` and `ceilings`) changes from regular to Type X. W.R. areas need Type X W.R. (F-02).
- **Ownership:** ours.
- **Evidence:** `img/F_typeX_spec_A001A.png`

### F-04 Moment clips and anchors at the base of partial-height walls (types 3 and 4) are missing
- **Source:** 3/A-410 and 4/A-410: "3 5/8" X 20GA TRACK W/ (2)-1/4"Ø X 1 5/8" HILTI KWIK HUSEZ CONCRETE SCREW AND MOMENT CLIP – SEE DETAIL" (A/A-410, ClarkDietrich "MC" series clip with 1/4" stiffening plate, "(1) #10-16 screw @ each flange").
- **Problem:** `familias_out` has no moment-clip family, and `expansion anchors` = 0. Types 3 and 4 are freestanding at 8'-0" and 7'-6" AFF, so the base clip is what holds them up.
- **Quantity (DERIVED):** studs from `studs_out`: type 3 = 40, type 4 = 122. That gives **162 moment clips** (one per stud, as drawn in A/A-410) and **324 Kwik HUS-EZ 1/4" x 1-5/8"** (2 per clip). The clip spacing is not printed separately: RFI to confirm "every stud".
- **Ownership:** ours.
- **Evidence:** `img/F_moment_clip_anchor_3-A410.png`

### F-05 Corner bead at the 9 column surrounds (C25) is missing
- **Source:** A-101 key note C25: "EX. COLUMN. NEW 24"x24" GWB SURROUND OVER 3 5/8" METAL FRAMING FROM SLAB TO 8'-0" AFF".
- **Problem:** The surrounds are in the take-off (CW-01..09), but `trim_items` has no corner bead for them.
- **Quantity (DERIVED):** 9 columns x 4 outside corners x 8.0 ft = **288 LF**. Add the top edge if the top is open: 9 x 4 x 2.0 ft = 72 LF (PENDING, the top condition is not drawn).
- **Ownership:** ours.
- **Evidence:** `img/F_C25_column_surround_A101.png`

### F-06 Corner bead and J-bead at the Cafe Seating GWB cloud edge are missing
- **Source:** 4/A-121 (USG drywall suspension detail used for the 12'-0" cloud): "J-BEAD" at the top of the fascia and "USG SHEETROCK BRAND DUR-A-BEAD CORNER BEAD" at the bottom edge.
- **Problem:** The cloud is in the take-off (573.69 SF, perimeter 107.21 LF), but no trim was loaded.
- **Quantity (DERIVED):** **107.2 LF corner bead + 107.2 LF J-bead**, plus the fascia board strip (height not printed: PENDING). The same edge condition applies to the free edges of the Cafe 11'-6" / 9'-0" bands and the 11'-0" soffit where they stop at an open edge (perimeters 52.5 / 43.3 / 66.7 LF; free-edge share PENDING).
- **Ownership:** ours.
- **Evidence:** `img/F_cloud_jbead_cornerbead_4-A121.png`

### F-07 Toilet-room backing (grab bars, lavatories, baby changing stations, accessories) and 2 recessed waste receptacles are missing
- **Source:**
  - 21/A-201: "3/4" FIRE RETARDANT PLYWOOD BACKING BOARD (TYP) AT ALL GRAB BARS. SECURE TO STUDS WITH SELF TAPPING SCREWS".
  - 26/A-201: the same backing at lavatories ("LAVATORIES SHALL BE INSTALLED TO SUSTAIN A DEAD WEIGHT OF 250 POUNDS").
  - A-200 elevation 4: "INWALL BLOCKING, STUD TO STUD – SEE DETAIL (26/A201) TYP ALL LAVATORIES".
  - A-001A Div 10 B.2: "INSTALL IN-WALL BLOCKING AS REQUIRED".
  - A-200 schedule: item 5 grab bars 42" x2, 48" x2, 18" x2; item 1 lavatory x2, wall mounted; item 12 baby changing station x2, surface mounted; item 7 mirror x2; item 8C waste receptacle x2, "RECESSED" (Bobrick B-3644).
- **Problem:** `FRT blocking` = 0.
- **Quantity (CONFIRMED counts):** **6 grab-bar backings + 2 lavatory backings + 2 baby-changing backings** = 10 pieces of 3/4" FRT plywood. Area PENDING: about 4 SF each if cut to bar length + 12" x one stud bay. Add light blocking for 2 mirrors, 2 hand dryers, 2 toilet-tissue holders and 2 seat-cover dispensers. Add **2 framed rough openings** for the recessed waste receptacles (header + sill + jack studs).
- **Ownership:** ours. In-wall blocking goes in before the board.
- **Evidence:** `img/F_grabbar_backing_21-A201.png`, `img/F_lav_backing_26-A201.png`, `img/F_accessory_schedule_A200.png`

### F-08 Fire extinguisher cabinets (C11): 6 recessed cabinets need framed openings
- **Source:**
  - A-101 key note C11: "...AT SALES AREA, PROVIDE COSMOPOLITAN SERIES, FULLY RECESSED FULL GLASS DOOR... PROVIDE FIRE RATED CABINETS FOR LOCATIONS IN RATED WALLS".
  - 4/A-101 Fire Extinguisher Detail: "RECESSED FIRE CABINET" and "F.R.T. WOOD STUD HEADER ABOVE AND BASE BELOW CABINET".
  - A-002 schedule: fire extinguishers and cabinets furnished and installed by the tenant contractor.
- **Quantity (CONFIRMED tags on A-101):** **6 cabinets**:
  - Stock Room west wall
  - Corridor at door 11
  - Corridor at door 10
  - Storage 112 at door 14
  - Sales SE near the Cafe Seating
  - Cafe Workroom at door 3

  Each needs a framed opening (FRT header + base + 2 jack studs). The cabinet itself is not ours.
- **Ownership:** framing and blocking are ours. Cabinet installation is ambiguous (Div 10).
- **Evidence:** `img/F_FE_cabinet_detail_4-A101.png`, `img/F_A002_blocking_signage_FE.png`

### F-09 Stock room and storage shelving: FRT blocking "by GC"
- **Source:**
  - 7/A-413: "SHELVING UNITS SUPPLIED AND INSTALLED BY BARNES & NOBLE. GENERAL CONTRACTOR TO SUPPLY BLOCKING IN WALLS" and "FASTEN STEEL SHELVING TO FRT WOOD BLOCKING IN PARTITION".
  - A-101 C14: "1'-6" DEEP X 3'-0" WIDE X 8'-0" HIGH STEEL SHELVING UNITS FASTENED TO PERIMETER WALLS".
  - A-101 C27: 1' deep units, same detail.
- **Quantity (DERIVED, approximate count of A-111 tags):**
  - 18x36 units: 4 on the north wall, about 18 on the west wall, about 16 on the stock face of W2-03.
  - 12x36 units: about 5 on the south / corridor side.
  - Total about 43 units x 3'-0" = about 129 LF of wall, times 3 blocking rows (3'-0" post / bracket levels in 7/A-413) = **about 387 LF of FRT 2x blocking**.
  - Storage 112 (C27) is PENDING (units not drawn on A-111).
- **Ownership:** ours (GC blocking). If 1A/1B are landlord furring (A-01), the blocking still goes into those walls before board.
- **Evidence:** `img/F_shelving_blocking_7-A413.png`, `img/F_stock_shelving_A111.png`

### F-10 Receiving table wall shelving: continuous 2x4 FRT blocking
- **Source:**
  - 8A/A-413: "CONTINUOUS 2x4 F.R.T. WOOD BLOCKING (TYP.)" and "PROVIDE WOOD BLOCKING IN WALL AS REQUIRED".
  - A-101 C16: "RECEIVING TABLE, BLOCKING AND WALL MOUNTED ADJUSTABLE SHELVING".
- **Quantity:** elevation 8/A-413 run **17'-3" (CONFIRMED)** x 4 blocking rows (as drawn in 8A) = **69 LF of 2x4 FRT** (DERIVED).
- **Ownership:** ours.
- **Evidence:** `img/F_receiving_blocking_8A-A413.png`

### F-11 Manager's Office counter and shelving: FRT blocking
- **Source:**
  - 3/A-412 and 4/A-412: "F.R.T. BLOCKING IN WALL BEHIND GWB".
  - 14/A-412: "COUNTER AND SHELF W/ F.R.T. WOOD BLKG. (TYP.)": counter at 2'-7" plus 3 shelves.
  - A-101 C12: "...PROVIDE F.R.T BLOCKING AS NEEDED".
- **Quantity (DERIVED):** elevation widths scaled at 1/4" = 1'-0" are about 12.9 ft (elevation 3) and 8.5 ft (elevation 4), both PENDING verification. Times 4 rows = **about 86 LF of FRT blocking**.
- **Ownership:** ours.
- **Evidence:** `img/F_office_frt_blocking_3-4-A412.png`, `img/F_counter_frt_blkg_14-A412.png`

### F-12 Break room kitchenette upper cabinets: blocking
- **Source:**
  - 6/A-412: "PROVIDE BLOCKING IN PARTITION FOR CABINETS AS REQUIRED".
  - A-101 C20: "PROVIDE F.R.T. BLOCKING AS NEEDED".
  - A-002: break room cabinets and lockers installed by GC.
- **Quantity (DERIVED):** cabinet run 2'-9" + 2'-7" = 5'-4" x 2 rows = **10.7 LF FRT**. Lockers (C15) are PENDING.
- **Ownership:** ours.
- **Evidence:** `img/F_kitchenette_blocking_6-A412.png`

### F-13 Cafe menu boards: FRT plywood blocking in the E1 back wall
- **Source:** 4/A-226A: "DASHED LINE INDICATES FRT TREATED PLYWOOD BLOCKING IN WALL FOR MOUNTING OF MENU BOARDS". The boards are 4 x 24"x31" and 1 x 70"x31", centered at 7'-0".
- **Problem:** The back counter wall is E1 (C-E1-S), which carries only 1/2" cement board in the take-off. No FRT plywood strip was loaded on E1.
- **Quantity (DERIVED):** run 2'-9" + 2'-5" + 4'-4" + 4'-4" + 2'-5" + 2'-9" = 19'-0" (printed dimensions) x about 3'-0" band (31" board + edges) = **about 57 SF of FRT plywood** behind the cement board / tile. Band height is PENDING.
- **Ownership:** ours.
- **Evidence:** `img/F_menuboard_frt_blocking_4-A226A.png`

### F-14 Janitor's closet: 3/4" fire-resistant plywood behind the shelving standards
- **Source:** 11/A-200: "AREA OF 3/4" FIRE RESISTANT PLYWOOD BLOCKING (TYP)", with 7 shelf levels of KV standards @ 24" O.C. A-002: janitor's closet shelving furnished and installed by the tenant contractor.
- **Quantity:** about 4'-0" wall (9/A-200 plan) x about 5'-9" (shelf zone up to the water-heater shelf) = **about 23 SF** (PENDING exact extent). This area is not FRP-backed plywood: it sits under FRP-1, which is excluded separately.
- **Ownership:** ours.
- **Evidence:** `img/F_janitor_plywood_11-A200.png`

### F-15 Server / music rack backboard: one 4'x8' FRT plywood sheet "by GC"
- **Source:** 2/E-103 Server Room Detail: "4'x8' FRT PLYWOOD SHEET AND POWER BY GC – ALL OTHER WORK BY OTHERS". A-101 C21 (Stock Room, music / POS / CCTV racks). The E specification (p44) also says "Provide fire-rated plywood terminal board as shown on drawings".
- **Quantity:** **1 sheet = 32 SF of 3/4" FRT plywood** (CONFIRMED).
- **Ownership:** GC scope. Usually carried by framing / drywall when FRT plywood is in our package. Confirm with the GC.
- **Evidence:** `img/F_music_frt_plywood_2-E103.png`

### F-16 Stud gauge not assigned, and 3-5/8" to 25'-0" exceeds the Metal Stud Schedule
- **Source:**
  - A-410 Metal Stud Schedule, 3-5/8" @16": max unsupported height 17'-11" (20 ST), 18'-6" (20 SJ), 19'-3" (18), 20'-0" (16), 22'-0" (14).
  - Brace schedule: 3-5/8" x 16 ga max unbraced 18'-0".
  - Stud schedule note 3: "WALLS OVER 12'-0" HIGH TO BE BRACED W/ 1 1/2", 16 GA. COLD-ROLLED CHANNELS".
  - 2/A-410: "3 5/8" STUDS @ 16" O.C. TO BOTTOM OF NESTED STUD BRACING. SEE SCHEDULE FOR GAUGE."
- **Problem:** The canon has no gauge on any wall (`gauge` = None). Types 2, 1, 1A, 1C, H2a, H2b and F are 3-5/8" studs carried full height to 25'-0" / 25'-7". That is above the 22'-0" maximum even for 14 ga, and 6" walls at 25'-0" need 16 ga or heavier.
- **Quantity:**
  - 3-5/8" studs = 16,813 LF, all of which need 14 ga plus bracing, or a stop at nested bracing below the deck as 2/A-410 draws.
  - 6" studs = 2,925 LF at 16 ga or heavier (6" x 16 ga max 30'-0").
  - The pricing impact is gauge only; the LF does not change.
- **Ownership:** ours. RFI on the stud termination at "nested stud bracing" vs. full height.
- **Evidence:** `img/F_stud_schedule_A410.png`

---

## 2. AMBIGUOUS (RFI, with the delta of each alternative)

### A-01 Perimeter furring (types 1, 1A, 1B, 1C): who frames it and who boards it? Biggest dollar item.
- **Printed text:**
  - A-002 Responsibility Schedule, Div 05 "STRUCTURAL & LIGHT GAUGE METAL FRAMING": Furnish = Landlord X + Tenant Contractor X; Install = Tenant Contractor X. Remarks: "PERIMETER STUDS, INSULATION, VAPOR BARRIER F/I BY LL" (revision delta 1). "DEMISING WALL STUDS": Existing / Landlord, "CMU EXTERIOR WALL ADJACENT TO ULTA BUILDING".
  - Div 09 "GYPSUM BOARD, DEMISING PARTITIONS": Existing X, F/I Tenant Contractor X, "PATCH/ REPAIR AS REQUIRED".
  - Details 1, 1A, 1B and 1C/A-410: "5/8" GYP BD BY FUTURE TENANT". B&N is the tenant, and we work for B&N's GC.
- **Alternative 1 (current take-off):** we frame, gyp excluded. No change.
- **Alternative 2 (A-002 literal):** studs by the landlord, board by us.
  - Framing: **−8,901 LF studs** (1A 1,692 + 1 4,236 + 1B 2,333 + 1C 640, from `studs_out`), plus their track, bracing and sheathing (F-01).
  - Board: **+10,358 SF of 5/8" board** (Σ length x height of the 17 exterior walls, one face, gross). Deduct doors 10 / 12 / 13. Board is Type X per F-03, and W.R. behind the restroom fixtures on EXT-07.
- **Alternative 3:** we frame and board: board +10,358 SF, framing unchanged.
- **Evidence:** `img/F_A002_perimeter_studs_by_LL.png`, `img/F_A002_demising_gyp_patch.png`, `img/F_1B_ext_sheathing_A410.png`

### A-02 Demising partition patch and repair (C5)
- **Printed text:** A-101 C5: "DEMISING PARTITION TO BE PATCHED AND REPAIRED TO MAINTAIN EXISTING FIRE RATING. PREPARE WALLS FOR NEW FINISH. ADD GWB/FURRING AS REQUIRED." The C5 leaders point to the north (adjacent-tenant) wall, the east storefront piers and the south wall.
- **Delta:** an allowance is needed; the quantity is not measurable.
  - Suggested allowance: 10% of the C5 wall faces. North wall EXT-02 / 1A runs are 159 + 81 LF x 25 ft.
  - If the wall is rated, patching needs Type X, firestop sealant at the head, and a UL-listed assembly.
  - RFI on the rating and the extent.
- **Evidence:** `img/F_C5_demising_A101.png`

### A-03 Corner guards: conflicting extent
- **Printed text:**
  - A-101 C22: "STAINLESS STEEL CORNER GUARDS AT 48" A.F.F. FOR ALL OUTSIDE GYPSUM BOARD CORNERS AT STOCKROOM WALLS."
  - A-001A spec: "INSTALL METAL CORNER GUARDS (2"X2"X72") AT ALL OUTSIDE CORNERS OR AS SPECIFIED IN THE PLANS. SPACKLE AND SAND SMOOTH."
- **Delta:**
  - Alternative 1 (C22): stock room outside corners only, 4 ft each. Count PENDING; the angled loading-zone wall gives about 4 to 6 corners.
  - Alternative 2 (spec): every outside corner in the store at 6 ft, including the 9 column surrounds x 4 = 36 corners.
  - Who installs (drywall vs. Div 10) is also open.
- **Evidence:** `img/F_C22_corner_guards_A101.png`, `img/F_corner_guards_spec_A001A.png`

### A-04 Vestibule GWB ceiling (10'-6")
- **Printed text:** A-121 room tag "VESTIBULE GWB 10'-6" PT-4". Ceiling key note 5: "NEW GWB CEILING AT ENTRY VESTIBULE".
- **Delta:** the take-off excludes only the "vestibule ceiling box framing (4/A-210)" and lists no vestibule ceiling. If the board and suspension are not inside that exclusion, add 8'-5" x 12'-8" (3'-4" + 6'-0" + 3'-4", A-101) = **about 107 SF** of suspended GWB (5/A-121 system), with perimeter about 42 LF.
- **Evidence:** `img/F_vestibule_GWB_ceiling_A121.png`

### A-05 Grab & Go GWB ceiling at 7'-1"
- **Printed text:** A-121 room tag "GRAB & GO GWB 7'-1" PT-7". 3/A-221 Soffit Section – Grab & Go.
- **Delta:** the take-off excludes the "Grab & Go header soffit (3/A-221)" but does not list the room ceiling. If the ceiling is separate, add 3'-5 3/4" x about 5'-2" (A-221) = **about 18 SF** of GWB plus framing.
- **Evidence:** `img/F_grabgo_GWB_ceiling_A121.png`

### A-06 Access panels: GC installs, quantity not shown
- **Printed text:**
  - M-100 general note 30: "...THE GENERAL CONTRACTOR SHALL INSTALL ACCESS PANELS."
  - E general note 12 (p40): same wording.
  - M specs (p50): "EACH CONTRACTOR SHALL BE RESPONSIBLE FOR PROVIDING ALL REQUIRED ACCESS PANELS".
  - A-002: access panels F/I tenant contractor.
- **Problem:** The canon says "none shown".
- **Delta:** install only, per panel, in the GWB ceilings: restrooms 2, cafe bands / soffit, vestibule. Count is PENDING the MEP coordination; suggest an allowance of 4 to 6 panels.
- **Evidence:** `img/F_access_panels_M100_note30.png`

### A-07 Sales perimeter W-3 fixtures: surface-mounted 3/4" FRT plywood blocking
- **Printed text:**
  - 1/A-414, 7/A-414: "SURFACE MOUNTED 3/4" F.R.T. PLYWOOD BLOCKING BY GC/FIXTURE INSTALLER" (2 strips, "CENTERLINE OF BLOCKING").
  - A-414 note: "DETAILS FOR MERCHANDISING ONLY. G.C. TO REFER TO MILLWORK DRAWINGS BY OTHERS".
  - A-002: "SALES PERIMETER WALL SYSTEM... BN MILLWORKER INSTALLS".
- **Delta:** if ours, 2 strips x the W3 run LF. The W3 runs are on A-111 along W2-03, W2-04 and the perimeter (count PENDING, roughly 40+ units x 3'-0").
- **Evidence:** `img/F_A414_surface_FRT_blocking.png`

### A-08 Illuminated "BN CAFE" sign: blocking
- **Printed text:** A-002 "CAFÉ SIGNAGE – ILLUMINATED ... GC TO PROVIDE POWER, BLOCKING, AND STRUT CHANNEL". A-002 "BLOCKING/POWER FOR SIGNAGE": F/I tenant contractor. 1/A-226A "INTERNALLY ILLUMINATED 'BN CAFE' SIGN" (5'-2" wide, on the WD-1 fascia).
- **Delta:** about 6 LF x 2 rows of FRT blocking in the fascia framing, or a strut channel if it hangs (A-121 shows a "B&N CAFE ILLUMINATED SIGN" outline). Other signage blocking is PENDING.
- **Evidence:** `img/F_cafe_illuminated_sign_1-A226A.png`

### A-09 Restroom tile wainscot and tile base backer (reconfirm the existing exclusion)
- **Printed text:** 22/A-201 Tile Base Detail: "5/8" CEMENT BOARD" 1'-2" base with "5/8" W.R. GYP.BD." above.
- **Delta:** already in the tile-backer RFI. It belongs to F-02 for the W.R. board above the base. Cement board is 1.17 ft x the restroom perimeter: Men's + Women's (2 x 32.33 LF) = about 76 SF.
- **Evidence:** `img/F_tilebase_cementbd_22-A201.png`

---

## 3. CHECKED AND OK (nothing new for our trade)

| Sheet | Result |
|---|---|
| A-000 (p1) | Cover / index only. |
| A-001A (p2) | Div 09, Div 05 and Div 10 notes read. They raise F-01, F-03, F-07, A-03. Level 4 finish only, so Level 5 = none is correct. Reveals: A-002 says N/A. |
| A-001 (p3) | Code analysis. No rated partitions called out. |
| A-002 (p4) | Read in full. Drives A-01, A-02, F-08, A-06, A-08. Sound batting is GC scope but already excluded (insulation). |
| A-003 (p5) | Egress plan, no scope. |
| A-101 (p6) | Key notes C1–C28 and general notes 1–8 + sound table read. New items: C5 (A-02), C11 (F-08), C12/C16/C20 (F-10..12), C14/C27 (F-09), C21 (F-15), C22 (A-03), C25 trim (F-05). C4/C6/C8/C9/C18/C19/C23/C24 are millwork / fixtures / EAS, not ours. 2/A-101 slab and 3/A-101 roof penetration: other trades. |
| A-111 (p7) | Fixture plan used only for shelving / W3 counts (F-09, A-07). FE symbols match C11. |
| A-121 (p8) | Ceilings re-checked: A-04, A-05, F-06. Ceiling notes 1–11 and key notes 1–11 have nothing else for us. Note 3 draftstopping above ceilings: no rated ceilings, OK. |
| A-131 (p9) | Floor finish, nothing. |
| A-151 (p10) | Power / signal, nothing. |
| A-200 / A-201 (p11–12) | F-02, F-07, F-14, A-09. The A-200 schedule shows partitions (item 20) qty 0 and urinal qty 0, so no toilet-partition blocking. |
| A-210 (p13) | Vestibule. Box framing is already excluded (A-04 covers the ceiling board). |
| A-220 (p14) | Render, nothing. |
| A-221 (p15) | Already covered in the take-off; re-read only. |
| A-222A/B, A-223 (p16–18) | Plumbing, floor penetrations and stub heights. No framing beyond what the walls carry. |
| A-224 (p19) | Equipment schedule. Wall shelf (item 6), wire shelving (127) and paper towel dispenser are on E2 / H1, which already carry 5/8" FRT plywood, so OK. |
| A-225 (p20) | Finish plan. FRP extent is already an RFI. |
| A-226A (p21) | Raises F-13 and A-08. Elevations 2/3/5/6 add nothing. |
| A-226B, A-227, A-228 (p22–24) | Cafe elevations, details and renders. Nothing new beyond the WD-1 / tile finishes on the FRT plywood already loaded. |
| A-300 (p25) | Front exterior elevation. Existing storefront / stone (Div 08 / landlord). |
| A-400A/B (p26–27) | Deck heights already used. |
| A-410 (p28) | Raises F-02, F-04, F-16. Partition notes 1–8 and fastener schedule read. Bridging @ 4'-0" is already carried as bracing. Deep-leg track 3/A-410 is OK. 6/7 A-410 rated penetrations: no rated walls. |
| A-412 (p29) | Raises F-11, F-12. |
| A-413 (p30) | Raises F-09, F-10. The cashwrap / tube holder are fixtures, not ours. |
| A-414 (p31) | Raises A-07. |
| A-500 (p32) | Doors are already framed. |
| A-510 (p33) | Finish schedule PT / TL / FRP only. No Level 5. |
| DM-101 (p34) | Demolition. No new framing. Demo is by the GC demo sub. |
| E-sheets (p35–45) | Raises F-15 (E-103). Panelboard 3/4" backboards (p42 note 7, p44 "electrical contractor shall furnish... plywood") are by the EC, not ours. Access panels: A-06. |
| M-100..M-303 (p46–52) | Access panels (A-06). Duct stud reinforcement is already an RFI. Fire dampers: no rated walls. |
| P-sheets (p53–60) | Water heater shelf (A-200 11: "SEE DETAILS IN PLUMBING") is by plumbing. Fixture carriers are not called (wall-hung lavatory uses in-wall FRT plywood, F-07). |
