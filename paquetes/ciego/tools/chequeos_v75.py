#!/usr/bin/env python3
"""chequeos_v75.py — compuertas v75 (arbitraje #23) sobre el canon. Genéricas: ningún dato de proyecto.

R75.5  Cambio de type sobre una línea recta (R73.10 hecha compuerta). Dos walls con tag distinto en la MISMA banda
       (misma orientación, caras c0 / c1 a ≤ 1.5 pt) que se tocan en una punta (≤ 1 pt) cambian de type en un NODO
       dibujado: la cara de un wall perpendicular que llega a esa línea (T / esquina). Si en ese punto no hay nodo
       (p. ej. el cambio se puso en el jamb de una door: la door quedó cargada al type del otro lado), es error
       salvo `type_change_rfi {alternativas, delta_lf, source}` en uno de los dos walls (PENDIENTE con las dos
       lecturas). Por qué: en una prueba ciega una corrida cortó en el nodo y otra en el jamb; la door pasó de un
       type al otro y los dos types salieron CERCA.
"""
TOL_CARA = 1.5      # pt: misma banda
TOL_PUNTA = 1.0     # pt: se tocan
TOL_NODO = 1.5      # pt: cara del perpendicular en el punto de cambio


def _b(w):
    b = w.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    try:
        return {k: float(b[k]) for k in ("c0", "c1", "lo", "hi")} | {"ori": b["ori"], "sheet": b.get("sheet")}
    except (KeyError, TypeError, ValueError):
        return None


def _tag(w):
    return str(w.get("tag") or "").strip().upper()


def cambios_sin_nodo(walls):
    """[(id1, id2, punto_pt)] de cambios de type colineales sin nodo perpendicular dibujado."""
    ws = [(w, _b(w)) for w in walls if w.get("element", "wall") == "wall" and _tag(w)]
    ws = [(w, b) for w, b in ws if b]
    out = []
    for i, (w1, b1) in enumerate(ws):
        for w2, b2 in ws[i + 1:]:
            if _tag(w1) == _tag(w2) or b1["ori"] != b2["ori"] or b1["sheet"] != b2["sheet"]:
                continue
            if abs(b1["c0"] - b2["c0"]) > TOL_CARA or abs(b1["c1"] - b2["c1"]) > TOL_CARA:
                continue
            p = None
            if abs(b1["hi"] - b2["lo"]) <= TOL_PUNTA:
                p = (b1["hi"] + b2["lo"]) / 2
            elif abs(b2["hi"] - b1["lo"]) <= TOL_PUNTA:
                p = (b2["hi"] + b1["lo"]) / 2
            if p is None:
                continue
            c0, c1 = min(b1["c0"], b2["c0"]), max(b1["c1"], b2["c1"])
            nodo = False
            for w3, b3 in ws:
                if b3["ori"] == b1["ori"] or b3["sheet"] != b1["sheet"]:
                    continue
                cara = min(abs(b3["c0"] - p), abs(b3["c1"] - p)) <= TOL_NODO
                llega = b3["lo"] - TOL_NODO <= c1 and b3["hi"] + TOL_NODO >= c0
                if cara and llega:
                    nodo = True
                    break
            if not nodo and not (w1.get("type_change_rfi") or w2.get("type_change_rfi")):
                out.append((w1["id"], w2["id"], round(p, 2)))
    return out


def verificar_r75_5(canon):
    malos = cambios_sin_nodo(canon.get("walls") or [])
    if malos:
        raise ValueError("R75.5: cambio de type colineal sin nodo dibujado (T / esquina) " +
                         "; ".join(f"{a} / {b} en {p} pt" for a, b, p in malos) +
                         ": corta en la cara del wall perpendicular (la door queda dentro del wall cuyo tag la "
                         "comparte en la línea) o declara type_change_rfi {alternativas, delta_lf, source} (R73.10)")
    return True


# R75.6  Un nicho / alcove (R74.3: grupo sin tag que abre en dos tramos colineales de otra línea) NUNCA es dueño de la
#        esquina con esa línea: sus lados perpendiculares terminan en la cara del wall de la línea y el wall de la línea
#        llega a la cara exterior del lado del alcove. Por qué: el alcove no es wall de la lista; si se queda la esquina,
#        el type de la línea pierde un espesor por punta (en una prueba ciega el type salió CERCA por eso).
def alcove_con_esquina(canon, pt):
    W = {w["id"]: w for w in canon.get("walls") or []}
    out = []
    for o in (pt or {}).get("other_framing") or []:
        if o.get("element") != "alcove":
            continue
        lineas = [_b(W[i]) for i in o.get("abre_en") or [] if i in W and _b(W[i])]
        for i in o.get("ids") or []:
            b = _b(W.get(i, {}))
            if not b:
                continue
            for L in lineas:
                if L["ori"] == b["ori"]:
                    continue
                solape = min(b["hi"], L["c1"]) - max(b["lo"], L["c0"])
                if solape > TOL_PUNTA:
                    out.append((i, round(solape, 2)))
                    break
    return out


# R75.7  Return corto (≤ 2 ft) que sale de un tramo LARGO (> 2 ft) del MISMO wall con tag (furring de monitor): se mide desde la cara
#        EXTERIOR del tramo al que vuelve, como la cota impresa (la cota del return va de cara a cara del contorno).
#        Un return que arranca en la cara interior (cota − espesor) le quita al type un espesor por return; si el
#        plano lo pide así, `return_basis {value: "inner_face", source N/HOJA}` lo declara.
def returns_sin_esquina(canon, pt, corto_ft=2.0, esc=18.0):
    W = {w["id"]: w for w in canon.get("walls") or []}
    out = []
    for x in ((pt or {}).get("types") or {}).values():
        for f in x.get("filas") or []:
            ids = [i for i in f.get("ids") or [] if i in W and _b(W[i])]
            for r in ids:
                br = _b(W[r])
                if (br["hi"] - br["lo"]) / esc > corto_ft or W[r].get("return_basis"):
                    continue
                for m in ids:
                    bm = _b(W[m])
                    if m == r or bm["ori"] == br["ori"] or (bm["hi"] - bm["lo"]) / esc <= corto_ft:
                        continue                    # solo returns de un tramo largo (un box chico de columna no)
                    if not (bm["lo"] - TOL_NODO <= br["c0"] and br["c1"] <= bm["hi"] + TOL_NODO):
                        continue
                    if abs(br["lo"] - bm["c1"]) <= TOL_PUNTA or abs(br["hi"] - bm["c0"]) <= TOL_PUNTA:
                        out.append((r, m))
                        break
    return out


def verificar_v75(canon, pt):
    err = []
    a = alcove_con_esquina(canon, pt)
    if a:
        err.append("R75.6: lado de alcove dueño de la esquina con el wall de su línea " +
                   "; ".join(f"{i} cruza {s} pt la banda" for i, s in a) +
                   ": el lado termina en la cara del wall de la línea y ese wall llega a la cara exterior del alcove")
    r = returns_sin_esquina(canon, pt)
    if r:
        err.append("R75.7: return corto medido desde la cara interior del tramo al que vuelve " +
                   "; ".join(f"{i} (vuelve a {m})" for i, m in r) +
                   ": mídelo desde la cara exterior (= cota impresa del return) o declara return_basis "
                   "{value: 'inner_face', source N/HOJA}")
    if err:
        raise ValueError(" | ".join(err))
    return True
