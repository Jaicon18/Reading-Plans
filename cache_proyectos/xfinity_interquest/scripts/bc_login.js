// Login BuildingConnected - un solo intento, sin volcar la página (REGLAS_PLAN_ROOM 4). Solo lectura.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true });
  const p = await ctx.newPage();
  await p.goto('https://app.buildingconnected.com/login', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(4000);
  const email = p.locator('input[type=email], input[name=email], input#userName, input[name=userName]').first();
  await email.waitFor({ timeout: 60000 });
  await email.fill(process.env.BC_EMAIL);
  const nxt = p.locator('button:has-text("Next"), button[type=submit], #verify_user_btn').first();
  await nxt.click();
  await p.waitForTimeout(6000);
  const pw = p.locator('input[type=password]').first();
  await pw.waitFor({ timeout: 60000 });
  await pw.fill(process.env.BC_PASSWORD);
  await p.locator('button:has-text("Sign in"), button[type=submit], #btnSubmit').first().click();
  await p.waitForTimeout(15000);
  const body = (await p.locator('body').innerText().catch(() => '')).toLowerCase();
  const errs = ["didn't match", 'incorrect', 'captcha', 'verification code', 'two-step', 'too many'].filter(e => body.includes(e));
  console.log('URL', p.url().split('?')[0], 'ERR', JSON.stringify(errs));
  await ctx.storageState({ path: '/root/xf/bc/state.json' });
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 200)); process.exit(1); });
