RESOLUCIÓN DIRIGIDA (R80e.37): resuelve SOLO las diferencias entre la lectura A y la lectura B listadas en {revision} (difieren / solo_A / solo_B / alertas). No releas el plano completo: abre el recorte de cada diferencia y la hoja que cita.

Valida el resultado con `python3 validar_canon.py {out} tools` hasta "CANON OK". No cambies ningún otro wall, ni Inputs del estimador (yields, waste, stock), ni reglas del skill. No calcules materiales.

{out} YA contiene el canon base ({canon_A}: la lectura más completa). EDITA {out} en su lugar: corrige solo los walls en diferencia (y agrega los que la otra lectura sí trae y el plano confirma), citando N/HOJA. La otra lectura está en este directorio (takeoff_canon_A.json / takeoff_canon_B.json). Plano: {pdf}. Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual. No abras otros directorios, repositorios, take-offs anteriores ni resultados de otras corridas.
