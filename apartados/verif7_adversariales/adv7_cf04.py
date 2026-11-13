# adv7_cf04: CB_BE_CF04 (v138, PASS sin '0 walls'): un muro de MADERA con framing en walls[] que el regex no ve. Sintético.
import sys; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB, compuerta_entrega as CE
EX = [{"id": "Z9-L9-01", "board_only": True, "decision": "wood framing EXCLUDED (Div. 06) per 1/Z9.0", "location": "L9 | faces: 905"}]
class B:
    def __init__(s, walls): s.canon = {"walls": walls, "existing_walls": EX}
    def walls(s, c=None): return CB.muros_canon(s.canon) if hasattr(CB, "muros_canon") else s.canon["walls"] + s.canon["existing_walls"]
for ss, ga in (("2x6", "DF"), ("2 X 6", "DF-L #2"), ("2×6", "SPF"), ("5-1/2\" DF stud", "lumber"), ("6\" timber stud", "n/a"), ("6\"", "WOOD")):
    w = [{"id": "Z9-W-01", "stud_size": ss, "gauge": ga, "length_ft": 20}]
    est, *ev = CB.be_cf04(B(w)); res = [{"id": "be_cf04", "estado": est, "evidencia": list(ev[0] if ev and isinstance(ev[0], list) else ev)}]
    CE.auditar_compuerta(res, {"walls": 943})
    print("C1 walls[] con stud_size", repr(ss), "gauge", repr(ga), "->", est, "| tras U-138:", res[0]["estado"], "|", str(ev)[:110])
