# adv7_be83: CB_BE_83 / completitud.caras_sobre_ceiling con 'faces' numérico (v138). Sintético.
import sys, os; sys.path.insert(0, os.path.join(sys.argv[1], "runner")); import completitud as CO
def can(**w):
    base = {"id": "Z9-L9-07", "faces": 2, "height_ft": 11.0, "location": "L9 | faces: 905 GUEST; corridor 916", "height_source": "4/Z9.05 printed level to level"}
    base.update(w); return {"walls": [], "ceilings": [{"room": "GUEST 905", "height_ft": 9.0}], "existing_walls": [base]}
print("F0 control (interior, 11 ft sobre cielo 9 ft, sin fuente) ->", CO.caras_sobre_ceiling(can()))
print("F1 muro exterior con su cara INTERIOR en 905: location 'L9 | faces: exterior; 905 GUEST' ->",
      CO.caras_sobre_ceiling(can(location="L9 | faces: exterior; 905 GUEST")))
print("F2 board con 'exterior gyp sheathing' + cara interior 905 ->",
      CO.caras_sobre_ceiling(can(board="5/8 Type X (905 side) + 1/2 exterior gyp sheathing")))
print("F3 fuente 'GWB to extend to underside of ceiling (6/Z9.21)' con altura 11 ft (la fuente dice que para en el cielo) ->",
      CO.caras_sobre_ceiling(can(height_source="GWB to extend to underside of ceiling (6/Z9.21)")))
print("F4 fuente que solo MENCIONA 'stair enclosure' (nota de otro detalle) ->",
      CO.caras_sobre_ceiling(can(height_source="type 3A, see stair enclosure note 5/Z9.02 for the next wall; 4/Z9.05 level to level")))
print("F5 fuente 'to structure' de otro dato ('anchored to structure', altura impresa 11 ft) ->",
      CO.caras_sobre_ceiling(can(height_source="11'-0\" per 4/Z9.05; top track anchored to structure")))
print("F6 location sin número de cuarto pero 'rooms' con el 905 ->",
      CO.caras_sobre_ceiling(can(location="L9 | guest side", rooms="905")))
