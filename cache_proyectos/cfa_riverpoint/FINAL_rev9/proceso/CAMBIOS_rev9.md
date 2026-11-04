# CAMBIOS rev9 - CFA #2284 River Point (coordination audit of rev8, U-138, 4-nov)

Excel produced by plantilla_excel.py armar (skill v81cf38 = v81cf37 + BE-CF24) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon (scripts/correcciones_rev9.py). rev1-rev8 files untouched.

| # | Item | rev8 | rev9 | Delta | N/SHEET | Rule / decision |
|---|---|---|---|---|---|---|
| 1 | W6-09-OUT-1 cement board base (corridor / service faces of the office W6) | 1.0 ft (G.3/A-202) | 1.25 ft (C3/A-604, same as W6-09-OUT-2) | +2.05 SF 1/2" cement board | C3/A-604 | RFI-23 / one source per wall |
| 2 | Board-only Source height text | old height text kept in the Source of rows changed in rev6 / rev7 (e.g. G.3 1'-0" [CONFIRMED] on 1.25 ft rows; 6.708 / 2.625 on the restroom rows) | height part of the Source = the entry's current height_source (one source, one number) | 0 | 40 rows | #0 / U-114 |
| 3 | RFI-27 drive-thru furr down | loaded 11.011 LF x (2.833 + 2.0 assumed) + framing (rev8) | not a furr down: RCP A-221 / A-202 / C1/A-603 show the 7'-8" line as the wall finish datum | -53.22 SF 1/2" cement board, -69.14 LF 3-5/8" stud, -33.03 LF track, -11.011 LF corner bead (vs rev8) | A-221, A-202, C1/A-603, A-501 | U-132: the plan resolves it; RFI-27 keeps the alternative |
| 4 | Review Item 5 DEMO-C6 (PENDING without RFI) | Review Item only | RFI-28 open, 38.35 SF loaded (conservative) | 0 | A-052 KN10 | U-042 / U-048 (CE_RFI_FORMATO) |
| 5 | Review Item 6 mop chase cement board height | [PENDING] | RESOLVED from drawings (E3/A-604 + A-601 / A-602 S-1 to the ceiling, G.7/A-202) | 0 | E3/A-604 | U-132 |

## Material Summary NET rev8 -> rev9

| Row | Unit | rev8 | rev9 | Delta |
|---|---|---|---|---|
| 3-5/8" metal stud (LF of material) - per source | LF | 335.47 | 266.33 | -69.14 |
| Ceiling / soffit track (size per source, see Where it comes from) - 362T125-33 track (as C4/A-624) | LF | 33.03 | - | -33.03 |
| Alkali-resistant glass-fiber mesh tape at cement backer board joints - printed product (see Where it comes from) | LF | 769.32 | 750.39 | -18.93 |
| Setting-type joint compound at cement board joints - printed product (see Where it comes from) | LB | 149.71 | 146.02 | -3.69 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead at the furr down outside corner (C4/A-624) | LF | 11.01 | - | -11.01 |
| 1/2" cement board / cementitious backer | SF | 2079.25 | 2028.09 | -51.16 |
