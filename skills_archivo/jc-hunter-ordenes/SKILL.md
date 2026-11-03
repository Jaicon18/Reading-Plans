---
name: jc-hunter-ordenes
description: Órdenes permanentes de JC Hunter (jaicon18) para take-offs de metal frame y drywall y para trabajar con él. Cargar SIEMPRE antes de cualquier take-off, revisión de RFI, cambio al skill take-off-metal-frame-drywall, arranque de proyecto o manejo de sesiones/Drive. Contiene todas sus órdenes desde el día 1, el proceso de mejora continua (cada proyecto mejora al siguiente sin borrar nada) y la verificación obligatoria antes de empezar.
---

# Órdenes de JC Hunter — leer completo antes de trabajar

Este skill NO calcula nada. Es la memoria permanente del usuario. El cálculo lo hace el skill `take-off-metal-frame-drywall` con sus programas.

## 1. Antes de empezar cualquier proyecto (obligatorio, en este orden)
1. Leer `ORDENES_DEL_USUARIO.md` completo. Si dos órdenes chocan, manda la MÁS RECIENTE (fecha entre paréntesis).
2. Leer `REGLAS_ALCANCE.md` (decisiones del estimador = reglas para todos los proyectos) y `BIBLIOTECA_ERRORES.md` (cada error ya cometido y su prueba).
3. Arrancar con la **VERSIÓN VIGENTE** que marca `skills_archivo/INDICE.md` del repo jaicon18/reading-plans (rama claude/gifted-pasteur-x2sfzs). Nunca una versión vieja ni una rama aparte.
4. Correr `python3 -I verificar_version.py <carpeta_del_skill_de_arranque> <repo>/skills_archivo <repo>/cache_proyectos`. Si reporta reglas faltantes: NO arrancar; primero unirlas.
5. Verificar permisos de red del plan room y bid set limpio (sin markups) antes de lanzar.
6. **TODA ENTREGA (BE-121, INVIOLABLE):** `python3 -I tools/compuerta_entrega.py <carpeta_del_proyecto>` (antes:
   `python3 -I tools/compuerta_entrega.py texto <bidset.pdf> --out <carpeta>/set_texto.json` y `entrega.json` con
   `drive.parent_id = 1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc`, `carpeta_proyecto`, `carpeta_proyecto_id`; y `fichas.json` = lectura
   independiente del Partition Type Schedule por un subagente que no ve el Excel, BE-122). Sin
   `ENTREGA_OK.json` VERDE (0 FAIL) no se entrega. AMBER se reporta. Desde v81cf24 la compuerta corre además
   `tools/chequeos_biblioteca.py` (un chequeo CB_<regla> por cada BE de la biblioteca y las U / R-ALC que eran
   programa-pendiente) y CE_CALLOUTS (U-113: toda burbuja N/HOJA seguida hasta el final; las que no aplican van en
   `<carpeta>/callouts_no_aplican.json` {"<hoja>": {"<etiqueta>": "motivo"}}).
7. **La subida SOLO con** `python3 -I tools/subir_entrega.py <carpeta_del_proyecto>`: se niega sin ENTREGA_OK.json verde,
   si un archivo cambió después de la compuerta o si la carpeta no es hija (en vivo) de Claude outputs de la raíz.
   Nunca `gdrive_fetch.py put` a mano para una entrega. COORDINACIÓN no reporta un resultado sin ENTREGA_OK.json verde.
8. `REGLAS_REGISTRO.json` dice qué hace cumplir cada regla (programa / conducta / histórica; desde v81cf24 0 programa-pendiente).
   Regla nueva = entrada nueva en el registro con su chequeo + test (si no, `verificar_version.py` falla).

## 2. Mejora continua (cómo un proyecto mejora al siguiente)
- Toda orden nueva del usuario, toda respuesta de RFI y todo error corregido se guarda **el mismo turno** en tres lugares: `ORDENES_DEL_USUARIO.md` (o `REGLAS_ALCANCE.md` si es decisión de alcance), el skill de take-off (regla R80e.N) y `BIBLIOTECA_ERRORES.md` (BE-N con su prueba).
- Al cerrar cada proyecto: nueva versión del skill = versión vigente + lo aprendido. Se archiva en `skills_archivo/` con INDICE.md; nunca se borra nada.
- Proyectos en paralelo: al cerrar cada uno, sus reglas se UNEN a la línea principal ese mismo día. Nunca quedan dos ramas.
- Ningún arreglo entra sin probarse gratis contra el banco de proyectos ya hechos (B&N rev13, O'Reilly, VS Downey, Chuze…): no puede empeorar ningún material.
- Una regla que solo vive en texto se olvida: toda regla inviolable lleva su COMPUERTA de programa + test que repite el error original (BE-121); `verificar_version.py` falla si una regla "programa" del registro no la tiene.

## 3. Las 15 que más se han roto
Están arriba de `ORDENES_DEL_USUARIO.md` (sección "LAS 15 QUE MÁS SE HAN ROTO"); se revisan punto por punto en CADA
entrega. Las de programa las revisa `compuerta_entrega.py`; las de conducta, COORDINACIÓN antes de pasarle nada al usuario.
Reglas viejas / duplicadas: `REGLAS_HISTORICO.md` (texto literal, nada se borra).

## 4. Cómo hablarle al usuario
Español, términos del trade en inglés. Poca información a la vez, rutas exactas paso a paso, sin preguntar lo que se puede buscar en el plano. Autonomía total; solo se pregunta lo que el plano no resuelve.
