"""Generate the Watts greedy sequence (OEIS A055265) and basic statistics.

a(1) = 1, a(n+1) = min { x >= 1 unused : a(n) + x is prime }.

Usage:
    python experiments/src/greedy.py --terms 1000000 --out experiments/results/run_1e6

Outputs (in --out directory):
    sequence.npy      a(1..N) as int64
    first_index.npy   first_index[m] = n with a(n) = m (0 if m not seen yet), for m <= max(a)
    summary.md        human-readable stats
"""

import argparse
import os
import time

import numpy as np


def sieve(limit: int) -> np.ndarray:
    is_p = np.ones(limit + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = False
    return is_p


def generate(n_terms: int):
    limit = max(1000, 8 * n_terms)
    is_p = sieve(limit)
    used = np.zeros(limit + 1, dtype=bool)
    # smallest unused value for each parity (index 0 = even, 1 = odd)
    lowest = [2, 1]

    seq = np.empty(n_terms, dtype=np.int64)
    a = 1
    seq[0] = 1
    used[1] = True
    lowest[1] = 3

    for i in range(1, n_terms):
        # next term has opposite parity to a (sum must be an odd prime; 1+1 is the only even-prime case and 1 is used)
        par = 1 - (a & 1)
        x = lowest[par]
        while True:
            if x + a > limit:
                # grow structures
                new_limit = 2 * limit
                is_p = sieve(new_limit)
                used = np.concatenate([used, np.zeros(new_limit - limit, dtype=bool)])
                limit = new_limit
            if not used[x] and is_p[a + x]:
                break
            x += 2
        seq[i] = x
        used[x] = True
        if x == lowest[par]:
            y = x
            while y <= limit and used[y]:
                y += 2
            lowest[par] = y
        a = x
    return seq


def summarize(seq: np.ndarray, elapsed: float) -> str:
    n = len(seq)
    mx = int(seq.max())
    first_index = np.zeros(mx + 1, dtype=np.int64)
    first_index[seq] = np.arange(1, n + 1)

    # smallest missing value after N terms
    seen = first_index[1:] > 0
    missing = np.flatnonzero(~seen) + 1
    smallest_missing = int(missing[0]) if len(missing) else mx + 1

    # values m <= smallest_missing - 1 are all present; how late did they show up relative to m?
    full = np.arange(1, smallest_missing)
    lag = first_index[full] - full  # index - value
    worst = np.argsort(lag)[-10:][::-1]

    ratio = seq / np.arange(1, n + 1)
    fixed = int(np.sum(seq == np.arange(1, n + 1)))

    lines = [
        f"# Greedy sequence run: N = {n:,} terms",
        "",
        f"- generation time: {elapsed:.1f}s",
        f"- max value a(n): {mx:,}",
        f"- smallest value not yet seen: {smallest_missing:,}",
        f"- number of values <= max not yet seen: {len(missing):,}",
        f"- fixed points a(n) = n: {fixed:,}",
        f"- max |a(n) - n|: {int(np.abs(seq - np.arange(1, n + 1)).max()):,} "
        f"(at n = {int(np.abs(seq - np.arange(1, n + 1)).argmax()) + 1:,})",
        f"- a(n)/n: min {ratio.min():.4f}, max {ratio.max():.4f}, mean over last 10% {ratio[-n // 10:].mean():.4f}",
        "",
        "## Latest arrivals among 1..(smallest missing - 1)",
        "",
        "| m | first index n | n - m |",
        "|---|---|---|",
    ]
    for j in worst:
        m = int(full[j])
        lines.append(f"| {m:,} | {int(first_index[m]):,} | {int(lag[j]):,} |")
    lines += [
        "",
        "## First 40 terms",
        "",
        ", ".join(str(int(v)) for v in seq[:40]),
        "",
    ]
    return "\n".join(lines), first_index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--terms", type=int, default=100_000)
    ap.add_argument("--out", default="experiments/results/run")
    args = ap.parse_args()

    t0 = time.time()
    seq = generate(args.terms)
    elapsed = time.time() - t0
    text, first_index = summarize(seq, elapsed)

    os.makedirs(args.out, exist_ok=True)
    np.save(os.path.join(args.out, "sequence.npy"), seq)
    np.save(os.path.join(args.out, "first_index.npy"), first_index)
    with open(os.path.join(args.out, "summary.md"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
