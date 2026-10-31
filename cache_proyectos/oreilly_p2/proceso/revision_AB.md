# Double-reading review — takeoff_canon_A.json vs takeoff_canon_B.json

Inventory: inventario.json · partition rule: **eje** · match tolerance: 2 % of LF · tag-to-wall radius: 5.0 ft

## Matching walls (one line per type)

- **S21**: 5 walls match · A 5 walls / 288.59 LF · B 5 walls / 287.92 LF · inventory tags 0
- **S24**: 1 walls match · A 3 walls / 37.14 LF · B 3 walls / 36.76 LF · inventory tags 0
- **S43**: 2 walls match · A 5 walls / 50.94 LF · B 5 walls / 52.3 LF · inventory tags 0
- **S61**: 0 walls match · A 1 walls / 8.1 LF · B 1 walls / 8.4 LF · inventory tags 0
- **S41**: 1 walls match · A 4 walls / 6.26 LF · B 4 walls / 6.46 LF · inventory tags 0
- **S42**: 2 walls match · A 2 walls / 115.71 LF · B 2 walls / 115.91 LF · inventory tags 0
- **EXT-8CFMF**: 0 walls match · A 2 walls / 11.94 LF · B 1 walls / 50.67 LF · inventory tags 0
- **EXT-6CFMF**: 1 walls match · A 3 walls / 47.94 LF · B 2 walls / 86.67 LF · inventory tags 0

## Items to review

1. **S24** — Sheet A1.1 (p.37) — LF differs -0.55 LF (3.3 %): A S24-02 16.77 LF vs B S24-RR 16.22 LF [matched by position] — ![img](img/001_DIF_S24_A1.1_p37.png)
2. **S24** — Sheet A1.1 (p.37) — LF differs +0.27 LF (3.1 %): A S24-03 8.56 LF vs B S24-RRS 8.83 LF [matched by position] — ![img](img/002_DIF_S24_A1.1_p37.png)
3. **S43** — Sheet A1.1 (p.37) — LF differs +0.30 LF (3.6 %): A S43-RW 8.10 LF vs B S43-RR-W 8.40 LF [matched by position] — ![img](img/003_DIF_S43_A1.1_p37.png)
4. **S43** — Sheet A1.1 (p.37) — LF differs +0.45 LF (5.7 %): A S43-OE 7.43 LF vs B S43-OF-E 7.88 LF [matched by position] — ![img](img/004_DIF_S43_A1.1_p37.png)
5. **S43** — Sheet A1.1 (p.37) — LF differs +0.45 LF (5.7 %): A S43-OW 7.43 LF vs B S43-OF-W 7.88 LF [matched by position] — ![img](img/005_DIF_S43_A1.1_p37.png)
6. **S61** — Sheet A1.1 (p.37) — LF differs +0.30 LF (3.6 %): A S61-01 8.10 LF vs B S61-RR 8.40 LF [matched by position] — ![img](img/006_DIF_S61_A1.1_p37.png)
7. **S41** — Sheet A1.1 (p.37) — LF differs -0.36 LF (21.4 %): A S41-NW-H 1.67 LF vs B S41-B1H 1.31 LF [matched by position] — ![img](img/007_DIF_S41_A1.1_p37.png)
8. **S41** — Sheet A1.1 (p.37) — LF differs +0.42 LF (19.2 %): A S41-NW-V 1.75 LF vs B S41-B1V 2.17 LF [matched by position] — ![img](img/008_DIF_S41_A1.1_p37.png)
9. **S41** — Sheet A1.1 (p.37) — LF differs +0.14 LF (10.9 %): A S41-SW-V 1.17 LF vs B S41-B2V 1.31 LF [matched by position] — ![img](img/009_DIF_S41_A1.1_p37.png)
10. **EXT-8CFMF** — Sheet A1.1 (p.37) — LF differs +44.70 LF (88.2 %): A EXT-W-02-8 5.97 LF vs B EXT-MS1-8+HEAD-A-8+EXT-MS2-8 50.67 LF [matched by position] — ![img](img/010_DIF_EXT-8CFMF_A1.1_p37.png)
11. **EXT-6CFMF** — Sheet A1.1 (p.37) — LF differs +44.70 LF (88.2 %): A EXT-W-02-6 5.97 LF vs B EXT-MS1-6+HEAD-A-6+EXT-MS2-6 50.67 LF [matched by position] — ![img](img/011_DIF_EXT-6CFMF_A1.1_p37.png)
12. **EXT-8CFMF** — Sheet A1.1 (p.37) — only in reading A: EXT-W-01-8 5.97 LF — ![img](img/012_ONLYA_EXT-8CFMF_A1.1_p37.png)
13. **EXT-6CFMF** — Sheet A1.1 (p.37) — only in reading A: EXT-W-01-6 5.97 LF — ![img](img/013_ONLYA_EXT-6CFMF_A1.1_p37.png)

## Alerts (inventory cross-check)

1. **TYPE NO INVENTARIADO** — S21 — Sheet A1.1 (p.37): reading A uses type S21 — not a schedule type (exterior / other framing / typo?) — ![img](img/014_ALERT_S21_A1.1_p37.png)
2. **TYPE NO INVENTARIADO** — S24 — Sheet A1.1 (p.37): reading A uses type S24 — not a schedule type (exterior / other framing / typo?) — ![img](img/015_ALERT_S24_A1.1_p37.png)
3. **TYPE NO INVENTARIADO** — S43 — Sheet A1.1 (p.37): reading A uses type S43 — not a schedule type (exterior / other framing / typo?) — ![img](img/016_ALERT_S43_A1.1_p37.png)
4. **TYPE NO INVENTARIADO** — S61 — Sheet A1.1 (p.37): reading A uses type S61 — not a schedule type (exterior / other framing / typo?) — ![img](img/017_ALERT_S61_A1.1_p37.png)
5. **TYPE NO INVENTARIADO** — S41 — Sheet A1.1 (p.37): reading A uses type S41 — not a schedule type (exterior / other framing / typo?) — ![img](img/018_ALERT_S41_A1.1_p37.png)
6. **TYPE NO INVENTARIADO** — S42 — Sheet A1.1 (p.37): reading A uses type S42 — not a schedule type (exterior / other framing / typo?) — ![img](img/019_ALERT_S42_A1.1_p37.png)
7. **TYPE NO INVENTARIADO** — EXT-8CFMF — Sheet A1.1 (p.37): reading A uses type EXT-8CFMF — not a schedule type (exterior / other framing / typo?) — ![img](img/020_ALERT_EXT-8CFMF_A1.1_p37.png)
8. **TYPE NO INVENTARIADO** — EXT-6CFMF — Sheet A1.1 (p.37): reading A uses type EXT-6CFMF — not a schedule type (exterior / other framing / typo?) — ![img](img/021_ALERT_EXT-6CFMF_A1.1_p37.png)
9. **TYPE NO INVENTARIADO** — S21 — Sheet A1.1 (p.37): reading B uses type S21 — not a schedule type (exterior / other framing / typo?) — ![img](img/022_ALERT_S21_A1.1_p37.png)
10. **TYPE NO INVENTARIADO** — EXT-8CFMF — Sheet A1.1 (p.37): reading B uses type EXT-8CFMF — not a schedule type (exterior / other framing / typo?) — ![img](img/023_ALERT_EXT-8CFMF_A1.1_p37.png)
11. **TYPE NO INVENTARIADO** — EXT-6CFMF — Sheet A1.1 (p.37): reading B uses type EXT-6CFMF — not a schedule type (exterior / other framing / typo?) — ![img](img/024_ALERT_EXT-6CFMF_A1.1_p37.png)
12. **TYPE NO INVENTARIADO** — S24 — Sheet A1.1 (p.37): reading B uses type S24 — not a schedule type (exterior / other framing / typo?) — ![img](img/025_ALERT_S24_A1.1_p37.png)
13. **TYPE NO INVENTARIADO** — S43 — Sheet A1.1 (p.37): reading B uses type S43 — not a schedule type (exterior / other framing / typo?) — ![img](img/026_ALERT_S43_A1.1_p37.png)
14. **TYPE NO INVENTARIADO** — S61 — Sheet A1.1 (p.37): reading B uses type S61 — not a schedule type (exterior / other framing / typo?) — ![img](img/027_ALERT_S61_A1.1_p37.png)
15. **TYPE NO INVENTARIADO** — S41 — Sheet A1.1 (p.37): reading B uses type S41 — not a schedule type (exterior / other framing / typo?) — ![img](img/028_ALERT_S41_A1.1_p37.png)
16. **TYPE NO INVENTARIADO** — S42 — Sheet A1.1 (p.37): reading B uses type S42 — not a schedule type (exterior / other framing / typo?) — ![img](img/029_ALERT_S42_A1.1_p37.png)

## Notes

- A: S24 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- A: S43 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- A: S41 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- A: S42 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: S21 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: S24 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: S43 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: S41 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: S42 (A1.1): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan

Legend: blue = reading A, orange = reading B, red circle = inventory tag.
