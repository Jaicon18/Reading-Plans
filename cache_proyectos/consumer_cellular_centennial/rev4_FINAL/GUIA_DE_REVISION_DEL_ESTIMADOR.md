# GUÍA DE REVISIÓN DEL ESTIMADOR — Consumer Cellular, Centennial CO · rev4 FINAL

**Para qué sirve:** revisar el take-off en el orden correcto y saber qué hay en cada archivo, sin abrir cosas de más. Cada paso dice qué abrir, qué buscar y qué decisión te toca a ti.

**Dónde está la entrega:** Shared drives › JC HUNTER PROJECTS › Claude outputs › Consumer Cellular - Centennial, CO (Elite Retail / Elder-Jones) 11-05-26 › **rev4 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR**

**Bids:** Elite Retail 5-nov · Elder-Jones 6-nov. Los dos sets son idénticos hoja por hoja (37 hojas); se usó el de Elder-Jones.

**Regla de la revisión:** mientras revisas, nadie toca este proyecto. Lo que encuentres me lo dices con el **Wall #** o el **# de burbuja**, y sale una versión nueva sin sobrescribir nada.

---

## ORDEN RECOMENDADO (de lo que más cuesta a lo que menos)

| Paso | Qué revisas | Archivo | Tiempo aprox. |
|---|---|---|---|
| 1 | Que estén marcados todos los walls del floor plan | `Planos marcados/Consumer_Cellular_Centennial_markups_rev4.pdf` (hoja A100) + PNG por type | 10–15 min |
| 2 | Que se hayan leído todos los detalles que llama ese floor plan | `Planos marcados/DETALLES_REVISADOS.pdf` + `DETALLES_REVISADOS_INDEX.md` | 10–15 min |
| 3 | Que cada partition type tenga sus materiales | `Planos marcados/SCHEDULES_REVISADOS.pdf` + `SCHEDULES_MATERIALES.md` | 5–10 min |
| 4 | Cantidades y de dónde salen | Excel `Take-off/…_rev4.xlsx` (Partition Takeoff y Material Summary) | 10–15 min |
| 5 | Alcance: qué se cargó y qué se excluyó | Excel, hoja Scope Checklist | 5 min |
| 6 | Lo que te toca decidir a ti | `PARA_REVISAR_EN_LA_MANANA.md` + Excel, hoja Review Items | 5 min |

---

## PASO 1 — Markups del floor plan (que no falte ningún wall)

**Abre:** `Planos marcados/Consumer_Cellular_Centennial_markups_rev4.pdf` en **Bluebeam**.

**Qué contiene:**
- **Hoja A100 (floor plan):** los **19 walls** marcados con una polilínea de color por type. Cada markup trae en Bluebeam:
  - **Subject** = el partition type (A3, C3, D, E3).
  - **Page Label** = la hoja (A100).
  - **Length** = el largo que mide Bluebeam a la escala impresa (1/4" = 1'-0").
  - **Depth** = la altura del wall.
  - **Wall Area** = LF × altura.
  - **Contents** (el texto): TYPE · LF · H · board SF · DETAIL · Wall ID, el mismo Wall ID del Excel.
- **Hoja D100 (demolition):** las líneas de demolición, **solo en SF** (los materiales demolidos no se desglosan).
- **Hoja A200 (RCP):** el polígono del cielo de gypsum del restroom (C-1).

**Totales que debes ver en A100:**

| Type | Walls | LF | Detalle |
|---|---|---|---|
| A3 | 4 | 99.86 | A3/A500 |
| C3 | 1 | 35.54 | C3/A500 |
| D | 1 | 7.67 | D/A500 |
| E3 | 13 | 57.45 | E3/A500 |
| **Total** | **19** | **200.52** | |

**Las imágenes PNG de la misma carpeta (para revisar rápido sin Bluebeam):**
- `A100_marked_by_type_rev4.png`: los 19 walls juntos, un color por type, con leyenda.
- `A100_type_A3.png`, `A100_type_C3.png`, `A100_type_D.png`, `A100_type_E3.png`: un type por imagen, para revisar type por type que no falte ninguno.
- `D100_marked_by_type_rev4.png` y `D100_DEMO.png`: la demolición.
- `A200_rcp_markups.png`: el cielo del restroom.

**Cómo revisarlo rápido:**
1. Abre `A100_marked_by_type_rev4.png` y busca en el plano un wall nuevo **sin color**. Si existe, es un wall que falta.
2. En Bluebeam, abre la **Markups List** y ordénala por Subject. Debes ver 4 A3, 1 C3, 1 D y 13 E3.
3. Compara la columna **Length** contra las cotas impresas del plano. Las diferencias menores a ~0.5 LF son por el espesor del wall o por qué wall se queda la esquina.
4. Revisa **Depth** (altura): los studs van al cielo más alto que toca el wall + 6" (A200: BOH, Hallway y Sales 11'-11"; Office y Utility 9'-0"; Restroom 8'-0"). En BOH los walls que llegan al deck van a 17'-1 9/16" (tu decisión RFI-01).

**Decisión que te toca:** si un wall no debería ir, o si falta uno, dime su ubicación.

---

## PASO 2 — Detalles que llama ese floor plan (que se hayan leído todos)

**Abre:** `Planos marcados/DETALLES_REVISADOS.pdf` (16 páginas).

**Qué contiene:**
- Cada burbuja (detail, building section, wall section, elevación) **circulada en rojo y numerada (#1, #2…)** en la hoja donde aparece **y también** en la vista a la que manda.
- Si dentro de ese detalle hay otra burbuja que manda a otro, también está circulada, hasta el final de la cadena.
- **Total: 49 burbujas.**
  - **Por hoja de origen:** A100 2 · A101 4 · A102 13 · A103 1 · A402 3 · A500 14 · A501 3 · A600 8 · A700 1.
  - **Hojas destino:** A300, A301, A400, A401, A402, A500, A501, A502, A504, A600 y G002.
- C1/G002 no existe impreso (G002 solo tiene los detalles 1–8). Está marcado en la vista más cercana con la nota "NOT PRINTED".

**Y abre al lado:** `DETALLES_REVISADOS_INDEX.md` (en la carpeta rev4 FINAL). Es una tabla con una fila por burbuja:
- **#**: el número rojo del PDF.
- **Bubble**: la burbuja, por ejemplo 3/A600.
- **Calling sheet**: la hoja donde está la burbuja.
- **Destination view**: la vista a la que manda.
- **Take-off row / out of scope**: en qué renglón del take-off se aplicó, o por qué no es de nuestro alcance (por ejemplo "floor transition, not drywall").

**Cómo revisarlo rápido:**
1. En la hoja A100 del PDF, cuenta las burbujas impresas y compáralas con los números rojos. Tienen que ser las mismas.
2. Para cada número, busca su fila en el INDEX: dice qué se cargó con ese detalle.
3. Las que dicen "out of scope" traen el motivo. Si no estás de acuerdo con uno, dime el #.

**Detalles que gobiernan cantidades (los más importantes):**
- **1/A500 (wall types):** board "ON EACH SIDE TO 6" ABOVE CEILING" → por eso los walls llevan board en las dos caras.
- **2/A500 y 3/A500:** "20 GA. MIN. TRACK" → todo el track va en 20 ga.
- **4/A500:** long-leg runner (slip track) en los walls que llegan a estructura.
- **2/A501:** grid del cielo de gypsum del restroom.
- **2/A600 y 3/A600:** head y jamb de las puertas (double studs en jambs).
- **1/A104, 2/A104 y 3/A104:** 20 ga metal strapping (blocking). **4/A104:** backing plate "BY G.C." → EXCLUDED.
- **5/A402:** 20 ga track de blocking en el restroom.
- **1/A504:** shelf del mop sink, 6" 16 ga.

---

## PASO 3 — Schedules y materiales por partition type

**Abre:** `Planos marcados/SCHEDULES_REVISADOS.pdf`.

**Qué contiene:** las **11 hojas de schedules** del trade, con cada renglón marcado: círculo rojo + palomita + número. Son **73 renglones**: partition types, door schedule, finish schedule, RCP / ceiling, etc.

**Y abre:** `SCHEDULES_MATERIALES.md`. Es una tabla con una fila por material de cada type:
- **Schedule / Type / Sheet:** de dónde sale.
- **Material / Value:** stud (size, gauge, spacing), track, board (tipo, espesor, capas por cara), altura, rating y accesorios.
- **Material Summary row / out of scope:** el renglón del Excel donde está cargado, o por qué no aplica.
- **Total: 145 materiales**, y todos tienen su renglón o su motivo.

**Cómo revisarlo rápido:** busca tu type en el PDF (ej. A3). Su número te lleva a las filas de SCHEDULES_MATERIALES y ahí ves si cada material quedó cargado.

---

## PASO 4 — El Excel (cantidades)

**Abre:** `Take-off/Consumer_Cellular_Centennial_Takeoff_FINAL_rev4.xlsx`. Tiene 6 hojas fijas:

1. **Inputs:** la hoja de datos del proyecto (dirección, GC, bid set, SF, códigos…) y los parámetros (waste %, largo de pieza). Si cambias el waste aquí, todo el Excel se recalcula.
2. **Partition Takeoff:** una fila por wall, en el orden del schedule (A3, C3, D, E3), con SUBTOTAL por type y GRAND TOTAL.
   - Columnas: Partition / Scope · **Wall #** (el mismo del markup) · Length (LF) · Height (FT) · Layers · Stud Size · Stud O.C. · Board (SF) · Location · **Source (DETAIL/SHEET)** · **Status**.
   - **Status:** [CONFIRMED] = cota impresa; [DERIVED] = calculado con su operación; [PENDING] = no impreso.
3. **Material Summary:** cada material con **Net · Waste % · Waste · Purchase · Selling unit · Pieces to buy**.
   - **Where it comes from:** de qué walls y detalles sale (N/HOJA + desglose).
   - **Yield check:** fórmula viva para comprobar la cantidad.
4. **Pending Items:** RFI abiertos → **0** (todos cerrados).
5. **Review Items:** las 6 cosas que conviene que mires tú, en orden (floor plan primero, luego detalles), cada una con su imagen en `Auditoria/review_items/`.
6. **Scope Checklist:** cada alcance como LOADED, EXCLUDED o NOT APPLICABLE, con nota y hoja.

**Qué cambió de rev3 a rev4 (por la auditoría):**
- Type X 4,358.06 → 4,293.90 SF y Type X W.R. 410.16 → 474.32 SF: la kitchenette lleva W.R. (A100 nota 5).
- Edge blocking 176.4 → 0 LF: el board llega a 6" sobre el cielo y ninguna hoja lo imprime.
- Blocking como está impreso: 145.33 LF de 20 ga metal strapping, 8.0 LF de 20 ga track y 42.0 LF de stud blocking.
- PVC trim del FRP 118.16 → 138.16 LF: se agregaron el outside corner y los division bars.
- Todo el track en 20 ga.

---

## PASO 5 — Alcance (Scope Checklist)

**Cargado aunque podría discutirse (lo que más mueve el precio):**
- **FRP B-3:** 148.33 SF + PVC trim 138.16 LF. G001 dice "FRP IN RESTROOMS AND MOP SINK AREA – GC"; se cargó por el precedente de O'Reilly / B&N.
- **Control joints:** 49.66 LF (ASTM C840, precedente R80e.34 #8).
- **Board en las dos caras de A3:** 1/A500 dice "ON EACH SIDE". Si fuera una sola cara serían −1,205.6 SF.

**Excluido (sin cantidad):**
- Tornillería, wood, ACT, insulation, paint, MEP y trades que no hacemos.
- Demo del cielo existente (falta información).
- Backing plate "BY G.C.".

---

## PASO 6 — Lo que te toca decidir

- **RFI abiertos: 0.** RFI-01 (deck 17'-1 9/16") y RFI-04 (Level 4) los cerraste tú con la opción A. Ya son regla para todos los proyectos (U-146 / U-147).
- **Revisa el Review Items** del Excel: son 6 puntos con su imagen circulada.
- **Notas en español:** `PARA_REVISAR_EN_LA_MANANA.md` (resumen) y `SEGUIMIENTO.md` (historial de RFI y supuestos).

---

## Carpeta `Auditoria/` (solo si quieres comprobar algo a fondo)

| Archivo / carpeta | Qué contiene |
|---|---|
| `burbujas/` | La verificación de cada burbuja: lista, coordenadas y la imagen de cada una. |
| `barrido_tags/` | Cada tag de wall encontrado en el plano, con su recorte circulado. Así se comprueba que ningún wall quedó sin contar. |
| `schedules/` | La lectura independiente del schedule: la hizo un revisor que no vio el Excel. |
| `backcheck/` | El back-check independiente (re-cuantificación a ciegas) y los renglones que corrigió. |
| `review_items/` y `rfi_img/` | Las imágenes de los Review Items y de los RFI. |
| `VERIFICACION_MARKUPS.md` | Cada markup comparado contra el Excel y la escala impresa: 26 de 26 OK. |
| `DEMO_CRUCE.md` | El demo plan D100 comparado contra el floor plan nuevo A100, wall por wall. |
| `comparacion_sets_Elite_vs_ElderJones.json` | La comparación de los sets de los 2 GC (idénticos). |
| `TOOL_LIMITS_CALC.md`, `PROCESO_CORRIDA.md`, `resolucion.md`, `revision.md` | Cómo se hizo la corrida y cómo se resolvió cada diferencia entre las lecturas A y B. |

**Compuerta de entrega:** 168 en verde, 2 en ámbar y 0 fallas.
- **Ámbar 1:** la hoja de la leyenda del PDF no tiene texto para comparar alturas.
- **Ámbar 2:** algunos materiales no los imprime el schedule.
