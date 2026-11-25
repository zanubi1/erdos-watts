"""C008 numerical check: hole-density criterion.

For every X <= N:
  (i)   H(X) = #{v <= X : v not in {a(1..X)}}  equals  #{k <= X : a(k) > X}
        (two independent incremental computations, plus brute-force spot checks).
  (iii) H(X) <= D + S(X)/D, S(X) = sum_{k<=X} max(a(k)-k, 0),
        for D in {1,2,5,10,20,50,100, ceil(sqrt S(X))+1}; checked exactly in integers
        as D*H <= D^2 + S.
Also prints growth tables of H and S at decades.

Usage: python experiments/src/c008_check.py [--seq PATH] [--terms N]
"""
import argparse
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_SEQ = "/home/user/erdos-watts/experiments/results/overshoot_1e7/sequence.npy"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seq", default=DEFAULT_SEQ)
    ap.add_argument("--terms", type=int, default=10_000_000)
    args = ap.parse_args()
    N = args.terms
    if os.path.exists(args.seq) and len(np.load(args.seq, mmap_mode="r")) >= N:
        a = np.load(args.seq)[:N].astype(np.int64)
    else:
        from greedy import generate
        a = generate(N)
    ref = [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15, 14, 17, 12, 11, 18, 19, 22]
    assert list(a[:20]) == ref, "sequence does not match A055265"
    assert len(np.unique(a)) == N
    k = np.arange(1, N + 1, dtype=np.int64)

    # pos[v] = index k with a(k)=v, or N+1 (= "later than N") if unseen
    M = int(a.max())
    pos = np.full(M + 2, N + 1, dtype=np.int64)
    pos[a] = k
    posv = pos[1 : N + 1]  # for v = 1..N

    # Method A: H(X) = #{k<=X : a(k)>X};  H(X)-H(X-1) = [a(X)>X] - [pos(X)<X]
    HA = np.cumsum((a > k).astype(np.int64) - (posv < k).astype(np.int64))
    # Method B: holes(X) = #{v<=X : pos(v)>X}; change = [pos(X)>X] - [a(X)<X]
    HB = np.cumsum((posv > k).astype(np.int64) - (a < k).astype(np.int64))
    ok_i = bool(np.array_equal(HA, HB))
    # brute-force spot checks
    rng = np.random.default_rng(0)
    spots = sorted(set([1, 2, 10, 100, 1000, N]) | set(rng.integers(1, N + 1, 30).tolist()))
    for X in spots:
        h1 = int(np.sum(a[:X] > X))
        used = np.zeros(X + 1, bool)
        v = a[:X]
        used[v[v <= X]] = True
        h2 = X - int(used[1:].sum())
        assert h1 == h2 == HA[X - 1], (X, h1, h2, HA[X - 1])
    H = HA
    print(f"(i) identity holds for all X <= {N}: {ok_i}; brute-force spot checks at {len(spots)} X: OK")

    S = np.cumsum(np.maximum(a - k, 0))
    assert S[-1] < 2**62
    Ds = [1, 2, 5, 10, 20, 50, 100]
    print("(iii) D : violations, min slack (D + S/D - H)")
    for D in Ds:
        viol = int(np.sum(D * H > D * D + S))
        slack = (D + S / D - H).min()
        print(f"   D={D}: {viol}, min slack {slack:.3f}")
    isq = np.sqrt(S.astype(np.float64)).astype(np.int64)
    isq -= (isq * isq > S)
    isq += ((isq + 1) * (isq + 1) <= S)
    # exact ceil(sqrt S) + 1 via corrected integer sqrt
    Dexact = isq + (isq * isq < S) + 1
    viol = int(np.sum(Dexact * H > Dexact * Dexact + S))
    bound = Dexact + S / Dexact
    print(f"   D=ceil(sqrt S)+1: {viol}, min slack {(bound - H).min():.3f}, max H/bound {(H / bound).max():.4f}")

    # growth
    print(f"\nmax H over X<={N}: {H.max()} at X={int(H.argmax()) + 1}; mean H {H.mean():.3f}")
    runmax = np.maximum.accumulate(H)
    idx = np.flatnonzero(np.diff(runmax, prepend=-1) > 0)
    print("records (X, H):", ", ".join(f"({i + 1},{H[i]})" for i in idx))
    print("\n| X | H(X) | max H(<=X) | mean H(<=X) | max_{X'<=X} H log X'/X' (X'>=X/10) | H(X) log X/X | S(X) | S/(X^2/log^2 X) | S/X^1.5 | 2sqrt(S)+3 |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    Xs = np.arange(1, N + 1, dtype=np.float64)
    ratio = H * np.log(np.maximum(Xs, 2)) / Xs
    for e in range(3, int(math.log10(N)) + 1):
        X = 10**e
        h = int(H[X - 1]); s = int(S[X - 1])
        lo = X // 10
        print(f"| 10^{e} | {h} | {H[:X].max()} | {H[:X].mean():.2f} | {ratio[lo - 1:X].max():.2e} | "
              f"{h * math.log(X) / X:.2e} | {s:,} | {s / (X * X / math.log(X) ** 2):.3e} | {s / X**1.5:.3f} | {2 * math.sqrt(s) + 3:.0f} |")


if __name__ == "__main__":
    main()
