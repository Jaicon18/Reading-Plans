"""Grand Kia: etapas/4_canon/alcance_notas.json = notas del Scope Checklist (24 ALC de alcances.py + exclusiones), cada una
con su N/HOJA o regla del usuario. Cantidades: solo las del canon / familias (se leen de familias_out.json)."""
import json, os
W = '/root/gk/work'
fo = json.load(open(f'{W}/etapas/4_canon/out/familias_out.json'))['familias']
EXT = json.load(open(f'{W}/etapas/2_lectura/A/EXTERIOR.json')) if os.path.exists(f'{W}/etapas/2_lectura/A/EXTERIOR.json') else None
q = lambda k: round(float(fo.get(k) or 0), 1)
EXC = "EXCLUDED - not in scope (estimator standing order, no RFI): "
ext_ok = bool(EXT and EXT.get('elements'))
alc = [
 ("ALC-01", "CUANTIFICADO", "Partition types A/A1 (3-5/8\" full height), B/B1 (3-5/8\" partial height), C/C1 (6\" full height), D/D1 (6\" partial), E/E1 (8\" full height, gyp bd ceiling height one side), F/F1 (2-1/2\" furring), G (3-5/8\" furring), H/H1 (6\" furring), all @16\" o.c. per A550 keynotes 5/8/12/13; gauge not printed for partitions (RFI-01, 20 ga / 33 mil loaded per S403 362S162-33)."),
 ("ALC-02", "CUANTIFICADO" if ext_ok else "RFI", "Exterior non-load-bearing CFS framing is in 05 40 00 (1.1.A.2): carried from the exterior reading (A310-A312 wall sections, S401-S403 CFS details); see rows of exterior framing / sheathing." if ext_ok else "Exterior CFS framing per 05 40 00 1.1.A.2: pending exterior reading."),
 ("ALC-03", "CUANTIFICADO" if ext_ok else "RFI", "Parapet framing taken from what the set prints: wall sections A310-A312, building sections A300-A301 and S121 / S122 / S403 (CFS parapet / band studs EXT-01..EXT-05); the parapet / roof-edge detail sheet cited by the sections is NOT in the set (see README 'Missing sheet'), no quantity depends on it alone."),
 ("ALC-04", "CUANTIFICADO", "Bottom track 10/A540 (Hilti shot pins excluded, U-053); top track in two families: 14 GA 2\" deep-leg deflection track 13/A540 at types A/C/E to structure, standard top track at partial-height B/D and furring F/G/H."),
 ("ALC-05", "CUANTIFICADO", "Heads: one runner track over HM frames (3/A530) and aluminum frames (12/A530); double studs at jambs (A550 keynotes 5/8 'PROVIDE DOUBLE STUDS AT DOOR JAMBS', 4/A530); sill track at interior window frames A221."),
 ("ALC-06", "CUANTIFICADO", "Bridging: 1-1/2\" C.R. channel through studs at mid-height (A550 keynotes 5/8/12/13), one row per wall (plan governs over spec 05 40 00 3.3.E, R-ALC-10); partial-height walls braced to structure per 8/A540 (dia. brace @4'-0\" o.c., keynote 7)."),
 ("ALC-07", "CUANTIFICADO", f"5/8\" gyp wallboard per face as drawn in each A550 type section (keynote 3), {q('5/8\" gyp board regular (walls + ceilings)'):,} SF regular walls + ceilings; 5/8\" Type X only on furring over the 2-hour CMU lines (keynote 3 'TYPE X AT RATED WALLS'), {q('5/8\" gyp board Type X'):,} SF."),
 ("ALC-08", "CUANTIFICADO", f"5/8\" DensShield glass-mat tile backer at all restroom gyp bd (2/A001 'ALL GYP. BD. WITHIN RESTROOM SHALL BE GEORGIA-PACIFIC DENS SHIELD' + A550 keynote 3), {q('5/8\" glass mat tile backer (Dens Shield)'):,} SF."),
 ("ALC-09", "CUANTIFICADO" if ext_ok else "RFI", "Exterior gypsum / glass-mat sheathing: drawings show 1/2\" glass mat sheathing (27/A540, 21/A530, A301 keynote 22); spec 092900 2.2.B Dens-Glass Gold 5/8\" Type X: plan governs (R-ALC-10, note with the delta)."),
 ("ALC-10", "NO APLICA", EXC + "FRT plywood / wood blocking / plywood sheathing (Div. 06, U-139): 061000 / 061600 items, plywood at roof / parapet / backing (A300-A312, A540)."),
 ("ALC-11", "CUANTIFICADO", "5/8\" gyp bd ceilings room by room from A131 / A132 (PGB tags): suspended (24/A540) and framed (section keynote 8, 12/A540) systems; ACT, open-to-structure and existing ceilings EXCLUDED per room with the printed reason (EXCLUDED markups in each room)."),
 ("ALC-12", "CUANTIFICADO", f"Drywall suspension (USG DGLW main tee @48\", cross tee @16\", angle molding at perimeter, 12 ga hanger wire): main tee {q('USG drywall main tee (DGLW26)'):,} LF, cross tee {q('USG drywall cross tee (DGLW424)'):,} LF, angle {q('USG angle molding (DGWM24)'):,} LF, hanger wire {{{{MS:Hanger wire}}}} LF."),
 ("ALC-13", "CUANTIFICADO", "Soffits / light coves / bulkheads from the RCP: sloped soffit 14/A540, light coves 23/A540 and 28/A540, gyp headers at A131 / A132 (framing + board, developed width)."),
 ("ALC-14", "NO APLICA", "EXCLUDED - the only canopy is the entry portal: A111 keynote 41 'ENTRY PORTAL BY GC & ACM CLADDING'; 1 / 2 / 3 / 6 / A521 draw its framing 'SEE STRUCT' (Review Item: delta to measure if the GC assigns it)."),
 ("ALC-15", "CUANTIFICADO", "Column / pier furring: type G furring at the exterior CMU piers of Delivery 115 / Break Room 139 / Dealer 140 (A111, grid A)."),
 ("ALC-16", "NO APLICA", EXC + "wood blocking / backing (Div. 06, U-139): A150 and A211 general note 16 'FURNISH AND INSTALL ALL BLOCKING AS REQUIRED' (toilet accessories), A502 ADA grab bar blocking, A220 / A221 'FURNISH & INSTALL ALL FRAMING, BLOCKING, AND REINFORCING' (window framing note), A521 parapet / coping blocking, A001 spec summary; casework by GC / vendor (A230 / A231). Metal stud blocking at 13/A540 is carried (BLK rows)."),
 ("ALC-17", "CUANTIFICADO", "4 ceiling access panels 30\"x30\" counted on A131 (AP-01..AP-04, A131 legend 'CASTWORKS CRG' / 'ARMSTRONG'); the A131 note 'PROVIDE ADDITIONAL CONCEALED ACCESS PANELS' gives no number (Review Item RI-40). " + EXC + "framed openings for ducts / air devices (R-ALC-03)."),
 ("ALC-18", "CUANTIFICADO", f"Control joints in gyp ceilings per 24/A540 at A131 keynote 6 lines ({q('control joint')} LF); wall control joints 7/A540 (A111 general note 2) and metal trim at exposed edges / outside corners (092900 3.5.C)."),
 ("ALC-19", "NO APLICA", EXC + "acoustical sealant / sound attenuation; batt insulation of types A1/B1/C1/D1/E1/F1/H1 (keynote 11, 07 21 00)."),
 ("ALC-20", "CUANTIFICADO", "Tile backer = DensShield at restrooms (ALC-08); FRP-1 at janitor (A140 finish schedule) = 066400 Plastic Paneling (Div. 06) by others - EXCLUDED."),
 ("ALC-21", "NO APLICA", "No shaft wall / area separation wall in the set (A550 types A-K only)."),
 ("ALC-22", "NO APLICA", "Rated assembly: 2-hour CMU wall UL U906 (A551, A002) - CMU by others; no rated metal-stud assembly; Type X carried on the furring over the rated CMU lines (keynote 3)."),
 ("ALC-23", "NO APLICA", "No ballistic, lead-lined or abuse-resistant panel in the set (A550, A140)."),
 ("ALC-24", "CUANTIFICADO", f"Level 4 at painted walls / ceilings and Level 5 at WC-1 wallcovering (A140 general note 1 + WC-1 row; spec 092900 3.6.D lists L1/L2/L4 only: drawing governs), Level 5 {q('Level 5 finish'):,} SF."),
]
extra = [
 ("Wood framing / blocking / plywood (Div. 06)", "EXCLUDED - wood framing, blocking, backing and plywood (Div. 06, U-139)."),
 ("Fasteners: screws, anchors, PAF", "EXCLUDED - estimator standing order U-053: drywall / framing screws, Hilti shot pins (A550 keynote 4, 10/A540), anchors at 0 (rows kept with their source)."),
 ("Framed openings for ducts", "EXCLUDED - estimator standing order R-ALC-03: duct / air device openings never quantified (M101-M106 swept)."),
 ("ACT ceilings and grid", "EXCLUDED - ACT-1 acoustical ceilings and grid (A131 / A132 tags; ACT section not in this spec book): other trade (U-061)."),
 ("Existing ceilings", "EXCLUDED - existing ceilings to remain / existing ceiling demolition without the type printed (R-ALC-05); keynote 52 ACT demolition = ACT trade."),
 ("Insulation", "EXCLUDED - batt insulation (keynote 11, types x1) and continuous insulation (07 21 00 / 07 21 13)."),
 ("Paint and wall covering", "EXCLUDED - paint / WC-1 wall covering (A140 finish legend; painting / wall covering sections not in this spec book): other trade; only Level 5 board finish is ours."),
 ("CMU, structural steel, joists, deck", "EXCLUDED - CMU types J / K (A550), 2-hour CMU U906 (A551), structural steel / joists / deck (S sheets), steel angles L5X3 (S402) and L6X3 (S403): other trades."),
 ("EIFS, ACM, metal panels, roofing", "EXCLUDED - exterior cladding / roofing (A200 / A201 finish legend, 07 41 20, 07 53 23): other trades."),
 ("Storefront, curtain wall, doors, frames, hardware", "EXCLUDED - aluminum storefront / curtain wall / doors / HM frames / hardware (08 sections): other trades; framing at their heads / jambs is ours."),
 ("Entry portal", "EXCLUDED - A111 keynote 41 'ENTRY PORTAL BY GC & ACM CLADDING'."),
 ("FRP", "EXCLUDED - FRP-1 janitor (A140 finish schedule) = 066400 Plastic Paneling (Div. 06)."),
 ("Casework and millwork", "EXCLUDED - casework by GC / owner's vendor (A111 keynotes 10, 11; A230 / A231)."),
 ("MEP, fire protection and electrical", "EXCLUDED - M / P / E / FP work."),
 ("Demolition of gypsum board and metal framing", f"QUANTIFIED - A108 / A109 existing metal-stud walls to remove: SF = L x H per element (U-143), {q('demolition - gypsum board and metal framing'):,} SF; keynote 1 building tear-down structure / CMU / exterior walls by GC (excluded)."),
]
barrido = [
 {"item": "header", "specs": "found 3/A530 (HM head at studs) and 12/A530 (aluminum head): one runner track", "schedule": "found A400 door schedule head / jamb details", "estructural": "steel lintels by structure at CMU openings (S sheets)"},
 {"item": "deflection clips", "specs": "none: 13/A540 deep-leg slotted deflection track (no clip)", "schedule": "none", "estructural": "none"},
 {"item": "bracing", "specs": "found 8/A540 diagonal brace @4'-0\" o.c. for partial-height walls (keynote 7)", "schedule": "none", "estructural": "S403 CFS brace details at structural soffits"},
 {"item": "bridging", "specs": "found A550 keynotes 5/8/12/13: 1-1/2\" channel at mid-height", "schedule": "none", "estructural": "S001 CFS notes"},
 {"item": "blocking", "specs": "wood backing only (Div. 06, excluded)", "schedule": "none", "estructural": "none"},
 {"item": "backing", "specs": "casework / grab bar backing wood (excluded)", "schedule": "none", "estructural": "none"},
]
json.dump({"alc": alc, "extra": extra, "barrido": barrido}, open(f'{W}/etapas/4_canon/alcance_notas.json', 'w'), indent=1, ensure_ascii=False)
print(len(alc), len(extra))
