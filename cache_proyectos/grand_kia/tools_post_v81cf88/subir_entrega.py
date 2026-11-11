#!/usr/bin/env python3
"""subir_entrega.py — BE-121 (usuario 3-nov, INVIOLABLE): CANDADO DE SUBIDA. Única forma de subir una entrega a Drive.

Envuelve /opt/takeoff/gdrive_fetch.py (no lo modifica). Se NIEGA a subir si:
  1. no existe <workdir>/ENTREGA_OK.json, o no es verde (ok = true, 0 FAIL), o viene de una corrida parcial;
  2. algún archivo de la carpeta de entrega cambió, se agregó o se borró DESPUÉS de la compuerta (sha256 distinto al
     registrado, o archivo más nuevo que ENTREGA_OK.json);
  3. drive.parent_id != 1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc (Claude outputs de la RAÍZ) o es el prohibido de Projects;
  4. la carpeta del proyecto (drive.carpeta_proyecto_id) no aparece EN VIVO como hija de la raíz (gdrive_fetch list);
  5. BE-CF27 (CFA rev10, 5-nov): hay una orden del usuario (U-NNN de ORDENES_DEL_USUARIO.md en el REMOTO, git fetch) que el
     REGLAS_REGISTRO.json del skill con que se corrió la compuerta no tiene: unir el skill y volver a pasar la compuerta.
     $TAKEOFF_REPO = el repo (por defecto /home/user/reading-plans); $SIN_ORDENES_REMOTAS=1 o un $GDRIVE_FETCH falso lo saltan (solo tests).
Sube la carpeta de entrega como subcarpeta NUEVA (nombre de la carpeta de entrega) dentro de la carpeta del proyecto,
archivo por archivo (gdrive_fetch put nunca sobrescribe), y escribe SUBIDA_OK.json.

Uso: python3 subir_entrega.py <project_workdir> [--revisar] [--auditoria-carpeta]      (--revisar = solo los candados, sin subir)
     $GDRIVE_FETCH = ruta alternativa del script de Drive (tests); por defecto /opt/takeoff/gdrive_fetch.py
"""
import datetime
import json, re
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import compuerta_entrega as CE  # noqa: E402

GDRIVE = os.environ.get("GDRIVE_FETCH") or "/opt/takeoff/gdrive_fetch.py"


class Bloqueo(Exception):
    pass


def _g(*args):
    p = subprocess.run([sys.executable, "-I", GDRIVE, *args], capture_output=True, text=True, timeout=3600)
    if p.returncode:
        raise Bloqueo(f"gdrive_fetch {args[0]} falló rc {p.returncode}: {(p.stderr or p.stdout)[-300:]}")
    return p.stdout


def candados(workdir):
    """-> (ENTREGA_OK dict, lista de archivos a subir). Lanza Bloqueo con el motivo."""
    w = os.path.abspath(workdir)
    okp = os.path.join(w, "ENTREGA_OK.json")
    if not os.path.isfile(okp):
        raise Bloqueo("no existe ENTREGA_OK.json: correr compuerta_entrega.py primero")
    ok = json.load(open(okp, encoding="utf-8"))
    malos = [c["id"] for c in ok.get("chequeos") or [] if c.get("estado") == "FAIL"]
    if not ok.get("ok") or malos:
        raise Bloqueo(f"ENTREGA_OK.json NO está en verde (FAIL: {', '.join(malos) or 'corrida parcial'})")
    ed = ok.get("entrega_dir")
    if not ed or not os.path.isdir(os.path.join(w, ed)):
        raise Bloqueo("ENTREGA_OK.json sin carpeta de entrega existente")
    t_ok = os.path.getmtime(okp)
    reg = ok.get("archivos") or {}
    real = {os.path.relpath(os.path.join(r, f), w) for r, _, fs in os.walk(os.path.join(w, ed)) for f in fs}
    nuevos, quitados = sorted(real - set(reg)), sorted(set(reg) - real)
    if nuevos or quitados:
        raise Bloqueo(f"la entrega cambió después de la compuerta: nuevos {nuevos[:5]} / faltan {quitados[:5]}")
    rz = CE.resumenes_fallas(os.listdir(os.path.join(w, ed)))   # U-164: no se suben RESUMEN viejos a la raíz
    if rz:
        raise Bloqueo(rz[0])
    rw = CE.rutas_entrega_fallas(((ok.get("drive") or {}).get("carpeta_proyecto")), os.path.basename(ed.rstrip("/")),
                                 [os.path.relpath(os.path.join(w, r), os.path.join(w, ed)) for r in reg], UMBRAL_ARCHIVOS)   # U-165: rutas en Drive
    if rw:
        raise Bloqueo(rw[0])
    mk = [os.path.basename(r) for r in reg if os.sep + "Planos marcados" + os.sep in os.sep + r and "_markups_" in r and r.endswith(".pdf")]
    if mk and not all(re.fullmatch(CE.MARKUPS_RE, b) for b in mk):   # U-165: nombre '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf'
        raise Bloqueo(f"PDF de markups con nombre fuera de U-165: {mk}")
    for rel, sha in reg.items():
        p = os.path.join(w, rel)
        if CE._sha(p) != sha:
            raise Bloqueo(f"{rel} cambió después de la compuerta (sha256 distinto): volver a correr compuerta_entrega.py")
        if os.path.getmtime(p) > t_ok + 1:
            raise Bloqueo(f"{rel} es más nuevo que ENTREGA_OK.json: volver a correr compuerta_entrega.py")
    d = ok.get("drive") or {}
    if d.get("parent_id") != CE.DRIVE_RAIZ or d.get("parent_id") == CE.DRIVE_PROHIBIDO:
        raise Bloqueo(f"drive.parent_id {d.get('parent_id')} != {CE.DRIVE_RAIZ} (Claude outputs de la RAÍZ)")
    if not d.get("carpeta_proyecto_id"):
        raise Bloqueo("entrega.json sin drive.carpeta_proyecto_id (crearla con gdrive_fetch mkdir "
                      f"{CE.DRIVE_RAIZ} '<proyecto>' y anotar el id)")
    return ok, sorted(reg)


def verificar_padre_en_vivo(d):
    hijos = [json.loads(x) for x in _g("list", CE.DRIVE_RAIZ).splitlines() if x.strip().startswith("{")]
    h = next((x for x in hijos if x.get("id") == d["carpeta_proyecto_id"]), None)
    if not h:
        raise Bloqueo(f"la carpeta {d['carpeta_proyecto_id']} NO es hija de Claude outputs de la raíz ({CE.DRIVE_RAIZ})")
    if d.get("carpeta_proyecto") and h.get("name") != d["carpeta_proyecto"]:
        raise Bloqueo(f"la carpeta {h['id']} se llama '{h.get('name')}', no '{d['carpeta_proyecto']}'")
    return h


RUTA_ORDENES = ".claude/skills/jc-hunter-ordenes/ORDENES_DEL_USUARIO.md"


def ordenes_sin_registro(ordenes_txt, registro):
    """BE-CF27: ids U-NNN de las órdenes del usuario que el registro del skill no tiene."""
    import re
    ids = list(dict.fromkeys(re.findall(r"\[(U-\d+)\s*·", ordenes_txt or "")))
    reg = {str(x.get("id")) for x in (registro or {}).get("reglas") or []}
    return [i for i in ids if i not in reg]


def ordenes_remotas(repo):
    """-> (texto de ORDENES_DEL_USUARIO.md en origin/<rama actual> tras git fetch, origen). Sin red: la copia local."""
    def git(*a):
        return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, timeout=120)
    rama = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if rama and git("fetch", "-q", "origin", rama).returncode == 0:
        p = git("show", f"origin/{rama}:{RUTA_ORDENES}")
        if p.returncode == 0:
            return p.stdout, f"origin/{rama}"
    loc = os.path.join(repo, RUTA_ORDENES)
    return (open(loc, encoding="utf-8").read() if os.path.isfile(loc) else ""), "local (sin fetch)"


def candado_ordenes():
    if os.environ.get("SIN_ORDENES_REMOTAS") == "1" or os.environ.get("GDRIVE_FETCH"):
        return                                          # tests (Drive falso): sin repo remoto
    repo = os.environ.get("TAKEOFF_REPO") or "/home/user/reading-plans"
    if not os.path.isdir(os.path.join(repo, ".git")):
        return
    txt, origen = ordenes_remotas(repo)
    rp = os.path.join(os.path.dirname(AQUI), "REGLAS_REGISTRO.json")
    falt = ordenes_sin_registro(txt, json.load(open(rp, encoding="utf-8")) if os.path.isfile(rp) else {})
    if falt:
        raise Bloqueo(f"órdenes del usuario en {origen} que el skill de la compuerta no tiene: {falt[:8]} "
                      "(BE-CF27: unir el skill con esas órdenes y volver a pasar compuerta_entrega.py antes de subir)")


# BE-CR28 (CR City Hotel rev2, COORDINACIÓN 6-nov): una subida de miles de archivos se cortó por tiempo y el Excel llegó al final.
# (1) orden de subida: Take-off/, Proposal/, Planos marcados/, archivos de la raíz, Auditoria/ al final (el usuario tiene el Excel primero);
# (2) entrega > UMBRAL_ARCHIVOS: Auditoria/ se sube como UN Auditoria.zip armado en una carpeta temporal desde los MISMOS archivos que
#     verificó la compuerta (sha256), sin perder nada; README_REVIEW.md lo dice (CE_SUBIDA_PAQUETE).
UMBRAL_ARCHIVOS = CE.UMBRAL_AUDITORIA_ZIP   # una sola cifra con la compuerta (U-165)
_ORDEN = {"Take-off": 0, "Proposal": 1, "Planos marcados": 2}


def orden_subida(rel, raiz_ed):
    partes = os.path.relpath(rel, raiz_ed).split(os.sep)
    if len(partes) == 1:
        return (3, rel)
    return (_ORDEN.get(partes[0], 4 if partes[0] == "Auditoria" else 3), rel)


def empaquetar_auditoria(w, raiz_ed, archivos, umbral=UMBRAL_ARCHIVOS):
    """-> (lista de (rel_destino, ruta_local)); con > umbral archivos, los de Auditoria/ van dentro de Auditoria.zip."""
    import tempfile
    import zipfile
    pares = [(rel, os.path.join(w, rel)) for rel in sorted(archivos, key=lambda r: orden_subida(r, raiz_ed))]
    if len(archivos) <= umbral:
        return pares
    aud = os.path.join(raiz_ed, "Auditoria") + os.sep
    dentro = [(rel, loc) for rel, loc in pares if rel.startswith(aud)]
    if not dentro:
        return pares
    zp = os.path.join(tempfile.mkdtemp(prefix="subida_"), "Auditoria.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, loc in dentro:
            z.write(loc, os.path.relpath(rel, raiz_ed))
    with zipfile.ZipFile(zp) as z:
        assert len(z.namelist()) == len(dentro), "Auditoria.zip incompleto"
    return [(rel, loc) for rel, loc in pares if not rel.startswith(aud)] + [(os.path.join(raiz_ed, "Auditoria.zip"), zp)]


def subir(workdir, solo_revisar=False, auditoria_carpeta=False):
    w = os.path.abspath(workdir)
    ok, archivos = candados(w)
    candado_ordenes()
    d = ok["drive"]
    verificar_padre_en_vivo(d)
    if solo_revisar:
        return {"revisado": True, "archivos": len(archivos)}
    raiz_ed = ok["entrega_dir"]
    ids = {raiz_ed: _g("mkdir", d["carpeta_proyecto_id"], os.path.basename(raiz_ed)).strip().splitlines()[-1]}
    log, listados = [], {}
    # BE-GK31 (Grand Kia, COORDINACIÓN U-008): --auditoria-carpeta sube Auditoria/ DESEMPACADA (como los demás proyectos) en la
    # misma carpeta de entrega (mkdir la reutiliza, lo ya subido con mismo nombre y tamaño se salta) y renombra el
    # Auditoria.zip de la subida anterior a "zz Auditoria.zip" (rename, nunca borrar)
    for rel, loc in empaquetar_auditoria(w, raiz_ed, archivos, umbral=10 ** 9 if auditoria_carpeta else UMBRAL_ARCHIVOS):
        sub = os.path.dirname(rel)
        partes = os.path.relpath(sub, raiz_ed).split(os.sep) if sub != raiz_ed else []
        cur = raiz_ed
        for pt in partes:
            if pt in ("", "."):
                continue
            nxt = os.path.join(cur, pt)
            if nxt not in ids:
                ids[nxt] = _g("mkdir", ids[cur], pt).strip().splitlines()[-1]
            cur = nxt
        # R80f.42 (Chuze FINAL7, 4-nov): una subida cortada (error 5xx de Drive) se RETOMA: el archivo que ya está en la carpeta
        # con el mismo nombre Y el mismo tamaño se da por subido; mismo nombre con otro tamaño = Bloqueo (nunca se sobrescribe)
        if cur not in listados:
            listados[cur] = {}
            for ln in _g("list", ids[cur]).splitlines():
                try:
                    it = json.loads(ln)
                except ValueError:
                    continue
                listados[cur][it.get("name")] = it
        ya = listados[cur].get(os.path.basename(rel))
        if ya is not None:
            if str(ya.get("size")) != str(os.path.getsize(loc)):
                raise Bloqueo(f"{rel}: ya existe en Drive con otro tamaño ({ya.get('size')} vs {os.path.getsize(loc)}): "
                              "no se sobrescribe; revisar a mano la carpeta")
            log.append({"archivo": rel, "carpeta_id": ids[cur], "salida": f"YA SUBIDO (mismo nombre y tamaño) id {ya.get('id')}"})
            continue
        out = _g("put", loc, ids[cur])
        log.append({"archivo": rel, "carpeta_id": ids[cur], "salida": out.strip()[-200:]})
    if auditoria_carpeta:
        for ln in _g("list", ids[raiz_ed]).splitlines():
            try:
                it = json.loads(ln)
            except ValueError:
                continue
            if it.get("name") == "Auditoria.zip":
                log.append({"archivo": "Auditoria.zip", "carpeta_id": ids[raiz_ed],
                            "salida": _g("rename", it["id"], "zz Auditoria.zip").strip()[-200:]})
    res = {"fecha_iso": datetime.datetime.now(datetime.timezone.utc).isoformat(), "entrega_ok_sha": CE._sha(os.path.join(w, "ENTREGA_OK.json")),
           "drive": d, "carpetas": ids, "subidos": log}
    json.dump(res, open(os.path.join(w, "SUBIDA_OK.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        r = subir(argv[1], "--revisar" in argv, "--auditoria-carpeta" in argv)
    except Bloqueo as e:
        print(f"SUBIDA BLOQUEADA: {e}")
        return 1
    print("CANDADOS OK" + ("" if r.get("revisado") else f" — {len(r['subidos'])} archivos subidos; SUBIDA_OK.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
