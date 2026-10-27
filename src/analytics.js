/* Analytics for the dashboard. Same definitions as the Excel workbook. */
function buildBase(D) {
  const DAY = 86400000, dayOf = t => Math.floor(t / DAY);
  const W0 = dayOf(Date.UTC(2025, 9, 1)), W1 = dayOf(Date.UTC(2026, 8, 30));
  const MONTHS = [];
  for (let k = 0; k < 12; k++) MONTHS.push({ start: dayOf(Date.UTC(2025, 9 + k, 1)), end: dayOf(Date.UTC(2025, 10 + k, 1)) - 1, y: 2025 + Math.floor((9 + k) / 12), m: (9 + k) % 12 });
  const monthIdx = d => { for (let i = 0; i < 12; i++) if (d >= MONTHS[i].start && d <= MONTHS[i].end) return i; return -1; };
  const people = [];
  for (const c of D.customers) {
    const all = c.orders.map(o => [dayOf(o[0]), o[1]]);
    people.push({ ni: c.ni, ch: c.ch, all, first: all[0][0], win: all.filter(o => o[0] >= W0 && o[0] <= W1) });
  }
  return { people, W0, W1, MONTHS, monthIdx, CHANGE: dayOf(Date.UTC(2026, 6, 20)), NICHES: D.NICHES, CHANNELS: D.CHANNELS };
}

const TH = { R: 60, F: 3, M: 41400 };
const SEGS = ["champ", "loyal", "risk", "hib"];
function segOf(R, F) { return R <= TH.R ? (F >= TH.F ? "champ" : "loyal") : (F >= TH.F ? "risk" : "hib"); }

function analyze(B, filt) {
  const P = B.people.filter(p => (filt.ni < 0 || p.ni === filt.ni) && (filt.ch < 0 || p.ch === filt.ch));
  const { W0, W1, MONTHS, monthIdx } = B;
  // monthly
  const mon = MONTHS.map(() => ({ orders: 0, rev: 0, nw: 0, buyers: 0, cohort: 0, rep30n: 0, rep30d: 0 }));
  // cohorts
  const coh = MONTHS.map(() => ({ size: 0, act: new Array(12).fill(0), rev: new Array(12).fill(0) }));
  const seg = {}; SEGS.forEach(s => seg[s] = { n: 0, M: 0, F: 0, R: 0, hi: 0, hiM: 0 });
  const gaps = [], Fs = [], Ms = [];
  const grid = {}; // R bin x F bin
  const RB = [30, 60, 120, 240, 365], FB = [1, 2, 4, 7, 999];
  const rbin = r => RB.findIndex(x => r <= x), fbin = f => FB.findIndex(x => f <= x);
  const diag = { ch: {}, ni: {} };
  const ttsBefore = new Array(19).fill(0), ttsAfter = new Array(19).fill(0);
  let totalRev = 0;
  for (const p of P) {
    const w = p.win;
    // monthly
    let lastM = -1;
    w.forEach(o => {
      const mi = monthIdx(o[0]); const M = mon[mi];
      M.orders++; M.rev += o[1]; totalRev += o[1];
      if (o[0] === p.first && o === w[0]) M.nw++;
      if (mi !== lastM) { M.buyers++; lastM = mi; }
    });
    // cohort
    if (p.first >= W0) {
      const c = monthIdx(p.first); const C = coh[c]; C.size++;
      const seen = new Set();
      w.forEach(o => { const k = monthIdx(o[0]) - c; C.rev[k] += o[1]; if (!seen.has(k)) { seen.add(k); C.act[k]++; } });
      if (p.first <= W1 - 30) {
        const r = w.length >= 2 && w[1][0] - w[0][0] <= 30 ? 1 : 0;
        mon[c].rep30d++; mon[c].rep30n += r;
        const per = (c >= 5 && c <= 8) ? "before" : c === 10 ? "after" : null; // Mar–Jun vs Aug
        if (per) {
          for (const [key, v] of [["ch", p.ch], ["ni", p.ni]]) {
            const o = diag[key][v] || (diag[key][v] = { before: [0, 0], after: [0, 0] });
            o[per][0] += r; o[per][1]++;
          }
        }
      }
      if (w.length >= 2) {
        const g = w[1][0] - w[0][0], b = Math.min(18, Math.floor(g / 5));
        if (c >= 5 && c <= 8) ttsBefore[b]++; else if (c === 10) ttsAfter[b]++;
      }
    }
    // RFM at W1
    if (w.length) {
      const R = W1 - w[w.length - 1][0], F = w.length, M = w.reduce((a, o) => a + o[1], 0);
      const s = segOf(R, F); const S = seg[s];
      S.n++; S.M += M; S.F += F; S.R += R; if (M >= TH.M) { S.hi++; S.hiM += M; }
      Fs.push(F); Ms.push(M); if (F >= 2) gaps.push(w[1][0] - w[0][0]);
      const key = rbin(R) + "_" + fbin(F); const g = grid[key] || (grid[key] = { n: 0, M: 0 }); g.n++; g.M += M;
    }
  }
  // migration Jul 31 → Sep 30
  const T0 = W1 - 61; // 2026-07-31
  const mig = {};
  const st0 = p => {
    if (p.first > T0) return "new";
    const w = p.all.filter(o => o[0] > T0 - 365 && o[0] <= T0);
    if (!w.length) return null;
    return segOf(T0 - w[w.length - 1][0], w.length);
  };
  for (const p of P) {
    const a = st0(p); if (!a) continue;
    const b = p.win.length ? segOf(W1 - p.win[p.win.length - 1][0], p.win.length) : "gone";
    const k = a + ">" + b; mig[k] = (mig[k] || 0) + 1;
  }
  Fs.sort((a, b) => a - b); Ms.sort((a, b) => a - b); gaps.sort((a, b) => a - b);
  const q = (arr, p) => arr.length ? arr[Math.min(arr.length - 1, Math.floor((arr.length - 1) * p))] : 0;
  const fCond = []; for (let n = 1; n <= 7; n++) { const a = Fs.filter(f => f >= n).length, b = Fs.filter(f => f >= n + 1).length; fCond.push({ n, a, b, p: a ? b / a : 0 }); }
  const gapHist = new Array(25).fill(0); gaps.forEach(g => gapHist[Math.min(24, Math.floor(g / 5))]++);
  return { gapHist, n: P.length, mon, coh, seg, totalRev, grid, RB, FB, diag, ttsBefore, ttsAfter, mig,
    gapMed: q(gaps, .5), gapP90: q(gaps, .9), mMed: q(Ms, .5), mP75: q(Ms, .75), fCond, buyers: Fs.length };
}
if (typeof module !== "undefined") module.exports = { buildBase, analyze, TH, SEGS };
