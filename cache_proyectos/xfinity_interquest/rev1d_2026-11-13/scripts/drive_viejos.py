"""BE-XF07: antes de re-subir rev1 FINAL, renombra en Drive (NUNCA borra) los archivos cuyo contenido cambió: 'BORRAR (NO USAR) - old <nombre>' (U-186; antes 'zz old');
el PDF de markups viejo -> 'BORRAR (NO USAR) - XF_markups_rev1 old.pdf'. Uso: drive_viejos.py <carpeta_local_entrega> <id_drive> [--hacer]"""
import sys, os, json, hashlib, requests
sys.path.insert(0, '/opt/takeoff'); import gdrive_fetch as G
sys.path.insert(0, os.environ.get("T", "/root/xf/skill98/take-off-metal-frame-drywall/tools")); import subir_entrega as SE   # U-186
loc, raiz, hacer = sys.argv[1], sys.argv[2], '--hacer' in sys.argv
U174 = "--u174" in sys.argv or "--tag" in sys.argv
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "U-174"
tok = G.access_token()
def lst(fid):
    p = {"q": f"'{fid}' in parents and trashed = false", "fields": "nextPageToken, files(id,name,mimeType,size,md5Checksum)",
         "includeItemsFromAllDrives": "true", "pageSize": 1000, **G.ALL_DRIVES}; out = []
    while True:
        b = requests.get(G.API, params=p, timeout=60, headers=G._auth(tok)).json(); out += b.get("files", [])
        if "nextPageToken" not in b: return out
        p["pageToken"] = b["nextPageToken"]
md5 = lambda f: hashlib.md5(open(f, 'rb').read()).hexdigest()
cambios = []
def rec(dl, fid):
    for it in lst(fid):
        n = it["name"]; pl = os.path.join(dl, n)
        if it["mimeType"].endswith("folder"):
            if os.path.isdir(pl): rec(pl, it["id"])
            continue
        if n.startswith(("zz ", "BORRAR (NO USAR) - ")):
            continue
        if n == "XF_markups_rev1c - OPEN IN BLUEBEAM.pdf" and TAG == "rev1d":           # rev1d: el PDF rev1c ya no es vigente
            cambios.append((it["id"], os.path.relpath(pl, loc), SE.nombre_borrar(n, "XF_markups_rev1d - OPEN IN BLUEBEAM.pdf"))); continue
        if n == "XF_markups_rev1b - OPEN IN BLUEBEAM.pdf" and TAG == "rev1c":           # rev1c: el PDF rev1b ya no es vigente
            cambios.append((it["id"], os.path.relpath(pl, loc), SE.nombre_borrar(n, "XF_markups_rev1c - OPEN IN BLUEBEAM.pdf"))); continue
        if U174 and n == "XF_markups_rev1b - OPEN IN BLUEBEAM.pdf" and os.path.isfile(pl) and it.get("md5Checksum") != md5(pl):
            cambios.append((it["id"], os.path.relpath(pl, loc), f"BORRAR (NO USAR) - XF_markups_rev1b old (antes de {TAG}).pdf")); continue
        if n == "XF_markups_rev1 - OPEN IN BLUEBEAM.pdf":
            cambios.append((it["id"], os.path.relpath(pl, loc), "BORRAR (NO USAR) - XF_markups_rev1 old.pdf"))
        elif os.path.isfile(pl) and it.get("md5Checksum") != md5(pl):
            cambios.append((it["id"], os.path.relpath(pl, loc), SE.nombre_borrar(f"old {TAG} {n}" if U174 else f"old {n}",
                                                                                  f"{n} ({TAG})" if U174 else n)))   # U-186
rec(loc, raiz)
for c in cambios:
    print(("RENOMBRADO " if hacer else "A RENOMBRAR ") + c[1] + " -> " + c[2])
    if hacer: G.rename(tok, c[0], c[2])
print(len(cambios), "archivos")
json.dump(cambios, open('/root/xf/work/drive_renombrados' + ('_' + TAG.replace('-', '').lower() if U174 else '') + '.json', 'w'), indent=1) if hacer else None
