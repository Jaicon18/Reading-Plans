const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json', acceptDownloads: true, viewport:{width:1400,height:900} });
  const p = await ctx.newPage();
  const reqs=[]; p.on('request', r => { if (/api/.test(r.url()) && r.method()!=='GET') reqs.push(r.method()+' '+r.url().split('?')[0]); });
  p.on('popup', pp => console.log('POPUP', pp.url().split('?')[0]));
  await p.goto('https://app.buildingconnected.com/opportunities/6aed6ad3afb7ca85c2b332e1/files', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  await p.screenshot({ path: '/root/xf/bc/files_page.png' });
  await p.locator('button:has-text("Download All")').first().click();
  await p.waitForTimeout(8000);
  await p.screenshot({ path: '/root/xf/bc/after_click.png' });
  console.log(reqs.join('\n'));
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
