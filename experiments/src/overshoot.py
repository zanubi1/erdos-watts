"""Overshoot / frontier / displacement statistics for the Watts greedy sequence (A055265).

a(1) = 1, a(n+1) = min { x >= 1 unused : a(n) + x is prime }.

Quantities (all "after n steps", i.e. after a(1..n) have been placed):
    u(n)      smallest unused positive integer; u_e(n), u_o(n) per parity
    O(n)      overshoot = #{used values > u(n)} = n + 1 - u(n)   (all of 1..u(n)-1 are used)
    O_e, O_o  per-parity overshoot: #{used even > u_e(n)}, #{used odd > u_o(n)}
    W(n)      frontier width = max(a(1..n)) - u(n)
    Dup(n)    upper displacement a(n) - n          (the one C005 needs bounded above)
    Dlo(n)    lower displacement n - a(n)          (a value arriving late)
    skip(n)   number of UNUSED candidates x of the right parity with u_par <= x < a(n+1)
              that the greedy step rejected (each one has a(n) + x composite)

Usage:
    python experiments/src/overshoot.py --terms 10000000 --out experiments/results/overshoot_1e7

Writes sequence.npy / skips.npy / blocked.npy (gitignored) into --out, plus stats.txt and PNG plots.
With --reuse, an existing sequence.npy / skips.npy in --out is loaded instead of regenerating.
"""

import argparse
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from greedy import sieve  # noqa: E402

A055265_START = [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15, 14, 17, 12, 11, 18, 19, 22,
                 21, 20, 23, 24, 29, 30, 31, 28, 25, 34, 27, 26, 33, 38, 35, 32, 39, 40, 43, 36]


# ----------------------------------------------------------------------------- generation

def generate(n_terms: int):
    """Same algorithm as greedy.generate, plus a per-step count of rejected unused candidates."""
    limit = max(1000, 8 * n_terms)
    is_p = sieve(limit)
    used = np.zeros(limit + 1, dtype=bool)
    lowest = [2, 3]  # smallest unused even / odd after a(1) = 1
    seq = np.empty(n_terms, dtype=np.int64)
    skips = np.zeros(n_terms, dtype=np.int32)  # skips[i] = rejected unused candidates when choosing seq[i]
    blocked = np.zeros(n_terms, dtype=np.int32)  # blocked[i] = used x < seq[i] (right parity, >= u_par) with seq[i-1]+x prime
    a = 1
    seq[0] = 1
    used[1] = True
    for i in range(1, n_terms):
        par = 1 - (a & 1)
        x = lowest[par]
        s = 0
        bl = 0
        while True:
            if x + a > limit:
                new_limit = 2 * limit
                is_p = sieve(new_limit)
                used = np.concatenate([used, np.zeros(new_limit - limit, dtype=bool)])
                limit = new_limit
            if not used[x]:
                if is_p[a + x]:
                    break
                s += 1
            elif is_p[a + x]:
                bl += 1
            x += 2
        seq[i] = x
        skips[i] = s
        blocked[i] = bl
        used[x] = True
        if x == lowest[par]:
            y = x
            while y <= limit and used[y]:
                y += 2
            lowest[par] = y
        a = x
    return seq, skips, blocked


# ----------------------------------------------------------------------------- derived series

def derived(seq: np.ndarray):
    N = len(seq)
    n = np.arange(1, N + 1)
    V = int(seq.max()) + 4
    fi = np.full(V + 1, N + 1, dtype=np.int64)  # first index; N+1 = not seen within N steps
    fi[seq] = n
    fi[0] = 0
    # u(n) > m  <=>  max(fi[1..m]) <= n
    pm = np.maximum.accumulate(fi[1:])
    u = np.searchsorted(pm, n, side="right") + 1
    pe = np.maximum.accumulate(fi[2::2])
    u_e = 2 * (np.searchsorted(pe, n, side="right") + 1)
    po = np.maximum.accumulate(fi[1::2])
    u_o = 2 * (np.searchsorted(po, n, side="right") + 1) - 1
    E = np.cumsum(seq % 2 == 0)
    Od = n - E
    O = n + 1 - u
    O_e = E - (u_e // 2 - 1)
    O_o = Od - ((u_o + 1) // 2 - 1)
    cmax = np.maximum.accumulate(seq)
    W = cmax - u
    Dup = seq - n
    Dlo = n - seq
    return dict(n=n, fi=fi, u=u, u_e=u_e, u_o=u_o, O=O, O_e=O_e, O_o=O_o, cmax=cmax, W=W, Dup=Dup, Dlo=Dlo)


def records(arr: np.ndarray):
    """Indices (0-based) where arr attains a new strict maximum."""
    cm = np.maximum.accumulate(arr)
    idx = np.flatnonzero(np.r_[True, cm[1:] > cm[:-1]])
    return idx


def top_events(arr: np.ndarray, k: int, sep: int):
    """Top-k indices of arr, requiring pairwise separation > sep (one representative per cluster)."""
    order = np.argsort(arr, kind="stable")[::-1]
    chosen = []
    for i in order:
        if all(abs(int(i) - c) > sep for c in chosen):
            chosen.append(int(i))
            if len(chosen) == k:
                break
    return chosen


# ----------------------------------------------------------------------------- primes

class Gaps:
    def __init__(self, limit):
        self.is_p = sieve(limit)
        self.p = np.flatnonzero(self.is_p)
        self.g = np.diff(self.p)
        # record (maximal) gaps
        r = records(self.g)
        self.record_gaps = [(int(self.p[i]), int(self.g[i])) for i in r]

    def max_gap_in(self, L, R):
        """Largest gap p_{i+1} - p_i among consecutive primes with the gap meeting [L, R]."""
        i0 = max(np.searchsorted(self.p, L, side="right") - 1, 0)
        i1 = np.searchsorted(self.p, R, side="left")
        j = i0 + int(np.argmax(self.g[i0:i1 + 1]))
        return int(self.g[j]), int(self.p[j])

    def gap_containing(self, x):
        i = np.searchsorted(self.p, x, side="right") - 1
        return int(self.p[i]), int(self.p[i + 1])


def smallest_factor(m: int) -> int:
    if m % 2 == 0:
        return 2
    f = 3
    while f * f <= m:
        if m % f == 0:
            return f
        f += 2
    return m


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--terms", type=int, default=100_000)
    ap.add_argument("--out", default="experiments/results/overshoot")
    ap.add_argument("--reuse", action="store_true", help="load sequence.npy/skips.npy from --out if present")
    ap.add_argument("--window", type=int, default=400, help="half-width H: look at primes in [2n-H, 2n+H]")
    ap.add_argument("--zoom", type=int, default=8_526_046, help="index to dissect step by step")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    out = []

    def P(*s):
        line = " ".join(str(x) for x in s)
        print(line)
        out.append(line)

    sp, kp = os.path.join(args.out, "sequence.npy"), os.path.join(args.out, "skips.npy")
    bp = os.path.join(args.out, "blocked.npy")
    if args.reuse and all(os.path.exists(f) for f in (sp, kp, bp)):
        seq, skips, blocked = np.load(sp), np.load(kp), np.load(bp)
        seq, skips, blocked = seq[: args.terms], skips[: args.terms], blocked[: args.terms]
    else:
        t0 = time.time()
        seq, skips, blocked = generate(args.terms)
        P(f"generation: {time.time() - t0:.1f}s")
        np.save(sp, seq)
        np.save(kp, skips)
        np.save(bp, blocked)
    N = len(seq)
    k = min(N, len(A055265_START))
    assert list(seq[:k]) == A055265_START[:k], "mismatch with OEIS A055265"
    P(f"N = {N:,}; first {k} terms match OEIS A055265")

    D = derived(seq)
    n = D["n"]
    names = ["Dup", "Dlo", "O", "O_e", "O_o", "W"]

    # --- maxima, checkpoints, ratio to (log n)^2
    P("\n## Running maxima at checkpoints (value / (ln n)^2)")
    cps = [10 ** j for j in range(3, 9) if 10 ** j <= N]
    P("| quantity | " + " | ".join(f"n=10^{int(math.log10(c))}" for c in cps) + " |")
    for nm in names:
        cm = np.maximum.accumulate(D[nm])
        cells = [f"{int(cm[c - 1])} ({cm[c - 1] / math.log(c) ** 2:.2f})" for c in cps]
        P(f"| max {nm} | " + " | ".join(cells) + " |")
    for nm in ["Dup", "Dlo", "O", "W"]:
        i = int(np.argmax(D[nm]))
        P(f"global max {nm} = {int(D[nm][i])} at n = {i + 1:,} (a(n) = {int(seq[i]):,})")

    # Dup also restricted to n >= 100 (small-n ratio artifacts)
    P(f"max a(n)/n for n>=1000: {np.max(seq[999:] / n[999:]):.6f}; max a(n) - n overall: {int(D['Dup'].max())}")

    # fits: log(record value) vs log log n
    P("\n## Fit of record values: value ~ c (ln n)^b  (least squares on records with n >= 1000)")
    for nm in ["Dup", "Dlo", "O", "W"]:
        r = records(D[nm])
        r = r[r >= 999]
        x = np.log(np.log(n[r]))
        y = np.log(np.maximum(D[nm][r], 1))
        b, c = np.polyfit(x, y, 1)
        P(f"{nm}: {len(r)} records after n=1000, b = {b:.2f}, c = {math.exp(c):.3f}; "
          f"last record {int(D[nm][r[-1]])} at n = {int(n[r[-1]]):,}")

    P("\n## Record list for Dup (upper displacement a(n) - n)")
    r = records(D["Dup"])
    P(", ".join(f"{int(D['Dup'][i])}@{i + 1}" for i in r))
    P("\n## Record list for Dlo (lower displacement n - a(n))")
    r = records(D["Dlo"])
    P(", ".join(f"{int(D['Dlo'][i])}@{i + 1}" for i in r))
    P("\n## Record list for O (overshoot)")
    r = records(D["O"])
    P(", ".join(f"{int(D['O'][i])}@{i + 1}" for i in r))
    P("\n## Record list for W (frontier width)")
    r = records(D["W"])
    P(", ".join(f"{int(D['W'][i])}@{i + 1}" for i in r))

    # --- distribution summaries
    P("\n## Distributions over n in [N/10, N]")
    lo = N // 10
    for nm in ["Dup", "Dlo", "O", "O_e", "O_o", "W"]:
        v = D[nm][lo:]
        qs = np.percentile(v, [50, 90, 99, 99.9, 100])
        P(f"{nm}: mean {v.mean():.1f}, median {qs[0]:.0f}, p90 {qs[1]:.0f}, p99 {qs[2]:.0f}, p99.9 {qs[3]:.0f}, max {qs[4]:.0f}")
    v = skips[lo:]
    P(f"skips (rejected unused candidates per step): mean {v.mean():.2f}, p99 {np.percentile(v, 99):.0f}, max {v.max()}"
      f" (global max {skips.max()} at n+1 = {int(np.argmax(skips)) + 1:,})")
    P(f"fraction of steps with a(n+1) = u_par (no rejection): {(skips[1:] == 0).mean():.4f}")
    # blocked[i]: primes P in [a(i) + u_par, a(i) + a(i+1)) whose partner P - a(i) was already used
    bl = blocked[1:]
    Op = np.where(seq[1:] % 2 == 0, D["O_e"][:-1], D["O_o"][:-1])
    P(f"blocked (primes skipped because partner used): mean {bl.mean():.2f}, p99 {np.percentile(bl, 99):.0f}, "
      f"max {bl.max()} (at n+1 = {int(np.argmax(bl)) + 2:,}); fraction of steps with blocked>0: {(bl > 0).mean():.4f}")
    P(f"check blocked(n) <= O_par(n) everywhere: {bool(np.all(bl <= Op))}; max blocked/O_par (O_par>0): "
      f"{np.max(bl[Op > 0] / Op[Op > 0]):.3f}; mean blocked / mean O_par = {bl.mean() / Op.mean():.3f}")
    # relation: a(n) - n <= W(n) - O(n) + 1 identically
    P("identity check: Dup(n) <= W(n) - O(n) + 1 :", bool(np.all(D["Dup"] <= D["W"] - D["O"] + 1)))
    # a(n) >= u(n-1) always, and O(n-1) = n - u(n-1), so Dlo(n) <= O(n-1), with equality iff a(n) = u(n-1)
    P("check Dlo(n) <= O(n-1) for n >= 2:", bool(np.all(D["Dlo"][1:] <= D["O"][:-1])),
      "; max Dlo =", int(D["Dlo"].max()), "; max O =", int(D["O"].max()))

    # --- prime gaps
    G = Gaps(2 * int(seq.max()) + 10_000)
    P("\n## Maximal prime gaps below", f"{2 * int(seq.max()) + 10_000:,}", "(p, gap)")
    P(", ".join(f"{g}@{p}" for p, g in G.record_gaps if g >= 50))
    H = args.window

    def gap_row(i, label):
        nn = i + 1
        g, p = G.max_gap_in(2 * nn - H, 2 * nn + H)
        g1, p1 = G.max_gap_in(nn - H // 2, nn + H // 2)
        return (label, nn, int(seq[i]), g, p, g / math.log(2 * nn), g1, p1)

    events = []
    for nm, kk in [("Dup", 20), ("Dlo", 20), ("O", 10), ("W", 10)]:
        for i in top_events(D[nm], kk, 2000):
            events.append((nm, int(D[nm][i]), i))
    P(f"\n## Top events vs prime gaps (window [2n-{H}, 2n+{H}] and [n-{H // 2}, n+{H // 2}])")
    P("| kind | value | n | a(n) | max gap near 2n | at p | gap/ln(2n) | max gap near n | at p |")
    P("|---|---|---|---|---|---|---|---|---|")
    ev_gaps = {}
    for nm, val, i in events:
        lab, nn, an, g, p, rel, g1, p1 = gap_row(i, nm)
        ev_gaps.setdefault(nm, []).append(g)
        P(f"| {nm} | {val} | {nn:,} | {an:,} | {g} | {p:,} | {rel:.1f} | {g1} | {p1:,} |")

    rng = np.random.default_rng(args.seed)
    ctrl_idx = rng.integers(N // 10, N - 1, size=2000)
    ctrl = np.array([G.max_gap_in(2 * (i + 1) - H, 2 * (i + 1) + H)[0] for i in ctrl_idx])
    P(f"\n## Control: 2000 random n in [N/10, N]: max gap in [2n-{H},2n+{H}]")
    P(f"median {np.median(ctrl):.0f}, p90 {np.percentile(ctrl, 90):.0f}, p99 {np.percentile(ctrl, 99):.0f}, max {ctrl.max()}")
    for nm, gl in ev_gaps.items():
        gl = np.array(gl)
        pct = [float((ctrl < g).mean() + 0.5 * (ctrl == g).mean()) for g in gl]
        P(f"{nm} top events: median max-gap {np.median(gl):.0f}; mean control-percentile {np.mean(pct):.3f}; "
          f"min {min(gl)}, max {max(gl)}")

    # block correlation
    B = 10_000
    nb = N // B
    P(f"\n## Block correlation ({nb} blocks of {B} indices, n >= N/10)")
    rows = []
    for b in range(nb):
        s, e = b * B, (b + 1) * B
        g, _ = G.max_gap_in(2 * (s + 1), 2 * e)
        rows.append((g, D["Dup"][s:e].max(), D["Dlo"][s:e].max(), D["O"][s:e].max(), D["W"][s:e].max()))
    rows = np.array(rows[nb // 10:], dtype=float)

    def spearman(x, y):
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(y)).astype(float)
        return np.corrcoef(rx, ry)[0, 1]

    for j, nm in enumerate(["Dup", "Dlo", "O", "W"], start=1):
        P(f"Spearman(block max gap near 2n, block max {nm}) = {spearman(rows[:, 0], rows[:, j]):.3f}; "
          f"Pearson = {np.corrcoef(rows[:, 0], rows[:, j])[0, 1]:.3f}")
    for j, nm in enumerate(["Dup", "Dlo", "O", "W"], start=1):
        sl = np.polyfit(rows[:, 0], rows[:, j], 1)
        P(f"linear fit block max {nm} ~ {sl[0]:.3f} * gap + {sl[1]:.1f}")

    # --- pointwise mechanism: Dup at a step vs the prime gap the sum had to jump
    P("\n## Sums a(n)+a(n+1) vs prime gaps")
    s_ = seq[:-1] + seq[1:]
    P(f"(a(n)+a(n+1)) - 2n: min {int((s_ - 2 * n[:-1]).min())}, max {int((s_ - 2 * n[:-1]).max())}")

    # --- late values: waiting time from 'overtaken' to 'picked'
    P("\n## Late values: for m < u(N), overtaken(m) = first n with max(a(1..n)) > m; wait(m) = fi(m) - overtaken(m)")
    fi = D["fi"]
    M = int(D["u"][-1]) - 1
    m = np.arange(1, M + 1)
    over = np.searchsorted(D["cmax"], m, side="right") + 1  # first n with cmax(n) > m
    wait = np.where(fi[m] > over, fi[m] - over, 0)
    late = wait > 0
    P(f"values overtaken before being used: {late.sum():,} of {M:,} ({late.mean():.3f})")
    w = wait[late]
    P(f"wait: mean {w.mean():.1f}, median {np.median(w):.0f}, p99 {np.percentile(w, 99):.0f}, max {w.max()} "
      f"(m = {int(m[np.argmax(wait)]):,})")
    for lo_, hi_ in [(1, 10 ** 5), (10 ** 5, 10 ** 6), (10 ** 6, M)]:
        sel = (m >= lo_) & (m < hi_)
        if not sel.any():
            continue
        P(f"  m in [{lo_:,},{hi_:,}): max wait {wait[sel].max()}, max fi(m)-m {int((fi[m[sel]] - m[sel]).max())}")
    P("by parity of m: max wait even "
      f"{wait[m % 2 == 0].max()}, odd {wait[m % 2 == 1].max()}")

    # --- excursion structure: maximal runs where O(n) > 0 is trivial; use runs with u stuck
    P("\n## Excursions: maximal intervals where u(n) is constant (frontier stuck)")
    u = D["u"]
    ch = np.flatnonzero(np.diff(u) != 0)
    lens = np.diff(np.r_[-1, ch, N - 1])
    P(f"number of intervals {len(lens):,}; longest {lens.max()} steps; p99 {np.percentile(lens, 99):.0f}")
    j = int(np.argmax(lens))
    st = int(np.r_[-1, ch][j]) + 2
    P(f"longest stuck interval starts at n = {st:,}, u = {int(u[st - 1]):,}")

    # --- Dup decomposition: a(n+1) - (n+1) = (s_n - 2n - 1) + (n - a(n)),  s_n = a(n) + a(n+1)
    P("\n## Decomposition of top upper-displacement events: Dup(n+1) = (s_n - 2n - 1) + Dlo(n)")
    P("search for a(n+1) starts at sum a(n) + u_par(n) =: t_n and ends at the prime s_n; "
      "blocked(n) = primes in [t_n, s_n) whose partner was used")
    P("| n+1 | Dup(n+1) | s_n - 2n - 1 | Dlo(n) | t_n - 2n | s_n | max prime gap in [t_n, s_n] (start) | blocked(n) | O_par(n) | O(n) |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for i in top_events(D["Dup"], 20, 2000):
        nn = i  # a(n+1) = seq[i], n = i
        sn = int(seq[i - 1] + seq[i])
        up = int(D["u_e"][i - 1]) if seq[i] % 2 == 0 else int(D["u_o"][i - 1])
        tn = int(seq[i - 1]) + up
        g, gp = G.max_gap_in(tn, sn - 1)
        P(f"| {i + 1:,} | {int(D['Dup'][i])} | {sn - 2 * nn - 1} | {int(D['Dlo'][i - 1])} | {tn - 2 * nn} | {sn:,} | "
          f"{g} ({gp:,}) | {int(blocked[i])} | {int(Op[i - 1])} | {int(D['O'][i - 1])} |")
    sx = seq[:-1] + seq[1:] - 2 * n[:-1]
    P(f"s_n - 2n over n in [N/10, N]: p1 {np.percentile(sx[lo:], 1):.0f}, median {np.median(sx[lo:]):.0f}, "
      f"p99 {np.percentile(sx[lo:], 99):.0f}, max {sx.max()}")

    # --- zoom: write a step table to zoom.md
    z = args.zoom
    if z <= N:
        P(f"\n## Zoom around n = {z:,} (full table in zoom.md)")
        g0, g1_ = G.gap_containing(2 * z)
        P(f"prime gap containing 2n = {2 * z:,}: ({g0:,}, {g1_:,}), length {g1_ - g0}")
        zl = [f"# Step table around n = {z:,}", "",
              "s = a(n)+a(n+1); rej = unused candidates x in [u_par(n), a(n+1)) rejected (composite sum); "
              "blk = used x in that range with a(n)+x prime (blocked); O, W after n steps.", "",
              "| n | a(n) | a(n)-n | a(n+1) | s | s-2n | u_par(n) | rej | blk | O(n) | W(n) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for t in range(z - 270, z + 12):
            i = t - 1
            a_t, nxt = int(seq[i]), int(seq[i + 1])
            up = int(D["u_e"][i]) if nxt % 2 == 0 else int(D["u_o"][i])
            zl.append(f"| {t:,} | {a_t:,} | {a_t - t} | {nxt:,} | {a_t + nxt:,} | {a_t + nxt - 2 * t} | {up:,} | "
                      f"{int(skips[i + 1])} | {int(blocked[i + 1])} | {int(D['O'][i])} | {int(D['W'][i])} |")
        with open(os.path.join(args.out, "zoom.md"), "w") as f:
            f.write("\n".join(zl) + "\n")

    with open(os.path.join(args.out, "stats.txt"), "w") as f:
        f.write("\n".join(out) + "\n")

    # --- plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    L2 = np.log(n) ** 2
    for nm in ["Dup", "Dlo", "O", "W"]:
        cm = np.maximum.accumulate(D[nm])
        ax.loglog(n[99:], cm[99:], label=f"running max {nm}")
    ax.loglog(n[99:], L2[99:], "k--", label="(ln n)^2")
    ax.set_xlabel("n")
    ax.legend(loc="upper left")
    ax.set_title("Running maxima: upper/lower displacement, overshoot, frontier width")
    fig.savefig(os.path.join(args.out, "running_maxima.png"), dpi=110, bbox_inches="tight")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(rows[:, 0], rows[:, 1], s=4, label="block max Dup")
    ax.scatter(rows[:, 0], rows[:, 2], s=4, label="block max Dlo")
    ax.set_xlabel(f"max prime gap in [2n_start, 2n_end] (blocks of {B})")
    ax.legend(loc="upper left")
    fig.savefig(os.path.join(args.out, "block_gap_vs_disp.png"), dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
