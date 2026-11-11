"""U-166 punto 5 / U-165: barre TODAS las carpetas de Claude outputs (raíz) y lista
archivos cuya ruta Windows simulada pase del límite. Solo lee (gdrive_fetch.py list).
Uso: python3 -I barrido_drive.py [limite=230] [salida=largos.json]"""
import json,subprocess,sys
G='/opt/takeoff/gdrive_fetch.py'; ROOT='1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc'
BASE=r'G:\Shared drives\JC HUNTER PROJECTS\Claude outputs'
LIM=int(sys.argv[1]) if len(sys.argv)>1 else 230
OUT=sys.argv[2] if len(sys.argv)>2 else 'largos.json'
PROHIB=set('<>:"/\\|?*')
def ls(fid):
    o=subprocess.run(['python3',G,'list',fid],capture_output=True,text=True).stdout
    return [json.loads(l) for l in o.splitlines() if l.startswith('{')]
res=[]
def walk(fid,path,depth):
    for d in ls(fid):
        p=path+'\\'+d['name']
        bad=bool(PROHIB & set(d['name']))
        if d['mimeType'].endswith('folder'):
            if depth<5: walk(d['id'],p,depth+1)
        elif len(p)>LIM or bad: res.append({'len':len(p),'id':d['id'],'ruta':p,'caracter_prohibido':bad,'no_abre':len(p)>260})
walk(ROOT,BASE,0)
res.sort(key=lambda x:-x['len'])
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=1)
print(f"{len(res)} rutas > {LIM}; no abren (>260): {sum(r['no_abre'] for r in res)}")
