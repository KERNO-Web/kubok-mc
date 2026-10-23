# v35: мобилка по аудиту docs/AUDIT_MOBILE.md — P0 (сетка HUNT, свайп в Safari, меню) и P1
p='index.html'; s=open(p).read()
old='  <nav class="mast__nav" aria-label="Разделы">'
assert old in s
s=s.replace(old,'  <nav class="mast__nav" id="mnav" aria-label="Разделы">',1)
old='  <button class="mast__cta" data-ticket="quarter">Билеты</button>\n</header>'
assert old in s
s=s.replace(old,'  <button class="mast__cta" data-ticket="quarter">Билеты</button>\n  <button class="mast__burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="mnav"><i></i><i></i></button>\n</header>',1)
s=s.replace('style.css?v=67','style.css?v=68').replace('app.js?v=38','app.js?v=39')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
s+='''
// Меню на телефоне: бургер раскрывает навигацию на весь экран
{
  const mast = $(".mast"), burger = $(".mast__burger");
  const setMenu = (open) => {
    mast.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    document.documentElement.classList.toggle("menu-open", open);
  };
  burger.addEventListener("click", () => setMenu(!mast.classList.contains("is-open")));
  $$(".mast__nav a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
  matchMedia("(min-width: 768px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });
}

// Просмотр фото: свайп пальцем листает
{
  let sx = null;
  lb.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (sx === null) return;
    const dx = e.changedTouches[0].clientX - sx;
    sx = null;
    if (Math.abs(dx) > 50) lbShow(lbIdx + (dx < 0 ? 1 : -1));
  });
}
'''
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''

/* ============ v35 Мобилка по аудиту (docs/AUDIT_MOBILE.md). Блок последний — поздние правила для ПК его не перебивают ============ */

/* Main Event: стрелки по центру кадра на любой ширине (cqw = ширина кадра внутри рамки) */
.extra__view { container-type: inline-size; }
.extra__nav--big { top: calc(14px + 100cqw * 9 / 32); }

/* Бургер (виден только на телефоне) */
.mast__burger { display: none; position: relative; width: 44px; height: 44px; margin-right: -10px; }
.mast__burger i { position: absolute; left: 11px; right: 11px; height: 2px; background: currentColor; transition: translate .3s var(--ease), rotate .3s var(--ease); }
.mast__burger i:first-child { top: 17px; }
.mast__burger i:last-child { top: 25px; }
.mast.is-open .mast__burger i:first-child { translate: 0 4px; rotate: 45deg; }
.mast.is-open .mast__burger i:last-child { translate: 0 -4px; rotate: -45deg; }
html.menu-open { overflow: hidden; }

/* Тач-устройства: ничего анимированного поверх лент (в Safari такие слои мешают свайпу), без 3D у шортсов */
@media (hover: none) {
  .event::after { z-index: -1; animation: none; }
  body::after { display: none; }
  .moment__frame { transform: none; transform-style: flat; }
  .moment__frame::before { display: none; }
}

@media (max-width: 1100px) {
  .ev-grid { grid-template-columns: minmax(0, 1fr); }
}

@media (max-width: 900px) {
  /* шапка HUNT: без пустого дерева, по углам два полароида с фото HUNT */
  .ev-head { min-height: auto; padding: 150px 16px 48px; }
  .wall { display: block; inset: 72px 0 auto; height: 60vw; width: auto; }
  .wall .scrap, .pol--b, .pol--d { display: none; }
  .pol { width: 31vw; padding: 6px 6px 22px; }
  .pol--a { left: 3%; top: 0; rotate: -9deg; }
  .pol--c { right: 3%; left: auto; top: 6vw; rotate: 8deg; }
  .ev-head__plate { width: min(78vw, 360px); }
}

@media (max-width: 767px) {
  /* меню */
  .mast__burger { display: block; }
  .mast__cta { padding: 12px 6px; }
  .mast.is-open { mix-blend-mode: normal; background: #0c0a09; }
  .mast.is-open .mast__nav { display: flex; position: fixed; inset: 60px 0 0; z-index: 49; flex-direction: column; gap: 0; padding: 18px var(--gutter) 40px; overflow-y: auto; background: #0c0a09; font: 700 34px/1 var(--disp); }
  .mast.is-open .mast__nav a { display: block; padding: 14px 0; border-bottom: 1px solid rgba(255, 255, 255, .1); }
  .mast.is-open .mast__nav a:nth-child(2), .mast.is-open .mast__nav a:nth-child(3) { display: block; }

  /* обложка: плашка в одну строку */
  .cover__band p span:last-child { display: none; }

  /* пары 1/4: ники переносятся внутри своей половины */
  .bracket__list b { font-size: 13px; white-space: normal; line-height: 1.05; }
  .bracket__list i { font-size: 15px; }
  /* пропали без вести */
  .gone { gap: 10px; }
  .gone figcaption { font-size: 12px; overflow-wrap: anywhere; }
  /* Main Event: стрелки 44px внутри кадра */
  .extra__nav--big { width: 44px; height: 44px; font-size: 22px; }
  .extra__nav--l { left: 2px; }
  .extra__nav--r { right: 2px; }

  /* афиша BTB по центру под текстом */
  .season__poster { justify-self: center; width: min(66%, 270px); margin-top: 22px; rotate: -2deg; }

  /* схема зала: подписи крупнее */
  .hall text { font-size: 20px; }
  .hall text.sm { font-size: 15px; }
  .hall text.ring { font-size: 22px; }

  /* мерч: лента со свайпом, знак меньше */
  .merch-zone .merch__row { display: flex; gap: 14px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin: 0 calc(-1 * var(--gutter)); padding: 0 var(--gutter) 10px; scroll-padding-inline: var(--gutter); }
  .merch-zone .merch__row::-webkit-scrollbar { display: none; }
  .merch-zone .tee { flex: 0 0 80vw; scroll-snap-align: start; }
  .merch-zone::before { height: 110px; top: 40px; opacity: .08; }
  .merch-zone .merch__head { min-height: 0; }
  .tee__flip button { min-height: 40px; padding-inline: 12px; }
  .mo__sizes { grid-template-columns: repeat(5, minmax(0, 1fr)); }
  .final__copy { min-height: 44px; }
}
'''
open(p,'w').write(s)
