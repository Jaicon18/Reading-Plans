# BACKCHECK rev2 vs rev1 (Barnes & Noble Colorado Springs take-off)

Method: openpyxl data_only=True; full cell diff of all sheets plus label-keyed comparison of Material Summary (rows shifted by one after a row was removed, so compared by label, not by row).

| # | Check | Result | Numbers |
|---|-------|--------|---------|
| 1 | 5/8" Type X (GWB ceilings moved) | PASS | 14,557.36 -> 15,538.74 SF (+981.38); waste 873.4416 -> 932.3244; purchase 15,430.8016 -> 16,471.0644; sheets 322 -> 344 |
| 2 | 5/8" regular row | PASS | 981.38 SF row removed entirely (no regular left) |
| 3 | 3/4" FRT plywood | PASS (minor) | 137.40 -> 141.84 SF (expected ~141.85; 137.40 + 17.78 - 13.33 = 141.85; 0.01 is rounding of 13.3333 -> 17.7778, delta 4.4444 -> 141.844). Waste 8.5104, purchase 150.3504, 4 sheets unchanged |
| 4 | Other Material Summary quantity rows | PASS | No other row differs in unit, net, waste %, waste, purchase or pieces (all other labels identical) |
| 5 | Partition Takeoff (A1:K106) | PASS | 0 cell differences |
| 6 | Arithmetic (net x waste% = waste; net + waste = purchase), all rows | PASS | 0 failures (tolerance 0.01) |
| 7 | Pending Items text | PASS | B30/C30 RFI-27 ceilings Type X, regular = 0; B4 RFI-01 kitchenette W.R. inside patch & repair allowance, amount stays BLANK; C26 backing 17.78 SF (13.33 x 16/12) |
| 8 | Review Items | PASS | Restroom backing height item (old row 14, 21/A-201) removed; questions renumbered 1/11..11/11 and header says 11 |
| 9 | Spanish text | PASS | No accents/Spanish keywords in any rev2 cell (regex scan) |
| 10 | Other text changes | INFO | Scope Checklist D8, D12, D17 updated consistently (rev2 wording); Material Summary source-note column shifted with rows; _reglas A2 canon hash changed (expected, metadata) |

Verdict: PASS. Only the three intended changes are present; no unintended quantity changes. Only observation: 3/4" plywood 141.84 vs 141.85 hand-calc is a 0.01 SF rounding artifact.
