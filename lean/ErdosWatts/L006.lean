import ErdosWatts.L001

/-!
# L006 - Step formula (the parts used by C013 (b))

Informal (lemmas/proven/L006-step-formula.md). For n >= 1:

* π_n is the parity of a(n+1); by L001 it is (n+1) mod 2.
* u*(n) = min { x >= 1 : x ≡ π_n (mod 2), x ∉ U_n } (parity frontier); t_n = a(n) + u*(n).
* O*(n) = #{ x ∈ U_n : x ≡ π_n (mod 2), x > u*(n) } (overshoot).

**(b)** u*(n) <= n + 1.
**(c)** a(n+1) - (n+1) <= q_{O*(n)+1} - t_n, where q_1 < q_2 < ... are the primes >= t_n.
Equivalently (L006's "Interpretation"): if [t_n, t_n + d] contains at least O*(n) + 1 primes,
then a(n+1) - (n+1) <= d.

## What is formalized here (only what C013 (b) needs)

* `piPar n := (n + 1) % 2`. This is a *definition* of π_n by the value that L001 gives it;
  `a_succ_mod_two_eq_piPar` proves that it is the parity of `a (n+1)` (for `n ≥ 1`).
* `uStar`, `tStar`, `Ostar` = u*(n), t_n, O*(n), exactly as above (u* via `Nat.find`).
* `L006_b : uStar n ≤ n + 1` (for `n ≥ 1`).
* `L006_c_interval`: the interval form of (c): if `#(primes in [t_n, t_n + d]) ≥ O*(n) + 1`
  then `a (n+1) ≤ uStar n + d`; and `L006_c : a (n+1) ≤ (n + 1) + d` (= informal
  a(n+1) - (n+1) <= d, without truncated subtraction). The q_K form is not stated: the interval
  form is the one used in C013 (b), and L006 itself states the equivalence.
* `Ostar_le_half : O*(n) ≤ n / 2`. C013 (b) gets this from (b') (O* = (n+1-u*)/2) and u* >= 1;
  here it is proved directly from (Cnt) (O*'s set is a subset of the used values of parity π_n,
  of which there are floor(n/2)). (b') and the exact formula (a) are **not** formalized.
* `card_U_filter_parity` is (Cnt): `#{x ∈ U_n : x ≡ π_n} = n / 2`.
-/

namespace ErdosWatts

open Finset

/-- Number of `x ∈ [1, m]` with `x % 2 = 0` is `m / 2`. -/
theorem card_Icc_filter_even (m : ℕ) : ((Icc 1 m).filter (fun x => x % 2 = 0)).card = m / 2 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [← Finset.insert_Icc_right_eq_Icc_add_one (by omega), filter_insert]
    split_ifs with h
    · rw [card_insert_of_notMem (by simp), ih]; omega
    · rw [ih]; omega

/-- Number of `x ∈ [1, m]` with `x % 2 = 1` is `(m + 1) / 2`. -/
theorem card_Icc_filter_odd (m : ℕ) :
    ((Icc 1 m).filter (fun x => x % 2 = 1)).card = (m + 1) / 2 := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [← Finset.insert_Icc_right_eq_Icc_add_one (by omega), filter_insert]
    split_ifs with h
    · rw [card_insert_of_notMem (by simp), ih]; omega
    · rw [ih]; omega

/-- Number of `x ∈ [1, n]` of parity `(n + 1) % 2` is `n / 2`. -/
theorem card_Icc_filter_succ_parity (n : ℕ) :
    ((Icc 1 n).filter (fun x => x % 2 = (n + 1) % 2)).card = n / 2 := by
  rcases Nat.mod_two_eq_zero_or_one (n + 1) with h | h
  · rw [h, card_Icc_filter_even]
  · rw [h, card_Icc_filter_odd]; omega

/-- Parity `(n+1) % 2` in `[1, n + 1]`: `n / 2 + 1` elements. -/
theorem card_Icc_succ_filter_succ_parity (n : ℕ) :
    ((Icc 1 (n + 1)).filter (fun x => x % 2 = (n + 1) % 2)).card = n / 2 + 1 := by
  rcases Nat.mod_two_eq_zero_or_one (n + 1) with h | h
  · rw [h, card_Icc_filter_even]; omega
  · rw [h, card_Icc_filter_odd]; omega

/-- π_n, the parity of a(n+1); by L001 it is `(n + 1) % 2` (see `a_succ_mod_two_eq_piPar`). -/
def piPar (n : ℕ) : ℕ := (n + 1) % 2

theorem piPar_lt (n : ℕ) : piPar n < 2 := Nat.mod_lt _ (by norm_num)

/-- `piPar n` is the parity of `a (n+1)` (L001). -/
theorem a_succ_mod_two_eq_piPar (n : ℕ) : a (n + 1) % 2 = piPar n :=
  a_mod_two (by omega)

/-- The set defining u*(n) is nonempty. -/
theorem exists_uStar (n : ℕ) : ∃ x, 1 ≤ x ∧ x % 2 = piPar n ∧ x ∉ U n := by
  refine ⟨2 * (U n).sup id + 2 + piPar n, by omega, by have := piPar_lt n; omega, fun hx => ?_⟩
  have : id (2 * (U n).sup id + 2 + piPar n) ≤ (U n).sup id := le_sup (f := id) hx
  simp only [id] at this; omega

/-- u*(n) = min { x ≥ 1 : x ≡ π_n (mod 2), x ∉ U_n }, the parity frontier. -/
noncomputable def uStar (n : ℕ) : ℕ := Nat.find (exists_uStar n)

/-- t_n = a(n) + u*(n). -/
noncomputable def tStar (n : ℕ) : ℕ := a n + uStar n

/-- O*(n) = #{ x ∈ U_n : x ≡ π_n (mod 2), x > u*(n) }, the overshoot. -/
noncomputable def Ostar (n : ℕ) : ℕ :=
  ((U n).filter (fun x => x % 2 = piPar n ∧ uStar n < x)).card

theorem uStar_spec (n : ℕ) : 1 ≤ uStar n ∧ uStar n % 2 = piPar n ∧ uStar n ∉ U n :=
  Nat.find_spec (exists_uStar n)

theorem uStar_min {n x : ℕ} (hx : 1 ≤ x) (hpar : x % 2 = piPar n) (hxU : x ∉ U n) :
    uStar n ≤ x :=
  Nat.find_min' (exists_uStar n) ⟨hx, hpar, hxU⟩

/-- **(Cnt)** (for any `n`): the used values of parity `p` are the `a k` with `k ≤ n`,
`k ≡ p`; so `#{x ∈ U_n : x ≡ p} = #{k ∈ [1, n] : k ≡ p}`. -/
theorem card_U_filter_mod (n p : ℕ) :
    ((U n).filter (fun x => x % 2 = p)).card = ((Icc 1 n).filter (fun k => k % 2 = p)).card := by
  have : (U n).filter (fun x => x % 2 = p) = ((Icc 1 n).filter (fun k => k % 2 = p)).image a := by
    ext x
    simp only [mem_filter, mem_image, U, mem_Icc]
    constructor
    · rintro ⟨⟨k, hk, rfl⟩, hp⟩
      exact ⟨k, ⟨hk, by rw [← a_mod_two hk.1]; exact hp⟩, rfl⟩
    · rintro ⟨k, ⟨hk, hp⟩, rfl⟩
      exact ⟨⟨k, hk, rfl⟩, by rw [a_mod_two hk.1]; exact hp⟩
  rw [this, card_image_of_injOn]
  intro i hi j hj h
  exact a_inj (mem_Icc.1 (mem_filter.1 hi).1).1 (mem_Icc.1 (mem_filter.1 hj).1).1 h

/-- **(Cnt)**: `#{x ∈ U_n : x ≡ π_n (mod 2)} = floor(n/2)`. -/
theorem card_U_filter_parity (n : ℕ) :
    ((U n).filter (fun x => x % 2 = piPar n)).card = n / 2 := by
  rw [card_U_filter_mod]; exact card_Icc_filter_succ_parity n

/-- **L006 (b).** For `n ≥ 1` (in fact for all `n`): u*(n) ≤ n + 1. Pigeonhole: [1, n+1]
contains floor(n/2) + 1 values of parity π_n, at most floor(n/2) of which are used. -/
theorem L006_b (n : ℕ) : uStar n ≤ n + 1 := by
  by_contra hlt
  push Not at hlt
  have hsub : (Icc 1 (n + 1)).filter (fun x => x % 2 = piPar n) ⊆
      (U n).filter (fun x => x % 2 = piPar n) := by
    intro x hx
    simp only [mem_filter, mem_Icc] at hx ⊢
    refine ⟨?_, hx.2⟩
    by_contra hxU
    have := uStar_min hx.1.1 hx.2 hxU
    omega
  have h1 := card_le_card hsub
  rw [card_U_filter_parity] at h1
  unfold piPar at h1
  rw [card_Icc_succ_filter_succ_parity] at h1
  omega

/-- O*(n) ≤ floor(n/2) (from (Cnt); C013 (b) uses this, informally via (b') and u* ≥ 1). -/
theorem Ostar_le_half (n : ℕ) : Ostar n ≤ n / 2 := by
  rw [← card_U_filter_parity]
  exact card_le_card (fun x hx => by
    simp only [mem_filter] at hx ⊢; exact ⟨hx.1, hx.2.1⟩)

/-- Step 0.2 of L006: t_n ≥ 3 (for `n ≥ 1`), since a(n) and u*(n) are ≥ 1 of opposite parity. -/
theorem three_le_tStar {n : ℕ} (hn : 1 ≤ n) : 3 ≤ tStar n := by
  have h1 := a_pos hn
  have h2 := a_mod_two hn
  obtain ⟨hu1, hu2, -⟩ := uStar_spec n
  unfold piPar at hu2
  unfold tStar
  rcases Nat.lt_or_ge (a n) 2 with h | h <;> omega

/-- **L006 (c), interval form, sharp version.** For `n ≥ 1` and `d ≥ 0`: if [t_n, t_n + d]
contains at least O*(n) + 1 primes, then a(n+1) ≤ u*(n) + d. -/
theorem L006_c_interval {n : ℕ} (hn : 1 ≤ n) (d : ℕ)
    (hQ : Ostar n + 1 ≤ ((Icc (tStar n) (tStar n + d)).filter Nat.Prime).card) :
    a (n + 1) ≤ uStar n + d := by
  by_contra hlt
  push Not at hlt
  set Q := (Icc (tStar n) (tStar n + d)).filter Nat.Prime with hQdef
  have hpar := a_mod_two hn
  have ht3 := three_le_tStar hn
  obtain ⟨hu1, hu2, huU⟩ := uStar_spec n
  have hsub : Q.image (fun q => q - a n) ⊆
      (U n).filter (fun x => x % 2 = piPar n ∧ uStar n < x) := by
    intro x hx
    obtain ⟨q, hq, rfl⟩ := mem_image.1 hx
    simp only [hQdef, mem_filter, mem_Icc, tStar] at hq
    obtain ⟨⟨hq1, hq2⟩, hqp⟩ := hq
    have hqodd : q % 2 = 1 := by
      rcases hqp.eq_two_or_odd with h | h
      · unfold tStar at ht3; omega
      · exact h
    have hxpar : (q - a n) % 2 = piPar n := by unfold piPar; omega
    have hxU : q - a n ∈ U n := by
      by_contra hxU
      have := a_succ_min hn (x := q - a n) (by omega) hxU
        (by rw [show a n + (q - a n) = q by omega]; exact hqp)
      omega
    refine mem_filter.2 ⟨hxU, hxpar, ?_⟩
    rcases Nat.lt_or_ge (uStar n) (q - a n) with h | h
    · exact h
    · exfalso
      have : q - a n = uStar n := by omega
      exact huU (this ▸ hxU)
  have hinj : Set.InjOn (fun q => q - a n) (Q : Set ℕ) := by
    intro p hp q hq h
    simp only [hQdef, coe_filter, mem_Icc, Set.mem_ofPred_eq, tStar] at hp hq
    simp only at h
    omega
  have := card_le_card hsub
  rw [card_image_of_injOn hinj] at this
  unfold Ostar at hQ
  omega

/-- **L006 (c), interval form.** For `n ≥ 1` and `d ≥ 0`: if [t_n, t_n + d] contains at least
O*(n) + 1 primes, then a(n+1) - (n+1) ≤ d (stated as `a (n+1) ≤ (n+1) + d`). -/
theorem L006_c {n : ℕ} (hn : 1 ≤ n) (d : ℕ)
    (hQ : Ostar n + 1 ≤ ((Icc (tStar n) (tStar n + d)).filter Nat.Prime).card) :
    a (n + 1) ≤ (n + 1) + d := by
  have := L006_c_interval hn d hQ
  have := L006_b n
  omega

end ErdosWatts
