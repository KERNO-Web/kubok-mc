# v36: Main Event — крупная подпись пары по центру, VS красным; Св*бода — фон просвечивает под видео; организаторы не моргают на телефоне
p='style.css'; s=open(p).read()
marker='/* ============ v35 Мобилка по аудиту'
assert marker in s
desk='''/* v36 Main Event: пара крупно и по центру, VS красным (оборачивает app.js) */
.extra__view .slide figcaption { flex-direction: column; justify-content: center; gap: 6px; padding: 16px 8px 20px; text-align: center; }
.extra__view .slide figcaption b { width: 100%; font: 900 clamp(28px, 3vw, 48px)/1 var(--slab); letter-spacing: .01em; }
.extra__view .slide figcaption b i { font-style: normal; color: #b3121a; padding: 0 .18em; }
.extra__view .slide figcaption .btn { margin: 6px auto 0; }

/* v36 Св*бода: стена видна на всю высоту блока, карточки полупрозрачные */
.sv::before { background: linear-gradient(#0c0a09, rgba(12, 10, 9, .55) 120px, rgba(12, 10, 9, 0) 320px), linear-gradient(transparent 88%, #0c0a09 100%), image-set(url("assets/svoboda-street.webp") 1x, url("assets/svoboda-street-2x.jpg") 2x) 50% 0 / cover no-repeat; filter: blur(3px) brightness(.62); }
.sv .tile { background: rgba(10, 9, 12, .55); }

'''
s=s.replace(marker, desk+marker,1)
s+='''
/* v36 Тач-экраны: наведение не срабатывает от пальца при прокрутке — организаторы не моргают цветом */
@media (hover: none) {
  .org:hover .org__ph.org__ph--a { opacity: 1 !important; scale: 1; }
  .org:hover .org__ph--b { opacity: 0; }
  .ofr:hover img { scale: 1; filter: grayscale(1) contrast(1.1) brightness(.88); }
  .ofr:not(.ofr--cut):hover img { filter: grayscale(1) contrast(1.08) brightness(1.25); }
  .ofr:hover::after { box-shadow: inset 0 0 0 2px rgba(255, 255, 255, .08); }
}
@media (max-width: 767px) {
  .sv::before { inset: 0; filter: blur(2px) brightness(.6); }
}
'''
open(p,'w').write(s)

p='app.js'; s=open(p).read()
s+='''
// Main Event: «vs» в подписи пары — красным
$$(".slide figcaption b").forEach((b) => { b.innerHTML = b.textContent.replace(/ vs /i, " <i>vs</i> "); });
'''
open(p,'w').write(s)
p='index.html'; s=open(p).read(); s=s.replace('style.css?v=69','style.css?v=70').replace('app.js?v=40','app.js?v=41'); open(p,'w').write(s)
