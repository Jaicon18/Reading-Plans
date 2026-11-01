// bc_descarga.js — baja los planos de un proyecto desde BuildingConnected (regla 0, v80h+).
//
// SOLO LECTURA: hace login y GETs. Nunca hace click en Bidding / Decline / Accept / Submit,
// nunca cambia el workflow state de una oportunidad. Si el status cambia, es un error de la tool.
//
// Credenciales: env BC_EMAIL y BC_PASSWORD (nunca se imprimen).
//
// Uso:
//   node bc_descarga.js buscar "<texto del nombre>"          → lista oportunidades que coinciden (id, GC, trade, due)
//   node bc_descarga.js arbol  <opportunity_id>              → árbol de archivos (carpeta/archivo, tamaño)
//   node bc_descarga.js bajar  <opportunity_id> <dest_dir> [carpeta ...]
//        sin carpetas: baja todo menos "Photos"; con carpetas: solo esas (nombre exacto de primer nivel)
//
// Cada archivo se verifica: bytes bajados == size de la API; si no cuadra, sale con error.
// Después se sube a Drive con: python3 -I /opt/takeoff/gdrive_fetch.py put <archivo> <folder_id>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const B = 'https://app.buildingconnected.com';

async function login() {
  if (!process.env.BC_EMAIL || !process.env.BC_PASSWORD) throw new Error('faltan BC_EMAIL / BC_PASSWORD');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(`${B}/login`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(8000);
  await page.locator('input[type=email], input[name=email], #userName').first().fill(process.env.BC_EMAIL);
  await page.keyboard.press('Enter');
  const pw = page.locator('input[type=password]').first();
  await pw.waitFor({ timeout: 30000 });
  await pw.fill(process.env.BC_PASSWORD);
  await page.keyboard.press('Enter');
  await page.waitForURL(/opportunities/, { timeout: 60000 });
  return { browser, ctx };
}

async function getJson(ctx, url) {
  const r = await ctx.request.get(B + url);
  if (!r.ok()) throw new Error(`${r.status()} ${url}`);
  return r.json();
}

async function buscar(ctx, q) {
  const out = [];
  for (const st of ['UNDECIDED', 'NEEDS_PROPOSAL', 'SUBMITTED', 'WON']) {
    for (let s = 0; s < 2000; s += 100) {
      const j = await getJson(ctx, `/api/opportunities/v2/pipeline?startIndex=${s}&count=100&order=asc&userFilter=IM_FOLLOWING&workflowStates%5B%5D=${st}&sortKey=DATE_DUE&archiveFilter=ACTIVE_ONLY`);
      for (const o of j.results || []) if (o.name.toLowerCase().includes(q.toLowerCase()))
        out.push({ id: o._id, name: o.name.trim(), gc: o.client?.company?.name, trade: o.tradeName, due: o.dateDue, state: st });
      if ((j.results || []).length < 100) break;
    }
  }
  return out;
}

async function arbol(ctx, opp, folderId = null, pre = '') {
  const j = await getJson(ctx, `/api/opportunities/${opp}/files${folderId ? '/' + folderId : ''}`);
  const res = [];
  for (const it of j.items || []) {
    const p = pre ? `${pre}/${it.name}` : it.name;
    if (it.type === 'FOLDER') res.push(...await arbol(ctx, opp, it._id, p));
    else res.push({ path: p, size: it.size, downloadUrl: it.downloadUrl });
  }
  return res;
}

(async () => {
  const [cmd, a1, a2, ...rest] = process.argv.slice(2);
  const { browser, ctx } = await login();
  try {
    if (cmd === 'buscar') console.log(JSON.stringify(await buscar(ctx, a1), null, 1));
    else if (cmd === 'arbol') for (const f of await arbol(ctx, a1)) console.log(f.size, f.path);
    else if (cmd === 'bajar') {
      const files = (await arbol(ctx, a1)).filter(f => {
        const top = f.path.split('/')[0];
        return rest.length ? rest.includes(top) : top !== 'Photos';
      });
      for (const f of files) {
        const dest = path.join(a2, f.path);
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        const r = await ctx.request.get(B + f.downloadUrl, { timeout: 1800000 });
        const b = await r.body();
        if (!r.ok() || b.length !== f.size) throw new Error(`descarga incompleta ${f.path}: ${r.status()} ${b.length}/${f.size}`);
        fs.writeFileSync(dest, b);
        console.log('OK', b.length, dest);
      }
    } else console.log('uso: buscar <texto> | arbol <opp_id> | bajar <opp_id> <dest> [carpeta ...]');
  } finally { await browser.close(); }
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
