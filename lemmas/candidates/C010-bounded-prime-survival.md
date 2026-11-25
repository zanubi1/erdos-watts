# C010 - (Conjecture) A hole survives only boundedly many primes

## Statement

**Conjecture.** There is an absolute constant K0 such that for all n >= 1 and all v with 2 <= v <= n and v ∉ {a(1), ..., a(n)}:

    π(n + v) - π(2v)  <=  K0.

Numerical evidence: K reaches 8 up to 10^7 but **11 up to 10^8** (at v = 76,132,619). The per-decade maxima are 6, 7, 8, 8, 11, and fit K ≈ 2 + 1.1 log10 v better than a constant. So an absolute K0 is doubtful, and the **C log v variant below is the realistic target**. See `experiments/results/k_survival_1e8/summary.md`.

**Uniform variants that also suffice.**
- K0 replaced by C log v, which the data supports equally well (the tail of K looks geometric, ratio about 0.15, and is creeping upward slowly).
- More generally, any bound F(n) = o(n / log n), by the argument of C011.

**Warning (prover, 2026-11-25): the per-v version is the conjecture itself.** "π(n + v) - π(2v) <= F(v) for every hole v at time n", for an arbitrary finite F, is *equivalent* to the permutation property: if v occurs, the left side is only defined for n < fi(v). The content of C010 is the **uniformity** of the bound.

## Why it would suffice

Suppose v never occurs. Then v is a hole at every time n >= v, so π(n + v) - π(2v) <= K0 for all n. This is impossible, because π(n + v) → ∞ as n → ∞. Hence v occurs, and moreover fi(v) <= v + ℓ_{K0+1}(2v).

A uniform bound also gives a quantitative delay bound fi(v) <= v + ℓ_{F+1}(2v). Turning that into a power of v needs short-interval prime counts (Huxley, or a quantitative Baker-Harman-Pintz; see C006 Remark R0).

## Depends on

C009. By C009, it would suffice to bound

    B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n)

by O(1). The data says these terms are not O(1) individually: H reaches 50. So the real content is that **among the <= H ahead or late opposite-parity values, only O(1) are prime partners of v**. In the data that count is at most 6-7.

## Proof

None yet.

## Numerical check

See `experiments/results/holes_dynamics_1e7/summary.md`, the table of K(v) by range of v.

2026-11-25 (experimenter, N = 10^8, `experiments/src/k_survival_1e8.py`): **K0 = 8 does not hold beyond 10^7.** Max K per decade (completed holes): 6, 7, 8, 8, 11 for [10^3,10^4), ..., [10^7,10^8). The maximum K = 11 occurs at v = 76,132,619 (lifetime 96, H(v) = 25); K = 10 occurs 10 times. Per 10^7 block (each about 4.76M holes, the same sample size as [10^6, 10^7)): 9, 9, 9, 10, 10, 9, 11, 10, 10. The tail is creeping: P(K >= 7) is 3.5e-5 for v < 10^7 and 5.1e-5 on [10^7, 10^8); P(K >= 8) is 3.2e-6 and 8.5e-6. The geometric ratio is about 0.16 on [10^7, 10^8), versus about 0.15 below. A fit of the decade maxima, maxK ≈ 1.95 + 1.10 log10 v, fits far better than a constant (residual SS 1.9 vs 14.0). With a geometric tail, the extreme-value prediction (M·P(K >= j) ≈ 1) fits the growth of the maxima. **The data now favour max K growing like log v, not K = O(1).** The uniform C log v variant is still consistent with the data.

## Review log

- 2026-11-25: conjecture recorded from the hole-dynamics experiment. Not a lemma until proved.
- 2026-11-25 (literature): **not found** in the sources read. These were the OEIS A055265, A117922, A117925, A086527, A282695-7, A282700, A128280 and A051237 entries, the EKG and Yellowstone papers, and Sloane 2018. The last of these calls A055265 possibly "beyond reach" because of prime gaps. None of them states a proved bound on A117922(n) - n; only the empirical A282696/7 records exist. The EKG/Yellowstone bounds are linear sieve bounds for gcd sequences and do not transfer directly. Not yet searched: the Hasler wiki, the erdosproblems forum, UPINT, MO 241569. See literature/search-C009-C010-hole-payers.md.
- 2026-11-25 (editor): replaced the 'weaker version' with the uniform variants (C log v, F(n) = o(n/log n)) and the prover's warning that the per-v form is equivalent to the conjecture.
