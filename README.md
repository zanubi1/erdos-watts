# erdos-watts

Working repo for **Watts' greedy question** in [Erdős Problem #473](https://www.erdosproblems.com/473).

## The problem

Define a(1) = 1 and

    a(n+1) = min { x >= 1 : x not in {a(1), ..., a(n)} and a(n) + x is prime }.

**Question (Watts):** does every positive integer occur in this sequence, i.e. is it a permutation of the positive integers?

This is OEIS [A055265](https://oeis.org/A055265):
1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15, 14, 17, 12, 11, 18, 19, 22, ...

## Status - read this before claiming anything

- The **main** question of #473 (does *some* permutation of N with all adjacent sums prime exist?) is **solved**: yes, attributed to Odlyzko. We are not working on that.
- Watts' **greedy** sub-question is open as far as we know: OEIS gives only a probabilistic argument, no proof. The erdosproblems.com page also notes (van Doorn) that not every prime occurs as a sum a(n) + a(n+1) - 197 never does.
- Related finite version (Segal): for every n >= 2, is there a permutation of {1..n} with all adjacent sums prime? Known for infinitely many n; see MathOverflow 241569.
- The analogous greedy question for the EKG sequence (A064413) was settled by Lagarias-Rains-Sloane (2002) - a model for the kind of argument we want.

Literature checking is not finished: see `literature/`.

## Where things are

| Path | What |
|---|---|
| `STRATEGY.md` | current plan and main lines of attack |
| `CLAUDE.md` | working rules for humans and agents |
| `literature/` | one note per source; prior-work checks |
| `lemmas/proven/` | statements that passed skeptic review |
| `lemmas/candidates/` | stated, possibly with a draft proof, not yet reviewed |
| `lemmas/refuted/` | dead statements with the counterexample or the gap |
| `attempts/` | dated proof attempts, including failures |
| `experiments/` | code and result write-ups |
| `lean/` | Lean 4 + Mathlib formalization: the sequence, L001-L005, L009, L011, L012 (no `sorry`), and the Watts conjecture stated with `sorry` |
| `.claude/agents/` | prover, skeptic, literature, experimenter |

## Quick start

    pip install numpy
    python experiments/src/greedy.py --terms 10000000 --out experiments/results/run_1e7

## Lean formalization

    export PATH="$HOME/.elan/bin:$PATH"
    cd lean && lake exe cache get && lake build

- **Toolchain:** Lean 4.36.0 with Mathlib v4.36.0, pinned in `lean/lakefile.toml`.
- **What is formalized:** L001, L002, L003, L004, L005, L009 (with L009' and its corollary), L011 and L012. All of them depend only on the axioms `propext`, `Classical.choice` and `Quot.sound`. The prime number theorem comes from Mathlib (`Nat.isEquivalent_primeCounting`).
- **The conjecture:** `lean/ErdosWatts/Conjecture.lean` states Watts' question as `Function.Bijective aPNat` and is the only `sorry`.
- **More:** conventions are in `lean/README.md`. The agent that does this work is `.claude/agents/formalizer.md`.
