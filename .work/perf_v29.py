# v29: параллакс обложки на CSS scroll-timeline (без отставания от прокрутки), зерно без mix-blend,
# пульс фото организаторов = цветная копия с opacity, старт анимации привязан к фону; мерч — отдельный светлый блок
p='style.css'; s=open(p).read()
s+='''
/* v29 Производительность: зерно без смешивания цветов (иначе вся страница перерисовывается на каждом кадре прокрутки) */
body::after, .cover::after, .event::after, .lower__bg::after, .org__stage::after { mix-blend-mode: normal; will-change: transform; }
.mast.is-solid { backdrop-filter: none; -webkit-backdrop-filter: none; background: rgba(12, 10, 9, .94); }

/* Параллакс обложки при прокрутке: в браузерах со scroll-timeline двигает сам CSS, синхронно со скроллом */
@supports (animation-timeline: scroll()) {
  .anim .cover__bg, .anim .cover__fg { translate: calc(var(--mx, 0) * 10px) calc(var(--my, 0) * 8px); animation: coverDown linear both, heroBg 1.8s cubic-bezier(.2, .7, .2, 1) backwards; animation-timeline: scroll(root), auto; animation-range: 0 100vh, normal; }
  .anim .cover__fg { translate: calc(var(--mx, 0) * 22px) calc(var(--my, 0) * 12px); }
  .anim .cover__logo { translate: calc(var(--mx, 0) * -26px) calc(var(--my, 0) * -18px); scale: 1; opacity: 1; animation: coverLogoUp linear both, heroLogo 1.1s cubic-bezier(.2, 1.5, .35, 1) .35s backwards, flicker .5s steps(1) .35s backwards; animation-timeline: scroll(root), auto, auto; animation-range: 0 100vh, normal, normal; }
  @keyframes coverDown { to { transform: translateY(26vh); } }
  @keyframes coverLogoUp { to { transform: translateY(-34vh) scale(1.18); opacity: 0; } }
}

/* Пульс фото организаторов: серая база статична, поверх цветная копия плавно проявляется (opacity — без рывков) */
.org .org__ph--a, .ofr img, .ofr--cut img { animation: none; filter: grayscale(1) contrast(1.1) brightness(.62); }
.org .org__ph--a.pc, .ofr img.pc { filter: saturate(1.15) contrast(1.05); opacity: 0; animation: orgCol 7s ease-in-out infinite; }
@keyframes orgCol { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
.ofr:hover img.pc { animation: none; opacity: 1; }
.ofr:hover img { scale: 1.06; }
@media (prefers-reduced-motion: reduce) { .org .org__ph--a.pc, .ofr img.pc { animation: none; opacity: .4; } }

/* v29 Мерч — отдельный светлый блок-лукбук: бетон/бумага, огромный КУБОК МЦ водяным знаком, бирки на футболках */
.merch-zone { position: relative; overflow: hidden; isolation: isolate; background: radial-gradient(70% 90% at 80% 0%, rgba(255, 255, 255, .55), transparent 60%), var(--noise), #e4ded3; color: #141110; }
.merch-zone::before { content: ""; position: absolute; z-index: -1; right: -6vw; top: 50%; translate: 0 -50%; width: 62vw; aspect-ratio: 336 / 271; background: url("assets/logo-ink.svg") center / contain no-repeat; opacity: .07; rotate: -8deg; }
.merch-zone::after { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 14px; background: repeating-linear-gradient(90deg, #141110 0 26px, var(--accent) 26px 52px); }
.merch-zone .merch { padding-top: clamp(64px, 6vw, 96px); padding-bottom: clamp(64px, 6vw, 96px); }
.merch-zone .merch__head h2 { color: #141110; font-size: clamp(64px, 8vw, 132px); line-height: .85; }
.merch-zone .merch__demo { background: #fff; }
.merch-zone .tee__frame { box-shadow: 0 30px 50px -26px rgba(20, 17, 16, .7); }
.merch-zone .tee__bar { position: relative; margin-top: -26px; margin-left: 14px; margin-right: 14px; padding: 16px 18px 12px 34px; background: #fff; border: 0; box-shadow: 0 10px 22px -12px rgba(20, 17, 16, .5); rotate: -1deg; }
.merch-zone .tee__bar::before { content: ""; position: absolute; left: 13px; top: 50%; width: 10px; height: 10px; margin-top: -5px; border-radius: 50%; background: #e4ded3; box-shadow: inset 0 1px 2px rgba(0, 0, 0, .4); }
.merch-zone .tee:nth-child(2) .tee__bar { rotate: .8deg; }
.merch-zone .tee__name { color: #141110; }
.merch-zone .tee__flip { box-shadow: inset 0 0 0 2px #141110; }
.merch-zone .tee__flip button { color: #6b625b; }
.merch-zone .tee__flip button[aria-pressed="true"] { background: #141110; color: #fff; }
.merch-zone .tee__note { color: #5a524c; padding: 0 14px; }
.merch-zone .tee__order { width: calc(100% - 28px); margin: 12px 14px 0; background: #141110; }
.merch-zone .tee__order:hover { background: var(--accent); color: #fff; }
'''
open(p,'w').write(s)

p='app.js'; s=open(p).read()
# JS-параллакс прокрутки только там, где нет scroll-timeline
old='  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(hero); } }, { passive: true });\n  hero();'
assert old in s
s=s.replace(old,'  if (!CSS.supports("animation-timeline: scroll()")) {\n    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(hero); } }, { passive: true });\n    hero();\n  }')
s+='''
// Пульс цвета у фото организаторов: цветная копия поверх серой, время анимации = время цветного слоя фона
{
  const bgAnim = document.querySelector(".lw--col")?.getAnimations()[0];
  $$(".org .org__ph--a, .ofr img").forEach((img) => {
    const c = img.cloneNode();
    c.classList.add("pc");
    c.alt = "";
    img.after(c);
    const a = c.getAnimations()[0];
    if (a && bgAnim) a.startTime = bgAnim.startTime;
  });
}
'''
open(p,'w').write(s)

p='index.html'; s=open(p).read()
# мерч вынести из .lower в свой блок
i=s.index('  <!-- КАРКАС. Мерч') if '  <!-- КАРКАС. Мерч' in s else s.index('  <section class="merch"')
j=s.index('  </div>\n\n  <footer class="final"')
merch=s[i:j]
s=s[:i]+'  </div>\n\n  <div class="merch-zone">\n'+merch+'  </div>\n\n  <footer class="final"'+s[j+len('  </div>\n\n  <footer class="final"'):]
s=s.replace('style.css?v=54','style.css?v=55').replace('app.js?v=32','app.js?v=33')
open(p,'w').write(s)
