#!/usr/bin/env python3
"""Tests v70 de inventario_tags.py (Etapa 1) con el PDF SINTÉTICO de test_inventario_tags.py (ningún dato real).
Correr: python3 test_inventario_tags_v70.py

- ids únicos en TODAS las listas de `ocurrencias` (antes partition_ambiguo / partition_candidato / partition_texto
  daban todos PA####);
- candidatos (tag en símbolo fuera del schedule) con prefijo PC#### y recorte PNG propio verificado.
"""
import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import test_inventario_tags as B  # noqa: E402  (arma el PDF sintético y corre el inventario una vez)

INV, DIR = B.INV, B.DIR


def test_ids_unicos_en_todas_las_listas():
    ids = [o["id"] for lst in INV["ocurrencias"].values() for o in lst]
    rep = [k for k, n in Counter(ids).items() if n > 1]
    assert not rep, f"ids repetidos entre listas: {rep[:10]}"
    # el PDF tiene a la vez ambiguos y candidatos (el caso que chocaba)
    assert INV["ocurrencias"]["partition_ambiguo"] and INV["ocurrencias"]["partition_candidato"]


def test_candidato_prefijo_pc_y_recorte_propio():
    cand = INV["ocurrencias"]["partition_candidato"]
    assert cand and all(o["id"].startswith("PC") for o in cand), [o["id"] for o in cand]
    amb_png = {o.get("png") for o in INV["ocurrencias"]["partition_ambiguo"]}
    for o in cand:
        assert o.get("type") == o["text"], o
        assert o.get("png") and o["png"] not in amb_png, o
        assert o.get("png_verificado") is True, o
        assert os.path.exists(os.path.join(DIR, "out", "recortes", o["png"]))


def test_prefijos_distintos():
    import inventario_tags as I
    assert len(set(I.PREFIJOS.values())) == len(I.PREFIJOS)
    assert I.PREFIJOS["partition_candidato"] == "PC" and I.PREFIJOS["partition_ambiguo"] == "PA"


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print("FALLA", k, e)
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
