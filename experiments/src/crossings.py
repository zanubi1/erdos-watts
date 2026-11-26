"""Down-crossings of levels in the Watts greedy sequence (A055265), and the crossing bound C012.

X_v(n) = #{ j in [2, n] : a(j-1) > v > a(j) }  (down-crossings of level v up to time n).

For every hole v (2 <= v <= N, fi(v) > v or never used by N) at n = fi(v) - 1 (or N), with eps = v mod 2:
  1 C012          K <= X_v(n) + 1 + H_{1-eps}(n) and |W1| + |W2| <= X_v(n); parity-refined forms
  2 size of X     X_v(n) per decade, against H(v) - 1 (the L009 bound for W1 + W2), X / ln v
  3 all levels    X_v(N) for every level v; where (j - v, j - fi(v)) the crossings happen; up/down identity
  4 bounds        classification of crossings (early hole fill / early frontier / late hole fill) and
                  candidate provable bounds
  5 reduction     residual K - X - 1 that W4 must carry

Generation: experiments/src/k_survival_1e8_gen.c (sequence, via k_survival_1e8.generate) and
experiments/src/crossings_gen.c (crossing counts), both compiled with gcc on first use.
About 70 s + 60 s of C at N = 10^8; peak RAM about 6 GB; about 4 GB of binaries in --workdir.

Usage:
    python experiments/src/crossings.py --terms 100000000 --workdir /path/to/scratch
    python experiments/src/crossings.py --selftest          # brute-force check at N = 4000
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

FIELDS = ["K", "W1", "W2", "W3", "W4", "X", "XEPS", "E", "EEPS", "L", "FFRONT",
          "HV", "HV1", "H1EN", "H1EV1", "BV", "AV", "LFILL", "LFILLEPS", "U", "NVN",
          "MAXO", "XTOT", "NMV", "MMV", "HFILLE"]


def run_gen(workdir):
    if os.path.exists(os.path.join(workdir, "H_rec.i16")) and \
            os.path.getmtime(os.path.join(workdir, "H_rec.i16")) > os.path.getmtime(os.path.join(workdir, "seq.i32")):
        print(f"[crossings] reusing {workdir}")
        return
    exe = os.path.join(workdir, "crossings_gen")
    subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "crossings_gen.c")], check=True)
    t0 = time.time()
    subprocess.run([exe, workdir], check=True)
    print(f"[crossings] done in {time.time() - t0:.1f}s")


def load(workdir):
    ld = lambda name, dt: np.fromfile(os.path.join(workdir, name), dtype=dt)
    v = ld("H_v.i32", np.int32)
    n = ld("H_n.i32", np.int32)
    rec = ld("H_rec.i16", np.int16).reshape(-1, len(FIELDS))
    R = {f: np.ascontiguousarray(rec[:, i]) for i, f in enumerate(FIELDS)}   # int16 (all values < 2^15)
    del rec
    R["v"], R["n"] = v.astype(np.int64), n.astype(np.int64)
    return R


def md(header, rows):
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


def decades(N):
    out, e = [], 1
    while 10 ** e < N:
        hi = 10 ** (e + 1)
        out.append((10 ** e, hi + 1 if hi == N else hi, f"[1e{e},1e{e+1}" + ("]" if hi == N else ")")))
        e += 1
    return out


# ---------------------------------------------------------------- brute force
def selftest(N=4000):
    import tempfile as tf
    wd = tf.mkdtemp(prefix="crossings_selftest_")
    _, a, fi, h0, h1, isp = generate(N, wd)
    run_gen(wd)
    R = load(wd)
    a = [0] + [int(x) for x in a]          # 1-indexed
    fi_ = [int(x) for x in fi]
    used_at = lambda x: fi_[x] if x < len(fi_) and fi_[x] > 0 else 10 ** 18
    isprime = lambda m: m > 1 and all(m % p for p in range(2, int(m ** 0.5) + 1))
    def Hp(p, m):
        return sum(1 for x in range(1, m + 1) if x % 2 == p and used_at(x) > m)
    bad = 0
    Ld = np.fromfile(os.path.join(wd, "L_Xd.i16"), dtype=np.int16)
    Lu = np.fromfile(os.path.join(wd, "L_Xu.i16"), dtype=np.int16)
    for v in range(2, N + 1):
        D = sum(1 for j in range(2, N + 1) if a[j - 1] > v > a[j])
        U = sum(1 for j in range(2, N + 1) if a[j - 1] < v < a[j])
        if D != Ld[v] or U != Lu[v]:
            bad += 1
    idx = {int(v): i for i, v in enumerate(R["v"])}
    nh = 0
    for v in range(2, N + 1):
        f = used_at(v)
        if not (f > v):
            continue
        nh += 1
        i = idx[v]
        n = N if f > N else f - 1
        e = v % 2
        W = [0] * 5
        for w in range(v + 1, n + 1, 2):
            if isprime(w + v):
                g = used_at(w)
                W[4 if g > n else 3 if g == n else 2 if g >= v else 1] += 1
        cr = [j for j in range(2, n + 1) if a[j - 1] > v > a[j]]
        ref = dict(K=sum(W), W1=W[1], W2=W[2], W3=W[3], W4=W[4], X=len(cr),
                   XEPS=sum(1 for j in cr if a[j] % 2 == e), E=sum(1 for j in cr if j <= v),
                   EEPS=sum(1 for j in cr if j <= v and a[j] % 2 == e), L=sum(1 for j in cr if j > v),
                   FFRONT=sum(1 for j in cr if a[j] >= j), HFILLE=sum(1 for j in cr if j <= v and a[j] <= j - 1),
                   HV=Hp(0, v) + Hp(1, v), HV1=Hp(0, v - 1) + Hp(1, v - 1), H1EN=Hp(1 - e, n),
                   H1EV1=Hp(1 - e, v - 1), BV=Hp(e, v) - 1,
                   AV=sum(1 for k in range(1, v) if a[k] > v),
                   LFILL=sum(1 for x in range(1, v) if v < used_at(x) <= n),
                   LFILLEPS=sum(1 for x in range(1, v) if v < used_at(x) <= n and x % 2 == e),
                   U=sum(1 for j in range(2, n + 1) if a[j - 1] < v < a[j]),
                   NVN=sum(1 for k in range(1, n + 1) if a[k] > v), XTOT=int(Ld[v]), NMV=n - v,
                   MMV=max(a[1:v]) - v)
        for k, val in ref.items():
            if R[k][i] != val:
                bad += 1
                if bad < 10:
                    print("mismatch", v, k, R[k][i], val)
    print(f"selftest N={N}: {nh} holes, {bad} mismatches")
    return bad == 0


# ---------------------------------------------------------------- analysis
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--terms", type=int, default=100_000_000)
    ap.add_argument("--workdir", default=os.path.join(tempfile.gettempdir(), "crossings_work"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)

    N, a, fi, h0, h1, isp = generate(args.terms, args.workdir)
    assert list(a[:20]) == OEIS_FIRST, "first 20 terms do not match A055265"
    print("first 20 terms match A055265")
    del isp
    Hall = (h0 + h1).astype(np.int16)  # Hall[m-1] = H(m)
    del h0, h1
    run_gen(args.workdir)
    R = load(args.workdir)
    v, n = R["v"], R["n"]
    lnv = np.log(np.maximum(v, 2).astype(np.float64))
    for k in ("K", "W1", "W2", "W4", "X", "XEPS", "HV"):
        R[k] = R[k].astype(np.int32)
    K, W1, W2, W4, X, XE = R["K"], R["W1"], R["W2"], R["W4"], R["X"], R["XEPS"]
    HV = R["HV"]
    print(f"N = {N:,}, holes = {len(v):,}")
    pw = os.path.join(args.workdir, "h_W.i8")
    if os.path.exists(pw) and os.path.getsize(pw) == 5 * len(v):   # cross-check against partners_gen.c
        Wp = np.fromfile(pw, dtype=np.int8).reshape(-1, 5)
        mism = sum(int((Wp[:, i] != R[f]).sum()) for i, f in enumerate(["K", "W1", "W2", "W3", "W4"]))
        print(f"cross-check K, W1..W4 against partners_gen.c output: {mism} mismatches")
        del Wp
    D = decades(N)
    sel = lambda lo, hi: (v >= lo) & (v < hi)

    # ---------------- 1
    print("\n## 1. C012\n")
    checks = [
        ("K <= X + 1 + H_{1-e}(n)", lambda: K - (X + 1 + R["H1EN"])),
        ("W1 + W2 <= X", lambda: W1 + W2 - X),
        ("W1 + W2 <= X^eps", lambda: W1 + W2 - XE),
        ("W1 <= E^eps", lambda: W1 - R["EEPS"]),
        ("W2 <= L", lambda: W2 - R["L"]),
        ("W2 <= L^eps (= X^eps - E^eps)", lambda: W2 - (XE - R["EEPS"])),
        ("K <= X^eps + 1 + H_{1-e}(n)", lambda: K - (XE + 1 + R["H1EN"])),
        ("W3 <= 1", lambda: R["W3"] - 1),
        ("W4 <= H_{1-e}(n)", lambda: W4 - R["H1EN"]),
    ]
    rows = []
    for name, fn in checks:
        d = fn()
        rows.append([name, int((d > 0).sum()), int((d == 0).sum()), f"{(d == 0).mean():.4f}", int(d.max())])
    md(["inequality", "violations", "equality", "eq. frac", "max(lhs-rhs)"], rows)

    # ---------------- 2
    print("\n## 2. Size of X_v(n) at holes\n")
    rows = []
    for lo, hi, lab in D:
        s = sel(lo, hi)
        if not s.any():
            continue
        x, xe, h = X[s], XE[s], HV[s] - 1
        rows.append([lab, int(s.sum()), int(x.max()), f"{x.mean():.3f}", int(np.percentile(x, 99)), int(xe.max()),
                     int(h.max()), f"{(x < h).mean():.3f}", f"{(x == h).mean():.3f}", f"{(x > h).mean():.3f}",
                     f"{(xe < h).mean():.3f}", f"{(xe == h).mean():.3f}", int((xe > h).sum()),
                     f"{(x / lnv[s]).max():.3f}"])
    md(["v", "holes", "max X", "mean X", "p99 X", "max X^eps", "max H(v)-1", "X<H-1", "X=H-1", "X>H-1",
        "X^e<H-1", "X^e=H-1", "#X^e>H-1", "max X/ln v"], rows)
    print("\nDistribution of X_v(n) over all holes with v >= 10^3:")
    s = v >= 1000
    vals, cnts = np.unique(X[s], return_counts=True)
    md(["X"] + [str(t) for t in vals], [["count"] + [int(t) for t in cnts]])
    print("\nX - (H(v)-1) distribution (v >= 10^3):")
    vals, cnts = np.unique(X[s] - (HV[s] - 1), return_counts=True)
    md(["X-(H-1)"] + [str(t) for t in vals], [["count"] + [int(t) for t in cnts]])
    i = int(np.argmax(X))
    print(f"\nmax X = {X[i]} at v = {v[i]:,} (n - v = {R['NMV'][i]}, H(v) = {HV[i]}, K = {K[i]})")
    s3 = v >= 1000
    j = int(np.argmax(np.where(s3, X / lnv, -1)))
    print(f"max X/ln v (v >= 10^3) = {X[j] / lnv[j]:.3f} at v = {v[j]:,} (X = {X[j]})")
    # top X holes
    print("\nTop 10 holes by X_v(n):")
    top = np.argsort(-X, kind="stable")[:10]
    md(["v", "n-v", "X", "X^eps", "E", "L", "H(v)", "H_{1-e}(n)", "K", "W1", "W2", "W4", "max a(1..v-1)-v"],
       [[f"{v[t]:,}", R["NMV"][t], X[t], XE[t], R["E"][t], R["L"][t], HV[t], R["H1EN"][t], K[t], W1[t], W2[t],
         W4[t], R["MMV"][t]] for t in top])

    # ---------------- 3
    print("\n## 3. Crossings of all levels\n")
    ldl = lambda name: np.fromfile(os.path.join(args.workdir, name), dtype=np.int16)
    Xd, Xu = ldl("L_Xd.i16"), ldl("L_Xu.i16")
    dmin, dmax, fmin, fmax = ldl("L_dmin.i16"), ldl("L_dmax.i16"), ldl("L_fmin.i16"), ldl("L_fmax.i16")
    a64 = a  # int32
    # only levels whose crossings are complete: v <= N - 2000 (no crossing of v can occur after time v+~400)
    Vtop = N - 5000
    lv = np.arange(N + 1)
    rows = []
    for lo, hi, lab in D:
        hi2 = min(hi, Vtop)
        if lo >= hi2:
            continue
        s = slice(lo, hi2)
        xd = Xd[s].astype(np.int32)
        has = xd > 0
        lnl = np.log(lv[s].astype(np.float64))
        dm = dmin[s][has]; dM = dmax[s][has]; fm = fmin[s][has & (fi[lo:hi2] > 0)]; fM = fmax[s][has & (fi[lo:hi2] > 0)]
        dl, dh = max(lo - 1, 0), min(hi2, N)
        rows.append([lab, int(xd.max()), f"{xd.mean():.3f}", f"{(xd == 0).mean():.3f}", f"{(xd / lnl).max():.3f}",
                     int(dm.min()), int(dM.max()), int(fm.min()), int(fM.max()),
                     int((a[dl:dh] - np.arange(dl + 1, dh + 1, dtype=np.int32)).max()),
                     int(-(a[dl:dh] - np.arange(dl + 1, dh + 1, dtype=np.int32)).min())])
    md(["levels v", "max X_v(inf)", "mean", "frac 0", "max X/ln v", "min j-v", "max j-v", "min j-fi(v)",
        "max j-fi(v)", "max a(j)-j", "max j-a(j)"], rows)
    print(f"(levels v <= N - 5000 only; mean X_v(inf) over all those levels = {Xd[2:Vtop].mean():.4f})")
    hd = np.fromfile(os.path.join(args.workdir, "hist_jmv.i64"), dtype=np.int64)
    hf = np.fromfile(os.path.join(args.workdir, "hist_jmfi.i64"), dtype=np.int64)
    def pct(h, off, qs):
        c = np.cumsum(h) / h.sum()
        return [int(np.searchsorted(c, q)) - off for q in qs]
    qs = [0.0001, 0.01, 0.1, 0.5, 0.9, 0.99, 0.9999]
    print("\nQuantiles over all down-crossings (all levels):")
    md(["quantity"] + [str(q) for q in qs], [["j - v"] + pct(hd, 2000, qs), ["j - fi(v)"] + pct(hf, 4000, qs)])
    print(f"fraction of crossings with j < fi(v): {hf[:4000].sum() / hf.sum():.4f}; "
          f"with j <= v: {hd[:2001].sum() / hd.sum():.4f}")
    # identity: U - D = [a(N) > v] - [a(f+1) > v] + [a(f-1) > v] for 1 < f < N
    nfail, CH = 0, 10 ** 7
    for c0 in range(2, N + 1, CH):
        c1 = min(c0 + CH, N + 1)
        f = fi[c0:c1].astype(np.int64)
        vv = np.arange(c0, c1, dtype=np.int64)
        t1 = (int(a[-1]) > vv).astype(np.int32)
        i2 = (f >= 1) & (f + 1 <= N)          # entry from v into "above" at time f+1
        i3 = (f >= 2) & (f <= N)              # exit from "above" into v at time f
        t2 = np.where(i2, a[np.where(i2, f, 0)] > vv, False).astype(np.int32)        # a(f+1) = a[f]
        t3 = np.where(i3, a[np.where(i3, f - 2, 0)] > vv, False).astype(np.int32)    # a(f-1) = a[f-2]
        lhs = Xu[c0:c1].astype(np.int32) - Xd[c0:c1]
        nfail += int((lhs != t1 - t2 + t3).sum())
    del f, vv, t1, t2, t3, i2, i3, lhs
    print(f"\nIdentity U_v(N) - X_v(N) = [a(N)>v] - [a(fi+1)>v] + [a(fi-1)>v]: "
          f"{nfail} failures over {N - 1:,} levels")
    hid = R["U"].astype(np.int32) - X - (a64[n - 1] > v).astype(np.int32)
    print(f"Hole identity X_v(n) = U_v(n) - [a(n) > v]: {int((hid != 0).sum())} failures")
    # provable all-level bound: X_v(N) <= H(v-1) + H(v) - [fi(v) != v]
    lvl = np.arange(2, Vtop)
    fv = fi[2:Vtop]
    bnd = Hall[lvl - 2].astype(np.int32) + Hall[lvl - 1] - ((fv != lvl)).astype(np.int32)
    dd = Xd[2:Vtop].astype(np.int32) - bnd
    print(f"All-level bound X_v(inf) <= H(v-1) + H(v) - [fi(v) != v]: {int((dd > 0).sum())} violations, "
          f"equality {(dd == 0).mean():.4f}, max lhs-rhs {int(dd.max())}")
    del lvl, fv, bnd, dd
    vals, cnts = np.unique(Xd[2:Vtop], return_counts=True)
    print("\nDistribution of X_v(inf) over levels 2..N-5000:")
    md(["X"] + [str(t) for t in vals], [["count"] + [int(t) for t in cnts]])
    # holes: X(inf) vs X(n)
    after = R["XTOT"] - X
    print(f"\nHoles: crossings after the fill (X_v(inf) - X_v(n)): mean {after.mean():.3f}, max {after.max()}")
    nonh = np.ones(N + 1, bool); nonh[v] = False; nonh[:2] = False; nonh[Vtop:] = False
    print(f"Non-holes (fi(v) <= v): mean X_v(inf) {Xd[nonh].mean():.3f}, max {Xd[nonh].max()}; "
          f"holes (v <= N-5000): mean {Xd[v[v < Vtop]].mean():.3f}, max {Xd[v[v < Vtop]].max()}")

    # ---------------- 4
    del Xd, Xu, dmin, dmax, fmin, fmax, Hall
    print("\n## 4. Classification and bounds\n")
    print(f"AV == H(v-1) (Sub-lemma S at m = v-1, v unused): {int((R['AV'] != R['HV1']).sum())} failures")
    E, L, FF, HFE = R["E"], R["L"], R["FFRONT"], R["HFILLE"]
    tot = X.sum()
    print(f"All crossings j <= n of hole levels: {tot:,}. early (j <= v): {E.sum() / tot:.4f} "
          f"[hole fill a(j) <= j-1: {HFE.sum() / tot:.4f}, frontier a(j) >= j: {FF.sum() / tot:.4f}], "
          f"late (v < j <= n, always a hole fill < v): {L.sum() / tot:.4f}")
    print(f"check FFRONT + HFILLE == E: {int((FF + HFE != E).sum())} failures")
    cands = [
        ("E <= AV = #{k<=v-1: a(k)>v}", lambda: E - R["AV"]),
        ("E^eps <= H_{1-e}(v-1)", lambda: R["EEPS"] - R["H1EV1"]),
        ("L <= LFILL", lambda: L - R["LFILL"]),
        ("L^eps <= B(v)", lambda: (XE - R["EEPS"]) - R["BV"]),
        ("X <= AV + LFILL", lambda: X - R["AV"] - R["LFILL"]),
        ("X^eps <= H(v) - 1", lambda: XE - (HV - 1)),
        ("X <= H(v-1) + H(v) - 1", lambda: X - (R["HV1"] + HV - 1)),
        ("X <= H(v) - 1", lambda: X - (HV - 1)),
        ("X <= H(v)", lambda: X - HV),
        ("X <= H(v) + 1", lambda: X - HV - 1),
        ("X <= NVN = #{k<=n: a(k)>v}", lambda: X - R["NVN"]),
        ("X <= max O*(j-1) at crossings", lambda: X - R["MAXO"]),
        ("X <= H(v-1)", lambda: X - R["HV1"]),
        ("E <= H_{1-e}(v-1) + 1", lambda: E - R["H1EV1"] - 1),
    ]
    rows = []
    for name, fn in cands:
        d = fn()
        rows.append([name, int((d > 0).sum()), f"{(d == 0).mean():.4f}", int(d.max()), f"{d.mean():.3f}"])
    md(["candidate", "violations", "eq. frac", "max(lhs-rhs)", "mean(lhs-rhs)"], rows)
    print("\nPer decade: max E, max L, max AV, max LFILL, max (X - H(v) + 1), max X - H(v-1)")
    rows = []
    for lo, hi, lab in D:
        s = sel(lo, hi)
        if not s.any():
            continue
        rows.append([lab, int(E[s].max()), int(L[s].max()), int(R["AV"][s].max()), int(R["LFILL"][s].max()),
                     int((X[s] - HV[s] + 1).max()), int((X[s] - R["HV1"][s]).max()),
                     int((XE[s] - HV[s] + 1).max()), int(R["MAXO"][s].max())])
    md(["v", "max E", "max L", "max AV", "max LFILL", "max X-(H(v)-1)", "max X-H(v-1)", "max X^e-(H(v)-1)",
        "max O* at crossings"], rows)

    # ---------------- 5
    print("\n## 5. Residual for W4\n")
    res = K - X - 1
    rese = K - XE - 1
    rows = []
    for lo, hi, lab in D:
        s = sel(lo, hi)
        if not s.any():
            continue
        rows.append([lab, int(K[s].max()), int(res[s].max()), int(rese[s].max()), int(W4[s].max()),
                     int(R["H1EN"][s].max()), f"{(res[s] / lnv[s]).max():.3f}", int((res[s] > 0).sum()),
                     f"{(res[s] > 0).mean():.4f}"])
    md(["v", "max K", "max K-X-1", "max K-X^e-1", "max W4", "max H_{1-e}(n)", "max (K-X-1)/ln v",
        "#(K-X-1>0)", "frac"], rows)
    print("\nJoint: K-X-1 vs W4 (v >= 10^3): rows K-X-1 = r, max W4 and count")
    s = v >= 1000
    rows = []
    for r in range(int(res[s].min()), int(res[s].max()) + 1):
        t = s & (res == r)
        if t.any():
            rows.append([r, int(t.sum()), int(W4[t].max()), f"{W4[t].mean():.2f}"])
    md(["K-X-1", "count", "max W4", "mean W4"], rows)
    i = int(np.argmax(res))
    print(f"max K-X-1 = {res[i]} at v = {v[i]:,}: K = {K[i]}, X = {X[i]}, W1..W4 = {W1[i]},{W2[i]},{R['W3'][i]},"
          f"{W4[i]}, H_(1-e)(n) = {R['H1EN'][i]}, n - v = {R['NMV'][i]}")


if __name__ == "__main__":
    main()
