#!/usr/bin/env python3
"""Builds the HEIGHT audit files (U-175 / U-176) for CR City Hotel from the canon + blind readings H-A / H-B."""
import csv, json, os, re, sys
from fractions import Fraction

W = "/root/cr0/work"
CAN = f"{W}/etapas/4_canon"
OUT = f"{W}/PRUEBA DESDE CERO 13-nov/Auditoria"
HA, HB = f"{W}/etapas/2_lectura/HA", f"{W}/etapas/2_lectura/HB"
can = json.load(open(f"{CAN}/takeoff_canon.json"))
TOL = 1 / 48 + 1e-6


def fi(x):
    """ft -> 9'-3 1/2" (nearest 1/16")."""
    if x is None:
        return ""
    neg = x < 0
    x = abs(x)
    s16 = round(x * 12 * 16)
    ft, r = divmod(s16, 12 * 16)
    inch, frac = divmod(r, 16)
    fr = Fraction(frac, 16)
    fs = f" {fr.numerator}/{fr.denominator}" if frac else ""
    if ft == 0:
        return f'{inch}{fs}"'
    return f"{'-' if neg else ''}{ft}'-{inch}{fs}\""


def P(s):  # ft-in -> ft
    s = s.strip().replace("''", '"')
    m = re.fullmatch(r"(\d+)'\s*-?\s*(\d+)?(?:\s+(\d+)/(\d+))?\"?", s)
    if m:
        return int(m.group(1)) + (int(m.group(2) or 0) + (int(m.group(3)) / int(m.group(4)) if m.group(3) else 0)) / 12
    m = re.fullmatch(r"(\d+)(?:\s+(\d+)/(\d+))?\"", s)
    return (int(m.group(1)) + (int(m.group(2)) / int(m.group(3)) if m.group(2) else 0)) / 12


abs_img = lambda p: os.path.join(CAN, p) if p and not os.path.isabs(p) else p
SH = lambda n: abs_img(f"img/walls/sheets/{n}.png")

# ------------------------------------------------------------------ readings' parameters (from their own tables)
# H-A: ALTURAS_TYPES_A.csv (B.O. structure / Board height / Operation) + ALTURAS_ROOMS_A.csv
A = dict(
    struct={("L1", "perim"): (P("12'-3 1/2\""), "ALTURAS_TYPES_A W/XW L1 Board height 12'-3 1/2\" (14'-0\" - 2 1/2\" - 1'-6\", A4.00 / A0.08 FS-1 / S1.02)",
                              "14'-0\" - 2 1/2\" - 1'-6\" = 12'-3 1/2\""),
            ("L1", "lobby"): (P("12'-3 1/2\""), "ALTURAS_TYPES_A W/XW L1 Board height 12'-3 1/2\" (A4.00 / A0.08 / S1.02)", "14'-0\" - 2 1/2\" - 1'-6\" = 12'-3 1/2\""),
            ("L1", "onestory"): (P("11'-2 5/8\""), "ALTURAS_TYPES_A W L1 Operation 'single-storey courtyard zones: B.O. DECK 11'-2 5/8\"' (A5.04/A5.08)", ""),
            ("L2", "unit"): (P("9'-3 1/2\""), "ALTURAS_TYPES_A L2 Board height 9'-3 1/2\" (A4.00; W head A0.06)", "11'-0\" - 2 1/2\" - 1'-6\" = 9'-3 1/2\""),
            ("L2", "corr"): (P("9'-3 1/2\""), "ALTURAS_TYPES_A L2 Board height 9'-3 1/2\" (A4.00; W head A0.06)", "11'-0\" - 2 1/2\" - 1'-6\" = 9'-3 1/2\""),
            ("L3", "unit"): (P("9'-3 1/2\""), "ALTURAS_TYPES_A L3 Board height 9'-3 1/2\" (A4.00; W head A0.06)", "11'-0\" - 2 1/2\" - 1'-6\" = 9'-3 1/2\""),
            ("L3", "corr"): (P("9'-3 1/2\""), "ALTURAS_TYPES_A L3 Board height 9'-3 1/2\" (A4.00; W head A0.06)", "11'-0\" - 2 1/2\" - 1'-6\" = 9'-3 1/2\""),
            ("L4", "nonrated"): (P("9'-0 5/8\""), "ALTURAS_TYPES_A W.6 0 / DW.4 0 L4 B.O. roof truss 9'-0 5/8\" (1/A5.06, PENDING)", "8'-11 1/4\" + 1 3/8\" = 9'-0 5/8\""),
            ("L4", "rated"): (P("10'-6 5/8\""), "ALTURAS_TYPES_A rated L4 rows: 'fire partitions extend to U/S roof sheathing' (A0.10 det 2) 10'-6 5/8\" (Board height cell reads 8\", truncated)",
                              "8'-11 1/4\" + 1 3/8\" + 1'-6\" = 10'-6 5/8\"")},
    shaft={"L1": P("14'-0\""), "L2": P("11'-0\""), "L3": P("11'-0\""), "L4": P("14'-0\"")},
    shaft_src="ALTURAS_TYPES_A CH.6 rows: Board height '14'-0\" / 11'-0\" per level segment (shaft continuous)' (A4.00; 3/A5.08)",
    # room C.H. and the reading's own 'above' (membrane) row used as cap
    rooms={("L1", "105"): (7.0, None, "105 LINEN / STOR. ACT-2 7'-0\" (1/A3.01)"), ("L1", "101"): (7.0, None, "101 CORRIDOR ACT-2 7'-0\" (1/A3.01)"),
           ("L1", "113"): (9.0, None, "113 TOILET GYP-1 9'-0\" (1/A3.01)"), ("L1", "111"): (9.5, None, "111 TOILET GYP-1 9'-6\" (1/A3.01)"),
           ("L1", "110"): (9.5, None, "110 TOILET GYP-1 9'-6\" (1/A3.01)"), ("L1", "116"): (9.5, None, "116 ELEVATOR CONTROLS GYP-2 9'-6\" (1/A3.01)"),
           ("L1", "115"): (9.5, None, "115 BREAK ACT-2 9'-6\" (2/A7.50)"), ("L1", "117"): (None, None, "117 OFFICE not printed"),
           ("L1", "121"): (None, None, "121 SERVICE CORRIDOR not printed"), ("L1", "107"): (11.0, None, "107 BAR WS-1 11'-0\" (1/A3.01)"),
           ("L1", "108"): (11.0, None, "108 LOBBY perimeter dropped band GYP-1 11'-0\" (1/A3.01)"),
           ("L2", "main"): (P("9'-2\""), None, "unit main area 9'-2\" (FS-1, unit general note 1)"), ("L3", "main"): (P("9'-2\""), None, "unit main area 9'-2\""),
           ("L2", "bath"): (8.5, P("9'-2\""), "unit bathroom GYP-1 8'-6\" (unit RCP), FS-1 above 9'-2\""), ("L3", "bath"): (8.5, P("9'-2\""), "unit bathroom GYP-1 8'-6\", FS-1 above 9'-2\""),
           ("L2", "corr"): (P("8'-11\""), P("9'-10 5/8\""), "216/218 CORRIDOR GYP-1 8'-11\", FS-1 above 9'-10 5/8\" (7/A7.23)"),
           ("L3", "corr"): (P("8'-11\""), P("9'-10 5/8\""), "316/318 CORRIDOR GYP-1 8'-11\", FS-1 above 9'-10 5/8\""),
           ("L2", "ws1"): (P("8'-0 1/2\""), P("9'-10 5/8\""), "217 LOBBY WS-1 8'-0 1/2\" (1/A7.23), FS-1 above 9'-10 5/8\""),
           ("L3", "ws1"): (P("8'-0 1/2\""), P("9'-10 5/8\""), "317 LOBBY WS-1 8'-0 1/2\", FS-1 above 9'-10 5/8\""),
           ("L2", "clean"): (P("9'-2\""), None, "215 CLEANING GYP-1 9'-2\" (1/A3.02)"), ("L3", "clean"): (None, None, "315 CLEANING not printed"),
           ("L4", "main"): (P("8'-11 1/4\""), None, "4xx unit main 8'-11 1/4\" (1/A5.06)"), ("L4", "bath"): (8.5, P("8'-11 1/4\""), "4xx bathroom GYP-1 8'-6\", roof membrane above 8'-11 1/4\""),
           ("L4", "corr"): (P("8'-11\""), None, "412 CORRIDOR GYP-1 8'-11\" (above not printed)"), ("L4", "ws1"): (P("8'-11\""), None, "412 CORRIDOR GYP-1 8'-11\" (no WS-1 row)"),
           ("L4", "clean"): (None, None, "406 CLEANING not printed")},
    src_rooms="ALTURAS_ROOMS_A",
)
B = dict(
    struct={("L1", "perim"): (P("12'-1 3/8\""), "ALTURAS_TYPES_B L1 'to B.O. structure ... 12'-1 3/8\" (perimeter, A5.03)' by location", ""),
            ("L1", "lobby"): (P("12'-0 3/4\""), "ALTURAS_TYPES_B L1 'to B.O. structure ... lobby 12'-0 3/4\" (2/A7.31)' by location", "14'-0\" - 1'-11 1/4\" = 12'-0 3/4\""),
            ("L1", "onestory"): (P("11'-2 5/8\""), "ALTURAS_TYPES_B L1 'one-story B.O. DECK 11'-2 5/8\" (A5.04, A5.08)' by location", ""),
            ("L2", "unit"): (P("9'-2\""), "ALTURAS_TYPES_B L2 'Units 9'-2\" (11'-0\"-1'-10\")' (A5.06)", "11'-0\" - 1'-10\" = 9'-2\""),
            ("L2", "corr"): (P("9'-10 5/8\""), "ALTURAS_TYPES_B L2 'corridor 9'-10 5/8\" (11'-0\"-1'-1 3/8\")' (7/A7.23)", "11'-0\" - 1'-1 3/8\" = 9'-10 5/8\""),
            ("L3", "unit"): (P("9'-2\""), "ALTURAS_TYPES_B L3 'Units 9'-2\"' (A5.06)", "11'-0\" - 1'-10\" = 9'-2\""),
            ("L3", "corr"): (P("9'-10 5/8\""), "ALTURAS_TYPES_B L3 'corridor 9'-10 5/8\"' (7/A7.23)", "11'-0\" - 1'-1 3/8\" = 9'-10 5/8\""),
            ("L4", "nonrated"): (P("8'-11 1/4\""), "ALTURAS_TYPES_B L4 '8'-11 1/4\" at L4 exterior wall (A5.06, A5.03)'", ""),
            ("L4", "rated"): (P("8'-11 1/4\""), "ALTURAS_TYPES_B L4 '8'-11 1/4\" at L4 exterior wall (A5.06, A5.03)'", "")},
    shaft={"L1": P("14'-0\""), "L2": P("11'-0\""), "L3": P("11'-0\""), "L4": P("13'-11\"")},
    shaft_src="ALTURAS_TYPES_B CH rows: F-F (A4.00) continuous; at L4 '14'-0\" L4->ROOF ... less 1\" deflection gap at head (A0.06 note 7)'",
    rooms={("L1", "105"): (7.0, None, "105 Linen / Stor. ACT-2 7'-0\""), ("L1", "101"): (7.0, None, "101 Corridor ACT-2 7'-0\""),
           ("L1", "113"): (9.0, None, "113 Toilet GYP-1 9'-0\""), ("L1", "111"): (9.5, None, "111 Toilet GYP-1 9'-6\""), ("L1", "110"): (9.5, None, "110 Toilet GYP-1 9'-6\""),
           ("L1", "116"): (9.5, None, "116 Elevator Controls GYP-2 9'-6\""), ("L1", "115"): (9.5, None, "115 Break ACT-2 9'-6\""),
           ("L1", "117"): (9.5, None, "117 Office ACT grid 9'-6\" (DERIVED)"), ("L1", "121"): (None, None, "121 Service Corridor PENDING"),
           ("L1", "107"): (11.0, None, "107 Bar WS-1 / field 11'-0\""), ("L1", "108"): (11.0, None, "108 Lobby GYP-1 11'-0\""),
           ("L2", "main"): (P("9'-2\""), P("9'-2\""), "unit sleeping/living FS-1 9'-2\""), ("L3", "main"): (P("9'-2\""), P("9'-2\""), "unit sleeping/living FS-1 9'-2\""),
           ("L2", "bath"): (8.5, P("9'-2\""), "unit Bathroom GYP-1 8'-6\", stacked membrane 9'-2\""), ("L3", "bath"): (8.5, P("9'-2\""), "unit Bathroom GYP-1 8'-6\", stacked membrane 9'-2\""),
           ("L2", "corr"): (P("8'-11\""), P("9'-10 5/8\""), "216/218 Corridor GYP-1 8'-11\", rated membrane 9'-10 5/8\""),
           ("L3", "corr"): (P("8'-11\""), P("9'-10 5/8\""), "316/318 Corridor GYP-1 8'-11\", rated membrane 9'-10 5/8\""),
           ("L2", "ws1"): (None, None, "217 Lobby (elevator) PENDING (no tag)"), ("L3", "ws1"): (None, None, "317 Lobby (elevator) PENDING (no tag)"),
           ("L2", "clean"): (P("9'-2\""), P("9'-2\""), "215 Cleaning GYP-1 9'-2\""), ("L3", "clean"): (P("9'-2\""), P("9'-2\""), "315 Cleaning 9'-2\" (DERIVED)"),
           ("L4", "main"): (None, None, "4xx sleeping/living: bottom of roof PENDING"), ("L4", "bath"): (8.5, None, "4xx Bathroom GYP-1 8'-6\" (above PENDING)"),
           ("L4", "corr"): (P("8'-11\""), None, "412 Corridor GYP-1 8'-11\" (above PENDING)"), ("L4", "ws1"): (P("8'-0 1/2\""), None, "412 Corridor WS-1 8'-0 1/2\""),
           ("L4", "clean"): (None, None, "406 Cleaning PENDING")},
    src_rooms="ALTURAS_ROOMS_B",
)
ONESTORY = {"100", "104", "107", "110", "111"}


def fam(w):
    return re.match(r"[A-Z]+", w["type_id"]).group(0)


def rated(w):
    m = re.search(r"-(\d)$", w["type_id"])
    return bool(m and int(m.group(1)) > 0)


def fw_room(w):
    hs, loc, fl = w["height_source"].lower(), w["location"].lower(), w["floor"]
    if fl == "L1":
        for k, rx in (("107", r"\bbar\b"), ("108", r"gyp-1 11'-0\""), ("105", r"linen"), ("121", r"service corridor"), ("101", r"corridor 101|\(corridor 1\d\d\)"), ("116", r"elevator controls"),
                      ("115", r"office/break"), ("113", r"toilet 113"), ("111", r"toilet 111"), ("110", r"toilet 110"),
                      ("108", r"11'-0\"|lobby")):
            if re.search(rx, hs):
                return k
        return None
    if "cleaning" in hs:
        return "clean"
    if "ws-1" in hs or "wood slat" in hs:
        return "ws1"
    if "corridor" in hs and "8'-11\"" in hs:
        return "corr"
    if "bath" in hs:
        return "bath"
    return "main"


def zona(w):
    fl, h, loc = w["floor"], w["height_ft"], w["location"].lower()
    if fl == "L1":
        return "onestory" if abs(h - 11.219) < .01 or re.search(r"\b(bar|toilet 11[01])\b", loc) and h < 12 else ("lobby" if abs(h - 12.063) < .01 else "perim")
    if fl == "L4":
        return "rated" if rated(w) else "nonrated"
    faces = re.sub(r"^.*faces?:", "", loc)
    return "corr" if ("corridor" in faces or "lobby" in faces) and "guest room" not in faces else "unit"


def cat(w):
    h, hs, f = w["height_ft"], w["height_source"].lower(), fam(w)
    if f == "CH":
        return "shaft"
    if "stair" in hs and ("no ceiling" in hs or "stair enclosure" in hs):
        return "stair"
    if h < 1:
        return "band"
    if abs(h - 8.5) < .01 and ("tile" in hs or "backer" in hs):
        return "tile"
    if f in ("FW", "FI"):
        return "fw"
    if "exterior" in hs and "sheathing" in hs and h in (14.0, 11.0):
        return "ext"
    if "mezzanine" in hs:
        return "mezz"
    return "struct"


def lectura(w, R, nombre):
    """-> (value ft or None, source, operation)."""
    c, fl, f = cat(w), w["floor"], fam(w)
    z = zona(w)
    zz = z if c not in ("ext", "mezz") else ({"L1": "perim", "L4": "rated" if rated(w) else "nonrated"}.get(fl, "unit"))

    def struct(zk=None):
        v, s, op = R["struct"][(fl, zk or zz)]
        return v, s, op

    def fwv(room):
        if nombre == "B" and f == "FI":                         # H-B: FI rows = 'to B.O. structure'
            zk = ("onestory" if room in ONESTORY else "perim") if fl == "L1" else ("corr" if room in ("corr", "ws1") else ("rated" if fl == "L4" else "unit"))
            if fl == "L4":
                zk = "nonrated"
            v, s, op = R["struct"][(fl, zk)]
            return v, f"ALTURAS_TYPES_B FI rows 'to B.O. structure': {s}", op
        if nombre == "A" and f == "FW" and w["type_id"].startswith("FW.1") and fl == "L1":
            return P("12'-3 1/2\""), "ALTURAS_TYPES_A FW.1 0 L1 'not printed (load: to B.O. structure 12'-3 1/2\")'", "14'-0\" - 2 1/2\" - 1'-6\" = 12'-3 1/2\""
        ch, above, rs = R["rooms"].get((fl, room), (None, None, f"room '{room}' not in table"))
        if ch is None:
            return None, f"{R['src_rooms']}: {rs} -> FW/FI head 'C.H. + 6\"' has no C.H.", ""
        v = ch + 0.5
        op = f"{fi(ch)} + 6\" = {fi(v)}"
        if nombre == "A":
            cap = above if above is not None else R["struct"][(fl, ("onestory" if room in ONESTORY else "perim") if fl == "L1" else ("unit" if fl != "L4" else "nonrated"))][0]
        else:
            if fl == "L4":
                cap = None                                     # H-B: L4 B.O. 'not printed generally'; bath 8'-6"+6"=9'-0"
            elif fl == "L1":
                cap = R["struct"][(fl, "onestory" if room in ONESTORY else "perim")][0]
            else:
                cap = above if above is not None else R["struct"][(fl, "unit")][0]
        if cap is not None and v > cap + 1e-6:
            op += f"; cap: {fi(cap)} = {fi(cap)}"
            v = cap
        return v, f"{R['src_rooms']}: {rs}; FW/FI head = line of ceiling + 6\" (A0.06)" + (f", capped at {fi(cap)} (reading's B.O. / membrane above)" if cap is not None and abs(v - cap) < 1e-6 else ""), op

    if c == "shaft":
        v = R["shaft"][fl]
        return v, R["shaft_src"], ""
    if c == "stair":
        return fwv("stair") if f in ("FW", "FI") else struct("unit" if fl in ("L2", "L3") else zz)
    if c == "tile":
        ch = R["rooms"][(fl, "bath")][0] if fl != "L1" else None
        return ch, f"{R['src_rooms']}: bathroom GYP-1 8'-6\" (unit RCPs) = tile/backer face to bath ceiling (CRITERIOS 2)", ""
    if c == "band":
        if f in ("FW", "FI"):
            top, s, op = fwv("bath")
        else:
            top, s, op = struct("unit" if fl in ("L2", "L3") else zz)
        if top is None:
            return None, s, ""
        v = top - 8.5
        return v, f"band above tile = top of face ({s}) - bath C.H. 8'-6\" ({R['src_rooms']})", f"{fi(top)} - 8'-6\" = {fi(v)}"
    if c == "fw":
        room = fw_room(w)
        return fwv(room)
    return struct()


def rounded(v):
    return None if v is None else round(v, 4)


# ------------------------------------------------------------------ final (canon) operation strings
def final_op(w):
    h, fl, c, hs = w["height_ft"], w["floor"], cat(w), w["height_source"]
    f = fam(w)
    if c == "shaft":
        if fl == "L1":
            return "DERIVED", "6211.75 - 6197.75 = 14.00", "LEVEL 2 6211.75' - LEVEL 1 6197.75' (A4.00); C-H shaft continuous (A5.08)"
        if fl == "L4":
            return "DERIVED", "14'-0\" - 3/4\" = 13'-11 1/4\"", "L4->ROOF 14'-0\" (A4.00) - 3/4\" roof sheathing (S1.05); 1/A5.08 'SHAFT WALLS CONTINUOUS TO UNDERSIDE OF ROOF SHEETHING'"
        return "DERIVED", "6222.75 - 6211.75 = 11.00", "F-F datums (A4.00); shaftwall continuous through the floor (7,8/A9.03; A5.08)"
    if c == "stair":
        if fl == "L1":
            return "DERIVED", "6211.75 - 6197.75 = 14.00", "LEVEL 2 - LEVEL 1 datums (A4.00, 5/A6.02): stair enclosure has no ceiling"
        if fl == "L4":
            return "DERIVED", "14'-0\" - 3/4\" = 13'-11 1/4\"", "L4->ROOF 14'-0\" (5/A6.02) - 3/4\" roof sheathing; 11/A6.01 'RATED WALL CONTINUOUS TO UNDERSIDE OF ROOF SHEETHING'"
        return "CONFIRMED", "", "11'-0\" printed floor to floor (19 risers, 11/A6.01; 5/A6.02)"
    if c == "tile":
        return "CONFIRMED", "", "bath GYP-1 8'-6\" tag (unit RCPs A7.00/A7.05/A7.09/A7.13/A7.16); tile/backer to bath ceiling (CRITERIOS 2)"
    if c == "band":
        if abs(h - 0.792) < .01:
            return "DERIVED", "11'-0\" - 1 3/4\" - 3/4\" - 1'-6\" = 9'-3 1/2\"; 9'-3 1/2\" - 8'-6\" = 9 1/2\"", "line of structure 9'-3 1/2\" (A4.00; A0.08 FS-1; S1.02; CRITERIOS 3) - bath GYP-1 8'-6\" (unit RCP)"
        if abs(h - 0.4375) < .01:
            return "DERIVED", "8'-11 1/4\" - 8'-6\" = 5 1/4\"", "L4 line of structure 8'-11 1/4\" (1/A5.06) - bath GYP-1 8'-6\" (unit RCP)"
        if abs(h - 0.5) < .01:
            return "DERIVED", "8'-6\" + 6\" - 8'-6\" = 6\"", "FW/FI head = bath ceiling 8'-6\" + 6\" (A0.06 FW/FI head) minus tile area to 8'-6\""
    if c == "fw":
        m = {7.5: ("7'-0\"", "ACT-2 7'-0\" (1/A3.01)"), 9.5: ("9'-0\"", "GYP-1 9'-0\" Toilet 113 (1/A3.01)"), 10.0: ("9'-6\"", "9'-6\" ceiling (1/A3.01, 2/A7.50)"),
             11.5: ("11'-0\"", "GYP-1 11'-0\" (1/A3.01, 2/A7.50)"), 9.417: ("8'-11\"", "corridor GYP-1 8'-11\" (1/A7.23, 7/A7.23)"),
             8.542: ("8'-0 1/2\"", "WS-1 8'-0 1/2\" (1/A7.23)"), 9.0: ("8'-6\"", "bath GYP-1 8'-6\" (unit RCP)"), 9.667: ("9'-2\"", "9'-2\" stack of 215 (1/A3.02), review item")}
        for k, (ch, s) in m.items():
            if abs(h - k) < .005:
                return "DERIVED", f"{ch} + 6\" = {fi(P(ch) + .5)}", f"{s} + 6\" (A0.06 FW/FI head)"
        if abs(h - 9.292) < .005 or abs(h - 9.29) < .005:
            return "DERIVED", "9'-2\" + 6\" = 9'-8\"; cap: 11'-0\" - 1 3/4\" - 3/4\" - 1'-6\" = 9'-3 1/2\"", "room ceiling 9'-2\" (A7.00 unit note 1) + 6\" (A0.06), capped at line of structure (A4.00; A0.08; CRITERIOS 3)"
        if abs(h - 8.9375) < .005:
            return "CONFIRMED", "", "room ceiling + 6\" capped at L4 line of structure 8'-11 1/4\" printed on 1/A5.06 and 1/A5.03"
        if abs(h - 11.219) < .005:
            return "CONFIRMED", "", "no ceiling at the wall: capped at printed B.O. DECK 11'-2 5/8\" (2/A5.04)"
    if fl == "L1":
        if abs(h - 12.115) < .005:
            return "DERIVED", "14'-0\" - 1'-10 5/8\" = 12'-1 3/8\"", "LEVEL 1 to underside of L2 floor framing 12'-1 3/8\" printed on 3/A5.03 (W head A0.06 to line of structure)"
        if abs(h - 11.219) < .005:
            return "CONFIRMED", "", "B.O. DECK 11'-2 5/8\" printed on 2/A5.04, 1/A5.04, 3/A5.08 (one-storey roof)"
        if abs(h - 12.063) < .005:
            return "DERIVED", "14'-0\" - 1'-11 1/4\" = 12'-0 3/4\"", "lobby zone: 1'-11 1/4\" RATED ASSEMBLY (2/A7.31), 12'-0 3/4\" elev. (7/A7.31)"
        if abs(h - 14.0) < .005:
            return "DERIVED", "6211.75 - 6197.75 = 14.00", "exterior sheathing full storey: LEVEL 2 - LEVEL 1 datums (A4.00/A5.08)"
    if fl in ("L2", "L3"):
        if abs(h - 9.292) < .005 or abs(h - 9.29) < .005:
            return "DERIVED", "11'-0\" - 1 3/4\" - 3/4\" - 1'-6\" = 9'-3 1/2\"", "11'-0\" F-F (A4.00) - floor framing 1'-8 1/2\" (A0.08 FS-1; S1.02; CRITERIOS 3) = line of structure"
        if abs(h - 9.885) < .005:
            return "DERIVED", "11'-0\" - 1'-1 3/8\" = 9'-10 5/8\"", "corridor face to underside of corridor rated assembly 1'-1 3/8\" (7/A7.23)"
        if abs(h - 11.0) < .005:
            return "DERIVED", "6222.75 - 6211.75 = 11.00", "F-F datums (A4.00)" + (": exterior sheathing continuous past floor framing" if c == "ext" else ": Mezzanine 219 height not printed (RFI)")
    if fl == "L4":
        if abs(h - 8.9375) < .005:
            return "CONFIRMED", "", "8'-11 1/4\" LEVEL 4 to bottom of roof assembly printed on 1/A5.06 and 1/A5.03"
        if abs(h - 14.0) < .005:
            return "DERIVED", "6247.75 - 6233.75 = 14.00", "exterior gyp sheathing: LEVEL 4 -> ROOF datums (A4.00)"
    return None, None, None


# ------------------------------------------------------------------ resolution texts (A != B)
def resol(w, va, vb):
    c, fl, h = cat(w), w["floor"], w["height_ft"]
    ok = lambda v: v is not None and abs(v - h) <= TOL
    took = "H-A" if ok(va) and not ok(vb) else ("H-B" if ok(vb) and not ok(va) else "neither (canon kept; listed in ALTURAS_DISCREPANCIAS.md)")
    why = {
        "struct": {"L1": "L1 line of structure by area: 12'-1 3/8\" printed on 3/A5.03 (under L2), 11'-2 5/8\" B.O. DECK printed on 2/A5.04 (one-storey), 12'-0 3/4\" on 2,7/A7.31 (lobby); printed beats H-A's derived 12'-3 1/2\" (CRITERIOS 3)",
                   "L2": "W/DW/XW to LINE OF STRUCTURE (W head A0.06): 11'-0\" (A4.00) - 1'-8 1/2\" floor framing (1 3/4\" + 3/4\" + 18\" truss, A0.08 FS-1 / S1.02) = 9'-3 1/2\" (CRITERIOS 3); corridor face = 11'-0\" - 1'-1 3/8\" rated assembly (7/A7.23) = 9'-10 5/8\"; 9'-2\" is the bottom of the ceiling membrane (1/A5.06), not structure",
                   "L4": "L4 line of structure = 8'-11 1/4\" LEVEL 4 to bottom of roof assembly printed on 1/A5.06 and 1/A5.03; 10'-6 5/8\" / 9'-0 5/8\" are H-A derivations not printed"},
        "shaft": "C-H shaft continuous (1/A5.08 'SHAFT WALLS CONTINUOUS TO UNDERSIDE OF ROOF SHEETHING'; 7,8/A9.03): no head deflection gap at intermediate floors; L4 = 14'-0\" (A4.00) - 3/4\" roof sheathing (S1.05)",
        "stair": "stair enclosure has no ceiling (11/A6.01, 5/A6.02): board floor to floor / to underside of roof sheathing, not 'C.H. + 6\"' nor B.O. of a unit floor",
        "tile": "tile/backer to bath ceiling GYP-1 8'-6\" (unit RCPs, CRITERIOS 2)",
        "band": "band above tile = top of the face (line of structure 9'-3 1/2\" per A4.00/A0.08/CRITERIOS 3; L4 8'-11 1/4\" per 1/A5.06; FW = bath 8'-6\" + 6\" A0.06) - tile top 8'-6\"",
        "fw": "FW/FI head = LINE OF CEILING + 6\" printed on the FW and FI head details (A0.06), never above the line of structure (CRITERIOS 3)",
        "ext": "exterior gypsum sheathing continuous floor to floor (A0.07 rated rows; A0.09 / A5.01 wall sections; datums A4.00)",
        "mezz": "Mezzanine 219 roof height not printed (A3.02 / 5/A5.04): loaded F-F 11'-0\" (A4.00) with RFI",
    }
    t = why[c]
    if isinstance(t, dict):
        t = t["L2" if fl in ("L2", "L3") else fl]
    tol = " (within the ± 1/4\" tolerance)" if took.startswith("H-") and abs((va if took == "H-A" else vb) - h) > 1e-3 else ""
    return f"{t}. Taken: {took}{tol} -> {fi(h)}"


# ------------------------------------------------------------------ images (canon img fields may be absent: path by convention)
def wall_img(w):
    p = os.path.join(CAN, "img", "walls", w["id"].replace(" ", "_") + ".png")
    if os.path.isfile(p):
        return p
    q = abs_img(w.get("img"))
    return q if q and os.path.isfile(q) else sheet_img(w)


def sheet_img(w):
    c, fl, h = cat(w), w["floor"], w["height_ft"]
    if c == "shaft":
        n = "A5.08" if fl in ("L1", "L4") else "A9.03"
    elif c == "stair":
        n = "A6.01"
    elif c in ("tile", "band"):
        n = "A5.06" if fl == "L4" else "A7.00"
    elif c == "fw":
        r = fw_room(w)
        n = "A3.01" if fl == "L1" else {"corr": "A7.23", "ws1": "A7.23", "clean": "A3.02"}.get(r, "A5.06" if fl == "L4" else "A7.00")
    elif c in ("ext",):
        n = "A4.00"
    elif c == "mezz":
        n = "A5.04"
    elif fl == "L1":
        n = {12.115: "A5.03", 11.219: "A5.04", 12.063: "A7.31"}.get(round(h, 3), "A4.00")
    elif fl == "L4":
        n = "A5.06"
    else:
        n = "A7.23" if abs(h - 9.885) < .005 else "A4.00"
    p = SH(n)
    return p if os.path.isfile(p) else SH("A4.00")


# ------------------------------------------------------------------ build
ew = can["existing_walls"]
rows_a, rows_b, rows_f, res, disc, unk = [], [], [], [], [], []
for w in ew:
    img = wall_img(w)
    himg = sheet_img(w)
    va, sa, oa = lectura(w, A, "A")
    vb, sb, ob = lectura(w, B, "B")
    for rows, v, s, op in ((rows_a, va, sa, oa), (rows_b, vb, sb, ob)):
        rows.append({"Wall ID": w["id"], "Printed H": fi(v), "Source (N/SHEET)": s, "Operation": op,
                     "Status": ("DERIVED" if op else "CONFIRMED") if v is not None else "PENDING", "Image": img, "side": "", "faces": ""})
    st, op, src = final_op(w)
    if st is None:
        unk.append((w["id"], w["floor"], w["height_ft"], cat(w), w["height_source"][:120]))
        st, op, src = "CONFIRMED", "", w["height_source"][:200]
    rows_f.append({"Wall ID": w["id"], "Printed H": f"{w['height_ft']:g}", "Source (N/SHEET)": src, "Operation": op, "Status": st, "Image": himg, "side": "", "faces": ""})
    a_ok = va is not None and abs(va - w["height_ft"]) <= TOL
    b_ok = vb is not None and abs(vb - w["height_ft"]) <= TOL
    if not (va is not None and vb is not None and abs(va - vb) <= TOL):
        res.append({"Wall ID": w["id"], "H-A": fi(va), "H-B": fi(vb), "Final": fi(w["height_ft"]), "Resolution": resol(w, va, vb), "Image": himg})
    if not a_ok and not b_ok:
        disc.append((w["id"], w["type_id"], w["floor"], cat(w), w["height_ft"], va, vb, w["location"][:70]))

# corridor soffits (misc_items SOF-L2/L3/L4, 7/A7.23): one developed width PER SIDE (BE-CR37)
SOFIMG = os.path.join(OUT, "img_alturas", "A7.24_7A7.23_corridor_soffit.png")
for m in can["misc_items"]:
    if not str(m.get("ref", "")).startswith("SOF-"):
        continue
    lv = m["ref"].split()[0]
    for suf, side, faces, op, val, a, b in (
        ("DIF", "left", "bottom 7 3/4\" left; bottom 4 1/2\" left; drop 6 1/2\" left", "7 3/4\" + 4 1/2\" + 6 1/2\" = 1'-6 3/4\"", P("1'-6 3/4\""),
         (P("6 1/2\""), "ALTURAS_SOFFITS_A 216 CORRIDOR diffuser box (4/A7.23): '2\" + 4 1/2\" = 6 1/2\" per side' (symmetric both sides)", "2\" + 4 1/2\" = 6 1/2\"", "2\" drop left; 4 1/2\" bottom left"),
         (P("1'-2 1/4\""), "ALTURAS_SOFFITS_B corridors diffuser box side (7/A7.23): 'bottom 7 3/4\"+4 1/2\"=1'-0 1/4\"; drop 2\"'", "7 3/4\" + 4 1/2\" + 2\" = 1'-2 1/4\"", "bottom 7 3/4\" left; bottom 4 1/2\" left; drop 2\" left")),
        ("OPP", "right", "bottom 7 3/4\" right; bottom 4 1/2\" right; drop 4 1/2\" right", "7 3/4\" + 4 1/2\" + 4 1/2\" = 1'-4 3/4\"", P("1'-4 3/4\""),
         (P("6 1/2\""), "ALTURAS_SOFFITS_A 216 CORRIDOR diffuser box (4/A7.23): 'both (symmetric) ... 6 1/2\" per side'", "2\" + 4 1/2\" = 6 1/2\"", "2\" drop right; 4 1/2\" bottom right"),
         (P("1'-0 1/4\""), "ALTURAS_SOFFITS_B corridors opposite side (7/A7.23): 'width 7 3/4\" (+4 1/2\" panel); drop 4 1/2\"' developed '7 3/4\" + 4 1/2\"'", "7 3/4\" + 4 1/2\" = 1'-0 1/4\"", "bottom 7 3/4\" right; panel 4 1/2\" right"))):
        wid = f"SOF-{lv.split('-')[1]}-{suf}"
        rows_a.append({"Wall ID": wid, "Printed H": fi(a[0]), "Source (N/SHEET)": a[1], "Operation": a[2], "Status": "DERIVED", "Image": SOFIMG, "side": side, "faces": a[3]})
        rows_b.append({"Wall ID": wid, "Printed H": fi(b[0]), "Source (N/SHEET)": b[1], "Operation": b[2], "Status": "DERIVED", "Image": SOFIMG, "side": side, "faces": b[3]})
        rows_f.append({"Wall ID": wid, "Printed H": fi(val), "Source (N/SHEET)": f"7/A7.23 WALL DETAIL - CORRIDOR CEILING (drawn PDF p.67) printed 7 3/4\", 4 1/2\", 6 1/2\" / 4 1/2\"; {m['ref']} developed width per side (canon op: {m['op'][:80]})",
                       "Operation": op, "Status": "DERIVED", "Image": SOFIMG, "side": side, "faces": faces})
        res.append({"Wall ID": wid, "H-A": fi(a[0]), "H-B": fi(b[0]), "Final": fi(val),
                    "Resolution": f"7/A7.23 (crop): {side} ({'diffuser box' if suf == 'DIF' else 'opposite'}) side box prints {faces}; H-A read only the 2\" + 4 1/2\" step, H-B dropped the {'6 1/2\" drop (took 2\")' if suf == 'DIF' else '4 1/2\" drop'}; developed = {op}. Taken: neither (canon kept; ALTURAS_DISCREPANCIAS.md)",
                    "Image": SOFIMG})
        disc.append((wid, "SOF", lv.split('-')[1], "soffit", val, a[0], b[0], m["ref"]))

F = ["Wall ID", "Printed H", "Source (N/SHEET)", "Operation", "Status", "Image", "side", "faces"]
for n, rows in (("ALTURAS_IMPRESAS_A.csv", rows_a), ("ALTURAS_IMPRESAS_B.csv", rows_b), ("ALTURAS_IMPRESAS.csv", rows_f)):
    with open(os.path.join(OUT, n), "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=F); wr.writeheader(); wr.writerows(rows)

# ------------------------------------------------------------------ rooms
def rooms_rows(path, lect):
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        room, ch = r["Room"], r["Printed C.H."]
        if not re.search(r"\b\d{3}[A-Z]?\b", room) or re.search(r"(?i)passage|alcove", room):
            continue
        m = re.search(r"(\d+)'\s*-?\s*(\d+)?(?:\s+(\d+)/(\d+))?\s*\"", ch.replace("' - ", "'-"))
        if not m:
            continue
        v = int(m.group(1)) + (int(m.group(2) or 0) + (int(m.group(3)) / int(m.group(4)) if m.group(3) else 0)) / 12
        out.append({"Level": r["Level"], "Room": f"{room}", "Ceiling tag": r["Ceiling tag"], "C.H. (ft)": round(v, 4), "C.H.": fi(v),
                    "Source": f"{lect}: {r['Source']}", "Status": r["Status"]})
    # per room key: stacked / above / membrane rows first, the room's own ceiling last
    def peso(x):
        t = x["Room"].lower()
        if re.search(r"above|stacked|membrane|under mezzanine", t):
            return 0
        if re.search(r"lowered|slat|border|frame|closet|coffer|band|feature|storefront|ws-1 panel", t) or (x["Ceiling tag"].startswith("WS-1") and not re.search(r"lobby \(elevator|^\d{3} lobby$|bar", t)):
            return 1
        return 2
    return sorted(out, key=lambda x: (x["Level"], re.search(r"\d{3}", x["Room"]).group(0), peso(x)))


sys.path.insert(0, "/root/cr0/skill_s/take-off-metal-frame-drywall/tools")
import comparar_alturas as T  # noqa: E402

ra, rb = rooms_rows(f"{HA}/ALTURAS_ROOMS_A.csv", "H-A"), rooms_rows(f"{HB}/ALTURAS_ROOMS_B.csv", "H-B")
FR = ["Level", "Room", "Ceiling tag", "C.H. (ft)", "C.H.", "Source", "Status"]
for n, rows in (("ALTURAS_CUARTOS_A.csv", ra), ("ALTURAS_CUARTOS_B.csv", rb)):
    with open(os.path.join(OUT, n), "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=FR); wr.writeheader(); wr.writerows(rows)
json.dump({"res": res, "disc": [list(map(str, d)) for d in disc], "unk": unk}, open("/tmp/claude-0/-home-user/730b0376-7d3b-5320-9f37-d528f66b6f66/scratchpad/stage1.json", "w"), indent=0)
print("walls", len(ew), "A", len(rows_a), "B", len(rows_b), "final", len(rows_f), "resol", len(res), "disc", len(disc), "unk", len(unk))
for u in unk[:30]:
    print("UNK", u)

# ------------------------------------------------------------------ rooms: A/B comparison as the tool does it, final table, resolutions
la, lb = T.llaves_ab(T.leer_cuartos(os.path.join(OUT, "ALTURAS_CUARTOS_A.csv")), T.leer_cuartos(os.path.join(OUT, "ALTURAS_CUARTOS_B.csv")))
da, db = {}, {}
for k, v in la:
    da[k] = v
for k, v in lb:
    db[k] = v
RRES = {  # key -> (final C.H., resolution with N/SHEET, image)
    "109": (9.5, "A3.01 tag GYP-1 9'-6\" at Janitor 109 (canon ceilings row 'L1 Janitor 109 - GYP-1 9'-6\"'); H-A read no tag inside the grey ACT-3 extent", SH("A3.01")),
    "117": (9.5, "2/A7.50 ACT grid drawn, untagged, continuous with ACT-2 9'-6\" of Break 115 (A3.01); canon rcp_excluded 'Break 115, Office 117, Data 118B, Toilet 119 ... ACT-2 9'-6\"' (other trade)", SH("A7.50")),
    "118B": (9.5, "2/A7.50 ACT grid drawn, untagged, continuous with ACT-2 9'-6\" (Break 115); ACT = other trade (canon rcp_excluded)", SH("A7.50")),
    "119-bath": (9.5, "2/A7.50 ACT grid drawn, untagged, continuous with ACT-2 9'-6\"; ACT = other trade (canon rcp_excluded)", SH("A7.50")),
    "315": (P("9'-2\""), "1/A3.02 GYP-1 9'-2\" tag at Cleaning 215, 315 is the same stack (A3.03 untagged, stippled gyp) = FS-1 membrane 9'-2\" (canon ceilings 'L3 Cleaning 315')", SH("A3.02")),
    "217": (P("8'-0 1/2\""), "1/A7.23 WS-1 tag 8'-0 1/2\" at elevator Lobby 217 (H-B left it PENDING, no tag inside the lobby outline; the tag sits on the WS-1 field)", SH("A7.23")),
    "317": (P("8'-0 1/2\""), "2/A7.23 L3 view drawn identical to 1/A7.23 (Sim): WS-1 8'-0 1/2\" at Lobby 317", SH("A7.23")),
}
for k in ("401", "402", "403", "404", "405"):
    RRES[k] = (P("8'-11 1/4\""), "8'-11 1/4\" LEVEL 4 to bottom of roof assembly printed on 1/A5.06 and 1/A5.03 (unit general note 1 A7.00: untagged = bottom of assembly); H-B left L4 PENDING", SH("A5.06"))
room_res = []
for k in sorted(set(da) | set(db)):
    a, b = da.get(k), db.get(k)
    if a is not None and b is not None and abs(a - b) <= TOL:
        continue
    if k not in RRES:
        print("ROOM SIN RESOLUCION", k, a, b)
        continue
    v, t, im = RRES[k]
    room_res.append({"Wall ID": "ROOM " + k, "H-A": fi(a), "H-B": fi(b), "Final": fi(v), "Resolution": f"{t}. Taken: {fi(v)}", "Image": im})
# final rooms = H-A rows (both readings agree on every room both read) + the rooms only H-B printed (resolved above)
ka = {T.sala(r["Room"]) for r in ra}
fin_rooms = [dict(r, Source=r["Source"].replace("H-A:", "H-A = H-B:") if T.sala(r["Room"]) in db else r["Source"]) for r in ra]
fin_rooms += [dict(r, Source=r["Source"] + " (resolved: ALTURAS_AB_RESOLUCION.csv)") for r in rb if T.sala(r["Room"]) not in ka and not T.RX_NO_CUARTO.search(r["Room"])]
# H-B zones of a room H-A also read but with another printed ceiling (e.g. 412 WS-1 8'-0 1/2" at the elevator front): added as their own zone row
vals_a = {}
for r in ra:
    vals_a.setdefault(T.sala(r["Room"]), []).append(r["C.H. (ft)"])
for r in rb:
    k = T.sala(r["Room"])
    if k in ka and not T.RX_NO_CUARTO.search(r["Room"]) and not re.search(r"(?i)stacked|membrane|above", r["Room"]) \
            and all(abs(r["C.H. (ft)"] - v) > TOL for v in vals_a.get(k, [])):
        tag = r["Ceiling tag"].split()[0]
        fin_rooms.insert(0, dict(r, Room=f"{r['Room']} - {tag} zone" + (" at elevator front" if k == "412" and tag == "WS-1" else ""),
                                 Source=r["Source"] + " (zone printed by H-B only; same RCP sheet)"))
for r in fin_rooms:
    k = T.sala(r["Room"])
    if k in RRES and r["Source"].startswith("H-A") and "(resolved" not in r["Source"]:
        r["Source"] += " (A != B resolved: ALTURAS_AB_RESOLUCION.csv)"
fin_rooms.sort(key=lambda x: (x["Level"], re.search(r"\d{3}", x["Room"]).group(0)))
with open(os.path.join(OUT, "ALTURAS_CUARTOS.csv"), "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=FR); wr.writeheader(); wr.writerows(fin_rooms)

RF = ["Wall ID", "H-A", "H-B", "Final", "Resolution", "Image"]
with open(os.path.join(OUT, "ALTURAS_AB_RESOLUCION.csv"), "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=RF); wr.writeheader(); wr.writerows(res + room_res)

# ------------------------------------------------------------------ discrepancies (canon vs BOTH readings)
L = ["# HEIGHT DISCREPANCIES - canon vs both blind readings (U-176 control 1)", "",
     "Canon `takeoff_canon.json` NOT edited. These are the Wall IDs where the canon height matches NEITHER blind reading H-A nor H-B (± 1/4\").",
     "A blank value = that reading's tables give no height for the face (room C.H. not printed / PENDING). The final table "
     "(ALTURAS_IMPRESAS.csv) carries the canon value with its printed N/SHEET; each row also has a line in ALTURAS_AB_RESOLUCION.csv.", "",
     f"Total: {len(disc)}", "", "| Wall ID | Type | Level | Category | Canon | H-A | H-B | Location / item |", "|---|---|---|---|---|---|---|---|"]
for d in disc:
    L.append(f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {fi(d[4])} | {fi(d[5])} | {fi(d[6])} | {d[7].replace('|', '/')} |")
L += ["", "## Groups", ""]
import collections
g = collections.Counter((d[2], d[3], fi(d[4]), fi(d[5]), fi(d[6])) for d in disc)
for (lv, c, h, a, b), n in sorted(g.items()):
    L.append(f"- {lv} {c}: {n} item(s) canon {h} vs H-A {a or '(none)'} / H-B {b or '(none)'}")
open(os.path.join(OUT, "ALTURAS_DISCREPANCIAS.md"), "w").write("\n".join(L) + "\n")
print("room_res", len(room_res), "rooms final", len(fin_rooms))
