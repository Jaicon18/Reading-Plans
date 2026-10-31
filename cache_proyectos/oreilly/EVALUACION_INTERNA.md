# EVALUACIÓN INTERNA DE EXACTITUD — O'Reilly Evans #1 (prueba ciega)

Control interno solamente: lectura A vs B, compuertas, paso 11, paso 12 e indicadores contra el **mejor skill (v80s / B&N rev13)**. No se abrió ningún take-off, Excel ni plano marcado de O'Reilly (el bid set traía 79 markups: se limpiaron antes de leer; solo se vieron sus títulos en las hojas 37/38).

## 1. Lectura A vs lectura B (independientes)
| Type | A LF | B LF | Δ % | Decisión |
|---|---|---|---|---|
| S21 | 250.71 | 250.06 | +0.3 | coinciden |
| S24 | 35.67 | 34.47 | +3.5 | A (esquinas con un dueño, R70.2; 7'-10" + 7'-10" impreso) |
| S41 | 6.46 | 6.22 | +3.9 | A (Δ 0.24 LF, review) |
| S42 | 122.61 | 115.91 | +5.8 | A (header wall dibujado hasta el break mark; RFI-03 −6.70 LF) |
| S43 | 53.58 | 51.16 | +4.7 | A (esquinas con un dueño) |
| S61 | 8.50 | 8.64 | −1.6 | A |
| Exterior CFMF + vestibule heads | 157.91 | 158.17 | −0.2 | iguales (elemento / gauge de B, RFI-05/14) |
| **Total** | **635.44** | **624.13** | **+1.8** | |
- Alturas: A a top of purlin, B a bottom of purlin medido (≈ 10" menos). Bottom of purlin no impreso → A (53.3) + RFI-01/02 con la cifra de B.
- Atributos: board W.R. en restrooms (A, nota 3.B) · glass mat solo en piers y FRT plywood en el head (B, 2/A3.1 key 34) · nailers 8/A3.2 (solo B, agregado).
- 13 decisiones documentadas en `takeoff_work/etapas/3_revision/resolucion.md`.

## 2. Compuertas
- `reglas.py compuerta`: 837 reglas, **0 fallas** (modo final con Excel). `bitacora.py compuerta`: **OK** (17 tools obligatorias vigentes + back-check). `registro.py entregable`: OK. `alcances.py compuerta`: OK (24 / 24 alcances cerrados). Suite del skill 5/5 OK. Markups: 33 / 33 walls con geometría.

## 3. Paso 11 (auditor independiente) y paso 12 (cobertura)
- **Paso 11, primera pasada: NO certificado** (4 FAIL: alcance, aritmética, Bluebeam; 3 PASS WITH COMMENTS). Diferencias resueltas en el plano y aplicadas: anchors 206 → 36, slab pins 226.82 → 151.04, FRT 2x4 en aberturas CMU +56.67 LF, board bajo header S42 +30.76 SF, studs dobles en control joints +62.96 LF, bands de Bluebeam corregidas, RFI-04 cerrado. Mantenidos con motivo: board sin descontar aberturas (precedente B&N rev13), Z-furring con jambs/nodes (regla de la tool), jamb return.
- **Paso 12, primera pasada: 85.5 % de cobertura (124 / 145), 13 huecos**, biblioteca 22 PASS / 19 FAIL / 8 N/A. Después de la resolución: **145 / 145 con destino** (renglón, EXCLUDED o RFI-18…27). No se repitió la pasada completa del paso 12 (R80e.30: revisión dirigida de lo cambiado); la biblioteca no se volvió a correr.

## 4. Indicadores contra el mejor skill (B&N rev13)
| Indicador | B&N rev13 | O'Reilly | Δ % |
|---|---|---|---|
| Partition LF (grand total) | 569.816 | 614.857 | +7.9 % |
| Wall area LF x H (SF) | 12,908.900 | 7,763.700 | -39.9 % |
| Partition board SF | 13,679.800 | 8,037.250 | -41.2 % |
| Board SF per LF of wall | 24.007 | 13.072 | -45.6 % |
| Stud + furring LF per SF of wall area | 1.146 | 0.843 | -26.4 % |
| Bottom + top track LF per LF of wall | 2.248 | 1.251 | -44.3 % |
| Total gypsum board SF (Material Summary) | 15,609.540 | 8,461.820 | -45.8 % |
| Drywall screws per SF of board | 1.181 | 1.197 | +1.4 % |
| Joint compound lb per SF of board | 0.071 | 0.072 | +1.4 % |
| Joint tape LF per SF of board | 0.364 | 0.369 | +1.4 % |
| Bracing LF per LF of wall | 5.061 | 1.366 | -73.0 % |
| Average wall height (ft) | 22.655 | 12.627 | -44.3 % |

Lectura de los porcentajes (por qué difieren y si es razonable):
- **Altura media −44 %** (B&N 25' a deck; O'Reilly ≈ 12.6': partitions de 8'-6" y furring a eave). Explica casi todo lo demás.
- **Board por SF de muro:** B&N 1.060 vs O'Reilly 1.035 → **−2.3 %** (casi igual: S21 y S24 son de una sola cara).
- **Studs por SF de muro, normalizado por O.C. (16" vs 24"):** B&N 0.764 vs O'Reilly 0.843 → **+10 %** (jambs, nodos, kickers y CJ dobles pesan más en walls bajos).
- **Track por LF sin el Z-furring (que no lleva track):** B&N 2.248 vs O'Reilly 2.113 → **−6.0 %**.
- **Screws, compound y tape por SF de board: +1.4 %** (mismas yields de Inputs).
- **Bracing −73 %:** walls de ≤ 16' llevan 1–3 filas (ROUNDUP(H×12/48) − 1) contra 6 en B&N.

## 5. Uso de API (incidencia)
El runner tomó `TAKEOFF_API_KEY` del entorno y lanzó **31 llamadas** a la API (corrección y cobertura) entre 07:40 y 08:28, contra la instrucción de correr por suscripción. Ninguna cambió cantidades: el Material Summary con y sin esas llamadas es idéntico, y la entrega final se rehízo con `--sin-api` y sin la variable (0 llamadas nuevas). Regla nueva R80e.69 (`--sin-api`); registro en `takeoff_work/costos_api_llamadas.csv`.
