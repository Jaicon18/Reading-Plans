# CAMBIOS rev2 — Chuze Fitness Austin Bluffs take-off (rev1 -> rev2, 2026-11-01)

Source: 6_auditoria/CERTIFICADO_AUDITORIA_rev1.md, COMPARATIVA_AUDITORIA_rev1.md; 7_cobertura/CERTIFICADO_PASO12_rev1.md (BE-44, BE-46, BE-55, BE-108). Wall LF unchanged. Deltas read from the Material Summary of the two Excels.

| Finding | Change | N/SHEET | Quantity delta |
|---|---|---|---|
| BE-46 / R80e.95 top track | Top track split per stud size into 2" slip / deflection track (heads D / E to the deck) and standard top track (heads C / F / G, walls not reaching structure), each with its per-wall breakdown and head-detail N/SHEET (tool R80w.31) | D/A301, E/A301, C/A301, F/A301, G/A301 | 3-5/8": 531.68 = slip 240.96 + standard 290.72; 6": 469.13 = slip 393.29 + standard 75.84 (incl. 600T250-54 22.41); 2-1/2": 103.96 slip; family total unchanged 1,104.77 LF |
| BE-55 / check 6 internal tokens | Breakdown items renamed in plain English (e.g. 'box header 13/A502 A-A423.A-1 studs', 'head C kickers A-A421-15'); OTHER FRAMING rows 'Soffit side (16/A502)'; no 'skill' wording (tools R80w.32 / R80w.33); MEP diagnostics and the ATM search text rewritten as plan citations | - | text (0 tokens left in the visible sheets) |
| Phantom wall A-A435-4 | Team Lounge 125 cabinet backing (A103 keys 51 / 52, 2 x 8.75 ft x 2 rows) re-attached to the owner wall A-A426-4 (A-A435-4 was removed as the double count of that wall); blocking row cites the A103 WALL BACKING SCHEDULE keys (8/A103 ... 52/A103) + 10/A505.B | 51/A103, 52/A103; A435; resolution of the double count (A426 owner) | 0 LF (same 35.0 LF, new host) |
| Edge-trim citation | L-bead items cite the head detail of each wall (D/A301, E/A301, C/A301) and spec 09 29 00 3.1.C; keynote A2.23 no longer cited | D/A301, E/A301, C/A301; spec 09 29 00 3.1.C | text |
| BE-108 MEP crossings | Duct crossings counted on M110 over the full-height walls (M110 registered to A101 by grid bubbles 1-7 / A-G, offset 6.9 / 36.7 pt; each crossing located with mep.cruces and checked on a crop, img_mep/): A-A427-2 31", A-A424-1 41", A-A424-2 29", A-A424-3 10", A-A424-9 10", A-A425-2 6" -> plates MAX(1, ROUNDUP(w/16)) = 2+3+2+1+1+1 = 10 and 1 duct sleeve each = 6. Unconfirmed candidates (A-A421-10, A-A422-2, A-A422-3, A-A435-2, A-A435-3 x2) and pipe sizes stay in the RFI as a range (+0 to +6 plates; +1 per pipe over 1") | M110, P110, P111, A101 | stud reinforcement 0 -> 10 PCS; duct sleeves 0 -> 6 PCS |
| BE-44 C3C pilasters | A-A426-2 / -3 markups drawn on the printed faces 10" + 3'-0" + 10" (print wins over vector): Bluebeam Length 4.67 each | A426 printed dims; C3C/A301 | Bluebeam C3C 24.36 -> 24.54 LF (= Excel) |
| Curved perimeter molding | SC151220EQ curved molding on the 62.2 LF reception arc (spec 09 51 23), straight KAM151220E on the rest (tool R80w.35) | spec 09 51 23; A421.A | KAM 458.91 -> 396.71 LF; SC151220EQ 0 -> 62.20 LF |
| Framing screws for new studs | Box-header (2 pieces per 20 ft of header), kicker and brace studs enter the 4-per-piece driver (tool R80w.34) | 6, 7, 13, 15/A502; C/A301; 6/A502 | framing screws 4,940 -> 5,140 (+200 = 50 pieces x 4) |
| Hidden _reglas sheet | Kept: it is the plantilla's seal (the reference project has it) | - | - |

## Material Summary rows rev1 -> rev2 (NET)

| Row | Unit | rev1 | rev2 |
|---|---|---|---|
| Top / deflection track 3-5/8" | LF | 531.68 | - |
| Top / deflection track 6" - per source | LF | 446.72 | - |
| Top / deflection track 6" - 600T250-54 | LF | 22.41 | - |
| Top / deflection track 2-1/2" | LF | 103.96 | - |
| Armstrong KAM151220E knurled angle molding at the C-5 perimeter (spec 09 51 23) | LF | 458.91 | 396.71 |
| Stud reinforcement at MEP penetrations | PCS | 0 | 10 |
| Power-driven fasteners and duct sleeves | PCS | 0 | 6 |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 4940 | 5140 |
| Top track 3-5/8" - standard (walls not reaching structure) | LF | - | 290.72 |
| Top slip / deflection track 6" (2" deflection leg, walls to structure) | LF | - | 393.29 |
| Top track 6" - standard (walls not reaching structure) - per source | LF | - | 53.43 |
| Top track 6" - standard (walls not reaching structure) - 600T250-54 | LF | - | 22.41 |
| Top slip / deflection track 3-5/8" (2" deflection leg, walls to structure) | LF | - | 240.96 |
| Top slip / deflection track 2-1/2" (2" deflection leg, walls to structure) | LF | - | 103.96 |
| Armstrong SC151220EQ curved perimeter molding at the reception circle (spec 09 51 23) | LF | - | 62.2 |
