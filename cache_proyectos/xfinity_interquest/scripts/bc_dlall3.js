const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ storageState: '/root/xf/bc/state.json' });
  const p = await ctx.newPage();
  let got = null;
  await p.route(/files-archive|\/archives\//, async (route) => { if (!got) got = route.request().url(); await route.abort(); });
  await p.goto('https://app.buildingconnected.com/opportunities/6aed6ad3afb7ca85c2b332e1/files', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  await p.locator('button:has-text("Download All")').first().click();
  for (let i = 0; i < 60 && !got; i++) await p.waitForTimeout(1000);
  if (!got) { console.log('NOURL'); process.exit(1); }
  console.log('HOST', new URL(got).host, 'PATH', new URL(got).pathname.slice(0,80));
  try { execFileSync('curl', ['-sS', '-f', '-o', '/root/xf/bc/files-archive.zip', got], { stdio: 'inherit' }); console.log('CURL OK'); }
  catch (e) { console.log('CURL FAIL'); }
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 300)); process.exit(1); });
