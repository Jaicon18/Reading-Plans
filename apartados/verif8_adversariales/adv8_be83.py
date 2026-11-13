# adv8_be83: CB_BE_83 completitud.caras_sobre_ceiling — v137 vs candidato. Cuarto 905 con cielo 9 ft; cara a 11 ft.
import sys, os, json, copy
S = sys.argv[1]; sys.path.insert(0, os.path.join(S, "runner")); import completitud as CO
def can(faces=None, **w):
    base = {"id": "Z9-L9-07", "location": "L9 | 905 GUEST", "height_ft": 11.0}
    base.update(w)
    if faces is not None: base["faces"] = faces
    return {"ceilings": [{"room": "905 GUEST", "height_ft": 9.0}], "walls": [base]}
def r(c):
    try: return CO.caras_sobre_ceiling(c)
    except Exception as e: return "EXC " + type(e).__name__
F = lambda src: [{"room": "905 GUEST", "height_ft": 11.0, "height_source": src}]
print("A0 control lista de caras, fuente sin justificar ->", r(can(F("A3.1 section 11'-0\""))))
print("A1 (regresión) lista de caras; fuente = cielo hung from 'underside of floor joists' ->", r(can(F("C-2 GWB ceiling hung from underside of floor joists above (A5.1); wall 11'-0\" per section"))))
print("A2 (regresión) lista de caras; fuente solo MENCIONA 'stair enclosure' (otro detalle) ->", r(can(F("11'-0\" per 3/A3.1; see stair enclosure detail 5/A6.02 for the other wall"))))
print("A3 (regresión) lista de caras; 'floor to floor' como dato de nivel (no de la cara) ->", r(can(F("level floor to floor 11'-0\" (A3.01) used as wall height"))))
print("A4 (regresión) lista de caras; 'extends to structure' de OTRO elemento ->", r(can(F("11'-0\"; duct shaft extends to structure (M2.1)"))))
print("A5 lista de caras; 'underside of ceiling' (no justifica: control del autor) ->", r(can(F("GWB to underside of ceiling, 11'-0\""))))
print("B1 faces = 2 (número), sin justificar (antes: crash) ->", r(can(2, height_source="A3.1 11'-0\"")))
print("B2 faces ausente (None) y location 'of 905 GUEST' de un muro EXTERIOR (exterior: true) ->", r(can(None, location="storefront pier of 905 GUEST - exterior 6\" CFMF (faces N+W)", exterior=True, height_source="A3.1 11'-0\"")))
print("B3 faces = 1, location 'faces: exterior' (única cara exterior) ->", r(can(1, location="L9 905 GUEST | faces: exterior", height_source="A3.1 11'-0\"")))
print("B4 faces = 1, location 'faces: outside face, 905 GUEST' (coma: la cara interior debe juzgarse) ->", r(can(1, location="L9 | faces: outside face, 905 GUEST", height_source="A3.1 11'-0\"")))
print("B5 faces = 2, location 'faces: EXT; 905 GUEST' ('EXT' abreviado) ->", r(can(2, location="L9 | faces: EXT; 905 GUEST", height_source="A3.1 11'-0\"")))
print("B6 faces = 2, location 'faces: exterior (905 GUEST side is sheathing only)' ->", r(can(2, location="L9 | faces: exterior (905 GUEST side n/a)", height_source="A3.1 11'-0\"")))
print("B7 faces = 1, sin height_source pero 'source' con la justificación ->", r(can(1, source="full height to deck", height_source=None)))
print("B8 faces = 1, room del cuarto SOLO en 'rooms' (location sin número) ->", r(can(1, location="L9 east wall", rooms=["905 GUEST"], height_source="A3.1 11'-0\"")))
print("B9 faces = [] (lista vacía) ->", r(can([], height_source="A3.1 11'-0\"")))
print("B10 faces = {'905 GUEST': 11} (dict) ->", r(can({"905 GUEST": 11.0}, height_source="A3.1 11'-0\"")))
