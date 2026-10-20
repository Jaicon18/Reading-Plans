# CAMBIOS v77 — decisiones del usuario D1-D6 (Bluebeam) hechas reglas, compuertas R76.7 sin falsos bloqueos

Origen: arbitraje de dos pruebas ciegas con v76 y las decisiones del estimador sobre los cuatro pendientes de §22 y el
borde de transición. Cada cambio es genérico (ningún número, wall ni room de un proyecto) y tiene test sintético
(test_v77.py). Reglas R77.1-R77.9 en SKILL §24.

## Decisiones del usuario (mandan)
- R77.1 (D1) extra framing ATM = la wall completa del ATM (studs piso a deck + bottom + top runner), contada una vez
  (sale de su familia de stud / track); sin sistered ni furring aparte.
- R77.2 (D2) box beam / box header = 4 piezas × (R.O. + 1'-4"); CONT. BOX BEAM = un run por frente, primera a última
  jamb + 1'-4" × 4 (`front_line`); headers del schedule con las piezas de su rótulo impreso.
- R77.3 (D3, inviolable) lo impreso se aplica sin RFI; lo no impreso se mide por vector a la escala del detalle con
  verificación contra algo impreso, imagen marcada y [DERIVADO].
- R77.4 (D4) 3/4" FRT plywood de piers = solo strips en las jambs del storefront (ancho por vector × alto impreso);
  2 capas dibujadas con rótulo singular = 1 ply + RFI.
- R77.5 (D5) sill track doble en R.O. > 4'-0", simple ≤ 4'-0", solo aberturas con sill.
- R77.6 (D6) borde de transición sin track de perímetro del ceiling (confirma R73.16 / R76.6).

## Del arbitraje
- R77.7 `constants.carrying_direction` obligatoria con ceilings suspendidos (dos corridas: +11 % de carrying channel por
  tomar el lado largo por room).
- R77.8 compuertas que bloqueaban datos verdaderos: "F.R.T." con puntos, español falso en rutas / ids, bands de otra
  hoja en vigas_sobre_walls, bitácora con lock y realpath, inventario y alcances sobre la copia limpia.
- R77.9 millwork empotrado en partición = abertura enmarcada (header del schedule) y su tramo de partición tiene dueño.

## Sin cambio
- Criterios de partición y valores aceptados por el usuario (los revisa uno por uno; sus respuestas van en v78).
