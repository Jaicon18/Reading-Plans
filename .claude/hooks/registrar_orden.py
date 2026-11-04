#!/usr/bin/env python3
"""UserPromptSubmit (U-136): guarda cada mensaje del usuario en la bandeja central
cache_proyectos/ORDENES_CRUDAS/_entrantes.jsonl para convertirlo en regla. Nunca bloquea."""
import hashlib, json, os, re, sys, datetime
SECRETO = re.compile(r"(password|passwd|contraseñ|api[_-]?key|secret|token\s*[:=]|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,})", re.I)
def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0
    texto = (d.get("prompt") or "").strip()
    if not texto or SECRETO.search(texto):
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
