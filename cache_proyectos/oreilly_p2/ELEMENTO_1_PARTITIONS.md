# ELEMENTO 1 — PARTITIONS rev3 (O'Reilly Evans CO #1, pasada 2)
rev3 = rev2 + (1) RFI-01 con −0.667 ft = purlin 8" SUPUESTO por shop drawing PEMB [PENDIENTE] (se quitó el 10" escalado, prohibido por #0) · (2) board por cara SIN descontar puertas (R70.3): quitadas deducciones en S21-N (doors 2, 3, 7), S43-OF-S (door 4), S43-RR-S (doors 5, 6); se quedan ventanas D1/D2 de S21-S (76.49 SF) y bandas de head de storefronts A/B1/B2/C · (3) head storefront A revisado por tramo (img_rev3/) · (4) dueño de esquina documentado. Números: overlay.py + canon.py / partition_types.py (modo eje), avisos = []. Tiempo: rev1 ~61 + rev2 ~38 + rev3 ~15 min.

## Regla de dueño de esquina (proceso/revision_dirigida.md § Corner ownership)
R70.2 (SKILL.md): "Cada esquina L / T tiene UN dueño: un wall llega a la cara exterior del otro y el otro arranca en su cara. Ni esquina sin dueño ni doble." Dueño leído por R78.35 (el wall cuyo stud core cruza el cuadrado de la esquina en la planta corre; el otro muere contra él).
- S24-OF / S43-OF-W (N36), S24-OF / S43-OF-E (N37), S24-RR / S43-RR-W (N40), S24-RRS / S43-RR-S (N42): dueño **S24** (el hatch de S24 llena el cuadrado en 1/A1.1; S43 arranca en la cara de S24, 322.4 pt).
- S21-S / S24-RR: dueño **S21-S** (corre de cara de CMU a cara de CMU; S24-RR muere en su cara, 1074.9 pt). S21-E y S21-S son paralelos a S24 (no forman esquina).

## Tabla
| Type | Wall ID | LF | H (ft) | Wall SF (LF×H) | Board SF | Caras / board |
|---|---|---|---|---|---|---|
| S21 | S21-N | 85.000 | 14.844 | 1,261.74 | 1,261.74 | 1 cara 5/8" X |
| S21 | S21-E | 84.646 | 13.958 | 1,181.49 | 924.71 | 1 cara X; 28.531 LF detrás de S24 solo arriba del hard lid (4.958) |
| S21 | S21-S | 85.000 | 14.844 | 1,261.74 | 1,093.66 | 1 cara X; 9.357 LF detrás de S24 (5.055); −D1/D2 76.49 |
| S21 | S21-W1 | 9.156 | 15.729 | 144.01 | 144.01 | 1 cara X |
| S21 | S21-W2 | 24.823 | 15.729 | 390.44 | 390.44 | 1 cara X |
| **S21 subtotal** | 5 | **288.62** | | **4,239.42** | **3,814.56** | |
| S24 | OF / RR / RRS | 11.708 / 16.823 / 8.854 = 37.38 | 8.5 | 317.78 | 317.77 | 1 cara: X / X WR / X WR |
| S41 | B1V / B1H / B2H / B2V | 6.46 | 12.0 | 77.52 | 77.52 | 1 cara X |
| S42 | S42-01+S42-02 | 38.667 + 25.455 = 64.122 | 11.792 pond. (14.505 / 7.672) | 756.15 | 1,368.50 | 2 caras X |
| S42 | S42-03+S42-04 | 50.333 + 8.167 = 58.500 | 9.241 pond. (8.202 / 15.644) | 540.59 | 898.66 | 2 caras X |
| **S42 subtotal** | 2 | **122.62** | | **1,296.74** | **2,267.16** | |
| S43 | OF-W / OF-E / OF-S / RR-W / RR-S | 8.0 / 8.0 / 11.708 / 8.5 / 16.521 = 52.73 | 8.5 (caras afuera 9.0) | 448.20 | 922.76 | 2 caras, sin descontar doors |
| S61 | S61-RR | 8.5 | 8.5 | 72.25 | 144.50 | 2 caras X WR |
| EXT-8CFMF | MS1-8 / MS2-8 | 6.0 / 6.0 | 20.667 | 248.00 | 154.89 | int. X a 12.0 (MS2 parcial 15.729) |
| EXT-6CFMF | MS1-6 / MS2-6 / CORN-S | 48.0 | 20.667 / 20.667 / 7.969 | 534.88 | 0 | |
| OTHER | HEAD-A-8 / HEAD-A-6 | 38.667 c/u | 9.333 | 721.76 | 20.45 | int. 11'-4"→12'-0" (1/A5.2) en 18'-8" + 12'-0" = 30.667 LF; vestíbulo 8'-0" = 0 [PENDIENTE RFI-15: B = +5.33 SF X, +5.33 SF 1/4", +8 LF RC, +8 LF corner bead] |
| OTHER | VH-C / VH-B1 / VH-B2 | 8.75 / 5.667 / 5.667 | 4.286 | 86.08 | 13.40 | 600S162-43 18 ga (dec. 14) |
Misc del head (RFI-06 = A): underside 13.42 SF 5/8 X + 11.82 SF 1/4" + 30.667 LF corner bead; 1/4" + RC en piers.

Interior S21–S61: 516.31 LF · Wall SF 6,451.91 · Board SF 7,544.27.
S21 detrás de S24: 37.888 LF (E 11.708 + 16.823; S 9.357) · board arriba del hard lid 188.76 SF → S21 CON 288.62 LF / SIN 250.73 LF.
Pendiente #0 fuera de partitions: purlin bay 5.0 ft escalado en G09 (1/S5.1, 4/S5.1: 600S200 / L4x4) → se corrige en ELEMENTO 3/5.
