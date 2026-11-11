const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json', acceptDownloads: true });
  const p = await ctx.newPage();
  const urls = [];
  p.on('request', r => { const u = r.url(); if (/download|signed|s3|derivative/i.test(u)) urls.push(r.method() + ' ' + u.split('?')[0]); });
  await p.goto('https://app.buildingconnected.com/opportunities/6aed6ad3afb7ca85c2b332e1/files', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  const names = ['Xfinity BP_Colorado Springs', 'Interquest Concrete Rough layout'];
  for (const n of names) {
    const row = p.locator(`text=${n}`).first();
    await row.hover().catch(()=>{});
    // try a download button in the row
    const rowEl = row.locator('xpath=ancestor::*[self::tr or @role="row" or contains(@class,"row")][1]');
    const btn = rowEl.locator('button[aria-label*="ownload" i], [data-id*="download" i], button:has-text("Download"), a:has-text("Download")').first();
    let dl;
    try {
      [dl] = await Promise.all([p.waitForEvent('download', { timeout: 30000 }), btn.click({ timeout: 10000 })]);
    } catch (e) { console.log('NOBTN', n, String(e).slice(0,120)); continue; }
    const f = '/root/xf/bc/' + dl.suggestedFilename();
    await dl.saveAs(f); console.log('OK', f, fs.statSync(f).size);
  }
  console.log(urls.slice(0,20).join('\n'));
  const btns = await p.locator('button').allInnerTexts(); console.log('BTNS', JSON.stringify([...new Set(btns.map(s=>s.trim()).filter(Boolean))].slice(0,40)));
  const al = await p.locator('button[aria-label]').evaluateAll(es => es.map(e => e.getAttribute('aria-label'))); console.log('ARIA', JSON.stringify([...new Set(al)].slice(0,40)));
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
