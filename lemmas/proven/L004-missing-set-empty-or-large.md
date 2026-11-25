# L004 - The missing set is empty or has size at least ~ X / log X

## Statement

Let M be the set of positive integers that never occur in the sequence. If M is nonempty, then

    |M ∩ [1, X]| >= π(X + m) - π(m) - N0 = (1 - o(1)) X / log X,

where m = min M and N0 is as in L003. In particular, **M finite implies M empty**.

## Depends on

L003.

## Proof

Let m = min M and N0 as in L003. Let p be a prime with p > m + 1, and set v = p - m >= 2. Then v + m = p is prime.

Parity check: m >= 2, since a(1) = 1 occurs. So p > m + 1 >= 3 is odd, and v = p - m has parity opposite to m. This is exactly the parity hypothesis of L003. (L003's proof in fact gives compositeness for every n >= N0, whatever the parity.)

Claim: v ∈ M ∪ {a(1), ..., a(N0 - 1)}.
Suppose v occurs at some index n >= N0, i.e. a(n) = v. Then a(n) + m = p is prime, contradicting L003. So either v never occurs (v ∈ M) or it only occurs before index N0.

The map p -> p - m is injective, so the number of v <= X obtained this way is π(X + m) - π(m + 1). At most N0 - 1 of them lie in {a(1..N0-1)}. Hence |M ∩ [1, X]| >= π(X + m) - π(m + 1) - (N0 - 1), which is ~ X / log X by the prime number theorem (Chebyshev's lower bound is enough for >> X / log X).

If M is finite, the left side is bounded while the right side tends to infinity: contradiction. So M finite implies M empty. ∎

## Numerical check

Up to 10^7 terms, the only values not yet seen are 13 values just below the current max (the "frontier"), consistent with M = ∅.

## Review log

- 2026-11-25: drafted at setup. **Awaiting skeptic.** Literature check needed: this "a missing value forces many missing values" trick is probably folklore for greedy prime-sum sequences.
- 2026-11-24 (skeptic): **PASS, conditional on L003** (L003 is still a candidate, so L004 is only as strong as L003). Checked:
  - Quantifiers: for any M ≠ ∅, with m = min M and N0 = 1 + (last index of any value < m) (finite because the sequence is injective and there are finitely many values < m), for all X ≥ 1 the inequality holds; the asymptotic is as X → ∞ with m, N0 fixed. The statement's bound uses π(m) and N0; the proof gives π(X+m) - π(m+1) - (N0-1), which is ≥ the stated bound since π(m+1) ≤ π(m) + 1. So the proof implies the statement.
  - Parity hypothesis of L003 (the proof does not check it; **editorial fix required**): m ≥ 2 since a(1) = 1, so p > m+1 ≥ 3 is odd, hence v = p - m has parity opposite to m, as L003 requires. Add this line to the proof.
  - v ≥ 2 and v ≠ m (p = 2m is not prime for m ≥ 2). Values v < m are covered by "occurs before N0" by the definition of N0. Correct.
  - Counting: p ↦ p - m is injective; v ≤ X iff p ≤ X + m; primes in (m+1, X+m] number π(X+m) - π(m+1). At most N0 - 1 of them are among a(1..N0-1). Correct.
  - Asymptotics: Chebyshev gives π(X+m) ≥ cX/log X, so the right side → ∞, and "M finite ⇒ M empty" follows. The "= (1 - o(1)) X/log X" in the statement holds by PNT (should read "≥" with lower bound X/log X·(1-o(1)), harmless).
  - Variant check: the argument uses only injectivity, the definition of N0, and L003, and transfers to any a(1). It makes no claim L003 does not already carry, so it does not "prove" a false variant on its own. All the mathematical risk is in L003.
  - Note: the drafting entry above is dated 2026-11-25, which is after this review. Check the date.
- 2026-11-25 (main-session review, with Matteo's delegated OK): PASS. I added the parity line (m >= 2, so p is odd and v = p - m has parity opposite to m). The count: primes in (m+1, X+m] biject onto v <= X; at most N0 - 1 of them occur before N0; and π(X+m) - π(m+1) - (N0-1) >= π(X+m) - π(m) - N0. The bound holds for every X >= 1 (trivially when the right side is negative). Chebyshev gives divergence. **Moved to lemmas/proven/ as L004 (formerly C004).**
