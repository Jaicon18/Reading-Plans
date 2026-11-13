#!/usr/bin/env python3
"""UserPromptSubmit (U-136): guarda cada mensaje del usuario en la bandeja central
cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl para convertirlo en regla. Nunca bloquea."""
import hashlib, json, os, re, sys, datetime
SECRETO = re.compile(r"(password|passwd|contraseñ|api[_-]?key|secret|token\s*[:=]|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,})", re.I)
# BE-143: los avisos automáticos (tareas en segundo plano, subagentes, mensajes de otras sesiones,
# tareas programadas) llegan como prompt pero NO son mensajes del usuario: no se guardan.
AUTOMATICO = re.compile(r"^\s*(<task-notification|<agent-message|<cross-session-message|<system-reminder|<wake\b|<webhook-payload|<child-session-event|<event source=|\[SYSTEM NOTIFICATION"
                        r"|This session's worker process was restarted"          # v132 (COORDINACIÓN 13-nov, id 3b88645a6b4d): aviso del sistema
                        r"|This session is being continued from a previous conversation)", re.I)   # resumen automático al compactar
def es_del_usuario(texto):
    return bool(texto) and not AUTOMATICO.search(texto) and not SECRETO.search(texto)
def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0
    texto = (d.get("prompt") or "").strip()
    if not es_del_usuario(texto):
        return 0
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or "."
    carpeta = os.path.join(raiz, "cache_proyectos", "ORDENES_CRUDAS")
    os.makedirs(carpeta, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    sid = d.get("session_id", "")
    rid = hashlib.sha1(f"{sid}|{ts}|{texto}".encode()).hexdigest()[:12]
    with open(os.path.join(carpeta, "_entrantes.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": rid, "ts_utc": ts, "session": sid, "texto": texto}, ensure_ascii=False) + "\n")
    print("U-136: mensaje del usuario guardado en cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl; "
          "si es una orden, regístrala en REGLAS_USUARIO_CLAUDE.md + MAPA_ORDENES.json y haz commit + push en este turno.")
    return 0
if __name__ == "__main__":
    sys.exit(main())
