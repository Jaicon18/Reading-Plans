# RESUMEN rev13 — CR City Hotel (Castle Rock, CO)

rev13 reemplaza a rev12. Origen: auditoría diaria U-138 de COORDINACIÓN sobre rev12, verificada punto por punto en el plano.

## E1 — Caras exteriores con la altura del board interior (U-058)
- **Mezzanine 219** (2/A5.04, 3/8" = 27 pt/ft): el exterior sheathing (línea x = 610.68) va del piso del mezzanine (1185.48) al tope bajo el borde del techo (1006.2). La línea del board interior (x = 627.4) para en 1026.1.
  - XW.6.4-L2-01 A y XW.6.3-L2-12 A: 5.915 → **6.64 ft** [DERIVADO: (1185.48 − 1006.2) / 27]; +36.96 SF cada uno.
  - Gable este XW.6.4-L2-02 A: 7.282 → **8.0065 ft** [DERIVADO: 6.64 + 2.733 / 2]; +14.08 SF.
  - XW.6.4-L2-03 (gable oeste) solo tiene cara interior: correcto.
  - Imagen: Auditoria/…/rev13/E1_2A504_sheathing.png.
- **Barrido de todas las caras exteriores:** se encontraron además los pilares del retail en grid 7 (XW.6.4-L1-01 / 02 / 05 A, cara courtyard). Usaban 12'-0" B.O. DECK (cara interior). Ahora van de piso a piso, 14'-0" [CONFIRMADO: LEVEL 2 6211.75' − LEVEL 1 6197.75'], igual que XW.6.3-L1-03 A; +27.76 SF.
- **Compuerta nueva CB_CR_R13_E1:** cara exterior y cara interior del mismo wall con la misma H de la misma línea = FAIL, salvo una cota que valga para ambas. Lleva test.

## E2 — Citas de norma sin sección (U-155)
- RFI-15 opción B: IBC 2018 Table 2508.1 (materiales de gypsum board) + ASTM C840 Table 1 / GA-216 Table 1 (espaciado máximo de framing de cielos).
- CB_U_155 endurecida: el nombre de una norma (GA-216, ASTM C1396, ANSI A108, TCNA, NFPA) sin sección o tabla = FAIL. Lleva test.

## Alerta — detector de RFI "no impreso"
- CE_RFI_BUSQUEDA_EXHAUSTIVA ahora reconoce "no partition tag", "does not give", "not labeled", "untagged", "not specified", etc. RFI-04, 13, 15 y 17 entran a la búsqueda exhaustiva. Lleva test.

## Pista RS-5 / RS-6 (verificada en A0.08 y A2.05)
- **RS-6** (2 capas 5/8" Type X): A2.05 lo marca 2 veces y las dos están cargadas.
  - Terraza 420 / 421 sobre 301–304: "RS6-L3 board", 855.0 SF.
  - Deck cubierto al este de 411 sobre 309: "RS6-L3-309 board", 613.44 SF.
  - Ahora el nombre "RS-6" aparece en el Excel (Scope Checklist ALC-25).
- **RS-5** NO es Type C. A0.08 RS-5 = membrane roofing / tapered insulation / METAL DECK, sin gypsum. Los cuartos de abajo llevan su cielo del RCP.
- **RS-1:** cargado en los cielos de L4.
- **RS-2 y RS-3:** sin board propio en el assembly.
- **RS-4** (Deck Bar 411): "CEILING ASSEMBLY - TBD". A7.55 dice "INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT".
- **RS-7:** sin gypsum.
- **Error de método corregido:** el canon decía que los RS / FS / MB "not tagged on any plan", y era falso. Ahora cada uno lleva su disposición real.

## Nota — familias_out.json del cache
Regenerado con la cadena de rev13 y subido al repo.

## Delta Material Summary (NET) rev12 → rev13
| Material | Unit | rev12 | rev13 | Delta |
|---|---|---|---|---|
| 5/8" exterior gypsum sheathing, Type X | SF | 18,077.97 | 18,193.73 | +115.76 |
