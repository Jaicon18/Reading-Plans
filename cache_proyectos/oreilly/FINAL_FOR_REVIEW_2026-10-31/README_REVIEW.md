# O'Reilly Auto Parts Store – 23rd Ave., Evans, CO #1 — Metal Frame & Drywall Take-off (FINAL FOR REVIEW, 2026-10-31)

Bid set: EV1 Current Conformed Set 11-20-2025 (clean copy: the Drive file carried 79 Bluebeam markups of a prior take-off; all annotations were removed before reading). Trade sheets only: A1.1, A1.2, A2.1, A3.1-A3.4, A4.1, A4.2, A5.1, A5.2, A6.1, S4.1, S5.1-S5.3. Civil, electrical, mechanical, plumbing, cabinets and MEP excluded by the estimator.

## Files
| File | Content |
|---|---|
| `Take-off/OReilly_Evans_Takeoff_FINAL.xlsx` | Fixed 6-sheet format: Inputs, Partition Takeoff (schedule order S21-S61, then exterior CFMF, subtotals, grand total), Material Summary, Pending Items (RFIs, (A) plans / (B) trade code / (C) other), Review Items, Scope Checklist |
| `Planos marcados/OReilly_Evans_FINAL_markups.pdf` | Bluebeam markups: one PolyLine per wall on A1.1 (33) + legend page; Subject = type; Contents = TYPE · LF · H · SF · N/SHEET · Wall ID; /Measure at the sheet scale and /Depth = height; page labels A1.1 / LEGEND |
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
