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

## 2. Mejora continua (cómo un proyecto mejora al siguiente)
- Toda orden nueva del usuario, toda respuesta de RFI y todo error corregido se guarda **el mismo turno** en tres lugares: `ORDENES_DEL_USUARIO.md` (o `REGLAS_ALCANCE.md` si es decisión de alcance), el skill de take-off (regla R80e.N) y `BIBLIOTECA_ERRORES.md` (BE-N con su prueba).
- Al cerrar cada proyecto: nueva versión del skill = versión vigente + lo aprendido. Se archiva en `skills_archivo/` con INDICE.md; nunca se borra nada.
- Proyectos en paralelo: al cerrar cada uno, sus reglas se UNEN a la línea principal ese mismo día. Nunca quedan dos ramas.
- Ningún arreglo entra sin probarse gratis contra el banco de proyectos ya hechos (B&N rev13, O'Reilly, VS Downey, Chuze…): no puede empeorar ningún material.
- Una regla que solo vive en texto se olvida: toda regla importante debe tener su COMPUERTA en un programa (reglas.py / verificar_version.py).

## 3. Las 12 que más se han olvidado (revisar al terminar cada entrega)
1. Hoja de datos del proyecto arriba de todo + lista de hojas obligatorias revisadas (R-ALC-09).
2. Spec sheets / project manual del trade cruzados contra cada material, con sección citada (R-ALC-08).
3. Demo: markup de línea a escala, alturas buscadas en todas las hojas, cruce demo vs floor plan (R-ALC-06).
4. Dos tipos de track en renglones separados (estándar y slip/deflexión).
5. Lo IMPRESO se carga; RFI solo para lo no impreso; nunca inventar "decisión del estimador".
6. Tornillería, ductos y trades que no hacemos = EXCLUDED sin RFI.
7. RFI: A planos · B código · C otro; con botones, en bloque de 4, con total y cuántos quedan.
8. Nunca abrir ni leer los take-offs humanos de referencia.
9. Una sesión por proyecto (título = carpeta de Drive); todo lo demás con subagentes; barra lateral limpia.
10. Excel con formato fijo (plantilla_excel.py), sin agregar hojas ni columnas.
11. Drive: versión nueva, nunca sobrescribir ni borrar; dar la ruta carpeta por carpeta.
12. Horas en hora de California; sin costos en dólares; mensajes cortos y claros (el usuario tiene autismo nivel 1 y TDAH).

## 4. Cómo hablarle al usuario
Español, términos del trade en inglés. Poca información a la vez, rutas exactas paso a paso, sin preguntar lo que se puede buscar en el plano. Autonomía total; solo se pregunta lo que el plano no resuelve.
