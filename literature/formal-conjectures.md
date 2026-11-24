# Google DeepMind formal-conjectures (Lean 4) - Erdős #473

## Citation/link

https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/473.lean (read raw from raw.githubusercontent.com, main branch, 2026-11-24). Copyright 2026, Apache 2.0.

## What it says

Two declarations in namespace `Erdos473`, both with `sorry` bodies:

1. `erdos_473`, tagged `research solved, question, AMS 11`, with `formal_proof using lean4 at "https://github.com/plby/lean-proofs/blob/8822f7d.../src/latest/ErdosProblems/Erdos473.lean#L236"`:

       theorem erdos_473 :
           ∃ a : ℕ ≃ ℕ+, ∀ n : ℕ, ((a n : ℕ) + (a (n + 1) : ℕ)).Prime

   The docstring says: "A question of Segal [ErGr80, p.94]. The answer is yes, as shown by Odlyzko." It also says the linked formal proof (Codex and GPT-5.6 Sol) "builds the permutation as a spanning one-way ray of the graph on the positive integers in which two numbers are adjacent when their sum is prime."
2. `erdos_473.variants.finite`, tagged `research open`: for every n >= 2 there is a permutation of {1..n} with adjacent sums prime.

**The file does not mention Watts, a greedy construction, or A055265.** I asked the fetch tool explicitly, and "greedy" does not occur in the file. **The greedy question is not formalized there.**

The erdosproblems database (teorth/erdosproblems, data/problems.yaml) agrees. For #473 it lists `status: proved (2025-08-31)`, `formalized: yes (2026-09-18)`, `oeis: ["A055265"]`, `forum: posts: 3`.

## Relevance

- Our target statement has no canonical formal version. If we formalize it, we would be writing it from scratch. The natural form: define `a` by well-founded recursion and state `Function.Surjective a`.
- The linked machine proof of the main question (an explicit construction, not greedy) is not evidence about the greedy sequence. Not read.

## Verified by

Literature agent, 2026-11-24: **read** the raw 473.lean through the fetch tool. Lean statements were quoted; docstrings were quoted in segments. Also **read** the #473 entry of https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml. Did **not** read the plby/lean-proofs file.
