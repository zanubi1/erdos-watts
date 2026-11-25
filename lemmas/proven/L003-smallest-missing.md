# L003 - The smallest missing value blocks a translate of the primes

## Statement

Suppose some positive integer never occurs in the sequence, and let m be the smallest such. Then there is N0 such that for every n >= N0 with a(n) of parity opposite to m, the number a(n) + m is composite.

## Depends on

L001, L002.

## Proof

Every x < m occurs, so there are finitely many indices at which the values 1, ..., m-1 occur; let N0 exceed all of them. Fix n >= N0 with a(n) of parity opposite to m. Suppose for contradiction a(n) + m is prime.

Consider the set S = { x >= 1 : x not in {a(1..n)}, a(n) + x prime }. Every x < m is in {a(1..n)} because n >= N0, so S contains no x < m. And m is not in {a(1..n)} (m never occurs), and a(n) + m is prime, so m ∈ S. Hence min S = m, so a(n+1) = m, contradicting that m never occurs. ∎

(Parity of a(n) opposite to m is not used in the argument; it only matters because if a(n) and m have the same parity, a(n) + m is even and > 2, so composite anyway.)

## Numerical check

Not applicable directly (concerns a hypothetical missing value).

## Review log

- 2026-11-25: drafted at setup. **Awaiting skeptic.**
- 2026-11-24 (skeptic): **PASS.**
  - Restated: if M = {k >= 1 : k never occurs} is nonempty and m = min M, then there exists N0 such that for all n >= N0, a(n) + m is not prime (the proof actually gives this for all n >= N0; the parity restriction in the statement only weakens it). Note m >= 2 since a(1) = 1, so the parity remark "a(n) + m even and > 2" is correct (and a(n) != m anyway).
  - N0: each of 1..m-1 occurs (by minimality of m), take N0 = 1 + max of their first-occurrence indices (distinctness makes "the" index unique anyway). Well defined; for m with no smaller values this is vacuous but m >= 2 regardless.
  - Main step: for n >= N0, {1..m-1} is a subset of {a(1..n)}, m is not in {a(1..n)} ("never occurs", not "not yet occurred" - correct use), so if a(n)+m is prime then min S = m and a(n+1) = m by the definition of the sequence. Contradiction is valid. Nonemptiness of S is witnessed by m itself, so even L002 is only needed for the sequence to be defined for all n.
  - Dependencies: L001 is not actually used (only cited for the parity remark, which is elementary); L002 is in lemmas/proven/. Result is unconditional.
  - Variant test: the argument uses only "a(n+1) = least unused x satisfying a predicate P(a(n), x)", so it also proves the analogue for composite sums and for any a(1). The analogous statements are true there too (same argument), so no false variant is "proved". No counterexample possible beyond the hypothesis being vacuous.
  - Housekeeping: the prior log entry is dated 2026-11-25, which is after this review date; likely a typo - Matteo should check. Section is titled "Draft proof" rather than "Proof" per conventions; consider renaming. Suggest updating "Depends on" to "L002 (L001 only for the parity remark)".
- 2026-11-25 (main-session review, with Matteo's delegated OK): PASS. N0 exceeds every index of a value < m, so U_n ⊇ [1, m-1] for n >= N0, while m ∉ U_n. If a(n)+m were prime, then m = min A_n, contradicting that m never occurs. The proof in fact shows compositeness for every n >= N0, whatever the parity. **Moved to lemmas/proven/ as L003 (formerly C003).**
