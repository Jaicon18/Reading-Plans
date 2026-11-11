# NOTAS - independent schedule reader (Xfinity Interquest, 1333 Interquest Pkwy)

Coordinates are visible-frame pt. Note on tooling: with PyMuPDF 1.28.x, `page.get_pixmap(clip=...)` takes the **visible** rect directly. Passing `rect * derotation_matrix`, as BRIEF_COMUN says, rendered the wrong area. I checked every crop by re-opening it.

## Conflicts / ambiguities
1. **Stud gauge and spacing are not printed in any wall type.** W2, W2A and W3 all say "REFER TO INTERIOR WALL LIMITING HEIGHTS THIS SHEET FOR STUD SPECS". Details 3 and 4/A2.0 say "SEE STUD TABLE FOR SPACING / SIZE & SPACING". The only gauge in the set is in the 4/A2.0 brace note: "MATCH WALL STUD SIZE & GAUGE (3 5/8" 20 GA. MIN.)". This implies W2 studs are 20 GA minimum (20 GA = 33 mil, so 362S125-33).
   - With W2 at 12'-6" (retail ACT 12'-0" + 6"), these rows from the table work:
     - Lightest row at 16" o.c.: 362S125-27 (limit 15'-0").
     - 362S125-18 at 16" o.c. fails (limit 12'-2").
     - 362S125-33 at 16" o.c. gives 16'-0".
   - Spacing is PENDING (open question), unless the take-off applies a standing rule.
2. **8/A2.0 backing detail** calls "16 GA. METAL STUD 16" O.C. @ ALL BACKING STUD TRACKS". So at backing locations the studs are 16 GA at 16" o.c., which differs from the field studs.
3. **W2A and W3 are defined in 2/A2.0 but no tag appears on the A2.0 plan.** The plan only has W1, W2 and W4 tags; I extracted all words on p5. On the plan, W2 is the only new partition type.
4. **The limiting-heights table is valid only for walls "FULLY SHEATHED WITH GYPSUM BOARD OR PLYWOOD ON BOTH SIDES OF WALL".** W2A (board on one side) falls outside that condition unless the "OPTION: CONTINUOUS BRIDGING/ BLOCKING AT 60" O.C." is used.
5. **New "GYP. BD. 8'-6" AFF" ceiling tag on A3.0.** It is not labelled EXISTING and its leader ends at the narrow strip between Storage 101 and Hallway 102.
   - Vector size, measured at 1/4"=1'-0" (18 pt/ft): (923.7-846.9)/18 = 4.27 ft by (1625.3-1618.3)/18 = 0.39 ft. This is DERIVED; I did not check the scale here, and the take-off must verify it.
   - It reads like a header/soffit over the storage-to-hallway opening.
   - The A4.0 Room Finish Schedule has no 8'-6" entry. Room 102 shows GYP. BD. at 9'-0", and A3.0 tags hallway 102 and toilet 103 as "EXISTING GYP. BD. 9'-0" AFF".
   - It is our trade (gypsum board ceiling/soffit plus its framing). Its extent should be confirmed (possible RFI).
6. **Wall height for W2.** The type says "FROM SLAB TO 6" ABOVE CEILING U.N.O.", and the legend says "FULL HEIGHT PARTITION TO 6" ABOVE CEILING U.N.O.".
   - The two sides of W2 have different ceilings: retail 12'-0" ACT, storage 10'-0" ACT, hallway 9'-0" existing gyp. bd.
   - Under the brief's rule the higher side governs, giving 12'-6". The board on the storage and hallway faces could be argued to stop at 10'-6" / 9'-6". The type text gives one height ("BOTH SIDES ... TO 6" ABOVE CEILING"), so per face it is ambiguous.
   - 4/A2.0 also requires a brace to structure at 8'-0" o.c. max (max length 25'-0"). The height of the structure is not printed; A0.1 only says "1 STORY - 26 FT". Brace length is PENDING.
7. **The details are drawn for 3-5/8" only** ("3-5/8" METAL TRACK", "3-5/8" METAL STUD NESTED IN METAL TRACK"). There is no detail for 6" W3, which is not used anyway.
8. **No slip or deflection track is printed anywhere.** 4/A2.0 top track is "TOP OF TRACK SECURED TO STUDS WITH #8 SHEET METAL SCREW EACH FLANGE" plus the brace to structure.
9. **Key notes call for both wood and metal blocking.** A4.0 KN13 "PROVIDE F.R. BLOCKING..." (wood, Div 06) and 7/A2.0 "F.R.T. WOOD BLOCKING AS REQ'D" sit alongside A2.0 KN2/KN6 and 8/A2.0, which call metal backing. The A5.0 legend has "6" SHEET METAL BLOCKING STRAPPING" for EV-44/EV-45 (6 + 1 fixtures, 7'-3" each) and 3/4" plywood for EV-10-6 (not ours).
10. **A4.0 KN7 says "3/4" FRP PLYWOOD"; A2.0 KN10 says "3/4" FRT PLYWOOD".** This is a typo. It is not our trade.
11. **The A0.3 spec cites "GYPSUM BOARD: ASTM A36".** A36 is a structural steel standard; it should be ASTM C1396. Joint tape and compound both cite "ASTM C 475". Note this; it does not change the scope.
12. **The A0.3 painting section lists "ALL PURPOSE TEXTURE FINISH"**, while A2.0 general note 3 requires Level 4 smooth ("TAPED, SANDED SMOOTH TO A 'LEVEL 4' FINISH"). The plans govern, so Level 4 applies; texture is not called anywhere else.
13. **Door 101 is the only new door** (in W2, frame type 1, HM). The DOOR & FRAME ELEVATIONS note says "MAY NEED TO ALTER THIS TO BE ONE DOOR". All other doors are existing.
14. **Existing walls W1 and W4** carry "PATCH AND REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)". No new board is called, so they are not counted. 6/A2.0 adds a METAL CORNER BEAD where a new wall meets existing gyp. bd. at the demising wall.
15. **Column furring (5/A2.0, KN1)** is "5/8" TYPE 'X' GYP. BD. ONE SIDE OVER 2 1/2" METAL STUDS (TYP. ALL SIDES)", with corner 'L' bead, to 6" above ceiling. It is keyed "5/A2.0 SIM." at the storefront columns. Gauge and spacing are not printed.
16. **Typos in the printed tables:** "16''-2"" (400S125-27 @16) and "17-0"" (250S162-43 mid-span 12").
17. **Landlord Room is N.I.C.** (A2.0 / A3.0 plan label "LANDLORD ROOM (N.I.C.)") and is excluded. A0.1 general note 4 says N.I.C. work is by others.

## Spec paragraphs (A0.3 SPECIFICATIONS, quoted; A0.3 has no CSI section numbers, so headings are given)
- **ARCHITECTURAL / METALS: LIGHTGAGE FRAMING:** "METAL STUDS SHALL BE USED IN WALLS AS SHOWN ON DRAWINGS (WALL FRAMING PLAN). STRUCTURAL PROPERTIES SHALL CONFORM TO AISI SPECIFICATIONS FOR THE DESIGN OF LIGHTGAGE COLD FORMED STRUCTURAL MEMBERS." (img/a03_metals.png)
- **FINISHES: GYPSUM DRYWALL:** "PRODUCT DELIVERY, STORAGE AND HANDLING: STORE MATERIALS IN PROTECTED, DRY AREA UNTIL USED. PRODUCTS-MATERIALS: A. GYPSUM BOARD: ASTM A36, TYPE X 5/8 FIRECODE, GOLD BOND, U.S.G. OR AN APPROVED EQUAL WHERE SHOWN ON DRAWINGS. B. TRIM: PROVIDE MFG'S STANDARD METAL TRIM ACCESSORIES OF BEADED TYPE WITH FACE FLANGES FOR CONCEALMENT IN JOINT COMPOUND EXCEPT WHERE SEMI-FINISHING OR EXPOSED TYPE IS INDICATED. C. JOINT TAPE: ASTM C 475 PERFORATED. D. JOINT COMPOUND: ASTM C 475 OF THE TYPE INDICATED." (img/a03_gypsum_drywall.png)
- **PAINTING / PRODUCTS-MATERIALS B. GYPSUM BOARD TREATMENT:** "U.S.G. GYPSUM CO. "PERF-A-TAPE", "READY MIXED ALL-PURPOSE JOINT COMPOUND" AND "ALL PURPOSE TEXTURE FINISH" OR EQUAL." (img/a03_gb_treatment.png)
- **THERMAL AND MOISTURE PROTECTION / BUILDING INSULATION:** "SOUND BATT INSULATION MATERIALS: PROVIDE OWENS/CORNING 3 1/2" BATT ACOUSTICAL INSULATION AS SHOWN ON DRAWINGS. (WHEN SPECIFIED)". This is not our trade.
- **ACOUSTICAL CEILINGS:** "SPACE 12 GA. HANGER WIRES NOT OVER 4'-0" O.C.; ... ATTACH WALL ANGLE MAX. 24" O.C." This is not our trade (ACT).
- **HOLLOW METAL FRAMES:** "FABRICATE FROM 16 GA COLD-ROLLED STEEL ... FURNISH WITH 3 ANCHORS PER JAMB". This is not ours, but it affects the jamb studs.
- **Not found in A0.3:**
  - level of finish (it is only in A2.0 GN3: Level 4)
  - control joints (only "CJ CONTROL JOINT" in the A0.1 abbreviations; none located on the drawings)
  - corner bead (only the generic "METAL TRIM ACCESSORIES OF BEADED TYPE"; METAL CORNER BEAD is in 6/A2.0, CORNER 'L' BEAD in 5/A2.0)
  - moisture-resistant board (it is only in A2.0 KN4: "USE WATER RESISTANT GYPSUM BOARD/FIBER BOARD AT ALL AREAS SUBJECT TO MOISTURE OR WHERE TILE IS USED. PROVIDE WATERPROOF MEMBRANE AT ALL AREAS WHEN THEY ARE ABOVE OTHER SPACES.")

## Other trade notes (plans)
- **A2.0 GN3:** Level 4, all gyp. bd. walls and ceilings (U.N.O.).
- **A3.0 GN4:** "NO ACCESS HATCHES SHALL BE INSTALLED IN GYPSUM BOARD CEILINGS WITHOUT PRIOR APPROVAL BY OWNER."
- **A0.1 interior/exterior note 7:** "CONTRACTOR, ALONG WITH MECHANICAL CONTRACTOR, SHALL PROVIDE AND LOCATE ACCESS DOORS/ PANELS IN WALL & CEILING CONSTRUCTION AS REQUIRED".
- **A0.1 note 3:** "WHERE OCCURS, CONTRACTOR SHALL PATCH ANY EXISTING WALLS AND/OR CEILINGS AS NEEDED TO REFURBISH THE LEASE SPACE".
- **A1.0 keynote:** "EXISTING STOREFRONT BULKHEAD ABOVE. PATCH AND MATCH AS REQUIRED. (V.I.F.)". This is patch only, with no quantity.
- **3/A2.0:** "BOTTOM TRACK WITH POWER-DRIVEN FASTENERS AT 16" O.C. MAX. ICC-ESR-1752". The fasteners are excluded per our rules; the track is ours.
