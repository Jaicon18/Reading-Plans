# O'Reilly Auto Parts - Evans, CO #1 — quick markup review

Program: revision_markups.py · printed scales {'A1.1': '9.000 pt/ft'} · LF ±0.5 %, H exact · GREEN 22 / RED 8

| Type | Wall ID | Excel LF | Measured LF | Excel H | Depth | Area SF | Verdict | Failures |
|---|---|---|---|---|---|---|---|---|
| S21 | S21-E | 84.646 | 84.911 | 13.958 | 13.958 | 1181.5 | 🟢 GREEN |  |
| S21 | S21-N | 85.000 | 85.389 | 14.844 | 14.844 | 1261.7 | 🟢 GREEN |  |
| S21 | S21-S | 85.000 | 85.389 | 14.844 | 14.844 | 1261.7 | 🟢 GREEN |  |
| S21 | S21-W1 | 9.156 | 9.189 | 15.729 | 15.729 | 144.1 | 🟢 GREEN |  |
| S21 | S21-W2 | 24.823 | 24.944 | 15.729 | 15.729 | 390.4 | 🟢 GREEN |  |
| S24 | S24-OF | 11.708 | 11.789 | 8.500 | 8.500 | 99.5 | 🔴 RED | LF measured 11.79 vs Excel 11.708 (+0.69 %) |
| S24 | S24-RR | 16.823 | 16.844 | 8.500 | 8.500 | 143.0 | 🟢 GREEN |  |
| S24 | S24-RRS | 8.854 | 8.944 | 8.500 | 8.500 | 75.2 | 🔴 RED | LF measured 8.94 vs Excel 8.854 (+1.02 %) |
| S41 | S41-B1H | 1.313 | 1.318 | 12.000 | 12.000 | 15.7 | 🟢 GREEN |  |
| S41 | S41-B1V | 2.167 | 2.176 | 12.000 | 12.000 | 26.0 | 🟢 GREEN |  |
| S41 | S41-B2H | 1.667 | 1.673 | 12.000 | 12.000 | 20.0 | 🟢 GREEN |  |
| S41 | S41-B2V | 1.313 | 1.318 | 12.000 | 12.000 | 15.7 | 🟢 GREEN |  |
| S42 | S42-01+S42-02 | 64.606 | 64.664 | 14.505 / 7.672 | 14.505 / 7.672 | 759.9 | 🟢 GREEN |  |
| S42 | S42-03+S42-04 | 58.500 | 58.889 | 8.202 / 15.644 | 8.202 / 15.644 | 540.6 | 🔴 RED | LF measured 58.89 vs Excel 58.500 (+0.66 %) |
| S43 | S43-OF-E | 8.000 | 8.036 | 8.500 | 8.500 | 68.0 | 🟢 GREEN |  |
| S43 | S43-OF-S | 11.708 | 11.76 | 8.500 | 8.500 | 99.5 | 🟢 GREEN |  |
| S43 | S43-OF-W | 8.000 | 8.036 | 8.500 | 8.500 | 68.0 | 🟢 GREEN |  |
| S43 | S43-RR-S | 16.521 | 16.593 | 8.500 | 8.500 | 140.4 | 🟢 GREEN |  |
| S43 | S43-RR-W | 8.500 | 8.538 | 8.500 | 8.500 | 72.2 | 🟢 GREEN |  |
| S61 | S61-RR | 8.500 | 8.556 | 8.500 | 8.500 | 72.2 | 🔴 RED | LF measured 8.56 vs Excel 8.500 (+0.65 %) |
| EXT-6CFMF | CORN-S | 36.000 | 36.222 | 7.969 | 7.969 | 286.9 | 🔴 RED | LF measured 36.22 vs Excel 36.000 (+0.62 %) |
| EXT-6CFMF | EXT-MS1-6 | 6.000 | 6.011 | 20.667 | 20.667 | 124.0 | 🟢 GREEN |  |
| EXT-6CFMF | EXT-MS2-6 | 6.000 | 6.011 | 20.667 | 20.667 | 124.0 | 🟢 GREEN |  |
| EXT-8CFMF | EXT-MS1-8 | 6.000 | 6.011 | 20.667 | 20.667 | 124.0 | 🟢 GREEN |  |
| EXT-8CFMF | EXT-MS2-8 | 6.000 | 6.011 | 20.667 | 20.667 | 124.0 | 🟢 GREEN |  |
| OTHER FRAMING | HEAD-A-6 | 38.667 | 38.756 | 9.333 | 9.333 | 360.9 | 🟢 GREEN |  |
| OTHER FRAMING | HEAD-A-8 | 38.667 | 38.756 | 9.333 | 9.333 | 360.9 | 🟢 GREEN |  |
| OTHER FRAMING | VH-B1 | 5.667 | 5.633 | 4.286 | 4.286 | 24.3 | 🔴 RED | LF measured 5.63 vs Excel 5.667 (-0.59 %) |
| OTHER FRAMING | VH-B2 | 5.667 | 5.633 | 4.286 | 4.286 | 24.3 | 🔴 RED | LF measured 5.63 vs Excel 5.667 (-0.59 %) |
| OTHER FRAMING | VH-C | 8.750 | 8.967 | 4.286 | 4.286 | 37.5 | 🔴 RED | LF measured 8.97 vs Excel 8.750 (+2.48 %) |

Height maps: height_map_A1.1.png

## Notes for the reviewer
- All 30 Excel rows (32 markups; S42-01+S42-02 and S42-03+S42-04 are one row each) match the Excel in Wall ID, TYPE, Depth = H (exact) and label Wall Area = LF x H. Every RED row is a LENGTH check only.
- Sheet A1.1 is a raster scan whose drawn length is 0.44 % longer than the printed scale (printed overall 86'-4" measures 9.04 pt/ft vs 1/8" = 9.00 pt/ft). Re-measuring at the PRINTED scale therefore adds about +0.44 % to every wall: S24-OF (+0.69 %), S42-03+S42-04 (+0.66 %), S61-RR (+0.65 %) and CORN-S (+0.62 %) are RED mainly from that scan offset (each one is +0.2 % or less against the calibrated scale).
- Real geometry differences (line drawn shorter or longer than the printed dimension used for the LF): VH-C +2.48 %, S24-RRS +1.02 %, VH-B1 / VH-B2 -0.59 %. The Excel LF comes from printed dimensions (A5.2 vestibule hold dims, A1.1 / 1A/A4.1 restroom dims); only the markup line is off.
- Heights of S21, S42 and VH walls depend on the assumed 8" PEMB purlin depth (RFI-01, closed: confirm with GC / PEMB shop drawings).
- height_map_A1.1.png: every wall painted by its height with its Wall ID; a wall whose color differs from its room is the one to check.
