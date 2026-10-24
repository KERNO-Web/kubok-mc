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
    ["nPfCwm6pGFU", "Перестрелка", "Майк Стикс vs Кукиш с Хаслом"],
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

// Видео с турнира HUNT по стадиям: список роликов или текст-заглушка
const STAGES = [
  ["1/8", [
    ["yFk37WqensU", "Body vs Killhomie"],
    ["TgrQ0N43CiU", "Бач vs Shala"],
    ["aAMWJh7chgE", "Микси vs Кукиш с Хаслом"],
    ["XiNIxZdJs6w", "Verch.Fate vs Zeiman"],
    ["yZyyW1XLNuM", "Ирен vs El Mad"],
    ["HwuMpB11GMY", "Энвими vs Doctor Kapustu!"],
    ["NEY-wCkF81w", "Нокту vs Кулакофф"],
    ["5uMRfEdG6ug", "Smoke [PlanB] vs Eeugene Speed"],
  ], "BPM · 2 раунда"],
  ["1/4", "Видео скоро появятся"],
  ["1/2", "Ивент ещё не начался"],
  ["Финал", "Ивент ещё не начался"],
];

const TICKETS = {
  quarter: { title: "Кубок МЦ: HUNT. 1/4 финала", meta: "24 октября, Москва, 18+", url: "https://kbkmc.bibilet.ru/" },
  after: { title: "Afterparty: HUNT", meta: "24 октября, 22:30, бар БТК, 18+", url: "https://kbkmc.bibilet.ru/w/afterparty-kubok-mc-hunt" },
};

const $ = (s, r = document) => r.querySelector(s);
// «vs» по формату: у перестрелки вместо vs скрещённые револьверы (как на их обложках), цвет берут от vs
const GUNS = `<i class="guns" title="Перестрелка"><span class="sr-only">vs</span></i>`;
const vsFor = (t, kind) => t.replace(" vs ", kind && /перестр/i.test(kind) ? ` ${GUNS} ` : " <i>vs</i> ");
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const yt = (id) => `https://www.youtube.com/watch?v=${id}`;

$(".bracket__list").innerHTML = BRACKET.map(([fa, a, fb, b]) => `
  <li><img src="assets/${fa}.jpg" alt="" width="56" height="56" loading="lazy"><b>${a}</b>${GUNS}<b>${b}</b><img src="assets/${fb}.jpg" alt="" width="56" height="56" loading="lazy"></li>`).join("");
$(".gone").innerHTML = GONE.map(([f, n]) => `
  <figure><img src="assets/${f}.jpg" alt="${n}" width="138" height="138" loading="lazy"><figcaption>${n}</figcaption></figure>`).join("");

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

const stageTabs = $(".stages");
const stagePanel = $(".stage-panel");
stageTabs.innerHTML = STAGES.map(([name, v], i) => `
  <button class="stage" type="button" role="tab" data-stage="${i}"${typeof v === "string" ? ' data-empty=""' : ""}>${name}</button>`).join("");
// Плеер выпусков — один на все блоки (HUNT по стадиям, прошлые сезоны целиком), вид задаёт сезон:
// слева экран (обложка с кнопкой → ролик прямо здесь), под ним подпись «01 / 08 · пара · ← →», справа нумерованный список
const VP = new WeakMap();
const vpPick = (host, k, play) => {
  const eps = VP.get(host);
  const [id, t, kind] = eps[k];
  const pad = (n) => String(n).padStart(2, "0");
  const pair = vsFor(t, kind);
  host.dataset.ep = k;
  $$(".eps--side button", host).forEach((b) => {
    const on = Number(b.dataset.ep) === k;
    b.classList.toggle("on", on);
    b.classList.toggle("is-play", on && play);
  });
  $(".vp__t", host).innerHTML = `<span class="vp__n">${pad(k + 1)} / ${pad(eps.length)}</span><b>${kind ? `<small>${kind}</small>` : ""}${pair}</b>
    <span class="vp__nav"><button type="button" data-ep-step="-1" aria-label="Предыдущий баттл">←</button><button type="button" data-ep-step="1" aria-label="Следующий баттл">→</button><a class="vp__yt" href="${yt(id)}" target="_blank" rel="noopener" aria-label="Смотреть на YouTube" title="Смотреть на YouTube"></a></span>`;
  $(".vp__screen", host).innerHTML = play
    ? `<iframe src="https://www.youtube-nocookie.com/embed/${id}?autoplay=1&playsinline=1&rel=0" title="${t}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`
    : `<button class="vp__poster" type="button" data-ep-play="${k}" aria-label="Смотреть: ${t}"><img src="assets/yt/${id}.jpg" alt="" width="1280" height="720"><span class="vp__play" aria-hidden="true"></span></button>`;
};
// eps: [[id, "A vs B", вид баттла?], …]
const playerUp = (host, eps) => {
  VP.set(host, eps);
  host.classList.add("vbox");
  host.innerHTML = `<div class="vp"><div class="vp__screen"></div><p class="vp__t"></p>
  <div class="vp__chan"><img src="assets/kbkmc-ava.webp" alt="" width="160" height="160"><p><b>Кубок МЦ</b><span>422 тыс. подписчиков</span></p>
    <a href="https://www.youtube.com/@kbkmc?sub_confirmation=1" target="_blank" rel="noopener">Подписаться</a></div></div>
  <ol class="eps eps--side">${eps.map(([id, t, kind], k) => `
  <li><button type="button" data-ep="${k}">
    <span class="n">${String(k + 1).padStart(2, "0")}</span>
    <img src="assets/yt/s/${id}.jpg" alt="" width="400" height="225" loading="lazy">
    <span class="t">${kind ? `<small>${kind}</small>` : ""}${vsFor(t, kind)}</span>
  </button></li>`).join("")}</ol>`;
  vpPick(host, 0, false);
};
document.addEventListener("click", (e) => {
  const host = e.target.closest(".vbox");
  if (!host || !VP.has(host)) return;
  const st = e.target.closest("[data-ep-step]");
  if (st) {
    const len = VP.get(host).length;
    vpPick(host, (Number(host.dataset.ep) + Number(st.dataset.epStep) + len) % len, !!$(".vp__screen iframe", host));
    return;
  }
  const b = e.target.closest("[data-ep], [data-ep-play]");
  if (b) vpPick(host, Number(b.dataset.ep ?? b.dataset.epPlay), true);
});
$$(".vbox--season").forEach((box) => playerUp(box, SEASONS[box.dataset.season].map(([id, kind, t]) => [id, t, kind])));

const showStage = (i) => {
  const [name, v, kind] = STAGES[i];
  $$(".stage", stageTabs).forEach((b, j) => b.setAttribute("aria-selected", String(j === i)));
  stagePanel.setAttribute("aria-label", name === "Финал" ? name : `${name} финала`);
  if (typeof v === "string") {
    VP.delete(stagePanel);
    stagePanel.classList.remove("vbox");
    stagePanel.innerHTML = `<p class="stage-panel__empty"><b>${v}</b></p>`;
  } else playerUp(stagePanel, v.map(([id, t, k]) => [id, t, k || kind]));
};
stageTabs.addEventListener("click", (e) => {
  const b = e.target.closest(".stage");
  if (b) showStage(Number(b.dataset.stage));
});
showStage(0);

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
lb.addEventListener("close", () => lb.classList.remove("is-single"));

// Афиши: не висят в шапках сезонов, у каждого одинаковая кнопка «Афиша» → просмотр. Новую афишу HUNT — дописать в массив
const POSTERS = {
  hunt: ["assets/hunt-board.jpg", "assets/hunt-top16.jpg", "assets/poster-after.jpg"],
  svoboda: ["assets/poster-svoboda.jpg"],
  btb: ["assets/poster-btb.jpg"],
};
$$("[data-posters]").forEach((b) => {
  const key = b.dataset.posters, list = POSTERS[key];
  if (list.length > 1) b.textContent = `Афиши · ${list.length}`;
  b.addEventListener("click", () => {
    lbList = list;
    lb.dataset.skin = key;
    lb.classList.toggle("is-single", list.length < 2);
    lbShow(0);
    lb.showModal();
  });
});

// «Фото с баттлов» — не лента, а доска с автосменой (boardUp ниже); при reduced-motion остаётся лента со стрелками
const krugBoard = !matchMedia("(prefers-reduced-motion: reduce)").matches;
$$("[data-krug]").forEach((box) => {
  const key = box.dataset.krug;
  if (krugBoard) box.classList.add("is-board");
  const row = $(".krug__row", box);
  const urls = KRUG[key].map(([f]) => `assets/krug/${key}/${f}.jpg`);
  row.innerHTML = KRUG[key].map(([f, w, h], i) => `
    <button class="krug__ph" data-i="${i}" aria-label="Открыть фото ${i + 1}">
      <img src="${urls[i]}" alt="" width="${w}" height="${h}" loading="lazy" draggable="false">
    </button>`).join("");
  const count = $(".krug__count", box);
  const items = $$(".krug__ph", row);
  const at = () => { const x = row.scrollLeft + 4; let i = 0; items.forEach((el, k) => { if (el.offsetLeft - row.offsetLeft <= x) i = k; }); return i; };
  // в конце ленты видно несколько последних фото сразу, левое из них не последнее — показываем максимум
  const atEnd = () => row.scrollLeft >= row.scrollWidth - row.clientWidth - 4;
  // счётчик ленты (у доски свой, его ставит boardUp); пересчёт и когда фото догрузились — до этого лента пустая и казалось, что мы в конце («20 / 20»)
  const upd = () => { if (box.classList.contains("is-board")) return; count.textContent = `${String(atEnd() ? items.length : at() + 1).padStart(2, "0")} / ${items.length}`; };
  upd();
  row.addEventListener("scroll", upd, { passive: true });
  if (!krugBoard) { const ro = new ResizeObserver(upd); items.forEach((el) => ro.observe(el)); }
  $$(".krug__nav", box).forEach((b) => b.addEventListener("click", () => {
    if (box.classList.contains("is-board")) return;
    const i = Math.max(0, Math.min(items.length - 1, at() + Number(b.dataset.dir)));
    row.scrollTo({ left: items[i].offsetLeft - row.offsetLeft, behavior: "smooth" });
  }));
  // перетаскивание мышью; если тянули, клик не открывает фото
  let down = null, moved = false;
  row.addEventListener("pointerdown", (e) => { if (e.pointerType !== "mouse" || box.classList.contains("is-board")) return; down = { x: e.clientX, s: row.scrollLeft }; moved = false; row.classList.add("is-drag"); });
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
  return draw;
};
const huntMoments = $('[data-moments="hunt"]');
const huntKrug = $('[data-krug="hunt"]');
if (huntMoments) stringUp(huntMoments, ".moments__row", ".moment");
const drawKrug = huntKrug && stringUp(huntKrug, ".krug__row", ".krug__ph");
// Доска «Фото с баттлов» во всех сезонах одинаковая: столько целых фото, сколько влезает; листается страницами
// только стрелками (на телефоне ещё свайп, с клавиатуры ← →). Колесо не трогаем — наведение не должно мешать прокрутке сайта. Как фото сменяется — стиль сезона (CSS .is-off/.is-on):
// HUNT — падает из-под булавки, Св*бода — новое напыляется баллончиком поверх старого (canvas, sprayIn), BTB — старый телик:
// новое уже лежит снизу, старое («призрак») поверх плавно растворяется, по экрану мягко бегут помехи
const FX = { hunt: [850, 800], svoboda: [0, 0], btb: [0, 1000] };
// Св*бода: новое фото «напыляется» на canvas поверх старого — плотное пятно краски с каплями по краю, сопло идёт зигзагом
// в четыре прохода с нахлёстом: к концу краска сама закрывает всё фото, без резкого «доливания» и пропадающих точек
const sprayIn = async (b, url) => {
  const img = $("img", b), pic = new Image();
  pic.src = url;
  await pic.decode().catch(() => {});
  const dpr = Math.min(2, devicePixelRatio || 1);
  const W = Math.round(img.clientWidth * dpr), H = Math.round(img.clientHeight * dpr);
  const cv = document.createElement("canvas"), mask = document.createElement("canvas");
  cv.className = "krug__spray";
  cv.width = mask.width = W;
  cv.height = mask.height = H;
  b.append(cv);
  const ctx = cv.getContext("2d"), m = mask.getContext("2d");
  const k = Math.max(W / pic.naturalWidth, H / pic.naturalHeight), sw = W / k, sh = H / k;
  const sx = (pic.naturalWidth - sw) / 2, sy = (pic.naturalHeight - sh) / 2;
  const path = [[-.08, .1], [1.08, .08], [-.08, .37], [1.08, .35], [-.08, .64], [1.08, .62], [-.08, .92], [1.08, .9]];
  const R = H * .3, T = 1250, t0 = performance.now();
  let last = 0;
  await new Promise((done) => {
    // время берём своё: метка rAF бывает раньше t0, отрицательный прогресс ронял анимацию и доска зависала
    const frame = () => {
      const p = Math.max(last, Math.min(1, (performance.now() - t0) / T));
      // сопло идёт от last до p, капли сыплются по всему отрезку, чтобы на быстрых кадрах не было дыр
      for (let q = last; q <= p; q += .012) {
        const seg = q * (path.length - 1), i = Math.min(path.length - 2, Math.floor(seg)), f = seg - i;
        const x = (path[i][0] + (path[i + 1][0] - path[i][0]) * f) * W, y = (path[i][1] + (path[i + 1][1] - path[i][1]) * f) * H;
        const g = m.createRadialGradient(x, y, 0, x, y, R * .78);
        g.addColorStop(0, "rgba(0,0,0,.8)");
        g.addColorStop(.55, "rgba(0,0,0,.5)");
        g.addColorStop(1, "rgba(0,0,0,0)");
        m.globalAlpha = 1;
        m.fillStyle = g;
        m.fillRect(x - R, y - R, R * 2, R * 2);
        m.fillStyle = "#000";
        for (let d = 0; d < 60; d++) {
          const a = Math.random() * 6.283, r = R * .42 * Math.sqrt(-2 * Math.log(Math.random() || 1e-6));
          m.globalAlpha = .4 + Math.random() * .6;
          m.beginPath();
          m.arc(x + Math.cos(a) * r, y + Math.sin(a) * r, (Math.random() * 1.6 + .5) * dpr, 0, 6.283);
          m.fill();
        }
      }
      last = p;
      // последние 20% — тонкий слой по всей площади каждый кадр: оставшиеся просветы затягиваются плавно
      if (p > .8) { m.globalAlpha = .1; m.fillRect(0, 0, W, H); }
      if (p >= 1) { m.globalAlpha = 1; m.fillRect(0, 0, W, H); }
      ctx.globalCompositeOperation = "source-over";
      ctx.clearRect(0, 0, W, H);
      ctx.drawImage(pic, sx, sy, sw, sh, 0, 0, W, H);
      ctx.globalCompositeOperation = "destination-in";
      ctx.drawImage(mask, 0, 0);
      if (p < 1) requestAnimationFrame(frame); else done();
    };
    requestAnimationFrame(frame);
  });
  return cv;
};
const boardUp = (box, redraw) => {
  const key = box.dataset.krug;
  const row = $(".krug__row", box);
  const btns = $$(".krug__ph", row);
  const count = $(".krug__count", box);
  const N = btns.length;
  const [tOff, tOn] = FX[key];
  const src = (i) => `assets/krug/${key}/${KRUG[key][i][0]}.jpg`;
  const pad = (v) => String(v).padStart(2, "0");
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  let n = 1, start = 0, busy = false, queued = 0;
  const label = () => { count.textContent = n > 1 ? `${pad(start + 1)}–${pad(start + n)} / ${N}` : `${pad(start + 1)} / ${N}`; };
  const put = (b, i) => { b.dataset.i = i; $("img", b).src = src(i); };
  // сколько фото помещается целиком; лишние места прячем
  const fit = () => {
    btns.forEach((b) => { b.hidden = false; });
    // целевая ширина фото ~400px; сколько влезает — столько и показываем, а ширину подгоняем, чтобы ряд был заполнен без дыр
    const cs = getComputedStyle(row), gap = parseFloat(cs.columnGap) || 0;
    const W = row.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    n = Math.min(N, Math.max(1, Math.floor((W + gap) / (400 + gap))));
    row.style.setProperty("--pw", `${Math.floor((W - gap * (n - 1)) / n)}px`);
    start = Math.min(start, N - n);
    btns.forEach((b, k) => { b.hidden = k >= n; if (k < n) put(b, start + k); });
    row.style.justifyContent = n === 1 ? "center" : "";
    label();
    redraw?.();
  };
  const swap = async (b, i, delay) => {
    await wait(delay);
    const img = $("img", b), pre = new Image();
    pre.src = src(i);
    await pre.decode().catch(() => {});
    if (key === "svoboda") {
      b.classList.add("is-on");
      const cv = await sprayIn(b, src(i));
      put(b, i);
      // холст убираем, когда новое фото уже раскодировано в самом img, иначе на телефоне мигает пустая рамка
      await img.decode().catch(() => {});
      cv.remove();
      b.classList.remove("is-on");
      return;
    }
    if (key === "btb") {
      const ghost = img.cloneNode();
      ghost.className = "krug__ghost";
      ghost.removeAttribute("loading");
      b.append(ghost);
      put(b, i);
      b.classList.add("is-on");
      await wait(tOn);
      ghost.remove();
      b.classList.remove("is-on");
      return;
    }
    b.classList.add("is-off");
    await wait(tOff);
    put(b, i);
    b.classList.replace("is-off", "is-on");
    await wait(tOn);
    b.classList.remove("is-on");
  };
  // страница вперёд/назад, по кругу
  // клик во время смены не теряется: запоминаем последний и выполняем сразу после
  const go = async (dir) => {
    if (busy) { queued = dir; return; }
    const to = dir > 0 ? (start >= N - n ? 0 : Math.min(start + n, N - n)) : (start === 0 ? N - n : Math.max(0, start - n));
    if (to === start) return;
    busy = true;
    start = to;
    label();
    const order = btns.slice(0, n).map((b, k) => [b, k]);
    if (dir < 0) order.reverse();
    try { await Promise.all(order.map(([b, k], step) => swap(b, start + k, step * (key === "hunt" ? 200 : 120)))); }
    finally {
      busy = false;
      if (queued) { const d = queued; queued = 0; go(d); }
    }
  };
  $$(".krug__nav", box).forEach((b) => b.addEventListener("click", () => go(Number(b.dataset.dir))));
  // свайп вбок листает; если палец шёл больше вниз/вверх — это прокрутка сайта, фото не трогаем
  let tx = null, ty = 0;
  row.addEventListener("touchstart", (e) => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  row.addEventListener("touchend", (e) => {
    if (tx === null) return;
    const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    tx = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.2) go(dx < 0 ? 1 : -1);
  }, { passive: true });
  row.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") go(1); if (e.key === "ArrowLeft") go(-1); });
  fit();
  let fitT;
  new ResizeObserver(() => { clearTimeout(fitT); fitT = setTimeout(fit, 150); }).observe(row);
};
$$(".krug.is-board").forEach((box) => boardUp(box, box === huntKrug ? drawKrug : null));
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
    [".ev-head__plate", "stamp"], [".ev-head__date", "pop"], [".ev-head__sub, .ev-head__acts", "up"],
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
const ORG = {"h": [["h-01", 0], ["h-02", 0], ["h-03", 0], ["h-10", 0]], "p": [["p-01", 0], ["p-02", 0], ["p-04", 0], ["p-06", 0]]};
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
  let sx = null, sy = 0;
  lb.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (sx === null) return;
    const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    sx = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) lbShow(lbIdx + (dx < 0 ? 1 : -1));
  }, { passive: true });
}

// Main Event: «vs» в подписи пары — красным
$$(".slide figcaption b:not(.nicks)").forEach((b) => { b.innerHTML = b.textContent.replace(/ vs /i, " <i>vs</i> "); });
// Список ников через «·»: точка, оказавшаяся в начале строки после переноса, прячется
const nickSeps = () => $$(".nicks").forEach((b) => {
  const items = $$("span", b);
  items.forEach((s) => { const i = $("i", s); if (i) i.hidden = false; });
  items.forEach((s, k) => { const i = $("i", s); if (i && k && s.offsetTop > items[k - 1].offsetTop + 4) i.hidden = true; });
});
document.fonts.ready.then(nickSeps);
$$(".nicks").forEach((b) => new ResizeObserver(nickSeps).observe(b));

// v38 Фильтры сезонов. HUNT: виньетка по краям экрана, пока HUNT в кадре (только ПК)
{
  const vig = $(".fx-vig"), ev = $("#event");
  if (vig && ev) new IntersectionObserver(([e]) => vig.classList.toggle("on", e.isIntersecting && e.intersectionRatio > .12), { threshold: [0, .12, .3] }).observe(ev);
}
// BTB: хроматическая аберрация — при появлении блока каналы разъехались и оседают до едва заметной (на телефоне сразу слабая)
{
  const groups = { title: ".btb__title", poster: ".btb .season__poster", tiles: ".btb .vbox", moments: ".moments--btb", krug: ".krug--btb" };
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
