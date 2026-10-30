#!/usr/bin/env python3
"""run_takeoff.py — runner de take-off por API con la cadena COMPLETA del skill (R80e.37: nunca saltar la cadena).

El modelo SOLO LEE (canon A y canon B independientes + resolución dirigida de diferencias). Los programas calculan:
inventario_tags.py → [lectura A | lectura B] → comparar.py → [resolución] → overlay de decisiones → canon.py
→ tools (inventario, framed_openings, alcance_filtro, markups) → plantilla_excel.py armar (compuerta reglas.py
adentro; si falla, el runner se DETIENE) → reglas.py compuerta (reporte; nunca stub).

Modos
  --dry-run        no llama a la API: usa --canon-ref como lectura A y B (prueba gratis de toda la cadena).
  (sin --dry-run)  llama `claude -p` con ANTHROPIC_API_KEY tomado de $TAKEOFF_API_KEY (el runner nunca imprime
                   ni guarda la clave), --model sonnet, --max-budget-usd por paso, --output-format json,
                   --allowedTools limitadas (nunca bypassPermissions). Tope total --budget (default 20 USD).

Uso (B&N, dry-run):
  python3 costeo_api/runner/run_takeoff.py --dry-run \
      --pdf <bid_set.pdf> --skill <dir del skill v80s> --project-inputs cache_proyectos/barnes_noble/takeoff_work \
      --evidence-root cache_proyectos/barnes_noble --overlay costeo_api/runner/decisiones_BN.json \
      --canon-ref cache_proyectos/barnes_noble/takeoff_work/etapas/4_canon/takeoff_canon.json \
      --compare-with cache_proyectos/barnes_noble/FINAL_FOR_REVIEW_2026-10-24_rev13/Take-off/<rev13>.xlsx \
      --work <dir de trabajo nuevo>
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import overlay  # noqa: E402
import completitud  # noqa: E402
import reconcile  # noqa: E402
import evidencia  # noqa: E402

# Archivos de entrada del proyecto que la lectura (o el estimador) produce además del canon. En dry-run se copian
# del proyecto de referencia; en una corrida real los escribe el paso de lectura (prompts/lectura.md).
PROJECT_INPUTS = ["etapas/4_canon/fo_in.json", "etapas/4_canon/alcance_in.json", "etapas/4_canon/existing_excluded.json",
                  "etapas/4_canon/evidencias_reglas.json", "renglones.json", "takeoff.json",
                  "etapas/PROCESO_CORRIDA.md", "etapas/5_auditoria/AUDIT_COMPLETENESS.md"]   # evidencia de proceso de la lectura
# Herramientas de PROCESO previas al canon (las corre la lectura: arranque, índice, conteo de tags, test ciego, alcances,
# registro). En dry-run se re-ejecutan desde la bitácora de la corrida de referencia, con las rutas reescritas.
PROCESO = ("arranque.py", "indice_set.py", "contar_tags.py", "test_ciego.py")
ALLOWED = "Read,Write,Glob,Grep,Bash(python3:*)"          # nunca bypassPermissions
STEP_BUDGET = {"lectura_A": 5.0, "lectura_B": 5.0, "resolucion": 2.0, "cobertura": 1.0, "correccion": 2.0}  # USD/paso
MAX_CONTINUAR = 2                                   # continuaciones por lectura si la compuerta falla
CONT_TOPE = 2.0                                     # tope de cada continuación (USD)
MAX_CORRECCION = 3                                  # rondas de corrección de la lectura si reglas.py no deja armar


class Alto(Exception):
    """El runner se detiene y reporta (R80e.37)."""


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def run(cmd, cwd, env=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise Alto(f"falló: {' '.join(map(str, cmd[:3]))} ... rc={p.returncode}\n{(p.stdout + p.stderr)[-1500:]}")
    return p


class Runner:
    def __init__(self, a):
        self.a = a
        self.root = os.path.abspath(a.work)
        self.k = os.path.join(self.root, "takeoff_work")        # misma profundidad que el proyecto (rutas ../../)
        self.t = os.path.join(os.path.abspath(a.skill), "tools")
        self.gasto = 0.0
        self.pasos = []
        self.env = dict(os.environ, BITACORA=os.path.join(self.k, "bitacora.jsonl"))
        self.plan_sheets = [x.strip() for x in (a.trade_plan_sheets or a.plan_sheet).split(",") if x.strip()]

    # ---------------------------------------------------------------- utilidades
    def tool(self, *args, check=True):
        return run([sys.executable, os.path.join(self.t, "bitacora.py"), "run", os.path.join(self.t, args[0]), *args[1:]],
                   self.k, self.env, check)

    def costo(self, paso, usd=0.0, inp=0, out=0, cr=0, cw=0, seg=0.0, modelo="-"):
        self.gasto += usd
        self.pasos.append((paso, round(usd, 4)))
        if self.a.dry_run:                      # dry-run: no ensucia costos.csv (no hubo llamada)
            return
        f = os.environ.get("RUNNER_COSTOS") or os.path.join(AQUI, "..", "costos.csv")    # pruebas: otro archivo
        nuevo = not os.path.exists(f)
        with open(f, "a", newline="") as fh:
            w = csv.writer(fh)
            if nuevo:
                w.writerow(["pasada", "paso", "modelo", "usd", "input", "output", "cache_read", "cache_write", "segundos"])
            w.writerow(["runner-dry" if self.a.dry_run else "runner", paso, modelo, round(usd, 6), inp, out, cr, cw, round(seg)])

    def sandbox(self, nombre, archivos):
        """Directorio aislado FUERA del workdir (sin la evidencia ni los entregables del proyecto) para una llamada."""
        d = self.root + "_" + nombre
        os.makedirs(d, exist_ok=True)
        out = {}
        for k, src in archivos.items():
            dst = os.path.join(d, os.path.basename(src))
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            out[k] = dst
        return d, out

    def claude(self, paso, prompt_file, extra, cwd=None, tope=None):
        """Una llamada `claude -p`. Nunca en dry-run. Corta si el tope total se pasaría."""
        if self.a.dry_run:
            raise Alto("BUG: claude() llamado en dry-run")
        tope = tope if tope is not None else STEP_BUDGET.get(paso.split(":")[0], 2.0)
        if tope < 0.25:
            raise Alto(f"{paso}: sin presupuesto restante en el tope del paso")
        if self.gasto + tope > self.a.budget:
            raise Alto(f"tope total {self.a.budget} USD: gastado {self.gasto:.2f}, el paso {paso} pide hasta {tope}")
        key = os.environ.get("TAKEOFF_API_KEY")
        if not key:
            raise Alto("falta $TAKEOFF_API_KEY")
        prompt = open(prompt_file, encoding="utf-8").read().format(**extra)
        env = dict(self.env, ANTHROPIC_API_KEY=key)
        t0 = time.time()
        p = run(["claude", "-p", prompt, "--model", "sonnet", "--max-budget-usd", str(tope), "--output-format", "json",
                 "--allowedTools", ALLOWED, "--append-system-prompt-file", os.path.join(os.path.abspath(self.a.skill), "SKILL.md")],
                cwd or self.k, env, check=False)
        try:
            r = json.loads(p.stdout or "{}")
        except ValueError:
            r = {}
        with open(os.path.join(cwd or self.k, f"respuesta_{paso.replace(':', '_')}.json"), "w") as fh:
            fh.write(p.stdout or "")            # la respuesta del modelo queda para diagnosticar
        u = r.get("usage") or {}
        self.costo(paso, float(r.get("total_cost_usd") or 0), u.get("input_tokens", 0), u.get("output_tokens", 0),
                   u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0), time.time() - t0, "sonnet")
        if p.returncode != 0:                   # el gasto ya quedó en costos.csv aunque la llamada falle (p. ej. tope agotado)
            raise Alto(f"falló: claude -p {paso} rc={p.returncode} {r.get('subtype', '')} {r.get('errors', '')}")
        return r

    # ---------------------------------------------------------------- pasos
    def preparar(self):
        if os.path.exists(self.root) and os.listdir(self.root):
            raise Alto(f"--work {self.root} no está vacío (no se pisa nada)")
        for d in ("1_inventario", "2_lectura", "3_revision", "4_canon/out", "5_auditoria", "6_markups", "7_imagenes", "8_excel"):
            os.makedirs(os.path.join(self.k, "etapas", d), exist_ok=True)
        # imágenes de evidencia con su ruta relativa (el canon las cita como ../../<carpeta>/img/...)
        ev = os.path.abspath(self.a.evidence_root)
        for n in sorted(os.listdir(ev)):
            src = os.path.join(ev, n)
            if os.path.isdir(src) and n != "takeoff_work":
                os.symlink(src, os.path.join(self.root, n))
        # imágenes propias del proyecto (4_canon/img, etc.) que el canon cita dentro de takeoff_work
        pin = os.path.abspath(self.a.project_inputs)
        for sub in ("etapas/4_canon/img", "etapas/2_lectura", "etapas/1_inventario", "etapas/3_revision", "etapas/5_auditoria/img",
                    "etapas/0_mapa"):
            s = os.path.join(pin, sub)
            if os.path.isdir(s):
                dst = os.path.join(self.k, sub)
                shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(s, dst, symlinks=True)
        for f in PROJECT_INPUTS:
            s = os.path.join(pin, f)
            if os.path.exists(s):
                os.makedirs(os.path.dirname(os.path.join(self.k, f)), exist_ok=True)
                shutil.copy2(s, os.path.join(self.k, f))
        log("1/11 workdir listo (evidencia enlazada con su ruta relativa)")

    def proceso(self):
        """Arranque, alcances y registro: SIEMPRE por bitacora.py run en esta corrida (la compuerta lo exige)."""
        pdf = os.path.abspath(self.a.pdf)
        pin = os.path.abspath(self.a.project_inputs)
        # Herramientas de proceso (scripts, $0) re-ejecutadas desde la bitácora de la referencia en ambos modos: la
        # corrida real solo cambia la LECTURA del canon; el proceso (índice, conteo de tags, test ciego, registro
        # verificado) se reutiliza de la referencia y así se declara en el resultado.
        if os.path.exists(os.path.join(pin, "bitacora.jsonl")):
            for l in open(os.path.join(pin, "bitacora.jsonl")):
                d = json.loads(l)
                if d.get("tool") in PROCESO:
                    args = [str(x).replace(pin, self.k) for x in d.get("args") or []]
                    for x in args:                      # carpetas de salida que la herramienta espera
                        if x.startswith(self.k) and os.path.splitext(x)[1]:
                            os.makedirs(os.path.dirname(x), exist_ok=True)
                    self.tool(d["tool"], *args)
        else:
            self.tool("arranque.py", pdf)
        self.tool("alcances.py", "escanear", pdf, "escaneo.json")
        self.tool("alcances.py", "renglones", "escaneo.json", "renglones_alcances.json")
        self.tool("registro.py", "crear", "registro.json", "renglones.json")
        if os.path.exists(os.path.join(pin, "registro.json")):
            # el registro verificado (marcas con su evidencia) es producto del proceso de referencia
            shutil.copy2(os.path.join(pin, "registro.json"), os.path.join(self.k, "registro.json"))
        self.costo("proceso")
        log("2/11 proceso OK: arranque, alcances escanear, registro crear (+ herramientas de proceso de la referencia)")

    def inventario_tags(self):
        out = os.path.join(self.k, "etapas", "1_inventario", "runner")
        self.tool("inventario_tags.py", os.path.abspath(self.a.pdf), out, "--sin-recortes")
        self.costo("inventario_tags")
        log("3/11 inventario_tags.py OK")
        return os.path.join(out, "inventario.json")

    def lecturas(self, inv):
        A = os.path.join(self.k, "etapas", "2_lectura", "takeoff_canon_A.json")
        B = os.path.join(self.k, "etapas", "2_lectura", "takeoff_canon_B.json")
        if self.a.dry_run:
            shutil.copy2(self.a.canon_ref, A)
            shutil.copy2(self.a.canon_ref, B)
            self.costo("lectura_A")
            self.costo("lectura_B")
        elif self.a.reusar_lecturas:
            # reanudación: las lecturas YA pagadas de una corrida anterior (sandboxes <run>_lectura_X); no se vuelve a llamar.
            # Una lectura que no pasa el esquema no se usa y se declara (la corrida queda con UNA sola lectura).
            self.lecturas_no_usadas = []
            seguir = [x.strip() for x in (self.a.continuar_lados or "").split(",") if x.strip()]
            for lado, out in (("A", A), ("B", B)):
                sd = self.a.reusar_lecturas + f"_lectura_{lado}"
                src = os.path.join(sd, f"takeoff_canon_{lado}.json")
                if os.path.exists(src) and lado in seguir:
                    # continuación PAGADA de la misma lectura, en su sandbox, con el validador vigente
                    shutil.copy2(os.path.join(AQUI, "validar_canon.py"), os.path.join(sd, "validar_canon.py"))
                    try:
                        self.compuerta_lectura(lado, (sd, {"pdf": os.path.join(sd, os.path.basename(self.a.pdf)),
                                                           "tools": os.path.join(sd, "tools")}, src, self.gasto), None)
                    except Alto as e:
                        log(f"   lectura {lado}: la continuación no la cerró ({str(e)[-300:]})")
                v = run([sys.executable, os.path.join(AQUI, "validar_canon.py"), src, self.t], self.root, check=False) \
                    if os.path.exists(src) else None
                if v is not None and v.returncode == 0:
                    shutil.copy2(src, out)
                    log(f"   lectura {lado}: reusada de {src}")
                else:
                    self.lecturas_no_usadas.append({"lado": lado, "motivo": (v.stdout.strip()[-300:] if v else "no existe")})
                    log(f"   lectura {lado}: NO usable ({self.lecturas_no_usadas[-1]['motivo']})")
            if len(self.lecturas_no_usadas) == 2:
                raise Alto("ninguna lectura reusada pasa el esquema")
            if not os.path.exists(A):
                shutil.move(B, A)
        else:
            pr = os.path.join(AQUI, "prompts", "lectura.md")
            sand, self.lecturas_no_usadas = {}, []
            for lado, out in (("A", A), ("B", B)):      # independientes: cada una en su propio sandbox, sin ver la otra
                d, f = self.sandbox(f"lectura_{lado}", {"pdf": os.path.abspath(self.a.pdf), "inv": inv, "tools": self.t,
                                                         "val": os.path.join(AQUI, "validar_canon.py")})
                o = os.path.join(d, os.path.basename(out))
                gasto0 = self.gasto
                try:
                    self.claude(f"lectura_{lado}", pr, {"pdf": f["pdf"], "inventario": f["inv"], "out": o, "lado": lado,
                                                         "plan_sheets": ", ".join(self.plan_sheets)}, cwd=d)
                except Alto as e:               # tope agotado: la lectura NO se descarta, se continúa (compuerta)
                    if "max_budget" not in str(e) and "rc=" not in str(e):
                        raise
                    log(f"   lectura {lado}: {str(e)[:160]} -> se continúa")
                sand[lado] = (d, f, o, gasto0)
                try:
                    self.compuerta_lectura(lado, sand[lado], None)
                except Alto as e:               # se continuó y no pasó: se declara y sigue la otra lectura
                    self.lecturas_no_usadas.append({"lado": lado, "motivo": str(e)[-400:]})
                    log(f"   lectura {lado}: NO pasa después de las continuaciones (se declara)")
            ok = [x for x in ("A", "B") if x not in {n["lado"] for n in self.lecturas_no_usadas}]
            if not ok:
                raise Alto("ninguna lectura pasa la compuerta: " + " | ".join(n["motivo"][-200:] for n in self.lecturas_no_usadas))
            # cruce: cada lectura debe traer los types / elements que encontró la otra (o justificarlos)
            if len(ok) == 2:
                for lado, otro in (("A", "B"), ("B", "A")):
                    try:
                        self.compuerta_lectura(lado, sand[lado], sand[otro][2])
                    except Alto as e:           # el cruce lo resuelve la resolución dirigida (diferencias A/B)
                        log(f"   lectura {lado}: cruce con la otra sin cerrar -> va a la resolución ({str(e)[-160:]})")
            for lado, out in (("A", A), ("B", B)):
                if lado in ok:
                    shutil.copy2(sand[lado][2], out)
            if "A" not in ok:
                shutil.move(B, A)
        log("4/11 lecturas A y B " + ("(dry-run: canon de referencia)" if self.a.dry_run else "OK"))
        return A, B

    def compuerta_lectura(self, lado, sb, otro_path):
        """Esquema (validar_canon.py = canon.py) + completitud por hojas / types; si falla, continúa la MISMA lectura."""
        d, f, o, gasto0 = sb
        for intento in range(MAX_CONTINUAR + 1):
            if not os.path.exists(o):
                motivo = "el archivo del canon no existe"
            else:
                v = run([sys.executable, os.path.join(AQUI, "validar_canon.py"), o, f["tools"]], d, check=False)
                c = json.load(open(o))
                otro = json.load(open(otro_path)) if otro_path else None
                r = completitud.revisar(c, self.plan_sheets, otro)
                motivo = "\n".join(x for x in (
                    "" if v.returncode == 0 else "ESQUEMA: " + v.stdout.strip()[-1200:],
                    "" if not r["faltan_hojas"] else "FALTAN HOJAS DE PLANTA SIN WALLS: " + ", ".join(r["faltan_hojas"]),
                    "" if not r["faltan_types"] else "TYPES DEL SCHEDULE SIN WALLS NI types_none_reason: " + ", ".join(r["faltan_types"]),
                    "" if not r["faltan_vs_otra"] else "TYPES / ELEMENTS QUE OTRA LECTURA SÍ ENCONTRÓ Y AQUÍ FALTAN (léelos en el plano, "
                    "no los copies): " + ", ".join(r["faltan_vs_otra"])) if x)
                if not motivo:
                    log(f"   lectura {lado}: compuerta OK ({r['walls']} walls, {r['lf']} LF)")
                    return
            if intento == MAX_CONTINUAR:
                raise Alto(f"la lectura {lado} no pasa la compuerta después de {MAX_CONTINUAR} continuaciones:\n{motivo}")
            reserva = STEP_BUDGET["cobertura"] + (0 if self.a.reusar_lecturas else STEP_BUDGET["resolucion"])
            resto = min(CONT_TOPE, self.a.budget - self.gasto - reserva)    # deja resolución y paso 12 pagados
            log(f"   lectura {lado}: compuerta NO pasa -> continuación {intento + 1} (resto del tope {resto:.2f} USD)")
            self.claude(f"lectura_{lado}:continuar{intento + 1}", os.path.join(AQUI, "prompts", "continuar.md"),
                        {"lado": lado, "out": o, "pdf": f["pdf"], "motivo": motivo}, cwd=d, tope=round(resto, 2))

    def comparar(self, A, B, inv):
        if not os.path.exists(B):
            log("5/11 comparar.py: OMITIDO (una sola lectura usable; sin cruce A/B)")
            self.costo("comparar")
            return 0, None
        out = os.path.join(self.k, "etapas", "3_revision", "runner")
        self.tool("comparar.py", A, B, inv, out, check=False)      # rc 1 = hay diferencias / alertas (se reporta)
        rv = json.load(open(os.path.join(out, "revision.json")))
        n = sum(len(rv.get(k) or []) for k in ("difieren", "solo_A", "solo_B"))
        self.costo("comparar")
        log(f"5/11 comparar.py: {n} diferencias")
        return n, out

    def resolver(self, A, n, rev_dir):
        final = os.path.join(self.k, "etapas", "2_lectura", "takeoff_canon_AB.json")
        B = os.path.join(os.path.dirname(A), "takeoff_canon_B.json")
        if os.path.exists(B):                     # la resolución parte de la lectura MÁS COMPLETA (walls, luego LF)
            ra = completitud.revisar(json.load(open(A)), [])
            rb = completitud.revisar(json.load(open(B)), [])
            if (rb["walls"], rb["lf"]) > (ra["walls"], ra["lf"]):
                A, B = B, A
                log(f"   resolución parte de la lectura B ({rb['walls']} walls) y no de la A ({ra['walls']})")
        if self.a.reusar_resolucion and not self.a.dry_run:     # resolución ya pagada de una corrida anterior
            shutil.copy2(self.a.reusar_resolucion, final)
            log(f"6/11 resolución reusada de {self.a.reusar_resolucion}")
            return final
        if n == 0 or self.a.dry_run:
            shutil.copy2(A, final)
            self.costo("resolucion")
        else:                                                     # SOLO las diferencias, con su recorte
            d, f = self.sandbox("resolucion", {"pdf": os.path.abspath(self.a.pdf), "rev": rev_dir, "A": A, "B": B,
                                               "tools": self.t, "val": os.path.join(AQUI, "validar_canon.py")})
            o = os.path.join(d, "takeoff_canon_AB.json")
            shutil.copy2(f["A"], o)             # punto de partida = lectura base; la resolución corrige SOLO las diferencias
            antes = open(o).read()
            self.claude("resolucion", os.path.join(AQUI, "prompts", "resolucion.md"),
                        {"pdf": f["pdf"], "revision": os.path.join(f["rev"], "revision.json"), "canon_A": f["A"], "out": o}, cwd=d)
            v = run([sys.executable, os.path.join(AQUI, "validar_canon.py"), o, f["tools"]], d, check=False)
            if v.returncode != 0:
                raise Alto(f"la resolución dejó el canon fuera de esquema: {v.stdout.strip()[-400:]}")
            if open(o).read() == antes:
                log("   resolución: el modelo no cambió la lectura base (se declara: diferencias sin resolver)")
                self.resolucion_sin_cambios = True
            shutil.copy2(o, final)
        log("6/11 resolución " + ("(sin diferencias)" if n == 0 else "OK"))
        return final

    def decisiones(self, canon_ab):
        ov = json.load(open(self.a.overlay)) if self.a.overlay else {}
        self.sin_objeto, self.emparejados = [], None
        leido = json.load(open(canon_ab))
        cs = leido.setdefault("constants", {})
        hoja = (cs.get("plan_scale_by_sheet") or {}).get(self.a.plan_sheet) or {}
        if not cs.get("plan_scale_pt_per_ft") and hoja.get("value"):
            # inventario.py exige la escala de la planta; la lectura la dio por hoja: misma cifra, fuente citada
            cs["plan_scale_pt_per_ft"] = {"value": hoja["value"], "source": f"[DERIVED] = plan_scale_by_sheet "
                                          f"{self.a.plan_sheet} of the reading: {hoja.get('source', '')}"}
            log(f"   plan_scale_pt_per_ft tomado de plan_scale_by_sheet {self.a.plan_sheet} = {hoja['value']}")
            sb = [w for w in leido.get("walls") or [] if isinstance(w.get("band"), dict) and not w["band"].get("sheet")
                  and w.get("sheet")]
            for w in sb:                    # con escala de planta canon.py exige band.sheet: la hoja del mismo wall
                w["band"]["sheet"] = w["sheet"]
            if sb:
                log(f"   band.sheet = sheet del wall en {len(sb)} wall(s)")
        json.dump(leido, open(canon_ab, "w"), indent=1, ensure_ascii=False)
        if self.a.ref_base:                 # reconciliación de ids por geometría (solo para aplicar decisiones)
            c, mapa, self.sin_objeto = reconcile.aplicar(leido, json.load(open(self.a.ref_base)), ov)
            self.mapa = mapa
            self.emparejados = len(mapa)
            dec = [x for x in self.sin_objeto if not x.get("derivado")]
            log(f"7/11 reconciliación: {len(mapa)} walls emparejados con la referencia; {len(dec)} decisión(es) sin objeto"
                f" (+ {len(self.sin_objeto) - len(dec)} nodes derivados)")
        else:
            c = overlay.aplicar_canon(leido, ov)
        t = overlay.aplicar_takeoff(json.load(open(os.path.join(self.k, "takeoff.json"))), ov)
        dst = os.path.join(self.k, "etapas", "4_canon", "takeoff_canon.json")
        mapa = os.path.join(self.k, "etapas", "0_mapa", "SHEET_MAP.md")
        if not self.a.dry_run and os.path.exists(mapa):
            # R80e.38: la evidencia visual y los estados #0 los genera el PROGRAMA desde las coordenadas
            # tags: inventario del proceso de referencia (barrido manual de tags, reutilizado como el registro)
            pinv = os.path.join(self.k, "etapas", "1_inventario", "inventario.json")
            inv = json.load(open(pinv)) if os.path.exists(pinv) else None
            ev = evidencia.Evidencia(os.path.abspath(self.a.pdf), evidencia.mapa_hojas(mapa),
                                     os.path.join(self.k, "etapas", "4_canon", "img_runner"))
            self.mep_registro(c, ev)
            n = evidencia.aplicar(c, ev, inv)
            log(f"7/11 evidencia por programa: {n}")
        json.dump(c, open(dst, "w"), indent=1, ensure_ascii=False)
        json.dump(t, open(os.path.join(self.k, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
        log("7/11 overlay de decisiones del estimador fusionado (idempotente)")
        return dst

    def mep_registro(self, c, ev):
        """R71.9 por PROGRAMA: mep.py registra cada hoja M / P de mep_sweep.sheets contra la planta (votos de segmentos de
        muro). >= 25 por dirección = registro usable; si no, no_usable con motivo, hoja e imagen de la hoja MEP."""
        import ast
        sw = c.get("mep_sweep")
        arq = ev.hojas.get(self.a.plan_sheet)
        if not isinstance(sw, dict) or arq is None:
            return
        regs = {}
        for h in sw.get("sheets") or []:
            if h not in ev.hojas or not str(h).startswith(("M", "P")):
                continue
            p = self.tool("mep.py", str(ev.hojas[h]), str(arq), "--pdf", os.path.abspath(self.a.pdf), check=False)
            try:
                r = ast.literal_eval([l for l in (p.stdout or "").splitlines() if l.startswith("{'dx'")][-1])
            except (ValueError, SyntaxError, IndexError):
                r = None
            img = ev.hoja(h)
            if not r:
                regs[h] = {"matches": 0, "source": f"{h} vs {self.a.plan_sheet} (mep.py registro)",
                           "no_usable": {"motivo": "mep.py found no matching wall segments between the sheets",
                                         "source": h, "img": img}}
                continue
            m = min(r["vx"], r["vy"])
            regs[h] = {"dx_pt": r["dx"], "dy_pt": r["dy"], "matches": m,
                       "source": f"{h} vs {self.a.plan_sheet} (mep.py registro: {r['vx']} V / {r['vy']} H)"}
            if not r["ok"]:
                regs[h]["no_usable"] = {"motivo": f"registration below 25 matching wall segments ({r['vx']} V / "
                                                  f"{r['vy']} H): sheet not used for geometric crossings; ducts / "
                                                  f"pipes crossing walls go to RFI", "source": h, "img": img}
        if regs:
            sw.pop("registro", None)
            sw["registros"] = regs
            log(f"   mep.py registro: " + ", ".join(f"{h} {v['matches']}" for h, v in regs.items()))

    def corregir(self, canon_ab, ronda, texto=None, origen="canon.py (con las decisiones del estimador aplicadas)"):
        """reglas.py no deja armar: las fallas que dependen de la LECTURA (no las de imagen: esas las genera el programa)
        vuelven al modelo con los ids de la lectura; corrige el canon AB en un sandbox y la cadena se repite."""
        f = os.path.join(self.k, "etapas", "REGLAS_FALLAS.md")
        inv = {v: k for k, v in (getattr(self, "mapa", None) or {}).items()}
        grupos = {}
        if texto:                               # error de canon.py (con las decisiones del estimador aplicadas)
            t = texto
            for ref, lec in inv.items():
                t = re.sub(rf"(?<![\w.-]){re.escape(ref)}(?![\w.-])", lec, t)
            grupos[origen] = {t}
        for l in (open(f, encoding="utf-8") if not texto and os.path.exists(f) else []):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) < 4 or c[0] in ("Regla", "---") or set(c[0]) <= set("-"):
                continue
            if re.sub(r"\([^)]*\)", "", c[2]).strip() == "falta imagen que exista":
                continue                        # la imagen la genera el programa, no la lectura
            caso = c[1]
            base = caso.split(".")[0].split("[")[0]
            caso = caso.replace(base, inv.get(base, base), 1)
            val = c[2]
            for ref, lec in inv.items():                # ids de la referencia citados dentro del texto -> ids de la lectura
                val = re.sub(rf"(?<![\w.-]){re.escape(ref)}(?![\w.-])", lec, val)
            grupos.setdefault(c[3][:200], set()).add(caso if val.startswith(("falta", "sin")) else f"{caso}: {val[:220]}")
        if not grupos:
            raise Alto("reglas.py: las fallas que quedan no dependen de la lectura (ver etapas/REGLAS_FALLAS.md)")
        motivo = "\n".join(f"- {k}: {', '.join(sorted(v)[:60])}" for k, v in sorted(grupos.items(), key=lambda kv: -len(kv[1])))
        d, fs = self.sandbox(f"correccion{ronda}", {"pdf": os.path.abspath(self.a.pdf), "AB": canon_ab, "tools": self.t,
                                                     "val": os.path.join(AQUI, "validar_canon.py")})
        log(f"   corrección {ronda}: {sum(len(v) for v in grupos.values())} falla(s) de lectura en {len(grupos)} grupo(s)")
        try:
            self.claude("correccion", os.path.join(AQUI, "prompts", "correccion.md"),
                        {"out": fs["AB"], "pdf": fs["pdf"], "motivo": motivo[:12000]}, cwd=d,
                        tope=min(STEP_BUDGET["correccion"], self.a.budget - self.gasto - STEP_BUDGET["cobertura"]))
        except Alto as e:
            log(f"   corrección {ronda}: {str(e)[:160]}")
        v = run([sys.executable, os.path.join(AQUI, "validar_canon.py"), fs["AB"], fs["tools"]], d, check=False)
        if v.returncode != 0:
            raise Alto(f"la corrección {ronda} dejó el canon fuera de esquema: {v.stdout.strip()[-400:]}")
        shutil.copy2(fs["AB"], canon_ab)

    def calcular(self, canon):
        k = self.k
        c4 = os.path.join(k, "etapas", "4_canon")
        self.tool("canon.py", canon, os.path.join(c4, "out"), "--fo", os.path.join(c4, "fo_in.json"))
        self.tool("inventario.py", canon, os.path.join(c4, "out", "inventario_out.json"))
        self.tool("framed_openings.py", os.path.join(c4, "fo_in.json"), os.path.join(c4, "out", "framed_openings_out.json"))
        self.tool("alcance_filtro.py", os.path.join(c4, "alcance_in.json"), os.path.join(c4, "out", "alcance_out.json"))
        if self.a.sealer:                       # sello closer.py + evidencia planmark.py (script del proyecto, textos de exclusión propios)
            dst = os.path.join(k, "scripts", os.path.basename(self.a.sealer))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(self.a.sealer, dst)
            run([sys.executable, os.path.join(self.t, "bitacora.py"), "run", dst, self.t, os.path.abspath(self.a.pdf)], k, self.env)
        self.tool("vigas_sobre_walls.py", os.path.abspath(self.a.pdf), "NONE", self.a.plan_sheet, canon, "--json",
                  os.path.join(c4, "vigas_out.json"))
        self.tool("markups_bluebeam.py", os.path.abspath(self.a.pdf), canon, os.path.join(k, "etapas", "6_markups", "markups.pdf"),
                  "--json", os.path.join(k, "etapas", "6_markups", "markups.json"))
        log("8/11 canon.py + tools OK (los números salen de los programas)")

    def excel(self):
        x = os.path.join(self.k, "etapas", "8_excel", "Takeoff_runner.xlsx")
        self.tool("plantilla_excel.py", "validar", "takeoff.json")
        p = self.tool("plantilla_excel.py", "armar", "takeoff.json", x, "--familias", "etapas/4_canon/out/familias_out.json",
                      "--trabajo", "etapas", check=False)
        if p.returncode != 0 or not os.path.exists(x):
            raise Alto("plantilla_excel armar NO armó (compuerta reglas.py dentro): ver etapas/REGLAS_FALLAS.md\n"
                       + (p.stdout + p.stderr)[-800:])
        self.tool("registro.py", "entregable", "registro.json")
        self.tool("alcances.py", "compuerta", "registro.json", "escaneo.json", x)
        r = self.tool("reglas.py", "compuerta", "etapas", "--excel", x, check=False)
        fallas = [l for l in r.stdout.splitlines() if l.startswith("FALLA")]
        # La única falla aceptada antes de entregar es la del back-check (paso humano / agente posterior, R80e.30);
        # cualquier otra detiene el runner.
        otras = [l for l in fallas if "back-check" not in l.lower() and "BACK-CHECK" not in l]
        if otras:
            raise Alto("reglas.py compuerta con fallas:\n" + "\n".join(otras[:20]))
        log(f"9/11 Excel armado; reglas.py: {len(fallas)} falla(s) = back-check pendiente" if fallas else "9/11 Excel armado; reglas.py OK")
        return x, len(fallas)

    def comparar_excel(self, x):
        if not self.a.compare_with:
            return None
        import openpyxl
        def load(p):
            wb = openpyxl.load_workbook(p, data_only=True)
            return {s: [list(r) for r in wb[s].iter_rows(values_only=True)] for s in wb.sheetnames if not s.startswith("_")}
        a, b = load(self.a.compare_with), load(x)
        res = {}
        for s in a:
            A, B = a[s], b.get(s, [])
            n = 0
            for i in range(max(len(A), len(B))):
                ra = A[i] if i < len(A) else []
                rb = B[i] if i < len(B) else []
                n += sum(1 for j in range(max(len(ra), len(rb)))
                         if (ra[j] if j < len(ra) else None) != (rb[j] if j < len(rb) else None))
            res[s] = n
        ms = lambda t: {r[0]: r[2] for r in t["Material Summary"][3:] if r and r[0]}
        ma, mb = ms(a), ms(b)
        res["material_summary_rows"] = (len(ma), len(mb))
        res["material_summary_net_diffs"] = [(k, ma.get(k), mb.get(k)) for k in sorted(set(ma) | set(mb), key=str)
                                            if ma.get(k) != mb.get(k)]
        log(f"10/11 comparación contra la referencia: {res}")
        return res

    def cobertura(self, x):
        """Paso 12 reducido: la lectura lista detalles / notas del trade con su destino; cobertura.py verifica."""
        lista = os.path.join(self.k, "etapas", "5_auditoria", "cobertura_lista.json")
        if self.a.dry_run:
            if not self.a.cobertura_lista:
                log("11/11 cobertura: sin --cobertura-lista en dry-run (omitida)")
                return None
            shutil.copy2(self.a.cobertura_lista, lista)
            self.costo("cobertura")
        else:
            d, f = self.sandbox("cobertura", {"pdf": os.path.abspath(self.a.pdf), "x": x})
            o = os.path.join(d, "cobertura_lista.json")
            self.claude("cobertura", os.path.join(AQUI, "prompts", "cobertura.md"), {"pdf": f["pdf"], "out": o, "excel": f["x"]}, cwd=d)
            if not os.path.exists(o):
                raise Alto("la cobertura no escribió la lista")
            shutil.copy2(o, lista)
        out = os.path.join(self.k, "etapas", "5_auditoria", "cobertura")
        p = run([sys.executable, os.path.join(AQUI, "cobertura.py"), lista,
                 os.path.join(self.k, "etapas", "4_canon", "takeoff_canon.json"), os.path.join(self.k, "takeoff.json"), out], self.k)
        s = json.loads(p.stdout.strip().splitlines()[-1])
        log(f"11/11 cobertura: {s['covered']}/{s['items']} ({s['coverage_pct']} %), {s['gaps']} huecos -> etapas/5_auditoria/cobertura.md")
        return s

    def correr(self):
        self.preparar()
        self.proceso()
        inv = self.inventario_tags()
        A, B = self.lecturas(inv)
        n, rev = self.comparar(A, B, inv)
        canon_ab = self.resolver(A, n, rev)
        for ronda in range(MAX_CORRECCION + 1):
            canon = self.decisiones(canon_ab)
            try:
                self.calcular(canon)
            except Alto as e:                   # canon.py rechaza la lectura con las decisiones: también es lectura
                if self.a.dry_run or ronda == MAX_CORRECCION or "ERROR canon.py" not in str(e):
                    raise
                self.corregir(canon_ab, ronda + 1, texto=[l for l in str(e).splitlines() if "ERROR canon.py" in l][0])
                continue
            try:
                x, nf = self.excel()
                break
            except Alto as e:
                alc = [l for l in str(e).splitlines() if l.startswith("FALLA") and "ALC-" in l]
                if self.a.dry_run or ronda == MAX_CORRECCION or ("reglas" not in str(e) and not alc):
                    raise
                if alc:                         # alcance marcado cuantificado sin cantidad: falta en la LECTURA
                    self.corregir(canon_ab, ronda + 1, texto="\n".join(alc), origen="alcances.py compuerta")
                else:
                    self.corregir(canon_ab, ronda + 1)
        cmp_ = self.comparar_excel(x)
        cob = self.cobertura(x)
        out = {"reconciliacion": {"emparejados": self.emparejados, "sin_objeto": self.sin_objeto},
               "cobertura": cob, "excel": x, "gasto_usd": round(self.gasto, 4), "pasos": self.pasos, "diferencias_AB": n,
               "reglas_fallas_backcheck": nf, "lecturas_no_usadas": getattr(self, "lecturas_no_usadas", []), "comparacion": cmp_, "dry_run": self.a.dry_run}
        json.dump(out, open(os.path.join(self.root, "runner_resultado.json"), "w"), indent=1, ensure_ascii=False, default=str)
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--project-inputs", required=True)
    ap.add_argument("--evidence-root", required=True)
    ap.add_argument("--overlay")
    ap.add_argument("--canon-ref")
    ap.add_argument("--compare-with")
    ap.add_argument("--work", required=True)
    ap.add_argument("--budget", type=float, default=20.0)
    ap.add_argument("--plan-sheet", default="A-101", help="hoja de planta para vigas_sobre_walls.py")
    ap.add_argument("--trade-plan-sheets", help="hojas de planta del trade que deben tener walls (ej. A-101,A-221)")
    ap.add_argument("--ref-base", help="canon de referencia SIN decisiones (ids del estimador) para reconciliar ids")
    ap.add_argument("--cobertura-lista", help="dry-run: lista de detalles / notas del trade con destino (paso 12)")
    ap.add_argument("--sealer", help="script del proyecto que sella con closer.py y marca con planmark.py")
    ap.add_argument("--reusar-lecturas", help="raíz --work de una corrida anterior: reusa sus lecturas ya pagadas")
    ap.add_argument("--reusar-resolucion", help="canon AB de una resolución ya pagada (con --reusar-lecturas)")
    ap.add_argument("--continuar-lados", help="con --reusar-lecturas: lados (A,B) a los que se paga una continuación")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.dry_run and not a.canon_ref:
        ap.error("--dry-run exige --canon-ref")
    try:
        r = Runner(a).correr()
    except Alto as e:
        print("RUNNER DETENIDO:", e)
        return 1
    print(json.dumps(r, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
