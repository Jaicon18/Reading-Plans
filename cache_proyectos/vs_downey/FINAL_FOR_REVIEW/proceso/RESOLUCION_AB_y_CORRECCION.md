# RESOLUCION A/B - VS #679 Stonewood (Downey CA) - R80e.37

Base: takeoff_canon_A.json (A). Other reading: takeoff_canon_B.json (B). Result: takeoff_canon_AB.json (`validar_canon.py` -> CANON OK).
Geometry rules applied: E28 (one wall = one straight line of a type; collinear runs through T's are one wall; jogs <= 1 ft go with the run), R70.2 (one owner per L corner: the H wall), R70.3 / R77.10 (doors and cased openings inside the run). Lengths stay DERIVED from the A02.01 135-deg hatch vectors at 18 pt/ft (text is outlined).

## Global decisions
- Type names (alerts 1-10 'type no inventariado'): final canon uses the M/A02.01 schedule hatch types as short tags STD, FUR, COL, INS, RFID, SF; `type_order` = schedule order. N/A02.01 (M)
- FUR vs STD (B: 33 walls FUR; A: all STD): M/A02.01 has a single (N) STANDARD PARTITION row calling A/A12.01 AND C/A12.01; C/A12.01 (FURRED PARTITION) is studs against the (E) demising wall with board on the room side only. FUR = the 8 runs along the (E) demising walls (W001, W007, W008, W061, W063, W064, W065, W066). The other 25 B 'FUR' pieces are niche / pilaster returns at enclosed voids: STD A/A12.01 with board one side ('INSTALL GYP BD / FINISH ON ONE SIDE ONLY AT INACCESSIBLE VOID CONDITIONS', M/A02.01; A/A12.01 'DO NOT INSTALL SHEATHING ON BACK SIDE OF STUDS IN VOID AND FURRED WALL LOCATIONS'). B-031 / B-104 are pier faces (inside SP2). Board is one face in both cases, so only the type LF changes. N/A02.01, C/A12.01, A/A12.01
- Face HEIGHT of paired walls (A: ceiling + 6" everywhere; B: to ceiling at gyp ceilings): rooms with a P-230 gyp board ceiling on drywall grid (N/A12.02) get board to B.O. ceiling (A/A12.01 shows the board ending at 'LINE OF CLG WHERE OCCURS'); ACT rooms (STOCK, RECEIVING, BREAK) get ceiling + 6" (C/A12.01 'GYP. BD. TO EXTEND 6" ABOVE A.C.T. CEILING'), capped at the wall height; ELECTRICAL (no ceiling) goes to the top of the wall. Ceiling heights are the A03.01 tags (both readings agree, except display windows below). N/A12.01, C/A12.01, A03.01
- Wall height: STD / FUR / RFID = T.O. STUD ±12'-0" printed (A/A12.01, C/A12.01); A's 12.5 ft at STOCK walls (W001, W020, W067, W074, W075) -> 12.0, conflict kept in RFI-02. INS = 15.917 ft tight to structure (conservative, RFI-01 / RFI-03; B had 15.0). SF = 13'-8 1/2" (A/A08.01).
- BOARD per face: walls whose back side is an enclosed void keep one face (A); T-caps at spine ends, the cashwrap closet ends and the go-back / lounge line keep two faces (B). Detail per wall below.

## Differences resolved (difieren, by revision item number)
- #28 W084 vs B-076: geometry B (5.111 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #29 W070 vs B-066: geometry B (5.556 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #30 W102 vs B-093: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #31 W097 vs B-089: geometry B (1.806 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #32 W103 vs B-094: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #33 W104 vs B-095: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #34 W109 vs B-100: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #35 W081 vs B-073: geometry B (1.556 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #36 W092 vs B-084: geometry B (1.778 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #37 W110 vs B-101: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #38 W068 vs B-064: geometry B (1.167 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #39 W053 vs B-045+B-051: geometry B (1.694 LF, extra W116=B-051); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #40 W086 vs B-078: geometry B (1.556 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #41 W073 vs B-068: geometry B (1.167 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #42 W095 vs B-087: geometry B (5.111 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #43 W034 vs B-025: geometry B (2.306 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #44 W089 vs B-081: geometry B (4.639 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #45 W045 vs B-037: geometry B (1.972 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #46 W027 vs B-017+B-079: geometry B (2.306 LF, extra W117=B-079); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #47 W026 vs B-016+B-071: geometry B (2.167 LF, extra W118=B-071); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #48 W048 vs B-041: geometry B (6.972 LF); restroom W north wall runs through door 8A to the corner (R77.10); faces from B. N/A02.01
- #49 W040 vs B-030: geometry B (10.75 LF); break room / MGR wall hatch is continuous 371.6-578.5 pt (the A-2 marks are shelving symbols, not gaps); A had split it (W038, W039); faces from B. N/A02.01
- #50 W072 vs B-067: geometry B (19.889 LF); break-room / MGR east line runs through the break-room cased opening (R70.3); A had cut it (W071); faces from B. N/A02.01
- #51 W021 vs B-011: geometry B (49.694 LF); FR alcove / lounge south line is one wall through the TRANS4 cased opening (P1/A10.03, dashed header on A02.01) (R70.3); A had cut it (W022); faces from B. N/A02.01
- #52 W101 vs B-092: geometry B (15.472 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #53 W107 vs B-098: geometry B (15.472 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #54 W049 vs B-042: geometry B (7.028 LF); restroom E north wall runs through door 8A to the corner (R77.10); faces from B. N/A02.01
- #55 W054 vs B-046+B-052: geometry B (1.917 LF, extra W119=B-052); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #56 W094 vs B-086: geometry B (5.111 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #57 W098 vs B-090: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #58 W108 vs B-099: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #59 W032 vs B-021: geometry B (3.972 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; S both rooms, N only east of spine. N/A02.01
- #60 W080 vs B-072: geometry B (1.528 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #61 W096 vs B-088: geometry B (2.389 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #62 W007 vs B-002: geometry B (20.944 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #63 W065 vs B-056: geometry B (20.944 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #64 W069 vs B-065: geometry B (2.139 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #65 W050+W051 vs B-043: geometry B (4.944 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #66 W042 vs B-034: geometry B (4.5 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #67 W020 vs B-010: geometry B (6.861 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #68 W099+W100 vs B-091: geometry B (18.694 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #69 W014 vs B-008: geometry B (36.278 LF); FR front line is one wall through the 6 fitting-room doors 5QG (R70.3 / R77.10); A had cut it at every jamb (W015-W019 = jamb stubs); faces from B. N/A02.01
- #70 W044 vs B-036: geometry B (1.944 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #71 W063 vs B-054: geometry B (19.667 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #72 W105 vs B-096: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #73 W052 vs B-044: geometry B (3.528 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #74 W064 vs B-055: geometry B (21.0 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #75 W056+W057 vs B-047: geometry B (4.444 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #76 W012 vs B-006: geometry B (2.583 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #77 W058 vs B-048: geometry B (4.417 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #78 W059 vs B-050: geometry B (2.583 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #79 W009 vs B-004: geometry B (2.028 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #80 W010+W011 vs B-005: geometry B (4.417 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #81 W001+W002+W003+W004+W005+W006 vs B-001: geometry B (68.472 LF); collinear furring line along the (E) demising wall is ONE wall although the FR partitions T into it (E28 rule 1); faces from B. N/A02.01
- #82 W111 vs B-102: geometry B (1.833 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #83 W023 vs B-013: geometry B (1.389 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #84 W112 vs B-103: keep A hatch extent (891.0-1114.6 pt, 12.422 LF); B ran the wall over 3.67 ft of unhatched line + pier face. N/A02.01
- #85 W055 vs B-049: geometry B (2.028 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #86 W085 vs B-077: geometry B (1.528 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #87 W090 vs B-082: geometry B (14.944 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #88 W093 vs B-085: geometry B (1.806 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #89 W047 vs B-040: geometry B (2.111 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #90 W031 vs B-023: geometry B (1.806 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face (A): back side = enclosed void. N/A02.01
- #91 W037 vs B-028: geometry B (2.222 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #92 W036 vs B-027: geometry B (1.333 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #93 W046 vs B-039: geometry B (10.944 LF); MGR south wall runs through door 11 to the corner (R77.10); faces from B. N/A02.01
- #94 W029 vs B-019: geometry B (1.889 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; one face N ROOM 4 (south = 5 pt void to W031). N/A02.01
- #95 W077 vs B-070: geometry B (17.083 LF); RFID line runs through door 7B to the end of the crosshatch (R77.10); B splits from B-069 at the 7 pt jog (gaps_ok); faces from B. N/A02.01
- #96 W114 vs B-108: geometry B (4.861 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #97 W115 vs B-109: geometry B (4.778 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #98 I07 vs B-061: geometry B (7.75 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #99 I04 vs B-032: geometry B (2.167 LF); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from A. N/A02.01
- #100 I01 vs B-009+B-060: geometry B (1.833 LF, extra I08=B-060); corner ownership per R70.2 (H wall owns the L corner) / hatch extent on A02.01; faces from B. N/A02.01
- #96 W114 vs B-108 (SF): geometry B (4.861 LF); faces: A had only the display-window side, B only the mall side -> both (display window 5/8 X to 11'-2" ceiling; mall 1/2" MR under SF-91 to 13'-8 1/2"). N/A02.01, A/A08.01, A/A08.05
- #97 W115 vs B-109 (SF): geometry B (4.778 LF); faces: A had only the display-window side, B only the mall side -> both (display window 5/8 X to 11'-2" ceiling; mall 1/2" MR under SF-91 to 13'-8 1/2"). N/A02.01, A/A08.01, A/A08.05
- #15 W061+W062 vs B-053 (coinciden LF, corner/E28): merged into W061 = B-053 band (18.194 LF), one wall through the T of W070 (E28 rule 1); fixes the two unowned corners W061/W070, W062/W070. N/A02.01

## Corner / partition fixes made while merging (R70.2, E28)
- corner W029: 692.5-726.5 pt (1.889 LF) -> 698.5-726.5 pt (1.556 LF): T into the RFID wall W075/W076 (jog 697-698.5): branch ends at its face 698.5 pt (R70.2). N/A02.01
- corner W031: 694.0-726.5 pt (1.806 LF) -> 697.0-726.5 pt (1.639 LF): T into the RFID wall W076: branch ends at its face 697.0 pt (R70.2). N/A02.01
- corner W034: 692.5-734.0 pt (2.306 LF) -> 697.0-734.0 pt (2.056 LF): T into the RFID wall W076: branch ends at its face 697.0 pt (R70.2). N/A02.01
- corner W037: 694.0-734.0 pt (2.222 LF) -> 697.0-734.0 pt (2.056 LF): T into the RFID wall W076: branch ends at its face 697.0 pt (R70.2). N/A02.01
- corner W047: 702.0-740.0 pt (2.111 LF) -> 703.5-740.0 pt (2.028 LF): T into the RFID wall W077: branch ends at its face 703.5 pt (R70.2). N/A02.01
- corner W053: 702.0-732.5 pt (1.694 LF) -> 703.5-732.5 pt (1.611 LF): T into the RFID wall W077: branch ends at its face 703.5 pt (R70.2). N/A02.01
- corner W074: 849.1-1097.0 pt (13.772 LF) -> 852.5-1097.0 pt (13.583 LF): T into the furring line W001: branch starts at its face 852.5 pt (R70.2) (= B-069). N/A02.01
- corner W082: 845.6-937.8 pt (5.122 LF) -> 852.5-937.8 pt (4.739 LF): T into the furring line W001: branch starts at its face 852.5 pt (R70.2) (= B-074). N/A02.01
- corner I03: 1213.5-1594.1 pt (21.144 LF) -> 1213.5-1587.0 pt (20.75 LF): L with I04: the H wall owns the corner (R70.2, as B-062/B-032). N/A02.01
- corner W041: 1117.6-1188.4 pt (3.933 LF) -> 1110.0-1188.4 pt (4.356 LF): L with W088: the H wall owns the corner (R70.2) (= B-033). N/A02.01
- corner W088: 1594.4-1608.1 pt (0.761 LF) -> 1594.0-1601.5 pt (0.417 LF): between W041 and W044, both H walls own their corners (R70.2) (= B-080). N/A02.01
- corner W024: 1144.6-1182.7 pt (2.167 LF) -> 1151.5-1190.5 pt (2.167 LF): L with W093: the H wall owns the corner; printed 2'-2" kept (= B-014). N/A02.01
- corner W030: 1109.7-1144.4 pt (1.928 LF) -> 1117.0-1151.5 pt (1.917 LF): L with spine W089: the H wall owns the corner (R70.2) (= B-020). N/A02.01
- corner W066: 2072.4-2441.5 pt (20.506 LF) -> 2072.0-2448.5 pt (20.917 LF): L with W111: the H wall owns the corner (R70.2) (= B-057). N/A02.01

## Only in A (solo_A)
- W015: removed, FR5 door jamb stub, inside the FR front run W014 (R70.3 / R77.10) -> carried in W014. N/A02.01
- W016: removed, FR4 door jamb stub, inside W014 -> carried in W014. N/A02.01
- W017: removed, FR3 door jamb stub, inside W014 -> carried in W014. N/A02.01
- W018: removed, FR2 door jamb stub, inside W014 -> carried in W014. N/A02.01
- W019: removed, FR1 door jamb stub, inside W014 -> carried in W014. N/A02.01
- W022: removed, east piece of the FR south line, joined to W021 through the TRANS4 cased opening (R70.3) -> carried in W021. N/A02.01
- W038: removed, part of the continuous break-room / MGR wall W040 (hatch continuous) -> carried in W040. N/A02.01
- W039: removed, part of the continuous break-room / MGR wall W040 (hatch continuous) -> carried in W040. N/A02.01
- W071: removed, upper piece of the break-room east line, joined to W072 through the cased opening (R70.3) -> carried in W072. N/A02.01
- W060: removed, same segment as B-051 (carried as W116 in the W053 jog group) -> carried in W116. N/A02.01
- W079: removed, 7 pt jog between W053 and W116: jog <= 1.0 ft goes with the run it touches (E28 rule 3); A double-counted both corners -> carried in W053. N/A02.01
- W078: removed, 5.5 pt closing jog between W029 and W031 (E28 rule 3; R74.3); A counted 1.35 LF of corners -> carried in W029. N/A02.01
- W087: removed, same segment as B-079 (carried in the W027 jog group) -> carried in W117. N/A02.01
- SP1, SP2: kept (see piers below). N/A02.01, S02.01

## Only in B (solo_B)
- B-012: ADDED as W120 - real 135-deg hatch 726.3-751.8 pt on A02.01 (pilaster jog between W080 and W026); missed by A. N/A02.01
- B-024: not added (duplicate) - south (SF) face of pier SP1; pier box carried whole as SP1 (E28 rule 5, printed chain 4 7/8"+3'-3"+6"+2"). N/A02.01
- B-106: not added (duplicate) - east (SF) face of pier SP1 (inside SP1). N/A02.01
- B-029: not added (duplicate) - north (SF) face of pier SP2 (inside SP2). N/A02.01
- B-107: not added (duplicate) - east (SF) face of pier SP2 (inside SP2). N/A02.01
- B-104: not added (duplicate) - west (STD hatch) face of pier SP2 (inside SP2). N/A02.01
- B-031: not added (duplicate) - south (STD hatch) face of pier SP2 (inside SP2). N/A02.01

## Paired walls - attributes (ALTURA / BOARD), ceilings, items
- W028 vs B-018 (coinciden, BOARD): T-cap at spine end, both sides exposed -> faces from B (2 sides). N/A02.01
- W033 vs B-022 (coinciden, BOARD): T-cap at spine end, both sides exposed -> faces from B (2 sides). N/A02.01
- W043 vs B-035 (coinciden, BOARD): T-cap at spine end, both sides exposed -> faces from B (2 sides). N/A02.01
- W113 vs B-105 (coinciden, BOARD): east side faces VS DISPLAY WINDOW 2 (exposed room, ceiling 11'-2") -> keep A (2 faces). N/A02.01, A03.01
- W025, W024, W030, W041, W088 vs B-015, B-014, B-020, B-033, B-080 (coinciden, BOARD): back side is an enclosed void (pilaster box / 3 pt double-wall gap) -> keep A (1 face). N/A02.01
- ceiling VS DISPLAY WINDOW 1: 10'-2" (A) vs 11'-2" (B) -> 11'-2" P-230 (tag in the display window). N/A03.01
- ceiling VS DISPLAY WINDOW 2: 10'-2" (A) vs 11'-2" (B) -> 11'-2" P-230 (tag in the display window). N/A03.01
- ceiling DISPLAY BLIND VESTIBULES 1+2 (only B, 25.9 SF @ 10'-2" P-230): added, tag confirmed on A03.01. N/A03.01
- ceiling TRANS 1 (only B, 10'-6" SF-91): NOT added - SF-91 is the storefront finish system, gyp board substrate not shown -> RFI. N/A03.01
- misc_items: added from B diagonal braces A/S03.01 (234 x (15.917-12) x 1.414 = 1296.04 LF, brace height on this canon's B.O. structure), brace clips 234 EA, water-heater jack studs 16 LF, third beam (1) 18.33 LF (3rd coded-note-1 tag on S02.01 plan; A carried only 2). Kept A for beams 1-4, posts, head boxes, trusses, clips and the water-heater shelf (A at max sizes; B's smaller counts superseded). N/S02.01, A/S03.01, N/S03.01
- blocking_items: added MIRROR-BLK-41 (A02.01 keynote 41 mirror, in-wall metal blocking) from B; A's restroom / FR / shelving / Garcy / beauty cabinet rows kept (B's RR and shelving rows are the same items). N/A02.01, E/A12.01
- trim_items: added cased-opening corner bead (TRANS4 + break room, 79.11 LF) from B; B's 1,335 LF outside-corner bead was computed on B's own geometry -> not merged, kept in RFI-14 as option. N/A02.01, A15.04
- soffit sides: B-SS1 = A SS1 (cashwrap, kept A F/A10.05); B-SS2/SS3 (display window heads H/A08.15) and B-SS4 (portal A/A08.01) = A misc 'display window head trusses' and 'grille portal head box' (S02.01) -> not duplicated; B-SS5 (A/A12.02 0.5 ft) not confirmed as framing -> not added. A's 6 beauty-cabinet valances (B/A10.03) kept. N/S02.01, A10.03
- piers SP1 / SP2 (only A, column_wrap boxes) vs B-024, B-106, B-029, B-107, B-104, B-031 (only B, pier faces): same two piers; kept A boxes (closed box = one wall, E28 rule 5; printed chain 4 7/8"+3'-3"+6"+2" and 2'-0"; the 6L door is inside SP1's north side, R70.3); B pieces not added (would double count). N/A02.01, A/A08.01, S02.01

## Result
- Walls in canon: 118 elements.

| Type | Count | LF |
|---|---|---|
| STD | 83 | 441.79 |
| FUR | 8 | 211.00 |
| COL | 4 | 16.87 |
| INS | 8 | 45.05 |
| RFID | 4 | 59.81 |
| SF | 4 | 34.93 |
| SOFFIT (soffit_side) | 1 | 15.12 |
| VALANCE (soffit_side) | 6 | 70.50 |

## Merged RFI list
- **RFI-01** (B RFI-01 + A RFI-18 + A RFI-12 (resolution R80e.37)): Height of the (E) roof structure over the tenant space is not printed (A/A12.01 and C/A12.01 show 'B.O. (E) ROOF DECK / STRUCTURE' without elevation; S03.02 / S05.01 give none; S05.01 says 'EXISTING ROOF CONSTRUCTION: WOOD JOISTS ON STEEL BEAMS' while N/A08.05 prints '±15'-11" B.O. JOIST / ±17'-0" B | Assumption: Conservative: 15.917 ft A.F.F. (the only printed structure elevation, N/A08.05 B.O. JOIST); not scaled | Delta: A: carried 15.917 ft; B: 15'-0" (reading B) = -0.917 ft x 234 diagonals x 1.414 = -303 LF of brace, -0.917 ft per insulated stud (45.05 LF of INS wall) and per hanger | C: field verify
- **RFI-02** (A RFI-02 + B RFI-03 (resolution R80e.37)): STOCK ceiling is 12'-0" ACT-2 (A03.01); C/A12.01 asks gyp bd 6" above ACT (12'-6") and the schedule studs 6"-12" above ceiling, but A/A12.01 and C/A12.01 print T.O. STUD ±12'-0". Walls facing STOCK (W001, W020, W067, W074, W075) carried at the printed 12.0 ft (stud and board). | Assumption: Printed T.O. stud ±12'-0" carried (printed = carried); board capped at 12'-0" | Delta: A: carried 12.0 ft | B: 12.5 ft = +0.5 ft of stud and board on the STOCK faces (~55 LF, ~28 SF)
- **RFI-03** (A RFI-01 (resolution R80e.37)): (N) INSULATED WALL: A02.01 schedule says 'TIGHT TO STRUCTURE ABOVE' but C/A12.01 (called by the same row) shows T.O. STUD ±12'-0" A.F.F. with diagonal bracing. Which governs? ELECTRICAL has no ceiling tag (board height). | Assumption: Carried conservative: tight to structure (15.917 ft) + deflection track | Delta: studs of I01-I08 (45.05 LF of wall): 15.917 ft (carried) vs 12.0 ft = -3.917 ft per stud; deflection track 45.05 LF -> standard track
- **RFI-04** (A RFI-04 + B RFI-14 (resolution R80e.37)): Storefront exterior faces (piers SP1/SP2, walls W114/W115 exterior side): printed '1/2" MOISTURE RESISTANT GYP BD' under storefront finish system SF-91 (A/A08.05). Confirm board and whether it is by the storefront finish vendor. | Assumption: Carried | Delta: 1/2" MR SF on pier faces (approx 2 x 10.65 x 13.708 = 292 SF) carried in '1/2 exterior gyp sheathing' family
- **RFI-05** (A RFI-05 (resolution R80e.37)): RFID SHIELDED PARTITION non-sales side: '(1) LAYER 5/8" FOIL-BACKED GYP BD ... EXTEND TO CEILING AT MINIMUM'. Spec 092900 H.3 (A15.04) prints the product: 'EQUIVALENT TO SHEETROCK BRAND REGULAR FOIL-BACK, FIRECODE OR FIRECODE "C" CORE ... 5/8" THICK' - which of the three cores is wanted? Carried in  | Assumption: Carried foil-backed in 5/8 regular row | Delta: non-sales faces of W074-W077 carried as 5/8 regular SF (foil-backed)
- **RFI-06** (A RFI-06 + B RFI-07 (resolution R80e.37)): Cashwrap backwrap soffit (F/A10.05) and beauty-cabinet valances (B/A10.03): both say 'SUSPENDED METAL STUD - REFER TO STRUCTURAL DWGS' above the ceiling; no structural detail for it in S01.01-S05.01. Carried: drop / valance studs to the ceiling line only. | Assumption: Carried 3.583 ft | Delta: drop studs carried 8'-5" to ±12'-0" = 3.583 ft on 15.139 LF; to B.O. joist would be 7.5 ft (+3.917 ft per stud)
- **RFI-07** (A RFI-07 (resolution R80e.37)): FR ALCOVE ceiling has no tag on A03.01; carried 9'-0" P-230 like FR LOUNGE / fitting rooms. | Assumption: 9'-0" | Delta: ceiling height affects board height of W014-W021 alcove faces (+/- 0.5 ft x 37.98 LF)
- **RFI-08** (A RFI-08 + B RFI-05 (resolution R80e.37)): H.M. doors 7B, 8A, 11: A/A10.08 and H/A10.08 print B.O. HEAD 7'-0 1/2" and frame '±2"' each jamb but no rough-opening width. Carried R.O. = 3'-0" + 2 x 2" = 3'-4". (FR doors D/A10.08 39 1/4" x 7'-6 1/2", go-back G/A10.08 54", blind doors K & J/A10.08 2'-9" x 8'-7 1/8" are printed and carried.) | Assumption: Leaf width carried | Delta: header/sill LF +/- 0.17 ft per H.M. door (4 doors)
- **RFI-09** (B RFI-06 (resolution R80e.37)): Break room east cased opening (3'-7 3/4" vector, no door tag): head height not printed. | Assumption: head at 8'-0" (corridor ceiling) [PENDING] | Delta: A: cripples/board above head change ± | B: n/a
- **RFI-10** (A RFI-09 + B RFI-09 + B RFI-12 (resolution R80e.37)): In-wall metal blocking whose LENGTH is not printed: restroom accessories (A13.01 keynotes 15,17,19,21,24,29), break-room cabinetry 3 rows (C/A14.02, run length), coat rack 3 rows (D/A14.02, rack width), wall-mounted shelving (A/A14.01 keynote 6, shelf lengths). Printed lengths are carried (A07.04 4' | Assumption: Carried estimates | Delta: blocking carried as PENDING estimates (see blocking_items lf_op)
- **RFI-11** (A RFI-11 + B RFI-08 (resolution R80e.37)): Water heater shelf N/S03.01: plan size '2'-6" MAX / 4'-0" MAX SEE ARCH' - no architectural detail found. Metal members carried at max sizes (6" 20 GA joists, 6" 16 GA edge track, L2x2 16 GA clips). The 3/4" FRT plywood deck is wood -> excluded (not RFI). | Assumption: Carried max | Delta: 12 LF 6" joist + 5 LF 6" track at max
- **RFI-12** (A RFI-13 (resolution R80e.37)): constants.carrying_direction is a schema placeholder: P-230 ceilings are drywall suspension grid (N/A12.02), no carrying channel. | Assumption: n/a | Delta: 0
- **RFI-13** (A RFI-14 (resolution R80e.37)): (E) demising walls: 'REPAIR OR REPLACE 5/8" TYPE X GYP BD IF REQUIRED TO MAINTAIN FIRE RATING (U.L. #U465)' - quantity unknown. | Assumption: Not carried; allowance by estimator | Delta: allowance not carried
- **RFI-14** (A RFI-15 (resolution R80e.37)): Outside-corner metal trim (corner bead) at spine-wall ends, pilasters, display window wall ends and niche returns not enumerated in this reading (only column wraps and pier interior corners carried). | Assumption: Partial | Delta: + corner bead LF (approx 2 per spine end x 11.5 ft)
- **RFI-15** (A RFI-16 (resolution R80e.37)): Ducts on M02.01 cross the RFID wall and FR walls above ceilings; partitions stop at ±12'-0" T.O. STUD and no duct elevation is printed: are any duct penetrations through framing required? Reading B registered 31 duct crossings of wall bands on M02.01 / P02.01 (plan view); none has a printed elevatio | Assumption: 0 | Delta: 0 framed penetrations carried
- **RFI-16** (A RFI-17 (resolution R80e.37)): Wall lengths: sheet text is outlined, so every wall length  is DERIVED from the vector hatch extents of A02.01 at 18 pt/ft, not from printed dimension strings; short jogs (< ~0.7 ft) at niche corners are not banded. | Assumption: Vector-derived lengths carried | Delta: +/- approx 1-2 % of wall LF
- **RFI-17** (A RFI-20 + B RFI-11 (resolution R80e.37)): Storefront head framing: beams, box posts, head boxes and clips are carried from S02.01 / S01.01 coded notes. NOT printed: (a) beam spans (measured in vector on S02.01 at 1/2"=1'-0"), (b) height of box posts to beam bottom (carried 13'-8 1/2"), (c) diagonal length of the 16 head-truss diagonals, (d) | Assumption: not carried | Delta: diagonals 16 pcs x ~4 ft = ~64 LF 3 5/8"; 2 1/2" studs ~ 2 x 11 x 0.5 ft
- **RFI-18** (B RFI-02 (resolution R80e.37)): Stock-room partitions that laterally support floor-mounted shelving (2442F/M rivet racks) fall under Table 3 -> S03.02 (Table A1/A2: 362S162-33 @16" max 13'-0", A2 continuous deep-leg track). A12.01 gives T.O. stud ±12'-0". Confirm stud height / top condition. | Assumption: carried 12'-0" T.O. stud (A/A12.01) | Delta: A: +1.0 ft per stud on stock walls (north furring stock part, electrical walls) | B: none expected (20 ga @16" both cases)
- **RFI-19** (B RFI-04 (resolution R80e.37)): Sales "Trans" spine partitions carry Garcy panels / fixtures on both faces (keynote 39). N/S01.01 note: "AT LOCATIONS WHERE SHELVING OCCURS ON EACH SIDE OF A SINGLE STUD WALL, REDUCE THE STUD SPACING ... BY ONE-HALF". Confirm 8" o.c. at spines. | Assumption: carried 16" o.c. (Garcy panels are wall fixtures, not floor shelving) | Delta: A: spines ~93 LF: stud count x2 (+~70 studs x 12 ft ≈ +840 LF 3-5/8"), diagonals @24" | B: none
- **RFI-20** (B RFI-10 (resolution R80e.37)): Partition schedule allows "(1) LAYER 1/4\" GYP BD W/ 3/8\" FINISH PANEL (REFER TO SPECIFIC DETAILS)" in lieu of 5/8" Type X at sales faces. | Assumption: 5/8" Type X carried on all faces | Delta: A: board type change only (same SF) | B: n/a
- **RFI-21** (B RFI-13 (resolution R80e.37)): FRP WC-1 (A00.03 KEMLITE, "NON-SALES") is tagged as wainscot in restrooms, break room, hallway and electrical (A05.01, note 8); T.O. FRP printed 4'-0" only in restrooms (A13.01). Tile cove base B-13 in restrooms has no cement board backer drawn. | Assumption: FRP only in the two restrooms; no cement board | Delta: A: non-sales FRP (break room/corridor) +4 ft x wall LF if required | B: n/a
- **RFI-22** (B RFI-15 (resolution R80e.37)): Access panels: RCP keynote 8 (24"x24" drop-in trimless at main ceiling) located "coordinate with MEP plans"; only one tag found on A03.01. | Assumption: 1 x 24"x24" + 2 x 36"x12" (keynote 5) | Delta: A: ±1 panel each | B: n/a
- **RFI-23** (new (resolution R80e.37: ceiling only in reading B)): TRANS #1 (storefront portal) ceiling is tagged 10'-6" SF-91 on A03.01 (SF-91 = storefront finish system). Is there a gyp board ceiling / drywall grid behind SF-91 (reading B carried 64.7 SF of gyp ceiling)? | Assumption: Not carried (finish by storefront vendor) | Delta: A: 0 (carried) | B: +64.7 SF gyp bd ceiling on drywall grid at 10'-6"

## Open issues
- B.O. of (E) roof structure not printed over the partitions: 15'-11" carried conservatively (RFI-01); INS walls, braces and hanger drops depend on it.
- STOCK ACT + 6" vs printed T.O. stud 12'-0" (RFI-02); INS 'tight to structure' vs C/A12.01 T.O. stud (RFI-03).
- TRANS #1 SF-91 ceiling (only in B) not carried, RFI-23; B-SS5 (A/A12.02 0.5 ft side) not carried.
- Outside-corner bead still not enumerated on this canon's geometry (RFI-14; B's 1,335 LF is an option only).
- SP1 / SP2 piers carried as whole boxes typed SF although their west / south faces carry the STD hatch (R70.6 parts not split).
- Water-heater shelf counts differ (A max sizes kept; RFI-11).
# CORRECCION — takeoff_canon_AB.json: heights of existing structure from A01.01

Base: `takeoff_canon_AB.pre_correccion.json` (backup). Scripts: `scripts/bays.py`, `scripts/corregir.py`, `scripts/crops.py`.
Crops (red circles = callouts used): `callouts_A0101_plan.png`, `callouts_A0101_INS_west.png`, `callouts_S0301_A_slope.png`.
Validation: `python3 validar_canon.py takeoff_canon_AB.json tools` -> **CANON OK**.

## 1. Callouts read on A01.01 (page 12). All are CONFIRMADO
Box: "LOWEST POINT OF DECK: 17'-0" A.F.F." / "LOWEST POINT OF STRUCTURE: 12'-1" A.F.F."; keynotes 19/20 "EXISTING STRUCTURAL BEAMS / JOISTS TO REMAIN - HEIGHTS NOTED ON PLAN".
The A01.01 and A02.01 coordinates are the same: same grid, same orientation, checked against grid bubbles 5/4/3/2 and A/B.

| Keynote | Callout | Member | Bay (grid) |
|---|---|---|---|
| 20 | @16'-8" | joists, NW (leader at grid 5) | W-5 N / 5-4 N |
| 19 | @12'-8" | grid-B beam, demising pilaster to grid-5 column | W-5 |
| 19 | @14'-11"± | grid-B beam just E of grid 5 | 5-4 |
| 19 | @14'-11" | grid-B beam | 5-4 |
| 19 | @12'-1" | beam on the west demising line (x~366-372 pt), N-S | W-5 |
| 19 | @14'-11 1/2" | grid-A beam | 5-4 |
| 19 | @14'-7 1/2" | grid-A beam | 5-4 |
| 19 | @16'-4" | grid-4 beam, N segment | 5-4 N / 4-3 N |
| 19 | @15'-0" | grid-B beam | 4-3 |
| 19 | @15'-3 1/2" | grid-B beam | 3-2 |
| 20 | @16'-3" | joists | 3-2 M |
| 19 | @15'-3 1/2" | grid-A beam | 3-2 |
| 20 | @15'-11" | joists, east end | 3-2 M / 2-E |
| 19 | @15'-6 1/2" | grid-2 beam, S segment | 3-2 S / 2-E S |

These callouts do not mark structure, so they were not used: keynote 17 duct (@11'-0", @11'-3 1/2"), 18 sprinkler (@15'-9 1/2", @15'-6", @15'-1 1/2", @14'-10", @14'-6"), 27 pipe (@12'-0"±) and 5 (@13'-2 1/2").
Two bays have no callout printed inside them. Both are DERIVADO (conservative): bay 4-3 S takes 16'-4" from the grid-4 beam that bounds it, and bay 2-E N takes 15'-11" from the east-end joists next to it.
The full record is in the canon under `estructura_a0101_info`.

## 2. INS walls (A02.01 "TIGHT TO STRUCTURE ABOVE" + A01.01 + L/S03.01)
Each wall now has `to_deck` true, `purlin` false (the top is wood joists or a steel beam, not a deck flute) and a deep-leg slip track per L/S03.01.

| Wall | LF | Old height | New height | Callout (A01.01) | Status |
|---|---|---|---|---|---|
| I01 | 1.833 | 15.917 | **16.667** | K20 @16'-8" | DERIVADO |
| I02 | 5.150 | 15.917 | **16.667** | K20 @16'-8" | DERIVADO |
| I08 | 0.889 | 15.917 | **16.667** | K20 @16'-8" | DERIVADO |
| I03 | 20.750 | 15.917 | **12.083** | K19 @12'-1" (beam along the run) | CONFIRMADO |
| I04 | 2.167 | 15.917 | **12.083** | K19 @12'-1" (crosses under it) | CONFIRMADO |
| I05 | 4.333 | 15.917 | **12.083** | K19 @12'-1" (only structure printed next to it) | DERIVADO |
| I06 | 2.178 | 15.917 | **12.083** | K19 @12'-1" | CONFIRMADO |
| I07 | 7.750 | 15.917 | **12.083** | K19 @12'-1" (directly under it) | CONFIRMADO |

Faces: the two ELECTRICAL faces (I01, I02) have no ceiling, so the board runs to the top of the wall: 15.917 -> 16.667. The other faces keep their ceiling heights (ceiling + 6" or B.O. ceiling; all are at or below the new wall height).
Note for I01/I08: the @12'-1" beam line is 0.2–0.4 ft east of the wall end. If studs land under its flange, they stop at 12'-1" (field condition).

## 3. RFI-01 CLOSED (answered by A01.01): the ±15'-11" assumption is removed
- `constants.bod_ft` was 15.917 [PENDING] and is now 17.0 (A01.01 "LOWEST POINT OF DECK"). `deck_breaks_none_reason` and the C/A12.01 notes were rewritten.
- **DIAG-BRACE** (misc_items, A/S03.01). The detail prints a 1:1 slope, so length = rise x sqrt(2) (nothing scaled). Rise = the A01.01 callout for the bay(s) the wall sits in, using the highest one (conservative), minus 12.0 (T.O. stud):
  - 48 x 2.958 x 1.4142 = 200.80 (14'-11 1/2", bays 5-4 M/S, W-5 S)
  - 23 x 3.292 x 1.4142 = 107.08 (15'-3 1/2", 3-2 N)
  - 29 x 3.542 x 1.4142 = 145.27 (15'-6 1/2", 3-2 S)
  - 65 x 4.333 x 1.4142 = 398.31 (16'-4", 4-3 N, plus 4-3 S DERIVADO)
  - 69 x 4.667 x 1.4142 = 455.41 (16'-8", W-5 N / 5-4 N). This line includes 1 diagonal of reading B's 234 that could not be placed on a wall (the per-wall ROUNDUP gives 233).
  - **Total 1296.04 -> 1306.85 LF**, single 3-5/8" 20 ga. The longest diagonal is 6.60 ft, under 10'-0", so a single stud is enough. DIAG-CLIP stays at 234. The assignment for each wall is in `diag_brace_bays_info`.
- **Hanger drops** (N/A12.02) were recomputed per room bay as callout minus ceiling. Changes: MGR/CORRIDOR/RESTROOMS 7.917 -> 6.958; HALLWAY 6.917 -> 5.958; AFR6/FR5/FR4/FR ALCOVE 6.917 -> 7.667; FR3/FR2/FR1/FR LOUNGE/GO-BACK 6.917 -> 7.333; CW CLOSETS 6.75 -> 5.791; ROOM 4 5.417 -> 6.167; ROOMS 3/2 4.917 -> 5.333; ROOM 1 4.917 -> 5.25; DISPLAY WINDOW 2 5.75 -> 5.375; DISPLAY WINDOW 1 and blind vestibules stay at 5.75 (DERIVADO 15'-11").
- RFI-06 delta: the suspended soffit studs measured to structure are now 14.958 - 8.417 = 6.541 ft (+2.958 ft/stud). It was 7.5 ft.

## 4. RFI-03 CLOSED
The A02.01 PARTITION SCHEDULE (N) INSULATED WALL row prints "TIGHT TO STRUCTURE ABOVE". The printed row governs over the generic ±12'-0" T.O. STUD of C/A12.01. The walls are carried to the A01.01 callouts with an L/S03.01 deflection track.

## 5. Exclusion (no RFI, no quantity)
Added to `exclusiones_info`: demolition is not our scope. This covers A01.01 keynote 3 "REMOVE EXISTING ENCLOSURE WALL AROUND COLUMN" and keynote 7 "REMOVE EXISTING FURRING TO FACE OF EXISTING DEMISING WALL GYP BD WHERE OCCURS".

## Untouched
The other 110 walls (heights, faces, lengths), nodes and every other RFI except the RFI-06 delta text.
