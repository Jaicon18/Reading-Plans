"""Verifica que un skill de arranque contenga TODAS las reglas acumuladas Y que cada regla "programa" tenga su compuerta.

Uso: python3 -I verificar_version.py <skill_dir_o_zip> <skills_archivo_dir> [<cache_proyectos_dir>]
     python3 -I verificar_version.py --selftest
1. (BE-115) Busca ids de reglas (R80e.N, R80w.N, R7x.N, R-ALC-NN, BE-N, BE-XX-NN, U-NNN) en todas las versiones archivadas
   (zips) y en cache_proyectos/*.md, y reporta las que no aparecen en el skill candidato.
2. (BE-121) revisar_registro: el candidato trae REGLAS_REGISTRO.json; toda regla "programa" tiene chequeo(s) que EXISTEN
   (archivo + función / compuerta A_*) y un test que existe y cita su token; "historico" apunta a una regla del registro;
   "programa-pendiente" dice por qué. Cobertura: todo R-ALC del REGLAS_ALCANCE.md, todo BE de la BIBLIOTECA_ERRORES.md y
   todo [U-NNN] de REGLAS_USUARIO_CLAUDE.md / REGLAS_HISTORICO.md está en el registro; toda regla vigente lleva su [U-NNN].
3. (U-020) revisar_zip: < 200 archivos, SKILL.md con YAML name / description, sin __pycache__, sin tools.orig_*, sin
   entradas de directorio (zip -D).
4. (U-027) revisar_indice: la VERSIÓN VIGENTE de skills_archivo/INDICE.md existe como zip archivado; (BE-146)
   revisar_indice_encabezado: el "(hoy vN" del encabezado = la última línea "vN = VERSIÓN VIGENTE".
Sale con código 1 si falta algo (no arrancar el proyecto ni marcar la versión vigente).
"""
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
# Ids citados solo como "no existe" (no son reglas).
IGNORAR = {"BE-109"}

PAT = re.compile(r"\b(R80[a-z]\.\d+|R7\d\.\d+|R-ALC-\d+|BE-[A-Z]{2,3}-?\d+|BE-\d+|U-\d{3})\b")


def ids_en_texto(t):
    return set(PAT.findall(t))


def ids_en_ruta(p):
    out = set()
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith((".md", ".py", ".json")):
                    out |= ids_en_texto(z.read(n).decode("utf-8", "ignore"))
    elif os.path.isdir(p):
        for raiz, _, archivos in os.walk(p):
            for a in archivos:
                if a.endswith((".md", ".py", ".json")):
                    with open(os.path.join(raiz, a), encoding="utf-8", errors="ignore") as f:
                        out |= ids_en_texto(f.read())
    elif os.path.isfile(p):
        with open(p, encoding="utf-8", errors="ignore") as f:
            out |= ids_en_texto(f.read())
    return out


class Fuente:
    """Lee archivos del skill candidato (zip o carpeta) por ruta relativa a la carpeta del skill (la que tiene SKILL.md)."""

    def __init__(self, p):
        self.zip = zipfile.ZipFile(p) if zipfile.is_zipfile(p) else None
        if self.zip:
            sk = [n for n in self.zip.namelist() if n.endswith("SKILL.md") and n.count("/") <= 1]
            self.base = sk[0][:-len("SKILL.md")] if sk else ""
        else:
            self.base = p if os.path.isfile(os.path.join(p, "SKILL.md")) else os.path.join(p, "take-off-metal-frame-drywall")

    def leer(self, rel):
        try:
            if self.zip:
                return self.zip.read(self.base + rel).decode("utf-8", "ignore")
            return open(os.path.join(self.base, rel), encoding="utf-8", errors="ignore").read()
        except (KeyError, OSError):
            return None


def _ruta(fuente, ordenes_dir, ref):
    pre, rel = ref.split(":", 1)
    if pre == "take-off":
        return fuente.leer(rel)
    if pre == "ordenes":
        p = os.path.join(ordenes_dir, rel)
        return open(p, encoding="utf-8", errors="ignore").read() if os.path.isfile(p) else None
    return None


def _tiene_funcion(txt, nombre):
    if nombre in ("modulo", "main") and txt is not None:
        return True
    if nombre.startswith("A_"):
        return f'"{nombre}"' in txt
    return re.search(r"^\s*def " + re.escape(nombre) + r"\b|^" + re.escape(nombre) + r"\s*=", txt, re.M) is not None


def ids_biblioteca(txt):
    ids = set()
    for l in txt.splitlines():
        m = re.match(r"\|\s*(BE-[A-Z0-9-]+)\s*\|", l) or re.match(r"#+\s*(BE-[A-Z0-9-]+)\b", l) or \
            re.match(r"[-*]\s*\*{0,2}(BE-[A-Z0-9-]+)\*{0,2}\s*[:—-]", l)
        if m:
            ids.add(m.group(1))
    return ids


def revisar_registro(fuente, ordenes_dir, cache_dir=None):
    """BE-121 -> lista de faltas (texto)."""
    f = []
    t = fuente.leer("REGLAS_REGISTRO.json")
    if t is None:
        return ["el skill candidato no trae REGLAS_REGISTRO.json (BE-121)"]
    reg = json.loads(t)
    ids = {e["id"] for e in reg.get("reglas") or []}
    for e in reg.get("reglas") or []:
        cat, i = e.get("categoria"), e["id"]
        if cat == "programa":
            chs, ts = e.get("chequeos") or [], [e.get("test")] + list(e.get("tests_extra") or [])
            if not chs:
                f.append(f"{i}: programa sin chequeo")
            for ch in chs:
                arch, _, fn = ch.partition("::")
                txt = _ruta(fuente, ordenes_dir, arch)
                if txt is None:
                    f.append(f"{i}: el chequeo {arch} no existe")
                elif not _tiene_funcion(txt, fn):
                    f.append(f"{i}: {arch} no tiene {fn}")
            for tt in ts:
                if not tt or not tt.get("archivo"):
                    f.append(f"{i}: programa sin test")
                    continue
                txt = _ruta(fuente, ordenes_dir, tt["archivo"])
                if txt is None:
                    f.append(f"{i}: el test {tt['archivo']} no existe")
                elif not re.search(r"(?<![\w-])" + re.escape(tt.get("token") or "") + r"(?![\w])", txt):
                    f.append(f"{i}: el test {tt['archivo']} no cita '{tt.get('token')}'")
        elif cat == "historico":
            if e.get("reemplazada_por") not in ids:
                f.append(f"{i}: histórica sin regla vigente que la reemplace")
        elif cat == "programa-pendiente":
            if not str(e.get("motivo") or "").strip():
                f.append(f"{i}: programa-pendiente sin motivo")
        elif cat != "conducta":
            f.append(f"{i}: categoría desconocida '{cat}'")
    alc = os.path.join(ordenes_dir, "REGLAS_ALCANCE.md")
    if os.path.isfile(alc):
        for x in sorted(set(re.findall(r"^## (R-ALC-\d+)", open(alc, encoding="utf-8").read(), re.M)) - ids):
            f.append(f"{x}: en REGLAS_ALCANCE.md pero no en el registro")
    bib = os.path.join(ordenes_dir, "BIBLIOTECA_ERRORES.md")
    if os.path.isfile(bib):
        for x in sorted(ids_biblioteca(open(bib, encoding="utf-8").read()) - ids):
            f.append(f"{x}: en BIBLIOTECA_ERRORES.md pero no en el registro")
    if cache_dir:
        for n in ("REGLAS_USUARIO_CLAUDE.md", "REGLAS_HISTORICO.md"):
            p = os.path.join(cache_dir, n)
            if not os.path.isfile(p):
                f.append(f"falta cache_proyectos/{n}")
                continue
            txt = open(p, encoding="utf-8").read()
            for x in sorted(set(re.findall(r"\[(U-\d{3})", txt)) - ids):
                f.append(f"{x}: en {n} pero no en el registro")
            if n == "REGLAS_USUARIO_CLAUDE.md":
                vig = txt.split("## REGLAS VIGENTES", 1)[-1]
                for l in vig.splitlines():
                    if l.startswith("- ") and not re.match(r"- \[U-\d{3}", l):
                        f.append(f"regla vigente sin id [U-NNN] (agregarla al registro): {l[:80]}")
    return f


def revisar_zip(p):
    """U-020 -> lista de faltas del zip del skill. BE-XF08 (Xfinity 11-nov, v81cf86 publicada con 208 archivos): con una CARPETA
    candidata también se cuentan los archivos (antes solo se contaban en un .zip y la carpeta pasaba); 200 o más = FAIL."""
    if not zipfile.is_zipfile(p):
        if os.path.isdir(p):
            base = p if os.path.isfile(os.path.join(p, "SKILL.md")) else os.path.join(p, "take-off-metal-frame-drywall")
            n = sum(len([f for f in fs]) for r, _d, fs in os.walk(base) if "__pycache__" not in r)
            if n >= 200:
                return [f"BE-XF08: la carpeta candidata tiene {n} archivos (límite de Upload skill < 200)"]
        return []
    f = []
    with zipfile.ZipFile(p) as z:
        ns = z.namelist()
        arch = [n for n in ns if not n.endswith("/")]
        if len(arch) >= 200:
            f.append(f"zip con {len(arch)} archivos (límite < 200)")
        if any(n.endswith("/") for n in ns):
            f.append("zip con entradas de directorio (usar zip -D)")
        if any("__pycache__" in n for n in ns):
            f.append("zip con __pycache__")
        if any(re.search(r"(^|/)tools\.orig_", n) for n in ns):
            f.append("zip con carpeta de respaldo tools.orig_*")
        sk = [n for n in ns if n.endswith("SKILL.md") and n.count("/") <= 1]
        if not sk:
            f.append("zip sin SKILL.md")
        else:
            t = z.read(sk[0]).decode("utf-8", "ignore")
            m = re.match(r"---\n(.*?)\n---", t, re.S)
            if not m or not re.search(r"^name:\s*\S", m.group(1), re.M) or not re.search(r"^description:\s*\S", m.group(1), re.M):
                f.append("SKILL.md sin YAML name / description")
    return f


def revisar_indice(archivo):
    """U-027 -> faltas: la versión vigente de INDICE.md tiene su zip archivado."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v[0-9a-z]+)", open(p, encoding="utf-8").read())
    if not m:
        return ["INDICE.md no marca la VERSIÓN VIGENTE"]
    v = m.group(1)
    enc = revisar_indice_encabezado(archivo)
    if enc:
        return enc
    zs = [n for n in os.listdir(archivo) if n.startswith(f"take-off-metal-frame-drywall_{v}_") and n.endswith(".zip")]
    if not zs:
        return [f"la versión vigente {v} no tiene zip en skills_archivo"]
    import hashlib
    distintos = {hashlib.md5(open(os.path.join(archivo, n), "rb").read()).hexdigest() for n in zs}
    for n in zs:             # BE-XF08: el zip VIGENTE publicado también se revisa (U-020: < 200 archivos, sin directorios ni __pycache__)
        malas = revisar_zip(os.path.join(archivo, n))
        if malas:
            return [f"BE-XF08: el zip vigente {n}: " + "; ".join(malas)]
    if len(distintos) > 1:   # BE-CF20 (copia idéntica FINAL-<Proyecto> de U-027 no cuenta): dos sesiones archivaron el MISMO número con contenido distinto (línea partida, BE-115)
        return [f"BE-CF20: la versión vigente {v} tiene {len(zs)} zips distintos ({', '.join(sorted(zs))}): unir en v+1"]
    return []


def revisar_indice_encabezado(archivo):
    """BE-146 -> faltas: el encabezado "VERSIÓN VIGENTE ... (hoy vN" de INDICE.md = la ÚLTIMA línea "vM = VERSIÓN VIGENTE" del
    archivo. Caso original (6-nov): v81cf55..v81cf57 publicadas y el encabezado seguía en "hoy v81cf54" (el hook SessionStart
    arrancaba con una versión vieja)."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v[0-9a-z]+)", txt)
    if not m:
        return ["INDICE.md no marca la VERSIÓN VIGENTE"]
    ult = re.findall(r"\b(v[0-9a-z]+) = VERSIÓN VIGENTE", txt)
    if ult and ult[-1] != m.group(1):
        return [f"BE-146: el encabezado de INDICE.md dice 'hoy {m.group(1)}' y la última línea '= VERSIÓN VIGENTE' es {ult[-1]}: "
                f"actualizar el encabezado (o la línea) para que digan la misma versión"]
    return []


def revisar_skill(fuente):
    """BE-87 / BE-VS-11 -> faltas del skill candidato:
    BE-87: dos encabezados R80e.N / R80f.N con el MISMO número y distinto título en SKILL.md (choque de numeración);
    BE-VS-11: un chequeo @chequeo("A_X") de reglas.py que ninguna regla de reglas_clasificacion.py referencia (no corre)."""
    f = []
    sk = fuente.leer("SKILL.md") or ""
    vistos = {}
    for m in re.finditer(r"^#{2,4}\s+(R80[a-z]\.\d+)\s*[—:-]+\s*(.+)$", sk, re.M):
        n, t = m.group(1), re.sub(r"\W+", " ", m.group(2)).strip().lower()[:40]
        if n in vistos and vistos[n] != t:
            f.append(f"BE-87: {n} usado por dos reglas distintas ('{vistos[n][:30]}' / '{t[:30]}')")
        vistos.setdefault(n, t)
    rg, cl = fuente.leer("tools/reglas.py") or "", fuente.leer("tools/reglas_clasificacion.py")
    if rg and cl is not None:
        for a in sorted(set(re.findall(r'@chequeo\("(A_[A-Z0-9_]+)"', rg))):
            if f'"{a}"' not in cl:
                f.append(f"BE-VS-11: el chequeo {a} de reglas.py no está en reglas_clasificacion.py (nunca corre)")
    return f


def revisar_banco(archivo):
    """U-043 / BE-94 -> faltas: la VERSIÓN VIGENTE del INDICE registra la prueba del banco con 0 familias distintas."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    bloques = re.split(r"\n(?=\*\*\d{2}-[a-z]{3}: )", open(p, encoding="utf-8").read())
    vig = [x for x in bloques if "VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO**" in x]
    if not vig:
        return ["INDICE.md sin bloque VERSIÓN VIGENTE"]
    v = vig[-1]
    if not re.search(r"(?i)banco", v):
        return ["U-043: la versión vigente no registra la prueba del banco (todas las lecturas guardadas)"]
    if not re.search(r"(?i)= ?0 (familias )?(distintas|diferencias)|0 familias distintas|0 diferencias|banco:? 0 distintas", v):
        return ["U-043: el banco de la versión vigente no dice 0 familias distintas / 0 diferencias"]
    return []


VERSIONES_DUPLICADAS_HISTORICAS = {"v80u"}


def revisar_versiones_unicas(archivo):
    """BE-144: dos sesiones armaron el mismo número de versión (v81cf43 O'Reilly y CFA; antes BE-CF20).
    Cada número de versión = un solo zip en skills_archivo/. El número se aparta antes de armar
    en skills_archivo/VERSION_EN_CURSO.md (commit + push primero)."""
    import collections, hashlib
    if not archivo or not os.path.isdir(archivo):
        return []
    hashes = collections.defaultdict(set)
    for n in os.listdir(archivo):
        m = re.match(r"take-off-metal-frame-drywall_([^_]+)_.*\.zip$", n)
        if m:
            # copia idéntica (mismo contenido, p. ej. el FINAL-<Proyecto> de U-027) no es otra versión
            hashes[m.group(1)].add(hashlib.md5(open(os.path.join(archivo, n), "rb").read()).hexdigest())
    c = {v: len(h) for v, h in hashes.items()}
    return [f"versión {v} archivada {k} veces (BE-144: apartar el número en VERSION_EN_CURSO.md antes de armar)"
            for v, k in sorted(c.items()) if k > 1 and v not in VERSIONES_DUPLICADAS_HISTORICAS]


def revisar_ordenes(cache, horas=24):
    """U-136: toda orden de la bandeja (_entrantes.jsonl) con más de `horas` sin clasificar en MAPA_ORDENES.json = falta."""
    import json, datetime
    if not cache:
        return []
    car = os.path.join(cache, "ORDENES_CRUDAS")
    ent = os.path.join(car, "_entrantes.jsonl")
    if not os.path.exists(ent):
        return []
    try:
        mapa = json.load(open(os.path.join(car, "MAPA_ORDENES.json"), encoding="utf-8"))
    except Exception:
        mapa = {}
    ahora = datetime.datetime.now(datetime.timezone.utc)
    faltas = []
    for linea in open(ent, encoding="utf-8"):
        try:
            r = json.loads(linea)
        except Exception:
            continue
        if r.get("id") in mapa:
            continue
        try:
            t = datetime.datetime.fromisoformat(r["ts_utc"])
        except Exception:
            t = ahora
        if (ahora - t).total_seconds() > horas * 3600:
            faltas.append(f"{r.get('id')} ({r.get('ts_utc')}) sin clasificar: {r.get('texto','')[:80]}")
    return faltas


RX_POSTMORTEM = re.compile(r"^POSTMORTEM_COBERTURA_(\d{4}-\d{2}-\d{2})[\w.-]*\.md$")
RX_PM_PRINCIPAL = re.compile(r"^POSTMORTEM_COBERTURA_(\d{4}-\d{2}-\d{2})([a-z]?)\.md$")   # el post-mortem; _VERIFICACION / _CIERRE
                                                                                        # / copias son acompañantes, no lo reemplazan


def tabla_postmortem(txt):
    """U-185: renglones de la tabla 'id | error / regla | chequeo | test | estado' -> [(id, estado)]."""
    out, dentro = [], False
    for ln in txt.splitlines():
        cs = [x.strip() for x in ln.strip().strip("|").split("|")]
        if ln.lstrip().startswith("|") and cs and cs[0].lower() == "id" and cs[-1].lower().startswith("estado"):
            dentro = True
            continue
        if dentro and not ln.lstrip().startswith("|"):
            dentro = False
            continue
        if dentro and cs and not set(cs[0]) <= set("-: "):
            out.append((cs[0], cs[-1]))
    return out


def causas_no_guard(txt):
    """U-185 (verificación 12b): tabla de causas '# | causa | candado | estado': un renglón con 'NO GUARD' en su estado sigue abierto."""
    out, dentro = [], False
    for ln in txt.splitlines():
        cs = [x.strip() for x in ln.strip().strip("|").split("|")]
        if ln.lstrip().startswith("|") and cs and cs[0] == "#" and cs[-1].lower().startswith("estado"):
            dentro = True
            continue
        if dentro and not ln.lstrip().startswith("|"):
            dentro = False
            continue
        if dentro and cs and not set(cs[0]) <= set("-: ") and re.search(r"(?i)NO\s+GUARD", cs[-1]):
            out.append((f"causa {cs[0]}", "NO GUARD"))
    return out


def abiertos_postmortem(txt):
    """U-185: renglones WEAK / MISSING abiertos. Cerrado = 'OK ...' o 'conducta: <motivo de al menos 3 palabras>'."""
    ab = []
    for i, e in tabla_postmortem(txt):
        u = e.strip("* ")
        if re.match(r"(?i)OK\b", u):
            continue
        m = re.match(r"(?i)conducta\s*[:—–-]\s*(.+)", u)
        if m and len(m.group(1).split()) >= 3:
            continue
        ab.append((i, (re.match(r"(?i)(WEAK|MISSING)", u) or re.match(r"(\S*)", u)).group(1).upper() or "SIN ESTADO"))
    return ab


def _cierre_pt(iso):
    import datetime
    try:
        t = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        from zoneinfo import ZoneInfo
        return t.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    except Exception:
        return str(iso or "")[:10]


def _cierre_dt(iso):
    import datetime
    try:
        return datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except Exception:
        return None


RX_PM_HORA = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{1,2}:\d{2})(?::\d{2})?\s*(UTC|Z|PT|PST|PDT|[+-]\d{2}:?\d{2})?")


def _pm_hora(nombre, txt):
    """momento del post-mortem: fecha-hora escrita en sus primeras líneas ('2026-11-12 18:40 UTC' / PT); si no trae hora, el FIN del día
    de su nombre en California (un post-mortem de la mañana no puede cubrir un cierre de la tarde si dice su hora)."""
    import datetime
    from zoneinfo import ZoneInfo
    pt = ZoneInfo("America/Los_Angeles")
    m = RX_PM_HORA.search("\n".join(txt.splitlines()[:12]))
    if m:
        t = datetime.datetime.fromisoformat(f"{m.group(1)}T{int(m.group(2).split(':')[0]):02d}:{m.group(2).split(':')[1]}")
        z = (m.group(3) or "PT").upper()
        if z in ("UTC", "Z"):
            return t.replace(tzinfo=datetime.timezone.utc)
        if z in ("PT", "PST", "PDT"):
            return t.replace(tzinfo=pt)
        return datetime.datetime.fromisoformat(t.isoformat() + (z if ":" in z else z[:3] + ":" + z[3:]))
    d = RX_POSTMORTEM.match(nombre).group(1)
    return datetime.datetime.fromisoformat(d + "T23:59:59").replace(tzinfo=pt)


def revisar_postmortem(cache):
    """U-185 (COORDINACIÓN 12-nov) + post-mortem 2026-11-12b (WEAK U-185): el CIERRE es la última subida de la rev vigente del proyecto
    cerrado más reciente (fecha_iso de TODOS sus SUBIDA_OK*.json, hora completa; no primera_subida_iso, no por día). Se evalúa SOLO
    el post-mortem MÁS NUEVO (orden de nombre: 2026-11-12b > 2026-11-12) y tiene que ser posterior al cierre; con WEAK / MISSING
    abiertos = falta (un post-mortem limpio más viejo ya no lo tapa)."""
    import json
    if not cache or not os.path.isdir(cache):
        return []
    cierres = []
    for d in os.listdir(cache):
        dd = os.path.join(cache, d)
        if not os.path.isdir(dd):
            continue
        for n in os.listdir(dd):
            if not re.match(r"SUBIDA_OK.*\.json$", n):
                continue
            try:
                x = json.load(open(os.path.join(dd, n), encoding="utf-8"))
            except Exception:
                continue
            t = _cierre_dt(x.get("fecha_iso") or x.get("primera_subida_iso"))
            if t:
                cierres.append((t, d))
    if not cierres:
        return []
    cierre, proy = max(cierres)
    pms = sorted((RX_PM_PRINCIPAL.match(n).groups(), n) for n in os.listdir(cache) if RX_PM_PRINCIPAL.match(n))
    if not pms:
        return [f"{proy} cerrado {cierre.isoformat()} sin cache_proyectos/POSTMORTEM_COBERTURA_<fecha>[letra].md posterior (U-185)"]
    n = pms[-1][1]                                       # SOLO el principal más nuevo (un _VERIFICACION / _CIERRE no lo reemplaza)
    txt = open(os.path.join(cache, n), encoding="utf-8").read()
    if _pm_hora(n, txt) < cierre:
        return [f"{proy} cerrado {cierre.isoformat()}: el post-mortem más nuevo ({n}) es anterior al cierre (U-185)"]
    if not tabla_postmortem(txt):
        return [f"{n}: sin la tabla principal 'id | error / regla | chequeo | test | estado' (0 renglones) = falla (U-185)"]
    base = n[:-3] + "_"
    todos = sorted(m for m in os.listdir(cache) if m.startswith(base) and m.endswith(".md"))
    verifs = sorted((_pm_hora(n, open(os.path.join(cache, m), encoding="utf-8").read()), m) for m in todos if "_VERIFICACION" in m.upper())
    acomp = [m for m in todos if "_VERIFICACION" not in m.upper()] + ([verifs[-1][1]] if verifs else [])
    # manda el más estricto entre el principal, cada acompañante (_CIERRE / copias) y la verificación MÁS NUEVA (una verificación nueva
    # reemplaza a la anterior; un _CIERRE o una copia nunca relajan lo que el principal o la verificación dejan abierto)
    abiertos = {}                                        # manda el más estricto: abierto en el principal O en un acompañante
    for m in [n] + acomp:
        t = txt if m == n else open(os.path.join(cache, m), encoding="utf-8").read()
        for i, e in abiertos_postmortem(t) + causas_no_guard(t):
            abiertos.setdefault(i, (e, m))
    if not abiertos:
        return []
    ab = list(abiertos.items())
    nw = sum(1 for _i, (e, _m) in ab if e == "WEAK")
    nm = sum(1 for _i, (e, _m) in ab if e == "MISSING")
    ng = sum(1 for _i, (e, _m) in ab if e == "NO GUARD")
    return [f"{n}{' + ' + ', '.join(acomp) if acomp else ''}: {nw} WEAK / {nm} MISSING / {ng} NO GUARD abiertos ({len(ab)} renglones sin OK "
            "ni 'conducta: motivo'; manda el más estricto; U-185): " + ", ".join(i for i, _e in ab[:30])]


RX_DEF_TEST = re.compile(r"(?m)^def (test_\w+)\(")


def tests_sin_llamar(fuente):
    """post-mortem 2026-11-12b (BE-CR42 / BE-GK47): todo 'def test_…' de tools/test_*.py del candidato se LLAMA en su archivo (a nivel de
    módulo, en __main__ o en una lista / tupla de funciones); correr_suite ejecuta cada archivo como script, no con pytest.
    -> [archivo::test sin llamar]"""
    if fuente.zip:
        nombres = [n[len(fuente.base):] for n in fuente.zip.namelist() if n.startswith(fuente.base)]
    else:
        nombres = [os.path.relpath(os.path.join(r, f), fuente.base) for r, _d, fs in os.walk(fuente.base) for f in fs]
    out = []
    for rel in sorted(nombres):
        b = os.path.basename(rel)
        if not (rel.startswith("tools/") and b.startswith("test_") and b.endswith(".py")):
            continue
        s = fuente.leer(rel) or ""
        for t in RX_DEF_TEST.findall(s):
            resto = s.replace(f"def {t}(", "")
            if not re.search(rf"\b{t}\s*\(|[\[(,=]\s*{t}\b", resto):
                out.append(f"{b}::{t}")
    return out


RX_VERSION_SKILL = re.compile(r"\*\*VERSION:\s*(v(\d+)cf(\d+)[a-z]?)\*\*")


def revisar_prueba_abiertos(archivo, fuente=None, desde=(81, 119)):
    """NO GUARD 3.1 / BE-PM04 (+ verificación 12b): ANTES de publicar, la versión del CANDIDATO (línea **VERSION: vNcfM** de su SKILL.md;
    si no, la vigente del INDICE) desde v81cf119 tiene skills_archivo/PRUEBA_ABIERTOS_<v>.json con TODOS los proyectos de
    skills_archivo/PROYECTOS_ABIERTOS.json ({"proyectos": [nombres de cache_proyectos]}), cada uno con 0 regresiones sin explicar."""
    import json
    m = RX_VERSION_SKILL.search((fuente.leer("SKILL.md") or "") if fuente else "")
    if not m:
        p = os.path.join(archivo, "INDICE.md")
        if not os.path.isfile(p):
            return []
        m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v(\d+)cf(\d+)[a-z]?)", open(p, encoding="utf-8").read())
    if not m or (int(m.group(2)), int(m.group(3))) < desde:
        return []
    v = m.group(1)
    fa = os.path.join(archivo, "PROYECTOS_ABIERTOS.json")
    try:
        abiertos = list(json.load(open(fa, encoding="utf-8")).get("proyectos") or [])
    except Exception:
        return [f"sin skills_archivo/PROYECTOS_ABIERTOS.json legible (lista de proyectos abiertos que la versión {v} tiene que probar)"]
    f = os.path.join(archivo, f"PRUEBA_ABIERTOS_{v}.json")
    if not os.path.isfile(f):
        return [f"la versión {v} no tiene skills_archivo/PRUEBA_ABIERTOS_{v}.json (compuerta de la candidata sobre los proyectos "
                "abiertos antes de publicar)"]
    try:
        x = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        return [f"{os.path.basename(f)} ilegible: {e}"]
    out = []
    if x.get("version_candidata") not in (None, v):
        out.append(f"{os.path.basename(f)} es de la versión {x.get('version_candidata')}, no de {v}")
    pr = x.get("proyectos") or {}
    falt = [a for a in abiertos if a not in pr]
    if falt:
        out.append(f"{os.path.basename(f)}: faltan proyectos abiertos {', '.join(falt)} (PROYECTOS_ABIERTOS.json)")
    sin = [r for r in x.get("regresiones") or [] if not str(r.get("explicacion") or "").strip()]
    if sin or not x.get("ok"):
        out.append(f"{os.path.basename(f)}: {len(sin)} regresión(es) PASS -> FAIL sin explicación: "
                   + ", ".join(f"{r.get('proyecto')}:{r.get('chequeo')}" for r in sin[:10]))
    return out


def main(argv):
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    candidato, archivo = argv[1], argv[2]
    extra = argv[3:]
    tiene = ids_en_ruta(candidato)
    todas = set()
    for n in os.listdir(archivo):
        p = os.path.join(archivo, n)
        if n.endswith(".zip") or os.path.isdir(p):
            todas |= ids_en_ruta(p)
    for e in extra:
        todas |= ids_en_ruta(e)
    faltan = sorted(todas - tiene - IGNORAR)
    print(f"Reglas acumuladas: {len(todas)} · en el candidato: {len(tiene & todas)} · faltan: {len(faltan)}")
    malo = False
    if faltan:
        print("FALTAN:", " ".join(faltan))
        malo = True
    reg = revisar_registro(Fuente(candidato), AQUI, extra[0] if extra else None)
    zp = revisar_zip(candidato)
    ix = revisar_indice(archivo)
    sk = revisar_skill(Fuente(candidato))
    bc = revisar_banco(archivo)
    od = revisar_ordenes(extra[0] if extra else None)
    vu = revisar_versiones_unicas(archivo)
    pm = revisar_postmortem(extra[0] if extra else None)
    tl = tests_sin_llamar(Fuente(candidato))
    pa = revisar_prueba_abiertos(archivo, Fuente(candidato))
    for nombre, xs in (("REGISTRO (BE-121)", reg), ("ZIP (U-020)", zp), ("INDICE (U-027)", ix), ("SKILL (BE-87 / BE-VS-11)", sk),
                       ("BANCO (U-043)", bc), ("ORDENES (U-136)", od), ("VERSIONES (BE-144)", vu),
                       ("POSTMORTEM (U-185)", pm), ("TESTS SIN LLAMAR (BE-CR42)", tl), ("PRUEBA ABIERTOS (NO GUARD 3.1)", pa)):
        if xs:
            malo = True
            print(f"{nombre}: {len(xs)} falta(s)")
            for x in xs[:40]:
                print("  - " + x)
    if malo:
        return 1
    print("OK: el skill contiene todas las reglas acumuladas y cada regla 'programa' tiene chequeo + test.")
    return 0


def selftest():
    sys.path.insert(0, AQUI)
    import test_verificar_version as T
    T.correr()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
