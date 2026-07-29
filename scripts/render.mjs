// HTMLテンプレート + データJSON -> PNG（1080x1920）
// 使い方: node scripts/render.mjs <template.html> <data.json> <out.png>
//
// Playwright はこの環境ではグローバルに導入されているため、
// グローバル node_modules から読み込む。
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
let globalRoot;
try {
  globalRoot = execSync("npm root -g", { encoding: "utf8" }).trim();
} catch {
  globalRoot = "/opt/node22/lib/node_modules";
}
const { chromium } = require(path.join(globalRoot, "playwright"));

const [, , tplPath, dataPath, outPath] = process.argv;
if (!tplPath || !dataPath || !outPath) {
  console.error("usage: node render.mjs <template.html> <data.json> <out.png>");
  process.exit(1);
}

const data = JSON.parse(readFileSync(dataPath, "utf8"));
const W = 1080, H = 1920;

const browser = await chromium.launch({ args: ["--no-sandbox", "--font-render-hinting=none"] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });

// テンプレートのスクリプトが走る前に window.__DATA__ を注入する
await page.addInitScript((d) => { window.__DATA__ = d; }, data);

await page.goto(pathToFileURL(path.resolve(tplPath)).href, { waitUntil: "networkidle" });
// Webフォントの読み込み完了を待つ（待たないと豆腐/フォールバックで撮れてしまう）
await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
await page.waitForTimeout(150);

await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: W, height: H } });
await browser.close();
console.log("rendered:", outPath);
