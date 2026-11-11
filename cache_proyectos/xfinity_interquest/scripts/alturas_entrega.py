"""U-175 / U-176: copia las dos lecturas ciegas de alturas a la entrega. Auditoria/ALTURAS_IMPRESAS_A.csv / _B.csv, ALTURAS_CUARTOS_A / _B,
la tabla final ALTURAS_IMPRESAS.csv + ALTURAS_CUARTOS.csv (= lectura A, que coincide con B o con la resolución), imágenes en
Auditoria/alturas_img/A y /B con ruta relativa. Uso: alturas_entrega.py <dir_A> <dir_B> <carpeta_entrega_rev>"""
import csv, os, shutil, sys
A, B, E = sys.argv[1], sys.argv[2], sys.argv[3]
au = os.path.join(E, "Auditoria")


def copiar(src, nombre, dest_csv, sub):
    dst = os.path.join(au, "alturas_img", sub); os.makedirs(dst, exist_ok=True)
    filas = list(csv.DictReader(open(os.path.join(src, nombre), encoding="utf-8-sig")))
    for r in filas:
        p = r["Image"] if os.path.isabs(r["Image"]) else os.path.join(src, r["Image"])
        if not os.path.isfile(p):
            sys.exit(f"falta la imagen {r['Image']} ({nombre})")
        shutil.copy2(p, dst); r["Image"] = f"Auditoria/alturas_img/{sub}/" + os.path.basename(p)
    with open(os.path.join(au, dest_csv), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
    return len(filas)


n = [copiar(A, "ALTURAS_IMPRESAS.csv", "ALTURAS_IMPRESAS_A.csv", "A"), copiar(B, "ALTURAS_IMPRESAS.csv", "ALTURAS_IMPRESAS_B.csv", "B"),
     copiar(A, "ALTURAS_CUARTOS.csv", "ALTURAS_CUARTOS_A.csv", "A"), copiar(B, "ALTURAS_CUARTOS.csv", "ALTURAS_CUARTOS_B.csv", "B")]
shutil.copy2(os.path.join(au, "ALTURAS_IMPRESAS_A.csv"), os.path.join(au, "ALTURAS_IMPRESAS.csv"))
shutil.copy2(os.path.join(au, "ALTURAS_CUARTOS_A.csv"), os.path.join(au, "ALTURAS_CUARTOS.csv"))
for src, tag in ((A, "A"), (B, "B")):
    if os.path.isfile(os.path.join(src, "NOTAS.md")):
        shutil.copy2(os.path.join(src, "NOTAS.md"), os.path.join(au, f"ALTURAS_NOTAS_{tag}.md"))
if os.path.isfile(os.path.join(os.path.dirname(A), "ALTURAS_AB_RESOLUCION.csv")):
    shutil.copy2(os.path.join(os.path.dirname(A), "ALTURAS_AB_RESOLUCION.csv"), au)
print("alturas A / B / cuartos:", n)
