/* Demo-data generator for the BookLover retention CRM.
   Deterministic (fixed seed). Every user of the six cohorts in the course brief is simulated,
   and the totals are pinned to the brief exactly:
   sign-ups 12/15/18/22/25/27 thousand, active on day 30: 5 400 / 6 750 / 8 100 / 8 360 / 7 500 / 7 560,
   65% finished a first book, 30% of finishers started a second one.
   Channels, platforms, app versions, genres, ratings and spend are invented to illustrate the case. */
function simulateBooklover() {
  let s = 20261027;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const gauss = () => { let u = 0; while (u === 0) u = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rnd()); };

  const NEW = [12000, 15000, 18000, 22000, 25000, 27000];
  const ACT = [5400, 6750, 8100, 8360, 7500, 7560];
  const DAYS = [31, 28, 31, 30, 31, 30];
  const FIN_SHARE = 0.65, SEC_SHARE = 0.30;

  // id, retention effect (logit), finish weight, second-book weight, CAC in tenge, core channel?
  const CHANNELS = [
    { id: "org", w: 0.15, f: 1.05, s: 1.05, cac: 0, core: 1 },
    { id: "ref", w: 0.40, f: 1.10, s: 1.15, cac: 300, core: 1 },
    { id: "ig", w: -0.20, f: 1.00, s: 1.00, cac: 900, core: 1 },
    { id: "tg", w: 0.02, f: 1.05, s: 1.05, cac: 650, core: 1 },
    { id: "tt", w: -2.3, f: 0.62, s: 0.70, cac: 450, core: 0 },
    { id: "promo", w: -3.4, f: 0.38, s: 0.55, cac: 250, core: 0 }
  ];
  // users per channel per month (thousands), sums equal NEW
  const MIX = [
    [4.4, 1.8, 3.6, 2.2, 0, 0],
    [5.4, 2.3, 4.6, 2.7, 0, 0],
    [6.4, 2.8, 5.6, 3.2, 0, 0],
    [6.6, 2.9, 5.7, 3.3, 2.3, 1.2],
    [6.7, 2.9, 5.8, 3.3, 3.6, 2.7],
    [6.8, 3.0, 5.8, 3.4, 4.5, 3.5]
  ];
  // genres: id, share, second-book weight (series genres continue more)
  const GENRES = [
    { id: "fantasy", w: .22, s: 1.35 }, { id: "romance", w: .18, s: 1.25 }, { id: "fiction", w: .20, s: .95 },
    { id: "business", w: .16, s: .75 }, { id: "selfhelp", w: .14, s: .7 }, { id: "classics", w: .10, s: .85 }
  ];
  // versions: 0 = v1.8 (Jan–Mar), 1 = v1.9 (Apr 1 – May 5), 2 = v2.0 (from May 6, new reader + paywall)
  const VERSIONS = ["1.8", "1.9", "2.0"];
  const V2_DAY = 31 + 28 + 31 + 30 + 5; // day index of May 6, counting Jan 1 as 0

  const N = NEW.reduce((a, b) => a + b, 0);
  const month = new Uint8Array(N), day = new Uint8Array(N), ch = new Uint8Array(N), plat = new Uint8Array(N),
    ver = new Uint8Array(N), genre = new Uint8Array(N), life = new Uint8Array(N), fin = new Uint8Array(N),
    finDay = new Uint8Array(N), sec = new Uint8Array(N), rating = new Uint8Array(N), minutes = new Uint16Array(N);
  const intent = new Float32Array(N), zAct = new Float32Array(N);

  const pickW = (arr, key) => { let r = rnd() * arr.reduce((a, x) => a + x[key], 0), a = 0; for (let i = 0; i < arr.length; i++) { a += arr[i][key]; if (r < a) return i; } return arr.length - 1; };

  // systematic sampling: picks exactly round(sum p) items with inclusion probability p (after scaling to target)
  function pickExact(idx, weight, target, out) {
    let lo = 0, hi = 50;
    const sumAt = k => { let t = 0; for (const i of idx) t += Math.min(1, k * weight[i]); return t; };
    for (let it = 0; it < 60; it++) { const mid = (lo + hi) / 2; if (sumAt(mid) < target) lo = mid; else hi = mid; }
    const k = hi;
    const order = idx.slice();
    for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = order[i]; order[i] = order[j]; order[j] = t; }
    let acc = rnd(), picked = 0;
    for (const i of order) {
      const p = Math.min(1, k * weight[i]);
      const before = Math.floor(acc); acc += p;
      if (Math.floor(acc) > before && picked < target) { out[i] = 1; picked++; }
    }
    // rounding guard: top up deterministically if one short
    for (let j = 0; picked < target && j < order.length; j++) if (!out[order[j]]) { out[order[j]] = 1; picked++; }
    return k;
  }

  // same idea on the logit scale: shift a so the expected count hits the target, then systematic sampling
  function pickLogit(idx, z, target, out) {
    const sig = x => 1 / (1 + Math.exp(-x));
    let lo = -12, hi = 12;
    for (let it = 0; it < 60; it++) { const mid = (lo + hi) / 2; let t = 0; for (const i of idx) t += sig(mid + z[i]); if (t < target) lo = mid; else hi = mid; }
    const order = idx.slice();
    for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = order[i]; order[i] = order[j]; order[j] = t; }
    let acc = rnd(), picked = 0;
    for (const i of order) { const before = Math.floor(acc); acc += sig(hi + z[i]); if (Math.floor(acc) > before && picked < target) { out[i] = 1; picked++; } }
    for (let j = 0; picked < target && j < order.length; j++) if (!out[order[j]]) { out[order[j]] = 1; picked++; }
  }

  let id = 0, dayOffset = 0;
  const byMonth = [];
  for (let m = 0; m < 6; m++) {
    const ids = [];
    MIX[m].forEach((k, c) => {
      const n = Math.round(k * 1000);
      for (let i = 0; i < n; i++) {
        month[id] = m; ch[id] = c;
        day[id] = Math.floor(rnd() * DAYS[m]);
        const absDay = dayOffset + day[id];
        plat[id] = rnd() < 0.62 ? 1 : 0; // 1 = Android, 0 = iOS
        ver[id] = absDay >= V2_DAY ? 2 : m >= 3 ? 1 : 0;
        genre[id] = pickW(GENRES, "w");
        const g = gauss();
        intent[id] = Math.exp(0.55 * g);
        let z = CHANNELS[c].w + 0.8 * g;
        if (ver[id] === 1) z -= 0.05;
        if (ver[id] === 2 && plat[id] === 1) z -= 0.6; // v2.0 Android reader regression
        zAct[id] = z;
        ids.push(id); id++;
      }
    });
    byMonth.push(ids);
    dayOffset += DAYS[m];
  }

  // D30 activity: exact per cohort
  const act = new Uint8Array(N);
  byMonth.forEach((ids, m) => pickLogit(ids, zAct, ACT[m], act));

  // lifetime in days: 30 = still active on day 30; churners leave earlier
  for (let i = 0; i < N; i++) {
    if (act[i]) { life[i] = 30; continue; }
    const coreBoost = CHANNELS[ch[i]].core ? 1 : 0.45;
    const mean = 7 * coreBoost * Math.min(2, intent[i]);
    let d = Math.floor(-Math.log(1 - rnd()) * mean);
    if (rnd() < (CHANNELS[ch[i]].core ? 0.18 : 0.42)) d = 0; // never came back after day 0
    life[i] = Math.min(29, d);
  }

  // first book finished: 65% of all users, linked to lifetime and channel
  const all = Array.from({ length: N }, (_, i) => i);
  const wFin = new Float32Array(N);
  for (let i = 0; i < N; i++) wFin[i] = CHANNELS[ch[i]].f * (0.25 + life[i] / 30) * Math.sqrt(intent[i]);
  pickExact(all, wFin, Math.round(N * FIN_SHARE), fin);
  for (let i = 0; i < N; i++) if (fin[i]) finDay[i] = Math.max(1, Math.min(life[i] || 3, Math.round(3 + rnd() * 12)));

  // second book started within 7 days of finishing: 30% of finishers
  const finIds = all.filter(i => fin[i]);
  const wSec = new Float32Array(N);
  for (const i of finIds) wSec[i] = CHANNELS[ch[i]].s * GENRES[genre[i]].s * (0.35 + life[i] / 30) * intent[i];
  pickExact(finIds, wSec, Math.round(finIds.length * SEC_SHARE), sec);

  // reading minutes in the first 30 days
  for (let i = 0; i < N; i++) {
    const base = 12 * (life[i] + 1) * (0.6 + 0.4 * intent[i]) * (fin[i] ? 1.5 : 0.8) * (sec[i] ? 1.3 : 1);
    minutes[i] = Math.min(4000, Math.round(base * Math.exp(0.3 * gauss())));
  }

  // store ratings: about 8% of users rate
  for (let i = 0; i < N; i++) {
    if (rnd() > 0.08) continue;
    let x = 4.61 + (act[i] ? 0.28 : 0) - (life[i] < 3 && !act[i] ? 0.5 : 0)
      - (ch[i] === 5 ? 0.9 : ch[i] === 4 ? 0.3 : 0)
      - (ver[i] === 2 && plat[i] === 1 ? 0.22 : 0) + 0.55 * gauss();
    rating[i] = Math.max(1, Math.min(5, Math.round(x)));
  }

  return { N, NEW, ACT, DAYS, CHANNELS, MIX, GENRES, VERSIONS, month, day, ch, plat, ver, genre, life, fin, finDay, sec, rating, minutes };
}
if (typeof module !== "undefined") module.exports = { simulateBooklover };
