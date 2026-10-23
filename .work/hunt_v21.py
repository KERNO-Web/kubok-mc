# v21 HUNT: шапка из живых полароидов на новом дереве, Main Event, ники, нитки-крест, новые названия блоков
import re
p='index.html'; s=open(p).read()

wall=lambda side, items: f'<div class="wall wall--{side}" aria-hidden="true"><div class="wall__in">' + ''.join(items) + '</div></div>'
pol=lambda cls, n: f'<figure class="pol {cls}"><img src="assets/krug/hunt/{n}.jpg" alt="" loading="lazy"></figure>'
scrap=lambda cls: f'<i class="scrap {cls}"></i>'
L=wall('l',[scrap('scrap--a'), pol('pol--a','01'), scrap('scrap--lined'), pol('pol--b','03')])
R=wall('r',[pol('pol--c','04'), scrap('scrap--b'), pol('pol--d','02'), scrap('scrap--c')])
old='    <section class="ev-head">\n      <div class="ev-head__in">'
assert old in s
s=s.replace(old,'    <section class="ev-head">\n      '+L+'\n      '+R+'\n      <div class="ev-head__in">',1)

s=s.replace('<h2 class="tag">Вне турнира</h2>','<h2 class="tag">Main Event</h2>')
caps={
 '<figcaption><b>Main event. Gokilla vs Zeiman</b> Бишкек против Воронежа</figcaption>':'<figcaption><b>Gokilla vs Zeiman</b></figcaption>',
 '<figcaption><b>Main event. Микси vs .OTRIX</b> Селенгинск против Краснодара</figcaption>':'<figcaption><b>Микси vs .OTRIX</b></figcaption>',
 '<figcaption><b>Main event. Ями vs Кения</b> Воронеж против Лениногорска</figcaption>':'<figcaption><b>Ями vs Кения</b></figcaption>',
 '<figcaption><b>Deathmatch Clash</b> Пятеро в&nbsp;одном круге: Hidji 17, Мишарик, Молодой Казах, МЦ Доналдас, Kumska</figcaption>':'<figcaption><b>Deathmatch Clash</b> Hidji 17, Мишарик, Молодой Казах, МЦ Доналдас, Kumska</figcaption>',
 '<figcaption><b>Afterparty</b> Бар БТК, проспект Мира 102к1, 18+ <button':'<figcaption><b>Afterparty</b> <button',
}
for a,b in caps.items():
    assert a in s, a; s=s.replace(a,b)
s=s.replace('<span class="tag">Моменты <small>1/8 финала</small></span>','<span class="tag">Лучшие моменты <small>1/8 финала</small></span>')
s=s.replace('<span class="tag">Из круга <small>','<span class="tag">Фото с баттлов <small>')
for c in ('moments__pill','moments__plate'):
    s=s.replace(f'<span class="{c}">Моменты</span>',f'<span class="{c}">Лучшие моменты</span>')
    s=s.replace(f'<span class="{c}">Из круга</span>',f'<span class="{c}">Фото с баттлов</span>')
assert 'Из круга' not in s and '>Моменты' not in s
s=s.replace('style.css?v=35','style.css?v=36').replace('app.js?v=24','app.js?v=25')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
old='if (huntKrug) stringUp(huntKrug, ".krug__row", ".krug__ph");'
assert old in s
s=s.replace(old, old+'\n// шапка HUNT: полароиды и бумажки на стене связаны ниткой, у каждой стены своя\n$$(".ev-head .wall").forEach((w) => stringUp(w, ".wall__in", ".pol, .scrap"));')
s=s.replace('// Карусель «Вне турнира»','// Карусель «Main Event»').replace('// Карусели «Из круга»','// Карусели «Фото с баттлов»')
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''
/* v21 HUNT: шапка без картинки-доски — живые полароиды с фото HUNT и бумажки на том же дереве, шва нет */
.ev-head::before { background: linear-gradient(#0c0a09 10px, rgba(12, 10, 9, 0) 200px), radial-gradient(42% 50% at 50% 48%, rgba(14, 8, 4, .5), transparent 75%); }
.ev-head__in { position: relative; z-index: 4; }
.wall { position: absolute; top: clamp(70px, 8vh, 100px); bottom: 20px; width: min(31vw, 470px); z-index: 2; pointer-events: none; }
.wall--l { left: 0; }
.wall--r { right: 0; }
.wall__in { display: contents; }
.wall .thr-layer { z-index: 3; }
.pol { position: absolute; width: clamp(170px, 15.5vw, 250px); padding: 11px 11px 40px; background: url("assets/paper-tex.jpg") 0 0 / 512px; box-shadow: inset 0 0 14px rgba(95, 60, 25, .4), 0 22px 34px -12px rgba(0, 0, 0, .9); }
.pol img { display: block; width: 100%; aspect-ratio: 1; object-fit: cover; filter: sepia(.22) contrast(1.08) brightness(.9); box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .3); }
.pol--a { left: 9%; top: 2%; rotate: -7deg; }
.pol--b { left: 40%; top: 46%; rotate: 5deg; background-position: -200px -150px; }
.pol--c { right: 10%; top: 0; rotate: 6deg; background-position: -320px -60px; }
.pol--d { right: 38%; top: 47%; rotate: -4deg; background-position: -90px -300px; }
.pol--a img { object-position: 40% 50%; }
.scrap { position: absolute; display: block; background: url("assets/paper-tex.jpg") 0 0 / 512px; box-shadow: inset 0 0 16px rgba(95, 60, 25, .5); filter: drop-shadow(0 12px 14px rgba(0, 0, 0, .7)); -webkit-mask: var(--torn) 0 0 / 100% 100%; mask: var(--torn) 0 0 / 100% 100%; }
.scrap--a { left: -2%; top: 30%; width: 46%; height: 24%; rotate: 8deg; background-position: -140px -40px; }
.scrap--lined { left: 4%; top: 62%; width: 44%; height: 30%; rotate: -3deg; background: repeating-linear-gradient(transparent 0 21px, rgba(70, 90, 120, .28) 21px 22px), linear-gradient(90deg, transparent 13%, rgba(170, 40, 40, .35) 13% calc(13% + 1.5px), transparent 0), url("assets/paper-tex.jpg") -260px -200px / 512px; }
.scrap--b { right: 0; top: 33%; width: 48%; height: 20%; rotate: -6deg; background-position: -380px -280px; }
.scrap--c { right: 4%; top: 74%; width: 34%; height: 18%; rotate: 9deg; background-position: -40px -420px; }
@media (max-width: 1100px) { .wall { width: 24vw; } .pol { width: 15vw; padding: 7px 7px 24px; } }
@media (max-width: 900px) { .wall { display: none; } }

/* Main Event: под картинкой только ники */
.slide figcaption b { width: auto; }

/* Пропали без вести: крест из красной нитки вместо линий */
.gone img { filter: sepia(.25) contrast(1.05) brightness(.85); }
.gone figure::before, .gone figure::after { left: -8%; right: -8%; top: calc(50% - 22px); height: 14px; background: url("assets/thread.png") 0 50% / auto 14px repeat-x; filter: drop-shadow(0 4px 2px rgba(0, 0, 0, .6)); }
.gone figcaption { text-decoration: none; color: #ebe3d4; }

/* Фото с баттлов HUNT: крупнее, рамка полароида шире, место до затемнения */
.krug--hunt .krug__row { --h: clamp(280px, 31vw, 470px); }
.krug--hunt .krug__ph { padding: 12px 12px 44px; }
.krug--hunt .krug__ph img { height: calc(var(--h) - 56px); }
.moments--hunt + .krug { padding-bottom: clamp(90px, 9vw, 150px); }
'''
open(p,'w').write(s)
