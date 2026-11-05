# Double-reading review — canon_A.json vs canon_B.json

Inventory: inventario.json · partition rule: **eje** · match tolerance: 2 % of LF · tag-to-wall radius: 5.0 ft

## Matching walls (one line per type)

- **A3**: 1 walls match · A 3 walls / 99.86 LF · B 2 walls / 99.86 LF · inventory tags 4
- **C3**: 0 walls match · A 1 walls / 31.54 LF · B 1 walls / 35.54 LF · inventory tags 2
- **D**: 1 walls match · A 1 walls / 7.67 LF · B 1 walls / 7.67 LF · inventory tags 1
- **E3**: 4 walls match · A 13 walls / 51.48 LF · B 8 walls / 57.45 LF · inventory tags 11

## Items to review

1. **A3** — Sheet A100 (p.7) — LF differs +14.41 LF (33.3 %): A A3-02 28.83 LF vs B A3-01 43.24 LF [matched by position] — ![img](img/001_DIF_A3_A100_p7.png)
2. **C3** — Sheet A100 (p.7) — LF differs +4.00 LF (11.2 %): A C3-01 31.54 LF vs B C3-01+C3-02 35.54 LF [matched by position] — ![img](img/002_DIF_C3_A100_p7.png)
3. **E3** — Sheet A100 (p.7) — LF differs +3.89 LF (52.3 %): A E3-05 3.54 LF vs B E3-04 7.43 LF [matched by position] — ![img](img/003_DIF_E3_A100_p7.png)
4. **E3** — Sheet A100 (p.7) — LF differs -4.00 LF (28.6 %): A E3-14+E3-11a+E3-11b 13.99 LF vs B E3-08 9.99 LF [matched by position] — ![img](img/004_DIF_E3_A100_p7.png)
5. **E3** — Sheet A100 (p.7) — LF differs +4.08 LF (58.3 %): A E3-10 2.92 LF vs B E3-07 7.00 LF [matched by position] — ![img](img/005_DIF_E3_A100_p7.png)
6. **E3** — Sheet A100 (p.7) — LF differs +8.86 LF (55.3 %): A E3-03 7.17 LF vs B E3-02+E3-03+E3-06 16.03 LF (2 straight segments) [matched by position] — ![img](img/006_DIF_E3_A100_p7.png)
7. **A3** — Sheet A100 (p.7) — only in reading A: A3-01 14.41 LF — ![img](img/007_ONLYA_A3_A100_p7.png)
8. **E3** — Sheet A100 (p.7) — only in reading A: E3-02 3.36 LF — ![img](img/008_ONLYA_E3_A100_p7.png)
9. **E3** — Sheet A100 (p.7) — only in reading A: E3-06 1.08 LF — ![img](img/009_ONLYA_E3_A100_p7.png)
10. **E3** — Sheet A100 (p.7) — only in reading A: E3-08 1.08 LF — ![img](img/010_ONLYA_E3_A100_p7.png)
11. **E3** — Sheet A100 (p.7) — only in reading A: E3-09 0.75 LF — ![img](img/011_ONLYA_E3_A100_p7.png)
12. **E3** — Sheet A100 (p.7) — only in reading A: E3-04 0.58 LF — ![img](img/012_ONLYA_E3_A100_p7.png)

## Alerts (inventory cross-check)

1. **TAG SIN WALL** — CO2 — Sheet G003 (p.4): tag PC0001 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/013_ALERT_CO2_G003_p4.png)
2. **TAG SIN WALL** — CO2 — Sheet D100 (p.5): tag PC0002 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/014_ALERT_CO2_D100_p5.png)
3. **TAG SIN WALL** — CO2 — Sheet D101 (p.6): tag PC0003 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/015_ALERT_CO2_D101_p6.png)
4. **TAG SIN WALL** — CO2 — Sheet A100 (p.7): tag PC0021 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/016_ALERT_CO2_A100_p7.png)
5. **TAG SIN WALL** — CO2 — Sheet A101 (p.8): tag PC0022 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/017_ALERT_CO2_A101_p8.png)
6. **TAG SIN WALL** — CO2 — Sheet A102 (p.9): tag PC0023 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/018_ALERT_CO2_A102_p9.png)
7. **TAG SIN WALL** — CO2 — Sheet A103 (p.10): tag PC0024 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/019_ALERT_CO2_A103_p10.png)
8. **TAG SIN WALL** — CO2 — Sheet A200 (p.12): tag PC0025 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/020_ALERT_CO2_A200_p12.png)
9. **TAG SIN WALL** — CO2 — Sheet M101 (p.25): tag PC0026 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/021_ALERT_CO2_M101_p25.png)
10. **TAG SIN WALL** — TC2 — Sheet E101 (p.29): tag PC0027 TC2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/022_ALERT_TC2_E101_p29.png)
11. **TAG SIN WALL** — TC1 — Sheet E101 (p.29): tag PC0028 TC1 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/023_ALERT_TC1_E101_p29.png)
12. **TAG SIN WALL** — CO2 — Sheet E101 (p.29): tag PC0029 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/024_ALERT_CO2_E101_p29.png)
13. **TAG SIN WALL** — TC2 — Sheet E111 (p.30): tag PC0030 TC2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/025_ALERT_TC2_E111_p30.png)
14. **TAG SIN WALL** — TC1 — Sheet E111 (p.30): tag PC0031 TC1 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/026_ALERT_TC1_E111_p30.png)
15. **TAG SIN WALL** — CO2 — Sheet E111 (p.30): tag PC0032 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/027_ALERT_CO2_E111_p30.png)
16. **TAG SIN WALL** — CO2 — Sheet P101 (p.35): tag PC0033 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/028_ALERT_CO2_P101_p35.png)
17. **TAG SIN WALL** — TC2 — Sheet FA101 (p.37): tag PC0034 TC2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/029_ALERT_TC2_FA101_p37.png)
18. **TAG SIN WALL** — TC1 — Sheet FA101 (p.37): tag PC0035 TC1 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/030_ALERT_TC1_FA101_p37.png)
19. **TAG SIN WALL** — CO2 — Sheet FA101 (p.37): tag PC0036 CO2 has no wall of its type within 5.0 ft in reading A nor B (tag in a symbol that is NOT in the partition schedule: missing type or RFI) — ![img](img/031_ALERT_CO2_FA101_p37.png)

Legend: blue = reading A, orange = reading B, red circle = inventory tag.
