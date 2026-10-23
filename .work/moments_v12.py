"""v12: «Моменты» — 4 шортса в каждом ивенте, в стиле ивента, видео играет прямо в карточке. python3 .work/moments_v12.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
js = (R / "app.js").read_text()


def block(key, head_cls, label):
    return (f'    <div class="moments moments--{key}" data-moments="{key}">\n'
            f'      <h3 class="moments__h"><span class="{head_cls}">{label}</span></h3>\n'
            f'      <div class="moments__row"></div>\n    </div>\n')


html = html.replace("  </div>\n\n  <!-- СЕЗОН: Св*бода -->",
                    block("hunt", "tag", "Моменты") + "  </div>\n\n  <!-- СЕЗОН: Св*бода -->", 1)
html = html.replace('    <div class="tiles" data-season="svoboda"></div>\n',
                    '    <div class="tiles" data-season="svoboda"></div>\n' + block("svoboda", "moments__pill", "Моменты"), 1)
html = html.replace('    <div class="tiles" data-season="btb"></div>\n',
                    '    <div class="tiles" data-season="btb"></div>\n' + block("btb", "moments__plate", "Моменты"), 1)
assert html.count('class="moments ') == 3
html = re.sub(r"style\.css\?v=\d+", "style.css?v=21", html)
html = re.sub(r"app\.js\?v=\d+", "app.js?v=15", html)

js = js.replace('const ARCHIVE = [', '''// Шортсы: моменты каждого ивента (обложки в assets/sh, вертикальные 9:16)
const MOMENTS = {
  hunt: [["YoJYnZUNnDI", "Хотел соскочить?"], ["2UoWbRU4cIY", "Гроулинг от Зеймана"], ["Uv7tubAMYaU", "Баттл на канале"], ["6SvWWvIPizE", "Высмеял фамилию"]],
  svoboda: [["GGSmuU7qm4M", "Это грайм-поинт"], ["n-xPEB1Xbh4", "Он быстрее Эминема"], ["5_YtLduaGsk", "Угорает со скуфа"], ["qHN80yrcbfA", "Его не остановить"]],
  btb: [["WX2qQ-eG-70", "Ресёрч на Палма"], ["sVpfOLDiy9U", "Убил самого лучшего рэпера"], ["FQVHj_vXIMA", "Тридцатиэтажная рифма"], ["lWjAqpVfuvw", "Уничтожил психолога"]],
};

const ARCHIVE = [''', 1)
js = js.replace('$(".eps").innerHTML', '''$$("[data-moments]").forEach((box) => {
  $(".moments__row", box).innerHTML = MOMENTS[box.dataset.moments].map(([id, t]) => `
    <figure class="moment">
      <button class="moment__frame" data-short="${id}" aria-label="Смотреть: ${t}">
        <img src="assets/sh/${id}.jpg" alt="" width="540" height="960" loading="lazy">
        <span class="moment__play" aria-hidden="true"></span>
      </button>
      <figcaption>${t}</figcaption>
    </figure>`).join("");
});
// Шортс играет прямо в карточке; запуск другого останавливает предыдущий
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-short]");
  if (!b) return;
  $$(".moment__frame.is-on").forEach((x) => { x.classList.remove("is-on"); $("iframe", x)?.remove(); });
  b.classList.add("is-on");
  b.insertAdjacentHTML("beforeend", `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.short}?autoplay=1&playsinline=1&rel=0" title="${b.getAttribute("aria-label")}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`);
});

$(".eps").innerHTML''', 1)

BONE, RED = "#ebe4d8", "#d3161d"
css = css.replace("/* СЕЗОНЫ: общее */", f'''/* МОМЕНТЫ: шортсы в каждом ивенте */
.moments {{ display: grid; grid-template-columns: clamp(150px, 15vw, 220px) repeat(4, minmax(0, 1fr)); gap: 28px clamp(16px, 1.8vw, 28px); align-items: start; max-width: 1440px; margin: clamp(44px, 5vw, 70px) auto 0; }}
.moments--hunt {{ padding: 0 var(--gutter) clamp(60px, 6vw, 90px); margin-top: 0; }}
.moments__h {{ margin: 0; }}
.moments__row {{ display: contents; }}
.moment {{ position: relative; margin: 0; min-width: 0; }}
.moment__frame {{ position: relative; display: block; width: 100%; aspect-ratio: 9 / 16; overflow: hidden; padding: 0; cursor: pointer; background: #000; }}
.moment__frame img {{ width: 100%; height: 100%; object-fit: cover; transition: transform .5s var(--ease); }}
.moment__frame:hover img {{ transform: scale(1.04); }}
.moment__frame iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }}
.moment__frame.is-on .moment__play {{ display: none; }}
.moment__play {{ position: absolute; left: 50%; top: 50%; width: 64px; height: 64px; translate: -50% -50%; border-radius: 50%; transition: scale .25s var(--ease); }}
.moment__play::after {{ content: ""; position: absolute; left: 54%; top: 50%; translate: -50% -50%; border: 13px solid transparent; border-left: 21px solid currentColor; border-right: 0; }}
.moment__frame:hover .moment__play {{ scale: 1.1; }}
.moment figcaption {{ text-transform: uppercase; }}

/* HUNT: полароиды на булавках, как на их обложках */
.moments--hunt .moment {{ padding: 10px 10px 0; background: var(--noise), #e9e0ca; box-shadow: 0 18px 34px -12px rgba(0, 0, 0, .9); rotate: -1.6deg; }}
.moments--hunt .moment:nth-child(2n) {{ rotate: 1.4deg; margin-top: 14px; }}
.moments--hunt .moment:nth-child(3) {{ rotate: -.6deg; }}
.moments--hunt .moment::before {{ content: ""; position: absolute; z-index: 2; left: 50%; top: -9px; width: 20px; height: 20px; translate: -50% 0; border-radius: 50%; background: radial-gradient(circle at 35% 32%, #ff7a7a, #c3161d 50%, #5c070b); box-shadow: 0 5px 8px rgba(0, 0, 0, .55); }}
.moments--hunt .moment__frame img {{ filter: sepia(.18) contrast(1.06); }}
.moments--hunt .moment__play {{ background: rgba(233, 224, 202, .92); color: #8c1015; }}
.moments--hunt figcaption {{ padding: 11px 4px 13px; text-align: center; color: #8c1015; font: 900 clamp(14px, 1.15vw, 17px)/1.15 var(--slab); }}

/* Св*бода: чёрная рама, белые наклонные имена и красный, как на их обложках */
.moments__pill {{ display: inline-block; background: #111; color: #fff; padding: 7px 20px 6px; border-radius: 999px; font: 700 22px/1 var(--disp); text-transform: uppercase; box-shadow: 0 0 0 2px rgba(255, 255, 255, .14), 0 0 10px 3px rgba(17, 17, 17, .4); }}
.moments--svoboda .moment {{ border: 7px solid #0e0e0e; box-shadow: 0 22px 40px -14px rgba(0, 0, 0, .95); }}
.moments--svoboda .moment__frame::after {{ content: ""; position: absolute; inset: 45% 0 0; background: linear-gradient(transparent, rgba(20, 9, 72, .92)); pointer-events: none; }}
.moments--svoboda .moment__frame.is-on::after {{ display: none; }}
.moments--svoboda .moment__play {{ background: #ff2f2f; color: #fff; box-shadow: 0 0 0 6px rgba(255, 47, 47, .25); }}
.moments--svoboda figcaption {{ position: absolute; z-index: 1; left: 14px; right: 14px; bottom: 16px; pointer-events: none; color: #fff; font: 700 clamp(20px, 1.9vw, 28px)/.98 var(--disp); transform: skewX(-8deg); text-shadow: 0 2px 10px rgba(0, 0, 0, .6); }}
.moments--svoboda figcaption::after {{ content: ""; display: block; width: 46px; height: 5px; margin-top: 9px; background: #ff2f2f; }}
.moments--svoboda .moment:has(.is-on) figcaption {{ display: none; }}

/* BTB: костяная рамка и красные плашки, как на афише */
.moments__plate {{ display: inline-block; padding: 9px 18px 7px; background: {RED}; color: {BONE}; font: 400 30px/1 "Anton", var(--disp); text-transform: uppercase; letter-spacing: .03em; box-shadow: inset 0 0 0 3px {RED}, inset 0 0 0 5px {BONE}; }}
.moments--btb .moment {{ box-shadow: 0 0 0 4px {BONE}, 0 22px 40px -14px rgba(0, 0, 0, .95); }}
.moments--btb .moment__frame img {{ filter: contrast(1.08) saturate(.9); }}
.moments--btb .moment__play {{ background: {BONE}; color: {RED}; }}
.moments--btb figcaption {{ position: absolute; z-index: 1; left: -6px; bottom: 18px; max-width: calc(100% - 4px); padding: 7px 11px 5px; rotate: -2deg; pointer-events: none; background: {RED}; color: {BONE}; font: 400 clamp(15px, 1.25vw, 19px)/1.05 "Anton", var(--disp); letter-spacing: .02em; box-shadow: inset 0 0 0 2px {RED}, inset 0 0 0 3.5px {BONE}, 0 8px 16px -6px rgba(0, 0, 0, .8); }}
.moments--btb .moment:has(.is-on) figcaption {{ display: none; }}

/* СЕЗОНЫ: общее */''', 1)

css = css.replace("@media (max-width: 1100px) {", '''@media (max-width: 1100px) {
  .moments { grid-template-columns: minmax(0, 1fr); }
  .moments__row { display: flex; gap: 18px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin: 0 calc(-1 * var(--gutter)); padding: 14px var(--gutter) 24px; }
  .moments__row::-webkit-scrollbar { display: none; }
  .moment { flex: 0 0 min(250px, 62vw); scroll-snap-align: center; }''', 1)

(R / "index.html").write_text(html)
(R / "style.css").write_text(css)
(R / "app.js").write_text(js)
print("ok")
