# SPEC SWEEP - Chuze Fitness Austin Bluffs (metal frame / drywall)

Date 2026-11-02. Read-only check of `Chuze_AustinBluffs_Takeoff_FINAL.xlsx` (Material Summary) against the Project Manual (`specs.pdf`, 1,025 pp.), with cross-checks against `bidset_SIN_MARKUPS.pdf`. Standing rules applied: scope is metal frame + gypsum board only; wood, insulation, ACT, FRP, tile, acoustical sealant, MEP, ducts and ALL fasteners are EXCLUDED. Source order: plans, then specs (both apply when they can coexist), then trade code.

## Sections read

| Section | PDF pages |
|---|---|
| 01 10 00 Summary | p37-40 |
| 01 25 00 Substitution Procedures | p42-45 |
| 01 35 16 Alteration Project Procedures | p77-82 |
| 01 60 00 Product Requirements | p101-105 |
| 05 40 00 Cold-Formed Metal Framing | p324-333 |
| 05 50 00 Metal Fabrications | p335-345 |
| 06 10 53 Misc. Rough Carpentry | p364-367 |
| 06 16 00 Sheathing | p369-373 |
| 07 21 00 Thermal Insulation | p378-380 |
| 07 92 00 Joint Sealants | p424-429 |
| 09 22 16 Non-Structural Metal Framing | p492-498 |
| 09 29 00 Gypsum Board | p500-504 |
| 09 30 13 Tiling | p506-512 |
| 09 51 23 Acoustical Tile Ceilings | p514-518 |

NOT in the manual: 05 41 00, 09 21 16, 07 84 00 (01 10 00 1.8.D.9 references it, but the section is absent), 06 10 00.

Plan sheets cross-checked: G001 p1, G002 p2, G003 p3, G004 p4, G005 p5, A010 p13 (note 27), A103 p16, A121 p18, A301 p21, A421.A p23, A502 p60, A504 p65, A610 p71, S100-S300 p73-76.

## Counts

Material Summary rows reviewed: 51. CONSISTENT 39, APPLY 8, CONFLICT 4. Fasteners: 9 rows stay EXCLUDED (counted as CONSISTENT). Spec items with no row: 13. Div. 01 items: 6, all CONSISTENT / informational. RFIs: 2 (RFI-S01, RFI-S02).

## Material Summary rows

| # | Material row | Spec § | Finding | Class | Delta |
|---|---|---|---|---|---|
| 1 | Bottom track 3-5/8" | 09 22 16 2.2.A.1-2, 2.2.B, 3.2.D; 05 40 00 2.6.B | ASTM C645 track, G40 hot-dip galvanized, depth per drawings, gauge = stud (Excel: track gauge = stud gauge). Min. base steel 0.0147" (25 ga EQ) satisfied. Track gauge on the 16+1 type-A walls follows RFI-S01. | **CONSISTENT** | 0 (gauge of 233.48 + 20.13 LF follows RFI-S01) |
| 2 | Bottom track 6" - per source | 09 22 16 2.2.A-B | C645, G40, gauge = stud. A6C 16.15 LF gauge follows RFI-S01. | **CONSISTENT** | 0 |
| 3 | Bottom track 6" - 600T250-54 | 05 40 00 2.3.B, 2.6.B; S200 C | Structural designation (54 mil, S200 C) = 05 40 00 framing: ASTM A1003 Structural Grade, Type H, coating G60 (not G40). Track unpunched, matching stud thickness. | **APPLY** | product only: specify G60 / A1003 structural on 22.41 LF; qty 0 |
| 4 | Bottom track 2-1/2" | 09 22 16 2.2.A-B | B2E furring track, C645 G40, gauge = stud. Furring studs are restrained by the Z-girt / existing CMU (B/A301), so free-span limiting height does not govern. | **CONSISTENT** | 0 |
| 5 | Top track 3-5/8" - standard (walls not reaching structure) | 09 22 16 2.2.B, 3.2.D | Standard runner where partitions terminate at/above suspended ceiling (3.2.D "except where partitions are indicated to terminate at suspended ceilings"). Head C kickers carry the lateral load (05 40 00 3.5.G stud kickers; RFI-36). | **CONSISTENT** | 0 |
| 6 | Top slip / deflection track 6" (2" deflection leg, walls to structure) | 09 22 16 2.2.C.1, 3.2.D.1; D/A301, E/A301 | Slip-type head joint where framing extends to structure: single long-leg track, 2" flanges, thickness not less than studs -> matches D/A301 "2" SLIP TRACK". The bridging row the spec ties to this track is charged to the C.R. bracing row (APPLY there). | **CONSISTENT** | 0 (see C.R. bracing row) |
| 7 | Top track 6" - standard (walls not reaching structure) - per source | 09 22 16 2.2.B, 3.2.D | Standard runner, C645 G40. | **CONSISTENT** | 0 |
| 8 | Top track 6" - standard (walls not reaching structure) - 600T250-54 | 05 40 00 2.3.B, 2.6.B; S200 C | Structural track (S200) = 05 40 00: A1003 structural, G60. | **APPLY** | product only: G60 / A1003 on 22.41 LF; qty 0 |
| 9 | Top slip / deflection track 3-5/8" (2" deflection leg, walls to structure) | 09 22 16 2.2.C.1, 3.2.D.1 | As 6" slip track. Gauge on type-A walls follows RFI-S01. | **CONSISTENT** | 0 (see C.R. bracing row; gauge per RFI-S01) |
| 10 | Top slip / deflection track 2-1/2" (2" deflection leg, walls to structure) | 09 22 16 2.2.C.1, 3.2.D.1; E/A301 | B2E to deck with 2" slip track (RFI-02). | **CONSISTENT** | 0 (see C.R. bracing row) |
| 11 | 2-1/2" stud | 09 22 16 2.2.A-B, 2.2.B.2 | C645 G40, 16" o.c. (RFI-04/32), furring restrained by Z-girt to existing CMU (B/A301) - deflection not free-span. | **CONSISTENT** | 0 |
| 12 | 6" metal stud (LF of material) - per source | 09 22 16 2.2.B.2; 05 40 00 1.1.A.3; S100 (5 psf interior lateral) | Spec: thickness "as required by performance requirements for horizontal deflection"; framing taller than non-structural limiting heights belongs to 05 40 00. A6C A-A422-3 / A-A422-4 at 22.83 ft in 25 ga (600S125-18) exceed L/240 at 5 psf (~19.9 ft gross-section upper bound). The A6D / X6D 6" 20 ga walls at 22.83 ft are marginal (~24.3 ft gross section), so check them against the manufacturer tables. This contradicts the RFI-04 gauge assumption -> RFI-S01. | **CONFLICT** | RFI-S01: 388.11 LF 25 ga -> 20 ga (A) or no change (B, L/120) |
| 13 | 6" metal stud (LF of material) - 600S162-33 | 05 40 00 2.3.B, 2.4-2.6; 2/A131 | RTU curb-cap frame printed as structural member 600S162-33 -> 05 40 00: A1003 Structural Grade (33 ksi for 33 mil), coating G60. | **APPLY** | product only: G60 / A1003 on 432 LF; qty 0 |
| 14 | 3-5/8" metal stud (LF of material) | 09 22 16 2.2.B.2; 05 40 00 1.1.A.3, 2.3.B, 3.5.E-F; A301 type notes (S501 not in set); A2/A301 "MIN. 25 GA"; S100 5 psf | 16 free-standing type-A walls (A2-3D x3, A3C x13) run 22.83 ft to deck in 25 ga 362S125-18. That cannot meet L/240 (~13.4 ft) or L/120 (~16.9 ft) at 5 psf. A-A421-15 (14.42 ft) fails L/240 only. The spec makes the member a performance item (05 40 00 for heights beyond non-structural limits). This contradicts the RFI-04 assumption (25 ga) -> RFI-S01. Furring types C3C/C3D (22.83 ft) also exceed free-span limits: their brace to the existing construction is not detailed (note in RFI-S01). | **CONFLICT** | RFI-S01 A: 7,115.29 LF -> 362S162-54 @ 12" o.c. (+2,371.6 LF net) + 259.56 LF -> 20 ga; B: 7,115.29 LF -> 362S162-43 @ 16", 0 LF |
| 15 | Ceiling perimeter track at GWB ceilings (size not printed, RFI) | 09 22 16 3.2.D; A502 "METAL CHANNEL"/"TOP TRACK" | Plan-printed member at soffit / ceiling junctions (A502). The 09 51 23 KAM molding is a different location (wall perimeter of the grid). No overlap found. | **CONSISTENT** | 0 |
| 16 | Bracing 1-1/2" C.R. channel | 09 22 16 2.2.F (0.053", 1/2" flanges), 2.2.C.1 ("continuous bridging located within 12 inches of the top of studs"); 05 40 00 3.5.E-F | The member matches 2.2.F (16 ga C.R.C.). Rows = ROUNDUP(H x 12/48) - 1 leaves the top row 2.8-3.8 ft below the head of every 22.83 ft slip-track wall. 2.2.C.1 adds a continuous row within 12" of the top of studs at the single long-leg (2") slip track: +1 row on every slip-track wall. | **APPLY** | +910.70 LF net (409.44 + 397.30 + 103.96 slip-track LF); +1,047.31 LF purchase = +66 sticks 16 ft (388 -> 453). Alt.: proprietary deflection track (2.2.C.2) on 910.70 LF instead, 0 LF bracing |
| 17 | Hanger wire | 09 51 23 3.2.A (ASTM C636), 2.6 schedule; 09 22 16 1.1.A.2, 2.3.C (0.16" dia.); RCP note 9 A121/A421.A; 13/A502 | Plan: #12 ga @ 4'-0" (C-5 is tagged 09 51 23, which only invokes ASTM C636 = 12 ga). 09 22 16 covers "suspension systems for interior ceilings" with 0.16" (~8 ga) wire hangers. Which section governs the C-5 GWB ceiling cannot be settled -> RFI-S02. | **CONFLICT** | RFI-S02: 0 LF; product 12 ga vs 0.16" on 2,428.49 LF |
| 18 | 5/8" gypsum board, MOISTURE RESISTANT | 09 29 00 2.3.E | Spec MR board = 5/8" Type X core, mold resistance ASTM D3273 score 10, consistent with RFI-05 decision ("Type X MR"). Buy as Type X MR (row label omits "Type X"). | **CONSISTENT** | 0 (label: Type X MR) |
| 19 | 5/8" gypsum board, Type X | 09 29 00 2.3.A, 2.3.B (flexible board "to bend to fit radii"), 3.1.B (ASTM C840); 16/A502 reception arc | Type X 5/8" tapered = spec. The reception soffit side A-A421.A-1 (16/A502, 62.2 LF arc, 673.63 SF) is curved. No radius is printed (grid bounding box 22.5 x 27.83 ft suggests R ~11-14 ft), which is below the dry-bend limit of 5/8" board (~25 ft lengthwise, USG/GA). Spec provides 1/4" flexible board for radii -> 2 layers 1/4" flexible on that face. Also noted: 2.3.C 1/2" ceiling board exists in spec, but RFI-05 (5/8" Type X everywhere) stands. | **APPLY** | -673.63 SF Type X (-714 SF purch., ~-15 sh 4x12); +1,347.26 SF 1/4" flexible (2 layers; +1,428 SF purch., ~45 sh 4x8). Conditional on actual radius |
| 20 | 5/8" gypsum board, Type X W.R. (water resistant) | A301 type notes (DensArmor Plus 5/8"); 09 29 00 (no interior glass-mat article); 09 30 13 2.5.B (glass-mat C1178 as tile backer) | Plan names DensArmor Plus 5/8" at pool/spa rooms. The spec is silent on interior glass-mat panels, so the plan governs. Buy DensArmor Plus Fireguard (Type X) per RFI-30. | **CONSISTENT** | 0 |
| 21 | Armstrong HD8906 drywall grid main tee (heavy-duty main runner, spec 09 51 23) | 09 51 23 2.3, 2.6 schedule (HD8906); 01 60 00 2.x sole manufacturer | Exact schedule product. Armstrong is the national-account (sole) manufacturer. Inputs/RFI-33 text says "USG DGLW26" - label only (12 ft length identical). | **CONSISTENT** | 0 (fix Inputs label USG -> Armstrong) |
| 22 | Armstrong XL8945P drywall grid cross tee (spec 09 51 23) | 09 51 23 2.6 schedule (XL8945P 48") | Exact schedule product, 4 ft. Spacing 16" o.c. is not set by the spec (Armstrong installation). | **CONSISTENT** | 0 |
| 23 | Armstrong KAM151220E knurled angle molding at the C-5 perimeter (spec 09 51 23) | 09 51 23 2.5, 2.6 schedule | Exact schedule product (22 ga x 12 ft x 1-1/2"). | **CONSISTENT** | 0 |
| 24 | Armstrong SC151220EQ curved perimeter molding at the reception circle (spec 09 51 23) | 09 51 23 2.6 schedule | Exact schedule product (SimpleCurve). | **CONSISTENT** | 0 |
| 25 | Cement board screws 1-1/4" (manufacturer spacing) | 09 29 00 2.8.B.2 | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 26 | #10 framing screws - printed stud-to-track fastener (see Where it comes from) | 05 40 00 2.8.E | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 27 | Deep-leg slotted deflection track - printed product (see Where it comes from) | 05 40 00 2.6.D; 09 22 16 2.2.C.2; 1/A506 | 16 ga x 4" legs at the roof hatch (1/A506) = deep-leg deflection track. As 05 40 00 member (16 ga, 54 mil): A1003 structural, G60. | **APPLY** | product only: G60 on 11 LF; qty 0 |
| 28 | Metal stud blocking at wall-mounted items (notes) | 09 22 16 3.1.C; 05 40 00 3.3.H; G004 "solid backing for grab bars"; A103 | Supplementary framing / blocking for fixtures, grab bars, toilet accessories required. A103 governs backing type (metal track / strap loaded, FRT wood excluded by rule). R-ALC-02 applied. | **CONSISTENT** | 0 |
| 29 | METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead | 09 29 00 2.6.A.1-2 (ASTM C1047, galv. steel; 2.6.A.2.g "Curved-Edge Cornerbead: with notched or flexible flanges") | Galvanized C1047 cornerbead = spec. The 62.2 LF at the bottom of the curved reception soffit (A-A421.A-1, 16/A502) must be curved-edge (flexible-flange) cornerbead. | **APPLY** | product split: 62.2 LF of 441.22 LF -> curved-edge cornerbead; qty 0 |
| 30 | METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - gypsum edge trim | 09 29 00 2.6.A.2.d (L-Bead), 3.1.C (edge trim at structural abutments) | L-bead where board stops short of deck / at slip heads, and head F metal edge, match the spec shapes. Plan "J-METAL EDGE TRIM" (head A/A301) belongs to an unused head detail (no type calls head A). | **CONSISTENT** | 0 |
| 31 | 5/8" cement backer units behind tile (A301 type notes; spec 09 29 00 2.5) | 09 29 00 2.5 (ANSI A118.9, C1288/C1325, 5/8", D3273 score 10); 09 30 13 2.5.A (C1325 Type A, 5/8"); 06 16 00 2.4.C | Product and thickness match (RFI-06 decision). Mold-resistance score 10 limits brands (Custom / GP / USG listed in 09 30 13 2.5.A). Joint treatment of the backer has no row (see NO-ROW N1). | **CONSISTENT** | 0 |
| 32 | Control joint, gypsum board walls (ASTM C840, 30 ft max) | 09 29 00 2.6.A.2.f (interior expansion/control joint, C1047); A010 note 27; RCP note 6 | Spec gives the product but no spacing. Plan note 27 (30 ft) governs walls. Ceiling joints "as indicated in specifications": spec silent -> ASTM C840 (applied in row). | **CONSISTENT** | 0 |
| 33 | Hanger wire 12 ga - hanger count (one per hanger, height per room) | see Hanger wire row | Same issue as hanger wire LF -> RFI-S02. | **CONFLICT** | RFI-S02: 187 hangers, gauge only |
| 34 | Additional head track at openings over 4'-0" wide | 09 22 16 3.2.D.2-3 (track section at head for cripples; 2 studs per jamb, jamb studs to structure) | Canon counts 4 jamb studs per opening (2 each side) at full height, matching 3.2.D.2.a-b. The head track for cripples is covered by the bottom track not deducted at the 18 openings (~84.7 LF of R.O.). Headers are steel by others (RFI-12). | **CONSISTENT** | 0 |
| 35 | Stud reinforcement at MEP penetrations | 05 40 00 3.2.H; 09 22 16 3.2.D | Hole-reinforcing plates only for oversize web cuts. Duct openings EXCLUDED (R-ALC-03). | **CONSISTENT** | 0 |
| 36 | Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its type) | - | Not applicable (no ATM). | **CONSISTENT** | 0 |
| 37 | 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | - (08 33 30 present, no grille on plans) | Not applicable. | **CONSISTENT** | 0 |
| 38 | Gypsum board jamb return at openings | 09 29 00 3.1 | Estimator decision (0 SF); spec adds nothing. | **CONSISTENT** | 0 |
| 39 | PVC trim - edge trim molding and inside corner molding at the FRP | - | FRP = other trade (excluded). | **CONSISTENT** | 0 |
| 40 | Power-driven fasteners and duct sleeves | 09 22 16 3.2.E.2; 05 40 00 2.8.D | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 41 | Access panel 24"x24" | 01 10 00 1.8.D.9 (refers to 08 31 00, not in this sweep) | Plan-printed (A131 A4.10); no 09 2x requirement. | **CONSISTENT** | 0 |
| 42 | Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | 09 29 00 2.8.B (C1002 / C954) | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 43 | Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | 09 22 16 2.4.A.1 | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 44 | Power-driven fasteners, slab pins for the bottom track | 09 22 16 2.4.A.1; 05 40 00 2.8.D | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 45 | Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | 05 40 00 2.8.C; 09 22 16 2.3.B | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 46 | Joint compound, all purpose | 09 29 00 2.7.C.1-4 (setting-type taping compound for prefill / embedding / first coat; setting-type sandable topping for fill and finish coats), 3.1.G.1-3 (Level 1 at plenum / concealed areas, Level 2 tile substrate, Level 4 exposed) | Spec requires SETTING-TYPE compounds for every coat, so an all-purpose ready-mix product does not comply. Finish levels by area also cut the quantity: board above ceilings / concealed = Level 1 (tape embedded, no fill/finish coats). The Excel applies one Level-4 yield (0.072 lb/SF) to all 65,388.8 SF. | **APPLY** | Product: all-purpose -> setting-type (taping + sandable topping), 4,708 lb max (weight basis to re-check with supplier yield). Qty: Level 1 share est. 40-55% of board -> -1,256 to -1,726 lb (0.072 x 2/3 x share x 65,388.8) |
| 47 | Joint tape, paper | 09 29 00 2.7.B.1-2 | Paper tape for interior board = spec. Tile-backer joints need different tape (NO-ROW N1). | **CONSISTENT** | 0 |
| 48 | Level 5 finish | 09 29 00 3.1.G.4 ("where indicated"); A610 P-17 | P-17 (Level 5) is applied to no surface -> 0 = spec. | **CONSISTENT** | 0 |
| 49 | Deflection clips at non-load-bearing walls to structure | 05 40 00 2.6.C-F, 3.5.D (track OR clips options); 09 22 16 2.2.C | Plan draws 2" slip track. Clips are only an alternative. | **CONSISTENT** | 0 |
| 50 | Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | 05 40 00 2.8.E | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |
| 51 | Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | 09 29 00 2.8.B.1 (C954) | Row EXCLUDED by estimator standing rule 2026-10-31 (all fasteners = 0, no RFI); spec lists it, no change. | **CONSISTENT** | 0 |

## APPLY items (spec coexists with plan and changes product or quantity)

- **Bottom track 6" - 600T250-54**: 05 40 00 2.3.B, 2.6.B; S200 C. Delta: product only: specify G60 / A1003 structural on 22.41 LF; qty 0.
- **Top track 6" - standard (walls not reaching structure) - 600T250-54**: 05 40 00 2.3.B, 2.6.B; S200 C. Delta: product only: G60 / A1003 on 22.41 LF; qty 0.
- **6" metal stud (LF of material) - 600S162-33**: 05 40 00 2.3.B, 2.4-2.6; 2/A131. Delta: product only: G60 / A1003 on 432 LF; qty 0.
- **Bracing 1-1/2" C.R. channel**: 09 22 16 2.2.F (0.053", 1/2" flanges), 2.2.C.1 ("continuous bridging located within 12 inches of the top of studs"); 05 40 00 3.5.E-F. Delta: +910.70 LF net (409.44 + 397.30 + 103.96 slip-track LF); +1,047.31 LF purchase = +66 sticks 16 ft (388 -> 453). Alt.: proprietary deflection track (2.2.C.2) on 910.70 LF instead, 0 LF bracing.
- **5/8" gypsum board, Type X**: 09 29 00 2.3.A, 2.3.B (flexible board "to bend to fit radii"), 3.1.B (ASTM C840); 16/A502 reception arc. Delta: -673.63 SF Type X (-714 SF purch., ~-15 sh 4x12); +1,347.26 SF 1/4" flexible (2 layers; +1,428 SF purch., ~45 sh 4x8). Conditional on actual radius.
- **Deep-leg slotted deflection track - printed product (see Where it comes from)**: 05 40 00 2.6.D; 09 22 16 2.2.C.2; 1/A506. Delta: product only: G60 on 11 LF; qty 0.
- **METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead**: 09 29 00 2.6.A.1-2 (ASTM C1047, galv. steel; 2.6.A.2.g "Curved-Edge Cornerbead: with notched or flexible flanges"). Delta: product split: 62.2 LF of 441.22 LF -> curved-edge cornerbead; qty 0.
- **Joint compound, all purpose**: 09 29 00 2.7.C.1-4 (setting-type taping compound for prefill / embedding / first coat; setting-type sandable topping for fill and finish coats), 3.1.G.1-3 (Level 1 at plenum / concealed areas, Level 2 tile substrate, Level 4 exposed). Delta: Product: all-purpose -> setting-type (taping + sandable topping), 4,708 lb max (weight basis to re-check with supplier yield). Qty: Level 1 share est. 40-55% of board -> -1,256 to -1,726 lb (0.072 x 2/3 x share x 65,388.8).

## CONFLICT items (see RFI_SPECS.md)

- **6" metal stud (LF of material) - per source**: RFI-S01: 388.11 LF 25 ga -> 20 ga (A) or no change (B, L/120).
- **3-5/8" metal stud (LF of material)**: RFI-S01 A: 7,115.29 LF -> 362S162-54 @ 12" o.c. (+2,371.6 LF net) + 259.56 LF -> 20 ga; B: 7,115.29 LF -> 362S162-43 @ 16", 0 LF.
- **Hanger wire**: RFI-S02: 0 LF; product 12 ga vs 0.16" on 2,428.49 LF.
- **Hanger wire 12 ga - hanger count (one per hanger, height per room)**: RFI-S02: 187 hangers, gauge only.

## Spec items in our trade with NO row in the Excel

| ID | Item | Spec § | Finding | Delta |
|---|---|---|---|---|
| N1 | Alkali-resistant glass-fiber mesh tape (2") at cement backer joints | 09 29 00 2.7.B.4, 2.7.E.2, 3.1.I; 09 30 13 3.3.K (ANSI A108.11) | Backer units are ours (RFI-06) and their joints must be treated per the manufacturer (AR mesh + thinset). There is no row: tape row covers 65,388.8 SF of gypsum only. | +447.6 LF net (1,209.77 SF x 0.37 LF/SF) / +474.5 LF purchase (6%) = 4 rolls 150 ft |
| N2 | 1/4" flexible gypsum board, 2 layers, curved reception soffit side | 09 29 00 2.3.B; 16/A502 | See Type X row (APPLY). New product row needed if the radius is under the 5/8" bend limit. | +1,347.26 SF net (+1,428 SF purch.) with -673.63 SF 5/8" Type X |
| N3 | Armstrong DW90CAG 90-degree drywall clip and SB12P drywall support hanger | 09 51 23 2.6 schedule | Listed in the product schedule with the four loaded grid items. Plans show no grid-formed vertical transitions (soffits are stud-framed per A502), so no count is printed. | TBD - allowance; 0 if field confirms no grid-formed 90-degree transitions |
| N4 | Foam-gasket / felt isolation strip where studs bear on exterior masonry or dissimilar metals | 09 22 16 2.4.B, 3.2.B | B2E: Z-girt + rigid insulation separate studs from CMU (n/a). C3D furring "at existing storefront" (A-A422-6, A-A431-1/-2, 34.20 LF) is against aluminum storefront at the exterior wall if in contact (verify). | 0 to +68.40 LF (top + bottom track contact line of 34.20 LF); up to 684.9 LF if every stud bears |
| N5 | Sealer gasket (1/4" closed-cell) under 05 40 00 bottom track on slab | 05 40 00 2.9.E, 3.1.D | Applies to 05 40 00 framing: the D6F 600T250-54 bottom track (S200 C). More if RFI-S01 option A moves type-A walls to 05 40 00. | +22.41 LF (+269.76 LF more under RFI-S01 A) |
| N6 | Galvanizing repair paint | 05 40 00 2.9.A, 3.8.A | Touch-up of cut / welded G60 members. | allowance (1 can) |
| N7 | Tie wire 0.062" (CRC bracing / furring ties) | 09 22 16 2.2.F.3, 2.3.A, 3.3.D | Consumable for wire-tied C.R. channel. Not a fastener, so it is not covered by the exclusion. | allowance (~1 coil per 2,000 LF CRC) |
| N8 | Temporary dust / noise-control partitions | 01 35 16 1.5.A.1, 3.1.A.5/8; 01 10 00 1.5 (full Owner occupancy) | Required by Div. 01 for alteration work. Normally GC general conditions, and none are drawn. | TBD (not loaded; confirm GC carries it) |
| N9 | Texture finishes (polystyrene / orange peel) | 09 29 00 1.1.A.4, 2.9, 3.2 | Section includes texture, but no texture is indicated on any sheet (A610/A611, RCP). | 0 (N/A) |
| N10 | Firestop track | 09 22 16 2.2.D, 3.2.D.4.a ("where indicated") | Not indicated. X6D head uses a continuous C track (X/A301); head-of-wall firestop = 07 84 00 (not in manual, other trade). | 0 |
| N11 | Steam-room integrated mockups (~50 SF each) built under 09 29 00 | 09 30 13 1.5.A.1 | No steam room on A101/A121 room names (A504 3 not called; A610 P-18 refers to CMU walls). | 0 (N/A) |
| N12 | Sound-attenuation blankets; acoustical sealant; Z-furring; thermal insulation | 09 29 00 2.8.C-D, 3.1.C; 09 51 23 3.2.B.1; 09 22 16 2.2.G, 3.2.F; 07 21 00 | Excluded trades / items per standing rules (insulation, acoustical sealant) and RFI-34 (Z-girt). Noted only. | 0 (EXCLUDED) |
| N13 | Fasteners (drywall / framing screws, PAF, anchors, hanger attachments) | 09 22 16 2.3.B, 2.4.A.1; 09 29 00 2.8.B; 05 40 00 2.8.B-E; 06 16 00 2.7 | Spec lists them; estimator standing rule 2026-10-31 keeps ALL fasteners EXCLUDED. | 0 (EXCLUDED) |

## Div. 01 scope items

| Spec § | Item | Finding | Class | Delta |
|---|---|---|---|---|
| 01 10 00 1.3 / 1.5 / 1.6 | Single prime contract; full Owner occupancy; work hours 6:00a-8:00p M-F; no phasing text beyond the 1.1 heading. | No material quantity effect (labor/schedule only). | CONSISTENT | 0 |
| 01 10 00 1.8 | Delegated design limited to fire sprinklers, pool, 03 10 00 formwork. CFMF is not delegated (05 40 00 requires shop drawings 1.2.B only). 09 51 23 1.3.B/2.1.A delegated seismic for ceilings: SDC B (S100) and A502 note -> no seismic bracing. | Supports RFI-S01: the member choice is not covered by a delegated engineer, so the estimator must price it. | CONSISTENT | 0 |
| 01 25 00 / 01 60 00 2.x | 09 22 16 ClarkDietrich = non-limited list (any C645 product certified per 1.4.A). 09 51 23 Armstrong = National Account / sole manufacturer. No substitution for convenience. | Excel rows already Armstrong; Inputs/RFI-33 text says USG (label only). | CONSISTENT | 0 |
| 01 35 16 1.2.G-H, 3.1.B.1 | Definitions Repair vs Replace; "do not remove existing materials unless otherwise indicated". | Existing-wall faces: estimator standing decision 2026-11-02 (full face replacement where AD101 D0.07 / D0.52) stands; spec does not contradict it (removal is indicated by keynote). Demolition = our scope per R-ALC-04. | CONSISTENT | 0 |
| Alternates / owner-furnished / work by others | No 01 23 00 Alternates section in the manual; G001 lists "ALT" only as an abbreviation. G002 responsibility schedule: owner/vendor items with "CONTRACTOR TO PROVIDE BLOCKING AS REQUIRED" (covered by A103 blocking row). Sauna C-6 cedar by vendor. | No alternate to price. | CONSISTENT | 0 |
| 01 35 16 1.5.A.1 | Temporary dust/noise partitions (see N8). | Not loaded; GC general conditions. | CONSISTENT | TBD |

## Method notes

- Limiting heights (RFI-S01) are computed in `/tmp/chuze/scratch/SPECS/lh.py`, `lh2.py` and `lh3.py` (gross Ix, E = 29,500 ksi, 5 psf from S100, 16" o.c.). These are upper bounds, so verify against ClarkDietrich / SSMA tables before pricing.
- The bracing APPLY assumes the current rule (ROUNDUP(H x 12/48) - 1 rows), which leaves no row within 12" of the head on any 22.83 ft slip-track wall.
- No deliverable was modified.
