"""BE-CR0-05 (CR desde cero 13-nov): comparar_alturas.alturas_revisadas insertaba la imagen en Rect(36, y+6, 756, 590) después de
listar los Wall ID; con ~500 walls de una misma altura y > 590 -> 'rect must be finite and not empty' y la compuerta de alturas caía."""
import os, sys, tempfile
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
import comparar_alturas as CA
from PIL import Image
def test():
    d = tempfile.mkdtemp(); Image.new("RGB", (40, 40), "white").save(os.path.join(d, "i.png"))
    final = [{"Wall ID": f"W.4-L2-{i:03d} A", "Printed H": "9.292", "Source": "A5.06", "Operation": "", "Status": "CONFIRMED", "Image": "i.png"} for i in range(600)]
    CA.alturas_revisadas(final, d, os.path.join(d, "out.pdf"), None, {})
    assert os.path.isfile(os.path.join(d, "out.pdf"))
if __name__ == "__main__":
    test(); print("OK")
