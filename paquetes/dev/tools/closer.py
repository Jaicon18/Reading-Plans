"""
closer.py — Compuerta de cierre de wall para take-off Metal Frame / Drywall.

NO es una lista de recomendaciones. Es una COMPUERTA: si el cierre no cumple,
emit() lanza CierreRechazado y NO se produce ningun archivo ni tabla.

Cada cantidad que llegue al usuario debe salir de aqui. Un numero escrito fuera
de este modulo NO esta entregado.

Reglas que hace cumplir (todas bloqueantes):
  ESTADO     todo valor lleva CONFIRMADO / DERIVADO / PENDIENTE
  FUENTE     todo CONFIRMADO cita hoja (A##.## / S##.##) y elemento
  OPERACION  todo DERIVADO muestra la operacion
  PENDIENTE  no recibe waste ni entra en compra
  CADENA     toda afirmacion de alcance trae >=2 eslabones citados con hoja
  TRACK      bottom y top en renglones SEPARADOS, y LF total / length == 2
  STUDS      campo = floor(largo_in / OC) + 1, y los adicionales CONTADOS
  CLIPS      = studs_total x lineas_bracing x 2
  BRACING    lineas = floor(height / espaciamiento)
  BOARD      por FACE y por TIPO, con aberturas deducidas
  SILL       una door no lleva sill
  HEADER     v64 (decisión usuario #2): LF = suma (R.O. + 1'-4") x piezas de cada abertura (header
             schedule o detalle del box); una abertura sin piezas con HEADER cuantificado -> rechazo.
             v70 (#18A): header de acero por otros: abertura(..., piezas=0, header="steel_by_others",
             header_source="N/HOJA") = header 0 con fuente (no se rechaza); piezas 0 sin eso -> rechazo
  DUCTO      v64 (decisión usuario #12): clase "ducto" (duct / fire damper) sin header ni sill, sin jambs
  WASTE      metal 15%, board 6%, sobre neto, por tipo
  COMPLETO   las 11 line items presentes o EXCLUIDAS con motivo

Origen: prueba <proyecto>, 18-sep-2026, despues de afirmar que unos detalles
aplicaban sin haber seguido la cadena de referencia.
"""

import hashlib
import json
import math
import re

ESTADOS = ("CONFIRMADO", "DERIVADO", "PENDIENTE")

PARTIDAS_OBLIGATORIAS = (
    "STUD", "TRACK_BOTTOM", "TRACK_TOP", "HEADER", "SILL_TRACK", "BRACING", "CLIPS",
    "BOARD", "INSULATION", "SEALANT", "BLOCKING", "PATCH", "CONTROL_JOINT",
)

# Exclusion de alcance de PROYECTO para la junta de control: el motivo es el mismo en todos
# los muros y se barre el set completo una sola vez. Se aplica sola si el cierre no dijo
# nada, para que ningun muro quede sin el renglon -- pero queda VISIBLE en cada cierre.
# El texto del barrido es DEL PROYECTO (hojas, sitios donde aparece, maximos medidos): va en
# $TAKEOFF_CONTROL_JOINT_MOTIVO. Sin el, sale el motivo generico de abajo, que exige el RFI.
import os as _os_cj
CONTROL_JOINT_PROYECTO = _os_cj.environ.get("TAKEOFF_CONTROL_JOINT_MOTIVO") or (
    "EXCLUDED. Se barre el set completo buscando 'CONTROL JOINT' y 'EXPANSION JOINT' "
    "(abreviaturas, civiles, leyendas de materiales exteriores, schedule de partitions, "
    "detalles de ceilings y specs 09 29 00). Una junta de estuco / plaster (Div 09 24 00) o "
    "de pavimento NO es de gypsum board. Si el set no rotula ni detalla ninguna junta de "
    "control de gypsum board, NO se cuantifica. "
    "RFI: ASTM C840 y GA-216 piden junta de control en paños de gypsum de mas de 30 ft "
    "corridos y en ceilings de mas de 2,500 SF (50 ft sin junta); se compara con el wall "  # [ciego-ok] norma
    "mas largo sin interrupcion y el ceiling de gyp mas grande del proyecto. Se pide "
    "confirmacion por escrito antes del award; si el arquitecto las quiere, se valorizan "
    "como alterno."
)

METAL = ("STUD", "TRACK_BOTTOM", "TRACK_TOP", "HEADER", "BRACING", "CLIPS")
BOARDLIKE = ("BOARD",)

# DEFECTO CORREGIDO 2026-09-27: el patron anterior exigia DOS digitos antes del punto
# (\b[A-Z]{1,2}\d{2}\.\d{2}\b), asi que rechazaba TODA la serie estructural real de este
# set -- S2.20, S5.20, S1.10 -- y cualquier hoja A4.01. Con eso, ningun dato sacado de las
# hojas S podia declararse CONFIRMADO. Ahora acepta las dos numeraciones reales:
#   con punto   A02.01 A12.01 S5.20 S2.20 A4.01 M01.01 P01.02 E02.01
#   con guion   A-410 A-101 S-201   (exactamente 3 digitos, para no tragarse codigos
#                                    de material como P-nn, GL-n, B-nn, TS-n, CT-nnX)
RE_HOJA = re.compile(r"\b[A-Z]{1,2}(?:\d{1,3}\.\d{1,2}|-\d{3})\b")
RE_DET = re.compile(r"\b\d{1,2}/[A-Z]{1,2}(?:\d{1,3}\.\d{1,2}|-\d{3})\b")
RE_NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}(?:\d{1,3}\.\d{1,2}|-\d{3})\b")   # v70: 7/S5.20, J/A09.23


class CierreRechazado(Exception):
    """El cierre no cumple. No se emitio nada."""


class Val:
    """Un numero con su estado y su backing. Sin backing no se construye."""

    def __init__(self, v, estado, fuente=None, operacion=None, unidad=None):
        if estado not in ESTADOS:
            raise CierreRechazado(f"estado invalido '{estado}' (v={v})")
        if estado == "CONFIRMADO":
            if not fuente or not RE_HOJA.search(fuente):
                raise CierreRechazado(
                    f"CONFIRMADO sin hoja citada: v={v} fuente={fuente!r}. "
                    f"Debe citar hoja tipo A02.01 / S5.20 y el elemento.")
        if estado == "DERIVADO":
            if not operacion or len(operacion) < 5:
                raise CierreRechazado(
                    f"DERIVADO sin operacion escrita: v={v}. Muestra el calculo.")
        if estado == "PENDIENTE" and v not in (None, 0):
            raise CierreRechazado(
                f"PENDIENTE no puede traer valor ({v}). Un pendiente no se cuantifica.")
        self.v, self.estado, self.fuente = v, estado, fuente
        self.operacion, self.unidad = operacion, unidad

    def __repr__(self):
        return f"{self.v}[{self.estado}]"

    def as_dict(self):
        return {"v": self.v, "estado": self.estado, "fuente": self.fuente,
                "operacion": self.operacion, "unidad": self.unidad}


class Cara:
    def __init__(self, nombre, alto_board: Val, board_tipo, capas):
        if not nombre:
            raise CierreRechazado("face sin nombre de cuarto")
        if capas < 1:
            raise CierreRechazado(f"face {nombre}: layers invalidas")
        self.nombre, self.alto, self.tipo, self.capas = nombre, alto_board, board_tipo, capas


HEADERS = ("metal", "steel_by_others")


class Abertura:
    def __init__(self, clase, ref, w_ft, h_ft, head=None, sill=None, piezas=None, header="metal",
                 header_source=None):
        if clase not in ("puerta", "ventana", "pass-through", "hueco", "ducto"):
            raise CierreRechazado(f"clase de abertura desconocida: {clase}")
        if clase == "ducto":
            if head or sill or piezas:
                raise CierreRechazado(
                    f"ducto {ref}: duct / fire damper NO se enmarca — sin header ni sill (decisión usuario #12).")
        else:
            if clase == "puerta" and sill:
                raise CierreRechazado(
                    f"door {ref}: lleva SILL ({sill}). Una door lleva header, nunca sill.")
            if not head:
                raise CierreRechazado(f"abertura {ref}: sin referencia de head/header.")
        if header not in HEADERS:
            raise CierreRechazado(f"abertura {ref}: header debe ser {' | '.join(HEADERS)} (vino {header!r})")
        if header == "steel_by_others":
            # v70: lintel / HSS de acero por otros (estructural): 0 piezas de metal stud header, con su fuente
            if not RE_NHOJA.search(str(header_source or "")):
                raise CierreRechazado(f"abertura {ref}: header steel_by_others sin header_source N/HOJA (detalle "
                                      f"estructural que dibuja el acero; v70)")
            if piezas not in (None, 0) or isinstance(piezas, bool):
                raise CierreRechazado(f"abertura {ref}: header steel_by_others lleva piezas=0 (vino {piezas!r})")
            piezas = 0
        elif piezas is not None and (not isinstance(piezas, int) or isinstance(piezas, bool) or piezas < 1):
            raise CierreRechazado(f"abertura {ref}: piezas debe ser entero >= 1 (vino {piezas!r}); 0 piezas solo "
                                  f"con header='steel_by_others' + header_source N/HOJA")
        self.clase, self.ref, self.w, self.h = clase, ref, w_ft, h_ft
        self.head, self.sill, self.piezas = head, sill, piezas
        self.header, self.header_source = header, header_source


class Wall:
    def __init__(self, num, tag, ubicacion):
        if not isinstance(num, int):
            raise CierreRechazado("el wall necesita su numero OFICIAL (int)")
        if not tag or not ubicacion:
            raise CierreRechazado(f"wall #{num}: falta tag o ubicacion")
        self.num, self.tag, self.ubicacion = num, tag, ubicacion
        self.largo = None
        self.alto_stud = None
        self.oc = None
        self.brace_sp = None
        self.hileras = 1
        self.caras = []
        self.aberturas = []
        self.partidas = {}
        self.excluidas = {}
        self.alcance = []

    # ---------- carga ----------
    def base(self, largo_ft: Val, alto_stud_ft: Val, oc_in, brace_sp_in, hileras=1):
        """rows = numero de ROWS DE STUD del wall.

        Un wall acustico de doble row (p. ej. dos rows de 1 5/8" con
        Soundguard isolator entre ellas) lleva DOS juegos de track y DOS rows de
        studs, o sea 4 runs de track, no 2. Antes esto era incerrable: la compuerta
        exigia 2.00 runs siempre y rechazaba el cierre correcto."""
        if not isinstance(hileras, int) or hileras < 1:
            raise CierreRechazado("rows invalidas: %r (entero >=1)" % (hileras,))
        self.largo, self.alto_stud = largo_ft, alto_stud_ft
        self.oc, self.brace_sp = oc_in, brace_sp_in
        self.hileras = hileras
        return self

    def cara(self, nombre, alto_board: Val, board_tipo, capas=1):
        self.caras.append(Cara(nombre, alto_board, board_tipo, capas))
        return self

    def abertura(self, clase, ref, w_ft, h_ft, head=None, sill=None, piezas=None, header="metal",
                 header_source=None):
        """w_ft = R.O.; piezas = piezas del header (header schedule o detalle del box, decisión usuario #2).
        v70: header='steel_by_others' + header_source N/HOJA -> piezas 0 (header de acero por otros)."""
        self.aberturas.append(Abertura(clase, ref, w_ft, h_ft, head, sill, piezas, header, header_source))
        return self

    @staticmethod
    def _key(nombre):
        """Mayusculiza solo el prefijo de line item; conserva el nombre del cuarto."""
        if ":" in nombre:
            pre, suf = nombre.split(":", 1)
            return pre.strip().upper() + ":" + suf.strip()
        return nombre.strip().upper()

    # Una cita legible por maquina: `6/A12.01`, `D/A9.22`, `11/S5.10`. La hoja admite 1 o 2
    # digitos antes del punto, porque la serie estructural se escribe S5.20, no S05.20.
    RE_CITA = re.compile(r'(?:\d{1,2}|[A-Z])\s*/\s*[A-Z]{1,2}\d{1,2}\.\d{2}')

    def partida(self, nombre, val: Val, unidad, formula=None):
        # TODA PARTIDA CITA HOJA + DETALLE (orden de Rodolfo, 2-oct-2026: "nunca dejes de usar
        # los detalles y cita la hoja y los detalles").
        #
        # Antes la hoja se exigia SOLO a CONFIRMADO; a DERIVADO le bastaba escribir la
        # operacion. Por ese hueco salio el track de la marquesina -- <n> LF, DERIVADO,
        # `fuente: None` -- un numero legal para la compuerta y sin ningun detalle detras.
        # Una derivacion tambien descansa sobre algo DIBUJADO, y eso tiene hoja y numero.
        #
        # Y la cita tiene que ser legible por maquina: "la seccion del este" en prosa no
        # sirve, porque una cita que una maquina no puede leer no se puede auditar.
        if val.estado != 'PENDIENTE':
            texto = ' '.join(str(x) for x in (val.fuente, val.operacion, formula) if x)
            if not self.RE_CITA.search(texto):
                raise CierreRechazado(
                    f"line item '{nombre}' ({val.estado}) sin cita de HOJA+DETALLE legible. "
                    f"Se exige la forma N/HOJA (6/A12.01, D/A9.22, 11/S5.20) en la fuente o "
                    f"dentro de la operacion. Si de verdad no hay detalle que la gobierne, "
                    f"dilo en la operacion y abre el RFI -- pero no se sella sin cita.")
        self.partidas[self._key(nombre)] = {"val": val, "unidad": unidad, "formula": formula}
        return self

    def excluir(self, nombre, motivo):
        if not motivo or len(motivo) < 15:
            raise CierreRechazado(
                f"EXCLUDED '{nombre}' sin motivo detallado. Di que buscaste, donde, y por que no aplica.")
        self.excluidas[self._key(nombre)] = motivo
        return self

    def afirmar_alcance(self, afirmacion, cadena):
        if not isinstance(cadena, (list, tuple)) or len(cadena) < 2:
            raise CierreRechazado(
                f"alcance '{afirmacion}': cadena de {len(cadena) if cadena else 0} eslabon(es). "
                f"Se exigen >=2: origen -> referencia -> destino.")
        citados = [c for c in cadena if RE_HOJA.search(str(c)) or RE_DET.search(str(c))]
        if len(citados) < 2:
            raise CierreRechazado(
                f"alcance '{afirmacion}': la cadena no cita hoja en al menos 2 eslabones. "
                f"cadena={cadena}")
        self.alcance.append({"afirmacion": afirmacion, "cadena": list(cadena)})
        return self

    # ---------- compuerta ----------
    def _fallos(self):
        F = []
        if self.largo is None or self.alto_stud is None:
            F.append("falta base(): length y alto de stud")
            return F
        if self.oc is None or self.brace_sp is None:
            F.append("falta O.C. de stud o espaciamiento de bracing")
        if not self.caras:
            F.append("el wall no tiene ni una face definida")

        # 1. completitud de partidas (admite renglones por cara: "BOARD:<cuarto>")
        def prefijos(d):
            return {k.split(":", 1)[0] for k in d}
        def _at2(a, k):
            return a.get(k) if isinstance(a, dict) else getattr(a, k, None)
        if "CONTROL_JOINT" not in prefijos(self.partidas) | prefijos(self.excluidas):
            self.excluidas["CONTROL_JOINT"] = CONTROL_JOINT_PROYECTO
        if "SILL_TRACK" not in prefijos(self.partidas) | prefijos(self.excluidas):
            if not [a for a in self.aberturas if _at2(a, "sill")]:
                self.excluidas["SILL_TRACK"] = (
                    "EXCLUDED. A sill track only exists under an opening that HAS a sill "
                    "(window, pass-through, or a framed opening with supported equipment). "
                    "This wall has no opening with a sill declared: %s. Inviolable rule: "
                    "doors carry a header and do NOT carry a sill."
                    % ('it has no openings' if not self.aberturas else
                       'its openings are ' + ', '.join(
                           '%s (%s)' % (_at2(a, 'ref'), _at2(a, 'clase'))
                           for a in self.aberturas)))
        pres = prefijos(self.partidas) | prefijos(self.excluidas)
        for p in PARTIDAS_OBLIGATORIAS:
            if p not in pres:
                F.append(f"line item {p}: ni cuantificada ni EXCLUDED. El wall no esta cerrado.")

        # 1-bis. una abertura CON antepecho obliga a su SILL_TRACK cuantificado
        def _at(a, k):
            return a.get(k) if isinstance(a, dict) else getattr(a, k, None)
        con_sill = [a for a in self.aberturas if _at(a, "sill")]
        if con_sill and "SILL_TRACK" not in prefijos(self.partidas):
            F.append("hay %d abertura(s) con sill declarado (%s) y SILL_TRACK no esta "
                     "cuantificado. Una abertura con sill SIEMPRE lleva su sill track."
                     % (len(con_sill), ', '.join(str(_at(a, 'ref')) for a in con_sill)))

        # 2. track en renglones separados y 2 corridas
        tb = self.partidas.get("TRACK_BOTTOM")
        tt = self.partidas.get("TRACK_TOP")
        if tb and tt:
            if tb["val"].estado != "PENDIENTE" and tt["val"].estado != "PENDIENTE":
                tot = (tb["val"].v or 0) + (tt["val"].v or 0)
                if self.largo.v:
                    corridas = tot / self.largo.v
                    esperado = 2.0 * self.hileras
                    # v62 (#12B): cada LF viene redondeado a 0.01 -> el cociente puede errar 0.01 / L por
                    # renglón; un stub corto daba 4.02 vs 4.00 y se rechazaba con tolerancia fija 0.02.
                    tol = 0.02 + 0.02 / max(self.largo.v, 0.01)
                    if abs(corridas - esperado) > tol + 1e-9:
                        F.append(f"TRACK: LF total {tot:.2f} / length {self.largo.v:.2f} "
                                 f"= {corridas:.2f} runs. Con {self.hileras} row(s) "
                                 f"de stud debe dar {esperado:.2f}.")
        elif "TRACK_BOTTOM" in self.partidas and "TRACK_TOP" in self.partidas:
            pass
        if "TRACK" in self.partidas:
            F.append("TRACK combinado en un solo renglon. Bottom y top van SEPARADOS.")

        # 3. studs de campo
        st = self.partidas.get("STUD")
        if st and st["val"].estado != "PENDIENTE" and self.oc and self.largo.v:
            enmarcadas = [a for a in self.aberturas if a.clase != "ducto"]
            # v68 (#16A): los studs de campo que caen DENTRO del R.O. no existen (studs_nodos los descuenta y suma
            # jambs + cripples aparte); el mínimo los descuenta: floor(R.O. x 12 / O.C.) por abertura.
            dentro = sum(math.floor((a.w or 0) * 12 / self.oc) for a in enmarcadas)
            campo = max(1, math.floor(self.largo.v * 12 / self.oc) + 1 - dentro)
            esperado = campo * self.hileras
            adic = 4 * len(enmarcadas) * self.hileras
            if st["val"].v is not None and st["val"].v < esperado:
                F.append(f"STUD: {st['val'].v} < campo minimo {esperado} "
                         f"= (floor({self.largo.v:.2f}ft x12 / {self.oc}) + 1 - {dentro} dentro de R.O.) "
                         f"x {self.hileras} row(s).")
            if enmarcadas and st["val"].v is not None and st["val"].v < esperado + adic:
                F.append(f"STUD: hay {len(enmarcadas)} abertura(s) = {adic} jamb studs "
                         f"que deben SUMARSE (min {esperado + adic}), no solo advertirse.")

        # 4. bracing y clips
        br = self.partidas.get("BRACING")
        cl = self.partidas.get("CLIPS")
        lineas = None
        if self.brace_sp and self.alto_stud.v:
            lineas = math.floor(self.alto_stud.v * 12 / self.brace_sp)
        if cl and cl["val"].estado != "PENDIENTE" and st and lineas is not None:
            if st["val"].v is not None and cl["val"].v is not None:
                esperado_cl = st["val"].v * lineas * 2
                if cl["val"].v != esperado_cl:
                    F.append(f"CLIPS: {cl['val'].v} != studs {st['val'].v} x lineas {lineas} x 2 "
                             f"= {esperado_cl}.")
        if br and br["val"].estado != "PENDIENTE" and lineas == 0:
            F.append("BRACING cuantificado pero floor(height/espaciamiento) = 0 lineas.")

        # 5. board POR CARA cuando las caras tienen alturas o tipos distintos
        bd_rows = [k for k in self.partidas if k.split(":", 1)[0] == "BOARD"]
        alturas = {c.alto.v for c in self.caras if c.alto.v is not None}
        tipos = {c.tipo for c in self.caras}
        if bd_rows and (len(alturas) > 1 or len(tipos) > 1) and len(bd_rows) < max(len(alturas), len(tipos)):
            F.append(f"BOARD en {len(bd_rows)} renglon(es) pero las faces difieren "
                     f"(alturas {sorted(alturas)}, tipos {sorted(tipos)}). "
                     f"El board va POR FACE: un renglon por face, nombrado BOARD:<cuarto>.")
        for k in bd_rows:
            if ":" in k:
                cuarto = k.split(":", 1)[1]
                if cuarto not in [c.nombre for c in self.caras]:
                    F.append(f"{k}: '{cuarto}' no es ninguna de las faces declaradas.")

        # 6. sill en puertas
        for a in self.aberturas:
            if a.clase == "puerta" and a.sill:
                F.append(f"door {a.ref}: lleva sill. Solo header.")

        # 7. pendientes no entran en compra
        for n, p in self.partidas.items():
            if p["val"].estado == "PENDIENTE" and p["val"].v:
                F.append(f"{n}: PENDIENTE con valor. Un pendiente no se cuantifica ni se compra.")

        # 7-bis. HEADER por piezas (decisión usuario #2, 2026-10-16)
        hd = self.partidas.get("HEADER")
        con_head = [a for a in self.aberturas if a.clase != "ducto"]
        if hd and hd["val"].estado != "PENDIENTE" and hd["val"].v and con_head:
            sin = [a.ref for a in con_head if a.piezas is None]
            if sin:
                F.append(f"HEADER cuantificado y abertura(s) sin piezas: {sin}. LF = (R.O. + 1'-4\") x piezas del "
                         f"header schedule o del detalle del box (decisión usuario #2).")
            else:
                esp = sum((a.w + 16.0 / 12.0) * a.piezas for a in con_head)
                if abs(hd["val"].v - esp) > 0.05:
                    F.append(f"HEADER {hd['val'].v} != suma (R.O. + 1'-4\") x piezas = {esp:.2f} "
                             f"(decisión usuario #2).")

        # 8. cada partida con su formula cuando es DERIVADO
        for n, p in self.partidas.items():
            if p["val"].estado == "DERIVADO" and not (p["val"].operacion or p["formula"]):
                F.append(f"{n}: DERIVADO sin operacion escrita.")
        return F

    def emit(self, out_path=None):
        F = self._fallos()
        if F:
            raise CierreRechazado(
                f"WALL #{self.num} ({self.tag}) RECHAZADO — {len(F)} fallo(s):\n  - "
                + "\n  - ".join(F)
                + "\n>> No se emitio ninguna cantidad.")
        d = {
            "muro": self.num, "tag": self.tag, "ubicacion": self.ubicacion,
            "largo": self.largo.as_dict(), "alto_stud": self.alto_stud.as_dict(),
            "oc": self.oc, "brace_sp": self.brace_sp, "hileras": self.hileras,
            "caras": [{"cuarto": c.nombre, "alto_board": c.alto.as_dict(),
                       "tipo": c.tipo, "capas": c.capas} for c in self.caras],
            "aberturas": [{"clase": a.clase, "ref": a.ref, "w": a.w, "h": a.h,
                           "head": a.head, "sill": a.sill, "piezas": a.piezas, "header": a.header,
                           "header_source": a.header_source} for a in self.aberturas],
            "partidas": {k: {**{kk: vv for kk, vv in v.items() if kk != "val"},
                             "val": v["val"].as_dict()} for k, v in self.partidas.items()},
            "excluidas": self.excluidas,
            "alcance": self.alcance,
        }
        blob = json.dumps(d, sort_keys=True, ensure_ascii=False).encode()
        d["sello"] = hashlib.sha256(blob).hexdigest()[:16]
        if out_path:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
        return d


# ---------------------------------------------------------------------------------------
# `round()` DE PYTHON NO REDONDEA COMO LA OBRA (10-oct-2026).
# Hace banker's rounding (el .5 va al par: round(0.125,2)=0.12) y ademas muchos decimales no
# son exactos en binario: 1.15 x 9.50 da 10.925, y round() lo baja a 10.92 porque el valor
# real es 10.9249999... El estimador que recalcule 1.15 x 9.50 a mano escribe 10.93 y no le
# cuadra el sello por un centesimo -- y un centesimo que no cuadra obliga a rehacer la
# verificacion entera para descubrir que no era nada.
#
# > Una cantidad sellada tiene que poder recalcularse A MANO y dar lo mismo. Se redondea
# > HALF-UP, como en obra, no como el default de Python.
#
# Se aplica en los closers nuevos. Los cierres viejos NO se tocan en bloque: cambiar el
# redondeo de golpe moveria centesimas en cantidades ya entregadas sin que nadie lo pida, y
# eso se decide a proposito, no de pasada.
def r2(x, n=2):
    """Redondeo HALF-UP a n decimales, el de la obra."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal('1').scaleb(-n)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def waste(neto, clase, metal_pct=0.15, board_pct=0.06):
    """Waste sobre NETO. Nunca sobre pendientes ni sobre fasteners."""
    if clase.upper() in METAL:
        p = metal_pct
    elif clase.upper() in BOARDLIKE:
        p = board_pct
    else:
        raise CierreRechazado(f"clase '{clase}' sin porcentaje de waste definido")
    return {"NETO": round(neto, 2), "DESPERDICIO": round(neto * p, 2),
            "COMPRA": round(neto * (1 + p), 2), "pct": p}
