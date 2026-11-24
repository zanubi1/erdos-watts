# Overshoot and prime-gap run: N = 10,000,000 terms (2026-11-24)

Commands:

    python experiments/src/overshoot.py --terms 10000000 --out experiments/results/overshoot_1e7
    python experiments/src/overshoot_extra.py --dir experiments/results/overshoot_1e7

The generator reproduces the first 40 terms of A055265. Full numbers are in `stats.txt` and `extra.txt`, and a step table around n ≈ 8,526,046 is in `zoom.md`. Plots: `running_maxima.png`, `block_gap_vs_disp.png`. The `.npy` files are gitignored; rerun the commands above to regenerate them.

## Notation

- u(n): the smallest unused value after n steps. u_par(n): the same, restricted to the parity of a(n+1).
- Dup(n) = a(n) - n: upper displacement, the quantity C005 needs.
- Dlo(n) = n - a(n): lower displacement.
- O(n): overshoot, the number of used values > u(n). O_e and O_o are the per-parity versions.
- W(n) = max a(1..n) - u(n): frontier width.

## Key numbers

Each cell is the running max, with max/(ln n)^2 in parentheses.

| quantity | 10^3 | 10^4 | 10^5 | 10^6 | 10^7 | global max at |
|---|---|---|---|---|---|---|
| **Dup** | 28 (0.59) | 74 (0.87) | 94 (0.71) | 156 (0.82) | **188 (0.72)** | n=8,525,842, a(n)=8,526,030 |
| Dlo | 38 | 54 | 104 | 150 | 200 (0.77) | n=8,526,046, a(n)=8,525,846 |
| O = n+1-u(n) | 38 | 54 | 104 | 150 | 200 | n=8,526,045 |
| O_e / O_o | 11/19 | 27/25 | 44/52 | 70/75 | 100/89 | - |
| W | 48 | 106 | 134 | 192 | 250 (0.96) | n=6,677,486 |

- **Growth fit:** fitting record values to c(ln n)^b gives b ≈ 2.3-2.4 for every quantity. Dup has only 18 records, so b is poorly determined.
- **Typical values over [10^6, 10^7]:**
  - Dup: median 0, p99 60.
  - O: median 28, p99 85.
  - W: median 56, p99 136.
  - Rejected candidates per step: mean 6.2, max 94.
  - Blocked primes per step (prime sum, but the partner is already used): mean 0.79, max 15.
- **Ratio:** a(n)/n <= 1.0316 for all n >= 1000.

## Correction to run_1e7/summary.md

The figure "max |a(n)-n| = 200 at n = 8,526,046" there is a **lower** displacement: the value 8,525,846 arrived 200 steps late. C005 needs only the **upper** bound. The measured max of a(n) - n is **188**, at n = 8,525,842, and it comes from the same event.

## Exact identities (checked for every n <= 10^7)

- **Overshoot formula:** O(n) = n + 1 - u(n).
- **Lower displacement vs overshoot:** Dlo(n) <= O(n-1), with equality iff a(n) = u(n-1). Hence max Dlo = max O = 200.
  - **Caution:** O(n) = o(n) already forces u(n) → ∞, which is the permutation property itself. "Bound the overshoot" is therefore not a weaker goal than the whole problem.
- **Frontier bound:** u_par(n) <= n + 1.
- **Step formula:** let t_n = a(n) + u_par(n), let P_k be the first prime >= t_n, and let b(n) be the number of blocked primes, with b(n) <= O_par(n). Then a(n+1) = u_par(n) + (P_{k+b} - t_n).
  - **Consequence:** a(n+1) - (n+1) <= 1 + the length needed, starting at t_n, to see O_par(n)+1 primes.
  - On this data that bound reaches at most 1542, against an actual max of 188.
- **Upper vs lower displacement:** Dup(n+1) = (s_n - 2n - 1) + Dlo(n), where s_n = a(n) + a(n+1). Over [10^6, 10^7], s_n - 2n has p1 = -97, p99 = 95 and max 273.

## Worst spots vs prime gaps

### Record events

The maximal prime gaps below 2·10^7 include 112@370,261, 114@492,113, 118@1,349,533, 132@1,357,201, 148@2,010,733, 154@4,652,353 and 180@17,051,707.

There are 9 Dup records after n = 10^5. Six of them sit exactly at a maximal prime gap at 2n:

| Dup record | maximal gap at 2n |
|---|---|
| 112 | 112 |
| 120 | 114 |
| 148 | 118 |
| 156 | 132 |
| 166 | 154 |
| 188 | 180 |

The other three records (116, 128, 184) sit at clusters of large gaps. For example, near 10,937,930 there are consecutive gaps of 102 and 96, then 88.

### Top 20 events vs a control sample

For each event, take the largest prime gap within 2n ± 400. Compare with 2,000 random n in [10^6, 10^7].

| sample | median largest gap | other |
|---|---|---|
| control (2,000 random n) | 60 | p99 112, max 156 |
| top 20 Dup events | 132 | range 100-180; mean percentile vs control 0.993 |
| top 20 Dlo events | 138 | |
| top 20 O events | 141 | |

Gaps near n itself, rather than near 2n, look typical at the worst spots.

### Blocks of 10^4 indices

- Spearman correlation between the block max and the block's max gap: 0.60 for Dup, 0.62 for Dlo and O.
- Linear fit: block max Dup ≈ 0.68·gap + 47.

## Step by step at n ≈ 8,526,046

The primes involved are p = 17,051,707, q = 17,051,887 (gap 180, the record gap below 2·10^7) and q' = q + 12.

1. **Entry (n ≈ 8,525,841).**
   - The first sums tried are about 2n - 21, inside the gap.
   - All 94 unused candidates up to q - a(n) give composite sums.
   - Four primes below p are blocked because their partners are already used (O_par = 19).
   - So a(8,525,842) = q - 8,525,857 = 8,526,030. This is the Dup = 188 event.
2. **Reflection lock (about 210 steps).**
   - Sums alternate between q (91 times) and q' (80 times).
   - One branch follows a(n+1) = q - a(n); the other follows a(n+2) = a(n) + 12.
   - Together these give two step-12 progressions walking towards each other.
3. **Late values.**
   - Values m near p/2 are skipped while their sums with current terms fall in the gap. Each waits until its partner q - m is the current term.
   - Example: m = 8,525,846 is picked after a(8,526,045) = 8,526,041, giving Dlo = 200 ≈ q - 2m.
4. **Exit.** Once 2n passes q, sums return to primes near 2n.

The same lock appears at every big gap:

- The 12 most-reused sum primes (73-91 uses each) all sit directly above gaps of 94-180.
- A prime's multiplicity as a sum correlates with the gap below it at r = 0.71.
- Mean multiplicity is 8.3 overall, 52 when the gap below is >= 100, and 77 when it is >= 150.

## Other patterns

- **Overtaken values:** 89% of values are overtaken (the running max passes them) before they are used.
- **Wait from overtaken to used:** mean 33, p99 103, max 309 (m = 5,469,106, at a gap cluster).
  - By range of m, the max wait is 131 (m < 10^5), 214 (m < 10^6) and 309 (m < 10^7).
- **Frontier stalls:** u(n) stays constant for at most 141 consecutive steps.
- **Parities:** the two parities behave alike; O_e and O_o both have mean 13.5.

## Conclusions

1. **Measured.** The quantity C005 needs, max(a(n) - n), is 188 for n <= 10^7, about 0.72(ln n)^2. That is far below n/log n ≈ 6·10^5.
2. **Measured.** The overshoot and the lower displacement are the same quantity (max O = max Dlo exactly). An o(n) bound on O alone already gives the permutation property.
3. **Measured.** The worst spots coincide with large prime gaps, or clusters of gaps, at 2n and not at n. Top events sit at the 99th percentile against the control sample.
4. **Observed mechanism, not proven.** Inside a gap (p, q) near 2n, the greedy is forced to sum to q and locks into the reflection x ↦ q - x for about the length of the gap.
   - Upper excursions are about q - 2n.
   - A left-behind value m waits until its partner q - m arrives, a delay of about q - 2m.
5. **Elementary, needs writing up as a lemma.** a(n+1) <= u_par(n) + d(a(n) + u_par(n), O_par(n) + 1), where d(t, K) is the length of the shortest interval starting at t that contains K primes.
   - Combined with C005 this is circular, because it needs O to be small.
6. **Suggested route (conjecture).** Bound how long a value can be left behind, using the reflection lock. While sums are locked on q, the partners q - m are taken in order, which might bound the wait by about one gap length.
7. **No counterexample.** Every value below 9,999,963 appears, and every delay is under 310 steps.
