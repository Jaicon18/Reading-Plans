#!/usr/bin/env python3
"""reglas_clasificacion.py — v72b: la decisión de CADA regla del catálogo (reglas_catalogo.py): tipo a / b / c.

  a  → "chequeos": funciones de reglas.py (CHEQUEOS) que la verifican con datos;
  b  → "spec": evidencia por caso (SPECS: qué casos dispara, de qué campos del canon sale la evidencia, qué cita
       exige: HOJA, N/HOJA o archivo, y qué valor la contradice) + chequeos (a) extra si los hay;
  c  → "fusion": la regla vigente que la contiene (fusionada / redundante) o la que la anuló. Nunca se borra el texto.

La decisión se toma por id explícito (E1, R72.1, REGLA 53.2 …) o, para las viñetas sin id, por la sección y una
palabra clave del texto (ver REGLAS_TEXTO). Una regla que nada clasifica queda SIN CLASIFICAR y la compuerta falla
(test_reglas.py también): toda regla nueva del SKILL entra con su chequeo o no se entrega.
"""
import re

A_OJO_RX = r"a ojo|eyeball|by eye|~\s?\d|approx\.?\s?\d|aprox\.?\s?\d"

# ------------------------------------------------------------------------------------------------ specs (b)
SPECS = {
    "G_PROCESO": dict(trigger="corrida", cita="archivo",
                      pide="archivo que muestra cómo se cumplió en esta corrida (o 'NO APLICA: <motivo>')"),
    "G_LARGO": dict(trigger="walls_medidos", src=["length_source"], img=["img"], valor=["length_op", "length_source"],
                    prohibido=A_OJO_RX + r"|p[ií]xel(?!.{0,40}calibr)",
                    pide="largo medido en vector / cota impresa, con su operación (faces lw alto, END CAP, cara del "
                         "wall que recibe)"),
    "G_BASE": dict(trigger="walls", src=["length_source"], img=["img"], valor=["length_basis", "length_source"],
                   requerido=r"face|cent|\bCL\b|c/c|stud_cl|\beje\b|axis",
                   pide="base del LF declarada: face a face o centro a centro / eje"),
    "G_THICK": dict(trigger="walls_medidos", src=["length_source"], img=["img"],
                    valor=["thickness_check", "thickness_measured_info"],
                    pide="thickness medido entre las dos faces = WALL THICKNESS del schedule (autoverifica el tag)"),
    "G_CADENA": dict(trigger="walls_cadena", src=["length_source"], img=["img"], valor=["length_op", "length_source"],
                     requerido=r"tick|simple|doble|single|double",
                     pide="tipo de ticks (SIMPLES / DOBLES) de la cadena sumada y su total"),
    "G_ALTO": dict(trigger="walls_alto", src=["height_source"], img=["height_img", "img"],
                   valor=["height_op", "height_source"], prohibido=A_OJO_RX,
                   pide="altura con su cadena: B.O.D. de la zona (marcadores contados), peralte, pendiente"),
    "G_TIPO": dict(trigger="walls", cita="nhoja", src=["detail", "detail_source", "type_source"],
                   img=["detail_img", "img"], valor=["source_chain", "detail_source", "type_source", "detail"],
                   pide="cadena tag → schedule → detalle del tipo (N/HOJA)"),
    "G_GAUGE": dict(trigger="walls", cita="hoja", src=["gauge_source", "oc_source", "stud_source"],
                    img=["stud_img", "detail_img", "img"], valor=["gauge", "oc_in"],
                    pide="calibre y O.C. del plano (la nota del detalle manda sobre el schedule general)"),
    "G_TOPTRACK": dict(trigger="walls", cita="nhoja", src=["to_deck_source", "detail_source", "detail"],
                       img=["detail_img", "img"], valor=["to_deck_source", "top_track"],
                       pide="condición del top track del tipo (slip / fijo / cap) con su detalle y el gap"),
    "G_2ROW": dict(trigger="walls_2row", cita="nhoja", src=["rows_source"], img=["detail_img", "img"],
                   valor=["rows_source"], pide="doble row con su detalle (dos juegos de track y studs)"),
    "G_CARA": dict(trigger="faces", src=["height_source", "length_source", "_wall.height_source"],
                   img=["img", "_wall.img"], valor=["room"],
                   pide="room que mira la face (verificado), board, layers y alto por face"),
    "G_IMG": dict(trigger="walls", src=["length_source", "source"], img=["img"], valor=["img"],
                  pide="imagen circulada, reabierta, de cada wall"),
    "G_ABERTURA": dict(trigger="openings", src=["ro_source", "ro_w_source", "source"], img=["img"],
                       valor=["ro_op", "ro_w_op", "ro_w_txt", "ro_w_ft"],
                       pide="R.O. impreso o medido entre jambs (nunca tecleado), cada abertura con su ancho"),
    "G_BANDAS": dict(trigger="openings_headed", src=["head_source", "sill_source", "source"], img=["img"],
                     valor=["head_ft"], pide="las dos bandas: head (arriba hasta ceiling / deck) y sill (abajo)"),
    "G_EXT_AB": dict(trigger="openings_ext", src=["jamb_return_source", "source"], img=["img"], valor=["jamb_return"],
                     pide="abertura exterior desde el storefront frame (R.O., sill, knee wall, returns)"),
    "G_CEILING": dict(trigger="ceilings", src=["height_source", "source"], img=["img"], valor=["system", "legend"],
                      pide="ceiling leído cuarto por cuarto en el RCP (tag con su leader, altura, sistema)"),
    "G_SOFFIT": dict(trigger="soffits", cita="nhoja", src=["detail", "source"], img=["img"],
                     valor=["detail", "source"], pide="soffit con TODOS sus detalles abiertos y citados"),
    "G_CAJA": dict(trigger="cajas", cita="nhoja", src=["faces_ft_source", "source", "detail"], img=["img"],
                   valor=["fos_chain", "faces_ft", "parts"], pide="caja con su cadena FOS / caras impresas por capa"),
    "G_PARAPET": dict(trigger="parapets", src=["length_source", "source"], img=["img"], valor=["line"],
                      pide="parapet por grid line, extensión leída en las cuatro elevaciones"),
    "G_FACADE": dict(trigger="facades", src=["source", "elevation_source"], img=["img"], valor=["elevation_check"],
                     requerido=r"callout|arrow|flecha|grid|content|contenido",
                     pide="elevación verificada con las cuatro: callout en planta, flecha, orden de grids, contenido"),
    "G_DETALLE": dict(trigger="details", cita="nhoja", src=["source", "layers_source"], img=["img"],
                      valor=["layers_per_face", "title", "notes"],
                      pide="detalle abierto y leído completo (cuerpo, notas, detalles que llama)"),
    "G_DET_SEALANT": dict(trigger="details", cita="nhoja", src=["sealant.source", "source"], img=["img"],
                          valor=["sealant", "sealant_none_reason"],
                          pide="corridas de sealant top / bottom × caras dibujadas en el detalle (beads)"),
    "G_BLOCKING": dict(trigger="blocking", cita="hoja", src=["source"], img=["img"], valor=["label", "material"],
                       pide="blocking con el rótulo literal del detalle / nota y su ubicación"),
    "G_MEP": dict(trigger="mep", src=["source"], img=["img"], valor=["method", "manual"],
                  pide="cruce de mep.cruces (sobresale ≥ 3 pt de las dos caras) o manual {motivo, img}"),
    "G_WET": dict(trigger="wet", src=["back_source"], img=["img"], valor=["kind"],
                  pide="fixture con su respaldo en el plano ampliado (censo por cuarto, tres fuentes)"),
    "G_TILE": dict(trigger="tile_base", src=["source"], img=["img"], valor=["perimeter_ft"],
                   pide="perímetro de acabado del cuarto con todas sus doors"),
    "G_SEALANT": dict(trigger="sealant", cita="nhoja", src=["source"], img=["img"], valor=["faces", "runs", "lf", "kind"],
                      pide="sealant de CADA tipo con su detalle"),
    "G_TRIM": dict(trigger="trim", cita="hoja", src=["source"], img=["img"], valor=["kind", "label", "lf"],
                   pide="metal trim con su callout o criterio 53.1"),
    "G_RFI": dict(trigger="rfis", src=["source"], img=["img"], valor=["fuentes_revisadas", "sources_checked"],
                  pide="las cuatro fuentes agotadas antes del RFI (designación, otra fila, regla estándar, detalle)"),
    "G_PENDIENTE": dict(trigger="pendientes", src=["length_source", "height_source", "source"], img=["img"],
                        valor=["pending_reason", "sheets_searched"],
                        pide="hojas recorridas antes de declarar faltante (Regla #3)"),
    "G_OTROS": dict(trigger="otros_framing", src=["height_source", "source"], img=["img"],
                    valor=["height_op", "height_source"], pide="altura del HOLD / detalle propio del elemento"),
    "G_EXCL": dict(trigger="excluidos", src=["source"], img=["img"], valor=["reason", "motivo"],
                   pide="exclusión con razón detallada (qué se buscó y dónde)"),
    "G_VENDOR": dict(trigger="vendor_ends", cita="nhoja", src=["source", "jamb_detail"], img=["img"],
                     valor=["jamb_detail", "accessories"], pide="jamb detail del vendor_end y sus accesorios"),
    "G_RECESSED": dict(trigger="recessed", src=["source"], img=["img"], valor=["width_in", "recessed"],
                       pide="un renglón por tag de la leyenda con su ancho (o 0 + RFI)"),
    "G_DEFAULT": dict(trigger="walls_sin_tag", src=["default_type_source", "untagged_reason", "length_source"],
                      img=["img"], valor=["default_type_source", "untagged_reason", "part_of"],
                      pide="wall sin tag: type por defecto con su nota o return del wall con tag"),
}
for _k, _v in SPECS.items():
    _v["nombre"] = _k


def A(*ch):
    return {"tipo": "a", "chequeos": list(ch)}


def B(spec, *ch):
    return {"tipo": "b", "spec": SPECS[spec], "chequeos": list(ch)}


def C(fusion):
    return {"tipo": "c", "fusion": fusion}


V72 = ("A_R72_1", "A_R72_2", "A_R72_3", "A_R72_5", "A_R72_6", "A_R72_10", "A_R72_11")
OBSOLETA_TOOL = "obsoleta: la tool no viaja en el paquete; el flujo v69 la reemplazó (inventario_tags.py, etapas.py, " \
                "canon.py, mep.py); su regla de fondo está en la regla vigente indicada"

# ------------------------------------------------------------------------------------------------ por id
POR_ID = {
    "E1": A("A_HEADER_LF"), "E2": A("A_HEADER_LF", "A_BOX4"), "E3": A("A_PARAPET", "A_VIGENCIA"),
    "E4": A("A_HANGER"), "E5": A("A_BALLISTIC", "A_R72_1"), "E6": A("A_BALLISTIC"), "E7": A("A_TRANSICION"),
    "E8": A("A_WRAP_FOS"), "E9": A("A_TRANSICION"), "E10": A("A_TRACK_RUNS"), "E11": A("A_AS_NEEDED"),
    "E12": A("A_DUCTOS"), "E13": A("A_CANOPY"), "E14": A("A_CEILING_SYS"), "E15": B("G_ABERTURA"),
    "E16": A("A_STOREFRONT"), "E17": B("G_PROCESO"), "E18": A("A_SILL", "A_DOOR_SILL"), "E19": A("A_BOX4"),
    "E20": A("A_BOX4"), "E21": A("A_HEADER_LF", "A_VIGENCIA"), "E22": A("A_RUN_ENDS"), "E23": B("G_RFI", "A_RFI_DELTA"),
    "E24": A("A_CIEGO"), "E25": A("A_FACADES"), "E26": A("A_STOPS_BEAM", "A_R72_4", "A_VIGAS_OUT"),
    "E27": A("A_ESTADO_DIM", "A_FUENTES", "A_VIGENCIA"), "E28": A("A_TAG_IDS", "A_ESQUINAS", "A_EJES", "A_VIGENCIA"),
    "A1": A("A_VIGENCIA"), "A2": A("A_MEP_SWEEP", "A_R72_5", "A_VIGENCIA"), "A3": A("A_R72_11", "A_DUCTOS", "A_VIGENCIA"),
    "A4": A("A_VIGENCIA"), "A5": A("A_JAMB_RETURN", "A_VIGENCIA"), "A6": A("A_FRP", "A_VIGENCIA"),
    "A7": A("A_PARAPET", "A_VIGENCIA"), "A8": A("A_VIGENCIA"), "A9–A11": A("A_VIGENCIA", "A_EXCEL"),
    "A12": A("A_VIGENCIA"), "A13": A("A_ANCHORS"), "A14": A("A_ANCHORS"), "A15": A("A_LEVEL5"),
    "PT1": A("A_VIGENCIA", "A_PARAPET", "A_EXCEL"), "PT2": A("A_TAG_IDS", "A_VIGENCIA", "A_EXCEL"),
    "PT3": A("A_VIGENCIA"), "PT4": A("A_RUN_ENDS", "A_VIGENCIA"), "PT5": A("A_VIGENCIA", "A_EXCEL"),
    "PT6": A("A_EXCEL"), "PT7": A("A_WRAP_FOS", "A_VIGENCIA"), "PT8": A("A_ESQUINAS"),
    "D1": A("A_MR"), "D2": A("A_BALLISTIC"), "D3": A("A_FRP"), "D4": A("A_FRP"), "D5": A("A_BLOCKING"),
    "D6": A("A_CEILING_SYS"), "D7": A("A_TRANSICION"), "D8": A("A_PARAPET"), "D9": A("A_DECK_BREAKS"),
    "D10": A("A_STOREFRONT"), "D11": A("A_VIGENCIA", "A_R72_11", "A_MEP_SWEEP"), "D12": A("A_VIGENCIA"),
    "R70.1": A("A_CEILING_SYS"), "R70.2": A("A_ESQUINAS"), "R70.3": A("A_ESQUINAS"), "R70.4": A("A_R72_1"),
    "R70.5": A("A_BALLISTIC", "A_R73_2"), "R70.6": A("A_WRAP_FOS", "A_R72_3"), "R70.7": A("A_ANCHORS", "A_STOREFRONT"),
    "R70.8": A("A_EXCEL"), "R70.9": A("A_VIGENCIA"),
    "R71.1": A("A_R71_1"), "R71.2": A("A_R71_2", "A_R72_3"), "R71.3": A("A_R71_3"), "R71.4": B("G_VENDOR"),
    "R71.5": A("A_R71_5"), "R71.6": B("G_RECESSED"), "R71.7": B("G_IMG"), "R71.8": A("A_EXCEL"),
    "R71.9": A("A_MEP_SWEEP", "A_R72_5"), "R71.10": A("A_BOX4"), "R71.11": A("A_RUN_ENDS"), "R71.12": A("A_TAG_IDS"),
    "R71.13": A("A_LAYERS_FACE", "A_VIGENCIA"), "R71.14": A("A_R72_4", "A_VIGAS_OUT"), "R71.15": A("A_ANCHORS"),
    "R71.16": A("A_VIGENCIA", "A_RFI_DELTA"),
    "R72.1": A("A_R72_1"), "R72.2": A("A_R72_2"), "R72.3": A("A_R72_3"), "R72.4": A("A_R72_4", "A_VIGAS_OUT"),
    "R72.5": A("A_R72_5", "A_R73_5"), "R72.6": A("A_R72_6"), "R72.7": A("A_VIGENCIA"), "R72.8": A("A_ANCHORS"),
    "R72.9": A("A_VIGENCIA", "A_R73_5"), "R72.10": A("A_R72_10", "A_FRP"), "R72.11": A("A_R72_11"),
    "R72.12": A("A_EXCEL"),
    # v73 (arbitraje #21): consistencia con el plano, no solo forma
    "R73.1": A("A_R73_1", "A_R72_1"), "R73.2": A("A_R73_2", "A_BALLISTIC"), "R73.3": A("A_EXCEL", "A_VIGENCIA", "A_R73_3"),
    "R73.4": B("G_PROCESO"), "R73.5": A("A_R73_5", "A_R72_5"), "R73.6": A("A_R73_6"), "R73.7": A("A_R73_7"),
    "R73.8": A("A_R73_8", "A_ESTADO_DIM"), "R73.9": A("A_EXCEL"), "R73.10": B("G_TIPO"), "R73.11": B("G_ABERTURA"),
    "R73.12": A("A_BLOCKING", "A_VIGENCIA"), "R73.13": B("G_CARA"), "R73.14": B("G_ALTO"), "R73.15": B("G_PROCESO"),
    "R73.16": A("A_TRANSICION", "A_VIGENCIA"), "R73.17": B("G_LARGO"), "R73.18": A("A_VIGENCIA"),
    # v74 (estudio de partición): reglas de la tool de partición, con test sintético por regla
    "R74.1": A("A_VIGENCIA"), "R74.2": A("A_VIGENCIA"), "R74.3": A("A_VIGENCIA"), "R74.4": A("A_VIGENCIA"),
    "R74.5": A("A_VIGENCIA", "A_R72_3"), "R74.6": A("A_VIGENCIA"),
    # v75 (arbitraje #23): compuertas en canon.py / accesorios.py / chequeos_v75.py (ValueError si no se cumplen)
    "R75.1": A("A_VIGENCIA"), "R75.2": A("A_VIGENCIA"), "R75.3": A("A_VIGENCIA"), "R75.4": A("A_VIGENCIA"),
    "R75.5": A("A_VIGENCIA"), "R75.6": A("A_VIGENCIA"), "R75.7": A("A_VIGENCIA"),
    # adendas del SKILL
    "REGLA 48.1": C("anulada por el paquete autocontenido (CAMBIOS_v72: el zip trae TODAS las tools; una prueba baja "
                    "solo el zip) — la regla de fondo (una sola fuente de tools) sigue en E24 / A_CIEGO + test_reglas"),
    "REGLA 48.2": C("anulada por el paquete autocontenido (las tools se integran en el arbitraje, §1.9)"),
    "REGLA 48.3": C("anulada por el paquete autocontenido (§1.9: una prueba no modifica tools)"),
    "REGLA 49.1": B("G_PROCESO"), "REGLA 50.1": A("A_ARCHIVOS", "A_BITACORA"),
    "REGLA 50.2": A("A_BITACORA_FINAL"), "REGLA 50.3": B("G_PROCESO"), "REGLA 50.4": B("G_PROCESO"),
    "REGLA 50.5": A("A_BITACORA_FINAL"), "REGLA 51.1": A("A_CATALOGO", "A_CIEGO"),
    "REGLA 52.1": A("A_BITACORA", "A_BITACORA_FINAL"), "REGLA 52.2": B("G_PROCESO"),
    "REGLA 52.3": C("anulada por el paquete autocontenido: py/_proyectos ya no existe; E24 (A_CIEGO) prohíbe datos "
                    "de proyecto en las tools"),
    "REGLA 52.4": A("A_EXCEL"),
    "REGLA 53.1": B("G_TRIM"), "REGLA 53.2": A("A_VIGENCIA"), "REGLA 53.3": A("A_RFI_DELTA", "A_ESTADO_DIM"),
    "REGLA 53.4": A("A_BRACING"), "REGLA 53.5": A("A_FACADES"), "REGLA 53.6": A("A_HEADER_LF"),
    "REGLA 53.7": A("A_SILL", "A_DOOR_SILL"), "REGLA 53.8": B("G_TIPO"), "REGLA 53.9": B("G_SEALANT", "A_MR"),
    "REGLA 54.1": A("A_VIGENCIA", "A_BITACORA"), "REGLA 54.2": A("A_EXCEL"), "REGLA 54.3": A("A_BLOCKING"),
    "REGLA 54.4": B("G_DET_SEALANT"), "REGLA 54.5": B("G_FACADE"), "REGLA 54.6": B("G_DETALLE", "A_DETALLE"),
    "REGLA 55.1": B("G_PROCESO"), "REGLA 55.2": A("A_DUPLICADOS"), "REGLA 55.3": B("G_PARAPET", "A_PARAPET"),
    "REGLA 55.4": B("G_ABERTURA"), "REGLA 55.5": A("A_VIGENCIA"), "REGLA 55.6": A("A_MR"),
    "REGLA 55.7": C("historial de tools (alcances.py / familias.py ya corregidas); sin regla de lectura propia"),
    "REGLA 56.1": A("A_ARCHIVOS", "A_BITACORA_FINAL"), "REGLA 56.2": B("G_GAUGE"), "REGLA 56.3": B("G_FACADE"),
    "REGLA 56.4": A("A_STOPS_BEAM", "A_R72_4"), "REGLA 56.5": A("A_DUPLICADOS"), "REGLA 56.6": B("G_DET_SEALANT"),
    "REGLA 56.7": B("G_OTROS"), "REGLA 56.8": B("G_PROCESO"), "REGLA 56.9": A("A_EXCEL"),
    "REGLA 56.10": C("historial de tools (plantilla_excel validar acepta citas con letra)"),
    "REGLA 57.1": A("A_BITACORA"), "REGLA 57.2": A("A_BITACORA_FINAL"), "REGLA 57.3": A("A_BITACORA_FINAL"),
    "REGLA 58.0": A("A_EXCEL"), "REGLA 58.1": A("A_VIGENCIA"), "REGLA 58.2": A("A_VIGENCIA", "A_EXCEL"),
    "REGLA 58.3": A("A_CANOPY"), "REGLA 58.4": A("A_FO_MODULO", "A_DUCTOS"), "REGLA 58.5": A("A_VIGENCIA"),
    "REGLA 58.6": A("A_BLOCKING"), "REGLA 58.7": A("A_CEMENT"),
    "REGLA 59.1": A("A_PURLIN"), "REGLA 59.2": B("G_FACADE"), "REGLA 59.3": B("G_LARGO"),
    "REGLA 59.4": A("A_PARAPET", "A_VIGENCIA"), "REGLA 59.5": A("A_VIGENCIA"), "REGLA 59.6": A("A_WRAP_FOS", "A_ESTADO_DIM"),
    "REGLA 59.7": A("A_VIGENCIA"), "REGLA 59.8": A("A_FO_MODULO"), "REGLA 59.9": A("A_MR"), "REGLA 59.10": A("A_FRP"),
    "REGLA 59.11": A("A_FACADES"), "REGLA 59.12": B("G_DET_SEALANT"), "REGLA 59.13": B("G_ALTO"),
    "REGLA 59.14": B("G_PROCESO"),
    "REGLA 60.0": A("A_BITACORA", "A_VIGENCIA"), "REGLA 60.1": A("A_VIGENCIA"), "REGLA 60.2": A("A_LAYERS_FACE"),
    "REGLA 60.3": A("A_STOPS_BEAM", "A_VIGENCIA"), "REGLA 60.4": A("A_CLADDING"),
    "REGLA 60.5": C("anulada por E2 (v64: header por PIEZAS, LF = (R.O. + 1'-4\") × piezas × qty)"),
    "REGLA 60.6": A("A_VIGENCIA"), "REGLA 60.7": A("A_BRACING"), "REGLA 60.8": A("A_VIGENCIA"),
    "REGLA 60.9": A("A_RFI_DELTA"), "REGLA 60.10": A("A_FO_MODULO"), "REGLA 60.11": A("A_MR"),
    # referencias/adenda_v44–v47
    "REGLA 44.1": A("A_ETAPAS"), "REGLA 44.2": C("fusionada en REGLA 44.1 (el inventario por tag de la Etapa 1 es el "
                                                  "inventario de contenido; un roll-up no lo reemplaza)"),
    "REGLA 44.3": A("A_CATALOGO"), "REGLA 45.1": B("G_LARGO"), "REGLA 45.2": A("A_VIGENCIA"),
    "REGLA 46.1": A("A_EXCEL"), "REGLA 46.2": A("A_EXCEL"), "REGLA 47.1": A("A_EXCEL"),
}

# ------------------------------------------------------------------------------------------------ por texto
# (prefijo del id o del título de la sección, regex sobre título + texto, decisión). Primera que coincide gana.
REGLAS_TEXTO = [
    # v72b
    ("S:regla", r"ninguna regla se interpreta|REGLAS INVIOLABLES: ninguna", A("A_CATALOGO")),
    ("S:19-v72b", r".", A("A_CATALOGO", "A_CIEGO")),
    ("S:etapa-2-lectura", r"evidencia \(b\) en la lectura", A("A_CATALOGO")),
    ("herramientas:reglas-py", r".", A("A_CATALOGO")),
    # PROTOCOLO v69 — etapas
    ("S:etapas-y-carpeta", r".", A("A_ETAPAS", "A_ARCHIVOS")),
    ("S:subagentes", r"Etapa 3: el script|guarda su salida", A("A_ETAPAS")),
    ("S:subagentes", r".", B("G_PROCESO")),
    ("S:etapa-1-inventario", r"type por defecto", A("A_TAG_IDS")),
    ("S:etapa-1-inventario", r"NO INVENTARIABLE", B("G_PROCESO")),
    ("S:etapa-1-inventario", r".", A("A_ETAPAS", "A_ARCHIVOS")),
    ("S:etapa-2-lectura", r"Partición de walls", A("A_TAG_IDS", "A_ESQUINAS", "A_VIGENCIA")),
    ("S:etapa-2-lectura", r"datos que la compuerta exige", A(*V72)),
    ("S:etapa-2-lectura", r"checklist de la tarea de exteriores", A("A_AS_NEEDED", "A_WRAP_FOS")),
    ("S:etapa-2-lectura", r"Todo tag del inventario", A("A_ETAPAS", "A_DESCARTADOS")),
    ("S:etapa-2-lectura", r".", A("A_ETAPAS")),
    ("S:etapa-3-doble", r"resolucion\.md", A("A_ETAPAS", "A_ARCHIVOS")),
    ("S:etapa-3-doble", r".", A("A_ETAPAS")),
    ("S:etapa-4", r".", A("A_CANON", "A_VIGENCIA")),
    ("S:etapa-5", r".", A("A_ETAPAS", "A_EXCEL", "A_BITACORA")),
    ("S:§0", r"Accesorios", A("A_ACCESORIOS")),
    # §1
    ("S:§1", r"HONESTIDAD", A("A_ESTADO_DIM")),
    ("S:§1", r"DETALLES\.", B("G_DETALLE", "A_DETALLE")),
    ("S:§1", r"BARRIDO\.", A("A_ETAPAS", "A_ARCHIVOS")),
    ("S:§1", r"EVIDENCIA VISUAL", B("G_IMG")),
    ("S:§1", r"IDIOMA", A("A_EXCEL")),
    ("S:§1", r"EJES", A("A_EJES")),
    ("S:§1", r"AMBIGÜEDAD", A("A_RFI_DELTA")),
    ("S:§1", r"ERRORES|PRUEBAS", B("G_PROCESO")),
    ("S:§1", r"REGISTRO\.", A("A_BITACORA_FINAL")),
    # §2–§8
    ("S:§2", r"Preparación", A("A_BITACORA")),
    ("S:§2", r"Etapa 1", A("A_BITACORA", "A_ETAPAS")),
    ("S:§2", r"Etapa 2", A("A_ETAPAS", "A_FUENTES")),
    ("S:§2", r"Etapa 3", A("A_ETAPAS")),
    ("S:§2", r"Etapa 4", A("A_BITACORA", "A_VIGENCIA")),
    ("S:§2", r"Etapa 5", A("A_EXCEL", "A_BITACORA")),
    ("S:3-qué-es-juicio", r".", A("A_VIGENCIA", "A_FUENTES")),
    ("S:§4", r"header: pieces", A("A_BOX4", "A_DUCTOS", "A_STOREFRONT", "A_PARAPET", "A_CANOPY", "A_WRAP_FOS",
                                   "A_FACADES")),
    ("S:§4", r"accesorios: mep_sweep", A("A_MEP_SWEEP", "A_R72_11", "A_JAMB_RETURN", "A_LEVEL5", "A_ACCESORIOS")),
    ("S:§4", r"v68 \(§14\)", A("A_MR", "A_BLOCKING", "A_PLYWOOD", "A_CEILING_SYS", "A_DECK_BREAKS", "A_FRP",
                               "A_TRANSICION", "A_PARAPET")),
    ("S:§4", r"v69 \(etapas\)", A("A_TAG_IDS", "A_DESCARTADOS")),
    # v73: campos que exige la compuerta (§20)
    ("S:§4", r"dim_scan", A("A_R73_1")), ("S:§4", r"ballistic_jogs\[\]\.band", A("A_R73_2")),
    ("S:§4", r"mep_penetrations\[\]", A("A_R73_5", "A_R72_5")), ("S:§4", r"deflection_clips", A("A_R73_6")),
    ("S:§4", r"thickness_measured_in", A("A_R73_7")), ("S:§4", r"plywood_strips\[\]\.uso", A("A_R73_3")),
    ("S:§4", r"_op.{0,30}aritmética", A("A_R73_8")),
    ("S:§5", r".", A("A_VIGENCIA", "A_TRACK_RUNS")),
    ("S:6-familias", r".", A("A_VIGENCIA", "A_ACCESORIOS")),
    ("S:§7", r"Studs:", A("A_VIGENCIA")),
    ("S:§7", r"Board:", A("A_BALLISTIC", "A_MR", "A_VIGENCIA")),
    ("S:§7", r"Wraps", A("A_WRAP_FOS")),
    ("S:§7", r"Bracing", A("A_BRACING")),
    ("S:§7", r"Header / sill", A("A_HEADER_LF", "A_FO_MODULO", "A_DUCTOS")),
    ("S:§7", r"Ceilings", A("A_VIGENCIA", "A_CEILING_SYS")),
    ("S:§7", r"Transiciones", A("A_TRANSICION")),
    ("S:§7", r"Exterior \(E25\)", A("A_FACADES")),
    ("S:§7", r"Blocking", A("A_BLOCKING")),
    ("S:§7", r"FRP / sealant", A("A_FRP", "A_CEMENT")),
    ("S:§7", r"Framed openings", A("A_FO_MODULO", "A_DUCTOS")),
    ("S:§7", r"Cladding", A("A_CLADDING", "A_ACCESORIOS")),
    ("S:§8", r"0b\. ", A("A_ESQUINAS")),
    ("S:§8", r"0c\. ", A("A_R71_1", "A_R71_2", "A_R71_3", "A_R71_5")),
    ("S:§8", r"0d\. ", A("A_R72_4", "A_VIGAS_OUT", *V72)),
    ("S:§8", r"0e\. ", A("A_CATALOGO")),
    ("S:§8", r"0\. ", A("A_ETAPAS", "A_ESQUINAS", "A_R71_1", "A_R71_2", "A_R71_3", "A_R71_5", "A_R72_4", *V72)),
    ("S:§8", r"1\. ", A("A_CANON", "A_VIGAS_OUT", "A_BITACORA")),
    ("S:§8", r"2\. ", A("A_VIGENCIA")),
    ("S:§8", r"3\. ", A("A_HEADER_LF", "A_DUCTOS")),
    ("S:§8", r"4\. ", A("A_RFI_DELTA", "A_FUENTES", "A_BITACORA_FINAL")),
    ("S:§8", r"5\. ", A("A_BITACORA_FINAL")),
    ("S:§8", r"6\. ", A("A_EXCEL", "A_BITACORA_FINAL")),
    ("S:§9", r"v68:", C("registro de anulaciones v68: aplicadas en E3, E12, D3, PT3, §15 (reglas vigentes)")),
    ("S:§9", r"v70:", C("registro de anulaciones v70: aplicadas en E28 y R70.1 (reglas vigentes)")),
    ("S:§9", r"v71:", C("registro de anulaciones v71: aplicadas en E28, R71.13, R71.8, R71.10, R71.9")),
    ("S:§9", r".", C("historial fuera del paquete (ARBITRAJE_13 a 19); sin regla propia")),
    ("S:10-anti-varianza", r".", C("resumen del flujo: fusionada en §8 (etapas.py compuerta + reglas.py)")),
    ("S:11-reglas-con-test", r".", C("índice de tests: la suite completa la exige test_reglas.py / A_CATALOGO")),
    ("S:15-compra", r".", A("A_EXCEL")),
    # REFERENCIA DE MÉTODO
    ("S:formato-de-salida", r"Layers = layers TOTALES", C("anulada por REGLA 60.2 (layers POR FACE)")),
    ("S:formato-de-salida", r"Agrega columnas", C("fusionada en REGLA 52.4 (un solo formato: plantilla_excel.py)")),
    ("S:formato-de-salida", r"LADO POR LADO", B("G_CARA")),
    ("S:formato-de-salida", r"Demolition", B("G_PROCESO")),
    ("S:formato-de-salida", r"desglose rastreable", A("A_VIGENCIA", "A_FUENTES")),
    ("S:formato-de-salida", r".", A("A_EXCEL")),
    ("S:orden-fijo", r".", A("A_EXCEL")),
    ("S:numeración-de-walls", r".", A("A_IDS")),
    ("S:regla-0-honestidad", r".", A("A_ESTADO_DIM", "A_RFI_DELTA", "A_EJES")),
    ("S:super-regla-las-dos-bandas", r".", B("G_BANDAS", "A_BANDAS")),
    ("S:evidencia-visual-obligat", r".", B("G_IMG")),
    ("S:método-técnico", r".", C("fusionada en inventario_tags.py (Etapa 1: posición por bbox / tamaño de texto + "
                                 "recorte circulado verificado; A_ETAPAS)")),
    ("S:texto-tapado", r".", C("fusionada en REGLA #0 (A_ESTADO_DIM): una cota ambigua se resuelve por texto y "
                               "queda en length_source")),
    ("S:dimensions-verticales", r".", C("fusionada en REGLA #0 / G_LARGO: la cota leída va a length_source con imagen")),
    ("S:geometría-vectorial", r"exterior sale de las faces INTERIORES", B("G_LARGO")),
    ("S:geometría-vectorial", r"thickness medido AUTOVERIFICA", B("G_THICK")),
    ("S:geometría-vectorial", r"Deduplica", A("A_DUPLICADOS")),
    ("S:geometría-vectorial", r".", B("G_LARGO")),
    ("S:medición-por-píxeles", r".", B("G_LARGO")),
    ("S:dimension-strings", r".", B("G_CADENA")),
    ("S:registro-de-dimension-strings", r".", B("G_PROCESO")),
    ("S:elevaciones-y-vistas", r".", B("G_FACADE")),
    ("S:regla-1-notas-condicionales", r".", B("G_PROCESO")),
    ("S:regla-2-verifica", r".", B("G_DETALLE")),
    ("S:regla-3-búsqueda", r".", B("G_PENDIENTE")),
    ("S:height-de-board", r".", B("G_CARA")),
    ("S:height-de-deck", r".", B("G_ALTO")),
    ("S:herramientas-el-código", r"arranque\.py", A("A_BITACORA")),
    ("S:herramientas-el-código", r"planmark\.py|closer\.py", A("A_BITACORA_FINAL")),
    ("S:herramientas-el-código", r"auditor\.py|verif_bandas|zoom\.py|wallgeom", C(OBSOLETA_TOOL + ": A_ETAPAS / "
                                                                                        "A_DUPLICADOS")),
    ("S:herramientas-el-código", r".", A("A_BITACORA", "A_BITACORA_FINAL")),
    ("S:verificación-adversarial", r"Caso real", C("narrativa del caso que originó la regla (sin regla propia)")),
    ("S:verificación-adversarial", r".", B("G_PROCESO")),
    ("S:los-markups-ajenos", r".", B("G_PROCESO")),
    ("S:las-tres-autoverific", r"thickness medido", B("G_THICK")),
    ("S:las-tres-autoverific", r".", B("G_LARGO")),
    ("S:granularidad-y-marcado", r"Si hay detalles, ábrelos", B("G_DETALLE")),
    ("S:granularidad-y-marcado", r"ESTILO DE MARCADO|corrección de cantidad|Verificación visual final|faltó una "
                                 r"ubicación|unidad de trabajo|LA TABLA DE BANDAS", B("G_PROCESO")),
    ("S:granularidad-y-marcado", r".", C("fusionada en el estilo de marcado aprobado (GRANULARIDAD Y MARCADO: ESTILO "
                                         "DE MARCADO APROBADO …), regla (b) con evidencia del juego de planos marcados")),
    ("S:archivo-todo-entregable", r".", C("anulada para DÓNDE se guarda por REGLA 49.1 (la propia sección lo dice)")),
    ("S:toda-afirmación-de-alcance", r".", B("G_TIPO")),
    ("S:el-dato-central", r".", A("A_LAYERS_FACE")),
    ("S:sets-con-walls-de-wood", r".", B("G_PROCESO")),
    # REGLAS INVIOLABLES (errores reales ya cometidos)
    ("S:reglas-inviolables-error", r"Cadenas paralelas|EQ/EQ TYP|EQ a los lados", B("G_CADENA")),
    ("S:reglas-inviolables-error", r"LF total ÷ length|Toda wall lleva bottom Y top", A("A_TRACK_RUNS")),
    ("S:reglas-inviolables-error", r"SIEMPRE en renglones o columnas separados", A("A_EXCEL")),
    ("S:reglas-inviolables-error", r"Condición del top track|Gap de deflection|bridging", B("G_TOPTRACK")),
    ("S:reglas-inviolables-error", r"Designación SSMA|Calibre que el plano|WALL CONSTRUCTION SHALL INCLUDE", B("G_GAUGE")),
    ("S:reglas-inviolables-error", r"SIN renglón en el partition schedule", B("G_TIPO")),
    ("S:reglas-inviolables-error", r"agota las cuatro fuentes", B("G_RFI", "A_RFI_DELTA")),
    ("S:reglas-inviolables-error", r"DOBLE ROW", B("G_2ROW")),
    ("S:reglas-inviolables-error", r"Doors: solo header", A("A_DOOR_SILL")),
    ("S:reglas-inviolables-error", r"Studs adicionales|Jambs:|Cerrar el wall completo", A("A_VIGENCIA")),
    ("S:reglas-inviolables-error", r"ENTRE DOS TIPOS", A("A_ESQUINAS")),
    ("S:reglas-inviolables-error", r"STOREFRONT FRAMES", B("G_EXT_AB")),
    ("S:reglas-inviolables-error", r"Jerarquía de medición|Dimension corta en planta|END CAP|banda\" de wall NO|"
                                   r"VARIOS TAGS en serie|lineweight ALTO", B("G_LARGO")),
    ("S:reglas-inviolables-error", r"face-a-face o centro-a-centro", B("G_BASE")),
    ("S:reglas-inviolables-error", r"Ningún número \"de paso\"|Al preguntar", A("A_FUENTES")),
    ("S:reglas-inviolables-error", r"Height por layer", B("G_CARA")),
    ("S:reglas-inviolables-error", r"GABINETES|Blocking de millwork|Hardware Group", B("G_BLOCKING")),
    ("S:reglas-inviolables-error", r"Línea guía del tag", C("fusionada en inventario_tags.py (Etapa 1, A_ETAPAS)")),
    ("S:reglas-inviolables-error", r"más de un tag: deduplica", A("A_DUPLICADOS")),
    ("S:reglas-inviolables-error", r"No inventar lectura", B("G_PENDIENTE")),
    ("S:reglas-inviolables-error", r"Mostrar SIEMPRE la imagen", B("G_IMG")),
    ("S:reglas-inviolables-error", r"Exclusión de material", B("G_EXCL")),
    ("S:reglas-inviolables-error", r"registro entre dos hojas", A("A_MEP_SWEEP")),
    ("S:reglas-inviolables-error", r"cruce de MEP real", B("G_MEP")),
    ("S:reglas-inviolables-error", r"numeración de walls no se vuelve", A("A_IDS")),
    ("S:reglas-inviolables-error", r"Soffits siempre separados", B("G_SOFFIT")),
    ("S:reglas-inviolables-error", r"varias alturas de cielo", B("G_CEILING")),
    ("S:reglas-inviolables-error", r"B\.O\.D\. varía|TAPERED|espejadas|steel joists", B("G_ALTO")),
    ("S:reglas-inviolables-error", r"\(HI\)/\(LOW\)", A("A_DECK_BREAKS")),
    ("S:reglas-inviolables-error", r"ARRIBA y lo que hay DEBAJO", B("G_BANDAS", "A_BANDAS")),
    ("S:reglas-inviolables-error", r"cache de render|md5 distinto", C("fusionada en arranque.py / inventario_tags.py "
                                                                      "(render desde la copia limpia; A_BITACORA)")),
    ("S:reglas-inviolables-error", r"Tile: cement board", A("A_CEMENT")),
    ("S:reglas-inviolables-error", r".", B("G_PROCESO")),
    ("S:los-errores-y-su-solució", r".", C("índice de errores: la regla desarrollada está en su sección de arriba "
                                           "(clasificada allí)")),
    # barrido / grafía / MEP / protocolo de ejecución
    ("S:barrido-completo-por-tag", r"tipo POR DEFECTO", B("G_DEFAULT", "A_TAG_IDS")),
    ("S:barrido-completo-por-tag", r"Modo desatendido", A("A_EXCEL")),
    ("S:barrido-completo-por-tag", r".", A("A_ETAPAS", "A_ARCHIVOS")),
    ("S:verificación-cruzada-del", r"CAJA CERRADA", A("A_WRAP_FOS")),
    ("S:verificación-cruzada-del", r"length NO EXPLICADO", B("G_LARGO")),
    ("S:verificación-cruzada-del", r".", B("G_PROCESO")),
    ("S:registro-entre-hojas", r"Penetración EN el stud", A("A_VIGENCIA")),
    ("S:registro-entre-hojas", r"Cruce\.", B("G_MEP")),
    ("S:registro-entre-hojas", r".", A("A_MEP_SWEEP")),
    ("S:protocolo-de-ejecución:", r"PASO 0 — Mapa|PASO 4A", A("A_BITACORA")),
    ("S:protocolo-de-ejecución:", r"PASO 3 —", A("A_BITACORA", "A_DETALLE")),
    ("S:protocolo-de-ejecución:", r"Mide el detalle por geometría", B("G_DETALLE")),
    ("S:protocolo-de-ejecución:", r"PASO 4 —", A("A_ETAPAS")),
    ("S:protocolo-de-ejecución:", r"PASO 4B", A("A_MEP_SWEEP", "A_R72_5")),
    ("S:protocolo-de-ejecución:", r"PASO 4D-BIS|PASO 7", A("A_VIGENCIA")),
    ("S:protocolo-de-ejecución:", r"PASO 4D —", B("G_BLOCKING")),
    ("S:protocolo-de-ejecución:", r"PASO 5|Alturas de elementos exteriores", B("G_ALTO")),
    ("S:protocolo-de-ejecución:", r"PASO 6", B("G_CEILING")),
    ("S:protocolo-de-ejecución:", r"Soffits —|Soffit exterior", B("G_SOFFIT")),
    ("S:protocolo-de-ejecución:", r"anchorage al deck", A("A_PURLIN")),
    ("S:protocolo-de-ejecución:", r"Elementos cerrados tipo caja", A("A_WRAP_FOS")),
    ("S:protocolo-de-ejecución:", r".", B("G_PROCESO")),
    ("S:protocolo-de-ejecución", r".", C("encabezado: cada PASO es una regla propia (clasificada abajo)")),
    ("S:formato-de-entrega", r".", C("anulada por REGLA 52.4 (un solo formato de Excel: plantilla_excel.py)")),
    ("S:clarifications-para-el-bid", r".", B("G_PROCESO")),
    ("S:antes-de-entregar", r".", C("checklist que repite reglas ya clasificadas (cada pregunta es una regla de "
                                    "arriba); la compuerta las revisa allí")),
    ("S:súper-reglas-de-las-adendas", r".", C("encabezado de copias")),
    ("S:super-regla-inviolable", r".", C("copia de referencias/adenda_v38.md (clasificada como v38:super-regla-inviolable)")),
    ("S:regla-inviolable", r"CONTEXTO|vocabulario|inglés|INGLÉS", C("copia de una súper regla de referencias/")),
    ("S:regla-inviolable", r".", C("copia de una súper regla de referencias/adenda_v39/v41/v42 (clasificada en su "
                                   "adenda)")),
    ("S:nota-propuesta-no-aplicada", r".", C("no es regla: propuesta rechazada; manda REGLA 53.2")),
    # referencias/
    ("v26:la-auditoría-adversarial", r".", B("G_PROCESO")),
    ("v26:regla-el-perfil-de-stud", r".", B("G_GAUGE")),
    ("v26:regla-ninguna-line-item", r".", A("A_VIGENCIA", "A_ACCESORIOS")),
    ("v26:regla-sumar-por-prefijo", r".", C("bug del generador viejo; plantilla_excel.fusionar (R72.12, A_EXCEL)")),
    ("v26:regla-cuando-se-corrige", r".", B("G_PROCESO")),
    ("v26:regla-doble-conteo", r".", A("A_DUPLICADOS")),
    ("v26:regla-alturas-line-items", r".", C("fusionada en G_ALTO (height_op del canon)")),
    ("v26:regla-un-material-distinto", r".", A("A_EXCEL")),
    ("v26:regla-el-track-se-compra", r".", A("A_EXCEL")),
    ("v26:regla-la-dimension-impresa-dice", r".", B("G_ALTO")),
    ("v26:regla-juntas-de-control", r".", B("G_PROCESO")),
    ("v26:regla-una-abertura-con-sill", r".", A("A_SILL")),
    ("v26:regla-cada-abertura", r".", B("G_ABERTURA")),
    ("v26:regla-un-hueco-de-equipo", r".", B("G_ABERTURA")),
    ("v26:regla-medir-lo-no-acotado", r".", B("G_DETALLE")),
    ("v26:regla-registro-de-cadenas", r".", B("G_CADENA")),
    ("v26:regla-el-título-y-la-leyenda", r".", C("fusionada en planmark.py (marcado verificado, A_BITACORA_FINAL)")),
    ("v26:regla-lo-que-no-se-resuelve", r".", A("A_ESTADO_DIM")),
    ("v27:regla-una-columna-de-resumen", r".", A("A_VIGENCIA")),
    ("v27:qué-verifica-la-compuerta", r".", C(OBSOLETA_TOOL + ": A_EXCEL (verificar_excel)")),
    ("v27:regla-una-compuerta-que-nunca", r".", A("A_CATALOGO")),
    ("v27:regla-el-decimal-raro", r".", B("G_PROCESO")),
    ("v28:regla-un-elemento-que-no-aparece", r".", A("A_ETAPAS")),
    ("v28:", r".", C("regla de código (un continue por geometría); cubierta por A_VIGENCIA (las tools fallan)")),
    ("v29:regla-la-familia-del-material", r".", A("A_EXCEL")),
    ("v29:regla-un-pendiente-se-escribe", r".", A("A_EXCEL", "A_ACCESORIOS")),
    ("v29:", r".", C("regla de código de plantilla_excel (clasificación / recálculo); cubierta por A_EXCEL")),
    ("v30:regla-el-w-r-es", r".", A("A_VIGENCIA")),
    ("v30:regla-el-censo-de-zonas", r".", A("A_MR")),
    ("v30:", r".", B("G_WET", "A_MR")),
    ("v31:regla", r".", A("A_EXCEL")),
    ("v31:compuerta-de-vigencia", r".", A("A_EXCEL", "A_VIGENCIA")),
    ("v31:", r".", C("reemplazada por bitacora.py compuerta + el sello del Excel (A_EXCEL, A_BITACORA_FINAL)")),
    ("v32:regla|v32:glosario|v32:compuerta", r".", A("A_EXCEL")),
    ("v32:", r".", C("regla de código / historial de la compuerta de idioma; cubierta por A_EXCEL (verificar)")),
    ("v33:regla-no-se-pregunta", r".", B("G_PROCESO")),
    ("v33:dónde-se-guardan", r".", C("anulada por REGLA 49.1")),
    ("v33:", r".", C("fusionada en v33:regla-no-se-pregunta (juego de planos marcados automático)")),
    ("v34:regla-no-se-cierra", r".", B("G_DETALLE")),
    ("v34:", r".", A("A_DETALLE")),
    ("v35:el-índice-se-genera", r".", B("G_PROCESO")),
    ("v35:la-carpeta-de-entrega", r".", C("anulada por REGLA 49.1")),
    ("v35:", r".", C("regla de código / operación de la PC del usuario; sin efecto en el take-off (historial)")),
    ("v36:", r".", A("A_DETALLE")),
    ("v37:el-bridging", r".", B("G_TOPTRACK")),
    ("v37:y-la-regla-general|v37:2-una-layer", r".", B("G_DETALLE")),
    ("v37:5-el-furring", r".", A("A_WRAP_FOS")),
    ("v37:4-trampa", r".", C("fusionada en REGLA 57.1 (bitacora.py run escribe a log; ver test_bitacora caso 17)")),
    ("v37:", r".", C("narrativa de un caso / bug de compuerta ya corregido; sin regla de lectura propia")),
    ("v38:", r".", A("A_VIGENCIA", "A_EXCEL")),
    ("v39:regla-inviolable|v39:1-falsos", r".", A("A_EXCEL")),
    ("v39:", r".", C("regla de código / historial de la compuerta de idioma; cubierta por A_EXCEL")),
    ("v40:la-compuerta-verif_respuesta", r".", B("G_PROCESO")),
    ("v40:", r".", C("historial de la compuerta de idioma (v39 / A_EXCEL)")),
    ("v41:", r".", B("G_CARA")),
    ("v42:regla-inviolable|v42:la-compuerta-nueva", r".", A("A_ESTADO_DIM")),
    ("v42:el-mapa-de-hojas|v42:el-registro-de-lo-que", r".", B("G_PROCESO")),
    ("v42:", r".", C("regla de código (normalización única); cubierta por las tools y sus tests")),
    ("estructura_carpeta:", r".", C("anulada por REGLA 49.1 (dónde se guarda) — la sección de ARCHIVO lo dice")),
    ("herramientas:planmark|herramientas:closer", r".", A("A_BITACORA_FINAL")),
    ("herramientas:mep-py", r".", A("A_MEP_SWEEP", "A_R72_5")),
    ("herramientas:arranque", r".", A("A_BITACORA")),
    ("herramientas:herramientas-de-etapas", r".", A("A_ETAPAS")),
    ("herramientas:", r".", C(OBSOLETA_TOOL + ": A_ETAPAS / A_DUPLICADOS / A_MEP_SWEEP")),
]


def clasificar(cat):
    """{id: decisión} para cada regla del catálogo que tiene decisión."""
    out = {}
    for r in cat:
        rid = r["id"]
        base = rid.split("~")[0]
        if base in POR_ID:
            out[rid] = POR_ID[base]
            continue
        txt = r["titulo"] + " " + r["texto"]
        for pref, rx, dec in REGLAS_TEXTO:
            if any(rid.startswith(p) for p in pref.split("|")) and re.search(rx, txt):
                out[rid] = dec
                break
    return out


def test_de(rid, c):
    t = (c or {}).get("tipo")
    if t == "a":
        return "test_reglas.py: " + ", ".join(f"malo/bueno {x}" for x in c["chequeos"])
    if t == "b":
        return f"test_reglas.py: sin evidencia falla / con evidencia pasa ({c['spec']['nombre']})"
    if t == "c":
        return "test_reglas.py: la fusión apunta a una regla vigente (a/b)"
    return "SIN CLASIFICAR"
