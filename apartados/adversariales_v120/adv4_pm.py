import sys, os, json, tempfile, shutil
sys.path.insert(0, sys.argv[1]); import verificar_version as V
real = sys.argv[2]
cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
IDS = ["U-185","U-189","U-190","BE-CR39","BE-CR40","BE-CR42","BE-GK47","NG-3.1 / BE-PM04","NG-3.2 / BE-PM05","NG-3.3 / BE-PM06","U-193","BE-PM08","BE-PM09","BE-GK54"]
import glob
def copia():
    c = tempfile.mkdtemp(dir=os.environ.get("ADVTMP"))
    for p in glob.glob(os.path.join(real, "POSTMORTEM_COBERTURA_*.md")): shutil.copy(p, c)
    for p in glob.glob(os.path.join(real, "*", "SUBIDA_OK*.json")):
        d = os.path.join(c, os.path.basename(os.path.dirname(p))); os.makedirs(d, exist_ok=True); shutil.copy(p, d)
    return c
def ver(c, name, hora, est):
    open(os.path.join(c, name), "w").write(f"# V\n\n{hora}\n\n" + cab + "".join(f"| {i} | x | x | x | {est(i)} |\n" for i in IDS))
# D1: unicode dashes in a closing state
for dash in ["‒", "―", "−", "⸺", "--"]:
    c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: f"OK {dash} CONFIRMED-CLOSED")
    print(f"D1 dash U+{ord(dash[0]):04X}{'x2' if len(dash)>1 else ''} closes?", V.revisar_postmortem(c) == [])
c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: "OK — CONFIRMED‐CLOSED")
print("D1b U+2010 hyphen inside token closes?", V.revisar_postmortem(c) == [])
# D2: prefix-only anchor: 'OK — CONFIRMED-CLOSED-NOT / STILL-WEAK'
c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: "OK — CONFIRMED-CLOSED-NOT, WEAK — STILL-WEAK")
print("D2 'OK — CONFIRMED-CLOSED-NOT, WEAK — STILL-WEAK' closes all?", V.revisar_postmortem(c) == [])
# D3: renamed row id in a later principal 12c (U185 / 'U-185 (renamed)') -> carried rows still open?
c = copia(); open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c.md"), "w").write("# PM\n\n2026-11-12 22:30 PT\n\n" + cab + "| U185 | x | x | x | OK |\n| BE‑GK54 | x | x | x | OK |\n")
open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12c_VERIFICACION.md"), "w").write("# V\n\n2026-11-12 22:40 PT\n\n" + cab + "| U185 | x | x | x | OK — CONFIRMED-CLOSED |\n| BE‑GK54 | x | x | x | OK — CONFIRMED-CLOSED |\n")
r = V.revisar_postmortem(c); print("D3 renamed ids in 12c close 12b rows?", r == [], "| still open:", r[-1].split("U-185):")[-1] if r else "")
# D4: an un-timed closing verification sorts last (end of day) and overrides a LATER timed STILL-WEAK verification
c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION5.md", "(no time)", lambda i: "OK — CONFIRMED-CLOSED")
ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: "WEAK — STILL-WEAK")
print("D4 untimed all-OK verif beats a later 22:00 STILL-WEAK verif (closes)?", V.revisar_postmortem(c) == [])
# D5: future-dated verification
c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION9.md", "2099-01-01 00:00 PT", lambda i: "OK — CONFIRMED-CLOSED")
ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: "WEAK — STILL-WEAK")
print("D5 future-dated (2099) all-OK verif beats real later STILL-WEAK (closes)?", V.revisar_postmortem(c) == [])
# D6: NG id trick: row 'NG-3.1 NG-3.3 junk' closes 'causa 3.1/3.3'
c = copia(); open(os.path.join(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md"), "w").write("# V\n\n2026-11-12 22:00 PT\n\n" + cab + "| junk NG-3.1 NG-3.3 | x | x | x | OK — CONFIRMED-CLOSED |\n")
r = V.revisar_postmortem(c); print("D6 junk row 'NG-3.1 NG-3.3' closes causas 3.1/3.3?", "causa 3.1" not in str(r), r[-1].split("U-185):")[-1])
# D7: baseline - exact correct verif closes
c = copia(); ver(c, "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION4.md", "2026-11-12 22:00 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("D7 control exact state closes all:", V.revisar_postmortem(c) == [])
