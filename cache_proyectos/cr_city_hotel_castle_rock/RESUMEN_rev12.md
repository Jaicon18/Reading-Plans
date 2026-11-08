# RESUMEN rev12 — CR City Hotel (Castle Rock, CO)

rev12 reemplaza a rev11. Origen: (1) tu orden U-155 del 8-nov (vía COORDINACIÓN): "buscar hasta encontrar las respuestas en los planos; si después de varios intentos no lo encuentras usa los códigos del IBC y cita su referencia". Apliqué la orden a los 11 RFI abiertos de rev11 y a los valores "assumed". (2) Revisión dirigida de COORDINACIÓN sobre rev11: E1–E4 + 2 observaciones (abajo).

## RFI cerrados
- **RFI-28** (cabeza de los fire barriers 2 HR de L1): el plano no imprime el detalle. Lo resuelve el código: IBC 2018 Section 707.5, "fire barriers shall extend … to the underside of the floor or roof sheathing, slab or deck above".
  - Sigue cargado a 13'-9 1/2" [DERIVADO]: 14'-0" − 1 1/2" topping − 1/4" mat − 3/4" sheathing (S1.02).
  - Fondo de las trusses de L2 aquí: 14'-0" − 2 1/2" − 18" (S1.03) = 11'-11 1/2" [DERIVADO]. 707.5 lleva el muro más allá, hasta el sheathing.
  - Corrección de COORDINACIÓN: el 12'-0" B.O. DECK de 5/A5.04 es la metal deck de los grids H–K, no de este bloque. Ya no se cita.
  - **DA-7 retirado.**
- **RFI-25** (FW.4-L4-19): el 1 HR está impreso.
  - Tag "FW.4 | 1" (1/A2.04), "1HR FP" en 2/A0.02 y puerta 411.1 "20 MIN" (A8.00).
  - El ensamble es la fire partition de IBC 2018 Section 708, Table 721.1(2): 1 capa 5/8" Type X por cara. Así está cargado; delta 0.

## Valores "assumed" con el rating impreso (sin cambio de cantidad)
- **ELEC 321:** el code plan de L3 en A0.02 encierra ELEC 321 / LINEN 322 / CLEANING 323 con la línea "1HR FP". Lo cité en las filas.
- **Demising sin tag (DW.4-1):** nota de A0.00 "CORRIDOR AND UNIT DEMISING WALLS CONSTRUCTED AS 1HR FIRE PARTITIONS" (IBC 2018 Section 708). Citada en las filas.
- **Spacings ya resueltos con su norma:**
  - resilient channel 16" o.c. (UL L546 / ASTM C754);
  - C-H studs 24" o.c. (UL U415);
  - suspensión según el fabricante: no la regula el código.

## RFI que siguen abiertos (ni el plano ni el código los resuelven)
- RFI-04: tipo de walls sin tag (el código da el rating, no el tipo).
- RFI-13: stud del MB-1 (listing UL no impreso).
- RFI-15: board del cielo RS-1 sin rating ("none applies").
- RFI-17, 21, 22: preguntas de alcance.
- RFI-23, 24: conflicto plano contra plano (A0.00 vs tags; 118B es tu decisión, U-052).
- RFI-26: furring sobre CMU (el código no lo pide).

## Revisión dirigida de COORDINACIÓN sobre rev11
- **E1** Deltas recalculados desde las filas actuales (W.6-2 de L1 ya a 13.7917 ft):
  - DA-1 −149.52 → **−171.84 SF**; DA-2 −360.24 → **−414.03 SF** [DERIVADO, suma L × H × caras × capas por fila].
  - Review Item 112: **−205.50 SF**; Review Item 118B: **−159.98 SF**.
  - Review Item W.6-L1-25: A8.00 imprime la puerta 120.1 de **5'-0" × 8'-0"** [CONFIRMADO]; el plano 1/A7.50 acota el vano en 7'-11". Es un conflicto puerta-plano. Base gruesa (U-057) = 8.01 × 13.7917 × 4 = 441.89 SF. Si se descuenta el vano: −160.00 SF (schedule) o −253.44 SF (ancho del plano).
  - Compuerta nueva **CB_CR_R12_E1**: todo delta de DA / Review Item se recalcula desde las filas actuales (±0.5 %).
- **E2** La proposal ahora regenera el DELTA real antes de armarse (PRICING A2 = cambios rev11 → rev12).
- **E3** Exterior sheathing unificado a glass-mat ASTM C1177 (06 16 00 2.5.B) en PROPOSAL y PRICING.
- **E4** Cita del compound completa: spec 3.6.E.1 "Level 1: For ceiling plenum areas, concealed areas" y 3.6.D (Level 1 = tape set only, 1 de las 3 aplicaciones de Level 4) → × 2/3 [DERIVADO]. El corte venía de un límite de 240 caracteres en la plantilla; ahora es 480.
- **Obs. vigas de borde norte de Retail 124** (S1.02 "(MF) W27X94", "(MF) W21X50", "W24X55"): más profundas que las trusses de 18". La membrana FS-1 las envuelve (A0.08 FS-1 "WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES"), fondo + cara interior. La cara exterior es el muro exterior (2/S3.02).
  - Medido en S1.02: 32.58 + 19.37 + 16.85 = 68.80 LF [DERIVADO].
  - **+92.71 SF Type C** y **+137.60 LF RC** [DERIVADO]; d / bf de AISC.
  - Review Item con su delta: si la banda GYP-1 11'-0" del tenant las encierra y no hace falta el wrap.

## Delta Material Summary (NET) rev11 → rev12
| Material | Unit | rev11 | rev12 | Delta |
|---|---|---|---|---|
| Resilient channel - printed product (see Where it comes from) | LF | 19,341.62 | 19,479.22 | +137.60 |
| 5/8" gypsum board, Type C (ceiling) | SF | 21,507.35 | 21,600.06 | +92.71 |
| Joint compound, all purpose | LB | 8,439.11 | 8,445.78 | +6.67 |
| Joint tape, paper | LF | 50,605.11 | 50,639.42 | +34.31 |
