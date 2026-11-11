const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json' });
  const p = await ctx.newPage();
  const keep = {};
  p.on('response', async r => { const u = r.url(); if (/\/api\/.*(file|folder|opportunities\/6aed6ad3afb7ca85c2b332e1$)/i.test(u.split('?')[0])) { try { keep[u] = await r.json(); } catch (e) {} } });
  await p.goto('https://app.buildingconnected.com/opportunities/6aed6ad3afb7ca85c2b332e1/files', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(15000);
  fs.writeFileSync('/root/xf/bc/files_api.json', JSON.stringify(keep, null, 1));
  console.log(Object.keys(keep).map(k => k.split('?')[0]).join('\n'));
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
