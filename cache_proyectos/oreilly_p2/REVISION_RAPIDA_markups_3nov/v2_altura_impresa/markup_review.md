# O'Reilly Auto Parts - Evans, CO #1 — quick markup review

Program: revision_markups.py · printed scales {'A1.1': '9.000 pt/ft'} · LF ±0.5 %, H exact vs the PRINTED source height · GREEN 16 / AMBER 6 / RED 8

| Type | Wall ID | Excel LF | Measured LF | Excel H | Depth | Printed source H | Area SF | Verdict | Failures / amber |
|---|---|---|---|---|---|---|---|---|---|
| S21 | S21-E | 84.646 | 84.911 | 13.958 | 13.958 | n/a (assumption) | 1181.5 | 🟠 AMBER | S21-E: no printed height to compare (assumption; sheets cited 2/A3.2, 3/A3.4) - depends on the RFI-01 purlin assumption |
| S21 | S21-N | 85.000 | 85.389 | 14.844 | 14.844 | n/a (assumption) | 1261.7 | 🟠 AMBER | S21-N: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.2, 3/A3.2, 4/A3.2) - depends on the RFI-01 purlin assumption |
| S21 | S21-S | 85.000 | 85.389 | 14.844 | 14.844 | n/a (assumption) | 1261.7 | 🟠 AMBER | S21-S: no printed height to compare (assumption; sheets cited 1/A3.4) - depends on the RFI-01 purlin assumption |
| S21 | S21-W1 | 9.156 | 9.189 | 15.729 | 15.729 | n/a (assumption) | 144.1 | 🟠 AMBER | S21-W1: no printed height to compare (assumption; sheets cited 1/A3.2) - depends on the RFI-01 purlin assumption |
| S21 | S21-W2 | 24.823 | 24.944 | 15.729 | 15.729 | n/a (assumption) | 390.4 | 🟠 AMBER | S21-W2: no printed height to compare (assumption; sheets cited 1/A3.2) - depends on the RFI-01 purlin assumption |
| S24 | S24-OF | 11.708 | 11.789 | 8.500 | 8.500 | 8.500 (A.F.F. note, A1.1, A1.2, C-3) | 99.5 | 🔴 RED | LF measured 11.79 vs Excel 11.708 (+0.69 %) |
| S24 | S24-RR | 16.823 | 16.844 | 8.500 | 8.500 | 8.500 (A.F.F. note, A1.1, A1.2, C-3) | 143.0 | 🟢 GREEN |  |
| S24 | S24-RRS | 8.854 | 8.944 | 8.500 | 8.500 | 8.500 (A.F.F. note, A1.1, A1.2, C-3) | 75.2 | 🔴 RED | LF measured 8.94 vs Excel 8.854 (+1.02 %) |
| S41 | S41-B1H | 1.313 | 1.318 | 12.000 | 12.000 | 12.000 (A.F.F. note, A1.1, S41) | 15.7 | 🟢 GREEN |  |
| S41 | S41-B1V | 2.167 | 2.176 | 12.000 | 12.000 | 12.000 (A.F.F. note, A1.1, S41) | 26.0 | 🟢 GREEN |  |
| S41 | S41-B2H | 1.667 | 1.673 | 12.000 | 12.000 | 12.000 (A.F.F. note, A1.1, S41) | 20.0 | 🟢 GREEN |  |
| S41 | S41-B2V | 1.313 | 1.318 | 12.000 | 12.000 | 12.000 (A.F.F. note, A1.1, S41) | 15.7 | 🟢 GREEN |  |
| S42 | S42-01+S42-02 | 64.606 | 64.664 | 14.505 / 7.672 | 14.505 / 7.672 | n/a (assumption) / n/a (assumption) | 759.9 | 🟠 AMBER | S42-01: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, A1.1, S42) - depends on the RFI-01 purlin assumption; S42-02: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, 6/A4.2) - depends on the RFI-01 purlin assumption |
| S42 | S42-03+S42-04 | 58.500 | 58.889 | 8.202 / 15.644 | 8.202 / 15.644 | n/a (assumption) / n/a (assumption) | 540.6 | 🔴 RED | LF measured 58.89 vs Excel 58.500 (+0.66 %); S42-03: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, 6/A4.2) - depends on the RFI-01 purlin assumption; S42-04: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, A1.1, S42) - depends on the RFI-01 purlin assumption |
| S43 | S43-OF-E | 8.000 | 8.036 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, A1.2) | 68.0 | 🟢 GREEN |  |
| S43 | S43-OF-S | 11.708 | 11.76 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, A1.2) | 99.5 | 🟢 GREEN |  |
| S43 | S43-OF-W | 8.000 | 8.036 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, A1.2) | 68.0 | 🟢 GREEN |  |
| S43 | S43-RR-S | 16.521 | 16.593 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, A1.2) | 140.4 | 🟢 GREEN |  |
| S43 | S43-RR-W | 8.500 | 8.538 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, A1.2) | 72.2 | 🟢 GREEN |  |
| S61 | S61-RR | 8.500 | 8.556 | 8.500 | 8.500 | 8.500 (A.F.F. note, 7/A4.2, A1.1, S61) | 72.2 | 🔴 RED | LF measured 8.56 vs Excel 8.500 (+0.65 %) |
| EXT-6CFMF | CORN-S | 36.000 | 36.222 | 7.969 | 7.969 | 7.969 (printed dimension, 1/A3.4) | 286.9 | 🔴 RED | LF measured 36.22 vs Excel 36.000 (+0.62 %) |
| EXT-6CFMF | EXT-MS1-6 | 6.000 | 6.011 | 20.667 | 20.667 | 20.667 (printed elevations, 1/A3.1) | 124.0 | 🟢 GREEN |  |
| EXT-6CFMF | EXT-MS2-6 | 6.000 | 6.011 | 20.667 | 20.667 | 20.667 (printed elevation above the printed F.F. datum, 1/A3.1) | 124.0 | 🟢 GREEN |  |
| EXT-8CFMF | EXT-MS1-8 | 6.000 | 6.011 | 20.667 | 20.667 | 20.667 (printed elevations, 1/A3.1) | 124.0 | 🟢 GREEN |  |
| EXT-8CFMF | EXT-MS2-8 | 6.000 | 6.011 | 20.667 | 20.667 | 20.667 (printed elevation above the printed F.F. datum, 1/A3.1) | 124.0 | 🟢 GREEN |  |
| OTHER FRAMING | HEAD-A-6 | 38.667 | 38.756 | 9.333 | 9.333 | 9.333 (printed elevations, 2/A3.1) | 360.9 | 🟢 GREEN |  |
| OTHER FRAMING | HEAD-A-8 | 38.667 | 38.756 | 9.333 | 9.333 | 9.333 (printed elevations, 2/A3.1) | 360.9 | 🟢 GREEN |  |
| OTHER FRAMING | VH-B1 | 5.667 | 5.633 | 4.286 | 4.286 | n/a (assumption) | 24.3 | 🔴 RED | LF measured 5.63 vs Excel 5.667 (-0.59 %); VH-B1: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, A5.2, B1, B2) - depends on the RFI-01 purlin assumption |
| OTHER FRAMING | VH-B2 | 5.667 | 5.633 | 4.286 | 4.286 | n/a (assumption) | 24.3 | 🔴 RED | LF measured 5.63 vs Excel 5.667 (-0.59 %); VH-B2: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, A5.2, B1, B2) - depends on the RFI-01 purlin assumption |
| OTHER FRAMING | VH-C | 8.750 | 8.967 | 4.286 | 4.286 | n/a (assumption) | 37.5 | 🔴 RED | LF measured 8.97 vs Excel 8.750 (+2.48 %); VH-C: no printed height to compare (assumption; sheets cited 1/A3.2, 2/A3.1, 2/A3.2, 3/A3.1, 3/A3.4, A5.2, B1, B2) - depends on the RFI-01 purlin assumption |

Height maps: height_map_A1.1.png
