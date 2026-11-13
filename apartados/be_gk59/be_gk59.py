"""BE-GK59 (Grand Kia rev3b, 13-nov): the gate rewrites <workdir>/ENTREGA_OK.json on EVERY run. rev3b was uploaded with the VERDE of
v81cf129 (run 60914f5fc798); a later re-run with v81cf130 (ROJA, process count) overwrote the local ENTREGA_OK.json, and the VERDE that
was delivered only survived in compuerta_corridas.jsonl. Rule: every gate run also keeps ENTREGA_OK_<corrida>.json (never overwritten),
and once SUBIDA_OK.json exists, ENTREGA_OK.json must be the one of the run that was uploaded (same Excel / PDF hashes, ok true, run
finished before the first upload); a later run writes only its ENTREGA_OK_<corrida>.json.
guardar(w, corrida): copy ENTREGA_OK.json -> ENTREGA_OK_<corrida>.json. fallas(w): the check. CLI: python3 be_gk59.py <workdir>."""
import datetime, json, os, shutil, sys


def guardar(w, corrida):
    src = os.path.join(w, "ENTREGA_OK.json")
    dst = os.path.join(w, f"ENTREGA_OK_{corrida}.json")
    if os.path.isfile(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
    return dst


def _iso(s):
    return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00")) if s else None


def fallas(w):
    sp, ep, cp = (os.path.join(w, n) for n in ("SUBIDA_OK.json", "ENTREGA_OK.json", "compuerta_corridas.jsonl"))
    if not os.path.isfile(sp):
        return []
    sub = json.load(open(sp, encoding="utf-8"))
    t_sub = _iso(sub.get("primera_subida_iso") or sub.get("fecha_iso"))
    fins = [json.loads(l) for l in open(cp, encoding="utf-8") if '"fin"' in l] if os.path.isfile(cp) else []
    subida = [f for f in fins if f.get("ok") and t_sub and _iso(f.get("ts")) <= t_sub]
    if not subida:
        return ["SUBIDA_OK.json without a VERDE run that finished before the upload in compuerta_corridas.jsonl (BE-GK59)"]
    run = subida[-1]
    ev = []
    if not os.path.isfile(os.path.join(w, f"ENTREGA_OK_{run['corrida']}.json")):
        ev.append(f"ENTREGA_OK_{run['corrida']}.json missing: the ENTREGA_OK of the uploaded run is not kept by run (BE-GK59)")
    ok = json.load(open(ep, encoding="utf-8")) if os.path.isfile(ep) else {}
    if not ok.get("ok") or (_iso(ok.get("fecha_iso")) and t_sub and _iso(ok.get("fecha_iso")) > t_sub):
        ev.append(f"ENTREGA_OK.json was rewritten after the upload ({ok.get('fecha_iso')}, ok={ok.get('ok')}, {ok.get('skill_version')}): "
                  f"the delivered VERDE is run {run['corrida']} ({run['ts']}); a run after the upload writes only ENTREGA_OK_<corrida>.json (BE-GK59)")
    return ev


if __name__ == "__main__":
    ev = fallas(sys.argv[1])
    print("\n".join(ev) if ev else "BE-GK59 PASS: ENTREGA_OK.json is the uploaded run's, kept by run")
    sys.exit(1 if ev else 0)
