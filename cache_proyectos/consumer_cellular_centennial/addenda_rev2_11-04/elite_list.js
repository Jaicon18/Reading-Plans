// Elite plan room (Pantera): open the project with the access key of the invitation e-mail and record the file-list
// JSON responses. READ ONLY: no clicks other than opening the page (U-129, REGLAS_PLAN_ROOM).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  const got = [];
  p.on('response', async r => { const u = r.url(); const ct = r.headers()['content-type'] || '';
    if (ct.includes('json')) { try { const t = await r.text(); got.push({u, t: t.slice(0, 200000)}); } catch (e) {} } });
  await p.goto(process.argv[2], { waitUntil: 'networkidle', timeout: 120000 }).catch(() => {});
  await p.waitForTimeout(15000);
  fs.writeFileSync('/root/cc/work/addenda/ER/net.json', JSON.stringify(got));
  console.log('responses', got.length, got.map(g => g.u.replace(/accesskey=[^&#]+/i, 'accesskey=***')).slice(0, 40).join('\n'));
  await b.close();
})();
