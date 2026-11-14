"""BE-CR0-03 (CR desde cero 13-nov): chequeos_v71.ids_canon no incluía existing_walls: en un set wood-framed (todo board-only)
un tag descartado con owner = id de un wall board-only fallaba R78.15 'owner no existe en el canon'."""
import sys, os
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
import chequeos_v71 as C
def test_owner_board_only():
    c = {"existing_walls": [{"id": "W.6-L1-01", "tag_ids": ["PT0300"]}],
         "tags_descartados": [{"id": "PT0021", "motivo": "CMU; its room face is counted in W.6-L1-01", "owner": "W.6-L1-01"}]}
    assert C.r78_15(c) == [], C.r78_15(c)
if __name__ == "__main__":
    test_owner_board_only(); print("OK")
