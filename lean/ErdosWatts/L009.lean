import ErdosWatts.Defs
import ErdosWatts.L001

/-!
# L009 - A hole can survive only as many primes as it has "payers"

Informal (lemmas/proven/L009-hole-prime-count.md). Let n >= 2 and 2 <= v <= n with v ∉ U_n,
and put ε = v mod 2. Then

    π(n + v) - π(2v)  <=  1 + B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n),

and (sharp form L009') π(n + v) - π(2v) <= H(v) + H_{1-ε}(n), because
1 + B(v) + H_{1-ε}(v - 1) = H(v) exactly. Corollary: if H(m) <= h for all m <= n, then every
hole v at time n (2 <= v <= n, v ∉ U_n) satisfies n - v < ℓ_{2h+1}(2v).

## Mapping informal -> formal

* informal a(n) = `a n` (n ≥ 1), U_n = `U n`, H_p(m) = `holes p m`, H(m) = `H m`, B(v) = `B v`,
  ε = `v % 2`, 1 - ε = `1 - v % 2` (natural subtraction; `v % 2 ∈ {0, 1}`).
* π = `Nat.primeCounting`. The prime count π(n + v) - π(2v) is used in two equivalent forms:
  `Nat.primeCounting (n + v) - Nat.primeCounting (2 * v)` (natural subtraction, harmless since π
  is monotone and 2v ≤ n + v) and `#{q ∈ (2v, n+v] : q prime}`; the two agree by
  `primeCounting_sub_eq_card`.
* fi-ranges of the partition are written with used sets: fi(w) ≤ m ↔ w ∈ U m
  (`mem_U_iff_fi_le`); the fi-form of each class is `mem_W1_iff_fi` ... `mem_W4_iff_fi`.
* P_K(x) (K-th prime > x) = `primeAfter K x`, ℓ_K(x) = `ell K x` (both in `Defs.lean`);
  `primeAfter_spec` shows `primeAfter K x` is prime, `> x`, with exactly K primes in (x, P_K(x)].
-/

namespace ErdosWatts

open Finset

/-! ### Primes in an interval and the K-th prime after x -/

/-- π(y) - π(x) is the number of primes in (x, y], for x ≤ y. -/
theorem primeCounting_sub_eq_card {x y : ℕ} (h : x ≤ y) :
    Nat.primeCounting y - Nat.primeCounting x = ((Ioc x y).filter Nat.Prime).card := by
  rw [← Nat.primesLE_card_eq_primeCounting, ← Nat.primesLE_card_eq_primeCounting,
    Nat.primesLE_eq_filter_Ioc_zero, Nat.primesLE_eq_filter_Ioc_zero,
    ← Finset.Ioc_union_Ioc_eq_Ioc (Nat.zero_le x) h, Finset.filter_union,
    Finset.card_union_of_disjoint]
  · omega
  · exact Finset.disjoint_filter_filter (Finset.Ioc_disjoint_Ioc_of_le le_rfl)

/-- π(nth prime j) = j + 1 (`Nat.nth Nat.Prime` is 0-indexed). -/
theorem primeCounting_nth_prime (j : ℕ) : Nat.primeCounting (Nat.nth Nat.Prime j) = j + 1 := by
  show Nat.count Nat.Prime (Nat.nth Nat.Prime j + 1) = j + 1
  rw [Nat.count_succ, Nat.count_nth_of_infinite Nat.infinite_setOfPred_prime j]
  simp [Nat.prime_nth_prime j]

/-- Characterization of P_K(x) = `primeAfter K x` for K ≥ 1: it is prime, it is `> x`,
π(P_K(x)) = π(x) + K, and (x, P_K(x)] contains exactly K primes. So it is the K-th prime > x. -/
theorem primeAfter_spec {K : ℕ} (x : ℕ) (hK : 1 ≤ K) :
    (primeAfter K x).Prime ∧ x < primeAfter K x ∧
      Nat.primeCounting (primeAfter K x) = Nat.primeCounting x + K ∧
      ((Ioc x (primeAfter K x)).filter Nat.Prime).card = K := by
  have hpi : Nat.primeCounting (primeAfter K x) = Nat.primeCounting x + K := by
    unfold primeAfter; rw [primeCounting_nth_prime]; omega
  have hlt : x < primeAfter K x := by
    by_contra hc
    have := Nat.monotone_primeCounting (not_lt.1 hc)
    omega
  refine ⟨Nat.prime_nth_prime _, hlt, hpi, ?_⟩
  rw [← primeCounting_sub_eq_card hlt.le]; omega

/-! ### Sub-lemma S (per-parity count) -/

/-- **Sub-lemma S.** For every m and p: #{ x ∈ U_m : x ≡ p (mod 2), x > m } = H_p(m).
(Informal: m ≥ 1 and p ∈ {0, 1}; the formal statement needs neither, the extra cases being
trivial: for m = 0 both sides are 0, and for p ≥ 2 both sides are 0.) Uses F1 (`a_mod_two`),
hence a(1) = 1. -/
theorem subLemmaS (p m : ℕ) :
    ((U m).filter (fun x => x % 2 = p ∧ m < x)).card = holes p m := by
  -- S1: exactly N_p(m) used values have parity p.
  have hS1 : ((U m).filter (fun x => x % 2 = p)).card =
      ((Icc 1 m).filter (fun k => k % 2 = p)).card := by
    rw [U, Finset.filter_image, Finset.card_image_of_injOn]
    · congr 1
      apply Finset.filter_congr
      intro k hk
      rw [a_mod_two (Finset.mem_Icc.1 hk).1]
    · intro i hi j hj h
      exact a_inj (Finset.mem_Icc.1 (Finset.mem_filter.1 hi).1).1
        (Finset.mem_Icc.1 (Finset.mem_filter.1 hj).1).1 h
  -- S2: exactly N_p(m) - H_p(m) of them are ≤ m.
  have hS2 := Finset.card_filter_add_card_filter_not
    (s := (Icc 1 m).filter (fun x => x % 2 = p)) (fun x => x ∈ U m)
  rw [Finset.filter_filter, Finset.filter_filter] at hS2
  have hH : holes p m = ((Icc 1 m).filter (fun x => x % 2 = p ∧ ¬ x ∈ U m)).card := rfl
  -- S3: split the parity-p used values at m.
  have hS3 := Finset.card_filter_add_card_filter_not
    (s := (U m).filter (fun x => x % 2 = p)) (fun x => x ≤ m)
  rw [Finset.filter_filter, Finset.filter_filter] at hS3
  have hlow : (U m).filter (fun x => x % 2 = p ∧ x ≤ m) =
      (Icc 1 m).filter (fun x => x % 2 = p ∧ x ∈ U m) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_Icc]
    constructor
    · rintro ⟨hx, hp, hxm⟩
      have : x ≠ 0 := fun h0 => zero_notMem_U m (h0 ▸ hx)
      exact ⟨⟨by omega, hxm⟩, hp, hx⟩
    · rintro ⟨⟨-, hxm⟩, hp, hx⟩
      exact ⟨hx, hp, hxm⟩
  have hhigh : (U m).filter (fun x => x % 2 = p ∧ ¬ x ≤ m) =
      (U m).filter (fun x => x % 2 = p ∧ m < x) := by
    apply Finset.filter_congr; intro x _; simp only [not_le]
  rw [hlow, hhigh] at hS3
  omega

/-- **Sub-lemma S, equivalent form.** H_p(m) = #{ k ∈ [1, m] : k ≡ p, a(k) > m }. -/
theorem subLemmaS_index (p m : ℕ) :
    ((Icc 1 m).filter (fun k => k % 2 = p ∧ m < a k)).card = holes p m := by
  rw [← subLemmaS, U, Finset.filter_image, Finset.card_image_of_injOn]
  · congr 1
    apply Finset.filter_congr
    intro k hk
    rw [a_mod_two (Finset.mem_Icc.1 hk).1]
  · intro i hi j hj h
    exact a_inj (Finset.mem_Icc.1 (Finset.mem_filter.1 hi).1).1
      (Finset.mem_Icc.1 (Finset.mem_filter.1 hj).1).1 h

/-! ### Step 0: the partner set W and its partition -/

/-- The partner set W = { q - v : q prime, 2v < q ≤ n + v }, written as
{ w ∈ (v, n] : w + v prime } (the translation q ↦ q - v; see `card_primes_eq_card_W`). -/
def W (v n : ℕ) : Finset ℕ := (Ioc v n).filter (fun w => (w + v).Prime)

/-- W1 = { w ∈ W : fi(w) ≤ v - 1 } (ahead values). -/
def W1 (v n : ℕ) : Finset ℕ := (W v n).filter (fun w => w ∈ U (v - 1))

/-- W2 = { w ∈ W : v ≤ fi(w) ≤ n - 1 } (steals). -/
def W2 (v n : ℕ) : Finset ℕ := (W v n).filter (fun w => w ∈ U (n - 1) ∧ w ∉ U (v - 1))

/-- W3 = { w ∈ W : fi(w) = n }. -/
def W3 (v n : ℕ) : Finset ℕ := (W v n).filter (fun w => w ∈ U n ∧ w ∉ U (n - 1))

/-- W4 = { w ∈ W : fi(w) ≥ n + 1 or fi(w) = ∞ } (late values). -/
def W4 (v n : ℕ) : Finset ℕ := (W v n).filter (fun w => w ∉ U n)

/-- Step 0: #Q = #W, where Q is the set of primes in (2v, n+v]; the map is q ↦ q - v. -/
theorem card_primes_eq_card_W (v n : ℕ) :
    ((Ioc (2 * v) (n + v)).filter Nat.Prime).card = (W v n).card := by
  symm
  apply Finset.card_nbij' (fun w => w + v) (fun q => q - v)
  · intro w hw
    simp only [W, Finset.coe_filter, Finset.mem_Ioc, Set.mem_ofPred_eq] at hw ⊢
    exact ⟨⟨by omega, by omega⟩, hw.2⟩
  · intro q hq
    simp only [W, Finset.coe_filter, Finset.mem_Ioc, Set.mem_ofPred_eq] at hq ⊢
    refine ⟨⟨by omega, by omega⟩, ?_⟩
    rw [show q - v + v = q by omega]; exact hq.2
  · intro w _; simp
  · intro q hq
    simp only [Finset.coe_filter, Finset.mem_Ioc, Set.mem_ofPred_eq] at hq
    simp only; omega

/-- Step 0: every partner has parity 1 - ε (q = w + v > 2v ≥ 4 is an odd prime). -/
theorem W_mod_two {v n w : ℕ} (hv : 2 ≤ v) (hw : w ∈ W v n) : w % 2 = 1 - v % 2 := by
  simp only [W, Finset.mem_filter, Finset.mem_Ioc] at hw
  rcases hw.2.eq_two_or_odd with h | h
  · omega
  · omega

/-- The partition in fi-form (class W1): w ∈ W1 ↔ w ∈ W ∧ fi(w) ≤ v - 1. -/
theorem mem_W1_iff_fi {v n w : ℕ} :
    w ∈ W1 v n ↔ w ∈ W v n ∧ ∃ h : Occurs w, fi w h ≤ v - 1 := by
  simp only [W1, Finset.mem_filter, mem_U_iff_fi_le]

/-- Class W2 in fi-form: w ∈ W2 ↔ w ∈ W ∧ v ≤ fi(w) ≤ n - 1. -/
theorem mem_W2_iff_fi {v n w : ℕ} :
    w ∈ W2 v n ↔ w ∈ W v n ∧ ∃ h : Occurs w, v ≤ fi w h ∧ fi w h ≤ n - 1 := by
  simp only [W2, Finset.mem_filter, mem_U_iff_fi_le]
  constructor
  · rintro ⟨hw, ⟨h, h1⟩, h2⟩
    refine ⟨hw, h, ?_, h1⟩
    by_contra hc
    exact h2 ⟨h, by omega⟩
  · rintro ⟨hw, h, h1, h2⟩
    refine ⟨hw, ⟨h, h2⟩, ?_⟩
    rintro ⟨h', h3⟩
    have := one_le_fi h
    have : fi w h' = fi w h := rfl
    omega

/-- Class W3 in fi-form: w ∈ W3 ↔ w ∈ W ∧ fi(w) = n. -/
theorem mem_W3_iff_fi {v n w : ℕ} (hn : 1 ≤ n) :
    w ∈ W3 v n ↔ w ∈ W v n ∧ ∃ h : Occurs w, fi w h = n := by
  simp only [W3, Finset.mem_filter, mem_U_iff_fi_le]
  constructor
  · rintro ⟨hw, ⟨h, h1⟩, h2⟩
    refine ⟨hw, h, ?_⟩
    by_contra hc
    exact h2 ⟨h, by omega⟩
  · rintro ⟨hw, h, h1⟩
    refine ⟨hw, ⟨h, h1.le⟩, ?_⟩
    rintro ⟨h', h3⟩
    have : fi w h' = fi w h := rfl
    omega

/-- Class W4 in fi-form: w ∈ W4 ↔ w ∈ W ∧ (fi(w) ≥ n + 1 or w never occurs). -/
theorem mem_W4_iff_fi {v n w : ℕ} :
    w ∈ W4 v n ↔ w ∈ W v n ∧ ∀ h : Occurs w, n + 1 ≤ fi w h := by
  simp only [W4, Finset.mem_filter, mem_U_iff_fi_le, not_exists, not_le]
  rfl

/-- Step 1: the four classes partition W, so #W = #W1 + #W2 + #W3 + #W4. -/
theorem card_W_eq {v n : ℕ} (hvn : v ≤ n) :
    (W v n).card = (W1 v n).card + (W2 v n).card + (W3 v n).card + (W4 v n).card := by
  have hsub1 : U (v - 1) ⊆ U (n - 1) := U_mono (by omega)
  have hsub2 : U (n - 1) ⊆ U n := U_mono (by omega)
  have e1 := Finset.card_filter_add_card_filter_not (s := W v n) (fun w => w ∈ U (n - 1))
  have e2 := Finset.card_filter_add_card_filter_not
    (s := (W v n).filter (fun w => w ∈ U (n - 1))) (fun w => w ∈ U (v - 1))
  have e3 := Finset.card_filter_add_card_filter_not
    (s := (W v n).filter (fun w => w ∉ U (n - 1))) (fun w => w ∈ U n)
  rw [Finset.filter_filter, Finset.filter_filter] at e2 e3
  have h1 : (W v n).filter (fun w => w ∈ U (n - 1) ∧ w ∈ U (v - 1)) = W1 v n := by
    unfold W1; apply Finset.filter_congr; intro w _
    exact ⟨fun h => h.2, fun h => ⟨hsub1 h, h⟩⟩
  have h2 : (W v n).filter (fun w => w ∈ U (n - 1) ∧ ¬ w ∈ U (v - 1)) = W2 v n := rfl
  have h3 : (W v n).filter (fun w => w ∉ U (n - 1) ∧ w ∈ U n) = W3 v n := by
    unfold W3; apply Finset.filter_congr; intro w _
    exact ⟨fun h => ⟨h.2, h.1⟩, fun h => ⟨h.2, h.1⟩⟩
  have h4 : (W v n).filter (fun w => w ∉ U (n - 1) ∧ ¬ w ∈ U n) = W4 v n := by
    unfold W4; apply Finset.filter_congr; intro w _
    exact ⟨fun h => h.2, fun h => ⟨fun h' => h (hsub2 h'), h⟩⟩
  rw [h1, h2] at e2
  rw [h3, h4] at e3
  omega

/-! ### Steps 2-5: the four bounds -/

/-- Step 2: #W1 ≤ H_{1-ε}(v - 1) (ahead values), via Sub-lemma S at m = v - 1. -/
theorem card_W1_le {v n : ℕ} (hv : 2 ≤ v) : (W1 v n).card ≤ holes (1 - v % 2) (v - 1) := by
  rw [← subLemmaS]
  apply Finset.card_le_card
  intro w hw
  have hpar := W_mod_two hv (Finset.mem_filter.1 hw).1
  simp only [W1, W, Finset.mem_filter, Finset.mem_Ioc] at hw
  simp only [Finset.mem_filter]
  exact ⟨hw.2, hpar, by omega⟩

/-- Step 3, (a)-(f): a steal. For w ∈ W2, with k = fi(w): v ≤ k, k + 1 ≤ n, and
x(w) = a(k+1) is a hole at time v, of parity ε, with 1 ≤ x(w) < v. -/
theorem steal_spec {v n w : ℕ} (hv : 2 ≤ v) (hvU : v ∉ U n) (hw : w ∈ W2 v n) :
    ∃ h : Occurs w, v ≤ fi w h ∧ fi w h + 1 ≤ n ∧
      a (fi w h + 1) ∈ (Ico 1 v).filter (fun x => x % 2 = v % 2 ∧ x ∉ U v) := by
  have hpar := W_mod_two hv (Finset.mem_filter.1 hw).1
  simp only [W2, W, Finset.mem_filter, Finset.mem_Ioc] at hw
  obtain ⟨⟨⟨hvw, hwn⟩, hprime⟩, hwU, hwU'⟩ := hw
  obtain ⟨h, hk⟩ := mem_U_iff_fi_le.1 hwU
  set k := fi w h with hkdef
  have hk1 : 1 ≤ k := one_le_fi h
  have hak : a k = w := a_fi h
  have hvk : v ≤ k := by
    by_contra hc
    exact hwU' (hak ▸ mem_U_self hk1 (by omega))
  refine ⟨h, hvk, by omega, ?_⟩
  rw [← hkdef]
  -- (a) v is available at step k
  have hvUk : v ∉ U k := fun hm => hvU (U_mono (by omega) hm)
  have hp : (a k + v).Prime := by rw [hak]; exact hprime
  -- (b) the greedy rule
  have hle : a (k + 1) ≤ v := a_succ_min hk1 (by omega) hvUk hp
  -- (c) a(k+1) ≠ v, since k + 1 ≤ n
  have hne : a (k + 1) ≠ v := fun he => hvU (he ▸ mem_U_self (by omega) (by omega))
  -- (d) parity
  have hpk := a_mod_two hk1
  have hpk1 := a_mod_two (by omega : 1 ≤ k + 1)
  -- (e) x(w) is a hole at time v
  have hnotU : a (k + 1) ∉ U v := fun hm => (a_succ_spec hk1).2.1 (U_mono hvk hm)
  have hpos := a_pos (by omega : 1 ≤ k + 1)
  simp only [Finset.mem_filter, Finset.mem_Ico]
  exact ⟨⟨hpos, by omega⟩, by omega, hnotU⟩

/-- Step 3: #W2 ≤ B(v) (steals), via the injection w ↦ a(fi(w) + 1). -/
theorem card_W2_le {v n : ℕ} (hv : 2 ≤ v) (hvU : v ∉ U n) : (W2 v n).card ≤ B v := by
  classical
  let f : ℕ → ℕ := fun w => if h : Occurs w then a (fi w h + 1) else 0
  have hf : ∀ w ∈ W2 v n, ∃ h : Occurs w, f w = a (fi w h + 1) ∧ v ≤ fi w h ∧
      a (fi w h + 1) ∈ (Ico 1 v).filter (fun x => x % 2 = v % 2 ∧ x ∉ U v) := by
    intro w hw
    obtain ⟨h, h1, -, h3⟩ := steal_spec hv hvU hw
    exact ⟨h, by simp [f, h], h1, h3⟩
  unfold B
  apply Finset.card_le_card_of_injOn f
  · intro w hw
    obtain ⟨h, he, -, hm⟩ := hf w hw
    rw [he]; exact hm
  · -- (g) injectivity
    intro w hw w' hw' hww
    obtain ⟨h, he, h1, -⟩ := hf w hw
    obtain ⟨h', he', h1', -⟩ := hf w' hw'
    have hv1 := one_le_fi h
    have hv1' := one_le_fi h'
    have : fi w h + 1 = fi w' h' + 1 := a_inj (by omega) (by omega) (he ▸ he' ▸ hww)
    rw [← a_fi h, ← a_fi h']
    congr 1; omega

/-- Step 4: #W3 ≤ 1, since W3 ⊆ {a(n)}. -/
theorem card_W3_le {v n : ℕ} (hn : 1 ≤ n) : (W3 v n).card ≤ 1 := by
  have hsub : W3 v n ⊆ {a n} := by
    intro w hw
    simp only [W3, Finset.mem_filter] at hw
    obtain ⟨-, h1, h2⟩ := hw
    obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
    rw [U_succ, Finset.mem_insert] at h1
    rw [Finset.mem_singleton]
    rcases h1 with h1 | h1
    · exact h1
    · exact absurd h1 (by simpa using h2)
  simpa using Finset.card_le_card hsub

/-- Step 5: #W4 ≤ H_{1-ε}(n) (late values). -/
theorem card_W4_le {v n : ℕ} (hv : 2 ≤ v) : (W4 v n).card ≤ holes (1 - v % 2) n := by
  apply Finset.card_le_card
  intro w hw
  have hpar := W_mod_two hv (Finset.mem_filter.1 hw).1
  simp only [W4, W, Finset.mem_filter, Finset.mem_Ioc] at hw
  simp only [Finset.mem_filter, Finset.mem_Icc]
  exact ⟨⟨by omega, hw.1.1.2⟩, hpar, hw.2⟩

/-! ### Main theorem -/

/-- **L009 (count form).** For n ≥ 2, 2 ≤ v ≤ n, v ∉ U_n, ε = v mod 2:
#{ q prime : 2v < q ≤ n + v } ≤ 1 + B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n). -/
theorem L009_count {n v : ℕ} (_hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    ((Ioc (2 * v) (n + v)).filter Nat.Prime).card ≤
      1 + B v + holes (1 - v % 2) (v - 1) + holes (1 - v % 2) n := by
  rw [card_primes_eq_card_W, card_W_eq hvn]
  have := card_W1_le (n := n) hv
  have := card_W2_le hv hvU
  have := card_W3_le (v := v) (by omega : 1 ≤ n)
  have := card_W4_le (n := n) hv
  omega

/-- **L009.** Informal: for n ≥ 2 and 2 ≤ v ≤ n with v ∉ U_n, ε = v mod 2,
π(n + v) - π(2v) ≤ 1 + B(v) + H_{1-ε}(v - 1) + H_{1-ε}(n).
Formal: π = `Nat.primeCounting`, U_n = `U n`, B = `B`, H_p = `holes p`, ε = `v % 2`. -/
theorem L009 {n v : ℕ} (hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) ≤
      1 + B v + holes (1 - v % 2) (v - 1) + holes (1 - v % 2) n := by
  rw [primeCounting_sub_eq_card (by omega)]
  exact L009_count hn hv hvn hvU

/-! ### Sharpening: 1 + B(v) + H_{1-ε}(v - 1) = H(v) -/

/-- Sharpening (i): H_ε(v) = B(v) + 1 when v ≥ 1 is a hole at time v. -/
theorem holes_same_parity {v : ℕ} (hv : 1 ≤ v) (hvU : v ∉ U v) : holes (v % 2) v = B v + 1 := by
  unfold holes B
  have hset : (Icc 1 v).filter (fun x => x % 2 = v % 2 ∧ x ∉ U v) =
      insert v ((Ico 1 v).filter (fun x => x % 2 = v % 2 ∧ x ∉ U v)) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_insert, Finset.mem_Ico]
    constructor
    · rintro ⟨⟨h1, h2⟩, h3⟩
      by_cases hx : x = v
      · exact Or.inl hx
      · exact Or.inr ⟨⟨h1, by omega⟩, h3⟩
    · rintro (rfl | ⟨⟨h1, h2⟩, h3⟩)
      · exact ⟨⟨hv, le_rfl⟩, rfl, hvU⟩
      · exact ⟨⟨h1, by omega⟩, h3⟩
  rw [hset, Finset.card_insert_of_notMem (by simp)]

/-- Sharpening (ii): H_{1-ε}(v) = H_{1-ε}(v - 1) for v ≥ 1, since a(v) ≡ v ≡ ε (F1). -/
theorem holes_opp_parity {v : ℕ} (hv : 1 ≤ v) : holes (1 - v % 2) v = holes (1 - v % 2) (v - 1) := by
  obtain ⟨m, rfl⟩ : ∃ m, v = m + 1 := ⟨v - 1, by omega⟩
  unfold holes
  have ha := a_mod_two (by omega : 1 ≤ m + 1)
  congr 1
  ext x
  simp only [Finset.mem_filter, Finset.mem_Icc, U_succ, Finset.mem_insert, not_or,
    show m + 1 - 1 = m from rfl]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3, -, h4⟩
    exact ⟨⟨h1, by omega⟩, h3, h4⟩
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨⟨h1, by omega⟩, h3, ?_, h4⟩
    intro he; rw [he] at h3; omega

/-- **Sharpening identity.** For v ≥ 2 a hole at time v: 1 + B(v) + H_{1-ε}(v - 1) = H(v). -/
theorem L009_identity {v : ℕ} (hv : 2 ≤ v) (hvU : v ∉ U v) :
    1 + B v + holes (1 - v % 2) (v - 1) = H v := by
  have h1 := holes_same_parity (by omega) hvU
  have h2 := holes_opp_parity (v := v) (by omega)
  unfold H
  rcases Nat.mod_two_eq_zero_or_one v with h | h
  · rw [h] at h1 h2 ⊢; simp only [Nat.sub_zero] at h2 ⊢; omega
  · rw [h] at h1 h2 ⊢; simp only [Nat.sub_self] at h2 ⊢; omega

/-- **L009' (sharp form).** For n ≥ 2 and 2 ≤ v ≤ n with v ∉ U_n, ε = v mod 2:
π(n + v) - π(2v) ≤ H(v) + H_{1-ε}(n). -/
theorem L009_sharp {n v : ℕ} (hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) ≤ H v + holes (1 - v % 2) n := by
  have := L009 hn hv hvn hvU
  rw [← L009_identity hv (fun h => hvU (U_mono hvn h))]
  omega

/-! ### Corollary -/

theorem holes_le_H (p m : ℕ) (hp : p = 0 ∨ p = 1) : holes p m ≤ H m := by
  unfold H; rcases hp with rfl | rfl <;> omega

/-- **Corollary, prime-count form.** Suppose n ≥ 2 and H(m) ≤ h for all 1 ≤ m ≤ n. Then every
hole v at time n (2 ≤ v ≤ n, v ∉ U_n) has π(n + v) - π(2v) ≤ 2h, i.e. the interval (2v, n + v]
contains at most 2h primes. -/
theorem L009_corollary_count {n v h : ℕ} (hn : 2 ≤ n) (hH : ∀ m, 1 ≤ m → m ≤ n → H m ≤ h)
    (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) ≤ 2 * h ∧
      ((Ioc (2 * v) (n + v)).filter Nat.Prime).card ≤ 2 * h := by
  have h1 := L009_sharp hn hv hvn hvU
  have h2 := hH v (by omega) hvn
  have h3 := hH n (by omega) le_rfl
  have h4 := holes_le_H (1 - v % 2) n (by omega)
  have h5 : Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) ≤ 2 * h := by omega
  refine ⟨h5, ?_⟩
  rw [← primeCounting_sub_eq_card (by omega)]; exact h5

/-- **Corollary (L009).** Informal: suppose H(m) ≤ h for all m ≤ n. Then every hole v at time n
(2 ≤ v ≤ n, v ∉ U_n) satisfies n - v < ℓ_{2h+1}(2v), with ℓ_K(x) = (K-th prime > x) - x.
Formal: the hypothesis is taken for 1 ≤ m ≤ n (H(0) = 0 anyway), n ≥ 2 as in the informal proof;
ℓ_K(x) = `ell K x`. -/
theorem L009_corollary {n v h : ℕ} (hn : 2 ≤ n) (hH : ∀ m, 1 ≤ m → m ≤ n → H m ≤ h)
    (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    n - v < ell (2 * h + 1) (2 * v) := by
  have hc := (L009_corollary_count hn hH hv hvn hvU).1
  obtain ⟨-, hlt, hpi, -⟩ := primeAfter_spec (2 * v) (by omega : 1 ≤ 2 * h + 1)
  unfold ell
  by_contra hcon
  have hle : primeAfter (2 * h + 1) (2 * v) ≤ n + v := by omega
  have := Nat.monotone_primeCounting hle
  omega

/-- **Corollary, lifetime form.** For a value v ≥ 2 that occurs with fi(v) > v: if H(m) ≤ h for
all 1 ≤ m < fi(v), then L(v) = fi(v) - v ≤ ℓ_{2h+1}(2v). (Apply the Corollary at n = fi(v) - 1.) -/
theorem L009_lifetime {v h : ℕ} (hv : 2 ≤ v) (hocc : Occurs v) (hlate : v < fi v hocc)
    (hH : ∀ m, 1 ≤ m → m < fi v hocc → H m ≤ h) :
    fi v hocc - v ≤ ell (2 * h + 1) (2 * v) := by
  have hvU : v ∉ U (fi v hocc - 1) := by
    intro hm
    obtain ⟨h', hle⟩ := mem_U_iff_fi_le.1 hm
    have : fi v h' = fi v hocc := rfl
    omega
  have := L009_corollary (n := fi v hocc - 1) (by omega) (fun m h1 h2 => hH m h1 (by omega))
    hv (by omega) hvU
  omega

end ErdosWatts
