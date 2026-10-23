# v38: фильтры по сезонам — HUNT (виньетка + царапины на трёх глубинах), Св*бода (растр 60%), BTB (рассеивающаяся аберрация)
p='index.html'; s=open(p).read()
a='  <div class="event" id="event" data-skin="hunt">\n'
assert a in s
s=s.replace(a, a+'    <i class="fx-wood" aria-hidden="true"></i><i class="fx-top" aria-hidden="true"></i>\n',1)
a='  <section class="season sv" id="svoboda" data-skin="svoboda">\n'
assert a in s
s=s.replace(a, a+'    <i class="fx-dots" aria-hidden="true"></i>\n',1)
ca=''.join(f'''<filter id="ca-{k}" x="-4%" y="0" width="108%" height="100%" color-interpolation-filters="sRGB"><feColorMatrix in="SourceGraphic" values="1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0" result="r"/><feOffset in="r" dx="1.2" result="r2"/><feColorMatrix in="SourceGraphic" values="0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0" result="g"/><feColorMatrix in="SourceGraphic" values="0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0" result="b"/><feOffset in="b" dx="-1.2" result="b2"/><feBlend in="r2" in2="g" mode="screen" result="rg"/><feBlend in="rg" in2="b2" mode="screen"/></filter>''' for k in ('title','poster','tiles','moments','krug'))
a='<script src="app.js'
s=s.replace(a, f'<div class="fx-vig" aria-hidden="true"></div>\n<svg class="fx-defs" width="0" height="0" aria-hidden="true">{ca}</svg>\n'+a,1)
s=s.replace('style.css?v=73','style.css?v=74').replace('app.js?v=43','app.js?v=44')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
s+='''
// v38 Фильтры сезонов. HUNT: виньетка по краям экрана, пока HUNT в кадре (только ПК)
{
  const vig = $(".fx-vig"), ev = $("#event");
  if (vig && ev) new IntersectionObserver(([e]) => vig.classList.toggle("on", e.isIntersecting && e.intersectionRatio > .12), { threshold: [0, .12, .3] }).observe(ev);
}
// BTB: хроматическая аберрация — при появлении блока каналы разъехались и оседают до едва заметной (на телефоне сразу слабая)
{
  const groups = { title: ".btb__title", poster: ".btb .season__poster", tiles: ".btb .tiles", moments: ".moments--btb", krug: ".krug--btb" };
  const animate = !touchUI.matches && !matchMedia("(prefers-reduced-motion: reduce)").matches;
  const setDx = (id, dx) => { const offs = document.querySelectorAll(`#ca-${id} feOffset`); offs[0].setAttribute("dx", dx.toFixed(2)); offs[1].setAttribute("dx", (-dx).toFixed(2)); };
  Object.entries(groups).forEach(([id, sel]) => {
    const el = $(sel);
    if (!el) return;
    if (!animate) { setDx(id, .9); return; }
    setDx(id, 8);
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      const t0 = performance.now(), D = 1300;
      const step = (t) => { const k = Math.min(1, (t - t0) / D), ease = 1 - Math.pow(1 - k, 3); setDx(id, 8 - (8 - 1.2) * ease); if (k < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }, { threshold: .25 });
    io.observe(el);
  });
}
'''
open(p,'w').write(s)

p='style.css'; s=open(p).read()
marker='/* ============ v35 Мобилка по аудиту'
desk='''/* ============ v38 Фильтры сезонов (Сергей выбрал на стенде .work/fx/compare.html) ============ */
/* HUNT — пыль и царапины на трёх глубинах: дерево (под всем), часть бумаги и фото (вразнобой), редкие поверх всего (только ПК) */
.fx-wood, .fx-top { position: absolute; inset: 0; pointer-events: none; }
.fx-wood { z-index: -1; background: url("assets/fx/scratch-wood.svg") 0 0 / 1100px; }
.fx-top { z-index: 6; background: url("assets/fx/scratch-top.svg") 300px 200px / 1500px; opacity: .8; }
.pol::after, .moments--hunt .moment::after, .krug--hunt .krug__ph::after, .bracket__list li::after, .extra__view::after, .ev-head__date::after, .tag::after { content: ""; position: absolute; inset: 0; z-index: 3; pointer-events: none; background: url("assets/fx/scratch-paper.svg") 0 0 / 620px; }
.bracket__list li, .tag { position: relative; }
/* вразнобой: у разных элементов разные куски царапин, у части их нет совсем */
.moments--hunt .moment:nth-child(2n)::after, .krug--hunt .krug__ph:nth-child(3n + 1)::after { background-position: -230px -140px; }
.moments--hunt .moment:nth-child(3n)::after, .krug--hunt .krug__ph:nth-child(4n)::after, .bracket__list li:nth-child(2n)::after { background-position: -410px -360px; }
.moments--hunt .moment:nth-child(4)::after, .krug--hunt .krug__ph:nth-child(5n + 2)::after, .bracket__list li:nth-child(3)::after, .tag:nth-of-type(2n)::after, .pol--c::after { content: none; }
.extra__view::after { background-position: -120px -300px; }
/* HUNT — виньетка по краям экрана, пока HUNT в кадре */
.fx-vig { position: fixed; inset: 0; z-index: 40; pointer-events: none; opacity: 0; transition: opacity .7s ease; background: radial-gradient(115% 90% at 50% 45%, transparent 42%, rgba(0, 0, 0, .5) 76%, rgba(0, 0, 0, .8) 100%); }
.fx-vig.on { opacity: 1; }
.fx-defs { position: absolute; width: 0; height: 0; overflow: hidden; }

/* Св*бода — растр печати на 60% силы: на стене, на листе-афише и на фото */
.sv { --dots: radial-gradient(rgba(0, 0, 0, .55) 32%, transparent 36%) 0 0 / 4px 4px; }
.sv > .fx-dots { position: absolute; inset: 0; z-index: 0; pointer-events: none; background: var(--dots); opacity: .3; }
.sv__left, .sv .tile, .moments--svoboda .moment { position: relative; }
.sv__left::after, .sv .tile::after, .moments--svoboda .moment::after, .krug--svoboda .krug__ph::after { content: ""; position: absolute; inset: 0; z-index: 2; pointer-events: none; background: var(--dots); opacity: .21; }
.sv .tile::after { bottom: auto; aspect-ratio: 16 / 9; }
.sv .tile img, .moments--svoboda .moment__frame img, .krug--svoboda .krug__ph img { filter: contrast(1.15) saturate(.91); }

/* BTB — хроматическая аберрация (смещение каналов анимирует app.js) */
.btb__title img { filter: url("#ca-title") drop-shadow(0 14px 28px rgba(0, 0, 0, .75)); }
.btb .season__poster { filter: url("#ca-poster"); }
.btb .tile img { filter: url("#ca-tiles"); }
.moments--btb .moment__frame img { filter: url("#ca-moments") contrast(1.08) saturate(.9); }
.krug--btb .krug__ph img { filter: url("#ca-krug"); }

'''
s=s.replace(marker, desk+marker,1)
s+='''
/* v38 на тач-экранах: ничего поверх лент HUNT (виньетка и верхние царапины только на ПК), виньетка — на самих фото */
@media (hover: none) {
  .fx-vig, .fx-top { display: none; }
  .pol::after, .moments--hunt .moment::after, .krug--hunt .krug__ph::after { background: url("assets/fx/scratch-paper.svg") 0 0 / 620px, radial-gradient(120% 110% at 50% 45%, transparent 50%, rgba(20, 10, 4, .45) 100%); }
}
'''
open(p,'w').write(s)
