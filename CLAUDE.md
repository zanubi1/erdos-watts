# Working rules

This repo is an attempt to prove (or disprove) that the Watts greedy sequence (OEIS A055265) is a permutation of the positive integers. See README.md for the problem, STRATEGY.md for the plan.

The human collaborator is Matteo, a mathematician (somewhat rusty) and data engineer. He is the final referee on every proof. Write in English in the repo; chat with him in whichever language he uses.

## Ground rules

1. **No claim without review.** A lemma moves from `lemmas/candidates/` to `lemmas/proven/` only after a skeptic pass that found no gap, recorded in the lemma file, and Matteo's OK. Trivial setup lemmas are marked as such.
2. **Never delete a dead idea.** Refuted statements go to `lemmas/refuted/` with the counterexample or the exact gap. Failed attempts stay in `attempts/` with a "why it died" section.
3. **Literature before novelty.** Before calling anything new, run the literature agent on it. Many "open" Erdős problems turned out to be solved somewhere obscure. Also beware of reproducing a known argument from memory without citing it.
4. **Data before proofs.** If a candidate lemma is numerically checkable, the experimenter checks it first (to at least 10^7 terms).
5. **Precision over fluency.** A proof sketch that "clearly works" is not a proof. State every quantifier. Mark any step you are not sure about with `GAP?`.
6. **Keep STRATEGY.md current.** After any meaningful result, update it: what changed, what is now the bottleneck.

## File conventions

- Lemmas: `lemmas/<status>/L###-short-name.md` (proven) or `C###-short-name.md` (candidates) or `R###-short-name.md` (refuted). Sections: Statement, Depends on, Proof (or draft), Numerical check, Review log.
- Attempts: `attempts/YYYY-MM-DD-short-name.md`. Sections: Goal, Idea, Work, Outcome, Why it died / what survives.
- Literature: `literature/<author-year-or-site>.md`. Sections: Citation/link, What it says, Relevance, Verified by (who actually read the source).
- Experiments: code in `experiments/src/`, write-ups in `experiments/results/<run>/summary.md`. Large binary outputs (`*.npy`) are gitignored - regenerate them.

## Agents (in `.claude/agents/`)

- **prover** - attacks one named candidate lemma; writes an attempt file.
- **skeptic** - reviews a proof adversarially, hunts counterexamples. Should be given only the statement and the final proof, not the prover's scratch work.
- **literature** - searches for prior work on a statement before we claim it.
- **experimenter** - turns a conjecture into code and data.

Typical loop: experimenter (is it true numerically?) -> literature (is it known?) -> prover (prove it) -> skeptic (break it) -> Matteo (accept) -> move to `proven/`, update STRATEGY.md.
