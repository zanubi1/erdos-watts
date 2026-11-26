import ErdosWatts.Defs
import ErdosWatts.L001
import ErdosWatts.L009

/-!
# L012 - Primes survived by a hole are paid by down-crossings of its level

Informal (lemmas/proven/L012-crossing-bound.md). For v ≥ 2 and n ≥ 2,
X_v(n) = #{ j ∈ [2, n] : a(j-1) > v > a(j) }. Let n ≥ 2 and 2 ≤ v ≤ n with v ∉ U_n,
ε = v mod 2. Then

  (a) π(n + v) - π(2v) ≤ X_v(n) + 1 + H_{1-ε}(n); more precisely, with W1..W4 as in L009,
      |W1| + |W2| ≤ X_v(n), |W3| ≤ 1 and |W4| ≤ H_{1-ε}(n).
  (b) With X^ε_v(n) counting only the down-crossings j with a(j) ≡ ε (mod 2):
      |W1| + |W2| ≤ X^ε_v(n) ≤ H(v) - 1, and X_v(n) ≤ H(v - 1) + H(v) - 1.

## Mapping informal -> formal

* X_v(n) = `downCrossings v n`, X^ε_v(n) = `downCrossingsPar v n` (both in `Defs.lean`);
  W, W1..W4 = `W`, `W1`..`W4` from `L009.lean`; π = `Nat.primeCounting`; ε = `v % 2`;
  H_p = `holes p`, H = `H`, B = `B`, U_n = `U n`; informal a(n) = `a n` for n ≥ 1.
* `H v - 1` and `H (v-1) + H v - 1` are natural subtractions; H(v) ≥ 1 here (v is a hole at
  time v), so they agree with the informal integers.
* Scope: the formal sequence `a` has a(1) = 1. The informal remark that (a) and the bound on
  X_v(n) hold for *every* start a(1) is not formalized (the start is fixed in `Defs.lean`).
-/

namespace ErdosWatts

open Finset

/-- W1 ∪ W2 = { w ∈ W : fi(w) ≤ n - 1 }, and #W1 + #W2 = #(W1 ∪ W2). -/
theorem card_W1_add_card_W2 {v n : ℕ} (hvn : v ≤ n) :
    (W1 v n).card + (W2 v n).card = ((W v n).filter (fun w => w ∈ U (n - 1))).card := by
  have hsub1 : U (v - 1) ⊆ U (n - 1) := U_mono (by omega)
  have e := Finset.card_filter_add_card_filter_not
    (s := (W v n).filter (fun w => w ∈ U (n - 1))) (fun w => w ∈ U (v - 1))
  rw [Finset.filter_filter, Finset.filter_filter] at e
  have h1 : (W v n).filter (fun w => w ∈ U (n - 1) ∧ w ∈ U (v - 1)) = W1 v n := by
    unfold W1; apply Finset.filter_congr; intro w _
    exact ⟨fun h => h.2, fun h => ⟨hsub1 h, h⟩⟩
  have h2 : (W v n).filter (fun w => w ∈ U (n - 1) ∧ ¬ w ∈ U (v - 1)) = W2 v n := rfl
  rw [h1, h2] at e
  exact e

/-- The crossing built from a partner w ∈ W1 ∪ W2 (fi(w) ≤ n - 1): j = fi(w) + 1 lies in
[2, n], a(j-1) = w > v, a(j) < v, and a(j) ≡ ε (the last by L001). -/
theorem crossing_of_partner {v n w : ℕ} (hv : 2 ≤ v) (hvU : v ∉ U n)
    (hw : w ∈ (W v n).filter (fun w => w ∈ U (n - 1))) :
    ∃ h : Occurs w, fi w h + 1 ∈ (Icc 2 n).filter
      (fun j => v < a (j - 1) ∧ a j < v ∧ a j % 2 = v % 2) := by
  have hpar := W_mod_two hv (Finset.mem_filter.1 hw).1
  simp only [W, Finset.mem_filter, Finset.mem_Ioc] at hw
  obtain ⟨⟨⟨hvw, hwn⟩, hprime⟩, hwU⟩ := hw
  obtain ⟨h, hk⟩ := mem_U_iff_fi_le.1 hwU
  refine ⟨h, ?_⟩
  have hk1 : 1 ≤ fi w h := one_le_fi h
  have hak : a (fi w h) = w := a_fi h
  -- v is available at step k = fi(w)
  have hvUk : v ∉ U (fi w h) := fun hm => hvU (U_mono (by omega) hm)
  have hp : (a (fi w h) + v).Prime := by rw [hak]; exact hprime
  have hle : a (fi w h + 1) ≤ v := a_succ_min hk1 (by omega) hvUk hp
  -- a(k+1) ≠ v since k + 1 ≤ n
  have hne : a (fi w h + 1) ≠ v := fun he => hvU (he ▸ mem_U_self (by omega) (by omega))
  -- parity, by L001
  have halt := L001_parity hk1
  simp only [Finset.mem_filter, Finset.mem_Icc, Nat.add_sub_cancel]
  refine ⟨⟨by omega, by omega⟩, by omega, by omega, by omega⟩

/-- **L012 (b)(i).** |W1| + |W2| ≤ X^ε_v(n). -/
theorem L012_W12_le_par {n v : ℕ} (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    (W1 v n).card + (W2 v n).card ≤ downCrossingsPar v n := by
  classical
  rw [card_W1_add_card_W2 hvn]
  unfold downCrossingsPar
  let g : ℕ → ℕ := fun w => if h : Occurs w then fi w h + 1 else 0
  have hg : ∀ w ∈ (W v n).filter (fun w => w ∈ U (n - 1)), ∃ h : Occurs w,
      g w = fi w h + 1 ∧ fi w h + 1 ∈ (Icc 2 n).filter
        (fun j => v < a (j - 1) ∧ a j < v ∧ a j % 2 = v % 2) := by
    intro w hw
    obtain ⟨h, hm⟩ := crossing_of_partner hv hvU hw
    exact ⟨h, by simp [g, h], hm⟩
  apply Finset.card_le_card_of_injOn g
  · intro w hw
    obtain ⟨h, he, hm⟩ := hg w hw
    rw [he]; exact hm
  · intro w hw w' hw' hww
    obtain ⟨h, he, -⟩ := hg w hw
    obtain ⟨h', he', -⟩ := hg w' hw'
    rw [← a_fi h, ← a_fi h']
    congr 1; omega

/-- X^ε_v(n) ≤ X_v(n). -/
theorem downCrossingsPar_le (v n : ℕ) : downCrossingsPar v n ≤ downCrossings v n := by
  apply Finset.card_le_card
  intro j hj
  simp only [Finset.mem_filter] at hj ⊢
  exact ⟨hj.1, hj.2.1, hj.2.2.1⟩

/-- **L012 (a), first class.** |W1| + |W2| ≤ X_v(n). -/
theorem L012_W12_le {n v : ℕ} (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    (W1 v n).card + (W2 v n).card ≤ downCrossings v n :=
  (L012_W12_le_par hv hvn hvU).trans (downCrossingsPar_le v n)

/-- **L012 (a), per-class form.** Under the hypotheses of L012: |W1| + |W2| ≤ X_v(n),
|W3| ≤ 1 and |W4| ≤ H_{1-ε}(n). -/
theorem L012_classes {n v : ℕ} (hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    (W1 v n).card + (W2 v n).card ≤ downCrossings v n ∧ (W3 v n).card ≤ 1 ∧
      (W4 v n).card ≤ holes (1 - v % 2) n :=
  ⟨L012_W12_le hv hvn hvU, card_W3_le (by omega), card_W4_le hv⟩

/-- **L012 (a).** Informal: for n ≥ 2 and 2 ≤ v ≤ n with v ∉ U_n, ε = v mod 2,
π(n + v) - π(2v) ≤ X_v(n) + 1 + H_{1-ε}(n). -/
theorem L012 {n v : ℕ} (hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) ≤
      downCrossings v n + 1 + holes (1 - v % 2) n := by
  rw [primeCounting_sub_eq_card (by omega), card_primes_eq_card_W, card_W_eq hvn]
  obtain ⟨h1, h2, h3⟩ := L012_classes hn hv hvn hvU
  omega

/-! ### Part (b): the ceilings -/

/-- Parity-free count: #{ x ∈ U_m : x > m } = H(m) (because |U_m| = m). -/
theorem H_eq_card_notMem (m : ℕ) : H m = ((Icc 1 m).filter (fun x => x ∉ U m)).card := by
  have e := Finset.card_filter_add_card_filter_not
    (s := (Icc 1 m).filter (fun x => x ∉ U m)) (fun x => x % 2 = 0)
  rw [Finset.filter_filter, Finset.filter_filter] at e
  have h0 : (Icc 1 m).filter (fun x => x ∉ U m ∧ x % 2 = 0) =
      (Icc 1 m).filter (fun x => x % 2 = 0 ∧ x ∉ U m) := by
    apply Finset.filter_congr; intro x _; exact And.comm
  have h1 : (Icc 1 m).filter (fun x => x ∉ U m ∧ ¬ x % 2 = 0) =
      (Icc 1 m).filter (fun x => x % 2 = 1 ∧ x ∉ U m) := by
    apply Finset.filter_congr; intro x _
    constructor
    · rintro ⟨h1, h2⟩; exact ⟨by omega, h1⟩
    · rintro ⟨h1, h2⟩; exact ⟨h2, by omega⟩
  rw [h0, h1] at e
  unfold H holes
  exact e

theorem card_U_filter_gt (m : ℕ) : ((U m).filter (fun x => m < x)).card = H m := by
  have e1 := Finset.card_filter_add_card_filter_not (s := U m) (fun x => x ≤ m)
  have e2 := Finset.card_filter_add_card_filter_not (s := Icc 1 m) (fun x => x ∈ U m)
  rw [card_U] at e1
  rw [Nat.card_Icc, Nat.add_sub_cancel] at e2
  have hlow : (U m).filter (fun x => x ≤ m) = (Icc 1 m).filter (fun x => x ∈ U m) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_Icc]
    constructor
    · rintro ⟨hx, hxm⟩
      have : x ≠ 0 := fun h0 => zero_notMem_U m (h0 ▸ hx)
      exact ⟨⟨by omega, hxm⟩, hx⟩
    · rintro ⟨⟨-, hxm⟩, hx⟩
      exact ⟨hx, hxm⟩
  have hhigh : (U m).filter (fun x => ¬ x ≤ m) = (U m).filter (fun x => m < x) := by
    apply Finset.filter_congr; intro x _; simp only [not_le]
  rw [hlow, hhigh] at e1
  rw [H_eq_card_notMem]
  omega

/-- The holes < v at time v number H(v) - 1, when v ≥ 1 is itself a hole at time v. -/
theorem card_holes_below {v : ℕ} (hv : 1 ≤ v) (hvU : v ∉ U v) :
    ((Ico 1 v).filter (fun x => x ∉ U v)).card + 1 = H v := by
  rw [H_eq_card_notMem]
  have hset : (Icc 1 v).filter (fun x => x ∉ U v) =
      insert v ((Ico 1 v).filter (fun x => x ∉ U v)) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_Icc, Finset.mem_insert, Finset.mem_Ico]
    constructor
    · rintro ⟨⟨h1, h2⟩, h3⟩
      by_cases hx : x = v
      · exact Or.inl hx
      · exact Or.inr ⟨⟨h1, by omega⟩, h3⟩
    · rintro (rfl | ⟨⟨h1, h2⟩, h3⟩)
      · exact ⟨⟨hv, le_rfl⟩, hvU⟩
      · exact ⟨⟨h1, by omega⟩, h3⟩
  rw [hset, Finset.card_insert_of_notMem (by simp)]

/-- A crossing at time j > v lands on a hole < v at time v: a(j) ∉ U_{j-1} ⊇ U_v. -/
theorem a_notMem_U_of_lt {v j : ℕ} (hj : 2 ≤ j) (hvj : v < j) : a j ∉ U v := by
  obtain ⟨k, rfl⟩ : ∃ k, j = k + 1 := ⟨j - 1, by omega⟩
  exact fun hm => (a_succ_spec (by omega : 1 ≤ k)).2.1 (U_mono (by omega) hm)

/-- **L012 (b)(ii).** X^ε_v(n) ≤ H(v) - 1 (needs a(1) odd; here a(1) = 1). -/
theorem L012_par_le {n v : ℕ} (_hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    downCrossingsPar v n ≤ H v - 1 := by
  have hvUv : v ∉ U v := fun h => hvU (U_mono hvn h)
  have hid := L009_identity hv hvUv
  unfold downCrossingsPar
  set C := (Icc 2 n).filter (fun j => v < a (j - 1) ∧ a j < v ∧ a j % 2 = v % 2)
  have e := Finset.card_filter_add_card_filter_not (s := C) (fun j => j ≤ v)
  -- crossings with j ≤ v: j ↦ a(j-1), a used value > v - 1 at time v - 1, of parity 1 - ε
  have hE : (C.filter (fun j => j ≤ v)).card ≤ holes (1 - v % 2) (v - 1) := by
    rw [← subLemmaS]
    apply Finset.card_le_card_of_injOn (fun j => a (j - 1))
    · intro j hj
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj ⊢
      obtain ⟨⟨⟨hj2, -⟩, h1, -, h3⟩, hjv⟩ := hj
      have halt := L001_parity (n := j - 1) (by omega)
      rw [show j - 1 + 1 = j by omega] at halt
      exact ⟨mem_U_self (by omega) (by omega), by omega, by omega⟩
    · intro j hj j' hj' h
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj hj'
      have := a_inj (by omega) (by omega) h
      omega
  -- crossings with v < j ≤ n: j ↦ a(j), a hole < v at time v of parity ε
  have hL : (C.filter (fun j => ¬ j ≤ v)).card ≤ B v := by
    unfold B
    apply Finset.card_le_card_of_injOn (fun j => a j)
    · intro j hj
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc, Finset.mem_Ico,
        Set.mem_ofPred_eq] at hj ⊢
      obtain ⟨⟨⟨hj2, -⟩, -, h2, h3⟩, hjv⟩ := hj
      exact ⟨⟨a_pos (by omega), h2⟩, h3, a_notMem_U_of_lt hj2 (by omega)⟩
    · intro j hj j' hj' h
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj hj'
      exact a_inj (by omega) (by omega) h
  omega

/-- **L012 (b)(iii).** X_v(n) ≤ H(v - 1) + H(v) - 1. -/
theorem L012_crossings_le {n v : ℕ} (_hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    downCrossings v n ≤ H (v - 1) + H v - 1 := by
  have hvUv : v ∉ U v := fun h => hvU (U_mono hvn h)
  have hbelow := card_holes_below (by omega) hvUv
  unfold downCrossings
  set C := (Icc 2 n).filter (fun j => v < a (j - 1) ∧ a j < v)
  have e := Finset.card_filter_add_card_filter_not (s := C) (fun j => j ≤ v)
  have hE : (C.filter (fun j => j ≤ v)).card ≤ H (v - 1) := by
    rw [← card_U_filter_gt]
    apply Finset.card_le_card_of_injOn (fun j => a (j - 1))
    · intro j hj
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj ⊢
      obtain ⟨⟨⟨hj2, -⟩, h1, -⟩, hjv⟩ := hj
      exact ⟨mem_U_self (by omega) (by omega), by omega⟩
    · intro j hj j' hj' h
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj hj'
      have := a_inj (by omega) (by omega) h
      omega
  have hL : (C.filter (fun j => ¬ j ≤ v)).card ≤ ((Ico 1 v).filter (fun x => x ∉ U v)).card := by
    apply Finset.card_le_card_of_injOn (fun j => a j)
    · intro j hj
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc, Finset.mem_Ico,
        Set.mem_ofPred_eq] at hj ⊢
      obtain ⟨⟨⟨hj2, -⟩, -, h2⟩, hjv⟩ := hj
      exact ⟨⟨a_pos (by omega), h2⟩, a_notMem_U_of_lt hj2 (by omega)⟩
    · intro j hj j' hj' h
      simp only [C, Finset.coe_filter, Finset.mem_filter, Finset.mem_Icc,
        Set.mem_ofPred_eq] at hj hj'
      exact a_inj (by omega) (by omega) h
  omega

/-- **L012 (b).** Under the hypotheses of (a): |W1| + |W2| ≤ X^ε_v(n) ≤ H(v) - 1, and
X_v(n) ≤ H(v - 1) + H(v) - 1. -/
theorem L012_b {n v : ℕ} (hn : 2 ≤ n) (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    (W1 v n).card + (W2 v n).card ≤ downCrossingsPar v n ∧ downCrossingsPar v n ≤ H v - 1 ∧
      downCrossings v n ≤ H (v - 1) + H v - 1 :=
  ⟨L012_W12_le_par hv hvn hvU, L012_par_le hn hv hvn hvU, L012_crossings_le hn hv hvn hvU⟩

end ErdosWatts
