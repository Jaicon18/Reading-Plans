# -*- coding: utf-8 -*-
"""bitacora.py -- 4a compuerta: ninguna entrega sin las tools obligatorias corridas.

Origen (15-oct-2026): en las pruebas el take-off a veces NO corria closer/planmark/verif_*
y el registro se creaba tarde. Una regla escrita se salta; esta compuerta no.

Uso:
  python3 bitacora.py run <tool.py> [args...]     corre la tool y la anota (rc, hashes)
  python3 bitacora.py backcheck <informe.md> <excel.xlsx>   anota el back-check hecho
  python3 bitacora.py compuerta <takeoff.json> <registro.json> <excel.xlsx>
  python3 bitacora.py ver                          lista la bitacora

La bitacora vive en $BITACORA o ./bitacora.jsonl. Cada renglon lleva el hash del anterior:
editarla a mano rompe la cadena y la compuerta lo rechaza.
Toda tool se corre SIEMPRE por `bitacora.py run`; una tool corrida por fuera no cuenta.

v67 (17-oct-2026): la compuerta EXIGE ademas
  - plantilla_excel.py armar corrido con --familias familias_out.json (accesorios + partition types de canon.py);
  - el Excel final con las 15 familias de accesorios en Material Summary y la hoja Partition Takeoff con la
    convencion de types (plantilla_excel.verificar_excel: bloques TYPE, nombres EXT-6CFMF / EXT-PARAPET /
    BULKHEAD-<tag> / CANOPY-COL / OTHER FRAMING, TOTAL fuera de la columna A);
  - contar_tags.py, vigas_sobre_walls.py y test_ciego.py (E24) con rc=0.
v72b (reglas inviolables): la compuerta corre reglas.py compuerta EN PROCESO en modo final (carpeta de trabajo
  con takeoff_canon.json, el Excel con el sello de reglas vigente) y exige además una corrida de
  `reglas.py compuerta` anotada en la bitácora con rc 0. Sin carpeta de trabajo: NO ENTREGABLE. No hay override.
v68 (arbitraje #16): la misma llamada a plantilla_excel.verificar_excel exige además compra y presentación:
  toda cita "Inputs!Bn" existe; Pieces = ROUNDUP(Purchase / stock) (desperdicio una vez); FRT plywood un renglón
  por material y espesor; sealant exterior aparte del acoustical y en tubes; hanger wire LF en continuous coil;
  yields con fórmula viva a su celda de Inputs; Pending Items sin duplicados ni delta vacío; Excel íntegro en
  inglés (hojas Review Items / Scope Checklist, estados CONFIRMED / DERIVED / PENDING).
v78 (W3, R78.24): la compuerta exige además el PDF de MARKUPS Bluebeam (markups_bluebeam.py): resumen JSON con el sha
  del canon vigente y markups_bluebeam.verificar(pdf, canon) sin fallas. Sin PDF de markups verificado: NO ENTREGABLE.
"""
import ast
import hashlib, json, os, re, subprocess, sys, time

# v77 (R76.7 d): la bitácora y las rutas se resuelven con realpath (un symlink al mismo archivo es el mismo archivo)
BIT = os.path.realpath(os.environ.get("BITACORA") or "bitacora.jsonl")


def _ruta(p):
    return os.path.realpath(p)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leer():
    if not os.path.exists(BIT):
        return []
    return [json.loads(l) for l in open(BIT, encoding="utf-8") if l.strip()]


def _hash_renglon(r):
    return hashlib.sha256(json.dumps(r, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def anotar(reg):
    """v77 (R76.7 d): lock exclusivo (fcntl) entre leer el último renglón y escribir: dos tools que anotan a la vez
    (subagentes en paralelo) ya no rompen la cadena de hashes."""
    import fcntl
    with open(BIT + ".lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            prev = leer()
            reg["prev"] = _hash_renglon(prev[-1]) if prev else "0"
            reg["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            with open(BIT, "a", encoding="utf-8") as f:
                f.write(json.dumps(reg, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)


# librerias sin linea de comandos: cuentan cuando las IMPORTA el script que se corrio
LIBRERIAS = ("closer", "planmark")


def usa(tool):
    """Librerías (closer, planmark) que la tool IMPORTA de verdad. v66 (#15A): se lee el AST — un import escrito
    dentro de un comentario o de un string (ej. este mismo archivo) ya no cuenta; bitacora.py nunca 'usa' nada
    (correr `bitacora.py run bitacora.py compuerta` anotaba usa=closer y la compuerta se rechazaba a sí misma)."""
    if os.path.basename(tool) == "bitacora.py":
        return []
    try:
        src = open(tool, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    try:
        arbol = ast.parse(src)
    except SyntaxError:
        arbol = None
    out = []
    for m in LIBRERIAS:
        if arbol is None:
            # v61 (arbitraje #11): 'x = 1; import closer', 'import os, closer as c', __import__ / import_module
            stmt = r"(?:^|;)\s*(?:import\s+(?:[\w.]+(?:\s+as\s+\w+)?\s*,\s*)*%s\b|from\s+%s\s+import\b|from\s+[\w.]+\s+import\s+\(?\s*(?:\w+(?:\s+as\s+\w+)?\s*,\s*)*%s\b)" % (m, m, m)
            dyn = r"(?:__import__|import_module)\(\s*['\"]%s['\"]" % m
            if re.search(stmt, src, re.M) or re.search(dyn, src):
                out.append(m)
            continue
        for n in ast.walk(arbol):
            hit = (isinstance(n, ast.Import) and any(a.name.split(".")[0] == m for a in n.names)) or \
                  (isinstance(n, ast.ImportFrom) and ((n.module or "").split(".")[0] == m
                                                      or any(a.name == m for a in n.names))) or \
                  (isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", "")) in
                   ("__import__", "import_module") and n.args and isinstance(n.args[0], ast.Constant)
                   and n.args[0].value == m)
            if hit:
                out.append(m)
                break
    return out


def run(tool, args):
    """v63 (#13A/#13B): la tool escribe a un log y la bitacora lo muestra despues. Antes, `bitacora.py run X | head`
    cerraba el pipe: la tool moria por SIGPIPE a mitad (rc != 0 o salida truncada) y la corrida quedaba mal anotada."""
    logdir = os.path.join(os.path.dirname(BIT), "bitacora_logs")
    os.makedirs(logdir, exist_ok=True)
    log = os.path.join(logdir, "%s_%s.log" % (os.path.basename(tool), time.strftime("%Y%m%dT%H%M%S")))
    with open(log, "w", encoding="utf-8") as fo:
        p = subprocess.run([sys.executable, tool] + args, stdout=fo, stderr=subprocess.STDOUT)
    hashes = {_ruta(a): sha(a) for a in args if os.path.isfile(a)}
    anotar({"tool": os.path.basename(tool), "args": args, "rc": p.returncode, "hashes": hashes,
            "usa": usa(tool), "log": log})
    try:
        sys.stdout.write(open(log, encoding="utf-8", errors="replace").read())
        sys.stdout.write("[bitacora] rc=%d log=%s\n" % (p.returncode, log))
        sys.stdout.flush()
    except BrokenPipeError:                    # `| head`: la tool ya termino y quedo anotada; solo se corta la vista
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
    return p.returncode


def cadena_ok(rows):
    for i, r in enumerate(rows):
        want = _hash_renglon(rows[i - 1]) if i else "0"
        if r.get("prev") != want:
            return i + 1
    return 0


def _vigente(r, path):
    """v77: busca por realpath (y por abspath, renglones viejos); un symlink apunta al mismo archivo."""
    p = _ruta(path)
    if not os.path.isfile(p):
        return False
    h = sha(p)
    return h in (r["hashes"].get(p), r["hashes"].get(os.path.abspath(path))) or \
        any(_ruta(k) == p and v == h for k, v in r["hashes"].items())


# (tool, subcomando o None, archivos que deben estar VIGENTES en esa corrida, descripcion)
OBLIGATORIAS = [
    ("arranque.py", None, (), "Paso 0 mecanico"),
    ("alcances.py", "escanear", (), "lista fija de alcances (52.1)"),
    ("registro.py", "crear", (), "registro antes del primer numero (56.1)"),
    ("usa:closer", None, (), "cantidades selladas por closer.py (un numero sin sello no se entrega)"),
    ("usa:planmark", None, (), "evidencia visual circulada con planmark.py"),
    ("inventario.py", None, (), "inventario cerrado de walls contra la planta: bandas, solapes, apilados, MR, purlin, zonas (v63)"),
    ("canon.py", None, (), "TODAS las familias con tool desde takeoff_canon.json (PROTOCOLO v61 P9: studs_nodos, board_caras, corridas, headers)"),
    ("contar_tags.py", None, (), "fixtures contadas por tag en la hoja E (v65; v66 normaliza sufijo ',x')"),
    ("vigas_sobre_walls.py", None, (), "walls bajo viga del plan S* (v66, E26): stops_under_beam o motivo"),
    ("framed_openings.py", None, (), "framed openings MEP deterministas (PROTOCOLO v61 P10)"),
    ("alcance_filtro.py", None, (), "filtro de alcance / cladding EXCLUDED (PROTOCOLO v61 P10, 60.4)"),
    # v76 (arbitraje #24): test_ciego.py viaja en el paquete ciego; también vale test_ciego_tools.py (cualquiera de
    # los dos con rc 0). Antes el ciego no lo traía y la compuerta nunca daba OK en una prueba.
    ("test_ciego.py|test_ciego_tools.py", None, (), "protocolo ciego E24: skill y tools sin valores de examen (v67)"),
    ("plantilla_excel.py", "validar", ("takeoff",), "formato del takeoff.json (52.4)"),
    ("plantilla_excel.py", "armar", ("takeoff", "excel"), "Excel armado del takeoff.json vigente"),
    ("registro.py", "entregable", ("registro",), "0 renglones pendientes (50.5)"),
    ("alcances.py", "compuerta", ("registro", "excel"), "ALCANCES OK contra el Excel final"),
    ("reglas.py", "compuerta", (), "v72b: reglas inviolables (reglas.py compuerta <work_dir> --excel <final>)"),
]


def carpeta_trabajo(takeoff, excel):
    """v72b: la carpeta con 4_canon/takeoff_canon.json (o takeoff_canon.json) de esta entrega."""
    import reglas
    cands = []
    for base in (os.environ.get("TAKEOFF_WORK"), os.path.dirname(os.path.abspath(takeoff)),
                 os.path.dirname(os.path.abspath(excel))):
        if base:
            cands += [base, os.path.join(base, "etapas"), os.path.join(base, ".."), os.path.join(base, "..", "etapas")]
    for c in cands:
        if os.path.isdir(c) and reglas.buscar_canon(c):
            return os.path.abspath(c)
    return None


def compuerta(takeoff, registro, excel, _desde_reglas=False):
    """v72b: además corre reglas.py compuerta en modo final (con el Excel: sello vigente + verificar_excel) sobre la
    carpeta de trabajo. `_desde_reglas` = llamada interna de reglas.py (evita la vuelta)."""
    fallas_r = []
    if not _desde_reglas:
        import reglas
        w = carpeta_trabajo(takeoff, excel)
        if w is None:
            fallas_r.append("REGLAS: no encuentro la carpeta de trabajo con takeoff_canon.json ($TAKEOFF_WORK o junto "
                            "al takeoff.json): reglas.py compuerta no se puede correr -> NO ENTREGABLE")
        else:
            out = reglas.compuerta(w, excel=excel)
            try:
                reglas.escribir(out, w)
            except OSError:
                pass
            if not out["ok"]:
                fallas_r.append("REGLAS: %d falla(s) de reglas inviolables (ver %s)"
                                % (out["n_fallas"], os.path.join(w, "REGLAS_FALLAS.md")))
                fallas_r += ["REGLAS: %s | %s | %s" % (x["regla"], x["elemento"], x["valor"]) for x in out["fallas"][:30]]
            fallas_r += markups_fallas(w, takeoff, excel)
    return fallas_r + _compuerta(takeoff, registro, excel, _desde_reglas)


def markups_fallas(w, takeoff, excel):
    """v78 (R78.24, W3): el PDF de markups Bluebeam (markups_bluebeam.py) es entregable FIJO. Exige su resumen JSON
    con el sha del canon VIGENTE y markups_bluebeam.verificar(pdf, canon) == []. Sin él: NO ENTREGABLE."""
    import reglas
    import markups_bluebeam as MB
    canon_p = reglas.buscar_canon(w)
    if not canon_p:
        return ["MARKUPS: sin takeoff_canon.json en %s: no se puede verificar el PDF de markups -> NO ENTREGABLE" % w]
    cd = os.path.dirname(canon_p)
    dirs = [w, os.path.join(w, "out"), os.path.join(w, "4_canon"), cd, os.path.join(cd, "out"),
            os.path.join(cd, "..", "out"), os.path.dirname(os.path.abspath(excel)),
            os.path.dirname(os.path.abspath(takeoff)), os.environ.get("TAKEOFF_OUT")]
    return ["MARKUPS: " + f for f in MB.compuerta(canon_p, dirs)]


def _compuerta(takeoff, registro, excel, _desde_reglas=False):
    rows = leer()
    fallas = []
    if not rows:
        return ["no hay bitacora en %s: ninguna tool se corrio por bitacora.py run" % BIT]
    roto = cadena_ok(rows)
    if roto:
        return ["bitacora editada a mano: cadena rota en el renglon %d" % roto]
    files = {"takeoff": takeoff, "registro": registro, "excel": excel}
    for f in files.values():
        if not os.path.isfile(f):
            fallas.append("no existe %s" % f)
    if fallas:
        return fallas
    idx = {}
    for tool, sub, vig, desc in OBLIGATORIAS:
        if _desde_reglas and tool == "reglas.py":
            continue
        if tool.startswith("usa:"):
            cand = [(i, r) for i, r in enumerate(rows) if tool[4:] in r.get("usa", [])]
        else:
            cand = [(i, r) for i, r in enumerate(rows) if r.get("tool") in tool.split("|")
                    and (sub is None or (r["args"][:1] == [sub]))]
        if not cand:
            fallas.append("NUNCA SE CORRIO %s %s -- %s" % (
                ("un script que importa " + tool[4:] + ".py") if tool.startswith("usa:") else tool,
                sub or "", desc))
            continue
        ult_i, ult = cand[-1]
        if ult["rc"] != 0:
            fallas.append("%s %s: su ultima corrida salio rc=%d" % (tool, sub or "", ult["rc"]))
            continue
        for k in vig:
            if not _vigente(ult, files[k]):
                fallas.append("%s %s: se corrio sobre otra version de %s (cambio despues)"
                              % (tool, sub or "", os.path.basename(files[k])))
        idx[(tool, sub)] = ult_i
    # v67: Excel con accesorios + convencion de partition types, armado desde familias_out.json
    if ("plantilla_excel.py", "armar") in idx and "--familias" not in rows[idx[("plantilla_excel.py", "armar")]]["args"]:
        fallas.append("plantilla_excel.py armar sin --familias familias_out.json: las familias de accesorios y la "
                      "hoja Partition Takeoff salen de canon.py v67 (v67)")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import plantilla_excel
        fallas += ["EXCEL: " + e for e in plantilla_excel.verificar_excel(excel)]
    except ImportError as e:
        fallas.append("no se pudo verificar el Excel (plantilla_excel.py): %s" % e)
    # el registro se crea ANTES del primer numero
    crear = [i for i, r in enumerate(rows) if r.get("tool") == "registro.py" and r["args"][:1] == ["crear"]]
    armar = [i for i, r in enumerate(rows) if r.get("tool") == "plantilla_excel.py" and r["args"][:1] == ["armar"]]
    if crear and armar and min(crear) > min(armar):
        fallas.append("registro.py crear corrio DESPUES del primer Excel (regla 56.1)")
    bc = [r for r in rows if r.get("tool") == "BACKCHECK"]
    if not bc:
        fallas.append("NO HAY BACK-CHECK anotado (bitacora.py backcheck <informe> <excel>)")
    elif not _vigente(bc[-1], excel):
        fallas.append("el back-check se hizo sobre otra version del Excel")
    elif not _vigente(bc[-1], bc[-1]["args"][0]):
        fallas.append("el informe del back-check cambio o desaparecio despues de anotarlo")
    return fallas


def backcheck(informe, excel):
    if not os.path.isfile(informe) or os.path.getsize(informe) < 200:
        sys.exit("BACKCHECK RECHAZADO: el informe no existe o esta vacio (<200 bytes)")
    if not os.path.isfile(excel):
        sys.exit("BACKCHECK RECHAZADO: no existe el Excel " + excel)
    anotar({"tool": "BACKCHECK", "args": [informe, excel], "rc": 0,
            "hashes": {_ruta(informe): sha(informe), _ruta(excel): sha(excel)}})
    print("OK back-check anotado")


def bit_fuera_de_tools():
    """v80 (R80.5): la bitácora es de la CORRIDA, no del paquete. Sin $BITACORA, ./bitacora.jsonl dentro de la carpeta
    de las tools (o debajo de ella) = error: la corrida quedaba sin bitácora en su carpeta de trabajo y la compuerta
    leía la de otra corrida. Devuelve el motivo o None."""
    tools = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    if os.path.commonpath([tools, BIT]) == tools:
        return ("bitácora dentro de la carpeta de las tools (%s): definir BITACORA=<carpeta de trabajo>/bitacora.jsonl "
                "o correr desde la carpeta de trabajo (R80.5)" % BIT)
    return None


def main():
    a = sys.argv[1:]
    if a and a[0] in ("run", "backcheck", "compuerta"):
        m = bit_fuera_de_tools()
        if m:
            print("ERROR bitacora.py:", m, file=sys.stderr)
            sys.exit(2)
    if len(a) >= 2 and a[0] == "run":
        sys.exit(run(a[1], a[2:]))
    elif len(a) == 3 and a[0] == "backcheck":
        backcheck(a[1], a[2])
    elif len(a) == 4 and a[0] == "compuerta":
        f = compuerta(a[1], a[2], a[3])
        for x in f:
            print("FALLA ", x)
        if f:
            print("NO ENTREGABLE: %d fallas de bitacora" % len(f))
            sys.exit(1)
        print("BITACORA OK: %d tools obligatorias vigentes + back-check" % len(OBLIGATORIAS))
    elif a == ["ver"]:
        for r in leer():
            print(r["ts"], r["rc"], r["tool"], " ".join(r["args"])[:90])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
