"""v13: анимации (интро обложки, параллакс, появления в стиле каждого ивента, 3D-наклон шортсов),
зерно по всему сайту, архив как их афиша TOP 16 (бумага, бордовая плашка, красные VS). python3 .work/anim_v13.py"""
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent

JS = r'''

// ---------- Анимации ----------
// Появления по скроллу: класс .rv + тип (data-rv), .in когда элемент в кадре; --i даёт ступеньку внутри группы
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!still) {
  document.documentElement.classList.add("anim");
  const groups = [
    [".ev-head__word", "stamp"], [".ev-head__info, .ev-head .btn", "up"],
    [".bracket__list li", "side"], [".gone figure", "drop"], [".extra", "up"], [".tag", "pop"],
    [".sv__left", "slap"], [".sv__bars span", "pop"],
    [".btb__title", "slam"], [".btb__bar", "stamp"], [".btb__when, .btb__text", "up"], [".btb .season__poster", "fly"],
    [".tiles .tile", "up"], [".moments__h", "pop"], [".moments--hunt .moment", "drop"], [".moments--svoboda .moment, .moments--btb .moment", "up"],
    [".archive__head", "up"], [".eps li", "side"], [".orgs > *", "up"], [".final > *", "up"],
  ];
  const io = new IntersectionObserver((list) => list.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -10% 0px" });
  groups.forEach(([sel, kind]) => {
    const seen = new Map();
    $$(sel).forEach((el) => {
      const i = seen.get(el.parentElement) || 0;
      seen.set(el.parentElement, i + 1);
      el.classList.add("rv");
      el.dataset.rv = kind;
      el.style.setProperty("--i", Math.min(i, 8));
      io.observe(el);
    });
  });

  // Параллакс обложки: фон отстаёт сильнее логотипа, люди впереди
  const cover = $(".cover");
  let ticking = false;
  const hero = () => {
    ticking = false;
    const p = Math.min(1, Math.max(0, scrollY / cover.offsetHeight));
    cover.style.setProperty("--hp", p.toFixed(4));
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(hero); } }, { passive: true });
  hero();

  // 3D-наклон карточек шортсов за курсором
  $$(".moment__frame").forEach((f) => {
    f.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      const r = f.getBoundingClientRect();
      f.style.setProperty("--ry", ((e.clientX - r.left) / r.width - .5) * 14 + "deg");
      f.style.setProperty("--rx", (.5 - (e.clientY - r.top) / r.height) * 12 + "deg");
      f.style.setProperty("--gx", ((e.clientX - r.left) / r.width) * 100 + "%");
      f.style.setProperty("--gy", ((e.clientY - r.top) / r.height) * 100 + "%");
    });
    f.addEventListener("pointerleave", () => { f.style.setProperty("--rx", "0deg"); f.style.setProperty("--ry", "0deg"); });
  });
}
'''

CSS = r'''

/* ---------- Зерно по всему сайту ---------- */
body::after { content: ""; position: fixed; inset: -50%; z-index: 90; pointer-events: none; background: var(--speck); opacity: .07; mix-blend-mode: screen; animation: grain .8s steps(4) infinite; }
.cover::after { content: ""; position: absolute; inset: 0; z-index: 3; pointer-events: none; background: var(--speck), var(--noise); opacity: .32; mix-blend-mode: screen; animation: grain 1s steps(5) infinite; }
@media (prefers-reduced-motion: reduce) { body::after, .cover::after { animation: none; } }

/* ---------- Архив = их афиша TOP 16: бежевая бумага, бордовая плашка, слэб, красные VS ---------- */
.archive { position: relative; max-width: 1440px; margin: clamp(30px, 4vw, 60px) auto; padding: clamp(30px, 3.4vw, 54px) clamp(20px, 3.4vw, 54px) clamp(36px, 3.6vw, 56px); background: radial-gradient(120% 90% at 50% 40%, transparent 55%, rgba(80, 52, 30, .28)), var(--noise), var(--noise), #d6cfbd; color: #1b1614; box-shadow: inset 0 0 0 10px #d6cfbd, inset 0 0 0 12px #1b1614, inset 0 0 0 16px #d6cfbd, inset 0 0 0 17px #1b1614, 0 30px 70px -20px rgba(0, 0, 0, .9); }
.archive__head { align-items: center; margin-bottom: 26px; }
.archive__head h2 { display: inline-flex; align-items: baseline; flex-wrap: wrap; gap: 6px 18px; padding: 10px 22px 8px; background: #6c0d10; color: #e9e0ca; font: 900 clamp(34px, 3.6vw, 58px)/1 var(--slab); box-shadow: inset 0 0 0 3px #6c0d10, inset 0 0 0 5px #e9e0ca; }
.archive__head h2 small { font: 700 clamp(15px, 1.3vw, 20px)/1 var(--slab); color: #d9b9a3; }
.archive__head a { color: #6c0d10; font-family: var(--slab); font-weight: 900; border-bottom: 2px solid; }
.archive .eps a { border-top: 2px dashed rgba(27, 22, 20, .45); }
.archive .eps img { box-shadow: 0 0 0 4px #ece4d0, 0 6px 14px rgba(40, 22, 10, .45); filter: sepia(.2) contrast(1.05); transition: transform .35s var(--ease); }
.archive .eps a:hover img { transform: rotate(-2deg) scale(1.06); }
.archive .eps .t { font: 900 clamp(17px, 1.5vw, 23px)/1.15 var(--slab); color: #1b1614; }
.archive .eps .t i { font-style: normal; color: #a3141a; padding: 0 .15em; }
.archive .eps .s { font: 700 13px var(--slab); color: #6c0d10; }
.archive .eps a:hover .t { color: #6c0d10; }
.archive::before, .archive::after { content: ""; position: absolute; top: -9px; width: 20px; height: 20px; border-radius: 50%; background: radial-gradient(circle at 35% 32%, #ff7a7a, #c3161d 50%, #5c070b); box-shadow: 0 5px 8px rgba(0, 0, 0, .55); }
.archive::before { left: 34px; }
.archive::after { right: 34px; }

/* ---------- Интро обложки + параллакс ---------- */
.anim .cover__bg { translate: 0 calc(var(--hp, 0) * 22vh); animation: heroBg 1.8s cubic-bezier(.2, .7, .2, 1) backwards; }
.anim .cover__logo { translate: 0 calc(var(--hp, 0) * 12vh); animation: heroLogo 1.1s cubic-bezier(.2, 1.5, .35, 1) .35s backwards, flicker .5s steps(1) .35s backwards; }
.anim .cover__fg { animation: heroFg 1.3s cubic-bezier(.16, 1, .3, 1) .55s backwards; }
.anim .cover__kicker { animation: rise .9s var(--ease) 1.05s backwards; }
.anim .cover__band { animation: band .9s cubic-bezier(.16, 1, .3, 1) 1.15s backwards; }
@keyframes heroBg { from { scale: 1.18; filter: blur(8px) brightness(.3); } }
@keyframes heroLogo { from { scale: 1.35; opacity: 0; } }
@keyframes flicker { 0% { opacity: 0; } 20% { opacity: 1; } 30% { opacity: .2; } 45% { opacity: 1; } 60% { opacity: .4; } 70% { opacity: 1; } }
@keyframes heroFg { from { translate: 0 8%; opacity: 0; } }
@keyframes rise { from { translate: 0 24px; opacity: 0; } }
@keyframes band { from { translate: 0 100%; } }

/* ---------- Появления по скроллу, у каждого ивента свой характер ---------- */
.anim .rv { opacity: 0; transition: opacity .7s var(--ease), transform .9s cubic-bezier(.16, 1, .3, 1), clip-path 1.1s cubic-bezier(.7, 0, .2, 1); transition-delay: calc(var(--i, 0) * 85ms); }
.anim .rv.in { opacity: 1; transform: none; }
.anim .rv[data-rv="up"] { transform: translateY(40px); }
.anim .rv[data-rv="side"] { transform: translateX(-46px); }
.anim .rv[data-rv="pop"] { transform: scale(.6) rotate(-4deg); transition-timing-function: var(--ease), cubic-bezier(.3, 1.8, .4, 1); }
.anim .rv[data-rv="stamp"] { transform: scale(1.7) rotate(-8deg); transition-duration: .35s, .55s; transition-timing-function: ease-out, cubic-bezier(.5, 0, .75, 0); }
.anim .rv[data-rv="stamp"].in { animation: shake .35s .5s; }
.anim .rv[data-rv="drop"] { transform: translateY(-90px) rotate(-12deg); transition-timing-function: var(--ease), cubic-bezier(.3, 1.45, .45, 1); }
.anim .rv[data-rv="slap"] { transform: scale(1.12) rotate(-4deg); transition-timing-function: ease-out, cubic-bezier(.3, 1.4, .45, 1); }
.anim .rv[data-rv="slam"] { transform: scale(1.9); transition-duration: .3s, .45s; transition-timing-function: ease-out, cubic-bezier(.55, 0, .8, .2); }
.anim .rv[data-rv="slam"].in { animation: shake .4s .42s; }
.anim .rv[data-rv="fly"] { transform: translate(120px, 40px) rotate(14deg); }
@keyframes shake { 20% { translate: -6px 3px; } 40% { translate: 5px -4px; } 60% { translate: -3px 2px; } 80% { translate: 2px -1px; } }
/* Св*бода: надпись проявляется мазком кисти, когда лист прилип */
.anim .sv__left .sv__title img { clip-path: inset(0 100% 0 0); transition: clip-path 1.2s cubic-bezier(.7, 0, .2, 1) .45s; }
.anim .sv__left.in .sv__title img { clip-path: inset(0 0 0 0); }
/* HUNT: красная нить в паре 1/4 натягивается слева направо */
.anim .bracket__list li i { display: inline-block; transform: scale(0); transition: transform .5s cubic-bezier(.3, 1.8, .4, 1) calc(var(--i, 0) * 85ms + .35s); }
.anim .bracket__list li.in i { transform: none; }

/* ---------- 3D-наклон шортсов ---------- */
.moment__frame { transform: perspective(900px) rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg)); transition: transform .4s var(--ease); transform-style: preserve-3d; }
.moment__frame:hover { transition-duration: .08s; }
.moment__frame::before { content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none; background: radial-gradient(circle at var(--gx, 50%) var(--gy, 0%), rgba(255, 255, 255, .22), transparent 45%); opacity: 0; transition: opacity .3s; }
.moment__frame:hover::before { opacity: 1; }
.moment__frame.is-on::before { display: none; }
'''

app = R / "app.js"
s = app.read_text()
if "// ---------- Анимации ----------" not in s:
    app.write_text(s.rstrip("\n") + "\n" + JS)
css = R / "style.css"
c = css.read_text()
if "Зерно по всему сайту" not in c:
    css.write_text(c.rstrip("\n") + "\n" + CSS)
h = R / "index.html"
t = h.read_text()
t = re.sub(r"style\.css\?v=\d+", "style.css?v=23", t)
t = re.sub(r"app\.js\?v=\d+", "app.js?v=17", t)
h.write_text(t)
print("ok")
