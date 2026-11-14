#!/usr/bin/env python3
"""UserPromptSubmit (U-136): guarda cada mensaje del usuario en la bandeja central
cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl para convertirlo en regla. Nunca bloquea.
BE-COORD03 (14-nov): la bandeja dejó de recibir órdenes desde el 11-nov porque (a) COORDINACIÓN trabaja en otra rama sin este hook y
(b) las sesiones escribían la línea en local y nunca la subían. Ahora la línea se PUBLICA en la rama de la bandeja
(claude/gifted-pasteur-x2sfzs) desde un clon propio en caché (fetch + append + commit + push, con reintentos y tope de tiempo);
si la publicación falla, la línea queda en local y en ~/.cache/u136_pendientes.jsonl y se reintenta en el próximo mensaje."""
import hashlib, json, os, re, sys, datetime, subprocess
SECRETO = re.compile(r"(password|passwd|contraseñ|api[_-]?key|secret|token\s*[:=]|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,})", re.I)
# BE-143: los avisos automáticos (tareas en segundo plano, subagentes, mensajes de otras sesiones,
# tareas programadas) llegan como prompt pero NO son mensajes del usuario: no se guardan.
AUTOMATICO = re.compile(r"^\s*(<task-notification|<agent-message|<cross-session-message|<system-reminder|<wake\b|<webhook-payload|<child-session-event|<event source=|\[SYSTEM NOTIFICATION"
                        r"|This session's worker process was restarted"          # v132 (COORDINACIÓN 13-nov, id 3b88645a6b4d): aviso del sistema
                        r"|This session is being continued from a previous conversation"   # resumen automático al compactar
                        r"|Stop hook feedback)", re.I)
RAMA_BANDEJA = os.environ.get("U136_RAMA", "claude/gifted-pasteur-x2sfzs")
REL = os.path.join("cache_proyectos", "ORDENES_CRUDAS", "_entrantes.jsonl")
CACHE = os.environ.get("U136_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "u136_bandeja")
PEND = os.environ.get("U136_PENDIENTES") or os.path.join(os.path.expanduser("~"), ".cache", "u136_pendientes.jsonl")


def es_del_usuario(texto):
    return bool(texto) and not AUTOMATICO.search(texto) and not SECRETO.search(texto)


def _git(args, cwd, t=20):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=t)


def publicar(lineas, raiz):
    """BE-COORD03: agrega las líneas (sin repetir id) a _entrantes.jsonl de la rama de la bandeja y hace push. -> True si quedó en el remoto."""
    url = os.environ.get("U136_ORIGIN") or (_git(["remote", "get-url", "origin"], raiz).stdout.strip() if os.path.isdir(os.path.join(raiz, ".git")) else "")
    if not url:
        return False
    if not os.path.isdir(os.path.join(CACHE, ".git")):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        if _git(["clone", "-q", "--depth", "20", "--branch", RAMA_BANDEJA, url, CACHE], os.path.dirname(CACHE), 60).returncode:
            return False
    for _ in range(3):
        _git(["fetch", "-q", "--depth", "20", "origin", RAMA_BANDEJA], CACHE, 40)
        _git(["reset", "-q", "--hard", f"origin/{RAMA_BANDEJA}"], CACHE)
        p = os.path.join(CACHE, REL)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        ya = open(p, encoding="utf-8").read() if os.path.isfile(p) else ""
        nuevas = [l for l in lineas if json.loads(l)["id"] not in ya]
        if not nuevas:
            return True
        with open(p, "a", encoding="utf-8") as f:
            f.writelines(l + "\n" for l in nuevas)
        _git(["add", REL], CACHE)
        if _git(["-c", "user.name=U-136 hook", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m",
                 f"U-136 bandeja: {len(nuevas)} mensaje(s) del usuario ({', '.join(json.loads(l)['id'] for l in nuevas)})"], CACHE).returncode:
            return False
        if _git(["push", "-q", "origin", f"HEAD:{RAMA_BANDEJA}"], CACHE, 40).returncode == 0:
            return True
    return False


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0
    texto = (d.get("prompt") or "").strip()
    if not es_del_usuario(texto):
        return 0
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or "."
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    sid = d.get("session_id", "")
    rid = hashlib.sha1(f"{sid}|{ts}|{texto}".encode()).hexdigest()[:12]
    linea = json.dumps({"id": rid, "ts_utc": ts, "session": sid, "texto": texto}, ensure_ascii=False)
    try:
        pend = [l.strip() for l in open(PEND, encoding="utf-8") if l.strip()] if os.path.isfile(PEND) else []
    except OSError:
        pend = []
    ok = False
    try:
        ok = publicar(pend + [linea], raiz)
    except Exception:                                   # noqa: BLE001 — el hook nunca bloquea
        ok = False
    try:
        if ok:
            if os.path.isfile(PEND):
                os.remove(PEND)
        else:
            os.makedirs(os.path.dirname(PEND), exist_ok=True)
            with open(PEND, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
            carpeta = os.path.join(raiz, "cache_proyectos", "ORDENES_CRUDAS")
            os.makedirs(carpeta, exist_ok=True)
            with open(os.path.join(carpeta, "_entrantes.jsonl"), "a", encoding="utf-8") as f:
                f.write(linea + "\n")
    except OSError:
        pass
    print(("U-136: mensaje del usuario publicado en la bandeja (" + RAMA_BANDEJA + ": " + REL + ")"
           if ok else "U-136: la bandeja no se pudo publicar ahora; quedó en local y se reintenta en el próximo mensaje") +
          "; si es una orden, regístrala en REGLAS_USUARIO_CLAUDE.md + ORDENES_DEL_USUARIO.md + MAPA_ORDENES.json en este turno.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
