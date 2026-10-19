#!/usr/bin/env python3
"""reglas_catalogo.py — v72b: el catálogo de TODAS las reglas del skill, extraído del texto (SKILL.md + referencias/).

Por qué existe: una regla escrita que ninguna tool revisa depende de que la corrida se acuerde de ella. Este módulo
recorre el texto y saca CADA regla con un id estable; `reglas_clasificacion.py` le da a cada una su tipo:
  (a) verificable con datos (canon, salidas de las tools, Excel)  → chequeo automático en `reglas.py`;
  (b) requiere juicio de plano → `reglas.py` exige evidencia registrada por caso (N/HOJA + imagen existente + valor
      + regla citada) y falla si falta o si el valor contradice la regla;
  (c) redundante / obsoleta → fusionada en otra regla (se dice en cuál) o anulada por una regla posterior; el
      texto del estimador no se borra.
`test_reglas.py` falla si aparece una regla en el texto que no está clasificada: no hay regla sin chequeo.

Unidades:
  - protocolo (SKILL.md antes de "REFERENCIA DE MÉTODO"): cada viñeta / renglón de tabla / ítem numerado de las
    secciones de reglas; los ids explícitos (E1…E28, R70.1…, PT1…, D1…, A1…) se respetan y una viñeta con dos ids
    (p. ej. **E9** … **E10** …) da dos reglas;
  - referencia de método y adendas del SKILL: cada sección ##/### con regla, y cada viñeta de las listas de reglas
    (REGLAS INVIOLABLES, LOS ERRORES Y SU SOLUCIÓN, ANTES DE ENTREGAR, PROTOCOLO DE EJECUCIÓN, GRANULARIDAD …);
  - referencias/*.md: cada sección ##/### que no es narración (De dónde salió, Estado, Probado …).

Uso:  python3 reglas_catalogo.py [carpeta_del_skill]      lista id · archivo:línea · título
      python3 reglas_catalogo.py --json [carpeta]         el catálogo en JSON
"""
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# v73: $TAKEOFF_SKILL primero (skill instalado en otra ruta: la prueba 21B corrió 37/45 por "SKILL.md fuera de ruta")
SKILL_DIRS = tuple(x for x in (os.environ.get("TAKEOFF_SKILL"),
                               os.path.join(AQUI, "..", "take-off-metal-frame-drywall"),
                               os.path.join(AQUI, "take-off-metal-frame-drywall"), os.path.join(AQUI, ".."),
                               os.path.expanduser("~/.claude/skills/take-off-metal-frame-drywall")) if x)

ID_EXPL = re.compile(r"\*\*(E\d{1,2}|R7\d\.\d{1,2}b?|PT\d|D\d{1,2}|A\d{1,2}(?:–A\d{1,2})?)\*\*")
ID_TABLA = re.compile(r"^\|\s*(R7\d\.\d{1,2}b?|PT\d|D\d{1,2}|A\d{1,2}(?:–A\d{1,2})?)\s*\|")
NARRATIVA = re.compile(
    r"De dónde|Lo que sali|Lo que se corrigi|Qué lo origin|Cómo se encontr|Cómo se cerr|Probad[oa]|^Estado|El ejemplo"
    r"|Lo que (la columna|el barrido|encontr|pas|se pag|sigue)|El hueco de verdad|No era error|Los cinco errores"
    r"|Por qué|El caso que|^El test|^Barrido de los|^Cobertura de detalles|^La regla de waste|Qué cambi|^ADENDA"
    r"|LO QUE PASÓ|Cómo se verific|CORRECCIÓN DEL MISMO DÍA|^\d\. `\S+` no existe|^Lo que el barrido|^RFIs$"
    r"|^El otro hallazgo|EL OTRO HALLAZGO|^LOS CUATRO CASOS|^Dos bugs propios|^Error de la propia|^Tres cosas que"
    r"|^LOS TRES ERRORES|^Lo que NO entró|^Y una corrección|^Cómo se resolvió|^El riesgo que cubre|^El modo 4"
    r"|^Las cuatro partes|^Lo que cambió|^Sigue valiendo|^Cómo se usa|^Dos RFIs nuevos|^El purlin que|^El bulkhead de"
    r"|^\d\. (La nota F|El FRP del|El B\w+ Room|Dos cantidades)|^La pregunta que|^Herramientas( \(|$)"
    r"|^CÓMO SE ENCONTRÓ|^POR QUÉ|^Los cuatro pasos|^Tres reglas nuevas|^Barrido de los|^La herramienta|el error de este día",
    re.I)
# secciones del protocolo cuyas viñetas / renglones son reglas una por una
LISTAS = re.compile(
    r"^(\d+\. |Etapa \d|Subagentes|Etapas y carpeta|REGLAS INVIOLABLES|LOS ERRORES Y SU SOLUCIÓN|ANTES DE ENTREGAR"
    r"|PROTOCOLO DE EJECUCIÓN|GRANULARIDAD Y MARCADO|FORMATO DE SALIDA|GEOMETRÍA VECTORIAL|EVIDENCIA VISUAL"
    r"|Método técnico|HEIGHT DE DECK|HEIGHT DE BOARD|LOS MARKUPS|VERIFICACIÓN ADVERSARIAL|LAS TRES AUTOVERIF"
    r"|HERRAMIENTAS — EL CÓDIGO|DIMENSION STRINGS|ELEVACIONES Y VISTAS|CLARIFICATIONS|FORMATO DE ENTREGA"
    r"|BARRIDO COMPLETO|VERIFICACIÓN CRUZADA DEL BARRIDO|REGISTRO ENTRE HOJAS)")
SALTAR = re.compile(r"^(ÍNDICE DE REGLAS POR ARCHIVO|TERMINOLOGÍA$|Take-off de Metal Frame|PROTOCOLO v69|"
                    r"REFERENCIA DE MÉTODO|ADENDAS v48|CÓMO ESTÁ ORGANIZADO|SÚPER REGLAS DE LAS ADENDAS|"
                    r"Desde `referencias/|ESTRUCTURA DE CARPETA|CONTRATO DE LAS HERRAMIENTAS)")


def skill_dir(d=None):
    for c in ([d] if d else []) + list(SKILL_DIRS):
        if c and os.path.isfile(os.path.join(c, "SKILL.md")):
            return os.path.abspath(c)
    raise SystemExit("no encuentro SKILL.md (pasar la carpeta del skill)")


def _slug(t, n=40):
    t = re.sub(r"[`*⛔—–:()\"'#.,/]", " ", t)
    t = re.sub(r"\s+", "-", t.strip()).lower()
    return t[:n].strip("-")


def _hid(texto):
    return hashlib.sha1(re.sub(r"\s+", " ", texto.strip()).encode()).hexdigest()[:6]


def _limpio(t):
    return re.sub(r"\s+", " ", re.sub(r"[*`]", "", t)).strip()


def _items(lineas, negrita=False):
    """[(n_linea, texto)] viñetas, ítems numerados y renglones de tabla (con su continuación); con `negrita`, también
    cada párrafo que empieza en negrita (**PASO 3 …**, **Alturas.** …)."""
    out, cur = [], None
    for n, l in lineas:
        s = l.rstrip()
        es_item = (re.match(r"^\s{0,3}([-*] |\d{1,2}[a-e]?\. |\| )", s) or negrita and s.startswith("**")) \
            and not re.match(r"^\|\s*[-:|\s]+\|?$", s)
        if es_item:
            if re.match(r"^\|\s*(#|Familia|Momento|Tool|Regla)\s*\|", s):     # encabezado de tabla
                cur = None
                continue
            cur = [n, s]
            out.append(cur)
        elif cur is not None and s.startswith("  ") and s.strip():
            cur[1] += " " + s.strip()
        elif not s.strip():
            cur = None
    return [(n, t) for n, t in out]


def _secciones(texto):
    """[(nivel, titulo, n_linea, [(n, linea)])]"""
    secs, cur, en_codigo = [], (0, "", 1, []), False
    for n, l in enumerate(texto.splitlines(), 1):
        if l.startswith("```"):
            en_codigo = not en_codigo
        m = re.match(r"^(#{1,4}) (.+)$", l) if not en_codigo else None
        if m:
            secs.append(cur)
            cur = (len(m.group(1)), m.group(2).strip(), n, [])
        else:
            cur[3].append((n, l))
    secs.append(cur)
    return secs


def _tiene_texto(lineas):
    return any(l.strip() and not l.startswith("---") for _, l in lineas)


def extraer(d=None):
    d = skill_dir(d)
    out = []
    skill = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
    corte = skill.find("# REFERENCIA DE MÉTODO")
    n_corte = skill[:corte].count("\n") + 1 if corte > 0 else 10 ** 9
    vistos = set()

    def add(rid, arch, n, titulo, texto, parte):
        base = rid
        k = 2
        while rid in vistos:
            rid = f"{base}~{k}"
            k += 1
        vistos.add(rid)
        out.append({"id": rid, "archivo": arch, "linea": n, "titulo": _limpio(titulo)[:160],
                    "texto": _limpio(texto)[:600], "parte": parte})

    for nivel, tit, n0, lineas in _secciones(skill):
        if not tit or SALTAR.search(tit):
            continue
        parte = "protocolo" if n0 < n_corte else ("adendas_skill" if re.search(r"ADENDA v[4-6]\d|REGLA \d\d\.\d", tit)
                                                 or n0 > skill.find("# ADENDAS v48") and skill.find("# ADENDAS v48") > 0
                                                 and n0 > skill[:skill.find("# ADENDAS v48")].count("\n") else "referencia_metodo")
        if parte == "protocolo" or LISTAS.search(tit):
            neg = parte != "protocolo"
            its = _items(lineas, neg)
            prosa = [l for n, l in lineas if l.strip() and not re.match(r"^\s{0,3}([-*] |\d{1,2}\. |\| |  |\*\*)", l)
                     and not l.startswith(("---", "```", "<!--"))]
            if its and parte != "protocolo" and prosa:
                add(f"S:{_slug(tit)}", "SKILL.md", n0, tit, " ".join(prosa)[:600], parte)
            if not its:
                if _tiene_texto(lineas) and not re.match(r"^\d+\. Criterios|^ADENDA", tit):
                    add(f"S:{_slug(tit)}", "SKILL.md", n0, tit, " ".join(l for _, l in lineas)[:600], parte)
                continue
            for n, t in its:
                ids = ID_EXPL.findall(t) if tit.startswith("0.") else []
                mt = ID_TABLA.match(t)
                if mt:
                    ids = [mt.group(1)]
                if ids:
                    for i in ids:
                        add(i, "SKILL.md", n, f"{i} ({tit})", t, parte)
                else:
                    sec = re.match(r"^(\d+)\. ", tit)
                    pref = f"§{sec.group(1)}" if sec else _slug(tit, 24)
                    add(f"S:{pref}:{_hid(t)}", "SKILL.md", n, f"{tit}: {t[:90]}", t, parte)
            continue
        m = re.search(r"REGLA (\d\d\.\d{1,2})", tit)
        if m:
            add(f"REGLA {m.group(1)}", "SKILL.md", n0, tit, " ".join(l for _, l in lineas), parte)
            continue
        if NARRATIVA.search(tit) or not _tiene_texto(lineas):
            continue
        add(f"S:{_slug(tit)}", "SKILL.md", n0, tit, " ".join(l for _, l in lineas), parte)

    rd = os.path.join(d, "referencias")
    for f in sorted(os.listdir(rd)) if os.path.isdir(rd) else []:
        if not f.endswith(".md") or f == "REGLAS_INVIOLABLES.md":    # la tabla generada no es una regla
            continue
        txt = open(os.path.join(rd, f), encoding="utf-8").read()
        corto = f[:-3].replace("adenda_", "")
        for nivel, tit, n0, lineas in _secciones(txt):
            m = re.search(r"REGLA (\d\d\.\d{1,2})", tit)
            if not tit or nivel == 1 and f.startswith("adenda") or NARRATIVA.search(tit) or \
                    not _tiene_texto(lineas) and not m:
                continue
            if f == "herramientas.md" and nivel == 1:
                continue
            rid = f"REGLA {m.group(1)}" if m else f"{corto}:{_slug(tit)}"
            add(rid, f"referencias/{f}", n0, tit, " ".join(l for _, l in lineas), "referencias")
    return out


def main(argv):
    a = [x for x in argv[1:] if x != "--json"]
    cat = extraer(a[0] if a else None)
    if "--json" in argv:
        json.dump(cat, sys.stdout, ensure_ascii=False, indent=1)
        return 0
    for r in cat:
        print(f"{r['id']:28s} {r['archivo']}:{r['linea']:<5d} {r['titulo'][:100]}")
    print(f"{len(cat)} reglas")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
