const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json', acceptDownloads: true });
  const p = await ctx.newPage();
  await p.goto('https://app.buildingconnected.com/opportunities/6aed6ad3afb7ca85c2b332e1/files', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 240000 }), p.locator('button:has-text("Download All")').first().click()]);
  const f = '/root/xf/bc/' + dl.suggestedFilename();
  await dl.saveAs(f); console.log('OK', f, fs.statSync(f).size);
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
