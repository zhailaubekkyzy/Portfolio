/* Demo data generator for the SmartFlow RFM dashboard.
   Deterministic: same seed → same 12 months of data. Simulates 24 months (12 warm-up + 12 shown). */
function simulate() {
  let s = 20261023;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const gauss = () => { let u = 0, v = 0; while (u === 0) u = rnd(); v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const DAY = 86400000;
  const START = Date.UTC(2024, 9, 1);
  const END = Date.UTC(2026, 8, 30, 23, 59);
  const CHANGE = Date.UTC(2026, 6, 20);
  const NICHES = [
    { id: "edu", name: "Онлайн-образование", w: .35, check: 22000, gap: 26 },
    { id: "health", name: "Здоровье и спорт", w: .25, check: 15000, gap: 20 },
    { id: "biz", name: "Бизнес и маркетинг", w: .25, check: 29000, gap: 33 },
    { id: "hobby", name: "Творчество и хобби", w: .15, check: 12000, gap: 22 }
  ];
  const CHANNELS = [
    { id: "ig", name: "Instagram", w: .40, k: 1.0 },
    { id: "tg", name: "Telegram", w: .30, k: 1.12 },
    { id: "tt", name: "TikTok", w: .20, k: .72 },
    { id: "ref", name: "Рекомендации", w: .10, k: 1.3 }
  ];
  const TYPES = [{ w: .16, p: .8, c: 1.15 }, { w: .34, p: .45, c: 1 }, { w: .5, p: .2, c: .92 }];
  const SEASON = [1.06, 1.02, 1.0, 1.08, 1.03, 1.0, .98, .97, .94, .92, .95, 1.06]; // Jan..Dec
  const pick = arr => { let r = rnd(), a = 0; for (let i = 0; i < arr.length; i++) { a += arr[i].w; if (r < a) return i; } return arr.length - 1; };

  const customers = [];
  for (let mi = 0; mi < 24; mi++) {
    const y = 2024 + Math.floor((9 + mi) / 12), mo = (9 + mi) % 12;
    const m0 = Date.UTC(y, mo, 1), m1 = Date.UTC(y, mo + 1, 1);
    const n = Math.round(3300 * SEASON[mo] * (1 + .03 * (rnd() * 2 - 1)));
    for (let i = 0; i < n; i++) {
      const ni = pick(NICHES), ch = pick(CHANNELS), ty = pick(TYPES);
      const N = NICHES[ni], T = TYPES[ty];
      let t = m0 + rnd() * (m1 - m0);
      const orders = [];
      for (let k = 0; k < 40; k++) {
        const amt = Math.round(N.check * T.c * Math.exp(.35 * gauss() - .06) / 100) * 100;
        orders.push([t, amt]);
        let p = T.p * CHANNELS[ch].k * Math.pow(.93, k);
        if (t >= CHANGE) p *= (k === 0 ? .66 : .88);
        if (rnd() > Math.min(p, .95)) break;
        t += N.gap * Math.exp(.6 * gauss()) * DAY;
        if (t > END) break;
      }
      customers.push({ ni, ch, ty, orders });
    }
  }
  return { customers, NICHES, CHANNELS, START, END, CHANGE, DAY };
}
if (typeof module !== "undefined") module.exports = { simulate };
