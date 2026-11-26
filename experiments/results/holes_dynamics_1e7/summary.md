# Hole dynamics to N = 10^7 (2026-11-25)

Command (about 10 min, 8 of them in the `bounds` section):

    python experiments/src/holes_dynamics.py --plots experiments/results/holes_dynamics_1e7

The script reuses `overshoot_1e7/sequence.npy` and asserts that the first 20 terms match A055265. The raw output of every section is in `stdout.txt`. Plots:
- `lifetimes.png`: lifetime histogram, and lifetime vs the local max prime gap.
- `holes_vs_gaps.png`: H vs the prime gap, with a zoom on H = 50.

## Notation

- A hole at time n is a value v <= n not in U_n = {a(1..n)}. H(n) is the number of holes, and H_p(n) the number of parity p.
- fi(v) is the index at which v first appears, and L(v) = fi(v) - v is the lifetime of v.
- s(v) = max{ fi(w) : w < v, w ≡ v mod 2 } is the time v becomes the frontier of its parity.
- T0 = max(s(v), v).

## Exact facts (all checked to 10^7, 0 violations)

- **E1 (parity of lifetimes).** a(k) ≡ k (mod 2), so fi(v) ≡ v and L(v) is always even.
  - Per parity, H_p(X) = #{ k <= X : k ≡ p, a(k) > X }.
- **E2 (frontier fill).** For all v >= 2 with s(v) < fi(v), fi(v) - 1 is the first k > s(v) with a(k) + v prime. Checked for 1,711,578 values of v.
- **E3 (pairs of frontiers).** If v and w are simultaneously the two parity frontiers and v + w is prime, they are filled at consecutive steps.
  - Checked for 541,586 pairs.
  - Both can stay frontier for up to 130 steps before this happens.
- **E4 (steals).** Let k ∈ [v, fi(v) - 2] with k ≡ v + 1. If a(k) + v is prime, then a(k+1) < v, i.e. a smaller hole of v's parity is filled instead ("stolen").
  - So stolen(v) <= #{ x < v : x ≡ v, x a hole at time v }. The bound is attained.
  - Of 39.4M such opportunities, 97.5% are lost because a(k) + v is composite, and only 2.5% to steals.
  - Steals per hole: median 0, max 6.
- **E5 (prime-count lemma, now candidate C009).** Checked for all 4.71M holes at n = fi(v) - 1, and for the smallest hole at every n.
  - The left side is at most 8; the right side reaches 52.

## Flow

| quantity | value |
|---|---|
| creation rate P(n+1 is a hole at time n+1) | 0.47126 |
| fill rate P(a(n+1) <= n) | 0.47126 |
| P(a(n+1) = n+1) | 0.041 |
| P(a(n+1) > n+1) | 0.487 |
| mean H | 8.82 (5.75 below 10^5; 7.48 in [10^5, 10^6); 8.99 in [10^6, 10^7)) |
| max H | 50, at n = 6,869,384 |
| P(fill at n+1, given fill at n) | 0.577 |
| P(fill at n+1, given no fill at n) | 0.377 |
| fill runs | median 2, p99 9, max 40 |

Drift conditional on H (n >= 10^5):

| H | E[ΔH] | P(fill) | P(create) |
|---|---|---|---|
| 0 | +0.696 | 0 | 0.696 |
| 2 | +0.242 | 0.314 | 0.556 |
| 4 | +0.088 | 0.415 | 0.503 |
| 6 | +0.011 | 0.463 | 0.474 |
| 7 | -0.010 | 0.480 | 0.470 |
| 10 | -0.043 | 0.496 | 0.453 |
| 15 | -0.062 | 0.513 | 0.451 |
| 20 | -0.071 | 0.510 | 0.439 |
| 30-39 | -0.080 | 0.496 | ≈0.42 |
| 40-50 | -0.064 | 0.442 | ≈0.37 |

- The drift is negative from H >= 7, but it saturates at about -0.07 per step.
- Per parity class, it is negative from H_π >= 4 and saturates at about -0.14.
- P(fill) caps at about 0.51.
- **So no drift or martingale argument will bound H on its own.**
- Excursions: 51 above H = 40, the longest lasting 75 steps; the longest above H = 30 lasts 110 steps.

## Lifetimes

There are 4.71M holes with v <= N - 5000.

- Mean L 18.7, median 14, p99 70, p99.9 98, max 200.
- Tail: P(L >= 40) = 1.0e-1, P(L >= 80) = 4.8e-3, P(L >= 160) = 6.2e-6.

| v range | max L | at v | max gap in [2v ± 300] | p99 L |
|---|---|---|---|---|
| 10^4-10^5 | 104 | 94,021 | 78 | 48 |
| 10^5-10^6 | 150 | 678,593 | 132 | 60 |
| 1-2·10^6 | 138 | 1,005,373 | 148 | 64 |
| 2-4·10^6 | 166 | 2,326,176 | 154 | 68 |
| 4-6·10^6 | 168 | 5,469,106 | 102 | 70 |
| 6-8·10^6 | 178 | 6,677,345 | 126 | 72 |
| 8-10·10^6 | 200 | 8,525,846 | 180 | 74 |

**There is no clean bound by a single gap.** With G the max gap in [2v ± 300], the best fits are L <= G + 80 and L <= 2.59·G. The worst case is v = 9,300,985: L = 146 with G = 66, caused by several medium gaps in a row.

**The clean relation is a prime count.** Let K(v) = π(2v + L - 1) - π(2v), the number of primes the sums sweep past while v waits.

| v range | max K | max H seen | P(K=0) | P(K>=5) | max L with K=0 |
|---|---|---|---|---|---|
| < 10^3 | 4 | 17 | 0.36 | 0 | 18 |
| 10^3-10^4 | 6 | 17 | 0.38 | 1.0e-3 | 38 |
| 10^4-10^5 | 7 | 29 | 0.38 | 8.7e-4 | 78 |
| 10^5-10^6 | 8 | 41 | 0.39 | 1.2e-3 | 122 |
| 10^6-3·10^6 | 7 | 47 | 0.39 | 1.4e-3 | 140 |
| 3·10^6-10^7 | 8 | 50 | 0.39 | 1.7e-3 | 158 |

**Max K is flat at about 8 across four decades, while max H tripled.**

For each prime q counted in K(v), its partner w = q - v was used at some time:

| when w was used | count | max per hole |
|---|---|---|
| before v ("ahead") | 561k | 6 |
| as a steal, in [v, fi - 2] | 279k | 5 |
| as the filler, at fi - 1 | 1.46M | 1 |
| not yet ("late": still a hole at fi - 1) | 1.96M | 7 |

## Frontier holes

- 1,692,087 holes are the frontier at some point while still a hole. Only 35.9% of fills are frontier picks.
- **Wait after becoming the frontier:** fi(v) - T0 has mean 11.7, p99 52, max 158.
- **Time from T0 to the first partner being used:** median 7, max 157.
- **Who fills the frontier hole:**
  - a hole partner, 47.3% of the time;
  - a partner in the gap above the frontier, 33.5%;
  - a fresh value, 19.2%.

## Pairs of coexisting opposite-parity holes

| sum | #pairs | max coexistence | p99 | P(\|Δfi\| = 1) |
|---|---|---|---|---|
| prime | 3.33M | 176 | 52 | 0.815 |
| composite | 17.5M | 178 | 52 | 0 (forced) |

- **L1 is false as a useful statement.** "Prime-sum hole pairs are both filled within T" needs T = 200, the max lifetime itself.
- **The hole set is not prime-sum-free.** Compared with a local random control, it has about 2× **more** prime cross-sums. At the burst at n = 2,326,240, all cross sums hit one of only two primes (4,652,317 and 4,652,353): the reflection lock.
- **Hole sets are local and dense:** at H = 50 they lie in [n - 86, n] and fill 50 of those 87 values.

## Bounds on H (n >= 1000)

G_W is the max prime gap meeting [2n - W, 2n + W].

| bound | holds? |
|---|---|
| H <= G_100 | yes, but with ratio exactly 1 at n = 8,918,331, so not robust |
| H <= G_300/2 + 7 | yes (best constant) |
| H <= Φ_4(n) := #{ v <= n : π(n+v) - π(2v) <= 4 } | yes (max ratio 0.75) |
| same, with K = 2 | fails at 35 values of n |

Correlations:
- H vs the prime gap containing 2n: 0.44.
- H vs #{ v : no prime in (2v, n+v] }: 0.74.

## Conclusions

1. **Measured: no restoring drift.** Creation and fill rates are equal, and the drift of H is weak and saturating. A drift argument alone cannot bound H.
2. **Measured: holes survive because of compositeness, not queueing.** A hole survives a step 97.5% of the time because a(k) + v is composite.
3. **Measured: lifetimes are governed by a prime count.** No hole outlived 9 primes in its sum window (2v, 2v + L): max K = 8, flat from 10^4 to 10^7.
4. **Measured: the pair and prime-sum-free ideas are dead as stated.**
5. **Proved, now candidate C009.** Each prime that hole v survives is "paid for" by one of four things:
   - a stolen smaller same-parity hole;
   - an opposite-parity value used ahead of time;
   - the term at the current step;
   - an opposite-parity hole at the current time.
6. **Interpretation: the missing ingredient.** Among the <= H ahead or late opposite-parity values, only O(1) are prime partners of a given hole. The data says at most 6-7. Proving that would give C010: an absolute bound on the number of primes a hole survives. That alone implies the permutation property.
