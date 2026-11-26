import ErdosWatts.Defs

/-!
# L002 - The sequence is well defined

Informal (lemmas/proven/L002-well-defined.md): for every n, the set
{ x >= 1 : x ∉ {a(1..n)} and a(n) + x prime } is nonempty, so a(n+1) exists.

Formal: `(A n).Nonempty` for every `n ≥ 1`, where `A n` is that set (`ErdosWatts.A`).
The construction in `Defs.lean` already needs this fact (`exists_next`), so here it is only
restated. The formal statement also holds for `n = 0` (junk `a 0 = 0`, `U 0 = ∅`), but `n = 0` is
not part of the informal statement, which only concerns actual terms.
-/

namespace ErdosWatts

/-- **L002.** For every `n ≥ 1` (informal a(n) = `a n`), the candidate set
`A n = { x ≥ 1 : x ∉ U n, a n + x prime }` is nonempty. Proof as in the informal note: a prime
`p ≥ a n + max (U n) + 1` gives the candidate `p - a n` (see `exists_next`). -/
theorem L002_wellDefined (n : ℕ) (_hn : 1 ≤ n) : (A n).Nonempty :=
  exists_next (a n) (U n)

/-- Restatement: for `n ≥ 1`, `a (n+1)` is the minimum of the nonempty set `A n`. -/
theorem L002_a_succ_eq_sInf {n : ℕ} (hn : 1 ≤ n) : a (n + 1) = sInf (A n) :=
  ((a_succ_isLeast hn).csInf_eq).symm

end ErdosWatts
