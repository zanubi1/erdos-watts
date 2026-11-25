import ErdosWatts.Defs

/-!
# L001 - Consecutive terms alternate in parity

Informal (lemmas/proven/L001-parity.md): for all n >= 1, a(n) and a(n+1) have opposite parity.
Corollary (L009 F1): a(n) ≡ n (mod 2) for all n >= 1.

Mapping: informal a(n) = `a n` for `n ≥ 1`; "opposite parity" = `a n % 2 ≠ a (n+1) % 2`.
-/

namespace ErdosWatts

/-- Proof step: `a n + a (n+1) ≥ 3`, since both are `≥ 1` and they are distinct. -/
theorem three_le_a_add_a_succ {n : ℕ} (hn : 1 ≤ n) : 3 ≤ a n + a (n + 1) := by
  have h1 := a_pos hn
  have h2 := a_pos (by omega : 1 ≤ n + 1)
  have h3 := a_ne_of_lt hn (by omega : n < n + 1)
  omega

/-- Proof step: `a n + a (n+1)` is an odd prime (prime by definition, and `≠ 2` since `≥ 3`). -/
theorem odd_a_add_a_succ {n : ℕ} (hn : 1 ≤ n) : Odd (a n + a (n + 1)) :=
  (a_succ_spec hn).2.2.odd_of_ne_two (by have := three_le_a_add_a_succ hn; omega)

/-- **L001.** For all `n ≥ 1`, `a n` and `a (n+1)` have opposite parity. -/
theorem L001_parity {n : ℕ} (hn : 1 ≤ n) : a n % 2 ≠ a (n + 1) % 2 := by
  have h := Nat.odd_iff.1 (odd_a_add_a_succ hn)
  omega

/-- **L001, corollary (L009 F1).** For all `n ≥ 1`, `a n ≡ n (mod 2)`. Induction on `n`
from `a 1 = 1`. -/
theorem a_mod_two {n : ℕ} (hn : 1 ≤ n) : a n % 2 = n % 2 := by
  induction n with
  | zero => omega
  | succ n ih =>
    rcases Nat.eq_zero_or_pos n with rfl | hpos
    · simp
    · have h1 := ih hpos
      have h2 := L001_parity hpos
      omega

/-- Form of F1 used in L009: for `n ≥ 1`, `a n` has parity `p` iff `n` has parity `p`. -/
theorem a_mod_two_eq_iff {n p : ℕ} (hn : 1 ≤ n) : a n % 2 = p ↔ n % 2 = p := by
  rw [a_mod_two hn]

end ErdosWatts
