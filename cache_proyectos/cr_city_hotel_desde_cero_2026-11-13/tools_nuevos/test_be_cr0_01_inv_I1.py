"""BE-CR0-01 (CR desde cero 13-nov): verificar_png normalizaba 'I'->'1' solo en el texto leído (FI.2 -> F1.2) y no en el
tag esperado: todo tag con letra+I (FI.2, XI.2.7) salía 'PNG NO VERIFICADO' y el inventario daba rc 1."""
import re
def norm(t): return re.sub(r"\b([A-Z])[lI|i]\b", r"\g<1>1", t)
def test_misma_normalizacion():
    for tag in ("FI.2", "XI.2.7", "FI.6"):
        leido = norm(tag)
        assert norm(tag) in leido          # con la regla nueva pasa
        assert not (tag in leido)          # la regla vieja fallaba (repite el error original)
if __name__ == "__main__":
    test_misma_normalizacion(); print("OK")
