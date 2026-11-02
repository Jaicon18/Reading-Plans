# CAMBIOS rev3 - CFA #2284 River Point (back-check of rev2: 6 defects)

Excel produced by plantilla_excel.py armar (skill v81cf8 = v81cf7 + tool fixes T1-T6, tools/CAMBIOS_tools_v81cf8.md) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon. rev1 / rev2 files untouched.

| # | Item | rev2 | rev3 | Delta | N/SHEET | Rule / decision |
|---|---|---|---|---|---|---|
| 1 | Ceiling board row (332.06 SF) | label '5/8" gypsum board, regular' + product note | row '5/8" gypsum ceiling board, SAG-RESISTANT (ceiling type)' | 0 SF (label / family) | C09250 2.1.E + 3.2.A.3 / A-909 | T2 (tool: board key 5/8 ceiling sag-resistant) |
| 2 | Z-furring row label (96 LF) | '1-1/2" Z-furring channel' + product note | '2" Z-furring channel (LF of material)' | 0 LF (label) | A-202 M2.1, A1/A-605 | T1 (tool: printed Z size) |
| 3 | J trim at play area wall base (A2/A-624) | 59.69 LF (play-room perimeter) | 30.794 LF (dining face, EX-DIN-03) | -28.9 LF | A2/A-624, A1/A-624, A-202 | P1 |
| 4 | MR rows spec citation (EX-RRM-01-GB, EX-RRW-01-GB) | C09250 §2.1.B (1/2 in standard interior) | C09250 §2.2.A water-resistant backing board | text | C09250 / A-909 | P2 |
| 5 | Spec reference on Material Summary rows (bracing, clips, trim, blocking, tracks, Level 5, mesh / setting compound) | missing on rows 17 / 22 / 27 | every row cites its spec section | text | C09111 / C09250 / A-909 | P2 |
| 6 | Setting-type compound at cement board joints | note only (not bought) | own LB row (family setting-type joint compound at cement board, waste none) | +129.62 lb in Net / Purchase | C09250 2.4.D.2 / 3.5.E (A-909) | T3 |
| 7 | Mesh tape waste | 6 % (purchase 706.07 LF) | 0 % yield row (purchase 666.10 LF) | -39.97 LF purchase | Inputs C23 / C24 | T4 |
| 8 | OTHER FRAMING block | no subtotal | SUBTOTAL OTHER FRAMING row (LF + board SF) | format | - | T5 |
| 9 | Workbook sheets | 7 (hidden _reglas seal) | 6 fixed sheets; seal in <excel>.sello.json next to the work Excel | format | - | T6 |
| 10 | Scope Checklist ALC-04 | MB-01 3-5/8"; 'no deflection track printed' | MB-01 6" (D3/A-624); C1/S-801 slotted track loaded; strongback own row | text | D3/A-624, C1/S-801 | P2 |
| 11 | Marked A-221 image | soffit sides only | gyp ceilings, soffit bottoms, Level 5, hatch shaft drawn with their take-off labels | image | A-221 | P3 |

## Material Summary NET rev2 -> rev3

| Row | Unit | rev2 | rev3 | Delta |
|---|---|---|---|---|
| 1-1/2" Z-furring channel (LF of material) | LF | 96 | - | -96.0 |
| 5/8" gypsum board, regular | SF | 332.06 | - | -332.06 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - J trim at top of cement board base (A2/A-624) | LF | 59.69 | 30.79 | -28.9 |
| 2" Z-furring channel (LF of material) | LF | - | 96 | +96.0 |
| 5/8" gypsum ceiling board, SAG-RESISTANT (ceiling type) | SF | - | 332.06 | +332.06 |
| Setting-type joint compound at cement board joints - printed product (see Where it comes from) | LB | - | 129.62 | +129.62 |
