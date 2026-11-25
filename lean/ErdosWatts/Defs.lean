import Mathlib

/-!
# Shared definitions for the Watts greedy sequence (OEIS A055265)

Informal definition (README.md): a(1) = 1, and

    a(n+1) = min { x >= 1 : x ∉ {a(1), ..., a(n)} and a(n) + x is prime }.

## Conventions (reuse these in every lemma file)

* **Indexing.** `a : ℕ → ℕ` is 1-indexed: the informal a(n) is `a n` for `n ≥ 1`, and `a 1 = 1`.
  The value `a 0 = 0` is junk (it is not a term of the sequence). Lemmas about terms carry the
  hypothesis `1 ≤ n`.
* **Used set.** `U n` is the `Finset` {a(1), ..., a(n)}, defined as `(Finset.Icc 1 n).image a`.
  In particular `U 0 = ∅` (as in L009's conventions), and `a 0` never enters any `U n`.
* **Candidate set.** `A n` is the `Set` { x ≥ 1 : x ∉ U n, a n + x prime } (L009's A_n).
  For `n ≥ 1`, `a (n+1)` is the least element of `A n` (`a_succ_isLeast`).
* **First index.** `Occurs v` means `∃ k ≥ 1, a k = v`; `fi v h` (with `h : Occurs v`) is the
  least such `k`, which is the unique such `k` by injectivity (`fi_unique`). "fi(v) = ∞" is
  expressed as `¬ Occurs v`, and "fi(v) ≤ n" as `v ∈ U n` (`mem_U_iff_fi_le`).
* **Parity.** "parity p" means `x % 2 = p` with `p ∈ {0, 1}`.
* **Holes.** `holes p m` is H_p(m) = #{ x ∈ [1, m] : x % 2 = p, x ∉ U m }; `H m = holes 0 m + holes 1 m`;
  `B v` = #{ x ∈ [1, v) : x % 2 = v % 2, x ∉ U v } (L009's B(v); note x ≥ 1 is explicit).

## Construction

The sequence is produced by iterating a step on a state `(last term, used set)`. The next term is
`Nat.find` of `exists_next`, which is the content of L002 (a prime `p ≥ last + max used + 1` gives
the candidate `p - last`). Everything is computable, so `#eval a 12` works.
-/

namespace ErdosWatts

/-- The predicate "x is an admissible next term after last term `l` with used set `s`":
`x ≥ 1`, `x ∉ s`, and `l + x` is prime. -/
def Admissible (l : ℕ) (s : Finset ℕ) (x : ℕ) : Prop :=
  1 ≤ x ∧ x ∉ s ∧ (l + x).Prime

instance (l : ℕ) (s : Finset ℕ) : DecidablePred (Admissible l s) := fun x => by
  unfold Admissible; infer_instance

/-- **Existence of a next term** (the content of L002): for any last term `l` and any finite used
set `s`, some `x ≥ 1` outside `s` has `l + x` prime. Take a prime `p ≥ l + max s + 1`, `x = p - l`. -/
theorem exists_next (l : ℕ) (s : Finset ℕ) : ∃ x, Admissible l s x := by
  obtain ⟨p, hp, hpr⟩ := Nat.exists_infinite_primes (l + s.sup id + 1)
  refine ⟨p - l, ?_, ?_, ?_⟩
  · omega
  · intro hx
    have : id (p - l) ≤ s.sup id := Finset.le_sup (f := id) hx
    simp only [id] at this
    omega
  · have : l + (p - l) = p := by omega
    rw [this]; exact hpr

/-- One greedy step on the state `(last term, used set)`. -/
def nextState (st : ℕ × Finset ℕ) : ℕ × Finset ℕ :=
  (Nat.find (exists_next st.1 st.2), insert (Nat.find (exists_next st.1 st.2)) st.2)

/-- `state n = (a n, U n)` for `n ≥ 1` (see `a`, `state_snd`); `state 0 = (0, ∅)`. -/
def state : ℕ → ℕ × Finset ℕ
  | 0 => (0, ∅)
  | 1 => (1, {1})
  | n + 2 => nextState (state (n + 1))

/-- **The Watts greedy sequence** (OEIS A055265), 1-indexed: informal a(n) = `a n` for `n ≥ 1`.
`a 0 = 0` is a junk value, not a term. -/
def a (n : ℕ) : ℕ := (state n).1

/-- The used set U_n = {a(1), ..., a(n)} (with U_0 = ∅). -/
def U (n : ℕ) : Finset ℕ := (Finset.Icc 1 n).image a

/-- L009's candidate set A_n = { x ≥ 1 : x ∉ U_n, a(n) + x prime }. -/
def A (n : ℕ) : Set ℕ := {x | 1 ≤ x ∧ x ∉ U n ∧ (a n + x).Prime}

@[simp] theorem a_zero : a 0 = 0 := rfl
@[simp] theorem a_one : a 1 = 1 := rfl

theorem mem_U {n x : ℕ} : x ∈ U n ↔ ∃ k, 1 ≤ k ∧ k ≤ n ∧ a k = x := by
  simp [U, and_assoc]

@[simp] theorem U_zero : U 0 = ∅ := by
  ext x; simp [mem_U]

theorem U_succ (n : ℕ) : U (n + 1) = insert (a (n + 1)) (U n) := by
  ext x
  simp only [mem_U, Finset.mem_insert]
  constructor
  · rintro ⟨k, hk1, hk2, rfl⟩
    rcases Nat.lt_or_ge k (n + 1) with h | h
    · exact Or.inr ⟨k, hk1, by omega, rfl⟩
    · left; rw [show k = n + 1 by omega]
  · rintro (rfl | ⟨k, hk1, hk2, rfl⟩)
    · exact ⟨n + 1, by omega, le_rfl, rfl⟩
    · exact ⟨k, hk1, by omega, rfl⟩

@[simp] theorem U_one : U 1 = {1} := by
  rw [U_succ, U_zero]; rfl

/-- The used-set component of the internal state is `U n`. -/
theorem state_snd (n : ℕ) : (state n).2 = U n := by
  induction n with
  | zero => simp [state]
  | succ n ih =>
    rcases n with _ | n
    · simp [state]
    · rw [U_succ, ← ih]; rfl

theorem mem_U_self {k n : ℕ} (hk : 1 ≤ k) (hkn : k ≤ n) : a k ∈ U n :=
  mem_U.2 ⟨k, hk, hkn, rfl⟩

/-- U is monotone (L009 F3, first half). -/
theorem U_mono {j k : ℕ} (h : j ≤ k) : U j ⊆ U k := by
  intro x hx
  obtain ⟨i, hi1, hi2, rfl⟩ := mem_U.1 hx
  exact mem_U_self hi1 (hi2.trans h)

/-- For `n ≥ 1`, `a (n+1)` is `Nat.find` of the existence statement for state `n`. -/
theorem a_succ_eq_find {n : ℕ} (hn : 1 ≤ n) :
    a (n + 1) = Nat.find (exists_next (a n) (U n)) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  show (nextState (state (m + 1))).1 = _
  simp only [nextState]
  rw [← state_snd]; rfl

/-- **Defining property, part 1.** For `n ≥ 1`: `a (n+1) ≥ 1`, `a (n+1) ∉ U n`, and
`a n + a (n+1)` is prime. -/
theorem a_succ_spec {n : ℕ} (hn : 1 ≤ n) :
    1 ≤ a (n + 1) ∧ a (n + 1) ∉ U n ∧ (a n + a (n + 1)).Prime := by
  rw [a_succ_eq_find hn]
  exact Nat.find_spec (exists_next (a n) (U n))

/-- **Defining property, part 2 (minimality).** For `n ≥ 1`, any `x ≥ 1` with `x ∉ U n` and
`a n + x` prime satisfies `a (n+1) ≤ x`. -/
theorem a_succ_min {n : ℕ} (hn : 1 ≤ n) {x : ℕ} (hx : 1 ≤ x) (hxU : x ∉ U n)
    (hp : (a n + x).Prime) : a (n + 1) ≤ x := by
  rw [a_succ_eq_find hn]
  exact Nat.find_min' (exists_next (a n) (U n)) ⟨hx, hxU, hp⟩

/-- Computation step: if `a n = l`, `U n = s` and `x` is the least admissible value for `(l, s)`,
then `a (n+1) = x` and `U (n+1) = insert x s`. Used to verify concrete terms with `decide`. -/
theorem step_of_least {n l x : ℕ} {s : Finset ℕ} (hn : 1 ≤ n) (h : a n = l ∧ U n = s)
    (hx : Admissible l s x ∧ ∀ y < x, ¬ Admissible l s y) :
    a (n + 1) = x ∧ U (n + 1) = insert x s := by
  obtain ⟨rfl, rfl⟩ := h
  have hax : a (n + 1) = x := by
    rw [a_succ_eq_find hn, Nat.find_eq_iff]
    exact hx
  exact ⟨hax, by rw [U_succ, hax]⟩

/-- For `n ≥ 1`, `a (n+1) = min A n`. -/
theorem a_succ_isLeast {n : ℕ} (hn : 1 ≤ n) : IsLeast (A n) (a (n + 1)) :=
  ⟨a_succ_spec hn, fun _ hx => a_succ_min hn hx.1 hx.2.1 hx.2.2⟩

/-- Positivity: `a n ≥ 1` for `n ≥ 1`. -/
theorem a_pos {n : ℕ} (hn : 1 ≤ n) : 1 ≤ a n := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  rcases m with _ | m
  · simp
  · exact (a_succ_spec (by omega)).1

theorem zero_notMem_U (n : ℕ) : 0 ∉ U n := by
  intro h
  obtain ⟨k, hk1, -, hk⟩ := mem_U.1 h
  have := a_pos hk1; omega

/-- Injectivity, ordered form (L009 F2): `a j ≠ a k` for `1 ≤ j < k`. -/
theorem a_ne_of_lt {j k : ℕ} (hj : 1 ≤ j) (hjk : j < k) : a j ≠ a k := by
  obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
  intro h
  have hmem : a j ∈ U m := mem_U_self hj (by omega)
  exact (a_succ_spec (by omega : 1 ≤ m)).2.1 (h ▸ hmem)

/-- **Injectivity (L009 F2).** For `i, j ≥ 1`, `a i = a j → i = j`. -/
theorem a_inj {i j : ℕ} (hi : 1 ≤ i) (hj : 1 ≤ j) (h : a i = a j) : i = j := by
  rcases lt_trichotomy i j with hij | hij | hij
  · exact absurd h (a_ne_of_lt hi hij)
  · exact hij
  · exact absurd h.symm (a_ne_of_lt hj hij)

/-- `a` is injective on the positive indices. -/
theorem a_injOn : Set.InjOn a {n | 1 ≤ n} := fun _ hi _ hj h => a_inj hi hj h

/-- For `k ≥ 1`: `a k ∈ U n ↔ k ≤ n`. -/
theorem a_mem_U_iff {k n : ℕ} (hk : 1 ≤ k) : a k ∈ U n ↔ k ≤ n := by
  constructor
  · intro h
    obtain ⟨i, hi1, hi2, hi⟩ := mem_U.1 h
    have := a_inj hi1 hk hi; omega
  · exact mem_U_self hk

/-- `U n` has exactly `n` elements. -/
theorem card_U (n : ℕ) : (U n).card = n := by
  rw [U, Finset.card_image_of_injOn (fun i hi j hj h => a_inj
    (Finset.mem_Icc.1 hi).1 (Finset.mem_Icc.1 hj).1 h)]
  simp

/-! ### First index -/

/-- `Occurs v`: the value `v` is a term of the sequence, i.e. `a k = v` for some `k ≥ 1`. -/
def Occurs (v : ℕ) : Prop := ∃ k, 1 ≤ k ∧ a k = v

/-- The first index fi(v) of an occurring value `v` (L009: "the unique k with a(k) = v").
Informal fi(v) = ∞ corresponds to `¬ Occurs v`. -/
def fi (v : ℕ) (h : Occurs v) : ℕ := Nat.find h

theorem one_le_fi {v : ℕ} (h : Occurs v) : 1 ≤ fi v h := (Nat.find_spec h).1

@[simp] theorem a_fi {v : ℕ} (h : Occurs v) : a (fi v h) = v := (Nat.find_spec h).2

/-- fi(v) is the unique index `k ≥ 1` with `a k = v`. -/
theorem fi_unique {v k : ℕ} (h : Occurs v) (hk : 1 ≤ k) (hak : a k = v) : fi v h = k :=
  a_inj (one_le_fi h) hk (by rw [a_fi, hak])

theorem occurs_a {k : ℕ} (hk : 1 ≤ k) : Occurs (a k) := ⟨k, hk, rfl⟩

@[simp] theorem fi_a {k : ℕ} (hk : 1 ≤ k) : fi (a k) (occurs_a hk) = k :=
  fi_unique _ hk rfl

/-- L009 F3, second half: `x ∈ U n ↔ fi(x) ≤ n` (with fi(x) = ∞ when `x` never occurs). -/
theorem mem_U_iff_fi_le {x n : ℕ} : x ∈ U n ↔ ∃ h : Occurs x, fi x h ≤ n := by
  constructor
  · intro hx
    obtain ⟨k, hk1, hk2, rfl⟩ := mem_U.1 hx
    exact ⟨occurs_a hk1, by rw [fi_a hk1]; exact hk2⟩
  · rintro ⟨h, hle⟩
    rw [← a_fi h]
    exact mem_U_self (one_le_fi h) hle

theorem occurs_of_mem_U {x n : ℕ} (hx : x ∈ U n) : Occurs x :=
  (mem_U_iff_fi_le.1 hx).1

/-! ### Holes -/

/-- H_p(m) = #{ x ∈ [1, m] : x ≡ p (mod 2), x ∉ U_m }: the number of holes of parity `p`
at time `m` (L009). Meaningful for `p ∈ {0, 1}` (it is `0` for `p ≥ 2`). -/
def holes (p m : ℕ) : ℕ :=
  ((Finset.Icc 1 m).filter (fun x => x % 2 = p ∧ x ∉ U m)).card

/-- H(m) = H_0(m) + H_1(m): the total number of holes at time `m`, i.e. #{ x ∈ [1, m] : x ∉ U_m }. -/
def H (m : ℕ) : ℕ := holes 0 m + holes 1 m

/-- B(v) = #{ x ∈ [1, v) : x ≡ v (mod 2), x ∉ U_v }: smaller same-parity holes at time `v`
(L009). The informal "x < v" ranges over positive integers; the bound `1 ≤ x` is explicit here
(it matters: `0` is never in `U v`). -/
def B (v : ℕ) : ℕ :=
  ((Finset.Ico 1 v).filter (fun x => x % 2 = v % 2 ∧ x ∉ U v)).card

end ErdosWatts
