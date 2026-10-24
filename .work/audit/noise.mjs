// Шум --noise и зерно --speck из style.css (SVG feTurbulence) -> готовые плитки 2x в assets/fx/ (webp без потерь).
// SVG-фильтр в фоне Safari пересчитывает при каждой отрисовке; картинка рисуется сразу.
// Цвет у шума постоянный (его задаёт feColorMatrix), меняется только прозрачность — RGB выравниваем, чтобы файл был маленьким.
// node .work/audit/noise.mjs  (потом cwebp, см. ниже)
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const css = fs.readFileSync("/Users/sergey-mac/Vibecode/kubok-mc/style.css", "utf8");
const get = (name) => css.match(new RegExp(`--${name}: url\\("(data:image/svg\\+xml,[^"]+)"\\)`))[1];
const browser = await pw.chromium.launch();
const p = await browser.newPage();
for (const [name, size, rgb] of [["noise", 200, [51, 41, 31]], ["speck", 240, [255, 255, 255]]]) {
  const b64 = await p.evaluate(async ([src, size, rgb]) => {
    const img = new Image();
    img.src = src;
    await img.decode();
    const c = document.createElement("canvas");
    c.width = c.height = size * 2;
    const x = c.getContext("2d");
    x.drawImage(img, 0, 0, size * 2, size * 2);
    const d = x.getImageData(0, 0, c.width, c.height);
    for (let i = 0; i < d.data.length; i += 4) { d.data[i] = rgb[0]; d.data[i + 1] = rgb[1]; d.data[i + 2] = rgb[2]; }
    x.putImageData(d, 0, 0);
    return c.toDataURL("image/png").split(",")[1];
  }, [get(name), size, rgb]);
  fs.writeFileSync(`/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/${name}.png`, Buffer.from(b64, "base64"));
}
await browser.close();
console.log("ok");
