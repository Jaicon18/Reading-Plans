"""BE-CR40 (CR City Hotel rev20, 12-nov): reporté a COORDINACIÓN que el cielo GYP-1 8'-11" de los corredores NO estaba cargado porque busqué
el TEXTO "8'-11" en el JSON del canon (las comillas van escapadas: 8'-11\\" no casa). Estaba cargado (CLG-L2-56 / -58, CLG-L3-87 / -88) y
canon.rcp_tags lo decía (tag A7.23 'GYP-1 8' - 11"' -> rows). Regla: antes de reportar un faltante, buscar por ID / TAG en canon.rcp_tags
(rows / none_reason) y por ref en misc_items / ceilings, nunca por texto libre. faltante_por_tag() es la búsqueda propuesta para la unión."""
import json
import re


def faltante_por_tag(canon, sheet, tag, height):
    """-> (faltante: bool, motivo). Faltante solo si NINGÚN rcp_tag (sheet, tag, height) tiene rows existentes ni none_reason."""
    refs = {str(m.get("ref")) for m in canon.get("misc_items") or []}
    nce = len(canon.get("ceilings") or [])
    norm = lambda h: re.sub(r"\s+", "", str(h))                                   # noqa: E731
    xs = [x for x in canon.get("rcp_tags") or [] if x.get("sheet") == sheet and x.get("tag") == tag and norm(x.get("height")) == norm(height)]
    if not xs:
        return True, "tag sin entrada en rcp_tags (barrido incompleto)"
    for x in xs:
        if str(x.get("none_reason") or "").strip():
            return False, "none_reason: " + x["none_reason"]
        ok = [r for r in x.get("rows") or [] if r in refs or (re.match(r"ceilings\[(\d+)\]", r) and int(re.match(r"ceilings\[(\d+)\]", r).group(1)) < nce)]
        if ok:
            return False, "cargado en " + ", ".join(ok)
    return True, "rows del tag no existen en el canon"


CANON = {"misc_items": [{"ref": "CLG-L2-56 board", "op": "442.09 SF", "source": "ceiling CONFIRMADO: GYP-1 8'-11\" on 1/A7.23"}],
         "ceilings": [{"room": "L2 Corridor 216"}],
         "rcp_tags": [{"sheet": "A7.23", "tag": "GYP-1", "height": "8' - 11\"", "rows": ["CLG-L2-56 board", "ceilings[0] FS-1"]}]}


def test_be_cr40_texto_falla_tag_encuentra():
    txt = json.dumps(CANON)
    assert "8'-11\"" not in txt                       # la búsqueda por texto (el error) no lo encuentra: comillas escapadas
    falta, motivo = faltante_por_tag(CANON, "A7.23", "GYP-1", "8' - 11\"")
    assert not falta and "CLG-L2-56" in motivo        # por tag: cargado


def test_be_cr40_faltante_real():
    c = json.loads(json.dumps(CANON)); c["rcp_tags"][0]["rows"] = ["CLG-L2-99 board"]
    assert faltante_por_tag(c, "A7.23", "GYP-1", "8' - 11\"")[0]
    c["rcp_tags"] = []
    assert faltante_por_tag(c, "A7.23", "GYP-1", "8' - 11\"")[0]
