# Changes rev4 -> rev5 (NET, before waste)
rev4 = pass 1 rev4 (01-nov). rev5 = pass 2 FINAL (independent take-off, all estimator answers RFI-01..32) re-run with skill
v81cf25. Every number below is read by program from the two Excel files (`tools/cambios_vs_rev4.py`); rows grouped by family.

| Material | Unit | rev4 | rev5 | Delta | Delta % |
|---|---|---|---|---|---|
| Bottom track 3-5/8" | LF | 218.32 | 219.68 | +1.36 | +0.6 % |
| Bottom track 6" (all) | LF | 95.17 | 56.50 | -38.67 | -40.6 % |
| Bottom track 8" (all) | LF | 50.67 | 50.67 | +0.00 | +0.0 % |
| Bottom track 6" other framing (600T) | LF | 0.00 | 38.67 | +38.67 | new |
| Bottom track roof step / heads | LF | 20.57 | 20.09 | -0.48 | -2.3 % |
| Top track 3-5/8" | LF | 171.48 | 96.57 | -74.91 | -43.7 % |
| Top track 6" (all) | LF | 95.17 | 56.50 | -38.67 | -40.6 % |
| Top track 8" (all) | LF | 50.67 | 50.67 | +0.00 | +0.0 % |
| Top track 6" other framing (600T) | LF | 0.00 | 38.67 | +38.67 | new |
| Top track roof step / heads | LF | 20.57 | 0.00 | -20.57 | -100.0 % |
| Deep-leg slotted deflection track | LF | 46.83 | 143.20 | +96.37 | +205.8 % |
| Z-furring 1-1/2" | LF | 2,570.64 | 2,220.63 | -350.01 | -13.6 % |
| 8" stud | LF | 537.32 | 537.32 | +0.00 | +0.0 % |
| 6" stud (all) | LF | 1,148.07 | 1,372.04 | +223.97 | +19.5 % |
| 3-5/8" stud (all) | LF | 2,165.17 | 2,052.02 | -113.15 | -5.2 % |
| Ceiling / soffit track | LF | 0.00 | 72.00 | +72.00 | new |
| Bracing C.R. channel | LF | 806.26 | 808.01 | +1.75 | +0.2 % |
| Header / box beam | LF | 56.00 | 56.00 | +0.00 | +0.0 % |
| Glass mat sheathing | SF | 534.88 | 534.88 | +0.00 | +0.0 % |
| FRT blocking | LF | 539.75 | 600.79 | +61.04 | +11.3 % |
| Metal stud blocking | LF | 6.00 | 0.00 | -6.00 | -100.0 % |
| 5/8" Type X | SF | 7,673.76 | 7,421.40 | -252.36 | -3.3 % |
| 5/8" Type X W.R. | SF | 734.15 | 721.21 | -12.94 | -1.8 % |
| Clips + clip angles | PCS | 38.00 | 41.00 | +3.00 | +7.9 % |
| FCB43.5 framing clips | PCS | 144.00 | 144.00 | +0.00 | +0.0 % |
| Resilient channel | LF | 243.00 | 128.51 | -114.49 | -47.1 % |
| 1/4" gypsum board | SF | 385.00 | 195.58 | -189.42 | -49.2 % |
| Flat strap bracing | LF | 98.00 | 96.91 | -1.09 | -1.1 % |
| Z-furring runner | LF | 501.41 | 577.25 | +75.84 | +15.1 % |
| W-4 panels | SF | 555.33 | 555.34 | +0.01 | +0.0 % |
| W-4 trim | LF | 0.00 | 100.67 | +100.67 | new |
| Track brace strut splice | LF | 0.00 | 6.00 | +6.00 | new |
| Metal trim (all) | LF | 709.63 | 1,127.26 | +417.63 | +58.9 % |
| Control joints | LF | 73.34 | 340.24 | +266.90 | +363.9 % |
| FRT plywood | SF | 420.25 | 407.63 | -12.62 | -3.0 % |
| Additional head track | LF | 32.73 | 0.00 | -32.73 | -100.0 % |
| Jamb return | SF | 7.24 | 11.78 | +4.54 | +62.7 % |
| Joint compound | LB | 605.37 | 586.27 | -19.10 | -3.2 % |
| Joint tape | LF | 3,110.93 | 3,012.77 | -98.16 | -3.2 % |
| Level 5 | SF | 7,673.76 | 6,440.16 | -1,233.60 | -16.1 % |

## Main causes (delta > 2 %)
- Top track 3-5/8" / roof step / deep-leg: same total length (rev4 238.88 / rev5 239.77 LF, +0.4 %); the hung framing S42-02/03 and the vestibule heads moved to deep-leg slotted track (estimator answer RFI-20 B, 4/S5.1).
- 6" track split: the storefront A head 600T (38.67 LF) has its own "other framing" row in rev5 (same LF in total).
- Z-furring -13.6 %: furring jambs carry no king + jack studs (2/A5.1, 12/A5.2: the jamb is FRT blocking; back-check F1, run15); furring counted continuous.
- 6" stud +19.5 %: third CONT 600S200-54 line printed in 2/S5.1, vestibule head diagonal 600S162-43 (3/A3.1) and ceiling / vestibule joists by member.
- 3-5/8" stud -5.2 %: no pier ties (RFI-11 A).
- 5/8" Type X -3.3 %, resilient channel -47 %, 1/4" gypsum -49 %: storefront head interior board at the printed 0.667 ft (1/A5.2), piers at 12'-0" (RFI-16 A); rev4 used the exterior dimension (BE-111).
- Level 5 -16 %: only W-2 painted faces (A1.2, RFI-15 B).
- Control joints +364 %, metal trim +59 %: A1.1 note 3.A (30 ft, change of direction, RFI-27 B / RFI-30 B) and note 3.C on every exposed edge.
- FRT blocking +11 %: 14/A4.1 two rows (RFI-25 B), sign backing + extinguishers (RFI-12 B), accessories two rows (RFI-24 A).
- Ceiling / soffit track +72 LF: track at the ends of the office / R.R. / vestibule joists (7/A4.2, 3/A3.1).
- Jamb return +63 %: with sill (13/A5.2, estimator answer).
- **Additional head track -32.73 LF (rev5, new):** no sheet prints a head track or a 4'-0" rule (7/A5.1 = box header only); the three openings were in S21 Z-furring on CMU (masonry lintels, S4.1). Tool fix R80e.144.
- Joint compound / tape -3.2 %: driver = board total (7,421.40 + 721.21 SF).
