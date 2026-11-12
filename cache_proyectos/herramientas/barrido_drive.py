"""U-166 punto 5 / U-165: barre TODAS las carpetas de Claude outputs (raíz) y lista
archivos cuya ruta Windows simulada pase del límite. Solo lee (gdrive_fetch.py list).
Uso: python3 -I barrido_drive.py [limite=230] [salida=largos.json]
     python3 -I barrido_drive.py borrar <skill_tools_dir> [salida=borrar.json]
       U-186: todo archivo / carpeta con marca de obsoleto (zz / REPLACED / superseded / NO USAR / old) sin el prefijo
       'BORRAR (NO USAR) - ' = FAIL; una carpeta Take-off/ o Planos marcados/ con TODO su Excel / PDF de markups en BORRAR
       (el vigente marcado para borrar) = FAIL. Usa subir_entrega.borrar_fallas del skill. rc 1 si hay fallas."""
import json,subprocess,sys
G='/opt/takeoff/gdrive_fetch.py'; ROOT='1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc'
BASE=r'G:\Shared drives\JC HUNTER PROJECTS\Claude outputs'
if len(sys.argv)>2 and sys.argv[1]=='borrar':
    sys.path.insert(0,sys.argv[2]); import subir_entrega as SE
    OUTB=sys.argv[3] if len(sys.argv)>3 else 'borrar.json'
    def lsb(fid):
        o=subprocess.run(['python3',G,'list',fid],capture_output=True,text=True).stdout
        return [json.loads(l) for l in o.splitlines() if l.startswith('{')]
    fallas=[]
    def walkb(fid,path,depth,padre_borrar=False):
        items=lsb(fid)
        nombres=[d['name'] for d in items]
        if not padre_borrar:
            fallas.extend({'ruta':path,'falla':e} for e in SE.borrar_fallas(nombres))
        base=path.rsplit('\\',1)[-1]
        for ext,carp in (('.xlsx','Take-off'),('.pdf','Planos marcados')):
            if base==carp:
                k=[n for n in nombres if n.lower().endswith(ext) and not n.startswith(('DETALLES_REVISADOS','SCHEDULES_REVISADOS','ALTURAS_REVISADAS'))]
                if k and all(n.startswith(SE.PREFIJO_BORRAR) for n in k) and not padre_borrar:
                    fallas.append({'ruta':path,'falla':f'todos los {ext} de {carp}/ llevan BORRAR: el vigente no puede llevar BORRAR (U-186)'})
        for d in items:
            if d['mimeType'].endswith('folder') and depth<5:
                walkb(d['id'],path+'\\'+d['name'],depth+1,padre_borrar or d['name'].startswith(SE.PREFIJO_BORRAR))
    walkb(ROOT,BASE,0)
    json.dump(fallas,open(OUTB,'w'),ensure_ascii=False,indent=1)
    print(f"U-186: {len(fallas)} fallas -> {OUTB}"); sys.exit(1 if fallas else 0)
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
