"""BE-GK39 (labels never on labels: hueco_etiqueta inside a big Square, EXCLUDED labels of rooms sharing a polygon) + BE-GK40 (blind
question = loaded magnitude)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_be_gk39_hueco_dentro_de_square():
    import pymupdf
    import compuerta_entrega as CE
    d = pymupdf.open()
    pg = d.new_page(width=800, height=600)
    sq = pg.add_rect_annot(pymupdf.Rect(50, 50, 750, 550))   # destination view covering the whole area
    sq.update()
    r = pymupdf.Rect(100, 100, 168, 118)
    a1 = pg.add_freetext_annot(CE.hueco_etiqueta(pg, r), "#1", fontsize=11)
    a1.update()
    s2 = CE.hueco_etiqueta(pg, r)
    a2 = pg.add_freetext_annot(s2, "#2", fontsize=11)
    a2.update()
    i = pymupdf.Rect(a1.rect) & pymupdf.Rect(a2.rect)
    assert i.is_empty or i.width <= 0.5 or i.height <= 0.5, (a1.rect, a2.rect)


def test_be_gk40_pregunta_misma_magnitud():
    import pregunta_ciega as PC
    canon = {"misc_items": [
        {"ref": "EXT-07 joists", "op": "ROUNDUP(125.667/1.3333)+1 = 96 joists x 0.82 ft = 78.72"},
        {"ref": "SOF-02 board", "op": "44.51 LF x developed 1.5 ft = 66.77"},
        {"ref": "EXT-04 studs", "op": "ROUNDUP(98.0/1.3333)+1 = 75 studs x 9.16 ft = 687.0"}]}
    t = {x["id"]: x["magnitude"] for x in PC.tareas(canon)}
    assert t == {"EXT-07": "joist_length", "SOF-02": "developed", "EXT-04": "stud_height"}, t
    mal = "| EXT-07 | pocket | depth of the joists (ft) |\n| SOF-02 | cove | developed board width (ft) |\n| EXT-04 | grid 4 | H of the 6\" studs (ft) |"
    ev = PC.pregunta_fallas(mal, canon)
    assert len(ev) == 1 and ev[0].startswith("EXT-07"), ev
    bien = mal.replace("depth of the joists", "LENGTH of each joist (pocket width)")
    assert PC.pregunta_fallas(bien, canon) == []


if __name__ == "__main__":
    test_be_gk39_hueco_dentro_de_square()
    test_be_gk40_pregunta_misma_magnitud()
    print("OK test_be_gk39_40")
