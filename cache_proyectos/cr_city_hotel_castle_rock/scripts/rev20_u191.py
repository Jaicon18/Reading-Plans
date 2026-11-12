"""CR City Hotel rev20 (U-191 / BE-CR41, v81cf109 CB_U_191_REF): every source that cites a UL listing or 'per assembly' carries the
item of the listing that supports what is loaded. Listings opened (UL Product iQ copies, scratchpad ul_*):
  UL L546 (2025-07-01): Item 2 trusses; Item 5 batts (16 in. OC -> max 3-1/2 in.; max 12 in. OC -> no limit, draped over the membrane);
           Item 6 resilient channels 16 in. OC, 12 in. OC when insulation is draped over the RC / gypsum membrane, two channels 6 in. OC
           at each end joint; Item 7 5/8 in. gypsum board perpendicular to the RC.
  UL U415 (2022-02-14): Item 1 'J' runner; Item 2 'C-H' studs min 2-1/2 in., min 25 MSG, 24 in. OC; Item 3 1 in. liner panels;
           Item 4 System B 2 Hr (two layers).
  UL U301 (2025-05-09): Item 4 5/8 in. gypsum board, two layers each side.
  RS-1 (A0.08): UL # blank (RE: A2.05) = no listing -> RC spacing per spec 09 22 16 3.1.A ('ASTM C 754, except comply with framing
           sizes and spacing indicated').
Also: the FS-1 misc RC rows still at 16 in. OC go to 12 in. OC (UL L546 Item 6 with A0.08 FS-1 'FULL CAVITY INSULATION').
Idempotent (re-reads the canon; replacements only add text once)."""
import json
import re
import sys

sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import chequeos_biblioteca as CB  # noqa: E402

P = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
C = json.load(open(P))
SPEC_RS1 = "RS-1 has no UL # on A0.08 (RE: A2.05): RC spacing per spec 09 22 16 3.1.A (ASTM C 754, spacing indicated)"
SEP = re.compile(r"(\s*(?:\||;|\n)\s*)")


def arreglar_seg(s, rs1):
    if not CB.RX_REF_EXT.search(s) or CB.RX_CITA_ITEM.search(s):
        return s
    if rs1 and 'FS-1' not in s and re.search(r"(?i)L546|per\s+assembly", s):
        s = re.sub(r"UL L546 / (RS-1|RFI-14)", r"\1", s)
        s = re.sub(r"\(?spacing 'per assembly', not printed\)?:?", "", s)
        s = re.sub(r"UL L546 \((?=\s*\))", "(", s)
        s = s.replace("UL L546", "RS-1").replace("(RS-1 ", "(")
        s = s.rstrip() + f" [{SPEC_RS1}]"
    s = re.sub(r"UL U415\b(?! \(Item)", "UL U415 (Item 2 C-H stud min 2-1/2 in. 25 MSG 24 in. OC, Item 1 J runner, Item 3 1 in. liner, Item 4 System B)", s)
    s = re.sub(r"UL U301\b(?! Item)", "UL U301 Item 4 (5/8 in. Type X, two layers each side)", s)
    if re.search(r"UL L546\b(?! Item)", s):
        if re.search(r"(?i)channel|\bRC\b|spacing|wrap", s):
            it = "Item 6"
        elif re.search(r"(?i)board|gyp|type c", s):
            it = "Item 7"
        else:
            it = "Item 6 / Item 7"
        s = re.sub(r"UL L546\b(?! Item)", f"UL L546 {it}", s)
    if CB.RX_REF_EXT.search(s) and not CB.RX_CITA_ITEM.search(s) and re.search(r"(?i)per\s+assembly", s):
        s = s.rstrip() + " (= UL L546 Item 6 + Item 5: 12 in. OC with the insulation draped over the membrane)"
    return s


CH_W419_U497 = ("UL W419 Item 2A / UL U497 Item 2A: C-H stud min 2-1/2 in., min 25 MSG, 24 in. o.c.; Item 1 J channel track; "
                "Item 3 1 in. liner panels")


def endurecer_seg(s, rs1):
    """v81cf114 (BE-AUD05): 'L546' / 'W419' / 'U497' sueltos también son listings -> 'Item N'; un renglón de RC / channel con listing
    lleva además 'N in. o.c.' (FS-1 12 in. o.c. UL L546 Item 6; RS-1 16 in. o.c., spec 09 22 16 3.1.A)."""
    if CB.falta_cita_u191(s) is None or not CB.falta_cita_u191(s):
        return s
    if re.search(r"(?<![\w./-])(?:W419|U497)(?![\w./-])", s) and "Item 2A" not in s:
        s = re.sub(r"\((?:UL )?W419, (?:UL )?U497\)", f"({CH_W419_U497})", s)
        if "Item 2A" not in s:
            s = s.rstrip() + f" [{CH_W419_U497}]"
    if not CB.RX_UL_ITEM.search(s):                    # 'L546' suelto (sin 'UL') también es el listing
        s = re.sub(r"(?<![\w./-])(?<!UL )L546(?![\w./-]|\.\d)", "UL L546", s)
    if re.search(r"(?i)\bUL\s*L546\b", s) and not CB.RX_UL_ITEM.search(s):
        s = re.sub(r"(?i)\bUL\s*L546\b", "UL L546 Item 6 / Item 7", s, count=1)
    f = CB.falta_cita_u191(s) or []
    if any('o.c.' in x for x in f):
        s = s.rstrip() + (" (16 in. o.c.: RS-1, spec 09 22 16 3.1.A)" if rs1 and 'FS-1' not in s
                          else " (12 in. o.c. + 2 channels 6 in. apart at end joints, UL L546 Item 6)")
    return s


def arreglar(t, rs1):
    return "".join(x if SEP.fullmatch(x) else endurecer_seg(arreglar_seg(x, rs1), rs1) for x in SEP.split(t))


# 1) FS-1 misc RC rows at 16 in. -> 12 in. (UL L546 Item 6)
n12 = 0
for m in C['misc_items']:
    op = str(m.get('op') or '')
    mm = re.match(r"([\d.]+) SF x 12 / 16 in\. o\.c\. = [\d.]+ LF", op)
    if str(m['ref']).endswith(' RC') and mm and 'FS-1' in str(m.get('source')) and '-L4-' not in m['ref']:
        sf = float(mm.group(1))
        m['qty'] = round(sf, 2)
        m['op'] = f"{sf} SF x 12 / 12 in. o.c. = {round(sf, 2)} LF (UL L546 Item 6: 12 in. OC, insulation draped over the membrane, A0.08 FS-1 'FULL CAVITY INSULATION')"
        m['source'] = str(m['source']).replace("resilient channel 16 in. o.c. (UL L546 / FS-1, as the unit rows; RFI-14)",
                                               "resilient channel 12 in. o.c. (UL L546 Item 6 / FS-1; RFI-14 closed)")
        n12 += 1

# 2) item / paragraph of every cited document
nf = 0
for k in ("misc_items", "walls", "existing_walls", "ceilings", "trim_items"):
    for x in C.get(k) or []:
        if not isinstance(x, dict):
            continue
        ide = str(x.get('ref') or x.get('id') or x.get('room') or '')
        _a = x.get('assembly')
        rs1 = bool(re.search(r"-L4-|^L4 ", ide)) or (isinstance(_a, dict) and _a.get('id') == 'RS-1')
        for c in ("source", "op", "assumption", "note", "height_source", "length_source"):
            if x.get(c):
                v = arreglar(str(x[c]), rs1)
                nf += v != x[c]
                x[c] = v
        for c in ("rc_oc_in", "layers", "assembly"):
            v = x.get(c)
            if isinstance(v, dict) and v.get("source"):
                w = arreglar(str(v["source"]), rs1)
                nf += w != v["source"]
                v["source"] = w
# v81cf116: el rendimiento de tornillos del estimador citaba 'GA-216' sin sección (default de accesorios.py): mismo valor 1.2 / SF,
# cita al párrafo del spec del proyecto (09 29 00 3.3.O.1)
C.setdefault('constants', {})['drywall_screws_per_sf'] = {"value": 1.2, "source": "Estimator yield, Inputs!B20 (1.2 screws / SF of board); "
    "screw spacing per spec 09 29 00 3.3.O.1 'Space screws a maximum of 12 inches (304.8 mm) o.c. for vertical applications'"}
json.dump(C, open(P, 'w'), indent=1, ensure_ascii=False)
quedan = [(d, s) for d, t in CB._textos_u191(C) if not d.startswith('rfis:') for s in re.split(r"\s*(?:\||;|\n)\s*", t)
          if CB.falta_cita_u191(s)]                       # v81cf114: misma regla que CB_U_191_REF
print(f"U-191: FS-1 RC rows -> 12 in.: {n12}; fields cited with item: {nf}; left (no rfis): {len(quedan)}")
for d, s in quedan[:10]:
    print("  ", d, "::", s[:160])
