# O'Reilly Auto Parts Store – 23rd Ave., Evans, CO #1 — Metal Frame & Drywall Take-off (FINAL FOR REVIEW rev3, 2026-10-31)

Bid set: EV1 Current Conformed Set 11-20-2025 (clean copy: the Drive file carried 79 Bluebeam markups of a prior take-off; all annotations were removed before reading). Trade sheets only: A1.1, A1.2, A2.1, A3.1-A3.4, A4.1, A4.2, A5.1, A5.2, A6.1, S4.1, S5.1-S5.3. Civil, electrical, mechanical, plumbing, cabinets and MEP excluded by the estimator.

## Files
| File | Content |
|---|---|
| `Take-off/OReilly_Evans_Takeoff_FINAL_rev3.xlsx` | Fixed 6-sheet format: Inputs, Partition Takeoff (schedule order S21-S61, then exterior CFMF, subtotals, grand total), Material Summary, Pending Items (RFIs, (A) plans / (B) trade code / (C) other), Review Items, Scope Checklist |
| `Planos marcados/OReilly_Evans_FINAL_markups_rev3.pdf` | Bluebeam markups: one PolyLine per wall on A1.1 (33) + legend page; Subject = type; Contents = TYPE · LF · H · SF · N/SHEET · Wall ID; /Measure at the sheet scale and /Depth = height; page labels A1.1 / LEGEND |
| `Planos marcados/A1.1_type_*.png`, `A1.1_OTHER_FRAMING_vestibule_heads.png` | One image per type on A1.1, each wall labelled with its Wall ID as in the Excel |
| `SEGUIMIENTO.md` | Every item the drawings do not resolve: assumption carried, RFI number, delta |
| `Auditoria/` | Step 11 independent audit (certificate, comparison, resolution) and Step 12 coverage matrix (certificate, MATRIZ_COBERTURA.xlsx, resolution) |

## Totals
- Partitions: 614.86 LF, 8,037.25 SF board (30 walls); other framing (vestibule heads) 20.57 LF.
- Studs: 3-5/8" 2,214.54 LF · 6" 1,105.09 LF · 8" 537.32 LF · Z-furring 1-1/2" 2,690.71 LF.
- Track (bottom = top): 3-5/8" 218.32 · 6" 95.17 · 8" 50.67 · heads 20.57 LF.
- Board: 5/8" Type X 7,741.58 SF · Type X W.R. 702.15 SF · glass mat 534.88 SF · FRT plywood 420.25 SF.

## Checks
reglas.py 837 rules, 0 failures · bitacora compuerta OK (17 tools + back-check) · registro / alcances OK · Step 11 differences resolved and applied (Auditoria/RESOLUCION_PASO11.md) · Step 12: every item has a destination after resolution (Auditoria/RESOLUCION_PASO12.md) · Bluebeam vs Partition Takeoff: same LF per type.

Nothing was sent to the client.

## rev2 changes (printed products loaded; Material Summary Net)
| Material | rev1 | rev2 | Source |
|---|---|---|---|
| Bottom track anchors (interior + exterior piers) | slab pins 151.04 + Kwik Bolt 36 (defaults of a previous project) | Titen HD 3/8" @ 48" 37.76 + 6 | S1.1 7.F/7.G; 3/S5.1, 4/S5.1 |
| Stud-to-track screws | #8-18, 1,352 | #10, 684 (none on the Z-furring without track) | S1.1 7.E |
| Top track 3-5/8" | 218.32 LF | 171.48 LF + deep-leg slotted 3" x 14 ga 46.83 LF | 3/S5.1, 4/S5.1 |
| Sheathing screws | - | 1,058 #6 x 1-1/4" @ 8" | S5.2 / S5.3 KN8 |
| Simpson FCB43.5 clips | - | 144 | 1/S5.3, 3/S5.3 |
| FRT blocking | 351.56 LF | 387.75 LF (+ D1 / D2 head and jambs) | 11/A5.2, 12/A5.2 |
Directed reading of the structural notes: `Auditoria/LECTURA_DIRIGIDA_S_rev2.md` (+ crops). rev1 folder kept unchanged.

## rev3 changes - estimator decision 2026-10-31: all fasteners excluded
Every fastener row is 0 with "EXCLUDED - estimator decision 2026-10-31: all fasteners excluded" in "Where it comes from"; Scope Checklist ALC-25. Clips, angles, track, blocking and all other materials stay. RFI-21 / 26 / 27 closed as EXCLUDED; the screw / bolt parts of RFI-09 / RFI-20 excluded; the slab pin spacing RFI removed.
| Material | Unit | rev2 | rev3 | Δ |
|---|---|---|---|---|
| Sheathing screws - printed product and spacing (see Where it comes from) | PCS | 1,058.00 | 0.00 | -1,058.00 |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 9,586.10 | 0.00 | -9,586.10 |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 684.00 | 0.00 | -684.00 |
| Power-driven fasteners, slab pins for the bottom track | PCS | 37.76 | 0.00 | -37.76 |
| Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | PCS | 6.00 | 0.00 | -6.00 |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 792.00 | 0.00 | -792.00 |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 546.37 | 0.00 | -546.37 |
