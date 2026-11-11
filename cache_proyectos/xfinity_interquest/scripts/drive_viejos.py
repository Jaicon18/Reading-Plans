"""BE-XF07: antes de re-subir rev1 FINAL, renombra en Drive (NUNCA borra) los archivos cuyo contenido cambió: 'zz old <nombre>';
el PDF de markups viejo -> 'zz NO USAR - XF_markups_rev1 old.pdf'. Uso: drive_viejos.py <carpeta_local_entrega> <id_drive> [--hacer]"""
import sys, os, json, hashlib, requests
sys.path.insert(0, '/opt/takeoff'); import gdrive_fetch as G
loc, raiz, hacer = sys.argv[1], sys.argv[2], '--hacer' in sys.argv
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
        if n == "XF_markups_rev1 - OPEN IN BLUEBEAM.pdf":
            cambios.append((it["id"], os.path.relpath(pl, loc), "zz NO USAR - XF_markups_rev1 old.pdf"))
        elif os.path.isfile(pl) and it.get("md5Checksum") != md5(pl):
            cambios.append((it["id"], os.path.relpath(pl, loc), "zz old " + n))
rec(loc, raiz)
for c in cambios:
    print(("RENOMBRADO " if hacer else "A RENOMBRAR ") + c[1] + " -> " + c[2])
    if hacer: G.rename(tok, c[0], c[2])
print(len(cambios), "archivos")
json.dump(cambios, open('/root/xf/work/drive_renombrados.json', 'w'), indent=1) if hacer else None
