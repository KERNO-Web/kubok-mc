// Плитки шума/зерна, снятые тем движком и с той плотностью, где их чаще смотрят:
// 2x — Chromium (ПК, Retina), 3x — WebKit (iPhone). Снимаем div с исходным SVG-фоном на прозрачном фоне,
// потом в браузере выравниваем RGB (цвет у шума постоянный, меняется только прозрачность).
// node .work/audit/noise2.mjs ; затем cwebp -lossless -exact -z 9 .work/audit/<name>-<d>x.png -o assets/fx/<name>-<d>x.webp
import { createRequire } from "module";
import fs from "fs";
import { execSync } from "child_process";
const require = createRequire(import.meta.url);
const pw = require("/Users/sergey-mac/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core");
const css = fs.readFileSync("/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/style-before.css", "utf8");
const get = (name) => css.match(new RegExp(`--${name}: url\\("(data:image/svg\\+xml,[^"]+)"\\)`))[1];
const W = "/Users/sergey-mac/Vibecode/kubok-mc/.work/audit/";
for (const [eng, d] of [["chromium", 2], ["webkit", 3]]) {
  const b = await pw[eng].launch();
  const p = await (await b.newContext({ deviceScaleFactor: d, viewport: { width: 600, height: 600 } })).newPage();
  for (const [name, size, rgb] of [["noise", 200, [51, 41, 31]], ["speck", 240, [255, 255, 255]]]) {
    await p.setContent(`<html><body style="margin:0;background:transparent"><div id="i" style="width:${size}px;height:${size}px;background:url(&quot;${get(name)}&quot;)"></div></body></html>`);
    await p.waitForTimeout(300);
    const raw = W + `${name}-${d}x-raw.png`;
    await p.locator("#i").screenshot({ path: raw, omitBackground: true });
    // выравнивание RGB в канвасе
    const b64 = await p.evaluate(async ([src, rgb]) => {
      const img = new Image(); img.src = src; await img.decode();
      const c = document.createElement("canvas"); c.width = img.naturalWidth; c.height = img.naturalHeight;
      const x = c.getContext("2d"); x.drawImage(img, 0, 0);
      const dd = x.getImageData(0, 0, c.width, c.height);
      for (let i = 0; i < dd.data.length; i += 4) { dd.data[i] = rgb[0]; dd.data[i + 1] = rgb[1]; dd.data[i + 2] = rgb[2]; }
      x.putImageData(dd, 0, 0);
      return [c.width, c.toDataURL("image/png").split(",")[1]];
    }, ["data:image/png;base64," + fs.readFileSync(raw).toString("base64"), rgb]);
    const out = W + `${name}-${d}x.png`;
    fs.writeFileSync(out, Buffer.from(b64[1], "base64"));
    execSync(`cwebp -quiet -lossless -exact -z 9 ${out} -o /Users/sergey-mac/Vibecode/kubok-mc/assets/fx/${name}-${d}x.webp`);
    console.log(eng, name, d + "x", b64[0] + "px", fs.statSync(`/Users/sergey-mac/Vibecode/kubok-mc/assets/fx/${name}-${d}x.webp`).size);
  }
  await b.close();
}
