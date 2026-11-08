# BITÁCORA rev12 — CR City Hotel

- 14:40: COORDINACIÓN pide aplicar U-155 a todos los RFI abiertos y valores assumed (orden recibida 21:45 UTC, leída después de entregar rev11).
- Revisé los 11 RFI abiertos uno por uno:
  - RFI-28 → IBC 2018 Section 707.5. Verifiqué que el 12'-0" B.O. DECK = fondo de las trusses (14'-0" − 2.5" − 18").
  - RFI-25 → impreso + IBC 2018 Section 708 / Table 721.1(2).
  - Los demás no los resuelve el código: alcance o conflicto entre planos.
- "Assumed": ELEC 321 verificado a ojo en el code plan de A0.02 (línea 1HR FP alrededor de ELEC / LINEN / CLEANING); demising con la nota de A0.00.
- Cadena rev12 OK. Delta 0.
- 15:00: COORDINACIÓN, revisión dirigida de rev11 (E1–E4 + Obs). Aplicado en rev12:
  - E1: DA-1 / DA-2 / RI por filas actuales. Verifiqué en A8.00 que la puerta 120.1 es 5'-0" × 8'-0" (el RI decía 7'-11"). Compuerta CB_CR_R12_E1 + test.
  - E2: build.sh regenera el delta antes de la proposal.
  - E3: C1177.
  - E4: límite de 240 → 480 + cita completa.
  - Obs: vigas de borde medidas en S1.02 (imagen MISC_BW-L1-RETAIL_N_S102.png / _A301.png), +92.71 SF Type C.
  - RFI-28: cita corregida (fondo de trusses 11'-11 1/2").
