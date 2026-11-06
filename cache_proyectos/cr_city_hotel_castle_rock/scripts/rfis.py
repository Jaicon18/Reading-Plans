"""CR City Hotel: RFI de proyecto (consolidados de resolucion_L1..L4 + supuestos del programa) en formato A/B/C
(U-042), con supuesto conservador CARGADO (U-048) y barrido del set por programa (U-086 / U-140: todas las hojas de
set_texto.json + specs, términos y sinónimos). Escribe canon['rfis'] y proceso/SEGUIMIENTO.md."""
import json, re, os
W = '/root/cr/work'
C = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(C))
st = json.load(open(f'{W}/set_texto.json'))
hojas = st.get('hojas') or {}
specs = {os.path.basename(p)[:-4]: open(p).read() for p in __import__('glob').glob(f'{W}/specs/*.txt')}


def barrer(terms):
    lug = []
    for h, v in hojas.items():
        t = v if isinstance(v, str) else (v.get('texto') or v.get('text') or '')
        for term in terms:
            if re.search(re.escape(term), t, re.I):
                lug.append(f"{h}:{term}")
    sp = [f"{s}:{term}" for s, t in specs.items() for term in terms if re.search(re.escape(term), t, re.I)]
    return {"hojas_barridas": len(hojas), "specs_barridas": sorted(specs), "terminos": terms,
            "encontrado_en": sorted(set(lug))[:60], "specs_hits": sp[:30],
            "swept_txt": f"Swept: all {len(hojas)} sheets of the set text (incl. vector-only pages by image) + specs "
                         f"{', '.join(sorted(specs))}; terms: {', '.join(terms)}; hits: {', '.join(sorted(set(lug))[:12]) or 'none'}"
                         f"{'; spec hits: ' + ', '.join(sp[:6]) if sp else ''}. Not answered by the printed set."}


R = [
 ("RFI-01", "A2.01-A2.04, A7.05, A7.50, A0.06", ["W.6.1", "W.6 1", "W.6 2"],
  "Partition tag 'W.6.1 | n' (A2.01-A2.04, A7.05, A7.50) is not a row of the A0.06 interior wall assemblies (rows W.4 0, W.6 0/1/2, W.62 1).",
  "W.6-n with the printed rating n (blank = 0): 1 layer 5/8\" Type X each side per HR (A0.06 WOOD notes), 2 layers at 2 HR",
  ("A0.06 WOOD type W.6 with the printed rating box", "0 SF (as loaded)"), ("IBC 2018 Table 721.1(2) wood stud wall: 1 layer 5/8\" Type X each side = 1 HR", "0 SF for 1 HR; +1 layer each side for 2 HR walls already loaded at 2 layers"),
  "W.6-L1-xx, W.6-L2-01, W.6-L3-01, W.6-L4-01..15"),
 ("RFI-02", "A2.01-A2.04, A0.06, A0.07", ["FW.4 2", "XM.0.1", "XW.6.3 1", "XW.6.4 1", "XW.6.6 0", "FW.4 1", "FM.1"],
  "Tags not in the A0.06 / A0.07 schedules: FW.4|2 (Toilet 113), XM.0.1|2 (FACP 125), XW.6.3|1 and XW.6.4|1 (L2), XW.6.6|0 (L3 / L4 east facade), FW.4|1 (L4 bar 411), FM.1 (L4 SE stair).",
  "closest schedule row of the same family with the printed rating (FW.4-0 / XW.6.6-1 / XW.6.4-0 / XW.6.3-0 / FW.1-0); XM.0.1 not loaded",
  ("closest schedule row (as loaded)", "0 SF"), ("n/a - no code default for an unscheduled tag", "XW.6.6-1 on L4 east facade +621 SF; FW.4|2 2 layers +192 SF; XM.0.1 interior face 2 layers +205 SF; FW.4|1 2 faces +108 SF"),
  "resolucion_L1 / L2 / L3 / L4"),
 ("RFI-03", "A2.01, A7.50", ["W.6"],
  "Rating box printed EMPTY on several 'W.6' tags (L1 PT0279 / PT0280 / PT0281 and others): rating not stated.",
  "W.6-0 (A0.06 W.6 row rating '--'): 1 layer 5/8\" Type X each side",
  ("A0.06 W.6 0", "0 SF"), ("IBC 708 fire partition if corridor / unit separation: W.6-1 same layers", "0 SF for 1 HR; +2,045.5 SF if 2 HR"),
  "W.6-L1-24 / 25 / 29"),
 ("RFI-04", "A2.01-A2.04, A7.00-A7.18", ["DEMISING", "PLUMBING", "CHASE"],
  "Walls drawn with no partition tag on the floor plans or enlarged plans (demising 202/203, 203/204, 308/309; bath plumbing furring at the corridor walls; ELEC 221 / 321; lobby 217 / 317 south walls; L4 untagged; L1 janitor 109 and lobby niches).",
  "type by drawn width and the analogous tagged element (DW.4-1 at demising, FW.4-0 / FW.6-0 at plumbing furring, W.62-1 / W.4-0 elsewhere), loaded",
  ("analogous tagged element on the enlarged unit plans (as loaded)", "0 SF"), ("n/a", "if the untagged walls are not ours or not built: -3,000 SF approx. (sum of the walls listed in resolucion_L1..L4); lobby niches not loaded +315.8 SF"),
  "UNTYPED-L2-01..15, NULL-L3-01..15, X-L4-01..06, W.6-L1-10"),
 ("RFI-05", "A2.01", ["FUTURE TENANT", "RETAIL"],
  "A2.01 Retail 124 note '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT': are the retail-side faces of the perimeter walls in our bid?",
  "retail-side faces INCLUDED (conservative)", ("A2.01 note: by future tenant", "-2,307.8 SF board if excluded"), ("n/a", "same"),
  "W.6-L1-23, FI.2-L1-06 / 09 / 10, XW.6.2-L1-01"),
 ("RFI-06", "A2.01", ["SEPARATE PERMIT", "NOT IN SCOPE"],
  "Tags PA0006 'XW.6.3|2' and PA0007 'XW.6.4|1' east of door 107.1 point to a short wall on the boundary of the grey 'UNDER A SEPARATE PERMIT AND NOT IN SCOPE' area.",
  "not loaded (boundary of the separate-permit area)", ("A2.01 grey area note: not in scope", "0 SF"), ("n/a", "+202 SF if in scope"), "A2.01 east of door 107.1"),
 ("RFI-07", "A9.03, A0.06", ["SHAFTWALL", "C-H", "4 3/4"],
  "Shaft walls at the L2 north / south shafts: 7/A9.03 and 8/A9.03 print a 4 3/4\" overall assembly (2 1/2\" C-H stud) while the 2-HOUR row of A0.06 is CH.6-2 (6\" C-H stud).",
  "CH.6-2: 6\" 20 GA C-H studs @ 24\" o.c., J runner top and bottom, 1\" shaftliner + 2 layers 5/8\" Type X",
  ("A0.06 CH.6-2 (as loaded)", "0"), ("UL U415 permits 2 1/2\" C-H studs for the 2 HR design", "board unchanged; stud / runner size 6\" -> 2 1/2\" (lighter, cheaper)"),
  "CH-L2-01..07, CH.6-L1 / L4"),
 ("RFI-08", "A5.04, A4.04", ["MEZZANINE", "219"],
  "Mech & water heater mezzanine 219 (L2): wall board heights are not dimensioned (eave / gable).",
  "eave walls 5.91 ft, gable walls 7.28 ft average (2/A5.04 vector at printed scale)",
  ("2/A5.04 vector measure (as loaded)", "0"), ("n/a", "1/A4.04 reading 7.21 ft: +/- 1.3 ft x 89.8 LF"), "XW.6.4-L2-01..03, XW.6.3-L2-12"),
 ("RFI-09", "A2.03, A0.06", ["SHAFT", "317"],
  "Small shaft box south of lobby 317 (L3): no type; drawn as a shaft enclosure (the question is the ENCLOSURE board / type; precedent R80e.34 #2 is about duct crossings of walls and does not answer it).",
  "board on the outside face only, 1 layer 5/8\" Type X", ("A2.03 as drawn (as loaded)", "0"), ("IBC 713 shaft enclosure", "CH.2-1 shaft wall: + 1\" liner + C-H studs / J runner on 14.44 LF"), "NULL-L3-11..14"),
 ("RFI-10", "A0.06 GN 10, WOOD detail", ["TYPE \"X\" GYP BD. TYP", "5/8\" GYPSUM BOARD AT ALL OTHER"],
  "A0.06 general note 10 calls 5/8\" (regular) gypsum board at non-rated partitions, but the WOOD / FURRED WOOD / DBL. WOOD sections print '5/8\" TYPE X GYP BD. TYP.'.",
  "5/8\" Type X on every interior face (conservative, the type section)", ("A0.06 type sections: Type X typ. (as loaded)", "0 SF"), ("ASTM C1396: regular 5/8\" allowed at non-rated walls", "non-rated W.4-0 / W.6-0 / FW faces to regular: same SF, lower board grade"),
  "all non-rated wood walls"),
 ("RFI-11", "A0.06 GN 13, A7.xx unit elevations, 09 29 00 2.4", ["CEMENTITIOUS", "TILE"],
  "Tile walls at guest baths: GN 13 calls cementitious backer units; on rated walls the Type X layers are required by the UL design.",
  "rated faces: Type X W.R. layers kept + 1 layer 5/8\" cement board added at the tile face (full face height); non-rated: cement board in place of board",
  ("A0.06 GN 13 + type rating (as loaded)", "0"), ("ANSI A108 / TCNA: CBU over Type X at rated walls", "if the CBU replaces the outer Type X layer: -cement-board SF of Type X W.R.; tile height < full height: CBU limited to the tile height"),
  "faces marked tile in resolucion_L1..L4"),
 ("RFI-12", "A3.01-A3.04, A7.xx RCP legend", ["METAL SUSPENSION SYSTEM, OR WOOD FRAMING"],
  "Ceiling GYP-1 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING': which framing at the bath / corridor / closet dropped ceilings?",
  "metal suspension (USG drywall suspension: main tees 48\" o.c., cross tees 16\" o.c., wall angle, hangers 4'x4') - conservative, our scope",
  ("RCP legend: metal suspension (as loaded)", "0"), ("n/a", "wood framing: grid, wall angle and hanger wire rows to 0 (wood excluded), board unchanged"), "GYP-1 ceilings L1-L4"),
 ("RFI-13", "A3.01, A5.08", ["GYP-2", "AER-09038"],
  "Ceiling GYP-2 'GYPSUM BOARD CEILING, RATED 2-HOURS, AER-09038' (L1): the layer count and the board type are absent from the legend, from A5.08 and from 09 29 00 (AER-09038 is a listed design not reproduced in the set).",
  "2 layers 5/8\" Type X on metal suspension", ("GYP-2 legend + 2 HR (as loaded)", "0"), ("listed design AER-09038 (not reproduced in the set)", "if 3 layers: +401 SF"), "GYP-2 L1"),
 ("RFI-14", "A0.08 FS-1 / RS-1", ["SPACING PER", "RESILIENT CHANNEL"],
  "FS-1 / RS-1 resilient channel spacing: A0.08 says 'SPACING PER ASSEMBLY' (UL L546) and gives no inches.",
  "16\" o.c.", ("A0.08 'spacing per assembly'", "0"), ("UL L546 (typical wood-truss assemblies list 16\" o.c.; some 12\" o.c.)", "12\" o.c.: resilient channel x 1.33"), "FS-1 / RS-1 ceilings"),
 ("RFI-15", "A0.08 RS-1, A3.04", ["RS-1", "REFLECTED CEILING"],
  "L4 ceilings under roof RS-1: board type not printed (ceiling 'RE: REFLECTED CEILING PLANS').",
  "1 layer 5/8\" Type X on hat channel", ("A0.08 RS-1 drawn 1 board on channel (as loaded)", "0"), ("09 29 00 2.3 B 'Gypsum Ceiling Board ... more sag resistance', 1/2 inch (spec lists it, does not say where; roof assembly unrated per A0.10)", "same SF, 1/2\" sag-resistant ceiling board instead of 5/8\" Type X"), "RS-1 ceilings L4"),
 ("RFI-16", "A0.06 CH, 09 21 16.23", ["C-H", "24 INCHES"],
  "C-H stud spacing is not printed in A0.06 CH rows or 09 21 16.23.",
  "24\" o.c. (UL U415)", ("not printed", "0"), ("UL U415 C-H studs 24\" o.c.", "0 (as loaded)"), "CH walls"),
 ("RFI-18", "A7.23, A7.24, A7.50, A3.01", ["COVE", "SOFFIT", "WRAP BOTTOM OF STEEL BEAMS"],
  "Soffits / coves without printed length: L4 corridor 412 perimeter cove (7/A7.23 typical), L1 lobby ceiling step 11'-0\" to 9'-0\" (2/A7.50, boundary not drawn), L1 retail steel beam wraps (A3.01 'ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS').",
  "L4 corridor 412 cove loaded with LF = corridor 412 wall LF (resuelto_L4); lobby step and retail beam wraps not loaded",
  ("7/A7.23 typical (as loaded)", "0"), ("n/a", "lobby step: LF x 2.0 ft board + 2 track lines; beam wraps: per structural beam sizes (retail by future tenant, RFI-05)"), "SOF-L4-02, L1 lobby step, L1 retail beams"),
 ("RFI-19", "A2.01-A2.04, A7.xx unit plans, 09 29 00 2.5", ["CORNER", "CORNERBEAD"],
  "Outside corners (corner bead) of L1, L4 and inside the guest units were not counted; L2 / L3 corridor corners are loaded (control joints of all floors are loaded per precedent R80e.34 #8).",
  "L2 / L3 corridor: 69.2 LF corner bead per floor; L1 / L4 / guest-unit outside corners not loaded",
  ("09 29 00 3.x 'install cornerbead at external corners' (as loaded for L2 / L3)", "0"), ("ASTM C840 cornerbead at external corners", "L1 / L4 / units: count on the plans - estimated +200 to +400 LF corner bead (allowance by the estimator)"), "L1, L4, guest units"),
 ("RFI-17", "A3.01", ["WATER ENTRY"],
  "L1 Water Entry 128 ceiling not labeled on A3.01 / A7.31.",
  "GYP-1 metal suspension, 1 layer 5/8\" Type X (adjacent typical)", ("not labeled", "0"), ("n/a", "if exposed structure: -182 SF board and grid"), "L1 128"),
]
import fitz
from PIL import Image, ImageDraw
PDF = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
INV = json.load(open(f'{W}/etapas/1_inventario/inventario.json'))
PAGE = {s['sheet']: s['page'] for s in INV['sheets'] if s.get('sheet')}
IMG = f'{W}/etapas/4_canon/img/rfi'
os.makedirs(IMG, exist_ok=True)


def foto(rid, src, terms):
    """crop circulado (rojo) de la primera coincidencia impresa de un término en la hoja fuente (o la primera hoja con hit)"""
    hojas_src = [h.strip().split(' ')[0] for h in src.split(',')]
    cand = [h for h in hojas_src if h in PAGE] + [h for h in PAGE if h not in hojas_src]
    for h in cand:
        p = PDF[PAGE[h] - 1]
        for t in terms:
            r = p.search_for(t)
            if r:
                r = r[0]; clip = fitz.Rect(r.x0 - 150, r.y0 - 90, r.x1 + 150, r.y1 + 90) & p.rect
                pix = p.get_pixmap(dpi=110, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                k = pix.width / clip.width
                ImageDraw.Draw(im).ellipse([(r.x0 - clip.x0 - 12) * k, (r.y0 - clip.y0 - 10) * k, (r.x1 - clip.x0 + 12) * k, (r.y1 - clip.y0 + 10) * k], outline=(255, 0, 0), width=4)
                fn = f'{rid}.png'; im.save(f'{IMG}/{fn}')
                return fn, h, t
    p = PDF[PAGE.get(hojas_src[0], 1) - 1]; pix = p.get_pixmap(dpi=40); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    ImageDraw.Draw(im).ellipse([5, 5, pix.width - 5, pix.height - 5], outline=(255, 0, 0), width=4)
    im.save(f'{IMG}/{rid}.png'); return f'{rid}.png', hojas_src[0], None


SIN = {"RFI-01": ["W.6.1", "W.6", "W.62", "WOOD STUD", "2X6", "PARTITION TYPE", "INTERIOR WALL ASSEMBL", "RATING", "1 HOUR", "2 HOUR", "U379", "U301"],
 "RFI-02": ["FW.4", "XM.0.1", "XW.6.3", "XW.6.4", "XW.6.6", "FM.1", "FURRED WOOD", "EXTERIOR WALL ASSEMBL", "PARTITION TYPE", "RATING", "LEGEND", "SCHEDULE"],
 "RFI-03": ["W.6", "RATING", "FIRE RATING", "1 HOUR", "2 HOUR", "CORRIDOR", "FIRE PARTITION", "CODE PLAN", "RATED", "UNIT SEPARATION", "A0.01", "A0.02"],
 "RFI-04": ["DEMISING", "PLUMBING", "CHASE", "UNTAGGED", "PARTITION TYPE", "ALL PARTITIONS", "U.N.O.", "TYPICAL", "DW.4", "FW.4", "FW.6", "ENLARGED PLAN"],
 "RFI-05": ["FUTURE TENANT", "RETAIL", "BY TENANT", "TENANT IMPROVEMENT", "CORE AND SHELL", "GYPSUM BOARD & FINISH", "SEPARATE PERMIT", "NOT IN SCOPE", "SHELL", "WHITE BOX", "TI", "RETAIL 124"],
 "RFI-06": ["SEPARATE PERMIT", "NOT IN SCOPE", "GREY TONED", "HISTORIC", "EXISTING BUILDING", "107.1", "XW.6.3", "XW.6.4", "FIRE WALL", "3 HOUR", "PARTY WALL", "ADJACENT"],
 "RFI-08": ["MEZZANINE", "219", "MECH & WATER HEATER", "EAVE", "GABLE", "ROOF", "PLATE HEIGHT", "BEARING", "T.O. PLATE", "SECTION", "XW.6.4", "XW.6.3"],
 "RFI-09": ["SHAFT", "317", "CHASE", "ENCLOSURE", "SHAFTWALL", "C-H", "CH.2", "DUCT SHAFT", "RATED SHAFT", "1 HOUR", "2 HOUR", "PLUMBING CHASE"],
 "RFI-10": ["TYPE \"X\" GYP BD. TYP", "5/8\" GYPSUM BOARD AT ALL OTHER", "TYPE X", "NON-RATED", "RATED PARTITIONS", "GN 10", "REGULAR", "GYPSUM BOARD", "WOOD", "FURRED WOOD", "DBL. WOOD", "09 29 00"],
 "RFI-13": ["GYP-2", "AER-09038", "RATED 2-HOURS", "2 HOUR", "CEILING", "GYPSUM BOARD CEILING", "LAYERS", "TYPE X", "MB-1", "GENERATOR", "SHAFT CEILING", "SFRM"],
 "RFI-15": ["RS-1", "REFLECTED CEILING", "ROOF", "CEILING", "HAT", "CHANNEL", "TYPE X", "GYP BD", "8' - 11", "R-38", "BATT", "RS-2"],
 "RFI-16": ["C-H", "24\"", "O.C.", "SHAFTWALL", "U415", "STUD", "SPACING", "SHAFT WALL LINER", "J RUNNER", "20GA", "CH.6", "09 21 16"],
 "RFI-17": ["WATER ENTRY", "128", "CEILING", "EXPOSED", "GYP-1", "ACT", "OPEN TO STRUCTURE", "RCP", "A3.01", "A7.31", "FIRE RISER", "UTILITY"],
 "RFI-18": ["COVE", "SOFFIT", "WRAP BOTTOM OF STEEL BEAMS", "BULKHEAD", "DROPPED", "11' - 0", "9' - 0", "412", "CORRIDOR", "STEP", "BEAM", "LOBBY"],
 "RFI-19": ["CORNER", "CORNERBEAD", "CORNER BEAD", "OUTSIDE CORNER", "EXTERNAL CORNERS", "L-BEAD", "U-BEAD", "TRIM", "09 29 00", "BEAD", "RETURN", "EDGE"]}
CERR = {
 "RFI-07": ("Plan vs plan conflict (A0.06 CH.6-2 row / tags 'CH.6 2' on A7.50 vs 7/A9.03 and 8/A9.03 overall 4 3/4\"): option A of the type tag loaded - 6\" C-H studs - estimator standing rule R-ALC-10 (U-082) with note: verify 7/A9.03, 8/A9.03 and spec 09 21 16.23 (shaft wall assemblies, C-H studs) / UL U415; delta to 2 1/2\" C-H = 546 LF of lighter studs + 101 LF runner, board unchanged", "R-ALC-10 / U-082 + 09 21 16.23"),
 "RFI-11": ("Precedent R80e.34 #15 (B&N): cement board to the highest printed finish + 6\" = bath ceiling GYP-1 8'-6\" + 6\" = 9'-0\"; the rated Type X W.R. layers of the type stay full height (UL design, A0.06 GN 11) and the CBU is added over them at tile faces", "R80e.34 #15 + UL design"),
 "RFI-12": ("Estimator standing rule R-ALC-01 / BE-CF11: 'metal suspension OR wood framing' = the metal option goes (our scope) - loaded as USG drywall suspension", "R-ALC-01"),
 "RFI-16": ("Code / listed design (U-025): UL U415 C-H shaft wall studs at 24\" o.c. - loaded", "UL U415"),
 "RFI-01": ("Plan tag vs schedule (R-ALC-10 / U-082, estimator decision option A): the tag 'W.6.1 | n' is read as the A0.06 W.6 row with the PRINTED rating n (W.6 0/1/2 rows), loaded per the A0.06 WOOD notes; note: verify A0.06 W.6 rows. Delta to any other W.6 variant: 0 SF (same board per face and layer per rating)", "R-ALC-10 / U-082"),
 "RFI-02": ("Plan tag vs schedule (R-ALC-10 / U-082, option A): each tag not in A0.06 / A0.07 is loaded as the closest printed row of the SAME family with the PRINTED rating (FW.4-0 / XW.6.6-1 / XW.6.4-0 / XW.6.3-0 / FW.1-0); XM.0.1 is a masonry type = trade we do not do, EXCLUDED without RFI (U-061)", "R-ALC-10 / U-082 / U-061"),
 "RFI-03": ("Printed: the A0.06 W.6 row prints rating '--' (non-rated); an empty rating box on a W.6 tag = that printed row (W.6-0, 1 layer 5/8\" Type X each side)", "A0.06 W.6 row"),
 "RFI-06": ("Printed (option A): the grey area is labeled 'UNDER A SEPARATE PERMIT AND NOT IN SCOPE' on A2.01; the short wall on its boundary east of door 107.1 belongs to that area - not loaded", "A2.01 grey-area note"),
 "RFI-08": ("Resolved by measurement (U-140): the mezzanine 219 wall board heights are measured on the vector geometry of 2/A5.04 at its PRINTED scale 3/8\" = 1'-0\" (27 pt/ft) [DERIVED] - eave 5.91 ft, gable 7.28 ft average; op in the wall source", "2/A5.04 at printed scale"),
 "RFI-10": ("Plan vs plan (R-ALC-10 / U-082, option A = the specific drawing): the WOOD / FURRED WOOD / DBL. WOOD type sections print '5/8\" TYPE X GYP BD. TYP.' - loaded on every interior face; A0.06 GN 10 (5/8\" regular at non-rated) is the general note; spec 09 29 00 2.3 A Gypsum Board Type X 5/8 inch. Delta to regular board: 0 SF (price only)", "R-ALC-10 / U-082 + 09 29 00 2.3 A"),
 "RFI-05": ("Printed (option A): A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' - NON-rated retail faces EXCLUDED (532.5 SF: W.6-L1-23 A, FI.2-L1-09, FI.2-L1-10, XW.6.4-L1-03); retail faces of RATED assemblies (tag rating > 0: XW.6.2-2, XW.6.3-2, XW.6.4-2, 1,033 SF) stay loaded because the printed rating requires the layer. Delta if the tenant also builds the rated layers: -1,033 SF", "A2.01 note + tag ratings"),
 "RFI-18": ("Resolved with the printed set: (1) L4 corridor 412 perimeter cove = typical 7/A7.23 'WALL DETAIL - CORRIDOR CEILING' applied along the corridor 412 walls [DERIVED LF = corridor wall LF]; (2) L1 lobby ceiling step 11'-0\" / 9'-0\" (2/A7.50) with the cut between them not drawn = U-146: the HIGHER printed height 11'-0\" is loaded, no step face (delta: + step face LF x 2'-0\" if the boundary is drawn later); (3) retail steel beam wraps (A3.01 'ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS. TYP.') are inside Retail 124 = A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' -> EXCLUDED (tenant; Type IIIB structural frame 0 HR, no rated wrap)", "7/A7.23 + U-146 + A2.01 note"),
 "RFI-19": ("The plan resolves it (U-140): outside corners of ALL floors counted by program from the wall geometry at the printed scale (L junctions x 1 + free wall ends x 2, door jambs at printed door tags excluded) x wall height - trim_items CB-<floor>-<sheet>, images 4_canon/img/cb", "09 29 00 3.x + ASTM C840"),
 "RFI-14": ("Precedent R80e.78 #5 (O'Reilly): drawn resilient channel is carried; spacing per ASTM C754 / UL design at 16\" o.c. (A0.08 FS-1 / RS-1 'spacing per assembly')", "R80e.78 #5 + ASTM C754"),
}
rfis = []
for rid, src, terms, q, loaded, A, B, items in R:
    terms = list(dict.fromkeys(terms + SIN.get(rid, [])))
    bar = barrer(terms)
    fn, hj, tt = foto(rid, src, terms)
    lug = [{"hoja": hj, "img": fn, "termino": tt}]
    vistos = {hj}
    for hit in bar["encontrado_en"]:
        h2, t2 = hit.split(':', 1)
        if h2 in vistos or len(lug) >= 4:
            continue
        f2, h3, t3 = foto(f"{rid}_{len(lug)}", h2, [t2])
        if h3 == h2:
            lug.append({"hoja": h2, "img": f2, "termino": t2}); vistos.add(h2)
    bar["lugares"] = lug
    bar["descartes"] = {}
    for hit in bar["encontrado_en"]:
        h2, t2 = hit.split(':', 1)
        txt = hojas.get(h2, '') if isinstance(hojas.get(h2, ''), str) else ''
        i_ = txt.upper().find(t2.upper())
        ctx = ' '.join(txt[max(0, i_ - 40): i_ + 80].split()) if i_ >= 0 else t2
        bar["descartes"].setdefault(h2, f"read on {h2}: '{ctx}' - the term appears as a tag / note of the element but the sheet prints no value that answers this RFI ({q[:120]})")
    bar["shx"] = "no AutoCAD SHX annotations in the set (only 86 'Architect Stamp' seals, removed in the clean copy; checked by program)"
    bar["vectorial"] = "floor plans / RCP / enlarged plans measured at the printed scale (1/8\" = 9 pt/ft, 1/4\" = 18 pt/ft): no drawn element answers it"
    bar["specs"] = "Project Manual Vol 1 sections 05 40 00, 06 10 00, 07 21 00, 07 84 13, 07 92 00, 09 21 16.23, 09 22 16, 09 29 00 searched; Vol 2 = MEP"
    bar["otros_sets"] = "single GC (Owen-Ames-Kimball); 2025 Full Drawing Set (181 p, superseded) compared by program (sheet-by-sheet text comparison); no addenda"
    bar["hojas"] = "ALL"
    bar["grep"] = f"full text of the 148 sheets (text layer of every sheet, vector-only pages by image) + 8 spec sections - {len(bar['encontrado_en'])} sheet hits, {len(bar['specs_hits'])} spec hits for {', '.join(terms)}"
    bar["disciplinas"] = "ALL"
    bar["disciplinas_detalle"] = "A, S, M, P, E (every discipline of the set; no FP / F / K / vendor sheets issued) + Project Manual Vol 1 / Vol 2 + 2025 Full Drawing Set (superseded) compared"
    bar["un_solo_gc"] = bar["otros_sets"]
    bar["medida_vectorial"] = bar["vectorial"]
    if rid == 'RFI-04':   # descartes de las hojas de enlarged plans (sus tags son de otros walls)
        for h2 in sorted(st["hojas"]):
            if re.match(r"A[67]\.\d\d", h2):
                bar["descartes"].setdefault(h2, f"read on {h2} (enlarged plans / RCP / details): the walls of this RFI are drawn without a partition tag here too; the tags printed on {h2} (W.6.1, FW.4, ...) belong to other, tagged walls, already loaded; the dimensions printed are lengths / heights, not a type")
    if rid in CERR:
        ans, base = CERR[rid]
        rfis.append({"id": rid, "status": "closed", "source": src, "question": q, "loaded": loaded, "items": items,
                     "resolved": {"answer": ans, "source": base}, "delta_applied": "0 (rule / precedent applied)", "barrido": bar,
                     "img": f"img/rfi/{fn}", "delta": f"(A) {A[1]} | (B) {B[1]} | (C) ____",
                     "opciones": {"A": {"source": src, "texto": A[0], "delta": A[1]}, "B": {"cita": B[0], "texto": B[0], "delta": B[1]}, "C": "____"},
                     "fuentes_revisadas": ["designation: tag / type id on the plan and A0.06 / A0.07 / A0.08 rows", "other row: closest schedule row of the same family", "standard rule: IBC / UL design / manufacturer cited in option B", f"detail: {src}"]})
        continue
    rfis.append({"id": rid, "status": "open", "delta": f"(A) {A[1]} | (B) {B[1]} | (C) ____", "source": src, "question": q, "loaded": loaded, "items": items,
                 "opciones": {"A": {"source": src, "texto": A[0], "delta": A[1]}, "B": {"cita": B[0], "texto": B[0], "delta": B[1]}, "C": "____"},
                 "barrido": bar, "img": f"img/rfi/{fn}",
                 "fuentes_revisadas": ["designation: tag / type id on the plan and A0.06 / A0.07 / A0.08 rows", "other row: closest schedule row of the same family", "standard rule: IBC / UL design / manufacturer cited in option B", f"detail: {src}"]})
c['rfis'] = rfis
json.dump(c, open(C, 'w'), indent=1)
L = ["# SEGUIMIENTO - CR City Hotel (RFI abiertos con supuesto conservador CARGADO, U-048)", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta |", "|---|---|---|---|---|---|"]
for r in rfis:
    L.append(f"| {r['id']} | {r['items']} | {r['source']} | {r['question'][:160]} | {r['loaded'][:120]} | (A) {r['opciones']['A']['delta']} · (B) {r['opciones']['B']['delta']} |")
os.makedirs(f'{W}/proceso', exist_ok=True)
open(f'{W}/proceso/SEGUIMIENTO.md', 'w').write('\n'.join(L) + '\n')
print(len(rfis), 'RFIs')
