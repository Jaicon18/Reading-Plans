"""Evidence fields only (no quantities): RFI source + image (G_RFI), top-track condition of the metal walls
(G_TOPTRACK) and the tick type of the printed M3.5-01 / M3.5-02 dimensions (G_CADENA), written into the reconciled
canon. Images: the crop of the resolution (3_revision/img) when the RFI has one, otherwise the full sheet cited first
in its source rendered from the clean PDF (same 40 dpi as runner/evidencia.py).
Use: python3 bitacora.py run scripts/evidencia_rfis.py <clean.pdf>"""
import json, os, re, sys
import pymupdf as fitz
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
doc = fitz.open(sys.argv[1])
smap = {v: int(k) - 1 for k, v in json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json"))).items()}
HOJA = re.compile(r"\b([A-Z]{1,2}-\d{3})\b")
CROP = {"RFI-01": "img/r10_A2_A605.png", "RFI-07": "img/r03_S241_C3_overview.png", "RFI-08": "img/r03_S241_A2_A3_schedule.png",
        "RFI-09": "img/r03_S241_A2_A3_schedule.png", "RFI-10": "img/r06_S201_kitchen_east.png", "RFI-13": "img/r10_A2_A605.png",
        "RFI-14": "img/r04_A1_A604_roofhatch.png", "RFI-15": "img/r04_C3_S801_strongback.png", "RFI-16": "img/r01_A202_wall_legend.png",
        "RFI-17": "img/r01_MB01_A202.png", "RFI-03": "img/r09_A622_serving_tile.png", "RFI-05": "img/r09_A622_serving_tile.png"}
os.makedirs(os.path.join(C4, "img_runner"), exist_ok=True)


def hoja_png(h):
    p = os.path.join(C4, "img_runner", f"sheet_{h}.png")
    if not os.path.exists(p):
        doc[smap[h]].get_pixmap(dpi=40).save(p)
    return f"img_runner/sheet_{h}.png"


n = 0
for r in c["rfis"]:
    a = (r.get("opciones") or {}).get("A") or {}
    src = a.get("source") or ", ".join(r.get("fuentes_revisadas") or [])
    if not r.get("source"):
        r["source"] = src
        n += 1
    if not r.get("img"):
        img = CROP.get(r["id"])
        if not img or not os.path.exists(os.path.join(C4, img)):
            hs = [h for h in HOJA.findall(src + " " + " ".join(r.get("fuentes_revisadas") or [])) if h in smap]
            img = hoja_png(hs[0])
        r["img"] = img
        n += 1
for w in c["walls"]:
    if w["id"] in ("M3.5-01", "M3.5-02", "MB-01") and not w.get("to_deck_source"):
        w["to_deck_source"] = ("fixed standard top track (no slip / deflection track, no gap printed): " +
                               (w.get("top_track_kind_source") or "") + "; framing height C.1/A-202 6\" above ceiling")
        n += 1
    if w["id"] in ("M3.5-01", "M3.5-02") and "tick" not in w.get("length_op", ""):
        w["length_op"] += (" | single printed dimension (not a chain), SIMPLE ticks (one slash at each end), total = the "
                           "printed value; crop etapas/4_canon/img_calc/A202_M35_01_dim.png")
        n += 1
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("evidence fields written:", n)
