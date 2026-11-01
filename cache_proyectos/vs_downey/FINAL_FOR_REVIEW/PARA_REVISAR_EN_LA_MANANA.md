# PARA REVISAR EN LA MAÑANA — VS #679 Downey (take-off rev1, 2026-11-01)

Bid due **11/02/2026 3:00 PM CT**. Excel: `Take-off/VS679_Downey_Takeoff_FINAL_rev1.xlsx` (6 hojas, formato fijo).

## 1. Decisiones tuyas que mueven cantidad (de mayor a menor impacto)
1. **RFI-18 / RFI-19 — studs bajo shelving (S01.01 / S03.02).** La nota impresa dice: donde hay shelving en las dos caras de un wall, el spacing de studs y de diagonales va a la MITAD; los walls del stock que soportan racks van a Table 3. Están cargados a 16" O.C. (sin reducir). Si aplica en los "Trans" spine walls y el stock: **+ ~el doble de studs en esos walls**. Es impreso: conviene cargarlo; lo dejé como RFI porque la ubicación exacta de shelving por cara sale del fixture plan A06.01 y no se cerró en esta corrida.
2. **RFI-16 — largos de walls.** El texto del plano está en curvas: casi todos los LF salen de la geometría vectorial de A02.01 (DERIVADO, 18 pt/ft), no de cotas impresas. Solo pocos walls tienen cota impresa (37'-11 3/4", 15'-1 1/2" HOLD, valances del beauty cabinet).
3. **Madera EXCLUIDA (tu orden):** el RTU support framing de S05.01 es 2x (madera) → no va. La nota del GC pide "Blocking/Support framing @ RTU" → al mandar el bid aclarar que el RTU support NO está incluido.
4. **RFI-24 — service door 12** en el wall existente del corredor de servicio: cargada como framing nuevo (lintel + jambs ≈ 62 LF). Si el wall existente queda, sale.
5. **RFI-17 / RFI-26 — storefront y display window platforms (S02.01):** spans y alturas no impresos; carga conservadora.
6. **RFI-14 — corner bead** de esquinas exteriores no enumerado completo (cargado 305 LF; la otra lectura contó ~1,335 LF).
7. **Bridging C.R. channel** 1,706.76 LF en TODOS los walls @ 48"; R/S03.01 dice que no hace falta donde hay sheathing en las dos caras → conservador (podría bajar).

## 2. Cosas corregidas por el orquestador (verifícalas en la imagen si quieres)
- A01.01 imprime **LOWEST POINT OF DECK 17'-0" / LOWEST POINT OF STRUCTURE 12'-1"** + alturas de joists: las dos lecturas no lo vieron; INS walls (tight to structure) y diagonales A/S03.01 recalculadas con esas alturas (`proceso/RESOLUCION_AB_y_CORRECCION.md`).
- Cielos de gyp: A15.04 092900 "UL LISTED FIRE RESISTANT GYPSUM BOARD THROUGHOUT" → **5/8" Type X** (las lecturas los traían en regular).
- Storefront estructural (box beams / box posts / head boxes S02.01) en su propio renglón (antes inflaba el header de doors).
- PVC trim de FRP → **metal FRP trim** (impreso E, A/A13.02).
- Cement board solo detrás del porcelain cove base B-13 de los restrooms (6", A00.03).

## 3. Revisión visual pendiente
- Planos marcados por type (`Planos marcados/A02.01_type_*.png`) y markups Bluebeam (PDF en Drive, 112 anotaciones). Los 6 valances del beauty cabinet (B/A10.03) no tienen banda en planta → no están en los markups (sí en el Excel).
- Cobertura paso 12: 317/334; los 17 "huecos" son elevaciones A07.xx / detalles de referencia cuyos renglones existen pero el script no los liga (`proceso/COBERTURA_paso12.md`). Revisar rápido.
- RFI-12 es interno (placeholder de esquema), no es pregunta al arquitecto: bórralo al mandar RFIs.
- "Access panel 36x12" (3 pcs) y la grid de drywall (USG DGLW) — las specs nombran Armstrong / Chicago Metallic: el producto equivalente es decisión comercial.

## 4. Back-check
Paso 11 (auditor independiente) NO corrido: `reglas.py` deja solo el back-check pendiente. Recomendado antes de mandar el número.
