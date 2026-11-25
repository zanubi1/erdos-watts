"""C010 evidence to N = 10^8: primes survived by each hole.

For every hole v (2 <= v, fi(v) > v) define
    K(v) = pi(fi(v) - 1 + v) - pi(2v),
the number of primes in (2v, n + v] at the last time n = fi(v) - 1 that v is still a hole
(this is the max over n of pi(n + v) - pi(2v) while v is a hole).

Reports: max K per decade / per 10^7 block, K tail P(K >= j), max H(n), max lifetime,
worst-K holes with local prime gaps, a check of C009' (K <= H(v) + H_{1-eps}(fi(v) - 1)),
|a(n) - n| records vs OEIS A282696/A282697, and a fit of max K against log v.

Generation is done by the C helper experiments/src/k_survival_1e8_gen.c (compiled with gcc on
first use; 10^8 terms in about 10 s). Raw binaries go to --workdir (default: a temp dir under
/tmp); nothing large is written into the repo.

Memory: about 4 GB peak at N = 10^8.

Usage:
    python experiments/src/k_survival_1e8.py --terms 100000000 --workdir /path/to/scratch
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OEIS_FIRST = [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15, 14, 17, 12, 11, 18, 19, 22]
# A282696 positions paired with A282697 values * 2 (see literature/oeis-A055265.md)
OEIS_RECORDS = [(678_572, 156), (8_525_842, 188), (8_526_046, 200), (10_415_643, 224),
                (23_003_613, 236), (51_382_797, 252), (61_727_309, 262), (71_207_280, 292),
                (108_334_625, 316)]


def generate(n, workdir):
    os.makedirs(workdir, exist_ok=True)
    meta = os.path.join(workdir, "meta.txt")
    if os.path.exists(meta) and int(open(meta).read().split()[0]) == n:
        print(f"[gen] reusing {workdir}")
    else:
        exe = os.path.join(workdir, "k_survival_1e8_gen")
        subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "k_survival_1e8_gen.c")], check=True)
        t0 = time.time()
        subprocess.run([exe, str(n), workdir], check=True)
        print(f"[gen] {n:,} terms in {time.time() - t0:.1f}s")
    N, VMAX, PLIM, maxa = map(int, open(meta).read().split())
    ld = lambda name, dt: np.fromfile(os.path.join(workdir, name), dtype=dt)
    return N, ld("seq.i32", np.int32), ld("fi.i32", np.int32), ld("h0.i16", np.int16), \
        ld("h1.i16", np.int16), ld("isp.u8", np.uint8)


def ranges(N):
    out = []
    e = 1
    while 10 ** e < N:
        out.append((10 ** e, min(10 ** (e + 1), N + 1), f"[1e{e}, 1e{e+1})"))
        e += 1
    blocks = [(k * 10 ** 7, (k + 1) * 10 ** 7, f"[{k}e7, {k+1}e7)") for k in range(1, 10) if k * 10 ** 7 < N]
    return out, blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--terms", type=int, default=100_000_000)
    ap.add_argument("--workdir", default=os.path.join(tempfile.gettempdir(), "k_survival_work"))
    ap.add_argument("--top", type=int, default=20, help="number of worst-K holes to list")
    args = ap.parse_args()

    N, a, fi, h0, h1, isp = generate(args.terms, args.workdir)
    assert list(a[:20]) == OEIS_FIRST, "first 20 terms do not match A055265"
    print("first 20 terms match A055265")
    pi = np.cumsum(isp, dtype=np.int32)
    del isp
    H = (h0.astype(np.int32) + h1)  # H[m-1] = H(m)

    # ---- holes
    v = np.arange(2, N + 1, dtype=np.int64)
    f = fi[2:N + 1].astype(np.int64)
    cens = (f == 0)
    hole = (f > v) | cens
    v, f, cens = v[hole], f[hole], cens[hole]
    print(f"holes v <= N: {len(v):,}  (still open at N: {int(cens.sum()):,}, max open v-gap N - min open v = "
          f"{N - int(v[cens].min()) if cens.any() else 0})")
    n = np.where(cens, N, f - 1)
    K = (pi[n + v] - pi[2 * v]).astype(np.int16)
    L = np.where(cens, -1, f - v)
    eps = (v & 1).astype(bool)
    Hv = H[v - 1]
    Hopp_n = np.where(eps, h0[n - 1], h1[n - 1]).astype(np.int32)
    rhs = Hv + Hopp_n
    done = ~cens

    decades, blocks = ranges(N)

    def maxtable(rr, title):
        print(f"\n## max K by v range ({title}); completed holes only")
        print("| v range | holes | max K | #holes at max | first v at max | max L | v at max L | mean K |")
        print("|---|---|---|---|---|---|---|---|")
        res = []
        for lo, hi, lab in rr:
            s = done & (v >= lo) & (v < hi)
            if not s.any():
                continue
            ks = K[s]; vs = v[s]; Ls = L[s]
            mk = int(ks.max()); at = vs[ks == mk]
            j = int(np.argmax(Ls))
            print(f"| {lab} | {int(s.sum()):,} | {mk} | {len(at)} | {int(at[0]):,} | {int(Ls[j])} | {int(vs[j]):,} | {ks.mean():.3f} |")
            res.append((lo, hi, mk, int(s.sum())))
        return res

    dec_res = maxtable(decades, "decades")
    maxtable(blocks, "10^7 blocks")

    # ---- tail distribution
    J = 13
    def tail(s):
        b = np.bincount(K[s].astype(np.int64), minlength=J + 1)
        c = np.cumsum(b[::-1])[::-1] / s.sum()
        return c[:J]
    sA = done & (v < 10 ** 7)
    sB = done & (v >= 10 ** 7) & (v < 10 ** 8)
    tA, tB = tail(sA), tail(sB)
    print("\n## tail P(K >= j)")
    print("| j | v < 1e7 | ratio | v in [1e7,1e8) | ratio | B/A |")
    print("|---|---|---|---|---|---|")
    for j in range(J):
        rA = tA[j] / tA[j - 1] if j and tA[j - 1] else float("nan")
        rB = tB[j] / tB[j - 1] if j and tB[j - 1] else float("nan")
        print(f"| {j} | {tA[j]:.3e} | {rA:.3f} | {tB[j]:.3e} | {rB:.3f} | {tB[j] / tA[j] if tA[j] else float('nan'):.3f} |")
    print("\n## tail per decade P(K >= j), j = 0..10")
    print("| v range | " + " | ".join(f">={j}" for j in range(11)) + " |")
    print("|---|" + "---|" * 11)
    dec_tails = []
    for lo, hi, lab in decades + blocks:
        s = done & (v >= lo) & (v < hi)
        if s.sum() < 1000:
            continue
        t = tail(s)
        dec_tails.append((lab, t, int(s.sum())))
        print(f"| {lab} | " + " | ".join(f"{x:.2e}" for x in t[:11]) + " |")
    print("\n## exact K counts (all completed holes)")
    print(dict(enumerate(np.bincount(K[done].astype(np.int64)).tolist())))
    print("K counts v in [1e7,1e8):", dict(enumerate(np.bincount(K[sB].astype(np.int64)).tolist())))
    print("K counts v < 1e7:", dict(enumerate(np.bincount(K[sA].astype(np.int64)).tolist())))

    # ---- H and lifetimes
    print("\n## H and lifetimes")
    for lo, hi in [(1, 10 ** 7), (10 ** 7, N + 1)]:
        seg = H[lo - 1:hi - 1]
        j = int(np.argmax(seg))
        print(f"max H(n) on [{lo:,}, {hi - 1:,}]: {int(seg[j])} at n = {lo + j:,}; mean H {seg.mean():.3f}")
        s = done & (v >= lo) & (v < hi)
        jj = int(np.argmax(L[s]))
        Ls = L[s]
        print(f"   lifetimes v in range: max {int(Ls[jj])} at v = {int(v[s][jj]):,}; mean {Ls.mean():.2f}; "
              f"p99 {np.percentile(Ls, 99):.0f}; p99.9 {np.percentile(Ls, 99.9):.0f}; "
              f"P(L>=160) {np.mean(Ls >= 160):.2e}; P(L>=200) {np.mean(Ls >= 200):.2e}")

    # ---- C009' check
    print("\n## C009' check: K <= H(v) + H_{1-eps}(n), n = fi(v) - 1")
    for lo, hi in [(2, 10 ** 7), (10 ** 7, N + 1), (2, N + 1)]:
        s = done & (v >= lo) & (v < hi)
        viol = int((K[s] > rhs[s]).sum())
        eq = s & (K == rhs)
        print(f"v in [{lo:,}, {hi:,}): holes {int(s.sum()):,}, violations {viol}, equalities {int(eq.sum()):,}, "
              f"max K at equality {int(K[eq].max()) if eq.any() else '-'}, "
              f"max v with equality & K>=2 {int(v[eq & (K >= 2)].max()) if (eq & (K >= 2)).any() else '-'}, "
              f"max rhs {int(rhs[s].max())}, max K/rhs {float((K[s] / rhs[s]).max()):.3f}")
    s = done & (v >= 10 ** 7)
    for lo, hi in [(1, 3), (3, 5), (5, 10), (10, 20), (20, 40), (40, 200)]:
        t = s & (rhs >= lo) & (rhs < hi)
        if t.any():
            print(f"  [1e7,1e8) rhs in [{lo},{hi}): {int(t.sum()):,}  max K {int(K[t].max())}  "
                  f"max K/rhs {float((K[t] / rhs[t]).max()):.3f}  mean K {K[t].mean():.2f}")
    # censored holes also satisfy C009 at n = N
    print(f"open holes at N: violations at n = N: {int((K[cens] > rhs[cens]).sum())}, "
          f"max K among them {int(K[cens].max()) if cens.any() else '-'}")

    # ---- worst-K holes
    print(f"\n## worst-K holes (top {args.top} by K, then by v)")
    print("| v | K | L | H(v) | H_{1-e}(n) | primes in (2v, n+v]: gaps | max gap in [2v-500, 2v+500] | gap containing 2v |")
    print("|---|---|---|---|---|---|---|---|")
    order = np.lexsort((v, -K.astype(np.int64)))
    order = [i for i in order if done[i]][:args.top]
    isp_local = lambda lo, hi: np.flatnonzero(pi[lo:hi + 1] - pi[lo - 1:hi]) + lo  # primes in [lo, hi]
    for i in order:
        vi, ni = int(v[i]), int(n[i])
        ps = isp_local(2 * vi + 1, ni + vi)
        ps_ext = isp_local(max(3, 2 * vi - 500), 2 * vi + 500)
        g = int(np.diff(ps_ext).max())
        below = ps_ext[ps_ext <= 2 * vi]; above = ps_ext[ps_ext > 2 * vi]
        gc = int(above[0] - below[-1]) if len(below) and len(above) else -1
        gaps = np.diff(np.concatenate([[2 * vi], ps, [ni + vi]])).tolist()
        print(f"| {vi:,} | {int(K[i])} | {int(L[i])} | {int(Hv[i])} | {int(Hopp_n[i])} | {gaps} | {g} | {gc} |")

    # ---- displacement records
    print("\n## records of |a(n) - n| (code check against A282696/A282697)")
    d = np.abs(a.astype(np.int64) - np.arange(1, N + 1))
    rm = np.maximum.accumulate(d)
    rec = np.flatnonzero(np.diff(np.concatenate([[-1], rm])) > 0)
    recs = [(int(r) + 1, int(d[r])) for r in rec]
    ours = dict(recs)
    for pos, val in OEIS_RECORDS:
        if pos <= N:
            print(f"OEIS n = {pos:,}, |a-n| = {val}: ours {'MATCH' if ours.get(pos) == val else 'MISMATCH ' + str(ours.get(pos))}")
    print("our records with n >= 5e5:", [(p, x) for p, x in recs if p >= 500_000])
    print("max |a(n)-n| on [1e7, N]:", int(d[10 ** 7 - 1:].max()), "at n =", int(np.argmax(d[10 ** 7 - 1:])) + 10 ** 7)
    print("max a(n) - n:", int((a - np.arange(1, N + 1)).max()), "  max(a(1..n)) - n max:",
          int((np.maximum.accumulate(a) - np.arange(1, N + 1)).max()))

    # ---- fits
    print("\n## fit of max K vs log10 v (decade maxima, decades from 1e3)")
    xs = np.array([np.log10(np.sqrt(lo * hi)) for lo, hi, mk, c in dec_res if lo >= 1000])
    ys = np.array([mk for lo, hi, mk, c in dec_res if lo >= 1000], float)
    b, c0 = np.polyfit(xs, ys, 1)
    print("decade maxima:", list(zip(np.round(xs, 2).tolist(), ys.astype(int).tolist())))
    print(f"linear fit maxK = {c0:.3f} + {b:.3f} log10 v; residual SS {float(((c0 + b * xs - ys) ** 2).sum()):.3f}; "
          f"const fit residual SS {float(((ys - ys.mean()) ** 2).sum()):.3f}")
    # model check: if the tail were a fixed geometric law, expected max over M holes ~ j with M P(K>=j) ~ 1
    print("expected number of K >= j holes per decade under the [1e7,1e8) tail (M * P_B(K>=j)):")
    for lo, hi, mk, cnt in dec_res:
        if lo >= 1000:
            print(f"  {lo:.0e}: M = {cnt:,}, observed max {mk}, M*P_B(K>=j) j=6..12: "
                  + ", ".join(f"{cnt * tB[j]:.2f}" for j in range(6, 13)))
    # mean K and high quantiles vs log v
    print("mean / 99.9% / 99.99% quantile of K per decade:")
    for lo, hi, lab in decades:
        s = done & (v >= lo) & (v < hi)
        if s.sum() > 10000:
            ks = K[s]
            print(f"  {lab}: mean {ks.mean():.3f}  q99.9 {np.percentile(ks, 99.9):.0f}  q99.99 {np.percentile(ks, 99.99):.0f}"
                  f"  q99.999 {np.percentile(ks, 99.999):.0f}")


if __name__ == "__main__":
    main()
