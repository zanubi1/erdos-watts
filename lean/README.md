# Lean formalization

Lean 4 + Mathlib (pinned in `lakefile.toml` / `lean-toolchain`, currently v4.36.0).

    export PATH="$HOME/.elan/bin:$PATH"
    cd lean && lake build          # never build Mathlib from source; use `lake exe cache get`

The formalizer agent's rules are in `../.claude/agents/formalizer.md`. One file per lemma
(`ErdosWatts/L###.lean`), each imported from `ErdosWatts.lean`. No `sorry` and no `axiom`
anywhere, except the single intentional `sorry` in `ErdosWatts/Conjecture.lean`.

## Files

| File | Content |
|---|---|
| `ErdosWatts/Defs.lean` | the sequence `a` and all shared notions (below), injectivity, positivity, fi |
| `ErdosWatts/L001.lean` | L001 parity (`L001_parity`) and F1 `a n % 2 = n % 2` (`a_mod_two`) |
| `ErdosWatts/L002.lean` | L002 well-definedness (`L002_wellDefined`) |
| `ErdosWatts/Conjecture.lean` | Watts' question (`watts_greedy_bijective`, `sorry`), sanity check of the first 12 terms |

`lean/scratch/` (if present) is not built; put unfinished work there.

## Conventions in `Defs.lean` - reuse them, never redefine the sequence

Everything is in `namespace ErdosWatts`.

- **Indexing.** `a : ℕ → ℕ` is 1-indexed: informal a(n) is `a n` for `n ≥ 1`, `a 1 = 1`.
  `a 0 = 0` is a junk value, not a term. Statements about terms carry `1 ≤ n`.
- **Construction.** `state : ℕ → ℕ × Finset ℕ` with `state 0 = (0, ∅)`, `state 1 = (1, {1})`,
  `state (n+2) = nextState (state (n+1))`, where `nextState` takes
  `Nat.find (exists_next last used)`. `exists_next` is L002's argument
  (`Nat.exists_infinite_primes`). `a n := (state n).1`. Computable: `#eval a 20` works.
  Do not reason about `state` directly; use the API lemmas below.
- **Used set.** `U n : Finset ℕ := (Finset.Icc 1 n).image a` = {a(1), ..., a(n)}, `U 0 = ∅`.
  (`state_snd : (state n).2 = U n`.) Lemmas: `mem_U`, `U_succ` (`U (n+1) = insert (a (n+1)) (U n)`),
  `U_mono`, `mem_U_self`, `a_mem_U_iff` (`a k ∈ U n ↔ k ≤ n` for `k ≥ 1`), `card_U`, `zero_notMem_U`.
- **Candidate set.** `Admissible l s x := 1 ≤ x ∧ x ∉ s ∧ (l + x).Prime` (decidable);
  `A n : Set ℕ := {x | 1 ≤ x ∧ x ∉ U n ∧ (a n + x).Prime}` (L009's A_n).
- **Defining property** (for `1 ≤ n`): `a_succ_spec` (`1 ≤ a (n+1) ∧ a (n+1) ∉ U n ∧ (a n + a (n+1)).Prime`),
  `a_succ_min` (any such `x` has `a (n+1) ≤ x`), `a_succ_isLeast : IsLeast (A n) (a (n+1))`,
  `a_succ_eq_find`. For concrete values use `step_of_least` + `decide` (see `a_first_terms`).
- **Basic facts.** `a_pos` (`1 ≤ a n` for `1 ≤ n`), `a_ne_of_lt` / `a_inj` / `a_injOn` (L009 F2).
- **First index.** `Occurs v : Prop := ∃ k, 1 ≤ k ∧ a k = v`; `fi v (h : Occurs v) : ℕ := Nat.find h`.
  Informal "fi(v) = ∞" is `¬ Occurs v`. Lemmas: `one_le_fi`, `a_fi`, `fi_unique`, `fi_a`,
  `occurs_a`, `mem_U_iff_fi_le` (`x ∈ U n ↔ ∃ h : Occurs x, fi x h ≤ n`, L009 F3), `occurs_of_mem_U`.
- **Parity.** "parity p" is `x % 2 = p` with `p ∈ {0, 1}`.
- **Holes.** `holes p m := #{x ∈ Icc 1 m | x % 2 = p ∧ x ∉ U m}` (H_p(m)), `H m := holes 0 m + holes 1 m`,
  `B v := #{x ∈ Ico 1 v | x % 2 = v % 2 ∧ x ∉ U v}` (L009's B(v); the bound `x ≥ 1` is explicit,
  since `0 ∉ U v` would otherwise be counted).
- **Conjecture.** `aPNat : ℕ+ → ℕ+` (`n ↦ a n`); `aPNat_injective` (proved),
  `aPNat_bijective_iff : Bijective aPNat ↔ ∀ v ≥ 1, Occurs v` (proved),
  `watts_greedy_bijective : Bijective aPNat` (`sorry`, research open).
