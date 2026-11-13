"""CR City Hotel rev20 / U-189 (2) (v81cf103 CB_DETALLE_CARAS): todo detalle que gobierna un SOF- / BW- lleva su revisión CARA POR CARA en
canon.detail_faces: TODAS las caras dibujadas (incluidas las que suben al plenum), cada una con el renglón que la carga ('loaded', primer
token = ref del canon) o su none_reason. Fuentes: 7/A7.23 (lecturas H-A / H-B rev20 + auditoría U-181), 12/A9.03 (U-181: 5 caras),
5/A7.31 + 2/3/4/7/A7.31 (coffers, borde exterior medido rev20), 7/A6.01 + 11/A6.01 (FCU L4), 3/S3.02 + A3.01 (beam wraps)."""
import json

CP = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
C = json.load(open(CP))
W_ = "wood per 7/A7.23 (box with X = wood blocking, same symbol as the wall top plates): Div. 06 EXCLUDED (COVE-7A723, R-ALC-10 / U-139; delta if metal in wood_excluded_cove)"
CORR_RCP = [{"face": "band run (1'-0\" bands along both corridor walls)", "dim": "1' - 0\"", "loaded": "SOF-L2-01 board / SOF-L2-02 / SOF-L3-316 / SOF-L3-318 / SOF-L4-02"},
            {"face": "plenum face of the right-hand box (one side)", "dim": "11 5/8\"", "loaded": "SOF-L2-01P board / SOF-L2-02P / SOF-L3-316P / SOF-L3-318P / SOF-L4-02P"},
            {"face": "GYP-1 8'-11\" field between the bands", "dim": "8' - 11\"", "loaded": "CLG-L2-56 board / CLG-L2-58 / CLG-L3-87 / CLG-L3-88 (L4 412: RS-1 ceilings[])"},
            {"face": "WS-1 wood slat panels", "dim": "WS-1", "none_reason": "WS-1 wood slat ceiling, USG specialty, other trade (deducted from the GYP-1 field rows)"}]
def LOBBY(lv, rm):
    return [{"face": f"vestibule 1'-0\" band loop (lobby {rm})", "dim": "1' - 0\"", "loaded": f"SOF-{lv}-{rm}V board"},
            {"face": f"gypsum border box around WS-1 (lobby {rm})", "dim": "1' - 4 1/2\"", "loaded": f"SOF-{lv}-{rm}B board"},
            {"face": f"dropped GYP-1 field of the lobby / vestibule / corridor strip ({rm})", "dim": "8' - 11\"", "loaded": f"CLG-{lv}-{rm}F board"}]


DF = [
    {"detail": "7/A7.23", "title": "WALL DETAIL - CORRIDOR CEILING", "faces": [
        {"face": "corridor face of each box (both sides)", "dim": "6 1/2\"", "loaded": "SOF-L2-01 board (x 1.9375 per side; same rows L2 / L3 / L4)"},
        {"face": "box bottom (both sides)", "dim": "4 1/2\"", "loaded": "SOF-L2-01 board"},
        {"face": "box face toward the cove (both sides)", "dim": "4 1/2\"", "loaded": "SOF-L2-01 board"},
        {"face": "cove bottom (both sides)", "dim": "7 3/4\"", "loaded": "SOF-L2-01 board"},
        {"face": "right-hand box corridor face ABOVE the GYP-1 field (plenum)", "dim": "9 1/2\" + 2 1/8\"", "loaded": "SOF-L2-01P board (0.9688 ft, one side)"},
        {"face": "left-hand (diffuser) box above the field", "dim": "-", "none_reason": "no board face drawn above the field (only dashed lines + wood blocking), H-A / H-B rev20"},
        {"face": "GYP-1 ceiling field 3'-11\" at 8'-11\" A.F.F., hanger wire drawn", "dim": "3' - 11\"", "loaded": "CLG-L2-56 board (+ main tee / cross tee / angle molding / hanger wire)"},
        {"face": "1'-1 3/8\" RATED ASSEMBLY membrane above", "dim": "1' - 1 3/8\"", "loaded": "FS-1 (ceilings[] corridors 216 / 218 / 316 / 318, Type C on RC)"},
        {"face": "face against the corridor wall", "dim": "-", "none_reason": "'WOOD WALL PANEL RE: ELEVATIONS' (not drywall)"},
        {"face": "DIFFUSER BOX 5 1/4\"", "dim": "5 1/4\"", "none_reason": "HVAC diffuser box; band loaded gross, Review Item -28.44 SF"},
        {"face": "box / cove framing members", "dim": "-", "none_reason": W_}]},
    {"detail": "1/A7.23", "title": "ENLARGED RCP N-S - LEVEL 2", "faces": CORR_RCP + LOBBY("L2", "217")},
    {"detail": "2/A7.23", "title": "ENLARGED RCP N-S - LEVEL 3", "faces": CORR_RCP + LOBBY("L3", "317")},
    {"detail": "5/A7.23", "title": "WOOD SLAT DETAIL", "faces": [
        {"face": "border box outer face (8'-0\" border to 8'-11\" field)", "dim": "11\"", "loaded": "SOF-L2-217B board / SOF-L3-317B"},
        {"face": "border box bottom", "dim": "4 1/2\"", "loaded": "SOF-L2-217B board"},
        {"face": "border box inner face at the slats", "dim": "11\"", "loaded": "SOF-L2-217B board"},
        {"face": "WS-1 slats, battens, DX grid, hanger wire 'BY OTHERS'", "dim": "-", "none_reason": "WS-1 wood slat ceiling (USG specialty, other trade, U-061)"}]},
    {"detail": "6/A7.23", "title": "WOOD SLAT DETAIL 2", "faces": [
        {"face": "border box (both faces + bottom)", "dim": "4 1/2\"", "loaded": "SOF-L2-217B board / SOF-L3-317B"},
        {"face": "WS-1 slats / black fabric", "dim": "-", "none_reason": "WS-1 wood slat ceiling (other trade, U-061)"}]},
    {"detail": "4/S3.08", "title": "SECTION AT GRID 1 (north edge beam)", "faces": [
        {"face": "beam south side face below the truss bottom", "dim": "d - 16 1/2\"", "loaded": "BW-L1-NORTH board"},
        {"face": "beam bottom", "dim": "bf", "loaded": "BW-L1-NORTH board"},
        {"face": "beam north face", "dim": "-", "none_reason": "covered by the exterior wall sheathing / pack-out (4/S3.08)"},
        {"face": "wood nailer / 2x6 bearing wall", "dim": "-", "none_reason": "Div. 06 wood (not our scope)"}]},
    {"detail": "3/A7.23", "title": "ENLARGED RCP N-S - LEVEL 4", "faces": CORR_RCP},
    {"detail": "1/A7.24", "title": "ENLARGED RCP E-W - LEVEL 2", "faces": CORR_RCP},
    {"detail": "3/A7.24", "title": "ENLARGED RCP E-W - LEVEL 4", "faces": CORR_RCP},
    {"detail": "1/A3.04", "title": "LEVEL 4 RCP", "faces": [{"face": "corridor 412 soffit double line (run measured 343.67 LF)", "dim": "-", "loaded": "SOF-L4-02 board"},
                                                         {"face": "plenum face, one side", "dim": "11 5/8\"", "loaded": "SOF-L4-02P board"}]},
    {"detail": "12/A9.03", "title": "WALL DETAIL - SMOKE CURTAIN", "faces": [
        {"face": "outer face", "dim": "14.87\" measured", "loaded": "SOF-L2-SCN board (5.04 ft, all 6 SC rows)"},
        {"face": "bottom", "dim": "4.49\" measured", "loaded": "SOF-L2-SCN board"},
        {"face": "inner face", "dim": "14.37\" measured", "loaded": "SOF-L2-SCN board"},
        {"face": "return", "dim": "3.00\" measured", "loaded": "SOF-L2-SCN board"},
        {"face": "shaft-side face on wood blocks (in front of the MASONRY SHAFT WALL)", "dim": "23.73\" measured", "loaded": "SOF-L2-SCN board (U-181 rev20: added)"},
        {"face": "9\" gray piece under the housing / black element below the shaft-side face", "dim": "-", "none_reason": "not drawn with the gypsum hatch; smoke-curtain housing / equipment (other trade)"}]},
    {"detail": "5/A7.31", "title": "DETAIL - LOBBY CEILING", "faces": [
        {"face": "downstand face (each coffer side)", "dim": "10 3/4\"", "loaded": "SOF-L1-01 board (1.25 ft per LF of coffer perimeter)"},
        {"face": "downstand bottom shared by two coffers", "dim": "7 1/2\" + 2 x 1/2\"", "loaded": "SOF-L1-01 board (half per LF; Review Item -104.77 SF possible double count with CLG-L1-12)"},
        {"face": "cripple studs of the downstand", "dim": "10 3/4\"", "loaded": "SOF-L1-01 cripples"},
        {"face": "1'-10\" border with 'PLASTER FINISH, RE: INTERIORS'", "dim": "1' - 10\"", "none_reason": "drawn as wood border / plaster finish by interiors (not gypsum board)"}]},
    {"detail": "1/A7.31", "title": "LOBBY RCP", "faces": [
        {"face": "coffer perimeters (10 coffers)", "dim": "295.83 LF", "loaded": "SOF-L1-01 board"},
        {"face": "outer edge of the coffer field (124.92 LF)", "dim": "-", "none_reason": "rev20 measured: bottom continues flat at 11'-0\" into CLG-L1-12 (no outer face, no step; 2/A7.31, 3/A7.31): 0 SF to add"},
        {"face": "flat GYP-1 11'-0\" ceiling", "dim": "11' - 0\"", "loaded": "CLG-L1-12 board"}]},
    {"detail": "2/A7.31", "title": "LOBBY SECTION", "faces": [
        {"face": "coffer top 12'-0 3/4\" (underside of the rated assembly)", "dim": "12' - 0 3/4\"", "loaded": "FS-1 (ceilings[] L1 FS-1 membrane under the LEVEL 2 floor)"},
        {"face": "1'-0 3/4\" DROPPED SOFFIT", "dim": "1' - 0 3/4\"", "loaded": "SOF-L1-01 board"},
        {"face": "flat ceiling 11'-0\"", "dim": "11' - 0\"", "loaded": "CLG-L1-12 board"}]},
    {"detail": "4/A7.31", "title": "LOBBY SECTION", "faces": [
        {"face": "1'-0 3/4\" DROPPED SOFFIT", "dim": "1' - 0 3/4\"", "loaded": "SOF-L1-01 board"},
        {"face": "coffer top", "dim": "12' - 0 3/4\"", "loaded": "FS-1 (ceilings[] L1 FS-1 membrane)"}]},
    {"detail": "7/A7.31", "title": "LOBBY CEILING DETAIL", "faces": [
        {"face": "12'-0 3/4\" coffer top", "dim": "12' - 0 3/4\"", "loaded": "FS-1 (ceilings[] L1 FS-1 membrane)"},
        {"face": "11'-0\" ceiling", "dim": "11' - 0\"", "loaded": "CLG-L1-12 board"}]},
    {"detail": "7/A6.01", "title": "STAIR SECTION (FCU soffit run)", "faces": [
        {"face": "GYP BD SOFFIT AT FCU run", "dim": "8' - 8 3/4\"", "loaded": "SOF-L4-01 board"}]},
    {"detail": "11/A6.01", "title": "GYP BD SOFFIT AT FCU", "faces": [
        {"face": "soffit bottom", "dim": "6.59 ft measured", "loaded": "SOF-L4-01 board"},
        {"face": "FCU face", "dim": "2.0 ft measured", "loaded": "SOF-L4-01 board"},
        {"face": "cripples", "dim": "2.0 ft", "loaded": "SOF-L4-01 cripples"}]},
    {"detail": "3/S3.02", "title": "BEAM / TRUSS CONNECTION", "faces": [
        {"face": "beam wrap (FS-1 membrane continuity, A5.00 / A0.08)", "dim": "d - 19.25\" + 1 1/8\"; bf + 2 1/4\"", "loaded": "BW-L1-RETAIL board"},
        {"face": "CONT. 2x NAILER / TOP MOUNT TRUSS HANGER", "dim": "-", "none_reason": "wood nailer / hanger: Div. 06 (structural), not our scope"}]},
]
# v81cf119 (post-mortem 12b, CB_DETALLE_CARAS): 'loaded' = refs EXACTAS del canon separadas por coma; el texto explicativo pasa a 'loaded_note'
import re as _re
_REFS = {str(m.get('ref')) for m in C.get('misc_items') or []} | {str(w.get('id')) for w in (C.get('existing_walls') or []) + (C.get('walls') or [])}
_CEI = [(i, str(c.get('room'))) for i, c in enumerate(C.get('ceilings') or [])]


def _exactas(ld):
    out = []
    for t in _re.findall(r"\b(?:SOF|CLG|BW|CW|CAN)-[A-Z0-9]+(?:-[A-Z0-9]+)*\b", ld):
        for c in (t, f"{t} board"):
            if c in _REFS:
                out.append(c); break
    if _re.search(r"FS-1|RS-1|ceilings\[", ld):
        rooms = _re.findall(r"\b([1-4]\d{2})\b", ld)
        if _re.search(r"L1 FS-1 membrane", ld):
            out += [f"ceilings[{i}]" for i, r in _CEI if r.startswith('L1 FS-1 membrane')]
        for rn in rooms:
            out += [f"ceilings[{i}]" for i, r in _CEI if _re.search(rf"\b{rn}\b", r) and ('Corridor' in r or 'Lobby' in r or 'L4' in r)]
    return list(dict.fromkeys(out))


for _d in DF:
    for _f in _d.get('faces') or []:
        _ld = str(_f.get('loaded') or '').strip()
        if not _ld:
            continue
        _tok = [x.strip() for x in _re.split(r"\s*[,;+]\s*", _ld) if x.strip()]
        if all(x in _REFS or _re.fullmatch(r"ceilings\[\d+\]", x) for x in _tok):
            continue
        _ex = _exactas(_ld)
        if _ex:
            _f['loaded_note'] = _ld
            _f['loaded'] = ", ".join(_ex)
C['detail_faces'] = DF
json.dump(C, open(CP, 'w'), indent=1)
print(f"detail_faces: {len(DF)} detalles, {sum(len(d['faces']) for d in DF)} caras")

# v81cf104 CB_RCP_TAGS (U-189): TODO tag de cielo impreso en un plano RCP (ACT / WS además de GYP) lleva renglón o none_reason con N/HOJA.
# Los ACT-n / WS-1 que faltaban: motivo 'by others' + la membrana rated de arriba (cargada). La vista N/HOJA = el título de vista más
# cercano DEBAJO del tag (mismo rango horizontal).
import re
import sys
import pymupdf as fitz
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import chequeos_biblioteca as CB  # noqa: E402

W = '/root/cr/work'
C = json.load(open(CP))
H = json.load(open(f'{W}/set_texto.json')).get('hojas') or {}
PG = {x['sheet']: x['page'] - 1 for x in json.load(open(f'{W}/etapas/1_inventario/paginas_hojas.json'))['sheets']}
doc = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
C['rcp_tags'] = [x for x in C.get('rcp_tags') or [] if not x.get('rev20_v104')]
cnt = {}
for x in C['rcp_tags']:
    k = (x['sheet'], re.sub(r"\s+", "", str(x['tag'])).upper()); cnt[k] = cnt.get(k, 0) + 1
RATED = {'A3.01': "L1 FS-1 membrane under the LEVEL 2 floor (ceilings[], A0.08 'LEVEL 2, 3, 4 FS-1 THROUGHOUT')"}
QUE = {'ACT': "lay-in acoustical ceiling (ACT, other trade, U-061)", 'WS': "WS-1 wood slat ceiling, USG specialty (other trade, U-061)"}
nuevos = []


def vista(p, x, y):
    best = None
    for b in p.get_text('blocks'):
        m = re.search(r"(?:^|\n)\s*(\d{1,2})\s*\n?\s*([A-Z][A-Z0-9 .,'/&-]{3,})", b[4])
        if not m or not re.search(r"(?i)RCP|PLAN|DETAIL|SECTION|ELEVATION|CEILING", m.group(2)):
            continue
        if b[1] > y and b[0] - 400 < x < b[2] + 900:
            d = b[1] - y
            if best is None or d < best[0]:
                best = (d, m.group(1), m.group(2).strip()[:60])
    return best


for h, t in sorted(H.items()):
    t = t if isinstance(t, str) else str(t or "")
    if not (CB.RX_HOJA_RCP.search(t) and CB.RX_PLAN_RCP.search(t)) or h not in PG:
        continue
    for tag, n in sorted(CB.tags_cielo(t).items()):
        fal = n - cnt.get((h, tag), 0)
        if fal <= 0 or not tag.startswith(('ACT', 'WS')):
            continue
        p = doc[PG[h]]
        ws = [w for w in p.get_text('words') if w[4] == tag]
        for w in ws[:fal]:
            v = vista(p, w[0], w[1])
            nh = f"{v[1]}/{h}" if v else h
            sigue = " ".join(x[4] for x in p.get_text('words') if abs(x[1] - w[3]) < 12 and abs(x[0] - w[0]) < 40 and x[1] > w[1])[:20]
            nuevos.append({"sheet": h, "tag": tag, "height": sigue, "xy": [round(w[0]), round(w[1])], "rows": [], "rev20_v104": True,
                           "none_reason": f"{nh}{' (' + v[2] + ')' if v else ''}: {tag} = {QUE[tag[:3].rstrip('-')]} - not gypsum; the rated "
                                         f"membrane above is loaded ({RATED.get(h, 'FS-1 / RS-1 ceilings[] of the room')})"})
C['rcp_tags'] += nuevos
json.dump(C, open(CP, 'w'), indent=1)
print(f"rcp_tags v104: + {len(nuevos)} ACT / WS con motivo N/HOJA")
for x in nuevos:
    print("  ", x['sheet'], x['tag'], x['height'], x['none_reason'][:90])

# v81cf96+ CE_CAMPOS_CANON (U-137) y CB_U_184_ELEV (U-184 (4)) - campos que la compuerta usa; sin ellos los chequeos pasarían en vacío
C = json.load(open(CP))
C['rated_floor_assemblies'] = [{"id": "FS-1", "levels": ["LEVEL 2", "LEVEL 3", "LEVEL 4"],
                                "source": "A0.08 FS-1 'LEVEL 2, 3, 4 FS-1 THROUGHOUT' (5/8\" Type C on RC, UL L546); membrane = ceilings[] of L1 / L2 / L3"}]
C['rated_floor_assemblies_note'] = ("Roof assemblies are not floor assemblies: RS-1 (A0.08, board on channel) is loaded as the L4 ceilings[] and over the "
                                    "L4 baths (CLG-L4-1xxR); RS-2 / RS-3 / RS-5 / RS-7 carry no board (ALC-25)")
C.pop('typical_floors', None); C.pop('stack_reasons', None)
C['typical_floors_none_reason'] = ("No typical-floor copy is used: L2, L3 and L4 are quantified wall by wall and room by room from their own plans "
                                   "(A2.02 / A2.03 / A2.04, A3.02-A3.04); L2 carries the mezzanine 219 and the lobby elevator zone, L3 the RS-6 terrace strip, L4 the roof RS-1")
C['stack_reasons_none_reason'] = "No stacked-floor comparison applies (typical_floors_none_reason)"
PC = {r"TOP OF LEVEL 2 FLOOR ELEVATION": "A2.01 plan: 'ELEVATION' here is the S1.02 level datum (TOP OF LEVEL 2 FLOOR), not an elevation drawing; the wall is located on 1/A2.01",
      r"1/A5\.06": "A2.04 plan: the wall is on the exterior facade line of L4 under the pitched roof eave (A2.05 roof plan slopes to this wall; 1/A4.05 cuts it)",
      r"3/A5\.07": "A2.04 plan: north wall of F&B 410 at grid 8 = the plane cut by 3/A5.07",
      r"2/A5\.04": "A2.02 plan: gable end walls (east / west) of the mezzanine 219 = the plane of section 2/A5.04"}
n = 0
for w in C.get('walls', []) + C.get('existing_walls', []):
    s_ = " ".join(str(w.get(k) or "") for k in ("height_source", "height_op"))
    if re.search(r"(?i)\belev(?:ation)?s?\b|\bEAVE\b", s_) and not re.search(r"\b[A-Z]{1,2}\d{1,2}\.\d{1,2}", str(w.get("height_plan_check") or "")):
        for rx_, txt in PC.items():
            if re.search(rx_, s_):
                w['height_plan_check'] = txt; n += 1
                break
json.dump(C, open(CP, 'w'), indent=1)
print(f"campos canon v105: rated_floor_assemblies FS-1, typical_floors / stack_reasons none_reason; height_plan_check {n}")

# UL L546 (COORDINACIÓN 12-nov, U-172 / U-155: el espaciamiento lo dice la listing): FS-1 -> RC 12 in. OC (Items 5 / 6, A0.08 'FULL CAVITY
# INSULATION') + dos canales a 6 in. en cada junta de testa del board (Item 6) = +1 canal cada 12 ft (board de 12 ft, 09 29 00).
C = json.load(open(CP))
L546 = ("UL L546 (Design No. L546, 2025-07-01) Item 6 'spaced 16 in. OC ... When insulation (Items 5, 5A, 5B) is draped over the resilient "
        "channel/gypsum board ceiling membrane, the spacing shall be reduced to 12 in. OC'; Item 5: at 16 in. OC insulation max 3-1/2 in.; A0.08 FS-1 "
        "'RESILIENT CHANNELS, SPACING PER ASSEMBLY TO ACHIEVE FULL CAVITY INSULATION' (18 in. trusses) -> 12 in. OC (RFI-14 closed)")
area = {}
for c in C['ceilings']:
    if (c.get('assembly') or {}).get('id') == 'FS-1' and c.get('system') == 'resilient_channel':
        c['rc_oc_in'] = {"value": 12, "source": L546}
        fl = str(c.get('floor') or str(c['room'])[:2])
        area[fl] = area.get(fl, 0) + float(c.get('area_sf') or 0)
C['misc_items'] = [m for m in C['misc_items'] if not str(m.get('ref', '')).startswith('RC-FS1-ENDJ')]
for fl, a in sorted(area.items()):
    q = round(a / 12, 2)
    C['misc_items'].append({"ref": f"RC-FS1-ENDJ-{fl} RC", "familia": "resilient channel (printed)", "qty": q, "detail": "A0.08 FS-1 / UL L546",
                            "op": f"{round(a, 2)} SF FS-1 ceilings {fl} / 12 ft (one end-joint line of 12 ft boards) = {q} LF (extra channel of the pair)",
                            "source": "UL L546 Item 6 'Two channels, spaced 6 in OC, oriented opposite each gypsum board end joint' (one extra channel per end "
                                      "joint; boards 12 ft long, 09 29 00 'minimize the number of abutting end joints' [DERIVED])"})
json.dump(C, open(CP, 'w'), indent=1)
print("UL L546: FS-1 RC 12 in. OC;", {k: round(v / 12, 1) for k, v in area.items()})
