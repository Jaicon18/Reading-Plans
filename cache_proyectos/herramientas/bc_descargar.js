// bc_descargar.js — BuildingConnected: login (un solo intento, sin volcar la página) + "Download All" de un RFP.
// SOLO lectura / descarga (U-129, REGLAS_PLAN_ROOM 1-5). Nunca Accept / Decline / Bidding / mensajes.
// BE-XF01 (Xfinity Interquest, 10-nov): el "Download All" redirige a una URL firmada de S3 (path-style) que el
// Chromium headless detrás del proxy no baja (SignatureDoesNotMatch). Arreglo: interceptar la URL del archivo
// (/archives/...files-archive.zip), abortar la navegación y bajarla con curl en el acto (expira en 60 s).
// Uso: BC_EMAIL / BC_PASSWORD del entorno;  node bc_descargar.js <rfp_or_opportunity_id> <carpeta_salida>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const [id, out] = process.argv.slice(2);
if (!id || !out) { console.log('uso: node bc_descargar.js <id> <carpeta>'); process.exit(2); }
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext();
  const p = await ctx.newPage();
  await p.goto('https://app.buildingconnected.com/login', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(4000);
  const email = p.locator('input[type=email], input[name=email], input#userName, input[name=userName]').first();
  await email.waitFor({ timeout: 60000 }); await email.fill(process.env.BC_EMAIL);
  await p.locator('button:has-text("Next"), button[type=submit], #verify_user_btn').first().click();
  await p.waitForTimeout(6000);
  const pw = p.locator('input[type=password]').first(); await pw.waitFor({ timeout: 60000 }); await pw.fill(process.env.BC_PASSWORD);
  await p.locator('button:has-text("Sign in"), button[type=submit], #btnSubmit').first().click();
  await p.waitForTimeout(15000);
  const body = (await p.locator('body').innerText().catch(() => '')).toLowerCase();
  const errs = ["didn't match", 'incorrect', 'captcha', 'verification code', 'two-step', 'too many'].filter(e => body.includes(e));
  if (errs.length) { console.log('LOGIN FAIL', JSON.stringify(errs)); process.exit(1); }   // un solo intento: PARAR
  let got = null;
  await p.route(/files-archive|\/archives\//, async (route) => { if (!got) got = route.request().url(); await route.abort(); });
  await p.goto(`https://app.buildingconnected.com/opportunities/${id}/files`, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(12000);
  await p.locator('button:has-text("Download All")').first().click();
  for (let i = 0; i < 90 && !got; i++) await p.waitForTimeout(1000);
  if (!got) { console.log('NO ARCHIVE URL'); process.exit(1); }
  execFileSync('curl', ['-sS', '-f', '-o', `${out}/files-archive.zip`, got], { stdio: 'inherit' });
  console.log('OK', `${out}/files-archive.zip`, fs.statSync(`${out}/files-archive.zip`).size);
  await b.close();
})().catch(e => { console.log('FAIL', String(e).slice(0, 200)); process.exit(1); });
