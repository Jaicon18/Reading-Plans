# Decisiones del estimador — Barnes & Noble Colorado Springs

## 2026-10-24 — RFI-01 Perimeter walls (types 1, 1A, 1B, 1C)
- Perimeter walls = EXISTING (1/DM-101 drawn "to remain", key note 3; A-101 legend "existing exterior wall / existing partition"; A-002 "PERIMETER STUDS ... F/I BY LL").
- Exterior/perimeter framing (studs, track, bracing, 1B sheathing) = EXCLUDED (−8,901 LF studs, −2,469 SF sheathing 1B). Goes to Scope Checklist as Excluded.
- Interior face patch & repair (key note 3 /DM-101, C5 /A-101) = ALLOWANCE (not field-verified), fixed amount LEFT BLANK for the estimator to fill.
- Consequence: RFI-07 (studs >22' types 1/1A/1C) and RFI-02 (1/1A boundary) no longer apply.
- Apply all decisions in ONE Excel update after all questions are answered.
- Q1 CLOSED 100%.

## 2026-10-24 — RFI-23 FRT blocking
- Option A: take off with the counts (rows per detail included): stock room ~387 LF (7/A-413, 3 rows), receiving 69 LF (8A/A-413, 4 rows), office ~86 LF (3,4/A-412, 4 rows), break room cabinets 10.7 LF (6/A-412, 2 rows), restrooms 10 pcs 3/4" FRT plywood (21, 26/A-201).
- Cafe menu boards (4/A-226A): continuous 3/4" FRT plywood strip, 31" high, full length of wall C-E1-S (23.46 LF, A-221) = 60.6 SF (DERIVED: 23.46 x 31/12).
- Q2 CLOSED 100%.

## 2026-10-24 — RFI-11 W.R. board in wet rooms
- Option A: W.R. gyp bd on ALL faces of Women's 109, Men's 108, Janitor 107 (A-410 "*" note, note 7, 2/A-410, A-101 general note 8), new walls only (EXT-07 faces are existing -> patch & repair allowance).
- Quantity to recompute from canon faces at update time: takeoff.json delta says 935.4 SF, audit says ~1,326 SF (Men's 284.4 + Women's 248.8 + Janitor 793.0) -> reconcile from faces, cite both.
- Plan governs over skill rule D1 when the plan explicitly asks W.R. on every face (general, all projects).
- Also W.R. at drinking fountain alcove (W2-06.2/.3/.4, corridor side) and break room kitchenette wall behind the sink (6/A-412): measure faces at update time.
- Q3 CLOSED 100%.

## Excel update instruction
- Every estimator decision + my comments (source N/SHEET, reasoning, derived operation, alternatives/deltas) go INTO the Excel in the existing columns only ("Where it comes from", "Source (DETAIL/SHEET)", Notes/Status, Review Items, Pending Items, Scope Checklist). No new sheets or columns.

## 2026-10-24 — RFI-27 Type X
- Option A: ALL 5/8" gyp bd on new walls = Type X (A-001A). Quantity recomputed after perimeter exclusion.
- W.R. faces (RFI-11) = 5/8" Type X W.R.
- Q4 CLOSED 100%. Q5 (RFI-07) and Q6 (RFI-02) N/A after RFI-01 (perimeter existing). ALL QUESTIONS CLOSED.

## rev1 questions (2026-10-24/25)
- Q4 rev1 (patch & repair allowance amount): BLANK (already decided).
- Q1 rev1: GWB ceilings (981.38 SF, 4/A-121, 5/A-121) -> Type X. CLOSED.
- Q2 rev1: restroom backing (21/A-201, 10 pcs 3/4" FRT plywood) height = 16" (one stud cavity). 13.33 SF @12" -> 17.78 SF (DERIVED: 13.33 x 16/12). CLOSED.
- Q3 rev1: kitchenette W.R. on existing wall EXT-07 (7/A-412) stays INSIDE the patch & repair allowance. CLOSED.
- ALL rev1 QUESTIONS CLOSED. Pending to apply (rev2): ceilings 981.38 SF -> Type X; restroom backing 16" (17.78 SF).

## Review Items (rev2 → rev3), one at a time
- RI 1/11: W2-05 = 12.92 LF (reading A, printed 12'-11" on A-101 [CONFIRMED]); reading B 7.92 rejected. W2-06 stays 25.86 LF. +5.00 LF type 2. CLOSED.
- RI 2/11 part 1: type 4 caps = open U (9'-0" bar + 2 returns + 2 legs into curved walls), 11.86 LF each (reading B, 4/A-410 on A-101). Kept as is.
- RI 2/11 part 2 (RFI-18): curved walls = face-average arc 25.68 LF each (+1.20 LF total vs printed 25'-1"), estimator choice. RI 2 CLOSED.
- RI 3/11 (RFI-17 count): column surrounds C25 = 9 (CW-01..CW-09, A-101). CLOSED. (Stud spacing 16" assumed stays under RFI-17.)
- RI 4/11: Workroom door pier (1/A-221): 1'-0" return = type I 1.00 LF (tag PT0050), pier = E1 2.11 LF (PT0045). Kept. CLOSED.
- RI 5/11 (RFI-19): board height where a ceiling exists = ceiling + 6" (2/A-410). Kept. CLOSED.
- RI 6/11 (RFI-04): 115 diagonal braces = 3-5/8" 20 ga stud, ~4 ft each at 45° top track to structure = 460 LF (DERIVED 115 x 4). Estimator choice; brace member/length not printed (keep note). CLOSED.
- RI 7/11 (RFI-06): Cafe walls H1, H2a, H2b, H3a, H3b, F: STUDS TO DECK 25'-0" (1/A-400B draws Cafe walls floor to B.O. deck; A-226A breaks at top). BOARD per face = ceiling + 6" (A-410 note 3): Workroom face ACT-1 10'-0" -> 10'-6"; Grab & Go face GWB 7'-1" -> 7'-7"; Cafe open-to-deck face -> to deck; Cafe GWB bands 9'-0"/11'-0"/11'-6" faces -> ceiling + 6". Evidence ri07_rcp/. CLOSED.
- RI 8/11 (RFI-08): type I (C-I) WD-1 top = 15'-0" AFF (6/A-226A, bubble on 1/A-221 looks west at C-I, verified). 5/8" FRT plywood floor to 15'-0" = 49.7 SF (DERIVED 3.31 x 15); GWB above per RI 7 rule. CLOSED.
- RI 9/11 (RFI-14), resolved from drawings (user rule: search, don't ask): 2/A-221 studs UP TO DECK, 5/8" FRT plywood behind WD-1, 5/8" GWB above WD-1 and at soffit bottom, "T.O. WD-1 SEE ELEVATION".
  - EAST face (6/A-226A, verified bubble): WD-1 from soffit bottom ~11'-0" to 15'-0" (printed 4'-0" band + 15'-0"); GWB above 15'-0" to deck.
  - NORTE face (1/A-226A, verified bubble): WD-1 from 9'-0" to 11'-0" (printed); sign panel WD-1 above: top NOT printed -> stays GWB, RFI-14 with delta (each 1 ft of WD-1 = SF of that face moves GWB -> FRT plywood). Soffit height conflict 9'-0" (1/A-226A) vs 11'-0" (A-121) -> RFI-14. CLOSED.
- RI 10/11 (RFI-15), from drawings: Cafe Seating cloud = USG drywall suspension per 4/A-121 (DGLW26 main tee @48" 194.17 LF/17 pcs, DGLW424 cross tee @16" 443.19 LF/120 pcs [USG standard spacing, not printed -> note + alt 24" = 84 pcs], DGCM27 107.21 LF, DGWM24 107.21 LF); remove furring -310.23 LF and carrying -194.16 LF from the cloud. Carrying direction E-W confirmed (joists N-S per 1/A-400A and 2/A-400A). CLOSED.
- RI 11/11 (RFI-16), from drawings: vestibule box per 4/A-210, 6/A-210, 1/A-210: 8" joist 11 pcs x 8.0 = 88.0 LF (new family); box beam 8" 18 ga stud 25.33 LF + 6" 16 ga track 25.33 LF; 8" ledger 12.67 LF; posts 3-5/8" 18 ga stud 126.0 LF + track 5.0 LF; 3/4" FRT plywood 106.6 SF; 5/8" Type X GWB ceiling 97.1 SF + box beam faces 8.4 SF; post sheathing "AS REQUIRED" = RFI; trim not drawn. CLOSED.
- ALL 11 REVIEW ITEMS CLOSED -> rev3.

## Open RFIs answered by estimator (rev3 → rev4)
- RFI-14 part 1: north face sign band WD-1 top = 15'-0" (same as east face, 6/A-226A). North face WD-1 from 9'-0" to 15'-0"; GWB above to deck.
- RFI-14 part 2: Cafe soffit bottom = 11'-0" (A-121 RCP governs over 1/A-226A 9'-0"). Consequence: north face WD-1 runs from soffit bottom 11'-0" to 15'-0" (same as east face). RFI-14 CLOSED.
- RFI-16: vestibule posts sheathing = 3/4" FRT plywood, 4 faces, full height: 6 posts x 4 faces x 5" x 10.5 ft = 105.0 SF (DERIVED; 6 posts per 4/A-210, height 10.5 ft as in posts studs). CLOSED.
