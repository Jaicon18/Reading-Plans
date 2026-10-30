CORRECCIÓN DE LA LECTURA (R80e.38). La cadena completa corrió con tu canon {out} y la compuerta reglas.py NO deja armar el Excel. Estas son las fallas que dependen de la LECTURA, con los ids de TU canon:

{motivo}

Si una falla habla de un ceiling / soffit / drop line, lee el RCP (A-121) y la sección del soffit (2/A-221): agrega los soffit sides que falten (element "soffit_side", soffit_of con el nombre del ceiling tal como aparece en la falla, drop_line, faces y height por la sección) y los ceilings del RCP.

Si una falla es de alcances.py (un alcance marcado cuantificado sin cantidad), cuantifícalo desde el plano: p. ej. metal trim (corner bead, casing bead, control joints, reveals) va en trim_items[] {{ref, kind, label, lf, source (hoja), op}} con el LF medido / derivado de las esquinas y bordes expuestos; si de verdad no aplica, trim_none_reason con la hoja revisada.

Corrige o completa EN EL MISMO ARCHIVO {out}, leyendo el plano {pdf} (no inventes: lo que no esté impreso va como RFI con su delta o PENDIENTE). No cambies coordenadas ni cantidades que ya están bien. No generes imágenes ni estados: los genera el programa. Valida con `python3 validar_canon.py {out} tools` hasta "CANON OK". Al terminar, responde solo "OK {out}".

AISLAMIENTO: trabaja SOLO con los archivos de tu directorio actual.
