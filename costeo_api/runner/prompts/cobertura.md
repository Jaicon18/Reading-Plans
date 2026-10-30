COBERTURA REDUCIDA (paso 12, R80e.37). Lista, sin calcular nada, TODOS los detalles, notas, key notes y spec lines del trade (metal frame y drywall, Div 05 / 09) que imprime el plano {pdf}. Mira las hojas raster como imagen.

Escribe {out} como JSON: [{{"sheet": "A-410", "type": "Detail" | "General note" | "Key note" | "Spec line" | "Schedule", "text": "<texto literal, con su N/HOJA si lo tiene>", "destination": "<renglón del Material Summary / Partition Takeoff, ALC-xx, RFI-xx, o n/a - motivo>"}}]. Toma los destinos del Excel ya armado ({excel}).

HERRAMIENTAS: escribe {out} con la herramienta Write (no con Bash ni heredocs). Bash solo admite comandos que empiezan con `python3` (sin mkdir, sin &&); guarda los renders en el directorio actual. Escribe la lista en cuanto la tengas; sé breve en el texto (el literal corto con su N/HOJA basta).

El script cobertura.py verifica que cada destino exista. Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual. No abras otros directorios, repositorios, take-offs anteriores ni resultados de otras corridas.
