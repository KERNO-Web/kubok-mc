# v37: «Нет в наличии» на белой и оверсайз; схема зала — подписи влезают (судьи в рамке побольше, проход в круг дугой по кольцу)
import re
p='index.html'; s=open(p).read()
arts=[m.start() for m in re.finditer(r'<article class="tee" data-side="front">', s)]
assert len(arts)==3
# белая (1-я) и оверсайз (3-я): класс + штамп в кадре; идём с конца, чтобы не сбить позиции
for i in (2, 0):
    a=arts[i]
    s=s[:a]+'<article class="tee tee--sold" data-side="front">'+s[a+len('<article class="tee" data-side="front">'):]
    f=s.index('<div class="tee__frame">', a)+len('<div class="tee__frame">')
    s=s[:f]+'\n          <span class="tee__sold" aria-hidden="true"><b>Нет</b> в наличии</span>'+s[f:]
s=s.replace('style.css?v=71','style.css?v=72').replace('app.js?v=41','app.js?v=42')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
old='  <rect class="hall__fix" x="192" y="74" width="76" height="18"/>'
assert old in s
s=s.replace(old,'  <rect class="hall__fix" x="176" y="67" width="108" height="25"/>\n  <path id="hall-arc" d="M175 172A55 55 0 0 1 285 172" fill="none"/>')
old='<text x="230" y="118" class="sm">ПРОХОД В КРУГ</text>'
assert old in s
s=s.replace(old,'<text class="sm"><textPath href="#hall-arc" startOffset="50%">ПРОХОД В КРУГ</textPath></text>')
s=s.replace('<text x="230" y="87" class="sm dark">СУДЬИ</text>','<text x="230" y="84.5" class="sm dark">СУДЬИ</text>')
# мерч: распроданные — кнопка неактивна, в форме модель недоступна
old='$(".mo__tees", mo).innerHTML = "<legend>Модель</legend>" + tees.map((n, i) => `<label class="chip"><input type="radio" name="tee" value="${n}"${i ? "" : " checked"}><span>${n}</span></label>`).join("");'
assert old in s
s=s.replace(old,'''const sold = $$(".tee").map((t) => t.classList.contains("tee--sold"));
const firstFree = sold.indexOf(false);
$(".mo__tees", mo).innerHTML = "<legend>Модель</legend>" + tees.map((n, i) => `<label class="chip${sold[i] ? " chip--sold" : ""}"><input type="radio" name="tee" value="${n}"${sold[i] ? " disabled" : ""}${i === firstFree ? " checked" : ""}><span>${n}</span></label>`).join("");
$$(".tee--sold .tee__order").forEach((b) => { b.disabled = true; b.textContent = "Нет в наличии"; });''')
old='''  $("form", mo).reset();
  $$("input[name=tee]", mo)[i].checked = true;'''
assert old in s
s=s.replace(old,'''  $("form", mo).reset();
  $$("input[name=tee]", mo)[sold[i] ? firstFree : i].checked = true;''')
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s=s.replace('''  .hall text { font-size: 20px; }
  .hall text.sm { font-size: 15px; }
  .hall text.ring { font-size: 22px; }''','''  .hall text { font-size: 18px; }
  .hall text.sm { font-size: 14px; }
  .hall text.ring { font-size: 21px; }''')
marker='/* ============ v35 Мобилка по аудиту'
desk='''/* v37 Мерч: «Нет в наличии» — штамп-наклейка поверх кадра, футболка приглушена */
.tee__sold { position: absolute; z-index: 2; left: 50%; top: 50%; translate: -50% -50%; rotate: -12deg; display: grid; justify-items: center; padding: 10px 24px 9px; background: var(--noise), #efe9dd; color: #d0141c; box-shadow: inset 0 0 0 3px #d0141c, inset 0 0 0 6px #efe9dd, inset 0 0 0 8px #d0141c, 0 14px 30px -10px rgba(0, 0, 0, .8); font: 700 clamp(20px, 2vw, 30px)/1 var(--disp); text-transform: uppercase; letter-spacing: .1em; white-space: nowrap; pointer-events: none; }
.tee__sold b { font-size: 1.9em; line-height: .9; letter-spacing: .04em; }
.tee--sold .tee__img { filter: grayscale(.6) brightness(.72); }
.tee--sold .tee__order, .merch-zone .tee--sold .tee__order { background: transparent; color: #8a8178; box-shadow: inset 0 0 0 2px #c9bfae; cursor: not-allowed; }
.chip--sold { cursor: not-allowed; }
.chip--sold span { color: #a59d92; text-decoration: line-through 2px #d0141c; background: #ece6da; }
.chip--sold:hover span { box-shadow: inset 0 0 0 2px #d8cfc0; }
.hall path#hall-arc { stroke: none; }

'''
s=s.replace(marker, desk+marker,1)
open(p,'w').write(s)
