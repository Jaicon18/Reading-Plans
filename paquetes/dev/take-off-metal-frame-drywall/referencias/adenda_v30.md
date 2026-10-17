# ADENDA v30 — 28-sep-2026 · barrido de ZONAS HÚMEDAS

## De dónde salió

Rodolfo: *"¿estás checando todas las wet areas y el tipo de gyp que lleva ahí? No veo que lo hayas hecho."*

Tenía razón. Había **[valor retirado E24] SF de W.R. board** y eran **únicamente las dos faces del chase**. El barrido completo encontró tres zonas más.

## REGLA — Censo por CUARTO, cruzando TRES fuentes

**Ninguna fuente sola alcanza.** Hay que cruzar las tres, y cada una tapa un agujero de las otras dos:

| fuente | qué da | qué NO da |
|---|---|---|
| **notas de hoja** del cuarto húmedo | qué **tipo de board** se exige | dónde están los aparatos |
| **Finish Plan** con sus key notes | qué **acabado** lleva cada cuarto | el sustrato detrás |
| **planos de plomería** | dónde hay **agua de verdad** | qué acabado le toca |

## Lo que salió

### 1. La nota F pedía DOS walls y sólo se cumplió una

`A08.01 TOILET ROOM SHEET NOTE F`, textual:

> **`USE MOISTURE RESISTANT GYPSUM BOARD BEHIND TOILET AND LAVATORY`**

Son **dos aparatos en dos walls distintas**:

- El **lavabo** va en el chase → [valor retirado E24] SF, ya estaban.
- El **inodoro** va contra la **face interior del wall exterior oeste** (probado con `D/A08.01 RESTROOM ELEVATION D`, que lo dibuja de perfil con su barra TA-nn). Esa face estaba como gyp **regular**.

**Faltaban [valor retirado E24] SF.** W.R. total: 100.80 → **[valor retirado E24] SF**.

### 2. El FRP del mop sink no estaba cuantificado

`Key note 6 del Finish Plan`, textual:

> **`FRP FROM FLOOR TO 4'-0" AFF, WIDTH TO MATCH WIDTH OF MOP SINK AT BOTH SIDES`**

Su marcador cae dentro del **JANITOR CLOSET 112** y su línea guía apunta a la face del wall oeste. `5/A08.01 PLAN SECTION @ MOP SINK` lo dibuja en **esquina**, con FRP en **las dos walls**, más `PVC EDGE TRIM MOLDING`, `PVC INSIDE CORNER TRIM MOLDING`, `TILING FLANGE` y `CLEAR SEALANT`.

**Cero cuantificado.** Alto **CONFIRMADO** (4'-0" de dimension impresa); width **PENDIENTE** — el aparato no viene acotado en A02.01, A08.01 ni en el Plumbing Fixture Schedule. No se inventa: se da la dimension superior para precio (24" → [valor retirado E24] SF; 28" → [valor retirado E24] SF).

### 3. El Break Room tiene fregadero y el plano no le pone nada

`P01.01 keyed note 1`: *"...ROUTE LOW VOLTAGE WIRING DOWN TO FLOODSTOP PANEL **BELOW BREAK SINK**"*.

El Finish Plan le rotula al 118 sólo `P-nn` / `VCT-2` / `B-nn`: ni FRP, ni tile, ni nota de W.R.

**El contraste es lo que decide que no es olvido de rotulación:** el mismo Finish Plan **sí** le pone key note 6 al mop sink, y A08.01 **sí** trae su nota F para los baños. El plano no lo pide aquí → **RFI + alterno**, no se cuantifica.

### 4. Dos cantidades sin desglose

Los dos renglones `BOARD_WR` de [valor retirado E24] SF tenían la **operación vacía**. Una cantidad sin desglose rastreable no se entrega: ahora queda escrito qué son (las dos faces del chase, [valor retirado E24] LF × [valor retirado E24] ft cada una, la wall del lavabo).

## REGLA — Una nota que nombra DOS aparatos hay que leerla como DOS walls

`behind toilet **and** lavatory` no es una zona: son dos, y **casi nunca están en el mismo wall**. Cumplir la mitad de la nota y darla por cerrada es el error.

Generalización: toda nota que enumere aparatos, elementos o condiciones se descompone en su lista y **cada ítem se ubica por separado** antes de cuantificar. La nota se cierra cuando todos sus ítems tienen ubicación, no cuando el primero la tiene.

## REGLA — El censo de zonas húmedas lleva compuerta de cobertura

Todo cuarto con aparato de plomería aparece en el censo con su resolución — cuantificado o RFI declarado. **Si alguno queda sin resolver, el cierre no se emite:**

```
BARRIDO DE ZONAS HUMEDAS INCOMPLETO: ['118'] sin resolver.
Un cuarto con agua que no esta resuelto no es un cuarto seco:
es un cuarto sin revisar. No se emitio nada.
```

Y el cierre guarda la frase de cobertura: *"los 4 cuartos con aparato de plomería del edificio están resueltos: 3 con su tipo de board cuantificado, 1 con RFI declarado"*.

## REGLA — El W.R. es RECLASIFICACIÓN, no board nuevo

La misma área **sale** del renglón de gyp regular. El total de board no cambia; lo que cambia es el **tipo** — y eso sí cambia el precio, porque cada tipo lleva su propio waste y su propio costo.

Regular: [valor retirado E24] → **[valor retirado E24] SF** · W.R.: [valor retirado E24] → **[valor retirado E24] SF**.

---
