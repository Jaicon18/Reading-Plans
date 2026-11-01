// monitor.js — vigila en BuildingConnected los proyectos de proyectos.json (SOLO LECTURA).
//
// Un solo login por corrida. Por cada invitación compara el árbol de archivos contra su foto:
//   NUEVO / CAMBIADO  → lo baja (salvo la carpeta Photos, que solo se reporta), lo sube a la carpeta del
//                        proyecto en Drive con gdrive_fetch.py (nunca sobrescribe: un archivo cambiado se sube
//                        como "REV <fecha> <nombre>") y actualiza la foto.
//   QUITADO           → solo se reporta.
// Además busca invitaciones NUEVAS del mismo proyecto (otro GC) por el texto 'buscar' y los trades de
// nuestro alcance; una invitación nueva se agrega a proyectos.json, se baja completa (sin Photos) a una
// subcarpeta con el nombre del GC y se reporta.
//
// Nunca hace click en Bidding / Decline / Accept / Submit ni manda mensajes. Credenciales: BC_EMAIL / BC_PASSWORD.
//
// Uso: node monitor_bc/monitor.js            → rc 0 sin cambios · rc 3 con cambios · rc 1 error
// Escribe monitor_bc/ultimo_reporte.md y agrega una línea a monitor_bc/historial.md.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const AQUI = __dirname;
const { login, buscar, arbol, B } = require(path.join(AQUI, '..', 'paquetes', 'dev', 'tools', 'bc_descarga.js'));
const GD = '/opt/takeoff/gdrive_fetch.py';
const TMP = fs.mkdtempSync('/tmp/monitor_bc_');
const hoy = new Date().toISOString().slice(0, 16).replace('T', ' ') + 'Z';

function subir(local, folder, nombre) {
  return execFileSync('python3', ['-I', GD, 'put', local, folder, nombre], { encoding: 'utf8' }).trim();
}
function mkdir(parent, nombre) {
  const out = execFileSync('python3', ['-I', GD, 'mkdir', parent, nombre], { encoding: 'utf8' });
  return out.match(/[A-Za-z0-9_-]{25,}/g).pop();
}
async function bajar(ctx, f, nombreLocal) {
  const r = await ctx.request.get(B + f.downloadUrl, { timeout: 1800000 });
  const b = await r.body();
  if (!r.ok() || b.length !== f.size) throw new Error(`descarga incompleta ${f.path}: ${r.status()} ${b.length}/${f.size}`);
  const dest = path.join(TMP, nombreLocal.replace(/[\/]/g, '_'));
  fs.writeFileSync(dest, b);
  return dest;
}
const foto = arr => arr.map(({ path, size, modified }) => ({ path, size, modified }));

(async () => {
  const cfgPath = path.join(AQUI, 'proyectos.json');
  const cfg = JSON.parse(fs.readFileSync(cfgPath));
  const { browser, ctx } = await login();
  const rep = [];
  let cambios = 0;
  try {
    for (const p of cfg.proyectos.filter(x => x.activo)) {
      rep.push(`## ${p.proyecto}`);
      // 1) invitaciones nuevas del mismo proyecto
      const conocidas = new Set(p.invitaciones.map(i => i.opp));
      for (const o of await buscar(ctx, p.buscar)) {
        if (conocidas.has(o.id) || !p.trades.includes(o.trade)) continue;
        const sub = mkdir(p.drive_folder_id, o.gc);
        const inv = { gc: o.gc, opp: o.id, foto: `fotos/${o.id}.json`, drive_folder_id: sub };
        p.invitaciones.push(inv);
        fs.writeFileSync(path.join(AQUI, inv.foto), JSON.stringify({ opp: o.id, fecha: hoy, archivos: [] }));
        rep.push(`- **INVITACIÓN NUEVA**: ${o.gc} · ${o.trade} · due ${o.due} (se baja completa abajo)`);
        cambios++;
      }
      // 2) archivos por invitación
      for (const inv of p.invitaciones) {
        const fp = path.join(AQUI, inv.foto);
        const viejo = new Map(JSON.parse(fs.readFileSync(fp)).archivos.map(f => [f.path, f]));
        const actual = await arbol(ctx, inv.opp);
        const lineas = [];
        for (const f of actual) {
          const v = viejo.get(f.path);
          const tipo = !v ? 'NUEVO' : (v.size !== f.size || v.modified !== f.modified) ? 'CAMBIADO' : null;
          viejo.delete(f.path);
          if (!tipo) continue;
          cambios++;
          if (f.path.split('/')[0] === 'Photos') { lineas.push(`- ${tipo} (Photos, no se baja): ${f.path}`); continue; }
          const base = path.basename(f.path);
          const nombre = tipo === 'NUEVO' ? base : `REV ${hoy.slice(0, 10)} ${base}`;
          const local = await bajar(ctx, f, nombre);
          let s;
          try { s = subir(local, inv.drive_folder_id, nombre); }
          catch (e) { s = 'NO SUBIDO (ya existe un archivo con ese nombre en Drive)'; }
          lineas.push(`- ${tipo}: ${f.path} (${f.size} bytes) → ${s}`);
        }
        for (const q of viejo.keys()) { lineas.push(`- QUITADO en BC: ${q}`); cambios++; }
        fs.writeFileSync(fp, JSON.stringify({ opp: inv.opp, fecha: hoy, archivos: foto(actual) }, null, 1));
        rep.push(`### ${inv.gc} (${inv.opp})`, ...(lineas.length ? lineas : ['- sin cambios']));
      }
    }
  } finally { await browser.close(); }
  fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n');
  const titulo = `# Monitor BuildingConnected — ${hoy} — ${cambios ? `CAMBIOS: ${cambios}` : 'SIN CAMBIOS'}`;
  fs.writeFileSync(path.join(AQUI, 'ultimo_reporte.md'), [titulo, '', ...rep, ''].join('\n'));
  fs.appendFileSync(path.join(AQUI, 'historial.md'), `| ${hoy} | ${cambios ? `CAMBIOS: ${cambios}` : 'sin cambios'} |\n`);
  console.log([titulo, ...rep].join('\n'));
  process.exitCode = cambios ? 3 : 0;
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
