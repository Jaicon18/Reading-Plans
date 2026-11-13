# adv8_be83_cr: en el canon real de CR, qué caras silencia SOLO la regex ampliada (RX_SUBE_JUSTIFICADO) frente a la de v137
import sys, os, json, re
S = sys.argv[1]; sys.path.insert(0, os.path.join(S, "runner")); import completitud as CO
c = json.load(open(sys.argv[2]))
VIEJA = re.compile(r"full height|to deck|above ceiling|hasta deck", re.I)
num = lambda t: set(re.findall(r"\b\d{3}\b", str(t or "")))
ceil = [(num(z.get("room")), float(z["height_ft"])) for z in c.get("ceilings") or [] if isinstance(z, dict) and z.get("height_ft") is not None and num(z.get("room"))]
print("ceilings con cuarto:", len(ceil))
n = {"eval": 0, "con_cielo": 0, "sobre": 0, "just_vieja": 0, "just_nueva_solo": 0, "cielo_impreso": 0, "sin_caras": 0}
solo_nueva = []
for w in CO._muros(c):
    caras = w.get("faces") if isinstance(w.get("faces"), list) else CO._cara_de_muro(w)
    if not caras: n["sin_caras"] += 1
    for f in caras:
        if f.get("height_ft") is None: continue
        n["eval"] += 1
        hs = [h for nn, h in ceil if nn & num(f.get("room"))]
        if not hs: continue
        n["con_cielo"] += 1
        if float(f["height_ft"]) <= max(hs) + 1.0: continue
        n["sobre"] += 1
        src = str(f.get("height_source") or "")
        bod = re.search(r"B\.O\. DECK|B\.O\.D", src, re.I)
        if VIEJA.search(src) and not bod: n["just_vieja"] += 1; continue
        if CO.RX_SUBE_JUSTIFICADO.search(src) and not bod:
            n["just_nueva_solo"] += 1; solo_nueva.append((w["id"], f["room"][:40], f["height_ft"], max(hs), CO.RX_SUBE_JUSTIFICADO.search(src).group(0), src[:220])); continue
        if CO.altura_cielo_impresa(f): n["cielo_impreso"] += 1; continue
        print("  FLAG", w["id"], f["room"][:40], f["height_ft"], max(hs), src[:150])
print(n)
for x in solo_nueva: print("  SOLO_NUEVA", x)
