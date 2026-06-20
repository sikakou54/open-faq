// SCR 画面モックの HTML を PNG へレンダリング(puppeteer-core + キャッシュ済み Chromium)
// 使い方: node render_mocks.js /tmp/mockwork/manifest.json /path/to/chrome
//   事前に `npm i puppeteer-core` とローカル Chromium が必要。
const fs = require('fs');
const puppeteer = require('puppeteer-core');

(async () => {
  const manifestPath = process.argv[2];
  const chromePath = process.argv[3];
  const items = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    args: ['--no-sandbox', '--font-render-hinting=none'],
  });
  let ok = 0, fail = 0;
  for (const it of items) {
    try {
      const page = await browser.newPage();
      await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: 2 });
      await page.goto('file://' + it.html, { waitUntil: 'networkidle0', timeout: 60000 });
      if (it.lucide) { await new Promise(r => setTimeout(r, 600)); }
      await new Promise(r => setTimeout(r, 150));
      const el = await page.$('#wrap');
      await el.screenshot({ path: it.png });
      await page.close();
      ok++;
      process.stdout.write('.');
    } catch (e) {
      fail++;
      console.error('\nFAIL', it.html, e.message);
    }
  }
  await browser.close();
  console.log(`\nrendered ok=${ok} fail=${fail}`);
})();
