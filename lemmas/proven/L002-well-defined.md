# L002 - The sequence is well defined

_Trivial setup lemma (no skeptic pass required)._

## Statement

For every n, the set { x >= 1 : x not in {a(1..n)} and a(n) + x prime } is nonempty, so a(n+1) exists.

## Proof

Let U = {a(1), ..., a(n)} and K = max U. There are infinitely many primes, so pick a prime p > a(n) + K. Then x = p - a(n) > K, so x is unused, x >= 1, and a(n) + x = p is prime.

(OEIS cites Dirichlet; plain infinitude of primes suffices.)

## Review log

- 2026-11-25: written at setup.
- 2026-11-25 (formalizer): **formalized: yes.** File: lean/ErdosWatts/L002.lean, theorem `ErdosWatts.L002_wellDefined` (for `1 ≤ n`, `(A n).Nonempty`, where `A n = {x | 1 ≤ x ∧ x ∉ U n ∧ (a n + x).Prime}`), plus `ErdosWatts.L002_a_succ_eq_sInf` (for `1 ≤ n`, `a (n + 1) = sInf (A n)`). The proof is the informal one (prime p >= a(n) + max U + 1 via `Nat.exists_infinite_primes`, x = p - a(n)); it lives in Defs.lean as `exists_next`, because the definition of the sequence itself needs it.
  Axioms: `'ErdosWatts.L002_wellDefined' depends on axioms: [propext, Classical.choice, Quot.sound]`; `'ErdosWatts.L002_a_succ_eq_sInf' depends on axioms: [propext, Classical.choice, Quot.sound]`. Explicit hypotheses: none.
  Discrepancies informal vs formal: the informal statement says "for every n"; the formal one assumes `1 ≤ n` (a(0) is not a term; in Lean `a 0 = 0` is junk, for which the set is in fact also nonempty). The informal "p > a(n) + K" is used as "p >= a(n) + K + 1" (same thing). GAPs found: none.
