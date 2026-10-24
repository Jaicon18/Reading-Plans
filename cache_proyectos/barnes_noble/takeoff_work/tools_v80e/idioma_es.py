#!/usr/bin/env python3
"""idioma_es.py (v72) — ¿un texto del entregable está en español? Lo usan plantilla_excel.es_texto_es y verif_idioma.

Por qué viaja en el paquete: hasta v71 este módulo venía del entorno de la prueba y no estaba en ninguna capa de
tools; sin él test_plantilla_v67 / v68 / v70 caían con ModuleNotFoundError. Si el entorno trae uno propio, el del
entorno puede reemplazar a este (misma API: es_espanol(texto) -> lista de marcas, vacía si está en inglés).

Regla: marcas de español = palabras funcionales y del oficio en español (no los términos del trade, que van en
inglés) y signos ¿ ¡. Un nombre propio de room con acento NO basta solo (p. ej. un nombre de cliente): hacen falta
2 marcas, o 1 marca que sea frase (artículo / preposición + palabra).
"""
import re

FUNCIONALES = {
    "el", "la", "los", "las", "del", "al", "una", "unos", "unas", "que", "por", "para", "con", "sin", "sobre",
    "entre", "hasta", "desde", "cada", "según", "segun", "también", "tambien", "pero", "porque", "cuando", "donde",
    "como", "más", "mas", "menos", "esta", "este", "estos", "estas", "ese", "esa", "hay", "son", "está", "están",
    "se", "su", "sus", "lo", "le", "les", "y", "o", "ni", "no", "sí", "ya", "muy", "todo", "toda", "todos", "todas",
}
OFICIO = {
    "muro", "muros", "pared", "paredes", "techo", "cielo", "piso", "losa", "viga", "vigas", "columna", "puerta",
    "puertas", "ventana", "ventanas", "altura", "ancho", "largo", "cara", "caras", "hoja", "hojas", "detalle",
    "detalles", "abertura", "aberturas", "esquina", "esquinas", "criterio", "estimador", "pendiente", "confirmado",
    "derivado", "cuantificado", "acotado", "acotada", "medido", "medida", "cerrado", "cerrada", "arriba", "abajo",
    "izquierda", "derecha", "norte", "sur", "este", "oeste", "fachada", "fachadas", "usuario", "regla", "falta",
}
PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
SIGNOS = re.compile(r"[¿¡]")
ACENTO = re.compile(r"[áéíóúñ]")
NO_ES = {"a", "o", "no", "se", "este", "la", "como"}   # también existen en inglés o como abreviatura / punto cardinal

# v78 (R78.3): ids de wall / elemento SIN dígito (p. ej. X-EXT-Q-LO: el sufijo de zona LO no es el pronombre "lo") y
# listas "#id+id" se quitan ANTES de buscar marcas. Genérico y en MAYÚSCULAS (case-sensitive): un id = 3+ segmentos
# de 1-5 caracteres [A-Z0-9] unidos por guion; una lista = '#' + ids unidos por '+'. Texto español real (minúsculas o
# palabras largas) no se toca.
IDS = [re.compile(r"#[A-Z0-9][A-Z0-9_\-]*(?:\+[A-Z0-9][A-Z0-9_\-]*)*"),
       re.compile(r"(?<![\w\-])[A-Z0-9]{1,5}(?:-[A-Z0-9]{1,5}){2,}(?![\w\-])")]


def quitar_ids(texto):
    for rx in IDS:
        texto = rx.sub(" ", texto)
    return texto


def es_espanol(texto):
    """-> lista ordenada de marcas de español en `texto` ([] = inglés o sin marcas suficientes)."""
    if not isinstance(texto, str) or len(texto) < 4:
        return []
    texto = quitar_ids(texto)                              # v78 R78.3
    marcas = set(SIGNOS.findall(texto))
    ws = [w.lower() for w in PALABRA.findall(texto)]
    fuertes = {w for w in ws if (w in FUNCIONALES or w in OFICIO) and w not in NO_ES}
    marcas |= fuertes
    acentos = {w for w in ws if ACENTO.search(w)}
    if SIGNOS.search(texto):
        return sorted(marcas | acentos)
    frase = any(ws[i] in FUNCIONALES and ws[i] not in NO_ES and i + 1 < len(ws) for i in range(len(ws)))
    if len(fuertes) >= 2 or (fuertes and frase) or (fuertes and acentos):
        return sorted(marcas | acentos)
    return []


if __name__ == "__main__":
    import sys
    for t in sys.argv[1:]:
        print(es_espanol(t) or "EN", "|", t)
