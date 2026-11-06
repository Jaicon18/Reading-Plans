# RESOLUCIÓN de los hallazgos de la auditoría U-138 #2 — CR City Hotel rev2

Cada hallazgo se verificó otra vez en el plano antes de aplicarlo (vectores a 9 pt/ft, cotas impresas con N/HOJA). La corrección es por programa dentro de la cadena, así que se repite en cada corrida. Las imágenes están en `etapas/4_canon/img/` y en `Auditoria/evidencia_walls/`.

| # | Sev. | Verificación propia | Corrección (programa) | Resultado |
|---|---|---|---|---|
| F1 + F2 | ALTA | **Confirmado.** 6/A7.02 (Type 1) y 8 / 9/A7.03 (Type 2) muestran TILE-1 solo dentro del shower. Usé el detector de shower pan del auditor (2 diagonales) y medí a mano en vectores los 4 de otro formato: 211 / 311 (x 585.4–612.4, y 1109–1136.6), 308 (= 208 de L2) y 402 (x 967.1–994.6, y 924.2–951.2). | `scripts/banos_cbu.py` borra todo el cement board de L2–L4 y lo vuelve a crear por shower, solo en los lados sólidos: línea de muro ≥ 1.0 pt colineal en ≥ 70 % del lado. Son 33 showers y todos los lados quedaron asignados a un wall. | Cement board L2 3,325.6 → 1,582.6 SF, L3 1,086.5 → 1,480.3, L4 1,240.5 → 530.4 (Material Summary −1,715.04 SF) |
| F3 | ALTA | **Confirmado.** 7/A9.03 y 8/A9.03 imprimen "2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT 54'-0"", y 10/A9.03 muestra HEAD OF SHAFT. En 1/A2.03 y 1/A2.04 las cajas están dibujadas en las mismas coordenadas que en L2. | `scripts/shafts_l3l4.py`: CH.6-2 en L3 (sur y norte, 11'-0" = LEVEL 3 6222.75' → LEVEL 4 6233.75') y en L4 norte (8'-11 1/4", 1/A5.06), con C-H stud @ 24" y J-runner. Salen con motivo NULL-L3-11..15 y FW.4-L4-04. RFI-09 se cierra. | Shaftliner +374.19 SF, C-H +351.31 LF, J-runner +72.40 LF |
| F4 | MEDIA | **Confirmado.** 4/A5.05 junto al muro exterior: zona de piso de 1'-1 1/4" en L2-L3 y en L3-L4 (8'-11" + 11 3/4"). | Caras interiores XW de L3: 9'-2 7/8" → 11'-0" − 1'-1 1/4" = 9'-10 3/4" | Igual que L2 |
| F5 | MEDIA | **Confirmado.** 4/A5.06 imprime 11'-0" de L2 a L3, y el sheathing pasa por delante del rim (L1 = 14'-0" y L3 = 11'-0" floor to floor). L4 se queda en 8'-11 1/4", impreso en 1/A5.06. | Sheathing de L2: 9'-10 3/4" → 11'-0" | Ver la fila de sheathing en el delta |
| F6 | MEDIA | **Confirmado** con el texto de RFI-11: "non-rated: cement board in place of board". | En `banos_cbu.py`, para los types '-0', la cara del cuarto del shower lleva la franja altura − 9'-0" sobre el tramo del cement board. Aplicado en 44 lados; los types rated conservan el W.R. completo. | W.R. −1,554.40 SF en total (junto con F7) |
| F7 + F8 | BAJA | **Confirmado** en vectores: caras del demising de 1001.2 a 1206.0 = 22.76 ft; baños 205/206/207 de 1128.0 a 1206.0 y 208 de 1101.7 a 1206.0; 213 / 313 en toda la cara sur. | `finalizar_canon.py` `_rehacer`: DW.4-L2-07..10, DW.4-L3-09..11 y DW.4-L2-01 / L3-05 por cara y por tramo: W.R. en el baño, Type X en el dormitorio. | — |
| F9 | BAJA | **Confirmado.** XW.6.2-0 es no rated; RFI-05 aplica. | Cara retail excluida (RFI-05); la cara exterior pasa a exterior gyp sheathing Type X. | — |
| F10 | BAJA | **Confirmado**, S1.02: trusses de 18" y vigas W16–W30. | RFI-20 queda abierto con el rango 0"–12" en el texto; lo cargado (1'-0") es el máximo. | 0 |
| F11 | BAJA | S1.02 / 3/S3.10 "PRE-FABRICATED ROOF CANOPY BY OTHERS". No está acotado que sea el mismo canopy de 08/A9.05. | RFI-21 lleva la alternativa (−58.2 SF, −21.7 LF). Se mantiene tu decisión del 6-nov (el soffit es nuestro). | 0 |
| F12 | BAJA | **Confirmado**: la cara del CMU está en 751.08. | FW.2-L4-11: 6.56 → 4.99 LF. Se mantiene la política de no descontar vanos (W.62-L4-11). | −14 SF |
| F13 | BAJA | **Confirmado.** | Las fuentes de los CH citan "7/A9.03 W419, U497" además de UL U415. | 0 |

## Error de cadena encontrado al aplicar la auditoría (BE-CR26)

`vanos_puertas.py` y `esquinas_cb.py` leían y escribían el canon **final de la corrida anterior**, mientras que `finalizar_canon.py` arranca de la base que deja `build_canon`. Por eso los arreglos de vanos de la auditoría #1 (W.4-L3-44, W.4-L4-22, W.4-L4-21 → A7.50, el recorte de W.62-L4-04) **nunca llegaron al canon final, tampoco en rev1**. El corner bead, además, se contaba sobre un canon viejo.

**Arreglo:**
- Los dos pasos trabajan ahora sobre `takeoff_canon.json.base.json`.
- `finalizar_canon.py` lleva un candado: si un wall eliminado por `vanos_puertas` sigue en la base, la cadena falla.

Ahora sí:
- W.4-L3-44 y W.4-L4-22 están fuera.
- W.4-L4-21 está en A7.50 con 1.06 LF.
- W.62-L4-04 lleva el recorte de −4.49 LF.
- El corner bead queda en 3,871.99 LF.
