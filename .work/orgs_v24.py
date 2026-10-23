# v24 «Организаторы»: без подписей, у каждого герой-кадр + досье из 8 фото (клик = просмотр); нижняя часть (организаторы, архив, мерч) на общем фоне-фото
import re
ORG={"h": [["h-01",0],["h-02",0],["h-03",0],["h-04",1],["h-05",1],["h-06",1],["h-07",1],["h-08",0]],
     "p": [["p-01",0],["p-02",0],["p-03",1],["p-04",0],["p-05",1],["p-06",0],["p-07",0],["p-08",1]]}
p='index.html'; s=open(p).read()
def org(key, k2, name, lines):
    return (f'''      <article class="org" data-org="{k2}">
        <div class="org__stage">
          <h3 class="org__name" aria-label="{name}">{'<br>'.join(lines)}</h3>
          <img class="org__ph org__ph--a" src="assets/orgs/{key}-a.webp" alt="{name}" loading="lazy">
          <img class="org__ph org__ph--b" src="assets/orgs/{key}-b.webp" alt="" loading="lazy">
        </div>
        <div class="org__grid"></div>
      </article>''')
new=f'''<section class="orgs" id="orgs" data-skin="shell">
    <h2 class="orgs__h">Организаторы</h2>
    <div class="orgs__row">
{org('halloween','h','Halloween',['Halloween'])}
{org('pohoronil','p','МЦ Похоронил',['МЦ','Похоронил'])}
    </div>
  </section>'''
s,n=re.subn(r'<section class="orgs" id="orgs".*?</section>', new, s, count=1, flags=re.S); assert n==1
# общий фон нижней части
i=s.index('  <section class="orgs" id="orgs"')
s=s[:i]+'  <div class="lower">\n    <div class="lower__bg" aria-hidden="true"></div>\n'+s[i:]
j=s.index('  <footer class="final"')
s=s[:j]+'  </div>\n\n'+s[j:]
s=s.replace('style.css?v=42','style.css?v=43').replace('app.js?v=26','app.js?v=27')
open(p,'w').write(s)

p='app.js'; s=open(p).read()
s+='''
// Организаторы: досье из 8 фото под каждым (вырезки на красном, фото ч/б), клик открывает просмотр
const ORG = ''' + str(ORG).replace("'",'"') + ''';
$$("[data-org]").forEach((art) => {
  const list = ORG[art.dataset.org];
  const urls = list.map(([f]) => `assets/orgs/${f}.webp`);
  const grid = $(".org__grid", art);
  grid.innerHTML = list.map(([f, cut], i) => `<button class="ofr${cut ? " ofr--cut" : ""}" data-i="${i}" aria-label="Открыть фото ${i + 1}"><img src="${urls[i]}" alt="" loading="lazy"></button>`).join("");
  grid.addEventListener("click", (e) => {
    const b = e.target.closest(".ofr");
    if (!b) return;
    lbList = urls;
    lb.dataset.skin = "shell";
    lbShow(Number(b.dataset.i));
    lb.showModal();
  });
});
'''
open(p,'w').write(s)

p='style.css'; s=open(p).read()
s+='''
/* v24 Нижняя часть: организаторы, архив и мерч на общем фоне — их кадр из перехода, ч/б, стоит на месте, пока блоки едут поверх */
.lower { position: relative; isolation: isolate; }
.lower__bg { position: sticky; top: 0; z-index: -1; height: 100vh; margin-bottom: -100vh; background: linear-gradient(#0c0a09, rgba(12, 10, 9, .35) 30%, rgba(12, 10, 9, .55) 75%, #0c0a09), radial-gradient(50% 60% at 30% 70%, rgba(225, 20, 30, .16), transparent 70%), url("assets/lower-bg.webp") 50% 50% / cover no-repeat; filter: grayscale(1) contrast(1.15) brightness(.55); }
.lower__bg::after { content: ""; position: absolute; inset: 0; background: var(--speck); opacity: .22; mix-blend-mode: screen; }
.lower > section { position: relative; background: transparent; }
.lower .merch { padding-bottom: clamp(70px, 7vw, 110px); }
.lower .tee__frame { box-shadow: 0 24px 40px -18px rgba(0, 0, 0, .9); }

/* Организаторы: только ники и фото, без подписей */
.orgs__h { font-size: clamp(54px, 6vw, 104px); line-height: .9; margin-bottom: clamp(20px, 2vw, 32px); }
.orgs__row { gap: clamp(16px, 2vw, 32px); align-items: start; }
.org { gap: 10px; }
.org__stage { box-shadow: 0 30px 50px -24px rgba(0, 0, 0, .95); }
.org__grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
.ofr { position: relative; display: block; aspect-ratio: 1; overflow: hidden; padding: 0; background: #151110; cursor: zoom-in; }
.ofr img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) contrast(1.12) brightness(.9); transition: filter .35s, scale .5s var(--ease); }
.ofr--cut { background: radial-gradient(80% 80% at 50% 100%, #e1141e, #8c0d12); }
.ofr--cut img { object-fit: contain; object-position: 50% 100%; inset: 8% 0 0; height: 92%; }
.ofr::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 0 2px rgba(255, 255, 255, .08); transition: box-shadow .25s; pointer-events: none; }
.ofr:hover img { filter: none; scale: 1.06; }
.ofr:hover::after { box-shadow: inset 0 0 0 3px var(--accent); }
.org:nth-child(2) .org__stage .org__name { top: 4%; }
'''
open(p,'w').write(s)
