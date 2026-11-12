import sys, os, json, tempfile, shutil, glob
sys.path.insert(0, sys.argv[1]); import verificar_version as V
real = sys.argv[2]; T = os.environ.get("ADVTMP")
cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
IDS = ["U-185","U-189","U-190","BE-CR39","BE-CR40","BE-CR42","BE-GK47","NG-3.1 / BE-PM04","NG-3.2 / BE-PM05","NG-3.3 / BE-PM06","U-193","BE-PM08","BE-PM09","BE-GK54"]
def copia(sin_viejas=True):
    c = tempfile.mkdtemp(dir=T)
    for p in glob.glob(os.path.join(real, "POSTMORTEM_COBERTURA_*.md")):
        if sin_viejas and "_VERIFICACION" in p: continue
        shutil.copy(p, c)
    for p in glob.glob(os.path.join(real, "*", "SUBIDA_OK*.json")):
        d = os.path.join(c, os.path.basename(os.path.dirname(p))); os.makedirs(d, exist_ok=True); shutil.copy(p, d)
    return c
def ver(c, name, cabecera, est, ids=IDS):
    open(os.path.join(c, name), "w").write(f"# V\n\n{cabecera}\n\n" + cab + "".join(f"| {i} | x | x | x | {est(i)} |\n" for i in ids))
W = "POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION%s.md"
# E0 positive control: proper Fecha, all OK closes
c = copia(); ver(c, W % "4", "Fecha: 2026-11-12 13:40 PT", lambda i: "WEAK — STILL-WEAK"); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("E0 control proper Fecha all OK -> []:", V.revisar_postmortem(c))
# E0b real cache copy (with the 4 old verifs w/o Fecha) + V5 all OK
c = copia(False); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("E0b real old verifs + V5 all OK ->", [x[:110] for x in V.revisar_postmortem(c)])
# E1 markdown bold Fecha '**Fecha:** ...' (common style) -> recognised?
c = copia(); ver(c, W % "5", "**Fecha:** 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("E1 '**Fecha:**' bold ->", [x[:120] for x in V.revisar_postmortem(c)])
# E2 status with bold '**OK — CONFIRMED-CLOSED**' closes (strip *) ; status with trailing period
c = copia(); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "**OK — CONFIRMED-CLOSED**")
print("E2 bold state closes:", V.revisar_postmortem(c) == [])
c = copia(); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED. (but see WEAK note)")
print("E3 'OK — CONFIRMED-CLOSED. (but ... WEAK)' closes?", V.revisar_postmortem(c) == [])
# E4 status 'OK — CONFIRMED-CLOSED (con reserva: STILL-WEAK en G5)' -> must not close
c = copia(); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED (con reserva)")
print("E4 suffix reserva closes?", V.revisar_postmortem(c) == [])
# E5 verification copy-pasted from V4 keeping V4's Fecha but changing all states to OK (same timestamp as V4 STILL-WEAK) 
c = copia(); ver(c, W % "4", "Fecha: 2026-11-12 13:40 PT", lambda i: "WEAK — STILL-WEAK"); ver(c, W % "5", "Fecha: 2026-11-12 13:40 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("E5 same Fecha as V4 (tie), V5 OK -> closes (name order)?", V.revisar_postmortem(c) == [])
# E6 V5 omits rows (only 9 closed ones listed) -> 5 weak stay open
c = copia(); ver(c, W % "4", "Fecha: 2026-11-12 13:40 PT", lambda i: "WEAK — STILL-WEAK" if i in ("U-185","NG-3.1 / BE-PM04","NG-3.3 / BE-PM06","U-193","BE-GK54") else "OK — CONFIRMED-CLOSED")
ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED", ids=["U-189","U-190"])
r = V.revisar_postmortem(c); print("E6 V5 omits the weak rows -> still open:", r[-1].split("U-185):")[-1] if r else r)
# E7 V5 with Fecha in PST but day typo (2026-11-21, future) -> falla
c = copia(); ver(c, W % "5", "Fecha: 2026-11-21 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED")
print("E7 future typo ->", [x[:100] for x in V.revisar_postmortem(c)])
# E8 V5 table with an extra trailing column 'notas' after estado
c = copia(); open(os.path.join(c, W % "5"), "w").write("# V\n\nFecha: 2026-11-12 13:50 PT\n\n| id | error | chequeo | test | estado | notas |\n|---|---|---|---|---|---|\n" + "".join(f"| {i} | x | x | x | OK — CONFIRMED-CLOSED | n |\n" for i in IDS))
print("E8 extra trailing column ->", [x[:110] for x in V.revisar_postmortem(c)])
# E9 a later verification of 12b that says 'WEAK — NOT CONFIRMED' for U-193 after V5 closed it -> reopens
c = copia(); ver(c, W % "5", "Fecha: 2026-11-12 13:50 PT", lambda i: "OK — CONFIRMED-CLOSED"); ver(c, W % "6", "Fecha: 2026-11-12 13:55 PT", lambda i: "WEAK — NOT CONFIRMED", ids=["U-193"])
r = V.revisar_postmortem(c); print("E9 later WEAK reopens U-193:", r)
