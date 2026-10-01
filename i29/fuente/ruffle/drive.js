// Banco en Ruffle: node drive.js SWF W H script.json
const path = require('path');
const pw = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [swf, W, H, scriptFile, outDir] = process.argv.slice(2);
  const steps = JSON.parse(fs.readFileSync(scriptFile, 'utf8'));
  const browser = await pw.chromium.launch({args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required']});
  const page = await browser.newPage({viewport: {width: +W, height: +H}, locale: 'en-US'});
  page.on('console', m => console.log('[console]', m.type(), m.text().slice(0, 300))); page.on('pageerror', e => console.log('[pageerror]', String(e).slice(0,300))); page.on('requestfailed', r => console.log('[reqfail]', r.url(), r.failure() && r.failure().errorText));
  await page.goto('http://127.0.0.1:8765/ruffle/page.html?swf=' + encodeURIComponent(swf));
  await page.addStyleTag({content: '.hardware-acceleration-modal, #hardware-acceleration-modal {display:none !important}'}).catch(()=>{});
  const dbg = async (cmd) => page.evaluate(c => { try { return window.__player.dbg(c); } catch (e) { return 'ERR ' + e; } }, cmd);
  for (const s of steps) {
    if (s.waitdbg) {
      const t0 = Date.now();
      while (Date.now() - t0 < s.waitdbg) {
        const ok = await page.evaluate(() => !!(window.__player && typeof window.__player.dbg === 'function'));
        if (ok) break;
        await page.waitForTimeout(500);
      }
      console.log('dbg listo en', (Date.now() - t0) / 1000, 's');
    }
    if (s.wait) await page.waitForTimeout(s.wait);
    if (s.dbg) { const r = await dbg(s.dbg); console.log('dbg', s.dbg, '->', String(r).slice(0, 4000)); }
    if (s.click) { await page.mouse.click(s.click[0], s.click[1]); }
    if (s.move) { await page.mouse.move(s.move[0], s.move[1], {steps: s.steps || 8}); }
    if (s.shot) { await page.screenshot({path: path.join(outDir, s.shot)}); console.log('shot', s.shot); }
    if (s.until) {
      const t0 = Date.now();
      while (Date.now() - t0 < (s.timeout || 60000)) {
        const r = await dbg(s.until);
        if (String(r) === String(s.eq)) break;
        await page.waitForTimeout(500);
      }
      console.log('until', s.until, '=', await dbg(s.until));
    }
  }
  await browser.close();
})();
