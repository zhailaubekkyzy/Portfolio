// ProjectPro demo accounts. The case gives only segment totals; this generator builds 2 045 accounts
// that add up EXACTLY to those totals (base, new, churned per segment, 60/40 usage split among churned).
// Everything below the totals (names, months, seats, health, reasons, per-segment usage split) is a demo assumption.
function simulateProjectPro(opt) {
  opt = opt || {};
  let s = 20261029;
  const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  const pick = a => a[Math.floor(rnd() * a.length)];
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const SEG = [
    { key: "st", base: 850, neu: 425, churn: 468, price: 2400, emp: [3, 20], basicChurn: 290, fullRet: 0.55 },
    { key: "mb", base: 420, neu: 168, churn: 134, price: 9600, emp: [21, 100], basicChurn: 74, fullRet: 0.7 },
    { key: "co", base: 130, neu: 52, churn: 23, price: 36000, emp: [101, 1500], basicChurn: 11, fullRet: 0.82 }
  ];
  // demo assumption: share of the churned who joined this same year (the case does not say) — adjustable on the page
  const NEW_SHARE = opt.newShare != null ? opt.newShare : 0.2;
  const A = ["Nova", "Blue", "Peak", "Kite", "Orbit", "Cedar", "Pixel", "Atlas", "North", "Sky", "Lumen", "Delta", "Echo", "Vertex", "Prime", "Bright", "Iron", "Silver", "Green", "Swift", "Polar", "Urban", "Quant", "Terra", "Nimbus", "Zen", "Bold", "Clear", "Sun", "Wave"];
  const B = ["Labs", "Works", "Studio", "Systems", "Digital", "Group", "Logic", "Soft", "Media", "Tech", "Partners", "Build", "Cloud", "Data", "Solutions", "Ventures", "Craft", "Hub", "Line", "Point"];
  const IND = 6; // industries: 0 IT, 1 agency, 2 e-com, 3 construction, 4 education, 5 finance
  // churn reasons (demo): 0 no value reached / didn't onboard, 1 price, 2 competitor, 3 missing feature, 4 company closed, 5 team/process change
  const reasonFor = (seg, full) => {
    const r = rnd();
    if (!full) {
      if (seg === 0) return r < .55 ? 0 : r < .75 ? 4 : r < .9 ? 1 : 5;
      return r < .7 ? 0 : r < .85 ? 1 : 5;
    }
    if (seg === 0) return r < .35 ? 4 : r < .6 ? 1 : r < .8 ? 2 : 3;
    return r < .35 ? 2 : r < .65 ? 3 : r < .85 ? 1 : 5;
  };

  const acc = [];
  const used = new Set();
  const name = () => { let n; do { n = pick(A) + " " + pick(B); } while (used.has(n) && used.size < A.length * B.length); used.add(n); return n; };

  SEG.forEach((g, si) => {
    const churnNew = Math.round(g.churn * NEW_SHARE);
    const churnBase = g.churn - churnNew;
    // which churned accounts are "basic only": exactly g.basicChurn of them
    const basicFlags = shuffle(Array.from({ length: g.churn }, (_, k) => k < g.basicChurn));
    let ck = 0;
    const mk = (cohort, churned) => {
      const emp = Math.round(g.emp[0] + Math.pow(rnd(), 1.6) * (g.emp[1] - g.emp[0]));
      const full = churned ? !basicFlags[ck++] : rnd() < g.fullRet;
      const joinM = cohort === 0 ? -1 - Math.floor(rnd() * 34) : Math.floor(rnd() * 12); // base: months before the year (up to ~3 years); new: 0..11
      const renewM = cohort === 0 ? Math.floor(rnd() * 12) : -1;
      const churnM = churned ? (cohort === 0 ? renewM : Math.min(11, joinM + 1 + Math.floor(rnd() * Math.max(1, 11 - joinM)))) : -1;
      const keyUsed = full ? 5 + Math.floor(rnd() * 3) : 1 + Math.floor(rnd() * 2); // of 7 key features
      const seatsPaid = Math.max(2, Math.round(emp * (0.35 + rnd() * 0.5)));
      let act = churned ? 0.15 + rnd() * 0.35 : 0.45 + rnd() * 0.5;
      if (full) act = Math.min(0.98, act + 0.12);
      const seatsUsed = Math.max(1, Math.round(seatsPaid * act));
      const lastLogin = churned ? 20 + Math.floor(rnd() * 60) : Math.floor(Math.pow(rnd(), 2) * (full ? 10 : 30));
      const health = Math.round(Math.max(5, Math.min(98, keyUsed / 7 * 45 + (seatsUsed / seatsPaid) * 35 + (1 - Math.min(lastLogin, 60) / 60) * 20 + (rnd() - .5) * 8)));
      const tickets = Math.floor(rnd() * (churned ? 8 : 5));
      acc.push({
        seg: si, name: name(), ind: Math.floor(rnd() * IND), emp, cohort, joinM, renewM, churned, churnM, full,
        keyUsed, seatsPaid, seatsUsed, lastLogin, health, tickets, price: g.price,
        reason: churned ? reasonFor(si, full) : -1, csm: si === 2 && rnd() < 0.35 // demo: only some corporates have a CSM today
      });
    };
    for (let k = 0; k < g.base; k++) mk(0, k < churnBase);
    for (let k = 0; k < g.neu; k++) mk(1, k < churnNew);
  });
  shuffle(acc);
  acc.forEach((a, i) => a.id = "PP-" + String(1001 + i));
  return { acc, SEG, NEW_SHARE };
}
