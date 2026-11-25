# C010 - (Conjecture) A hole survives only boundedly many primes

## Statement

**Conjecture.** There is an absolute constant K0 such that for all n >= 1 and all v with 2 <= v <= n and v ∉ {a(1), ..., a(n)}:

    π(n + v) - π(2v)  <=  K0.

The numerical evidence is K0 = 8: the maximum is 8 up to n = 10^7, and the maximum per decade is flat from 10^4 to 10^7.

Weaker version, which suffices: π(n + v) - π(2v) <= F(v) for every hole v at time n, with F(v) = o(v^{0.525} / log v).

## Why it would suffice

Suppose v never occurs. Then v is a hole at every time n >= v, so π(n + v) - π(2v) <= K0 for all n. This is impossible, because π(n + v) → ∞ as n → ∞. Hence v occurs, and moreover fi(v) <= v + ℓ_{K0+1}(2v).

For the weaker version, the same argument works, provided some interval (2v, n + v] with n - v <= v^{0.525} contains more than F(v) primes. GAP?: this needs a quantitative Baker-Harman-Pintz lower bound for the count of primes, not just existence; see C006 Remark R0.

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
