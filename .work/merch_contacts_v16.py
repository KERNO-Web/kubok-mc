"""v16: раздел «Мерч» (3 пары спереди/сзади, «только для демонстрации») и контакты в финале (Boosty, Telegram, VK,
YouTube + почта для сотрудничества с копированием). python3 .work/merch_contacts_v16.py (один раз)"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
html = (R / "index.html").read_text()
css = (R / "style.css").read_text()
js = (R / "app.js").read_text()

MERCH = [("white", "Белая", "Логотип спереди, XX на спине"),
         ("black", "Чёрная", "Логотип спереди, XX на спине"),
         ("model", "Oversize", "Кубок спереди, Ultimate на спине")]
cards = "\n".join(f'''      <article class="tee" data-side="front">
        <div class="tee__frame">
          <img class="tee__img tee__img--front" src="assets/merch/{k}-front.jpg" alt="Футболка «{n}», спереди" loading="lazy">
          <img class="tee__img tee__img--back" src="assets/merch/{k}-back.jpg" alt="Футболка «{n}», сзади" loading="lazy">
        </div>
        <div class="tee__bar">
          <h3 class="tee__name">{n}</h3>
          <div class="tee__flip" role="group" aria-label="Сторона"><button data-side="front" aria-pressed="true">Спереди</button><button data-side="back" aria-pressed="false">Сзади</button></div>
        </div>
        <p class="tee__note">{d}</p>
      </article>''' for k, n, d in MERCH)

merch = f'''  <!-- КАРКАС. Мерч (концепт) -->
  <section class="merch" id="merch" data-skin="shell">
    <div class="merch__head">
      <h2>Мерч</h2>
      <p class="merch__demo">Только для демонстрации</p>
    </div>
    <div class="merch__row">
{cards}
    </div>
  </section>

  <!-- КАРКАС. Финал -->'''
html = html.replace("  <!-- КАРКАС. Финал -->", merch, 1)

links = '''      <nav class="final__links" aria-label="Мы в сети">
        <a href="https://t.me/kbkmc" target="_blank" rel="noopener"><span>Telegram</span><i>t.me/kbkmc</i></a>
        <a href="https://vk.com/kbkmc" target="_blank" rel="noopener"><span>ВКонтакте</span><i>vk.com/kbkmc</i></a>
        <a href="https://www.youtube.com/@kbkmc" target="_blank" rel="noopener"><span>YouTube</span><i>@kbkmc</i></a>
        <a href="https://boosty.to/kbkmc" target="_blank" rel="noopener"><span>Boosty</span><i>boosty.to/kbkmc</i></a>
      </nav>
      <div class="final__mail">
        <p>Для предложений и&nbsp;сотрудничества</p>
        <a href="mailto:kubokmc@gmail.com">kubokmc@gmail.com</a>
        <button class="final__copy" data-copy="kubokmc@gmail.com">Скопировать</button>
      </div>'''
html = re.sub(r'      <nav class="final__links">.*?</nav>\n', links + "\n", html, flags=re.S)
assert "final__mail" in html
html = html.replace('<footer class="final" data-skin="shell">', '<footer class="final" id="contacts" data-skin="shell">', 1)
html = html.replace('    <a href="#archive">Архив</a>\n', '    <a href="#archive">Архив</a>\n    <a href="#merch">Мерч</a>\n    <a href="#contacts">Контакты</a>\n', 1)
html = re.sub(r"style\.css\?v=\d+", "style.css?v=28", html)
html = re.sub(r"app\.js\?v=\d+", "app.js?v=21", html)

js = js.replace("\n// ---------- Анимации ----------", r'''
// Мерч: переключатель спереди/сзади; на компьютере сторона меняется и при наведении
$$(".tee").forEach((t) => {
  const set = (side) => {
    t.dataset.side = side;
    $$(".tee__flip button", t).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.side === side)));
  };
  $$(".tee__flip button", t).forEach((b) => b.addEventListener("click", () => set(b.dataset.side)));
  const fr = $(".tee__frame", t);
  fr.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") set("back"); });
  fr.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse") set("front"); });
});

// Почта: копирование в буфер
$$("[data-copy]").forEach((b) => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = "Скопировано"; }
  catch { location.href = "mailto:" + b.dataset.copy; }
  setTimeout(() => { b.textContent = "Скопировать"; }, 1800);
}));

// ---------- Анимации ----------''', 1)
js = js.replace('[".orgs > *", "up"],', '[".orgs > *", "up"], [".merch__head", "up"], [".tee", "up"], [".final__links a", "side"], [".final__mail", "up"],', 1)

css = css.replace("/* АРХИВ */", '''/* МЕРЧ (концепт) */
.merch { max-width: 1440px; margin: 0 auto; padding: clamp(60px, 6vw, 90px) var(--gutter); }
.merch__head { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; margin-bottom: 26px; }
.merch__head h2 { font: 700 clamp(44px, 4.6vw, 76px)/.9 var(--disp); text-transform: uppercase; }
.merch__demo { padding: 7px 14px 6px; border: 2px dashed var(--accent); color: var(--accent); font: 700 15px/1 var(--disp); text-transform: uppercase; letter-spacing: .06em; rotate: -2deg; }
.merch__row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(14px, 1.6vw, 24px); }
.tee { min-width: 0; }
.tee__frame { position: relative; aspect-ratio: 1; overflow: hidden; background: #000; cursor: pointer; }
.tee__img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: opacity .45s var(--ease), scale .6s var(--ease); }
.tee [class*="model"], .tee__img[src*="model"] { object-position: 50% 12%; }
.tee__img--back { opacity: 0; scale: 1.04; }
.tee[data-side="back"] .tee__img--back { opacity: 1; scale: 1; }
.tee[data-side="back"] .tee__img--front { opacity: 0; scale: .97; }
.tee__bar { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 14px 0 6px; border-bottom: 2px solid rgba(255, 255, 255, .14); }
.tee__name { font: 700 26px/1 var(--disp); text-transform: uppercase; }
.tee__flip { display: flex; box-shadow: inset 0 0 0 2px rgba(255, 255, 255, .25); }
.tee__flip button { padding: 8px 12px 7px; font: 700 13px/1 var(--disp); text-transform: uppercase; letter-spacing: .04em; color: var(--muted); transition: background-color .2s, color .2s; }
.tee__flip button[aria-pressed="true"] { background: var(--fg); color: var(--bg); }
.tee__note { margin-top: 8px; color: var(--muted); font-size: 15px; }

/* АРХИВ */''', 1)

for start in [".final__links {", ".final__links a:hover"]:
    css = re.sub(r"^" + re.escape(start) + r"[^\n]*\n", "", css, flags=re.M)
css = css.replace(".final__note {", '''.final__links { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; width: 100%; }
.final__links a { display: grid; gap: 6px; padding: 16px 18px 14px; background: rgba(0, 0, 0, .16); box-shadow: inset 0 0 0 2px rgba(255, 255, 255, .28); transition: background-color .25s, color .25s, translate .25s var(--ease); }
.final__links a span { font: 700 clamp(22px, 2vw, 30px)/1 var(--disp); text-transform: uppercase; }
.final__links a span::after { content: " ↗"; font-size: .7em; opacity: .7; }
.final__links a i { font: 500 15px/1.2 var(--text); font-style: normal; opacity: .8; }
.final__links a:hover { background: #fff; color: var(--accent); translate: 0 -3px; }
.final__mail { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; width: 100%; padding-top: 18px; }
.final__mail p { width: 100%; font: 500 16px var(--disp); text-transform: uppercase; letter-spacing: .04em; opacity: .85; }
.final__mail a { font: 700 clamp(26px, 3.2vw, 48px)/1 var(--disp); box-shadow: inset 0 -3px rgba(255, 255, 255, .5); transition: box-shadow .2s; }
.final__mail a:hover { box-shadow: inset 0 -3px #fff; }
.final__copy { padding: 10px 16px 9px; background: #fff; color: var(--accent); font: 700 14px/1 var(--disp); text-transform: uppercase; letter-spacing: .04em; }
.final__copy:hover { background: #111; color: #fff; }
.final__note {''', 1)
css = css.replace("@media (max-width: 767px) {", '''@media (max-width: 767px) {
  .merch__row { grid-template-columns: minmax(0, 1fr); }
  .final__links { grid-template-columns: repeat(2, minmax(0, 1fr)); }''', 1)

(R / "index.html").write_text(html)
(R / "style.css").write_text(css)
(R / "app.js").write_text(js)
print("ok")
