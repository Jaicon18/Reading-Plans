"""R80w.11: MR por nota de cuartos del set. Falla con la tool v80v (MR sin fixture rechazado aunque el set lo pida)."""
import inventario as I
def canon(nota=True, room="MEN'S LOCKER ROOM 128"):
    c = {"walls": [{"id": "W1", "faces": [{"side": "A", "room": room, "board": "5/8 MR"}]}], "constants": {}}
    if nota: c["constants"]["mr_rooms_note"] = {"value": ["LOCKER", "RESTROOM", "POOL"], "source": "A111 general note 3"}
    return c
I._mr(canon())                                      # sala listada en la nota: OK sin fixture
for c in (canon(nota=False), canon(room="LOBBY 101")):
    try: I._mr(c); raise SystemExit("FALLA: MR sin fixture fuera de la nota debía rechazarse")
    except ValueError: pass
c = canon(); c["constants"]["mr_rooms_note"]["source"] = ""
try: I._mr(c); raise SystemExit("FALLA: nota sin source debía rechazarse")
except ValueError: pass
print("test_mr_rooms_note OK")
