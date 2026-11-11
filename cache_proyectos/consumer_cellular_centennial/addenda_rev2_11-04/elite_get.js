// Elite plan room: download the files listed in sel.json (addenda + Current Set) through the page's own session. READ ONLY.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const sel = JSON.parse(fs.readFileSync('/root/cc/work/addenda/ER/sel.json'));
  const b = await chromium.launch(); const ctx = await b.newContext(); const p = await ctx.newPage();
  let auth = null;
  p.on('request', r => { const h = r.headers(); if (!auth && h['authorization'] && r.url().includes('panteratools')) auth = h['authorization']; });
  await p.goto(process.argv[2], { waitUntil: 'networkidle', timeout: 120000 }).catch(() => {});
  await p.waitForTimeout(12000);
  let ok = 0;
  for (const s of sel) {
    const dir = '/root/cc/work/addenda/ER/' + (s.path.includes('Addenda') ? 'addenda' : 'current');
    fs.mkdirSync(dir, { recursive: true });
    const r = await ctx.request.get(s.url, { headers: auth ? { authorization: auth } : {} , timeout: 120000});
    if (r.ok()) { fs.writeFileSync(path.join(dir, s.name), await r.body()); ok++; } else console.log('FAIL', s.name, r.status());
  }
  console.log('downloaded', ok, 'of', sel.length, 'auth header', !!auth);
  await b.close();
})();
