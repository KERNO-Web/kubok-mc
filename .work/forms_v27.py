# v27: «Купить билет» -> попап выбора (форма сайта / Bibilet), своя форма билета, форма заказа мерча
p='index.html'; s=open(p).read()
dialogs='''<dialog class="buy" aria-labelledby="buy-title">
  <button class="buy__x" aria-label="Закрыть">✕</button>
  <div class="buy__stub">
    <p class="buy__kicker">Кубок МЦ</p>
    <h2 id="buy-title" class="buy__title"></h2>
    <p class="buy__meta"></p>
  </div>
  <div class="buy__step buy__step--pick">
    <button class="buy__opt buy__opt--site" data-go="form">
      <span class="buy__badge">Специально для сайта</span>
      <b>Купить на сайте</b>
      <i>Пара полей и билет у вас на почте</i>
    </button>
    <button class="buy__opt" data-go="bibilet">
      <b>Через Bibilet</b>
      <i>Официальная касса Кубка</i>
    </button>
  </div>
  <form class="buy__step buy__step--form" novalidate>
    <fieldset class="buy__cats"></fieldset>
    <div class="buy__qty"><span>Билетов</span><button type="button" data-q="-1" aria-label="Меньше">−</button><output>1</output><button type="button" data-q="1" aria-label="Больше">+</button></div>
    <label class="fld"><span>Имя</span><input name="name" autocomplete="name" required></label>
    <label class="fld"><span>Телефон или Telegram</span><input name="contact" required placeholder="+7 … или @ник"></label>
    <label class="fld"><span>Почта для билета</span><input name="email" type="email" autocomplete="email" required></label>
    <div class="buy__sum"><span>Итого</span><b class="buy__total"></b></div>
    <button class="btn btn--accent buy__go" type="submit">Перейти к оплате</button>
    <p class="buy__note">Демо-форма концепта: цены условные, данные никуда не отправляются.</p>
  </form>
  <div class="buy__step buy__step--done">
    <p class="buy__ok">Бронь создана</p>
    <p class="buy__done-text"></p>
    <button class="btn btn--ink buy__close" type="button">Готово</button>
  </div>
</dialog>
<dialog class="buy buy--merch" aria-labelledby="mo-title">
  <button class="buy__x" aria-label="Закрыть">✕</button>
  <div class="buy__stub">
    <p class="buy__kicker">Мерч Кубка МЦ</p>
    <h2 id="mo-title" class="buy__title">Заказ футболки</h2>
    <p class="buy__meta">Свяжемся, подтвердим размер и оплату</p>
  </div>
  <form class="buy__step buy__step--form" novalidate>
    <fieldset class="mo__tees"></fieldset>
    <fieldset class="mo__sizes"><legend>Размер</legend></fieldset>
    <label class="fld"><span>Имя</span><input name="name" autocomplete="name" required></label>
    <label class="fld"><span>Контакт для связи</span><input name="contact" required placeholder="Telegram, телефон или почта"></label>
    <button class="btn btn--accent buy__go" type="submit">Оформить заказ</button>
    <p class="buy__note">Демо-форма концепта: данные никуда не отправляются.</p>
  </form>
  <div class="buy__step buy__step--done">
    <p class="buy__ok">Заказ принят</p>
    <p class="buy__done-text"></p>
    <button class="btn btn--ink buy__close" type="button">Готово</button>
  </div>
</dialog>
'''
anchor='<dialog class="drawer"'
assert anchor in s
s=s.replace(anchor, dialogs+anchor,1)
# кнопка «Заказать» у каждой футболки
old='<p class="tee__note">'
assert s.count(old)==3
s=s.replace(old,'<button class="tee__order" type="button">Заказать</button>\n        <p class="tee__note">')
s=s.replace('style.css?v=47','style.css?v=48').replace('app.js?v=30','app.js?v=31')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
old='''$$("[data-ticket]").forEach((b) => b.addEventListener("click", () => {
  const t = TICKETS[b.dataset.ticket];'''
new='''const openBibilet = (key) => {
  const t = TICKETS[key];'''
assert old in s; s=s.replace(old,new)
old2='''  if (frame.src !== t.url) { dlg.classList.remove("loaded"); frame.src = t.url; }
  dlg.showModal();
}));'''
new2='''  if (frame.src !== t.url) { dlg.classList.remove("loaded"); frame.src = t.url; }
  dlg.showModal();
};'''
assert old2 in s; s=s.replace(old2,new2)
s+='''
// Билеты: сначала попап выбора — своя форма сайта или касса Bibilet
const CATS = {
  quarter: [["dance", "Танцпол", "Стоя у круга", 1500], ["ring", "Первый ряд", "Вплотную к баттлерам", 2500]],
  after: [["entry", "Вход", "Бар БТК, 22:30, 18+", 500]],
};
const rub = (n) => n.toLocaleString("ru-RU") + "\\u00a0₽";
const buy = $(".buy:not(.buy--merch)");
let buyKey = "quarter", qty = 1;
const step = (d, name) => { d.dataset.step = name; };
const total = () => {
  const c = $("input[name=cat]:checked", buy);
  $(".buy__total", buy).textContent = rub((c ? Number(c.dataset.price) : 0) * qty);
  $(".buy__qty output", buy).textContent = qty;
};
$$("[data-ticket]").forEach((b) => b.addEventListener("click", () => {
  buyKey = b.dataset.ticket; qty = 1;
  const t = TICKETS[buyKey];
  $(".buy__title", buy).textContent = t.title;
  $(".buy__meta", buy).textContent = t.meta;
  $(".buy__cats", buy).innerHTML = "<legend>Билет</legend>" + CATS[buyKey].map(([v, n, d, p], i) => `
    <label class="cat"><input type="radio" name="cat" value="${v}" data-price="${p}"${i ? "" : " checked"}><span><b>${n}</b><i>${d}</i></span><em>${rub(p)}</em></label>`).join("");
  $("form", buy).reset();
  $$("input[name=cat]", buy)[0].checked = true;
  total();
  step(buy, "pick");
  buy.showModal();
}));
$$("[data-go]", buy).forEach((b) => b.addEventListener("click", () => {
  if (b.dataset.go === "bibilet") { buy.close(); openBibilet(buyKey); return; }
  step(buy, "form");
  $("input[name=name]", buy).focus();
}));
$(".buy__cats", buy).addEventListener("change", total);
$$("[data-q]", buy).forEach((b) => b.addEventListener("click", () => { qty = Math.max(1, Math.min(10, qty + Number(b.dataset.q))); total(); }));

// общая отправка демо-форм: проверка полей и экран «готово»
const demoForm = (d, done) => {
  $("form", d).addEventListener("submit", (e) => {
    e.preventDefault();
    const bad = $$("input[required]", d).filter((i) => !i.checkValidity());
    $$(".fld", d).forEach((f) => f.classList.toggle("is-bad", bad.includes($("input", f))));
    if (bad.length) { bad[0].focus(); return; }
    $(".buy__done-text", d).textContent = done(new FormData(e.target));
    step(d, "done");
  });
  $(".buy__x", d).addEventListener("click", () => d.close());
  $(".buy__close", d).addEventListener("click", () => d.close());
  d.addEventListener("click", (e) => { if (e.target === d) d.close(); });
};
demoForm(buy, (f) => {
  const c = $("input[name=cat]:checked", buy);
  return `${f.get("name")}, ${c.closest(".cat").querySelector("b").textContent.toLowerCase()} × ${qty} на ${rub(Number(c.dataset.price) * qty)}. Билет придёт на ${f.get("email")}. В рабочей версии здесь откроется оплата.`;
});

// Мерч: заказ футболки — модель, размер, имя, контакт
const mo = $(".buy--merch");
const tees = $$(".tee").map((t) => $(".tee__name", t).textContent);
$(".mo__tees", mo).innerHTML = "<legend>Модель</legend>" + tees.map((n, i) => `<label class="chip"><input type="radio" name="tee" value="${n}"${i ? "" : " checked"}><span>${n}</span></label>`).join("");
$(".mo__sizes", mo).insertAdjacentHTML("beforeend", ["S", "M", "L", "XL", "XXL"].map((z) => `<label class="chip"><input type="radio" name="size" value="${z}"${z === "L" ? " checked" : ""}><span>${z}</span></label>`).join(""));
$$(".tee").forEach((t, i) => $(".tee__order", t).addEventListener("click", () => {
  $("form", mo).reset();
  $$("input[name=tee]", mo)[i].checked = true;
  step(mo, "form");
  mo.showModal();
}));
demoForm(mo, (f) => `${f.get("name")}, футболка «${f.get("tee")}», размер ${f.get("size")}. Напишем вам: ${f.get("contact")}.`);
'''
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''
/* v27 Попап покупки (выбор: форма сайта / Bibilet) и заказ мерча — билет с перфорацией */
.buy { width: min(520px, calc(100vw - 24px)); max-height: calc(100dvh - 24px); margin: auto; padding: 0; border: 0; overflow: auto; background: #f1ebde; color: #161211; box-shadow: 0 40px 80px -20px rgba(0, 0, 0, .9); }
.buy[open] { animation: buyIn .35s var(--ease); }
@keyframes buyIn { from { opacity: 0; translate: 0 24px; scale: .97; } }
.buy::backdrop { background: rgba(5, 4, 4, .78); backdrop-filter: blur(4px); }
.buy__x { position: absolute; top: 12px; right: 12px; z-index: 2; width: 40px; height: 40px; color: #fff; font-size: 18px; }
.buy__x:hover { background: rgba(255, 255, 255, .15); }
.buy__stub { position: relative; padding: 26px 28px 30px; background: var(--accent); color: #fff; }
.buy__stub::after { content: ""; position: absolute; left: 14px; right: 14px; bottom: -1px; height: 2px; background: repeating-linear-gradient(90deg, #f1ebde 0 8px, transparent 8px 14px); }
.buy__stub::before { content: ""; position: absolute; left: -12px; right: -12px; bottom: -12px; height: 24px; background: radial-gradient(circle at 12px 12px, #050404 11px, transparent 12px) 0 0 / 100% 24px no-repeat, radial-gradient(circle at calc(100% - 12px) 12px, #050404 11px, transparent 12px) 0 0 / 100% 24px no-repeat; }
.buy__kicker { font: 700 14px/1 var(--disp); text-transform: uppercase; letter-spacing: .14em; opacity: .8; }
.buy__title { margin-top: 10px; padding-right: 30px; font: 700 clamp(28px, 4vw, 36px)/.95 var(--disp); text-transform: uppercase; }
.buy__meta { margin-top: 8px; font: 500 16px/1.3 var(--text); opacity: .9; }
.buy__step { display: none; padding: 26px 28px 28px; }
.buy[data-step="pick"] .buy__step--pick, .buy[data-step="form"] .buy__step--form, .buy[data-step="done"] .buy__step--done { display: grid; gap: 14px; }
.buy__opt { position: relative; display: grid; gap: 4px; padding: 20px 22px; text-align: left; background: #fff; box-shadow: inset 0 0 0 2px #161211; transition: translate .2s var(--ease), box-shadow .2s; }
.buy__opt b { font: 700 26px/1 var(--disp); text-transform: uppercase; }
.buy__opt i { font: 500 15px/1.3 var(--text); font-style: normal; color: #6b625b; }
.buy__opt:hover { translate: 0 -3px; box-shadow: inset 0 0 0 2px var(--accent), 0 14px 24px -14px rgba(0, 0, 0, .5); }
.buy__opt--site { background: #161211; color: #fff; padding-top: 34px; }
.buy__opt--site i { color: #c9c1b6; }
.buy__badge { position: absolute; top: -11px; left: 18px; padding: 5px 10px 4px; background: var(--accent); color: #fff; font: 700 13px/1 var(--disp); text-transform: uppercase; letter-spacing: .06em; rotate: -2deg; }
.buy fieldset { display: grid; gap: 8px; margin: 0; padding: 0; border: 0; }
.buy legend, .fld > span, .buy__qty > span { margin-bottom: 6px; font: 700 13px/1 var(--disp); text-transform: uppercase; letter-spacing: .1em; color: #6b625b; }
.cat { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 12px; padding: 14px 16px; background: #fff; box-shadow: inset 0 0 0 2px #d8cfc0; cursor: pointer; transition: box-shadow .2s; }
.cat input, .chip input { position: absolute; opacity: 0; pointer-events: none; }
.cat span { display: grid; gap: 2px; }
.cat b { font: 700 20px/1 var(--disp); text-transform: uppercase; }
.cat i { font: 500 14px var(--text); font-style: normal; color: #6b625b; }
.cat em { font: 700 22px/1 var(--disp); font-style: normal; }
.cat:has(input:checked) { box-shadow: inset 0 0 0 3px var(--accent); }
.cat:has(input:checked) em { color: var(--accent); }
.buy__qty { display: flex; align-items: center; gap: 0; }
.buy__qty > span { margin: 0 auto 0 0; }
.buy__qty button { width: 44px; height: 44px; background: #161211; color: #fff; font: 700 22px/1 var(--disp); }
.buy__qty button:hover { background: var(--accent); }
.buy__qty output { width: 52px; text-align: center; font: 700 24px/1 var(--disp); }
.fld { display: grid; }
.fld input { height: 50px; padding: 0 14px; border: 0; border-radius: 0; background: #fff; box-shadow: inset 0 0 0 2px #d8cfc0; color: #161211; font: 500 17px var(--text); outline: none; transition: box-shadow .2s; }
.fld input:focus { box-shadow: inset 0 0 0 2px #161211; }
.fld.is-bad input { box-shadow: inset 0 0 0 2px var(--accent); }
.fld.is-bad > span { color: var(--accent); }
.buy__sum { display: flex; justify-content: space-between; align-items: baseline; padding-top: 14px; border-top: 2px dashed #c9bfae; }
.buy__sum span { font: 700 16px var(--disp); text-transform: uppercase; letter-spacing: .08em; color: #6b625b; }
.buy__sum b { font: 700 34px/1 var(--disp); }
.buy__go { width: 100%; min-height: 56px; font-size: 20px; }
.buy__note { font-size: 13px; color: #8a8178; text-align: center; }
.buy__ok { font: 700 40px/1 var(--disp); text-transform: uppercase; color: var(--accent); }
.buy__done-text { font: 500 17px/1.45 var(--text); }
.mo__tees, .mo__sizes { grid-template-columns: repeat(auto-fit, minmax(64px, 1fr)); }
.mo__tees legend, .mo__sizes legend { grid-column: 1 / -1; }
.chip { position: relative; cursor: pointer; }
.chip span { display: grid; place-items: center; min-height: 46px; padding: 0 10px; background: #fff; box-shadow: inset 0 0 0 2px #d8cfc0; font: 700 17px/1 var(--disp); text-transform: uppercase; transition: box-shadow .2s, background .2s, color .2s; }
.chip input:checked + span { background: #161211; color: #fff; box-shadow: none; }
.chip:hover span { box-shadow: inset 0 0 0 2px #161211; }
.tee__order { width: 100%; min-height: 48px; margin-top: 12px; background: var(--accent); color: #fff; font: 700 17px var(--disp); text-transform: uppercase; letter-spacing: .04em; transition: background .2s; }
.tee__order:hover { background: #fff; color: var(--accent); }
'''
open(p,'w').write(s)
