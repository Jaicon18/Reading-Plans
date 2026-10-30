RESOLUCIÓN DIRIGIDA (R80e.37): resuelve SOLO las diferencias entre la lectura A y la lectura B listadas en {revision} (difieren / solo_A / solo_B / alertas). No releas el plano completo: abre el recorte de cada diferencia y la hoja que cita.

Valida el resultado con `python3 validar_canon.py {out} tools` hasta "CANON OK". No cambies ningún otro wall, ni Inputs del estimador (yields, waste, stock), ni reglas del skill. No calcules materiales.

Parte del canon base ({canon_A}: la lectura más completa). Corrige solo los walls en diferencia, citando N/HOJA, y escribe el resultado en {out}. Plano: {pdf}. Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual. No abras otros directorios, repositorios, take-offs anteriores ni resultados de otras corridas.
