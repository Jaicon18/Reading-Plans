"""BE-CR0-04 (CR desde cero 13-nov): comparar.ambiguos comparaba el type del tag ambiguo solo con w.tag / w.type; los walls
board-only (existing_walls) traen la designación en type_id y un texto largo en type -> 'citado en tag_ids de un wall de otro type'
aunque el tag estaba bien asignado (PA0004/PA0005 XW.6.3 en CR)."""
import os, sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
import comparar as C
def test():
    inv = {"ocurrencias": {"partition_ambiguo": [{"id": "PA0004", "type": "XW.6.3", "sheet": "A2.01", "page": 17}]}}
    canon = {"existing_walls": [{"id": "XW.6.3-L1-01", "type_id": "XW.6.3-0", "type": "XW.6.3 (exterior 2x6 wood stud) non-rated", "tag_ids": ["PA0004"]}]}
    f = C.ambiguos_sin_disposicion(inv, [canon]) if hasattr(C, "ambiguos_sin_disposicion") else None
    assert f == [], f
if __name__ == "__main__":
    test(); print("OK")
