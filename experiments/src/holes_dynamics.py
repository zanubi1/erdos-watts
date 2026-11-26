"""Holes dynamics for the Watts greedy sequence (OEIS A055265).

A hole at time n is a value v <= n with v not in {a(1..n)}; H(n) = number of holes.
Notation (all exact, computed from the sequence):
  fi(v)   first index of v (N+1 if unseen within N terms)
  L(v)    = fi(v) - v (lifetime when positive)
  s(v)    = max{ fi(w) : w < v, w = v mod 2 }  (time at which v becomes the frontier of its parity)
  T0(v)   = max(s(v), v): start of the "frontier hole" period of v
  M(n)    = max a(1..n), u(n) = smallest unused value at time n
Note a(n) = n (mod 2) (L001 with a(1)=1), so the fill at step n+1 and the creation of
the hole n+1 concern the same parity class.

Sections:
  flow       Delta H, creation/fill rates, drift conditional on H and per parity
  life       lifetime distribution and relation to prime gaps near 2v
  frontier   frontier-hole waits, partner counts, exact fill-by-first-partner check
  pairs      mutual blocking pairs (v+w prime, opposite parity, coexisting holes)
  queue      why a hole survives a step: composite sum vs stolen by a smaller hole
  graph      fill runs as greedy walks on the prime-sum graph of holes; control for prime-sum-freeness\n  bounds     candidate bounds H(n) vs prime gaps near 2n

Usage:
  python experiments/src/holes_dynamics.py [--seq PATH] [--terms N] [--sections flow,life,...]
          [--plots DIR]
"""
import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_SEQ = "/home/user/erdos-watts/experiments/results/overshoot_1e7/sequence.npy"
REF = [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15, 14, 17, 12, 11, 18, 19, 22]


def sieve(limit):
    is_p = np.ones(limit + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i:: i] = False
    return is_p


def pct(x, qs=(50, 90, 99, 99.9, 100)):
    if len(x) == 0:
        return "n/a"
    return ", ".join(f"p{q}={np.percentile(x, q):.0f}" for q in qs)


class Data:
    def __init__(self, a):
        N = len(a)
        self.N = N
        self.a = a  # a[k-1] = a(k)
        self.k = np.arange(1, N + 1, dtype=np.int64)
        M = int(a.max())
        self.M = M
        fi = np.full(M + 3, N + 1, dtype=np.int64)
        fi[a] = self.k
        fi[0] = 0
        self.fi = fi
        lim = 2 * M + 4000
        self.isp = sieve(lim)
        idx = np.arange(lim + 1)
        pr = np.where(self.isp, idx, -1)
        self.prevp = np.maximum.accumulate(pr)  # largest prime <= x
        nx = np.where(self.isp, idx, lim + 10)
        self.nextp = np.minimum.accumulate(nx[::-1])[::-1]  # smallest prime >= x
        self.primes = np.flatnonzero(self.isp)
        # H(n), n=1..N : change at n = [fi(n) > n] - [a(n) < n]
        fiv = fi[1: N + 1]
        self.created = fiv > self.k  # value n is a hole at time n
        self.fill = a < self.k  # step n fills a hole (a(n) <= n-1)
        self.H = np.cumsum(self.created.astype(np.int64) - self.fill.astype(np.int64))
        par = self.k & 1
        self.He = np.cumsum(((self.created & (par == 0)).astype(np.int64) - (self.fill & (par == 0)).astype(np.int64)))
        self.Ho = self.H - self.He
        # check identity C008(i) H(X) = #{k <= X : a(k) > X}
        HA = np.cumsum((a > self.k).astype(np.int64) - (fiv < self.k).astype(np.int64))
        assert np.array_equal(HA, self.H)
        # running max and smallest unused
        self.Mrun = np.maximum.accumulate(a)  # Mrun[n-1] = M(n)
        P = np.maximum.accumulate(fi[1:])  # P[v-1] = max_{w<=v} fi(w)
        self.Pmax = P
        # s(v) per parity
        s = np.zeros(M + 3, dtype=np.int64)
        for p in (0, 1):
            vals = np.arange(2 if p == 0 else 1, M + 3, 2)
            f = fi[vals]
            pm = np.maximum.accumulate(f)
            s[vals[1:]] = pm[:-1]
            s[vals[0]] = 0
        self.s = s

    def u(self, T):
        """smallest unused value at time T (vectorized)."""
        return np.searchsorted(self.Pmax, T, side="right") + 1

    def Mof(self, T):
        T = np.asarray(T)
        return np.where(T >= 1, self.Mrun[np.maximum(T, 1) - 1], 0)

    def holes_at(self, n):
        u = int(self.u(n))
        vs = np.arange(u, n + 1)
        return vs[self.fi[vs] > n]


# ---------------------------------------------------------------- flow
def sec_flow(D, out):
    N = D.N
    H = D.H
    k = D.k
    # step n -> n+1 for n = 1..N-1
    cr = D.created[1:].astype(np.int64)  # [n+1 is a hole at time n+1]
    fl = D.fill[1:].astype(np.int64)  # [a(n+1) <= n]
    dH = cr - fl
    assert np.array_equal(dH, np.diff(H))
    Hn = H[:-1]
    out.append("## 1. Flow")
    out.append(f"steps n->n+1, n=1..{N-1:,}")
    out.append(f"creation rate P(n+1 not used at step n+1) = {cr.mean():.5f}")
    out.append(f"fill rate     P(a(n+1) <= n)               = {fl.mean():.5f}")
    fix = (D.a[1:] == k[1:]).mean()
    out.append(f"P(a(n+1) = n+1) = {fix:.5f}; P(a(n+1) > n+1) = {(D.a[1:] > k[1:]).mean():.5f}")
    out.append(f"P(created and filled same step) = {(cr & fl).mean():.5f}")
    out.append(f"mean H over n<=N: {H.mean():.3f}; max H {H.max()} at n={int(np.argmax(H))+1:,}")
    for lo, hi in [(1, 10**5), (10**5, 10**6), (10**6, 10**7)]:
        sl = slice(lo - 1, min(hi, N) - 1)
        out.append(f"  n in [{lo:.0e},{hi:.0e}): creation {cr[sl].mean():.4f}, fill {fl[sl].mean():.4f}, mean H {Hn[sl].mean():.2f}")
    out.append("")
    out.append("### Drift conditional on H(n) = h (n >= 10^5)")
    out.append("| h | #n | E[dH] | P(fill) | P(create) | P(fill | next step's parity class has h_pi holes = h) | E[dH_pi | H_pi=h] |")
    out.append("|---|---|---|---|---|---|---|")
    sel = k[:-1] >= 10**5
    # parity-class count of the class touched at step n+1 (parity of n+1)
    par_next = (k[:-1] + 1) & 1
    Hpi = np.where(par_next == 0, D.He[:-1], D.Ho[:-1])
    for h in range(0, int(H.max()) + 1):
        m = sel & (Hn == h)
        mp = sel & (Hpi == h)
        if m.sum() == 0 and mp.sum() == 0:
            continue
        e = dH[m].mean() if m.sum() else float("nan")
        pf = fl[m].mean() if m.sum() else float("nan")
        pc = cr[m].mean() if m.sum() else float("nan")
        pfp = fl[mp].mean() if mp.sum() else float("nan")
        edp = dH[mp].mean() if mp.sum() else float("nan")
        out.append(f"| {h} | {int(m.sum()):,} | {e:+.4f} | {pf:.4f} | {pc:.4f} | {pfp:.4f} (#{int(mp.sum()):,}) | {edp:+.4f} |")
    out.append("")
    # coarse bins
    out.append("### Coarse bins (n >= 10^5)")
    out.append("| H bin | #n | E[dH] | P(fill) |  E[dH_pi | H_pi in bin] |")
    out.append("|---|---|---|---|---|")
    for lo, hi in [(0, 4), (4, 8), (8, 12), (12, 16), (16, 20), (20, 25), (25, 30), (30, 40), (40, 60)]:
        m = sel & (Hn >= lo) & (Hn < hi)
        mp = sel & (Hpi >= lo) & (Hpi < hi)
        if m.sum() == 0:
            continue
        edp = dH[mp].mean() if mp.sum() else float("nan")
        out.append(f"| [{lo},{hi}) | {int(m.sum()):,} | {dH[m].mean():+.4f} | {fl[m].mean():.4f} | {edp:+.4f} (#{int(mp.sum()):,}) |")
    out.append("")
    # excursions: lengths of runs with H >= h0
    out.append("### Excursions above level h0 (all n): number, max duration, max height")
    out.append("| h0 | #excursions | max duration | median duration |")
    out.append("|---|---|---|---|")
    for h0 in (10, 20, 30, 40):
        above = (H >= h0).astype(np.int8)
        d = np.diff(np.concatenate([[0], above, [0]]))
        st = np.flatnonzero(d == 1)
        en = np.flatnonzero(d == -1)
        dur = en - st
        if len(dur):
            out.append(f"| {h0} | {len(dur):,} | {dur.max():,} | {np.median(dur):.0f} |")
    out.append("")
    return dict(dH=dH, Hpi=Hpi)


# ---------------------------------------------------------------- life
def sec_life(D, out, plots=None):
    N = D.N
    fi = D.fi
    Nv = N - 5000
    v = np.arange(1, Nv + 1)
    L = fi[v] - v
    assert (fi[v] <= N).all(), "censoring: some v <= N-5000 unseen"
    out.append("## 2. Lifetimes L(v) = fi(v) - v, v <= N - 5000")
    out.append(f"P(L>0) = {(L>0).mean():.4f}, P(L=0) = {(L==0).mean():.4f}, P(L<0) = {(L<0).mean():.4f}")
    Lp = L[L > 0]
    out.append(f"positive L: mean {Lp.mean():.2f}, {pct(Lp)}")
    out.append(f"sum of positive L over v<=Nv = {Lp.sum():,} = sum_n H(n) check: {D.H[:Nv].sum():,} (diff due to boundary)")
    out.append("")
    out.append("### Distribution of positive L")
    out.append("| L range | count | fraction of holes |")
    out.append("|---|---|---|")
    for lo, hi in [(1, 2), (2, 5), (5, 10), (10, 20), (20, 50), (50, 100), (100, 150), (150, 200), (200, 250), (250, 400)]:
        c = int(((Lp >= lo) & (Lp < hi)).sum())
        out.append(f"| [{lo},{hi}) | {c:,} | {c/len(Lp):.2e} |")
    out.append("")
    out.append("tail: P(L >= x) for x = 10,20,40,80,160: " + ", ".join(f"{(Lp>=x).mean():.2e}" for x in (10, 20, 40, 80, 160)))
    out.append("")
    # prime structure near 2v
    twov = 2 * v
    pplus = D.nextp[twov + 1]  # smallest prime > 2v
    pminus = D.prevp[twov]  # largest prime <= 2v
    gap_c = pplus - pminus  # gap containing 2v
    # fill prime: q = v + a(fi(v)-1)
    hv = v[L > 0]
    Lh = L[L > 0]
    partner = D.a[fi[hv] - 2]
    qf = hv + partner
    assert D.isp[qf].all()
    # max gap with an endpoint in window [2v - W, 2v + W]
    def maxgap_window(x, W):
        pr = D.primes
        gaps = np.diff(pr)
        # index of first prime >= x-W and last prime <= x+W
        i0 = np.searchsorted(pr, x - W, side="left")
        i1 = np.searchsorted(pr, x + W, side="right") - 1
        # max of gaps[i0-1 .. i1] (gaps straddling the window boundaries included)
        # use sparse table
        return range_max(gaps, np.maximum(i0 - 1, 0), np.minimum(i1, len(gaps) - 1))
    st = build_sparse(np.diff(D.primes))
    global _ST
    _ST = st
    out.append("### Max lifetime per range of v, with prime gaps at 2v")
    out.append("| v range | #holes | max L | v at max | gap containing 2v | nextprime(2v)-2v | fill prime q - 2v | max gap in [2v-300, 2v+300] | p99 L |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    edges = [1, 10**3, 10**4, 10**5, 10**6, 2 * 10**6, 4 * 10**6, 6 * 10**6, 8 * 10**6, Nv + 1]
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (hv >= lo) & (hv < hi)
        if not m.any():
            continue
        j = np.flatnonzero(m)[np.argmax(Lh[m])]
        vv = int(hv[j])
        mg = int(maxgap_window(np.array([2 * vv]), 300)[0])
        out.append(f"| [{lo:,},{hi:,}) | {int(m.sum()):,} | {int(Lh[j])} | {vv:,} | {int(gap_c[vv-1])} | {int(pplus[vv-1]-2*vv)} | {int(qf[j]-2*vv)} | {mg} | {np.percentile(Lh[m],99):.0f} |")
    out.append("")
    # top 20 lifetimes
    order = np.argsort(-Lh)[:20]
    out.append("### Top 20 lifetimes")
    out.append("| v | L(v) | fi(v) | partner a(fi-1) | q=v+partner | q-2v | gap containing 2v (p-,p+) | gap containing q-? | max gap [2v-300,2v+300] | prev prime <= 2v+L |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for j in order:
        vv = int(hv[j]); q = int(qf[j])
        pm = int(D.prevp[q - 1])
        mg = int(maxgap_window(np.array([2 * vv]), 300)[0])
        out.append(f"| {vv:,} | {int(Lh[j])} | {int(fi[vv]):,} | {int(partner[j]):,} | {q:,} | {q-2*vv} | {int(gap_c[vv-1])} ({int(pminus[vv-1]):,},{int(pplus[vv-1]):,}) | prev prime before q: {pm:,} (q-gap {q-pm}) | {mg} | {int(D.prevp[2*vv+int(Lh[j])]):,} |")
    out.append("")
    # relation L vs q - 2v and vs prime-free interval
    d_fill = qf - 2 * hv
    out.append("### Lifetime vs fill prime")
    out.append(f"q_fill - 2v: {pct(d_fill, (0, 1, 50, 99, 100))}")
    out.append(f"L - (q_fill - 2v) = 1 - Dup(fi-1): {pct(Lh - d_fill, (0, 1, 50, 99, 100))}")
    # prime-free interval right of 2v: does L ever exceed (2v -> first prime p > 2v with p - v unused at time ...)?
    # Simple bound candidates: L <= c * maxgap_window(2v, W)
    for W in (100, 200, 300, 500):
        mg = maxgap_window(2 * hv, W)
        r = Lh / mg
        jj = int(np.argmax(r))
        out.append(f"L / maxgap[2v-{W},2v+{W}]: max {r.max():.3f} at v={int(hv[jj]):,} (L={int(Lh[jj])}, gap={int(mg[jj])}); "
                   f"#(L > maxgap) = {int((Lh > mg).sum()):,}; #(L > 1.5 maxgap) = {int((Lh > 1.5*mg).sum())}; #(L>2 maxgap) = {int((Lh>2*mg).sum())}")
    # relation with the "previous gap": distance from 2v back to the last prime below the window
    out.append("")
    # correlation by gap bins
    mg300 = maxgap_window(2 * hv, 300)
    out.append("### Max L conditional on max gap g in [2v-300, 2v+300] (v >= 10^5)")
    out.append("| g bin | #holes | mean L | max L | max L / g |")
    out.append("|---|---|---|---|---|")
    m5 = hv >= 10**5
    for lo, hi in [(0, 40), (40, 60), (60, 80), (80, 100), (100, 120), (120, 140), (140, 200)]:
        m = m5 & (mg300 >= lo) & (mg300 < hi)
        if m.any():
            out.append(f"| [{lo},{hi}) | {int(m.sum()):,} | {Lh[m].mean():.2f} | {int(Lh[m].max())} | {(Lh[m]/mg300[m]).max():.2f} |")
    out.append("")
    if plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
        ax[0].hist(Lh, bins=np.arange(1, Lh.max() + 2), log=True)
        ax[0].set_xlabel("lifetime L(v)"); ax[0].set_ylabel("count"); ax[0].set_title("hole lifetimes, v <= 1e7")
        sub = np.random.default_rng(1).choice(len(hv), 200000, replace=False)
        ax[1].scatter(mg300[sub] + np.random.default_rng(2).uniform(-0.8, 0.8, len(sub)), Lh[sub], s=1, alpha=0.2)
        ax[1].set_xlabel("max prime gap in [2v-300, 2v+300]"); ax[1].set_ylabel("L(v)")
        ax[1].plot([0, 200], [0, 200], "r--", lw=1)
        fig.tight_layout(); fig.savefig(os.path.join(plots, "lifetimes.png"), dpi=110)
    return dict(hv=hv, Lh=Lh)


def build_sparse(arr):
    tab = [arr.copy()]
    j = 1
    while (1 << j) <= len(arr):
        prev = tab[-1]
        h = 1 << (j - 1)
        tab.append(np.maximum(prev[:-h], prev[h:]))
        j += 1
    return tab


_ST = None


def range_max(arr, lo, hi):
    """max arr[lo..hi] inclusive, vectorized via the sparse table _ST built on arr."""
    st = _ST
    length = hi - lo + 1
    length = np.maximum(length, 1)
    j = np.floor(np.log2(length)).astype(np.int64)
    res = np.empty(len(lo), dtype=arr.dtype)
    for jj in np.unique(j):
        m = j == jj
        t = st[jj]
        res[m] = np.maximum(t[lo[m]], t[hi[m] - (1 << jj) + 1])
    return res


# ---------------------------------------------------------------- frontier
def sec_frontier(D, out):
    N = D.N
    fi, s, a = D.fi, D.s, D.a
    Nv = N - 5000
    v = np.arange(1, Nv + 1)
    fv = fi[v]
    sv = s[v]
    # fills: a(k+1) <= k
    kk = D.k[1:]
    vals = a[1:]
    isfill = vals < kk
    front_pick = s[vals] < kk  # s(a(k+1)) <= k  <=> a(k+1) is the parity frontier u*(k)
    out.append("## 3. Frontier holes")
    out.append(f"all steps: P(a(k+1) = u*(k)) = {front_pick.mean():.4f}")
    out.append(f"fills (a(k+1) <= k): {int(isfill.sum()):,}; fraction that are frontier picks = {front_pick[isfill].mean():.4f}")
    # non-frontier fills: how deep (rank among unused of the same parity)?
    # exact-fact check: for every v with s(v) < fi(v): first k > s(v) with a(k)+v prime is k = fi(v)-1
    ever_front = sv < fv
    vf = v[ever_front]
    sf = sv[ever_front]
    ff = fv[ever_front]
    span = ff - 1 - sf  # number of k in (s, fi-1]
    out.append(f"values that are ever the parity frontier while unused: {len(vf):,} of {Nv:,}; max (fi - s) = {int((ff - sf).max())}")
    viol = 0
    for d in range(1, int(span.max())):
        m = d < span
        if not m.any():
            break
        kq = sf[m] + d  # k in (s, fi-1)
        viol += int(D.isp[a[kq - 1] + vf[m]].sum())
    okend = D.isp[a[ff[vf >= 2] - 2] + vf[vf >= 2]].all()  # v=1 has fi=1, no predecessor
    out.append(f"EXACT CHECK (fill at first partner after becoming frontier): violations = {viol}, last partner prime for all = {bool(okend)}")
    # frontier holes
    T0 = np.maximum(sv, v)
    fh = fv > T0  # was a frontier hole for at least one time
    vh = v[fh]; T0h = T0[fh]; fh_f = fv[fh]
    wait = fh_f - T0h
    out.append(f"frontier holes: {len(vh):,} (out of {int((fv > v).sum()):,} holes); holes never frontier while hole: {int(((fv > v) & ~fh).sum()):,}")
    out.append(f"(a) frontier wait fi(v) - T0(v): mean {wait.mean():.2f}, {pct(wait)}")
    # wait by v range
    out.append("| v range | #frontier holes | mean wait | p99 | max wait | v at max |")
    out.append("|---|---|---|---|---|---|")
    edges = [1, 10**4, 10**5, 10**6, 10**7]
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (vh >= lo) & (vh < hi)
        if m.any():
            j = np.flatnonzero(m)[np.argmax(wait[m])]
            out.append(f"| [{lo:.0e},{hi:.0e}) | {int(m.sum()):,} | {wait[m].mean():.2f} | {np.percentile(wait[m],99):.0f} | {int(wait[j])} | {int(vh[j]):,} |")
    out.append("")
    # (b) partners unused at T0, w opposite parity, w <= M(T0) [holes w <= T0, gaps T0 < w <= M(T0)], plus fresh partner
    MT = D.Mof(T0h)
    uT = D.u(T0h)
    base = uT + ((uT + vh + 1) & 1)  # first value >= u(T0) of opposite parity to v
    nh = np.zeros(len(vh), np.int64)  # # hole partners (w <= T0)
    ng = np.zeros(len(vh), np.int64)  # # gap partners (T0 < w <= M)
    nunused_opp = np.zeros(len(vh), np.int64)  # unused opp-parity values <= M(T0)
    first_h = np.full(len(vh), 10**12, np.int64)
    first_g = np.full(len(vh), 10**12, np.int64)
    min_partner = np.full(len(vh), 10**12, np.int64)
    width = int((MT - base).max())
    for d in range(0, width + 1, 2):
        w = base + d
        m = w <= MT
        if not m.any():
            break
        unused = np.zeros(len(vh), bool)
        unused[m] = fi[w[m]] > T0h[m]
        nunused_opp += unused
        isq = np.zeros(len(vh), bool)
        isq[m] = D.isp[vh[m] + w[m]]
        p = unused & isq
        hole = p & (w <= T0h)
        gap = p & (w > T0h)
        nh += hole; ng += gap
        fw = np.where(p, fi[np.minimum(w, D.M + 1)], 10**12)
        first_h = np.where(hole, np.minimum(first_h, fw), first_h)
        first_g = np.where(gap, np.minimum(first_g, fw), first_g)
        min_partner = np.where(p & (w < min_partner), w, min_partner)
    # fresh partner: smallest prime q with q - v > M(T0)
    qf = D.nextp[vh + MT + 1]
    wf = qf - vh
    first_f = fi[np.minimum(wf, D.M + 1)]
    filler = a[fh_f - 2]
    cls = np.where(filler <= T0h, 0, np.where(filler <= MT, 1, 2))
    out.append("(b) partners of the frontier hole v at time T0 (opposite parity, unused, prime sum):")
    out.append(f"   # hole partners (w <= T0): mean {nh.mean():.3f}, max {nh.max()}, P(>=1) = {(nh>0).mean():.4f}")
    out.append(f"   # gap partners (T0 < w <= M(T0)): mean {ng.mean():.3f}, max {ng.max()}, P(>=1) = {(ng>0).mean():.4f}")
    out.append(f"   # unused opposite-parity values <= M(T0): mean {nunused_opp.mean():.2f}, max {nunused_opp.max()}")
    out.append(f"   time to first use of a partner, min over all three classes, minus T0: {pct(np.minimum(np.minimum(first_h, first_g), first_f) - T0h)}")
    out.append(f"   filler class: hole partner {np.mean(cls==0):.4f}, gap partner {np.mean(cls==1):.4f}, fresh (> M(T0)) {np.mean(cls==2):.4f}")
    is_first_fresh = (filler == wf)
    out.append(f"   among fresh fillers: filler is the *first* fresh partner nextprime(v+M+1)-v: {is_first_fresh[cls==2].mean():.4f}")
    out.append(f"   filler is the smallest unused partner (incl. fresh): {np.mean(filler == np.minimum(min_partner, wf)):.4f}")
    # (c) filled exactly at first partner use: fi(v) - 1 == min(first_h, first_g, first_f?)  (fresh: first use among all fresh may be a later fresh partner)
    first_any = np.minimum(np.minimum(first_h, first_g), first_f)
    # fresh partners beyond wf could be used earlier than wf; check filler directly
    out.append(f"(c) fi(v) - 1 == first use time among (hole, gap, first fresh) partners: {np.mean(fh_f - 1 == first_any):.4f}; "
               f"fi(v)-1 < that (filled by a later fresh partner used earlier): {np.mean(fh_f - 1 < first_any):.4f}; > : {int((fh_f - 1 > first_any).sum())}")
    # wait vs fresh-partner timing
    lagf = first_f - T0h
    out.append(f"   fresh partner wf = nextprime(v+M(T0)+1) - v: (fi(wf) - T0) {pct(lagf)}; wf - M(T0): {pct(wf - MT)}")
    # bound candidate (L2'): wait <= (fi(wf) - T0) + 1 always (since wf is a partner unused at T0)
    out.append(f"   (L2) wait <= fi(wf) - T0 + 1: violations {int((wait > lagf + 1).sum())} (must be 0: wf is a partner)")
    # how late is fi(wf) relative to wf: Dlo of the fresh partner
    out.append(f"   fi(wf) - wf (lateness of the fresh partner): {pct(first_f - wf, (0, 1, 50, 99, 100))}")
    # predictor purely from primes: wait <= (nextprime(v+M+1) - v) - T0 + lateness
    # worst waits
    order = np.argsort(-wait)[:12]
    out.append("")
    out.append("### Worst frontier waits")
    out.append("| v | T0 | s(v) | fi(v) | wait | M(T0) | #hole partners | #gap partners | filler | class | first fresh wf | fi(wf) | gap at v+M(T0) |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    cn = ["hole", "gap", "fresh"]
    for j in order:
        x = int(vh[j] + MT[j] + 1)
        g = int(D.nextp[x] - D.prevp[x])
        out.append(f"| {int(vh[j]):,} | {int(T0h[j]):,} | {int(s[vh[j]]):,} | {int(fh_f[j]):,} | {int(wait[j])} | {int(MT[j]):,} | {int(nh[j])} | {int(ng[j])} | {int(filler[j]):,} | {cn[cls[j]]} | {int(wf[j]):,} | {int(first_f[j]):,} | {g} |")
    out.append("")
    return dict(vh=vh, wait=wait, nh=nh, ng=ng, cls=cls)


# ---------------------------------------------------------------- pairs
def sec_pairs(D, out, life):
    N = D.N
    fi = D.fi
    Nv = N - 5000
    v = np.arange(1, Nv + 1)
    fv = fi[v]
    Lmax = int((fv - v).max())
    out.append("## 4. Mutual-blocking pairs: v < w, opposite parity, both holes at some time, v+w prime")
    out.append("| sum | #pairs coexisting | max coexistence | p99 coex | P(|fi(v)-fi(w)|=1) | max T = max(fi)-w (L1 from first common time) | max over pairs of min(fi)-w |")
    out.append("|---|---|---|---|---|---|---|")
    res = {}
    for kind in ("prime", "composite"):
        coex_all = []; adj = 0; tot = 0; Tmax = 0; Targ = None; dlist = []
        for d in range(1, Lmax + 1, 2):
            w = v + d
            m = (fv > w) & (fi[np.minimum(w, D.M + 1)] > w) & (w <= Nv)
            ip = D.isp[2 * v + d]
            m &= ip if kind == "prime" else ~ip
            if not m.any():
                continue
            vv = v[m]; ww = w[m]
            c = np.minimum(fi[vv], fi[ww]) - ww
            T = np.maximum(fi[vv], fi[ww]) - ww
            coex_all.append(c)
            adj += int((np.abs(fi[vv] - fi[ww]) == 1).sum())
            dlist.append(np.abs(fi[vv] - fi[ww]))
            tot += len(vv)
            j = int(np.argmax(T))
            if T[j] > Tmax:
                Tmax = int(T[j]); Targ = (int(vv[j]), int(ww[j]), int(fi[vv[j]]), int(fi[ww[j]]))
        c = np.concatenate(coex_all)
        res[kind] = (c, Targ)
        dl = np.concatenate(dlist)
        out.append(f"[{kind}] |fi(v)-fi(w)| over coexisting pairs: {pct(dl)}")
        out.append(f"| {kind} | {tot:,} | {c.max()} | {np.percentile(c,99):.0f} | {adj/tot:.4f} | {Tmax} at (v,w,fi v,fi w)={Targ} | {c.max()} |")
    out.append("")
    # exact fact: both parity frontiers at a common time with prime sum -> filled consecutively
    # pairs (v,w) with v+w prime, both frontier holes simultaneously at some time
    cnt = 0; consec = 0; mx = 0
    for d in range(1, Lmax + 1, 2):
        w = v + d
        wc = np.minimum(w, D.M + 1)
        m = (fv > w) & (fi[wc] > w) & (w <= Nv) & D.isp[2 * v + d]
        if not m.any():
            continue
        vv = v[m]; ww = w[m]
        start = np.maximum(np.maximum(D.s[vv], D.s[ww]), ww)
        end = np.minimum(fi[vv], fi[ww])
        both = start < end
        cnt += int(both.sum())
        consec += int((np.abs(fi[vv] - fi[ww])[both] == 1).sum())
        if both.any():
            mx = max(mx, int((end - start)[both].max()))
    out.append(f"pairs that are simultaneously the two parity frontiers with prime sum: {cnt:,}; filled at consecutive steps: {consec:,} (exact fact predicts all); max time both frontier = {mx}")
    out.append("")
    return res


def cross_prime_pairs(D, hs):
    ev = hs[hs % 2 == 0]; od = hs[hs % 2 == 1]
    if len(ev) == 0 or len(od) == 0:
        return 0, 0.0, 0
    S = ev[:, None] + od[None, :]
    obs = int(D.isp[S].sum())
    exp = float((2.0 / np.log(S)).sum())
    return obs, exp, S.size


def sec_structure(D, out):
    N = D.N
    out.append("## 5. Structure of the simultaneous hole set")
    # record times
    rec = [6_869_384] if N > 6_869_384 else []
    # find bursts: local maxima of H near 419,146 and 2,326,231
    for c in (419_146, 2_326_231):
        if c + 3000 > N:
            continue
        sl = slice(c - 3000, c + 3000)
        j = int(np.argmax(D.H[sl])) + c - 3000 + 1
        rec.append(j)
    rec.append(int(np.argmax(D.H)) + 1)
    for n in sorted(set(rec)):
        hs = D.holes_at(n)
        obs, exp, npairs = cross_prime_pairs(D, hs)
        ev = hs[hs % 2 == 0]; od = hs[hs % 2 == 1]
        out.append(f"### n = {n:,}: H = {len(hs)} (even {len(ev)}, odd {len(od)}), holes in [{hs.min():,}, {hs.max():,}], M(n) = {int(D.Mrun[n-1]):,}, a(n) = {int(D.a[n-1]):,}")
        out.append(f"  cross-parity pairs {npairs}, with prime sum: observed {obs}, expected (random, 2/ln s) {exp:.1f}")
        sums = (ev[:, None] + od[None, :]).ravel() if len(ev) and len(od) else np.array([], int)
        if len(sums):
            out.append(f"  sums range [{sums.min():,}, {sums.max():,}]; primes in that range: {int(D.isp[sums.min():sums.max()+1].sum())}; "
                       f"largest prime gap inside: {int(np.diff(np.flatnonzero(D.isp[sums.min()-300:sums.max()+301])).max())}")
            pp = np.flatnonzero(D.isp[sums.min():sums.max() + 1]) + sums.min()
            out.append(f"  primes hit by a cross sum: {sorted(set(int(x) for x in sums[D.isp[sums]]))[:30]}")
            out.append(f"  primes in [min sum, max sum]: {[int(x) for x in pp][:40]}")
        out.append(f"  holes (offset from n): {[int(x - n) for x in hs]}")
        # lifetimes of these holes
        out.append(f"  fi - n of these holes: {[int(D.fi[x] - n) for x in hs]}")
        out.append("")
    # systematic: sample times
    rng = np.random.default_rng(0)
    out.append("### Prime-sum-freeness over sampled times (every 997th n in [10^5, N])")
    out.append("| H bin | #times | mean obs cross prime pairs | mean expected | obs/exp |")
    out.append("|---|---|---|---|---|")
    ts = np.arange(10**5, N - 1000, 997)
    O = []; E = []; Hs = []
    for n in ts:
        hs = D.holes_at(int(n))
        o, e, _ = cross_prime_pairs(D, hs)
        O.append(o); E.append(e); Hs.append(len(hs))
    O = np.array(O); E = np.array(E); Hs = np.array(Hs)
    for lo, hi in [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 60)]:
        m = (Hs >= lo) & (Hs < hi)
        if m.any():
            out.append(f"| [{lo},{hi}) | {int(m.sum())} | {O[m].mean():.3f} | {E[m].mean():.3f} | {O[m].sum()/max(E[m].sum(),1e-9):.3f} |")
    out.append(f"all: obs {O.sum()}, exp {E.sum():.1f}, ratio {O.sum()/E.sum():.3f}; times with obs=0: {(O==0).mean():.3f}")
    out.append("")
    # compare with random sets of same size in the same window (control): holes are spread in [u(n), n]
    return dict(O=O, E=E, Hs=Hs, ts=ts)


# ---------------------------------------------------------------- bounds
def sec_bounds(D, out, plots=None):
    N = D.N
    k = D.k
    H = D.H
    out.append("## 6. Candidate bounds H(n) vs primes near 2n")
    two = 2 * k
    r = two - D.prevp[two]  # distance from 2n back to the last prime <= 2n
    # max gap among primes in [2n - W, 2n + W']
    pr = D.primes
    gaps = np.diff(pr)
    global _ST
    _ST = build_sparse(gaps)
    def mg(lo_off, hi_off):
        i0 = np.searchsorted(pr, two + lo_off, side="left")
        i1 = np.searchsorted(pr, two + hi_off, side="right") - 1
        return range_max(gaps, np.maximum(i0 - 1, 0), np.minimum(i1, len(gaps) - 1))
    sel = k >= 1000
    out.append("| statistic G(n) | max H/G (n>=1000) | n at max | best C in H <= G/2 + C | best C in H <= G/4 + C | corr(H, G) |")
    out.append("|---|---|---|---|---|---|")
    cand = {}
    for name, G in [("gap containing 2n", D.nextp[two + 1] - D.prevp[two]),
                    ("2n - prevprime(2n)", np.maximum(r, 1)),
                    ("maxgap [2n-100,2n+100]", mg(-100, 100)),
                    ("maxgap [2n-300,2n]", mg(-300, 0)),
                    ("maxgap [2n-300,2n+300]", mg(-300, 300)),
                    ("maxgap [2n-600,2n+100]", mg(-600, 100))]:
        Gs = G[sel]; Hs = H[sel]
        ratio = Hs / Gs
        j = int(np.argmax(ratio))
        C2 = int((Hs - Gs / 2).max()); C4 = int(np.ceil((Hs - Gs / 4).max()))
        cand[name] = G
        out.append(f"| {name} | {ratio.max():.3f} | {int(k[sel][j]):,} (H={int(Hs[j])}, G={int(Gs[j])}) | {C2} | {C4} | {np.corrcoef(Hs, Gs)[0,1]:.3f} |")
    out.append("")
    # primes in short windows near 2n: number of primes in (2n - A, 2n]
    cs = np.concatenate([[0], np.cumsum(D.isp)])
    out.append("### H(n) vs pi(2n) - pi(2n - A) (number of primes in a window left of 2n)")
    out.append("| A | max H - #primes | at n | mean #primes | corr(H, -#primes) |")
    out.append("|---|---|---|---|---|")
    for A in (50, 100, 200, 400):
        cnt = cs[two + 1] - cs[np.maximum(two - A + 1, 0)]
        dlt = (H - cnt)[sel]
        j = int(np.argmax(dlt))
        out.append(f"| {A} | {int(dlt.max())} | {int(k[sel][j]):,} | {cnt[sel].mean():.2f} | {np.corrcoef(H[sel], -cnt[sel])[0,1]:.3f} |")
    out.append("")
    # heuristic predictor: Hpred(n) = #{ j in [1, J] : the interval (2n - 2j, 2n - j] has no prime }  (v = n - j would have no partner yet)
    out.append("### Heuristic predictor Hpred(n) = #{ v in [n-400, n] : no prime in (2v, n + v] }")
    out.append("(v is a hole candidate if no prime q with partner q - v in (v, n] exists, i.e. q in (2v, n+v])")
    Hp = np.zeros(N, np.int64)
    for j in range(0, 401):
        vv = k - j
        ok = vv >= 1
        lo = 2 * vv; hi = k + vv
        c = cs[np.maximum(hi, 0) + 1] - cs[np.maximum(lo, 0) + 1]
        Hp += (ok & (c == 0))
    out.append(f"corr(H, Hpred) (n>=1000) = {np.corrcoef(H[sel], Hp[sel])[0,1]:.3f}; max H - Hpred = {int((H-Hp)[sel].max())}; max Hpred - H = {int((Hp-H)[sel].max())}; "
               f"mean H {H[sel].mean():.2f}, mean Hpred {Hp[sel].mean():.2f}")
    out.append("")
    # J(n) = pi(u(n) + n) - pi(2u(n)) for the smallest hole u(n), and Phi_K(n) = #{v <= n : pi(v+n) - pi(2v) <= K}
    hasH = H > 0
    un = D.u(k)
    J = np.where(hasH, cs[np.minimum(un + k, len(cs) - 2) + 1] - cs[2 * un + 1], -1)
    out.append("### Frontier window: J(n) = pi(u(n) + n) - pi(2u(n)), u(n) = smallest hole")
    out.append(f"max J(n) = {int(J.max())} at n = {int(np.argmax(J))+1:,}; {pct(J[hasH & sel], (50, 99, 99.9, 100))}")
    for lo, hi in [(10**3, 10**5), (10**5, 10**6), (10**6, 10**7 + 1)]:
        m = hasH & (k >= lo) & (k < hi)
        out.append(f"  n in [{lo:.0e},{hi:.0e}): max J = {int(J[m].max())}")
    out.append("| K | max (H - Phi_K) | #n with H > Phi_K | max H/Phi_K | mean Phi_K |")
    out.append("|---|---|---|---|---|")
    for K in (0, 2, 4, 6, 8):
        Phi = np.zeros(N, np.int64)
        for j in range(0, 401):
            vv = k - j
            ok = vv >= 1
            c = cs[np.maximum(k + vv, 0) + 1] - cs[np.maximum(2 * vv, 0) + 1]
            Phi += ok & (c <= K)
        dd = (H - Phi)[sel]
        out.append(f"| {K} | {int(dd.max())} | {int((dd > 0).sum()):,} | {(H[sel]/np.maximum(Phi[sel],1)).max():.3f} | {Phi[sel].mean():.2f} |")
    out.append("")
    if plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
        G = cand["maxgap [2n-300,2n+300]"]
        sub = np.arange(1000, N, 37)
        ax[0].scatter(G[sub] + np.random.default_rng(3).uniform(-0.8, 0.8, len(sub)), H[sub], s=1, alpha=0.15)
        ax[0].set_xlabel("max prime gap in [2n-300, 2n+300]"); ax[0].set_ylabel("H(n)")
        ax[0].plot([0, 200], [0, 100], "r--", lw=1, label="H = G/2")
        ax[0].legend()
        c0 = 6_869_384 if N > 6_870_000 else int(np.argmax(H)) + 1
        w = np.arange(c0 - 1500, c0 + 1500)
        ax[1].plot(w, H[w - 1], lw=0.8, label="H(n)")
        ax[1].plot(w, Hp[w - 1], lw=0.8, label="Hpred(n)")
        for p in np.flatnonzero(D.isp[2 * (c0 - 1500): 2 * (c0 + 1500)]) + 2 * (c0 - 1500):
            pass
        g = (D.nextp[2 * w + 1] - D.prevp[2 * w]) / 2
        ax[1].plot(w, g, lw=0.8, label="(gap containing 2n)/2")
        ax[1].set_xlabel("n"); ax[1].legend(); ax[1].set_title("around the record H=50")
        fig.tight_layout(); fig.savefig(os.path.join(plots, "holes_vs_gaps.png"), dpi=110)
    return dict(Hp=Hp)


# ---------------------------------------------------------------- queue
def sec_queue(D, out):
    """For each hole v, classify its opportunities k in [v, fi(v)-2], k = v+1 (mod 2)
    (steps k -> k+1 at which a(k+1) has the parity of v):
      composite: a(k)+v composite  ("no partner")
      stolen:    a(k)+v prime, so a(k+1) <= v is a fill, and a(k+1) < v (a smaller hole wins)
    Exact claim checked: stolen(v) <= #{ holes x < v, x = v mod 2, at time v }."""
    N = D.N; fi = D.fi; a = D.a
    Nv = N - 5000
    v = np.arange(2, Nv + 1)
    fv = fi[v]
    hm = fv > v
    vh = v[hm]; fh = fv[hm]
    L = fh - vh
    stolen = np.zeros(len(vh), np.int64)
    comp = np.zeros(len(vh), np.int64)
    bad_steal = 0
    for d in range(1, int(L.max()), 2):
        k = vh + d
        m = k <= fh - 2
        if not m.any():
            break
        kk = k[m]
        pr = D.isp[a[kk - 1] + vh[m]]
        stolen[m] += pr
        comp[m] += ~pr
        # when stolen, a(k+1) must be < v and be a hole of v's parity
        nxt = a[kk[pr]]  # a(k+1)
        bad_steal += int((nxt >= vh[m][pr]).sum())
    # same-parity holes below v at time v: x in [u(v), v-2], x = v mod 2, fi(x) > v
    below = np.zeros(len(vh), np.int64)
    uv = D.u(vh)
    for d in range(2, 400, 2):
        x = vh - d
        m = x >= np.maximum(uv, 1)
        if not m.any():
            break
        below[m] += fi[x[m]] > vh[m]
    out.append("## 7. Queue mechanism: why a hole survives a step")
    out.append(f"holes v in [2, N-5000]: {len(vh):,}; opportunities (steps of v's parity while v is a hole, excluding the fill) total {int((stolen+comp).sum()):,}")
    out.append(f"  composite-sum opportunities: {int(comp.sum()):,} ({comp.sum()/(stolen+comp).sum():.4f}); stolen (prime sum, smaller hole taken): {int(stolen.sum()):,}")
    out.append(f"  sanity: stolen steps where a(k+1) >= v: {bad_steal} (must be 0)")
    out.append(f"  stolen(v): mean {stolen.mean():.3f}, {pct(stolen)}; P(stolen>=1) = {(stolen>0).mean():.4f}")
    out.append(f"  EXACT CHECK stolen(v) <= #same-parity holes below v at time v: violations {int((stolen > below).sum())}; "
               f"max slack used stolen/below = {np.max(np.where(below>0, stolen/np.maximum(below,1), 0)):.3f}; #below: {pct(below)}")
    out.append(f"  composite(v) = L/2 - 1 - stolen: max {comp.max()}; corr(L, stolen) = {np.corrcoef(L, stolen)[0,1]:.3f}, corr(L, comp) = {np.corrcoef(L, comp)[0,1]:.3f}")
    # longest runs of consecutive composite opportunities (sums a(k)+v avoiding primes)
    out.append("| L range | #holes | mean stolen | max stolen | mean composite | max composite |")
    out.append("|---|---|---|---|---|---|")
    for lo, hi in [(2, 20), (20, 50), (50, 100), (100, 150), (150, 250)]:
        m = (L >= lo) & (L < hi)
        if m.any():
            out.append(f"| [{lo},{hi}) | {int(m.sum()):,} | {stolen[m].mean():.2f} | {int(stolen[m].max())} | {comp[m].mean():.2f} | {int(comp[m].max())} |")
    out.append("")
    # top lifetimes: sums a(k)+v over the opportunities; how many distinct primes are in their range
    out.append("### Top 8 lifetimes: sums a(k)+v seen while v was a hole")
    out.append("| v | L | stolen | composite | sums range (offset from 2v) | #primes in that range | #primes hit |")
    out.append("|---|---|---|---|---|---|---|")
    for j in np.argsort(-L)[:8]:
        vv = int(vh[j]); ks = np.arange(vv + 1, int(fh[j]) - 1, 2)
        sm = a[ks - 1] + vv
        lo, hi = int(sm.min()), int(sm.max())
        out.append(f"| {vv:,} | {int(L[j])} | {int(stolen[j])} | {int(comp[j])} | [{lo-2*vv}, {hi-2*vv}] | {int(D.isp[lo:hi+1].sum())} | {int(D.isp[sm].sum())} |")
    out.append("")
    # EXACT LEMMA CHECK (prime-count bound on lifetimes):
    #   pi(v + fi(v) - 1) - pi(2v) <= stolen(v) + 1 + H_opp(v-1) + H_opp(fi(v)-1)
    # (each prime q in (2v, v+fi-1] has partner w=q-v in (v, fi-1] of opposite parity; w was
    #  used in [v, fi-2] (a steal), at fi-1 (the filler), before v (ahead at v-1, = H_opp(v-1)),
    #  or is still unused at fi-1 (a hole at fi-1)).
    cs = np.concatenate([[0], np.cumsum(D.isp)])
    npr = cs[vh + fh - 1 + 1] - cs[2 * vh + 1]
    par_opp = 1 - (vh & 1)
    Hopp_before = np.where(par_opp == 0, D.He[vh - 2], D.Ho[vh - 2])
    Hopp_after = np.where(par_opp == 0, D.He[fh - 2], D.Ho[fh - 2])
    rhs = stolen + 1 + Hopp_before + Hopp_after
    out.append("### Exact prime-count bound on lifetimes")
    out.append("  pi(v+fi(v)-1) - pi(2v) <= stolen(v) + 1 + H_opp(v-1) + H_opp(fi(v)-1)")
    out.append(f"  violations: {int((npr > rhs).sum())}; #primes in (2v, v+fi-1]: {pct(npr)}; rhs: {pct(rhs)}; min slack rhs-lhs = {int((rhs-npr).min())}; "
               f"P(equality) = {(rhs==npr).mean():.4f}")
    # decomposition of the primes for the top holes
    out.append("| v | L | #primes in (2v, v+fi-1] | stolen | H_opp(v-1) | H_opp(fi-1) | rhs |")
    out.append("|---|---|---|---|---|---|---|")
    for j in np.argsort(-L)[:6]:
        out.append(f"| {int(vh[j]):,} | {int(L[j])} | {int(npr[j])} | {int(stolen[j])} | {int(Hopp_before[j])} | {int(Hopp_after[j])} | {int(rhs[j])} |")
    # exact classification of the primes q in (2v, 2v+L-1] by when the partner w = q - v was used
    i0 = np.searchsorted(pr_all := D.primes, 2 * vh, side="right")
    cnt = {"ahead (used before v)": 0, "steal (used in [v, fi-2])": 0, "filler (used at fi-1)": 0, "late (unused at fi-1)": 0}
    Kahead = np.zeros(len(vh), np.int64); Klate = np.zeros(len(vh), np.int64); Ksteal = np.zeros(len(vh), np.int64)
    for j in range(int(npr.max())):
        m = npr > j
        q = pr_all[i0[m] + j]
        w = q - vh[m]
        fw = fi[w]
        ff = fh[m]; vv = vh[m]
        c0 = fw < vv; c1 = (fw >= vv) & (fw <= ff - 2); c2 = fw == ff - 1; c3 = fw > ff - 1
        cnt["ahead (used before v)"] += int(c0.sum()); cnt["steal (used in [v, fi-2])"] += int(c1.sum())
        cnt["filler (used at fi-1)"] += int(c2.sum()); cnt["late (unused at fi-1)"] += int(c3.sum())
        Kahead[np.flatnonzero(m)[c0]] += 1; Klate[np.flatnonzero(m)[c3]] += 1; Ksteal[np.flatnonzero(m)[c1]] += 1
    out.append(f"  classification of the {int(npr.sum()):,} primes q in (2v, 2v+L-1] (over all holes): " + "; ".join(f"{k}: {v:,}" for k, v in cnt.items()))
    out.append(f"  per hole: max #ahead-blocked = {int(Kahead.max())}, max #late = {int(Klate.max())}, max stolen = {int(stolen.max())}")
    out.append("")
    Kfill = npr - Kahead - Klate - Ksteal
    out.append("| v range | max K | max ahead-blocked | max stolen (in window) | max late | max H(v) | mean K | mean ahead | mean stolen | mean late |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for lo, hi in [(2, 10**4), (10**4, 10**5), (10**5, 10**6), (10**6, 3 * 10**6), (3 * 10**6, 10**7)]:
        m = (vh >= lo) & (vh < hi)
        if m.any():
            out.append(f"| [{lo:.0e},{hi:.0e}) | {int(npr[m].max())} | {int(Kahead[m].max())} | {int(Ksteal[m].max())} | {int(Klate[m].max())} | {int(D.H[vh[m]-1].max())} | {npr[m].mean():.3f} | {Kahead[m].mean():.3f} | {Ksteal[m].mean():.3f} | {Klate[m].mean():.3f} |")
    out.append(f"  filler term inside the window: {int(Kfill.sum()):,} holes (0/1 each), check min {int(Kfill.min())} max {int(Kfill.max())}")
    # time-local version for the smallest hole u(n) at every n:
    #   pi(u+n) - pi(2u) <= 1 + #{x<u, x=u mod 2, hole at time u} + H_opp(u-1) + H_opp(n)
    kk = D.k
    has = D.H > 0
    nn = kk[has & (kk >= 3)]
    un = D.u(nn)
    lhs = cs[un + nn + 1] - cs[2 * un + 1]
    belowmap = np.zeros(D.M + 3, np.int64); belowmap[vh] = below
    po = 1 - (un & 1)
    rhs2 = 1 + belowmap[un] + np.where(po == 0, D.He[un - 2], D.Ho[un - 2]) + np.where(po == 0, D.He[nn - 1], D.Ho[nn - 1])
    okm = un >= 2
    okm &= un <= N - 5000  # 'below' is only computed for v <= N-5000
    bad = np.flatnonzero(okm & (lhs > rhs2))
    out.append(f"  time-local lemma for the smallest hole u(n), all n <= N with H(n)>0 and u(n) <= N-5000: violations {len(bad)}; max lhs {int(lhs[okm].max())}; max rhs {int(rhs2[okm].max())}")
    for b in bad[:5]:
        out.append(f"    violation at n={int(nn[b])}, u={int(un[b])}, lhs={int(lhs[b])}, rhs={int(rhs2[b])}")
    out.append("")
    out.append("### K(v) = pi(2v + L(v) - 1) - pi(2v): primes strictly inside the lifetime window, by range of v")
    out.append("| v range | #holes | max K | v at max (L) | P(K=0) | P(K>=3) | P(K>=5) | max L among K=0 holes |")
    out.append("|---|---|---|---|---|---|---|---|")
    edges = [2, 10**3, 10**4, 10**5, 10**6, 3 * 10**6, 10**7]
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (vh >= lo) & (vh < hi)
        if m.any():
            j = np.flatnonzero(m)[np.argmax(npr[m])]
            m0 = m & (npr == 0)
            out.append(f"| [{lo:,},{hi:,}) | {int(m.sum()):,} | {int(npr[j])} | {int(vh[j]):,} ({int(L[j])}) | {(npr[m]==0).mean():.3f} | {(npr[m]>=3).mean():.4f} | {(npr[m]>=5).mean():.1e} | {int(L[m0].max()) if m0.any() else 0} |")
    out.append("")
    # tighter: count only partners actually unused/ahead (exact classification)
    out.append("")

    # best constants: L <= G + C with G = max gap in window around 2v
    pr = D.primes; gaps = np.diff(pr)
    global _ST
    _ST = build_sparse(gaps)
    out.append("### L(v) <= G(v) + C, G = max prime gap meeting [2v - W, 2v + W]")
    out.append("| W | best C | v at worst | best c in L <= c*G | ")
    out.append("|---|---|---|---|")
    for W in (100, 200, 300, 500):
        i0 = np.searchsorted(pr, 2 * vh - W, side="left"); i1 = np.searchsorted(pr, 2 * vh + W, side="right") - 1
        G = range_max(gaps, np.maximum(i0 - 1, 0), np.minimum(i1, len(gaps) - 1))
        j = int(np.argmax(L - G))
        out.append(f"| {W} | {int((L-G).max())} | {int(vh[j]):,} (L={int(L[j])}, G={int(G[j])}) | {(L/G).max():.2f} |")
    # length needed after 2v - W0 to see K primes
    out.append("")
    out.append("### L(v) vs ell_K(v) = (K-th prime > 2v - 100) - 2v  (length to collect K primes)")
    out.append("| K | max L - ell_K | #(L > ell_K) |")
    out.append("|---|---|---|")
    i0 = np.searchsorted(pr, 2 * vh - 100, side="right")
    for K in (2, 4, 6, 8, 10, 12):
        ell = pr[i0 + K - 1] - 2 * vh
        out.append(f"| {K} | {int((L - ell).max())} | {int((L > ell).sum()):,} |")
    out.append("")


# ---------------------------------------------------------------- graph
def sec_graph(D, out):
    N = D.N; a = D.a; k = D.k; fi = D.fi
    fill = D.fill  # fill[n-1] = [a(n) <= n-1]
    out.append("## 8. Fill runs = greedy walks on the prime-sum graph of holes")
    f = fill[1:]
    prev = fill[:-1]
    out.append(f"P(fill at n+1 | fill at n) = {f[prev].mean():.4f};  P(fill at n+1 | no fill at n) = {f[~prev].mean():.4f}")
    # run lengths of consecutive fills
    x = np.concatenate([[0], fill.astype(np.int8), [0]])
    d = np.diff(x)
    st = np.flatnonzero(d == 1); en = np.flatnonzero(d == -1)
    rl = en - st
    out.append(f"fill runs: {len(rl):,}; length {pct(rl)}; mean {rl.mean():.3f}")
    out.append("| run length r | #runs | fraction |")
    out.append("|---|---|---|")
    for r in (1, 2, 3, 4, 5, 6, 8, 10):
        out.append(f"| {'>=' if r==10 else ''}{r} | {int((rl==r).sum() if r<10 else (rl>=10).sum()):,} | {((rl==r).mean() if r<10 else (rl>=10).mean()):.4f} |")
    j = int(np.argmax(rl))
    out.append(f"longest run: {int(rl[j])} fills, steps {int(st[j])+1:,}..{int(en[j]):,}")
    # entry into the graph: a fill at n+1 with no fill at n means a(n) is fresh (a(n) >= n) and a(n)+hole prime
    # exit: after a fill at n (a(n)=h a hole value), no fill at n+1 means h has no unused hole partner of opposite parity
    out.append(f"fills preceded by a fresh term (entries): {int((f & ~prev).sum()):,}; fills preceded by a fill (graph steps): {int((f & prev).sum()):,}")
    # non-fill steps: a(n+1) >= n+1; how far ahead
    nf = ~fill[1:]
    ahead = (a[1:] - k[1:])[nf]
    out.append(f"non-fill steps: a(n+1) - (n+1): {pct(ahead, (50, 90, 99, 100))}")
    out.append("")
    # control for prime-sum-freeness: random same-size same-parity subsets of [min hole, n]
    out.append("### Prime-sum-freeness vs a local control (random subsets of [min hole, n] with the same parity counts)")
    out.append("| n | H | obs cross prime pairs | control mean | control p5 | control p95 | obs/control |")
    out.append("|---|---|---|---|---|---|---|")
    rng = np.random.default_rng(5)
    def control(hs, n, reps=400):
        lo = int(hs.min())
        ev_pool = np.arange(lo + (lo & 1), n + 1, 2); od_pool = np.arange(lo + 1 - (lo & 1), n + 1, 2)
        ne = int((hs % 2 == 0).sum()); no = len(hs) - ne
        res = []
        for _ in range(reps):
            e = rng.choice(ev_pool, ne, replace=False); o = rng.choice(od_pool, no, replace=False)
            res.append(int(D.isp[e[:, None] + o[None, :]].sum()))
        return np.array(res)
    times = [419_156, 2_326_240, 6_869_384] + [int(t) for t in np.flatnonzero(D.H >= 40)[::7] + 1][:8]
    tot_o = 0; tot_c = 0
    for n in times:
        if n > N:
            continue
        hs = D.holes_at(n)
        o, _, _ = cross_prime_pairs(D, hs)
        c = control(hs, n)
        out.append(f"| {n:,} | {len(hs)} | {o} | {c.mean():.1f} | {np.percentile(c,5):.0f} | {np.percentile(c,95):.0f} | {o/max(c.mean(),1e-9):.2f} |")
    # sampled times overall
    ts = np.arange(10**5, N - 1000, 4999)
    O = []; C = []; Hs = []
    for n in ts:
        hs = D.holes_at(int(n))
        if len(hs) < 2:
            continue
        o, _, _ = cross_prime_pairs(D, hs)
        c = control(hs, int(n), reps=40)
        O.append(o); C.append(c.mean()); Hs.append(len(hs))
    O = np.array(O); C = np.array(C); Hs = np.array(Hs)
    out.append("")
    out.append("| H bin (sampled every 4999 steps) | #times | mean obs | mean control | obs/control |")
    out.append("|---|---|---|---|---|")
    for lo, hi in [(2, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 60)]:
        m = (Hs >= lo) & (Hs < hi)
        if m.any():
            out.append(f"| [{lo},{hi}) | {int(m.sum())} | {O[m].mean():.2f} | {C[m].mean():.2f} | {O[m].sum()/max(C[m].sum(),1e-9):.2f} |")
    out.append("")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seq", default=DEFAULT_SEQ)
    ap.add_argument("--terms", type=int, default=10_000_000)
    ap.add_argument("--sections", default="flow,life,frontier,pairs,structure,queue,graph,bounds")
    ap.add_argument("--plots", default=None, help="directory for PNG plots (optional)")
    args = ap.parse_args()
    N = args.terms
    if os.path.exists(args.seq) and len(np.load(args.seq, mmap_mode="r")) >= N:
        a = np.load(args.seq)[:N].astype(np.int64)
    else:
        from greedy import generate
        a = generate(N)
    assert list(a[:20]) == REF, "sequence does not match A055265"
    assert len(np.unique(a)) == N
    t0 = time.time()
    D = Data(a)
    print(f"[setup {time.time()-t0:.1f}s]", file=sys.stderr)
    if args.plots:
        os.makedirs(args.plots, exist_ok=True)
    out = []
    secs = args.sections.split(",")
    life = None
    for sname in secs:
        t1 = time.time()
        if sname == "flow":
            sec_flow(D, out)
        elif sname == "life":
            life = sec_life(D, out, args.plots)
        elif sname == "frontier":
            sec_frontier(D, out)
        elif sname == "pairs":
            sec_pairs(D, out, life)
        elif sname == "structure":
            sec_structure(D, out)
        elif sname == "graph":
            sec_graph(D, out)
        elif sname == "queue":
            sec_queue(D, out)
        elif sname == "bounds":
            sec_bounds(D, out, args.plots)
        print(f"[{sname} {time.time()-t1:.1f}s]", file=sys.stderr)
        print("\n".join(out)); out.clear(); sys.stdout.flush()


if __name__ == "__main__":
    main()
