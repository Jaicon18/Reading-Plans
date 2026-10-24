"""Barrido manual de hojas NO INVENTARIABLES (texto vectorizado) -> partition_tag en inventario.json.
Símbolo = rombo detectado en vector (rombos.py); etiqueta = lectura visual en hoja de contactos (img/p*_contactos.png).
Recortes y overview con las funciones de inventario_tags.py; la verificación de texto bajo la marca no aplica
(hoja sin texto extraíble): se reemplaza por la lectura visual registrada en `lectura_visual`."""
import sys, json, os, re
T, W, D = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, T)
import inventario_tags as it
import pymupdf as fitz
LAB = {
 6: "1A 1 1 2 1B 1A 1B 1C 1C 4 2 1A 1C 1B 3 3 1C 1B 3 3 2 2 2 2 1B 2 2 2 2 2 5 1B 1B 1 1 1B 1B".split(),
 15: "I H3b H3a I H1 H2a B C A A D A H1 I H2b E1 E2 E1 F I".split(),
}
SHEET = {6: "A-101", 15: "A-221"}
SCHED = {"1": "1/A-410", "1A": "1A/A-410", "1B": "1B/A-410", "1C": "1C/A-410", "2": "2/A-410", "3": "3/A-410",
         "4": "4/A-410", "5": "5/A-410", "E1": "E/A-221", "E2": "E/A-221", "F": "F/A-221", "H1": "G/A-221",
         "H2a": "G/A-221", "H2b": "G/A-221", "H3a": "H/A-221", "H3b": "H/A-221", "I": "I/A-221", "A": "A/A-221",
         "B": "B/A-221", "C": "C/A-221", "D": "D/A-221"}
ORDER = "1A 1 1B 1C 2 5 3 4 H1 H2a H2b H3a H3b E2 E1 F I A B D C".split()
invp = os.path.join(D, "inventario.json")
inv = json.load(open(invp))
pdf = inv["pdf_path"]; doc = fitz.open(pdf)
tags = []
for pg, labs in LAB.items():
    R = json.load(open(os.path.join(W, "img", f"rombos_p{pg}.json")))
    assert len(R) == len(labs), (pg, len(R), len(labs))
    for r, t in zip(R, labs):
        h = r["w"] / 2
        tags.append({"kind": "partition_tag", "type": t, "text": t, "sheet": SHEET[pg], "page": pg,
                     "center_pt": [r["cx"], r["cy"]], "bbox_pt": [r["cx"]-6, r["cy"]-5, r["cx"]+6, r["cy"]+5],
                     "size": 8.0, "simbolo": {"forma_aprox": "rombo", "radio": round(h, 2)},
                     "metodo": "barrido manual (hoja sin texto extraíble): rombo detectado en vector + lectura visual",
                     "lectura_visual": f"img/p{pg}_contactos.png id {r['id']}", "rombo_id": r["id"]})
tags.sort(key=lambda o: (ORDER.index(o["type"]), o["page"], o["center_pt"][1], o["center_pt"][0]))
for n, o in enumerate(tags, 1): o["id"] = f"PT{n:04d}"
orig = it.verificar_png
def ver(ruta, clip, c, rad, z, page, o, tp=None):
    ok, det = orig(ruta, clip, c, rad, z, page, o, tp)
    if not ok and det.startswith("texto bajo la marca ''"):
        return True, "anillo y tinta OK; texto vectorizado -> etiqueta por lectura visual (" + o["lectura_visual"] + ")"
    return ok, det
it.verificar_png = ver
rec = os.path.join(D, "recortes")
fallas = it.recortes(doc, tags, rec, 150)
for h in inv["sheets"]:
    if h["page"] in LAB:
        h["es_planta_partition"] = True
        h["sheet"] = SHEET[h["page"]]
        h["barrido_manual"] = "texto vectorizado: tags por rombo en vector + lectura visual con imagen"
occ = inv["ocurrencias"]; occ["partition_tag"] = tags
_, fov = it.overview(doc, inv["sheets"], occ, rec)
tipos = [{"type": t, "fuentes": [SCHED[t] + " (detalle del type; schedule raster, leído con imagen)"]} for t in ORDER]
inv["partition_types"] = {"schedule": tipos, "conteo": it.resumen_types(tipos, occ, inv["sheets"])}
inv["avisos"] = [a for a in inv["avisos"] if not a.startswith("NO se encontró schedule")]
inv["avisos"].append("Hojas de planta A-101 (p.6) y A-221 (p.15) con texto vectorizado: barrido manual de tags "
                     "(rombos en vector + lectura visual, img/p6_contactos.png, img/p15_contactos.png). "
                     "Rombos en p.54/57/60 (M/P) = keynotes de equipo, no partition tags.")
inv["avisos"] += [f"PNG NO VERIFICADO: {f}" for f in fallas + fov]
inv["barrido_manual"] = {"herramienta": "scripts/rombos.py + scripts/inventario_manual.py",
                         "hojas": [6, 15], "otras_hojas_con_rombos": {"54": "keynote MEP", "57": "keynote MEP", "60": "keynote MEP"}}
json.dump(inv, open(invp, "w"), indent=1, ensure_ascii=False)
open(os.path.join(D, "inventario.md"), "w").write(it.md(inv))
for t, d in inv["partition_types"]["conteo"].items(): print(t, d["total"], dict(d["por_hoja"]))
print("fallas", fallas + fov)
