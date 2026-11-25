import ErdosWatts.L004

/-!
# L005 - Reduction: an upper displacement bound implies the permutation property

Informal (lemmas/proven/L005-displacement-reduction.md): suppose there is a nondecreasing
function f : N -> N with f(x) = o(x / log x) such that a(n) <= n + f(n) for all n. Then every
positive integer occurs in the sequence.

## Mapping informal -> formal

* f : N -> N is `f : ℕ → ℕ`; "nondecreasing" is `Monotone f`.
* "f(x) = o(x / log x)" is encoded with Mathlib's little-o along `atTop` on ℕ, cast to ℝ:
  `(fun x : ℕ => (f x : ℝ)) =o[atTop] (fun x : ℕ => (x : ℝ) / Real.log x)`,
  i.e. for every `c > 0`, eventually `|f x| ≤ c * |x / log x|`. (Only the behaviour for large `x`
  matters, so the junk values `Real.log 0 = 0`, `Real.log 1 = 0` are irrelevant.)
* "a(n) <= n + f(n) for all n": informal a(n) = `a n` for `n ≥ 1`; the hypothesis is
  `∀ n, 1 ≤ n → a n ≤ n + f n`. (For `n = 0`, `a 0 = 0` is junk and the inequality is trivial,
  so this is equivalent to `∀ n`.)
* "every positive integer occurs" = `∀ v, 1 ≤ v → Occurs v`; equivalently `missingSet = ∅`
  (`L005_missingSet_empty`).
* The proof uses L004's asymptotic lower bound `L004_eventually_ge`, which rests on Mathlib's
  prime number theorem `Nat.isEquivalent_primeCounting` (a Mathlib theorem, not a hypothesis).
-/

namespace ErdosWatts

open Filter Asymptotics

/-- **Counting step.** If `f` is monotone and `a n ≤ n + f n` for `n ≥ 1`, then
`|M ∩ [1, X]| ≤ f X` for every `X`. (For `n ≤ X' = X - f X`, `a n ≤ X`, so the `X'` distinct
values `a 1, ..., a X'` lie in `[1, X]` and outside M.) -/
theorem missing_count_le {f : ℕ → ℕ} (hmono : Monotone f)
    (hbound : ∀ n, 1 ≤ n → a n ≤ n + f n) (X : ℕ) :
    (missingSet ∩ Set.Icc 1 X).ncard ≤ f X := by
  classical
  rw [ncard_missing_eq]
  set X' := X - f X with hX'
  set MX := (Finset.Icc 1 X).filter (fun v => v ∈ missingSet) with hMX
  set T := (Finset.Icc 1 X').image a with hT
  have hTcard : T.card = X' := by
    rw [hT, Finset.card_image_of_injOn (fun i hi j hj h => a_inj
      (Finset.mem_Icc.1 hi).1 (Finset.mem_Icc.1 hj).1 h)]
    simp
  have hdisj : Disjoint MX T := by
    rw [Finset.disjoint_left]
    intro v hvM hvT
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.1 hvT
    exact (Finset.mem_filter.1 hvM).2.2 (occurs_a (Finset.mem_Icc.1 hk).1)
  have hsub : MX ∪ T ⊆ Finset.Icc 1 X := by
    intro v hv
    rcases Finset.mem_union.1 hv with h | h
    · exact (Finset.mem_filter.1 h).1
    · obtain ⟨k, hk, rfl⟩ := Finset.mem_image.1 h
      obtain ⟨hk1, hkX⟩ := Finset.mem_Icc.1 hk
      have h1 := hbound k hk1
      have h2 : f k ≤ f X := hmono (by omega)
      exact Finset.mem_Icc.2 ⟨a_pos hk1, by omega⟩
  have := Finset.card_le_card hsub
  rw [Finset.card_union_of_disjoint hdisj, hTcard, Nat.card_Icc] at this
  omega

/-- **L005.** Informal: suppose there is a nondecreasing f : N -> N with f(x) = o(x / log x) such
that a(n) <= n + f(n) for all n. Then every positive integer occurs in the sequence. -/
theorem L005_displacementReduction {f : ℕ → ℕ} (hmono : Monotone f)
    (hlittle : (fun x : ℕ => (f x : ℝ)) =o[atTop] (fun x : ℕ => (x : ℝ) / Real.log x))
    (hbound : ∀ n, 1 ≤ n → a n ≤ n + f n) :
    ∀ v, 1 ≤ v → Occurs v := by
  intro v hv
  by_contra hocc
  have hM : missingSet.Nonempty := ⟨v, hv, hocc⟩
  -- L004: eventually |M ∩ [1, X]| ≥ (1/2) X / log X
  have hlow := L004_eventually_ge hM (ε := 1 / 2) (by norm_num)
  -- f = o(X / log X): eventually f X ≤ (1/4) X / log X
  have hup := hlittle.def (c := 1 / 4) (by norm_num)
  have hpos : ∀ᶠ X : ℕ in atTop, 0 < (X : ℝ) / Real.log X :=
    tendsto_div_log_nat.eventually_gt_atTop 0
  obtain ⟨X, hX1, hX2, hX3⟩ := (hlow.and (hup.and hpos)).exists
  have hcount : ((missingSet ∩ Set.Icc 1 X).ncard : ℝ) ≤ f X := by
    exact_mod_cast missing_count_le hmono hbound X
  rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg (Nat.cast_nonneg _),
    abs_of_pos hX3] at hX2
  linarith

/-- **L005, set form.** Under the same hypotheses, the missing set M is empty. -/
theorem L005_missingSet_empty {f : ℕ → ℕ} (hmono : Monotone f)
    (hlittle : (fun x : ℕ => (f x : ℝ)) =o[atTop] (fun x : ℕ => (x : ℝ) / Real.log x))
    (hbound : ∀ n, 1 ≤ n → a n ≤ n + f n) :
    missingSet = ∅ := by
  ext v
  simp only [Set.mem_empty_iff_false, iff_false]
  exact fun hv => hv.2 (L005_displacementReduction hmono hlittle hbound v hv.1)

end ErdosWatts
