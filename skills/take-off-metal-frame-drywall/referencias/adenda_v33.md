# ADENDA v33 — 29-sep-2026 · EL JUEGO DE PLANOS MARCADOS ES AUTOMÁTICO

## De dónde salió

Rodolfo: *"todos los planos que creaste en este proyecto, es lo que vas a hacer de aquí en adelante en cada proyecto: creas un plano por partition type, incluyendo los soffit and ceiling, y los guardas con su respectivo nombre para yo saber qué contiene cada plano. Todo esto lo vas a hacer en cada proyecto y lo vas a guardar en el folder que le corresponda, tal como lo hiciste en este proyecto. Todo eso lo harás sin que yo te lo pida, todo será automático."*

## REGLA — No se pregunta, no se ofrece, no se espera

El juego completo de planos marcados es **entregable obligatorio de todo take-off**, al mismo nivel que el Excel. Se produce solo, en cada proyecto, sin que nadie lo pida.

## Qué compone el juego, sin faltar ninguno

| hoja | cuántas |
|---|---|
| **una por cada partition type** del schedule que tenga instancias | las que haya (en BofA: A1, A1K, A5, B, B2, B2K, C1, F, G, G1, bulkhead = 11) |
| **walls exteriores** | 1 |
| **ceilings de gypsum board** | 1 |
| **soffits** (y canopy si el proyecto lo tiene) | 1 |

## El NOMBRE dice qué contiene

`NN_PLANO_<LO QUE CONTIENE>.jpg` — numerado en el orden del recorrido, con el contenido en el nombre:

```
01_PLANO_A1.jpg      05_PLANO_B2.jpg       09_PLANO_G.jpg          13_PLANO_EXTERIORES.jpg
02_PLANO_A1K.jpg     06_PLANO_B2K.jpg      10_PLANO_G1.jpg         14_PLANO_SOFFITS.jpg
03_PLANO_A5.jpg      07_PLANO_C1.jpg       11_PLANO_BULKHEAD.jpg
04_PLANO_B.jpg       08_PLANO_F.jpg        12_PLANO_CIELOS_GWB.jpg
```

> El punto es que se sepa qué trae cada hoja **sin abrirla**. `plano1.jpg` no sirve.

## Dónde se guardan

`<proyecto>\<proyecto>\2 - Take-Off Claude\Planos marcados por tipo\` — **escritos en la PC**, no solo mandados al chat. Y el `00_INDICE_DE_ARCHIVOS.md` lista cada hoja con su tipo, sus walls y sus LF, para que el nombre del archivo y el índice digan lo mismo.

## Sigue valiendo todo lo de antes

Estilo de marcado aprobado (hoja completa, un tipo por hoja, rectángulo sobre la extensión real, número oficial + LF, azul/rojo/naranja/verde, 300 dpi sin markups, auto-test de tinta de 7 sondas) · tabla de bandas **derivada de los cierres sellados**, nunca re-tecleada · `verif_bandas` antes de dibujar · `verif_planos` antes de entregar · verificación visual de cada hoja ya generada.

---
