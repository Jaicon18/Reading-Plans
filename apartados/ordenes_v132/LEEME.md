# v81cf132 APARTADA (NO publicada; COORDINACIÓN 13-nov 03:44)

Cambio solo en el hook de órdenes (`.claude/hooks/registrar_orden.py`, BE-143) y su test (`test_verificar_version.py::hook_solo_usuario`):
- El hook guardó como orden del usuario el aviso del sistema "This session's worker process was restarted…" (id 3b88645a6b4d en
  cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl).
- AUTOMATICO ahora también filtra ese aviso, y el resumen automático "This session is being continued from a previous conversation…".
- Test: los dos textos = no son del usuario; una frase del usuario que menciona "worker process was restarted" en otro orden sí se guarda.
- Control: con el hook vigente el aviso se guardaba (es_del_usuario = True); con el apartado = False.

Al publicar: copiar `registrar_orden.py` a `.claude/hooks/` y `test_verificar_version.py` a `.claude/skills/jc-hunter-ordenes/` (unir por
contenido si alguien los cambió, BE-XF15); el skill de take-off no cambia (v132 = v131 + este hook).
