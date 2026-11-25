import ErdosWatts.L004
import ErdosWatts.L009

/-!
# L011 - Unconditional hole-density criterion

Informal (lemmas/proven/L011-unconditional-hole-criterion.md). H(n) = #{x ∈ [1, n] : x ∉ U_n},
H_p(n) the number of such holes of parity p.

**(i)** Suppose v >= 2 never occurs, ε = v mod 2. Then for every n >= v,
`H_{1-ε}(n) >= π(n + v) - π(2v) - H(v)`.

**(ii)** If some value never occurs, then `liminf_{n → ∞} H(n) log n / n >= 1`.
Contrapositive: if `liminf H(n) log n / n < 1`, every positive integer occurs.

## Mapping informal -> formal

* informal a(n) = `a n` for `n ≥ 1`; U_n = `U n`; H(n) = `H n`; H_p(n) = `holes p n`;
  π = `Nat.primeCounting`; log = `Real.log`; "v never occurs" = `¬ Occurs v`;
  "every positive integer occurs" = `∀ v, 1 ≤ v → Occurs v`
  (equivalent to `Function.Bijective aPNat` by `aPNat_bijective_iff`, Conjecture.lean).
* (i) = `L011_i` (ℕ, truncated subtraction, exactly the informal rearrangement) and
  `L011_i_int` (same inequality in ℤ, no truncation). `L011_i_hole` is the stronger version
  noted by the skeptic: it only needs `v ∉ U_n` (v a hole at time n), not "v never occurs".
* (ii), for an *arbitrary* missing `v ≥ 1` (not only the smallest one):
  - `L011_ii_holes`: for every `ε > 0`, eventually `H_{1-(v mod 2)}(n) ≥ (1 - ε) n / log n`
    (one parity class, as the skeptic remarked);
  - `L011_ii`: for every `ε > 0`, eventually `H(n) ≥ (1 - ε) n / log n` (primary form);
  - `L011_ii_ratio`: for every `ε > 0`, eventually `H(n) log n / n ≥ 1 - ε`;
  - `L011_ii_liminf_ereal`: `1 ≤ liminf (H(n) log n / n)` with the liminf taken in `EReal`
    (a complete lattice, so no boundedness side conditions);
  - `L011_ii_liminf`: the same with the liminf in `ℝ`, under the side condition
    `IsCoboundedUnder (· ≥ ·) atTop (H(n) log n / n)`. This side condition is needed because
    `Filter.liminf` in `ℝ` takes the junk value `0` when the sequence tends to `+∞`.
* Contrapositive:
  - `L011_criterion`: if for some `δ > 0`, `H(n) ≤ (1 - δ) n / log n` for infinitely many `n`
    (`∃ᶠ n in atTop`), then every `v ≥ 1` occurs (the usable criterion);
  - `L011_criterion_liminf_ereal`: `liminf (H(n) log n / n) < 1` in `EReal` implies every `v ≥ 1`
    occurs (literally the informal contrapositive, with liminf in the extended reals);
  - `L011_criterion_liminf`: the same with the liminf in `ℝ`, under the coboundedness condition.

The PNT is Mathlib's `Nat.isEquivalent_primeCounting` (via `L004_rhs_isEquivalent` and
`eventually_ge_of_isEquivalent` in L004.lean, which are pure PNT consequences: they do not use
L003 or the L004 bound). No explicit hypotheses.
-/

namespace ErdosWatts

open Filter Asymptotics Topology

/-- A missing positive value is at least 2, since a(1) = 1. -/
theorem two_le_of_not_occurs {v : ℕ} (hv : 1 ≤ v) (hmiss : ¬ Occurs v) : 2 ≤ v := by
  by_contra h
  have : v = 1 := by omega
  exact hmiss ⟨1, le_rfl, by simp [this]⟩

/-- A value that never occurs is not in any `U n`. -/
theorem notMem_U_of_not_occurs {v : ℕ} (hmiss : ¬ Occurs v) (n : ℕ) : v ∉ U n :=
  fun h => hmiss (occurs_of_mem_U h)

/-- **L011 (i), hole form.** If `2 ≤ v ≤ n` and `v ∉ U_n` (v is a hole at time n), then
`H_{1-ε}(n) ≥ π(n + v) - π(2v) - H(v)` with `ε = v mod 2`. -/
theorem L011_i_hole {n v : ℕ} (hv : 2 ≤ v) (hvn : v ≤ n) (hvU : v ∉ U n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) - H v ≤ holes (1 - v % 2) n := by
  have := L009_sharp (by omega) hv hvn hvU
  omega

/-- **L011 (i).** Suppose `v ≥ 2` never occurs, `ε = v mod 2`. Then for every `n ≥ v`,
`H_{1-ε}(n) ≥ π(n + v) - π(2v) - H(v)` (truncated subtraction in ℕ). -/
theorem L011_i {v : ℕ} (hv : 2 ≤ v) (hmiss : ¬ Occurs v) {n : ℕ} (hvn : v ≤ n) :
    Nat.primeCounting (n + v) - Nat.primeCounting (2 * v) - H v ≤ holes (1 - v % 2) n :=
  L011_i_hole hv hvn (notMem_U_of_not_occurs hmiss n)

/-- **L011 (i), in ℤ** (no truncated subtraction). -/
theorem L011_i_int {v : ℕ} (hv : 2 ≤ v) (hmiss : ¬ Occurs v) {n : ℕ} (hvn : v ≤ n) :
    (Nat.primeCounting (n + v) : ℤ) - Nat.primeCounting (2 * v) - H v ≤ holes (1 - v % 2) n := by
  have := L011_i hv hmiss hvn
  omega

/-- **L011 (ii), one parity class.** If `v ≥ 1` never occurs, then for every `ε > 0`, eventually
`H_{1-(v mod 2)}(n) ≥ (1 - ε) n / log n`. -/
theorem L011_ii_holes {v : ℕ} (hv1 : 1 ≤ v) (hmiss : ¬ Occurs v) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n : ℕ in atTop, (1 - ε) * ((n : ℝ) / Real.log n) ≤ holes (1 - v % 2) n := by
  have hv := two_le_of_not_occurs hv1 hmiss
  set N0 : ℕ := Nat.primeCounting (2 * v) - Nat.primeCounting v + H v with hN0
  have hmono : Nat.primeCounting v ≤ Nat.primeCounting (2 * v) :=
    Nat.monotone_primeCounting (by omega)
  have hsum : (Nat.primeCounting v : ℝ) + N0 = Nat.primeCounting (2 * v) + H v := by
    have : Nat.primeCounting v + N0 = Nat.primeCounting (2 * v) + H v := by omega
    exact_mod_cast this
  have hnn : ∀ᶠ n : ℕ in atTop, 0 ≤ (n : ℝ) / Real.log n := by
    filter_upwards [eventually_ge_atTop 1] with n hn
    exact div_nonneg (Nat.cast_nonneg _) (Real.log_nonneg (by exact_mod_cast hn))
  filter_upwards [eventually_ge_of_isEquivalent (L004_rhs_isEquivalent v N0) hnn hε,
    eventually_ge_atTop v] with n hn hvn
  have hi := L011_i hv hmiss hvn
  have hi' : Nat.primeCounting (n + v) ≤ holes (1 - v % 2) n + Nat.primeCounting (2 * v) + H v := by
    omega
  have hi'' : (Nat.primeCounting (n + v) : ℝ) ≤
      holes (1 - v % 2) n + Nat.primeCounting (2 * v) + H v := by exact_mod_cast hi'
  linarith

/-- **L011 (ii), primary form.** If some `v ≥ 1` never occurs, then for every `ε > 0`,
eventually `H(n) ≥ (1 - ε) n / log n`. -/
theorem L011_ii {v : ℕ} (hv1 : 1 ≤ v) (hmiss : ¬ Occurs v) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n : ℕ in atTop, (1 - ε) * ((n : ℝ) / Real.log n) ≤ H n := by
  filter_upwards [L011_ii_holes hv1 hmiss hε] with n hn
  have : holes (1 - v % 2) n ≤ H n := holes_le_H _ _ (by omega)
  have : (holes (1 - v % 2) n : ℝ) ≤ H n := by exact_mod_cast this
  linarith

/-- For `n ≥ 2`: `(1 - ε) n / log n ≤ h` implies `1 - ε ≤ h log n / n`. -/
theorem ratio_of_le {n : ℕ} (hn : 2 ≤ n) {c h : ℝ} (hle : c * ((n : ℝ) / Real.log n) ≤ h) :
    c ≤ h * Real.log n / n := by
  have hn0 : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hlog : 0 < Real.log n := Real.log_pos (by exact_mod_cast (show 1 < n by omega))
  have hpos : 0 ≤ Real.log n / n := div_nonneg hlog.le hn0.le
  have := mul_le_mul_of_nonneg_right hle hpos
  have e1 : c * ((n : ℝ) / Real.log n) * (Real.log n / n) = c := by
    field_simp
  have e2 : h * (Real.log n / n) = h * Real.log n / n := by ring
  linarith

/-- **L011 (ii), ratio form.** If some `v ≥ 1` never occurs, then for every `ε > 0`, eventually
`H(n) log n / n ≥ 1 - ε`. -/
theorem L011_ii_ratio {v : ℕ} (hv1 : 1 ≤ v) (hmiss : ¬ Occurs v) {ε : ℝ} (hε : 0 < ε) :
    ∀ᶠ n : ℕ in atTop, 1 - ε ≤ (H n : ℝ) * Real.log n / n := by
  filter_upwards [L011_ii hv1 hmiss hε, eventually_ge_atTop 2] with n hn h2
  exact ratio_of_le h2 hn

/-- **L011 (ii), liminf form in `EReal`.** If some `v ≥ 1` never occurs, then
`liminf_{n → ∞} H(n) log n / n ≥ 1`, the liminf taken in the extended reals. -/
theorem L011_ii_liminf_ereal {v : ℕ} (hv1 : 1 ≤ v) (hmiss : ¬ Occurs v) :
    (1 : EReal) ≤ liminf (fun n : ℕ => (((H n : ℝ) * Real.log n / n : ℝ) : EReal)) atTop := by
  refine le_of_forall_lt_imp_le_of_dense fun c hc => ?_
  induction c using EReal.rec with
  | bot => exact bot_le
  | top => exact absurd hc (not_lt.2 le_top)
  | coe r =>
    have hr : r < 1 := by exact_mod_cast hc
    refine le_liminf_of_le (by isBoundedDefault) ?_
    filter_upwards [L011_ii_ratio hv1 hmiss (sub_pos.2 hr)] with n hn
    have : r ≤ (H n : ℝ) * Real.log n / n := by linarith
    exact_mod_cast this

/-- **L011 (ii), liminf form in `ℝ`.** If some `v ≥ 1` never occurs, then
`liminf_{n → ∞} H(n) log n / n ≥ 1`, provided the real liminf is meaningful
(`IsCoboundedUnder (· ≥ ·)`, i.e. the sequence does not tend to `+∞`). -/
theorem L011_ii_liminf {v : ℕ} (hv1 : 1 ≤ v) (hmiss : ¬ Occurs v)
    (hcob : IsCoboundedUnder (· ≥ ·) atTop (fun n : ℕ => (H n : ℝ) * Real.log n / n)) :
    (1 : ℝ) ≤ liminf (fun n : ℕ => (H n : ℝ) * Real.log n / n) atTop := by
  refine le_of_forall_lt_imp_le_of_dense fun r hr => ?_
  refine le_liminf_of_le hcob ?_
  filter_upwards [L011_ii_ratio hv1 hmiss (sub_pos.2 hr)] with n hn
  linarith

/-- **L011, contrapositive (usable criterion).** If for some `δ > 0`,
`H(n) ≤ (1 - δ) n / log n` for infinitely many `n`, then every positive integer occurs. -/
theorem L011_criterion {δ : ℝ} (hδ : 0 < δ)
    (hfreq : ∃ᶠ n : ℕ in atTop, (H n : ℝ) ≤ (1 - δ) * ((n : ℝ) / Real.log n)) :
    ∀ v : ℕ, 1 ≤ v → Occurs v := by
  intro v hv1
  by_contra hmiss
  have hev := L011_ii hv1 hmiss (half_pos hδ)
  obtain ⟨n, ⟨h1, h2⟩, hn2⟩ := ((hfreq.and_eventually hev).and_eventually
    (eventually_ge_atTop 2)).exists
  have hn0 : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hlog : 0 < Real.log n := Real.log_pos (by exact_mod_cast (show 1 < n by omega))
  have hx : 0 < (n : ℝ) / Real.log n := div_pos hn0 hlog
  nlinarith

/-- **L011, contrapositive, liminf form in `EReal`.** If `liminf H(n) log n / n < 1` (in the
extended reals), then every positive integer occurs. -/
theorem L011_criterion_liminf_ereal
    (h : liminf (fun n : ℕ => (((H n : ℝ) * Real.log n / n : ℝ) : EReal)) atTop < 1) :
    ∀ v : ℕ, 1 ≤ v → Occurs v := by
  intro v hv1
  by_contra hmiss
  exact absurd (L011_ii_liminf_ereal hv1 hmiss) (not_le.2 h)

/-- **L011, contrapositive, liminf form in `ℝ`.** If the real liminf of `H(n) log n / n` is
meaningful (coboundedness) and `< 1`, then every positive integer occurs. -/
theorem L011_criterion_liminf
    (hcob : IsCoboundedUnder (· ≥ ·) atTop (fun n : ℕ => (H n : ℝ) * Real.log n / n))
    (h : liminf (fun n : ℕ => (H n : ℝ) * Real.log n / n) atTop < 1) :
    ∀ v : ℕ, 1 ≤ v → Occurs v := by
  intro v hv1
  by_contra hmiss
  exact absurd (L011_ii_liminf hv1 hmiss hcob) (not_le.2 h)

end ErdosWatts
