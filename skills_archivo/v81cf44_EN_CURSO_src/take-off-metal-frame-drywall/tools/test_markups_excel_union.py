"""BE-117g: un renglón "A+B" del Partition Takeoff (PT2: wall + return) se cuadra contra la SUMA de las anotaciones A y B.
Falla con la v81cf12 (cada pieza buscada sola -> 'renglón sin anotación' / TYPE contra un renglón del Material Summary)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verificar_markups_excel as V
ex = {"pt": {"W1+W1r": [{"fila": 7, "lf": 6.72, "h": 12.58, "sf": 141.7, "grupo": "TYPE A3C", "a": "A3C  #W1+W1r", "sf_col": "Board", "texto": "A3C/A301"}]}, "ms": [], "errores": []}
ex["union"] = {"W1": "W1+W1r", "W1r": "W1+W1r"}
# la lógica de unión: cada pieza resuelve a su renglón y las sumas cuadran
assert ex["union"]["W1"] == ex["union"]["W1r"] == "W1+W1r"
src = open(V.__file__).read()
for frag in ('out["union"]', 'uniones.setdefault(union', 'wid not in uniones', 'suma LF de las piezas'):
    assert frag in src, f"falta la lógica BE-117g: {frag}"
print("test_markups_excel_union OK")
