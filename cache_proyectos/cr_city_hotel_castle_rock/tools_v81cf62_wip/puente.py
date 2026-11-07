#!/usr/bin/env python3
"""puente.py — R80e.159: buzón _PUENTE_CLAUDE entre Claude Code y Claude en Chrome (Drive › JC HUNTER PROJECTS › _PUENTE_CLAUDE).
Solo AGREGA archivos nuevos (gdrive_fetch put rechaza nombres existentes): nunca borra ni sobrescribe -> no se pierde nada.

  python3 puente.py estado [--json out.json]        lee TODOS los archivos de la carpeta: COD abiertos, preguntas sin respuesta,
                                                    EN CURSO sin TERMINADO, inconsistencias. Correr al INICIAR y al TERMINAR.
  python3 puente.py bitacora "<proyecto>" "<msg>"   nueva línea en BITACORA_<AAAA-MM-DD_HHMM>_code.md
  python3 puente.py abrir "<proyecto>" "<edición + N/HOJA>" "<sección>" "<para qué: row/RFI/N/HOJA>" "<alternativas y delta>"
                                                    crea CODIGO_PENDIENTE_COD-###.md + línea "EN CURSO [COD-###]" -> luego
                                                    REACTIVAR y DISPARAR la tarea del buzón (update_trigger enabled=true +
                                                    fire_trigger) para que el aviso llegue YA al celular del usuario.
  python3 puente.py pregunta "<proyecto>" "<pregunta>"   "PREGUNTA [Q-###]" (el buzón se la avisa al usuario)
  python3 puente.py respuesta "<proyecto>" Q-### "<respuesta del usuario>"
  python3 puente.py terminado "<proyecto>" "<clave>"     cierra "EN CURSO [clave]" (o el texto libre, p. ej. rev5)
  python3 puente.py pendientes                       lista ~/.puente_salida sin '.subido' (crear con Google Drive create_file y
                                                    luego: python3 puente.py hecho <nombre>)
  python3 puente.py --selftest
Convenciones (las mismas del buzón de Chrome): CODIGO_VERIFICADO_COD-###.md o '## COD-###' en CODIGO_VERIFICADO.md = respondido."""
import json, os, re, subprocess, sys, tempfile, datetime
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Los_Angeles")
except Exception:  # pragma: no cover
    TZ = None

FOLDER = "1iMhLoh4WDBARekFUatCqA2YUWI0DMKCf"
TRIGGER = "trig_01H86QExcTotU3k5rovLP6R6"
GD = "/opt/takeoff/gdrive_fetch.py"
RX_COD = re.compile(r"COD-(\d{3})")
RX_HEAD = re.compile(r"^#+\s*COD-(\d{3})\s*\|\s*(ABIERTO|CERRADO)", re.M)
RX_LINE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| ([^|]+)\| ([^|]+)\| (.*)$", re.M)


def ahora():
    d = datetime.datetime.now(TZ) if TZ else datetime.datetime.now()
    return d.strftime("%Y-%m-%d %H:%M"), d.strftime("%Y-%m-%d_%H%M")


def gd(*a):
    r = subprocess.run([sys.executable, "-I", GD, *a], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"gdrive_fetch {a[0]} falló: {r.stderr.strip()[-300:]}")
    return r.stdout


def leer_carpeta():
    files = [json.loads(l) for l in gd("list", FOLDER).splitlines() if l.strip().startswith("{")]
    tmp = tempfile.mkdtemp(prefix="puente_")
    out = {}
    for f in files:
        if not f["name"].endswith(".md"):
            continue
        p = os.path.join(tmp, f["name"])
        gd("get", f["id"], p)
        out[f["name"]] = open(p, encoding="utf-8", errors="replace").read()
    return out


def analizar(docs):
    pend, cerr, verif = {}, set(), set()
    for n, t in docs.items():
        if n.startswith("CODIGO_PENDIENTE"):
            for num, est in RX_HEAD.findall(t):
                (cerr.add(num) if est == "CERRADO" else pend.setdefault(num, n))
        if n.startswith("CODIGO_VERIFICADO"):
            m = re.match(r"CODIGO_VERIFICADO_COD-(\d{3})", n)
            if m:
                verif.add(m.group(1))
            verif.update(re.findall(r"^#+\s*COD-(\d{3})", t, re.M))
    lineas = []
    for n, t in docs.items():
        if n.startswith("BITACORA"):
            lineas += [(ts, q.strip(), p.strip(), msg.strip(), n) for ts, q, p, msg in RX_LINE.findall(t)]
    lineas.sort()
    abiertos = sorted(c for c in pend if c not in verif and c not in cerr)
    cerrado_sin_resp = sorted(c for c in cerr if c not in verif)
    en_curso = []
    for ts, q, p, msg, n in lineas:
        if msg.startswith("EN CURSO"):
            k = re.search(r"\[([^\]]+)\]", msg)
            clave = k.group(1) if k else None
            hecho = any(t2 >= ts and m2.startswith("TERMINADO") and p2 == p and (clave is None or clave in m2 or
                        (clave.startswith("COD-") and clave[4:] in verif)) for t2, _, p2, m2, _ in lineas)
            if not hecho:
                en_curso.append({"ts": ts, "proyecto": p, "msg": msg[:200], "archivo": n})
    preg = {}
    for ts, q, p, msg, n in lineas:
        m = re.match(r"PREGUNTA \[(Q-\d{3})\]", msg)
        if m:
            preg[m.group(1)] = {"ts": ts, "proyecto": p, "msg": msg[:300]}
    for ts, q, p, msg, n in lineas:
        m = re.match(r"RESPUESTA \[(Q-\d{3})\]", msg)
        if m:
            preg.pop(m.group(1), None)
    nums = [int(x) for t in docs.values() for x in RX_COD.findall(t)]
    qs = [int(x) for t in docs.values() for x in re.findall(r"Q-(\d{3})", t)]
    return {"cod_abiertos": [{"cod": f"COD-{c}", "archivo": pend[c]} for c in abiertos],
            "cerrado_sin_respuesta": [f"COD-{c}" for c in cerrado_sin_resp],
            "en_curso_sin_terminado": en_curso, "preguntas_sin_respuesta": [{"q": k, **v} for k, v in preg.items()],
            "siguiente_cod": f"COD-{(max(nums) if nums else 0) + 1:03d}", "siguiente_q": f"Q-{(max(qs) if qs else 0) + 1:03d}",
            "archivos": sorted(docs)}


SALIDA = os.path.expanduser("~/.puente_salida")


def subir(nombre, texto):
    """Cuenta de servicio (gdrive_fetch put) primero. _PUENTE_CLAUDE vive en Mi unidad del usuario y la cuenta de
    servicio NO tiene cuota ahí (HTTP 403 'storage quota'): entonces el archivo queda en ~/.puente_salida y el modelo
    lo crea EN EL MISMO TURNO con el conector Google Drive create_file (cuenta del usuario), title=<nombre>,
    parentId=FOLDER, contentMimeType text/markdown, disableConversionToGoogleType=true. Nunca se pierde: queda local."""
    os.makedirs(SALIDA, exist_ok=True)
    p = os.path.join(SALIDA, nombre)
    open(p, "w", encoding="utf-8").write(texto)
    r = subprocess.run([sys.executable, "-I", GD, "put", p, FOLDER], capture_output=True, text=True)
    if r.returncode == 0 and "fail" not in (r.stdout + r.stderr).lower():
        print(r.stdout.strip()); os.rename(p, p + ".subido")
        return
    print(f"CREAR_CON_MCP title={nombre} parentId={FOLDER} archivo={p}")


def linea(proyecto, msg):
    ts, tsf = ahora()
    subir(f"BITACORA_{tsf}_code.md", f"{ts} | Claude Code | {proyecto} | {msg}\n")


def aviso_trigger():
    print(f"\n>>> AHORA: update_trigger {TRIGGER} enabled=true  +  fire_trigger {TRIGGER}"
          " (el buzón avisa al celular del usuario: 'abre la sesión Verificador de código (This computer) y escribe: revisa el buzón').")


def selftest():
    docs = {"CODIGO_PENDIENTE.md": "## COD-001 | CERRADO 2026-11-06 21:55 | x\n## COD-002 | ABIERTO | y\n",
            "CODIGO_PENDIENTE_COD-003.md": "## COD-003 | ABIERTO | z\n",
            "CODIGO_VERIFICADO.md": "## COD-001 | p\n", "CODIGO_VERIFICADO_COD-003.md": "ok",
            "BITACORA.md": "2026-11-06 22:09 | Claude Chrome | CR | EN CURSO: rev5 del take-off\n"
                           "2026-11-06 22:10 | Claude Code | CR | EN CURSO [COD-003] abierto\n"
                           "2026-11-06 22:11 | Claude Code | CR | PREGUNTA [Q-001] ¿altura?\n",
            "BITACORA_x_code.md": "2026-11-06 23:00 | Claude Code | CR | TERMINADO rev5\n"}
    r = analizar(docs)
    assert [x["cod"] for x in r["cod_abiertos"]] == ["COD-002"], r
    assert r["en_curso_sin_terminado"] == [] and r["siguiente_cod"] == "COD-004", r
    assert [x["q"] for x in r["preguntas_sin_respuesta"]] == ["Q-001"], r
    docs["BITACORA_y_code.md"] = "2026-11-06 23:05 | Claude Code | CR | RESPUESTA [Q-001] 9 ft\n"
    assert analizar(docs)["preguntas_sin_respuesta"] == []
    print("puente selftest OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        selftest(); sys.exit(0)
    cmd = a[0]
    if cmd == "estado":
        r = analizar(leer_carpeta())
        print(json.dumps({k: v for k, v in r.items() if k != "archivos"}, ensure_ascii=False, indent=1))
        if "--json" in a:
            json.dump(r, open(a[a.index("--json") + 1], "w"), ensure_ascii=False, indent=1)
        if r["cod_abiertos"] or r["preguntas_sin_respuesta"] or r["en_curso_sin_terminado"]:
            print(f"\nBuzón debe estar ACTIVO ({TRIGGER}).")
    elif cmd == "bitacora":
        linea(a[1], a[2])
    elif cmd == "abrir":
        proyecto, edicion, seccion, para, alts = a[1:6]
        cod = analizar(leer_carpeta())["siguiente_cod"]
        ts, _ = ahora()
        subir(f"CODIGO_PENDIENTE_{cod}.md", f"## {cod} | ABIERTO | {ts}\n- Proyecto: {proyecto}\n- Edicion del codigo: {edicion}\n"
              f"- Seccion o tema: {seccion}\n- Para que: {para}\n- Alternativas en juego y delta de cada una: {alts}\n"
              f"- Mientras no haya respuesta: CODE: [PENDIENTE verificar - {cod}]; el base lleva la opcion de mayor cantidad (R80e.38-4).\n")
        linea(proyecto, f"EN CURSO [{cod}] {seccion} — esperando verificación en ICC (Claude en Chrome)")
        print(cod); aviso_trigger()
    elif cmd == "pregunta":
        q = analizar(leer_carpeta())["siguiente_q"]
        linea(a[1], f"PREGUNTA [{q}] {a[2]}"); print(q); aviso_trigger()
    elif cmd == "respuesta":
        linea(a[1], f"RESPUESTA [{a[2]}] {a[3]}")
    elif cmd == "terminado":
        linea(a[1], f"TERMINADO [{a[2]}] {a[3] if len(a) > 3 else ''}".strip())
    elif cmd == "pendientes":
        for n in sorted(os.listdir(SALIDA)) if os.path.isdir(SALIDA) else []:
            if not n.endswith(".subido"):
                print(os.path.join(SALIDA, n))
    elif cmd == "hecho":
        os.rename(os.path.join(SALIDA, a[1]), os.path.join(SALIDA, a[1] + ".subido"))
    else:
        sys.exit(__doc__)
