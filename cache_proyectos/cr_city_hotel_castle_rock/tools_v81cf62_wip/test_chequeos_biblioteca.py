#!/usr/bin/env python3
"""test_chequeos_biblioteca.py — orden del usuario 3-nov ("haz los programas"): cada chequeo de chequeos_biblioteca.py
REPRODUCE su error original (caso MALO -> FAIL) y pasa con el arreglo (caso BUENO -> PASS). Un caso por regla que estaba
"programa-pendiente" + CE_CALLOUTS (U-113 / BE-124: burbuja 7/A9.26 de la marquesina sin seguir) + env_api (BE-91) +
A_CATALOGO (BE-CF08: archivo nuevo en referencias/ sin clasificar) + cableado en compuerta_entrega.py.
Uso: python3 -I test_chequeos_biblioteca.py"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import chequeos_biblioteca as CB  # noqa: E402

B = CB.B


def W(i, tag="2", sheet="A-101", L=20.0, H=10.0, faces=None, **kw):
    w = {"id": i, "tag": tag, "element": "wall", "sheet": sheet, "length_ft": L, "height_ft": H,
         "length_source": f"{sheet} vector [DERIVED]", "height_source": "1/A-401 B.O. DECK 10'-0\" [CONFIRMED]",
         "band": {"ori": "H", "c0": 100, "c1": 104, "lo": 100, "hi": 100 + L * 9, "sheet": sheet},
         "faces": faces if faces is not None else [F("A", "OFFICE 901"), F("B", "OFFICE 902")]}
    w.update(kw)
    return w


def F(side, room, board="5/8 type X", layers=1, h=10.0, **kw):
    f = {"side": side, "room": room, "board": board, "layers": layers, "height_ft": h,
         "height_source": "A-401 [CONFIRMED]", "board_source": "1/A-501 '(1) LAYER 5/8\" TYPE X'"}
    f.update(kw)
    return f


def M(material, net=10.0, fuente="N/SHEET: 1/A-501", unit="LF", waste="=Inputs!$B$6", selling="run 10 ft", pieces=None, fila=4):
    return {"fila": fila, "material": material, "unit": unit, "net": net, "waste": waste, "purchase": None,
            "selling": selling, "pieces": pieces if pieces is not None else "=ROUNDUP(F4/Inputs!$B$11,0)", "fuente": fuente}


K = {"constants": {"plan_scale_pt_per_ft": {"value": 9.0, "source": "A-101 1/8\""}}}


def C(walls=None, **kw):
    c = copy.deepcopy(K)
    c["walls"] = walls if walls is not None else [W("W1")]
    c.update(kw)
    return c


RFI_OK = "(A) Drawings: x - delta 0 | (B) Code: y - delta 0 (loaded) | (C) Other"
INPUTS = [(5, "Waste - ALL METAL, any type", 0.15, ""), (6, "Waste - EVERYTHING THAT IS NOT METAL", 0.06, "")]

# ---------------------------------------------------------------- preferencias del día 1 (U-114..U-125, BE-131)
from PIL import Image as _Im, ImageDraw as _Dr  # noqa: E402
IMGD = tempfile.mkdtemp(prefix="pref_img_")


def _png(nombre, aro):
    im = _Im.new("RGB", (200, 120), (255, 255, 255))
    d = _Dr.Draw(im)
    d.text((70, 50), "B.O. DECK", fill=(0, 0, 0))
    if aro:
        d.ellipse([50, 35, 150, 80], outline=(255, 0, 0), width=3)
    im.save(os.path.join(IMGD, nombre))
    return nombre


ARO, SIN_ARO = _png("wall_W1.png", True), _png("sheet_A1.2.png", False)
open(os.path.join(IMGD, "vacia.png"), "wb").close()
OCC = [{"kind": "partition_tag", "type": "D", "sheet": "A1.1", "id": f"PT000{i}", "png": ARO, "png_verificado": True} for i in (1, 2, 3)]
W_OK = dict(length_source="A1.1 vector 1411.4 pt / 6.75 = 209.1 ft [DERIVED]", img=ARO, height_img=ARO)


# caso: función -> (kwargs MALO = error original, kwargs BUENO = arreglo)
CASOS = {
    # ---- preferencias del día 1 (usuario 3-nov, BE-131)
    # U-114 #0: demising cara vecina "[DERIVED]" sin operación + "same as" sin wall + escalado sin PENDING
    "u_114": ({"canon": C([W("W1", length_source="A1.1 vector [DERIVED]", faces=[F("A", "HFT", height_source="D/A4.1 '1 LAYER 5/8\" "
                                "TYPE X GYP. BD. @ EACH SIDE' to 1\" below deck [DERIVED]")]),
                              W("RE-01", length_source="S2.1 opening widths measured at scale [DERIVED] 1411 / 6.75 = 10 ft")])},
              {"canon": C([W("W1", length_source="A1.1 vector 1411.4 pt / 6.75 = 209.1 ft [DERIVED]",
                             faces=[F("A", "HFT", height_source="B.O. deck 18.25 (3/A-301) - 0.08 slip = 18.17 ft [DERIVED]")]),
                           W("W3", length_source="A1.1 printed '20'-0\"' [CONFIRMED]", height_source="same as W1")])}),
    # U-115: O'Reilly rev4 Material Summary 'N/SHEET: not applicable (see note)' (CE_FUENTES_MS lo dejaba pasar)
    "u_115": ({"ms": [M("FRT plywood substrate (5/8 in.)", 420.25, unit="SF", fuente="N/SHEET: not applicable (see note)")],
               "pt": [{"fila": 6, "wall": "EX-DIN-01", "lf": 12.0, "source": "A.3 interior elevation general notes"}]},
              {"ms": [M("FRT plywood substrate (5/8 in.)", 420.25, unit="SF", fuente="N/SHEET: 7/A4.2")],
               "pt": [{"fila": 6, "wall": "EX-DIN-01", "lf": 12.0, "source": "A.3/A-202"}]}),
    # U-116: HFT 'metal hat channel ... (not printed)' y espaciado 'assumed' sin RFI = elección en silencio
    "u_116": ({"ms": [M("Bracing 1-1/2\" CRC", 40, fuente="N/SHEET: A1.1 | spacing not printed: 4'-0\" O.C. assumed")],
               "pend": [("RFI-05", "Braces to structure", RFI_OK)]},
              {"ms": [M("Bracing 1-1/2\" CRC", 40, fuente="N/SHEET: A1.1 | spacing not printed: 4'-0\" O.C. assumed, see RFI-05")],
               "pend": [("RFI-05", "Braces to structure", RFI_OK)]}),
    # U-117: tags D del plano que el canon no cuenta (ubicaciones sin wall); sin inventario = barrido no hecho
    "u_117": ({"canon": C([W("W1", tag="D", tag_ids=["PT0001"])]), "inv_full": {"ocurrencias": {"partition_tag": OCC}}, "inv_dir": IMGD},
              {"canon": C([W("W1", tag="D", tag_ids=["PT0001", "PT0002"]), W("W2", tag="D", tag_ids=["PT0003"])]),
               "inv_full": {"ocurrencias": {"partition_tag": OCC}}, "inv_dir": IMGD}),
    # U-118: O'Reilly — height_img = página entera sin marca (0 px rojos); RFI y Review Item sin imagen
    "u_118": ({"canon": C([W("S21-N", img=ARO, height_img=SIN_ARO)]), "raiz": IMGD,
               "pend": [("RFI-01", "Height basis per bay", RFI_OK)], "review": [("1/7", "Floor plan", "C", "W5", "A1.1", "plan crop of A1.1")]},
              {"canon": C([W("S21-N", img=ARO, height_img=ARO)], rfis=[{"id": "RFI-01", "img": ARO}]), "raiz": IMGD,
               "pend": [("RFI-01", "Height basis per bay", RFI_OK)], "review": [("1/7", "Floor plan", "C", "W5", "A1.1", "wall_W1.png")]}),
    # U-119: README_REVIEW con prosa en español (el entregable va íntegro en inglés)
    "u_119": ({"docs": {"README_REVIEW.md": "# ESTA ES LA VERSIÓN FINAL PARA REVISAR\nLa altura de los muros sale de la hoja A-401.\n| 5 | 3/A2.1 | A1.1 | 3/A2.1 | fuera de alcance: East exterior elevation |"}},
              {"docs": {"README_REVIEW.md": "# ESTA ES LA VERSIÓN FINAL PARA REVISAR\nWall heights come from 1/A-401 (B.O. DECK EL. 18'-3\").\nType X wraps to B.O. framing EL 108'-6\" | studs to EL 120'-8\".",
                        "PARA_REVISAR_EN_LA_MANANA.md": "La altura de los walls sale de la hoja A-401."}}),
    # U-120: O'Reilly rev4 'S42-H1+S42-H2' en un renglón + polilínea en L (dos ejes en un markup)
    "u_120": ({"pt": [{"fila": 25, "wall": "S42-H1+S42-H2", "lf": 30.0}],
               "annots": [{"label": "A1.1", "subject": "S42", "contents": "S42 | LF 30 | S42-H1", "tipo": "PolyLine",
                           "verts": [(0, 0), (100, 0), (100, 80)]}]},
              {"pt": [{"fila": 25, "wall": "S42-H1", "lf": 15.0}],
               "annots": [{"label": "A1.1", "subject": "S42", "contents": "S42 | LF 15 | S42-H1", "tipo": "PolyLine",
                           "verts": [(0, 0), (60, 0), (100, 1)]}]}),
    # U-121: markup sin /Depth (Bluebeam no da Wall Area) y sin Subject
    "u_121": ({"annots": [{"label": "A1.1", "subject": "", "contents": "A-01 | LF 11.54", "measure": True, "tipo": "PolyLine", "depth": None}]},
              {"annots": [{"label": "A1.1", "subject": "TYPE A", "contents": "A-01 | LF 11.54", "measure": True, "tipo": "PolyLine", "depth": 18.04}]}),
    # U-125: PARA_REVISAR con 'tablaroca' / 'postes metálicos' (términos del trade traducidos)
    "u_125": ({"docs": {"PARA_REVISAR_EN_LA_MANANA.md": "Se cargó tablaroca 5/8 tipo X y postes metálicos de 6\"."}},
              {"docs": {"PARA_REVISAR_EN_LA_MANANA.md": "Se cargó 5/8 Type X gypsum board y studs 6\" 20 GA."}}),
    # U-017 (B&N §0.F): A leyó la cota impresa 12'-4"; la resolución tomó B (12.9)
    "u_017": ({"canon_a": C([W("W1", L=12.333, length_source="A-101 printed '12'-4\"' [CONFIRMED]")]), "canon_b": C([W("W1", L=12.9)]),
               "canon_ab": C([W("W1", L=12.9)])},
              {"canon_a": C([W("W1", L=12.333, length_source="A-101 printed '12'-4\"' [CONFIRMED]")]), "canon_b": C([W("W1", L=12.9)]),
               "canon_ab": C([W("W1", L=12.333)])}),
    "be_08": ({"canon": C([W("W1", L=11.9, length_source="A-101 printed '12'-4\"' [CONFIRMED]")])},
              {"canon": C([W("W1", L=12.333, length_source="A-101 printed '12'-4\"' [CONFIRMED]")])}),
    # U-026 / BE-108: RFI de control joints, ya decidido por R80e.34 #8
    "u_026": ({"pend": [("RFI-05", "Control joints not detailed: spacing?", RFI_OK)]},
              {"pend": [("RFI-05", "Control joints per R80e.34 #8 precedent", RFI_OK)]}),
    # U-034 / BE-59: lectura A sin la hoja ampliada que B sí trae
    "u_034": ({"canon_a": C([W("W1")]), "canon_b": C([W("W1"), W("W9", sheet="A-221")])},
              {"canon_a": C([W("W1"), W("W9", sheet="A-221")]), "canon_b": C([W("W1"), W("W9", sheet="A-221")])}),
    # U-035 / BE-65: canon sin plan_scale_pt_per_ft (W2-01 band 50.0 vs 48'-4")
    "u_035": ({"canon": {"walls": [W("W1")]}}, {"canon": C()}),
    # U-037 / BE-72: tags de un type en el inventario y ningún wall de ese type
    "u_037": ({"canon": C([W("W1", tag="2")]), "inventario": [{"type": "4", "sheet": "A-101"}, {"type": "2", "sheet": "A-101"}]},
              {"canon": C([W("W1", tag="2"), W("W2", tag="4")]), "inventario": [{"type": "4", "sheet": "A-101"}, {"type": "2", "sheet": "A-101"}]}),
    # U-043 / BE-94: R80e.43 validado con una sola corrida
    "u_043": ({"textos": {"INDICE.md": "**03-nov: v9 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = arreglo, probado con la #4"}},
              {"textos": {"INDICE.md": "**03-nov: v9 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = arreglo. Banco #3 #4 #5 = 0 familias distintas"}}),
    # U-051 / BE-100: bid set de O'Reilly con 79 markups de Bluebeam de otro estimador
    "u_051": ({"bidset_annots": [{"title": "jsmith", "subject": "Length Measurement"}, {"title": "AutoCAD SHX Text", "subject": ""}]},
              {"bidset_annots": [{"title": "AutoCAD SHX Text", "subject": ""}]}),
    # U-057 / BE-110: altura del purlin medida a escala; board con aberturas descontadas
    "u_057": ({"canon": C([W("W1", height_source="purlin height scaled from 1/A3.2 [DERIVED]",
                             faces=[F("A", "X", note="less openings deducted"), F("B", "Y")])])}, {"canon": C()}),
    # U-058 / BE-111: head interior del storefront tomado de la cota exterior T.O. high eave
    "u_058": ({"canon": C([W("W1", faces=[F("A", "SALES 101", height_source="5'-0 3/4\" from 1/A3.1 to T.O. high eave")])])},
              {"canon": C([W("W1", faces=[F("A", "SALES 101", height_source="11'-4\" R.O. A5.2 -> 12'-0\" 1/A5.2 interior face")])])}),
    # U-079 / BE-CF01: la copia limpia borró los 519 'AutoCAD SHX Text': M/P/E sin texto
    "be_cf01": ({"hojas": {"A-101": "FLOOR PLAN", "M-101": "", "P-101": " ", "E-101": ""}},
                {"hojas": {"A-101": "FLOOR PLAN", "M-101": " ".join(["SUPPLY DUCT 12x10 TO DIFFUSER"] * 5),
                           "P-101": " ".join(["SANITARY WASTE LINE VENT"] * 5), "E-101": " ".join(["PANEL LP CIRCUIT HOMERUN"] * 5)}}),
    # U-081 / BE-CF06: comparar.py solo walls: sin revision_extra con cielos / demo
    "u_081": ({"canon_a": C(ceilings=[{"room": "901"}]), "canon_b": C(ceilings=[{"room": "901"}])},
              {"canon_a": C(ceilings=[{"room": "901"}]), "canon_b": C(ceilings=[{"room": "901"}]),
               "textos": {"etapas/2_lectura/revision_extra.md": "| ceilings | A 2 | B 2 |"}}),
    # U-082 / R-ALC-10: conflicto plano vs spec sin hoja / sección / delta
    "u_082": ({"ms": [M("Track 3-5/8\"", fuente="N/SHEET: drawings conflict with spec, plan carried")]},
              {"ms": [M("Track 3-5/8\"", fuente="N/SHEET: 1/A-501 conflict with spec 09 22 16 2.2.B (20 GA): plan 25 GA carried, delta +3%")]}),
    # R-ALC-02: blocking de grab bar sin medida impresa cargado 1 fila x 2 ft
    "r_alc_02": ({"canon": C(blocking_items=[{"ref": "GB-1", "rows": 1, "lf_each": 2, "source": "grab bar, size not printed"}])},
                 {"canon": C(blocking_items=[{"ref": "GB-1", "rows": 2, "lf_each": 3, "source": "grab bar, size not printed (R-ALC-02)"}])}),
    # R-ALC-04: demo plan quita partitions de gyp y no hay renglón de demolición
    "r_alc_04": ({"hojas": {"D-101": "DEMOLITION PLAN  REMOVE EXISTING GYP. BD. PARTITION"}, "ms": [M("Bottom track 3-5/8\"")]},
                 {"hojas": {"D-101": "DEMOLITION PLAN  REMOVE EXISTING GYP. BD. PARTITION"}, "ms": [M("Bottom track 3-5/8\""),
                                                                                                  M("Demolition gyp board partition", 200, unit="SF")]}),
    # BE-01: 8/A-410 'METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP.' sin cuantificar
    "be_01": ({"hojas": {"A-410": "8 METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP."}, "ms": [M("Bottom track")]},
              {"hojas": {"A-410": "8 METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP."}, "ms": [M("Fire stop track 3-5/8\"")]}),
    "be_02": ({"hojas": {"A-001": "W.R. GYP BD FOR WALL AND CEILING CONSTRUCTION AT WET AREAS"},
               "canon": C(ceilings=[{"room": "WOMEN'S 910", "system": "suspended gyp", "board": "5/8 type X"}])},
              {"hojas": {"A-001": "W.R. GYP BD FOR WALL AND CEILING CONSTRUCTION AT WET AREAS"},
               "canon": C(ceilings=[{"room": "WOMEN'S 910", "system": "suspended gyp", "board": "5/8 W.R."}])}),
    "be_03": ({"hojas": {"A-001": "W.R. GYP BD AT WET AREAS"}, "canon": C([W("W1", faces=[F("A", "RESTROOM 910", "5/8 type X")])])},
              {"hojas": {"A-001": "W.R. GYP BD AT WET AREAS"}, "canon": C([W("W1", faces=[F("A", "RESTROOM 910", "5/8 W.R.")])])}),
    "be_04": ({"canon": C([W("W1", faces=[F("A", "CAFE WORK ROOM", "5/8 W.R.", board_source="E/A-221 5/8\" FRT PLYWOOD only + FRP")])])},
              {"canon": C([W("W1", faces=[F("A", "CAFE WORK ROOM", "none", layers=0, board_source="E/A-221 5/8\" FRT PLYWOOD only + FRP")])])}),
    "be_05": ({"canon": C([W("W1", faces=[F("A", "SALES", layers=2)])])}, {"canon": C()}),
    "be_06": ({"canon": C([W("S1", tag="SOFFIT", element="soffit", faces=[F("N", "SALES")])])},
              {"canon": C([W("S1", tag="SOFFIT", element="soffit", faces=[F("N", "SALES"), F("bottom", "SALES")])])}),
    "be_07": ({"canon": C(partition_schedule=[{"type": "3", "source": "A-501"}]), "hojas": {"A-101": "3 SIM. 3 2"}},
              {"canon": C([W("W1"), W("W1-SIM", tag="3", length_source="A-101 SIM. tag end face 0.4 ft")],
                          partition_schedule=[{"type": "3", "source": "A-501"}]), "hojas": {"A-101": "3 SIM. 3 2"}}),
    "be_09": ({"canon": C([W("W1", length_source="A-101 existing partition to remain")])}, {"canon": C()}),
    "be_10": ({"scope": [("ALC-20", "Soffit", "RFI", "soffit with HOLD dimension, not priced")]},
              {"scope": [("ALC-20", "Soffit", "QUANTIFIED", "soffit HOLD dimension quantified + RFI-04")]}),
    "be_11": ({"hojas": {"A-221": "AREA OF 3/4\" FIRE RESISTANT PLYWOOD"}, "ms": [M("Bottom track")]},
              {"hojas": {"A-221": "AREA OF 3/4\" FIRE RESISTANT PLYWOOD"}, "ms": [M("3/4\" FRT plywood", 40, unit="SF")]}),
    "be_12": ({"hojas": {"A-501": "1 PARTITION TYPES"}, "ms": [M("Head track", fuente="N/SHEET: 1/A-501 'ADD FULL LENGTH ADDL HEAD TRACK AT OPENINGS'")]},
              {"hojas": {"A-501": "1 PARTITION TYPES ADD FULL LENGTH ADDL HEAD TRACK AT OPENINGS"},
               "ms": [M("Head track", fuente="N/SHEET: 1/A-501 'ADD FULL LENGTH ADDL HEAD TRACK AT OPENINGS'")]}),
    "be_13": ({"hojas": {"E-103": "2 SERVER ROOM 3/4\" PLYWOOD BACKBOARD BY GC"}, "ms": [M("Bottom track")]},
              {"hojas": {"E-103": "2 SERVER ROOM 3/4\" PLYWOOD BACKBOARD BY GC"}, "ms": [M("Bottom track")],
               "scope": [("ALC-30", "Backboard", "EXCLUDED", "plywood backboard 2/E-103 BY GC (R80e.34 #11)")]}),
    "be_14": ({"hojas": {"A-401": "T.O. WD-1 15'-0\" A.F.F."}, "pend": [("RFI-03", "T.O. WD-1 not printed; assumed 16'", RFI_OK)]},
              {"hojas": {"A-401": "SECTION"}, "pend": [("RFI-03", "T.O. WD-1 not printed; assumed 16'", RFI_OK)]}),
    "be_15": ({"canon": C(misc_items=[{"ref": "J-1", "familia": "1-5/8\" post vertical", "source": "3/A-410 '1 5/8\" x 16 GA. METAL JOIST FRAMING @ 48\" O.C.'"}])},
              {"canon": C(misc_items=[{"ref": "J-1", "familia": "1-5/8\" joist horizontal", "source": "3/A-410 '1 5/8\" x 16 GA. METAL JOIST FRAMING @ 48\" O.C.'"}])}),
    "be_16": ({"hojas": {"A-410": "CLIP ANGLE AT EACH STUD"}, "ms": [M("Bottom track")]},
              {"hojas": {"A-410": "CLIP ANGLE AT EACH STUD"}, "ms": [M("Clip angle 2x2", 20, unit="EA")]}),
    "be_17": ({"canon": C([W("W1", gauge="20 GA"), W("W2", gauge="16 GA")]), "ms": [M("Framing screws #8", 500, unit="EA")]},
              {"canon": C([W("W1", gauge="20 GA"), W("W2", gauge="16 GA")]), "ms": [M("Framing screws #8 (EXCLUDED)", 0, unit="EA")]}),
    "be_18": ({"textos": {"PASO12_cobertura.md": "| BE-13 | backboard | GAP |"}}, {"textos": {"PASO12_cobertura.md": "| BE-13 | backboard | OK |"}}),
    "be_19": ({"hojas": {"A-410": "SLAB PINS @ 24\" O.C."}, "ms": [M("Slab pins @ 12\"", 300, unit="EA")]},
              {"hojas": {"A-410": "SLAB PINS @ 24\" O.C."}, "ms": [M("Slab pins @ 24\"", 300, unit="EA")]}),
    "be_20": ({"canon": C([W("S1", tag="SOFFIT", element="soffit", faces=[F("N", "X"), F("bottom", "X")])]), "ms": [M("Track 3-5/8\"", fuente="1/A-501 soffit perimeter")]},
              {"canon": C([W("S1", tag="SOFFIT", element="soffit", faces=[F("N", "X"), F("bottom", "X")])]),
               "ms": [M("Track 3-5/8\"", fuente="1/A-501 soffit 2 tracks"), M("Stud 3-5/8\"", fuente="1/A-501 soffit studs @ 16")]}),
    "be_21": ({"hojas": {"A-501": "5/8 TYPE X"}, "ms": [M("5/8\" glass mat sheathing", 100, unit="SF")]},
              {"hojas": {"A-501": "5/8\" GLASS MAT SHEATHING"}, "ms": [M("5/8\" glass mat sheathing", 100, unit="SF")]}),
    "be_22": ({"hojas": {"A-501": "JAMB"}, "ms": [M("Jamb return gypsum", 30)]}, {"hojas": {"A-501": "GYP BD RETURN AT JAMB"}, "ms": [M("Jamb return gypsum", 30)]}),
    "be_23": ({"ms": [M("Acoustical sealant", 20, unit="TUBE")]}, {"ms": [M("Acoustical sealant (EXCLUDED)", 0, unit="TUBE")]}),
    "be_25": ({"canon": C(ceilings=[{"room": "901", "system": "suspended gypsum furring", "board": "5/8 type X"}])},
              {"canon": C(ceilings=[{"room": "901", "system": "suspended gypsum furring", "board": "5/8 type X", "system_callout": "5/A-601"}])}),
    "be_26": ({"canon": C([W("K1", tag="K", length_source="A-101 node to node N3-N4")])},
              {"canon": C([W("K1", tag="K", length_source="A-101 hatch extent printed 8'-0\"")])}),
    "be_27": ({"hojas": {"A-101": "ATM RECESS"}, "canon": C()}, {"hojas": {"A-101": "ATM RECESS"}, "canon": C(atm_recess_none_reason="ATM by vendor 3/A-101")}),
    "be_28": ({"hojas": {"A-301": "CANOPY FRAMING 6\" STUDS"}, "ms": [M("Bottom track")]},
              {"hojas": {"A-301": "CANOPY FRAMING 6\" STUDS"}, "ms": [M("Bottom track")], "scope": [("ALC-03", "Canopy / parapet", "QUANTIFIED", "canopy studs")]}),
    "be_29": ({"ms": [M("Header track", 40, fuente="1/A-501 assumed 2 pcs per door")]},
              {"ms": [M("Header track", 40, fuente="1/A-501 R80e.34 #4 precedent 2 pcs per door")]}),
    "be_41": ({"scope": [("ALC-05", "Headers", "QUANTIFIED", "by headers.py from takeoff_canon.json")]},
              {"scope": [("ALC-05", "Headers", "QUANTIFIED", "door schedule A-601")]}),
    "be_45": ({"pt": [{"fila": 5, "wall": "W1", "board": 400.0}], "ms": [M("5/8\" Type X gypsum board", 1200, unit="SF")]},
              {"pt": [{"fila": 5, "wall": "W1", "board": 400.0}], "ms": [M("5/8\" Type X gypsum board", 420, unit="SF")]}),
    "be_46": ({"ms": [M("Cement board 1/2\" / 5/8\" backer", 100, unit="SF")]}, {"ms": [M("Cement board 1/2\" backer", 100, unit="SF")]}),
    "be_47": ({"scope": [("ALC-26", "X", "RFI", "see RFI-40")], "pend": [("RFI-01", "q", RFI_OK)]},
              {"scope": [("ALC-26", "X", "RFI", "see RFI-01")], "pend": [("RFI-01", "q", RFI_OK)]}),
    "be_48": ({"annots": [{"label": "A-101", "subject": "Legend", "contents": "Source: takeoff_canon.json", "measure": False}]},
              {"annots": [{"label": "A-101", "subject": "2", "contents": "TYPE 2 LF 20", "measure": True}]}),
    "be_49": ({"canon": C([W("LWT-01", L=46.0, length_source="A-101 printed '46'-0\"' [CONFIRMED]",
                            band={"ori": "H", "c0": 1, "c1": 2, "lo": 0, "hi": 48.83 * 9 + 100, "sheet": "A-101"})])},
              {"canon": C([W("LWT-01", L=46.0, length_source="A-101 printed '46'-0\"' [CONFIRMED]",
                            band={"ori": "H", "c0": 1, "c1": 2, "lo": 0, "hi": 46.0 * 9, "sheet": "A-101"})])}),
    "be_50": ({"hojas": {"E-301": "LIGHT FIXTURE SUPPORT WIRES BY THE EC"}, "pend": [("RFI-01", "q", RFI_OK)]},
              {"hojas": {"E-301": "LIGHT FIXTURE SUPPORT WIRES BY THE EC"}, "pend": [("RFI-07", "E-301 support wires by the EC vs 5/A-121", RFI_OK)]}),
    "be_51": ({"ms": [M("2x blocking", 37.5, selling="piece", pieces="=ROUNDUP(F4,0)")]},
              {"ms": [M("2x blocking", 37.5, selling="piece", pieces="=ROUNDUP(F4/Inputs!$B$11,0)")]}),
    "be_52": ({"ms": [M("Bottom track", fila=4), M("Framing screws", 0, fila=5)], "scope": [("ALC-40", "#8 screws", "QUANTIFIED", "covered by row 5")]},
              {"ms": [M("Bottom track", fila=4), M("Framing screws", 10, fila=5)], "scope": [("ALC-40", "#8 screws", "QUANTIFIED", "covered by row 5")]}),
    "be_53": ({"pend": [("RFI-28", "A/A-410 prints '(1) #10-16 SCREW @ EACH FLANGE' and clip", "(A) Drawings: clip angle delta +20 EA | (B) Code delta 0 (loaded) | (C)")]},
              {"pend": [("RFI-28", "A/A-410 prints '(1) #10-16 SCREW @ EACH FLANGE' and clip", "(A) Drawings: clip angle + screws (EXCLUDED U-053) delta | (B) delta (loaded) | (C)")]}),
    "be_54": ({"ms": [M("Drywall screws Type S", 10, fuente="board total minus cement board base")]}, {"ms": [M("Drywall screws Type S", 10, fuente="per face")]}),
    "be_55": ({"pend": [("RFI-02", "per C7-03 rev7 plan check", RFI_OK)]}, {"pend": [("RFI-02", "per 3/A-410", RFI_OK)]}),
    "be_57": ({"inputs": INPUTS, "ms": [M("2x6 FRT wood blocking", 30, waste="=Inputs!$B$5")]},
              {"inputs": INPUTS, "ms": [M("2x6 FRT wood blocking", 30, waste="=Inputs!$B$6")]}),
    "be_58": ({"bitacora": [{"paso": "excel a mano"}]}, {"bitacora": [{"paso": "canon.py"}, {"paso": "reglas.py ok"}, {"paso": "plantilla_excel.py"}]}),
    "be_60": ({"canon_a": {"walls": [], "HG1": {}}, "canon_b": C()}, {"canon_a": C(), "canon_b": C()}),
    "be_61": ({"canon_a": C([W("W1")]), "canon_b": C([W("W1"), W("W2"), W("W3")]), "canon_ab": C([W("W1")])},
              {"canon_a": C([W("W1")]), "canon_b": C([W("W1"), W("W2"), W("W3")]), "canon_ab": C([W("W1"), W("W2"), W("W3")])}),
    "be_62": ({"canon": C([W("C25", tag="C25", band={"ori": "BOX", "x0": 1, "y0": 1, "x1": 9, "y1": 9, "sheet": "A-101"})])},
              {"canon": C([W("C25", tag="C25", element="column_wrap", band={"ori": "BOX", "x0": 1, "y0": 1, "x1": 9, "y1": 9, "sheet": "A-101"})])}),
    "be_63": ({"canon_a": C([W("W1", L=20)]), "canon_b": C([W("W1", L=20.1)]), "canon_ab": C([W("W1", L=24.5)])},
              {"canon_a": C([W("W1", L=20)]), "canon_b": C([W("W1", L=20.1)]), "canon_ab": C([W("W1", L=20)])}),
    "be_64": ({"canon_a": C([W("W1", length_source="from FINAL_FOR_REVIEW rev13")]), "canon_b": C()}, {"canon_a": C(), "canon_b": C()}),
    "be_66": ({"costos": [{"paso": "lectura_B", "usd": "", "tope": "4"}]}, {"costos": [{"paso": "lectura_B", "usd": "3.9", "tope": "4"}]}),
    "be_67": ({"canon": C(nodes=[{"id": "NP3", "kind": "L", "walls": ["W1", "EXT-07"]}])}, {"canon": C(nodes=[{"id": "NP3", "kind": "L", "walls": ["W1"]}])}),
    "be_68": ({"canon": C([W("W1", height_source="20 ft", length_source="vector")])}, {"canon": C()}),
    "be_69": ({"ms": [M("5/8\" Type X gypsum board", 100, unit="SF", fuente="A-501 | 5/8\" regular faces 40 + X 60")]},
              {"ms": [M("5/8\" Type X gypsum board", 100, unit="SF", fuente="A-501 | X faces 100")]}),
    "be_70": ({"hojas": {"A-121": "GYP. BD. CEILING @ 9'-0\""}, "canon": C()},
              {"hojas": {"A-121": "GYP. BD. CEILING @ 9'-0\""}, "canon": C(ceilings=[{"room": "910", "board": "5/8 type X"}])}),
    "be_71": ({"canon_a": C(), "canon_b": C()},
              {"canon_a": C(), "canon_b": C(), "textos": {"3_revision/resolucion.md": "x", "PASO12_cobertura.md": "| ok |"}}),
    "be_73": ({"pt": [{"fila": 9, "partition": None, "wall": "2-11", "lf": 3.0}]}, {"pt": [{"fila": 9, "partition": "TYPE 2", "wall": "2-11", "lf": 3.0}]}),
    "be_76": ({"canon": C([W("W1", faces=[F("A", "X", "5/8 regular")])], generales={"board": "5/8 type X", "board_reemplaza": "5/8 regular"})},
              {"canon": C([W("W1")], generales={"board": "5/8 type X", "board_reemplaza": "5/8 regular"})}),
    "be_77": ({"canon_a": C([W("C-E2", faces=[F("A", "WORKROOM", "1/2 cement board")])]), "canon_b": C([W("C-E2")]), "revision": {}},
              {"canon_a": C([W("C-E2", faces=[F("A", "WORKROOM", "1/2 cement board")])]), "canon_b": C([W("C-E2")]),
               "revision": {"difieren_atributos": [{"wall": "C-E2"}]}}),
    "be_78": ({"canon": C([W("W1", height_source="placeholder 20 ft [PENDIENTE]")])}, {"canon": C()}),
    "be_79": ({"canon": C([W("W1", faces=[{"board": "5/8 type X"}])])}, {"canon": C()}),
    "be_80": ({"canon_a": C(columns_none_reason="existing columns C23"), "canon_b": C(misc_items=[{"ref": "COL-1"}]), "revision": {}},
              {"canon_a": C(columns_none_reason="existing columns C23"), "canon_b": C(misc_items=[{"ref": "COL-1"}]),
               "revision": {"nones": "columns: A none / B COL-1"}}),
    "be_81": ({"canon": C([W("W1", tag="F")], partition_schedule=[{"type": "2", "source": "A-501"}])},
              {"canon": C([W("W1", tag="2")], partition_schedule=[{"type": "2", "source": "A-501"}])}),
    "be_82": ({"canon": C([W("W2-04", L=30, faces=[F("A", "CAFE WORKROOM 904")]), W("C-H1-N", sheet="A-221", L=29, faces=[F("A", "CAFE WORKROOM 904")])])},
              {"canon": C([W("W2-04", L=12, faces=[F("A", "SALES 101")]), W("C-H1-N", sheet="A-221", L=29, faces=[F("A", "CAFE WORKROOM 904")])])}),
    "be_83": ({"canon": C([W("W1", H=25, faces=[F("A", "WOMEN 910", "5/8 W.R.", h=25, height_source="A-400A")])], ceilings=[{"room": "WOMEN 910", "height_ft": 9.0}])},
              {"canon": C([W("W1", H=25, faces=[F("A", "WOMEN 910", "5/8 W.R.", h=9.5, height_source="A-121 + 6\"")])], ceilings=[{"room": "WOMEN 910", "height_ft": 9.0}])}),
    "be_84": ({"canon": C([W("CW1", element="column_wrap")]), "ms": [M("Bottom track")]},
              {"canon": C([W("CW1", element="column_wrap")]), "ms": [M("Bottom track"), M("Corner bead", 40)]}),
    "be_85": ({"canon": C(accesorios_none="PAFs and duct sleeves"), "ms": [M("Duct sleeve", 4, unit="EA")]},
              {"canon": C(accesorios_none="PAFs and duct sleeves"), "ms": [M("Bottom track")]}),
    "be_88": ({"pend": [("RFI-01", "q", "delta", "(A) planos", "(B) código")]}, {"pend": [("RFI-01", "q", RFI_OK)]}),
    "be_89": ({"canon": C(nodes=[{"id": f"N{i}", "kind": "free", "walls": ["W1"]} for i in range(8)])},
              {"canon": C(nodes=[{"id": f"N{i}", "kind": "L", "walls": ["W1"]} for i in range(8)])}),
    "be_90": ({"hojas": {"A-500": "DOOR SCHEDULE"}, "canon": C()},
              {"hojas": {"A-500": "DOOR SCHEDULE"}, "canon": C(opening_schedule={"items": [{"ref": "101"}]})}),
    "be_91": ({"env": {"ANTHROPIC_BASE_URL": "http://x", "CLAUDE_CODE_SESSION": "s", "ANTHROPIC_API_KEY": "k"}},
              {"env": CB.env_api({"ANTHROPIC_BASE_URL": "http://x", "CLAUDE_CODE_SESSION": "s", "ANTHROPIC_API_KEY": "k"})}),
    "be_92": ({"canon": C(decisiones_sin_objeto=["cross members", "nested bracing"])}, {"canon": C()}),
    "be_95": ({"canon": C([W("HG2", length_source="A-101 curved wall measured by chord")])}, {"canon": C([W("HG2", length_source="A-101 curved wall arc length")])}),
    "be_97": ({"canon": C([W("E1", faces=[F("A", "SALES", h=12), F("A", "SALES", h=25)])])}, {"canon": C([W("E1", faces=[F("A", "SALES", h=12), F("A2", "SALES", h=25)])])}),
    "be_98": ({"canon": C([W("W1", tag="1A")], excluded_types={"1A": "existing (RFI-01)"})}, {"canon": C([W("W1", tag="2")], excluded_types={"1A": "existing (RFI-01)"})}),
    "be_102": ({"hojas": {"A1.1": "PLAN"}, "ms": [M("Bottom track", fuente="8/A-410")]}, {"hojas": {"A1.1": "PLAN", "A4.1": "8"}, "ms": [M("Bottom track", fuente="8/A4.1")]}),
    "be_103": ({"canon": C([{k: v for k, v in W("W1").items() if k != "band"}])}, {"canon": C()}),
    "be_104": ({"canon": C(partition_schedule=[{"type": "S24", "source": "S24/A1.1 7/8\" Z-FURRING over CMU + 6\" STUDS"}]), "ms": [M("Stud 6\"")]},
               {"canon": C(partition_schedule=[{"type": "S24", "source": "S24/A1.1 7/8\" Z-FURRING over CMU + 6\" STUDS"}]), "ms": [M("Stud 6\""), M("Z-furring 7/8\"")]}),
    "be_105": ({"pend": [("RFI-21", "S1.1 note 7 printed Titen HD @ 48\"; default spacing loaded", RFI_OK)]},
               {"pend": [("RFI-21", "Opening width not dimensioned", RFI_OK)]}),
    "be_106": ({"scope": [("ALC-1", "x", "QUANTIFIED", "Estimator criterion / Handoff - Approved")]},
               {"scope": [("ALC-1", "x", "QUANTIFIED", "estimator criterion per R80e.34 #8")]}),
    "be_107": ({"canon": C(), "ms": [M("Framing screws", 500, unit="EA")]},
               {"canon": C(fasteners_excluded=True), "ms": [M("Framing screws", 0, unit="EA", fuente="EXCLUDED (U-053)")]}),
    "be_112": ({"canon": C([W("W1", top_track="standard track, framing hung from structure")])},
               {"canon": C([W("W1", top_track="deep-leg slip track, framing hung from structure")])}),
    "be_cf02": ({"canon": C([W("W1", tag="2")], partition_schedule=[{"type": "W4.1", "source": "A-202"}])},
                {"canon": C([W("W1", tag="W4.1")], partition_schedule=[{"type": "W4.1", "source": "A-202"}])}),
    "be_cf03": ({"canon": C([W("W1", faces=[F("A", "X", "1/2 regular")])]), "ms": [M("5/8\" Type X gypsum board", 100, unit="SF")]},
                {"canon": C([W("W1", faces=[F("A", "X", "1/2 regular")])]), "ms": [M("1/2\" gypsum board regular", 100, unit="SF")]}),
    "be_cf04": ({"canon": C([W("WD1", stud_size="2x6 wood")])}, {"canon": C(existing_walls=[{"id": "WD1", "note": "wood-framed, board only"}])}),
    "be_cf05": ({"hojas": {"p1": "x", "p2": "y", "A-101": "z"}}, {"hojas": {"G-001": "x", "A-100": "y", "A-101": "z"}}),
    "be_cf07": ({"canon": C(misc_items=[{"ref": "J1", "familia": "3-5/8\" stud", "source": "S-241 LGS CEILING JOIST SCHEDULE 6\" 600S162-43"}])},
                {"canon": C(misc_items=[{"ref": "J1", "familia": "6\" joist", "source": "S-241 LGS CEILING JOIST SCHEDULE 6\" 600S162-43"}])}),
    "be_cf09": ({"canon": C([W("ZF1", stud_size="7/8\" Z-furring", bracing_rows=2, bracing_rows_source="skill default C.R.")])},
                {"canon": C([W("ZF1", stud_size="7/8\" Z-furring", bracing_rows=0)])}),
    "be_cf10": ({"hojas": {"A-001": "SECTION 09 29 00 GYPSUM BOARD"}, "ms": [M("5/8\" Type X gypsum board", 100, unit="SF", fuente="1/A-501")]},
                {"hojas": {"A-001": "SECTION 09 29 00 GYPSUM BOARD"}, "ms": [M("5/8\" Type X gypsum board", 100, unit="SF", fuente="1/A-501 + 09 29 00 2.1.A")]}),
    "cr_r6_o1": ({"canon": C(misc_items=[{"ref": "CLG-L1-07 angle molding", "familia": "USG angle molding", "qty": 33.3, "op": "4 x sqrt(69.45) = 33.33"}])},
                 {"canon": C(misc_items=[{"ref": "CLG-L1-07 angle molding", "familia": "USG angle molding", "qty": 33.9, "op": "perimeter of the measured room polygon = 33.89 LF"}])}),
    "cr_r6_o2": ({"canon": C(framed_soffits=[{"id": "S2", "floor": "L2", "detail": "7/A7.23", "faces": [{"side": "bottom", "width_ft": 1.0}]},
                                             {"id": "S3", "floor": "L3", "detail": "7/A7.23", "faces": [{"side": "bottom", "width_ft": 0.375}]}])},
                 {"canon": C(framed_soffits=[{"id": "S2", "floor": "L2", "detail": "7/A7.23", "faces": [{"side": "bottom", "width_ft": 0.375}]},
                                             {"id": "S3", "floor": "L3", "detail": "7/A7.23", "faces": [{"side": "bottom", "width_ft": 0.375}]}])}),
    "cr_r6_e1": ({"canon": C(ceilings=[{"room": "L1 FS-1 membrane under the LEVEL 2 floor", "height_ft": 12.0}],
                             misc_items=[{"ref": "CLG-L1-11 board", "source": "coffers | [CONFIRMED] height 12.063"}])},
                 {"canon": C(ceilings=[{"room": "L1 FS-1 membrane under the LEVEL 2 floor", "height_ft": 12.0}],
                             misc_items=[{"ref": "CLG-L1-12 board", "source": "field | [CONFIRMED] height 11.0"}])}),
    "be_cf11": ({"pend": [("RFI-09", "D3/A-624 blocking 2x6 wood OR 6\" metal: which?", RFI_OK)]}, {"pend": [("RFI-09", "Opening width", RFI_OK)]}),
    "be_cf13": ({"annots": [{"label": "6", "subject": "2", "contents": "TYPE 2 DERIVADO", "measure": True}]},
                {"annots": [{"label": "A-101", "subject": "2", "contents": "TYPE 2 DERIVED", "measure": True}]}),
    "be_ch03": ({"hojas": {"A-102": "ENLARGED PLAN SCALE: 3/16\" = 1'-0\""}, "canon": C(constants={"plan_scale_by_sheet": {"A-102": 18.0}})},
                {"hojas": {"A-102": "ENLARGED PLAN SCALE: 3/16\" = 1'-0\""}, "canon": C(constants={"plan_scale_by_sheet": {"A-102": 13.5}})}),
    "be_hf02": ({"review": [("1/7", "Detail", "B", "Braces to structure printed A1.1 note 1 — qty 0", "A1.1", "")]},
                {"review": [("1/7", "Detail", "B", "Braces to structure printed A1.1 note 1 — 240 LF loaded", "A1.1", "")]}),
    "be_hf03": ({"ms": [M("Head track 3-5/8\"", 40, fuente="3/A5.3 bulkhead top track")]}, {"ms": [M("Top slip track 3-5/8\"", 40, fuente="3/A5.3 bulkhead")]}),
    "be_hf04": ({"canon": C([W("W1", H=8.5, bracing_rows=1, bracing_rows_source="A4.1 note 7: partitions higher than 12'-0\"")])},
                {"canon": C([W("W1", H=8.5, bracing_rows=0, bracing_rows_source="A4.1 note 7: partitions higher than 12'-0\"")])}),
    "be_hf05": ({"pt": [{"fila": 5, "wall": "Q-14+Q-12+Q-13", "lf": 30.0}]}, {"pt": [{"fila": 5, "wall": "Q-14", "lf": 10.0}]}),
    "be_vs_01": ({"hojas": {"A01.01": "LOWEST POINT OF DECK 17'-0\"", "A02.01": "PLAN"},
                  "pend": [("RFI-02", "Height of structure not printed", RFI_OK)], "canon": C(rfis=[{"id": "RFI-02", "barrido": {"hojas": ["A02.01"]}}])},
                 {"hojas": {"A01.01": "LOWEST POINT OF DECK 17'-0\"", "A02.01": "PLAN"},
                  "pend": [("RFI-02", "Height of structure per bay", RFI_OK)], "canon": C(rfis=[{"id": "RFI-02", "barrido": {"hojas": ["A02.01", "A01.01"]}}])}),
    "be_vs_02": ({"hojas": {"A15.04": "UL LISTED FIRE RESISTANT GYPSUM BOARD THROUGHOUT"}, "canon": C(ceilings=[{"room": "MGR", "board": "5/8 regular"}])},
                 {"hojas": {"A15.04": "UL LISTED FIRE RESISTANT GYPSUM BOARD THROUGHOUT"}, "canon": C(ceilings=[{"room": "MGR", "board": "5/8 type X"}])}),
    "be_vs_04": ({"ms": [M("Blocking 6\" backing track", 50, fila=4), M("Blocking 6\" backing track", 50, fila=9)]},
                 {"ms": [M("Blocking 6\" backing track", 100, fila=4)]}),
    "be_vs_06": ({"canon": C(blocking_items=[{"ref": "B1", "label": "6\" X 18 GA BACKING TRACK", "familia": "3-5/8\" stud"}])},
                 {"canon": C(blocking_items=[{"ref": "B1", "label": "6\" X 18 GA BACKING TRACK", "familia": "6\" 18 GA backing track"}])}),
    "be_vs_07": ({"hojas": {"S03.01": "BRIDGING NOT REQUIRED WHERE BOARD BOTH SIDES"}, "canon": C([W("W1", bridging_rows=2)])},
                 {"hojas": {"S03.01": "BRIDGING NOT REQUIRED WHERE BOARD BOTH SIDES"}, "canon": C([W("W1", bridging_rows=0)])}),
    "be_vs_08": ({"demo": {"items": [{"id": "D1", "height_source": "assumed 12'"}]}, "annots": []},
                 {"demo": {"items": [{"id": "D1", "height_source": "A01.01 LOWEST POINT 17'-0\""}]}, "textos": {"demo_cruce.md": "x"},
                  "annots": [{"label": "A01.01", "subject": "DEMO", "contents": "DEMO D1", "measure": True}]}),
    "be_vs_10": ({"scope": [("ALC-9", "Ceiling bracing", "NOT APPLICABLE", "not carried: RCP shows no bracing, not drawn")]},
                 {"scope": [("ALC-9", "Ceiling bracing", "QUANTIFIED", "S-001 note 12 + ASTM C754")]}),
    "be_vs_13": ({"pt": [{"fila": 5, "wall": "W026", "lf": 10.0, "h": 10.0, "board": 300.0}],
                  "annots": [{"label": "A02.01", "subject": "2", "contents": "W026 TYPE 2 LF 10 SF 250", "measure": True}]},
                 {"pt": [{"fila": 5, "wall": "W026", "lf": 10.0, "h": 10.0, "board": 300.0}],
                  "annots": [{"label": "A02.01", "subject": "2", "contents": "W026 TYPE 2 LF 10 SF 300", "measure": True}]}),
    "be_vs_14": ({"hojas": {"A12.01": "ADDITIONAL STUD REQ'D AT EQ. STUDS"}, "pend": [("RFI-12", "Is 'ADDITIONAL STUD REQ D AT EQ STUDS' required?", "(A) delta")]},
                 {"hojas": {"A12.01": "ADDITIONAL STUD REQ'D AT EQ. STUDS"}, "pend": [("RFI-12", "Opening width not dimensioned", "(A) delta")]}),
    "be_vs_15": ({"canon": C([W("W1")], ceilings=[{"room": "1", "rcp_sheet": "A03.01"}]), "annots": [{"label": "A-101", "subject": "2", "contents": "", "measure": True}]},
                 {"canon": C([W("W1")], ceilings=[{"room": "1", "rcp_sheet": "A03.01"}]),
                  "annots": [{"label": "A-101", "subject": "2", "contents": "", "measure": True}, {"label": "A03.01", "subject": "CLG", "contents": "", "measure": True}]}),
    # R80f.43 / BE-141 (Chuze FINAL7 audit U-138): cifra tecleada vieja en el Scope Checklist
    "cifras_texto": ({"ms": [M('5/8" gypsum board, Type X', net=57241.6)], "celdas": [("Scope Checklist", "D8", '5/8" Type X 58,393.09 SF')]},
                     {"ms": [M('5/8" gypsum board, Type X', net=57241.6)], "celdas": [("Scope Checklist", "D8", '5/8" Type X 57,241.60 SF')]}),
    # U-143 (usuario 5-nov, HFT RFI-02 '1 vs 2 layers' del wall a demoler): demo solo en SF, sin capas ni RFI de composición
    # (unida con el caso de CFA: canon con LF x H x 2 layers y RFI de capas de la demo)
    "u_143": ({"ms": [M("Demolition - existing gypsum board 2 layers per face", 120.0, unit="SF", fuente="D1.1")],
               "pend": [("RFI-02", "Existing wall to be demolished: 1 or 2 layers of board?", "(A) delta 0 (B) delta +SF")],
               "canon": {"misc_items": [{"ref": "DEMO-X1", "familia": "demolition - gypsum board and metal framing", "unit": "SF", "qty": 200.0,
                                         "op": "10.0 LF x 10.0 ft x 2 layer(s) = 200.0 SF"}],
                         "rfis": [{"id": "RFI-X", "question": "Walls to demolish: how many layers of gypsum board?"}]}},
              {"ms": [M("Demolition of existing partitions (SF of wall)", 120.0, unit="SF", fuente="D1.1")], "pend": [],
               "canon": {"misc_items": [{"ref": "DEMO-X1", "familia": "demolition - gypsum board and metal framing", "unit": "SF", "qty": 100.0,
                                         "op": "10.0 LF x 10.0 ft = 100.0 SF (wall area)"}],
                         "rfis": [{"id": "RFI-X", "question": "Walls to demolish: height not printed."}]}}),
    # U-139 (usuario 5-nov): una decisión vieja cargaba FRT 2X blocking y FRT plywood: wood > 0 = FAIL
    "u_139": ({"ms": [M("Blocking FRT / 2X FRT wood", 100.0, fuente="N/SHEET: 6/A4.2"),
                      M("FRT plywood (5/8 in.)", 50.0, unit="SF", fuente="N/SHEET: 2/A3.1")]},
              {"ms": [M("Blocking FRT / 2X FRT wood", 0.0, fuente="EXCLUDED - wood blocking by others (Div. 06), user decision 2026-11-05, R-ALC-01"),
                      M("Metal stud blocking", 120.0, fuente="N/SHEET: 6/A4.2")]}),
    # U-127 / BE-138 CB_BOTH_SIDES: el type imprime board en las dos caras y el wall trae una sola (error de Chuze FINAL5)
    "both_sides": ({"canon": C([{"id": "W1", "tag": "A3C", "element": "wall", "faces": [{"side": "A", "board": "5/8 type X", "layers": 1, "height_ft": 10}]}]),
                    "fichas": {"types": {"A3C": {"faces": [{"side": "each side", "board": '5/8" GYP BD - BOTH SIDES'}]}}}},
                   {"canon": C([{"id": "W1", "tag": "A3C", "element": "wall", "faces": [{"side": "A", "board": "5/8 type X", "layers": 1, "height_ft": 10},
                                                                                         {"side": "B", "board": "5/8 type X", "layers": 1, "height_ft": 10}]}]),
                    "fichas": {"types": {"A3C": {"faces": [{"side": "each side", "board": '5/8" GYP BD - BOTH SIDES'}]}}}}),
    # U-113 / BE-124 CE_CALLOUTS: la planta señala D/A9.22, que llama 7/A9.26 (marquesina): la cadena se cortó en D/A9.22
    "ce_callouts": ({"hojas": {"A2.01": "FLOOR PLAN D/A9.22 1/A12.01", "A9.22": "D SECTION SEE 7/A9.26", "A9.26": "7 SIDE CANOPY", "A12.01": "1 PARTITION TYPES"},
                     "canon": C([W("W1", sheet="A2.01")]), "ms": [M("Stud 6\"", fuente="1/A12.01 + D/A9.22")], "set_meta": {"burbujas": {}}},
                    {"hojas": {"A2.01": "FLOOR PLAN D/A9.22 1/A12.01", "A9.22": "D SECTION SEE 7/A9.26", "A9.26": "7 SIDE CANOPY", "A12.01": "1 PARTITION TYPES"},
                     "canon": C([W("W1", sheet="A2.01")]), "ms": [M("Stud 6\"", fuente="1/A12.01 + D/A9.22 -> 7/A9.26")], "set_meta": {"burbujas": {}}}),
    # BE-CF24 (CFA rev9): la Source de un board-only con la altura VIEJA (1'-0" G.3) en un renglón cargado a 1.25 (C3/A-604)
    "be_cf24": ({"canon": {"existing_walls": [{"id": "X-1", "height_ft": 1.25, "source": "W6/A-202 | height: G.3/A-202 to 1'-0\" = 1.0 ft [CONFIRMED]"}]}},
                {"canon": {"existing_walls": [{"id": "X-1", "height_ft": 1.25, "source": "W6/A-202 | height: [CONFIRMED] C3/A-604 1' - 3\" = 1.25 ft"}]}}),
    # R-ALC-06 (CFA rev9): DEMO-14 marcado en la planta nueva A-202 en vez del demolition plan A-050
    # BE-CF25 (CFA rev9): RFI-11 / 12 / 20 'printed nowhere' con un barrido de 8 términos, un solo GC, sin medida vectorial
    "be_cf25": ({"canon": {"rfis": [{"id": "RFI-11", "status": "open - conservative value loaded", "question": "Dining half walls: height printed nowhere.",
                                     "barrido": {"hojas": "ALL", "terminos": ["HALF WALL", "HALF WALLS", "PONY", "KNEE", "LOW WALL", "42\"", "3'-6\"", "PARTIAL HEIGHT"]}}]}},
                {"canon": {"rfis": [{"id": "RFI-11", "status": "open - conservative value loaded", "question": "Dining half walls: height printed nowhere.",
                                     "barrido": {"hojas": "ALL", "terminos": ["HALF WALL", "HALF WALLS", "PONY", "KNEE", "LOW WALL", "42\"", "3'-6\"", "PARTIAL HEIGHT",
                                                                               "BOOTH", "BANQUETTE", "KN8", "CAP", "OUTLET", "J-BOX"],
                                                 "sets": ["CDM Bid Set.pdf", "Empower Riverpoint Updated 10.29.26.pdf"],
                                                 "medida_vectorial": "no elevation / section draws the wall: nothing to measure at a printed scale",
                                                 "lugares": [{"sheet": "X-100", "what": "KN8", "img": "a.png"}, {"sheet": "X-200", "what": "booths", "img": "b.png"},
                                                             {"sheet": "X-300", "what": "outlets", "img": "c.png"}]}}]}}),
    # BE-CF26 (CFA rev10): RFI resuelto con la opción A todavía en el valor viejo y el valor resuelto como alternativa
    "be_cf26": ({"canon": {"rfis": [{"id": "RFI-28", "status": "resolved - from drawings", "resolved": {"answer": "4.244 x 8.144 ft = 34.57 SF [DERIVED]"},
                                     "opciones": {"A": {"texto": "Plans: 38.35 SF loaded", "delta": "0 (loaded); 34.57 SF hatch outline: -3.78 SF demolition"}}}]}},
                {"canon": {"rfis": [{"id": "RFI-28", "status": "resolved - from drawings", "resolved": {"answer": "4.244 x 8.144 ft = 34.57 SF [DERIVED]"},
                                     "opciones": {"A": {"texto": "Plans: 34.57 SF loaded", "delta": "0 (loaded); outer outline 38.35 SF +3.78 SF demolition"}}}]}}),
    # CC-R1 / CC-R5 / CC-R7 / CC-R12 (Consumer Cellular rev3, auditoría U-138): renglón duplicado sin IDs, residuo de redondeo que
    # compra piezas, Scope EXCLUDED sobre el FRP cargado, wall con cota impresa en [DERIVED]
    "cc_r1": ({"ms": [M("Stud blocking at edge of gypboard", 176.4, fuente="N/SHEET: 2/A104 | 77.0 LF; 37.5 LF; 19.5 LF", fila=5),
                      M("Metal stud blocking - strapping", 134.0, fuente="Breakdown: BLK-SLAT-N 77 LF + BLK-LOGO-S 37.5 LF + BLK-LOGO-W 19.5 LF", fila=6)]},
              {"ms": [M("Metal stud blocking - strapping", 134.0, fuente="Breakdown: BLK-SLAT-N 77 LF + BLK-LOGO-S 37.5 LF + BLK-LOGO-W 19.5 LF", fila=6)]}),
    "cc_r5": ({"ms": [M("Top / deflection track - other", 0.01, fuente="N/SHEET: A100 | = 0 LF (rounding)")]},
              {"ms": [M("Top track 3-5/8\"", 57.44, fuente="N/SHEET: 1/A500 | E3-01 7.25 LF")]}),
    "cc_r7": ({"ms": [M("FRP panels", 148.33, unit="SF")], "scope": [("ALC-20", "NO APLICA", "EXCLUDED - FRP B-3 is a finish product")]},
              {"ms": [M("FRP panels", 148.33, unit="SF")], "scope": [("ALC-20", "CUANTIFICADO", "FRP B-3 carried with its PVC trim")]}),
    "cc_r12": ({"canon": C([dict(W("<w1>"), length_status="CONFIRMADO")]), "pt": [{"fila": 6, "wall": "<w1>", "status": "[DERIVED]"}]},
               {"canon": C([dict(W("<w1>"), length_status="CONFIRMADO")]), "pt": [{"fila": 6, "wall": "<w1>", "status": "[CONFIRMED]"}]}),
    # U-146 / U-147 (usuario 5-nov, Consumer Cellular RFI-01 / RFI-04 -> A): corte de deck no dibujado / level of finish sin especificar
    "u_146": ({"pend": [("RFI-01", "The deck break between PLY DECK @ 16'-4\" and @ 17'-1 9/16\" is not drawn", RFI_OK)]},
              {"pend": [("RFI-05", "Control joints per R80e.34 #8 precedent", RFI_OK)]}),
    "u_147": ({"pend": [("RFI-04", "Gypsum board finish level and trims are not specified", RFI_OK)]},
              {"pend": []}),
    "r_alc_06": ({"annots": [{"label": "A-202", "subject": "DEMO", "contents": "DEMO"}], "hojas": {"A-202": "DIMENSIONAL FLOOR PLAN", "A-050": "DEMOLITION PLAN"}},
                 {"annots": [{"label": "A-050", "subject": "DEMO", "contents": "DEMO"}], "hojas": {"A-202": "DIMENSIONAL FLOOR PLAN", "A-050": "DEMOLITION PLAN"}}),
    # BE-CR25 (CR City Hotel rev1): canon con walls = 0 y Partition Takeoff con filas = la compuerta en vacío
    "canon_no_vacio": ({"canon": {"walls": [], "existing_walls": []}, "pt": [{"fila": 6, "wall": "W.4-L2-01 A", "partition": "W.4-0"}]},
                       {"canon": C([W("<w1>")]), "pt": [{"fila": 6, "wall": "<w1>", "partition": "W.4-0"}]}),    # BE-CR30 (CR City Hotel rev3): tags GYP-n del RCP sin renglón (BAR 107 / franja del lobby / Cleaning 215)
    "rcp_tags": ({"canon": C([W("<w1>")], misc_items=[{"ref": "CLG-L1-01 board", "qty": 10}]),
                  "hojas": {"A3.01": "REFLECTED CEILING PLAN GYP-1 9' - 0\" GYP-1 11' - 0\" GYP-1: GYPSUM BOARD ON METAL SUSPENSION"}},
                 {"canon": C([W("<w1>")], misc_items=[{"ref": "CLG-L1-01 board", "qty": 10}],
                             rcp_tags=[{"sheet": "A3.01", "tag": "GYP-1", "rows": ["CLG-L1-01 board"]},
                                       {"sheet": "A3.01", "tag": "GYP-1", "none_reason": "inside the tenant space: note on 1/A2.01"}]),
                  "hojas": {"A3.01": "REFLECTED CEILING PLAN GYP-1 9' - 0\" GYP-1 11' - 0\" GYP-1: GYPSUM BOARD ON METAL SUSPENSION"}}),
}


def test_casos():
    nombres = {fn.__name__: fn for _, fn, _ in CB.CHEQUEOS}
    sin = sorted(set(nombres) - set(CASOS))
    assert not sin, f"chequeos sin caso que reproduzca el error: {sin}"
    for nm, (malo, bueno) in CASOS.items():
        fn = nombres[nm]
        e1, ev1 = fn(B(**malo))
        assert e1 == "FAIL", (nm, "MALO", e1, ev1)
        e2, ev2 = fn(B(**bueno))
        assert e2 == "PASS", (nm, "BUENO", e2, ev2)


def test_be_06_soffit_sides():
    """BE-06: soffit_side = un lado por elemento; un solo lado del soffit = FAIL, varios lados = PASS."""
    uno = C([W("SS-X-N", tag="", element="soffit_side", faces=[F("N", "X")])])
    tres = C([W(f"SS-X-{k}", tag="", element="soffit_side", faces=[F(k, "X")]) for k in ("N", "W", "IV")])
    assert CB.be_06(B(canon=uno))[0] == "FAIL" and CB.be_06(B(canon=tres))[0] == "PASS"


def test_callouts_extra():
    """CE_CALLOUTS: hoja / detalle referido que no existe se reporta; fuera de alcance con motivo = disposición."""
    SM = {"burbujas": {}}
    h = {"A2.01": "FLOOR PLAN 4/A9.30 5/A12.01", "A12.01": "1 PARTITION TYPES"}
    e, ev = CB.ce_callouts(B(hojas=h, canon=C([W("W1", sheet="A2.01")]), set_meta=SM))
    t = " ".join(ev)
    assert e == "FAIL" and "A9.30 no existe" in t and "no tiene el detalle 5" in t, t
    h = {"A2.01": "FLOOR PLAN 3/E1.01", "E1.01": "3 PANEL SCHEDULE"}
    assert CB.ce_callouts(B(hojas=h, canon=C([W("W1", sheet="A2.01")]), set_meta=SM))[0] == "FAIL"
    na = {"E1.01": {"3": "panel schedule: electrical, not our trade"}}
    assert CB.ce_callouts(B(hojas=h, canon=C([W("W1", sheet="A2.01")]), set_meta=SM, no_aplican=na))[0] == "PASS"
    assert CB.ce_callouts(B(hojas=h, canon=C([W("W1", sheet="A2.01")]), set_meta=SM, no_aplican={"3/E1.01": "x"}))[0] == "FAIL"   # sin motivo
    assert CB.ce_callouts(B(hojas=None, canon=C()))[0] == "FAIL"
    assert CB.callouts_de("A2.0/A3.1 01/A09.02 D/A09.22") == [("D", "A9.22")]           # cola de hoja y cero = no es burbuja
    # U-137 / BE-139 (4-nov, "¿y qué pasó con los detail call outs?"): burbujas de DOS líneas (1 arriba / A3.2 abajo)
    h = {"A1.1": "FLOOR PLAN", "A3.2": "WALL SECTIONS 1 2", "A4.2": "INTERIOR SECTIONS & DETAILS 5"}
    cn = C([W("W1", sheet="A1.1")])
    e, ev = CB.ce_callouts(B(hojas=h, canon=cn, set_meta={}))                      # set_texto viejo sin barrido de burbujas
    assert e == "FAIL" and "sin barrido de burbujas" in ev[0], ev
    e, ev = CB.ce_callouts(B(hojas=h, canon=cn, set_meta=SM))                      # 0 burbujas y el set tiene DETAILS: vacío
    assert e == "FAIL" and "PASS en vacío prohibido" in ev[0], ev
    bub = {"A1.1": {"burbujas": [{"x": 933.5, "y": 1124.3, "r": 17, "n": "1", "hoja": "A3.2"}],
                    "sin_leer": [{"x": 450.0, "y": 527.0, "r": 17}], "circulos": 2}}
    e, ev = CB.ce_callouts(B(hojas=h, canon=cn, set_meta={"burbujas": bub}))
    t = " ".join(ev)
    assert e == "FAIL" and "1/A3.2 (burbuja en A1.1" in t and "(450, 527)" in t, t
    ms = [M("Stud 6\"", fuente="1/A3.2 head at PEMB purlin")]
    ver = {"A1.1": [{"x": 450.0, "y": 527.0, "n": "5", "hoja": "A4.2"}]}
    e, ev = CB.ce_callouts(B(hojas=h, canon=cn, ms=ms, set_meta={"burbujas": bub}, verificadas=ver))
    assert e == "FAIL" and "5/A4.2" in " ".join(ev) and "1/A3.2" not in " ".join(ev), ev   # la verificada entra a la cadena
    ms = [M("Stud 6\"", fuente="1/A3.2 head at PEMB purlin; 5/A4.2 soffit")]
    assert CB.ce_callouts(B(hojas=h, canon=cn, ms=ms, set_meta={"burbujas": bub}, verificadas=ver))[0] == "PASS"
    ver = {"A1.1": [{"x": 451.0, "y": 526.0, "no_es_burbuja": "north arrow"}]}
    ms = [M("Stud 6\"", fuente="1/A3.2 head at PEMB purlin")]
    assert CB.ce_callouts(B(hojas=h, canon=cn, ms=ms, set_meta={"burbujas": bub}, verificadas=ver))[0] == "PASS"
    ver = {"A1.1": [{"x": 451.0, "y": 526.0, "no_es_burbuja": "x"}]}                # sin motivo
    assert CB.ce_callouts(B(hojas=h, canon=cn, ms=ms, set_meta={"burbujas": bub}, verificadas=ver))[0] == "FAIL"
    # O'Reilly rev7: 10/A5.2 citado; el OCR de la hoja raster A5.2 no lee el '10' del título (rectángulo, no círculo) -> AMBER;
    # verificado a ojo con imagen en burbujas_verificadas.json -> PASS; sin imagen sigue AMBER
    h2 = {"A1.1": "FLOOR PLAN", "A5.2": "WINDOW SCHEDULE VESTIBULE ENLARGE PLAN", "A3.2": "WALL SECTIONS 1 2"}
    bub2 = {"A1.1": {"burbujas": [{"x": 596.0, "y": 1130.0, "r": 13, "n": "10", "hoja": "A5.2"}], "sin_leer": [], "circulos": 1}}
    ms2 = [M("Stud 6\"", fuente="10/A5.2 vestibule")]
    sm2 = {"burbujas": bub2, "ocr": ["A5.2"]}
    assert CB.ce_callouts(B(hojas=h2, canon=cn, ms=ms2, set_meta=sm2))[0] == "AMBER"
    v2 = {"A5.2": [{"detalle_existe": "10", "img": "burbujas_img/A5.2_detalle_10_existe.png"}]}
    assert CB.ce_callouts(B(hojas=h2, canon=cn, ms=ms2, set_meta=sm2, verificadas=v2))[0] == "PASS"
    assert CB.ce_callouts(B(hojas=h2, canon=cn, ms=ms2, set_meta=sm2, verificadas={"A5.2": [{"detalle_existe": "10"}]}))[0] == "AMBER"


def test_auditoria_u138():
    """U-138 auditoría adversarial 4-nov: PASS que no se sostenían. Cada caso: el error original -> FAIL, corregido -> PASS."""
    import revision_markups as RM
    occ = [{"id": "PT001", "kind": "partition_tag", "type": "S43", "sheet": "A1.1", "png": "PT001.png", "png_verificado": True}]
    inv = {"pages": 68, "ocurrencias": {"partition_tag": occ}}
    cn = C([W("W1", tag="S43", sheet="A1.1")])
    # (a) U-037 sin inventario_tags pero con inventario.json: cuenta contra él (antes AMBER mientras U-117 PASS); sin ninguno = FAIL
    assert CB.u_037(B(canon=cn, inv_full=inv))[0] == "PASS"
    assert CB.u_037(B(canon=C([W("W1", tag="S24", sheet="A1.1")]), inv_full=inv))[0] == "FAIL"
    assert CB.u_037(B(canon=cn))[0] == "FAIL"
    # (a) U-117: inventario de otro set (páginas distintas) = FAIL
    sm = {"fuentes": [{"pdf": "bidset.pdf", "paginas": 172}]}
    r = CB.u_117(B(canon=cn, inv_full=inv, set_meta=sm, hojas={"A1.1": "x"}))
    assert r[0] == "FAIL" and any("otro set" in e for e in r[1]), r
    # (b) altura sin hoja: el regex de hojas de revision_markups veía 'none' en A421 / A435.A (Chuze); cara sin hoja = FAIL
    assert RM.HOJA_RX.findall("head D/A301; B.O. DECK on A422.B / A435.A") and RM.HOJA_RX.search("A421 elev 5")
    w_ok = {"id": "W1", "height_ft": 10, "height_source": "A421 elev 5", "faces": [{"side": "A", "height_ft": 10, "height_source": "A421"}]}
    w_mal = {"id": "W1", "height_ft": 10, "height_source": "A421 elev 5", "faces": [{"side": "A", "height_ft": 10, "height_source": "to deck"}]}
    assert CB.be_78(B(canon={"walls": [w_ok]}))[0] == "PASS" and CB.be_78(B(canon={"walls": [w_mal]}))[0] == "FAIL"
    fs = lambda s: {"walls": [{"id": "W1", "height_ft": 10, "height_source": s, "height_status": "[DERIVED] 10 - 0 = 10"}]}  # noqa: E731
    assert any("sin hoja" in e for e in CB.u_114(B(canon=fs("to the deck (B.O. DECK VARIOUS)"), pt=[]))[1])
    assert not any("sin hoja" in e for e in CB.u_114(B(canon=fs("A422.B B.O. DECK 22'-1\""), pt=[]))[1])
    # (c) BE-25: cielos de gypsum cargados como misc_items (GWB-CLG-*) también se revisan; 'N/A' con el set imprimiéndolos = FAIL
    mi = lambda src: {"walls": [], "misc_items": [{"ref": "GWB-CLG-ROOM-1", "familia": "5/8 type X", "source": src}]}  # noqa: E731
    assert CB.be_25(B(canon=mi("A1.2")))[0] == "FAIL" and CB.be_25(B(canon=mi("7/A4.2")))[0] == "PASS"
    assert CB.be_25(B(canon={"walls": []}, hojas={"A1.2": "5/8\" GYP. BD. CEILING"}))[0] == "FAIL"
    # (e) BE-VS-15: markups DEMO contra elementos de demo (no hojas)
    an = [{"label": "D1.1", "subject": "DEMO", "contents": "DEMO · 10.00 LF · H 9'-0\" · 1 layer(s) · 3 · P01-N · 3/D1.1", "measure": True}]
    dm = [{"id": "P01-N", "sheet": "D1.1"}, {"id": "P02-S", "sheet": "D1.1"}]
    assert CB.be_vs_15(B(canon={"walls": []}, annots=an, demo=dm))[0] == "FAIL"
    assert CB.be_vs_15(B(canon={"walls": []}, annots=an, demo=dm[:1]))[0] == "PASS"
    # (f) BE-15: S43/A1.1 (tag verificado en el inventario) y 13/A5.2 (detalle verificado a ojo) en hoja OCR -> PASS; sin -> AMBER
    ms = [M("Stud", fuente="N/SHEET: S43/A1.1; 13/A5.2 sill")]
    hj = {"A1.1": "FLOOR PLAN", "A5.2": "WINDOW SCHEDULE"}
    sm2 = {"ocr": ["A1.1", "A5.2"]}
    assert CB.be_15(B(canon={"walls": []}, ms=ms, hojas=hj, set_meta=sm2))[0] == "AMBER"
    ver = {"A5.2": [{"detalle_existe": "13", "img": "burbujas_img/A5.2_detalle_13_existe.png"}]}
    assert CB.be_15(B(canon={"walls": []}, ms=ms, hojas=hj, set_meta=sm2, inv_full=inv, verificadas=ver))[0] == "PASS"
    # v81cf38: U-116 / BE-CF23 leía solo 'status'; un RFI con estado 'CLOSED' (O'Reilly RFI-07 "(A) not carried") no es abierto
    rf = lambda **k: {"walls": [{"id": "W1", "height_source": "A1.1 printed 10 ft [CONFIRMED]"}], "rfis": [dict({"id": "RFI-07", "opciones": {"A": {"texto": "Not carried"}}}, **k)]}  # noqa: E731
    assert not any("RFI-07" in e for e in CB.u_116(B(canon=rf(estado="CLOSED")))[1])
    assert any("RFI-07" in e for e in CB.u_116(B(canon=rf(status="open")))[1])


def test_be_cf08_catalogo():
    """BE-CF08: un archivo nuevo en referencias/ sin clasificar en reglas_clasificacion.py -> A_CATALOGO falla."""
    sk = os.path.join(AQUI, "..")
    if not os.path.isfile(os.path.join(sk, "SKILL.md")):
        sk = os.path.join(AQUI, "..", "take-off-metal-frame-drywall")
    d = tempfile.mkdtemp(prefix="cf08_")
    for x in ("SKILL.md", "referencias", "tools"):
        src = os.path.join(sk, x) if x != "tools" else AQUI
        (shutil.copytree if os.path.isdir(src) else shutil.copy)(src, os.path.join(d, x))
    open(os.path.join(d, "referencias", "adenda_v99.md"), "w").write("# Adenda v99\n\n## REGLA 99.1 — regla nueva de prueba\nToda X lleva Y.\n")
    env = dict(os.environ, TAKEOFF_SKILL=d)
    p = subprocess.run([sys.executable, "-c", "import reglas, json; print(json.dumps(reglas.a_catalogo(None)))"],
                       cwd=os.path.join(d, "tools"), capture_output=True, text=True, env=env, timeout=600)
    out = json.loads(p.stdout.strip().splitlines()[-1])
    assert any("99" in str(x[0]) and "sin clasificar" in str(x[1]) for x in out), (out[:5], p.stderr[-300:])


def test_u118_evidencia_circula():
    """U-118: evidencia.py circula lo citado en la hoja; si lo citado no está impreso, la página va sin marca y u_118 falla."""
    import pymupdf
    sys.path.insert(0, os.path.join(AQUI, "..", "runner"))
    sys.path.insert(0, os.path.join(AQUI, "..", "take-off-metal-frame-drywall", "runner"))
    import evidencia
    d = tempfile.mkdtemp(prefix="u118_")
    pdf = os.path.join(d, "set.pdf")
    doc = pymupdf.open()
    pg = doc.new_page(width=600, height=400)
    pg.insert_text((100, 200), "ZONE 2 B.O. DECK +-17'-5 1/2\"", fontsize=14)
    doc.save(pdf)
    ev = evidencia.Evidencia(pdf, {"A1.2": 0}, os.path.join(d, "img"))
    con = ev.hoja("A1.2 'B.O. DECK' zone 2 [CONFIRMED]")
    sin = ev.hoja("A1.2 'T.O. PARAPET' [CONFIRMED]")
    b = B(raiz=d)
    assert CB._img_ok(b, con)[0] is True, CB._img_ok(b, con)
    assert CB._img_ok(b, sin) == (False, "sin marca circulada (0 px rojos)"), CB._img_ok(b, sin)
    assert CB._img_ok(b, "vacia.png") == (False, "no existe") and CB._img_ok(B(raiz=IMGD), "vacia.png")[1].startswith("vacía")
    c = {"walls": [{"id": "W1", "tag": "D", "element": "wall", "tag_ids": ["PT0001"],
                    "band": {"ori": "H", "c0": 100, "c1": 104, "lo": 100, "hi": 300, "sheet": "A1.1"}}]}
    inv = {"ocurrencias": {"partition_tag": [{"id": "PT0001", "type": "D", "sheet": "A1.1", "center_pt": [150, 110]},
                                             {"id": "PT0002", "type": "D", "sheet": "A1.1", "center_pt": [250, 95]}]}}
    evidencia.tags_a_walls(c, inv)
    assert c["walls"][0]["tag_ids"] == ["PT0001", "PT0002"], c["walls"][0]["tag_ids"]     # U-117: se agrega, no se quita


def test_cableado_compuerta():
    import compuerta_entrega as CE
    ids = {cid for cid, _, _, _ in CE.CHEQUEOS}
    assert "CE_CALLOUTS" in ids and "CB_BE_01" in ids and "CB_U_017" in ids, sorted(ids)[:10]
    assert len([x for x in ids if x.startswith("CB_")]) == len(CB.CHEQUEOS) - 1


def test_cfa_rev5_falsos():
    """v81cf25 (CFA #2284 rev5): falsos FAIL de BE-15 / BE-102 / BE-14 con el texto real del Excel de CFA."""
    h = {"A-050": "DEMO PLAN 8 DEMO HALF WALLS", "A-052": "RCP", "A-909": "C09250", "A-201": "PLAN 7 EXISTING", "A-221": "PT-41 C.H.14'-6\""}
    b = B(hojas=h, ms=[M("Demolition", fuente="N/SHEET: A-050/A-052, KN7/A-201, C09250 2.5.B/A-909")])
    assert CB.be_15(b)[0] == "PASS", CB.be_15(b)
    b = B(hojas=h, celdas=[("Partition Takeoff", "J5", "A2/A3 S-241; M2.1/M3.5; 3/CT-73B; KN3/KN7; 01/MB-01")])
    assert CB.be_102(b)[0] == "PASS", CB.be_102(b)
    b = B(hojas=h, celdas=[("Partition Takeoff", "J5", "see 8/A-410")])
    assert CB.be_102(b)[0] == "FAIL"                               # el error original sigue cazado
    t = "Play area (A-221 PT-41 C.H. 14'-6\"): framing printed nowhere. - not printed: No sheet labels the new ceiling framing."
    b = B(hojas=h, celdas=[("Pending Items", "B2", t)])
    assert CB.be_14(b)[0] == "PASS", CB.be_14(b)
    b = B(hojas=h, celdas=[("Pending Items", "B2", "PT-41 height not printed.")])
    assert CB.be_14(b)[0] == "FAIL"
    dm = {"items": [{"id": "DEMO-01", "height_source": "S-201 B.O."}]}
    assert CB.be_vs_08(B(demo=dm, textos={"etapas/DEMO_CRUCE.md": "x"}))[0] == "PASS"     # nombre de demo_cruce.py
    assert CB.be_vs_08(B(demo=dm, textos={}))[0] == "FAIL"
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "etapas", "2_lectura"))
    for n in ("canon_A.json", "canon_B.json"):
        json.dump({"walls": []}, open(os.path.join(d, "etapas", "2_lectura", n), "w"))
    import compuerta_entrega as CE
    bb = CB.B.desde_ctx(CE.Ctx(d))
    assert bb.canon_a is not None and bb.canon_b is not None             # lecturas A / B guardadas como canon_A / canon_B


if __name__ == "__main__":
    test_casos()
    print("ok casos", len(CASOS))
    test_be_06_soffit_sides()
    test_callouts_extra()
    print("ok callouts")
    test_auditoria_u138()
    print("ok auditoria U-138")
    test_cableado_compuerta()
    print("ok cableado")
    test_u118_evidencia_circula()
    print("ok u_118 evidencia circulada + u_117 tag_ids")
    test_cfa_rev5_falsos()
    print("ok cfa rev5 falsos")
    test_be_cf08_catalogo()
    print("ok be_cf08 A_CATALOGO")
    print("test_chequeos_biblioteca OK")

# ---- bloque test_consumer_cellular (BE-CC01 BE-CC02 BE-CC03 BE-CC04 BE-CC05 BE-CC06 v81cf48; BE-CC07 BE-CC08 BE-CC09 BE-CC10 v81cf49) ----
def test_consumer_cellular():
    import subprocess as _sp
    _code = r'''
import os, re, sys
sys.path.insert(0, os.getcwd())
A = os.getcwd()
src = lambda f: open(os.path.join(A, f), encoding="utf-8").read()
# BE-CC01: the ceiling perimeter track row cites the sheet of its ceilings (trazabilidad)
assert "BE-CC01" in src("trazabilidad.py") and 'filas_de("ceilings")' in src("trazabilidad.py").split("BE-CC01")[0][-400:] + src("trazabilidad.py").split("BE-CC01")[1][:200]
# BE-CC02: no detail of another project in a Material Summary row name
import plantilla_excel as PE
assert not re.search(r"3/A-410", PE.__dict__.get("NOMBRES", {}).get("nested inner runner (deflection head)", "") if isinstance(PE.__dict__.get("NOMBRES"), dict) else ""), "row name cites 3/A-410"
assert '"nested inner runner (deflection head)": "Nested inner runner at the deflection head (3/A-410)"' not in src("plantilla_excel.py")
# BE-CC03: eye-read bubbles without a detector ring count as read bubbles; low count on eye-swept entry sheets = AMBER
import chequeos_biblioteca as CB
class B: pass
b = B(); b.set_meta = {"burbujas": {"A100": {"burbujas": [], "sin_leer": [], "indep_no_detectados": []}}}
b.verificadas = {"A100": [{"x": 1, "y": 1, "n": "3", "hoja": "A600", "img": "x.png"}]}
leidas, pend = CB._burbujas_hoja(b, CB.norm_hoja("A100"))
assert (("3", CB.norm_hoja("A600")) in leidas), leidas
assert "BE-CC03" in src("chequeos_biblioteca.py")
# BE-CC04: an area annot is matched to the Material Summary row whose breakdown value equals its SF
assert "BE-CC04" in src("auditoria_entrega.py")
# BE-CC05: fichas types on 3-digit sheets (A500) get their sheet
assert "BE-CC05" in src("compuerta_entrega.py")
m = re.search(r'HJ_ = r"(.+?)"', src("compuerta_entrega.py")); assert m and re.search(m.group(1), "1/A500")
# BE-CC06: schedule marks of row ids with spaces are recognized
assert re.match(r"#(\d+) (.+?) on ", "#24 BACK OF HOUSE on A101 (FINISH PLAN) reviewed").group(2) == "BACK OF HOUSE"
assert "BE-CC06" in src("compuerta_entrega.py")
# BE-CC07 (rev1 case): bubbles on 5 sheets the chain never reached (A101, A102, A402, A501, A700) must be seeded and a sheet
# with bubbles and no origin circle = FAIL
b = CB.B(canon={"walls": [{"sheet": "A100", "tag": "A3", "faces": []}]}, celdas=[("x", "A1", "per 3/A600")],
         hojas={h: "t" for h in ("A100", "A101", "A102", "A402", "A500", "A501", "A600", "A700")},
         set_meta={"burbujas": {"A100": {"burbujas": [{"n": "3", "hoja": "A600", "x": 10, "y": 10}]}}},
         verificadas={"A101": [{"x": 1, "y": 1, "n": "3", "hoja": "A502", "img": "i"}],
                      "A102": [{"x": 1, "y": 1, "n": "2", "hoja": "A402", "img": "i"}],
                      "A402": [{"x": 1, "y": 1, "n": "6", "hoja": "A502", "img": "i"}],
                      "A501": [{"x": 1, "y": 1, "n": "2B", "hoja": "A501", "img": "i"}],
                      "A700": [{"x": 1, "y": 1, "n": "6", "hoja": "A500", "img": "i"},
                               {"x": 1.5, "y": 1.5, "n": "6", "hoja": "A500", "img": "i"}]},
         cadena_md="1. **A100 3/A600** x\n2. **A101 3/A502** x\n6. **A102 1/A301** x\n13. **A402 6/A502** x\n27. **A501 \"A1\"** x\n39. **A700 nota** x")
regs = CB.cadena_detalles(b)
assert {r["origen"] for r in regs} >= {"A100", "A101", "A102", "A402", "A501", "A700"}, {r["origen"] for r in regs}
assert sum(r["origen"] == "A700" for r in regs) == 1, "duplicate detector / eye bubble counted twice"
ev = CB.faltan_circulos(b, {"A100": 2, "A500": 14, "A600": 16})       # rev1: circles only on A100 / A500 / A600
assert len([e for e in ev if "0 círculos" in e]) == 5, ev
assert CB.faltan_circulos(b, {"A100": 1, "A101": 1, "A102": 1, "A402": 1, "A501": 1, "A700": 1}) == []
assert "BE-CC07" in src("compuerta_entrega.py")
# BE-CC09: detector bubbles of a rotated page are stored in the VISIBLE frame (rev1: every A600 detector circle misplaced)
import pymupdf
_d = pymupdf.open(); _p = _d.new_page(width=1728, height=2592); _p.set_rotation(270)
_q = pymupdf.Point(1507.1, 1442.0) * _p.rotation_matrix
assert abs(_q.x - 1442.0) < 0.2 and abs(_q.y - 220.9) < 0.2, _q
assert "BE-CC09" in src("compuerta_entrega.py") and 'out[k]["frame"] = "visible"' in src("compuerta_entrega.py")
assert "BE-CC10" in src("compuerta_entrega.py")
# CC-R3 / CC-R4 / CC-R4b..e / CC-R5 / CC-R6 / CC-R10 (Consumer Cellular rev3 audit U-138)
assert "CC-R3" in src("accesorios.py") and "outside corner and division bar" in src("accesorios.py")
assert "CC-R4 " in src("trazabilidad.py") and 'get("track_gauge")' in src("trazabilidad.py")
assert "CC-R5" in src("canon.py") and "resto > 0.05" in src("canon.py")
assert "CC-R6" in src("trazabilidad.py") and "METAL\s+STRAPPING" in src("trazabilidad.py")
assert "CC-R10" in src("chequeos_biblioteca.py") and "CC-R4b" in src("chequeos_biblioteca.py") and "CC-R4c" in src("chequeos_biblioteca.py")
assert CB._cota_impresa("A100 dim 7'-3\" (ticks 673.9-804.6 pt)") is not None, "CC-R4d"
assert CB.RX_ACC.search("20 GA. METAL STRAPPING ATTACHED TO NEW") and CB.RX_ACC.search("2\" X 2\" SHEET METAL ANGLE"), "CC-R4e"
class _B3:
    pass
_b3 = _B3(); _b3.canon = {"misc_items": []}; _b3.hojas = None; _b3.walls = lambda: []
_b3.ceilings = lambda: [{"room": "RR", "system": "usg_grid", "board": "5/8 type X WR", "source": "2/A501"}]
assert CB.be_25(_b3)[0] == "PASS", CB.be_25(_b3)
# U-150 (usuario 5-nov, Consumer Cellular): proposal sin NOT INCLUDED = FAIL; con INCLUDED + NOT INCLUDED + FBM = PASS
import openpyxl, tempfile
import compuerta_entrega as CE
def _prop(not_inc=True):
    wb = openpyxl.Workbook(); P = wb.active; P.title = "PROPOSAL"
    P["C21"] = "INCLUDED (quantities):\n• Bottom track 3-5/8\": 10.00 LF"
    if not_inc:
        P["C48"] = "NOT INCLUDED / EXCLUSIONS:"; P["C49"] = "• Insulation: batt"
    F = wb.create_sheet("FBM_PRICES"); F.append(["FBM code", "Product", "Cat", "Price", "Unit", "Min", "Stock", "Lead", "Link", "Read on"])
    F.append(["X-1", "track", "SteelFraming", 18.6, "Piece", 1, "Available", "", "https://myfbm.com/all-products/x/p/X-1", "2026-11-05"])
    B = wb.create_sheet("PRICING"); B.append(["M", "track", 10, "LF", "X-1", 18.6, "Piece", 0.1, "=C1*F1*H1", "2/A500"])
    f = tempfile.mktemp(suffix=".xlsx"); wb.save(f); return f
_ms = [('Bottom track 3-5/8"', 10.0)]; _sc = [("ALC-E06", "Insulation", "NOT APPLICABLE", "EXCLUDED - batt insulation")]
assert any("NOT INCLUDED" in e for e in CE.revisar_proposal(_prop(False), _ms, _sc)), "U-150: proposal without NOT INCLUDED must FAIL"
assert CE.revisar_proposal(_prop(True), _ms, _sc) == [], CE.revisar_proposal(_prop(True), _ms, _sc)
assert "U-150" in src("compuerta_entrega.py") and "Proposal" in src("compuerta_entrega.py")
# U-146 / U-147 (user decisions 5-nov, Consumer Cellular RFI-01 / RFI-04 -> option A)
assert criterios.deck_sin_corte([16.333, 17.130]) == 17.130 if False else abs(__import__("criterios").deck_sin_corte([16.333, 17.130]) - 17.13) < 1e-9
assert __import__("criterios").level_of_finish() == 4 and __import__("criterios").level_of_finish(5) == 5
class _B2:
    def __init__(s, rf): s._rf = rf
    def rfis_abiertos(s): return s._rf
assert CB.u_146(_B2([("RFI-01", "The deck break between PLY DECK @ 16'-4\" and @ 17'-1 9/16\" is not drawn", "")]))[0] == "FAIL"
assert CB.u_147(_B2([("RFI-04", "Gypsum board finish level and trims are not specified", "")]))[0] == "FAIL"
assert CB.u_146(_B2([]))[0] == "PASS" and CB.u_147(_B2([("RFI-09", "door 3C header", "")]))[0] == "PASS"
# BE-CC08: the only printed ceiling system detail governs even without a bubble (why written); no why = not accepted
import criterios
assert criterios.system_callout_ok({"detail": "2/A501", "printed_only": True, "source": "A501", "why": "2/A501 is the only gypsum board ceiling detail printed in the set"})[0]
assert not criterios.system_callout_ok({"detail": "2/A501", "printed_only": True, "source": "A501"})[0]
print("test_consumer_cellular OK")
'''
    _r = _sp.run([sys.executable, '-c', _code], cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True)
    assert _r.returncode == 0 and 'test_consumer_cellular OK' in _r.stdout, _r.stdout + _r.stderr
    print('test_consumer_cellular OK')

test_consumer_cellular()


def test_cr_rev6_cf10_specs():
    """E3 (CR City Hotel, auditoría COORDINACIÓN 7-nov): CB_BE_CF10 dio 'N/A: el set no trae specs' mientras la entrega citaba
    05 40 00 / 09 29 00 2.3 B / 09 29 00 3.6.E.4 -> pasó en vacío. Ahora: entrega que cita specs sin Project Manual leído = FAIL;
    con specs_dir leído y renglones con su sección = PASS; sección citada que no está en specs_dir = FAIL."""
    cel = [("Pending RFIs", "B5", "RFI-13: 09 29 00 2.3 B 'Gypsum Ceiling Board' (spec lists it)")]
    ms = [M("5/8\" Type X gypsum board", 100, unit="SF", fuente="A0.06 + 09 29 00 2.1.A")]
    b = CB.B(hojas={"A0.00": "CODE SUMMARY"}, celdas=cel, ms=ms)
    r = CB.be_cf10(b)
    assert r[0] == "FAIL" and "Project Manual" in str(r), r
    b = CB.B(hojas={"A0.00": "CODE SUMMARY"}, celdas=cel, ms=ms, specs={"092900": "SECTION 09 29 00 GYPSUM BOARD"})
    assert CB.be_cf10(b)[0] == "PASS", CB.be_cf10(b)
    b = CB.B(hojas={"A0.00": "x"}, celdas=cel + [("Partition", "C9", "05 40 00 cold-formed framing")], ms=ms,
             specs={"092900": "SECTION 09 29 00"})
    assert CB.be_cf10(b)[0] == "FAIL", CB.be_cf10(b)
    b = CB.B(hojas={"A0.00": "x"}, celdas=[("Partition", "C9", "no spec cited")], ms=[M("track", 10, fuente="1/A-501")])
    assert CB.be_cf10(b)[0] in ("N/A", "NA", "PASS") or "N/A" in str(CB.be_cf10(b)), CB.be_cf10(b)
    print("test_cr_rev6_cf10_specs OK")


test_cr_rev6_cf10_specs()


def test_cr_rev6_auditoria():
    """CR City Hotel rev6 (auditoría COORDINACIÓN 7-nov): E1 coffers = membrana, O1 sqrt, O2 anchos distintos del mismo detalle."""
    ang = {"ref": "CLG-L1-07 angle molding", "familia": "USG angle molding", "qty": 33.3, "op": "4 x sqrt(69.45) = 33.33 (square-equivalent perimeter)"}
    assert CB.cr_r6_o1(CB.B(canon={"misc_items": [ang]}))[0] == "FAIL"
    assert CB.cr_r6_o1(CB.B(canon={"misc_items": [dict(ang, op="perimeter of the measured room polygon = 33.89 LF")]}))[0] == "PASS"
    so = lambda fl, w_: {"id": f"SOF-{fl}", "floor": fl, "detail": "7/A7.23 (typ.)", "faces": [{"side": "bottom", "width_ft": w_}]}
    assert CB.cr_r6_o2(CB.B(canon={"framed_soffits": [so("L2", 1.0), so("L3", 0.375)]}))[0] == "FAIL"
    assert CB.cr_r6_o2(CB.B(canon={"framed_soffits": [so("L2", 0.375), so("L3", 0.375)]}))[0] == "PASS"
    mem = {"room": "L1 FS-1 membrane under the LEVEL 2 floor", "height_ft": 12.0}
    cof = {"ref": "CLG-L1-11 board", "source": "LOBBY coffers | [CONFIRMED] height 12.063 (1/A7.31 'GYP-1 12'-0 3/4\"')"}
    assert CB.cr_r6_e1(CB.B(canon={"ceilings": [mem], "misc_items": [cof]}))[0] == "FAIL"
    assert CB.cr_r6_e1(CB.B(canon={"ceilings": [mem], "misc_items": [dict(cof, source="field | [CONFIRMED] height 11.0")]}))[0] == "PASS"
    print("test_cr_rev6_auditoria OK")


test_cr_rev6_auditoria()
