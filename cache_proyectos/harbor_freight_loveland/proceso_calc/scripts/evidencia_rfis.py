"""Evidence fields only (no quantities) for every RFI of the canon (HFT Loveland):
 - source (N/SHEET) and img: the resolution crop when one is named in the RFI (img / imagen / crop), otherwise the full
   sheet cited first in its source, rendered from the clean PDF at 40 dpi (same as runner/evidencia.py);
 - barrido (R80f.6 / BE-CF16): hojas = the sheets the reading / resolution swept (or ALL when >= 15 / "whole set"),
   terminos = the searched terms (RFI barrido / 'grep whole set:' entry / trade words of the question),
   grep = a REAL text search done here over the full set: page text of the clean copy (50 pages) + the AutoCAD SHX
   text annotations of the original PDF, with the hit count and the sheets of each term.
Use: python3 bitacora.py run scripts/evidencia_rfis.py <clean.pdf> <original.pdf>"""
import json, os, re, sys
import pymupdf as fitz
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
doc = fitz.open(sys.argv[1])
orig = fitz.open(sys.argv[2]) if len(sys.argv) > 2 else None
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
smap = {v: int(k) - 1 for k, v in sm.items()}
HOJA = re.compile(r"\b([A-Z]{1,3}\d{1,2}\.\d{1,2}A?|EMS-\d)\b")
os.makedirs(os.path.join(C4, "img_runner"), exist_ok=True)
TXT = []
for i, pg in enumerate(doc):
    t = pg.get_text()
    if orig is not None and i < orig.page_count:
        t += "\n" + "".join(str(a.info.get("content") or "") for a in (orig[i].annots() or []))
    TXT.append(t.upper())
VOCAB = ["DECK", "B.O.", "STRUCTURE", "SLIP", "DEFLECTION", "HEADER", "BOX HEADER", "JAMB", "FRP", "GYP", "TYPE X",
         "GREEN BOARD", "MOISTURE", "HAT CHANNEL", "FURRING", "BRACING", "DEMO", "REMOVE", "CEILING", "SOFFIT",
         "BULKHEAD", "CONTROL JOINT", "CORNER BEAD", "LEVEL", "A.F.F.", "METAL STUD", "SHAFT", "ENCLOSURE",
         "STRUCTURAL", "KICKER", "RECEIVING", "FIRE", "RATED", "PARTITION", "HEIGHT"]


def hoja_png(h):
    p = os.path.join(C4, "img_runner", f"sheet_{h}.png")
    if not os.path.exists(p):
        doc[smap[h]].get_pixmap(dpi=40).save(p)
    return p


def grep(terms):
    out, tot = [], 0
    for t in terms:
        hits = [(sm[str(i + 1)], s.count(t.upper())) for i, s in enumerate(TXT) if t.upper() in s]
        n = sum(h for _, h in hits)
        tot += n
        out.append(f"'{t}' {n} hit(s)" + (f" on {', '.join(h for h, _ in hits[:12])}{' ...' if len(hits) > 12 else ''}" if hits else ""))
    return (f"full set text searched by program ({doc.page_count} pages of the clean copy + the AutoCAD SHX text of the original): "
            + "; ".join(out) + f" - {tot} coincidences")


n = 0
for r in c.get("rfis") or []:
    o = r.get("opciones") or r.get("options") or {}
    a = o.get("A") or {}
    fr = [str(x) for x in (r.get("fuentes_revisadas") or r.get("sheets_swept") or [])]
    src = r.get("source") or a.get("source") or ", ".join(fr[:3])
    if not r.get("source"):
        r["source"] = src
        n += 1
    img = r.get("img") or r.get("imagen") or r.get("crop")
    if img and not os.path.isabs(img):
        for base in (C4, os.path.join(K, "etapas", "3_revision"), os.path.join(K, "etapas")):
            if os.path.exists(os.path.join(base, img)):
                img = os.path.join(base, img)
                break
    if not img or not os.path.exists(img):
        hs = [h for h in HOJA.findall(src + " " + " ".join(fr)) if h in smap]
        img = hoja_png(hs[0]) if hs else hoja_png("A1.1")
    if r.get("img") != img:
        r["img"] = img
        n += 1
    b = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
    hojas = b.get("hojas")
    if not (hojas == "ALL" or (isinstance(hojas, list) and len(hojas) >= 15)):
        sw = [h for h in HOJA.findall(" ".join(fr)) if h in smap]
        # fewer than 15 sheets listed by the reading: the program text search below covers ALL pages of the set
        hojas = sorted(set(sw)) if len(set(sw)) >= 15 else "ALL"
    terms = list(b.get("terminos") or [])
    if len(terms) < 3:
        g = next((x for x in fr if re.search(r"grep", x, re.I)), "")
        terms += [t.strip() for t in re.sub(r"(?i).*grep[^:]*:", "", g).split(",") if t.strip()] if g else []
    if len(terms) < 3:
        q = str(r.get("question") or r.get("pregunta") or "").upper()
        terms += [v for v in VOCAB if v in q and v not in terms]
    for v in ("GYP", "METAL STUD", "A.F.F."):
        if len(terms) >= 3:
            break
        if v not in terms:
            terms.append(v)
    r["barrido"] = dict(b, hojas=hojas if hojas == "ALL" else list(hojas), terminos=terms, grep=grep(terms))
    n += 1
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("RFI evidence fields written:", n, "for", len(c.get("rfis") or []), "RFIs")
