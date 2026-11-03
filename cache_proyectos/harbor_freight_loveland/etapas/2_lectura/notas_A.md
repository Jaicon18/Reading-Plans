# Reader A notes — Harbor Freight Tools, Loveland CO

## Project data sheet
| Item | Value | Sheet |
|---|---|---|
| Name | Harbor Freight Tools (HFT) tenant improvement | A0.0 / title block |
| Address | 1325 E. Eisenhower Blvd., Loveland, CO 80537 | title block |
| Type | Interior TI in existing building + exterior mods (bi-parting entry, H.M. doors, 8'x10' O.H. door, receiving enclosure 20'x60') | A0.0 project scope |
| Owner / tenant | Harbor Freight Tools (tenant); landlord riser room demised | A0.0, A1.1 |
| Architect | ADA Architects, Lakewood OH, job 26041, 10/07/26 | title block |
| GC | Marco Contractors (invite only, not in set) | — |
| Area | 15,813 SF gross leased (sales 9,769 / non-sales 6,044) | A0.0, A1.2 |
| Stories | 1 | A0.0 / A3.x |
| Construction type | IIB, fully sprinklered | A0.0 |
| Occupancy | M (Mercantile); B core, S-1 stock in load calc | A0.0 |
| Codes | 2024 IBC / IECC / IMC / IPC / IFC, 2023 NEC | A0.0 |
| Occupant load | 186 calculated (150 anticipated) | A0.0 |
| Sprinklered | yes (8" main/riser in landlord riser room) | A0.0 |
| Demo | yes — D1.0 (200-series keynotes) | D1.0 |
| Specs | no project manual; A0.3/A0.4 = concrete repair / floor specs (raster) only; A0.2 general notes; A4.1 wall type notes; S1.0 CFS notes | A0.2, A0.3, A0.4, A4.1, S1.0 |

## Wall types (read on A4.1 — NOTE: brief summary had A/B swapped)
- A: 6" x 20 GA studs @ 16" to existing deck (6" track at deck, standard), 5/8" gyp each side ending 6" above ceiling or to deck where no ceiling; one side to deck at support-office walls; studs stop 6" above ceiling between toilet rooms.
- B: 2-1/2" x 20 GA @ 16", 8'-6", 5/8" one side (furring against wall). C: 3-5/8" x 20 GA @ 16", 8'-6", 5/8" one side.
- D: 1-hour UL U419, 6" x 20 GA @ 16", 1 layer 5/8" Type X each side to 1" below deck, slip track 10/A4.1, CJ 9/A4.1 @ 30'.
- E: 5/8" on 1-1/2" hat channel @ 24" vertical over masonry; south wall to underside of deck, west wall to 16'-0".

## Heights chain
- B.O. deck (A1.2 chart + spots, A2.0 spots): ±16'-11" north end → ±17'-3 1/2" / ±17'-5 1/2" (RR) → ±18'-0 1/2" (offices) → ±18'-2" / ±18'-1 1/2" (vestibule) → ±18'-3" (riser, south end). B.O. structure: Sales ±16'-9"/±15'-9 1/2", Replenishment ±15'-9 1/2"/±15'-5".
- D-01: 18'-3" − 1" = 18.17 ft (conservative high point, RFI-01). D-02..04: 18.17 (riser bay 18'-3").
- A office cluster: deck ±18'-0 1/2" (A-04 at storage: 18'-3"). RR/BR block: ±17'-5 1/2". A-15: 8'-6" (stop 6" above ceiling).
- Room faces with lay-in ceiling 8'-0" (A2.0): 8'-0" + 6" = 8.5 ft. Faces to open-to-structure rooms: to deck.
- B / C: 8'-6" printed. E west 16'-0" printed; E south to deck 18'-3".
- Vestibule bulkhead (1/A5.3): storefront ±10'-0" V.I.F. + 6" box header → deck 18'-3": studs 7.75 ft; sales face 8.25 ft; vestibule face to 6" above 10'-6" ceiling = 1.0 ft.
- Demo: B.O. structure of bay (A1.2) — Sales 16'-9", Replenishment 15'-9 1/2" (RFI-03).

## FRP finding
WC-1 = "FIBER REINFORCED PLASTIC (FRP) TO CEILING", Marlite (A1.3 finish schedule), on Restroom 1 107 / Restroom 2 108 walls (A1.3 room schedule, A4.0 keynote 701) and mop sink alcove ("WC-1 TO GYP. BD SHELF EA. WALL", 1/A4.1). Not by tenant vendor — G.C. finish. Loaded misc_items FRP-01 530 SF (RR, to 8'-0" ceiling), FRP-02 53 SF (mop alcove, to shelf 8'-0"). Calculator decides scope.

## Results (reader A)
- LF: D 239.12 (D-01 209.10 + riser 30.02), A 143.30, B 32.04, C 22.86, E 156.63 (hat channel), vestibule bulkhead (VH) 30.97.
- Board SF (faces, no deductions): 5/8 Type X 8,689.6; 5/8 regular 6,125.2; 5/8 MR 804.5 (+5.3 mop shelf = 809.8).
- Ceilings: no gypsum ceilings; ACT excluded; mop-sink gypsum shelf 5.27 SF in misc_items.
- Demo: 7,605.7 SF (9 elements, demo_geom_A.json, demo_cruce_A.md).
- RFIs: RFI-01 D sloped deck height; RFI-02 headers not called; RFI-03 demo construction/height; RFI-04 receiving enclosure structural CFS (not quantified).

## Problems with tools / schema (data kept in allowed places)
1. No hat-channel family: type E loaded with stud_size '1-1/2" hat channel (Z-furring slot)' -> counted in "1-1/2\" Z-furring" family (1,393.75 LF), bottom/top track False. Label in Excel will read Z-furring; the member is a 1-1/2" hat channel @ 24" O.C.
2. Mop-sink gypsum shelf (1/A4.1) cannot be a ceilings[] framed_soffit without drop_lines; kept as misc_items SHELF-J (3-5/8" joists + track 11.3 LF) and SHELF-B (MR 5.27 SF).
3. FRP block requires tile_base perimeters; used frp_none_reason + misc_items familia "FRP".
4. Vestibule bulkhead walls use element "vestibule_head" with tag "VH" (no partition tag); faces/heights per 1/A5.3.
5. Bracing (2/A4.1 Spazzer, A4.1 note 7 CRC) entered as bracing_rows=2 on walls > 12'; Spazzer item listed in misc_info (no family).
6. Receiving enclosure structural CFS (S2.1/S4.1, 600S162-54, built-up box beams) NOT taken off — misc_info RECV-ENCL + RFI-04. This is the biggest open gap of this reading.
7. G.C. bar stock at top of E west wall (E/A4.1, A2.0 520) in misc_info (no family).
8. Window 306: one keynote with two leaders; recorded as two 4'-0" openings (A-01 and A-02); each wall shows a 27 pt (4'-0") gap.

## Sheets opened
A0.0, A0.2 (text), A0.3, A0.4 (raster, rendered: concrete specs), D1.0 (rendered + vectors), A1.1 (rendered + vectors), A1.2 (rendered), A1.3 (text), A1.3A (text grep), A2.0 (rendered + text), A3.0 / A3.1 (text grep), A4.0 (rendered + vectors), A4.1 (rendered), A4.2 / A4.3 (text), A5.0 (text), A5.2 (rendered), A5.3 (rendered), S1.0-S4.1 (text grep), M1.0-M1.3 / P1.0-P1.1 / FP1.0 / E sheets (text grep only for heights, ducts excluded by order). Whole-set grep: DECK, B.O., STRUCTURE, JOIST, A.F.F., FRP, GYP, METAL STUD, LEVEL, HEADER.
