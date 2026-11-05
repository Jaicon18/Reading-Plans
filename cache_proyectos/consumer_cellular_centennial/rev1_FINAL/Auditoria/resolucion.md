# Resolution of reading A vs reading B - Consumer Cellular Centennial (A100)

Base: reading A. Each item decided on the comparar.py crop (blue = A, orange = B) and the A100 vector geometry.

| # | Item | A vs B | Decision | N/SHEET | Image |
|---|---|---|---|---|---|
| 1 | E3 door 6C | A E3-02 3.356 vs B E3-02 6.694 | B: 6.694 LF (door R.O. inside the wall line) | A100 + A600 | img/006_DIF_E3_A100_p7.png |
| 2 | E3 door 4C | A E3-04 0.583 + E3-05 3.542 vs B E3-04 7.428 | B: 7.428 LF (door R.O. inside the wall line) | A100 + A600 | img/003_DIF_E3_A100_p7.png |
| 3 | E3 door 5C | A E3-09 0.75 + E3-10 2.917 vs B E3-07 7.0 | B: 7.0 LF (door R.O. inside the wall line) | A100 + A600 | img/005_DIF_E3_A100_p7.png |
| 4 | C3 / E3 infill over cased opening | A E3-14 4.00 LF @ 4.417 ft (E3) vs B C3-02 4.00 LF @ 17.13 ft (C3) | B: C3-02 4.00 LF to deck (conservative), RFI-06 with delta | A100 / 2/A400 | img/002_DIF_C3_A100_p7.png |
| 5 | C3-01 length | A C3-01 31.542 LF + E3-14 4.0 LF vs B C3-01 31.542 + C3-02 4.0 LF | C3-01 35.542 LF (31'-6 1/2" printed + 4'-0" cased opening inside the C3 line) | A100 | img/002_DIF_C3_A100_p7.png |
| 6 | C3-01 stud height | A 16.333 ft (BOH deck) vs B 17.13 ft (Sales deck) | B: 17.13 ft (higher printed deck, conservative); RFI-01 keeps the 16'-4" alternative with its delta | A100 deck tags | img/002_DIF_C3_A100_p7.png |
| 7 | A3 north sales wall | A A3-01 14.41 + A3-02 28.83 LF vs B A3-01 43.24 LF | A: two walls (two A3 tags, line broken by the existing column, D100 key 14); same total 43.24 LF | A100 / D100 | img/001_DIF_A3_A100_p7.png |
| 8 | E3 alcove returns E3-06 / E3-08 | A two returns 1.083 LF each vs B E3-06 2.167 LF (two axes in one number) | A: one wall per axis (U-120), same total 2.17 LF | A100 | img/009_ONLYA_E3_A100_p7.png |

Alerts: 19 CO2 / TC1 / TC2 symbols = store number and electrical tags (tags_descartados of both readings); TYPE NO INVENTARIADO A3 / C3 / D / E3 = inventario_tags.py did not read the 1/A500 legend (types are section titles with a diamond A#, C#, D, E#, H; # = stud size code of the plan-view key, 3 = 3-5/8"); the 5 types are verified on the 1/A500 crop by the independent schedule reader (fichas.json). Type D tag (single letter) located by both readings at A100 (D-01).

Totals after resolution: A3 99.86 LF / 4 walls, C3 35.54 LF / 1 walls, D 7.67 LF / 1 walls, E3 57.45 LF / 13 walls
