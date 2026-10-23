# RANGOS v22 — propuesta (arbitraje #25, 2026-10-20)

Solo para el árbitro / estimador. **Nunca viaja en el zip ciego.** Base: rangos_v18m. Fuente de cada valor:
`BOA_Broomfield_REFERENCIA_v5.xlsx` (hojas "CAMBIOS v5" y "D1-D6 v5 detail") e imágenes `img/D1_*`, `img/D2_*`,
`img/D4_*`. Archivo de máquina: `anexos/rangos_v22.json`.

| Familia | v18m (min–max) | v22 (min–max) | Decisión | Operación |
|---|---|---|---|---|
| extra framing ATM | 49.87–51.41 | **381.39** | D1 | ATM wall A02.01 grid 2: studs 338.47 (23 full × 14.3583 + 1 cripple 8.23; S1.11 6" @ 16" + 12" zone) + bottom 21.46 + top 21.46 |
| 6" stud (todos los gauges) | 4,392.44–4,580.41 | **4,053.97–4,241.94** | D1 | − 338.47 (los studs de la wall del ATM se cuentan una vez, en el renglón del ATM) |
| bottom track (todos) | 1,347.53 | **1,326.07** | D1 | − 21.46 (bottom runner de la wall del ATM) |
| top / deflection track (todos) | 1,347.53 | **1,326.07** | D1 | − 21.46 (top runner de la wall del ATM) |
| header / box beam | 791.96 | **796.76** | D2 / D3 | 13 doors × 4.67 + 102 10.33 + ATM-WU 3.58 + MW01 4.46 + ATM-DU 14.17 + 6 windows × 37.33 + door 123 18.67 + grille 117.33 + VB-101 67.92 + VB-100A 31.00 + office front E (39.977 + 1.333) × 4 = 165.24 + W (18.508 + 1.333) × 4 = 79.37 |
| sill track | 119.09 | **119.14** | D5 | 6 windows × (8.0 + 1.333) × 2 = 112.00 + ATM-WU (2.25 + 1.333) × 1 = 3.58 + ATM-DU (2.2083 + 1.333) × 1 = 3.54 |
| FRT plywood (SF) | 6,481.82–6,855.85 | **6,478.55–6,852.58** | D4 | piers 26.86 → 23.59 (−3.27): (0.7589 + 0.7578 + 0.7589 + 0.5000) ft × 8.5 × 1 ply |
| track de ceilings / soffits | 1,323.03 | **1,246.00** | D6 | 1,323.03 − 77.03 (track de perímetro en los bordes de transición de Waiting 104, RFI-CEIL-104 del arbitraje #21) |

Sin cambio: todo lo demás de v18m, incluidos los valores aceptados por el usuario (3-5/8" stud, A1, G, G1, B2K,
Exterior 6" CFMF) y los criterios de partición (los revisa el usuario; van en v78).

## Propuestas NO aplicadas en rangos_v22.json (las decide el usuario)
- A5 (partition type): el plano respalda 45.75 LF (25B): A02.01 imprime 3'-1 1/2" con ticks sobre la línea A5 frente al
  MW01 y B3 / B4/A12.03 dibujan la partición sobre el cabinet (`img/A5_1_*`, `img/A5_3_*`). Rango vigente 39.12–42.76.
  Propuesta: 42.63–45.75 (o 45.75). Es criterio de partición: queda para la revisión del usuario.
- acoustical sealant: RFI de interfaz (10/A12.01 "SEALANT" en la jamb del office front BY BANK VENDOR, +193.00; 8/A12.10
  "1/4" SEALANT" del wall channel del glass GL-4, +40.00, glazing). Con D2 el bead del bulkhead sigue al box beam por
  frente (58.48 ft × 4 = 233.92 en vez de 180.00, +53.92). Rango vigente sin cambio hasta la respuesta.

## RFIs con delta (referencia v5)
- RFI-H6: R.O. del drive-up ATM 2'-2 1/2" (7/A08.11 plan, usado) vs 2'-2 1/8" (26.4", 5/A08.11): header −0.125, sill −0.031.
- RFI-H7: sill del drive-up ATM: el R.O. está acotado desde la línea de sill 2'-8 1/8" (6/A08.11) → 1 pieza (usado);
  si el 6" stud corre abierto hasta el plinth: −3.54 LF.
- RFI-ATM-H: alto de los studs de la wall del ATM: 14.3583 (bajo la perimeter beam W12X19, 10/S5.10; usado) vs B.O.D.
  15.375 "piso a deck" literal: +23.38 LF (23 studs × 1.0167).
- RFI-PIER-PLY: 1/A09.25 y 2/A09.25 dibujan 2 capas con rótulo singular "3/4" FRT PLYWOOD": +23.59 SF si son 2 plies.
- RFI-CEIL-DIR: dirección del carrying channel no impresa: N-S 316.45 (usado por las dos corridas v77) / E-W 321.05
  (+4.60) / lado largo por room 347.81 (+31.36).
