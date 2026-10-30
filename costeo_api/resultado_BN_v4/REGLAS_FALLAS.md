# REGLAS_FALLAS — reglas.py compuerta (v73)

Carpeta: `/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/runner_r4g/takeoff_work/etapas` · reglas: 825 (a 417 · b 210 · c 198) · fallas: **3** · **NO OK**

## Fallas por regla

| Regla | Fallas |
|---|---|
| S:§1:2fab33 | 2 |
| S:etapa-5-entrega | 1 |

## Detalle

| Regla | Wall / renglón | Valor | Qué esperaba |
|---|---|---|---|
| S:§1:2fab33 | bitacora | EXCEL: Partition Takeoff: renglón 'F  #F-01  -  F-01' PENDING (partition_types sin dato obligatorio: se resuelve en el canon antes de entregar) | bitacora.py compuerta sin fallas |
| S:§1:2fab33 | bitacora | NO HAY BACK-CHECK anotado (bitacora.py backcheck <informe> <excel>) | bitacora.py compuerta sin fallas |
| S:etapa-5-entrega | Excel | Partition Takeoff: renglón 'F  #F-01  -  F-01' PENDING (partition_types sin dato obligatorio: se resuelve en el canon antes de entregar) | plantilla_excel.verificar_excel sin errores |
