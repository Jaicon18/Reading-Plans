const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json' });
  const p = await ctx.newPage();
  const api = [];
  p.on('response', r => { const u = r.url(); if (/\/api\//.test(u) && !/analytics|segment|track/.test(u)) api.push(r.status() + ' ' + u.split('?')[0]); });
  await p.goto('https://app.buildingconnected.com/rfps/6aed6ad3afb7ca85c2b332e1', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  console.log('URL', p.url());
  const tabs = await p.locator('a, [role=tab]').allInnerTexts();
  console.log('TABS', JSON.stringify([...new Set(tabs.map(t => t.trim()).filter(t => t && t.length < 30))].slice(0, 60)));
  console.log(api.slice(0, 60).join('\n'));
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
