"""Prime partners of holes in the Watts greedy sequence (A055265): who pays for each prime a hole survives.

For a hole v at n = fi(v) - 1 (L009), each prime q in (2v, n+v] has partner w = q - v in (v, n] with
parity 1 - eps, and w falls in one of four classes (L009 Step 1):
    W1 Ahead  fi(w) <= v-1      W2 steal  v <= fi(w) <= n-1      W3 fi(w) = n      W4 Late fi(w) > n.
K = |W1| + |W2| + |W3| + |W4| = pi(n+v) - pi(2v).

Sections:
  1 decomposition   joint law of (|W1|, |W2|, |W4|), maxima per decade, what drives K >= 9
  2 null            observed |W1|, |W4| vs three null models:
                      g  hypergeometric: the K primes spread over the (n-v+1)/2 slots, E_i = K S_i / M
                      j  jitter: each prime moved uniformly by up to +-R slots (default R = 5, i.e. +-10)
                      p  random primes: each slot of class i is a partner with prob. 2/ln(w+v)
  3 geometry        where Late / Ahead partners sit; cut decompositions at max a(1..v-1) and at the
                    smallest Late slot
  4 recursion       K(v) against max K of holes alive at time v / at time n; Ahead-set partners;
                    chain flags of Ahead partners (was a(k-1) a (frontier) hole fill?)
  5 candidates      max |W1| + |W4| per decade and against log v

Generation: experiments/src/k_survival_1e8_gen.c (sequence) and experiments/src/partners_gen.c
(per-hole / per-partner arrays), both compiled with gcc on first use. About 75 s of C at N = 10^8,
then a few minutes of numpy; peak RAM about 8 GB; about 5 GB of binaries in --workdir.

Usage:
    python experiments/src/partners.py --terms 100000000 --workdir /path/to/scratch
"""

import argparse
import math
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from k_survival_1e8 import OEIS_FIRST, generate  # noqa: E402


def run_partners(workdir, R):
    rf = os.path.join(workdir, "partners_R.txt")
    if os.path.exists(os.path.join(workdir, "h_alive.i8")) and os.path.exists(rf) and \
            open(os.path.join(workdir, "partners_R.txt")).read().strip() == str(R):
        print(f"[partners] reusing {workdir}")
        return
    exe = os.path.join(workdir, "partners_gen")
    subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "partners_gen.c"), "-lm"], check=True)
    t0 = time.time()
    subprocess.run([exe, workdir, str(R)], check=True)
    open(os.path.join(workdir, "partners_R.txt"), "w").write(str(R))
    print(f"[partners] done in {time.time() - t0:.1f}s")


def md(header, rows):
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--terms", type=int, default=100_000_000)
    ap.add_argument("--workdir", default=os.path.join(tempfile.gettempdir(), "partners_work"))
    ap.add_argument("--R", type=int, default=5, help="jitter half-width in same-parity slots")
    args = ap.parse_args()

    N, a, fi, h0, h1, isp = generate(args.terms, args.workdir)
    assert list(a[:20]) == OEIS_FIRST, "first 20 terms do not match A055265"
    print("first 20 terms match A055265")
    del isp
    run_partners(args.workdir, args.R)
    ld = lambda name, dt: np.fromfile(os.path.join(args.workdir, name), dtype=dt)
    H = (h0 + h1).astype(np.int16)
    cols = lambda name, dt, k: [np.ascontiguousarray(c) for c in ld(name, dt).reshape(-1, k).T]
    v = ld("h_v.i32", np.int32)
    n = ld("h_n.i32", np.int32)
    K, W1, W2, W3, W4 = cols("h_W.i8", np.int8, 5)        # int8 (all <= 127)
    S1, S2, S3, S4 = cols("h_S.i16", np.int16, 4)
    Atot, AP, Mv = cols("h_A.i16", np.int16, 3)
    KbM, Kbu = cols("h_cut.i8", np.int8, 2)
    E1g, E4g, E1j, E4j, E1p, E4p = cols("h_E.f32", np.float32, 6)
    Kal_v, Nal_v, Kal_n, Nal_n = cols("h_alive.i8", np.int8, 4)
    eps = (v & 1).astype(np.int8)
    done = fi[v] != 0
    Hv = H[v - 1]
    Hn = H[n - 1]
    Hopp_n = np.where(eps == 1, h0[n - 1], h1[n - 1]).astype(np.int16)
    Hopp_v1 = np.where(eps == 1, h0[v - 2], h1[v - 2]).astype(np.int16)
    print(f"holes {len(v):,} (open at N: {int((~done).sum())}), partners {int(K.sum()):,}")
    # consistency checks against L009 / Sub-lemma S
    assert np.all(Atot == Hopp_v1), "Ahead count != H_{1-eps}(v-1) (Sub-lemma S)"
    assert np.all(W1 <= Atot) and np.all(W4 <= Hopp_n) and np.all(S4 <= Hopp_n)
    assert np.all(K <= Hv + Hopp_n), "L009' violated"
    print("checks: |Ahead(v)| = H_{1-eps}(v-1) for all holes; W1 <= H_{1-eps}(v-1); W4 <= H_{1-eps}(n); L009' holds")
    lg = np.log(v.astype(np.float32))
    dec = np.minimum(np.floor(np.log10(v)), 7).astype(np.int8)
    decs = [d for d in range(2, 8) if (done & (dec == d)).sum() > 100]
    big = done & (v >= 1000)

    # ================= 1 decomposition
    print("\n# 1. Decomposition at n = fi(v) - 1 (completed holes)")
    rows = []
    for d in decs:
        s = done & (dec == d)
        rows.append([f"[1e{d},1e{d+1})", f"{int(s.sum()):,}", K[s].max(), W1[s].max(), W2[s].max(), W3[s].max(),
                     W4[s].max(), (W1 + W4)[s].max(), (W1 + W2)[s].max(), (W2 + W4)[s].max(),
                     f"{W1[s].mean():.3f}", f"{W2[s].mean():.3f}", f"{W3[s].mean():.3f}", f"{W4[s].mean():.3f}"])
    md(["v range", "holes", "max K", "max W1", "max W2", "max W3", "max W4", "max W1+W4", "max W1+W2", "max W2+W4",
        "mean W1", "mean W2", "mean W3", "mean W4"], rows)

    print("\n## mean / max class sizes by K (v >= 1e3)")
    rows = []
    for k in range(0, 12):
        s = big & (K == k)
        if not s.any():
            continue
        rows.append([k, f"{int(s.sum()):,}"] + [f"{x[s].mean():.2f}/{x[s].max()}" for x in (W1, W2, W3, W4)] +
                    [f"{Hv[s].mean():.1f}", f"{Hopp_n[s].mean():.1f}", f"{(n - v)[s].mean():.1f}"])
    md(["K", "holes", "W1 mean/max", "W2 mean/max", "W3 mean/max", "W4 mean/max", "mean H(v)", "mean H_{1-e}(n)",
        "mean n-v"], rows)

    print("\n## joint law of (W1, W2, W4): most frequent tuples, v >= 1e3")
    code = W1.astype(np.int32) * 10000 + W2.astype(np.int32) * 100 + W4
    for lab, s in [("all", big), ("K >= 6", big & (K >= 6)), ("K >= 8", big & (K >= 8))]:
        u, c = np.unique(code[s], return_counts=True)
        o = np.argsort(-c)[:15]
        print(f"{lab} ({int(s.sum()):,} holes): " + ", ".join(
            f"({u[i] // 10000},{u[i] // 100 % 100},{u[i] % 100}):{c[i]}" for i in o))
    print("\n## joint maxima: max W4 given W1, and max W1 given W4 (v >= 1e3)")
    print("max W4 | W1 = j:", {j: int(W4[big & (W1 == j)].max()) for j in range(0, W1[big].max() + 1) if (big & (W1 == j)).any()})
    print("max W1 | W4 = j:", {j: int(W1[big & (W4 == j)].max()) for j in range(0, W4[big].max() + 1) if (big & (W4 == j)).any()})
    print("\n## share of K paid by each class, by K (v >= 1e3): sum Wi / sum K")
    rows = []
    for k in range(1, 12):
        s = big & (K == k)
        if s.any():
            t = K[s].sum()
            rows.append([k] + [f"{x[s].sum() / t:.3f}" for x in (W1, W2, W3, W4)])
    md(["K", "W1", "W2", "W3", "W4"], rows)

    print("\n## all holes with K >= 9")
    s = np.flatnonzero(done & (K >= 9))
    rows = []
    for i in s[np.lexsort((v[s], -K[s]))]:
        rows.append([f"{v[i]:,}", K[i], f"({W1[i]},{W2[i]},{W3[i]},{W4[i]})", n[i] - v[i] + 1, Hv[i], Hopp_v1[i],
                     Hopp_n[i], f"({S1[i]},{S2[i]},{S3[i]},{S4[i]})", f"{E1p[i]:.2f}", f"{E4p[i]:.2f}",
                     f"{E1g[i]:.2f}", f"{E4g[i]:.2f}", Mv[i], KbM[i], Kbu[i]])
    md(["v", "K", "(W1,W2,W3,W4)", "L", "H(v)", "H_{1-e}(v-1)", "H_{1-e}(n)", "slots (S1..S4)", "E1p", "E4p",
        "E1g", "E4g", "max a(1..v-1)-v", "K below max", "K below 1st Late"], rows)

    # ================= 2 null models
    print("\n# 2. Null models (completed holes, v >= 1e3)")
    print("O = observed; g = hypergeometric K*S_i/M; j = jitter +-%d slots; p = random primes sum 2/ln(w+v)" % args.R)

    def nulltab(groups, title):
        print(f"\n## by {title}")
        rows = []
        for lab, s in groups:
            if s.sum() < 50:
                continue
            o1, o4 = W1[s].sum(), W4[s].sum()
            r = [lab, f"{int(s.sum()):,}"]
            for o, eg, ej, ep in ((o1, E1g, E1j, E1p), (o4, E4g, E4j, E4p)):
                r += [f"{o / s.sum():.3f}", f"{o / eg[s].sum():.3f}", f"{o / ej[s].sum():.3f}", f"{o / ep[s].sum():.3f}"]
            # dispersion vs random-prime model: var(O - E) / mean(E)
            for o, ep in ((W1, E1p), (W4, E4p)):
                r.append(f"{np.var(o[s] - ep[s]) / ep[s].mean():.2f}")
            rows.append(r)
        md([title, "holes", "W1 mean", "W1 O/g", "W1 O/j", "W1 O/p", "W4 mean", "W4 O/g", "W4 O/j", "W4 O/p",
            "W1 disp(p)", "W4 disp(p)"], rows)

    nulltab([(str(k), big & (K == k)) for k in range(0, 12)] + [("all", big)], "K")
    hb = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 40), (40, 60), (60, 200)]
    nulltab([(f"[{lo},{hi})", big & (Hn >= lo) & (Hn < hi)) for lo, hi in hb], "H(n)")
    nulltab([(f"[{lo},{hi})", big & (Hv >= lo) & (Hv < hi)) for lo, hi in hb], "H(v)")
    nulltab([(f"[1e{d},1e{d+1})", done & (dec == d)) for d in decs], "decade")

    # hypergeometric tails: K primes placed uniformly on the M slots; class sizes fixed
    print("\n## tails vs hypergeometric mixture (K primes uniform on the M = S1+..+S4 slots), v >= 1e3")
    Mslots = (S1 + S2 + S3 + S4).astype(np.int16)

    def hyp_tail_mix(Sc, Obs, sel, jmax=10):
        kk, ss, mm = K[sel].astype(np.int64), Sc[sel].astype(np.int64), Mslots[sel].astype(np.int64)
        key = (kk.astype(np.int64) * 4096 + ss) * 4096 + mm
        u, inv = np.unique(key, return_inverse=True)
        ku, su, mu = u // (4096 * 4096), u // 4096 % 4096, u % 4096
        tails = np.zeros((len(u), jmax + 1))
        varu = np.zeros(len(u))
        for t in range(len(u)):
            k_, s_, m_ = int(ku[t]), int(su[t]), int(mu[t])
            if m_ == 0:
                tails[t, 0] = 1; continue
            den = math.comb(m_, k_)
            pm = [math.comb(s_, i) * math.comb(m_ - s_, k_ - i) / den for i in range(0, min(k_, s_) + 1)]
            cs = np.cumsum(pm[::-1])[::-1]
            for j in range(min(len(cs), jmax + 1)):
                tails[t, j] = cs[j]
            p_ = s_ / m_
            varu[t] = k_ * p_ * (1 - p_) * ((m_ - k_) / (m_ - 1) if m_ > 1 else 0)
        cnt = np.bincount(inv, minlength=len(u))
        pred = (tails * cnt[:, None]).sum(0)
        meanvar = (varu * cnt).sum() / cnt.sum()
        return pred, meanvar

    rows = []
    preds = {}
    for name, Sc, Obs in (("W4", S4, W4), ("W1", S1, W1), ("W1+W4", S1 + S4, W1 + W4)):
        pred, mv = hyp_tail_mix(Sc, Obs, big)
        preds[name] = pred
        Eg = K * Sc / np.maximum(Mslots, 1)
        print(f"{name}: var(O - E_g) = {np.var((Obs - Eg)[big]):.4f} vs mean hypergeometric variance {mv:.4f} "
              f"(ratio {np.var((Obs - Eg)[big]) / mv:.2f})")
    for j in range(1, 11):
        rows.append([j] + sum([[int(((W4 if nm == "W4" else W1 if nm == "W1" else W1 + W4)[big] >= j).sum()),
                                f"{preds[nm][j]:.1f}"] for nm in ("W4", "W1", "W1+W4")], []))
    md(["j", "#W4>=j", "hyp pred", "#W1>=j", "hyp pred", "#W1+W4>=j", "hyp pred"], rows)

    # Poisson tails of W1 + W4 under the random-prime model, mixture over holes
    print("\n## tail of W1 + W4 vs Poisson(E1p + E4p) mixture, and W4 vs Poisson(E4p) (v >= 1e3)")
    lam14 = (E1p + E4p)[big]
    lam4 = E4p[big]
    o14 = (W1 + W4)[big]
    o4 = W4[big]
    rows = []
    for j in range(1, 11):
        def ptail(lam, j):
            # P(Pois(lam) >= j) = 1 - sum_{i<j} e^-lam lam^i / i!
            acc = np.zeros_like(lam); term = np.exp(-lam)
            for i in range(j):
                acc += term; term = term * lam / (i + 1)
            return np.clip(1 - acc, 0, None).sum()
        rows.append([j, int((o14 >= j).sum()), f"{ptail(lam14, j):.1f}", int((o4 >= j).sum()), f"{ptail(lam4, j):.1f}"])
    md(["j", "#(W1+W4 >= j)", "Poisson pred", "#(W4 >= j)", "Poisson pred"], rows)

    # ================= 3 geometry
    print("\n# 3. Geometry")
    ph = ld("p_hole.i32", np.int32)
    pg = ld("p_geo.i16", np.int16).reshape(-1, 3)
    pc = ld("p_cls.u8", np.uint8)
    pcl = pc & 15
    pchain = pc >> 4
    dwv, dnw, dMw = [np.ascontiguousarray(c).astype(np.int32) for c in pg.T]
    del pg
    pbig = big[ph]
    win = (n - v)[ph]
    for c, name in ((4, "Late W4"), (1, "Ahead W1"), (2, "steal W2"), (3, "W3")):
        s = pbig & (pcl == c)
        t = dwv[s] / win[s]
        print(f"{name}: {int(s.sum()):,} partners; n - w: mean {dnw[s].mean():.1f}, p50 {np.median(dnw[s]):.0f}, "
              f"p90 {np.percentile(dnw[s], 90):.0f}, p99 {np.percentile(dnw[s], 99):.0f}, max {dnw[s].max()}; "
              f"w - v: mean {dwv[s].mean():.1f}, p50 {np.median(dwv[s]):.0f}, p99 {np.percentile(dwv[s], 99):.0f}, "
              f"max {dwv[s].max()}; relative position (w-v)/(n-v): mean {t.mean():.3f}, "
              f"deciles {np.round(np.percentile(t, [10, 25, 50, 75, 90]), 2).tolist()}")
    s = pbig & (pcl == 1)
    print(f"Ahead partners vs running max M = max a(1..v-1): M - w mean {dMw[s].mean():.1f}, p50 {np.median(dMw[s]):.0f}, "
          f"p1 {np.percentile(dMw[s], 1):.0f}, min {dMw[s].min()}, p99 {np.percentile(dMw[s], 99):.0f}, max {dMw[s].max()};"
          f" fraction with w > (v+M)/2: {np.mean(dwv[s] > (Mv[ph][s] / 2)):.3f}")
    print(f"running max at v: M - v mean {Mv[big].mean():.1f}, max {Mv[big].max()}; Ahead set size mean "
          f"{Atot[big].mean():.2f}, max {Atot[big].max()}")
    # histogram of n - w for Late, and fraction of Late partners in the top part of the window
    s = pbig & (pcl == 4)
    hist = np.bincount(np.minimum(dnw[s], 259) // 10, minlength=26)
    print("Late partners, histogram of n - w in bins of 10:", hist.tolist())
    s1 = pbig & (pcl == 1)
    hist = np.bincount(np.minimum(dwv[s1], 259) // 10, minlength=26)
    print("Ahead partners, histogram of w - v in bins of 10:", hist.tolist())
    hist = np.bincount(np.clip(dMw[s1], 0, 259) // 10, minlength=26)
    print("Ahead partners, histogram of M - w in bins of 10:", hist.tolist())

    print("\n## cut decompositions: K = K_below + K_above")
    print("cut A: m = max a(1..v-1) (partners above it cannot be Ahead).  cut B: m = smallest Late slot u4 (below it no Late)")
    rows = []
    for d in decs:
        s = done & (dec == d)
        KaM = K - KbM; Kau = K - Kbu
        rows.append([f"[1e{d},1e{d+1})", K[s].max(), KbM[s].max(), KaM[s].max(), f"{KbM[s].mean():.2f}",
                     f"{KaM[s].mean():.2f}", (KbM - W1)[s].max(), Kbu[s].max(), Kau[s].max(),
                     f"{Kbu[s].mean():.2f}", f"{Kau[s].mean():.2f}", (Kau - W4)[s].max()])
    md(["v range", "max K", "max K<=M", "max K>M", "mean K<=M", "mean K>M", "max (K<=M) - W1",
        "max K<u4", "max K>=u4", "mean K<u4", "mean K>=u4", "max (K>=u4) - W4"], rows)
    # combined: Ahead side and Late side
    print("max over holes with K >= 9 of (K<=M, K>M, K<u4, K>=u4):",
          [(int(v[i]), int(KbM[i]), int(K[i] - KbM[i]), int(Kbu[i]), int(K[i] - Kbu[i]))
           for i in np.flatnonzero(done & (K >= 9))][:20])
    # fraction of n beyond M
    print(f"fraction of holes with n <= M (whole window below running max): {np.mean((n - v)[big] <= Mv[big]):.3f}")

    # ================= 4 recursion
    print("\n# 4. Recursion / contraction (v >= 1e3)")
    print("Kal_v = max K(u) over holes u < v alive at time v (-1 if none); Kal_n = max K(u), u != v alive at time n")
    rows = []
    for k in range(-1, 12):
        s = big & (Kal_v == k)
        if s.sum():
            rows.append([k, f"{int(s.sum()):,}", K[s].max(), f"{K[s].mean():.2f}", (W1 + W4)[s].max()])
    md(["Kal_v", "holes", "max K(v)", "mean K(v)", "max W1+W4"], rows)
    print("\nbest beta for K(v) <= alpha * X + beta over all completed holes v >= 1e3:")
    rows = []
    for name, X in (("Kal_v", np.maximum(Kal_v, 0)), ("Kal_n", np.maximum(Kal_n, 0)), ("H(v)", Hv),
                    ("H_{1-e}(n)", Hopp_n), ("H(v)+H_{1-e}(n)", Hv + Hopp_n), ("sqrt(H(v)+H_{1-e}(n))", np.sqrt(Hv + Hopp_n)),
                    ("ln v", lg)):
        r = [name]
        for al in (0, 0.25, 0.5, 0.75, 1.0):
            r.append(f"{(K[big] - al * X[big]).max():.2f}")
        rows.append(r)
    md(["X", "a=0", "a=0.25", "a=0.5", "a=0.75", "a=1"], rows)
    print("\nsame for W1 + W4:")
    rows = []
    for name, X in (("Kal_v", np.maximum(Kal_v, 0)), ("H(v)", Hv), ("H_{1-e}(n)", Hopp_n),
                    ("H_{1-e}(v-1)+H_{1-e}(n)", Hopp_v1 + Hopp_n), ("ln v", lg)):
        r = [name]
        for al in (0, 0.25, 0.5, 0.75, 1.0):
            r.append(f"{((W1 + W4)[big] - al * X[big]).max():.2f}")
        rows.append(r)
    md(["X", "a=0", "a=0.25", "a=0.5", "a=0.75", "a=1"], rows)

    print("\n## what follows the fill: a(n+2) vs the Late partners of v (holes with W4 >= 1, v >= 1e3)")
    s = pbig & (pcl == 4)
    hidx, first = np.unique(ph[s], return_index=True)
    wmin = (dwv[s][first] + v[hidx])
    ok = n[hidx] + 1 < N
    hidx, wmin = hidx[ok], wmin[ok]
    nxt = a[n[hidx] + 1].astype(np.int64)  # a(n+2) is a[n+1]
    # is a(n+2) a Late partner of v?  w + v prime and w a Late slot
    in_w4 = ((nxt - v[hidx]) % 2 == 1) & (nxt > v[hidx]) & (nxt <= n[hidx])
    print(f"holes: {len(hidx):,}; a(n+2) = min Late partner: {np.mean(nxt == wmin):.3f}; a(n+2) < min Late partner: "
          f"{np.mean(nxt < wmin):.3f}; a(n+2) in (v, n] (so a Late slot, partner of v since v + a(n+2) prime): {np.mean(in_w4):.3f}")
    print(f"  check: a(n+2) <= min Late partner always (greedy): {bool(np.all(nxt <= wmin))}")

    print("\n## Late partners vs (n - c ln^2 n, n]")
    s = pbig & (pcl == 4)
    nn = n[ph][s].astype(np.float64)
    r = dnw[s] / np.log(nn) ** 2
    print(f"max (n - w)/ln^2 n over Late partners: {r.max():.3f}; p99.9 {np.percentile(r, 99.9):.3f}")
    rr = (n - v)[big] / np.log(n[big].astype(float)) ** 2
    print(f"max (n - v)/ln^2 n over holes: {rr.max():.3f} (so any window (n - c ln^2 n, n] with c >= this contains all"
          f" Late slots; the inequality is then the definition, not a contraction)")
    print("\n## Ahead set: all of it vs. partners")
    rows = []
    for d in decs:
        s = done & (dec == d)
        rows.append([f"[1e{d},1e{d+1})", Atot[s].max(), f"{Atot[s].mean():.2f}", AP[s].max(), f"{AP[s].mean():.2f}",
                     W1[s].max(), f"{(AP[s].sum() / (Atot[s] * 2.0 / (lg[s] + np.log(2))).sum()):.3f}"])
    md(["v range", "max |Ahead(v)|", "mean", "max #Ahead partners (any w)", "mean", "max W1 (w <= n)",
        "#Ahead partners / sum 2|A|/ln(2v)"], rows)

    print("\n## chain flags: was the Ahead value w = a(k) produced right after a hole fill a(k-1) < k-1?")
    sf = ld("step_flags.u8", np.uint8)
    up = np.flatnonzero(sf & 4) + 1  # k with a(k) > k
    up = up[up >= 2]
    prev = sf[up - 2]
    print(f"baseline over all k with a(k) > k: P(a(k-1) < k-1) = {np.mean(prev & 1):.3f}, "
          f"P(a(k-1) frontier) = {np.mean((prev & 2) > 0):.3f}, P(a(k-1) frontier and < k-1) = {np.mean((prev & 3) == 3):.3f}")
    pr = sf[:N - 1]  # flags of step k-1 for k = 2..N
    print(f"baseline over all k: P(a(k-1) < k-1) = {np.mean(pr & 1):.3f}, P(frontier) = {np.mean((pr & 2) > 0):.3f}")
    s = pbig & (pcl == 1)
    ch = pchain[s]
    print(f"Ahead partners (W1): P(pred fill) = {np.mean(ch & 1):.3f}, P(pred frontier) = {np.mean((ch & 2) > 0):.3f}, "
          f"P(pred frontier fill) = {np.mean((ch & 3) == 3):.3f}")
    for k in (6, 8):
        sk = s & (K[ph] >= k)
        if sk.any():
            ch = pchain[sk]
            print(f"  for holes with K >= {k}: P(pred fill) = {np.mean(ch & 1):.3f}, P(pred frontier fill) = "
                  f"{np.mean((ch & 3) == 3):.3f}")

    # pre-steal: an Ahead partner w = a(k) (k <= v-1) forces a(k+1) < v, since v is unused at time k+1 <= v
    s = pbig & (pcl == 1)
    vv = v[ph[s]].astype(np.int64)
    ww = dwv[s] + vv
    kk = fi[ww].astype(np.int64)
    y = a[kk].astype(np.int64)  # a(k+1)
    print(f"Ahead partners: a(k+1) < v always: {bool(np.all(y < vv))}; a(k+1) < k+1 (fills a hole): {np.mean(y < kk + 1):.3f}; "
          f"a(k+1) = k+1: {np.mean(y == kk + 1):.3f}; k+1 < a(k+1) < v: {np.mean((y > kk + 1) & (y < vv)):.3f}")
    print(f"  v - k (how long before v the Ahead partner was placed): mean {np.mean(vv - kk):.1f}, p50 {np.median(vv - kk):.0f}, "
          f"p99 {np.percentile(vv - kk, 99):.0f}, max {int((vv - kk).max())}")
    # injectivity count: distinct a(k+1) per hole equals W1 (k distinct -> a(k+1) distinct), so W1 <= #{y < v, y = eps, used at a time k+1 <= v right after an Ahead partner}
    del vv, ww, kk, y

    # ================= 5 candidates
    print("\n# 5. Candidate statements")
    X = W1 + W4
    rows = []
    for d in decs:
        s = done & (dec == d)
        i = np.flatnonzero(s)[np.argmax(X[s])]
        rows.append([f"[1e{d},1e{d+1})", X[s].max(), f"{v[i]:,}", f"{(X[s] / lg[s]).max():.3f}",
                     f"{(K[s] / lg[s]).max():.3f}", f"{((W1 + W4 + W2)[s]).max()}",
                     f"{np.percentile(X[s], 99.99):.0f}"])
    md(["v range", "max W1+W4", "at v", "max (W1+W4)/ln v", "max K/ln v", "max W1+W2+W4", "q99.99 W1+W4"], rows)
    blocks = [(k * 10 ** 7, (k + 1) * 10 ** 7) for k in range(1, 10) if k * 10 ** 7 < N]
    print("max W1+W4 per 10^7 block:", [int(X[done & (v >= lo) & (v < hi)].max()) for lo, hi in blocks])
    print("max W4 per 10^7 block:", [int(W4[done & (v >= lo) & (v < hi)].max()) for lo, hi in blocks])
    print("max W1 per 10^7 block:", [int(W1[done & (v >= lo) & (v < hi)].max()) for lo, hi in blocks])
    print("tail P(W1+W4 >= j), v < 1e7 vs [1e7,1e8):")
    for j in range(3, 11):
        a_ = np.mean(X[done & (v < 10 ** 7) & (v >= 1000)] >= j)
        b_ = np.mean(X[done & (v >= 10 ** 7)] >= j) if (done & (v >= 10 ** 7)).any() else float("nan")
        print(f"  j={j}: {a_:.2e}  {b_:.2e}")
    # excess over random-prime null
    ex = X - (E1p + E4p)
    print(f"max (W1+W4) - (E1p+E4p): {ex[big].max():.2f} at v = {int(v[big][np.argmax(ex[big])]):,}; "
          f"max per decade: {[round(float(ex[done & (dec == d)].max()), 2) for d in decs]}")
    print(f"max (W1+W4) / (E1p+E4p+1): {(X / (E1p + E4p + 1))[big].max():.2f}")
    # open holes
    print(f"\nopen holes at N ({int((~done).sum())}): K, W1, W4 =",
          [(int(v[i]), int(K[i]), int(W1[i]), int(W4[i])) for i in np.flatnonzero(~done)])


if __name__ == "__main__":
    main()
