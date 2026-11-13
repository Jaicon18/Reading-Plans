import json, os, shutil, subprocess
R = "/home/user/Reading-Plans"; os.chdir(R)
ZIP = "take-off-metal-frame-drywall_v81cf138d_registro-BE-CR46_2026-11-13.zip"
subprocess.run("cd /tmp/v138d && rm -f /tmp/claude-0/r2/v138d.zip && zip -qr -D -X /tmp/claude-0/r2/v138d.zip take-off-metal-frame-drywall", shell=True, check=True)
shutil.copy("/tmp/claude-0/r2/v138d.zip", f"skills_archivo/{ZIP}")
open("apartados/v81cf138d_desde_v81cf138c.patch", "w").write(subprocess.run(
    "cd /tmp && diff -ruN v138b/take-off-metal-frame-drywall v138c/take-off-metal-frame-drywall -x __pycache__", shell=True, capture_output=True, text=True).stdout)
shutil.copy("/tmp/claude-0/r2/PRUEBA_ABIERTOS_v81cf138d.json", "skills_archivo/PRUEBA_ABIERTOS_v81cf138d.json")
viv = ".claude/skills/jc-hunter-ordenes/REGLAS_REGISTRO.json"
rv = json.load(open(viv)); ids = {x["id"] for x in rv["reglas"]}
rc = json.load(open("/tmp/v138d/take-off-metal-frame-drywall/REGLAS_REGISTRO.json"))
nuevas = [x for x in rc["reglas"] if x["id"] not in ids]; rv["reglas"] += nuevas
json.dump(rv, open(viv, "w"), ensure_ascii=False, indent=1)
os.makedirs("apartados/ordenes_v138d", exist_ok=True)
for f in ("REGLAS_REGISTRO.json", "verificar_version.py", "test_verificar_version.py"):
    shutil.copy(f".claude/skills/jc-hunter-ordenes/{f}", f"apartados/ordenes_v138d/{f}")
print("nuevas:", [x["id"] for x in nuevas])
open("skills_archivo/VERSION_EN_CURSO.md", "a").write(f"- v81cf138d · Xfinity · 13-nov ~21:35 UTC (COORDINACIÓN, opción B) · v81cf138c + BE-CR46 solo en el registro (programa-pendiente; CB_HEAD_TYPE en la 140); tools/ idénticos (sha_tools 43808ab09904) · PUBLICADA = skills_archivo/{ZIP}\n")
p = "skills_archivo/INDICE.md"; t = open(p, encoding="utf-8").read()
fila = (f"| BE-CR46 en el registro (Xfinity, COORDINACIÓN, CR rev19 / rev20d): v81cf138c + BE-CR46 programa-pendiente (head del type antes que la cota de muro; "
        f"CB_HEAD_TYPE en la próxima versión); solo REGLAS_REGISTRO.json y SKILL.md; tools/ idénticos (sha_tools 43808ab09904); suite 47/47 | v81cf138d | 2026-11-13 | {ZIP} |\n")
t = t.replace("| Proyecto | Versión | Fecha | Archivo |\n|---|---|---|---|\n", "| Proyecto | Versión | Fecha | Archivo |\n|---|---|---|---|\n" + fila, 1)
t = t.replace("**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf138c = ",
              f"**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf138d = v81cf138c + BE-CR46 en el registro, zip {ZIP}; antes v81cf138c = ", 1)
blq = ("**13-nov: v81cf138d = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (COORDINACIÓN, opción B) = v81cf138c + BE-CR46 (CR rev19: los lectores ciegos de alturas leen el "
       "HEAD DEL TYPE antes de la cota de muro; '6 in above (line of) ceiling' = C.H. + 6\" con tope en estructura) como programa-pendiente (CB_HEAD_TYPE y el arreglo de "
       "CE_ALTURAS_EXTREMO en la próxima versión). Sin cambio de programa: tools/ idénticos (sha_tools 43808ab09904): PRUEBA_ABIERTOS de v138a vale (XF 0 / GK 0 / CR 1 "
       "explicada); banco 0 distintas (8; mismas tools). SKILL.md **VERSION: v81cf138d**. Suite 47/47; 199 archivos; verificar_version 0 reglas faltantes y BE-XF19 "
       "(version_fallas del candidato) 0.\n\nCONGELADO de nuevo: no se publica otra versión sin aviso de COORDINACIÓN.\n\n")
k = t.index("**12-nov: CR City Hotel CERRADO**"); t = t[:k] + blq + t[k:]
open(p, "w", encoding="utf-8").write(t)
print("ok")
