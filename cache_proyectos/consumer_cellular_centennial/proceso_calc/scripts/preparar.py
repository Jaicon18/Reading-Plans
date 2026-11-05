"""Stage-4 inputs that are pure layout (no quantities): etapas/0_mapa/SHEET_MAP.md (Page | Sheet | Title) from
SHEET_MAP.json (title blocks) + the inventory sheet titles, and a backup of the canon as delivered by the resolution
(etapas/4_canon/takeoff_canon_RESUELTO.json, written once, never overwritten) so every program change of this stage is
traceable.  Use: python3 bitacora.py run scripts/preparar.py"""
import json, os, shutil
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(K, "etapas")
sm = json.load(open(os.path.join(E, "SHEET_MAP.json")))
inv = json.load(open(os.path.join(E, "1_inventario", "inventario.json")))
tit = {int(s["page"]): s.get("title", "") for s in inv["sheets"]}
os.makedirs(os.path.join(E, "0_mapa"), exist_ok=True)
L = ["# SHEET MAP - Consumer Cellular - Centennial, CO (title block of each page, clean PDF)", "",
     "| Page | Sheet | Title |", "|---|---|---|"]
for p in sorted(sm, key=int):
    L.append(f"| {p} | {sm[p]} | {tit.get(int(p), '')} |")
open(os.path.join(E, "0_mapa", "SHEET_MAP.md"), "w").write("\n".join(L) + "\n")
b = os.path.join(E, "4_canon", "takeoff_canon_RESUELTO.json")
if not os.path.exists(b):
    shutil.copy2(os.path.join(E, "4_canon", "takeoff_canon.json"), b)
print(len(sm), "sheets mapped; canon backup", os.path.basename(b))
