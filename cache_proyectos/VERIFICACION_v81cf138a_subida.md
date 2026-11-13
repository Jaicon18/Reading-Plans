# VERIFICACIÓN v81cf138a (subir_entrega.py, U-201 (6)): revisión adversarial independiente

**VEREDICTO: NO PUBLICAR.** La causa no es la ruta normal. Hay cuatro entradas con las que `candados` deja pasar una subida que v138 niega y que la regla no permite. Los arreglos son chicos (ver "Arreglos mínimos").

- Alcance: `apartados/v81cf138a_wip/v81cf138a_desde_v81cf138.patch`. Candidato en `/tmp/v1381/...`, publicado en `/tmp/v138fb/...`.
- Scripts (python3 -I, workdirs sintéticos en /tmp/v1381rev, Drive falso, sin tocar Drive ni entregas):
  - `/tmp/v1381rev/casos.py <tools>`: `SE.candados` con 21 entradas.
  - `/tmp/v1381rev/vigente.py <tools>`: `verificar_vigente(w=)` y la subida de punta a punta por subprocess con GDRIVE_FETCH falso.
  - `/tmp/v1381rev/candados_otros.py <tools>`: los otros candados y una corrida real de `--solo`.
- Lo que está bien: el caso válido de control pasa en v1381 (en v138 se niega). Con eso se confirma que v1381 permite lo que la regla quiere.

## Hallazgos (entrada, resultado en v138 y en v1381)

### H1. Un estado no verde que no sea exactamente "FAIL" no cuenta como FAIL (MEDIO)
- `fails = [... if c.get("estado") == "FAIL"]`. Un segundo chequeo con estado `"fail"` o `"ERROR"` (o cualquier valor que no sea `"FAIL"`) queda fuera de la regla "único FAIL".
- Entrada: `ok:false`, chequeos `[CE_X PASS, CE_PROTOCOLO_3H FAIL, CE_Y "fail"]` (o `CE_Y "ERROR"`) y una excepción válida para CE_PROTOCOLO_3H.
- v138: BLOQUEA ("NO está en verde").
- v1381: `candados` PASA. `verificar_vigente(w=)` también PASA con el set completo de chequeos más CE_Y "fail", porque fuerza ok=True.
- La compuerta solo escribe PASS, AMBER y FAIL, así que esto pide editar ENTREGA_OK a mano. Pero la excepción misma se agrega a mano a ENTREGA_OK, y la regla dice "el ÚNICO FAIL". Arreglo: cualquier estado distinto de PASS y AMBER cuenta como FAIL, con `str(estado).strip().upper()`.

### H2. README_REVIEW se verifica por subcadena y puede pasar sin que la excepción esté escrita (MEDIO)
- El código pide `str(check) in txt and str(texto).strip()[:60] in txt`, sin borde de palabra, sin largo mínimo de texto y sin que ambas cosas estén en la misma línea o sección.
- Entrada A: `texto:"P"` y un README que solo dice `see CE_PROTOCOLO_3H_OLD notes`.
  - v138: BLOQUEA. v1381: PASA.
- Entrada B: un README con `CE_PROTOCOLO_3HX` (el id solo dentro de otra palabra) más el texto en otra línea.
  - v138: BLOQUEA. v1381: PASA.
- Entrada C: `texto:true` (bool) y un README con `CE_PROTOCOLO_3H True`.
  - v138: BLOQUEA. v1381: PASA.
- Arreglo: `texto` debe ser str con un largo mínimo (por ejemplo >= 20 tras strip), y `check` debe ser str. Exigir una línea del README que contenga el id con borde de palabra y el texto completo, o una sección "Process exception".

### H3. Corrida parcial o incompleta con un solo FAIL (MEDIO-BAJO)
- `excepcion_usuario_fallas` no comprueba que hayan corrido todos los chequeos. El rechazo "corrida parcial" solo se dispara con 0 FAIL.
- Entrada: `chequeos:[CE_PROTOCOLO_3H FAIL]` (nada más), una excepción válida y ENTREGA_OK sin `vigentes`.
  - v138: `candados` BLOQUEA. La subida de punta a punta da rc=1.
  - v1381: `candados` PASA. La subida de punta a punta da rc=0 ("CANDADOS OK — 2 archivos subidos"), con SUBIDA_OK escrito.
- Mitigación real:
  - La compuerta `--solo` escribe ENTREGA_RAPIDA.json, no ENTREGA_OK.json.
  - Con `vigentes` presente, `verificar_vigente` BLOQUEA ("faltan 240 chequeos"). Esto está verificado con `listar` falso.
  - Por eso hace falta un ENTREGA_OK hecho o renombrado a mano y sin `vigentes`.
- El propio mensaje del código ("la excepción solo cubre un FAIL nombrado") deja ver que la intención es negar las corridas parciales. Arreglo: exigir que estén corridos todos los `CE.CHEQUEOS` (o `'tipo'` ausente y `vigentes` presente) en la ruta de la excepción.

### H4. ok:true con un FAIL sube por la excepción pero SUBIDA_OK no la registra (BAJO, auditoría)
- Entrada: `ok:true`, `[CE_X PASS, CE_PROTOCOLO_3H FAIL]` y una excepción válida.
  - v138: BLOQUEA.
  - v1381: PASA de punta a punta (rc=0), pero queda `SUBIDA_OK.excepcion_usuario = None` porque la condición es `if not ok.get("ok")`.
- Que pase está permitido (no es verde y cumple la regla), pero la subida queda sin el registro de la excepción. Arreglo: registrar la excepción cuando `not ok.get("ok") or malos`.

### H5. Validaciones laxas (BAJO, a decidir)
- `autorizado_por:" Usuario "`: v1381 PASA porque normaliza con strip() y lower(). La regla dice `"usuario"`. Se puede aceptar o exigir que sea exacto.
- `fecha:"x"`: v1381 PASA, porque la fecha no se valida.
- `check:7` con id `7` (no str): v1381 PASA. En v138 da TypeError en el mensaje, o sea que también niega.
- `evidencia:null` explícita se trata como si no hubiera evidencia y PASA. Es coherente con "evidencia opcional".

## Lo que se niega bien en v1381 (igual que v138)
- check vacío o de puros espacios: falta check.
- Dos FAIL con el mismo id: "solo se sube si el ÚNICO FAIL".
- Sin chequeos: corrida parcial.
- autorizado_por como lista o bool: no autorizada.
- texto de puros espacios: falta texto.
- evidencia como str contra lista, o `[]` contra FAIL sin evidencia: la evidencia no coincide.
- Sin excepción: igual que v138.

## Los demás candados siguen aplicando en la ruta de la excepción (verificado de punta a punta en v1381)
- Archivo nuevo en la entrega: BLOQUEA ("la entrega cambió después de la compuerta").
- README cambiado después de la compuerta: BLOQUEA (sha256 distinto).
- `drive.parent_id` malo: BLOQUEA.
- Carpeta del proyecto que no es hija viva de la raíz: BLOQUEA.
- Órdenes remotas: `candado_ordenes()` se llama sin condición después de `candados()` (línea 374). En las pruebas se salta por GDRIVE_FETCH, igual que en v138.
- `--vigente`:
  - Con la excepción válida, la comparación de md5 se hace como si fuera verde. Sin excepción falla igual que en v138.
  - La comprobación de chequeos faltantes se mantiene.
  - Hereda H1 (un "fail" en minúscula pasa).
  - El ok forzado a True también habilita `entrega_ok_anterior_valida`, que es coherente con el trato de una entrega verde.

## Arreglos mínimos antes de publicar
1. H1: tratar como FAIL todo estado que no sea PASS ni AMBER.
2. H2: tipos str, largo mínimo del texto, y el id con borde de palabra y el texto en la misma línea o sección del README.
3. H3: en la ruta de la excepción, exigir el set completo de chequeos o `vigentes` presente.
4. H4: guardar `excepcion_usuario` en SUBIDA_OK cuando se usó.
5. Agregar a `test_v1381_excepcion_usuario_subida` los casos H1 a H4.
