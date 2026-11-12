"""BE-GK40 (Grand Kia rev2, BE-CR35 blind A/B of every Depth): the blind question asks the SAME magnitude the loaded Depth measures,
with its definition. GK asked 'depth of the joists' for EXT-07 while the loaded 0.82 ft was the joist LENGTH (pocket width): both
blind readers measured another thing (0.30 = 362S web) and the comparison was void.

  magnitud(op)                 -> (key, definition) of the Depth from the item's operation text
  tareas(canon)                -> [{id, magnitude, definition}] for every misc item with a Depth (no loaded value is written)
  pregunta_fallas(tareas_md, canon) -> [fallas]: a blind task row whose 'what to read' does not name the magnitude of its Depth
Uso: python3 pregunta_ciega.py tareas <canon.json>  |  python3 pregunta_ciega.py revisar <TAREAS.md> <canon.json>"""
import json
import re
import sys

MAGNITUDES = (   # (key, regex on the operation, definition for the blind reader, words the question must contain)
    ("joist_length", r"\bjoists?\s*x\s*\d", "LENGTH of each joist piece (= width of the pocket / soffit it spans), ft", ("length",)),
    ("developed", r"developed\s*\d", "DEVELOPED board width of the section = sum of every face with board, per side, ft", ("developed",)),
    ("return_depth", r"return depth", "DEPTH of the board return from the wall face to the frame, ft", ("return",)),
    ("stud_height", r"\bstuds?\s*x\s*(average height\s*)?\d", "HEIGHT of each stud (bottom track to top track), ft", ("h", "height")),
    ("face_height", r"\bLF\s*x\s*\d", "HEIGHT of the board face, ft", ("h", "height")),
)


def magnitud(op):
    t = str(op or "")
    for k, rx, d, _w in MAGNITUDES:
        if re.search(rx, t, re.I):
            return k, d
    return None, None


def _id(ref):
    return str(ref).split()[0]


def tareas(canon):
    out, vistos = [], set()
    for m in canon.get("misc_items") or []:
        k, d = magnitud(m.get("op"))
        i = _id(m.get("ref"))
        if k and (i, k) not in vistos:
            vistos.add((i, k))
            out.append({"id": i, "magnitude": k, "definition": d})
    return out


def pregunta_fallas(tareas_md, canon):
    filas = {}
    for ln in str(tareas_md or "").splitlines():
        cs = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cs) >= 3 and re.match(r"^[A-Z]{2,4}-[\w.-]+", cs[0]):
            for i in re.findall(r"[A-Z]{2,4}-[\w-]+", cs[0]):
                filas[i] = cs[-1].lower()
    ev = []
    for t in tareas(canon):
        q = filas.get(t["id"])
        if q is None:
            continue
        w = next(w for k, _rx, _d, w in MAGNITUDES if k == t["magnitude"])
        if not any(re.search(r"\b" + re.escape(x) + r"\b", q) for x in w):
            ev.append(f"{t['id']}: the blind question '{q[:60]}' does not ask the loaded magnitude ({t['definition']}) (BE-GK40)")
    return ev


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "tareas":
        for t in tareas(json.load(open(sys.argv[2]))):
            print(f"| {t['id']} | {t['definition']} |")
    elif len(sys.argv) >= 4 and sys.argv[1] == "revisar":
        ev = pregunta_fallas(open(sys.argv[2], encoding="utf-8").read(), json.load(open(sys.argv[3])))
        print("\n".join(ev) or "OK: every blind question asks the loaded magnitude")
        sys.exit(1 if ev else 0)
    else:
        print(__doc__)
