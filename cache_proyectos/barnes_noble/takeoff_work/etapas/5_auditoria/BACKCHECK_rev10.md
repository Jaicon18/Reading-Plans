VERDICT: PASS WITH COMMENTS
LIBRARY: 3 PASS · 0 FAIL · 0 N/A

# Back-check rev10: B&N Colorado Springs (form-only change)

File: `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev10.xlsx`, md5 955ae545b664a403fea07d668b3ecbb7. Read with openpyxl data_only=True, plus a formula read. Diffed cell by cell against rev9 (md5 48be3bb5). Per the coordinator's scope, only BE-46, BE-47 and BE-51 were run.

**No quantity changes.** Every Material Summary Net (col C) and Pieces to buy (col H) value is identical to rev9. The cells that differ are:
- Inputs A26:C29 (new)
- MS A37, A38, A39, G22 to G25, G45, I55, I56
- Pending Items B49 and C57

The internal-name scan (codes C7-/C8-/C-0x/N-xx, "plan check", .json/.py, skill, PASO, AUDITORIA, work folders, "RI 7") finds nothing. Every RFI / ALC ID cited exists.

| ID | Result | Evidence |
|---|---|---|
| BE-46 | PASS | One size per row: 3-5/8" (R37), 6" (R38), 8" (R39). The names now give the gauge split, which matches the Net and the sources. **R37:** 14 ga 157.81 (fire-stop on W2 / C-H2 walls) + 16 ga 5.00 (8/A-210 nested columns "3 5/8"x16 GA") + 20 ga 118.28 (soffits 45.54 + 20.24 + 40 + 12.5) = 281.09. **R38:** 16 ga 25.33 (8/A-210 "6"x16 GA" beam) + 20 ga 118.73 (SS-GG 12.33 + fire-stop 106.40) = 144.06. **R39:** ledger gauge not printed, sent to RFI-54 |
| BE-47 | PASS | The new numbers in texts match their rows: the A37 / A38 gauge splits sum to C37 / C38. RFI-54 cites the ledger at 12.67 LF, which is C39. I55 lists 377 wall pieces + 108 CW pieces = 485, and 4 × 485 = 1,940, which is C55. I56 cites 518.29 LF / Inputs!B22, giving C56 = 777.43. No undefined IDs |
| BE-51 | PASS | Stock lengths are now Inputs cells: B26 2x = 8, B27 main tee = 12, B28 cross tee = 4, B29 molding = 12. H18 / H42 divide by Inputs!$B$26, H22 by $B$27, H23 by $B$28, and H24 / H25 by $B$29. Pieces are unchanged (82, 3, 19, 132, 11, 11). G45 = "each" |

## Blocking issues

None.

## Non-blocking comments

- **N1.** R37 and R38 each hold several gauges, so the buyer must split the purchase by gauge. Pieces are computed only on the row total. This is consistent with the bottom / top track rows, which give their gauge split in col J.
- **N2 (carried from rev9).** Revision-history tags "(rev1)…(rev7):" remain in Pending Items and the Scope Checklist. They are not internal names. B49 still reads "...2026-10-26). the same phrase..." with a lowercase start.
- **N3 (carried from rev9 N5).** R37 nested-column track is 5.00 LF. If 8/A-210 track runs the full column length, it would be 6 × 2 × 10.5 = 126 LF. Confirm.
