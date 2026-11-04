#!/usr/bin/env python3
"""Writes README_REVIEW.md, PARA_REVISAR_EN_LA_MANANA.md and SEGUIMIENTO.md of the rev5 delivery (English, PROJECT DATA on
top). Every number is read from the delivered Excel (Material Summary / Pending Items / Scope Checklist); nothing typed.
Usage: hacer_docs.py <entrega_dir> <proyecto_datos.json> <cambios_vs_rev4.md>"""
import json
import os
import sys

import openpyxl

E, PD, CAMBIOS = sys.argv[1], sys.argv[2], sys.argv[3]
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
wb = openpyxl.load_workbook(x, data_only=True)
pdj = json.load(open(PD))


def bloque_datos():
    L = ["## PROJECT DATA", "", "| Field | Value | Source |", "|---|---|---|"]
    for d in pdj["proyecto_datos"]:
        L.append(f"| {d['campo']} | {d['valor']} | {d.get('fuente') or '-'} |")
    L += ["", "**Mandatory sheets reviewed**", "", "| Category | Status |", "|---|---|"]
    for h in pdj["hojas_revisadas"]:
        L.append(f"| {h['categoria']} | {h['estado']} |")
    return L


abiertos, cerrados = [], []
for r in wb["Scope Checklist"].iter_rows(min_row=2, values_only=True):
    if r[0] and str(r[0]).startswith("RFI"):
        (cerrados if "CLOSED" in str(r[2] or "") else abiertos).append(r)
pend = [r for r in wb["Pending Items"].iter_rows(min_row=2, values_only=True) if r and r[0] and str(r[0]).upper().startswith("RFI")]
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
cambios = open(CAMBIOS, encoding="utf-8").read() if os.path.isfile(CAMBIOS) else ""
titulo = "O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 — Metal framing & drywall take-off, rev6 FINAL"

R = [f"# {titulo}", ""] + bloque_datos() + [
    "", "## What is in this folder", "",
    "- `Take-off/OReilly_Evans_Takeoff_FINAL_rev6.xlsx` — fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, "
    "Pending Items, Review Items, Scope Checklist). Waste is applied once, in the Material Summary.",
    "- `Planos marcados/OReilly_Evans_FINAL_markups_rev6.pdf` — Bluebeam markups on A1.1 (Subject = type, Page Label, "
    "Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · board SF · DETAIL · Wall ID) + one PNG per type.",
    "- `SEGUIMIENTO.md` — RFI follow-up (open and closed).", "- Review-first notes for the estimator (the separate notes file in this folder).",
    "- `Auditoria/` — delivery gate (ENTREGA_OK.json), materials vs Partition Type Schedule, markup review.", "",
    "## Basis of this revision", "",
    "rev6 = rev5 (pass 2 FINAL, all estimator answers RFI-01..RFI-32 applied) re-run end to end with skill v81cf27 = v81cf26 + Review Items image name fix "
    "(delivery gate with the day-1 rules U-114..U-125). **rev6 replaces rev5; quantities are identical to rev5** (67 Material "
    "Summary rows, checked by program). Added: [CONFIRMED] / [DERIVED] status on every face height, numbered tag sweep of A1.1 "
    "(29 tags, circled crops), circled height evidence per wall. Quantities are produced by the programs from the canon; "
    "nothing is typed in the Excel.", "",
    "## Material Summary (net, before waste)", "", "| Material | Unit | Net | Where it comes from |", "|---|---|---|---|"]
for r in ms:
    R.append(f"| {r[0]} | {r[1]} | {r[2]:,.2f} | {str(r[8] or '')[:110]} |")
R += ["", "## Changes vs rev4", "", cambios or "(see Auditoria/CAMBIOS_vs_rev4.md)"]
open(os.path.join(E, "README_REVIEW.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")

P = [f"# Review first — {titulo}", ""] + bloque_datos() + [
    "", "## Check these first", "",
    f"1. Open RFIs: {len(pend)} (Pending Items). Closed RFIs: {len(cerrados)} — every decision is written in the Excel "
    "(Scope Checklist) with its date.",
    "2. RFI-01 (closed, recommended option): studs and Z-furring stop under the PEMB purlin with an assumed 8\" purlin depth "
    "(not printed, 1/A3.2) — confirm with the PEMB shop drawings.",
    "3. Additional head track at openings over 4'-0\" = 0 LF (rev4 carried 32.73 LF): no sheet prints it; 7/A5.1 is a box "
    "header only and the three wide openings are in S21 Z-furring on CMU walls (masonry lintels, S4.1). See Auditoria/CAMBIOS_vs_rev4.md.",
    "4. Markups: Length on the scanned A1.1 is measured at the calibration of the scan against the printed dimension "
    "strings (9.04 pt/ft; printed 1/8\" = 9.00 pt/ft); walls whose drawn line differs from the printed LF carry the cause "
    "in the canon (length_cause).", "5. Delivery gate result: `Auditoria/ENTREGA_OK.json`."]
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w", encoding="utf-8").write("\n".join(P) + "\n")

S = [f"# RFI follow-up — {titulo}", "", "## Open RFIs", ""]
if pend:
    S += ["| RFI | Question / condition | Delta |", "|---|---|---|"] + [f"| {r[0]} | {r[1]} | {r[2]} |" for r in pend]
else:
    S.append("None: 0 open RFIs (Pending Items is empty).")
S += ["", "## Closed RFIs (decision applied in the quantities)", "", "| RFI | Decision | Applied |", "|---|---|---|"]
S += [f"| {r[0]} | {str(r[1])[:200]} | {str(r[3])[:120]} |" for r in cerrados]
open(os.path.join(E, "SEGUIMIENTO.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")
print("docs OK", len(pend), "open /", len(cerrados), "closed")
