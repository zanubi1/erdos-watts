import ErdosWatts.L003

/-!
# L004 - The missing set is empty or has size at least ~ X / log X

Informal (lemmas/proven/L004-missing-set-empty-or-large.md): let M be the set of positive
integers that never occur in the sequence. If M is nonempty, then

    |M ∩ [1, X]| >= π(X + m) - π(m) - N0 = (1 - o(1)) X / log X,

where m = min M and N0 is as in L003. In particular, M finite implies M empty.

## Mapping informal -> formal

* M = `missingSet` (L003.lean), m = min M is `IsLeast missingSet m`.
* "N0 as in L003" = any `N0` with L003's conclusion
  `∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime` (hypothesis `hN0`). The bound is
  proved for *every* such `N0`; `L004_exists` packages it with the `N0` produced by L003.
* |M ∩ [1, X]| = `(missingSet ∩ Set.Icc 1 X).ncard` (a finite set, so `ncard` is its size).
* π = `Nat.primeCounting`. The inequality is stated in `ℤ` to avoid truncated subtraction
  (it holds for every `X : ℕ`, trivially when the right side is negative).
* "= (1 - o(1)) X / log X" is not part of the inequality. We prove the asymptotic content
  separately, using Mathlib's prime number theorem `Nat.isEquivalent_primeCounting` (proved in
  Mathlib, not a hypothesis):
  - `L004_rhs_isEquivalent`: the right side, cast to ℝ, is `~ X / log X` as `X → ∞` in ℕ;
  - `L004_eventually_ge`: for every `ε > 0`, eventually `|M ∩ [1, X]| ≥ (1 - ε) X / log X`.
* "M finite implies M empty" = `L004_finite_imp_empty : missingSet.Finite → missingSet = ∅`.
  Its proof uses only the infinitude of primes (`Nat.tendsto_primeCounting`), not the PNT.
-/

namespace ErdosWatts

open Filter Asymptotics Topology

/-- The number of primes in `(m, X + m]` is `π(X + m) - π(m)`. -/
theorem card_primes_Ioc_add (m X : ℕ) :
    ((Finset.Ioc m (X + m)).filter Nat.Prime).card + Nat.primeCounting m =
      Nat.primeCounting (X + m) := by
  rw [← Nat.primesLE_card_eq_primeCounting, ← Nat.primesLE_card_eq_primeCounting,
    ← Finset.card_union_of_disjoint]
  · congr 1
    ext p
    simp only [Finset.mem_union, Finset.mem_filter, Finset.mem_Ioc, Nat.mem_primesLE]
    constructor
    · rintro (⟨⟨_, h⟩, hp⟩ | ⟨h, hp⟩) <;> exact ⟨by omega, hp⟩
    · rintro ⟨h, hp⟩
      rcases Nat.lt_or_ge m p with h' | h'
      · exact Or.inl ⟨⟨h', h⟩, hp⟩
      · exact Or.inr ⟨h', hp⟩
  · rw [Finset.disjoint_left]
    intro p hp hp'
    simp only [Finset.mem_filter, Finset.mem_Ioc, Nat.mem_primesLE] at hp hp'
    omega

/-- `|M ∩ [1, X]|` as a `Finset` cardinality. -/
theorem ncard_missing_eq (X : ℕ) :
    (missingSet ∩ Set.Icc 1 X).ncard =
      (by classical exact ((Finset.Icc 1 X).filter (fun v => v ∈ missingSet)).card) := by
  classical
  rw [← Set.ncard_coe_finset]
  congr 1
  ext v
  simp only [Set.mem_inter_iff, Set.mem_Icc, Finset.coe_filter, Finset.mem_Icc]
  exact ⟨fun h => ⟨h.2, h.1⟩, fun h => ⟨h.2, h.1⟩⟩

/-- **Main claim of the proof.** For `p` prime in `(m, X + m]`, `v = p - m` lies in
`M ∪ {a(1), ..., a(N0 - 1)}`. -/
theorem mem_missing_or_early {m N0 : ℕ} (hm : IsLeast missingSet m)
    (hN0 : ∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime)
    {p : ℕ} (hpm : m < p) (hp : p.Prime) :
    p - m ∈ missingSet ∨ ∃ k, 1 ≤ k ∧ k < N0 ∧ a k = p - m := by
  have hm2 := two_le_of_mem_missingSet hm.1
  by_cases hv : p - m ∈ missingSet
  · exact Or.inl hv
  · right
    have hocc : Occurs (p - m) := by
      by_contra h; exact hv ⟨by omega, h⟩
    obtain ⟨k, hk1, hak⟩ := hocc
    refine ⟨k, hk1, ?_, hak⟩
    by_contra hk
    -- parity: p > m ≥ 2 is an odd prime, so p - m has parity opposite to m
    have hodd : p % 2 = 1 := by
      rcases hp.eq_two_or_odd with h | h
      · omega
      · exact h
    have hpar : a k % 2 ≠ m % 2 := by rw [hak]; omega
    exact hN0 k (by omega) hk1 hpar (by rw [hak, show p - m + m = p by omega]; exact hp)

/-- **L004, quantitative bound** (in ℕ, without subtraction). -/
theorem L004_bound_nat {m N0 : ℕ} (hm : IsLeast missingSet m)
    (hN0 : ∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime) (X : ℕ) :
    Nat.primeCounting (X + m) ≤
      (missingSet ∩ Set.Icc 1 X).ncard + Nat.primeCounting m + N0 := by
  classical
  rw [ncard_missing_eq]
  have hPcount := card_primes_Ioc_add m X
  set P := (Finset.Ioc m (X + m)).filter Nat.Prime with hP
  set MX := (Finset.Icc 1 X).filter (fun v => v ∈ missingSet) with hMX
  set E := (Finset.Ico 1 N0).image a with hE
  have hsub : P.image (fun p => p - m) ⊆ MX ∪ E := by
    intro v hv
    obtain ⟨p, hpP, rfl⟩ := Finset.mem_image.1 hv
    simp only [hP, Finset.mem_filter, Finset.mem_Ioc] at hpP
    obtain ⟨⟨hpm, hpX⟩, hp⟩ := hpP
    rcases mem_missing_or_early hm hN0 hpm hp with h | ⟨k, hk1, hkN, hak⟩
    · exact Finset.mem_union_left _ (Finset.mem_filter.2 ⟨Finset.mem_Icc.2 ⟨by omega, by omega⟩, h⟩)
    · exact Finset.mem_union_right _ (Finset.mem_image.2 ⟨k, Finset.mem_Ico.2 ⟨hk1, hkN⟩, hak⟩)
  have hinj : Set.InjOn (fun p => p - m) (P : Set ℕ) := by
    intro p hp q hq h
    simp only [hP, Finset.coe_filter, Finset.mem_Ioc, Set.mem_ofPred_eq] at hp hq
    simp only at h
    omega
  have hcardP : P.card ≤ MX.card + E.card := by
    rw [← Finset.card_image_of_injOn hinj]
    exact (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
  have hcardE : E.card ≤ N0 - 1 := by
    refine Finset.card_image_le.trans ?_
    simp
  omega

/-- **L004, quantitative bound, as stated.** If `m = min M` and `N0` is as in L003, then for every
`X`, `|M ∩ [1, X]| ≥ π(X + m) - π(m) - N0` (in ℤ). -/
theorem L004_bound {m N0 : ℕ} (hm : IsLeast missingSet m)
    (hN0 : ∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime) (X : ℕ) :
    (Nat.primeCounting (X + m) : ℤ) - Nat.primeCounting m - N0 ≤
      (missingSet ∩ Set.Icc 1 X).ncard := by
  have := L004_bound_nat hm hN0 X
  omega

/-- **L004, packaged.** If M is nonempty, then with m = min M there is an N0 as in L003 (with
`N0 ≥ 1`) such that `|M ∩ [1, X]| ≥ π(X + m) - π(m) - N0` for every `X`. -/
theorem L004_exists (hM : missingSet.Nonempty) :
    ∃ m N0, IsLeast missingSet m ∧ 1 ≤ N0 ∧
      (∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime) ∧
      ∀ X : ℕ, (Nat.primeCounting (X + m) : ℤ) - Nat.primeCounting m - N0 ≤
        (missingSet ∩ Set.Icc 1 X).ncard := by
  classical
  have hex : ∃ v, v ∈ missingSet := hM
  set m := Nat.find hex
  have hm : IsLeast missingSet m := ⟨Nat.find_spec hex, fun v hv => Nat.find_min' hex hv⟩
  obtain ⟨N0, hN0, h⟩ := L003_smallestMissing hm
  exact ⟨m, N0, hm, hN0, h, L004_bound hm h⟩

/-- **L004, "in particular".** If M is finite, then M is empty. Uses only the infinitude of
primes (`Nat.tendsto_primeCounting`). -/
theorem L004_finite_imp_empty (hfin : missingSet.Finite) : missingSet = ∅ := by
  by_contra hne
  obtain ⟨m, N0, hm, -, hN0, -⟩ := L004_exists (Set.nonempty_iff_ne_empty.2 hne)
  have hev := (Nat.tendsto_primeCounting).eventually_ge_atTop
    (missingSet.ncard + Nat.primeCounting m + N0 + 1)
  obtain ⟨X, hX⟩ := hev.exists
  have h1 := L004_bound_nat hm hN0 X
  have h2 : (missingSet ∩ Set.Icc 1 X).ncard ≤ missingSet.ncard :=
    Set.ncard_le_ncard Set.inter_subset_left hfin
  have h3 : Nat.primeCounting X ≤ Nat.primeCounting (X + m) :=
    Nat.monotone_primeCounting (by omega)
  omega

/-! ### Asymptotics (via Mathlib's prime number theorem) -/

/-- The prime number theorem along the naturals: `π(n) ~ n / log n`. -/
theorem primeCounting_isEquivalent_nat :
    (fun n : ℕ => (Nat.primeCounting n : ℝ)) ~[atTop] fun n : ℕ => (n : ℝ) / Real.log n := by
  have h := Nat.isEquivalent_primeCounting.comp_tendsto tendsto_natCast_atTop_atTop
  simpa [Function.comp_def] using h

/-- `n / log n → ∞` along the naturals (from the PNT and `π n → ∞`). -/
theorem tendsto_div_log_nat :
    Tendsto (fun n : ℕ => (n : ℝ) / Real.log n) atTop atTop :=
  primeCounting_isEquivalent_nat.tendsto_atTop
    (tendsto_natCast_atTop_atTop.comp Nat.tendsto_primeCounting)

/-- `π(X + m) - π(m) - N0 ~ X / log X` as `X → ∞` (for fixed `m`, `N0`): the informal
"= (1 - o(1)) X / log X". -/
theorem L004_rhs_isEquivalent (m N0 : ℕ) :
    (fun X : ℕ => (Nat.primeCounting (X + m) : ℝ) - Nat.primeCounting m - N0) ~[atTop]
      fun X : ℕ => (X : ℝ) / Real.log X := by
  -- write the left side as π X + c X with c bounded
  set c : ℕ → ℝ := fun X =>
    (Nat.primeCounting (X + m) : ℝ) - Nat.primeCounting X - Nat.primeCounting m - N0
  have hc : c =O[atTop] (fun _ : ℕ => (1 : ℝ)) := by
    refine IsBigO.of_bound (m + 1 + Nat.primeCounting m + N0) ?_
    filter_upwards [eventually_ge_atTop 1] with X hX
    have hle : Nat.primeCounting (X + m) ≤ Nat.primeCounting X + Nat.totient 1 * (m / 1 + 1) :=
      Nat.primeCounting_add_le (by norm_num) hX m
    have hge : Nat.primeCounting X ≤ Nat.primeCounting (X + m) :=
      Nat.monotone_primeCounting (by omega)
    simp only [Nat.totient_one, Nat.div_one, one_mul] at hle
    have hle' : (Nat.primeCounting (X + m) : ℝ) ≤ Nat.primeCounting X + (m + 1) := by
      exact_mod_cast hle
    have hge' : (Nat.primeCounting X : ℝ) ≤ Nat.primeCounting (X + m) := by exact_mod_cast hge
    have h0 : (0 : ℝ) ≤ Nat.primeCounting m := Nat.cast_nonneg _
    have h0' : (0 : ℝ) ≤ N0 := Nat.cast_nonneg _
    rw [norm_one, mul_one, Real.norm_eq_abs, abs_le]
    simp only [c]
    constructor <;> linarith
  have h1 : (fun _ : ℕ => (1 : ℝ)) =o[atTop] fun X : ℕ => (X : ℝ) / Real.log X := by
    rw [isLittleO_one_left_iff]
    exact tendsto_norm_atTop_atTop.comp tendsto_div_log_nat
  have := primeCounting_isEquivalent_nat.add_isLittleO (hc.trans_isLittleO h1)
  refine this.congr_left (Eventually.of_forall fun X => ?_)
  simp only [Pi.add_apply, c]
  ring

/-- From `u ~ v` with `v ≥ 0`: for every `ε > 0`, eventually `(1 - ε) v ≤ u`. -/
theorem eventually_ge_of_isEquivalent {u v : ℕ → ℝ} (h : u ~[atTop] v)
    (hv : ∀ᶠ n in atTop, 0 ≤ v n) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n in atTop, (1 - ε) * v n ≤ u n := by
  filter_upwards [h.isLittleO.def hε, hv] with n hn hvn
  rw [Pi.sub_apply, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg hvn, abs_le] at hn
  linarith [hn.1]

/-- **L004, asymptotic form.** If M is nonempty, then for every `ε > 0`, eventually
`|M ∩ [1, X]| ≥ (1 - ε) X / log X`, i.e. `|M ∩ [1, X]| ≥ (1 - o(1)) X / log X`. -/
theorem L004_eventually_ge (hM : missingSet.Nonempty) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ X : ℕ in atTop, (1 - ε) * ((X : ℝ) / Real.log X) ≤ (missingSet ∩ Set.Icc 1 X).ncard := by
  obtain ⟨m, N0, -, -, -, hbound⟩ := L004_exists hM
  have hnn : ∀ᶠ X : ℕ in atTop, 0 ≤ (X : ℝ) / Real.log X := by
    filter_upwards [eventually_ge_atTop 1] with X hX
    exact div_nonneg (Nat.cast_nonneg _) (Real.log_nonneg (by exact_mod_cast hX))
  filter_upwards [eventually_ge_of_isEquivalent (L004_rhs_isEquivalent m N0) hnn hε] with X hX
  have hb := hbound X
  have hb' : ((Nat.primeCounting (X + m) : ℤ) - Nat.primeCounting m - N0 : ℤ) ≤
      ((missingSet ∩ Set.Icc 1 X).ncard : ℤ) := hb
  have hb'' : (Nat.primeCounting (X + m) : ℝ) - Nat.primeCounting m - N0 ≤
      ((missingSet ∩ Set.Icc 1 X).ncard : ℝ) := by exact_mod_cast hb'
  linarith

end ErdosWatts
