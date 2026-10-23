# v25: фон нижней части = стена ч/б кадров толпы с баттлов; организаторы: вырезка на фоне толпы, белый ник снизу, досье 2x2 крупных квадратных фото
import re
p='index.html'; s=open(p).read()
pics=[('svoboda',13),('btb',17),('svoboda',12),('btb',14),('svoboda',7),('btb',11),('svoboda',9),('btb',16),('svoboda',17),('btb',4),('svoboda',6),('btb',9)]
wall=''.join(f'<img src="assets/krug/{k}/{n:02d}.jpg" alt="" loading="lazy">' for k,n in pics)
old='<div class="lower__bg" aria-hidden="true"></div>'
assert old in s
s=s.replace(old,f'<div class="lower__bg" aria-hidden="true">{wall}</div>')
s=s.replace('style.css?v=44','style.css?v=45').replace('app.js?v=27','app.js?v=28')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
s,n=re.subn(r'const ORG = \{.*?\};', 'const ORG = {"h": [["h-01", 0], ["h-02", 0], ["h-03", 0], ["h-08", 0]], "p": [["p-01", 0], ["p-02", 0], ["p-04", 0], ["p-06", 0]]};', s, count=1, flags=re.S)
assert n==1
s=s.replace('// Организаторы: досье из 8 фото под каждым (вырезки на красном, фото ч/б), клик открывает просмотр','// Организаторы: по 4 крупных квадратных фото под каждым, ч/б, клик открывает просмотр')
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''
/* v25 Фон нижней части: стена ч/б кадров толпы с их баттлов (не чёрный), стоит на месте */
.lower__bg { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); grid-auto-rows: calc(100vh / 3); gap: 4px; overflow: hidden; background: #0c0a09; filter: none; }
.lower__bg img { width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) contrast(1.1) brightness(.5); }
.lower__bg::before { content: ""; position: absolute; inset: 0; z-index: 1; background: linear-gradient(#0c0a09, rgba(12, 10, 9, .25) 22%, rgba(12, 10, 9, .25) 80%, rgba(12, 10, 9, .7)), radial-gradient(70% 60% at 50% 50%, transparent 40%, rgba(12, 10, 9, .55)); }
.lower__bg::after { z-index: 2; opacity: .25; }

/* Организаторы v25: без красного ника — человек на фоне толпы, белый ник снизу как подписи на их обложках */
.org__stage { background: linear-gradient(transparent 55%, rgba(12, 10, 9, .85)), rgba(12, 10, 9, .35); box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .08); }
.org__stage .org__name { inset: auto auto 4% 5%; top: auto; z-index: 2; font-size: 11cqw; line-height: .86; color: #fff; text-align: left; transform: skewX(-8deg); transform-origin: left bottom; text-shadow: 0 6px 24px rgba(0, 0, 0, .7); }
.org .org__ph { height: 94%; filter: grayscale(1) contrast(1.12) drop-shadow(0 0 50px rgba(0, 0, 0, .75)); }
.org:nth-child(2) .org__stage .org__name { top: auto; }
.org__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.ofr { box-shadow: 0 20px 36px -18px rgba(0, 0, 0, .9); }
'''
open(p,'w').write(s)
