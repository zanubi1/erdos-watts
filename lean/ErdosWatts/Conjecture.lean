import ErdosWatts.Defs

/-!
# Watts' greedy question (Erdős Problem 473, OEIS A055265)

*References:*
- [erdosproblems.com/473](https://www.erdosproblems.com/473)
- [OEIS A055265](https://oeis.org/A055265)
- [ErGr80] Erdős, P. and Graham, R., *Old and new problems and results in combinatorial
  number theory*, Monographies de L'Enseignement Mathématique (1980).

Style follows google-deepmind/formal-conjectures (`FormalConjectures/ErdosProblems/473.lean`,
which formalizes the main question `erdos_473` and the finite variant, but not Watts' greedy
sub-question). Their attributes are not available in this project; in their notation this
statement would carry `@[category research open, AMS 11]`.

This file is the ONLY place in the project where `sorry` is allowed: `watts_greedy_bijective`.
-/

namespace ErdosWatts

/-- The sequence as a map `ℕ+ → ℕ+`: `n ↦ a n` (well defined by `a_pos`). -/
def aPNat (n : ℕ+) : ℕ+ := ⟨a n, a_pos n.pos⟩

@[simp] theorem coe_aPNat (n : ℕ+) : (aPNat n : ℕ) = a n := rfl

/-- `aPNat` is injective (L009 F2; proved). -/
theorem aPNat_injective : Function.Injective aPNat := fun i j h =>
  PNat.coe_injective (a_inj i.pos j.pos (congrArg PNat.val h))

/-- Since injectivity is proved, bijectivity is equivalent to "every positive integer occurs". -/
theorem aPNat_bijective_iff : Function.Bijective aPNat ↔ ∀ v : ℕ, 1 ≤ v → Occurs v := by
  constructor
  · rintro ⟨-, hs⟩ v hv
    obtain ⟨n, hn⟩ := hs ⟨v, hv⟩
    exact ⟨n, n.pos, congrArg PNat.val hn⟩
  · intro h
    refine ⟨aPNat_injective, fun v => ?_⟩
    obtain ⟨k, hk, hak⟩ := h v v.pos
    exact ⟨⟨k, hk⟩, PNat.coe_injective hak⟩

/--
**Watts' greedy question.** Let a(1) = 1 and let a(n+1) be the least positive integer, not among
a(1), ..., a(n), such that a(n) + a(n+1) is prime. Is (a(n))_{n ≥ 1} a permutation of the
positive integers?

A sub-question of Erdős Problem 473 attributed to Watts (erdosproblems.com/473; OEIS A055265,
which gives only a probabilistic argument). Status: **research open** (category research open,
AMS 11). Stated here in the "yes" direction; a disproof would be a proof of the negation.
The proof is `sorry` on purpose.
-/
theorem watts_greedy_bijective : Function.Bijective aPNat := by
  sorry

/-- Equivalent form of the conjecture, derived from `watts_greedy_bijective`: every `v ≥ 1`
occurs. (Inherits the `sorry`.) -/
theorem watts_greedy_every_value_occurs : ∀ v : ℕ, 1 ≤ v → Occurs v :=
  aPNat_bijective_iff.1 watts_greedy_bijective

/-- Sanity check: the definition reproduces the first twelve terms of A055265,
1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16.

Proof: one `step_of_least` per term; each side condition ("`x` is admissible and no `y < x` is")
is a concrete finite fact closed by plain `decide` (kernel-checked; no `native_decide`, so no
extra axiom). A single `decide` on the whole list is far too slow in the kernel. -/
theorem a_first_terms :
    (List.range 12).map (fun i => a (i + 1)) = [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16] := by
  have h1 : a 1 = 1 ∧ U 1 = {1} := ⟨rfl, U_one⟩
  have h2 := step_of_least (x := 2) (by norm_num) h1 (by decide)
  have h3 := step_of_least (x := 3) (by norm_num) h2 (by decide)
  have h4 := step_of_least (x := 4) (by norm_num) h3 (by decide)
  have h5 := step_of_least (x := 7) (by norm_num) h4 (by decide)
  have h6 := step_of_least (x := 6) (by norm_num) h5 (by decide)
  have h7 := step_of_least (x := 5) (by norm_num) h6 (by decide)
  have h8 := step_of_least (x := 8) (by norm_num) h7 (by decide)
  have h9 := step_of_least (x := 9) (by norm_num) h8 (by decide)
  have h10 := step_of_least (x := 10) (by norm_num) h9 (by decide)
  have h11 := step_of_least (x := 13) (by norm_num) h10 (by decide)
  have h12 := step_of_least (x := 16) (by norm_num) h11 (by decide)
  simp [List.range_succ, h1.1, h2.1, h3.1, h4.1, h5.1, h6.1, h7.1, h8.1, h9.1, h10.1, h11.1,
    h12.1]

end ErdosWatts
