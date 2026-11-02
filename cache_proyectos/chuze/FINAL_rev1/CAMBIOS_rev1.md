# CAMBIOS rev1 — Chuze Fitness Austin Bluffs take-off (rev0 -> rev1, 2026-11-01)

Source of the gaps: 7_cobertura/CERTIFICADO_PASO12.md + MATRIZ_COBERTURA.xlsx (GAP-01..12, BE tests), 6_auditoria/COMPARATIVA_AUDITORIA.md, decisions 7_cobertura/DECISIONES_ORQUESTADOR.md. Measured wall LF unchanged (1,006.72 partitions + 220.24 soffit sides). Quantities from canon.py over the canon additions (misc / trim / blocking items with N/SHEET and operation); deltas read from familias_out.json rev0 vs rev1.

| Gap / finding | Change | N/SHEET | Quantity delta |
|---|---|---|---|
| GAP-01 control joints > 30 ft | Own row 'Control joint': ROUNDUP(L/30)-1 joints x length-weighted board height of each face, every wall / soffit side over 30 ft (8 partitions + 2 soffit sides) | A010 GN 27; elevation GN 5; A121 RCP GN 6; 27/A101 | control joint LF 0.00 -> 363.93 (+363.93) |
| GAP-02 A103 metal backing | 6 x 16 ga continuous track per A103 key (runs measured on the plans: keys 8, 33, 41, 45, 50, 51, 52; assumed 10 ft / 5.67 ft runs for the not-drawn tags 8, 18, 33, 48 - RFI-13); metal strap 4 ft per tag (keys 7, 9, 16); 10/A505.B 2 horizontal studs x 2 ft. 12/13 A505.B = plywood blocking (wood, EXCLUDED). Texts RFI-13 / RFI-28 / ALC-16 made consistent | A103 schedule + plan tags; 10/A505.B | metal blocking LF 0.00 -> 225.31 (+225.31) |
| GAP-03 tile backer | 5/8" cement backer board on every printed tile zone (tile top + 6", capped at the face height); cement board screws 1.2 / SF; gypsum not deducted (RFI-06 delta) | F/A301 + A301 type notes; spec 09 29 00 2.5; A421.B / A421.C / A424.C / A425.B; A111 GN 6 | cement board SF 0.00 -> 1,209.77 (+1,209.77); screws 0.00 -> 1,451.72 (+1,451.72) |
| GAP-04 RTU curb caps | 9 caps x (20 LF perimeter + 7 members @ 12" x 4 ft) of 600S162-33 + (2) #10 TEK @ 6" + member ends; curb 4'-0" x 6'-0" assumed (RFI-14) | 2/A131; AD103 D0.18 | 6" stud +432.00 LF; #10 TEK +972 |
| GAP-05 A502 box headers | MTL STUD BOX HEADER: 2 x 6" 20 ga stud + 1 track per LF of the soffit sides of 6, 7, 13, 15/A502 (117.1 LF) | 6, 7, 13, 15/A502 | 6" stud +234.20 LF; ceiling / soffit track +117.10 LF |
| GAP-06 diagonal bracing | 3 braces per locker-entry soffit x 2.83 ft (diagonal of the 2'-0" box, not dimensioned - RFI-35) | 6/A502 | 6" stud +16.96 LF |
| GAP-07 Z-girt B2E | EXCLUDED + RFI-34 (cladding / insulation substrate furring), Scope Checklist ALC-X45 | B/A301; spec 09 22 16 2.2.G / 3.2.F | 0 (delta ~1,370 LF in RFI-34) |
| GAP-08 head F metal edge | Metal edge both top edges (2 x LF) + 5/8" type X cap over the D6F wall tops | F/A301 | edge trim +44.82 LF; type X +11.13 SF |
| GAP-09 head C wall bracing | Kickers of the wall stud @ 48" O.C. at 45 deg to the deck on every head-C wall at the ceiling (returns braced with their wall) - RFI-36 | C/A301; spec 05 40 00 3.5.G | 3-5/8" stud +380.74 LF; 6" stud +43.49 LF |
| GAP-10 edge trim | L-bead along the top of every board face finished to the B.O. deck (exposed structure) | spec 09 29 00 3.1.C / 2.6 | edge trim +1,290.95 LF |
| GAP-11 A-A435-1 Retail Storage | Retail Storage 126 segment (5.91 ft) studs to deck (6 studs x 12.33 ft) + 3 extra bracing rows; board unchanged (finish to deck per elevation 7) | A435.A elev 7; A435 RCP | 3-5/8" stud +73.98 LF; C.R. channel +17.73 LF |
| GAP-12 1/A506 hatch wall + '13/A506' | 16 ga x 4" deep-leg track around the 2'-6" x 3'-0" hatch (11 LF) + 16 ga top runner tracks 2 x 5'-0" (10 LF); RFI-37 on the orphan citation | 1/A506; A423 keynote A2.163 | deep-leg track +11.00 LF; ceiling / soffit track +10.00 LF |
| Auditor #4 corner bead | Corner bead at the 5 C3C boxes (2 exposed corners x board height) and the 2 cased openings (jambs both faces + head) | C3C/A301; A421 / A423 / A426; A429; RFI-29 | corner bead +247.32 LF |
| Auditor #5 MR soffit faces | Men's Locker 128 soffit faces A-A424.A-2 / -3 from type X to MR | 3/A111 (A111 GN 3) | MR SF 5,402.49 -> 5,483.88 (+81.39); type X 30,526.94 -> 30,456.68 (-70.26) (incl. +11.13 head F cap) |
| Auditor #6 / BE-12 grid molding | One perimeter molding (KAM151220E angle) per spec 09 51 23; channel molding row removed; rows named with the Armstrong products of the spec (HD8906, XL8945P, KAM151220E) | A121 C-5; spec 09 51 23 | channel molding 458.91 -> 0.00 (-458.91); angle molding 458.91 -> 458.91 (+0.00) |
| BE-12 RFI-05 citation | 'spec 09 29 00 2.3.F' (does not exist) -> 2.3.E (mold-resistant gypsum board) | spec 09 29 00 2.3 | text |
| Auditor #7 / #8 / #9, BE-44 Bluebeam | RCP pages A421.A-A425.A calibrated 1/4" = 1'-0" (18 pt/ft); A-A421.A-1 drawn as the arc (49-point polyline); C3C boxes drawn on their 3 loaded sides | A421.A-A425.A view titles | Bluebeam Length: soffit sides 480.00 -> 220.21 LF (Excel 220.24); C3C 36.98 -> 24.36 LF (Excel 24.54) |
| BE-48 PDF metadata | Markups PDF keywords / creator emptied (tool R80w.26) | - | text |
| BE-40 rows without sheet | Every Material Summary row cites a sheet: 2-1/2" stud with its per-wall breakdown (B2E/A301), grid / hanger rows cite C-5/A121, zero rows cite the none reason with its sheet (tools R80w.22 / R80w.28 / R80w.29) | B2E/A301; C-5/A121 | 2-1/2" stud 2,009.04 -> 2,009.04 (+0.00) (unchanged, now traced) |
| BE-41 / BE-55 internal tokens | Pending Items / Scope Checklist without process tokens (stage / resolution ids, tool names, rule ids) | - | text |
| BE-13 plywood backboards | E111 / E112 / E401 8' x 4' x 3/4" plywood backboards = EXCLUDED (wood, Div. 06), Scope Checklist ALC-X44 | E111, E112, E401 | 0 |
| BE-47 text vs rows | RFI-06 / RFI-13 / RFI-14 / RFI-28 'LOADED' texts now match the loaded rows; ALC-08 no longer claims impact board (RFI-25 not loaded); ALC-18 points to its own control-joint row | - | text |

## Family totals rev0 -> rev1 (NET)

| Family | rev0 | rev1 | delta |
|---|---|---|---|
| #10 framing screws (printed) | 176.00 | 1,148.00 | +972.00 |
| 3-5/8" stud (todos los gauges) | 10,090.37 | 10,545.09 | +454.72 |
| 5/8" gyp MOISTURE RESISTANT | 5,402.49 | 5,483.88 | +81.39 |
| 5/8" gyp board Type X | 30,526.94 | 30,456.68 | -70.26 |
| 6" stud (todos los gauges) | 10,952.22 | 11,678.87 | +726.65 |
| USG channel molding (DGCM27) | 458.91 | 0.00 | -458.91 |
| bracing C.R. channel | 5,372.66 | 5,390.39 | +17.73 |
| cement board | 0.00 | 1,209.77 | +1,209.77 |
| cement board screws | 0.00 | 1,451.72 | +1,451.72 |
| control joint | 0.00 | 363.93 | +363.93 |
| deep-leg slotted deflection track (printed) | 0.00 | 11.00 | +11.00 |
| drywall screws | 44,885.34 | 44,898.70 | +13.36 |
| framing screws | 4,916.00 | 4,940.00 | +24.00 |
| joint compound | 2,693.12 | 2,693.92 | +0.80 |
| joint tape | 13,839.65 | 13,843.76 | +4.11 |
| metal stud blocking (362CR / STUD BLOCKING) | 0.00 | 225.31 | +225.31 |
| metal trim (corner bead, casing, shadow molding) | 193.90 | 1,776.99 | +1,583.09 |
| track de ceilings / soffits | 440.48 | 567.58 | +127.10 |
