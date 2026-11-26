import ErdosWatts.L004
import ErdosWatts.L006
import ErdosWatts.L009
import ErdosWatts.L011

/-!
# C013 - Permanent holes block their whole parity class; (G) implies the permutation property

Informal: lemmas/candidates/C013-blocking-cascade-binary-hypothesis.md (a candidate, not yet in
`lemmas/proven/`; formalized on Matteo's request as a mechanical check).

Notation (C013): P = primes; "m occurs" = `Occurs m`; for real Y >= 1 and integer h >= 1,
r_Y(h) = #{p ∈ P : p <= Y, h + p ∈ P}; for real Z, Y and integer c >= 0,
Bad_c(Z, Y) = {h ∈ [1, Z] : h even, r_Y(h) <= c}.

* **(a)** If S is a nonempty finite set of positive integers none of which occurs, then
  #{k >= 1 : a(k) + m ∈ P for some m ∈ S} <= max S - 1. In particular (S = {m0}): if m0 never
  occurs, at most m0 - 1 primes p > m0 have p - m0 occurring.
* **(b)** There is an absolute constant C0 with a(n) <= C0 n log n for every n >= 2.
* **(c)** If m0 never occurs, then for every integer N >= 1, real Y >= 1 and real
  Z >= max_{k <= N} a(k): |Bad_{2m0}(Z, Y)| >= (N - 1)/2 - Y - m0 + 1.
* **(d)** Under (G) (see `G_hyp`), every positive integer occurs.

## Mapping informal -> formal

* informal a(n) = `a n` for `n ≥ 1`; "m occurs" = `Occurs m`; P = `Nat.Prime`; log = `Real.log`.
* r_Y(h) = `rY Y h` (`Y : ℝ`, `h : ℕ`), counting primes `p ≤ ⌊Y⌋₊` (equivalent to `p ≤ Y`).
* Bad_c(Z, Y) = `Bad c Z Y : Finset ℕ` (`Z Y : ℝ`), the even `h ∈ [1, ⌊Z⌋₊]` (= integers
  `1 ≤ h ≤ Z`) with `rY Y h ≤ c`.
* (G) = `G_hyp : Prop`. **(G) is an explicit hypothesis of `C013_d`, not an axiom and not proved.**
  Z_j, Y_j are real sequences indexed by `j : ℕ` ("sequences" in C013); "Z_j → ∞" is
  `Tendsto Z atTop atTop`; the two limits are `Tendsto ... atTop (𝓝 0)`. Real (not natural)
  Z, Y are used because C013's Notation takes them real and the canonical instance
  Y = Z/(log Z)^2 is not an integer.
* (a) = `C013_a` (finiteness plus `Set.ncard ≤ S.max' - 1`), Finset core `blocking_finset`;
  S = {m0} = `C013_a_single` (Finset core `blocking_single_finset`).
* (b) = `C013_b` (with `20 ≤ C0` added, as in the informal choice C0 = max(20, ...)).
  Growth step `growth_step`: a(n+1) <= a(n)/3 + 13 n log n for n >= n1 (n1 >= 10).
  It uses L006 (b) and (c) (interval form) and O*(n) <= n/2 from `L006.lean`, and the PNT form
  `pnt_three_quarters`: π(x) - π(⌊3x/4⌋) >= x/(5 log x) for all *integers* x >= x2, derived from
  Mathlib's `Nat.isEquivalent_primeCounting` (no hypothesis).
* (c) = `C013_c` (with the hypothesis `1 ≤ m0`, implicit in the informal "positive integer";
  "Z >= max_{k <= N} a(k)" is `∀ k, 1 ≤ k → k ≤ N → a k ≤ Z`). `C013_c_core` is the
  sharper bound `(N - 1)/2 - Y - m0 + 2` of Step 4, without `N ≥ 1`.
* (d) = `C013_d : G_hyp → ∀ v, 1 ≤ v → Occurs v` ("every positive integer occurs"; equivalent
  to `Function.Bijective aPNat` by `aPNat_bijective_iff`).
* (d') is not formalized.
-/

namespace ErdosWatts

open Finset Filter Topology Asymptotics

/-! ### Definitions: r_Y(h), Bad_c(Z, Y), hypothesis (G) -/

/-- r_Y(h) := #{ p prime : p ≤ Y, h + p prime } (C013, Notation), for real `Y` and natural `h`.
For a prime `p ∈ ℕ`, `(p : ℝ) ≤ Y ↔ p ≤ ⌊Y⌋₊` (for `Y ≥ 0`; for `Y < 0` both sides count no prime),
so the count is over `p ∈ [0, ⌊Y⌋₊]`. -/
noncomputable def rY (Y : ℝ) (h : ℕ) : ℕ :=
  ((range (⌊Y⌋₊ + 1)).filter (fun p => p.Prime ∧ (h + p).Prime)).card

/-- Bad_c(Z, Y) := { h ∈ [1, Z] : h even, r_Y(h) ≤ c } (C013, Notation), for real `Z`, `Y` and
natural `c`. Integers `h ≥ 1` with `(h : ℝ) ≤ Z` are exactly `h ∈ [1, ⌊Z⌋₊]`. -/
noncomputable def Bad (c : ℕ) (Z Y : ℝ) : Finset ℕ :=
  (Icc 1 ⌊Z⌋₊).filter (fun h => Even h ∧ rY Y h ≤ c)

/-- **Hypothesis (G)** (C013 (d)), a binary Goldbach-type hypothesis, NOT proved here (its
proposed proof, candidate C014, uses the circle method, which is not in Mathlib):

for every integer `c ≥ 0` there are real sequences `Z_j → ∞` and `Y_j ≥ 1` such that
`Y_j log Z_j / Z_j → 0` and `|Bad_c(Z_j, Y_j)| log Z_j / Z_j → 0` (as `j → ∞`).

Sequences are indexed by `j : ℕ`; `Z_j`, `Y_j` are real (as in C013's Notation). -/
def G_hyp : Prop :=
  ∀ c : ℕ, ∃ Z Y : ℕ → ℝ, Tendsto Z atTop atTop ∧ (∀ j, 1 ≤ Y j) ∧
    Tendsto (fun j => Y j * Real.log (Z j) / Z j) atTop (𝓝 0) ∧
    Tendsto (fun j => ((Bad c (Z j) (Y j)).card : ℝ) * Real.log (Z j) / Z j) atTop (𝓝 0)

theorem mem_range_floor_iff {p : ℕ} {Y : ℝ} (hY : 0 ≤ Y) : p ∈ range (⌊Y⌋₊ + 1) ↔ (p : ℝ) ≤ Y := by
  rw [mem_range, Nat.lt_succ_iff, Nat.le_floor_iff hY]

/-! ### (a) Blocking lemma -/

/-- **(a), core (Finset form, with an arbitrary upper bound `M` for `S`).** Let `S` be a finite
set of positive integers none of which occurs, all `≤ M`. Then every finite set `K` of indices
`k ≥ 1` such that `a k + m` is prime for some `m ∈ S` has at most `M - 1` elements.
Proof: `k ↦ a (k+1)` maps `K` injectively into `[1, M - 1]`. -/
theorem blocking_finset {S : Finset ℕ} {M : ℕ} (hS : ∀ m ∈ S, 1 ≤ m ∧ ¬ Occurs m ∧ m ≤ M)
    {K : Finset ℕ} (hK : ∀ k ∈ K, 1 ≤ k ∧ ∃ m ∈ S, (a k + m).Prime) : K.card ≤ M - 1 := by
  have hmap : ∀ k ∈ K, a (k + 1) ∈ Icc 1 (M - 1) := by
    intro k hk
    obtain ⟨hk1, m, hmS, hp⟩ := hK k hk
    obtain ⟨hm1, hmocc, hmM⟩ := hS m hmS
    have hle := a_succ_min hk1 hm1 (notMem_U_of_not_occurs hmocc k) hp
    have hne : a (k + 1) ≠ m := fun h => hmocc ⟨k + 1, by omega, h⟩
    have hpos := (a_succ_spec hk1).1
    exact mem_Icc.2 ⟨hpos, by omega⟩
  have hinj : Set.InjOn (fun k => a (k + 1)) (K : Set ℕ) := by
    intro i _ j _ h
    have := a_inj (by omega : 1 ≤ i + 1) (by omega : 1 ≤ j + 1) h
    omega
  calc K.card = (K.image (fun k => a (k + 1))).card := (card_image_of_injOn hinj).symm
    _ ≤ (Icc 1 (M - 1)).card := card_le_card (fun x hx => by
        obtain ⟨k, hk, rfl⟩ := mem_image.1 hx; exact hmap k hk)
    _ = M - 1 := by simp

/-- **C013 (a), blocking lemma.** Let `S` be a nonempty finite set of positive integers, none of
which occurs. Then the set `{k ≥ 1 : a(k) + m ∈ P for some m ∈ S}` is finite and has at most
`max S - 1` elements. -/
theorem C013_a {S : Finset ℕ} (hSne : S.Nonempty) (hS : ∀ m ∈ S, 1 ≤ m ∧ ¬ Occurs m) :
    {k : ℕ | 1 ≤ k ∧ ∃ m ∈ S, (a k + m).Prime}.Finite ∧
      {k : ℕ | 1 ≤ k ∧ ∃ m ∈ S, (a k + m).Prime}.ncard ≤ S.max' hSne - 1 := by
  set Kset := {k : ℕ | 1 ≤ k ∧ ∃ m ∈ S, (a k + m).Prime}
  have hS' : ∀ m ∈ S, 1 ≤ m ∧ ¬ Occurs m ∧ m ≤ S.max' hSne :=
    fun m hm => ⟨(hS m hm).1, (hS m hm).2, S.le_max' m hm⟩
  have hmaps : ∀ k ∈ Kset, a (k + 1) ∈ (Icc 1 (S.max' hSne - 1) : Set ℕ) := by
    intro k hk
    obtain ⟨hk1, m, hmS, hp⟩ := hk
    obtain ⟨hm1, hmocc, hmM⟩ := hS' m hmS
    have hle := a_succ_min hk1 hm1 (notMem_U_of_not_occurs hmocc k) hp
    have hne : a (k + 1) ≠ m := fun h => hmocc ⟨k + 1, by omega, h⟩
    have hpos := (a_succ_spec hk1).1
    simp only [coe_Icc, Set.mem_Icc]; omega
  have hinj : Set.InjOn (fun k => a (k + 1)) Kset := by
    intro i _ j _ h
    have := a_inj (by omega : 1 ≤ i + 1) (by omega : 1 ≤ j + 1) h
    omega
  have hfin : Kset.Finite :=
    Set.Finite.of_finite_image ((Icc 1 (S.max' hSne - 1)).finite_toSet.subset
      (Set.image_subset_iff.2 hmaps)) hinj
  refine ⟨hfin, ?_⟩
  calc Kset.ncard ≤ (Icc 1 (S.max' hSne - 1) : Set ℕ).ncard :=
        Set.ncard_le_ncard_of_injOn _ hmaps hinj (Icc 1 _).finite_toSet
    _ = S.max' hSne - 1 := by rw [Set.ncard_coe_finset]; simp

/-- **(a) with S = {m0}, Finset form.** If `m0 ≥ 1` never occurs, every finite set of primes
`p > m0` with `p - m0` occurring has at most `m0 - 1` elements. -/
theorem blocking_single_finset {m0 : ℕ} (hm1 : 1 ≤ m0) (hm0 : ¬ Occurs m0) {P : Finset ℕ}
    (hP : ∀ p ∈ P, p.Prime ∧ m0 < p ∧ Occurs (p - m0)) : P.card ≤ m0 - 1 := by
  classical
  have hK : ∀ k ∈ P.image (fun p => if h : Occurs (p - m0) then fi (p - m0) h else 0),
      1 ≤ k ∧ ∃ m ∈ ({m0} : Finset ℕ), (a k + m).Prime := by
    intro k hk
    obtain ⟨p, hp, rfl⟩ := mem_image.1 hk
    obtain ⟨hpp, hpm, hocc⟩ := hP p hp
    simp only [hocc, ↓reduceDIte, mem_singleton, exists_eq_left, a_fi]
    exact ⟨one_le_fi hocc, by rw [show p - m0 + m0 = p by omega]; exact hpp⟩
  have hinj : Set.InjOn (fun p => if h : Occurs (p - m0) then fi (p - m0) h else 0) (P : Set ℕ) := by
    intro p hp q hq h
    obtain ⟨-, hpm, hpo⟩ := hP p hp
    obtain ⟨-, hqm, hqo⟩ := hP q hq
    simp only [hpo, hqo, ↓reduceDIte] at h
    have h2 : a (fi (p - m0) hpo) = a (fi (q - m0) hqo) := by rw [h]
    simp only [a_fi] at h2
    omega
  rw [← card_image_of_injOn hinj]
  exact blocking_finset (S := {m0}) (M := m0) (by simpa using ⟨hm1, hm0⟩) hK

/-- **C013 (a), "in particular" (S = {m0}).** If `m0 ≥ 1` never occurs, then the set of primes
`p > m0` with `p - m0` occurring is finite with at most `m0 - 1` elements. -/
theorem C013_a_single {m0 : ℕ} (hm1 : 1 ≤ m0) (hm0 : ¬ Occurs m0) :
    {p : ℕ | p.Prime ∧ m0 < p ∧ Occurs (p - m0)}.Finite ∧
      {p : ℕ | p.Prime ∧ m0 < p ∧ Occurs (p - m0)}.ncard ≤ m0 - 1 := by
  set Pset := {p : ℕ | p.Prime ∧ m0 < p ∧ Occurs (p - m0)}
  have hbound : ∀ P : Finset ℕ, (P : Set ℕ) ⊆ Pset → P.card ≤ m0 - 1 :=
    fun P hP => blocking_single_finset hm1 hm0 (fun p hp => hP hp)
  have hfin : Pset.Finite := by
    by_contra hinf
    obtain ⟨P, hP, hcard⟩ := Set.Infinite.exists_subset_card_eq hinf m0
    have := hbound P hP
    omega
  refine ⟨hfin, ?_⟩
  rw [Set.ncard_eq_toFinset_card _ hfin]
  exact hbound _ (by simp)

/-! ### (c) A missing value forces a large exceptional set -/

/-- **(c), core** (no hypothesis `N ≥ 1`; for `N = 0` the bound is trivially true). -/
theorem C013_c_core {m0 : ℕ} (hm1 : 1 ≤ m0) (hm0 : ¬ Occurs m0) (N : ℕ) {Y Z : ℝ}
    (hY : 1 ≤ Y) (hZ : ∀ k, 1 ≤ k → k ≤ N → (a k : ℝ) ≤ Z) :
    ((N : ℝ) - 1) / 2 - Y - m0 + 2 ≤ (Bad (2 * m0) Z Y).card := by
  classical
  have hm2 : 2 ≤ m0 := two_le_of_not_occurs hm1 hm0
  set Yn := ⌊Y⌋₊ with hYn
  have hYn1 : 1 ≤ Yn := Nat.le_floor (by exact_mod_cast hY)
  have hYnY : (Yn : ℝ) ≤ Y := Nat.floor_le (by linarith)
  set ε := m0 % 2
  -- Step 1: the blocking set S and K_S (restricted to [1, N])
  set S : Finset ℕ := ((Ioc m0 Yn).filter (fun p => p.Prime ∧ ¬ Occurs (p - m0))).image
    (fun p => p - m0) with hSdef
  have hS : ∀ m ∈ S, 1 ≤ m ∧ ¬ Occurs m ∧ m ≤ Yn - m0 := by
    intro m hm
    obtain ⟨p, hp, rfl⟩ := mem_image.1 hm
    simp only [mem_filter, mem_Ioc] at hp
    exact ⟨by omega, hp.2.2, by omega⟩
  set K := (Icc 1 N).filter (fun k => ∃ m ∈ S, (a k + m).Prime) with hKdef
  have hKcard : K.card ≤ Yn - m0 - 1 := blocking_finset hS (fun k hk => by
    simp only [hKdef, mem_filter, mem_Icc] at hk; exact ⟨hk.1.1, hk.2⟩)
  -- Step 2: the times of parity ε
  set T := (Icc 1 N).filter (fun k => k % 2 = ε) with hTdef
  have hTcard : N ≤ 2 * T.card + 1 := by
    rcases Nat.mod_two_eq_zero_or_one m0 with h | h
    · have := card_Icc_filter_even N
      simp only [hTdef, ε, h]; omega
    · have := card_Icc_filter_odd N
      simp only [hTdef, ε, h]; omega
  set T' := T.filter (fun k => k ∉ K ∧ m0 < a k) with hT'def
  set L := (Icc 1 N).filter (fun k => a k ≤ m0) with hLdef
  have hLcard : L.card ≤ m0 - 1 := by
    have hinj : Set.InjOn a (L : Set ℕ) := fun i hi j hj h => a_inj
      (by simp [hLdef] at hi; omega) (by simp [hLdef] at hj; omega) h
    rw [← card_image_of_injOn hinj]
    calc (L.image a).card ≤ (Icc 1 (m0 - 1)).card := card_le_card (fun x hx => by
          obtain ⟨k, hk, rfl⟩ := mem_image.1 hx
          simp only [hLdef, mem_filter, mem_Icc] at hk
          have hpos := a_pos hk.1.1
          have hne : a k ≠ m0 := fun h => hm0 ⟨k, hk.1.1, h⟩
          exact mem_Icc.2 ⟨hpos, by omega⟩)
      _ = m0 - 1 := by simp
  have hT'card : T.card ≤ T'.card + K.card + L.card := by
    have hsub : T ⊆ T' ∪ K ∪ L := by
      intro k hk
      simp only [hTdef, hT'def, hKdef, hLdef, mem_union, mem_filter] at hk ⊢
      by_cases h1 : ∃ m ∈ S, (a k + m).Prime
      · exact Or.inl (Or.inr ⟨hk.1, h1⟩)
      · by_cases h2 : m0 < a k
        · exact Or.inl (Or.inl ⟨hk, fun h => h1 h.2, h2⟩)
        · exact Or.inr ⟨hk.1, by omega⟩
    exact (card_le_card hsub).trans ((card_union_le _ _).trans
      (by have := card_union_le T' K; omega))
  -- Step 3: each k ∈ T' gives an element h = a k - m0 of Bad_{2 m0}(Z, Y)
  have hstep : ∀ k ∈ T', a k - m0 ∈ Bad (2 * m0) Z Y := by
    intro k hk
    simp only [hT'def, hTdef, mem_filter, mem_Icc] at hk
    obtain ⟨⟨⟨hk1, hkN⟩, hkpar⟩, hkK, hkm⟩ := hk
    have hak := a_mod_two hk1
    have haZ : (a k : ℝ) ≤ Z := hZ k hk1 hkN
    have hhZ : a k - m0 ≤ ⌊Z⌋₊ := by
      have : a k ≤ ⌊Z⌋₊ := Nat.le_floor haZ
      omega
    refine mem_filter.2 ⟨mem_Icc.2 ⟨by omega, hhZ⟩, ?_, ?_⟩
    · rw [Nat.even_iff]; omega
    · -- r_Y(h) ≤ 2 m0 - 2
      set R := (range (Yn + 1)).filter (fun p => p.Prime ∧ (a k - m0 + p).Prime)
      have hsplit : R ⊆ (Icc 2 m0) ∪ R.filter (fun p => m0 < p) := by
        intro p hp
        simp only [R, mem_filter, mem_union, mem_Icc] at hp ⊢
        by_cases h : m0 < p
        · exact Or.inr ⟨hp, h⟩
        · exact Or.inl ⟨hp.2.1.two_le, by omega⟩
      have hbig : (R.filter (fun p => m0 < p)).card ≤ m0 - 1 := by
        refine blocking_single_finset hm1 hm0 (fun p hp => ?_)
        simp only [R, mem_filter, mem_range] at hp
        obtain ⟨⟨hpY, hpp, hhp⟩, hpm⟩ := hp
        refine ⟨hpp, hpm, ?_⟩
        by_contra hocc
        apply hkK
        simp only [hKdef, mem_filter, mem_Icc]
        refine ⟨⟨hk1, hkN⟩, p - m0, ?_, ?_⟩
        · exact mem_image.2 ⟨p, by simp only [mem_filter, mem_Ioc]; exact ⟨⟨hpm, by omega⟩, hpp, hocc⟩, rfl⟩
        · rw [show a k + (p - m0) = a k - m0 + p by omega]; exact hhp
      have := (card_le_card hsplit).trans (card_union_le _ _)
      simp only [Nat.card_Icc] at this
      show R.card ≤ 2 * m0
      omega
  -- Step 4: count
  have hinj : Set.InjOn (fun k => a k - m0) (T' : Set ℕ) := by
    intro i hi j hj h
    simp only [hT'def, hTdef, coe_filter, mem_filter, mem_Icc, Set.mem_ofPred_eq] at hi hj
    simp only at h
    exact a_inj hi.1.1.1 hj.1.1.1 (by omega)
  have hcard : T'.card ≤ (Bad (2 * m0) Z Y).card := by
    rw [← card_image_of_injOn hinj]
    exact card_le_card (fun x hx => by obtain ⟨k, hk, rfl⟩ := mem_image.1 hx; exact hstep k hk)
  -- arithmetic
  have hK' : (K.card : ℝ) ≤ Y - 1 := by
    have : K.card ≤ Yn - 1 := by omega
    have : (K.card : ℝ) ≤ (Yn : ℝ) - 1 := by
      have h' : K.card + 1 ≤ Yn := by omega
      have : ((K.card + 1 : ℕ) : ℝ) ≤ Yn := by exact_mod_cast h'
      push_cast at this; linarith
    linarith
  have hL' : (L.card : ℝ) ≤ m0 - 1 := by
    have h' : L.card + 1 ≤ m0 := by omega
    have : ((L.card + 1 : ℕ) : ℝ) ≤ m0 := by exact_mod_cast h'
    push_cast at this; linarith
  have hT1 : (N : ℝ) ≤ 2 * T.card + 1 := by exact_mod_cast hTcard
  have hT2 : (T.card : ℝ) ≤ T'.card + K.card + L.card := by exact_mod_cast hT'card
  have hT3 : (T'.card : ℝ) ≤ (Bad (2 * m0) Z Y).card := by exact_mod_cast hcard
  linarith

/-- **C013 (c).** Suppose `m0` (a positive integer) never occurs. Then for every integer
`N ≥ 1`, every real `Y ≥ 1` and every real `Z ≥ max_{1 ≤ k ≤ N} a(k)`:
`|Bad_{2 m0}(Z, Y)| ≥ (N - 1)/2 - Y - m0 + 1`. -/
theorem C013_c {m0 : ℕ} (hm1 : 1 ≤ m0) (hm0 : ¬ Occurs m0) {N : ℕ} (_hN : 1 ≤ N) {Y Z : ℝ}
    (hY : 1 ≤ Y) (hZ : ∀ k, 1 ≤ k → k ≤ N → (a k : ℝ) ≤ Z) :
    ((N : ℝ) - 1) / 2 - Y - m0 + 1 ≤ (Bad (2 * m0) Z Y).card := by
  have := C013_c_core hm1 hm0 N hY hZ
  linarith

/-! ### PNT form used in (b): π(x) - π(3x/4) ≥ x / (5 log x) for large x -/

theorem le_log_of_three_pow_le {k : ℕ} {x : ℝ} (h : (3 : ℝ) ^ k ≤ x) : (k : ℝ) ≤ Real.log x := by
  have h3 : (1 : ℝ) ≤ Real.log 3 := by
    rw [Real.le_log_iff_exp_le (by norm_num)]; exact Real.exp_one_lt_three.le
  calc (k : ℝ) ≤ k * Real.log 3 := by nlinarith [show (0 : ℝ) ≤ k from Nat.cast_nonneg k]
    _ = Real.log ((3 : ℝ) ^ k) := by rw [Real.log_pow]
    _ ≤ Real.log x := Real.log_le_log (by positivity) h

/-- `x / log x` is monotone on `[e, ∞)` (from Mathlib's `Real.log_div_self_antitoneOn`). -/
theorem div_log_le_div_log {x y : ℝ} (hx : Real.exp 1 ≤ x) (hxy : x ≤ y) :
    x / Real.log x ≤ y / Real.log y := by
  have hx0 : 0 < x := lt_of_lt_of_le (Real.exp_pos 1) hx
  have hy0 : 0 < y := by linarith
  have hlx : 1 ≤ Real.log x := by rw [Real.le_log_iff_exp_le hx0]; exact hx
  have hly : 1 ≤ Real.log y := by rw [Real.le_log_iff_exp_le hy0]; linarith
  have hanti := Real.log_div_self_antitoneOn hx (show Real.exp 1 ≤ y by linarith) hxy
  simp only at hanti
  rw [div_le_div_iff₀ (by linarith) (by linarith)]
  rw [div_le_div_iff₀ hy0 hx0] at hanti
  nlinarith

/-- From `u ~ v` with `v ≥ 0`: for every `ε > 0`, eventually `u ≤ (1 + ε) v`. -/
theorem eventually_le_of_isEquivalent {u v : ℕ → ℝ} (h : u ~[atTop] v)
    (hv : ∀ᶠ n in atTop, 0 ≤ v n) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n in atTop, u n ≤ (1 + ε) * v n := by
  filter_upwards [h.isLittleO.def hε, hv] with n hn hvn
  rw [Pi.sub_apply, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg hvn, abs_le] at hn
  linarith [hn.2]

/-- **PNT form used in C013 (b).** There is `x2` such that for every integer `x ≥ x2`,
`π(x) - π(3x/4) ≥ x / (5 log x)`. Here `π(3x/4)` is `π ⌊3x/4⌋ = Nat.primeCounting (3 * x / 4)`.
Derived from Mathlib's prime number theorem `Nat.isEquivalent_primeCounting` (via
`primeCounting_isEquivalent_nat`, L004.lean). Restricting to integer `x` suffices for (b). -/
theorem pnt_three_quarters : ∃ x2 : ℕ, ∀ x : ℕ, x2 ≤ x →
    (x : ℝ) / (5 * Real.log x) ≤ (Nat.primeCounting x : ℝ) - Nat.primeCounting (3 * x / 4) := by
  have hnn : ∀ᶠ X : ℕ in atTop, 0 ≤ (X : ℝ) / Real.log X := by
    filter_upwards [eventually_ge_atTop 1] with X hX
    exact div_nonneg (Nat.cast_nonneg _) (Real.log_nonneg (by exact_mod_cast hX))
  obtain ⟨A, hA⟩ := eventually_atTop.1 (eventually_ge_of_isEquivalent
    primeCounting_isEquivalent_nat hnn (show (0 : ℝ) < 1 / 100 by norm_num))
  obtain ⟨B, hB⟩ := eventually_atTop.1 (eventually_le_of_isEquivalent
    primeCounting_isEquivalent_nat hnn (show (0 : ℝ) < 1 / 100 by norm_num))
  refine ⟨max A (4 * B + 4 + 3 ^ 9 * 4), fun x hx => ?_⟩
  have hxA : A ≤ x := le_of_max_le_left hx
  have hxB : 4 * B + 4 + 3 ^ 9 * 4 ≤ x := le_of_max_le_right hx
  have hyB : B ≤ 3 * x / 4 := by omega
  have hy3 : 3 ≤ 3 * x / 4 := by omega
  have hx9 : (3 : ℝ) ^ 9 ≤ x := by exact_mod_cast (by omega : 3 ^ 9 ≤ x)
  have hL : (9 : ℝ) ≤ Real.log x := by exact_mod_cast le_log_of_three_pow_le hx9
  have hx0 : (0 : ℝ) < x := by linarith [show (0 : ℝ) < 3 ^ 9 by norm_num]
  have h1 := hA x hxA
  have h2 := hB (3 * x / 4) hyB
  have hyle : ((3 * x / 4 : ℕ) : ℝ) ≤ 3 * (x : ℝ) / 4 := by
    have : 4 * (3 * x / 4) ≤ 3 * x := by omega
    have : ((4 * (3 * x / 4) : ℕ) : ℝ) ≤ ((3 * x : ℕ) : ℝ) := by exact_mod_cast this
    push_cast at this; linarith
  have hye : Real.exp 1 ≤ ((3 * x / 4 : ℕ) : ℝ) := by
    have : (3 : ℝ) ≤ ((3 * x / 4 : ℕ) : ℝ) := by exact_mod_cast hy3
    linarith [Real.exp_one_lt_three]
  have h3 := div_log_le_div_log hye hyle
  have hlog34 : Real.log x - 1 / 3 ≤ Real.log (3 * x / 4) := by
    have : Real.log (3 * (x : ℝ) / 4) = Real.log x + Real.log (3 / 4) := by
      rw [show (3 * (x : ℝ) / 4) = x * (3 / 4) by ring, Real.log_mul hx0.ne' (by norm_num)]
    have h34 : 1 - (3 / 4 : ℝ)⁻¹ ≤ Real.log (3 / 4) := Real.one_sub_inv_le_log_of_pos (by norm_num)
    norm_num at h34
    linarith
  have h4 : (3 * (x : ℝ) / 4) / Real.log (3 * x / 4) ≤ (3 * x / 4) / (Real.log x - 1 / 3) :=
    div_le_div_of_nonneg_left (by positivity) (by linarith) hlog34
  have hkey : (1 + 1 / 100) * ((3 * (x : ℝ) / 4) / (Real.log x - 1 / 3)) ≤
      (79 / 100) * (x / Real.log x) := by
    have hL0 : 0 < Real.log x := by linarith
    have hL1 : 0 < Real.log x - 1 / 3 := by linarith
    rw [show (1 + 1 / 100) * ((3 * (x : ℝ) / 4) / (Real.log x - 1 / 3)) =
      (x : ℝ) * ((303 / 400) / (Real.log x - 1 / 3)) by ring]
    rw [show (79 / 100) * ((x : ℝ) / Real.log x) = (x : ℝ) * ((79 / 100) / Real.log x) by ring]
    apply mul_le_mul_of_nonneg_left _ hx0.le
    rw [div_le_div_iff₀ hL1 hL0]
    nlinarith
  have h5 : (x : ℝ) / (5 * Real.log x) = (1 / 5) * (x / Real.log x) := by
    rw [div_mul_eq_div_div_swap]; ring
  rw [h5]
  nlinarith

/-! ### (b) Growth: a(n) ≤ C0 n log n -/

/-- **(b), growth step.** There is `n1 ≥ 10` with `a(n+1) ≤ a(n)/3 + 13 n log n` for `n ≥ n1`.
Uses L006 (b) (`L006_b`), L006 (c) in interval form (`L006_c`), O*(n) ≤ n/2
(`Ostar_le_half`) and the PNT form `pnt_three_quarters`. -/
theorem growth_step : ∃ n1 : ℕ, 10 ≤ n1 ∧ ∀ n, n1 ≤ n →
    (a (n + 1) : ℝ) ≤ a n / 3 + 13 * n * Real.log n := by
  obtain ⟨x2, hx2⟩ := pnt_three_quarters
  refine ⟨max 10 x2, le_max_left _ _, fun n hn => ?_⟩
  have hn10 : 10 ≤ n := le_of_max_le_left hn
  have hnx2 : x2 ≤ n := le_of_max_le_right hn
  have hn1 : 1 ≤ n := by omega
  have hnR : (10 : ℝ) ≤ n := by exact_mod_cast hn10
  have hn0 : (0 : ℝ) < n := by linarith
  have hlogn : (2 : ℝ) ≤ Real.log n := by
    have := le_log_of_three_pow_le (k := 2) (x := n) (by norm_num; linarith)
    exact_mod_cast this
  set D : ℝ := 12 * n * Real.log n with hD
  have htle : tStar n ≤ a n + n + 1 := by have := L006_b n; unfold tStar; omega
  set t := tStar n with ht
  set Dn := ⌈D⌉₊ with hDn
  set d := t / 3 + 1 + Dn with hd
  set x := t + d with hx
  have hDle : D ≤ Dn := Nat.le_ceil D
  have hDn1 : (Dn : ℝ) < D + 1 := Nat.ceil_lt_add_one (by positivity)
  have hDge : 24 * (n : ℝ) ≤ D := by rw [hD]; nlinarith
  have hxD : D ≤ (x : ℝ) := by
    have : Dn ≤ x := by omega
    have : (Dn : ℝ) ≤ x := by exact_mod_cast this
    linarith
  have hx2x : x2 ≤ x := by
    have : (x2 : ℝ) ≤ x := by
      have : (x2 : ℝ) ≤ n := by exact_mod_cast hnx2
      linarith
    exact_mod_cast this
  have hpnt := hx2 x hx2x
  -- primes in (3x/4, x] lie in [t, t + d], since 3d ≥ t
  have hsub : (Ioc (3 * x / 4) x).filter Nat.Prime ⊆ (Icc t (t + d)).filter Nat.Prime := by
    intro p hp
    simp only [mem_filter, mem_Ioc, mem_Icc] at hp ⊢
    exact ⟨⟨by omega, by omega⟩, hp.2⟩
  have hcount : (Nat.primeCounting x : ℝ) - Nat.primeCounting (3 * x / 4) ≤
      ((Icc t (t + d)).filter Nat.Prime).card := by
    have h1 := primeCounting_sub_eq_card (show 3 * x / 4 ≤ x by omega)
    have h2 := Nat.monotone_primeCounting (show 3 * x / 4 ≤ x by omega)
    have h3 := card_le_card hsub
    have : Nat.primeCounting x ≤
        Nat.primeCounting (3 * x / 4) + ((Icc t (t + d)).filter Nat.Prime).card := by omega
    have : (Nat.primeCounting x : ℝ) ≤
        Nat.primeCounting (3 * x / 4) + ((Icc t (t + d)).filter Nat.Prime).card := by
      exact_mod_cast this
    linarith
  -- x/(5 log x) ≥ D/(5 log D) ≥ 0.6 n
  have hDe : Real.exp 1 ≤ D := by linarith [Real.exp_one_lt_three]
  have hmono := div_log_le_div_log hDe hxD
  have hD0 : 0 < D := by linarith
  have hlogD : Real.log D ≤ 4 * Real.log n := by
    have hlog_le : Real.log n ≤ n := by have := Real.log_le_sub_one_of_pos hn0; linarith
    have : D ≤ (n : ℝ) ^ 4 := by
      have h12 : D ≤ 12 * n * n := by rw [hD]; nlinarith
      have : 12 * (n : ℝ) * n ≤ n ^ 4 := by nlinarith
      linarith
    calc Real.log D ≤ Real.log ((n : ℝ) ^ 4) := Real.log_le_log hD0 this
      _ = 4 * Real.log n := by rw [Real.log_pow]; norm_num
  have hlogD0 : 0 < Real.log D := by
    have : (1 : ℝ) ≤ Real.log D := by rw [Real.le_log_iff_exp_le hD0]; exact hDe
    linarith
  have h06 : (6 / 10) * (n : ℝ) ≤ D / Real.log D / 5 := by
    rw [div_div, le_div_iff₀ (by positivity)]
    rw [hD]; nlinarith
  have hfive : ∀ z : ℝ, z / (5 * Real.log z) = z / Real.log z / 5 := fun z => by
    rw [div_div, mul_comm]
  rw [hfive] at hpnt
  -- O*(n) + 1 ≤ #(primes in [t_n, t_n + d])
  have hO : (Ostar n : ℝ) + 1 ≤ ((Icc t (t + d)).filter Nat.Prime).card := by
    have h1 : 2 * Ostar n ≤ n := by have := Ostar_le_half n; omega
    have h2 : (2 * Ostar n : ℝ) ≤ n := by exact_mod_cast h1
    linarith
  have hO' : Ostar n + 1 ≤ ((Icc (tStar n) (tStar n + d)).filter Nat.Prime).card := by
    exact_mod_cast hO
  have hstep := L006_c hn1 d hO'
  -- arithmetic
  have hstepR : (a (n + 1) : ℝ) ≤ n + 1 + (t / 3 : ℕ) + 1 + Dn := by
    have : a (n + 1) ≤ n + 1 + (t / 3 + 1 + Dn) := hstep
    exact_mod_cast (by omega : a (n + 1) ≤ n + 1 + t / 3 + 1 + Dn)
  have ht3 : ((t / 3 : ℕ) : ℝ) ≤ (t : ℝ) / 3 := Nat.cast_div_le
  have htR : (t : ℝ) ≤ a n + n + 1 := by exact_mod_cast htle
  have hnlog : 2 * (n : ℝ) ≤ n * Real.log n := by nlinarith
  rw [hD] at hDn1
  nlinarith

/-- **C013 (b).** There is a constant `C0` (here with `C0 ≥ 20`) such that
`a(n) ≤ C0 n log n` for every `n ≥ 2`. Unconditional (PNT from Mathlib). -/
theorem C013_b : ∃ C0 : ℝ, 20 ≤ C0 ∧ ∀ n : ℕ, 2 ≤ n → (a n : ℝ) ≤ C0 * n * Real.log n := by
  obtain ⟨n1, hn1, hstep⟩ := growth_step
  set C0 := max 20 (∑ n ∈ Icc 2 n1, (a n : ℝ) / (n * Real.log n)) with hC0
  refine ⟨C0, le_max_left _ _, ?_⟩
  have hpos : ∀ n : ℕ, 2 ≤ n → 0 < (n : ℝ) * Real.log n := fun n hn => by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    have : 0 < Real.log n := Real.log_pos (by linarith)
    positivity
  have hbase : ∀ n, 2 ≤ n → n ≤ n1 → (a n : ℝ) ≤ C0 * n * Real.log n := by
    intro n hn hnn1
    have hterm : (a n : ℝ) / (n * Real.log n) ≤ ∑ m ∈ Icc 2 n1, (a m : ℝ) / (m * Real.log m) :=
      single_le_sum (f := fun m => (a m : ℝ) / (m * Real.log m))
        (fun m _ => div_nonneg (Nat.cast_nonneg _)
          (mul_nonneg (Nat.cast_nonneg _) (Real.log_natCast_nonneg _)))
        (mem_Icc.2 ⟨hn, hnn1⟩)
    have := (div_le_iff₀ (hpos n hn)).1 (hterm.trans (le_max_right (20 : ℝ) _))
    rw [mul_assoc]; exact this
  intro n hn
  induction n, hn using Nat.le_induction with
  | base => exact hbase 2 le_rfl (by omega)
  | succ n hn ih =>
    by_cases h : n + 1 ≤ n1
    · exact hbase (n + 1) (by omega) h
    · have hs := hstep n (by omega)
      have hC : (20 : ℝ) ≤ C0 := le_max_left _ _
      have hp := hpos n hn
      have hmono : (n : ℝ) * Real.log n ≤ ((n + 1 : ℕ) : ℝ) * Real.log ((n + 1 : ℕ) : ℝ) := by
        have h1 : (n : ℝ) ≤ ((n + 1 : ℕ) : ℝ) := by exact_mod_cast (by omega : n ≤ n + 1)
        have h2 : Real.log n ≤ Real.log ((n + 1 : ℕ) : ℝ) :=
          Real.log_le_log (by have : (2 : ℝ) ≤ n := by exact_mod_cast hn
                              linarith) h1
        exact mul_le_mul h1 h2 (Real.log_natCast_nonneg n) (by positivity)
      have : (a (n + 1) : ℝ) ≤ C0 * (n * Real.log n) := by nlinarith
      calc (a (n + 1) : ℝ) ≤ C0 * (n * Real.log n) := this
        _ ≤ C0 * (((n + 1 : ℕ) : ℝ) * Real.log ((n + 1 : ℕ) : ℝ)) :=
          mul_le_mul_of_nonneg_left hmono (by linarith)
        _ = C0 * ((n + 1 : ℕ) : ℝ) * Real.log ((n + 1 : ℕ) : ℝ) := by ring

/-! ### (d) Conditional theorem -/

/-- **C013 (d).** Under hypothesis (G) (`G_hyp`, an explicit hypothesis, not proved), every
positive integer occurs in the sequence, i.e. the Watts sequence is a permutation of ℕ⁺
(equivalently `Function.Bijective aPNat`, by `aPNat_bijective_iff`). -/
theorem C013_d : G_hyp → ∀ v, 1 ≤ v → Occurs v := by
  intro hG v hv
  by_contra hmiss
  obtain ⟨C0, hC0, hC0b⟩ := C013_b
  obtain ⟨Z, Y, hZ, hY1, hYlim, hBadlim⟩ := hG (2 * v)
  have hC0pos : 0 < C0 := by linarith
  set δ := 1 / (6 * C0) with hδdef
  have hδ : 0 < δ := by positivity
  have hLZ : Tendsto (fun j => Real.log (Z j) / Z j) atTop (𝓝 0) := by
    have := (Real.tendsto_pow_log_div_mul_add_atTop 1 0 1 one_ne_zero).comp hZ
    simpa [Function.comp_def] using this
  have ev1 : ∀ᶠ j in atTop, Real.exp 1 ≤ Z j := hZ.eventually_ge_atTop _
  have ev2 : ∀ᶠ j in atTop, Y j * Real.log (Z j) / Z j < δ := hYlim.eventually (gt_mem_nhds hδ)
  have ev3 : ∀ᶠ j in atTop, ((Bad (2 * v) (Z j) (Y j)).card : ℝ) * Real.log (Z j) / Z j < δ :=
    hBadlim.eventually (gt_mem_nhds hδ)
  have ev4 : ∀ᶠ j in atTop, (v : ℝ) * (Real.log (Z j) / Z j) < δ := by
    have := hLZ.const_mul (v : ℝ)
    rw [mul_zero] at this
    exact this.eventually (gt_mem_nhds hδ)
  obtain ⟨j, hj1, hj2, hj3, hj4⟩ := (ev1.and (ev2.and (ev3.and ev4))).exists
  set z := Z j with hz
  set y := Y j with hy
  set L := Real.log z with hLdef
  set B := ((Bad (2 * v) z y).card : ℝ) with hB
  have hz0 : 0 < z := lt_of_lt_of_le (Real.exp_pos 1) hj1
  have hL1 : 1 ≤ L := by rw [hLdef, Real.le_log_iff_exp_le hz0]; exact hj1
  have hz1 : 1 ≤ z := by linarith [Real.add_one_le_exp (1 : ℝ)]
  have hCL : 0 < C0 * L := by positivity
  set N := ⌊z / (C0 * L)⌋₊ with hN
  have hNle : (N : ℝ) ≤ z / (C0 * L) := Nat.floor_le (by positivity)
  have hNge : z / (C0 * L) - 1 < N := Nat.sub_one_lt_floor _
  have hNz : (N : ℝ) * (C0 * L) ≤ z := (le_div_iff₀ hCL).1 hNle
  have hzZ : ∀ k, 1 ≤ k → k ≤ N → (a k : ℝ) ≤ z := by
    intro k hk1 hkN
    rcases (show k = 1 ∨ 2 ≤ k by omega) with rfl | hk2
    · simp only [a_one, Nat.cast_one]; exact hz1
    · have hkR : (k : ℝ) ≤ N := by exact_mod_cast hkN
      have hk2R : (2 : ℝ) ≤ k := by exact_mod_cast hk2
      have hNz' : (N : ℝ) ≤ z :=
        (le_mul_of_one_le_right (Nat.cast_nonneg _) (by nlinarith)).trans hNz
      have hlogk : Real.log k ≤ L := Real.log_le_log (by linarith) (by linarith)
      have hlogk0 : 0 ≤ Real.log k := Real.log_natCast_nonneg k
      have := hC0b k hk2
      calc (a k : ℝ) ≤ C0 * k * Real.log k := this
        _ ≤ C0 * N * L := by
          apply mul_le_mul (mul_le_mul_of_nonneg_left hkR hC0pos.le) hlogk hlogk0
          positivity
        _ ≤ z := by nlinarith
  have hc := C013_c_core hv hmiss N (hY1 j) hzZ
  rw [← hB] at hc
  -- B ≥ z/(2 C0 L) - y - v, multiply by L/z
  have hlow : z / (2 * C0 * L) - y - v ≤ B := by
    have : z / (2 * C0 * L) = (z / (C0 * L)) / 2 := by field_simp
    rw [this]; linarith
  have hr : 0 < L / z := by positivity
  have hmul := mul_le_mul_of_nonneg_right hlow hr.le
  have e1 : z / (2 * C0 * L) * (L / z) = 1 / (2 * C0) := by field_simp
  have e2 : (z / (2 * C0 * L) - y - v) * (L / z) =
      1 / (2 * C0) - y * L / z - v * (L / z) := by rw [sub_mul, sub_mul, e1]; ring
  have e3 : B * (L / z) = B * L / z := by ring
  rw [e2, e3] at hmul
  have : 1 / (2 * C0) = 3 * δ := by rw [hδdef]; field_simp; ring
  linarith

end ErdosWatts
