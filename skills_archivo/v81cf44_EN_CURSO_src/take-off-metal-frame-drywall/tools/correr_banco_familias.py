"""correr_banco_familias.py — R80e.58 / BE-115: prueba de regresión del banco. Recalcula con canon.py cada canon guardado
con las tools de referencia (versión con la que se entregó) y con las tools candidatas; reporta familias distintas.
Uso: python3 correr_banco_familias.py '[["nombre", "<canon.json>", "<tools_ref>"], ...]' <tools_candidatas>
Un arreglo entra solo con 0 familias que empeoren (v81cf: B&N rev13, VS rev8, Chuze FINAL, O'Reilly = 0 distintas)."""
import json,os,subprocess,sys,tempfile
def run(tools,canon):
    d=tempfile.mkdtemp()
    p=subprocess.run([sys.executable,os.path.join(tools,'canon.py'),canon,d],capture_output=True,text=True,cwd=os.path.dirname(canon))
    f=os.path.join(d,'familias_out.json')
    if p.returncode or not os.path.exists(f): return None,(p.stdout+p.stderr)[-300:]
    j=json.load(open(f)); fam=j.get('familias') or j
    return {k:v for k,v in fam.items() if isinstance(v,(int,float))},''
def main(casos, NEW):
    for nombre,canon,ref in casos:
      a,ea=run(ref,canon); b,eb=run(NEW,canon)
      if a is None or b is None: print(nombre,'ERROR ref' if a is None else '', ea, '| new', eb); continue
      diffs=[(k,a.get(k,0),b.get(k,0)) for k in sorted(set(a)|set(b)) if abs((a.get(k,0) or 0)-(b.get(k,0) or 0))>0.01]
      print(f"{nombre}: {len(a)} familias, {len(diffs)} distintas", diffs[:12])


if __name__ == '__main__':
    main(json.loads(sys.argv[1]), sys.argv[2])
