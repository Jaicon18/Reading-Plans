#!/usr/bin/env python3
"""registro.py — libro de partidas del take-off (lista maestra que el código protege).

Idea (Anthropic, "Effective harnesses for long-running agents"): al inicio se lista TODO lo
que hay que resolver, cada renglón arranca PENDIENTE, y después solo se puede cambiar el
ESTADO. Nadie puede borrar ni editar renglones, y no se entrega con renglones pendientes.

Estados:  pendiente -> verificado      (con evidencia: hoja+detalle, imagen, sello)
          pendiente -> pendiente_rfi   (con número de RFI y motivo)
          pendiente_rfi -> verificado  (cuando llega la respuesta)
Nunca:    verificado -> otro estado; ni borrar; ni editar id/tipo/ubicación/fuente.
Anexar (v66, #15B ALC-22): a un renglón verificado o pendiente_rfi se le puede AGREGAR evidencia (hojas que faltaba
          citar, corrección de una cita) sin cambiar su estado: queda en el historial como "ANEXO" y se concatena a
          la nota. No borra ni reemplaza la nota anterior.

Uso:
  registro.py crear    <registro.json> <renglones.json>   (solo una vez; falla si ya existe)
  registro.py agregar  <registro.json> <renglones.json>   (renglones NUEVOS hallados después)
  registro.py marcar   <registro.json> <id> verificado "<evidencia>"
  registro.py marcar   <registro.json> <id> pendiente_rfi "<RFI-## motivo>"
  registro.py anexar   <registro.json> <id> "<evidencia adicional>"   (v66: solo verificado / pendiente_rfi)
  registro.py estado   <registro.json>                    (resumen por tipo y por estado)
  registro.py entregable <registro.json>                  (exit 1 si queda algo pendiente)

renglones.json: lista de objetos {"id","tipo","ubicacion","fuente"}; tipo ∈
  wall, tag, detalle, zona_humeda, cielo, soffit, abertura, mep, otro.
"""
import hashlib, json, os, sys, time

ESTADOS = {"pendiente", "verificado", "pendiente_rfi"}
TRANSICIONES = {("pendiente", "verificado"), ("pendiente", "pendiente_rfi"),
                ("pendiente_rfi", "verificado")}
CAMPOS_FIJOS = ("id", "tipo", "ubicacion", "fuente")


class RegistroRoto(Exception):
    """El registro fue alterado por fuera de esta herramienta o una operación es ilegal."""


def _huella(renglon):
    base = json.dumps({k: renglon[k] for k in CAMPOS_FIJOS}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(base.encode()).hexdigest()


def _cadena(renglones):
    h = hashlib.sha256()
    for r in renglones:
        h.update(r["huella"].encode())
    return h.hexdigest()


def _validar_nuevo(r):
    falt = [k for k in CAMPOS_FIJOS if not str(r.get(k, "")).strip()]
    if falt:
        raise RegistroRoto(f"renglón sin {falt}: {r}")


def leer(path):
    with open(path, encoding="utf-8") as f:
        reg = json.load(f)
    vistos = set()
    for r in reg["renglones"]:
        if r["id"] in vistos:
            raise RegistroRoto(f"id duplicado: {r['id']}")
        vistos.add(r["id"])
        if _huella(r) != r["huella"]:
            raise RegistroRoto(f"renglón {r['id']} editado por fuera (huella no coincide)")
        if r["estado"] not in ESTADOS:
            raise RegistroRoto(f"estado inválido en {r['id']}: {r['estado']}")
    if reg["total"] != len(reg["renglones"]) or reg["cadena"] != _cadena(reg["renglones"]):
        raise RegistroRoto("faltan o sobran renglones: alguien borró o reordenó el registro")
    return reg


def _guardar(path, reg):
    reg["total"] = len(reg["renglones"])
    reg["cadena"] = _cadena(reg["renglones"])
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def crear(path, nuevos):
    if os.path.exists(path):
        raise RegistroRoto(f"{path} ya existe: el registro se crea una sola vez")
    reg = {"creado": time.strftime("%Y-%m-%d %H:%M"), "renglones": []}
    _guardar(path, reg)
    return agregar(path, nuevos)


def agregar(path, nuevos):
    reg = leer(path)
    ids = {r["id"] for r in reg["renglones"]}
    for r in nuevos:
        _validar_nuevo(r)
        if r["id"] in ids:
            raise RegistroRoto(f"id ya existe, no se puede re-agregar ni editar: {r['id']}")
        fila = {k: str(r[k]) for k in CAMPOS_FIJOS}
        fila.update(estado="pendiente", nota="", historial=[])
        fila["huella"] = _huella(fila)
        reg["renglones"].append(fila)
        ids.add(fila["id"])
    _guardar(path, reg)
    return reg


def marcar(path, rid, nuevo, nota):
    reg = leer(path)
    if nuevo not in ESTADOS:
        raise RegistroRoto(f"estado inválido: {nuevo}")
    if not nota.strip():
        raise RegistroRoto("marcar exige evidencia (verificado) o RFI y motivo (pendiente_rfi)")
    if nuevo == "pendiente_rfi" and "RFI" not in nota.upper():
        raise RegistroRoto("pendiente_rfi exige el número de RFI en la nota")
    for r in reg["renglones"]:
        if r["id"] == rid:
            if (r["estado"], nuevo) not in TRANSICIONES:
                raise RegistroRoto(f"{rid}: {r['estado']} -> {nuevo} no está permitido")
            r["historial"].append([time.strftime("%Y-%m-%d %H:%M"), r["estado"], nuevo, nota])
            r["estado"], r["nota"] = nuevo, nota
            _guardar(path, reg)
            return r
    raise RegistroRoto(f"id no existe: {rid}")


def anexar(path, rid, texto):
    """v66: agrega evidencia a un renglón ya resuelto sin cambiar su estado (la huella cubre solo CAMPOS_FIJOS)."""
    reg = leer(path)
    if not texto.strip():
        raise RegistroRoto("anexar exige texto (hojas / evidencia adicional)")
    for r in reg["renglones"]:
        if r["id"] == rid:
            if r["estado"] not in ("verificado", "pendiente_rfi"):
                raise RegistroRoto(f"{rid}: anexar solo a verificado / pendiente_rfi (está {r['estado']}; usar marcar)")
            r["historial"].append([time.strftime("%Y-%m-%d %H:%M"), r["estado"], r["estado"], "ANEXO: " + texto])
            r["nota"] = (r["nota"] + " | ANEXO: " + texto).strip()
            _guardar(path, reg)
            return r
    raise RegistroRoto(f"id no existe: {rid}")


def resumen(reg):
    por = {}
    for r in reg["renglones"]:
        por.setdefault(r["tipo"], {e: 0 for e in sorted(ESTADOS)})[r["estado"]] += 1
    tot = {e: sum(1 for r in reg["renglones"] if r["estado"] == e) for e in sorted(ESTADOS)}
    return por, tot


def entregable(reg):
    """Se entrega solo si no queda NINGÚN renglón en 'pendiente' (los pendiente_rfi sí salen,
    declarados en la lista PARA REVISAR)."""
    faltan = [r["id"] for r in reg["renglones"] if r["estado"] == "pendiente"]
    return (not faltan and reg["total"] > 0), faltan


def _cargar(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    a = sys.argv[1:]
    try:
        if len(a) == 3 and a[0] == "crear":
            reg = crear(a[1], _cargar(a[2])); print(f"OK creado: {reg['total']} renglones, todos pendiente")
        elif len(a) == 3 and a[0] == "agregar":
            reg = agregar(a[1], _cargar(a[2])); print(f"OK total: {reg['total']} renglones")
        elif len(a) == 5 and a[0] == "marcar":
            r = marcar(a[1], a[2], a[3], a[4]); print(f"OK {r['id']}: {r['estado']}")
        elif len(a) == 4 and a[0] == "anexar":
            r = anexar(a[1], a[2], a[3]); print(f"OK {r['id']}: {r['estado']} + anexo")
        elif len(a) == 2 and a[0] == "estado":
            por, tot = resumen(leer(a[1]))
            for t, c in sorted(por.items()):
                print(f"{t:14s} " + "  ".join(f"{e}={n}" for e, n in c.items()))
            print("TOTAL          " + "  ".join(f"{e}={n}" for e, n in tot.items()))
        elif len(a) == 2 and a[0] == "entregable":
            ok, faltan = entregable(leer(a[1]))
            if ok:
                print("ENTREGABLE: 0 renglones pendientes"); sys.exit(0)
            print(f"NO ENTREGABLE: {len(faltan)} pendientes: {', '.join(faltan[:30])}"); sys.exit(1)
        else:
            sys.exit(__doc__)
    except RegistroRoto as e:
        print(f"REGISTRO ROTO: {e}"); sys.exit(2)
