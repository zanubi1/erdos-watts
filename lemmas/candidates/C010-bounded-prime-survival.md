# C010 - (Conjecture) A hole survives only boundedly many primes

## Statement

**Conjecture.** There is an absolute constant K0 such that for all n >= 1 and all v with 2 <= v <= n and v ∉ {a(1), ..., a(n)}:

    π(n + v) - π(2v)  <=  K0.

The numerical evidence is K0 = 8: the maximum is 8 up to n = 10^7, and the maximum per decade is flat from 10^4 to 10^7.

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

## Review log

- 2026-11-25: conjecture recorded from the hole-dynamics experiment. Not a lemma until proved.
- 2026-11-25 (literature): **not found** in the sources read. These were the OEIS A055265, A117922, A117925, A086527, A282695-7, A282700, A128280 and A051237 entries, the EKG and Yellowstone papers, and Sloane 2018. The last of these calls A055265 possibly "beyond reach" because of prime gaps. None of them states a proved bound on A117922(n) - n; only the empirical A282696/7 records exist. The EKG/Yellowstone bounds are linear sieve bounds for gcd sequences and do not transfer directly. Not yet searched: the Hasler wiki, the erdosproblems forum, UPINT, MO 241569. See literature/search-C009-C010-hole-payers.md.
- 2026-11-25 (editor): replaced the 'weaker version' with the uniform variants (C log v, F(n) = o(n/log n)) and the prover's warning that the per-v form is equivalent to the conjecture.
