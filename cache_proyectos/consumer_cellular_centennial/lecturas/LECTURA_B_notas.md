# Reader B notes: Consumer Cellular, 8283 S. Akron St #110 (A100 p.7)

Scale: 1/4" = 1'-0" = 18 pt/ft. Checked against 31'-6 1/2" (567.75 pt vs. 568.0 pt band) and 44'-3 1/2" (797.25 pt vs. 797.3 pt). New walls are the 0.6-gray filled poché on A100. Coordinates are in pt in the visible (rotated) frame.

## Tag occurrence -> wall (A100)
| Tag id | Type | pos (pt) | Wall |
|---|---|---|---|
| PC0007, PC0004 | A3 | (1117,558), (1525,552) | A3-01 north demising, sales |
| PC0008 | A3 | (1419,1287) | A3-02 south demising, sales |
| PC0009 | A3 | (916,1286) | A3-03 south demising, utility |
| PC0005, PC0010 | C3 | (1011,786), (1011,1055) | C3-01 BOH/Hall vs Sales |
| (none) | C3 assumed | n/a | C3-02 framing over 4'-0" cased opening (2/A400, T.O. opening 8'-0") |
| MANUAL D @ (709,855) | D | n/a | D-01 restroom north / office south. The script missed this single-letter tag. |
| PC0013 / PC0014 | E3 | (774,781)/(773,781) | One diamond with 2 leaders, detected twice: PC0013 -> E3-01 office N, PC0014 -> E3-02 office E (+door 6C) |
| PC0015 | E3 | (828,915) | E3-03 restroom E |
| PC0018 | E3 | (737,1057) | E3-04 hallway N west (+door 4C, 7" pier) |
| PC0017, PC0016 | E3 | (793,1057), (837,1057) | E3-05 vanity alcove back |
| (untagged) | E3 | n/a | E3-06 alcove returns 2 x 1'-1" |
| PC0006 | E3 | (953,1002) | E3-07 hallway N east (+door 5C) |
| PC0011, PC0012 | E3 | (1011,1159), (1011,1256) | E3-08 utility/sales |
| PC0020, PC0019 | E3 | (716,1212), (851,1212) | E3-09 / E3-10 mop sink walls 2'-4" |

Discarded: CO2 (13 occurrences) is the title-block store number. TC1/TC2 (6 occurrences) are electrical/FA tags.

## Type legend (1/A500, 3/4"=1'-0"; suffix = stud size: 1=1 5/8, 2=2 1/2, 3=3 5/8, 4=6")
- **A#**: furred wall to deck. 20 ga @16", 5/8" X board to 6" above the ceiling, 1/2" gap from the existing wall. Top 4/A500 (bubble) and 5/A500 (furred condition, board one side).
- **C#**: wall to deck. 18 ga @16", 5/8" X each side to ceiling +6". Top 4/A500 (slip).
- **D**: 6" 20 ga @16", 5/8" X each side to ceiling +6", batt insulation, to deck. Top 4/A500.
- **E**: 18 ga @16", 5/8" X each side to ceiling +6". Studs stop at about ceiling +6" on a 20 ga track and are braced to structure per 3/A500 (362S137-33 @48"; doubled up to 15').
- **H**: furred, 6" 20 ga, one side. Not used on A100.
- Bottom track for all types: 2/A500 (20 ga, Hilti X-U @24").

## Heights
- Deck heights: Sales 17'-1 9/16" and BOH 16'-4" (A100).
- Ceilings (A200): BOH, Sales and Hallway 11'-11" C-2 ACT; Office and Utility 9'-0" C-2; Restroom 8'-0" C-1 gyp board (PT-1).
- Each face goes to its room's ceiling +6".
- E framing goes to the highest adjacent ceiling +6" = 12'-5" (Utility mop-sink walls 9'-6").

## Details followed
2/A500, 3/A500, 4/A500, 5/A500, 6/A500; doors 2/A600, 3/A600 (HM KD frame, double studs at jambs); 2/A400 (opening 4'-0" x 8'-0", logo-wall face 30'-7", 9'-7"); 1/A402 (restroom FRP to 4'-0"); D100 (keynotes 14 column, 17 existing hallway-south wall remains, 20/22 existing furring/soffit remain, 27 existing south furring removed).

## Open questions (RFIs in JSON)
1. Type A text says "each side", but the wall is furred. Carried one side.
2. Deck height at the C3 line and in the west zone is not tagged.
3. The type above the 4'-0" opening is not tagged.
4. Finish level is not specified (A700 is a finish schedule only).
5. E walls between rooms with different ceilings: carried to the higher ceiling +6".
6. A3-01 at the existing column: stop or wrap?
7. No framing detail for the C-1 restroom ceiling.
8. The existing hallway-south wall is patch only.
