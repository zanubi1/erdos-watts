# C009 - A hole can survive only as many primes as it has "payers"

## Statement

Notation:
- U_n = {a(1), ..., a(n)}.
- H_p(m) = #{ x ∈ [1, m] : x ≡ p (mod 2), x ∉ U_m } is the number of holes of parity p at time m.
- B(v) = #{ x < v : x ≡ v (mod 2), x ∉ U_v } is the number of smaller same-parity holes at time v.

Let n >= 2 and 2 <= v <= n with v ∉ U_n, and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  1 + B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n).

**Corollary.** Suppose H(m) <= h for all m <= n, where H = H_0 + H_1. Then every hole v at time n (2 <= v <= n, v ∉ U_n) satisfies

    n - v  <  ℓ_{3h+2}(2v),   where ℓ_K(x) = (the K-th prime > x) - x.

## Depends on

L001, L002. Uses the per-parity count from C007 Step 2, generalized to both parities: at time m, the number of used values of parity p that are > m equals H_p(m).

## Proof

_Draft by the experimenter (2026-11-25), checked by the main session. Awaiting the prover's full write-up._

- **The partners.** Each prime q ∈ (2v, n + v] is odd, since q > 2v >= 4.
  - Put w = q - v. Then w ∈ (v, n] and w ≡ 1 - ε (mod 2).
  - Distinct q give distinct w.
- **The four cases.** Classify each such w by fi(w), its index of first occurrence (fi(w) = ∞ if it never occurs). The cases cover all possibilities.
  1. **fi(w) <= v - 1 ("ahead").** Then w > v - 1, w has parity 1 - ε, and w ∈ U_{v-1}.
     - At time m, the number of used values of parity p that are > m equals H_p(m). This is the counting argument of C007 Step 2, applied to either parity, using a(k) ≡ k (mod 2).
     - So there are at most H_{1-ε}(v-1) such w.
  2. **v <= fi(w) = k <= n - 1 (a "steal").** Then a(k) + v = q is prime. Also v ∉ U_k, since k <= n.
     - So a(k+1) <= v by the greedy rule, and a(k+1) ≠ v since v ∉ U_n and k + 1 <= n. Hence x := a(k+1) < v.
     - x has parity ε, by L001.
     - x ∉ U_k ⊇ U_v, since k >= v. So x is counted by B(v).
     - Distinct k give distinct x, so there are at most B(v) such w.
  3. **fi(w) = n.** There is at most one such w, namely a(n).
  4. **fi(w) > n.** Then w ∈ [1, n], w ∉ U_n, and w has parity 1 - ε. So w is a hole at time n, and there are at most H_{1-ε}(n) such w.
- **Conclusion.** Summing the four cases bounds the number of primes in (2v, n + v], which is π(n + v) - π(2v). ∎
- **Corollary.** B(v), H_{1-ε}(v-1) and H_{1-ε}(n) are each <= h. So (2v, n + v] contains at most 3h + 1 primes. Then n + v < (the (3h+2)-th prime > 2v), i.e. n - v < ℓ_{3h+2}(2v). ∎

## Numerical check

`experiments/src/holes_dynamics.py`, section `bounds`. Checked for all 4.71M holes v at n = fi(v) - 1, and for the smallest hole at every n <= 10^7: 0 violations.
- The left side is at most 8; the right side reaches 52.
- See `experiments/results/holes_dynamics_1e7/summary.md`.

## Review log

- 2026-11-25: candidate created from the hole-dynamics experiment (E5). The main session checked the four-case split. **Awaiting prover (write-up), literature and skeptic.**
- 2026-11-25 (literature): Case 2 ("steals") is the charging argument of Lagarias-Rains-Sloane 2002, EKG Lemma 7 (each admissible partner of a missing value forces a smaller next term, and distinct times give distinct values). Cite it. The special case B(v) = 0 is the classical smallest-missing step (EKG Lemmas 3-4, Yellowstone Theorem 1(vi), A253074). I did **not find** the four-case partition or the inequality itself in the sources read. No delay bound for A055265 was found anywhere. See literature/search-C009-C010-hole-payers.md.
