# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off (for review)

Bid set: B&N Store 3566 / Project 33288, 3173 Cinema Point, Colorado Springs, CO 80922 — WJCA (revision 07-23-25).
Run: 2026-10-24, unattended. Skill take-off-metal-frame-drywall v80e (+ run patches, see SKILL §29).

## Files
| Folder | File |
|---|---|
| Take-off/ | `Barnes_Noble_ColoradoSprings_Takeoff_FINAL.xlsx` (6 sheets, formulas recalculated) |
| Planos marcados/ | `Barnes_Noble_ColoradoSprings_FINAL_markups.pdf` (Bluebeam Polylength markups, A-101 1/8" and A-221 1/2" scales, Depth = wall height) + images per sheet / type |
| Proposal/ | `Barnes_Noble_ColoradoSprings_Proposal_FINAL.xlsx` (prices BLANK) |

## Partition LF by type (Partition Takeoff, in schedule order)
1A 81.11 · 1 216.32 · 1B 99.74 · 1C 20.26 · 2 273.57 · 5 5.70 · 3 38.68 · 4 82.47 · H1 42.15 · H2a 12.17 · H2b 1.95 · H3a 4.08 · H3b 6.17 · E2 29.30 · E1 27.88 · F 3.26 · I 3.31 · A 20.27 · B 3.17 · D 5.14 · C 3.17 — **Total 979.87 LF**.
Other framing: column surrounds C25 9 ea (72 LF perimeter), soffit sides 59.14 LF.

## Main quantities (net, before waste)
- Studs: 3-5/8" 16,812.96 LF · 6" 2,925.00 LF · 8" 2,332.99 LF
- Track: bottom 1,051.87 LF · top / deflection 1,051.87 LF · ceiling / soffit 385.99 LF
- Bracing C.R. channel 5,230.74 LF · furring channel 493.02 LF · carrying channel 341.09 LF · hanger wire 103 pcs
- 5/8" gyp bd 16,562.77 SF · 1/2" exterior gyp sheathing (1B) 2,469.22 SF · cement board 851.40 SF · FRT plywood 2,591.90 SF
- Metal trim 891.72 LF (incl. C25 corner bead 288 LF and Cafe cloud corner bead + J-bead 107.21 LF each)

## Exclusions (estimator decisions)
Gyp bd on exterior types 1 / 1A / 1B / 1C (by future tenant, RFI-01) · acoustical sealant · insulation.

## RFIs (30) — each one has its delta in the Excel "Pending Items" sheet
Most important:
1. **RFI-01** — A-002 Responsibility Schedule: "PERIMETER STUDS, INSULATION, VAPOR BARRIER F/I BY LL". The perimeter framing (types 1 / 1A / 1B / 1C) may be by the landlord. Carried: INCLUDED. Delta −8,901 LF studs plus their track, bracing and sheathing.
2. **RFI-23** — FRT blocking / backing is called on many details (A-101 C12 / C16 / C20, A-412, A-413, A-201, A-226A, P-201) but nothing is dimensioned. Not carried. Approximate audit counts are in the delta.
3. **RFI-04 / RFI-07** — 3-5/8" studs at 24'-0" to 25'-7" exceed the 22'-0" limit of the A-410 stud schedule.
4. **RFI-11 / RFI-27** — W.R. board in wet rooms (about 1,326 SF) and Type X board (A-001A, 16,563 SF). Both carried as regular.
5. **RFI-24 / RFI-25 / RFI-28 / RFI-29 / RFI-30** — control joints, C5 demising patch, moment clips + anchors at types 3 / 4, corner guards, access panels.

## Review Items (14) — "Review Items" sheet
These are floor-plan points by type, plus detail points in plan order. Each comes with an image.

## Gates passed
- `reglas.py compuerta` OK and `alcances.py compuerta` OK (24 scope rows: 20 closed, 4 RFI).
- `registro.py entregable` OK.
- closer: 78 walls sealed. planmark and markups verified.
- Independent completeness audit (16 findings incorporated as quantities or RFIs).
- Back-check: see `takeoff_work/etapas/5_auditoria/BACKCHECK.md`.
