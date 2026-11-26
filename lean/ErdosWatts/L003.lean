import ErdosWatts.Defs

/-!
# L003 - The smallest missing value blocks a translate of the primes

Informal (lemmas/proven/L003-smallest-missing.md): suppose some positive integer never occurs in
the sequence, and let m be the smallest such. Then there is N0 such that for every n >= N0 with
a(n) of parity opposite to m, the number a(n) + m is composite.

## Mapping informal -> formal

* informal a(n) = `a n` for `n ≥ 1` (see `Defs.lean`); "v never occurs" = `¬ Occurs v`.
* The missing set M = { v ≥ 1 : v never occurs } is `missingSet` (defined here, not in `Defs.lean`).
* "m is the smallest positive integer that never occurs" = `IsLeast missingSet m`.
* "n >= N0" ranges over term indices, so the formal statement quantifies over `n` with
  `N0 ≤ n` and `1 ≤ n`. We additionally return `1 ≤ N0`, so `1 ≤ n` is in fact implied.
* "parity opposite to m" = `a n % 2 ≠ m % 2`.
* "a(n) + m is composite" = `¬ (a n + m).Prime`. (Since `a n ≥ 1` and `m ≥ 2`, `a n + m ≥ 3`,
  so "not prime" is the same as "composite"; we also prove `2 ≤ m`, see `two_le_of_mem_missingSet`.)

The proof, as the informal note observes, does not use the parity hypothesis; we also prove
the stronger all-parity version `L003_smallestMissing_all`, and derive `L003_smallestMissing`
from it.
-/

namespace ErdosWatts

/-- The missing set M = { v ≥ 1 : v never occurs in the sequence } (L003, L004, L005). -/
def missingSet : Set ℕ := {v | 1 ≤ v ∧ ¬ Occurs v}

theorem mem_missingSet {v : ℕ} : v ∈ missingSet ↔ 1 ≤ v ∧ ¬ Occurs v := Iff.rfl

/-- `1 = a 1` occurs, so every missing value is at least `2`. -/
theorem two_le_of_mem_missingSet {v : ℕ} (hv : v ∈ missingSet) : 2 ≤ v := by
  obtain ⟨hv1, hvo⟩ := hv
  by_contra h
  have : v = 1 := by omega
  exact hvo ⟨1, le_rfl, by simp [this]⟩

/-- Step 1 of the proof: if every value `1 ≤ x < m` occurs, there is `N0 ≥ 1` such that
`[1, m-1] ⊆ U n` for all `n ≥ N0`. (N0 exceeds all first indices of the values `< m`.) -/
theorem exists_N0_lower_used {m : ℕ} (h : ∀ x, 1 ≤ x → x < m → Occurs x) :
    ∃ N0, 1 ≤ N0 ∧ ∀ n, N0 ≤ n → ∀ x, 1 ≤ x → x < m → x ∈ U n := by
  classical
  -- N0 = 1 + ∑_{x ∈ [1, m)} fi(x) (a crude but valid upper bound for the maximum).
  let g : ℕ → ℕ := fun x => if hx : 1 ≤ x ∧ x < m then fi x (h x hx.1 hx.2) else 0
  refine ⟨1 + ∑ x ∈ Finset.Ico 1 m, g x, by omega, ?_⟩
  intro n hn x hx1 hxm
  have hmem : x ∈ Finset.Ico 1 m := Finset.mem_Ico.2 ⟨hx1, hxm⟩
  have hle : g x ≤ ∑ y ∈ Finset.Ico 1 m, g y :=
    Finset.single_le_sum (f := g) (fun _ _ => Nat.zero_le _) hmem
  have hgx : g x = fi x (h x hx1 hxm) := by simp [g, hx1, hxm]
  exact mem_U_iff_fi_le.2 ⟨h x hx1 hxm, by omega⟩

/-- Step 2 of the proof: if `[1, m-1] ⊆ U n`, `m` never occurs, `m ≥ 1` and `n ≥ 1`, then
`a n + m` is not prime (otherwise `a (n+1) = m`). -/
theorem not_prime_of_lower_used {m n : ℕ} (hn : 1 ≤ n) (hm : m ∈ missingSet)
    (hlow : ∀ x, 1 ≤ x → x < m → x ∈ U n) : ¬ (a n + m).Prime := by
  intro hp
  have hmU : m ∉ U n := fun hU => hm.2 (occurs_of_mem_U hU)
  -- m ∈ A n, so a (n+1) ≤ m.
  have hle : a (n + 1) ≤ m := a_succ_min hn hm.1 hmU hp
  obtain ⟨h1, hnotU, -⟩ := a_succ_spec hn
  rcases Nat.lt_or_ge (a (n + 1)) m with hlt | hge
  · exact hnotU (hlow _ h1 hlt)
  · have : a (n + 1) = m := le_antisymm hle hge
    exact hm.2 ⟨n + 1, by omega, this⟩

/-- **L003, all-parity form** (what the proof actually shows). If `m` is the least positive
integer that never occurs, there is `N0 ≥ 1` such that `a n + m` is not prime for every `n ≥ N0`. -/
theorem L003_smallestMissing_all {m : ℕ} (hm : IsLeast missingSet m) :
    ∃ N0, 1 ≤ N0 ∧ ∀ n, N0 ≤ n → ¬ (a n + m).Prime := by
  have hocc : ∀ x, 1 ≤ x → x < m → Occurs x := by
    intro x hx1 hxm
    by_contra hx
    have := hm.2 ⟨hx1, hx⟩
    omega
  obtain ⟨N0, hN0, hlow⟩ := exists_N0_lower_used hocc
  exact ⟨N0, hN0, fun n hn => not_prime_of_lower_used (by omega) hm.1 (hlow n hn)⟩

/-- **L003 (as stated).** Informal: suppose some positive integer never occurs, and let m be the
smallest such (`IsLeast missingSet m`). Then there is N0 (here `N0 ≥ 1`) such that for every
`n ≥ N0` (a term index, `1 ≤ n`) with a(n) of parity opposite to m (`a n % 2 ≠ m % 2`), the number
a(n) + m (`a n + m`) is composite (`¬ (a n + m).Prime`; note `a n + m ≥ 3`). -/
theorem L003_smallestMissing {m : ℕ} (hm : IsLeast missingSet m) :
    ∃ N0, 1 ≤ N0 ∧ ∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 → ¬ (a n + m).Prime := by
  obtain ⟨N0, hN0, h⟩ := L003_smallestMissing_all hm
  exact ⟨N0, hN0, fun n hn _ _ => h n hn⟩

/-- "Composite" form: under the hypotheses of L003, for `n ≥ N0`, `a n + m` is at least `3` and not
prime (hence composite in the usual sense). -/
theorem L003_smallestMissing_composite {m : ℕ} (hm : IsLeast missingSet m) :
    ∃ N0, 1 ≤ N0 ∧ ∀ n, N0 ≤ n → 1 ≤ n → a n % 2 ≠ m % 2 →
      3 ≤ a n + m ∧ ¬ (a n + m).Prime := by
  obtain ⟨N0, hN0, h⟩ := L003_smallestMissing hm
  refine ⟨N0, hN0, fun n hn hn1 hpar => ⟨?_, h n hn hn1 hpar⟩⟩
  have := a_pos hn1
  have := two_le_of_mem_missingSet hm.1
  omega

end ErdosWatts
