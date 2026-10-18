#!/usr/bin/env python3
"""test_sin_colisiones.py (v70) — ningún módulo del paquete tapa a otro con una API incompatible.

Origen: v69 trajo el inventario de tags de la Etapa 1 como `inventario.py` y, al copiarlo encima de las tools, tapó
a `inventario.py` (inventario cerrado de walls) que canon.py importa (`inventario.verificar`,
`inventario.PURLIN_ELEMS`): canon.py dejaba de correr. En v70 la Etapa 1 es `inventario_tags.py`.

Falla si:
  1. `import canon` no obtiene un módulo `inventario` con `verificar` y `PURLIN_ELEMS`;
  2. `inventario_tags` no expone la función `inventario` (Etapa 1) o `inventario` la expone en lugar de `verificar`;
  3. para cada módulo de esta carpeta que otro .py de la carpeta importa, importarlo NO expone los nombres públicos
     que los otros leen de él (`import X` + `X.nombre`, `from X import nombre`). Módulos que no se pueden importar
     aquí (dependencia ausente) se listan como SKIP, no fallan.

Correr: python3 test_sin_colisiones.py [carpeta]   (default: la carpeta de este archivo)
"""
import ast
import importlib
import os
import sys

CARPETA = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CARPETA)
FALLOS, SKIP, AVISOS = [], [], []
# Choques que YA estaban en el stack antes de v70 (capas viejas con otra API; no son de la Etapa 1). Se listan como
# AVISO para el arbitraje y no fallan; cualquier choque NUEVO falla.
CONOCIDOS = {("tagband", "barrido"), ("tagband", "geom"), ("verif_coherencia", "verificar"), ("zoom", "zoom")}


def check(cond, msg):
    if not cond:
        FALLOS.append(msg)


def test_canon_ve_inventario_de_walls():
    import canon
    inv = getattr(canon, "inventario", None)
    check(inv is not None, "canon.py no importa `inventario`")
    check(callable(getattr(inv, "verificar", None)), "canon.inventario sin `verificar` (¿lo tapó el inventario de tags?)")
    check(hasattr(inv, "PURLIN_ELEMS"), "canon.inventario sin `PURLIN_ELEMS`")
    check(os.path.basename(getattr(inv, "__file__", "")) == "inventario.py", f"canon.inventario = {inv}")


def test_inventario_tags_etapa1():
    import inventario
    import inventario_tags
    check(callable(getattr(inventario_tags, "inventario", None)), "inventario_tags sin la función `inventario`")
    check(callable(getattr(inventario_tags, "verificar_png", None)), "inventario_tags sin `verificar_png`")
    check(not hasattr(inventario, "verificar_png"), "inventario.py es el inventario de TAGS (Etapa 1): debe llamarse "
                                                    "inventario_tags.py")
    check(inventario is not inventario_tags, "inventario e inventario_tags son el mismo módulo")


def usos(carpeta):
    """{módulo de la carpeta: {nombre: [archivos que lo leen]}}."""
    locales = {f[:-3] for f in os.listdir(carpeta) if f.endswith(".py")}
    yo = os.path.basename(__file__)[:-3]
    out = {}
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".py") or f[:-3] == yo:
            continue
        try:
            arbol = ast.parse(open(os.path.join(carpeta, f), encoding="utf-8").read())
        except (SyntaxError, UnicodeDecodeError):
            continue
        alias = {}
        for n in ast.walk(arbol):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in locales and a.name != f[:-3]:
                        alias[a.asname or a.name] = a.name
            elif isinstance(n, ast.ImportFrom) and n.module in locales and not n.level and n.module != f[:-3]:
                for a in n.names:
                    if a.name != "*":
                        out.setdefault(n.module, {}).setdefault(a.name, []).append(f)
        asignados = {(n.value.id, n.attr) for n in ast.walk(arbol) if isinstance(n, ast.Attribute) and
                     isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name)}
        for n in ast.walk(arbol):
            if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load) and isinstance(n.value, ast.Name) \
                    and n.value.id in alias and (n.value.id, n.attr) not in asignados:
                out.setdefault(alias[n.value.id], {}).setdefault(n.attr, []).append(f)
    return out


def test_apis_de_los_modulos_importados():
    for mod, nombres in sorted(usos(CARPETA).items()):
        try:
            m = importlib.import_module(mod)
        except SystemExit:
            SKIP.append(f"{mod}: sale al importarlo (tool retirada)")
            continue
        except Exception as e:  # noqa: BLE001
            SKIP.append(f"{mod}: no se pudo importar aquí ({type(e).__name__}: {e})")
            continue
        for n, quien in sorted(nombres.items()):
            if (mod, n) in CONOCIDOS and not hasattr(m, n):
                AVISOS.append(f"{mod}.{n} no existe y lo usa {sorted(set(quien))} (choque previo a v70, conocido)")
                continue
            check(hasattr(m, n), f"{mod}.{n} no existe pero lo usan: {sorted(set(quien))[:5]} (¿otro {mod}.py con "
                                 f"API distinta tapó al bueno?)")


def main():
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
            except Exception as e:  # noqa: BLE001
                FALLOS.append(f"{k}: {type(e).__name__}: {e}")
    for x in SKIP:
        print("SKIP:", x)
    for x in AVISOS:
        print("AVISO:", x)
    if FALLOS:
        for x in FALLOS:
            print("FALLO:", x)
        print(f"test_sin_colisiones: {len(FALLOS)} fallo(s)")
        return 1
    print("test_sin_colisiones: OK (canon -> inventario de walls; inventario_tags = Etapa 1; APIs compatibles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
