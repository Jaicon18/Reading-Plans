# Double-reading review — canon_A.json vs canon_B.json

Inventory: inventario.json · partition rule: **eje** · match tolerance: 2 % of LF · tag-to-wall radius: 5.0 ft

## Matching walls (one line per type)

- **W2**: 1 walls match · A 2 walls / 14.64 LF · B 2 walls / 17.97 LF · inventory tags 3
- ****: 0 walls match · A 2 walls / 4.76 LF · B 0 walls / 0 LF · inventory tags 0
- **W1**: 5 walls match · A 5 walls / 154.8 LF · B 5 walls / 155.08 LF · inventory tags 10
- **W4**: 5 walls match · A 6 walls / 51.39 LF · B 6 walls / 50.98 LF · inventory tags 7
- **CF**: 0 walls match · A 0 walls / 0 LF · B 2 walls / 4.77 LF · inventory tags 0

## Items to review

1. **W2** — Sheet A2.0 (p.5) — LF differs +3.33 LF (23.9 %): A W2-01 10.64 LF vs B W2-01 13.97 LF [matched by position] — ![img](img/001_DIF_W2_A2.0_p5.png)
2. **W4** — Sheet A2.0 (p.5) — LF differs -0.40 LF (3.7 %): A W4-04 10.99 LF vs B W4-04 10.59 LF [matched by position] — ![img](img/002_DIF_W4_A2.0_p5.png)
3. **** — Sheet A2.0 (p.5) — only in reading A: CF-01 2.38 LF — ![img](img/003_ONLYA__A2.0_p5.png)
4. **** — Sheet A2.0 (p.5) — only in reading A: CF-02 2.38 LF — ![img](img/004_ONLYA__A2.0_p5.png)
5. **CF** — Sheet A2.0 (p.5) — only in reading B: CF-01 2.38 LF — no image: no page or no geometry
6. **CF** — Sheet A2.0 (p.5) — only in reading B: CF-02 2.38 LF — no image: no page or no geometry

## Alerts (inventory cross-check)

1. **TAG SIN WALL** — W1 — Sheet A2.0 (p.5): tag PT0018 W1 has no wall of its type within 5.0 ft in reading A nor B — ![img](img/007_ALERT_W1_A2.0_p5.png)
2. **TAG SIN WALL** — W2 — Sheet A2.0 (p.5): tag PT0019 W2 has no wall of its type within 5.0 ft in reading A nor B — ![img](img/008_ALERT_W2_A2.0_p5.png)
3. **TAG SIN WALL** — W2A — Sheet A2.0 (p.5): tag PT0020 W2A has no wall of its type within 5.0 ft in reading A nor B — ![img](img/009_ALERT_W2A_A2.0_p5.png)
4. **TAG SIN WALL** — W3 — Sheet A2.0 (p.5): tag PT0021 W3 has no wall of its type within 5.0 ft in reading A nor B — ![img](img/010_ALERT_W3_A2.0_p5.png)
5. **TAG SIN WALL** — W4 — Sheet A2.0 (p.5): tag PT0022 W4 has no wall of its type within 5.0 ft in reading A nor B — ![img](img/011_ALERT_W4_A2.0_p5.png)
6. **TYPE NO INVENTARIADO** —  — Sheet A2.0 (p.5): reading A uses type  — not a schedule type (exterior / other framing / typo?) — ![img](img/012_ALERT__A2.0_p5.png)
7. **TYPE NO INVENTARIADO** — CF — Sheet A2.0 (p.5): reading B uses type CF — not a schedule type (exterior / other framing / typo?) — no image: no page or no geometry

## Notes

- A: W2-01a (W2, A2.0) stub sin tag <= 0.5 ft que no toca un wall con tag de su type: no es wall de la lista ni suma LF (R74.2); su material sigue en el canon
- A:  (A2.0): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan
- B: CF-01 (CF, A2.0) sin band H|V (ori BOX): wall propio, no se puede unir
- B: CF-02 (CF, A2.0) sin band H|V (ori BOX): wall propio, no se puede unir
- B: CF (A2.0): ningún segmento trae tag_ids; corte en cada esquina (regla 1 de eje), returns / jogs <= 1.0 ft se suman al tramo que tocan

Legend: blue = reading A, orange = reading B, red circle = inventory tag.
