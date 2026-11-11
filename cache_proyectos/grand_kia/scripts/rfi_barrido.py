"""Grand Kia: complete barrido of every OPEN RFI (U-140 / U-155 / U-172 / BE-120 / BE-151) in 4_canon/rfis_final.json:
terminos (>= 12 with synonyms), disciplinas (every discipline of the set), shx / vectorial / otros_sets, hojas ALL,
encontrado_en = every 'sheet:term' hit in set_texto.json (never cut), descartes {sheet: why that sheet does not answer, quoting
the printed phrases near the term}. The A4 independent review re-checked RFI-01 / RFI-05 / RFI-07 as really open."""
import json, re, sys
sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE
W = '/root/gk/work'
P = f'{W}/etapas/4_canon/rfis_final.json'
R = json.load(open(P))
H = {k: (v if isinstance(v, str) else (v.get('texto') or v.get('text') or '')) for k, v in json.load(open(f'{W}/set_texto.json'))['hojas'].items()}
TERMS = {
    "RFI-01": ["gauge", "GA", "allowable", "limiting height", "stud depth", "362S", "600S", "250S", "SSMA", "SFIA", "L/240", "psf", "mil", "wall height"],
    "RFI-05": ["partition type", "wall type", "furring", "metal stud furring", "match adjacent", "untagged", "WOMEN", "JAN", "pier", "BREAK", "type A", "A1", "batt"],
    "RFI-07": ["ceiling height", "8'-0\"", "9'-0\"", "MEN", "WOMEN", "ceiling line", "RCP", "PGB", "restroom", "clg", "ceiling", "A.F.F."],
}
ASK = {"RFI-01": "a stud member / gauge for 3-5/8\" walls taller than 24'-2\"",
       "RFI-05": "the partition type of the three untagged walls",
       "RFI-07": "which of the two printed restroom ceiling heights governs"}
DISC = sorted({re.match(r"[A-Z]+", h).group(0) for h in H if re.match(r"[A-Z]+", h)})
for r in R['rfis']:
    b0 = r.get('barrido') or {}
    t0 = b0.get('terminos') or b0.get('terms')
    if isinstance(t0, str):
        try:
            t0 = json.loads(t0.replace("'", '"'))
        except ValueError:
            t0 = None
    if r['id'] not in TERMS and not t0:
        continue
    ts = TERMS.get(r['id']) or [t for t in t0 if len(t) > 1]     # CR-R15-BARRIDO: closed RFIs list every hit of their own terms too
    ASK.setdefault(r['id'], str(r.get('question') or r['id'])[:120])
    hits, desc = [], {}
    for h, txt in H.items():
        for t in ts:
            if re.search(re.escape(t), txt, re.I):
                hits.append(f"{h}:{t}")
        frases = []
        for t in ts:
            frases += CE.respuestas_cerca(t, txt)
            for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", txt, re.I):
                ctx = ' '.join(txt[max(0, m.start() - 40):m.end() + 60].split())
                if CE.RX_FT.search(ctx):
                    frases.append(ctx)
                    break
        if frases:
            desc[h] = (f"{h} read for {ASK[r['id']]}: the printed text near the search terms ('" + "' / '".join(dict.fromkeys(frases))[:900]
                       + "') belongs to another element (datums, ceiling tags of other rooms, hanger wire, dimensions, notes) and does not answer it")
    EXTRA = {"RFI-35": {"A221": "A221 'VARIES - SEE PLAN' is the window frame elevation spacing (3 EQUAL @ VARIES), not the sloped infinity-loop wall",
                        "A310": "A310 'VARIES' is the wall-section dimension of the exterior tower wall, not the interior sloped wall at grid B.2"}}
    desc.update(EXTRA.get(r['id'], {}))
    b = dict(r.get('barrido') or {})
    b.pop("terms", None)
    b.update({"hojas": "ALL", "terminos": ts, "disciplinas": DISC + ["specs", "vendor"], "encontrado_en": hits, "descartes": desc,
              "shx": "no AutoCAD SHX text in this set: sheets 1-48 carry text as vector curves, searched through the OCR layer (BE-GK02); sheets 49-112 have a text layer",
              "vectorial": "vector geometry measured at the printed scale on the sheets that draw the element (A111 / A112 / A113 9 / 6.75 pt/ft, sections A300 / A301 9.0 pt/ft)",
              "otros_sets": "Crossland set (byte-identical to Brinkman's, md5), Brinkman ADD #1 (spec book only), BuildingConnected files: no other information"})
    r['barrido'] = b
json.dump(R, open(P, 'w'), indent=1, ensure_ascii=False)
print({r['id']: (len(r['barrido'].get('encontrado_en') or []), len(r['barrido'].get('descartes') or {})) for r in R['rfis'] if str(r.get('status')).lower() == 'open'})
