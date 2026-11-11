# Bluebeam CSV comparison (U-157) – Consumer Cellular rev4 FINAL
CSV exported by the user from Bluebeam (Markups List): "CC_markups_rev4 - OPEN IN BLUEBEAM.csv" (11-11-2026), from
"Planos marcados/CC_markups_rev4 - OPEN IN BLUEBEAM.pdf".

## 1. CSV vs PDF of markups (comparar_csv_bluebeam.py, by program)
- CSV: 30 markups · PDF: 30 markups · paired: 30 · in the PDF and not in the CSV: 0 · in the CSV and not in the PDF: 0.
  (30 = 26 measured markups + 4 legend labels A3 / C3 / D / E3.)

## 2. CSV vs Excel (Take-off rev4 FINAL), row by row
| Group | Markups | Checked | Result |
|---|---|---|---|
| Walls A100 (A3 x4, C3, D, E3 x13) | 19 | Page Label, Length = Partition Takeoff LF, Depth = face height, Wall Area = LF x H | 19 / 19 OK |
| Demolition D100 (DEMO-01..06) | 6 | Length, Depth 17.13 ft, Wall Area = Material Summary DEMO SF | 6 / 6 OK (Bluebeam rounds 0.02 SF: e.g. 765.90 vs 765.88) |
| Restroom C-1 ceiling A200 | 1 | Area 60.49 SF, perimeter 31.75 LF | 1 / 1 OK |

**Result: 26 / 26 markups match the Excel; 0 markups missing on either side. No error found.**
