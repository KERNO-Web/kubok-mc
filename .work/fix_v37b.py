# v37b: ошибки в никах и подписях (сверено с их картинками, афишами, YouTube и t.me/s/kbkmc) + окрашивание фото организаторов по касанию
p='index.html'; s=open(p).read()
rep=[
 ('alt="Main event: Ями из Воронежа против Кении из Лениногорска"','alt="Main event: Ями из Воронежа против Кени из Лениногорска"'),
 ('<figcaption><b>Ями vs Кения</b></figcaption>','<figcaption><b>Ями vs Кеня</b></figcaption>'),
 ('МЦ Доналдас, Kumska"','МЦ Доналдс, Kumska"'),
 ('Молодой Казах, МЦ Доналдас, Kumska</figcaption>','Молодой Казах, МЦ Доналдс, Kumska</figcaption>'),
 ('<span>Клуб «Свобода», Ленинградский просп., 47</span>','<span>Клуб «Свобода», Ленинградский просп., 47, стр.&nbsp;19</span>'),
]
for a,b in rep:
    assert a in s, a; s=s.replace(a,b)
assert 'Доналдас' not in s and 'Кения' not in s
s=s.replace('style.css?v=72','style.css?v=73').replace('app.js?v=42','app.js?v=43')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
rep=[
 ('["nPfCwm6pGFU", "BPM", "Майк Стикс vs Кукиш с Хаслом"]','["nPfCwm6pGFU", "Перестр*лка", "Майк Стикс vs Кукиш с Хаслом"]'),
 ('["R0GMUgBNY_A", "A capella", "Хайд vs Palmdropov"]','["R0GMUgBNY_A", "Перестр*лка", "Хайд vs Palmdropov"]'),
 ('["ZGzIiM49Y2c", "Special", "Epic Rap Battle"]','["ZGzIiM49Y2c", "Epic Rap Battle", "Сыночка-корзиночка vs Дочка-просрочка"]'),
]
for a,b in rep:
    assert a in s, a; s=s.replace(a,b)
# организаторы на телефоне: касание окрашивает (досье: второе касание открывает фото; большой кадр: переключает на цветной второй)
old='''  grid.addEventListener("click", (e) => {
    const b = e.target.closest(".ofr");
    if (!b) return;'''
assert old in s
s=s.replace(old,'''  grid.addEventListener("click", (e) => {
    const b = e.target.closest(".ofr");
    if (!b) return;
    if (touchUI.matches && !b.classList.contains("is-color")) { $$(".ofr.is-color").forEach((x) => x.classList.remove("is-color")); b.classList.add("is-color"); return; }''')
old='const ORG = '
assert old in s
s=s.replace(old,'''const touchUI = matchMedia("(hover: none)");
// большой кадр организатора: на телефоне касание переключает на цветной второй кадр и обратно
$$(".org__stage").forEach((st) => st.addEventListener("click", () => { if (touchUI.matches) st.closest(".org").classList.toggle("is-color"); }));
const ORG = ''',1)
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''@media (hover: none) {
  .org.is-color .org__ph.org__ph--a { opacity: 0 !important; }
  .org.is-color .org__ph--b { opacity: 1; }
  .ofr.is-color img, .ofr.is-color:hover img { filter: none; }
  .ofr.is-color::after, .ofr.is-color:hover::after { box-shadow: inset 0 0 0 3px var(--accent); }
}
'''
open(p,'w').write(s)
