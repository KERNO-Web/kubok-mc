// Данные. Сменная зона ивента и сезоны собираются отсюда: новый сезон = новые данные.
const BRACKET = [
  ["face-verch", "Verch.Fate", "face-kukish", "Кукиш с Хаслом"],
  ["face-iren", "Ирен", "face-nokty", "Нокту"],
  ["face-shala", "Shala", "face-body", "Body"],
  ["face-eeugene", "Eeugene Speed", "face-envimi", "Энвими"],
];
const GONE = [["face-kapustu", "Doctor Kapustu!"], ["face-bach", "Бач"], ["face-smoke", "Smoke [PlanB]"], ["face-kulakoff", "Кулакофф"], ["face-killhomie", "Killhomie"], ["face-elmad", "El Mad"]];

const SEASONS = {
  svoboda: [
    ["sg3dTXCI8GQ", "Title match", "Palmdropov vs Изтолпы"],
    ["kEjqtsZIfQs", "BPM", "Нокту vs Jollo"],
    ["ifDfwytzN74", "BPM", "Никита Мастяк vs Ирен"],
    ["nPfCwm6pGFU", "Перестр*лка", "Майк Стикс vs Кукиш с Хаслом"],
    ["CG8uANZNedE", "BPM", "GD4 vs Smoke [PlanB]"],
    ["OgdpmpIjeKs", "2x2", "Verch.Fate, Killhomie vs Mickey Mouse, Бач"],
    ["MaFPQ9g302k", "Beatbox battle", "Alphavite, Saidmusician vs Doctor Kapustu!, Checkmate"],
    ["1qiIXkYuqOM", "Cypher", "Jollo, Bumble Beezy, Halloween, Похоронил"],
  ],
  btb: [
    ["LsVvuYnQ_A4", "Title match", "Abbalbisk vs Doctor Kapustu!"],
    ["R0GMUgBNY_A", "Перестр*лка", "Хайд vs Palmdropov"],
    ["nKBMggjdfWs", "A capella", "13/47 vs Юля Kiwi"],
    ["-rM3bXoUlU0", "A capella", "Коснарт vs Микси"],
    ["Ua9QH7VbzP8", "A capella", "Бига One vs Вишня"],
    ["tDnHPgZLMQE", "A capella", "Shala vs Xxoc"],
    ["ZGzIiM49Y2c", "Epic Rap Battle", "Сыночка-корзиночка vs Дочка-просрочка"],
    ["HTyyo-za-Y4", "Закулисье", "Как это было"],
  ],
};

// Шортсы: моменты каждого ивента (обложки в assets/sh, вертикальные 9:16)
const MOMENTS = {
  hunt: [["YoJYnZUNnDI", "Хотел соскочить?"], ["2UoWbRU4cIY", "Гроулинг от Зеймана"], ["Uv7tubAMYaU", "Баттл на канале"], ["6SvWWvIPizE", "Высмеял фамилию"], ["Hsbtt14y0Eo", "Загордился"]],
  svoboda: [["GGSmuU7qm4M", "Это грайм-поинт"], ["n-xPEB1Xbh4", "Он быстрее Эминема"], ["5_YtLduaGsk", "Угорает со скуфа"], ["qHN80yrcbfA", "Его не остановить"], ["MyZux-W9hoc", "Нокту вернулся в баттлы"]],
  btb: [["WX2qQ-eG-70", "Ресёрч на Палма"], ["sVpfOLDiy9U", "Убил самого лучшего рэпера"], ["FQVHj_vXIMA", "Тридцатиэтажная рифма"], ["lWjAqpVfuvw", "Уничтожил психолога"], ["jcwS65q3dXY", "Рефлекс работает"]],
};

// Фото из круга по ивентам: [файл, ширина, высота], лучшие первыми (assets/krug/<ивент>/)
const KRUG = {"hunt":[["01",1280,853],["02",1280,854],["03",1280,854],["04",1280,853],["05",1280,854],["06",1280,853],["07",1280,853],["08",1280,854],["09",1280,853],["10",1280,854],["11",1280,1280],["12",1280,854],["13",1280,853],["14",1280,853],["15",1280,854],["16",1280,853],["17",1280,853],["18",1280,853],["19",1280,854],["20",1280,854]],"svoboda":[["01",1280,853],["02",1280,853],["03",1280,853],["04",1280,853],["05",1280,1280],["06",1280,853],["07",1280,853],["08",1280,853],["09",1280,853],["10",1280,853],["11",1280,853],["12",1280,853],["13",1280,853],["14",1280,853],["15",1280,853],["16",1280,853],["17",1280,853],["18",1280,853],["19",1280,853],["20",1280,853]],"btb":[["01",1280,853],["02",1280,853],["03",1280,853],["04",1280,853],["05",1280,853],["06",1280,853],["07",1280,853],["08",1280,853],["09",1280,853],["10",1280,853],["11",1280,853],["12",1280,853],["13",1280,853],["14",1280,853],["15",1280,853],["16",1280,853],["17",1280,853],["18",1280,853],["19",1280,853]]};

const ARCHIVE = [
  ["yFk37WqensU", "Body vs Killhomie", "HUNT, 1/8"],
  ["TgrQ0N43CiU", "Бач vs Shala", "HUNT, 1/8"],
  ["aAMWJh7chgE", "Микси vs Кукиш с Хаслом", "HUNT, 1/8"],
  ["XiNIxZdJs6w", "Verch.Fate vs Zeiman", "HUNT, 1/8"],
  ["yZyyW1XLNuM", "Ирен vs El Mad", "HUNT, 1/8"],
  ["HwuMpB11GMY", "Энвими vs Doctor Kapustu!", "HUNT, 1/8"],
  ["NEY-wCkF81w", "Нокту vs Кулакофф", "HUNT, 1/8"],
  ["5uMRfEdG6ug", "Smoke [PlanB] vs Eeugene Speed", "HUNT, 1/8"],
];

const TICKETS = {
  quarter: { title: "Кубок МЦ: HUNT. 1/4 финала", meta: "24 октября, Москва, 16+", url: "https://kbkmc.bibilet.ru/" },
  after: { title: "Afterparty: HUNT", meta: "24 октября, 22:30, бар БТК, 18+", url: "https://kbkmc.bibilet.ru/w/afterparty-kubok-mc-hunt" },
};

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const yt = (id) => `https://www.youtube.com/watch?v=${id}`;

$(".bracket__list").innerHTML = BRACKET.map(([fa, a, fb, b]) => `
  <li><img src="assets/${fa}.jpg" alt="" width="56" height="56" loading="lazy"><b>${a}</b><i>vs</i><b>${b}</b><img src="assets/${fb}.jpg" alt="" width="56" height="56" loading="lazy"></li>`).join("");
$(".gone").innerHTML = GONE.map(([f, n]) => `
  <figure><img src="assets/${f}.jpg" alt="${n}" width="138" height="138" loading="lazy"><figcaption>${n}</figcaption></figure>`).join("");

$$(".tiles").forEach((box) => {
  box.innerHTML = SEASONS[box.dataset.season].map(([id, k, t]) => `
    <a class="tile" href="${yt(id)}" target="_blank" rel="noopener">
      <img src="assets/yt/${id}.jpg" alt="" width="1280" height="720" loading="lazy">
      <span class="tile__k">${k}</span><span class="tile__t">${t}</span>
    </a>`).join("");
});

$$("[data-moments]").forEach((box) => {
  $(".moments__row", box).innerHTML = MOMENTS[box.dataset.moments].map(([id, t]) => `
    <figure class="moment">
      <button class="moment__frame" data-short="${id}" aria-label="Смотреть: ${t}">
        <img src="assets/sh/${id}.jpg" alt="" width="540" height="960" loading="lazy">
        <span class="moment__play" aria-hidden="true"></span>
      </button>
      <figcaption>${t}</figcaption>
    </figure>`).join("");
});
// Шортс играет прямо в карточке; запуск другого останавливает предыдущий
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-short]");
  if (!b) return;
  $$(".moment__frame.is-on").forEach((x) => { x.classList.remove("is-on"); $("iframe", x)?.remove(); });
  b.classList.add("is-on");
  b.insertAdjacentHTML("beforeend", `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.short}?autoplay=1&playsinline=1&rel=0" title="${b.getAttribute("aria-label")}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`);
});

$(".eps").innerHTML = ARCHIVE.map(([id, t, s], i) => `
  <li><a href="${yt(id)}" target="_blank" rel="noopener">
    <img src="assets/yt/${id}.jpg" alt="" width="1280" height="720" loading="lazy">
    <span class="t">${t.replace(" vs ", " <i>vs</i> ")}</span><span class="s">${s}</span>
  </a></li>`).join("");

// Карусель «Main Event»: прокрутка с привязкой, стрелки и счётчик
const slides = $(".slides");
const count = $(".extra__count");
const total = $$(".slide", slides).length;
const current = () => Math.round(slides.scrollLeft / slides.clientWidth);
$$(".extra__nav").forEach((b) => b.addEventListener("click", () => {
  const i = Math.max(0, Math.min(total - 1, current() + Number(b.dataset.dir)));
  slides.scrollTo({ left: i * slides.clientWidth, behavior: "smooth" });
}));
const syncSlides = () => { count.textContent = `${current() + 1} / ${total}`; };
slides.addEventListener("scroll", syncSlides, { passive: true });
syncSlides();

// Билеты: страница Bibilet внутри сайта
const dlg = $(".drawer");
const frame = $("iframe", dlg);
frame.addEventListener("load", () => dlg.classList.add("loaded"));
const openBibilet = (key) => {
  const t = TICKETS[key];
  $(".drawer__title", dlg).textContent = t.title;
  $(".drawer__meta", dlg).textContent = t.meta;
  $(".drawer__out", dlg).href = t.url;
  if (frame.src !== t.url) { dlg.classList.remove("loaded"); frame.src = t.url; }
  dlg.showModal();
};
$(".drawer__x").addEventListener("click", () => dlg.close());
dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });



// Карусели «Фото с баттлов»: стрелки, счётчик, перетаскивание мышью, клик открывает фото на весь экран
const lb = $(".lb");
let lbList = [], lbIdx = 0;
const lbShow = (i) => {
  lbIdx = (i + lbList.length) % lbList.length;
  $(".lb__img", lb).src = lbList[lbIdx];
  $(".lb__count", lb).textContent = `${lbIdx + 1} / ${lbList.length}`;
};
$$(".lb__nav", lb).forEach((b) => b.addEventListener("click", () => lbShow(lbIdx + Number(b.dataset.dir))));
$(".lb__x", lb).addEventListener("click", () => lb.close());
lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") lbShow(lbIdx - 1); if (e.key === "ArrowRight") lbShow(lbIdx + 1); });

$$("[data-krug]").forEach((box) => {
  const key = box.dataset.krug;
  const row = $(".krug__row", box);
  const urls = KRUG[key].map(([f]) => `assets/krug/${key}/${f}.jpg`);
  row.innerHTML = KRUG[key].map(([f, w, h], i) => `
    <button class="krug__ph" data-i="${i}" aria-label="Открыть фото ${i + 1}">
      <img src="${urls[i]}" alt="" width="${w}" height="${h}" loading="lazy" draggable="false">
    </button>`).join("");
  const count = $(".krug__count", box);
  const items = $$(".krug__ph", row);
  const at = () => { const x = row.scrollLeft + 4; let i = 0; items.forEach((el, k) => { if (el.offsetLeft - row.offsetLeft <= x) i = k; }); return i; };
  const upd = () => { count.textContent = `${String(at() + 1).padStart(2, "0")} / ${items.length}`; };
  upd();
  row.addEventListener("scroll", upd, { passive: true });
  $$(".krug__nav", box).forEach((b) => b.addEventListener("click", () => {
    const i = Math.max(0, Math.min(items.length - 1, at() + Number(b.dataset.dir)));
    row.scrollTo({ left: items[i].offsetLeft - row.offsetLeft, behavior: "smooth" });
  }));
  // перетаскивание мышью; если тянули, клик не открывает фото
  let down = null, moved = false;
  row.addEventListener("pointerdown", (e) => { if (e.pointerType !== "mouse") return; down = { x: e.clientX, s: row.scrollLeft }; moved = false; row.classList.add("is-drag"); });
  addEventListener("pointermove", (e) => { if (!down) return; const dx = e.clientX - down.x; if (Math.abs(dx) > 5) moved = true; row.scrollLeft = down.s - dx; });
  addEventListener("pointerup", () => { if (!down) return; down = null; row.classList.remove("is-drag"); });
  row.addEventListener("click", (e) => {
    const b = e.target.closest(".krug__ph");
    if (!b || moved) return;
    lbList = urls;
    lb.dataset.skin = key;
    lbShow(Number(b.dataset.i));
    lb.showModal();
  });
});

// HUNT: настоящая красная нитка (текстура с их доски) натянута от булавки к булавке; булавки тоже с доски.
// Слой кладётся в контейнер, который прокручивается (лента), иначе в сам блок.
const stringUp = (box, rowSel, cardSel) => {
  const row = $(rowSel, box);
  const layer = document.createElement("div");
  layer.className = "thr-layer";
  layer.setAttribute("aria-hidden", "true");
  const draw = () => {
    const host = getComputedStyle(row).display === "contents" ? box : row;
    if (layer.parentElement !== host) host.append(layer);
    const hr = host.getBoundingClientRect();
    const pts = $$(cardSel, box).filter((el) => el.offsetParent).map((el) => {  // спрятанные карточки не связываем
      const r = el.getBoundingClientRect();
      return [r.left + r.width / 2 - hr.left + host.scrollLeft, r.top - hr.top + host.scrollTop + 7];
    });
    layer.style.width = host.scrollWidth + "px";
    layer.style.height = host.scrollHeight + "px";
    layer.innerHTML = pts.slice(1).map(([x, y], i) => {
      const [px, py] = pts[i];
      const len = Math.hypot(x - px, y - py), ang = Math.atan2(y - py, x - px) * 180 / Math.PI;
      return `<i class="thr" style="left:${px}px;top:${py}px;width:${len}px;transform:rotate(${ang}deg)"></i>`;
    }).join("") + pts.map(([x, y]) => `<img class="pin" src="assets/pin.png" alt="" style="left:${x}px;top:${y}px">`).join("");
  };
  draw();
  addEventListener("load", draw);
  new ResizeObserver(draw).observe(box);
};
const huntMoments = $('[data-moments="hunt"]');
const huntKrug = $('[data-krug="hunt"]');
if (huntMoments) stringUp(huntMoments, ".moments__row", ".moment");
if (huntKrug) stringUp(huntKrug, ".krug__row", ".krug__ph");
// шапка HUNT: полароиды и бумажки на стене связаны ниткой, у каждой стены своя
$$(".ev-head .wall").forEach((w) => stringUp(w, ".wall__in", ".pol"));

// Мерч: переключатель спереди/сзади; на компьютере сторона меняется и при наведении
$$(".tee").forEach((t) => {
  const set = (side) => {
    t.dataset.side = side;
    $$(".tee__flip button", t).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.side === side)));
  };
  $$(".tee__flip button", t).forEach((b) => b.addEventListener("click", () => set(b.dataset.side)));
  const fr = $(".tee__frame", t);
  fr.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") set("back"); });
  fr.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse") set("front"); });
});

// Почта: копирование в буфер
$$("[data-copy]").forEach((b) => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = "Скопировано"; }
  catch { location.href = "mailto:" + b.dataset.copy; }
  setTimeout(() => { b.textContent = "Скопировать"; }, 1800);
}));

// ---------- Анимации ----------
// Появления по скроллу (только текст и плашки; фото и шортсы без анимации — Сергей: лагает): класс .rv + тип (data-rv), .in когда элемент в кадре; --i даёт ступеньку внутри группы
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!still) {
  document.documentElement.classList.add("anim");
  const groups = [
    [".ev-head__plate", "stamp"], [".ev-head__date", "pop"], [".ev-head__sub, .ev-head__btn", "up"],
    [".bracket__list li", "side"], [".tag", "pop"],
    [".sv__left", "slap"], [".sv__bars span", "pop"],
    [".btb__title", "slam"], [".btb__bar", "stamp"], [".btb__when, .btb__text", "up"],
    [".moments__h", "pop"], [".krug__h", "pop"],
    [".archive__head", "up"], [".orgs__h", "up"], [".merch__head", "up"], [".final__links a", "side"], [".final__mail", "up"],
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
  if (!CSS.supports("animation-timeline: scroll()")) {
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(hero); } }, { passive: true });
    hero();
  }
  // за мышью: фон, логотип и люди смещаются на разную глубину
  // цель задаёт мышь, а слои догоняют её плавно в rAF — при резких движениях не дёргается
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
  const follow = () => {
    cx += (tx - cx) * .09; cy += (ty - cy) * .09;
    cover.style.setProperty("--mx", cx.toFixed(4));
    cover.style.setProperty("--my", cy.toFixed(4));
    raf = Math.abs(tx - cx) + Math.abs(ty - cy) > .0005 ? requestAnimationFrame(follow) : 0;
  };
  const aim = (x, y) => { tx = x; ty = y; if (!raf) raf = requestAnimationFrame(follow); };
  cover.addEventListener("pointermove", (e) => { if (e.pointerType === "mouse") aim(e.clientX / innerWidth - .5, e.clientY / innerHeight - .5); });
  cover.addEventListener("pointerleave", () => aim(0, 0));

  // 3D-наклон карточек шортсов за курсором
  $$(".moment__frame").forEach((f) => {
    f.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      const r = f.getBoundingClientRect();
      const card = f.closest(".moment") || f;  // наклоняется вся карточка с рамкой, а не только видео
      card.style.setProperty("--ry", ((e.clientX - r.left) / r.width - .5) * 14 + "deg");
      card.style.setProperty("--rx", (.5 - (e.clientY - r.top) / r.height) * 12 + "deg");
      card.style.setProperty("--gx", ((e.clientX - r.left) / r.width) * 100 + "%");
      card.style.setProperty("--gy", ((e.clientY - r.top) / r.height) * 100 + "%");
    });
    f.addEventListener("pointerleave", () => { const card = f.closest(".moment") || f; card.style.setProperty("--rx", "0deg"); card.style.setProperty("--ry", "0deg"); });
  });
}

// шапка: после обложки — тёмная подложка вместо difference, иначе меню тонет на светлых фото
{
  const mast = document.querySelector(".mast");
  const cover = document.querySelector(".cover");
  const set = () => mast.classList.toggle("is-solid", scrollY > cover.offsetHeight - 80);
  addEventListener("scroll", set, { passive: true });
  set();
}

// Организаторы: по 4 крупных квадратных фото под каждым, ч/б, клик открывает просмотр
const touchUI = matchMedia("(hover: none)");
// большой кадр организатора: на телефоне касание переключает на цветной второй кадр и обратно
$$(".org__stage").forEach((st) => st.addEventListener("click", () => { if (touchUI.matches) st.closest(".org").classList.toggle("is-color"); }));
const ORG = {"h": [["h-01", 0], ["h-02", 0], ["h-03", 0], ["h-07", 1]], "p": [["p-01", 0], ["p-02", 0], ["p-04", 0], ["p-06", 0]]};
$$("[data-org]").forEach((art) => {
  const list = ORG[art.dataset.org];
  const urls = list.map(([f]) => `assets/orgs/${f}.webp`);
  const grid = $(".org__grid", art);
  grid.innerHTML = list.map(([f, cut], i) => `<button class="ofr${cut ? " ofr--cut" : ""}" data-i="${i}" aria-label="Открыть фото ${i + 1}"><img src="${urls[i]}" alt="" loading="lazy"></button>`).join("");
  grid.addEventListener("click", (e) => {
    const b = e.target.closest(".ofr");
    if (!b) return;
    if (touchUI.matches && !b.classList.contains("is-color")) { $$(".ofr.is-color").forEach((x) => x.classList.remove("is-color")); b.classList.add("is-color"); return; }
    lbList = urls;
    lb.dataset.skin = "shell";
    lbShow(Number(b.dataset.i));
    lb.showModal();
  });
});

// Билеты: сначала попап выбора — своя форма сайта или касса Bibilet
const CATS = {
  quarter: [["dance", "Танцпол", "Стоя в зале", 1500], ["ring", "Проход в круг", "Вплотную к баттлерам", 2500], ["balcony", "Балкон", "Вид на круг сверху", 2000]],
  after: [["entry", "Вход", "Бар БТК, 22:30, 18+", 500]],
};
// схема зала Кубка для формы билета: балконы буквой П, танцпол, проход вокруг круга, судьи, бар, вход
const HALL = `<svg class="hall" viewBox="0 0 460 300" role="img" aria-label="Схема зала: выберите зону">
  <rect class="hall__wall" x="6" y="6" width="448" height="288"/>
  <path class="zone" data-zone="balcony" d="M10 10H450V236H404V62H56V236H10Z"/>
  <rect class="zone" data-zone="dance" x="56" y="62" width="348" height="228"/>
  <circle class="zone" data-zone="ring" cx="230" cy="172" r="76"/>
  <circle class="hall__circle" cx="230" cy="172" r="42"/>
  <rect class="hall__fix" x="176" y="67" width="108" height="25"/>
  <path id="hall-arc" d="M175 172A55 55 0 0 1 285 172" fill="none"/>
  <rect class="hall__fix" x="340" y="248" width="64" height="42"/>
  <text x="230" y="40">БАЛКОН</text><text x="33" y="150" transform="rotate(-90 33 150)">БАЛКОН</text><text x="427" y="150" transform="rotate(90 427 150)">БАЛКОН</text>
  <text x="110" y="270">ТАНЦПОЛ</text><text class="sm"><textPath href="#hall-arc" startOffset="50%">ПРОХОД В КРУГ</textPath></text>
  <text x="230" y="178" class="ring">КРУГ</text><text x="230" y="84.5" class="sm dark">СУДЬИ</text><text x="372" y="273" class="sm dark">БАР</text>
  <path class="hall__door" d="M200 294H260"/><text x="230" y="288" class="sm">ВХОД</text>
</svg>`;
const syncHall = () => {
  const c = $("input[name=cat]:checked", buy);
  $$("[data-zone]", buy).forEach((z) => z.classList.toggle("on", c && z.dataset.zone === c.value));
};
const rub = (n) => n.toLocaleString("ru-RU") + "\u00a0₽";
const buy = $(".buy:not(.buy--merch)");
let buyKey = "quarter", qty = 1;
const step = (d, name) => { d.dataset.step = name; };
const buyTotal = () => {
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
  if (buyKey === "quarter") $(".buy__cats legend", buy).insertAdjacentHTML("afterend", HALL);
  $("form", buy).reset();
  $$("input[name=cat]", buy)[0].checked = true;
  syncHall();
  buyTotal();
  step(buy, "pick");
  buy.showModal();
}));
$$("[data-go]", buy).forEach((b) => b.addEventListener("click", () => {
  if (b.dataset.go === "bibilet") { buy.close(); openBibilet(buyKey); return; }
  step(buy, "form");
  $("input[name=name]", buy).focus();
}));
$(".buy__cats", buy).addEventListener("change", () => { buyTotal(); syncHall(); });
// схема зала: клик по зоне выбирает категорию
$(".buy__cats", buy).addEventListener("click", (e) => {
  const z = e.target.closest("[data-zone]");
  if (!z) return;
  const r = $(`input[name=cat][value=${z.dataset.zone}]`, buy);
  if (r) { r.checked = true; buyTotal(); syncHall(); }
});
$$("[data-q]", buy).forEach((b) => b.addEventListener("click", () => { qty = Math.max(1, Math.min(10, qty + Number(b.dataset.q))); buyTotal(); }));

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
const sold = $$(".tee").map((t) => t.classList.contains("tee--sold"));
const firstFree = sold.indexOf(false);
$(".mo__tees", mo).innerHTML = "<legend>Модель</legend>" + tees.map((n, i) => `<label class="chip${sold[i] ? " chip--sold" : ""}"><input type="radio" name="tee" value="${n}"${sold[i] ? " disabled" : ""}${i === firstFree ? " checked" : ""}><span>${n}</span></label>`).join("");
$$(".tee--sold .tee__order").forEach((b) => { b.disabled = true; b.textContent = "Нет в наличии"; });
$(".mo__sizes", mo).insertAdjacentHTML("beforeend", ["S", "M", "L", "XL", "XXL"].map((z) => `<label class="chip"><input type="radio" name="size" value="${z}"${z === "L" ? " checked" : ""}><span>${z}</span></label>`).join(""));
$$(".tee").forEach((t, i) => $(".tee__order", t).addEventListener("click", () => {
  $("form", mo).reset();
  $$("input[name=tee]", mo)[sold[i] ? firstFree : i].checked = true;
  step(mo, "form");
  mo.showModal();
}));
demoForm(mo, (f) => `${f.get("name")}, футболка «${f.get("tee")}», размер ${f.get("size")}. Напишем вам: ${f.get("contact")}.`);


// Меню на телефоне: бургер раскрывает навигацию на весь экран
{
  const mast = $(".mast"), burger = $(".mast__burger");
  const setMenu = (open) => {
    mast.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    document.documentElement.classList.toggle("menu-open", open);
  };
  burger.addEventListener("click", () => setMenu(!mast.classList.contains("is-open")));
  $$(".mast__nav a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
  matchMedia("(min-width: 768px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });
}

// Просмотр фото: свайп пальцем листает
{
  let sx = null;
  lb.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (sx === null) return;
    const dx = e.changedTouches[0].clientX - sx;
    sx = null;
    if (Math.abs(dx) > 50) lbShow(lbIdx + (dx < 0 ? 1 : -1));
  });
}

// Main Event: «vs» в подписи пары — красным
$$(".slide figcaption b").forEach((b) => { b.innerHTML = b.textContent.replace(/ vs /i, " <i>vs</i> "); });

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
