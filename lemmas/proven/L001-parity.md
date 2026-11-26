# L001 - Consecutive terms alternate in parity

_Trivial setup lemma (no skeptic pass required)._

## Statement

For all n >= 1, a(n) and a(n+1) have opposite parity.

## Proof

a(n) and a(n+1) are distinct positive integers, so a(n) + a(n+1) >= 1 + 2 = 3. It is prime by definition, hence an odd prime, so the two terms have opposite parity. Since a(1) = 1, a(n) is odd for n odd and even for n even.

## Numerical check

Holds for the first 10^7 terms (by construction of `greedy.py`, which only searches the opposite parity; first 100,000 terms also match OEIS A055265).

## Review log

- 2026-11-25: written at setup.
- 2026-11-25 (formalizer): **formalized: yes.** File: lean/ErdosWatts/L001.lean, theorems `ErdosWatts.L001_parity` (for `1 ≤ n`, `a n % 2 ≠ a (n + 1) % 2`) and the corollary `ErdosWatts.a_mod_two` (for `1 ≤ n`, `a n % 2 = n % 2`; this is L009's F1). Sub-steps follow the informal proof: `three_le_a_add_a_succ` (sum >= 3 from positivity + distinctness), `odd_a_add_a_succ` (prime and != 2, hence odd). Uses the shared definitions in lean/ErdosWatts/Defs.lean.
  Axioms: `'ErdosWatts.L001_parity' depends on axioms: [propext, Classical.choice, Quot.sound]`; `'ErdosWatts.a_mod_two' depends on axioms: [propext, Classical.choice, Quot.sound]`. Explicit hypotheses: none.
  Discrepancies informal vs formal: none ("opposite parity" is rendered as `a n % 2 ≠ a (n+1) % 2`; informal a(n) = `a n` for n >= 1). GAPs found: none.
